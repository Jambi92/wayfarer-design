# va2_eval.py OUT.json CFG ID:PREFIX [ID:PREFIX ...] : Vael body / face source order (2026-10-28) -- one evaluator for probes and candidates.
#   CFG = c1 | c2 (comparators at 178 cm from the Vael Part A workspace: Marchfolk, Sagekin, frozen Fenn sources, frozen Aelari sources); PREFIX + _meas.json
#   and _r6.npz must exist (run_candidate output). Ears are excluded everywhere (hm08 w_ears > 0.05).
# BODY
#   canon      : the 18 VAEL_V1 rows of va_partA.py (strict directions vs Fenn / Aelari; leg / arm > MF; W1n conventions) + VA-P2a / VA-P6 (skin = joint
#                landmark readings: hip-joint height and spine joints are the same values the skeletal proxy reads).
#   systems    : eight written Vael body systems (order §4.3 directions) read against humans (Marchfolk; Sagekin-Marchfolk = ordinary human-family
#                variation). MATERIAL: a descriptor differs from Marchfolk in the system's Vael direction by >= 1 % AND by more than the Sagekin-Marchfolk
#                difference, or the region correspondence RMS vs Marchfolk exceeds the Sagekin-Marchfolk RMS by >= 25 %. STRONG: the descriptor rule at 2x.
# FACE
#   systems    : the six order §13 systems read against Marchfolk after similarity alignment (head size removed): material when a descriptor departs >= 1 % and
#                > 2x human baseline in the intended direction, or every system region RMS > 2x baseline and > 0.5 % HH -- and no descriptor departs materially the
#                wrong way; plus the Vael-vs-Aelari / Fenn canon rows.
import sys, os, json, numpy as np, scipy.sparse as sp
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001')
import fn_face_metrics as F
OUT, CF = sys.argv[1:3]; ITEMS = [a.split(':') for a in sys.argv[3:]]; PA = os.environ.get('VA_PA', '/tmp/claude-0/rt/va/partA')
CMP = {'c1': dict(MF='MFM178', SG='SGM178', FN='FNM178', AE='AEM178'), 'c2': dict(MF='MFF178', SG='SGF178', FN='FNF178', AE='AEF178')}[CF]
jl = lambda p: json.load(open(p))
def load(prefix):
    m = jl(prefix + '_meas.json')['combined']; z = F.load(prefix + '_r6.npz'); return dict(m=m, V=z['V'], we=z['we'])
REF = {k: load('%s/cmp/%s' % (PA, n)) for k, n in CMP.items()}
# native topology regions (dominant weight), as va_hidden_ear.py
nz = np.load('/tmp/claude-0/rt/fn/src/FNL4_native.npz'); bones = [str(b) for b in nz['bones']]; dom = np.array(bones)[np.asarray(nz['W']).argmax(1)]
def breg(b):
    if b.startswith(('upperarm', 'lowerarm')): return 'arm'
    if b.startswith(('hand', 'index', 'middle', 'ring', 'pinky', 'thumb')): return 'hand'
    if b.startswith(('thigh', 'calf')): return 'leg'
    if b.startswith(('foot', 'ball')): return 'foot'
    if b.startswith(('spine', 'pelvis', 'clavicle', 'Root')): return 'trunk'
    if b.startswith('neck'): return 'neck'
    return 'head'
BREG = np.array([breg(b) for b in dom]); EAR = F.EAR
def neck_dims(V):                                                   # neck breadth / depth at mid-neck height (skin), over stature
    m = (BREG == 'neck') & ~EAR; z = V[m, 2]; zc = 0.5 * (np.percentile(z, 10) + np.percentile(z, 90)); s = m & (np.abs(V[:, 2] - zc) < 0.6); P = V[s]; H = V[:, 2].max() - V[:, 2].min()
    return (P[:, 0].max() - P[:, 0].min()) / H, (P[:, 1].max() - P[:, 1].min()) / H
def R(d, k):
    m = d['m']; r = m['ratio']
    if k in r: return r[k]
    if k == 'thoracic_vertical_share': return m['thoracic_vertical'] / m['stature']
    if k == 'cranial_vertical_share': return (m['cranio']['V'][2] - m['cranio']['OC_l'][2]) / m['stature']
    if k == 'central_vertical_share': return R(d, 'cranial_vertical_share') + r['neck_share'] + r['torso_share']
    if k == 'extremity_share': return r['arm_share'] + r['hand_share'] + r['leg_share'] + r['foot_share']
    if k == 'shin_over_thigh': return r['shin_share'] / r['thigh_share']
    if k == 'foot_breadth_over_length': return m['mean']['foot_breadth'] / m['mean']['foot_len']
    if k == 'joint_mean': return np.mean([r['elbow_over_humerus'], r['wrist_over_forearm'], r['knee_over_femur'], r['ankle_over_shin']])
    if k == 'neck_breadth_share': return neck_dims(d['V'])[0]
    if k == 'neck_depth_share': return neck_dims(d['V'])[1]
    if k == 'neck_breadth_over_shoulder_joint': return neck_dims(d['V'])[0] / r['shoulder_joint_share']
    raise KeyError(k)
