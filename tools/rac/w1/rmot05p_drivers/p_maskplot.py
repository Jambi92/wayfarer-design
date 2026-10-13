# Visualise the LOW masks on the REF vertices (front / profile / rear projections): protected interior (red), falloff band
# (orange), tissue displacement (blue, intensity = cm). Usage: python3 p_maskplot.py REF.obj LOW_masks.npz OUT.png
import sys, numpy as np, trimesh, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
V = trimesh.load(sys.argv[1], process=False).vertices; M = np.load(sys.argv[2]); pi, P, D = M['protected_interior'], M['protection'], M['displacement']
fig, axs = plt.subplots(1, 3, figsize=(15, 9))
for ax, (title, u, sgn, depth) in zip(axs, (('front (image right = -X)', 0, -1, 1), ('profile (anterior right)', 1, 1, 0), ('rear', 0, 1, -1))):
    o = np.argsort(V[:, depth] * (1 if title.startswith('front') else (-1 if title.startswith('rear') else 1)))
    x = sgn * V[o, u]; z = V[o, 2]
    c = np.full((len(o), 3), 0.82); d = D[o]; c[d > 0.02] = np.c_[0.75 - 0.6 * np.clip(d[d > 0.02] / 3, 0, 1), 0.8 - 0.4 * np.clip(d[d > 0.02] / 3, 0, 1), np.ones((d > 0.02).sum())]
    band = (P[o] > 0) & ~pi[o]; c[band] = (1.0, 0.65, 0.2); c[pi[o]] = (0.85, 0.1, 0.1)
    ax.scatter(x, z, c=c, s=0.6, linewidths=0); ax.set_aspect('equal'); ax.set_title(title); ax.grid(alpha=.25); ax.set_ylabel('z cm')
fig.suptitle('GO-RD4-LOW masks on GO-RD4-REF (x-ray vertex projection, no occlusion): red = protected interior (displacement exactly 0), orange = 3 cm falloff band, blue = tissue reduction (darker = deeper, max %.2f cm)' % D.max(), fontsize=10)
fig.savefig(sys.argv[3], dpi=95, bbox_inches='tight'); print(sys.argv[3])
