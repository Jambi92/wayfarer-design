# adjudicate.py V001.json FIT_V005.json OUTDIR [REV] : apply the author rulings AD-R1..AD-R12
# (reviews/chatgpt-rac-rp2-grask-rig-landmark-adjudication-and-diagnostic-rig-order.md) and write the versioned diagnostic landmark
# package GR_U_REF_RP2_rigprep_landmarks_v002.json (+ validation). Read-only on every parent; the frozen package is never edited.
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fitlib import *
V1, FIT, OUT = json.load(open(sys.argv[1])), json.load(open(sys.argv[2])), sys.argv[3]
REV = sys.argv[4] if len(sys.argv) > 4 else 'v002'
OVR = json.load(open(os.environ['LM_OVERRIDE'])) if os.environ.get('LM_OVERRIDE') else {}   # bounded revision (v003) only
os.makedirs(OUT, exist_ok=True)
FROZEN = json.load(open('/home/claude/wayfarer-design/reviews/rac-rp2-evidence/grask_retopo_v003_audit_closure/production/GR_U_REF_RP2_retopo_v003_landmarks.json'))['landmarks']
FZ = lambda k: np.array(FROZEN[k]['source_frame_cm'], float)
J1 = V1['joints']; P1 = lambda k: np.array(J1[k]['position_source_frame_cm'], float)
m5 = load('/tmp/claude-0/src3d/v5/v005.npz'); m3 = load('/tmp/claude-0/rt/frz/v003_frz.npz')
A = np.asarray; UP = A([0, 0, 1.0]); FWD = A([0, 1.0, 0]); LEFT = A([1.0, 0, 0])
R = {}; LOG = []
def depth(m, p):
    _, d, _ = m.nearest.on_surface(A([p])); return bool(m.contains(A([p]))[0]), float(d[0])
def rec(k, side, p, cls, suit, rule, limitation, **kw):
    ins5, d5 = depth(m5, p); ins3, d3 = depth(m3, p)
    R[k] = dict(id=k, side=side, provenance_class=cls, suitability=suit, p=A(p, float), construction_rule=rule, limitation=limitation,
                inside_v005=ins5, depth_v005_cm=d5, inside_v003=ins3, depth_v003_cm=d3, **kw)
def cap_move(p0, target, cap=0.5):
    d = target - p0; L = np.linalg.norm(d); return (p0 + d * min(1.0, cap / L) if L > 1e-12 else p0.copy()), float(L), float(min(L, cap))
def hloop(m, z, pick, keep=None):
    s = section(m, A([0, 0, z]), UP, pick, 25.0, keep); return s
def clipped_centroid(pts, xc):
    """area centroid of the closed polygon pts (horizontal) clipped to |x| <= xc (Sutherland-Hodgman, two half-planes)"""
    P = [tuple(p) for p in pts[:-1]] if np.allclose(pts[0], pts[-1]) else [tuple(p) for p in pts]
    def clip(P, inside, inter):
        out = []
        for i in range(len(P)):
            a, b = np.array(P[i - 1]), np.array(P[i])
            if inside(b):
                if not inside(a): out.append(tuple(inter(a, b)))
                out.append(tuple(b))
            elif inside(a): out.append(tuple(inter(a, b)))
        return out
    for sgn in (1, -1):
        P = clip(P, lambda q: sgn * q[0] <= xc, lambda a, b: a + (b - a) * ((sgn * xc - a[0]) / (b[0] - a[0])))
    Q = np.array(P); x, f = Q[:, 0], Q[:, 1]; x2, f2 = np.roll(x, -1), np.roll(f, -1); cr = x * f2 - x2 * f; Ar = cr.sum() / 2
    return A([((x + x2) * cr).sum() / (6 * Ar), ((f + f2) * cr).sum() / (6 * Ar), Q[0, 2]]), abs(Ar)

# ---------------------------------------------------------------- root / pelvis (AD-R7)
root = -T_PROD                                                          # production (0,0,0) in the source frame
rec('root', 'c', root, 'rig control (production origin)', 'diagnostic rig; final carry-forward subject to rig contract',
    'world/root-motion bone at the production origin on the ground plane (0,0,0 production)', 'not an anatomical point')
p0 = P1('pelvis_root'); sc = hloop(m5, p0[2], p0); pel, dist, mv = cap_move(p0, sc['c'], 0.5)
rec('pelvis', 'c', pel, 'manual-author-rig', 'diagnostic rig', 'v001 internal pelvis proposal moved toward the torso-section centroid at its height, capped at 5 mm',
    'internal; no pelvic bony anatomy in the source', adjustment_cm=mv, adjustment_reason='section-centroid fitting (centroid %.2f cm away; capped)' % dist)
