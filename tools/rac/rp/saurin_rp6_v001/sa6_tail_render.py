# sa6_tail_render.py OUTDIR BODYDIR:NAME:ARTDIR|-:POSE:FRAC [...] : tail centreline / silhouette evidence for the tail-kink calibration (order 8e3b7b4d §3).
#   Per case one figure, same body: neutral (grey) | plain LBS (black) | packaged blend v004 (blue) | baked (red, when ARTDIR is given).
#   Row 1: side (y-z) and top (x-y) views of the tail: centreline through the 181 frozen ring centroids + every 6th ring outline (cross-section silhouette),
#          worst-kink junction marked; tail joint heads marked.
#   Row 2: per-junction turning (deg) for each column, the neutral turning (inherited curvature) dashed, and the deformation-introduced turning |th - th0|.
#   Row 3: motion strip around the frame: the baked (else packaged) centreline at FRAC-0.1, FRAC-0.05, FRAC, FRAC+0.05 (side view, coloured by local turning).
import sys, os, json, numpy as np, matplotlib
from matplotlib.collections import PolyCollection, LineCollection
matplotlib.use('Agg'); import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('RP6_LAYERS', 'SA_RP6_creator_layers_v004.json')
import sa6_common as C, sa6_correctives as CC, sa6_layer_harness as H, sa6_blend as BL, sa6_gates as GT, ast
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sa6_render.py')).read()   # shaded mesh = sa6_render.draw, extracted (not re-implemented)
exec(compile(ast.Module([n for n in ast.parse(src).body if isinstance(n, ast.FunctionDef) and n.name in ('view_basis', 'draw')], []), 'sa6_render', 'exec'))
OD = sys.argv[1]; os.makedirs(OD, exist_ok=True); rings = C.load()['tail_rings']
def cen(P): return np.array([P[rg].mean(0) for rg in rings])
def turning(P):
    dv = np.diff(cen(P), axis=0); dv /= np.linalg.norm(dv, axis=1, keepdims=True); return np.degrees(np.arccos(np.clip((dv[1:] * dv[:-1]).sum(1), -1, 1)))
def kink(th):
    w = np.array([th[max(0, k - 5):k + 6].mean() for k in range(len(th))]); m = th > 0.2; r = np.where(m, th / np.maximum(w, 0.05), 0); return float(r.max()), int(r.argmax())
