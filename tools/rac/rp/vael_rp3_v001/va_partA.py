# va_partA.py WORK OUT.json : Vael order (2026-10-28) Part A -- Vael configuration-2 central reference (VALF178) validation:
#   determinism (record build + independent full re-solve), native hm08 integrity, stature / envelope, configuration consistency (VALF178 - VAL4 vs the
#   human-family configuration architecture MFF - MFM / SGF - SGM), Vael body identity at matched stature (178 cm) for BOTH configurations against
#   Marchfolk, Sagekin, frozen Fenn (FNL4-CF2 / FNF181-CF2 records) and frozen Aelari (AEL1-R1 / AELF190-R1 records), using the canon rows of VAEL_V1
#   (L35-47, L114-154) with the conventions accepted at W1n / W1o (strict directions; limb-balance rows ~ MF +/- 0.010), and the Vael pelvis rules
#   VA-P2a / P2b / P2c / P3 / P4 / P6 on the skeletal proxy (t = 0 / 0.5 / 1.0 cm; a rule holds only at all three) with skin readings as diagnostics.
import sys, os, json, numpy as np
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001')
W, OUT = sys.argv[1:3]; RA = '/home/claude/wayfarer-design/reviews/reference-assets'; PA = W + '/partA'
import importlib.util
from collections import Counter
from scipy.spatial import cKDTree
src = open('/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001/fenn_partA.py').read(); exec(src[src.index('def integrity'):src.index('meas = lambda')])
meas = lambda p: json.load(open(p))['combined']
P = {'VAL4': PA + '/ref/VAL4_meas.json', 'VALF178': PA + '/build/VALF178_meas.json'}
for n in ('MFM178', 'MFF178', 'SGM178', 'SGF178', 'FNM178', 'FNF178', 'AEM178', 'AEF178'): P[n] = '%s/cmp/%s_meas.json' % (PA, n)
M = {k: meas(v) for k, v in P.items()}; M['VA157-NAT'] = meas(RA + '/builds/VA157-NAT_meas.json'); M['VA203'] = meas(RA + '/builds/VA203_meas.json')
def R(n, k):
    m = M[n]; r = m['ratio']
    if k in r: return r[k]
    if k == 'thoracic_vertical_share': return m['thoracic_vertical'] / m['stature']
    if k == 'cranial_vertical_share': return (m['cranio']['V'][2] - m['cranio']['OC_l'][2]) / m['stature']
    if k == 'central_vertical_share': return R(n, 'cranial_vertical_share') + r['neck_share'] + r['torso_share']
    if k == 'extremity_share': return r['arm_share'] + r['hand_share'] + r['leg_share'] + r['foot_share']
    if k == 'shin_over_thigh': return r['shin_share'] / r['thigh_share']
    if k == 'foot_breadth_over_length': return m['mean']['foot_breadth'] / m['mean']['foot_len']
    if k == 'neck_over_torso': return r['neck_share'] / r['torso_share']
    raise KeyError(k)
