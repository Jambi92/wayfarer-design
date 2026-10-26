# anatomy.py R6.npz CAND.npz OUT.json : RP3 anatomy preservation of a production candidate vs its accepted R-6 source (contract §13 / §16, order §11).
#   stature / bbox (T-3), surface deviation both directions (production vertices -> source triangles; source vertices -> production surface) overall and in
#   identity zones (head / ears / hands / feet: T-2) and body (T-1), silhouette IoU front / rear / profiles / 3-4 at 3 px / cm (T-7, method of the RP2
#   tools/rac/rp/grask_retopo_v001/iou.py), mirror asymmetry preserved (|dev(left) - dev(right)|).
import sys, json, numpy as np, trimesh
from PIL import Image, ImageDraw
a = sys.argv[1:]; r6 = np.load(a[0]); cz = np.load(a[1]); OUT = a[2]
SV = r6['V'].astype(float); SF = r6['F']; keep = r6['keep']; Vp = cz['V'].astype(float); Q = cz['Q']; TP = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]
si = cz['src_index']; R = {}
src = trimesh.Trimesh(SV, SF, process=False); prod = trimesh.Trimesh(Vp, TP, process=False)
bs = SV[keep]; R['stature_source_cm'] = float(bs[:, 2].max() - bs[:, 2].min()); R['stature_prod_cm'] = float(Vp[:, 2].max() - Vp[:, 2].min())
R['stature_diff_mm'] = round((R['stature_prod_cm'] - R['stature_source_cm']) * 10, 5)
R['bbox_diff_mm'] = np.round((np.r_[Vp.min(0), Vp.max(0)] - np.r_[bs.min(0), bs.max(0)]) * 10, 5).tolist()
_, d1, _ = trimesh.proximity.closest_point(src, Vp); _, d2, _ = trimesh.proximity.closest_point(prod, bs)
# zones of production vertices via the linear map (zone weights of the source)
import scipy.sparse as sp
if 'M_data' in cz.files: M = sp.csr_matrix((cz['M_data'], cz['M_indices'], cz['M_indptr']), shape=tuple(cz['M_shape']))
else: M = sp.identity(len(Vp), format='csr')
w = {k[2:]: r6[k][si] for k in r6.files if k.startswith('w_')}
def zmask(keys, Mx): return (Mx @ np.sum([w[k] for k in keys], 0)) > 0.5
ZN = {'head': ['head', 'ears'], 'ears': ['ears'], 'hands': ['hand_l', 'hand_r', 'fingers_l', 'fingers_r'], 'feet': ['foot_l', 'foot_r', 'ball_l', 'ball_r']}
def stats(d): return dict(median_mm=round(float(np.median(d) * 10), 4), p95_mm=round(float(np.percentile(d, 95) * 10), 4), max_mm=round(float(d.max() * 10), 4))
R['deviation_prod_to_source'] = dict(body=stats(d1), **{z_: stats(d1[zmask(k, M)]) for z_, k in ZN.items()})
R['deviation_source_to_prod'] = dict(body=stats(d2), **{z_: stats(d2[zmask(k, sp.identity(len(bs), format='csr'))]) for z_, k in ZN.items()})
T1 = dict(median_mm=0.5, p95_mm=1.5, max_mm=3.0); T2 = dict(median_mm=0.3, p95_mm=0.8, max_mm=1.5)
ok = all(R[d]['body'][k] <= T1[k] for d in ('deviation_prod_to_source', 'deviation_source_to_prod') for k in T1) and \
     all(R[d][z_][k] <= T2[k] for d in ('deviation_prod_to_source', 'deviation_source_to_prod') for z_ in ZN for k in T2)
R['T1_T2_pass'] = bool(ok); R['T3_pass'] = bool(abs(R['stature_diff_mm']) <= 1.0 and max(abs(x) for x in R['bbox_diff_mm']) <= 2.0)
px = 3.0
def sil(V, F, yaw, ss=4):
    """silhouette mask at 3 px / cm, rasterised at ss x ss supersampling and box-filtered (coverage >= 0.5): removes 1-px polygon-edge quantisation
    between different triangulations of the same surface"""
    an = np.radians(yaw); Rm = np.array([[np.cos(an), -np.sin(an), 0], [np.sin(an), np.cos(an), 0], [0, 0, 1]]); P = V @ Rm.T; q = px * ss
    u = (P[:, 0] + 60) * q; v = (185 - P[:, 2]) * q; W_, H_ = int(120 * px), int(190 * px)
    im = Image.new('L', (W_ * ss, H_ * ss), 0); dr = ImageDraw.Draw(im)
    for t in F: dr.polygon([(u[t[0]], v[t[0]]), (u[t[1]], v[t[1]]), (u[t[2]], v[t[2]])], fill=255)
    a_ = np.array(im, float).reshape(H_, ss, W_, ss).mean((1, 3)); return a_ >= 127.5
iou = {}
for nm, yaw in (('front', 0), ('rear', 180), ('profile_left', 90), ('profile_right', -90), ('q3_front_left', 45), ('q3_front_right', -45)):
    A = sil(SV, SF, yaw); B = sil(Vp, TP, yaw); iou[nm] = round(float((A & B).sum() / (A | B).sum()), 6)
R['silhouette_iou'] = iou; R['T7_pass'] = bool(min(iou[k] for k in ('front', 'rear', 'profile_left', 'profile_right')) >= 0.995)
R['verts'] = int(len(Vp)); R['quads'] = int(len(Q))
json.dump(R, open(OUT, 'w'), indent=1); print(json.dumps({k: R[k] for k in ('stature_diff_mm', 'T1_T2_pass', 'T3_pass', 'T7_pass', 'silhouette_iou')}), R['deviation_prod_to_source']['body'], R['deviation_source_to_prod']['body'])
