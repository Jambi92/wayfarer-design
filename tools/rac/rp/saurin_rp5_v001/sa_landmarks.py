# sa_landmarks.py BASE.npz OUT_DIR : RP5 Saurin source-first landmark package + region labels (order 53976fb §15) on the canonical W2I6 SA-M188 base
# (unsurfaced; the surfaced organism differs by the <= 0.17 cm normal-only scale delta). Analysis frame cm: x right, f forward, u up.
# Every landmark records its method:
#   section  : centroid of an exact plane section of the body (vertices within 0.35 cm of the plane, nearest connected cluster) -- limb joints are
#              re-fitted from the accepted Saurin construction skeleton seeds (tools/rodin/gate1/g7geo.py ARM / LEG) by iterating plane-normal =
#              local limb axis; the seed itself is never used as the landmark;
#   extremal : surface vertex extremal along a stated direction inside a stated region (crown, rostrum tip, claw / digit tips, toe tips);
#   canon    : accepted Saurin head-frame definition carried to world (w3b_head.py EYE / hinge in the TS6 skull frame, head_world = (L - PIV) * 1.08 + PIV + AT);
#   derived  : stated construction from other landmarks (pelvis root = hip mid-point; MCP / MTP lines along the fitted digit chains).
# Regions (vertex labels): tail, head, neck, torso, arm_l/r, hand_l/r, leg_l/r, foot_l/r -- nearest fitted segment of the landmark skeleton
# (graph distance proxy: Euclidean distance to segments), used for identity-zone statistics (T-2) and density audits.
import sys, os, json, numpy as np
from scipy.spatial import cKDTree
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
BP, OUT = sys.argv[1:3]; os.makedirs(OUT, exist_ok=True)
z = np.load(BP); V = z['v'].astype(float); F = z['f'].astype(np.int64); n = len(V); KD = cKDTree(V)
A = sp.coo_matrix((np.ones(3 * len(F)), (np.r_[F[:, 0], F[:, 1], F[:, 2]], np.r_[F[:, 1], F[:, 2], F[:, 0]])), shape=(n, n)).tocsr(); A = A + A.T
L = {}
def add(k, p, method, note=None, axis=None):
    L[k] = dict(p_cm=np.round(np.asarray(p, float), 4).tolist(), method=method)
    if note: L[k]['note'] = note
    if axis is not None: a = np.asarray(axis, float); L[k]['axis'] = np.round(a / np.linalg.norm(a), 5).tolist()
def section(c, d, rad=14.0, tol=0.35):
    """centroid of the plane section through c (normal d) restricted to the connected surface cluster nearest c within rad"""
    d = d / np.linalg.norm(d); idx = np.array(KD.query_ball_point(c, rad)); s = (V[idx] - c) @ d; m = idx[np.abs(s) < tol]
    if len(m) < 6: return None, None
    sub = A[m][:, m]; nc, lab = connected_components(sub, directed=False)
    # clusters can be fragmented by the thin band: merge by proximity of their centroids to c, keep the cluster(s) whose centroid is nearest
    cen = np.array([V[m[lab == k]].mean(0) for k in range(nc)]); sz = np.bincount(lab)
    dist = np.linalg.norm(cen - c, axis=1); best = np.argmin(dist + 50 * (sz < 8))
    ring = m[lab == best]
    # band fragments of the same ring: include clusters within 1.5 x the ring radius of its centroid
    r0 = np.linalg.norm(V[ring] - cen[best], axis=1).mean()
    keep = [k for k in range(nc) if np.linalg.norm(cen[k] - cen[best]) < 1.6 * r0 + 0.5 and sz[k] >= 3]
    ring = m[np.isin(lab, keep)]; P = V[ring]; P = P - np.outer((P - c) @ d, d)
    return P.mean(0), np.linalg.norm(P - P.mean(0), axis=1).mean()
