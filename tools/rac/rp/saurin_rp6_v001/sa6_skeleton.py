# sa6_skeleton.py OUTDIR : Saurin RP6 production-rig pilot skeleton (order a407015 §3, §5, §6, §13, §17).
#   SAURIN-SPECIFIC pilot hierarchy (not a universal game skeleton). One hierarchy / naming for c1 (SA-M188) and c2 (SA-F188); joint coordinates per configuration.
#   Joint sources (c1): the frozen RP5 landmark package + section / loop centroids of the frozen semantic rings (finger / thumb / toe r1-r2, base rings, wrist,
#   knuckle, tail module rings). c2: the SAME definitions re-evaluated on the c2 realisation (loop / ring centroids directly; landmark-defined joints transferred
#   through local affine coordinates over their 48 nearest c1 cage vertices -> identical vertices on c2 = shared topology).
#   Writes SA_RP6_skeleton_v001.json (hierarchy, roles, deform flags, method, pose axes) + SA_RP6_joint_placement_{M,F}_v001.json (the tail-count study is sa6_tail_study.py).
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa6_common as C
d = C.load(); LM = d['LM']; V1, V2 = d['V1'], d['V2']; loops = d['loops']; NM = d['names']
from scipy.spatial import cKDTree
kd1 = cKDTree(V1)
def transfer(p, V):
    """c1 point -> configuration V via least-norm affine coordinates over the 48 nearest c1 cage vertices (sum w = 1)"""
    p = np.asarray(p, float); _, ix = kd1.query(p, 48); A = np.vstack([V1[ix].T, np.ones(len(ix))]); w = np.linalg.lstsq(A, np.r_[p, 1.0], rcond=None)[0]
    return w @ V[ix]
def lcen(name, V): return V[loops[name]].mean(0)
CLAW = "claw tip = the vertex of the digit's OWN authored digit + claw-cap component farthest along the base-ring -> r2-ring direction (topology-identified; the RP5 tip landmarks are not digit-matched)"
def clawtip(V, s_, pre, k):
    comp = C.digit_components()[(s_, pre, k)]; base = V[loops['%s_th_r1' % s_ if pre == 'th' else '%s_%s%d_base' % (s_, pre, k)]].mean(0)
    r2 = V[loops['%s_th_r2' % s_ if pre == 'th' else '%s_%s%d_r2' % (s_, pre, k)]].mean(0); u = (r2 - base) / np.linalg.norm(r2 - base)
    return V[comp[np.argmax((V[comp] - base) @ u)]]
