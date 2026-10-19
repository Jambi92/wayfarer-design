import numpy as np, json, sys, subprocess
from scipy.spatial import cKDTree
# usage: cktoes.py "Lt1:1,Lt3:1,Rt1:1,Rt3:1"  (rings placed per tube)
spec = dict((k, int(v)) for k, v in (x.split(':') for x in sys.argv[1].split(',') if x))
subprocess.run(['/home/claude/stc/bin/python3', 'blendcage.py', '--', '/mnt/user-data/uploads/RaceBodies/production/Gorrund/RP1/GO_U_REF_RP1E_retopo_v006.blend', 'ui_cur.npz'], capture_output=True)
z = np.load('ui_cur.npz'); V = z['V']; base = np.load('ui_v006a.npz')['V']
p = json.load(open('feet_plan.json'))
T = [np.array(p[s]['rings'][k]) for k in range(1, 7) for s in 'LR']
for key, n in spec.items():
    T += [np.array(r) for r in p[key[0]]['tubes'][key[1:]][:n]]
T = np.vstack(T) / 100 if False else np.vstack(T)
d, _ = cKDTree(base).query(V); new = V[d > 1e-3]
dd, ii = cKDTree(T).query(new)
print('verts', len(V), 'faces', len(z['F']), 'new', len(new), 'expected', len(T), 'max dev mm %.3f' % (dd.max() * 10), 'unique hit', len(set(ii.tolist())))
for b in np.where(dd > 0.02)[0]: print('  off', new[b].round(2), 'nearest', T[ii[b]].round(2), 'cm %.2f' % dd[b])
