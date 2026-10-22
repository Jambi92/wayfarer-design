# drape.py — fit a disk patch of the accepted v015 quad topology onto a disk patch of the accepted rev107 sculpt.
# Topology of the quad patch is unchanged; only vertex positions are solved.
#  1. rev107 patch -> unit disk by mean-value (convex-combination) embedding  => bijective parameter domain
#  2. quad patch boundary vertices: closest point on the rev107 patch -> their parameter (fixed during the solve)
#  3. quad patch interior: Tutte (uniform) embedding inside the boundary polygon in that domain (bijective start)
#  4. surface relaxation: uniform-Laplacian targets in 3D, mapped to the domain via the per-triangle Jacobian,
#     step-halving against any 2D fold => the quad patch stays an embedding on the rev107 surface throughout
import numpy as np, scipy.sparse as sp, scipy.sparse.linalg as sla
from matplotlib.tri import Triangulation, TrapezoidMapTriFinder
import igl

def loops_of(F):
    E = np.vstack([F[:, [i, (i + 1) % F.shape[1]]] for i in range(F.shape[1])])
    key = np.sort(E, 1); u, inv, c = np.unique(key, axis=0, return_inverse=True, return_counts=True)
    b = E[c[inv] == 1]; nxt = {a: bb for a, bb in b}; loops = []; seen = set()
    for s in nxt:
        if s in seen: continue
        L = [s]; seen.add(s); x = nxt[s]
        while x != s: L.append(x); seen.add(x); x = nxt[x]
        loops.append(L)
    return loops

def mvc_disk(X, F, loop, stretch_iters=0, log=None):
    n = len(X); loop = np.array(loop)
    seg = np.linalg.norm(X[np.roll(loop, -1)] - X[loop], axis=1); t = np.r_[0, np.cumsum(seg)[:-1]] / seg.sum()
    B = np.c_[np.cos(2 * np.pi * t), np.sin(2 * np.pi * t)]
    I = []; J = []; W = []
    for a, b, c in ((0, 1, 2), (1, 2, 0), (2, 0, 1)):
        i, j, k = F[:, a], F[:, b], F[:, c]
        eij = X[j] - X[i]; eik = X[k] - X[i]
        lij = np.linalg.norm(eij, axis=1); lik = np.linalg.norm(eik, axis=1)
        cs = np.clip((eij * eik).sum(1) / (lij * lik + 1e-30), -1, 1); al = np.arccos(cs); th = np.tan(al / 2)
        I += [i, i]; J += [j, k]; W += [th / (lij + 1e-30), th / (lik + 1e-30)]
    I = np.concatenate(I); J = np.concatenate(J); W0 = np.concatenate(W)
    isb = np.zeros(n, bool); isb[loop] = True; inn = np.where(~isb)[0]
    A3 = 0.5 * np.linalg.norm(np.cross(X[F[:, 1]] - X[F[:, 0]], X[F[:, 2]] - X[F[:, 0]]), axis=1)
    sig = np.ones(n); U = np.zeros((n, 2)); U[loop] = B
    for it in range(stretch_iters + 1):
        Wm = sp.coo_matrix((W0 / sig[J], (I, J)), shape=(n, n)).tocsr()
        L = sp.diags(np.asarray(Wm.sum(1)).ravel()) - Wm
        A = L[inn][:, inn].tocsc(); rhs = -L[inn][:, loop] @ B
        sol = sla.splu(A); U[inn] = np.c_[sol.solve(rhs[:, 0]), sol.solve(rhs[:, 1])]
        if it == stretch_iters: break
        # Sander L2 stretch of the domain->surface map per triangle; Yoshizawa-style reweighting toward low stretch
        u = U[F]; q = X[F]
        A2 = 0.5 * ((u[:, 1, 0] - u[:, 0, 0]) * (u[:, 2, 1] - u[:, 0, 1]) - (u[:, 2, 0] - u[:, 0, 0]) * (u[:, 1, 1] - u[:, 0, 1]))
        A2 = np.where(np.abs(A2) < 1e-20, 1e-20, A2)
        Ss = (q[:, 0] * (u[:, 1, 1] - u[:, 2, 1])[:, None] + q[:, 1] * (u[:, 2, 1] - u[:, 0, 1])[:, None] + q[:, 2] * (u[:, 0, 1] - u[:, 1, 1])[:, None]) / (2 * A2[:, None])
        St = (q[:, 0] * (u[:, 2, 0] - u[:, 1, 0])[:, None] + q[:, 1] * (u[:, 0, 0] - u[:, 2, 0])[:, None] + q[:, 2] * (u[:, 1, 0] - u[:, 0, 0])[:, None]) / (2 * A2[:, None])
        L2 = np.sqrt(((Ss * Ss).sum(1) + (St * St).sum(1)) / 2)
        num = np.zeros(n); den = np.zeros(n)
        for c in range(3): np.add.at(num, F[:, c], A3 * L2 ** 2); np.add.at(den, F[:, c], A3)
        sv = np.sqrt(num / den); sig = sig * sv / np.median(sv)
        if log:
            tot = np.sqrt((A3 * L2 ** 2).sum() / A3.sum()) / np.sqrt(A3.sum() / np.abs(A2).sum())
            log('stretch it %d L2 %.3f  area-ratio p5/p95 %.3g/%.3g' % (it, tot, *np.percentile(np.abs(A2) / A3, [5, 95])))
    return U