CFG = {'c1': dict(VA='VAL4', MF='MFM178', SG='SGM178', FN='FNM178', AE='AEM178'), 'c2': dict(VA='VALF178', MF='MFF178', SG='SGF178', FN='FNF178', AE='AEF178')}
# canon rows (label, key, rules, canon source); '>X' / '<X' strict, '~MF' within +/- 0.010 of MF (W1n balance convention), '>=X' with a 0.3 % tie band
CANON = [('greater torso share than Fenn', 'torso_share', ['>FN'], 'VAEL L37'),
         ('deeper ribcage than Fenn and Aelari (thorax depth / stature)', 'thorax_depth_share', ['>FN', '>AE'], 'VAEL L37, L116'),
         ('less elongated torso / waist continuity than Aelari (waist interval / torso)', 'waist_interval_over_torso', ['<AE'], 'VAEL L37, L123; ECR'),
         ('more compact vertical distribution than Aelari (cranium + neck + torso share)', 'central_vertical_share', ['<AE'], 'order §1; ECR'),
         ('less extremity emphasis than Fenn (arm + hand + leg + foot share)', 'extremity_share', ['<FN'], 'order §1; ECR'),
         ('legs long vs humans, somewhat smaller leg share than Fenn and Aelari', 'leg_share', ['>MF', '<FN', '<AE'], 'VAEL L46, L153'),
         ('arms long vs humans, less elongated than Fenn', 'arm_share', ['>MF', '<FN'], 'VAEL L44, L151'),
         ('arms less elongated than Aelari (W1n BM-3: not demonstrated within 1 % accepted)', 'arm_share', ['<=AE'], 'VAEL L44; BM-3'),
         ('balanced femur and lower leg (lower leg / thigh ~ MF)', 'shin_over_thigh', ['~MF'], 'VAEL L46'),
         ('balanced upper arm and forearm (forearm / upper arm ~ MF)', 'forearm_over_upperarm', ['~MF'], 'VAEL L44'),
         ('elbow presence > Fenn / Aelari, gracile vs MF (elbow / humerus)', 'elbow_over_humerus', ['>FN', '>AE', '<MF'], 'VAEL L37, L145'),
         ('wrist presence > Fenn / Aelari, gracile vs MF (wrist / forearm)', 'wrist_over_forearm', ['>FN', '>AE', '<MF'], 'VAEL L37, L145'),
         ('knee presence > Fenn / Aelari, gracile vs MF (knee / femur)', 'knee_over_femur', ['>FN', '>AE', '<MF'], 'VAEL L37, L145'),
         ('ankle presence > Fenn / Aelari, gracile vs MF (ankle / lower leg)', 'ankle_over_shin', ['>FN', '>AE', '<MF'], 'VAEL L37, L46, L145'),
         ('broader palm / hand base than Fenn and Aelari (palm breadth / hand)', 'palm_breadth_over_hand', ['>FN', '>AE'], 'VAEL L45, L152'),
         ('elven hands: hand share > human', 'hand_share', ['>MF'], 'VAEL L45'),
         ('feet broader than Fenn and Aelari (foot breadth / length)', 'foot_breadth_over_length', ['>FN', '>AE'], 'VAEL L47, L154'),
         ('feet moderately elongated: foot share > human', 'foot_share', ['>MF'], 'VAEL L47')]
REPORT = [('neck / torso (Fenn >= Vael, RAC-03 E-4; Aelari > Vael)', 'neck_over_torso'), ('thorax breadth / stature (moderate width; not stocky)', 'thorax_breadth_share'),
          ('shoulder-joint breadth / stature (spacing, not presence)', 'shoulder_joint_share'), ('thoracic vertical / stature', 'thoracic_vertical_share'), ('neck share', 'neck_share'),
          ('cranial vertical share', 'cranial_vertical_share'), ('shin / leg', 'shin_over_leg'), ('thorax depth / breadth', 'thorax_d_over_b')]
TIE = 0.003
def check(v, ref, rule):
    if rule.startswith('~'): return abs(v - ref) <= 0.010
    if rule.startswith('>='): return v >= ref * (1 - TIE)
    if rule.startswith('<='): return v <= ref * (1 + 0.01)
    if rule.startswith('>'): return v > ref
    if rule.startswith('<'): return v < ref
res = dict(order='reviews/chatgpt-rac-rp3-vael-body-face-ear-order.md (2026-10-28)', configs={}, notes=[])
for cfg, C in CFG.items():
    rows = []
    for lab, k, rules, srcl in CANON:
        v = {r_: R(C[r_], k) for r_ in ('VA', 'MF', 'SG', 'FN', 'AE')}; ok = {}
        for rule in rules: ok[rule] = bool(check(v['VA'], v[rule.lstrip('>=<~')], rule))
        rows.append(dict(measure=lab, key=k, canon=srcl, **{x: round(v[x], 5) for x in v}, VA_vs_MF_pct=round(100 * (v['VA'] / v['MF'] - 1), 2), VA_vs_FN_pct=round(100 * (v['VA'] / v['FN'] - 1), 2),
                         VA_vs_AE_pct=round(100 * (v['VA'] / v['AE'] - 1), 2), VA_vs_SG_pct=round(100 * (v['VA'] / v['SG'] - 1), 2), rules=rules, rule_results=ok, holds=all(ok.values())))
    rep = [dict(measure=lab, key=k, **{x: round(R(C[x], k), 5) for x in ('VA', 'MF', 'SG', 'FN', 'AE')}) for lab, k in REPORT]
    res['configs'][cfg] = dict(bodies=C, stature={k_: M[C[k_]]['stature'] for k_ in C}, canon=rows, report=rep, holds=sum(r['holds'] for r in rows), of=len(rows))