def refit_chain(pts, iters=4):
    """re-fit a joint chain (list of seed points): each joint = section centroid with normal = bisector of the adjacent segment directions"""
    P = [np.asarray(p, float) for p in pts]; R = [None] * len(P)
    for _ in range(iters):
        for i in range(len(P)):
            d = (P[min(i + 1, len(P) - 1)] - P[max(i - 1, 0)]); c, r = section(P[i], d)
            if c is not None: P[i] = c; R[i] = r
    return P, R
# ---------------- limbs from the construction-skeleton seeds (re-fitted)
ARM = {-1: dict(S=(-23.5, -6.0, 147.0), E=(-30.5, -4.5, 117.0), W=(-36.8, 6.0, 97.0)), 1: dict(S=(23.0, -5.0, 147.0), E=(28.8, -3.5, 117.0), W=(35.2, 7.0, 97.0))}
LEG = {-1: dict(H=(-13.0, 3.5, 86.0), K=(-17.4, 2.8, 62.0), A=(-26.4, 0.2, 9.6)), 1: dict(H=(13.0, 3.5, 86.0), K=(15.2, 3.0, 62.0), A=(21.6, 1.6, 9.6))}
SIDE = {-1: 'r', 1: 'l'}    # analysis x right -> subject left is -x?  (resolved below from the production contract: subject left = +X after the frame map)
for sg in (-1, 1):
    s = 'xneg' if sg < 0 else 'xpos'
    # elbow seed lies outside the W2 surface: pull it to the mid-point of its neighbours' section line before refitting
    S0, E0, W0 = [np.asarray(ARM[sg][k], float) for k in 'SEW']; E0 = 0.5 * (S0 + W0) + 0.35 * (E0 - 0.5 * (S0 + W0))
    (S, E, W), Rr = refit_chain([S0, E0, W0])
    add('glenohumeral_' + s, S, 'section', 'shoulder section centroid, normal = upper-arm axis (seed g7geo ARM.S)', axis=E - S)
    add('elbow_' + s, E, 'section', 'elbow section centroid, normal = bisector upper arm / forearm', axis=W - E)
    add('wrist_' + s, W, 'section', 'wrist section centroid', axis=W - E)
    H0, K0, A0 = [np.asarray(LEG[sg][k], float) for k in 'HKA']
    (H, K, Aa), _ = refit_chain([H0, K0, A0])
    add('hip_' + s, H0, 'canon', 'accepted construction hip centre (g7geo LEG.H; inside the closed W2 surface, 5.9 cm deep); a hip-joint section is ill-posed at the groin')
    add('knee_' + s, K, 'section', 'knee section centroid, normal = bisector thigh / shank', axis=Aa - K)
    add('ankle_' + s, Aa, 'section', 'ankle section centroid (normal = shank axis)', axis=Aa - K)
