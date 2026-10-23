import sys, numpy as np
from scipy.spatial import cKDTree
R = '/tmp/claude-0/rp2/'
s = np.load(R + 'sstar.npz'); Q0 = s['Q']; V0 = s['V']; m0 = np.load(R + 'mir_body.npy')
cr = np.load(R + sys.argv[1]); b = np.load(R + 'sstar_p.npz'); Vp = b['V']; Qp = b['Q']; ax = np.load(R + 'axR_2.npy')
d, j = cKDTree(V0).query(Vp); fk = {frozenset(q): i for i, q in enumerate(Q0.tolist())}
axS = np.zeros(len(Q0), bool)
same = len(Qp) == len(Q0) and np.array_equal(Qp, Q0)
for i in np.where(ax)[0]:
    k = i if same else fk[frozenset(j[Qp[i]].tolist())]; axS[k] = True; axS[fk[frozenset(m0[Q0[k]].tolist())]] = True
ex = cr | axS; np.save(R + 'excl_quads.npy', ex); print('excluded', ex.sum(), 'crotch', cr.sum(), 'axillae', axS.sum())
