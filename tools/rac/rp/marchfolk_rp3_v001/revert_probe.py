# revert_probe.py CORE.npz STATION C : effect of reverting relocated vertices near a station back to their v002 rows (diagnostic)
import sys, os, json, numpy as np, scipy.sparse as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core3lib import *
B = load(); z = np.load(sys.argv[1]); nm = sys.argv[2]; M3 = sp.csr_matrix((z['M_data'], z['M_indices'], z['M_indptr']), shape=tuple(z['M_shape'])); Q = z['Q']; nV = M3.shape[0]
loops = closed_loops(Q, nV)
# base rows: v002 rows + ring rows as built (rings rows = midpoints of base rows) -> rebuild from v003_build ring stage is heavy; use: v002 rows for ids < n2
M2 = B['M2']; n2 = M2.shape[0]; mv = z['moved']
for C in sys.argv[3].split(','):
    S = {s[0]: s for s in stations(B[C]['meta'])}; c = np.asarray(S[nm][1]); V = M3 @ B[C]['Vh']
    for rad in (4, 6, 8, 10, 14):
        ids = mv[(mv < n2) & (np.linalg.norm(V[mv] - c, axis=1) < rad)]
        Ml = M3.tolil(copy=True); M2l = M2.tolil()
        for v in ids: Ml.rows[v] = list(M2l.rows[v]); Ml.data[v] = list(M2l.data[v])
        Mx = Ml.tocsr(); out = {}
        for CC in 'MF':
            R = full_s7(Mx @ B[CC]['Vh'], Q, B[CC]['meta'], loops); out[CC] = sorted(k for k, r in R.items() if not r['firm'])
        print(C, nm, 'revert radius', rad, 'verts', len(ids), 'firm fails', out, flush=True)
