# untangle.py (bpy) IN.npz OUT.npz [step_cm] [maxit] [protect.npy]: resolve residual local self-intersections by moving the
# vertices of every intersecting quad pair inward along their vertex normals in small steps (both sheets retreat), with a light
# Laplacian smooth of the moved set; repeats until no pair remains. Symmetric if 'mir' is present.
import sys, numpy as np, bpy, json
from mathutils.bvhtree import BVHTree
a = sys.argv[sys.argv.index('--') + 1:]
z = dict(np.load(a[0])); V = z['V'].copy(); Q = z['Q']; step = float(a[2]) if len(a) > 2 else 0.02; MAXIT = int(a[3]) if len(a) > 3 else 60
mir = z.get('mir'); n = len(V)
T = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]
vol = np.einsum('ij,ij->i', V[T[:, 0]], np.cross(V[T[:, 1]], V[T[:, 2]])).sum(); sgn = 1.0 if vol > 0 else -1.0
import scipy.sparse as sp
E = np.unique(np.sort(np.vstack([Q[:, [i, (i + 1) % 4]] for i in range(4)]), 1), axis=0)
A = sp.coo_matrix((np.ones(len(E)), (E[:, 0], E[:, 1])), shape=(n, n)); A = (A + A.T).tocsr(); deg = np.asarray(A.sum(1)).ravel()
def pairs(V):
    t = BVHTree.FromPolygons(V.tolist(), Q.tolist(), all_triangles=False, epsilon=0.0)
    pr = np.array(t.overlap(t), int).reshape(-1, 2); pr = pr[pr[:, 0] < pr[:, 1]]
    if len(pr): X = Q[pr[:, 0]]; Y = Q[pr[:, 1]]; pr = pr[~(X[:, :, None] == Y[:, None, :]).any((1, 2))]
    return pr
def vn(V):
    fn = np.cross(V[T[:, 1]] - V[T[:, 0]], V[T[:, 2]] - V[T[:, 0]]); out = np.zeros_like(V)
    for k in range(3): np.add.at(out, T[:, k], fn)
    return sgn * out / (np.linalg.norm(out, axis=1)[:, None] + 1e-30)
tot = np.zeros(n)
for it in range(MAXIT):
    pr = pairs(V)
    if not len(pr): break
    mv = np.zeros(n, bool); mv[np.unique(Q[pr].ravel())] = True
    N_ = vn(V); V[mv] -= step * N_[mv]; tot[mv] += step
    L = (A @ V) / deg[:, None] - V; V[mv] += 0.3 * L[mv]
    if mir is not None:
        m = mir >= 0; V[m] = 0.5 * (V[m] + V[mir[m]] * np.array([-1, 1, 1])); s_ = m & (mir == np.arange(n)); V[s_, 0] = 0
    print('it', it, 'pairs', len(pr), flush=True)
pr = pairs(V); print(json.dumps(dict(remaining=int(len(pr)), moved=int((tot > 0).sum()), max_retreat_mm=float(tot.max() * 10))))
z['V'] = V; np.savez(a[1], **z)