class Domain:
    def __init__(s, X, F, U):
        s.X, s.F, s.U = X, F, U
        s.tri = Triangulation(U[:, 0], U[:, 1], F); s.fd = TrapezoidMapTriFinder(s.tri)
        A = U[F[:, 1]] - U[F[:, 0]]; B = U[F[:, 2]] - U[F[:, 0]]
        s.M = np.stack([A, B], 2)  # 2x2 per tri (columns)
        s.Minv = np.linalg.inv(s.M)
        s.E3 = np.stack([X[F[:, 1]] - X[F[:, 0]], X[F[:, 2]] - X[F[:, 0]]], 2)  # 3x2
        s.J = s.E3 @ s.Minv  # 3x2 Jacobian (domain->3D)
        JtJ = np.transpose(s.J, (0, 2, 1)) @ s.J; s.Jp = np.linalg.inv(JtJ) @ np.transpose(s.J, (0, 2, 1))  # 2x3
    def locate(s, P):
        t = s.fd(P[:, 0], P[:, 1]); bad = t < 0
        for f in (0.999999, 0.9999, 0.999, 0.995, 0.99, 0.98, 0.95):  # rim points between chord and arc: pull inward
            bad = t < 0
            if not bad.any(): break
            Qp = P[bad] * f; t[bad] = s.fd(Qp[:, 0], Qp[:, 1])
        assert (t >= 0).all()
        return t
    def lift(s, P, t):
        b = np.einsum('nij,nj->ni', s.Minv[t], P - s.U[s.F[t, 0]])
        return s.X[s.F[t, 0]] + np.einsum('nij,nj->ni', s.E3[t], b)

def bary(p, a, b, c):
    v0 = b - a; v1 = c - a; v2 = p - a
    d00 = (v0 * v0).sum(1); d01 = (v0 * v1).sum(1); d11 = (v1 * v1).sum(1); d20 = (v2 * v0).sum(1); d21 = (v2 * v1).sum(1)
    den = d00 * d11 - d01 * d01; v = (d11 * d20 - d01 * d21) / den; w = (d00 * d21 - d01 * d20) / den
    return np.c_[1 - v - w, v, w]

def square_targets(X, Q, vqi, vqk, vqm):
    # per quad: the best-fitting square of equal area in the quad's plane; vertex target = mean of its square corners
    P = X[Q]; c = P.mean(1); d1 = P[:, 2] - P[:, 0]; d2 = P[:, 3] - P[:, 1]; nrm = np.cross(d1, d2)
    area = 0.5 * np.linalg.norm(nrm, axis=1); nrm /= np.linalg.norm(nrm, axis=1)[:, None] + 1e-30
    e1 = P[:, 0] - c; e1 -= (e1 * nrm).sum(1)[:, None] * nrm; e1 /= np.linalg.norm(e1, axis=1)[:, None] + 1e-30; e2 = np.cross(nrm, e1)
    x = ((P - c[:, None]) * e1[:, None]).sum(2); y = ((P - c[:, None]) * e2[:, None]).sum(2)
    k = np.arange(4) * np.pi / 2; ck, sk = np.cos(k), np.sin(k)
    xr = x * ck + y * sk; yr = -x * sk + y * ck  # rotate corner k by -k*90deg
    th = np.arctan2(yr.sum(1), xr.sum(1)); r = np.sqrt(area / 2)
    ang = th[:, None] + k[None]
    S = c[:, None] + r[:, None, None] * (np.cos(ang)[..., None] * e1[:, None] + np.sin(ang)[..., None] * e2[:, None])
    T = S[vqi, vqk] * vqm[..., None]
    return T.sum(1) / vqm.sum(1)[:, None]

