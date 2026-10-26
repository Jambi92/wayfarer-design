# v3diag.py CORE.npz : per-station diagnosis of a v003 core state (both configurations)
import sys, os, json, numpy as np, scipy.sparse as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core3lib import *
B = load(); z = np.load(sys.argv[1]); M3 = sp.csr_matrix((z['M_data'], z['M_indices'], z['M_indptr']), shape=tuple(z['M_shape'])); Q = B['Q2']; nV = M3.shape[0]
loops = closed_loops(Q, nV); pin = z['pin']
for C in 'MF':
    R = full_s7(M3 @ B[C]['Vh'], Q, B[C]['meta'], loops)
    for k, r in sorted(R.items()):
        if not r['strict']:
            print(C, '%-12s' % k, 'firm' if r['firm'] else 'FIRM-FAIL', 'loops %d (band %d %s, rings %d) need %d' % (r['loops_s7'], r['loops'], r['loops_by_side'], r['closed_rings'], r['required']),
                  'merged', r['merged'], 'crease', r['crease'], 'w2', r['within2'], 'poles', [(p, round(t, 2), bool(pin[p])) for p, t in zip(r['pole_ids'], r['pole_t'])], 'h %.2f' % r['h'])
