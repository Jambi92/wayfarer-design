# extvis.py (bpy) MESH.npz OUT.npz [nrays] : exterior visibility of triangle centroids and vertices: a point is exterior-visible
# if at least one of nrays rays from (point + outward normal * 0.2 mm), over the outward hemisphere, escapes without hitting the mesh.
import sys, numpy as np, bpy, mathutils
from mathutils.bvhtree import BVHTree
a = sys.argv[sys.argv.index('--') + 1:]; NR = int(a[2]) if len(a) > 2 else 96
z = np.load(a[0]); V = z['V'].astype(float); Q = z['Q']; T = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]
vol = np.einsum('ij,ij->i', V[T[:, 0]], np.cross(V[T[:, 1]], V[T[:, 2]])).sum(); sgn = 1.0 if vol > 0 else -1.0
fn = np.cross(V[T[:, 1]] - V[T[:, 0]], V[T[:, 2]] - V[T[:, 0]]); tn = sgn * fn / np.linalg.norm(fn, axis=1)[:, None]
vn = np.zeros_like(V)
for k in range(3): np.add.at(vn, T[:, k], fn)
vn = sgn * vn / (np.linalg.norm(vn, axis=1)[:, None] + 1e-30)
bvh = BVHTree.FromPolygons(V.tolist(), T.tolist(), all_triangles=True)
rng = np.random.default_rng(0); D = rng.normal(size=(NR, 3)); D /= np.linalg.norm(D, axis=1)[:, None]
def vis(P, N):
    out = np.zeros(len(P), bool)
    for i in range(len(P)):
        p = P[i] + N[i] * 0.02; dd = D[(D @ N[i]) > 0.05]
        for d in dd:
            if bvh.ray_cast(mathutils.Vector(p), mathutils.Vector(d), 1000.0)[0] is None: out[i] = True; break
    return out
tv = vis(V[T].mean(1), tn); vv = vis(V, vn)
np.savez(a[1], tri=tv, vert=vv); print('triangles not exterior-visible', int((~tv).sum()), 'vertices', int((~vv).sum()))
