# untangle_sub.py (bpy) IN.npz OUT.npz [step_cm] [maxit] : like untangle.py but the intersection test runs on the level-2 bilinear
# subdivision (what the production is built from); offending base quads (parent = child // 16) retreat along base vertex normals.
import sys, numpy as np, bpy, json
from mathutils.bvhtree import BVHTree
sys.path.insert(0, '/tmp/claude-0/rp2/tools'); from subdiv import subdivide_levels
a = sys.argv[sys.argv.index('--') + 1:]
z = dict(np.load(a[0])); V = z['V'].copy(); Q = z['Q']; step = float(a[2]) if len(a) > 2 else 0.005; MAXIT = int(a[3]) if len(a) > 3 else 60
mir = z.get('mir'); n = len(V)
Q2, n2, S, _ = subdivide_levels(Q, n, 2, None); S = S.tocsr()
T = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]
vol = np.einsum('ij,ij->i', V[T[:, 0]], np.cross(V[T[:, 1]], V[T[:, 2]])).sum(); sgn = 1.0 if vol > 0 else -1.0
import scipy.sparse as sp
E = np.unique(np.sort(np.vstack([Q[:, [i, (i + 1) % 4]] for i in range(4)]), 1), axis=0)
A = sp.coo_matrix((np.ones(len(E)), (E[:, 0], E[:, 1])), shape=(n, n)); A = (A + A.T).tocsr(); deg = np.asarray(A.sum(1)).ravel()
def pairs(P2):
    t = BVHTree.FromPolygons(P2.tolist(), Q2.tolist(), all_triangles=False, epsilon=0.0)
    pr = np.array(t.overlap(t), int).reshape(-1, 2); pr = pr[pr[:, 0] < pr[:, 1]]
    if len(pr): X = Q2[pr[:, 0]]; Y = Q2[pr[:, 1]]; pr = pr[~(X[:, :, None] == Y[:, None, :]).any((1, 2))]
    return pr
def vn(V):
    fn = np.cross(V[T[:, 1]] - V[T[:, 0]], V[T[:, 2]] - V[T[:, 0]]); out = np.zeros_like(V)
    for k in range(3): np.add.at(out, T[:, k], fn)
    return sgn * out / (np.linalg.norm(out, axis=1)[:, None] + 1e-30)
tot = np.zeros(n)
for it in range(MAXIT):
    pr = pairs(S @ V)
    if not len(pr): break
    bq = np.unique(pr.ravel() // 16); mv = np.zeros(n, bool); mv[np.unique(Q[bq].ravel())] = True
    N_ = vn(V); V[mv] -= step * N_[mv]; tot[mv] += step
    L = (A @ V) / deg[:, None] - V; V[mv] += 0.3 * L[mv]
    if mir is not None:
        m = mir >= 0; V[m] = 0.5 * (V[m] + V[mir[m]] * np.array([-1, 1, 1])); s_ = m & (mir == np.arange(n)); V[s_, 0] = 0
    print('it', it, 'L2 pairs', len(pr), flush=True)
pr = pairs(S @ V); print(json.dumps(dict(remaining_L2=int(len(pr)), moved=int((tot > 0).sum()), max_retreat_mm=float(tot.max() * 10))))
z['V'] = V; np.savez(a[1], **z)
