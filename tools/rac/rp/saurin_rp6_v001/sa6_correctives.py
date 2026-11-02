# sa6_correctives.py : Saurin RP6 bounded pose-space corrective shapes (order a407015 §8-§10).
#   A corrective FAMILY = one joint degree of freedom (bone, local axis).  Its driver = the swing-twist TWIST angle of the bone's LOCAL rotation
#   (R_parent^T R_bone) about that axis -- read from the posed armature only (never from the pose name).  A family holds signed angle samples
#   s_1 < ... < s_n with rest-space vertex deltas; the implicit sample 0 has delta 0.  Activation = piecewise-linear hat interpolation over the samples,
#   held at the outermost sample (bounded: never extrapolated).  Neutral (all twists 0) -> every key 0 -> the neutral mesh is untouched exactly.
#   Shape-key semantics = Blender / UE morph-before-skinning: posed = sum_b w_b (R_b (v + d) + t_b).
#   SOLVER (per pose / fraction): current = LBS + existing correctives; region = vertices whose bone blend is non-rigid (rotation spread) or that
#   touch a flipped quad, dilated 3 rings; boundary ring held at current; interior solved by ARAP (uniform quad-edge + diagonal weights, rotations
#   initialised to the polar factor of the blended LBS matrix, 12 local/global iterations).  Posed residual -> rest delta d = M_v^-1 (P* - P_cur)
#   (M_v = sum w_b R_b, exact inverse of the shape-key-through-LBS map) -> added to the sample of the family whose pivot is nearest the vertex.
import sys, os, json, numpy as np, scipy.sparse as sp, scipy.sparse.linalg as spl
from scipy.spatial.transform import Rotation as Rot
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
def twist(R, a):
    q = Rot.from_matrix(R).as_quat(); a = np.asarray(a, float); a = a / np.linalg.norm(a); t = 2 * np.degrees(np.arctan2(q[:3] @ a, q[3]))
    return (t + 180) % 360 - 180
