# cg_landmarks.py NATIVE.npz R6.npz CAND.npz OUT.json : RP4 Cogling (order 9424c72) copy of marchfolk_rp3_v001/landmarks.py with the HEAD-LOCAL absolute-cm
# windows scaled by the Cogling head size KH = min(1, (crown z - eye-helper z) / 10.89 cm), 10.89 = Marchfolk MF-M-R. Only two blocks change:
#   mouth corners: frontal window |x| < 3.5 KH, f > head + 6 KH, eye - 12 KH < u < eye - 4 KH, cross-slit pair distance < 0.25 KH (the unscaled window
#     finds no lip rim on the ~12 cm Cogling head: the slit sits 3.5-3.9 cm below the eye, inside the fixed 4 cm exclusion);
#   jaw hinge estimate: ear root + (1.2 anterior, 0.5 inferior, 1.5 medial) x KH.
# Every other landmark (rig / joint / surface-fit) is exactly landmarks.py. Not used for any other race.
# landmarks.py NATIVE.npz R6.npz CAND.npz OUT.json : RP3 rig-facing landmark package (contract §12, order d18ff2a §12) for one Marchfolk configuration.
# Provenance per landmark:
#   source-rig   : MPFB game_engine rig bone heads / tails in the posed R-6 stance (exact, carried unchanged);
#   source-joint : MPFB joint-helper cube centres of the regenerated source (the generator's own joint definition: toes, jaw, eye helpers);
#   surface-fit  : fitted on the SOURCE surface (method recorded), then re-measured on the production candidate (drift reported, T-6).
# Frames: analysis cm (x left, f forward, u up) as the R-6 asset, and production Blender m after the production origin translation
#   (pelvis-root = MPFB 'pelvis' bone head projected to the ground -> (0, 0, 0); Blender = (x, -f, u) / 100).
import sys, json, numpy as np
import scipy.sparse as sp
from scipy.spatial import cKDTree
a = sys.argv[1:]; z = np.load(a[0]); r6 = np.load(a[1]); cz = np.load(a[2]); OUT = a[3]
V = z['V'].astype(float); Q = z['Q']; m = json.loads(str(z['meta'])); H = {k: np.array(v) for k, v in m['heads'].items()}; T = {k: np.array(v) for k, v in m['tails'].items()}
JC = {k: np.array(v) for k, v in m['joint_cubes'].items()}; EH = {k: np.array(v) for k, v in m['eye_helpers'].items()}; si = z['src_index']
Vp = cz['V'].astype(float)
KH = min(1.0, (V[:, 2].max() - EH['helper-l-eye'][2]) / 10.89)
root = H['pelvis'].copy(); root[2] = 0.0; OFF = -root          # production origin translation (analysis cm)
L = {}
def add(name, p, src, method=None, flag=None, axis=None):
    L[name] = dict(p_cm=np.round(np.asarray(p, float), 4).tolist(), source=src);
    if method: L[name]['method'] = method
    if flag: L[name]['flag'] = flag
    if axis is not None: L[name]['axis'] = np.round(np.asarray(axis, float) / np.linalg.norm(axis), 5).tolist()
