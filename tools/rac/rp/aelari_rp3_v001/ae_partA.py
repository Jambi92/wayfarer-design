# ae_partA.py WORK OUT.json : order fd71f15 Part A -- Aelari configuration-2 central reference (AELF190) validation.
#   determinism (record rebuild + independent full re-solve), native hm08 integrity, stature / envelope, configuration consistency (AELF190 - AEL1 vs the
#   human-family configuration architecture MFF190 - MFM190 / SGF190 - SGM190), Aelari body identity at matched stature (~190 cm) for BOTH configurations
#   against Marchfolk, Sagekin and frozen Fenn CF2 (canon directions from AELARI_V1 v1.0 / v1.1 and the order §1 / §5), and the relational pelvis rules
#   (AE-P2a / AE-P2b / AE-P3 / AE-P6) on the skeletal proxy (t = 0 / 0.5 / 1.0 cm; a direction holds only at all three) with skin readings as diagnostics.
import sys, os, json, numpy as np
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001')
W, OUT = sys.argv[1:3]; RA = '/home/claude/wayfarer-design/reviews/reference-assets'; PA = W + '/partA'
import importlib.util
spec = importlib.util.spec_from_file_location('fpa_int', '/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001/fenn_partA.py')
src = open(spec.origin).read(); integrity_src = src[src.index('def integrity'):src.index('meas = lambda')]
from collections import Counter
from scipy.spatial import cKDTree
exec(integrity_src)
meas = lambda p: json.load(open(p))['combined']
P = {'AEL1': PA + '/ref/AEL1_meas.json', 'AELF190': PA + '/build/AELF190_meas.json'}
for n in ('MFM190', 'MFF190', 'SGM190', 'SGF190', 'FNM190', 'FNF190'): P[n] = '%s/cmp/%s_meas.json' % (PA, n)
M = {k: meas(v) for k, v in P.items()}; M['AE168N-NAT'] = meas(RA + '/builds/AE168N-NAT_meas.json'); M['AE221'] = meas(RA + '/builds/AE221_meas.json')
def R(n, k):
    m = M[n]; r = m['ratio']
    if k in r: return r[k]
    if k == 'thoracic_vertical_share': return m['thoracic_vertical'] / m['stature']
    if k == 'waist_interval_share': return m['waist_interval'] / m['stature']
    if k == 'head_height_share': return m['cranio']['HH'] / m['stature']
    if k == 'cranial_vertical_share': return (m['cranio']['V'][2] - m['cranio']['OC_l'][2]) / m['stature']
    if k == 'central_vertical_share': return R(n, 'cranial_vertical_share') + r['neck_share'] + r['torso_share']
    if k == 'extremity_share': return r['arm_share'] + r['hand_share'] + r['leg_share'] + r['foot_share']
    if k.endswith('_breadth_share'): return m['mean'][k.replace('_share', '')] / m['stature']
    raise KeyError(k)