TAILN = 16
def build(V, cfg):
    J = {}; M = {}
    def lm(k): return LM[k] if cfg == 'c1' else transfer(LM[k], V)
    def put(n, p, method): J[n] = np.asarray(p, float); M[n] = method
    # axial
    put('pelvis_h', lm('pelvis_root'), 'landmark pelvis_root (derived, hip-joint level)')
    for k, nm_ in (('spine_lower_axial_107', 'spine_01_h'), ('spine_lower_axial_123', 'spine_02_h'), ('spine_mid_138', 'spine_03_h'), ('spine_upper_150', 'spine_04_h')):
        put(nm_, lm(k), 'landmark %s (section centroid)' % k)
    # neck_01 joint = centroid of the authored neck / trunk seam ring (frozen quad labels; topology-defined, identical vertex set on c2).  The RP5 'neck_base'
    # landmark lies at the FRONT of the neck base (throat surface, ~3.7 cm inside the anterior wall): flexion about it stretched the whole nape (+3.6 L LBS).
    nk = np.zeros(len(V), bool); nk[d['Q'][d['qlab'] == 'neck'].ravel()] = True; tk = np.zeros(len(V), bool); tk[d['Q'][np.isin(d['qlab'], ('trunk', 'shoulder'))].ravel()] = True
    put('neck_01_h', V[nk & tk].mean(0), 'centroid of the neck / trunk seam ring (frozen quad labels) -- RP6 v002 fix: RP5 neck_base landmark is anterior'); put('neck_02_h', lm('neck_min_section'), 'landmark neck_min_section (section centroid)')
    put('head_h', lm('head_pivot'), 'landmark head_pivot (canon)'); put('head_t', lm('crown'), 'landmark crown (extremal)')
    put('jaw_h', 0.5 * (lm('jaw_hinge_xpos') + lm('jaw_hinge_xneg')), 'mid-point of the canonical jaw hinges'); put('jaw_t', lm('rostrum_tip') - np.array([0, 0, 1.5]), 'rostrum tip - 1.5 cm (lower jaw line)')
    # tail: 16 deform segments, graded spacing (equal increments of integral ds / sqrt(r)) on the tail-module ring centroid line; root = tail-root ring centroid
    R = d['tail_rings']; cen = np.array([V[r].mean(0) for r in R]); rad = np.array([np.linalg.norm(V[r] - V[r].mean(0), axis=1).mean() for r in R])
    s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(cen, axis=0), axis=1))]; g = np.r_[0, np.cumsum(np.diff(s) / np.sqrt(0.5 * (rad[1:] + rad[:-1])))]
    kn = np.interp(np.linspace(0, g[-1], TAILN + 1), g, s); P = np.array([np.interp(kn, s, cen[:, k]) for k in range(3)]).T
    for i in range(TAILN + 1): put('tail_%02d_h' % (i + 1) if i < TAILN else 'tail_%02d_t' % TAILN, P[i], 'tail-module ring centroid line, graded knot %d / %d' % (i, TAILN))
    # glenohumeral joint (RP6 v002): the RP5 landmarks sit at different depths inside their shoulders (left 0.5 cm, right 2.1 cm posterior of the
    # shoulder-ring centroid) -> one bilateral rule: shoulder_ring0 centroid + the MEAN landmark offset of both sides (lateral component mirrored).
    ring = lambda s_: V[loops['shoulder_ring0_' + s_]].mean(0); mirr = lambda s_: np.array([1.0 if s_ == 'xpos' else -1.0, 1, 1])
    gh_off = 0.5 * ((lm('glenohumeral_xpos') - ring('xpos')) * mirr('xpos') + (lm('glenohumeral_xneg') - ring('xneg')) * mirr('xneg'))
    gh = lambda s_: ring(s_) + gh_off * mirr(s_)
    GHM = 'shoulder_ring0 centroid + bilateral mean glenohumeral-landmark offset (lateral mirrored)'
    for s_ in ('xpos', 'xneg'):
        t = C.side_tag(s_)
        put('clavicle_%s_h' % t, lm('neck_base') + 0.22 * (gh(s_) - lm('neck_base')) - np.array([0, 4.0, 0]) * 0, 'neck_base + 22 %% toward glenohumeral (sterno-clavicular region)')
        put('upperarm_%s_h' % t, gh(s_), GHM); put('forearm_%s_h' % t, lm('elbow_' + s_), 'landmark elbow (section)')
        put('hand_%s_h' % t, lm('wrist_' + s_), 'landmark wrist (section)')
        for k in range(1, 5):
            put('meta_%d_%s_h' % (k, t), lm('wrist_' + s_) + 0.15 * (lcen('%s_f%d_base' % (s_, k), V) - lm('wrist_' + s_)), 'wrist + 15 % toward the finger base ring (carpal)')
            put('finger_%d_01_%s_h' % (k, t), lcen('%s_f%d_base' % (s_, k), V), 'finger MCP base ring centroid (semantic loop %s_f%d_base)' % (s_, k))
            put('finger_%d_02_%s_h' % (k, t), lcen('%s_f%d_r1' % (s_, k), V), 'finger ring r1 centroid (PIP)'); put('finger_%d_03_%s_h' % (k, t), lcen('%s_f%d_r2' % (s_, k), V), 'finger ring r2 centroid (DIP / claw base)')
            put('finger_%d_03_%s_t' % (k, t), clawtip(V, s_, 'f', k), CLAW)
        r1 = lcen('%s_th_r1' % s_, V); r2 = lcen('%s_th_r2' % s_, V); tp = clawtip(V, s_, 'th', 0)
        put('thumb_01_%s_h' % t, r1 - 1.0 * (r2 - r1), 'thumb ring r1 - (r2 - r1) (CMC region)'); put('thumb_02_%s_h' % t, r1, 'thumb ring r1 centroid (MCP)'); put('thumb_03_%s_h' % t, r2, 'thumb ring r2 centroid (IP / claw base)')
        put('thumb_03_%s_t' % t, tp, CLAW)
        put('thigh_%s_h' % t, lm('hip_' + s_), 'landmark hip (canon)'); put('shin_%s_h' % t, lm('knee_' + s_), 'landmark knee (section)'); put('foot_%s_h' % t, lm('ankle_' + s_), 'landmark ankle (section)')
        put('ball_%s_h' % t, lm('ball_line_' + s_) + np.array([0, 0, 1.2]), 'ball_line landmark + 1.2 cm (MTP joint height above the ground contact)')
        for k in range(1, 6):
            put('toe_%d_01_%s_h' % (k, t), lcen('%s_t%d_base' % (s_, k), V), 'toe MTP base ring centroid'); put('toe_%d_02_%s_h' % (k, t), lcen('%s_t%d_r1' % (s_, k), V), 'toe ring r1 centroid')
            put('toe_%d_03_%s_h' % (k, t), lcen('%s_t%d_r2' % (s_, k), V), 'toe ring r2 centroid (claw base)'); put('toe_%d_03_%s_t' % (k, t), clawtip(V, s_, 't', k), CLAW)
    return J, M
