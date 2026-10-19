import numpy as np, json, sys, subprocess
from scipy.spatial import cKDTree
nrings = int(sys.argv[1])
subprocess.run(['/home/claude/stc/bin/python3', 'blendcage.py', '--', '/mnt/user-data/uploads/RaceBodies/production/Gorrund/RP1/GO_U_REF_RP1E_retopo_v006.blend', 'ui_cur.npz'], capture_output=True)
z = np.load('ui_cur.npz'); V = z['V']
base = np.load('ui_v006a.npz')['V']
p = json.load(open('feet_plan.json'))
T = np.vstack([np.array(p[s]['rings'][k]) for k in range(1, nrings + 1) for s in 'LR'])
d, _ = cKDTree(base).query(V); new = V[d > 1e-3]
dd, ii = cKDTree(T).query(new)
print('verts', len(V), 'new', len(new), 'expected', len(T), 'max dev from target mm %.3f' % (dd.max() * 10), 'targets hit', len(set(ii.tolist())))
bad = np.where(dd > 0.02)[0]
for b in bad: print('  off', new[b].round(2), 'nearest target', T[ii[b]].round(2), 'dist cm %.2f' % dd[b])
