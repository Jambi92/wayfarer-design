# sa6_layer_render.py OUTDIR BODYDIR:NAME:POSE:FRAC [...] : close-up evidence for the corrective-layer validation (order 3e76b509).
#   Per case three panels at the same view, centred on the rig-owned defects: plain LBS | base correctives only | production (base + creator layers of
#   RP6_LAYERS).  Red = rig-owned folded quads, orange = vertices of rig-owned tear edges / new contact; composition-owned folds (closure rules, as in
#   sa6_blend.evaluate) are left grey.  Draw routine = sa6_render.draw (extracted from its source, not re-implemented).
import sys, os, ast, json, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection, LineCollection
from scipy.spatial import cKDTree
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sa6_correctives as CC, sa6_fit as FT, sa6_layer_harness as H, sa6_blend as BL
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sa6_render.py')).read()
exec(compile(ast.Module([n for n in ast.parse(src).body if isinstance(n, ast.FunctionDef) and n.name in ('view_basis', 'draw')], []), 'sa6_render', 'exec'))
OD = sys.argv[1]; os.makedirs(OD, exist_ok=True)
for case in sys.argv[2:]:
    BD, nm, pn, fr = case.split(':'); fr = float(fr); b = json.load(open(os.path.join(BD, 'bodies.json')))['bodies'][nm]
    R, z = BL.rig_of(nm, b, BD); Sv = CC.Solver(R); F = np.r_[R.Q[:, [0, 1, 2]], R.Q[:, [0, 2, 3]]].astype(np.int64); w0 = FT.wn_out(R.V, F)
    Bc = H.load_base(R, b['cfg']); P = H.Blend(Bc, [(w, H.load_state(R, s)[0]) for s, w in b['w'].items()])
    T = R.pose([(bb, p, a, dg * fr) for bb, p, a, dg in R.suite('anat')[pn]]); pts = z['pts']; kd = cKDTree(pts) if len(pts) else None; inv = z['rest_inverted']
    cols = []
    for tag, dl in (('plain LBS', None), ('base correctives only', Bc.delta(T)), ('production (base + layers)', P.delta(T))):
        Pp = R.skin(T) if dl is None else R.skin(T, R.V + dl); f = np.nonzero(R.relcos(Pp, T) < 0)[0]; cols.append((tag, Pp, f))
    lbs_f = cols[0][2]
    def own(f):
        if not len(f): return f
        near = (kd.query(R.V[R.Q[f]].mean(1))[0] <= 1.0) if kd is not None else np.zeros(len(f), bool)
        return f[~((near & np.isin(f, lbs_f)) | inv[f])]
    Pp = cols[2][1]; rf = own(cols[2][2]); te = Sv.tear_edges(Pp)[0]; tv = np.zeros(R.nv, bool); tv[Sv._E1[te].ravel()] = True
    pen = FT.penetration(R, Pp, F, w0) & ~FT.penetration(R, cols[0][1], F, w0); mark = tv | pen
    foc = R.V[R.Q[rf]].mean((0, 1)) if len(rf) else (R.V[mark].mean(0) if mark.any() else R.V.mean(0))
    ctr = Pp[R.Q[rf]].mean((0, 1)) if len(rf) else (Pp[mark].mean(0) if mark.any() else Pp.mean(0))
    lat = ctr - Pp.mean(0); lat[2] = 0; view = (np.sign(lat[0]) or 1.0, 0.35, 0.25) if abs(lat[0]) > abs(lat[1]) else (0.25, np.sign(lat[1]) or 1.0, 0.25)
    rad = 40.0 if pn.startswith('tail') else 22.0
    fig, ax = plt.subplots(1, 3, figsize=(13, 4.6))
    for a_, (tag, Pq, f) in zip(ax, cols):
        o = own(f); draw(a_, R, Pq, view, ctr, rad, flips=o, pen=mark if tag.startswith('production') else None,
                         title='%s  %s @%.0f%%\n%s: folds %d, rig-owned %d' % (nm, pn, fr * 100, tag, len(f), len(o)))
    plt.tight_layout(); fo = os.path.join(OD, 'SA_RP6_layer_%s_%s_%03d.png' % (nm.replace('@', '_').replace('.', 'p'), pn, round(fr * 100))); fig.savefig(fo, dpi=100); plt.close(fig)
    print('wrote', fo, 'rig-owned folds', len(rf), 'tear/contact verts', int(mark.sum()), flush=True)