def fam_key(b, ax): ax = np.asarray(ax, float); ax = ax / np.linalg.norm(ax); return b + '|' + ','.join('%.5f' % x for x in ax)
class Correctives:
    def __init__(self, rig, snap=4.0): self.r = rig; self.F = {}; self.snap = snap; self.PK = {}          # key -> dict(bone, axis, pivot, samples[list], D[list of (idx, delta)])
    def driver(self, T, f):
        p = self.r.par[f['bone']]; R = T[f['bone']][0]; Rp = T[p][0] if p else np.eye(3); return twist(Rp.T @ R, f['axis'])
    def hat(self, s, x):
        """weights over samples s (sorted, implicit 0) at driver x -> list of (k, w)"""
        pts = sorted([(v, k) for k, v in enumerate(s)] + [(0.0, -1)]); xs = [p[0] for p in pts]
        if x <= xs[0]: return [(pts[0][1], 1.0)] if pts[0][1] >= 0 else []
        if x >= xs[-1]: return [(pts[-1][1], 1.0)] if pts[-1][1] >= 0 else []
        i = np.searchsorted(xs, x) - 1; t = (x - xs[i]) / (xs[i + 1] - xs[i]); out = []
        if pts[i][1] >= 0 and t < 1: out.append((pts[i][1], 1 - t))
        if pts[i + 1][1] >= 0 and t > 0: out.append((pts[i + 1][1], t))
        return out
    def delta(self, T, detail=False):
        d = np.zeros_like(self.r.V); act = {}
        for key, f in self.F.items():
            x = self.driver(T, f); ws = self.hat(f['samples'], x)
            for k, w in ws:
                idx, dd = f['D'][k]; d[idx] += w * dd
            act[key] = (x, ws)
        for name, pk in self.PK.items():                       # pose keys: product of per-joint tents (exactly 0 when any driving joint is at rest)
            w = self.pk_weight(T, pk)
            if w > 0: d[pk['idx']] += w * pk['d']
            act['PK:' + name] = (w, [(0, w)] if w > 0 else [])
        return (d, act) if detail else d
    def pk_weight(self, T, pk):
        w = 1.0
        for b, ax, s in pk['drivers']:
            x = self.driver(T, dict(bone=b, axis=ax)); w *= max(0.0, 1.0 - abs(x - s) / abs(s))
            if w == 0: break
        return w
    def add_pose_key(self, name, drivers, idx, dd):
        """pose-space key (resolves conflicts between poses that share joint angles but need different local shapes): driver = product over its driving
        joints of tent(x_j; 0 -> s_j -> 2 s_j), s_j = the joint's measured twist in the owning pose."""
        if name not in self.PK: self.PK[name] = dict(drivers=[(b, list(np.asarray(a, float)), float(s_)) for b, a, s_ in drivers], idx=np.zeros(0, np.int64), d=np.zeros((0, 3)))
        pk = self.PK[name]; full = np.zeros((self.r.nv, 3)); full[pk['idx']] = pk['d']; full[idx] += dd; nz = np.nonzero(np.abs(full).sum(1) > 1e-9)[0]; pk['idx'] = nz; pk['d'] = full[nz]
    def interp_at(self, f, x):
        n = self.r.nv; d = np.zeros((n, 3))
        for k, w in self.hat(f['samples'], x):
            idx, dd = f['D'][k]; d[idx] += w * dd
        return d
    def resolve(self, bone, axis, tol_deg=30.0):
        """family for a driving (bone, axis): an existing family of the same bone whose axis is within tol_deg (either sign) is reused (one driver per
        joint degree of freedom: nearly parallel axes would double-activate), else a new family key."""
        a = np.asarray(axis, float); a = a / np.linalg.norm(a)
        for k, f in self.F.items():
            if f['bone'] == bone and abs(np.dot(f['axis'], a)) > np.cos(np.radians(tol_deg)): return k, np.asarray(f['axis'])
        return fam_key(bone, a), a
    def add(self, key, bone, axis, pivot, x, idx, dd):
        if key not in self.F: self.F[key] = dict(bone=bone, axis=list(np.asarray(axis, float) / np.linalg.norm(axis)), pivot=list(pivot), samples=[], D=[])
        f = self.F[key]
        near = sorted([k for k, s in enumerate(f['samples']) if abs(s - x) < self.snap], key=lambda k: abs(f['samples'][k] - x))   # snap to an existing sample
        if near: k = near[0]
        else:                                                    # new sample: initialise with the current interpolated value (no change), then add
            cur = self.interp_at(f, x); nz = np.nonzero(np.abs(cur).sum(1) > 0)[0]; f['samples'].append(float(x)); f['D'].append((nz, cur[nz])); k = len(f['samples']) - 1
        i0, d0 = f['D'][k]; full = np.zeros((self.r.nv, 3)); full[i0] = d0; full[idx] += dd; nz = np.nonzero(np.abs(full).sum(1) > 1e-9)[0]; f['D'][k] = (nz, full[nz])
    def save(self, path, meta):
        out = dict(meta); out['families'] = []
        arrays = {}
        for j, (key, f) in enumerate(sorted(self.F.items())):
            o = order = np.argsort(f['samples']); rec = dict(id='CF%03d' % j, bone=f['bone'], axis_parent_frame=f['axis'], pivot_rest_cm=f['pivot'], samples_deg=[f['samples'][k] for k in o], keys=[])
            for k in o:
                idx, dd = f['D'][k]; nm = '%s_%s_%+.1f' % ('CF%03d' % j, f['bone'], f['samples'][k]); arrays[nm + '_idx'] = idx.astype(np.int32); arrays[nm + '_d'] = dd.astype(np.float32)
                rec['keys'].append(dict(name=nm, sample_deg=f['samples'][k], n_vertices=int(len(idx)), max_delta_cm=float(np.linalg.norm(dd, axis=1).max()) if len(idx) else 0.0,
                                        mean_delta_cm=float(np.linalg.norm(dd, axis=1).mean()) if len(idx) else 0.0))
            out['families'].append(rec)
        out['pose_keys'] = []
        for j, (name, pk) in enumerate(sorted(self.PK.items())):
            nm = 'PK%03d_%s' % (j, name.replace(':', '_').replace(' ', '_')); arrays[nm + '_idx'] = pk['idx'].astype(np.int32); arrays[nm + '_d'] = pk['d'].astype(np.float32)
            out['pose_keys'].append(dict(name=nm, pose=name, drivers=[dict(bone=b, axis_parent_frame=a, sample_deg=s_) for b, a, s_ in pk['drivers']], n_vertices=int(len(pk['idx'])),
                                         max_delta_cm=float(np.linalg.norm(pk['d'], axis=1).max()) if len(pk['idx']) else 0.0))
        np.savez_compressed(path.replace('.json', '.npz'), **arrays); json.dump(out, open(path, 'w'), indent=1)
    @classmethod
    def load(cls, rig, path):
        c = cls(rig); js = json.load(open(path)); z = np.load(path.replace('.json', '.npz'))
        for f in js['families']:
            key = fam_key(f['bone'], f['axis_parent_frame'])
            c.F[key] = dict(bone=f['bone'], axis=f['axis_parent_frame'], pivot=f['pivot_rest_cm'], samples=[k['sample_deg'] for k in f['keys']],
                            D=[(z[k['name'] + '_idx'].astype(np.int64), z[k['name'] + '_d'].astype(np.float64)) for k in f['keys']])
        for pk in js.get('pose_keys', []):
            c.PK[pk['pose']] = dict(drivers=[(d_['bone'], d_['axis_parent_frame'], d_['sample_deg']) for d_ in pk['drivers']], idx=z[pk['name'] + '_idx'].astype(np.int64), d=z[pk['name'] + '_d'].astype(np.float64), name=pk['name'])
        return c
