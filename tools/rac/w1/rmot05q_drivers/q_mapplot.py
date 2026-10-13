# RM-OT-05Q: unwrapped (theta, s) map of the arm-local frame from patch_selection.json, coloured by normal.axis and by label.
# Usage: python3 q_mapplot.py MESH patch_selection.json labels.npy OUT.png
import trimesh, numpy as np, sys, json
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
m = trimesh.load(sys.argv[1], process=False); V = m.vertices; F = m.faces; R = json.load(open(sys.argv[2])); lab = np.load(sys.argv[3])
O = np.array(R['frame']['origin']); d = np.array(R['frame']['axis']); d /= np.linalg.norm(d); e1 = np.cross([0, 1, 0], d); e1 /= np.linalg.norm(e1); e2 = np.cross(d, e1)
c = V[F].mean(1) - O; s = c @ d; r = np.hypot(c @ e1, c @ e2); th = np.degrees(np.arctan2(c @ e2, c @ e1)); na = m.face_normals @ d
sel = (np.abs(s) < 10) & (r < 13) & (np.arange(len(F)) < len(lab))
fig, ax = plt.subplots(1, 2, figsize=(22, 8))
ax[0].scatter(th[sel], s[sel], c=na[sel], s=4, cmap='coolwarm', vmin=-1, vmax=1); ax[0].set_title('face normal . arm axis (red = facing up the arm, blue = down): ledges')
cols = np.array(['0.75', 'red', 'b', 'orange', 'g', 'purple']); ax[1].scatter(th[sel], s[sel], c=cols[lab[sel]], s=4); ax[1].set_title('labels: red garment G, orange seam band S, grey protected')
for a in ax:
    a.plot(R['ledge_theta'], R['s_lo'], 'k-'); a.plot(R['ledge_theta'], R['s_hi'], 'k-'); a.axvline(R['sector_theta_deg'][0]); a.axvline(R['sector_theta_deg'][1])
    a.set_xticks(range(-180, 181, 15)); a.grid(alpha=.3); a.set_xlabel('theta deg (0 lateral +X, +90 anterior)'); a.set_ylabel('s cm along arm axis (r < 13 cm only)')
plt.tight_layout(); plt.savefig(sys.argv[4], dpi=70)
