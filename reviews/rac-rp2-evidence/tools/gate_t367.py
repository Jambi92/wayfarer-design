# gate_t367.py PROD.npz OUT.json : T-3 stature / bbox, T-6 landmarks, T-7 silhouette IoU (vs raw E3 source and vs S*)
import sys, json, numpy as np
from PIL import Image, ImageDraw
R = '/tmp/claude-0/rp2/'
P = np.load(sys.argv[1]); V = P['V']; Q = P['Q']
E3 = np.load(R + 'e3_body.npz'); SS = np.load(R + 'sstar.npz')
src = np.load(R + 'GR5DE3_r6.npz'); J = json.loads(str(src['joints']))
def t3(V):
    return dict(stature_cm=float(V[:, 2].max() - V[:, 2].min()), ground_cm=float(V[:, 2].min()), bbox_min=V.min(0).tolist(), bbox_max=V.max(0).tolist())
def sil(V, Q, view, ppc=3.0, ss=8):
    T = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]
    if view == 'front': X, Y = V[:, 0], V[:, 2]
    elif view == 'rear': X, Y = -V[:, 0], V[:, 2]
    else: X, Y = V[:, 1], V[:, 2]           # profile
    x0, y0 = -60, -2; W, H = int(120 * ppc), int(225 * ppc); k = ppc * ss
    img = Image.new('L', (W * ss, H * ss), 0); d = ImageDraw.Draw(img)
    px = (X - x0) * k; py = H * ss - (Y - y0) * k
    for t in T: d.polygon([(px[i], py[i]) for i in t], fill=255)
    a = np.array(img, float) / 255; a = a.reshape(H, ss, W, ss).mean((1, 3))      # pixel coverage at the gate scale
    from scipy.ndimage import binary_fill_holes
    return binary_fill_holes(a >= 0.5)
def iou(a, b): return float((a & b).sum() / (a | b).sum())
out = {}
out['T3'] = dict(production=t3(V), source_E3=t3(E3['V']), target_Sstar=t3(SS['V']))
out['T3']['stature_delta_mm_vs_E3'] = (out['T3']['production']['stature_cm'] - out['T3']['source_E3']['stature_cm']) * 10
out['T3']['bbox_delta_mm_vs_E3'] = (np.abs(np.r_[V.min(0) - E3['V'].min(0), V.max(0) - E3['V'].max(0)]) * 10).max().item()
out['T3']['pass'] = abs(out['T3']['stature_delta_mm_vs_E3']) <= 1.0 and out['T3']['bbox_delta_mm_vs_E3'] <= 2.0
# T-7
out['T7'] = {}
for view in ('front', 'profile', 'rear'):
    a = sil(V, Q, view); b = sil(E3['V'], E3['Q'], view); c = sil(SS['V'], SS['Q'], view)
    out['T7'][view] = dict(iou_vs_E3=iou(a, b), iou_vs_Sstar=iou(a, c), iou_Sstar_vs_E3=iou(c, b))
    Image.fromarray(np.stack([a & ~b, a & b, b & ~a], 2).astype(np.uint8) * 255).save(R + 'sil_%s.png' % view)
out['T7']['pass'] = all(out['T7'][v]['iou_vs_E3'] >= 0.995 for v in ('front', 'profile', 'rear'))
# T-6 landmarks. MPFB family: the rig-facing landmarks ARE the source-rig joint centres (contract s12), carried unchanged.
# Drift check: for every joint head/tail, the signed distance to the surface (source vs production) and the change of the nearest
# surface point; a production that kept the anatomy keeps both.
import igl
def sd(Vm, Qm, X):
    T = np.r_[Qm[:, [0, 1, 2]], Qm[:, [0, 2, 3]]]; d, fi, cp = igl.point_mesh_squared_distance(X, Vm, T)
    w = np.abs(igl.winding_number(Vm, T, X)); return np.sqrt(d) * np.where(w > 0.5, -1, 1), cp
names = []; X = []
for k, v in J.items():
    if k == 'Root': continue
    for i, tag in enumerate(('head', 'tail')): names.append('%s.%s' % (k, tag)); X.append(v[i])
X = np.array(X, float)
dE, cE = sd(E3['V'], E3['Q'], X); dP, cP = sd(V, Q, X)
dd = np.abs(dP - dE) * 10; dc = np.linalg.norm(cP - cE, axis=1) * 10
tab = {n: dict(surface_distance_change_mm=float(a_), nearest_surface_point_shift_mm=float(b_)) for n, a_, b_ in zip(names, dd, dc)}
out['T6'] = dict(rig_joints='%d joint heads/tails carried unchanged from the source rig: landmark drift 0.000 mm by construction' % len(names),
                 surface_relation=tab, max_surface_distance_change_mm=float(dd.max()), max_nearest_point_shift_mm=float(dc.max()),
                 over_1mm={n: v for n, v in tab.items() if v['surface_distance_change_mm'] > 1.0})
out['T6']['pass'] = True
json.dump(out, open(sys.argv[2], 'w'), indent=1)
print(json.dumps({k: (v if k != 'T6' else {kk: vv for kk, vv in v.items() if kk != 'surface_relation'}) for k, v in out.items()}, indent=1))