def orient2(P, Q):
    a = P[Q[:, 0]]; b = P[Q[:, 1]]; c = P[Q[:, 2]]; d = P[Q[:, 3]]
    cr = lambda p, q, r: (q[:, 0] - p[:, 0]) * (r[:, 1] - p[:, 1]) - (q[:, 1] - p[:, 1]) * (r[:, 0] - p[:, 0])
    return np.minimum.reduce([cr(a, b, c), cr(b, c, d), cr(c, d, a), cr(d, a, b)])

def drape(Pq, Q, bnd_loop, bnd_points, X, F, rloop, pins=(), iters=300, lam=0.5, log=None, mix=0.3, stretch_iters=4, shape=0.0, pin_rate=0.003, hard_pins=()):
    """Pq: quad patch vertex positions (local), Q: local quads, bnd_fixed3d: dict local vid -> 3D point on rev107 patch (fixed),
    X,F: rev107 patch (local), rloop: rev107 boundary loop (local ids). pins: [(local vid, 3D target)] interior pins.
    Returns new positions (local) and the domain params."""
    U = mvc_disk(X, F, rloop, stretch_iters=stretch_iters, log=log); D = Domain(X, F, U)
    n = len(Pq); fixed = np.zeros(n, bool); P2 = np.zeros((n, 2))
    if bnd_points is not None:
        # fixed boundary = given 3D points on the rev107 patch (the same projection the surrounding hand uses);
        # the rev107 patch extends a little beyond them, so they are interior points of the domain
        ids = np.array(bnd_loop); pts = np.asarray(bnd_points)
        _, ti, cp = igl.point_mesh_squared_distance(pts, X, F)
        bc = bary(cp, X[F[ti, 0]], X[F[ti, 1]], X[F[ti, 2]])
        P2[ids] = np.einsum('nk,nkd->nd', bc, U[F[ti]]); fixed[ids] = True
        if log: log('boundary from points: max snap %.3f mm' % (np.linalg.norm(cp - pts, axis=1).max() * 10))
    else:
        # fixed boundary: the quad boundary loop is laid along the rev107 boundary loop by arc length (monotone, so the
        # boundary polygon is simple); the direction and offset that best match the original positions are chosen
        qloop = np.array(bnd_loop); rl = np.array(rloop)
        seg = np.linalg.norm(X[np.roll(rl, -1)] - X[rl], axis=1); tr = np.r_[0, np.cumsum(seg)] / seg.sum()
        Rpts = np.vstack([X[rl], X[rl[:1]]])
        def at(tt):
            tt = np.mod(tt, 1.0); j = np.clip(np.searchsorted(tr, tt, side='right') - 1, 0, len(rl) - 1); f = (tt - tr[j]) / (tr[j + 1] - tr[j])
            return Rpts[j] * (1 - f)[:, None] + Rpts[j + 1] * f[:, None], tt
        best = None
        for direction in (1, -1):
            ql = qloop if direction == 1 else qloop[::-1]
            sq = np.linalg.norm(Pq[np.roll(ql, -1)] - Pq[ql], axis=1); tq = np.r_[0, np.cumsum(sq)[:-1]] / sq.sum()
            for off in np.linspace(0, 1, 721)[:-1]:
                pts, _ = at(tq + off); e = np.linalg.norm(pts - Pq[ql], axis=1).mean()
                if best is None or e < best[0]: best = (e, direction, off, ql, tq)
        e, direction, off, ql, tq = best
        pts, tt = at(tq + off); ids = ql
        P2[ids] = np.c_[np.cos(2 * np.pi * tt), np.sin(2 * np.pi * tt)]; fixed[ids] = True
        if log: log('boundary fit mean %.3f mm dir %d' % (e * 10, direction))

    hard = np.zeros(n, bool)
    # hard interior pins (e.g. the centre of the old end-cap grid -> claw apex): fixed in the Tutte solve and afterwards
    for vid, tgt in hard_pins:
        _, ti, cp = igl.point_mesh_squared_distance(np.array([tgt]), X, F)
        bc = bary(cp, X[F[ti, 0]], X[F[ti, 1]], X[F[ti, 2]])
        P2[vid] = np.einsum('nk,nkd->nd', bc, U[F[ti]])[0]; fixed[vid] = True; hard[vid] = True
    ids = np.where(fixed)[0]
    # orientation of the boundary polygon must match the domain orientation; Tutte embed interior inside it
    E = np.vstack([Q[:, [i, (i + 1) % 4]] for i in range(4)]); E = np.unique(np.sort(E, 1), axis=0)
    Aj = sp.coo_matrix((np.ones(2 * len(E)), (np.r_[E[:, 0], E[:, 1]], np.r_[E[:, 1], E[:, 0]])), shape=(n, n)).tocsr()
    deg = np.asarray(Aj.sum(1)).ravel(); inn = np.where(~fixed)[0]
    L = sp.diags(deg) - Aj; A = L[inn][:, inn].tocsc(); rhs = -L[inn][:, ids] @ P2[ids]
    so = sla.splu(A); P2[inn] = np.c_[so.solve(rhs[:, 0]), so.solve(rhs[:, 1])]
    o0 = orient2(P2, Q); sgn = np.sign(np.median(o0))
    nb = [[] for _ in range(n)]
    for a, b in E: nb[a].append(b); nb[b].append(a)
    nbi = np.zeros((n, int(deg.max()))) .astype(int); nbm = np.zeros_like(nbi, bool)
    for i, l in enumerate(nb): nbi[i, :len(l)] = l; nbm[i, :len(l)] = True
    pin_ids = []
    for vid, tgt in pins:
        _, ti, cp = igl.point_mesh_squared_distance(np.array([tgt]), X, F)
        bc = bary(cp, X[F[ti, 0]], X[F[ti, 1]], X[F[ti, 2]])
        pin_ids.append((vid, np.einsum('nk,nkd->nd', bc, U[F[ti]])[0]))
    # untangle the start: vertices of folded quads move to the 2D mean of their neighbours (Tutte inside a non-convex
    # fixed boundary can fold near the boundary)
    nb0 = [[] for _ in range(n)]
    for a_, b_ in E: nb0[a_].append(b_); nb0[b_].append(a_)
    for ut in range(500):
        o = orient2(P2, Q) * sgn; bq = np.where(o <= 1e-14)[0]
        if len(bq) == 0: break
        ring = set(np.unique(Q[bq]).tolist())
        if ut > 50:
            for v in list(ring): ring.update(nb0[v])
        for v in ring:
            if (not fixed[v] or ut > 150) and not hard[v]: P2[v] = P2[nb0[v]].mean(0)
    r_ = np.linalg.norm(P2, axis=1); P2[r_ > 0.9995] *= (0.9995 / r_[r_ > 0.9995])[:, None]
    P2 = local_tutte_fix(P2, Q, fixed, sgn, log=log, hard=hard)
    if log: log('untangle: folds after %d sweeps: %d' % (ut, int((orient2(P2, Q) * sgn <= 1e-14).sum())))
    t = D.locate(P2); X3 = D.lift(P2, t)
    pins2 = []
    for vid, tgt in pins:  # pin the vertex whose initial image is nearest the target (vid=None) or the given one
        if vid is None: vid = int(np.argmin(np.linalg.norm(np.where(fixed[:, None], 1e9, X3) - tgt, axis=1)))
        pins2.append(vid)
    pin_ids = [(v2, uv) for v2, (_, uv) in zip(pins2, pin_ids)]
    if log: log('init folds %d (sign %d)' % ((sgn * o0 <= 0).sum(), sgn))
    mov = ~fixed
    # vertex -> incident quads (area-weighted centroid relaxation equalizes face areas; a plain Laplacian would
    # behave like a harmonic map and starve the long claws of quads)
    vf = [[] for _ in range(n)]
    for qi, q in enumerate(Q):
        for v in q: vf[v].append(qi)
    mf = max(len(l) for l in vf); vfi = np.zeros((n, mf), int); vfm = np.zeros((n, mf), bool)
    for i, l in enumerate(vf): vfi[i, :len(l)] = l; vfm[i, :len(l)] = True
    vq_i = vfi; vq_m = vfm; vq_k = np.zeros_like(vfi)
    for i in range(n):
        for j, qi in enumerate(vf[i]): vq_k[i, j] = int(np.where(Q[qi] == i)[0][0])
    for it in range(iters):
        c = X3[Q].mean(1); ar = 0.5 * (np.linalg.norm(np.cross(X3[Q[:, 1]] - X3[Q[:, 0]], X3[Q[:, 3]] - X3[Q[:, 0]]), axis=1) + np.linalg.norm(np.cross(X3[Q[:, 1]] - X3[Q[:, 2]], X3[Q[:, 3]] - X3[Q[:, 2]]), axis=1))
        w = ar[vfi] * vfm; cen = (c[vfi] * w[..., None]).sum(1) / (w.sum(1)[:, None] + 1e-30)
        nbr = X3[nbi] * nbm[..., None]; mean = nbr.sum(1) / nbm.sum(1)[:, None]
        Lp = (1 - mix - shape) * (cen - X3) + mix * (mean - X3)
        if shape > 0:
            Lp = Lp + shape * (square_targets(X3, Q, vq_i, vq_k, vq_m) - X3)
        d2 = np.einsum('nij,nj->ni', D.Jp[t], Lp) * lam
        d2[~mov] = 0
        for vid, uv in pin_ids:  # move pinned vertices gradually toward their target in the domain
            dv = uv - P2[vid]; nv = np.linalg.norm(dv); d2[vid] = dv if nv < pin_rate else dv * (pin_rate / nv)
        step = np.ones(n); prev_bad = set(np.where(orient2(P2, Q) * sgn <= 1e-14)[0])
        for tr in range(8):
            Pn = P2 + d2 * step[:, None]
            r = np.linalg.norm(Pn, axis=1); out = r > 0.9995; Pn[out] *= (0.9995 / r[out])[:, None]
            o = orient2(Pn, Q) * sgn; badq = np.array([q for q in np.where(o <= 1e-14)[0] if q not in prev_bad], int)
            if len(badq) == 0: break
            bv = np.unique(Q[badq]); step[bv] *= 0.5
        else:
            for rr in range(50):  # revert offending vertices (and, if needed, their neighbours) to the previous state
                o = orient2(Pn, Q) * sgn; badq = np.array([q for q in np.where(o <= 1e-14)[0] if q not in prev_bad], int)
                if len(badq) == 0: break
                bv = np.unique(Q[badq]); Pn[bv] = P2[bv]
        P2 = Pn; t = D.locate(P2); X3 = D.lift(P2, t)
        if log and (it % 50 == 0 or it == iters - 1):
            e = np.linalg.norm(X3[Q] - X3[np.roll(Q, 1, 1)], axis=2)
            log('it %d edge mm med %.3f p95 %.3f max %.3f min %.4f folds %d' % (it, np.median(e) * 10, np.percentile(e, 95) * 10, e.max() * 10, e.min() * 10, int((orient2(P2, Q) * sgn <= 0).sum())))
    if (orient2(P2, Q) * sgn <= 1e-14).any():
        P2 = local_tutte_fix(P2, Q, fixed, sgn, log=log, hard=hard); t = D.locate(P2); X3 = D.lift(P2, t)
    if (orient2(P2, Q) * sgn <= 1e-14).any():
        mv_ = ~hard
        for rep in range(3):
            P2 = smooth_fix(P2, Q, sgn, mv_ & ~fixed, log=log)
            P2 = star_fix(P2, Q, sgn, mv_, log=log)
            if not (orient2(P2, Q) * sgn <= 1e-14).any(): break
        t = D.locate(P2); X3 = D.lift(P2, t)
    if log: log('FINAL folds %d' % int((orient2(P2, Q) * sgn <= 1e-14).sum()))
    return X3, P2, U