CANON = [('torso share > Fenn', 'torso_share', ['>FN']), ('thorax depth > Fenn, Aelari', 'thorax_depth_share', ['>FN', '>AE']), ('waist interval / torso < Aelari (VA-P6)', 'waist_interval_over_torso', ['<AE']),
         ('central vertical < Aelari', 'central_vertical_share', ['<AE']), ('extremity < Fenn', 'extremity_share', ['<FN']),
         ('hip-joint height / stature > MF, < Fenn, < Aelari (VA-P2a)', 'leg_share', ['>MF', '<FN', '<AE']), ('arm share > MF, < Fenn', 'arm_share', ['>MF', '<FN']), ('arm <= Aelari (BM-3)', 'arm_share', ['<=AE']),
         ('elbow presence > FN, AE', 'elbow_over_humerus', ['>FN', '>AE']), ('wrist presence > FN, AE', 'wrist_over_forearm', ['>FN', '>AE']), ('knee presence > FN, AE', 'knee_over_femur', ['>FN', '>AE']),
         ('ankle presence > FN, AE', 'ankle_over_shin', ['>FN', '>AE']), ('joints gracile vs humans (mean of 4 joint / segment ratios < MF)', 'joint_mean', ['<MF']),
         ('palm breadth / hand > FN, AE', 'palm_breadth_over_hand', ['>FN', '>AE']), ('hand share > MF', 'hand_share', ['>MF']), ('foot breadth / length > FN, AE', 'foot_breadth_over_length', ['>FN', '>AE']),
         ('foot share > MF', 'foot_share', ['>MF']), ('pelvic AP depth > FN, AE (VA-P4 skin)', 'pelvic_depth_share', ['>FN', '>AE']), ('bitroch / crest >= MF (VA-P2b skin)', 'bitroch_over_crest', ['>=MF'])]
def chk(v, ref, rule):
    if rule.startswith('>='): return v >= ref * 0.997
    if rule.startswith('<='): return v <= ref * 1.01
    return v > ref if rule[0] == '>' else v < ref
# body systems vs humans: (descriptors with elven direction), region
BSYS = {'1 ribcage depth / thoracic volume': ([('thorax_depth_share', +1), ('thorax_d_over_b', +1)], 'trunk'),
        '2 torso-to-pelvis continuity': ([('pelvic_depth_over_thorax_depth', +1), ('waist_interval_over_torso', -1)], 'trunk'),
        '3 limb share (long vs humans)': ([('leg_share', +1), ('arm_share', +1)], 'leg'),
        '4 joint scale (gracile vs humans)': ([('joint_mean', -1), ('wrist_over_forearm', -1), ('ankle_over_shin', -1)], 'arm'),
        '5 hand base / elven hand': ([('finger_over_hand', +1), ('palm_breadth_over_hand', +1)], 'hand'),
        '6 foot base': ([('foot_breadth_over_length', +1)], 'foot'),
        '7 pelvis / hip relationship': ([('pelvic_depth_share', +1), ('bitroch_over_crest', +1)], None),
        '8 shoulder / neck integration': ([('neck_breadth_over_shoulder_joint', +1), ('neck_breadth_share', +1), ('neck_depth_share', +1)], 'neck')}
def face_desc(d):
    V = d['V']; m = d['m']; x = F.descriptors(V); g = lambda k: V[F.LM[k]]; zy = abs(g('zygion_l')[0] - g('zygion_r')[0]); HH = x['head_height_cm']
    x['cranial_height_over_stature'] = (g('vertex')[2] - g('nasion')[2]) / (V[:, 2].max() - V[:, 2].min())
    x['face_height_over_bizygomatic'] = (g('nasion')[2] - g('menton')[2]) / zy
    x['forehead_to_chin_over_bizygomatic'] = (g('forehead')[2] - g('menton')[2]) / zy
    x['brow_projection_over_HH'] = (g('glabella')[1] - g('nasion')[1]) / HH
    x['orbit_breadth_over_HL'] = m['cranio']['ORB_breadth_over_HL']; x['orbit_height_over_HH'] = m['cranio']['ORB_height_over_HH']
    ap = m['cranio']['aperture']; x['eye_aperture_area_over_HH2'] = 0.5 * (ap['l']['area_cm2'] + ap['r']['area_cm2']) / HH ** 2
    return x