keys = [k for _, k, _, _ in CANON]
cons = []
for k in dict.fromkeys(keys):
    dV = R('VALF178', k) - R('VAL4', k); dM = R('MFF178', k) - R('MFM178', k); dS = R('SGF178', k) - R('SGM178', k)
    cons.append(dict(key=k, d_VA=round(dV, 5), d_MF=round(dM, 5), d_SG=round(dS, 5), same_sign_as_MF=bool(np.sign(dV) == np.sign(dM) or abs(dM) < 1e-4)))
res['configuration_consistency'] = dict(rows=cons, same_sign=sum(c['same_sign_as_MF'] for c in cons), of=len(cons))
# pelvis on the skeletal proxy
SK = {n: json.load(open('%s/skp/%s_skp.json' % (PA, n))) for n in ('VAL4', 'VALF178', 'MFM178', 'MFF178', 'FNM178', 'FNF178', 'AEM178', 'AEF178')}
def sk(n, k, t):
    b = SK[n]['by_t'][t]; r = b['ratio']; H = SK[n]['stature_r6']
    if k == 'leg_share': return SK[n]['leg_share']
    if k == 'hip_joint_scale_share': return b['extra']['prox_femur'] / H          # proximal-femur head / neck span (hip-joint scale proxy) / stature
    if k == 'iliac_envelope_share': return r['crest_share'] * r['pelvic_depth_share']   # iliac crest breadth x AP depth / stature^2 (structural-presence proxy)
    return r[k]
PR = [('VA-P2a hip-joint height / stature > MF', 'leg_share', '>MF'), ('VA-P2a hip-joint height / stature < Fenn', 'leg_share', '<FN'), ('VA-P2a hip-joint height / stature < Aelari', 'leg_share', '<AE'),
      ('VA-P2b bitrochanteric / crest not lower than MF', 'bitroch_over_crest', '>=MF'),
      ('VA-P2c hip-joint scale (proximal femur / stature) > Fenn', 'hip_joint_scale_share', '>FN'), ('VA-P2c hip-joint scale > Aelari', 'hip_joint_scale_share', '>AE'),
      ('VA-P2c hip-joint scale gracile vs MF', 'hip_joint_scale_share', '<MF'),
      ('VA-P3 iliac structural presence (crest x AP depth / stature^2) > Fenn', 'iliac_envelope_share', '>FN'), ('VA-P3 iliac structural presence > Aelari', 'iliac_envelope_share', '>AE'),
      ('VA-P3 iliac structural presence lighter than MF', 'iliac_envelope_share', '<MF'),
      ('VA-P3 no Aelari-style vertical iliac elongation (pelvic vertical / crest < Aelari)', 'pelvic_vertical_over_crest', '<AE'),
      ('VA-P4 pelvic AP depth / stature > Fenn', 'pelvic_depth_share', '>FN'), ('VA-P4 pelvic AP depth / stature > Aelari', 'pelvic_depth_share', '>AE'),
      ('VA-P4 pelvic AP depth / stature ~ MF (minimum relation; > MF not required)', 'pelvic_depth_share', '~=MF'),
      ('VA-P6 waist interval / torso < Aelari (compact continuity)', 'waist_interval_over_torso', '<AE')]
def pchk(a, b, rel):
    if rel == '~=MF': return a >= b * 0.98                                          # "approximately MF is sufficient": within 2 % below MF or above
    return check(a, b, rel)
