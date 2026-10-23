# clearance2.py MESH.npz OUT.npy : proximity clearance (cm). For r in a ladder, q = p + n r; if the mesh comes closer to q than
# 0.75 r, another sheet is within about 2 r of p in the outward half-space -> clearance = r.
import sys, numpy as np, igl
z = np.load(sys.argv[1]); V = z['V']; Q = z['Q']; T = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]
vol = np.einsum('ij,ij->i', V[T[:, 0]], np.cross(V[T[:, 1]], V[T[:, 2]])).sum(); sgn = 1.0 if vol > 0 else -1.0
fn = np.cross(V[T[:, 1]] - V[T[:, 0]], V[T[:, 2]] - V[T[:, 0]]); vn = np.zeros_like(V)
for k in range(3): np.add.at(vn, T[:, k], fn)
vn = sgn * vn / (np.linalg.norm(vn, axis=1)[:, None] + 1e-30)
c = np.full(len(V), 99.0)
for r in (0.8, 0.4, 0.2, 0.1, 0.05):
    d = np.sqrt(igl.point_mesh_squared_distance(V + vn * r, V, T)[0]); c = np.where(d < 0.75 * r, r, c)
np.save(sys.argv[2], c); print({r: int((c <= r).sum()) for r in (0.05, 0.1, 0.2, 0.4, 0.8)})