LOG.append('AD-R7: root at production origin; pelvis = v001 proposal + %.2f cm toward section centroid' % mv)
# ---------------------------------------------------------------- legs (AD-R1, AD-R2)
for s, sg in (('l', 1), ('r', -1)):
    ct, dt = A(FIT['thigh_axis_' + s]['point']), A(FIT['thigh_axis_' + s]['dir'])
    h0 = P1('hip_' + s); foot = ct + ((h0 - ct) @ dt) * dt; hip, dist, mv = cap_move(h0, foot, 0.5)
    rec('hip_' + s, s, hip, 'manual-author-rig', 'diagnostic rig', 'v001 consensus hip moved toward the proximal-thigh load axis (soft-tissue thigh centreline), capped at 5 mm',
        'femoral head internal; no trochanteric relief', adjustment_cm=mv, adjustment_reason='thigh load axis %.2f cm from the consensus; moved 0.5 cm toward it' % dist)
    zk = P1('knee_' + s)[2]; s_ = hloop(m5, zk, P1('knee_' + s), keep=lambda e: 3 < sg * e[:, 0].mean() < 25)
    rec('knee_' + s, s, A([s_['c'][0], s_['c'][1], zk]), 'manual-author-rig', 'diagnostic rig', 'v001 consensus level; AP/ML = horizontal leg-section centroid at that level',
        'no condylar relief; level is an author decision', adjustment_cm=float(np.linalg.norm(s_['c'][:2] - P1('knee_' + s)[:2])), adjustment_reason='section centre (horizontal) vs v001 consensus xy')
    za = P1('ankle_' + s)[2]; s_ = hloop(m5, za, P1('ankle_' + s), keep=lambda e: 3 < sg * e[:, 0].mean() < 25)
    rec('ankle_' + s, s, A([s_['c'][0], s_['c'][1], za]), 'manual-author-rig', 'diagnostic rig', 'v001 consensus / anterior-crease level; AP/ML = distal-shin horizontal section centroid',
        'no malleolar relief; diagnostic engineering axis (mediolateral), not a biological axis',
        adjustment_cm=float(np.linalg.norm(s_['c'][:2] - P1('ankle_' + s)[:2])), adjustment_reason='section centre vs v001 xy')
    LOG.append('AD-R1/R2 %s: hip +%.2f cm toward thigh axis; knee z %.2f, ankle z %.2f on section centres' % (s, mv, zk, za))
# ---------------------------------------------------------------- arms (AD-R3, AD-R4)
GHINFO = {}
for s, sg in (('l', 1), ('r', -1)):
    acr = FZ('acromion_' + s); E1 = P1('elbow_' + s)
    d0 = A(FIT['upperarm_axis_' + s]['dir']); C = []; t = 3.0; zm = None
    while t < 40:                                                       # free upper-arm sections: elbow+3 cm up to the armpit contact
        o = E1 + d0 * t; sc_ = section(m5, o, d0, o, 7.0)
        if sc_ is None or sc_['area'] > 160: zm = o[2]; break
        C.append(sc_['c']); t += 0.5
    C = A(C); cu, du, ru = line_fit(C); du = du if du @ UP > 0 else -du
    # sensitivity: fits on the distal and proximal halves of the free sections
    half = len(C) // 2; alt = []
    for CC in (C[:half + 1], C[half:]):
        c2, d2, _ = line_fit(CC); d2 = d2 if d2 @ UP > 0 else -d2; alt.append((c2, d2))
    def at_z(c, d, z): return c + d * ((z - c[2]) / d[2])
    cand = []
    for off in (3.5, 4.0, 4.5):
        p = at_z(cu, du, acr[2] - off); ins, dd = depth(m5, p); cand.append((off, p, ins, dd))
    off, gh, ins, dd = [c for c in cand if c[0] == float(OVR.get('gh_offset_' + s, 4.0))][0]
    spread = max(np.linalg.norm(at_z(c2, d2, acr[2] - off) - gh) for c2, d2 in alt)
    ok = ins and dd >= 1.5
    GHINFO[s] = dict(n_sections=len(C), section_z=[float(C[0, 2]), float(C[-1, 2])], axis_point=cu, axis_dir=du, axis_rms_cm=ru, armpit_contact_z=zm,
                     candidates=[dict(offset_cm=o_, p=p_, inside=i_, depth_cm=d_) for o_, p_, i_, d_ in cand], half_fit_spread_cm=float(spread), rule_satisfied=bool(ok))
    if not ok: LOG.append('AD-R3 %s: RULE NOT SATISFIED (inside=%s depth=%.2f) -> STOP' % (s, ins, dd))
    rec('glenohumeral_' + s, s, gh, 'manual-author-rig', 'diagnostic rig', 'acromion anchor; free upper-arm shaft centreline (%d sections, z %.1f-%.1f) extrapolated superiorly; point %.1f cm inferior to the acromion on that line' % (len(C), C[0, 2], C[-1, 2], off),
        'humeral head internal; extrapolation over %.1f cm from a short free-arm base (half-fit spread %.2f cm)' % (acr[2] - off - C[-1, 2], spread),
        acromion_to_gh_cm=float(np.linalg.norm(acr - gh)), acromion_vertical_drop_cm=off, gh_rule=GHINFO[s])
    # elbow: v001 target level, moved toward the upper-arm/forearm hinge (midpoint of the two axes at that level), cap 5 mm
    cf, df = A(FIT['forearm_axis_' + s]['point']), A(FIT['forearm_axis_' + s]['dir']); df = df if df @ UP > 0 else -df
    hinge = 0.5 * (at_z(cu, du, E1[2]) + at_z(cf, df, E1[2])); el, dist, mv = cap_move(E1, hinge, 0.5)
    b = np.cross(du, df); b = b / np.linalg.norm(b); b = b if b @ LEFT >= 0 else -b
    rec('elbow_' + s, s, el, 'manual-author-rig', 'diagnostic rig', 'v001 cubital/waist target level; moved toward the reference-stance hinge (midpoint of the upper-arm and forearm axes at that level), capped at 5 mm',
        'no epicondylar relief', adjustment_cm=mv, adjustment_reason='hinge point %.2f cm from target' % dist, flex_axis=b)
    LOG.append('AD-R3/R4 %s: GH %.1f cm below acromion (inside=%s depth %.2f, half-fit spread %.2f); elbow +%.2f cm' % (s, off, ins, dd, spread, mv))