add('pelvis_root', 0.5 * (np.array(L['hip_xneg']['p_cm']) + np.array(L['hip_xpos']['p_cm'])), 'derived', 'mid-point of the hip centres')
# ---------------- region labels (nearest skeleton segment), tail first
# tail root (anatomical): the root plane passes through the midsagittal DORSAL lumbar-concavity point (the most anterior point of the posterior
# outline between u 110 and 145 -- where the back outline turns into the tail's dorsal line) and the midsagittal VENTRAL perineal junction (the
# point of the midline ventral outline at the f of the posterior thigh / buttock surface, u 80-86, where the tail underside leaves the thighs); normal in the
# sagittal plane, perpendicular to that line, pointing caudally; root section = plane points between the two root points (|x| < 25 cm).
# Tail centreline: root centre -> f-plane section centroids of the free tail (f <= -24 cm) -> tip; 16 equal-arc chain points.
mid = np.abs(V[:, 0]) < 0.4; Pm = V[mid]
bandD = Pm[(Pm[:, 2] > 110) & (Pm[:, 2] < 145)]; uD = np.arange(110, 145, 0.5); fD = np.array([bandD[np.abs(bandD[:, 2] - u) < 0.3][:, 1].min() for u in uD])
Dp = np.array([0.0, fD.max(), uD[np.argmax(fD)]])
thigh = V[(V[:, 2] > 80) & (V[:, 2] < 86) & (np.abs(V[:, 0]) > 7) & (np.abs(V[:, 0]) < 22) & (V[:, 1] > -30)]; fT = thigh[:, 1].min()     # posterior thigh / buttock surface below the tail
bandV = Pm[(np.abs(Pm[:, 1] - fT) < 0.3) & (Pm[:, 2] > 80) & (Pm[:, 2] < 120)]
Vp = np.array([0.0, fT, bandV[:, 2].min()])
t_ = Dp - Vp; t_ /= np.linalg.norm(t_); nrm = np.cross(np.array([1.0, 0, 0]), t_)
if nrm[1] > 0: nrm = -nrm
Lr = np.linalg.norm(Dp - Vp); q = V - Vp; tt = q @ t_; rp = (np.abs(q @ nrm) < 0.3) & (tt > -0.5) & (tt < Lr + 0.5) & (np.abs(V[:, 0]) < 25)
ring = V[rp]; c0 = ring.mean(0); e1 = np.array([1.0, 0, 0]); e2 = t_; loc = ring - c0; xy = np.c_[loc @ e1, loc @ e2]
o = np.argsort(np.arctan2(xy[:, 1], xy[:, 0])); xy = xy[o]
root_area = 0.5 * abs(np.dot(xy[:, 0], np.roll(xy[:, 1], -1)) - np.dot(xy[:, 1], np.roll(xy[:, 0], -1)))
# centreline: root centre, then f-plane section centroids of the free tail (f <= -24 cm: tail only), then the tip
tip = V[np.argmin(V[:, 1])]; tp = []
for f0 in np.arange(-24.0, tip[1] + 0.4, -1.0):
    m = (np.abs(V[:, 1] - f0) < 0.25) & (V[:, 2] > 40)
    if m.sum() < 5: break
    tp.append(V[m].mean(0))
chain = np.vstack([c0[None], np.array(tp), tip[None]])
seg = np.linalg.norm(np.diff(chain, axis=0), axis=1); s_arc = np.r_[0, np.cumsum(seg)]; Ltail = s_arc[-1]
root = c0; tipv = tip
add('tail_root_dorsal', Dp, 'section', 'midsagittal posterior outline: most anterior point between u 110-145 (lumbar concavity, back -> tail dorsal line)')
add('tail_root_ventral', Vp, 'section', 'midline ventral outline at the posterior thigh surface f (perineal junction: the tail underside leaves the thighs)')
add('tail_root_centre', root, 'section', 'centroid of the root-plane section (plane through tail_root_dorsal / tail_root_ventral, sagittal normal); root section area %.2f cm2' % root_area, axis=nrm)
for k in range(16):
    t = (k + 1) / 17.0 * Ltail; p = np.array([np.interp(t, s_arc, chain[:, j]) for j in range(3)]); add('tail_chain_%02d' % (k + 1), p, 'section', '%d/17 equal-arc point of the tail section-centroid centreline' % (k + 1))
add('tail_tip', tipv, 'extremal', 'most posterior surface vertex')
# spine / axial: horizontal section centroids of the trunk between the hips and the neck (arms excluded by nearest-cluster rule)
hipu = L['pelvis_root']['p_cm'][2]
for nm, u in (('spine_lower_axial_91', 91.0), ('spine_lower_axial_107', 107.0), ('spine_lower_axial_123', 123.0), ('spine_mid_138', 138.0), ('spine_upper_150', 150.0)):
    c, r = section(np.array([0.0, 0.0, u]), np.array([0, 0, 1.0]), rad=26); add(nm, c, 'section', 'horizontal trunk section centroid at u = %.0f cm (lower axial trunk stations as W2I I91 / I123)' % u)
nb = None
for u in np.arange(150, 172, 0.5):
    c, r = section(np.array([0.0, 0.0, u]), np.array([0, 0, 1.0]), rad=20)
    if c is None: continue
    if nb is None or r < nb[1]: nb = (u, r, c)