def bones(J):
    """hierarchy: name -> (parent, head key, tail key, deform, role)"""
    B = {'root': (None, None, None, False, 'control: world / root motion (non-deform, at the ground below the pelvis)'),
         'pelvis': ('root', 'pelvis_h', 'spine_01_h', True, 'axial'), 'spine_01': ('pelvis', 'spine_01_h', 'spine_02_h', True, 'axial lumbar'),
         'spine_02': ('spine_01', 'spine_02_h', 'spine_03_h', True, 'axial abdominal'), 'spine_03': ('spine_02', 'spine_03_h', 'spine_04_h', True, 'axial thoracic'),
         'spine_04': ('spine_03', 'spine_04_h', 'neck_01_h', True, 'axial upper thoracic'), 'neck_01': ('spine_04', 'neck_01_h', 'neck_02_h', True, 'neck'),
         'neck_02': ('neck_01', 'neck_02_h', 'head_h', True, 'neck'), 'head': ('neck_02', 'head_h', 'head_t', True, 'head (cranium + rostrum + display: one rigid deform unit)'),
         'jaw': ('head', 'jaw_h', 'jaw_t', True, 'jaw (mandible)')}
    for i in range(1, 17): B['tail_%02d' % i] = ('pelvis' if i == 1 else 'tail_%02d' % (i - 1), 'tail_%02d_h' % i, 'tail_%02d_h' % (i + 1) if i < 16 else 'tail_16_t', True, 'tail')
    for t in ('l', 'r'):
        B['clavicle_' + t] = ('spine_04', 'clavicle_%s_h' % t, 'upperarm_%s_h' % t, True, 'shoulder girdle'); B['upperarm_' + t] = ('clavicle_' + t, 'upperarm_%s_h' % t, 'forearm_%s_h' % t, True, 'arm')
        B['forearm_' + t] = ('upperarm_' + t, 'forearm_%s_h' % t, 'hand_%s_h' % t, True, 'arm'); B['hand_' + t] = ('forearm_' + t, 'hand_%s_h' % t, 'meta_2_%s_h' % t, True, 'hand (carpus)')
        for k in range(1, 5):
            B['meta_%d_%s' % (k, t)] = ('hand_' + t, 'meta_%d_%s_h' % (k, t), 'finger_%d_01_%s_h' % (k, t), True, 'metacarpal (palm cupping)')
            B['finger_%d_01_%s' % (k, t)] = ('meta_%d_%s' % (k, t), 'finger_%d_01_%s_h' % (k, t), 'finger_%d_02_%s_h' % (k, t), True, 'finger proximal phalanx')
            B['finger_%d_02_%s' % (k, t)] = ('finger_%d_01_%s' % (k, t), 'finger_%d_02_%s_h' % (k, t), 'finger_%d_03_%s_h' % (k, t), True, 'finger middle phalanx')
            B['finger_%d_03_%s' % (k, t)] = ('finger_%d_02_%s' % (k, t), 'finger_%d_03_%s_h' % (k, t), 'finger_%d_03_%s_t' % (k, t), True, 'finger distal phalanx + claw')
        B['thumb_01_' + t] = ('hand_' + t, 'thumb_01_%s_h' % t, 'thumb_02_%s_h' % t, True, 'thumb metacarpal (CMC)'); B['thumb_02_' + t] = ('thumb_01_' + t, 'thumb_02_%s_h' % t, 'thumb_03_%s_h' % t, True, 'thumb proximal')
        B['thumb_03_' + t] = ('thumb_02_' + t, 'thumb_03_%s_h' % t, 'thumb_03_%s_t' % t, True, 'thumb distal + claw')
        B['thigh_' + t] = ('pelvis', 'thigh_%s_h' % t, 'shin_%s_h' % t, True, 'leg'); B['shin_' + t] = ('thigh_' + t, 'shin_%s_h' % t, 'foot_%s_h' % t, True, 'leg')
        B['foot_' + t] = ('shin_' + t, 'foot_%s_h' % t, 'ball_%s_h' % t, True, 'foot (tarsus / metatarsus)')
        for k in range(1, 6):
            B['toe_%d_01_%s' % (k, t)] = ('foot_' + t, 'toe_%d_01_%s_h' % (k, t), 'toe_%d_02_%s_h' % (k, t), True, 'toe proximal phalanx (MTP)')
            B['toe_%d_02_%s' % (k, t)] = ('toe_%d_01_%s' % (k, t), 'toe_%d_02_%s_h' % (k, t), 'toe_%d_03_%s_h' % (k, t), True, 'toe middle phalanx')
            B['toe_%d_03_%s' % (k, t)] = ('toe_%d_02_%s' % (k, t), 'toe_%d_03_%s_h' % (k, t), 'toe_%d_03_%s_t' % (k, t), True, 'toe distal + claw')
    return B