# ---------------------------------------------------------------- SC (AD-R5): anchor = v001 jugular/clavicular skin summit, 3.0 cm posterior
for s, sg in (('l', 1), ('r', -1)):
    anc = A(FIT['sternoclavicular_' + s]['surface_point']); dirn = -FWD
    loc, _, _ = m5.ray.intersects_location(A([anc - dirn * 0.01]), A([dirn]), multiple_hits=True)
    hits = sorted(float((q - anc) @ dirn) for q in loc if (q - anc) @ dirn > 0.05)
    exitd = hits[0] if hits else 0.0; dep = min(3.0, exitd - 0.05)
    p = anc + dirn * dep
    rec('sternoclavicular_' + s, s, p, 'manual-author-rig', 'diagnostic rig', 'jugular-notch / clavicular anterior surface summit moved %.2f cm straight posterior (−f, local AP)' % dep,
        'manual rigging landmark, not a measured joint', surface_anchor=anc, inward_direction=dirn, inward_cm=dep, through_thickness_cm=exitd)
# ---------------------------------------------------------------- spine (AD-R6)
for k in ('spine_01', 'spine_02', 'spine_03', 'neck_base'):
    rec(k, 'c', FZ(k), 'frozen package marker (MPFB/E3-seeded fitted estimate), carried unchanged', 'diagnostic rig (reference position)',
        'frozen v003 record, unchanged (AD-R6)', 'MPFB/E3-derived placement; not independently anatomical')
z3, zn = FZ('spine_03')[2], FZ('neck_base')[2]
ztrunk = 152.0; tl = hloop(m5, ztrunk, A([0, -4, ztrunk]), keep=lambda e: abs(e[:, 0].mean()) < 6)
XC = float(np.abs(tl['pts'][:, 0]).max())                                # trunk half-width below the armpit (arms still separate)
for i, fr in enumerate((0.25, 0.5, 0.75)):
    z = z3 + fr * (zn - z3); lp = hloop(m5, z, A([0, -4, z]), keep=lambda e: abs(e[:, 0].mean()) < 8)
    c, ar = clipped_centroid(lp['pts'], XC)
    rec('thoracic_%02d' % (i + 1), 'c', A([c[0], c[1], z]), 'manual-author-rig (rig-prep control)', 'diagnostic rig',
        '%d%% of the spine_03->neck_base vertical interval; AP/ML = torso horizontal-section centroid, section clipped to |x| <= %.2f cm (trunk half-width at z %.0f, below the armpit) so the arm/deltoid masses do not bias it' % (fr * 100, XC, ztrunk),
        'rig-prep control, not a declared vertebra', clip_half_width_cm=XC, clipped_area_cm2=ar)