add('neck_min_section', nb[2], 'section', 'minimum-radius horizontal neck section between u 150 and 172 cm')
add('neck_base', section(np.array([0.0, 0.0, 156.0]), np.array([0, 0, 1.0]), rad=20)[0], 'section', 'horizontal section centroid at the shoulder line (u 156)')
AT = np.array([0.0, 3.0, 179.3]); PIV = np.array([0.0, -3.0, 8.6]); HS = 1.08
hw = lambda p: (np.asarray(p, float) - PIV) * HS + PIV + AT
add('head_pivot', hw((0.0, -2.0, 2.0)), 'canon', 'TS6 skull frame occipital pivot (head-local (0, -2, 2))')
add('crown', V[np.argmax(V[:, 2])], 'extremal', 'highest surface vertex')
H_ = V[:, 2] > 170; add('rostrum_tip', V[H_][np.argmax(V[H_][:, 1])], 'extremal', 'most anterior head vertex (u > 170)')
for sg, s in ((1, 'xpos'), (-1, 'xneg')):
    add('eye_' + s, hw((sg * 3.3, 6.55, 4.5)), 'canon', 'w3b_head.py EYE centre (canonical orbit), head frame -> world')
    add('jaw_hinge_' + s, hw((sg * 4.8, -0.9, 0.3)), 'canon', 'w3b_head.py quadrate hinge centre, head frame -> world')
# mouth corners: oral-line slit = non-adjacent vertex pairs < 0.12 cm apart in the face below the eyes; corners = posterior-most slit vertices per side
fr = np.nonzero((V[:, 2] > 172) & (V[:, 2] < L['eye_xpos']['p_cm'][2]) & (V[:, 1] > 0))[0]; kd = cKDTree(V[fr]); pr = kd.query_pairs(0.12)
Es = set(map(tuple, np.sort(np.r_[F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]], 1).tolist())); rim = set()
for i, j in pr:
    a, b = fr[i], fr[j]
    if (min(a, b), max(a, b)) not in Es: rim.add(a); rim.add(b)
rim = np.array(sorted(rim))
for sg, s in ((1, 'xpos'), (-1, 'xneg')):
    c = rim[V[rim, 0] * sg > 1.0] if len(rim) else []
    if len(c): add('mouth_corner_' + s, V[c[np.argmin(V[c, 1])]], 'extremal', 'posterior-most vertex of the oral-line slit (non-adjacent pairs < 1.2 mm)')
# ---------------- hands / feet: digit tips = farthest surface clusters from the wrist / ankle
def tips(region, origin, axis, k, mind=1.0):
    P = V[region]; t = (P - origin) @ axis; o = np.argsort(-t); out = []
    for i in o:
        if all(np.linalg.norm(P[i] - q) > mind for q in out): out.append(P[i])
        if len(out) == k: break
    return out
lab = np.full(n, 'torso', object)
segs = []
for sg in (-1, 1):
    s = 'xneg' if sg < 0 else 'xpos'; g = lambda k: np.array(L[k + '_' + s]['p_cm'])
    segs += [('arm_' + s, g('glenohumeral'), g('elbow')), ('arm_' + s, g('elbow'), g('wrist')), ('leg_' + s, g('hip'), g('knee')), ('leg_' + s, g('knee'), g('ankle'))]
    hd = g('wrist') - g('elbow'); hd = 0.55 * hd / np.linalg.norm(hd) + 0.45 * np.array([0, 0, -1.0]); hd /= np.linalg.norm(hd)
    segs += [('hand_' + s, g('wrist'), g('wrist') + 16 * hd)]
    segs += [('foot_' + s, g('ankle'), g('ankle') + np.array([0, 18.0, -8.0]))]