for case in sys.argv[2:]:
    BD, nm, AD, pn, fr = case.split(':'); fr = float(fr); AD = None if AD == '-' else AD
    b = json.load(open(os.path.join(BD, 'bodies.json')))['bodies'][nm]; R, z = BL.rig_of(nm, b, BD)
    P0 = H.Blend(H.load_base(R, b['cfg']), [(w, H.load_state(R, s)[0]) for s, w in b['w'].items()]); K = CC.Correctives.load(R, os.path.join(AD, 'BK_%s.json' % nm)) if AD else None
    spec = GT.gate_poses(R)[pn]
    def posed(f, col):
        T = R.pose([(bb, p, a, dg * f) for bb, p, a, dg in spec])
        if col == 'lbs': return R.skin(T)
        return R.skin(T, R.V + P0.delta(T) + (K.delta(T) if col == 'bake' else 0))
    cols = [('neutral', R.V, '0.6', '--'), ('lbs', posed(fr, 'lbs'), 'k', '-'), ('prod', posed(fr, 'prod'), 'b', '-')] + ([('bake', posed(fr, 'bake'), 'r', '-')] if K else [])
    th0 = turning(R.V); fig = plt.figure(figsize=(18, 12)); last = cols[-1][0]
    for j, (ax_i, ax_j, nmv) in enumerate(((1, 2, 'side (y-z)'), (0, 1, 'top (x-y)'))):
        ax = fig.add_subplot(3, 2, 1 + j)
        for tag, P, col, ls in cols:
            c = cen(P); ax.plot(c[:, ax_i], c[:, ax_j], color=col, ls=ls, lw=1.2, label='%s (kink %.3f)' % (tag, kink(turning(P))[0]))
            for rg in rings[::6]: X = P[rg]; ax.plot(np.r_[X[:, ax_i], X[:1, ax_i]], np.r_[X[:, ax_j], X[:1, ax_j]], color=col, lw=0.3, alpha=0.6)
            if tag == last: k = kink(turning(P))[1]; ax.plot(c[k + 1, ax_i], c[k + 1, ax_j], 'o', mfc='none', mec='m', ms=14, mew=2)
        ax.set_aspect('equal'); ax.set_title('%s  %s @%.0f%%  %s view (magenta = worst-kink ring of %s)' % (nm, pn, fr * 100, nmv, last), fontsize=9); ax.legend(fontsize=7)
    ax = fig.add_subplot(3, 1, 2)
    for tag, P, col, ls in cols:
        th = turning(P); ax.plot(np.arange(1, len(th) + 1), th, color=col, ls=ls, lw=1, label='turning ' + tag)
        if tag != 'neutral': ax.plot(np.arange(1, len(th) + 1), np.abs(th - th0), color=col, ls=':', lw=1, label='|turning - neutral| ' + tag)
    for tb in sorted(x for x in R.bi if x.startswith('tail_')):
        k = int(np.linalg.norm(cen(R.V) - np.asarray(R.H(tb)), axis=1).argmin()); ax.axvline(k, color='g', lw=0.4); ax.text(k, ax.get_ylim()[1] * 0.95, tb[5:], fontsize=6, color='g')
    ax.set_xlabel('ring junction (root -> tip; green = tail joint heads)'); ax.set_ylabel('deg'); ax.legend(fontsize=7, ncol=4); ax.grid(alpha=.3)
    for j, f in enumerate([max(0.025, fr - 0.1), max(0.025, fr - 0.05), fr, min(1.0, fr + 0.05)]):
        ax = fig.add_subplot(3, 4, 9 + j); P = posed(f, last); c = cen(P); th = turning(P)
        ax.scatter(c[1:-1, 1], c[1:-1, 2], c=th, s=4, cmap='viridis', vmin=0, vmax=6); ax.plot(c[:, 1], c[:, 2], 'k-', lw=0.3); ax.set_aspect('equal'); ax.set_xticks([]); ax.set_yticks([])
        ax.set_title('%s @%.1f%%  kink %.3f  max turn %.2f deg' % (last, f * 100, kink(th)[0], th.max()), fontsize=8)
    plt.tight_layout(); fo0 = os.path.join(OD, 'TR_%s_%s_%04d.png' % (nm.replace('@', '_').replace('.', 'p'), pn, round(fr * 1000))); plt.savefig(fo0, dpi=100); plt.close(fig)
    # shaded mesh of the tail at the junction where the deformation concentrates turning most (max over columns of (th - win) - (th0 - win0)), lateral + dorsal views
    def win_(t): return np.array([t[max(0, k - 5):k + 6].mean() for k in range(len(t))])
    e0 = th0 - win_(th0); kj = max(((int(((turning(P) - win_(turning(P))) - e0).argmax()), float(((turning(P) - win_(turning(P))) - e0).max())) for tag, P, _, _ in cols[1:]), key=lambda x: x[1])[0]
    fig, ax = plt.subplots(2, len(cols), figsize=(4.4 * len(cols), 8.4))
    for j, (tag, P, col, ls) in enumerate(cols):
        ctr = P[rings[kj + 1]].mean(0); th = turning(P); ex = float(((th - win_(th)) - e0)[kj])
        for i, view in enumerate(((1.0, 0.12, 0.1), (0.05, 0.1, 1.0))):
            draw(ax[i, j], R, P, view, ctr, 22.0, title='%s %s @%.0f%%\n%s  ring %d: turning %.2f deg, concentration %+.2f deg vs neutral' % (nm, pn, fr * 100, tag, kj + 1, th[kj], ex) if i == 0 else '%s (dorsal view)' % tag)
    plt.tight_layout(); fo = os.path.join(OD, 'TM_%s_%s_%04d.png' % (nm.replace('@', '_').replace('.', 'p'), pn, round(fr * 1000))); plt.savefig(fo, dpi=100); plt.close(fig); print('wrote', fo, flush=True)
