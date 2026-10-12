# section breadth / depth profile of the trunk (fast_stations trunk mask: arm weight < 0.2; exact plane sections) for one or more OBJs
import sys, numpy as np
from k_envelope import *
V0, B, L, J, f, z0 = route_state(SKELETON_BODY); keep = B['keep'].astype(bool)[:NBODY]
w = lambda k: B['w_' + k][:NBODY]
armw = np.maximum.reduce([w(x) for x in ('upperarm_l', 'upperarm_r', 'lowerarm_l', 'lowerarm_r', 'hand_l', 'hand_r', 'fingers_l', 'fingers_r')])
F = B['F']; F = F[(F < NBODY).all(1)]; tr = keep & (armw < 0.2); TF = F[tr[F].all(1)]
def sec(V, z):
    A, Bq, C = V[TF[:, 0]], V[TF[:, 1]], V[TF[:, 2]]; P = []
    for a, b in ((A, Bq), (Bq, C), (C, A)):
        m = (a[:, 2] - z) * (b[:, 2] - z) < 0; t = (z - a[m, 2]) / (b[m, 2] - a[m, 2]); P.append(a[m, :2] + (b[m, :2] - a[m, :2]) * t[:, None])
    P = np.vstack(P); return np.ptp(P[:, 0]), np.ptp(P[:, 1])
Ms = [read_obj(p)[0] for p in sys.argv[1:]]
for z in np.arange(112, 188, 3.0):
    print('%5.1f ' % z + ' | '.join('%5.1f %5.1f' % sec(V, z) for V in Ms))