spine = [np.array(L[k]['p_cm']) for k in ('pelvis_root', 'spine_lower_axial_107', 'spine_lower_axial_123', 'spine_mid_138', 'spine_upper_150', 'neck_base')]
segs += [('torso', a, b) for a, b in zip(spine[:-1], spine[1:])]
segs += [('neck', np.array(L['neck_base']['p_cm']), np.array(L['head_pivot']['p_cm'])), ('head', np.array(L['head_pivot']['p_cm']), np.array(L['rostrum_tip']['p_cm']))]
segs += [('tail', a, b) for a, b in zip(chain[:-1], chain[1:])]
D = np.full(n, 1e9)
for nm, a, b in segs:
    v = b - a; t = np.clip(((V - a) @ v) / (v @ v), 0, 1); d = np.linalg.norm(V - (a + np.outer(t, v)), axis=1)
    m = d < D; D[m] = d[m]; lab[m] = nm
lab[(V[:, 2] > np.array(L['neck_min_section']['p_cm'])[2] + 2) & (lab == 'neck')] = 'head'
for sg in (-1, 1):
    s = 'xneg' if sg < 0 else 'xpos'; g = lambda k: np.array(L[k + '_' + s]['p_cm'])
    # hand / foot split at the wrist / ankle plane
    for limb, part, j0, j1 in (('arm', 'hand', 'elbow', 'wrist'), ('leg', 'foot', 'knee', 'ankle')):
        ax_ = g(j1) - g(j0); m = np.isin(lab, [limb + '_' + s, part + '_' + s]); dist = (V - g(j1)) @ (ax_ / np.linalg.norm(ax_))
        lab[m & (dist > 0)] = part + '_' + s; lab[m & (dist <= 0)] = limb + '_' + s
    hand = lab == 'hand_' + s; hd = g('wrist') - g('elbow'); hd = 0.55 * hd / np.linalg.norm(hd) + 0.45 * np.array([0, 0, -1.0]); hd /= np.linalg.norm(hd)
    for k, p in enumerate(tips(np.nonzero(hand)[0], g('wrist'), hd, 5, 1.2)): add('hand_tip%d_%s' % (k + 1, s), p, 'extremal', 'k-th farthest (>= 1.2 cm apart) hand vertex along the wrist->hand axis (claw tips; ordering by reach, digit identity in the cage pass)')
    foot = lab == 'foot_' + s
    for k, p in enumerate(tips(np.nonzero(foot)[0], g('ankle'), np.array([0, 1.0, -0.15]), 5, 1.2)): add('toe_tip%d_%s' % (k + 1, s), p, 'extremal', 'k-th most anterior (>= 1.2 cm apart) foot vertex (toe-claw tips)')
    FP = V[foot]; add('ball_line_' + s, FP[np.argmin(np.abs(FP[:, 1] - (g('ankle')[1] + 13.0)) + 5 * FP[:, 2])], 'derived', 'plantar vertex 13 cm anterior of the ankle (metatarsal-head band, foot.py MET heads 12-14 cm)')
np.savez_compressed(OUT + '/SA-M188_regions.npz', label=lab.astype('<U12'), tail_chain=chain, tail_arc=s_arc)
json.dump(dict(tail_root_section_area_cm2=round(float(root_area), 2), frame='analysis cm: x right (subject left = -x? see contract map), f forward, u up; canonical W2I6 SA-M188 base', tail_length_centreline_cm=round(float(Ltail), 2),
               region_counts={k: int(v) for k, v in zip(*np.unique(lab, return_counts=True))}, landmarks=L), open(OUT + '/SA-M188_landmarks.json', 'w'), indent=1)
print('landmarks', len(L), 'tail L', round(Ltail, 1), {k: int(v) for k, v in zip(*np.unique(lab, return_counts=True))})
for k in ('glenohumeral_xneg', 'elbow_xneg', 'wrist_xneg', 'knee_xneg', 'ankle_xneg', 'tail_root_centre', 'neck_min_section', 'mouth_corner_xpos', 'rostrum_tip', 'crown'):
    print(k, L.get(k, {}).get('p_cm'))
