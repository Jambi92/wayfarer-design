# face_identity.py CAND.npz IDENTITY_R6.npz PRE_IDENTITY_R6.npz OUT.json : race identity gate helper (MPFB Family Propagation Standard v1, §8).
# Proves that a family-base realization keeps the race's accepted identity face (e.g. Skarn C1R) and has not regressed toward the pre-identity /
# generic face:
#   face region   = hm08 body vertices with head weight > 0.5, no ear weight, in front of the ear centroid (the anterior face / jaw / cheek region);
#   pre-identity source aligned to the identity source by a rigid (Kabsch) fit on the NON-face head vertices (cranium + ears);
#   identity signal  = |identity - aligned pre-identity| on the face hm08 vertices;
#   family -> identity source  and  family -> aligned pre-identity source: distances of the production face vertices to each source surface.
# Identity holds when the family face lies on the identity source (median ~0) and the pre-identity distance stays at the size of the identity signal.
import sys, json, numpy as np, trimesh, scipy.sparse as sp
cz = np.load(sys.argv[1]); r1 = np.load(sys.argv[2]); r0 = np.load(sys.argv[3]); OUT = sys.argv[4]
si = cz['src_index']; M = sp.csr_matrix((cz['M_data'], cz['M_indices'], cz['M_indptr']), shape=tuple(cz['M_shape'])); Vp = cz['V'].astype(float)
V1 = r1['V'].astype(float); V0 = r0['V'].astype(float); h1 = V1[si]; h0 = V0[si]
wh = r1['w_head'][si]; we = r1['w_ears'][si]; ear_y = h1[we > 0.5, 1].mean()
face = (wh > 0.5) & (we == 0) & (h1[:, 1] > ear_y); cran = (wh > 0.5) & ~face
def kabsch(P, Q):
    pc, qc = P.mean(0), Q.mean(0); U, S, Vt = np.linalg.svd((P - pc).T @ (Q - qc)); D = np.diag([1, 1, np.sign(np.linalg.det(Vt.T @ U.T))]); R = Vt.T @ D @ U.T
    return R, qc - pc @ R.T
R, t = kabsch(h0[cran], h1[cran]); V0a = V0 @ R.T + t; h0a = h0 @ R.T + t
sig = np.linalg.norm(h1[face] - h0a[face], axis=1)
pf = (M @ face.astype(float)) > 0.5
s1 = trimesh.Trimesh(V1, r1['F'], process=False); s0 = trimesh.Trimesh(V0a, r0['F'], process=False)
_, d1, _ = trimesh.proximity.closest_point(s1, Vp[pf]); _, d0, _ = trimesh.proximity.closest_point(s0, Vp[pf])
st = lambda d: dict(median=round(float(np.median(d) * 10), 4), p95=round(float(np.percentile(d, 95) * 10), 4), max=round(float(d.max() * 10), 4))
res = dict(face_vertices_hm08=int(face.sum()), face_vertices_production=int(pf.sum()), alignment_rms_mm=round(float(np.sqrt(((h0a[cran] - h1[cran]) ** 2).sum(1).mean()) * 10), 4),
           identity_signal_mm=dict(mean=round(float(sig.mean() * 10), 4), p95=round(float(np.percentile(sig, 95) * 10), 4), max=round(float(sig.max() * 10), 4)),
           family_face_to_identity_source_mm=st(d1), family_face_to_pre_identity_source_mm=st(d0),
           identity_preserved=bool(np.median(d1) * 10 < 0.1 and np.median(d0) > 0.5 * np.median(sig)),
           definition='face = hm08 head weight > 0.5, no ear weight, anterior of the ear centroid; pre-identity rigidly aligned on the remaining head vertices')
json.dump(res, open(OUT, 'w'), indent=1); print(json.dumps(res))
