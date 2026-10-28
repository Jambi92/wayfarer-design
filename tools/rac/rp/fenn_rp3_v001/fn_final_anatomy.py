# fn_final_anatomy.py R6.npz PROD.npz OUT.json : order 6d2eadc §8 -- Standard v1 anatomy preservation (anatomy.py: T-1 / T-2 / T-3 / T-7) of a Fenn
# production body against its accepted R-6 source, with the accepted ear branch EXCLUDED on both sides. The R-6 source still carries the MPFB human
# auricle (non-final source anatomy); the production body carries the accepted E2 ear branch (topology v002), so the external ear is not a
# source-preservation zone any more -- it is gated by the ear final gate (ear_audit / ear_measure / ear_deform / probes).
#   production : branch vertices (part != v005: ear patch + transition ring) are excluded as measured points;
#   source     : vertices with w_ears > 0.05 (the hidden-ear rule) or within 1.0 cm of a production branch vertex are excluded as measured points;
#   distances are taken to the FULL other surface (no holes). T-1 body / T-2 identity zones (head without ears, hands, feet), same limits as anatomy.py;
#   T-3 stature / bbox on the full meshes; T-7 silhouettes of the full meshes (anatomy.py method, 3 px / cm, 4x supersampling) compared outside the ear
#   pixels (pixels covered by the source ear triangles or the production branch faces in that view). The unmasked anatomy.py result is reported beside it.
import sys, json, numpy as np, trimesh, scipy.sparse as sp
from scipy.spatial import cKDTree
from PIL import Image, ImageDraw
a = sys.argv[1:]; r6 = np.load(a[0]); cz = np.load(a[1]); OUT = a[2]
SV = r6['V'].astype(float); SF = r6['F']; keep = r6['keep']; Vp = cz['V'].astype(float); Q = cz['Q']; si = cz['src_index']; part = cz['part']
brv = part != 'v005'; brf = brv[Q].any(1); Qk = Q[~brf]; TPk = np.r_[Qk[:, [0, 1, 2]], Qk[:, [0, 2, 3]]]; TPa = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]
ear_s = r6['w_ears'] > 0.05; near = np.zeros(len(SV), bool); d_, _ = cKDTree(Vp[brv]).query(SV); near = d_ < 1.0
sx = ear_s | near | ~keep; SFk = SF[~sx[SF].any(1)]; R = dict(rule='ear branch excluded as measured points (production part != v005; source w_ears > 0.05 or within 1 cm of the branch); distances to the full other surface; T-7 compared outside the ear pixels',
                                                            excluded_production_vertices=int(brv.sum()), excluded_production_faces=int(brf.sum()), excluded_source_vertices=int((sx & keep).sum()))
