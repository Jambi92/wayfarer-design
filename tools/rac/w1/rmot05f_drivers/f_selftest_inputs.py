# RAC RM-OT-05F pipeline self-test inputs (NOT sculpt candidates). Writes OBJs into WORK/selftest:
#   T0 identity  : the template itself (must ingest PASS and rebuild the unorganized route exactly, volume 1.0000)
#   T1 transport : the failed 05D E1 organized reference surface used purely as a known non-zero displacement signal, to prove that the
#                  ingest -> skinned-frame field -> build path reproduces a delivered surface at the reference state and transports it to
#                  low / Narrow / Broad. E1 remains a FAILED candidate; T1 is never a reference or a candidate.
#   X1 scale     : template scaled 1.02 about the ground origin       -> must FAIL I2 / I3
#   X2 floor     : thigh region pushed 4 cm inward along the normal   -> must FAIL I5
#   X3 no-touch  : left hand / digits moved 1 cm                      -> must FAIL I4
import os, numpy as np
from f_common import *
if __name__ == '__main__':
    O = WORK + '/selftest'; os.makedirs(O, exist_ok=True)
    V, B, L, J, f, z0 = route_state(SKELETON_BODY); F = B['F']; keep = B['keep'].astype(bool)
    write_obj(O + '/T0.obj', V, F, 'self-test T0 identity')
    E = np.load(CG.path('GO5DE1') + '_r6.npz', allow_pickle=True)['V'].astype(float); write_obj(O + '/T1.obj', E, F, 'self-test T1 transport signal (failed E1 surface)')
    X = V.copy(); X[:, :2] *= 1.02; X[:, 2] *= 1.02; write_obj(O + '/X1.obj', X, F, 'self-test X1 uniform scale')
    n = TE.outward_normals(V, F, keep); th = np.maximum(B['w_thigh_l'], B['w_thigh_r']) > 0.8
    X = V.copy(); X[th] -= 4.0 * n[th]; write_obj(O + '/X2.obj', X, F, 'self-test X2 inside the true floor')
    X = V.copy(); h = (B['w_hand_l'] + B['w_fingers_l']) > 0.5; X[h, 1] += 1.0; write_obj(O + '/X3.obj', X, F, 'self-test X3 hand moved')
    print('ok')