rec('head_pivot', 'c', P1('head_pivot'), 'fitted joint-centre estimate (v001 consensus)', 'diagnostic rig', 'v001 consensus (unchanged)', 'internal; no skull anatomy')
rec('crown', 'c', FZ('crown'), 'frozen surface marker', 'diagnostic rig + final carry-forward', 'frozen v003 surface record', 'surface marker')
rec('chin', 'c', FZ('chin'), 'frozen surface marker', 'diagnostic rig + final carry-forward', 'frozen v003 surface record', 'surface marker')
# ---------------------------------------------------------------- face (AD-R8, AD-R11)
for s, sg in (('l', 1), ('r', -1)):
    rec('eye_' + s, s, P1('eye_' + s), 'copied construction coordinate (surface-validated)', 'diagnostic rig — NON-DEFORMING eye aim/reference only',
        'v003 eyeball-volume centre; sphere check 0.1-0.15 cm', 'no eyeball geometry; body mesh never weighted to it')
    rec('jaw_hinge_' + s, s, FZ('jaw_hinge_' + s), 'deferred facial placeholder (rule-based; corrects the frozen "construction coordinate (copied)" label)',
        'DEFERRED — REQUIRES FACIAL/ORAL COMPONENT STAGE (not in the diagnostic rig)', FROZEN['jaw_hinge_' + s]['note'], 'closed sculpted mouth; no mandible / oral cavity',
        frozen_label=FROZEN['jaw_hinge_' + s]['evidence'])
    for k in ('mouth_corner_', 'ear_root_', 'ear_tip_'):
        rec(k + s, s, FZ(k + s), 'frozen surface marker', 'reference marker (not a rig joint)', 'frozen v003 surface record', 'surface marker')
# ---------------------------------------------------------------- girdle markers and scapula proxy (AD-R9)
for s, sg in (('l', 1), ('r', -1)):
    acr, inf = FZ('acromion_' + s), FZ('scapular_inferior_proxy_' + s)
    rec('acromion_' + s, s, acr, 'frozen surface marker', 'diagnostic rig anchor + final carry-forward', 'frozen v003 surface record', 'lateral position derived from the frozen E3 GH seed ray')
    rec('scapular_inferior_proxy_' + s, s, inf, 'frozen surface proxy', 'diagnostic rig anchor', 'frozen v003 surface record', 'surface proxy only')
    zt = inf[2] + 0.6 * (acr[2] - inf[2]); xt = 0.45 * acr[0]
    loc, _, _ = m5.ray.intersects_location(A([[xt, -60.0, zt]]), A([[0, 1.0, 0]]), multiple_hits=False)
    p = loc[0]
    rec('scapula_medial_proxy_' + s, s, p, 'manual-author-rig-proxy', 'diagnostic rig only (girdle mechanics); not canon bony anatomy',
        'level = inferior proxy + 60%% toward the acromion (z %.2f); x = 45%% from the posterior midline toward the acromion x (%.2f); projected onto the posterior source surface (ray +f)' % (zt, xt),
        'no measurable scapular border in the source (GR-G2 constrained)', target=A([xt, np.nan, zt]))
# ---------------------------------------------------------------- hand / foot construction joints, balls (unchanged from v001)
for k, j in J1.items():
    if any(k.startswith(t) for t in ('wrist', 'index', 'middle', 'ring', 'pinky', 'thumb', 'hallux', 'toe2', 'toe3', 'toe4', 'toe5', 'ball')):
        rec(k, j['side'], A(j['position_source_frame_cm']), 'copied construction coordinate (surface-validated)' if not k.startswith('ball') else 'derived from copied construction coordinates',
            'diagnostic rig + final carry-forward candidate', j['method'], j['note'] or 'construction-defined', v001_frame=j.get('frame'))
for k, v in OVR.get('positions', {}).items():                            # bounded revision overrides (logged)
    R[k]['p'] = A(v['p']); R[k]['construction_rule'] += ' | REVISED (%s): %s' % (REV, v['reason']); LOG.append('REVISION %s %s: %s' % (REV, k, v['reason']))
def jsn(o):
    if isinstance(o, dict): return {k: jsn(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [jsn(v) for v in o]
    if isinstance(o, np.ndarray): return jsn(o.tolist())
    if isinstance(o, (np.floating, np.integer, np.bool_)): return o.item()
    return o
json.dump(jsn(dict(R=R, LOG=LOG, GH=GHINFO)), open(os.path.join(OUT, 'adjudicated_raw_%s.json' % REV), 'w'), indent=1)
print('\n'.join(LOG)); print(len(R), 'records')