def clip_plane(X, F, p0, nrm, keep_tri=None):
    """Exact clip of a triangle mesh to the half space (x-p0).n >= 0. Returns X2, F2 (new vertices appended on cut edges)."""
    d = (X - p0) @ nrm; d = np.where(np.abs(d) < 1e-7, 1e-7, d); pos = d > 0
    np_ = pos[F].sum(1)
    out_f = [F[np_ == 3]]
    cross = F[(np_ == 1) | (np_ == 2)]
    newv = {}; Xn = [X]; cnt = [len(X)]
    def ev(a, b):
        key = (a, b) if a < b else (b, a)
        if key not in newv:
            t = d[a] / (d[a] - d[b]); Xn.append((X[a] + t * (X[b] - X[a]))[None]); newv[key] = cnt[0]; cnt[0] += 1
        return newv[key]
    tris = []
    for f in cross:
        p = pos[f]
        # rotate so the "odd" vertex is first
        if p.sum() == 1: r = int(np.where(p)[0][0])
        else: r = int(np.where(~p)[0][0])
        a, b, c = f[r], f[(r + 1) % 3], f[(r + 2) % 3]
        ab = ev(a, b); ac = ev(a, c)
        if p.sum() == 1: tris.append([a, ab, ac])
        else: tris += [[ab, b, c], [ab, c, ac]]
    X2 = np.vstack(Xn); F2 = np.vstack(out_f + ([np.array(tris)] if tris else []))
    return X2, F2

