# sa_patchopt.py IN.npz OUT.npz : JOINT local optimisation of T-4 residual clusters (order 236dddc §9 "local edge sliding / web / fan / 2:1 shape"),
#   complementing the one-vertex-at-a-time sa_qopt (which cannot leave local minima where every single move worsens a neighbour).
#   Each cluster of residual quads (aspect > 3.9 or angle outside 46-134, tips excepted) + 2 quad rings is a patch; its interior vertices move TOGETHER in
#   their tangent planes (2 DOF each, positions re-projected onto the working source), minimising
#   sum_quads [ max(0, aspect - 3.4)^2 + sum_corners (max(0, 50 - a) / 10)^2 + (max(0, a - 130) / 10)^2 ] + 20 * sum_samples max(0, d - thr)^2 / thr^2
#   (local source coverage with the zone thresholds 1.35 / 2.7 mm, evaluated at acceptance). L-BFGS with numeric gradients; a patch is accepted only if its worst quad
#   improves and no local source vertex ends above its threshold that was below it before.
import sys, os, numpy as np, igl, scipy.sparse as sp, scipy.optimize as so
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_geo as G
from scipy.sparse.csgraph import connected_components
IN, OUT = sys.argv[1:3]
z = dict(np.load(IN)); Q = z['Q']; V = (z['bc'][:, :, None] * G.V[G.F[z['tri']]]).sum(1); nv = len(V); nq = len(Q); nb = int(z['n_body']); ql = z['qlab'].astype(str)
pin = np.zeros(nv, bool); pin[nb:] = True; pin[z['tail_ring']] = True; pin[z['pinned']] = True; TIP = np.isin(ql, ['finger_cap', 'thumb_cap', 'toe_cap', 'tail'])
zone = np.isin(G.LAB, ['head', 'hand_xneg', 'hand_xpos', 'foot_xneg', 'foot_xpos', 'tail']); thr = np.where(zone, 0.135, 0.27)
tr = igl.AABB(); tr.init(G.V, G.F)
VQ = sp.coo_matrix((np.ones(4 * nq), (Q.ravel(), np.repeat(np.arange(nq), 4))), shape=(nv, nq)).tocsr(); QQ = (VQ.T @ VQ).tocsr()
def qmetrics(P4):
    sd = np.linalg.norm(np.roll(P4, -1, -2) - P4, axis=-1); asp = sd.max(-1) / np.maximum(sd.min(-1), 1e-9)
    u1 = np.roll(P4, 1, -2) - P4; u2 = np.roll(P4, -1, -2) - P4
    ang = np.degrees(np.arccos(np.clip((u1 * u2).sum(-1) / (np.linalg.norm(u1, axis=-1) * np.linalg.norm(u2, axis=-1) + 1e-12), -1, 1))); return asp, ang
def ptri(P, A, B, C):
    import importlib; return _pt(P, A, B, C)
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sa_qopt.py')).read().split('def ptri')[1].split('def shape_ex')[0].replace('(P, A, B, C):', 'def _pt(P, A, B, C):', 1))
asp, ang = qmetrics(V[Q]); badq = ((asp > 3.9) | (ang.min(1) < 46) | (ang.max(1) > 134)) & ~TIP
AT = float(os.environ.get('ASP_T', 3.4))
if os.environ.get('TARGET_PTS'):                     # deformation-targeted mode: the quads nearest the given points (topology-test folds) are the cores
    pts = np.array([[float(c) for c in t.split(',')] for t in os.environ['TARGET_PTS'].split(';')]); qcn = V[Q].mean(1)
    badq = np.zeros(nq, bool); badq[[int(np.argmin(np.linalg.norm(qcn - p_, axis=1))) for p_ in pts]] = True
