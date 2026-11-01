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
    def __init__(self, rig): self.r = rig; self.F = {}           # key -> dict(bone, axis, pivot, samples[list], D[list of (idx, delta)])
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
        return (d, act) if detail else d
    def interp_at(self, f, x):
        n = self.r.nv; d = np.zeros((n, 3))
        for k, w in self.hat(f['samples'], x):
            idx, dd = f['D'][k]; d[idx] += w * dd
        return d
    def add(self, key, bone, axis, pivot, x, idx, dd):
        if key not in self.F: self.F[key] = dict(bone=bone, axis=list(np.asarray(axis, float) / np.linalg.norm(axis)), pivot=list(pivot), samples=[], D=[])
        f = self.F[key]
        near = [k for k, s in enumerate(f['samples']) if abs(s - x) < 1.0]
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
        np.savez_compressed(path.replace('.json', '.npz'), **arrays); json.dump(out, open(path, 'w'), indent=1)
    @classmethod
    def load(cls, rig, path):
        c = cls(rig); js = json.load(open(path)); z = np.load(path.replace('.json', '.npz'))
        for f in js['families']:
            key = fam_key(f['bone'], f['axis_parent_frame'])
            c.F[key] = dict(bone=f['bone'], axis=f['axis_parent_frame'], pivot=f['pivot_rest_cm'], samples=[k['sample_deg'] for k in f['keys']],
                            D=[(z[k['name'] + '_idx'].astype(np.int64), z[k['name'] + '_d'].astype(np.float64)) for k in f['keys']])
        return c
# ---------------- solver ----------------
class Solver:
    def __init__(self, rig):
        self.r = rig; Q = rig.Q; nv = rig.nv
        E = np.r_[Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]], Q[:, [0, 2]], Q[:, [1, 3]]]; E = np.unique(np.sort(E, 1), axis=0); self.E = E
        self.A = sp.coo_matrix((np.ones(2 * len(E)), (np.r_[E[:, 0], E[:, 1]], np.r_[E[:, 1], E[:, 0]])), shape=(nv, nv)).tocsr()
        Qe = np.unique(np.sort(np.r_[Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]], 1), axis=0)
        self.A1 = sp.coo_matrix((np.ones(2 * len(Qe)), (np.r_[Qe[:, 0], Qe[:, 1]], np.r_[Qe[:, 1], Qe[:, 0]])), shape=(nv, nv)).tocsr()
    def dilate(self, m, k):
        for _ in range(k): m = m | (self.A1 @ m.astype(np.float32) > 0)
        return m
    def solve(self, T, Pcur, flips, iters=12, ring=3, spread_tol=2e-3):
        r = self.r; W = r.W; Rb = np.stack([T[b][0] for b in r.DB]); M = np.einsum('vb,bij->vij', W, Rb)
        spread = np.zeros(r.nv)                                                               # sum_b w_b ||R_b - M_v|| (bone loop: memory-bounded)
        for j in range(len(r.DB)):
            m_ = W[:, j] > 0
            if m_.any(): spread[m_] += W[m_, j] * np.linalg.norm(Rb[j][None] - M[m_], axis=(1, 2))
        reg = spread > spread_tol
        fm = np.zeros(r.nv, bool); fm[r.Q[flips].ravel()] = True; reg |= self.dilate(fm, 2)
        reg = self.dilate(reg, ring)
        bnd = self.dilate(reg, 1) & ~reg
        I = np.nonzero(reg)[0]; B = np.nonzero(bnd)[0]; gi = -np.ones(r.nv, np.int64); gi[I] = np.arange(len(I))
        sel = reg[self.E[:, 0]] | reg[self.E[:, 1]]; E = self.E[sel]
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
    def unfold(self, T, P, relcos, rounds=40, it=10, grow=2, lam=0.5):
        """flip removal: uniform-Laplacian relaxation restricted to the flipped quads' vertices (dilated by `grow`, growing each round the flips
        persist); everything else held.  Returns P, remaining flips."""
        r = self.r; P = P.copy(); deg = np.asarray(self.A1.sum(1)).ravel(); g = grow
        for k in range(rounds):
            fl = np.nonzero(relcos(P, T) < 0)[0]
            if not len(fl): return P, fl
            m = np.zeros(r.nv, bool); m[r.Q[fl].ravel()] = True; m = self.dilate(m, g); idx = np.nonzero(m)[0]
            for _ in range(it):
                avg = (self.A1 @ P) / deg[:, None]; P[idx] = (1 - lam) * P[idx] + lam * avg[idx]
            if k % 5 == 4: g += 1
        return P, np.nonzero(relcos(P, T) < 0)[0]
    def contact_plane(self, T, P, bone, pivot, eps=0.05):
        """single-hinge contact corrective: the bisector plane of the posed parent / child directions through the posed pivot; on the flexion side only,
        child-subtree-owned vertices lying past the plane on the parent side (and vice versa) are projected onto the plane (+-eps): the two tissue
        masses meet on a flat contact surface instead of interpenetrating."""
        r = self.r; p = r.par[bone]; R0, t0 = T[bone]; piv = R0 @ np.asarray(pivot) + t0
        Rp, tp = T[p]; u = -(Rp @ (r.Tl(p) - r.H(p))); v = R0 @ (r.Tl(bone) - r.H(bone)); u /= np.linalg.norm(u); v /= np.linalg.norm(v)
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
    def contact_general(self, P, pen, rex=2.0, eps=0.05, k=48):
        """general contact corrective (digit-palm, digit-digit, any non-hinge contact): every vertex found inside another part of the posed body is
        moved onto the surface it penetrates (+eps outward), using the nearest posed quad whose REST position is > rex cm away (i.e. a different body
        part, never the vertex's own neighbourhood).  Both contacting sides are treated -> they meet on a shared contact surface."""
        from scipy.spatial import cKDTree
        r = self.r; Q = r.Q; idx = np.nonzero(pen)[0]
        if not len(idx): return P, 0
        cq = P[Q].mean(1); rc = r.V[Q].mean(1); dist, ii = cKDTree(cq).query(P[idx], k=k)
        far = np.linalg.norm(rc[ii] - r.V[idx][:, None], axis=2) > rex; ok = far.any(1); first = far.argmax(1); q = ii[np.arange(len(idx)), first]
        n = np.cross(P[Q[q, 2]] - P[Q[q, 0]], P[Q[q, 3]] - P[Q[q, 1]]); n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
        s = ((P[idx] - cq[q]) * n).sum(1); mv = ok & (s < eps); P = P.copy(); P[idx[mv]] += ((eps - s[mv]))[:, None] * n[mv]
        return P, int(mv.sum())
    def rest_delta(self, Pstar, Pcur, I, M):
        return I, np.linalg.solve(M[I], (Pstar[I] - Pcur[I])[:, :, None])[:, :, 0]