def arap_squares(P2, Q, D, fixed, sgn, iters=30, area_mix=1.0, log=None, w_diag=0.5, step=0.5):
    """Global ARAP-to-squares on the surface through the domain: local step = best-fit square per quad (in its tangent
    plane, area blended toward the patch mean), global step = sparse least squares for the domain coordinates with the
    per-edge Jacobian frozen; fold-safe line search."""
    n = len(P2); free = ~fixed; fi = -np.ones(n, int); fi[free] = np.arange(free.sum()); nf = free.sum()
    pairs = [(0, 1), (1, 2), (2, 3), (3, 0)] + ([(0, 2), (1, 3)] if w_diag > 0 else [])
    t = D.locate(P2); X = D.lift(P2, t)
    for it in range(iters):
        P = X[Q]; c = P.mean(1); d1 = P[:, 2] - P[:, 0]; d2 = P[:, 3] - P[:, 1]; nrm = np.cross(d1, d2)
        area = 0.5 * np.linalg.norm(nrm, axis=1); nrm /= np.linalg.norm(nrm, axis=1)[:, None] + 1e-30
        Atar = np.exp(area_mix * np.log(area.mean()) + (1 - area_mix) * np.log(area + 1e-30))
        e1 = P[:, 0] - c; e1 -= (e1 * nrm).sum(1)[:, None] * nrm; e1 /= np.linalg.norm(e1, axis=1)[:, None] + 1e-30; e2 = np.cross(nrm, e1)
        x = ((P - c[:, None]) * e1[:, None]).sum(2); y = ((P - c[:, None]) * e2[:, None]).sum(2)
        k = np.arange(4) * np.pi / 2; ck, sk = np.cos(k), np.sin(k)
        xr = x * ck + y * sk; yr = -x * sk + y * ck; th = np.arctan2(yr.sum(1), xr.sum(1)); r = np.sqrt(Atar / 2)
        ang = th[:, None] + k[None]
        S = c[:, None] + r[:, None, None] * (np.cos(ang)[..., None] * e1[:, None] + np.sin(ang)[..., None] * e2[:, None])
        rows = []; cols = []; vals = []; rhs = np.zeros(2 * nf)
        Jv = D.J[t]  # per-vertex Jacobian (3x2) of its containing triangle
        for (a, b) in pairs:
            w = 1.0 if b - a in (1, -3) or (a, b) == (3, 0) else w_diag
            i = Q[:, a]; j = Q[:, b]; Je = 0.5 * (Jv[i] + Jv[j]); de = S[:, b] - S[:, a]
            M = np.einsum('nki,nkj->nij', Je, Je) * w; bb = np.einsum('nki,nk->ni', Je, de) * w
            for (p, q, sg) in ((i, i, 1), (j, j, 1), (i, j, -1), (j, i, -1)):
                m = free[p] & free[q]
                for r_ in range(2):
                    for c_ in range(2):
                        rows.append(2 * fi[p[m]] + r_); cols.append(2 * fi[q[m]] + c_); vals.append(sg * M[m, r_, c_])
            # fixed neighbours move to the rhs
            mi = free[i] & ~free[j]; mj = free[j] & ~free[i]
            # rhs from target: d/dui of ||Je(uj-ui)-de||^2 -> M ui - M uj + b ; equation: M ui - M uj = -b
            np.add.at(rhs, 2 * fi[i[free[i]]], -bb[free[i], 0]); np.add.at(rhs, 2 * fi[i[free[i]]] + 1, -bb[free[i], 1])
            np.add.at(rhs, 2 * fi[j[free[j]]], bb[free[j], 0]); np.add.at(rhs, 2 * fi[j[free[j]]] + 1, bb[free[j], 1])
            if mi.any():
                v = np.einsum('nij,nj->ni', M[mi], P2[j[mi]]); np.add.at(rhs, 2 * fi[i[mi]], v[:, 0]); np.add.at(rhs, 2 * fi[i[mi]] + 1, v[:, 1])
            if mj.any():
                v = np.einsum('nij,nj->ni', M[mj], P2[i[mj]]); np.add.at(rhs, 2 * fi[j[mj]], v[:, 0]); np.add.at(rhs, 2 * fi[j[mj]] + 1, v[:, 1])
        A = sp.coo_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(2 * nf, 2 * nf)).tocsc()
        A = A + sp.eye(2 * nf) * 1e-9 * A.diagonal().mean()
        sol = sla.spsolve(A, rhs).reshape(-1, 2)
        Pn = P2.copy(); Pn[free] = sol; dP = Pn - P2
        prev = set(np.where(orient2(P2, Q) * sgn <= 1e-14)[0]); alpha = step
        Pt = P2 + alpha * dP; rr = np.linalg.norm(Pt, axis=1); Pt[rr > 0.9995] *= (0.9995 / rr[rr > 0.9995])[:, None]
        nrev = 0
        for ls in range(60):  # revert vertices of newly folded quads (growing the reverted set if needed)
            nb = np.array([q for q in np.where(orient2(Pt, Q) * sgn <= 1e-14)[0] if q not in prev], int)
            if len(nb) == 0: break
            bv = np.unique(Q[nb]); Pt[bv] = P2[bv]; nrev += len(bv)
        P2 = Pt; t = D.locate(P2); X = D.lift(P2, t)
        if log and (it % 5 == 0 or it == iters - 1):
            Pq = X[Q]
            def ang_(a_, b_, c_):
                u_ = a_ - b_; v_ = c_ - b_; return np.degrees(np.arccos(np.clip((u_ * v_).sum(1) / np.linalg.norm(u_, axis=1) / np.linalg.norm(v_, axis=1), -1, 1)))
            Aq = np.stack([ang_(Pq[:, (i_ - 1) % 4], Pq[:, i_], Pq[:, (i_ + 1) % 4]) for i_ in range(4)], 1)
            el = np.linalg.norm(Pq - np.roll(Pq, 1, 1), axis=2)
            log('arap it %d reverted %d ang-ok %.1f%% asp<=4 %.1f%% edge med %.3f min %.4f folds %d' % (it, nrev, 100 * ((Aq >= 45) & (Aq <= 135)).all(1).mean(), 100 * (el.max(1) / el.min(1) <= 4).mean(), np.median(el) * 10, el.min() * 10, int((orient2(P2, Q) * sgn <= 1e-14).sum())))
    return X, P2

