# crops.py : isolated hand / foot inspection crops (derived npz, source frame). Hand = the connected piece of the side's mesh
# below z 108.5 cm that contains the construction wrist (so the thigh, which the palm faces, is never included).
import sys, numpy as np, scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
sys.path.insert(0, '/tmp/claude-0/src3d/v5/tools'); from hand_frame import frame
def comp_keep(V, F, k, seed):
    Fk = F[k]; n = len(V); E = np.r_[Fk[:, [0, 1]], Fk[:, [1, 2]], Fk[:, [2, 0]]] if F.shape[1] == 3 else np.r_[Fk[:, [0, 1]], Fk[:, [1, 2]], Fk[:, [2, 3]], Fk[:, [3, 0]]]
    A = sp.coo_matrix((np.ones(len(E)), (E[:, 0], E[:, 1])), shape=(n, n)); nc, lab = connected_components(A, directed=False)
    used = np.unique(Fk); vi = used[np.argmin(np.linalg.norm(V[used] - seed, axis=1))]
    idx = np.nonzero(k)[0]; return idx[lab[Fk[:, 0]] == lab[vi]]
for nm, src in (('v005', '/tmp/claude-0/src3d/v5/v005.npz'), ('v003', '/tmp/claude-0/rt/frz/v003_frz.npz')):
    z = np.load(src); V = z['V']; F = np.asarray(z['Q']); VF = V[F]
    for s, sg in (('l', 1), ('r', -1)):
        W, _ = frame(s.upper())
        k = ((sg * VF[:, :, 0] > 15) & (VF[:, :, 2] < 108.5)).all(1); np.savez('hand_%s_%s.npz' % (nm, s), V=V, Q=F[comp_keep(V, F, k, W)])
        k = ((sg * VF[:, :, 0] > 4.0) & (VF[:, :, 2] < 11)).all(1); np.savez('foot_%s_%s.npz' % (nm, s), V=V, Q=F[k])
    print(nm, 'crops ok')
# arm-free trunk for unobstructed hip side views: drop faces lateral of |x| 24 cm between z 95 and 160 (the hanging arm/hand)
for nm, src in (('v005', '/tmp/claude-0/src3d/v5/v005.npz'), ('v003', '/tmp/claude-0/rt/frz/v003_frz.npz')):
    z = np.load(src); V = z['V']; F = np.asarray(z['Q']); VF = V[F]
    k = ~((np.abs(VF[:, :, 0]) > 24.0) & (VF[:, :, 2] > 95) & (VF[:, :, 2] < 160)).any(1); np.savez('noarm_%s.npz' % nm, V=V, Q=F[k])
    print(nm, 'noarm ok')
