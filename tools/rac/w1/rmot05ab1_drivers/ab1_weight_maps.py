# RM-OT-05AB1: weight visualisation of each armpit web, cp2 vs cp3: upper-arm share (upperarm / (upperarm + trunk)) on rest
# positions inside the changed region, front and lateral projections, nearest-to-camera points drawn last. Read-only.
# Usage: python3 ab1_weight_maps.py RIG_cp2.npz W_cp2.npz W_cp3.npz OUT.png
import sys, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
rp, w2p, w3p, out = sys.argv[1:5]; d = np.load(rp); V = d['V'] * 100; names = [str(x) for x in d['names']]
W2 = np.load(w2p)['W'].astype(float); W3 = np.load(w3p)['W'].astype(float); it = names.index('trunk')
fig, ax = plt.subplots(2, 4, figsize=(20, 11))
for r, s in enumerate('LR'):
    iu = names.index('upperarm_' + s); ch = np.abs(W3[:, iu] - W2[:, iu]) > 5e-5; c = V[ch].mean(0)
    box = (np.abs(V[:, 0] - c[0]) < 14) & (np.abs(V[:, 2] - c[2]) < 18) & (np.abs(V[:, 1] - c[1]) < 18)
    for k, (W, tag) in enumerate(((W2, 'cp2'), (W3, 'cp3'))):
        m = W[:, iu] + W[:, it]; u = np.where(m > 0, W[:, iu] / np.maximum(m, 1e-9), np.nan)
        for j, (xi, dk, sg, vn) in enumerate(((0, 1, -1, 'front'), (1, 0, 1 if s == 'L' else -1, 'lateral'))):
            a = ax[r, k * 2 + j]; sel = np.where(box)[0]; o = sel[np.argsort(sg * V[sel, dk])][::2]
            sc = a.scatter(V[o, xi], V[o, 2], c=u[o], cmap='coolwarm', vmin=0, vmax=1, s=0.6, linewidths=0)
            a.scatter(V[ch & box][::25, xi], V[ch & box][::25, 2], s=0.2, c='k', alpha=0.15) if tag == 'cp3' else None
            a.set_aspect('equal'); a.set_title('%s web - %s - %s view' % (s, tag, vn), fontsize=11)
fig.colorbar(sc, ax=ax.ravel().tolist(), shrink=0.6, label='upper-arm share of trunk+upper-arm weight (blue = trunk, red = upper arm)')
fig.suptitle('05AB1 armpit-web weights, rest positions (cp3 panels: grey dots = changed vertices)', fontsize=14); fig.savefig(out, dpi=75)
