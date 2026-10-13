# Trunk half-breadth / AP profile along z (cm). Arm-separated: per slice, the midline component; where the hanging arm
# touches the trunk the slice is cut at X = arm_cut(z) (the arm's medial edge interpolated from the nearest slices where
# the arm is separate) and the cut is FLAGGED. Usage: python3 p_trunkprofile.py MESH.obj OUT.json [z0 z1 dz]
import sys, json, numpy as np, trimesh, igl
from scipy import ndimage as ndi
m = trimesh.load(sys.argv[1], process=False); V = np.ascontiguousarray(m.vertices); F = np.ascontiguousarray(m.faces, np.int64)
z0, z1, dz = (float(x) for x in sys.argv[3:6]) if len(sys.argv) > 5 else (100.0, 176.0, 2.0)
H = 0.25; xs = np.arange(0, 60, H); ys = np.arange(V[:, 1].min() - 1, V[:, 1].max() + 1, H); X, Y = np.meshgrid(xs, ys, indexing='ij')
rows = []
for z in np.arange(z0, z1 + 0.01, dz):
    s = igl.fast_winding_number(V, F, np.c_[X.ravel(), Y.ravel(), np.full(X.size, z)]).reshape(X.shape) > 0.5
    L, n = ndi.label(s); comps = []
    for i in range(1, n + 1):
        w = np.where(L == i); comps.append((xs[w[0]].min(), xs[w[0]].max(), len(w[0]) * H * H, i))
    mid = [c for c in comps if c[0] < 0.5]; arm = [c for c in comps if c[0] > 15 and c[2] > 20]
    if not mid: continue
    t = max(mid, key=lambda c: c[2]); rows.append(dict(z=float(z), mid_x1=float(t[1] + H), arm_x0=float(min(c[0] for c in arm)) if arm else None, contact=not arm, mask=L == t[3]))
# interpolate the arm medial edge over contact slices and cut there
zs = np.array([r['z'] for r in rows]); ax = np.array([np.nan if r['arm_x0'] is None else r['arm_x0'] for r in rows]); ok = ~np.isnan(ax)
out = []
for r in rows:
    x1 = r['mid_x1']; cut = None
    if r['contact'] and ok.any():
        cut = float(np.interp(r['z'], zs[ok], ax[ok])) - 0.5; mk = r['mask'] & (xs[:, None] < cut)
        w = np.where(mk); x1 = float(xs[w[0]].max() + H) if len(w[0]) else x1
    w = np.where(r['mask'] & ((xs[:, None] < cut) if cut else True)); y = ys[w[1]]
    col = r['mask'][xs <= 2.0].any(0); yy = ys[col]
    out.append(dict(z=r['z'], half_breadth=round(x1, 2), breadth=round(2 * x1, 2), ap_depth=round(float(y.max() - y.min() + H), 2), midline_ap=round(float(yy.max() - yy.min() + H), 2) if len(yy) else None, arm_contact=bool(r['contact']), arm_cut_x=None if cut is None else round(cut, 2)))
json.dump(dict(mesh=sys.argv[1], method=__doc__ if False else 'midline component; arm contact slices cut at the interpolated arm medial edge (flagged)', rows=out), open(sys.argv[2], 'w'), indent=1)
for r in out: print('%5.1f  breadth %5.1f  AP %5.1f  midAP %s %s' % (r['z'], r['breadth'], r['ap_depth'], r['midline_ap'], ('CONTACT cut@%.1f' % r['arm_cut_x']) if r['arm_contact'] else ''))
