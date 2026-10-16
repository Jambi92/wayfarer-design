# RM-OT-05AC: per-checkpoint sculpt masks (1 = masked / not sculptable) for the 05AB1 clean baseline, built from the protection
# mask plus the 05AB rig groups (rest-pose labels; vertex order is shared). Masks only restrict WHERE brushes can act.
#   AC1 torso + shoulder girdle: everything masked except the trunk below the neck (not the tail) and the deltoid cap
#       (upper-arm vertices within 9 cm below the shoulder joint height).
#   AC2 arms + legs: everything masked except upper arm, forearm, thigh, shin (wrists, ankles, hands, feet stay protected).
#   AC3 posterior: everything masked except the gluteal / posterior-thigh zone (trunk + thigh, behind the hip-joint plane,
#       between 74 and 104 cm rest height), tail and its fused root still protected.
# Edges are feathered 1.5 cm. Usage: python3 ac_region_masks.py BASE_V_F.npz PROTECT.npy WEIGHTS_cp2.npz JOINTS_C.json OUTDIR
import sys, os, json, numpy as np
from scipy.spatial import cKDTree
bp, pp, wp, jp, od = sys.argv[1:6]
V = np.load(bp)['V'].astype(float) * 100; P = np.load(pp).astype(float)
W = np.load(wp); names = [str(x) for x in W['names']]; lab = W['label_welded'][W['welded_index']]; Wt = W['weights_welded'][W['welded_index']]
J = json.load(open(jp)); OFF = np.array([6.888, -39.481, 0.0]); g = lambda n: Wt[:, names.index(n)]
trunk = g('trunk'); arm = g('upperarm_L') + g('upperarm_R'); fore = g('forearm_L') + g('forearm_R'); thigh = g('thigh_L') + g('thigh_R'); shin = g('shin_L') + g('shin_R')
shz = min(J['shoulder_L'][2], J['shoulder_R'][2]); hipy = (np.array(J['hip_L']) + OFF)[1]
def feather(allow, fe=1.5):
    m = np.ones(len(V)); m[allow] = 0.0
    if (~allow).any() and allow.any():
        d, _ = cKDTree(V[~allow]).query(V[allow]); m[allow] = np.clip(1 - d / fe, 0, 1)
    return np.maximum(m, P)
regions = {
    'AC1': (trunk > 0.5) & (V[:, 2] < 168.3) | ((arm > 0.5) & (V[:, 2] > shz - 9)),
    'AC2': ((arm + fore + thigh + shin) > 0.5),
    'AC3': ((trunk + thigh) > 0.5) & (V[:, 1] > hipy) & (V[:, 2] > 74) & (V[:, 2] < 104)}
rep = {}
os.makedirs(od, exist_ok=True)
for k, allow in regions.items():
    m = feather(allow & (P < 1)); np.save(os.path.join(od, 'GO-05AC_mask_%s.npy' % k), m.astype(np.float32)); rep[k] = dict(sculptable_vertices=int((m < 0.5).sum()))
print(json.dumps(rep))
