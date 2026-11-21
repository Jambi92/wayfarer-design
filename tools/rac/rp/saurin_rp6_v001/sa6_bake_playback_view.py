# sa6_bake_playback_view.py OUT_PREFIX BODYDIR NAME ARTDIR POSE VIEW CROP_CM : reviewer-friendly playback of a per-body bake (standards order c65e6c93 §3).
#   Same frames as sa6_bake_playback.py (pose's full range in 1 s at 30 fps, 31 frames), but drawn for a person: the whole body in a fixed camera
#   (VIEW = front | back | left | right; left = looking from -x, right = from +x), cropped to CROP_CM around the moving joint, plain skin shading.
#   Left: the baked body.  Right: the same view coloured by how far the skin moved (relative to plain LBS) since the previous frame (cm, 0 -> 0.5).
#   Bottom: that per-frame movement over the whole move (baked = red, packaged blend v004 = blue dashed), with a marker at the current frame.
#   Writes OUT_PREFIX.gif (real time, 33 ms per frame, forward then reverse) and OUT_PREFIX_slow.gif (x4 slower).
import sys, os, io, json, ast, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection, LineCollection
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('RP6_LAYERS', 'SA_RP6_creator_layers_v004.json')
import sa6_correctives as CC, sa6_layer_harness as H, sa6_blend as BL
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sa6_render.py')).read()
exec(compile(ast.Module([n for n in ast.parse(src).body if isinstance(n, ast.FunctionDef) and n.name in ('view_basis', 'draw')], []), 'sa6_render', 'exec'))
OUT, BD, nm, AD, pn, VIEW, CROP = sys.argv[1:8]; CROP = float(CROP); NF = 30
VV = dict(front=(0, 1, 0), back=(0, -1, 0), left=(-1, 0, 0), right=(1, 0, 0))[VIEW]
b = json.load(open(os.path.join(BD, 'bodies.json')))['bodies'][nm]; R, z = BL.rig_of(nm, b, BD)
P0 = H.Blend(H.load_base(R, b['cfg']), [(w, H.load_state(R, s)[0]) for s, w in b['w'].items()]); K = CC.Correctives.load(R, os.path.join(AD, 'BK_%s.json' % nm))
spec = R.suite('anat')[pn]; full = max(abs(dg) for _, _, _, dg in spec); fr = np.arange(NF + 1) / NF
PB, RB, RP = [], [], []
for f in fr:
    T = R.pose([(bb, p, a, dg * f) for bb, p, a, dg in spec]); L = R.skin(T); dP = P0.delta(T); Pb = R.skin(T, R.V + dP + K.delta(T)); Pp = R.skin(T, R.V + dP)
    PB.append(Pb); RB.append(Pb - L); RP.append(Pp - L)
cb = np.array([np.zeros(R.nv)] + [np.linalg.norm(RB[k] - RB[k - 1], axis=1) for k in range(1, NF + 1)])
cp = np.array([np.zeros(R.nv)] + [np.linalg.norm(RP[k] - RP[k - 1], axis=1) for k in range(1, NF + 1)])
moving = cb.max(0) > 0.05; x, y, _ = view_basis(VV)
ctr = np.array([np.median(PB[NF][moving] @ x), np.median(PB[NF][moving] @ y)]) if moving.any() else np.array([0, 100.0])
deg = fr * full; frames = []
for k in range(NF + 1):
    fig = plt.figure(figsize=(9, 7.2)); g = fig.add_gridspec(2, 2, height_ratios=[3.2, 1])
    for j, (vals, t) in enumerate(((None, 'baked body'), (cb[k][R.Q].mean(1), 'skin movement this frame (pale = still, dark red = 0.5 cm)'))):
        ax = fig.add_subplot(g[0, j]); draw(ax, R, PB[k], VV, vals=vals, vmax=0.5, cmap='YlOrRd') if vals is not None else draw(ax, R, PB[k], VV)
        ax.set_xlim(ctr[0] - CROP, ctr[0] + CROP); ax.set_ylim(ctr[1] - CROP, ctr[1] + CROP); ax.set_aspect('equal'); ax.set_xticks([]); ax.set_yticks([]); ax.set_title(t, fontsize=8)
    ax = fig.add_subplot(g[1, :]); m = cb[1:].max(1); mp = cp[1:].max(1)
    ax.plot(deg[1:], m, 'r-', lw=1.5, label='baked'); ax.plot(deg[1:], mp, 'b--', lw=1, label='packaged blend v004'); ax.axhline(0.5, color='0.5', lw=0.7, ls=':')
    if k: ax.plot(deg[k], m[k - 1], 'ko', ms=7)
    ax.set_xlabel('joint angle (deg)'); ax.set_ylabel('max skin movement\nper frame (cm)', fontsize=8); ax.legend(fontsize=7, loc='upper left'); ax.set_xlim(0, full)
    fig.suptitle('%s  %s   %.0f deg  (frame %d/30, real time = whole move in 1 second)' % (nm, pn, deg[k], k), fontsize=10)
    buf = io.BytesIO(); plt.savefig(buf, dpi=72, format='png'); plt.close(fig); buf.seek(0); frames.append(Image.open(buf).convert('P', palette=Image.ADAPTIVE))
frames[0].save(OUT + '.gif', save_all=True, append_images=frames[1:] + frames[::-1], duration=33, loop=0)
frames[0].save(OUT + '_slow.gif', save_all=True, append_images=frames[1:] + frames[::-1], duration=133, loop=0)
print('wrote', OUT, flush=True)
