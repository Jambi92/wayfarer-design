# sa_local.py IN.npz OUT.npz : bounded LOCAL source-driven sliding + shape repair on the full cage (order 236dddc §3-§9). Topology unchanged.
#   active source = working-source vertices farther than TH from the cage; free cage vertices = within RAD of them (+ vertices of T-4 failing quads and their
#   1-ring when SHAPE=1); everything else (incl. the accepted tail module) is pinned. Loop: coverage pull (active sources -> their closest cage triangle),
#   tiny tangential smoothing, parallelogram shape rule on failing quads, reprojection onto the local source patch (normal-consistent, step-limited:
#   a projection that jumps > 4 mm is rejected -> no crossing of finger / toe / lip gaps). Output keeps the face list (c1 / c2 shared topology).
import sys, os, numpy as np, igl, scipy.sparse as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_geo as G
from scipy.spatial import cKDTree
IN, OUT = sys.argv[1:3]; TH = float(os.environ.get('TH', 0.10)); RAD = float(os.environ.get('RAD', 2.5)); IT = int(os.environ.get('IT', 80)); SHAPE = os.environ.get('SHAPE', '1') == '1'
z = dict(np.load(IN)); Q = z['Q']; nb = int(z['n_body']); V = (z['bc'][:, :, None] * G.V[G.F[z['tri']]]).sum(1); nv = len(V); T = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]
pin = np.zeros(nv, bool); pin[nb:] = True; pin[z['tail_ring']] = True; pin[z['pinned']] = True
E = np.unique(np.sort(np.r_[Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]], 1), axis=0)
A = sp.coo_matrix((np.ones(2 * len(E)), (np.r_[E[:, 0], E[:, 1]], np.r_[E[:, 1], E[:, 0]])), shape=(nv, nv)).tocsr(); deg = np.asarray(A.sum(1)).ravel()
def shape_bad(P):
    sd = np.stack([np.linalg.norm(P[Q[:, (k + 1) % 4]] - P[Q[:, k]], axis=1) for k in range(4)], 1); asp = sd.max(1) / np.maximum(sd.min(1), 1e-9); ang = []
    for k in range(4):
        u1 = P[Q[:, (k - 1) % 4]] - P[Q[:, k]]; u2 = P[Q[:, (k + 1) % 4]] - P[Q[:, k]]; ang.append(np.degrees(np.arccos(np.clip((u1 * u2).sum(1) / (np.linalg.norm(u1, axis=1) * np.linalg.norm(u2, axis=1) + 1e-12), -1, 1))))
    ang = np.stack(ang, 1); return (asp > 4) | (ang.min(1) < 45) | (ang.max(1) > 135), asp
d2, _, _ = igl.point_mesh_squared_distance(G.V, V, T); act = np.nonzero(np.sqrt(d2) > TH)[0]
free = np.zeros(nv, bool)
if len(act): free[np.unique(np.concatenate(cKDTree(V).query_ball_point(G.V[act], RAD)))] = True
bq, _ = shape_bad(V)
if SHAPE:
    m = np.zeros(nv, bool); m[Q[bq].ravel()] = True
    for _ in range(2): m |= (A @ m.astype(float)) > 0
    free |= m
free &= ~pin; fi_ = np.nonzero(free)[0]
print('active sources', len(act), 'free cage vertices', len(fi_), 'bad quads', int(bq.sum()), flush=True)
# local source patch (faces within 3 cm of the free vertices) + its AABB
sv = np.unique(np.concatenate(cKDTree(G.V).query_ball_point(V[fi_], 3.0))); fm = np.isin(G.F, sv).all(1); FS = G.F[fm]
NS = igl.per_face_normals(G.V, FS, np.array([0, 0, 1.0]))
def project(P, prev):
    _, f_, cp = igl.point_mesh_squared_distance(P, G.V, FS)
    jump = np.linalg.norm(cp - prev, axis=1) > 0.4; cp[jump] = prev[jump]; return cp
for it in range(IT):
    Vf = V.copy()
    # coverage pull
    d2, ti, cp = igl.point_mesh_squared_distance(G.V[act], V, T); far = np.sqrt(d2) > TH * 0.5
    acc = np.zeros_like(V); cnt = np.zeros(nv)
    tv = T[ti[far]]; dv = G.V[act[far]] - cp[far]
    for k in range(3): np.add.at(acc, tv[:, k], dv); np.add.at(cnt, tv[:, k], 1)
    D = np.where(cnt[:, None] > 0, acc / np.maximum(cnt, 1)[:, None], 0)
    N = np.nan_to_num(igl.per_vertex_normals(V, T))
    L = (A @ V) / deg[:, None] - V; L -= (L * N).sum(1)[:, None] * N
    # parallelogram rule on failing quads: vertex -> mean over its bad quads of (a + c - b)
    bq, asp = shape_bad(V); S = np.zeros_like(V); sc = np.zeros(nv)
    for k in range(4):
        q = Q[bq]; v = q[:, k]; a = q[:, (k + 1) % 4]; b = q[:, (k + 2) % 4]; c = q[:, (k + 3) % 4]
        np.add.at(S, v, V[a] + V[c] - V[b] - V[v]); np.add.at(sc, v, 1)
    Sd = np.where(sc[:, None] > 0, S / np.maximum(sc, 1)[:, None], 0); Sd -= (Sd * N).sum(1)[:, None] * N
    wl = np.where(cnt > 0, 0.03, 0.15)[:, None]; ws = 0.25 if SHAPE else 0.0
    Vt = V + wl * L + 1.0 * D + ws * Sd
    Vt[fi_] = project(Vt[fi_], V[fi_]); V[fi_] = Vt[fi_]
    if it % 10 == 0 or it == IT - 1:
        dd = np.sqrt(igl.point_mesh_squared_distance(G.V[act], V, T)[0]) * 10; print(it, 'active max %.2f mm p99 %.2f' % (dd.max(), np.percentile(dd, 99)), 'bad quads', int(bq.sum()), 'aspect>4', int((asp > 4).sum()), flush=True)
fi2, bc2, dist = G.embed(V); z['V'] = V; z['tri'] = fi2; z['bc'] = bc2
np.savez_compressed(OUT, **z); print('saved', OUT, 'off-surface max %.4f mm' % (dist.max() * 10))