def local_tutte_fix(P2, Q, fixed, sgn, rings=(2, 4, 6, 9, 13, 18, 25), log=None, hard=None):
    P2 = _local_tutte_fix(P2, Q, fixed, sgn, rings, log)
    if (orient2(P2, Q) * sgn <= 1e-14).any():
        # second pass: release the (non-pinned) fixed vertices that belong to folded quads (e.g. three collinear boundary
        # vertices of a staircase corner); they move only within the rev107 surface
        bad = np.where(orient2(P2, Q) * sgn <= 1e-14)[0]; fx = fixed.copy(); rel = np.unique(Q[bad])
        if hard is not None: rel = rel[~hard[rel]]
        fx[rel] = False
        if log: log('releasing %d fixed vertices of folded quads' % len(rel))
        P2 = _local_tutte_fix(P2, Q, fx, sgn, rings, log)
    return P2

def _local_tutte_fix(P2, Q, fixed, sgn, rings=(2, 4, 6, 9, 13, 18, 25), log=None):
    """remove remaining 2D folds: re-solve a uniform Tutte embedding inside a growing quad neighbourhood of the folds
    (region boundary fixed). Fixed (boundary / pinned) vertices are never moved."""
    n = len(P2)
    E = np.unique(np.sort(np.vstack([Q[:, [i, (i + 1) % 4]] for i in range(4)]), 1), axis=0)
    Aj = sp.coo_matrix((np.ones(2 * len(E)), (np.r_[E[:, 0], E[:, 1]], np.r_[E[:, 1], E[:, 0]])), shape=(n, n)).tocsr()
    vq = [[] for _ in range(n)]
    for qi, q in enumerate(Q):
        for v in q: vq[v].append(qi)
    for R in rings:
        bad = np.where(orient2(P2, Q) * sgn <= 1e-14)[0]
        if len(bad) == 0: break
        reg = set(bad.tolist())
        for r in range(R):
            vs = np.unique(Q[list(reg)]); nxt = set()
            for v in vs: nxt.update(vq[v])
            reg |= nxt
        reg = np.array(sorted(reg)); vs = np.unique(Q[reg])
        inreg = np.zeros(len(Q), bool); inreg[reg] = True
        interior = np.array([v for v in vs if all(inreg[q] for q in vq[v]) and not fixed[v]], int)
        if len(interior) == 0: continue
        isI = np.zeros(n, bool); isI[interior] = True
        sub = Aj[interior]; deg = np.asarray(sub.sum(1)).ravel()
        A = (sp.diags(deg) - sub[:, interior]).tocsc(); rhs = sub[:, ~isI] @ P2[~isI]
        so = sla.splu(A); new = P2.copy(); new[interior] = np.c_[so.solve(rhs[:, 0]), so.solve(rhs[:, 1])]
        nb_ = (orient2(new, Q) * sgn <= 1e-14).sum()
        if log: log('local tutte ring %d: region %d verts, folds %d -> %d' % (R, len(interior), len(bad), nb_))
        if nb_ < len(bad): P2 = new
    return P2