# face systems vs Marchfolk: descriptors (elven / Vael direction), regions
FSYS = {'1 cranial proportion / shared elven ancestry': ([('cranial_height_over_stature', +1), ('cranial_height_over_face', +1)], ['cranium_vault', 'forehead']),   # Vael width: moderate-broad variation, no direction
        '2 compact vertical distribution': ([('face_height_over_bizygomatic', -1), ('lower_face_height_over_HH', -1)], ['jaw_chin', 'mouth']),
        '3 cheek / mid-face integration': ([('bizygomatic_over_HH', +1), ('cheekbone_height_over_HH', +1)], ['cheeks_midface']),
        '4 mid-face depth': ([('midface_projection_over_HH', +1)], ['cheeks_midface', 'nose']),
        '5 orbit / brow system': ([('brow_projection_over_HH', -1)], ['orbit_eye_region']),     # elven direction vs humans = lighter brow (no heavy human brow / scowl, order §10.5); 'stronger than Aelari' is the face_canon_vs_elves row     # orbit_breadth_over_HL reported only: its landmark is unstable (MF vs SG 7 % on identical faces)
        '6 mandibular system (more than elves, gracile vs humans)': ([('jaw_width_over_bizygomatic', -1), ('lower_face_width_over_bizygomatic', -1)], ['jaw_chin'])}
FCANON = {'face_height_over_bizygomatic': (-1, 'AE'), 'forehead_to_chin_over_bizygomatic': (-1, 'AE'), 'cranial_height_over_stature': (-1, 'AE'), 'bizygomatic_over_HH': (+1, 'AE'),
          'midface_projection_over_HH': (+1, 'AE'), 'orbit_breadth_over_HL': (+1, 'AE'), 'brow_projection_over_HH': (+1, 'AE'), 'jaw_width_over_bizygomatic': (+1, 'AE'), 'jaw_width_over_bizygomatic@FN': (+1, 'FN')}
FD = {k: face_desc(v) for k, v in REF.items()}; hd = F.HEAD
fsm = F.procrustes(REF['SG']['V'][hd], REF['MF']['V'][hd]); BASE_F = {r: float(np.sqrt((np.linalg.norm(REF['MF']['V'][m] - fsm(REF['SG']['V'])[m], axis=1) ** 2).mean()) * 10) for r, m in F.REG.items()}
def rms_body(Va, Vb, r):
    m = (BREG == r) & ~EAR; return float(np.sqrt((np.linalg.norm(Va[m] - Vb[m], axis=1) ** 2).mean()) * 10)
BASE_B = {r: rms_body(REF['SG']['V'], REF['MF']['V'], r) for r in ('trunk', 'arm', 'hand', 'leg', 'foot', 'neck')}
res = dict(cfg=CF, comparators=CMP, rules=dict(body_material='descriptor: >= 1 % and > |SG/MF - 1| in the Vael direction (strong: > 2 x); or region RMS vs MF >= 1.25 x SG-MF RMS',
                                                    face_material='descriptor: >= 1 % and > 2 x |SG/MF - 1| in the Vael direction; or region RMS vs MF > 2 x SG-MF RMS and > 0.5 % HH'),
           human_baseline_body_rms_mm={k: round(v, 2) for k, v in BASE_B.items()}, human_baseline_face_rms_mm={k: round(v, 3) for k, v in BASE_F.items()}, items={})