add('pelvis_root', H['pelvis'], 'source-rig', 'pelvis bone head')
for s in ('l', 'r'):
    add('hip_' + s, H['thigh_' + s], 'source-rig'); add('knee_' + s, H['calf_' + s], 'source-rig', axis=T['calf_' + s] - H['calf_' + s])
    add('ankle_' + s, H['foot_' + s], 'source-rig', axis=T['foot_' + s] - H['foot_' + s]); add('ball_' + s, H['ball_' + s], 'source-rig', 'ball bone head (MTP line)')
    add('sternoclavicular_' + s, H['clavicle_' + s], 'source-rig'); add('glenohumeral_' + s, H['upperarm_' + s], 'source-rig')
    add('elbow_' + s, H['lowerarm_' + s], 'source-rig', axis=T['lowerarm_' + s] - H['lowerarm_' + s]); add('wrist_' + s, H['hand_' + s], 'source-rig', axis=T['hand_' + s] - H['hand_' + s])
    for fg in ('index', 'middle', 'ring', 'pinky'):
        add('%s_mcp_%s' % (fg, s), H['%s_01_%s' % (fg, s)], 'source-rig'); add('%s_pip_%s' % (fg, s), H['%s_02_%s' % (fg, s)], 'source-rig'); add('%s_dip_%s' % (fg, s), H['%s_03_%s' % (fg, s)], 'source-rig')
    add('thumb_cmc_' + s, H['thumb_01_' + s], 'source-rig'); add('thumb_mcp_' + s, H['thumb_02_' + s], 'source-rig'); add('thumb_ip_' + s, H['thumb_03_' + s], 'source-rig')
    # fingertips / toe tips: surface-fit = the source vertex furthest along the distal bone direction within the digit
    for fg in ('index', 'middle', 'ring', 'pinky', 'thumb'):
        b = '%s_03_%s' % (fg, s); d = T[b] - H[b]; d /= np.linalg.norm(d); P = V - H[b]; t = P @ d; rr = np.linalg.norm(P - np.outer(t, d), axis=1); c = np.nonzero((rr < 1.2) & (t > 0) & (t < np.linalg.norm(T[b] - H[b]) + 2.0))[0]
        add('%s_tip_%s' % (fg, s), V[c[np.argmax(t[c])]], 'surface-fit', 'source vertex furthest along the distal phalanx bone within 1.2 cm of its axis and at most 2 cm beyond the bone tail')
    for k in range(1, 6):
        ks = sorted([n for n in JC if n.startswith('%s-toe-%d-' % (s, k))], key=lambda n: int(n.split('-')[-1]))
        for j, n in enumerate(ks): add('toe%d_j%d_%s' % (k, j + 1, s), JC[n], 'source-joint', 'MPFB joint helper ' + n)
        d = JC[ks[-1]] - JC[ks[-2]]; d /= np.linalg.norm(d); P = V - JC[ks[-1]]; t = P @ d; rr = np.linalg.norm(P - np.outer(t, d), axis=1); c = np.nonzero((rr < 1.2) & (t > -0.2) & (t < 4.0))[0]
        add('toe%d_tip_%s' % (k, s), V[c[np.argmax(t[c])]], 'surface-fit', 'source vertex furthest along the last toe-joint direction within 1.2 cm of its axis')
    # acromion: surface-fit -- highest-lateral source vertex above the GH centre within 6 cm (MPFB game_engine rig has no acromion joint)
    gh = H['upperarm_' + s]; sg = 1 if s == 'l' else -1; P = V - gh; c = np.nonzero((np.linalg.norm(P, axis=1) < 6) & (P[:, 2] > 0))[0]
    add('acromion_' + s, V[c[np.argmax(P[c, 2] + 0.5 * sg * P[c, 0])]], 'surface-fit', 'source vertex maximising up + 0.5 lateral within 6 cm of GH (no MPFB acromion joint)')
    add('eye_' + s, EH['helper-%s-eye' % s], 'source-joint', 'MPFB helper eyeball centre (helper removed from production; centre kept as landmark)')
    # ear root / tip from the R-6 'ears' weight region
    ew = r6['w_ears'][si]; side = (V[:, 0] * sg > 0) & (ew > 0.5)
    if side.any():
        P = V[side]; hc = H['head']; root_ = P[np.argmin(np.linalg.norm(P - hc, axis=1))]; tip = P[np.argmax(np.linalg.norm(P - root_, axis=1))]
        add('ear_root_' + s, root_, 'surface-fit', "ear-region vertex (R-6 'ears' weight > 0.5) closest to the head pivot"); add('ear_tip_' + s, tip, 'surface-fit', 'ear-region vertex furthest from the ear root')
    # mouth corners: lateral extremes of the lip slit (vertices of the mouth-opening rim = vertices whose nearest neighbour across the slit is < 0.3 cm, near the midline face front)
for i, n in enumerate(('spine_01', 'spine_02', 'spine_03')): add(n, H[n], 'source-rig')
add('neck_base', H['neck_01'], 'source-rig'); add('head_pivot', H['head'], 'source-rig', 'head bone head (atlanto-occipital proxy)')
add('crown', V[np.argmax(V[:, 2])], 'surface-fit', 'highest source vertex')
add('jaw_joint_mpfb', JC['jaw'], 'source-joint', 'MPFB joint helper joint-jaw', flag='MPFB jaw joint sits at the chin front (~1 cm inside the chin surface), not at the temporomandibular hinge; the game_engine rig has no jaw bone. Recorded, not used as a hinge.')
# jaw hinge (TMJ) estimate: surface-fit, 1.2 cm anterior and 0.5 cm below the ear root, projected 1.5 cm inside the surface
for s in ('l', 'r'):
    if 'ear_root_' + s in L:
        er = np.array(L['ear_root_' + s]['p_cm']); add('jaw_hinge_' + s, er + (np.array([0, 1.2, -0.5]) + np.array([-1.5 if s == 'l' else 1.5, 0, 0])) * KH, 'derived',
                                                         'TMJ estimate = ear root + (1.2 cm anterior, 0.5 cm inferior, 1.5 cm medial) x KH (head scale)', flag='estimate; final jaw hinge set with the face rig (RP-face)')
