# RAC RM-OT-05O §3: sagittal leg-axis landmarks of a body mesh (left leg, X > 0; the body is bilaterally symmetric).
# Per 1 cm slice (exact winding-number inside test, 0.25 cm grid) the leg section's anterior / posterior / medial / lateral
# extents are taken; the segment axes are least-squares lines through the AP-and-ML MID-POINTS of the thigh (z 66-92) and
# shank (z 20-46) sections (mid-points of extents, not area centroids, so calf / quadriceps mass does not bias the axis).
# Joint centres: knee = point on the thigh / shank axes at the knee joint line height (closest approach of the two axes,
# z clamped to the knee station); ankle = shank axis at the ankle height (default 11 cm); hip = thigh axis extended to the
# hip height (default 106 cm). Heights are declared inputs, not fitted constants. Writes JSON + a profile plot.
# Usage: python3 o_legaxes.py MESH.obj OUTPREFIX [--knee_z 57] [--ankle_z 11] [--hip_z 106]
import argparse, json, numpy as np, igl, trimesh
from scipy import ndimage as ndi
ap = argparse.ArgumentParser(); ap.add_argument('mesh'); ap.add_argument('out'); ap.add_argument('--knee_z', type=float, default=57.0)
ap.add_argument('--ankle_z', type=float, default=11.0); ap.add_argument('--hip_z', type=float, default=106.0); ap.add_argument('--zmax', type=float, default=100.0); ap.add_argument('--thigh', type=float, nargs=2, default=[66, 92]); ap.add_argument('--shank', type=float, nargs=2, default=[20, 46]); a = ap.parse_args()
m = trimesh.load(a.mesh, process=False); V = np.ascontiguousarray(m.vertices, float); F = np.ascontiguousarray(m.faces, np.int64)
H = 0.25; xs = np.arange(0, 50, H); ys = np.arange(V[:, 1].min() - 2, V[:, 1].max() + 2, H); X, Y = np.meshgrid(xs, ys, indexing='ij')
rows = []
for z in np.arange(2, a.zmax, 1.0):
    s = igl.fast_winding_number(V, F, np.c_[X.ravel(), Y.ravel(), np.full(X.size, z)]).reshape(X.shape) > 0.5
    L, n = ndi.label(s); best = None
    for i in range(1, n + 1):
        w = np.where(L == i); x = xs[w[0]]
        if x.mean() > 5 and x.max() < 45 and (best is None or len(x) > best[0]): best = (len(x), w)
    if best is None: continue
    x = xs[best[1][0]]; y = ys[best[1][1]]
    rows.append(dict(z=float(z), y_ant=float(y.max()), y_post=float(y.min()), x_med=float(x.min()), x_lat=float(x.max()), area=best[0] * H * H))
R = {r['z']: r for r in rows}
def fit(z0, z1):
    zz = np.array([z for z in R if z0 <= z <= z1]); ym = np.array([(R[z]['y_ant'] + R[z]['y_post']) / 2 for z in zz]); xm = np.array([(R[z]['x_med'] + R[z]['x_lat']) / 2 for z in zz])
    by = np.polyfit(zz, ym, 1); bx = np.polyfit(zz, xm, 1); return bx, by     # x(z), y(z) lines
tbx, tby = fit(*a.thigh); sbx, sby = fit(*a.shank)
pt = lambda bx, by, z: np.array([np.polyval(bx, z), np.polyval(by, z), z])
knee = 0.5 * (pt(tbx, tby, a.knee_z) + pt(sbx, sby, a.knee_z)); hip = pt(tbx, tby, a.hip_z); ankle = pt(sbx, sby, a.ankle_z)
def ang(u, v): return float(np.degrees(np.arccos(np.clip(np.dot(u, v) / np.linalg.norm(u) / np.linalg.norm(v), -1, 1))))
thigh = knee - hip; shank = ankle - knee
sag = lambda v: np.degrees(np.arctan2(v[1], -v[2]))          # sagittal inclination from vertical (+ = distal end anterior)
out = dict(mesh=a.mesh, method='AP/ML mid-point axes; thigh z%g-%g, shank z%g-%g' % (*a.thigh, *a.shank), declared_heights=dict(hip=a.hip_z, knee=a.knee_z, ankle=a.ankle_z),
           hip=hip.round(2).tolist(), knee=knee.round(2).tolist(), ankle=ankle.round(2).tolist(),
           thigh_length=round(float(np.linalg.norm(thigh)), 2), shank_length=round(float(np.linalg.norm(shank)), 2),
           thigh_sagittal_incl_deg=round(float(sag(thigh)), 1), shank_sagittal_incl_deg=round(float(sag(shank)), 1),
           knee_flexion_sagittal_deg=round(float(sag(shank) - sag(thigh)), 1) if False else round(float(sag(thigh) - sag(shank)), 1),
           knee_angle_3d_deg=round(180 - ang(-thigh, shank), 1), knee_ahead_of_hip_ankle_line_cm=None, profile=rows)
# knee offset from the hip-ankle line in the sagittal plane (+ = anterior)
t = (knee[2] - hip[2]) / (ankle[2] - hip[2]); line_y = hip[1] + t * (ankle[1] - hip[1]); out['knee_ahead_of_hip_ankle_line_cm'] = round(float(knee[1] - line_y), 2)
json.dump(out, open(a.out + '.json', 'w'), indent=1)
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5, 9)); zz = [r['z'] for r in rows]
ax.plot([r['y_ant'] for r in rows], zz, 'k-', lw=1); ax.plot([r['y_post'] for r in rows], zz, 'k-', lw=1)
for bx, by, z0, z1, c in ((tbx, tby, 60, 108, 'tab:red'), (sbx, sby, 8, 62, 'tab:blue')):
    z = np.linspace(z0, z1, 10); ax.plot(np.polyval(by, z), z, c + '' if False else c, ls='--')
for p, l in ((hip, 'hip'), (knee, 'knee'), (ankle, 'ankle')): ax.plot(p[1], p[2], 'o', color='tab:green'); ax.text(p[1] + 1, p[2], l)
ax.set_aspect('equal'); ax.grid(alpha=.3); ax.set_xlabel('Y (cm, +anterior)'); ax.set_ylabel('Z (cm)'); ax.set_title('%s\nthigh %.1f deg, shank %.1f deg, knee %+.1f cm vs hip-ankle line' % (a.mesh.split('/')[-1], out['thigh_sagittal_incl_deg'], out['shank_sagittal_incl_deg'], out['knee_ahead_of_hip_ankle_line_cm']), fontsize=8)
fig.savefig(a.out + '.png', dpi=110, bbox_inches='tight')
print(json.dumps({k: v for k, v in out.items() if k != 'profile'}, indent=1))
# coronal (front-view) alignment: knee offset from the hip-ankle line in X (+ = lateral, i.e. varus / bowed)
t = (knee[2] - hip[2]) / (ankle[2] - hip[2]); lx = hip[0] + t * (ankle[0] - hip[0]); out['knee_lateral_of_hip_ankle_line_cm'] = round(float(knee[0] - lx), 2)
json.dump(out, open(a.out + '.json', 'w'), indent=1); print('knee lateral of hip-ankle line (cm):', out['knee_lateral_of_hip_ankle_line_cm'])