bi = np.nonzero(badq)[0]; nc, lab = connected_components(QQ[bi][:, bi], directed=False); print('residual quads', len(bi), 'clusters', nc, flush=True)
T = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]; cg = igl.AABB(); cg.init(V, T); d0 = np.sqrt(cg.squared_distance(V, T, G.V)[0])
from scipy.spatial import cKDTree
acc = 0
for c in range(nc):
    core = bi[lab == c]
    if len(core) > 40:                                                   # large residual bands (orbit fans): optimise in windows of 40 core quads
        core = core[np.argsort(np.linalg.norm(V[Q[core]].mean(1) - V[Q[core]].mean(1)[0], axis=1))[:40]]
    pq = set(core.tolist())
    for _ in range(int(os.environ.get('RINGS', 2))): pq |= set(QQ[list(pq)].indices.tolist())
    pq = np.array(sorted(pq)); pv = np.unique(Q[pq])
    inner = np.array([v for v in pv if not pin[v] and set(VQ[v].indices.tolist()) <= set(pq.tolist())])
    if not len(inner): continue
    # local samples: source vertices whose nearest cage triangle belongs to the patch
    cen = V[pv].mean(0); rad = np.linalg.norm(V[pv] - cen, axis=1).max()
    sv = np.array(cKDTree(G.V).query_ball_point(cen, rad), int)
    if len(sv) > 500: sv = sv[np.argsort(-d0[sv] / thr[sv])[:500]]
    Qp = Q[pq]; P0 = V.copy(); N = np.nan_to_num(igl.per_vertex_normals(V, T))[inner]
    t1 = np.cross(N, [0.37, 0.59, 0.71]); t1 /= np.linalg.norm(t1, axis=1, keepdims=True) + 1e-12; t2 = np.cross(N, t1)
    el = np.median(np.linalg.norm(V[Qp[:, 1]] - V[Qp[:, 0]], axis=1))
    def place(x):
        X = x.reshape(-1, 2) * el; P = P0[inner] + X[:, :1] * t1 + X[:, 1:] * t2; _, _, cp = tr.squared_distance(G.V, G.F, P); return cp
    def energy(x, detail=False):
        Pall = P0.copy(); Pall[inner] = place(x); P4 = Pall[Qp]; a, g = qmetrics(P4)
        e = (np.maximum(0, a - AT) ** 2).sum() + ((np.maximum(0, 50 - g) / 10) ** 2).sum() + ((np.maximum(0, g - 130) / 10) ** 2).sum()
        if len(sv) and detail:
            A_ = P4[:, [0, 0]].reshape(-1, 3); B_ = P4[:, [1, 2]].reshape(-1, 3); C_ = P4[:, [2, 3]].reshape(-1, 3)
            dd = np.sqrt(_pt(G.V[sv][:, None], A_[None], B_[None], C_[None]).min(1)); dd = np.minimum(dd, d0[sv] + 0.5)
            e += 20 * ((np.maximum(0, dd - thr[sv]) / thr[sv]) ** 2).sum()
            if detail: return e, a, g, dd
        return (e, a, g, None) if detail else e
    x0 = np.zeros(2 * len(inner))

    e0, a0, g0, dd0 = energy(x0, True)
    r = so.minimize(energy, x0, method='L-BFGS-B', options=dict(maxiter=int(os.environ.get('MAXIT', 40)), maxfun=int(os.environ.get('MAXFUN', 3000))), bounds=[(-0.6, 0.6)] * len(x0))
    e1, a1, g1, dd1 = energy(r.x, True)
    w0 = max(a0.max() - 4, 46 - g0.min(), g0.max() - 134); w1 = max(a1.max() - 4, 46 - g1.min(), g1.max() - 134)
    covok = True if dd0 is None else not np.any((dd1 > thr[sv]) & (dd0 <= thr[sv]))
    if e1 < e0 - 1e-6 and (w1 <= w0 + 1e-6 or os.environ.get('TARGET_PTS')) and w1 <= max(w0, 0) + 1e-6 and covok:
        # full local coverage validation: every source vertex in the patch region vs the patch quads (+2 rings), before / after
        pq2 = set(pq.tolist())
        for _ in range(2): pq2 |= set(QQ[list(pq2)].indices.tolist())
        Ql = Q[sorted(pq2)]; Tl = np.r_[Ql[:, [0, 1, 2]], Ql[:, [0, 2, 3]]]; sva = np.array(cKDTree(G.V).query_ball_point(cen, rad + 0.3), int)
        Vn = V.copy(); Vn[inner] = place(r.x)
        if len(sva):
            db = np.sqrt(igl.point_mesh_squared_distance(G.V[sva], V, Tl)[0]); da = np.sqrt(igl.point_mesh_squared_distance(G.V[sva], Vn, Tl)[0])
            if np.any((da > thr[sva]) & (da > db + 1e-5)): continue
        V[:] = Vn; acc += 1
    if c % 20 == 0: print('cluster', c, 'of', nc, 'accepted', acc, flush=True)
asp, ang = qmetrics(V[Q]); print('after: aspect>4 non-tip', int(((asp > 4) & ~TIP).sum()), 'angle out', int(((ang.min(1) < 45) | (ang.max(1) > 135)).sum()))
fi, bc, _ = G.embed(V); z['V'] = V; z['tri'] = fi; z['bc'] = bc; np.savez_compressed(OUT, **z)