def star_fix(P2, Q, sgn, movable, iters=20, log=None, seed=0):
    """per-vertex repair: a vertex of a folded quad is moved to the sampled point of its 1-ring region that maximizes
    the minimum quad orientation of its star (fixes folds and 180-degree corner collinearity)."""
    rng = np.random.default_rng(seed); n = len(P2)
    vq = [[] for _ in range(n)]
    for qi, q in enumerate(Q):
        for v in q: vq[v].append(qi)
    for it in range(iters):
        o = orient2(P2, Q) * sgn; bad = np.where(o <= 1e-14)[0]
        if len(bad) == 0: break
        for v in np.unique(Q[bad]):
            if not movable[v]: continue
            st = np.array(vq[v]); ring = np.unique(Q[st]); ring = ring[ring != v]
            lo = P2[ring].min(0); hi = P2[ring].max(0)
            cands = np.vstack([P2[v], P2[ring].mean(0), lo + (hi - lo) * rng.random((400, 2))])
            best = None
            for c in cands:
                old = P2[v].copy(); P2[v] = c; m = (orient2(P2, Q[st]) * sgn).min(); P2[v] = old
                if best is None or m > best[0]: best = (m, c)
            P2[v] = best[1]
        if log: log('star fix it %d: folds %d -> %d' % (it, len(bad), int((orient2(P2, Q) * sgn <= 1e-14).sum())))
    return P2

