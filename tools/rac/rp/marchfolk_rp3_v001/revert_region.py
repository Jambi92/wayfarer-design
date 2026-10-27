# revert_region.py CORE_IN.npz CORE_OUT.npz STATION[,STATION..] RADIUS_CM : restore (to their v002 / root-ring base rows) every relocated vertex that lies
# within RADIUS of the listed stations' centres in either configuration -- used to undo T-4 relaxation that degraded a large-reach band station
# (shoulder band rays reach ~1.5 R + W from the joint). Reports the §7 verdicts before / after for both configurations.
import sys, os, json, numpy as np, scipy.sparse as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core3lib import *
IN, OUT, names, rad = sys.argv[1], sys.argv[2], sys.argv[3].split(','), float(sys.argv[4])
B = load(); z = np.load(IN); Q = z['Q']; nV = int(z['M_shape'][0]); bs = np.load(W + '/v3_base.npz'); surf = Surface(B['A'], B['Qh'], bs['chart'])
Qb = B['Q2'].copy(); UVb = B['UV2'].copy(); Mb = B['M2'].copy(); loops0 = closed_loops(Qb, Mb.shape[0]); mir0 = mirror_map(Mb @ B['A'], 0.3)
RINGS = [('pinky_mcp_hypothenar_root', 412, 1006), ('toe1_mtp_root', 491, 1113), ('toe2_mtp_root', 497, 1120), ('toe3_mtp_root', 508, 1132), ('toe4_toe5_mtp_root', 520, 1147)]
for nm, la, lb in RINGS:
    for A_, B_ in ((loops0[la], loops0[lb]), (mir0[loops0[la]], mir0[loops0[lb]])): Qb, UVb, Mb, _ = insert_ring(Qb, UVb, Mb, A_.tolist(), B_.tolist())
assert np.array_equal(Qb, Q)
moved = {int(v): (int(t), b) for v, t, b in zip(z['moved'], z['tri'], z['bary'])}
def rows():
    Ml = Mb.tolil(copy=True)
    for v, (t, bc) in moved.items():
        row = {}
        for j, w in zip(surf.T[t], bc):
            if w > 1e-12: row[int(j)] = row.get(int(j), 0.0) + float(w)
        Ml.rows[v] = sorted(row); Ml.data[v] = [row[j] for j in sorted(row)]
    return Ml.tocsr()
loops = closed_loops(Q, nV); M = rows(); before = {C: full_s7(M @ B[C]['Vh'], Q, B[C]['meta'], loops) for C in 'MF'}
drop = set()
for C in 'MF':
    V = M @ B[C]['Vh']; S = {s[0]: s for s in stations(B[C]['meta'])}; mv = np.array(sorted(moved), int)
    for n_ in names: drop.update(mv[np.linalg.norm(V[mv] - np.asarray(S[n_][1]), axis=1) < rad].tolist())
for v in drop: moved.pop(v)
M = rows(); after = {C: full_s7(M @ B[C]['Vh'], Q, B[C]['meta'], loops) for C in 'MF'}
for C in 'MF':
    print(C, 'restored', len(drop), 'firm fail before', sorted(k for k, r in before[C].items() if not r['firm']), 'after', sorted(k for k, r in after[C].items() if not r['firm']))
    for n_ in names: print('   ', n_, before[C][n_]['loops_by_side'], '->', after[C][n_]['loops_by_side'])
UV3 = UVb.copy()
for f, q in enumerate(Q):
    for k, v in enumerate(q):
        if int(v) in moved:
            t, bc = moved[int(v)]; corners = [0, 1, 2] if surf.tk[t] == 0 else [0, 2, 3]; UV3[f, k] = (B['UVh'][surf.tq[t]][corners] * bc[:, None]).sum(0)
log = json.loads(str(z['log'])); log.setdefault('region_restore', []).append(dict(stations=names, radius_cm=rad, restored=len(drop)))
mv = np.array(sorted(moved), int)
np.savez_compressed(OUT, Q=Q, UV=UV3, M_data=M.data, M_indices=M.indices, M_indptr=M.indptr, M_shape=np.array(M.shape), moved=mv, tri=np.array([moved[v][0] for v in mv], int),
                    bary=np.array([moved[v][1] for v in mv]).reshape(-1, 3), pin=z['pin'], n_v002=z['n_v002'], log=json.dumps(log))