pel = {}
for cfg, C in CFG.items():
    rows = []
    for lab, k, rel in PR:
        by = {}
        for t in SK[C['VA']]['by_t']:
            a = sk(C['VA'], k, t); ref = C[rel.lstrip('~=<>')[:2]]; b = sk(ref, k, t)
            by[t] = dict(VA=round(a, 5), ref=round(b, 5), diff_pct=round(100 * (a / b - 1), 2), holds=bool(pchk(a, b, rel)))
        gate = k not in ('hip_joint_scale_share', 'iliac_envelope_share')        # VA-P2c / VA-P3 construction: PV-D17 visual for W1, no accepted numeric proxy -> report only
        rows.append(dict(rule=lab, key=k, rel=rel, by_t=by, holds_all_t=all(x['holds'] for x in by.values()), gating=gate, align_resid_cm=SK[C['VA']]['align_joint_resid_cm']))
    pel[cfg] = rows
res['pelvis_skeletal_proxy'] = pel; res['pelvis_gating_summary'] = {c: dict(gating_hold=sum(r['holds_all_t'] for r in v if r['gating']), gating_of=sum(r['gating'] for r in v), failing=[r['rule'] for r in v if r['gating'] and not r['holds_all_t']], report_only_not_holding=[r['rule'] for r in v if not r['gating'] and not r['holds_all_t']]) for c, v in pel.items()}
res['pelvis_proxy_note'] = ('hip-joint scale = proximal-femur head / neck span from the skeletal proxy (girdle_femur); iliac structural presence = iliac-crest breadth x AP depth '
                            '(skeletal stations S5 x S6, both / stature) -- proxies for construction that RM-UB-06 cannot measure directly; the visual check is on the pelvis sheet')
res['pelvis_skin_diagnostic'] = {cfg: {k: dict(VA=R(C['VA'], k), MF=R(C['MF'], k), FN=R(C['FN'], k), AE=R(C['AE'], k)) for k in ('bitroch_over_crest', 'pelvic_vertical_over_crest', 'pelvic_depth_share', 'waist_interval_over_torso', 'leg_share', 'crest_share')} for cfg, C in CFG.items()}
b1 = json.load(open(PA + '/build/VALF178_build.json')); b2 = json.load(open(PA + '/build2/VALF178_build.json'))
z1 = np.load(PA + '/build/VALF178_r6.npz'); z2 = np.load(PA + '/build2/VALF178_r6.npz'); bv = json.load(open(RA + '/builds/VAL4_build.json'))['cfg']
res['determinism'] = dict(height_macro=[b1['height_macro'], b2['height_macro']], second_resolve_max_abs_dV_cm=float(np.abs(z1['V'].astype(float) - z2['V'].astype(float)).max()),
                          faces_identical=bool(np.array_equal(z1['F'], z2['F'])), stature_r6=[b1['stature_r6'], b2['stature_r6']], cfg_differs_from_VAL4=[k for k in set(b1['cfg']) | set(bv) if b1['cfg'].get(k) != bv.get(k)])
res['envelope'] = dict(VA157_NAT=M['VA157-NAT']['stature'], VAL4=M['VAL4']['stature'], VALF178=M['VALF178']['stature'], VA203=M['VA203']['stature'], inside=bool(M['VA157-NAT']['stature'] < M['VALF178']['stature'] < M['VA203']['stature']))
if os.path.exists(PA + '/regen/VALF178_native.npz'): res['native_integrity'] = integrity(PA + '/regen/VALF178_native.npz')
json.dump(res, open(OUT, 'w'), indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
for cfg in CFG: print(cfg, 'canon %d/%d' % (res['configs'][cfg]['holds'], res['configs'][cfg]['of']), [(r['key'], {k: v for k, v in r['rule_results'].items() if not v}) for r in res['configs'][cfg]['canon'] if not r['holds']])
for cfg in CFG: print(cfg, 'pelvis', [(r['rule'][:44], r['holds_all_t'], r['by_t']['0.5']['diff_pct']) for r in pel[cfg]])
print('consistency', res['configuration_consistency']['same_sign'], '/', res['configuration_consistency']['of'], '| determinism', res['determinism'], '| envelope', res['envelope'])