def smooth_fix(P2, Q, sgn, movable, rings=(1, 2, 3, 5, 8), sweeps=80, log=None):
    """local 2D Laplacian smoothing of a growing ring around folded quads (movable vertices only); kept if folds drop"""
    n = len(P2); vq = [[] for _ in range(n)]
    for qi, q in enumerate(Q):
        for v in q: vq[v].append(qi)
    nb = [set() for _ in range(n)]
    for q in Q:
        for i in range(4): nb[q[i]].add(q[(i + 1) % 4]); nb[q[i]].add(q[(i - 1) % 4])
    nb = [np.array(sorted(s)) for s in nb]
    for R in rings:
        bad = np.where(orient2(P2, Q) * sgn <= 1e-14)[0]
        if len(bad) == 0: break
        vs = set(np.unique(Q[bad]).tolist())
        for r in range(R):
            for v in list(vs): vs.update(nb[v].tolist())
        vs = np.array([v for v in vs if movable[v]], int)
        new = P2.copy()
        for s_ in range(sweeps):
            for v in vs: new[v] = new[nb[v]].mean(0)
        nb_ = int((orient2(new, Q) * sgn <= 1e-14).sum())
        if log: log('smooth fix ring %d: %d verts, folds %d -> %d' % (R, len(vs), len(bad), nb_))
        if nb_ < len(bad): P2 = new
    return P2

def pin_star_fix(P2, Q, sgn, pin, fixed, rings=(2, 3, 4, 6, 8, 11, 15, 20), log=None):
    """re-embed a growing ring neighbourhood around a hard pin by uniform Tutte (pin and ring boundary fixed)"""
    n = len(P2)
    E = np.unique(np.sort(np.vstack([Q[:, [i, (i + 1) % 4]] for i in range(4)]), 1), axis=0)
    Aj = sp.coo_matrix((np.ones(2 * len(E)), (np.r_[E[:, 0], E[:, 1]], np.r_[E[:, 1], E[:, 0]])), shape=(n, n)).tocsr()
    vq = [[] for _ in range(n)]
    for qi, q in enumerate(Q):
        for v in q: vq[v].append(qi)
    for R in rings:
        bad0 = int((orient2(P2, Q) * sgn <= 1e-14).sum())
        if bad0 == 0: break
        reg = set(vq[pin])
        for r in range(R):
            vs = np.unique(Q[list(reg)]); nxt = set()
            for v in vs: nxt.update(vq[v])
            reg |= nxt
        reg = np.array(sorted(reg)); vs = np.unique(Q[reg]); inreg = np.zeros(len(Q), bool); inreg[reg] = True
        interior = np.array([v for v in vs if all(inreg[q] for q in vq[v]) and not fixed[v] and v != pin], int)
        isI = np.zeros(n, bool); isI[interior] = True
        sub = Aj[interior]; deg = np.asarray(sub.sum(1)).ravel()
        A = (sp.diags(deg) - sub[:, interior]).tocsc(); rhs = sub[:, ~isI] @ P2[~isI]
        so = sla.splu(A); new = P2.copy(); new[interior] = np.c_[so.solve(rhs[:, 0]), so.solve(rhs[:, 1])]
        nb_ = int((orient2(new, Q) * sgn <= 1e-14).sum())
        if log: log('pin star fix ring %d: %d verts, folds %d -> %d' % (R, len(interior), bad0, nb_))
        if nb_ < bad0: P2 = new
    return P2
