# sa6_shoulder_ba.py OUTDIR [render | compose] : shoulder / elbow before-after evidence (order 07a3f24c §5).
#   render (run once per rig: RP6_RIG unset = archived v001 rig + base correctives v002, RP6_RIG=v002 = corrected rig + base correctives v003):
#     c1 / c2, the corrected shoulder poses (abduction 45 / 90, flexion 60 / 90, both sides), combined shoulder + elbow (abd90 + elbow 90, flex90 + elbow 130),
#     front / side / rear views around the shoulder; flipped quads red, interpenetrating vertices' quads orange; per panel the total / humeral / girdle split.
#     OUTDIR/<rig>/<cfg>_<pose>_<view>.png + stats.json (flips, penetrating vertices per panel).
#   compose: one sheet per (cfg, pose) with v001 (top) vs v002 (bottom) rows across the three views -> OUTDIR/sheet_<cfg>_<pose>.png.
import sys, os, json, ast, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection, LineCollection
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
OD = sys.argv[1]; MODE = sys.argv[2] if len(sys.argv) > 2 else 'render'
POSES = ['shoulder_abd45_xneg', 'shoulder_abd90_xneg', 'shoulder_abd90_xpos', 'shoulder_flex60_xneg', 'shoulder_flex90_xneg', 'abd90+elbow90_xneg', 'flex60+elbow130_xneg']   # shoulder_flex90 = 1.5 x the defined flex60 pose: BEYOND the gated range, rendered as a record only
VIEWS = dict(front=(0, 1, 0), side=(-1, 0.15, 0.1), rear=(0, -1, 0))
if MODE == 'render':
    import sa6_common as C, sa6_pose as SP, sa6_fit as FT, sa6_layer_harness as H
    src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sa6_render.py')).read()
    exec(compile(ast.Module([n for n in ast.parse(src).body if isinstance(n, ast.FunctionDef) and n.name in ('view_basis', 'draw')], []), 'r', 'exec'))
    od = os.path.join(OD, C.RIGV); os.makedirs(od, exist_ok=True); st = {}
    for cfg in 'MF':
        R = SP.Rig(cfg, C.w_path(cfg)); B = H.load_base(R, cfg); A = R.suite('anat')
        Ft = np.r_[R.Q[:, [0, 1, 2]], R.Q[:, [0, 2, 3]]].astype(np.int64); w0 = FT.wn_out(R.V, Ft)
        def spec_of(p):
            s = p.rsplit('_', 1)[1]
            if p.startswith('abd90+elbow90'): return list(A['shoulder_abd90_' + s]) + SP.Rig.scaled(R, A['elbow_130_' + s], 90 / 130.)
            if p.startswith('flex60+elbow130'): return list(A['shoulder_flex60_' + s]) + list(A['elbow_130_' + s])
            if p.startswith('shoulder_flex90'): return SP.Rig.scaled(R, A['shoulder_flex60_' + s], 1.5)
            return list(A[p])
        for p in POSES:
            sp = spec_of(p); T = R.pose(sp); P = R.skin(T, R.V + B.delta(T)); fl = np.nonzero(R.relcos(P, T) < 0)[0]; pen = FT.penetration(R, P, Ft, w0)
            side = 'r' if p.endswith('xneg') else 'l'; gh = R.H('upperarm_' + side); gh = T['upperarm_' + side][0] @ gh + T['upperarm_' + side][1]
            ex = R.expand(sp) if hasattr(R, 'expand') else sp
            split = ', '.join('%s %.1f' % (e[0], e[3]) for e in ex if e[0].startswith(('clavicle', 'upperarm', 'forearm')))
            st['%s_%s' % (cfg, p)] = dict(flips=int(len(fl)), penetrating_vertices=int(pen.sum()), split=split)
            for vn, vv in VIEWS.items():
                vv = np.array(vv, float)
                if side == 'l': vv = vv * [-1, 1, 1]
                f, ax = plt.subplots(figsize=(5, 5)); draw(ax, R, P, vv, flips=fl, pen=pen); x, y, _ = view_basis(vv)
                c = np.array([gh @ x, gh @ y]); ax.set_xlim(c[0] - 32, c[0] + 32); ax.set_ylim(c[1] - 36, c[1] + 28)
                ax.set_title('rig %s %s %s %s\n%s | flips %d pen %d' % (C.RIGV, cfg, p, vn, split, len(fl), int(pen.sum())), fontsize=7)
                plt.tight_layout(); plt.savefig(os.path.join(od, '%s_%s_%s.png' % (cfg, p, vn)), dpi=80); plt.close(f)
            print(C.RIGV, cfg, p, st['%s_%s' % (cfg, p)], flush=True)
    json.dump(st, open(os.path.join(od, 'stats.json'), 'w'), indent=1)
else:
    from PIL import Image
    for cfg in 'MF':
        for p in POSES:
            rows = []
            for rig in ('v001', 'v002'):
                ims = [Image.open(os.path.join(OD, rig, '%s_%s_%s.png' % (cfg, p, v))) for v in VIEWS]
                w, h = ims[0].size; row = Image.new('RGB', (w * len(ims), h), 'white')
                for i, im in enumerate(ims): row.paste(im, (i * w, 0))
                rows.append(row)
            sh = Image.new('RGB', (rows[0].size[0], rows[0].size[1] * 2), 'white'); sh.paste(rows[0], (0, 0)); sh.paste(rows[1], (0, rows[0].size[1]))
            sh.save(os.path.join(OD, 'sheet_%s_%s.png' % (cfg, p)))
    print('sheets', len(POSES) * 2)