src_k = trimesh.Trimesh(SV, SF, process=False); prod_k = trimesh.Trimesh(Vp, TPa, process=False)
SFe = SF[(ear_s | near)[SF].any(1)]; TPe = np.r_[Q[brf][:, [0, 1, 2]], Q[brf][:, [0, 2, 3]]]
bs = SV[keep]; R['stature_source_cm'] = float(bs[:, 2].max() - bs[:, 2].min()); R['stature_prod_cm'] = float(Vp[:, 2].max() - Vp[:, 2].min())
R['stature_diff_mm'] = round((R['stature_prod_cm'] - R['stature_source_cm']) * 10, 5)
R['bbox_diff_mm'] = np.round((np.r_[Vp.min(0), Vp.max(0)] - np.r_[bs.min(0), bs.max(0)]) * 10, 5).tolist()
pv = np.nonzero(~brv)[0]; sv = np.nonzero(keep & ~sx)[0]
_, d1, _ = trimesh.proximity.closest_point(src_k, Vp[pv]); _, d2, _ = trimesh.proximity.closest_point(prod_k, SV[sv])
M = sp.csr_matrix((cz['M_data'], cz['M_indices'], cz['M_indptr']), shape=tuple(cz['M_shape']))
w = {k[2:]: r6[k][si] for k in r6.files if k.startswith('w_')}; wfull = {k[2:]: r6[k] for k in r6.files if k.startswith('w_')}
ZN = {'head': ['head', 'ears'], 'hands': ['hand_l', 'hand_r', 'fingers_l', 'fingers_r'], 'feet': ['foot_l', 'foot_r', 'ball_l', 'ball_r']}
def stats(d): return dict(median_mm=round(float(np.median(d) * 10), 4), p95_mm=round(float(np.percentile(d, 95) * 10), 4), max_mm=round(float(d.max() * 10), 4), n=int(len(d)))
zp = {z_: ((M @ np.sum([w[k] for k in ks], 0)) > 0.5)[pv] for z_, ks in ZN.items()}; zs = {z_: (np.sum([wfull[k] for k in ks], 0) > 0.5)[sv] for z_, ks in ZN.items()}
R['deviation_prod_to_source'] = dict(body=stats(d1), **{z_: stats(d1[m]) for z_, m in zp.items()}); R['deviation_source_to_prod'] = dict(body=stats(d2), **{z_: stats(d2[m]) for z_, m in zs.items()})
T1 = dict(median_mm=0.5, p95_mm=1.5, max_mm=3.0); T2 = dict(median_mm=0.3, p95_mm=0.8, max_mm=1.5)
R['T1_pass'] = bool(all(R[d]['body'][k] <= T1[k] for d in ('deviation_prod_to_source', 'deviation_source_to_prod') for k in T1))
R['T2_pass'] = bool(all(R[d][z_][k] <= T2[k] for d in ('deviation_prod_to_source', 'deviation_source_to_prod') for z_ in ZN for k in T2)); R['T1_T2_pass'] = R['T1_pass'] and R['T2_pass']
R['T3_pass'] = bool(abs(R['stature_diff_mm']) <= 1.0 and max(abs(x) for x in R['bbox_diff_mm']) <= 2.0)
px = 3.0; ZT = max(185.0, float(np.ceil(SV[keep][:, 2].max() + 5))); XO = max(60.0, float(np.ceil(np.abs(SV[keep][:, :2]).max() + 10)))
def sil(V, F, yaw, ss=4):
    an = np.radians(yaw); Rm = np.array([[np.cos(an), -np.sin(an), 0], [np.sin(an), np.cos(an), 0], [0, 0, 1]]); P = V @ Rm.T; q = px * ss
    u = (P[:, 0] + XO) * q; v = (ZT - P[:, 2]) * q; W_, H_ = int(2 * XO * px), int((ZT + 5) * px)
    im = Image.new('L', (W_ * ss, H_ * ss), 0); dr = ImageDraw.Draw(im)
    for t in F: dr.polygon([(u[t[0]], v[t[0]]), (u[t[1]], v[t[1]]), (u[t[2]], v[t[2]])], fill=255)
    a_ = np.array(im, float).reshape(H_, ss, W_, ss).mean((1, 3)); return a_ >= 127.5
iou = {}
for nm, yaw in (('front', 0), ('rear', 180), ('profile_left', 90), ('profile_right', -90), ('q3_front_left', 45), ('q3_front_right', -45)):
    A = sil(SV, SF, yaw); B = sil(Vp, TPa, yaw); X_ = sil(SV, SFe, yaw) | sil(Vp, TPe, yaw); A &= ~X_; B &= ~X_; iou[nm] = round(float((A & B).sum() / (A | B).sum()), 6)
R['silhouette_iou'] = iou; R['T7_pass'] = bool(min(iou[k] for k in ('front', 'rear', 'profile_left', 'profile_right')) >= 0.995)
R['verts'] = int(len(Vp)); R['quads'] = int(len(Q))
json.dump(R, open(OUT, 'w'), indent=1); print(json.dumps({k: R[k] for k in ('stature_diff_mm', 'T1_T2_pass', 'T3_pass', 'T7_pass', 'silhouette_iou')}), R['deviation_prod_to_source']['body'], R['deviation_source_to_prod']['body'])
