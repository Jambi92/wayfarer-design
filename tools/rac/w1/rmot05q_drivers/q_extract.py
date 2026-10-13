# RM-OT-05Q source provenance + F1 extraction (reproducible, no field / remesh / mirror).
#  - loads base.glb (hash checked), the single textured mesh (trimesh, default load);
#  - global islands: vertices merged at 1e-5 (rounding) -> face connectivity components (05M/05N 'lab');
#  - F1 = the face-index list committed in reviews/rac-rmot05q-evidence/source/F1_face_indices.npz. It was recorded by
#    matching the 05N extraction (component 0 split at the F1/F2 contact slab, slab faces re-assigned to the nearest figure;
#    the slab bounds were not recorded in 05N, so the index list is the authoritative record of what F1 is);
#  - writes F1 in GLB units (untouched coordinates, original vertex order of the used vertices) and the RAC-frame working
#    copy with the documented 05N transform (rotation 180 deg about Z + scale 2.70634 + translation; NO mirroring).
# Usage: python3 q_extract.py --glb base.glb --faces F1_face_indices.npz --out OUTDIR
import argparse, hashlib, json, os, numpy as np, trimesh
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
ap = argparse.ArgumentParser(); ap.add_argument('--glb'); ap.add_argument('--faces'); ap.add_argument('--out'); a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
h = hashlib.sha256(open(a.glb, 'rb').read()).hexdigest(); assert h == '78ecfa87d169380ecb46ece3f0c0df3491d10e4547038a3c35c06df933f38a7b', h
m = list(trimesh.load(a.glb).geometry.values())[0]; V = np.asarray(m.vertices); F = np.asarray(m.faces)
q = np.round(V * 1e5).astype(np.int64); _, inv = np.unique(q, axis=0, return_inverse=True); inv = inv.ravel(); Fm = inv[F]; n = inv.max() + 1
A = sp.coo_matrix((np.ones(len(Fm) * 3), (np.r_[Fm[:, 0], Fm[:, 1], Fm[:, 2]], np.r_[Fm[:, 1], Fm[:, 2], Fm[:, 0]])), shape=(n, n))
nc, vl = connected_components(A, directed=False); flab = vl[Fm[:, 0]]
f1 = np.load(a.faces)['faces']; comp = np.unique(flab[f1])
sub = F[f1]; vi = np.unique(sub); mp = -np.ones(len(V), int); mp[vi] = np.arange(len(vi)); F1 = mp[sub]
G = V[vi]                                                           # GLB units, untouched
trimesh.Trimesh(G, F1, process=False).export(os.path.join(a.out, 'F1_glb_units.obj'))
W = np.c_[G[:, 0], -G[:, 2], G[:, 1]] * 100                         # 05N working orientation (x, -z, y) * 100
XC, FLOOR, CROWN = -76.1, float(W[:, 2].min()), 119.5; S = 229.0 / (CROWN - FLOOR)
R = np.c_[-(W[:, 0] - XC), -W[:, 1], W[:, 2] - FLOOR] * S
yc = float(np.median(R[(R[:, 2] > 140) & (R[:, 2] < 170), 1])); R[:, 1] -= yc
trimesh.Trimesh(R, F1, process=False).export(os.path.join(a.out, 'F1_rac_frame.obj'))
# working copy: UV-seam duplicate vertices welded (exactly coincident: merge distance 0), face order unchanged
qq = np.round(R * 1e4).astype(np.int64); _, first, winv = np.unique(qq, axis=0, return_index=True, return_inverse=True); winv = winv.ravel()
merge_dist = float(np.abs(R - R[first][winv]).max())
trimesh.Trimesh(R[first], winv[F1], process=False).export(os.path.join(a.out, 'F1_working.obj'))
np.save(os.path.join(a.out, 'F1_weld_map.npy'), winv)
# per-component face counts of the global islands, and which island F1 came from
counts = {int(c): int((flab == c).sum()) for c in np.unique(flab)}
rec = dict(glb=a.glb, glb_sha256=h, glb_bytes=os.path.getsize(a.glb), glb_vertices=int(len(V)), glb_faces=int(len(F)), islands=nc, island_face_counts=counts,
           F1_faces=int(len(f1)), F1_vertices=int(len(vi)), F1_from_islands=comp.tolist(), F1_face_index_sha256=hashlib.sha256(f1.astype(np.int64).tobytes()).hexdigest(),
           working_copy=dict(file='F1_working.obj', vertices=int(len(first)), weld_merge_distance_cm=merge_dist, weld_map='F1_weld_map.npy (rac-frame vertex -> working vertex)'),
           rac_transform=dict(steps='W=(x,-z,y)*100; X=-(Wx-XC)*S; Y=-Wy*S - yshift; Z=(Wz-floor)*S', XC=XC, floor=FLOOR, crown_glb_work_units=CROWN, S=S, yshift=yc, mirrored=False),
           note='F1 is face-identical to 05N c0s_1 (GO-RD0-SOURCE); the 05N 229 cm crown assumption is a scale convention, not a measurement')
json.dump(rec, open(os.path.join(a.out, 'extraction_record.json'), 'w'), indent=1); print(json.dumps({k: v for k, v in rec.items() if k != 'island_face_counts'}, indent=1))