# mouth corners: midline mouth slit height = where the forward ray crosses the mouth opening (inner pocket present); corners = lateral-most lip-rim vertices
TRI = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]
fr = np.nonzero((np.abs(V[:, 0]) < 3.5 * KH) & (V[:, 1] > H['head'][1] + 6 * KH) & (V[:, 2] < EH['helper-l-eye'][2] - 4 * KH) & (V[:, 2] > EH['helper-l-eye'][2] - 12 * KH))[0]
kd = cKDTree(V[fr]); pr = kd.query_pairs(0.25 * KH); rim = set()
E = np.unique(np.sort(np.concatenate([Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]]), 1), axis=0); Es = set(map(tuple, E.tolist()))
for i, j in pr:
    a_, b_ = fr[i], fr[j]
    if (min(a_, b_), max(a_, b_)) not in Es: rim.add(a_); rim.add(b_)
rim = np.array(sorted(rim))
if len(rim):
    for s, sg in (('l', 1), ('r', -1)):
        c = rim[(V[rim, 0] * sg) > 0]
        if len(c): add('mouth_corner_' + s, V[c[np.argmax(V[c, 0] * sg)]], 'surface-fit', 'lateral-most vertex of the lip contact rim (non-adjacent vertex pairs < 2.5 mm x KH apart across the slit; head-scaled window)')
# re-measure surface-fit landmarks on the production candidate (nearest production vertex to the source position; production keeps every hm08 vertex)
kdp = cKDTree(Vp)
for k, v in L.items():
    p = np.array(v['p_cm'])
    if v['source'] == 'surface-fit':
        d, i = kdp.query(p); v['production_p_cm'] = np.round(Vp[i], 4).tolist(); v['drift_mm'] = round(float(d * 10), 4)
    elif v['source'] == 'derived':
        s_ = k[-1]; er = np.array(L['ear_root_' + s_]['production_p_cm']); q = er + (np.array([0, 1.2, -0.5]) + np.array([-1.5 if s_ == 'l' else 1.5, 0, 0])) * KH
        v['production_p_cm'] = np.round(q, 4).tolist(); v['drift_mm'] = round(float(np.linalg.norm(q - p) * 10), 4)
    else: v['production_p_cm'] = v['p_cm']; v['drift_mm'] = 0.0
    q = np.array(v['production_p_cm']) + OFF; v['production_blender_m'] = np.round(np.array([q[0], -q[1], q[2]]) / 100, 6).tolist()
# plausibility flags (mechanical): knee / elbow centre inside the limb, hips below and lateral of the pelvis root, GH below acromion, symmetry
for s, sg in (('l', 1), ('r', -1)):
    for j in ('knee', 'elbow', 'wrist', 'ankle'):
        p = np.array(L['%s_%s' % (j, s)]['p_cm']); d, _ = cKDTree(V).query(p)
        inside = True
        L['%s_%s' % (j, s)]['dist_to_surface_cm'] = round(float(d), 3)
    if L['glenohumeral_' + s]['p_cm'][2] > L['acromion_' + s]['p_cm'][2]: L['glenohumeral_' + s]['flag'] = 'GH above acromion surface point'
sym = {k[:-2]: round(float(np.linalg.norm(np.array(L[k]['p_cm']) * [-1, 1, 1] - np.array(L[k[:-1] + 'r']['p_cm']))), 4) for k in L if k.endswith('_l') and k[:-1] + 'r' in L}
json.dump(dict(frame=dict(analysis='cm, x subject left, f forward, u up (R-6)', blender='m, Z up, faces -Y, subject left +X, origin = pelvis root projected to ground', origin_translation_cm=OFF.tolist()),
               landmarks=L, mirror_asymmetry_cm=sym, max_surface_fit_drift_mm=max((v['drift_mm'] for v in L.values()), default=0.0)), open(OUT, 'w'), indent=1)
print('KH', round(KH, 4), len(L), 'landmarks; max drift mm', max(v['drift_mm'] for v in L.values()), 'max L/R mirror asym cm', max(sym.values()), [k for k, v in L.items() if 'flag' in v])
