# diag_lib.py : numpy linear-blend skinning identical to Blender's armature modifier (vertex groups, normalised by total weight),
# pose definitions D1..D10 and deformation measurements for the Grask diagnostic rig. Mesh = frozen v003 read-back (never written).
import json, numpy as np, os
T_PROD = np.array([-0.11179767867288516, 5.722717396009755, 0.0])
def src_to_bl(V): P = V + T_PROD; return np.c_[P[:, 0], -P[:, 1], P[:, 2]] / 100.0
def bl_to_src(Vb): P = np.c_[Vb[:, 0], -Vb[:, 1], Vb[:, 2]] * 100.0; return P - T_PROD
def rotm(axis, deg):
    a = np.radians(deg); c, s = np.cos(a), np.sin(a)
    return {'X': np.array([[1, 0, 0], [0, c, -s], [0, s, c]]), 'Y': np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]]), 'Z': np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])}[axis]
class Rig:
    def __init__(self, rigjson, wnpz):
        R = json.load(open(rigjson)); self.B = {b['name']: b for b in R['bones']}; self.order = [b['name'] for b in R['bones']]
        z = np.load(wnpz); self.W = z['W'].astype(np.float64); self.names = [str(n) for n in z['names']]
        self.rest = {n: np.array(self.B[n]['matrix_local'], float) for n in self.order}
        tot = self.W.sum(1); self.tot = np.where(tot > 0, tot, 1.0); self.zero = tot <= 0
    def pose_mats(self, pose, pivots=None):
        """pose: {bone: [(axis, deg), ...]} local rotations (applied in list order, Blender matrix_basis). pivots: {bone: new head (Blender m)} placement test"""
        M = {}; S = {}
        for n in self.order:                                              # bones are stored parent-before-child
            b = self.B[n]; Rl = self.rest[n].copy()
            if pivots and n in pivots: Rl[:3, 3] = pivots[n]
            basis = np.eye(4)
            for ax, d in pose.get(n, []): basis[:3, :3] = basis[:3, :3] @ rotm(ax, d)
            if b['parent']:
                Rp = self.rest[b['parent']].copy()
                if pivots and b['parent'] in pivots: Rp[:3, 3] = pivots[b['parent']]
                M[n] = M[b['parent']] @ np.linalg.inv(Rp) @ Rl @ basis
            else: M[n] = Rl @ basis
            S[n] = M[n] @ np.linalg.inv(Rl)
        return M, S
    def skin(self, Vb, pose, pivots=None):
        M, S = self.pose_mats(pose, pivots); out = np.zeros_like(Vb); L = np.zeros((len(Vb), 3, 3))
        for i, n in enumerate(self.names):
            w = self.W[:, i]; k = w > 0
            if not k.any(): continue
            out[k] += w[k, None] * (Vb[k] @ S[n][:3, :3].T + S[n][:3, 3]); L[k] += w[k, None, None] * S[n][:3, :3]
        out /= self.tot[:, None]; L /= self.tot[:, None, None]
        out[self.zero] = Vb[self.zero]; L[self.zero] = np.eye(3)
        return out, L, M
    def head(self, n, M=None): return (M[n] if M is not None else self.rest[n])[:3, 3]
    def axis(self, n, ax, M=None): return (M[n] if M is not None else self.rest[n])[:3, 'XYZ'.index(ax)]
    def choose(self, bone, child_dir_wanted_bl, axes=('X', 'Z')):
        """local axis + sign whose positive 10-degree rotation moves the bone tail most along the wanted (Blender) direction"""
        best = None; t0 = np.array(self.B[bone]['tail']); h = np.array(self.B[bone]['head'])
        for ax in axes:
            for sg in (1, -1):
                _, S = self.pose_mats({bone: [(ax, 10 * sg)]}); t1 = S[bone][:3, :3] @ t0 + S[bone][:3, 3]
                sc = (t1 - t0) @ child_dir_wanted_bl
                if best is None or sc > best[0]: best = (sc, ax, sg)
        return best[1], best[2]
