# RM-OT-05AB: diagnostic image of the temporary-rig vertex groups (dominant group per welded vertex), front / back / profile point
# projection with depth ordering. Read-only.  Usage: python3 ab_label_sheet.py MESH.npz WEIGHTS.npz OUT.png
import sys, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
m, w, out = sys.argv[1:4]; d = np.load(m); V = d['V'].astype(float) * 100; Wd = np.load(w)
names = list(Wd['names']); inv = Wd['welded_index']; lab = Wd['label_welded'][inv]; Wt = Wd['weights_welded'][inv]
blend = 1 - Wt.max(1)                                    # 0 = single group, 0.5 = even blend
cm = plt.get_cmap('tab20'); col = cm(lab % 20); col[:, :3] = col[:, :3] * (1 - 0.8 * blend[:, None])
fig, ax = plt.subplots(1, 3, figsize=(18, 10))
for a, (t, xi, yi, dk, sg) in zip(ax, [('front', 0, 2, 1, 1), ('back', 0, 2, 1, -1), ('left profile', 1, 2, 0, 1)]):
    o = np.argsort(sg * V[:, dk])[::-1]; o = o[::3]
    a.scatter(V[o, xi] * (-1 if t == 'back' else 1), V[o, yi], c=col[o], s=0.3, linewidths=0); a.set_aspect('equal'); a.set_title(t)
h = [plt.Line2D([], [], marker='o', ls='', color=cm(i % 20), label=n) for i, n in enumerate(names)]
fig.legend(handles=h, loc='lower center', ncol=7); fig.suptitle('05AB temporary-rig vertex groups (dark = joint blend band)'); fig.savefig(out, dpi=80)