for tag, prefix in ITEMS:
    d = load(prefix); it = {}
    rows = []
    for lab, k, rules in CANON:
        v = R(d, k); ok = {rl: bool(chk(v, R(REF[rl.lstrip('>=<')], k), rl)) for rl in rules}
        rows.append(dict(row=lab, key=k, VA=round(v, 5), **{x: round(R(REF[x], k), 5) for x in REF}, vs_pct={x: round(100 * (v / R(REF[x], k) - 1), 2) for x in REF}, results=ok, holds=all(ok.values())))
    it['canon'] = rows; it['canon_holds'] = sum(r['holds'] for r in rows); it['canon_of'] = len(rows); it['canon_failing'] = [r['row'] for r in rows if not r['holds']]
    bs = {}
    for s, (ds, reg) in BSYS.items():
        dl = []
        for k, sg in ds:
            v, mf, sgv = R(d, k), R(REF['MF'], k), R(REF['SG'], k); dv = 100 * (v / mf - 1); hb = abs(100 * (sgv / mf - 1))
            dl.append(dict(key=k, dir=sg, VA=round(v, 5), MF=round(mf, 5), SG=round(sgv, 5), VA_vs_MF_pct=round(dv, 2), human_var_pct=round(hb, 2), material=bool(np.sign(dv) == sg and abs(dv) >= 1.0 and abs(dv) > hb), strong=bool(np.sign(dv) == sg and abs(dv) >= 1.0 and abs(dv) > 2 * hb)))
        rr = None
        if reg: a = rms_body(d['V'], REF['MF']['V'], reg); rr = dict(region=reg, VA_vs_MF_mm=round(a, 2), SG_vs_MF_mm=round(BASE_B[reg], 2), material=bool(a >= 1.25 * BASE_B[reg]))
        bs[s] = dict(descriptors=dl, region=rr, material=bool(any(x['material'] for x in dl) or (rr and rr['material'])), strong=bool(any(x['strong'] for x in dl)))
    it['body_systems'] = bs; it['body_systems_material'] = sum(v['material'] for v in bs.values()); it['body_systems_strong'] = sum(v['strong'] for v in bs.values())
    it['body_region_rms_mm'] = {r: dict(VA_vs_MF=round(rms_body(d['V'], REF['MF']['V'], r), 2), VA_vs_SG=round(rms_body(d['V'], REF['SG']['V'], r), 2), VA_vs_FN=round(rms_body(d['V'], REF['FN']['V'], r), 2),
                                        VA_vs_AE=round(rms_body(d['V'], REF['AE']['V'], r), 2), SG_vs_MF=round(BASE_B[r], 2)) for r in BASE_B}
    fd = face_desc(d); Va = d['V']; HH = fd['head_height_cm']; maps = {k: F.procrustes(REF[k]['V'][hd], Va[hd]) for k in REF}
    freg = {}
    for r, m in F.REG.items():
        rm = {k: float(np.sqrt((np.linalg.norm(Va[m] - maps[k](REF[k]['V'])[m], axis=1) ** 2).mean()) * 10) for k in REF}
        freg[r] = dict(**{'VA_vs_%s_mm' % k: round(v, 3) for k, v in rm.items()}, human_baseline_mm=round(BASE_F[r], 3), material_vs_MF=bool(rm['MF'] > 2 * BASE_F[r] and rm['MF'] / 10 / HH * 100 > 0.5))
    fs = {}
    for s, (ds, regs) in FSYS.items():
        dl = []
        for k, sg in ds:
            v, mf, sgv = fd[k], FD['MF'][k], FD['SG'][k]; dv = 100 * (v / mf - 1); hb = abs(100 * (sgv / mf - 1))
            dl.append(dict(key=k, dir=sg, VA=round(v, 5), MF=round(mf, 5), VA_vs_MF_pct=round(dv, 2), human_var_pct=round(hb, 2), material=bool(np.sign(dv) == sg and abs(dv) >= 1.0 and abs(dv) > 2 * hb),
                           wrong_material=bool(np.sign(dv) == -sg and abs(dv) >= 1.0 and abs(dv) > 2 * hb)))
        rg = {r: freg[r]['material_vs_MF'] for r in regs}
        fs[s] = dict(descriptors=dl, regions=rg, material=bool((any(x['material'] for x in dl) or all(rg.values())) and not any(x['wrong_material'] for x in dl)))
    fc = {}
    for key, (sg, ref) in FCANON.items():
        k = key.split('@')[0]; dv = 100 * (fd[k] / FD[ref][k] - 1); fc[key] = dict(VA=round(fd[k], 5), ref=ref, ref_value=round(FD[ref][k], 5), VA_vs_ref_pct=round(dv, 2), holds=bool(np.sign(dv) == sg))
    it['face_systems'] = fs; it['face_systems_material'] = sum(v['material'] for v in fs.values()); it['face_regions'] = freg; it['face_canon_vs_elves'] = fc
    it['face_canon_vs_elves_holds'] = sum(v['holds'] for v in fc.values()); it['face_desc'] = {k: round(v, 5) for k, v in fd.items()}
    it['face_desc_vs_MF_pct'] = {k: round(100 * (fd[k] / FD['MF'][k] - 1), 2) for k in fd}
    it['stature'] = d['m']['stature']; res['items'][tag] = it
    print('%-26s st %.2f | canon %d/%d fail %s | bodysys %d/8 (strong %d) | facesys %d/6 | faceVsElves %d/9' % (tag, it['stature'], it['canon_holds'], it['canon_of'], [x[:28] for x in it['canon_failing']], it['body_systems_material'], it['body_systems_strong'], it['face_systems_material'], it['face_canon_vs_elves_holds']))
json.dump(res, open(OUT, 'w'), indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
