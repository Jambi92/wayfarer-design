# RM-OT-05AB1: evaluate a weight set on the cp2 rig WITHOUT Blender (exact linear-blend reproduction of the Armature modifier,
# verified to 0.0003 mm against the cp2 evaluated mesh). Reports self-intersecting faces (pymeshlab, welded), flipped faces vs
# rest, and where they are. Diagnostic preview only; the checkpoint result itself is produced by Blender's Armature modifier.
# Usage: python3 ab1_preview.py RIG_cp2.npz WEIGHTS.npz OUT.json [OUT_X.npz]
import sys, json, numpy as np, pymeshlab
from scipy.cluster.hierarchy import fcluster, linkage
rp, wp, out = sys.argv[1:4]; d = np.load(rp); V = d['V']; F = d['F']; M = d['M']
W = np.load(wp)['W'].astype(np.float64); W /= W.sum(1, keepdims=True)
Vh = np.c_[V, np.ones(len(V))]; X = np.zeros_like(V)
for i in range(len(M)): X += W[:, i:i + 1] * (Vh @ M[i].T)[:, :3]
def selfint(P):
    key, inv = np.unique(np.round(P * 100, 4), axis=0, return_inverse=True); inv = inv.ravel()
    ms = pymeshlab.MeshSet(); ms.add_mesh(pymeshlab.Mesh(key, inv[F])); ms.compute_selection_by_self_intersections_per_face()
    return np.where(ms.current_mesh().face_selection_array())[0]
def fn(P):
    n = np.cross(P[F[:, 1]] - P[F[:, 0]], P[F[:, 2]] - P[F[:, 0]]); return n / np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-15)
si = selfint(X); dot = (fn(V) * fn(X)).sum(1); flip = np.where(dot < 0)[0]
def clusters(fi):
    if len(fi) == 0: return []
    c = V[F[fi]].mean(1) * 100
    if len(fi) == 1: return [dict(faces=1, rest_centre_cm=np.round(c[0], 1).tolist())]
    cl = fcluster(linkage(c, 'single'), 3.0, 'distance')
    return [dict(faces=int((cl == k).sum()), rest_centre_cm=np.round(c[cl == k].mean(0), 1).tolist()) for k in np.unique(cl)]
R = dict(self_intersecting_faces=int(len(si)), self_intersection_clusters=clusters(si), flipped_faces=int(len(flip)), flipped_clusters=clusters(flip),
         rotated_over_60deg=int((dot < 0.5).sum()), self_intersecting_face_ids=si.tolist(), flipped_face_ids=flip.tolist())
json.dump(R, open(out, 'w'), indent=1); print(json.dumps({k: v for k, v in R.items() if not k.endswith('_ids')}))
if len(sys.argv) > 4: np.savez(sys.argv[4], V=X.astype(np.float32), F=F)