CFG = {'c1': dict(AE='AEL1', MF='MFM190', SG='SGM190', FN='FNM190'), 'c2': dict(AE='AELF190', MF='MFF190', SG='SGF190', FN='FNF190')}
# canon rows: (label, key, rule) ; rule: '>FN' Aelari > Fenn ; '>MF' > Marchfolk ; '<MF' < Marchfolk ; 'FN>' Fenn ordering for joints etc.
# canon rows: (label, key, rules) ; '>FN' Aelari > Fenn ; '>MF' / '<MF' vs Marchfolk (stock human reference); '>=..' tie band; 'evenMF' closer to MF than Fenn is;
# Sagekin is a long-limbed human race: reported in every row, used as a rule only where AELARI_V1 compares with "humans" for the trunk / neck.
CANON = [('central vertical share (cranium + neck + torso) > Fenn', 'central_vertical_share', ['>FN']),
         ('extremity share (arm + hand + leg + foot) < Fenn (Fenn extremity emphasis)', 'extremity_share', ['<FN']),
         ('torso share > Fenn (longer torso)', 'torso_share', ['>FN']),
         ('neck contribution > Fenn and > humans', 'neck_share', ['>FN', '>MF', '>SG']),
         ('cranial vertical contribution > Fenn and humans', 'cranial_vertical_share', ['>FN', '>MF']),
         ('ribcage / thoracic vertical > Fenn', 'thoracic_vertical_share', ['>FN']),
         ('waist interval / torso > Fenn, >= MF (AE-P6 skin diag.)', 'waist_interval_over_torso', ['>FN', '>=MF']),
         ('arm share > human (MF)', 'arm_share', ['>MF']),
         ('arm elongation even: forearm / upper arm closer to MF than Fenn', 'forearm_over_upperarm', ['evenMF']),
         ('leg share > human (MF)', 'leg_share', ['>MF']),
         ('leg elongation even: shin / leg closer to MF than Fenn', 'shin_over_leg', ['evenMF']),
         ('hands long: hand share > human (MF)', 'hand_share', ['>MF']),
         ('finger / hand >= human (MF)', 'finger_over_hand', ['>=MF']),
         ('wrist gracile: wrist breadth share < MF, Fenn more gracile', 'wrist_breadth_share', ['<MF', '>=FN']),
         ('elbow gracile: elbow breadth share < MF, Fenn more gracile', 'elbow_breadth_share', ['<MF', '>=FN']),
         ('knee gracile: knee breadth share < MF, Fenn more gracile', 'knee_breadth_share', ['<MF', '>=FN']),
         ('ankle gracile: ankle breadth share < MF, Fenn more gracile', 'ankle_breadth_share', ['<MF', '>=FN']),
         ('relatively shallow ribcage: thorax depth share < MF', 'thorax_depth_share', ['<MF']),
         ('feet longer: foot share > MF', 'foot_share', ['>MF'])]
TIE = 0.003                                                                                  # relative tie band for '>=' rules (method resolution, as Fenn A4)
def check(v, ref, rule):
    if rule.startswith('>='): return v >= ref * (1 - TIE)
    if rule.startswith('>'): return v > ref
    if rule.startswith('<'): return v < ref
res = dict(order='fd71f15', configs={}, notes=[])
for cfg, C in CFG.items():
    rows = []
    for lab, k, rules in CANON:
        v = {r_: R(C[r_], k) for r_ in ('AE', 'MF', 'SG', 'FN')}; ok = []
        for rule in rules:
            if rule == 'evenMF': ok.append(abs(v['AE'] - v['MF']) < abs(v['FN'] - v['MF']))
            else: ok.append(bool(check(v['AE'], v[rule.lstrip('>=<')], rule)))
        ok_ = dict(zip(rules, ok))
        rows.append(dict(measure=lab, key=k, AE=round(v['AE'], 5), MF=round(v['MF'], 5), SG=round(v['SG'], 5), FN=round(v['FN'], 5), AE_vs_MF_pct=round(100 * (v['AE'] / v['MF'] - 1), 2),
                         AE_vs_FN_pct=round(100 * (v['AE'] / v['FN'] - 1), 2), AE_vs_SG_pct=round(100 * (v['AE'] / v['SG'] - 1), 2), rules=rules, rule_results=ok_, holds=all(ok)))
    res['configs'][cfg] = dict(bodies=C, stature={k_: M[C[k_]]['stature'] for k_ in C}, canon=rows, holds=sum(r['holds'] for r in rows), of=len(rows))
# configuration consistency: AELF190 - AEL1 vs MFF190 - MFM190 and SGF190 - SGM190 (same sign, gap)
keys = [k for _, k, _ in CANON]
cons = []
for k in keys:
    dA = R('AELF190', k) - R('AEL1', k); dM = R('MFF190', k) - R('MFM190', k); dS = R('SGF190', k) - R('SGM190', k); dF = R('FNF190', k) - R('FNM190', k)
    cons.append(dict(key=k, d_AE=round(dA, 5), d_MF=round(dM, 5), d_SG=round(dS, 5), d_FN=round(dF, 5), same_sign_as_MF=bool(np.sign(dA) == np.sign(dM) or abs(dM) < 1e-4)))
res['configuration_consistency'] = dict(rows=cons, same_sign=sum(c['same_sign_as_MF'] for c in cons), of=len(cons), c1_signs_replicated_in_c2=sum(
    1 for _, k, _ in CANON if np.sign(R('AEL1', k) - R('MFM190', k)) == np.sign(R('AELF190', k) - R('MFF190', k))))
