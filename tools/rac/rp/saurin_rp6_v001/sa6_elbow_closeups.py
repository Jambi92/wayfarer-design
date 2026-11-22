# sa6_elbow_closeups.py OUTDIR [BODIES] : elbow-muscle close-ups (order 07a3f24c §2 / §5), rig v002.
#   Bodies: base M (c1), base F (c2) with base correctives v003; heavy-body controls FAHI, MUFAHI (state bodies with their v005 state layers = the fitted
#   CF_state sets).  Right arm, elbow flexion 0 / 45 / 90 / 130 deg, lateral and anterior views of the upper arm, WITHOUT the muscle layer (its families
#   removed) vs WITH it; a third row = the muscle layer's own displacement magnitude as a heat map (same scale per body).  Plus one combined shoulder +
#   elbow strip (abduction 90 + elbow 0 / 90 / 130).  OUTDIR/elbow_<body>.png, OUTDIR/elbow_shoulder_<body>.png.
import sys, os, ast, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection, LineCollection
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
assert os.environ.get('RP6_RIG') == 'v002'
import sa6_common as C, sa6_pose as SP, sa6_correctives as CC, sa6_layer_harness as H, sa6_pd2_fit as PF
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sa6_render.py')).read()
exec(compile(ast.Module([n for n in ast.parse(src).body if isinstance(n, ast.FunctionDef) and n.name in ('view_basis', 'draw')], []), 'r', 'exec'))
OD = sys.argv[1]; os.makedirs(OD, exist_ok=True); BODIES = (sys.argv[2] if len(sys.argv) > 2 else 'M,F,FAHI,MUFAHI').split(',')
LAYERS = os.environ.get('LAYERS_DIR', '/tmp/claude-0/rp6/layers5'); ANG = (0, 45, 90, 130)
def body(nm):
    if nm in ('M', 'F'): R = SP.Rig(nm, C.w_path(nm)); return R, H.load_base(R, nm)
    R, cfg = PF.state_rig(nm); return R, CC.Correctives.load(R, os.path.join(LAYERS, 'CF_state_%s.json' % nm))
def without_muscle(R, K):
    K2 = CC.Correctives(R); K2.F = {k: f for k, f in K.F.items() if not f.get('layer')}; K2.PK = K.PK; return K2
for nm in BODIES:
    R, K = body(nm); K0 = without_muscle(R, K); A = R.suite('anat'); s130 = A['elbow_130_xneg']
    rows = [('without muscle layer', K0), ('with muscle layer', K)]; views = [('lateral', (-1, 0.15, 0)), ('anterolateral', (-0.8, 0.6, 0.45))]   # the medial side of the right arm faces the trunk
    f, axs = plt.subplots(len(rows) * 2 + 1, len(ANG), figsize=(4 * len(ANG), 4 * (len(rows) * 2 + 1)))
    vmax = None
    for j, a in enumerate(ANG):
        sp = SP.Rig.scaled(R, s130, a / 130.) if a else []; T = R.pose(sp); E = T['upperarm_r'][0] @ R.H('forearm_r') + T['upperarm_r'][1]
        P = {lab: R.skin(T, R.V + k.delta(T)) for lab, k in rows}; dm = np.linalg.norm(K.delta(T) - K0.delta(T), axis=1)
        if vmax is None: vmax = max(1e-3, np.linalg.norm(K.delta(R.pose(s130)) - K0.delta(R.pose(s130)), axis=1).max())
        for i, (lab, _) in enumerate(rows):
            for v, (vn, vv) in enumerate(views):
                ax = axs[i * 2 + v, j]; vv = np.array(vv, float); draw(ax, R, P[lab], vv); x, y, _ = view_basis(vv); c = np.array([E @ x, E @ y])
                ax.set_xlim(c[0] - 20, c[0] + 14); ax.set_ylim(c[1] - 10, c[1] + 24); ax.set_title('%s | elbow %d | %s | %s' % (nm, a, vn, lab), fontsize=8)
        ax = axs[-1, j]; vv = np.array(views[0][1], float); draw(ax, R, P['with muscle layer'], vv, vals=dm[R.Q].mean(1), vmax=vmax, cmap='magma'); x, y, _ = view_basis(vv); c = np.array([E @ x, E @ y])
        ax.set_xlim(c[0] - 20, c[0] + 14); ax.set_ylim(c[1] - 10, c[1] + 24); ax.set_title('%s | elbow %d | muscle |d| max %.2f cm (scale 0-%.2f)' % (nm, a, dm.max(), vmax), fontsize=8)
    plt.tight_layout(); plt.savefig(os.path.join(OD, 'elbow_%s.png' % nm), dpi=55); plt.close(f)
    f, axs = plt.subplots(1, 3, figsize=(15, 5))
    for j, a in enumerate((0, 90, 130)):
        sp = list(A['shoulder_abd90_xneg']) + (SP.Rig.scaled(R, s130, a / 130.) if a else []); T = R.pose(sp); P = R.skin(T, R.V + K.delta(T))
        vv = np.array((0, 1, 0.2), float); draw(axs[j], R, P, vv, flips=np.nonzero(R.relcos(P, T) < 0)[0]); gh = T['upperarm_r'][0] @ R.H('upperarm_r') + T['upperarm_r'][1]
        x, y, _ = view_basis(vv); c = np.array([gh @ x, gh @ y]); axs[j].set_xlim(c[0] - 55, c[0] + 15); axs[j].set_ylim(c[1] - 35, c[1] + 35)
        axs[j].set_title('%s | shoulder abd 90 + elbow %d | flips %d' % (nm, a, int((R.relcos(P, T) < 0).sum())), fontsize=9)
    plt.tight_layout(); plt.savefig(os.path.join(OD, 'elbow_shoulder_%s.png' % nm), dpi=55); plt.close(f); print(nm, 'done', flush=True)
