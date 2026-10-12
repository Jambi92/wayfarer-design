# rdiag.py SID : locate the re-entry guard failures of GO5F<SID> (read-only diagnostic)
import sys, json, numpy as np
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/rmot05f_drivers')
from f_common import *
import arm_clearance as AC
sid = sys.argv[1]; n = 'GO5F' + sid
B = np.load(CG.path(n) + '_r6.npz', allow_pickle=True); V = B['V'].astype(float); F = B['F']; keep = B['keep'].astype(bool)
V0, B0, L0, J0, f0, z00 = route_state(SKELETON_BODY)
Vr = CG.route_baseline(B)
R = regions(B, V0, J0)
lab = np.array(['-'] * len(V), dtype=object)
for k, m in R.items(): lab[m] = k[:14]
def wtop(i):
    ws = {k[2:]: float(B[k][i]) for k in B.files if k.startswith('w_') and B[k].ndim == 1 and len(B[k]) == len(V)}
    return sorted(ws.items(), key=lambda x: -x[1])[:3]
# delivered raw delta
Vs = read_obj(sys.argv[2])[0] if len(sys.argv) > 2 else None
# hand digit
hf = np.clip(sum(B['w_' + k] for k in ('hand_l', 'hand_r', 'fingers_l', 'fingers_r', 'ball_l', 'ball_r', 'toes_l', 'toes_r') if 'w_' + k in B.files), 0, 1) > 0.5
d = np.abs(V - Vr).max(1); idx = np.where(keep & hf & (d > 0.5))[0]
print('HAND/DIGIT >0.5:', len(idx), 'max', d[keep & hf].max())
for i in idx[np.argsort(-d[idx])][:12]:
    raw = np.linalg.norm(Vs[i] - V0[i]) if Vs is not None and i < NBODY else None
    print('  ', i, lab[i], np.round(V[i], 1), 'chg %.2f raw %.2f' % (d[i], raw if raw is not None else -1), wtop(i))
# floor
L = dict(np.load(CG.path(json.loads(str(B['meta'])).get('skeleton', n + '-LEAN').replace('-LEAN', '')) + '-LEAN_r6.npz', allow_pickle=True))
J = json.loads(str(B['joints']))
Fv = TE.floor(L['V'].astype(float), L)[0]
JL = json.loads(str(L['joints'])); a = np.array([JL[k][0] for k in JL]); b = np.array([J[k][0] for k in JL])
sc = np.sqrt(((b - b.mean(0)) ** 2).sum() / ((a - a.mean(0)) ** 2).sum()); Fb = (Fv - a.mean(0)) * sc + b.mean(0)
nF = TE.outward_normals(Fb, F, keep); sd = np.einsum('ij,ij->i', V - Fb, nF)
ext = np.clip(B['w_head'] + B['w_neck_01'] + B['w_hand_l'] + B['w_hand_r'] + B['w_fingers_l'] + B['w_fingers_r'], 0, 1) >= 0.3
bad = np.where(keep & ~ext & (sd < -0.2))[0]
print('FLOOR:', len(bad))
for i in bad:
    raw = np.linalg.norm(Vs[i] - V0[i]) if Vs is not None else -1
    print('  ', i, lab[i], np.round(V[i], 1), 'sd %.2f raw %.2f' % (sd[i], raw), wtop(i))
# arm clearance
armw = np.maximum.reduce([B['w_' + x] for x in ("upperarm_l", "upperarm_r", "lowerarm_l", "lowerarm_r", "hand_l", "hand_r", "fingers_l", "fingers_r")])
trunk = keep & (armw < 0.05)
for s in ('l', 'r'):
    sh = J["upperarm_" + s][0]; el = J["lowerarm_" + s][0]
    ua = np.where(keep & (B["w_upperarm_" + s] > 0.5) & (V[:, 2] < sh[2] - 2) & (V[:, 2] > el[2]))[0]
    ss = AC.section_signed(V, F, trunk, V[ua]); ins = ua[ss < 0]
    print('ARM', s, 'inside', len(ins), 'shoulder z %.1f elbow z %.1f' % (sh[2], el[2]))
    for i in ins: print('  ', i, lab[i], np.round(V[i], 1), 'ss %.2f' % ss[list(ua).index(i)])
    # nearest trunk point and its label
    from scipy.spatial import cKDTree
    tz = np.where(trunk)[0]; kd = cKDTree(V[tz])
    for i in ins:
        dd, j = kd.query(V[i]); j = tz[j]; print('     nearest trunk', j, lab[j], np.round(V[j], 1), 'd %.2f' % dd, 'raw trunk move', np.round(Vs[j] - V0[j], 2) if Vs is not None and j < NBODY else '')
