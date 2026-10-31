# sa_surface_rep.py OUT.json : RP5 Saurin scale-surface comparison (order 53976fb §10 / §18) -- canonical unsurfaced base vs canonical surfaced W2 organism.
#   * per region: |surface delta| mean / p95 / max (mm) -- the canonical delta is normal-only float16 on the igl.upsample of the base (base vertices first);
#   * silhouette contribution: IoU of the surfaced vs the unsurfaced organism (front / profile, 3 px / cm, tail included) and the share of the delta above the
#     T-1 p95 capture tolerance (1.5 mm) -- what a cage that follows the base (not the scales) would miss in silhouette;
#   * spatial frequency: mean edge of the upsampled surface vs production cage edge (the scale relief period cannot be carried by a 4-10 mm cage);
#   * deformation-zone overlap: delta energy within the joint zones (12 cm of the elbow / wrist / knee / ankle / glenohumeral landmarks, 10 cm of the tail root).
import sys, json, os, numpy as np, igl
from scipy.spatial import cKDTree
from PIL import Image, ImageDraw
OUT = sys.argv[1]; W = '/tmp/claude-0/rt/sa'
b = np.load(W + '/src/saurin_w2_final_base.npz'); V = b['v'].astype(float); F = b['f'].astype(np.int64)
S = np.load(W + '/src/SA-M188_surfaced.npz'); VS = S['v'].astype(float); FS = S['f'].astype(np.int64)
d = np.load(W + '/src/saurin_w2_final_surface_delta.npz')['d'].astype(float); dm = np.linalg.norm(d, axis=1)
lab = np.load(W + '/lm/SA-M188_regions.npz')['label']; LM = json.load(open(W + '/lm/SA-M188_landmarks.json'))['landmarks']
nb = len(V); labS = np.empty(len(VS), dtype=lab.dtype); labS[:nb] = lab; _, nn = cKDTree(V).query(VS[nb:]); labS[nb:] = lab[nn]
res = dict(base_verts=nb, surfaced_verts=int(len(VS)), surfaced_tris=int(len(FS)), delta_max_mm=round(float(dm.max() * 10), 3), delta_mean_mm=round(float(dm.mean() * 10), 4),
           share_over_1p5mm=float((dm > 0.15).mean()), share_over_0p8mm=float((dm > 0.08).mean()))
grp = {'head': ['head'], 'neck': ['neck'], 'trunk_pelvis': ['torso'], 'arms': ['arm_xneg', 'arm_xpos'], 'hands': ['hand_xneg', 'hand_xpos'], 'legs': ['leg_xneg', 'leg_xpos'],
       'feet': ['foot_xneg', 'foot_xpos'], 'tail': ['tail']}
res['by_region'] = {k: dict(mean_mm=round(float(dm[np.isin(labS, v)].mean() * 10), 4), p95_mm=round(float(np.percentile(dm[np.isin(labS, v)], 95) * 10), 4),
                            max_mm=round(float(dm[np.isin(labS, v)].max() * 10), 4)) for k, v in grp.items()}
E = np.unique(np.sort(np.r_[FS[:, [0, 1]], FS[:, [1, 2]]][::50], 1), axis=0); res['surfaced_mean_edge_mm'] = round(float(np.linalg.norm(VS[E[:, 0]] - VS[E[:, 1]], axis=1).mean() * 10), 3)
J = [np.array(LM[k]['p_cm']) for k in LM if any(k.startswith(p) for p in ('elbow', 'wrist', 'knee', 'ankle', 'glenohumeral'))]
jz = np.zeros(len(VS), bool)
for p in J: jz |= np.linalg.norm(VS - p, axis=1) < 12
jz |= np.linalg.norm(VS - np.array(LM['tail_root_centre']['p_cm']), axis=1) < 10
res['joint_zone_share_of_vertices'] = float(jz.mean()); res['joint_zone_delta_mean_mm'] = round(float(dm[jz].mean() * 10), 4); res['outside_joint_delta_mean_mm'] = round(float(dm[~jz].mean() * 10), 4)
px = 3.0; ZT = float(np.ceil(V[:, 2].max() + 5)); XO = float(np.ceil(np.abs(V[:, :2]).max() + 10))
def sil(Vv, Ff, yaw, ss=2):
    an = np.radians(yaw); Rm = np.array([[np.cos(an), -np.sin(an), 0], [np.sin(an), np.cos(an), 0], [0, 0, 1]]); P = Vv @ Rm.T; q = px * ss
    u = (P[:, 0] + XO) * q; v = (ZT - P[:, 2]) * q; W_, H_ = int(2 * XO * px), int((ZT + 5) * px); im = Image.new('L', (W_ * ss, H_ * ss), 0); dr = ImageDraw.Draw(im)
    for t in Ff: dr.polygon([(u[t[0]], v[t[0]]), (u[t[1]], v[t[1]]), (u[t[2]], v[t[2]])], fill=255)
    return np.array(im, float).reshape(H_, ss, W_, ss).mean((1, 3)) >= 127.5
res['silhouette_iou_surfaced_vs_base'] = {}
for nm, yaw in (('front', 0), ('profile_left', 90)):
    A = sil(V, F, yaw); B = sil(VS, FS, yaw); res['silhouette_iou_surfaced_vs_base'][nm] = round(float((A & B).sum() / (A | B).sum()), 6); print(nm, res['silhouette_iou_surfaced_vs_base'][nm], flush=True)
json.dump(res, open(OUT, 'w'), indent=1); print(json.dumps({k: v for k, v in res.items() if k != 'by_region'}), res['by_region'])
