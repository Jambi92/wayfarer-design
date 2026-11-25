# sa6_pleat_arm_render.py STATE POSE[,POSE] : corrected-system pleat close-ups for the visual review (rig v002 pass 9b): plain LBS | state layer front | top, pleated quads red. ARMOUT = output dir.
import sys, os, ast, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection, LineCollection
sys.path.insert(0, os.getcwd())
import sa6_pd2_fit as PF, sa6_correctives as CC, sa6_gates as GT
src = open('sa6_render.py').read()
exec(compile(ast.Module([n for n in ast.parse(src).body if isinstance(n, ast.FunctionDef) and n.name in ('view_basis', 'draw')], []), 'sa6_render', 'exec'))
nm, poses = sys.argv[1], sys.argv[2].split(',')
R, cfg = PF.state_rig(nm); K = CC.Correctives.load(R, '/tmp/claude-0/rp6/layers9b/CF_state_%s.json' % nm); S = CC.Solver(R); S.tear_edges(R.V); S.pleat_edges(R.V)
PS = dict(R.suite('anat')); PS.update({'gate:' + k: v for k, v in GT.gate_poses(R).items()})
fig, axs = plt.subplots(len(poses), 3, figsize=(15, 5 * len(poses)), squeeze=False)
for i, pn in enumerate(poses):
    T = R.pose(PS[pn]); P = R.skin(T, R.V + K.delta(T)); L = R.skin(T)
    x = np.abs(S._dih(P) - S._d0) > 90; q = np.unique(S._pq[x].ravel()); xl = np.abs(S._dih(L) - S._d0) > 90; ql = np.unique(S._pq[xl].ravel())
    c = P[R.Q[q]].mean((0, 1)) if len(q) else P[R.Q[ql]].mean((0, 1))
    for j, (PP, qq, tt, vw) in enumerate([(L, ql, 'plain LBS', [0, -1, 0.3]), (P, q, 'state layer (front)', [0, -1, 0.3]), (P, q, 'state layer (top)', [0.3, -0.3, 1])]):
        draw(axs[i, j], R, PP, vw, centre=c, rad=14, flips=qq, title='%s %s: %s, %d pleated quads' % (nm, pn, tt, len(qq)))
fig.tight_layout(); fig.savefig(os.environ.get('ARMOUT', '/tmp/claude-0/rp6/armpleat') + '/%s.png' % nm, dpi=70); print('ok', nm)
