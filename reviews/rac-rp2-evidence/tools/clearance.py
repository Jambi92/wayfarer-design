# clearance.py (bpy) MESH.npz OUT.npy : outward clearance per vertex (ray along the outward vertex normal to the mesh itself), cm
import sys, numpy as np, bpy, mathutils
from mathutils.bvhtree import BVHTree
a = sys.argv[sys.argv.index('--') + 1:]
z = np.load(a[0]); V = z['V']; Q = z['Q']; T = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]
vol = np.einsum('ij,ij->i', V[T[:, 0]], np.cross(V[T[:, 1]], V[T[:, 2]])).sum(); sgn = 1.0 if vol > 0 else -1.0
fn = np.cross(V[T[:, 1]] - V[T[:, 0]], V[T[:, 2]] - V[T[:, 0]]); vn = np.zeros_like(V)
for k in range(3): np.add.at(vn, T[:, k], fn)
vn = sgn * vn / (np.linalg.norm(vn, axis=1)[:, None] + 1e-30)
bvh = BVHTree.FromPolygons(V.tolist(), Q.tolist(), all_triangles=False)
c = np.full(len(V), 99.0)
for i in range(len(V)):
    p = mathutils.Vector(V[i] + vn[i] * 0.005); loc, nrm, idx, dist = bvh.ray_cast(p, mathutils.Vector(vn[i]), 10.0)
    if loc is not None: c[i] = dist
np.save(a[1], c); print('clearance <0.5cm:', int((c < 0.5).sum()), '<0.2cm:', int((c < 0.2).sum()))
