# ear_sections.py WORK OUTDIR : order bdcd6a6 §16 item 13 sectional views. Horizontal slices (root-frame up = const) through the left ear,
# plotted in the (posterior b, lateral n) plane of the root frame, true scale; ear sheet orange / violet / yellow, cuff blue, head grey.
import sys, os, json, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
W_, OUT = sys.argv[1], sys.argv[2]; HEADS = {'c1': 'FNL4-CF2', 'c2': 'FNF181-CF2'}; CANDS = ['E1', 'E2', 'E3']
COL = {'front': '#d9774a', 'back': '#8f6fb8', 'rim': '#d8b23a', 'cuff': '#4f8fd0', 'transition': '#4caf50', 'v005': '#9a9a9a'}
for cf_, h in HEADS.items():
    LV = [-2.0, 0.0, 2.0, 4.0]; fig, axs = plt.subplots(len(CANDS), len(LV), figsize=(4.2 * len(LV), 4.2 * len(CANDS)))
    for i, c in enumerate(CANDS):
        z = np.load('%s/build/%s_%s_branch.npz' % (W_, h, c)); r = json.load(open('%s/build/%s_%s_branch.json' % (W_, h, c))); f = r['sides']['l']['frame']
        O, n, b, u = [np.array(f[k]) for k in ('O', 'n', 'b', 'u')]; V = z['V']; Q = z['Q']; part = z['part']
        d = V - O; B = d @ b; U = d @ u; N = d @ n; near = (np.abs(B) < 6) & (N > -4) & (V[:, 0] > 0)
        Qs = Q[near[Q].all(1)]; Es = np.concatenate([Qs[:, [0, 1]], Qs[:, [1, 2]], Qs[:, [2, 3]], Qs[:, [3, 0]]]); Es = np.unique(np.sort(Es, 1), axis=0)
        for j, lv in enumerate(LV):
            ax = axs[i, j]; a, b_ = Es[:, 0], Es[:, 1]; s = (U[a] - lv) * (U[b_] - lv) < 0; t = (lv - U[a[s]]) / (U[b_[s]] - U[a[s]])
            pb = B[a[s]] + t * (B[b_[s]] - B[a[s]]); pn = N[a[s]] + t * (N[b_[s]] - N[a[s]]); pp = np.where(part[a[s]] != 'v005', part[a[s]], part[b_[s]])
            for k_, col in COL.items():
                m = pp == k_; ax.scatter(pb[m], pn[m], s=4, c=col, label=k_ if (i == 0 and j == 0) else None)
            ax.set_aspect('equal'); ax.set_xlim(-3.5, 4.0); ax.set_ylim(-1.5, 4.0); ax.grid(alpha=0.3); ax.set_title('%s  up %+.1f cm' % (c, lv), fontsize=10)
            if j == 0: ax.set_ylabel('lateral from root plane (cm)')
            if i == len(CANDS) - 1: ax.set_xlabel('posterior (cm)')
    fig.legend(loc='upper right'); fig.suptitle('Fenn ear branch %s (%s) — horizontal sections through the left ear (root frame; true scale)' % (cf_, h)); fig.tight_layout(rect=(0, 0, 0.95, 0.96))
    fig.savefig(os.path.join(OUT, 'FENN_EAR_13b_sections_%s.jpg' % cf_), dpi=110); plt.close(fig)
print('sections done')
