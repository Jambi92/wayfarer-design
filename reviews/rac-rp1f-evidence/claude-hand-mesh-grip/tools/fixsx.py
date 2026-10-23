# fixsx.py (bpy python) -- IN.npz PAIRS.npy OUT.npz [rings] [iters] [target_npz_fmt]
# Local self-intersection repair: vertices of the intersecting quads (+ k rings) are Laplacian-smoothed in small
# steps (optionally re-projected to a target surface), the region is re-tested after each round, rings grow if needed.
import sys, numpy as np, json
import bpy
from mathutils.bvhtree import BVHTree
import scipy.sparse as sp, igl
a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
z = np.load(a[0]); pr = np.load(a[1]); outf = a[2]; K = int(a[3]) if len(a) > 3 else 2; IT = int(a[4]) if len(a) > 4 else 10
V = z['V'].astype(np.float64).copy(); Q = z['Q']; n = len(V)
E = np.vstack([Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]])
A = sp.coo_matrix((np.ones(len(E)), (E[:, 0], E[:, 1])), shape=(n, n)); A = ((A + A.T) > 0).astype(float).tocsr(); deg = np.asarray(A.sum(1)).ravel()
vq = sp.coo_matrix((np.ones(Q.size), (Q.ravel(), np.repeat(np.arange(len(Q)), 4))), shape=(n, len(Q))).tocsr()
tg = None
if len(a) > 5:
    T = np.load(a[5]); tg = (T['V'], T['F'])
def region_sx(V, qs):
    t = BVHTree.FromPolygons(V.tolist(), Q[qs].tolist(), all_triangles=False, epsilon=0.0)
    p = np.array(t.overlap(t), int).reshape(-1, 2); p = p[p[:, 0] < p[:, 1]]
    if len(p): A_ = Q[qs][p[:, 0]]; B_ = Q[qs][p[:, 1]]; p = p[~(A_[:, :, None] == B_[:, None, :]).any((1, 2))]
    return qs[p] if len(p) else p
cur = pr; rnd = 0
while len(cur) and rnd < 12:
    vs = np.zeros(n, bool); vs[np.unique(Q[cur.ravel()])] = True
    for _ in range(K + rnd // 3): vs = vs | (A @ vs.astype(float) > 0)
    mv = np.where(vs)[0]
    for it in range(IT):
        L = (A[mv] @ V) / deg[mv][:, None] - V[mv]; V[mv] += 0.5 * L
    if tg is not None:
        _, _, cp = igl.point_mesh_squared_distance(V[mv], tg[0], tg[1]); V[mv] = cp
    # region test around the moved set
    c = V[mv].mean(0); r = np.linalg.norm(V[mv] - c, axis=1).max() + 1.0
    qs = np.where(np.linalg.norm(V[Q].mean(1) - c, axis=1) < r)[0]
    cur = region_sx(V, qs); rnd += 1
    print('round', rnd, 'moved verts', len(mv), 'remaining pairs', len(cur), flush=True)
np.savez(outf, V=V, **{k: z[k] for k in z.files if k != 'V'})
print(json.dumps(dict(remaining=int(len(cur)), rounds=rnd)))