# pelvis on the skeletal proxy
SK = {n: json.load(open('%s/skp/%s_skp.json' % (PA, n))) for n in ('AEL1', 'AELF190', 'MFM190', 'MFF190', 'FNM190', 'FNF190')}
def sk(n, k, t): return SK[n]['by_t'][t]['ratio'][k]
pel = {}
for cfg, C in CFG.items():
    rows = []
    for lab, k, rel in [('AE-P2a hip-joint height / stature > MF', 'leg_share', '>MF'), ('AE-P2b / E-A2 bitrochanteric / crest not lower than MF', 'bitroch_over_crest', '>=MF'),
                        ('AE-P3 pelvic vertical / crest > MF', 'pelvic_vertical_over_crest', '>MF'), ('AE-P3 pelvic vertical / crest > Fenn', 'pelvic_vertical_over_crest', '>FN'),
                        ('AE-P6 waist interval / torso > Fenn', 'waist_interval_over_torso', '>FN'), ('AE-P6 waist interval / torso >= MF', 'waist_interval_over_torso', '>=MF')]:
        by = {}
        for t in SK[C['AE']]['by_t']:
            a = SK[C['AE']]['leg_share'] if k == 'leg_share' else sk(C['AE'], k, t); ref_n = C['MF'] if 'MF' in rel else C['FN']
            b = SK[ref_n]['leg_share'] if k == 'leg_share' else sk(ref_n, k, t); by[t] = dict(AE=round(a, 5), ref=round(b, 5), diff_pct=round(100 * (a / b - 1), 2), holds=bool(check(a, b, rel)))
        rows.append(dict(rule=lab, key=k, by_t=by, holds_all_t=all(x['holds'] for x in by.values()), align_resid_cm=SK[C['AE']]['align_joint_resid_cm']))
    pel[cfg] = rows
res['pelvis_skeletal_proxy'] = pel; res['pelvis_skin_diagnostic'] = {cfg: {k: dict(AE=R(C['AE'], k), MF=R(C['MF'], k), FN=R(C['FN'], k)) for k in ('bitroch_over_crest', 'pelvic_vertical_over_crest', 'waist_interval_over_torso', 'leg_share')} for cfg, C in CFG.items()}
# determinism and integrity
b1 = json.load(open(PA + '/build/AELF190_build.json')); b2 = json.load(open(PA + '/build2/AELF190_build.json'))
z1 = np.load(PA + '/build/AELF190_r6.npz'); z2 = np.load(PA + '/build2/AELF190_r6.npz')
res['determinism'] = dict(height_macro=[b1['height_macro'], b2['height_macro']], second_resolve_max_abs_dV_cm=float(np.abs(z1['V'].astype(float) - z2['V'].astype(float)).max()),
                          faces_identical=bool(np.array_equal(z1['F'], z2['F'])), stature_r6=[b1['stature_r6'], b2['stature_r6']], cfg_equals_AEL1_except=[k for k in set(b1['cfg']) | set(json.load(open(RA + '/builds/AEL1_build.json'))['cfg']) if b1['cfg'].get(k) != json.load(open(RA + '/builds/AEL1_build.json'))['cfg'].get(k)])
res['envelope'] = dict(AE168N_NAT=M['AE168N-NAT']['stature'], AEL1=M['AEL1']['stature'], AELF190=M['AELF190']['stature'], AE221=M['AE221']['stature'], inside=bool(M['AE168N-NAT']['stature'] < M['AELF190']['stature'] < M['AE221']['stature']))
json.dump(res, open(OUT, 'w'), indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
for cfg in CFG: print(cfg, 'canon %d/%d' % (res['configs'][cfg]['holds'], res['configs'][cfg]['of']), [r['key'] for r in res['configs'][cfg]['canon'] if not r['holds']], 'pelvis', [(r['rule'][:20], r['holds_all_t']) for r in pel[cfg]])
print('consistency', res['configuration_consistency']['same_sign'], '/', len(cons), 'c1 signs replicated', res['configuration_consistency']['c1_signs_replicated_in_c2'], '| determinism', res['determinism'])