# ---------------- solver ----------------
class Solver:
    def __init__(self, rig):
        self.r = rig; Q = rig.Q; nv = rig.nv
        E = np.r_[Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]], Q[:, [0, 2]], Q[:, [1, 3]]]; E = np.unique(np.sort(E, 1), axis=0); self.E = E
        self.A = sp.coo_matrix((np.ones(2 * len(E)), (np.r_[E[:, 0], E[:, 1]], np.r_[E[:, 1], E[:, 0]])), shape=(nv, nv)).tocsr()
        Qe = np.unique(np.sort(np.r_[Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]], 1), axis=0)
        self.A1 = sp.coo_matrix((np.ones(2 * len(Qe)), (np.r_[Qe[:, 0], Qe[:, 1]], np.r_[Qe[:, 1], Qe[:, 0]])), shape=(nv, nv)).tocsr()
        self.rigid = rig.W.max(1) > 0.999
    def dilate(self, m, k):
        for _ in range(k): m = m | (self.A1 @ m.astype(np.float32) > 0)
        return m
    def solve(self, T, Pcur, flips, iters=12, ring=3, spread_tol=2e-3, smooth=0, local=False, seed=None):
        r = self.r; W = r.W; Rb = np.stack([T[b][0] for b in r.DB]); M = np.einsum('vb,bij->vij', W, Rb)
        spread = np.zeros(r.nv)                                                               # sum_b w_b ||R_b - M_v|| (bone loop: memory-bounded)
        for j in range(len(r.DB)):
            m_ = W[:, j] > 0
            if m_.any(): spread[m_] += W[m_, j] * np.linalg.norm(Rb[j][None] - M[m_], axis=(1, 2))
        reg = (spread > spread_tol) if not local else np.zeros(r.nv, bool)      # local mode: only the folds / contacts and `ring` rings around them
        fm = np.zeros(r.nv, bool); fm[r.Q[flips].ravel()] = True
        if seed is not None: fm |= seed
        reg |= self.dilate(fm, 2)
        reg = self.dilate(reg, ring)
        if getattr(self, 'pin', True):                # rigid vertices (one bone >= 0.999) stay exactly rigid unless they carry a fold / contact themselves
            reg &= ~(self.rigid & ~self.dilate(fm, 1))
        bnd = self.dilate(reg, 1) & ~reg
        I = np.nonzero(reg)[0]; B = np.nonzero(bnd)[0]; gi = -np.ones(r.nv, np.int64); gi[I] = np.arange(len(I))
        sel = reg[self.E[:, 0]] | reg[self.E[:, 1]]; E = self.E[sel]
        if smooth:                                        # smoother rotation field across the crease: Laplacian-average the blended matrices inside the region
            M9 = M.reshape(-1, 9).copy(); deg1 = np.asarray(self.A1.sum(1)).ravel()
            for _ in range(smooth): M9[I] = 0.5 * M9[I] + 0.5 * ((self.A1 @ M9)[I] / deg1[I, None])
            M = M9.reshape(-1, 3, 3)
        U, S, Vt = np.linalg.svd(M[I]); Ri = U @ Vt; dn = np.linalg.det(Ri) < 0; U[dn, :, -1] *= -1; Ri = U @ Vt
        Rall = np.repeat(np.eye(3)[None], r.nv, 0); Rall[I] = Ri
        # boundary rotations: polar of their own blend
        Ub, Sb, Vtb = np.linalg.svd(M[B]); Rall[B] = Ub @ Vtb
        V0 = r.V; P = Pcur.copy()
        # Laplacian over interior
        a, b = E[:, 0], E[:, 1]; nI = len(I)
        rows, cols, vals = [], [], []
        for x, y in ((a, b), (b, a)):
            m = reg[x]; rows.append(gi[x[m]]); cols.append(gi[x[m]]); vals.append(np.ones(m.sum()))
            m2 = m & reg[y]; rows.append(gi[x[m2]]); cols.append(gi[y[m2]]); vals.append(-np.ones(m2.sum()))
        L = sp.coo_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(nI, nI)).tocsc()
        fac = spl.splu(L)
        for it in range(iters):
            rhs = np.zeros((nI, 3))
            for x, y in ((a, b), (b, a)):
                m = reg[x]; e = V0[x[m]] - V0[y[m]]; Rm = 0.5 * (Rall[x[m]] + Rall[y[m]]); c = np.einsum('kij,kj->ki', Rm, e)
                fixed = m & ~reg[y]; c2 = c.copy(); c2[fixed[m]] += P[y[m]][fixed[m]]          # boundary neighbours move to rhs
                np.add.at(rhs, gi[x[m]], c2)
            P[I] = fac.solve(rhs)
            # local step
            Sx = np.zeros((r.nv, 3, 3))
            for x, y in ((a, b), (b, a)):
                m = reg[x]; e0 = V0[x[m]] - V0[y[m]]; e1 = P[x[m]] - P[y[m]]; np.add.at(Sx, x[m], np.einsum('ki,kj->kij', e0, e1))
            u, s_, vt = np.linalg.svd(Sx[I]); Rn = np.einsum('kji,klj->kil', vt, u)  # R = V U^T
            dn = np.linalg.det(Rn) < 0; vt[dn, -1, :] *= -1; Rn = np.einsum('kji,klj->kil', vt, u); Rall[I] = Rn
        return P, I, M
    def unfold(self, T, P, relcos, rounds=40, it=10, grow=2, lam=0.5, pin_rigid=True):
        """flip removal: uniform-Laplacian relaxation restricted to the flipped quads' vertices (dilated by `grow`, growing each round the flips
        persist); everything else held.  Returns P, remaining flips."""
        r = self.r; P = P.copy(); deg = np.asarray(self.A1.sum(1)).ravel(); g = grow
        for k in range(rounds):
            fl = np.nonzero(relcos(P, T) < 0)[0]
            if not len(fl): return P, fl
            m0 = np.zeros(r.nv, bool); m0[r.Q[fl].ravel()] = True; m = self.dilate(m0, g)
            if pin_rigid: m &= ~(self.rigid & ~m0)
            idx = np.nonzero(m)[0]
            for _ in range(it):
                avg = (self.A1 @ P) / deg[:, None]; P[idx] = (1 - lam) * P[idx] + lam * avg[idx]
            if k % 5 == 4: g += 1
        return P, np.nonzero(relcos(P, T) < 0)[0]
    def contact_plane(self, T, P, bone, pivot, eps=0.05):
        """single-hinge contact corrective: the bisector plane between the child bone's rest line carried by the parent (reversed) and its posed line, through the posed pivot; on the flexion side only,
        child-subtree-owned vertices lying past the plane on the parent side (and vice versa) are projected onto the plane (+-eps): the two tissue
        masses meet on a flat contact surface instead of interpenetrating."""
        r = self.r; p = r.par[bone]; R0, t0 = T[bone]; piv = R0 @ np.asarray(pivot) + t0
        Rp, tp = T[p]; dr = r.Tl(bone) - r.H(bone); u = -(Rp @ dr); v = R0 @ dr; u /= np.linalg.norm(u); v /= np.linalg.norm(v)   # parent side = the child's own rest line, reversed
        n = u - v
        if np.linalg.norm(n) < 1e-6: return P, 0
        n /= np.linalg.norm(n); inner = u + v
        if np.linalg.norm(inner) < 1e-6: return P, 0
        inner /= np.linalg.norm(inner)
        wc = r.W[:, [r.bi[b] for b in r.sub(bone) if b in r.bi]].sum(1)
        x = P - piv; s = x @ n; lim = 0.5 * min(np.linalg.norm(r.Tl(p) - r.H(p)), np.linalg.norm(r.Tl(bone) - r.H(bone)))
        flex = (x @ inner > 0) & (np.linalg.norm(x, axis=1) < lim)
        a = flex & (wc > 0.5) & (s > -eps); b = flex & (wc <= 0.5) & (s < eps)
        P = P.copy(); P[a] -= (s[a] + eps)[:, None] * n; P[b] -= (s[b] - eps)[:, None] * n
        return P, int(a.sum() + b.sum())
    def contact_general(self, P, pen, rex=2.0, eps=0.05, k=200):
        """general contact corrective (digit-palm, digit-digit, any non-hinge contact): every vertex found inside another part of the posed body is
        moved onto the surface it penetrates (+eps outward), using the nearest posed quad of a different body part (REST position > rex cm away, or
        another digit), never the vertex's own neighbourhood.  Both contacting sides are treated -> they meet on a shared contact surface."""
        from scipy.spatial import cKDTree
        r = self.r; Q = r.Q; idx = np.nonzero(pen)[0]
        if not len(idx): return P, 0
        cq = P[Q].mean(1); rc = r.V[Q].mean(1); dist, ii = cKDTree(cq).query(P[idx], k=k)
        if not hasattr(self, 'part'):                                   # digit membership (each digit = its own part; -1 elsewhere)
            import sa6_common as _C
            self.part = np.full(r.nv, -1); [self.part.__setitem__(v, j) for j, v in enumerate(_C.digit_components().values())]
        pv = self.part[idx][:, None]; pq = self.part[Q[ii, 0]]
        far = (np.linalg.norm(rc[ii] - r.V[idx][:, None], axis=2) > rex) | ((pq != pv) & ((pq >= 0) | (pv >= 0)))   # another body part: far at rest, or another digit
        ok = far.any(1); first = far.argmax(1); q = ii[np.arange(len(idx)), first]
        n = np.cross(P[Q[q, 2]] - P[Q[q, 0]], P[Q[q, 3]] - P[Q[q, 1]]); n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
        s = ((P[idx] - cq[q]) * n).sum(1); mv = ok & (s < eps); P = P.copy(); P[idx[mv]] += ((eps - s[mv]))[:, None] * n[mv]
        return P, int(mv.sum())
    def body_volume(self, P):
        Q = self.r.Q; a, b, c, d = (P[Q[:, k]] for k in range(4)); return (np.einsum('ij,ij->i', a, np.cross(b, c)) + np.einsum('ij,ij->i', a, np.cross(c, d))).sum() / 6
    def volume_fix(self, T, P, V0, iters=4, tol=1.0):
        """bounded volume-preservation corrective: the closed-body volume lost (or gained) by the deformation is restored inside the joints' blend zones
        only (vertices whose bone blend is non-rigid; weight = the normalised rotation spread, so the correction fades to 0 at the rigid parts), by a
        displacement along the posed vertex normals: dP = alpha * w_v * n_v with alpha = -dV / sum(w_v A_v) (first-order exact), iterated."""
        r = self.r; W = r.W; Rb = np.stack([T[b][0] for b in r.DB]); M = W @ Rb.reshape(len(r.DB), 9); M = M.reshape(-1, 3, 3)
        spread = np.zeros(r.nv)
        for j in range(len(r.DB)):
            m_ = W[:, j] > 0
            if m_.any(): spread[m_] += W[m_, j] * np.linalg.norm(Rb[j][None] - M[m_], axis=(1, 2))
        if spread.max() < 1e-6: return P, 0.0
        wv = np.clip(spread / max(np.percentile(spread[spread > 1e-6], 95), 1e-9), 0, 1); wv[self.rigid] = 0; wv = 3 * wv ** 2 - 2 * wv ** 3
        excl = [r.bi[b] for b in r.DB if b == 'jaw' or b.startswith(('finger', 'thumb', 'toe', 'meta'))]
        wv[W[:, excl].sum(1) > 0] = 0                      # never inflate the mouth / jaw or the digits
        Q_ = r.Q
        def varea(P_):
            a_ = np.zeros(r.nv); qa = 0.5 * np.linalg.norm(np.cross(P_[Q_[:, 2]] - P_[Q_[:, 0]], P_[Q_[:, 3]] - P_[Q_[:, 1]]), axis=1)
            for k in range(4): np.add.at(a_, Q_[:, k], qa / 4)
            return a_
        comp = np.clip(1.0 - varea(P) / np.maximum(varea(r.V), 1e-12), 0, 1)   # tissue bulges where the surface is compressed, not where it stretches
        deg1 = np.asarray(self.A1.sum(1)).ravel()
        for _ in range(10): comp = 0.5 * comp + 0.5 * (self.A1 @ comp) / deg1
        wv = wv * np.clip(comp / max(comp[wv > 0].max() if (wv > 0).any() else 1, 1e-9), 0, 1)
        P = P.copy(); Q = r.Q; dV0 = self.body_volume(P) - V0
        U_, _, Vt_ = np.linalg.svd(M); Mr = U_ @ Vt_                                             # polar rotation of the blend
        n_rest = np.zeros_like(r.V)
        for k in range(4): np.add.at(n_rest, Q[:, k], np.cross(r.V[Q[:, (k + 1) % 4]] - r.V[Q[:, k]], r.V[Q[:, (k + 3) % 4]] - r.V[Q[:, k]]))
        for _ in range(iters):
            dV = self.body_volume(P) - V0
            if abs(dV) < tol: break
            n = np.zeros_like(P)
            for k in range(4): np.add.at(n, Q[:, k], np.cross(P[Q[:, (k + 1) % 4]] - P[Q[:, k]], P[Q[:, (k + 3) % 4]] - P[Q[:, k]]) / 2)
            A = np.linalg.norm(n, axis=1) / 4                                                   # vertex area (posed)
            n = np.einsum('vij,vj->vi', Mr, n_rest)                                              # push along the REST outward normal carried by the blended
            n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12                                # rotation (not the crease normal: no push into the opposite wall)
            den = (wv * A * 4).sum()
            if den < 1e-9: break
            P += (-dV / den) * wv[:, None] * n
        return P, float(dV0)
    def bulge_safe(self, T, P, V0, bad, rounds=8, grow=3, **kw):
        """bulge with self-masking: after each trial the vertices of quads it newly folded / made interpenetrate (bad(P) -> vertex mask) are dilated
        `grow` rings and removed from the bulge field; the volume is re-solved on what remains.  Returns the first clean trial (or the cleanest)."""
        mask = np.zeros(self.r.nv, bool); bad0 = bad(P); best = None
        for k in range(rounds):
            Pt = self.bulge(T, P, V0, exclude=mask, **kw); b = bad(Pt) & ~bad0; nb = int(b.sum())
            if best is None or nb < best[0]: best = (nb, Pt)
            if nb == 0: return Pt, 0
            mask |= self.dilate(b, grow)
        return best[1], best[0]
    def bulge(self, T, P, V0, smooth=150, iters=6, tol=5.0, exclude=None):
        """RP6 v002 volume corrective (replaces the concentrated volume_fix as first choice): restores the closed-body volume by a BROAD, smooth flesh
        bulge around the joint -- weight = blend-zone smoothstep(rotation spread) x (1 - crease), crease = surface compressed below 85 %% area (the
        fold itself is never pushed), the weight field Laplacian-smoothed `smooth` times (no local spikes), rigid / jaw / digit vertices 0; direction =
        rest outward normal carried by the blend's polar rotation; magnitude by a secant solve on the exact closed volume."""
        r = self.r; W = r.W; Rb = np.stack([T[b][0] for b in r.DB]); M = (W @ Rb.reshape(len(r.DB), 9)).reshape(-1, 3, 3)
        spread = np.zeros(r.nv)
        for j in range(len(r.DB)):
            m_ = W[:, j] > 0
            if m_.any(): spread[m_] += W[m_, j] * np.linalg.norm(Rb[j][None] - M[m_], axis=(1, 2))
        if spread.max() < 1e-6: return P
        wv = np.clip(spread / max(np.percentile(spread[spread > 1e-6], 95), 1e-9), 0, 1); wv = 3 * wv ** 2 - 2 * wv ** 3
        excl = W[:, [r.bi[b] for b in r.DB if b == 'jaw' or b.startswith(('finger', 'thumb', 'toe', 'meta'))]].sum(1) > 0; wv[excl] = 0
        Q = r.Q; deg = np.asarray(self.A1.sum(1)).ravel()
        def varea(P_):
            a_ = np.zeros(r.nv); qa = 0.5 * np.linalg.norm(np.cross(P_[Q[:, 2]] - P_[Q[:, 0]], P_[Q[:, 3]] - P_[Q[:, 1]]), axis=1)
            for k in range(4): np.add.at(a_, Q[:, k], qa / 4)
            return a_
        crease = np.clip((0.85 - varea(P) / np.maximum(varea(r.V), 1e-12)) / 0.25, 0, 1)
        for _ in range(5): crease = 0.5 * crease + 0.5 * (self.A1 @ crease) / deg
        g = wv * (1 - crease)
        for _ in range(smooth): g = 0.5 * g + 0.5 * (self.A1 @ g) / deg
        g[self.rigid | excl] = 0
        if exclude is not None: g[exclude] = 0
        U_, _, Vt_ = np.linalg.svd(M); Mr = U_ @ Vt_
        n = np.zeros_like(r.V)
        for k in range(4): np.add.at(n, Q[:, k], np.cross(r.V[Q[:, (k + 1) % 4]] - r.V[Q[:, k]], r.V[Q[:, (k + 3) % 4]] - r.V[Q[:, k]]))
        n = np.einsum('vij,vj->vi', Mr, n); n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12; dirn = g[:, None] * n
        P = P.copy()
        for _ in range(iters):
            dV = self.body_volume(P) - V0
            if abs(dV) < tol: break
            dd = (self.body_volume(P + 1e-3 * dirn) - self.body_volume(P)) / 1e-3
            if abs(dd) < 1e-9: break
            P += (-dV / dd) * dirn
        return P
    def rest_delta(self, Pstar, Pcur, I, M):
        return I, np.linalg.solve(M[I], (Pstar[I] - Pcur[I])[:, :, None])[:, :, 0]