def rec(J, M, cfg, B=None):
    B = B or bones(J)
    out = {}
    for b, (par, h, tl, dfm, role) in B.items():
        if h is None: out[b] = dict(parent=None, head=[0, 0, 0], tail=[0, 0, 10.0], deform=False, role=role, method='fixed control'); continue
        hv, tv = J[h], J[tl]; y = (tv - hv) / np.linalg.norm(tv - hv)
        up = np.array([0, 0, 1.0]) if abs(y[2]) < 0.9 else np.array([0, 1.0, 0]); x = np.cross(y, up); x /= np.linalg.norm(x); zax = np.cross(x, y)
        out[b] = dict(parent=par, head=np.round(hv, 5).tolist(), tail=np.round(tv, 5).tolist(), length_cm=round(float(np.linalg.norm(tv - hv)), 4), deform=dfm, role=role,
                      local_axes=dict(y_bone=np.round(y, 5).tolist(), x=np.round(x, 5).tolist(), z=np.round(zax, 5).tolist()), head_method=M[h], tail_method=M[tl],
                      configuration=cfg, c2_relation='same definition re-evaluated on this configuration' if not cfg.startswith('c1') else 'source (c1)')
    return out
if __name__ == '__main__':
    OUT = sys.argv[1] if len(sys.argv) > 1 else C.EV6; os.makedirs(OUT, exist_ok=True)
    J1, M1 = build(V1, 'c1'); J2, M2 = build(V2, 'c2'); B = bones(J1)
    P1 = rec(J1, M1, 'c1 SA-M188'); P2 = rec(J2, M2, 'c2 SA-F188')
    skel = dict(name='SA_RP6_skeleton_v001', status='RP6 RIG PILOT / NOT FROZEN', scope='Saurin-specific production-rig pilot hierarchy; NOT a universal game skeleton',
                units='cm, x right (+x = subject left = _l), y forward, z up', bones={b: dict(parent=v[0], deform=v[3], role=v[4]) for b, v in B.items()},
                counts=dict(total=len(B), deform=sum(v[3] for v in B.values()), tail=16), naming='lowercase, _l = subject left (+x, xpos), _r = subject right (-x, xneg); stable; no circular constraints',
                notes=['jaw: single hinge bone; no independent moving rostrum (rostrum is part of head)', 'cranial display / eyes: rigid with head; no biological mobility added',
                       'no twist bones in the pilot baseline: the 34-pose suite has no forearm / upper-arm axial twist pose (added only if deformation evidence requires)',
                       'metacarpals are deform bones so palm cupping is distributed (fist / grasp)', 'root is the only control bone; all other bones deform'])
    json.dump(skel, open(OUT + '/SA_RP6_skeleton_v001.json', 'w'), indent=1)
    json.dump(dict(configuration='c1 SA-M188', bones=P1), open(OUT + '/SA_RP6_joint_placement_M_v001.json', 'w'), indent=1)
    json.dump(dict(configuration='c2 SA-F188', bones=P2), open(OUT + '/SA_RP6_joint_placement_F_v001.json', 'w'), indent=1)
    dd = {b: float(np.linalg.norm(np.array(P2[b]['head']) - np.array(P1[b]['head']))) for b in B}
    print('bones', len(B), 'deform', skel['counts']['deform'], '| c1->c2 head offset max %.2f cm (%s)' % (max(dd.values()), max(dd, key=dd.get)))