def bl_dir(v): v = np.asarray(v, float); return np.array([v[0], -v[1], v[2]])     # analysis direction -> Blender
LEFT, FWD, UP = np.array([1.0, 0, 0]), np.array([0, 1.0, 0]), np.array([0, 0, 1.0])
def build_poses(rig):
    """D1..D10 technical test poses (degrees; engineering diagnostics, not range-of-motion canon)"""
    P = {}; ch = lambda b, d, axes=('X', 'Z'): rig.choose(b, bl_dir(d), axes)
    for s, sg in (('l', 1), ('r', -1)):
        ax_ab, s_ab = ch('upperarm_' + s, sg * LEFT); ax_fl, s_fl = ch('upperarm_' + s, FWD)
        P['D1_%s_abd45' % s] = {'upperarm_' + s: [(ax_ab, s_ab * 37)]}            # 8 deg stance abduction + 37 = 45
        P['D1_%s_abd90' % s] = {'upperarm_' + s: [(ax_ab, s_ab * 82)]}
        P['D1_%s_flex90' % s] = {'upperarm_' + s: [(ax_fl, s_fl * 90)]}
        P['D1_%s_ext30' % s] = {'upperarm_' + s: [(ax_fl, -s_fl * 30)]}
        ax_hf, s_hf = ch('thigh_' + s, FWD); ax_ha, s_ha = ch('thigh_' + s, sg * LEFT)
        P['D6_%s_flex45' % s] = {'thigh_' + s: [(ax_hf, s_hf * 45)]}
        P['D6_%s_flex90' % s] = {'thigh_' + s: [(ax_hf, s_hf * 90)]}
        P['D6_%s_abd30' % s] = {'thigh_' + s: [(ax_ha, s_ha * 30)]}
    s = 'l'
    FIT = json.load(open('/tmp/claude-0/rt/rpr/fit_v005.json'))
    Mh = np.array(FIT['wrist_l']['hand_frame']); u_d, v_rad, w_dor = Mh[:, 0], Mh[:, 1], Mh[:, 2]     # construction hand frame (analysis)
    dor = lambda j: np.array(FIT['cx_' + j]['dorsal'])
    ax, sg_ = ch('forearm_l', FWD, ('X',)); P['D2_l_flex90'] = {'forearm_l': [(ax, sg_ * 90)]}; P['D2_l_flex130'] = {'forearm_l': [(ax, sg_ * 130)]}
    if os.environ.get('ELBOW_SET'): P['D2_l_flex45'] = {'forearm_l': [(ax, sg_ * 45)]}   # elbow isolation set only (order b303b9e §4); not part of the 43-pose suite
    ax, sg_ = ch('hand_l', -w_dor, ('X', 'Z')); P['D3_l_flex60'] = {'hand_l': [(ax, sg_ * 60)]}; P['D3_l_ext60'] = {'hand_l': [(ax, -sg_ * 60)]}
    ax2 = 'Z' if ax == 'X' else 'X'; a2, s2 = ch('hand_l', v_rad, (ax2,)); P['D3_l_radial20'] = {'hand_l': [(a2, s2 * 20)]}; P['D3_l_ulnar20'] = {'hand_l': [(a2, -s2 * 20)]}
    fist = {}
    for f in ('index', 'middle', 'ring', 'pinky'):
        for k, deg, jn in ((1, 90, 'mcp'), (2, 100, 'pip'), (3, 70, 'dip')):
            b = '%s_p%d_l' % (f, k); a_, s_ = ch(b, -dor('%s_%s_l' % (f, jn)), ('X',)); fist[b] = [(a_, s_ * deg)]
    P['D4_l_fist'] = fist
    for sgn, nm in ((1, 'spread_p10'), (-1, 'spread_m10')):
        sp = {}
        for f, w in (('index', 1.0), ('ring', -1.0), ('pinky', -1.5)):
            b = '%s_p1_l' % f; a_, s_ = ch(b, v_rad * np.sign(w), ('Z',)); sp[b] = [(a_, s_ * sgn * 10 * abs(w))]
        P['D4_l_' + nm] = sp                                         # +: index radial, ring/pinky ulnar (spread apart); -: together
    # opposition target: the thumb tip moves toward the index fingertip (direction from the thumb tip to the index tip at rest)
    tt = np.array(rig.B['thumb_p2_l']['tail']); it = np.array(rig.B['index_p3_l']['tail']); tgt = bl_to_dir_from_bl(it - tt)
    a1, s1 = ch('thumb_mc_l', tgt, ('X', 'Z')); a2_, s2_ = ch('thumb_p1_l', tgt, ('X',)); a3, s3 = ch('thumb_p2_l', tgt, ('X',))
    # bounded searches (thumb CMC three axes, MCP, IP): thumb tip as close as possible to (a) the pinky MCP base and (b) the index tip
    # with the index finger in a pinch (MCP 45, PIP 60, DIP 30). The index tip itself is out of reach of the extended-index thumb
    # (CMC -> index tip 22.9 cm vs thumb length 15.7 cm), so a pinch is the meaningful opposition test.
    tail = lambda S, b: S[b][:3, :3] @ np.array(rig.B[b]['tail']) + S[b][:3, 3]
    head = lambda S, b: S[b][:3, :3] @ np.array(rig.B[b]['head']) + S[b][:3, 3]
    pinch = {}
    for k, deg, jn in ((1, 45, 'mcp'), (2, 60, 'pip'), (3, 30, 'dip')):
        b = 'index_p%d_l' % k; a_, s_ = ch(b, -dor('index_%s_l' % jn), ('X',)); pinch[b] = [(a_, s_ * deg)]
    def search(extra, target):
        best = None
        for ay in (-40, -20, 0, 20, 40):
            for am in (-45, -30, -15, 0, 15, 30, 45):
                for bm in (-60, -45, -30, -15, 0, 15, 30, 45, 60):
                    for p1 in (0, 20, 40, 60):
                        for p2 in (0, 20, 40, 60):
                            pz = dict(extra, **{'upperarm_l': P['D1_l_abd45']['upperarm_l'], 'thumb_mc_l': [('Y', ay), ('X', am), ('Z', bm)], 'thumb_p1_l': [(a2_, s2_ * p1)], 'thumb_p2_l': [(a3, s3 * p2)]})
                            _, S = rig.pose_mats(pz); d = np.linalg.norm(tail(S, 'thumb_p2_l') - target(S))
                            if best is None or d < best[0]: best = (d, pz)
        return best
    b1 = search({}, lambda S: head(S, 'pinky_p1_l')); b2 = search(pinch, lambda S: tail(S, 'index_p3_l'))
    P['D5_l_oppose_pinky'] = b1[1]; P['D5_l_oppose_pinch'] = b2[1]
    P['_D5_search'] = {'pinky_bone_tip_gap_cm': float(b1[0] * 100), 'pinch_bone_tip_gap_cm': float(b2[0] * 100)}
    ax, sg_ = ch('shin_l', -FWD, ('X',)); P['D7_l_flex90'] = {'shin_l': [(ax, sg_ * 90)]}; P['D7_l_flex140'] = {'shin_l': [(ax, sg_ * 140)]}
    ax, sg_ = ch('foot_l', UP, ('X',)); P['D8_l_dorsi20'] = {'foot_l': [(ax, sg_ * 20)]}; P['D8_l_plantar40'] = {'foot_l': [(ax, -sg_ * 40)]}
    te = {}; tf = {}
    for t in ('hallux', 'toe2', 'toe3', 'toe4', 'toe5'):
        b = '%s_p1_l' % t; a_, s_ = ch(b, UP, ('X',)); te[b] = [(a_, s_ * 30)]; tf[b] = [(a_, -s_ * 30)]
    P['D8_l_toes_ext30'] = te; P['D8_l_toes_flex30'] = tf
    # test setup: the reference stance holds the palm against the thigh, so D2-D5 start from 45 deg shoulder abduction (the D1_l_abd45 pose)
    # to keep the forearm / hand clear of the thigh and trunk; the base rotation is recorded with each pose
    base = P['D1_l_abd45']['upperarm_l']
    for k in [k for k in P if k.startswith(('D2_', 'D3_', 'D4_', 'D5_'))]: P[k] = dict(P[k], upperarm_l=base)
    P['D2_l_base_abd45'] = {'upperarm_l': base}
    # D6 test setup: the hanging arm sits against the lateral thigh, so hip tests start with that side's arm at 45 deg abduction
    for s in 'lr':
        for k in [k for k in P if k.startswith('D6_%s_' % s)]: P[k] = dict(P[k], **{'upperarm_' + s: P['D1_%s_abd45' % s]['upperarm_' + s]})
    # D1 girdle-assisted variants: part of the elevation taken by the clavicle (scapulohumeral participation), diagnostic only
    for s, sg in (('l', 1), ('r', -1)):
        ax_c, s_c = ch('clavicle_' + s, UP, ('X', 'Z'))
        ab = P['D1_%s_abd90' % s]['upperarm_' + s][0]; fl = P['D1_%s_flex90' % s]['upperarm_' + s][0]
        P['D1_%s_abd90_girdle' % s] = {'upperarm_' + s: [(ab[0], ab[1] * 62 / 82)], 'clavicle_' + s: [(ax_c, s_c * 20)]}
        P['D1_%s_flex90_girdle' % s] = {'upperarm_' + s: [(fl[0], fl[1] * 70 / 90)], 'clavicle_' + s: [(ax_c, s_c * 20)]}
    sp = ['spine_01', 'spine_02', 'spine_03', 'thoracic_01', 'thoracic_02', 'thoracic_03']
    P['D9_twist_p30'] = {b: [('Y', 5.0)] for b in sp}; P['D9_twist_m30'] = {b: [('Y', -5.0)] for b in sp}
    fl = {}
    for b in sp: a_, s_ = ch(b, FWD, ('X',)); fl[b] = [(a_, s_ * 5.0)]
    P['D9_flex30'] = fl
    an, sn = ch('neck', FWD, ('X',)); ah, sh = ch('head', FWD, ('X',))
    P['D10_flex30'] = {'neck': [(an, sn * 15)], 'head': [(ah, sh * 15)]}; P['D10_ext30'] = {'neck': [(an, -sn * 15)], 'head': [(ah, -sh * 15)]}
    P['D10_rot_p45'] = {'neck': [('Y', 25)], 'head': [('Y', 20)]}; P['D10_rot_m45'] = {'neck': [('Y', -25)], 'head': [('Y', -20)]}
    return P
def bl_to_dir_from_bl(v):                                                          # Blender vector -> analysis direction (for ch(), which converts back)
    v = np.asarray(v, float); return np.array([v[0], -v[1], v[2]])
