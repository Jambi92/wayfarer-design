# RM-OT-05AF evidence map: 05AF body (grey), welded seam positions (green), protected / passive duplicate groups left unwelded
# (red = protected interface, blue = non-sculpt passive: hands / feet), front and back.
import sys, json, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
od = sys.argv[1]; rows = json.load(open(od + '/af_groups.json')); B = np.load(od + '/base_VF.npz'); V = B['V'] * 100; F = B['F']
z0 = V[:, 2].min(); T = V[F]; c = T.mean(1); n = np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0]); n /= np.maximum(np.linalg.norm(n, axis=1), 1e-20)[:, None]
fig, ax = plt.subplots(1, 2, figsize=(14, 14), facecolor='#222')
for a, (sgn, t) in zip(ax, [(-1, 'front'), (1, 'back')]):
    m = (sgn * n[:, 1]) > 0; o = np.argsort(-sgn * c[m, 1])
    a.scatter(c[m, 0][o] * (1 if sgn < 0 else -1), c[m, 2][o] - z0, c=np.clip(sgn * n[m, 1][o], 0, 1), cmap='gray', s=0.05, vmin=0, vmax=1, linewidths=0)
    for cls, col, sz in [('weld', '#3c3', 2), ('passive', '#48f', 1), ('prot', '#f33', 1.5)]:
        if cls == 'weld': P = [r['members'][0] for r in rows if r['in_sculpt_zone'] and r['cls'] == 'SAFE_SCULPT_SEAM']
        elif cls == 'passive': P = [r['members'][0] for r in rows if not r['in_sculpt_zone'] and r['cls'] != 'PROTECTED_INTERFACE']
        else: P = [r['members'][0] for r in rows if r['cls'] == 'PROTECTED_INTERFACE']
        p = V[P]; vis = (sgn * (p[:, 1] - np.median(V[:, 1]))) > -8
        a.scatter(p[vis, 0] * (1 if sgn < 0 else -1), p[vis, 2] - z0, c=col, s=sz, linewidths=0)
    a.set_aspect('equal'); a.axis('off'); a.set_facecolor('#222'); a.set_title('05AF ' + t + ' - green: welded sculpt-zone seams, red: protected (head, tail, genital, tail junction, perineal fold), blue: hands/feet passive', color='w', fontsize=8)
plt.tight_layout(); plt.savefig(od + '/af_seam_map.jpg', dpi=90, facecolor='#222', pil_kwargs=dict(quality=85))
