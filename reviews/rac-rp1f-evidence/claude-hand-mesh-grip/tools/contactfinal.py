# contactfinal.py -- RIG SIDE TASK.json OUT.json KV.json : fixture contact per digit at the LAST frame using the
# delivered (key-blended) corrective, i.e. the geometry Blender shows.
import sys, json, numpy as np
src = open('/tmp/claude-0/hand/tools/keyverify.py').read()
pre = src[:src.index('from scipy.optimize import nnls')]
a = sys.argv[sys.argv.index('--') + 1:]; kvj = a[4]
sys.argv = ['x', '--'] + a[:4] + ['/tmp/_cf.json']
exec(pre)
K = json.load(open(kvj)); i = nF - 1; w = K['weights'][str(i)]
O = np.zeros((nV, 3))
for k, x in w.items():
    idx, d = OFF[int(k)]; O[idx] += x * d
ang = FR[i]['angles']; P = H.pose(ang) + np.einsum('nij,nj->ni', dq_rot(ang), O)
sd = fixture_sd(P, T['fixture']); res = {}
for j, k in enumerate(digs):
    m = own == j
    if m.any(): res[k] = round(float(sd[m].min() * 1000), 3)
res['palm'] = round(float(sd[own < 0].min() * 1000), 3)
print(json.dumps(dict(contact_mm=res, CONTACT_mm=CONTACT * 1000, FIX_TOL_mm=FIX_TOL * 1000)))
