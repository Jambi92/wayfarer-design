# hv_partA.py WORK OUT.json : Halvren central-anchor order (2026-10-29) Part A / C / D --
#   A  HVF178 configuration-2 central anchor validation: determinism (record build + independent full re-solve), HVC1 rebuild identity, native hm08
#      integrity, stature / envelope, configuration consistency (HVF178 - HVC1 against the human-family configuration architecture MFF - MFM / SGF - SGM).
#   C  matched-stature (178 cm) body comparison against Marchfolk, Sagekin, Skarn (diagnostic, below the Skarn envelope), frozen Fenn, frozen Aelari and
#      frozen Vael for both configurations; per metric group (torso, shoulder / clavicle, arm, leg, joint scale, hand, foot, head / neck):
#        - source-population protection: Halvren vs each source (material = |diff| >= 1 % and > 2x the human baseline |SG - MF|);
#        - "not an arithmetic average": for every human / elf pair (MF-FN, MF-AE, MF-VA, SG-FN, SK-VA) the position t = (HV - H) / (E - H) of each metric
#          with a material pair gap, and a one-parameter scalar-blend fit HV ~ H + a (E - H) over all such metrics (a mechanical average shows a consistent
#          t near a with small residual on every group);
#        - nearest-source table (which population each metric is closest to, in units of the pair gap).
#   D  pelvis report on the skeletal proxy (t = 0 / 0.5 / 1.0 cm) and skin: hip-joint height / stature, bitrochanteric / crest, pelvic vertical
#      contribution, AP depth, waist / torso continuity, hip-joint scale proxy -- REPORT ONLY (Halvren pelvic inheritance is OPEN; no canon is applied).
import sys, os, json, numpy as np
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001')
W, OUT = sys.argv[1:3]; RA = '/home/claude/wayfarer-design/reviews/reference-assets'; PA = W + '/partA'
from collections import Counter
from scipy.spatial import cKDTree
src = open('/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001/fenn_partA.py').read(); exec(src[src.index('def integrity'):src.index('meas = lambda')])
meas = lambda p: json.load(open(p))['combined']
P = {'HVC1': PA + '/ref/HVC1_meas.json', 'HVF178': PA + '/build/HVF178_meas.json'}
for n in ('MFM178', 'MFF178', 'SGM178', 'SGF178', 'SKM178', 'SKF178', 'FNM178', 'FNF178', 'AEM178', 'AEF178', 'VAM178', 'VAF178'): P[n] = '%s/cmp/%s_meas.json' % (PA, n)
M = {k: meas(v) for k, v in P.items()}
for n in ('HV152N-NAT', 'HV213M'): M[n] = meas(RA + '/builds/%s_meas.json' % n)
def R(n, k):
    m = M[n]; r = m['ratio']
    if k in r: return r[k]
    if k == 'thoracic_vertical_share': return m['thoracic_vertical'] / m['stature']
    if k == 'cranial_vertical_share': return (m['cranio']['V'][2] - m['cranio']['OC_l'][2]) / m['stature']
    if k == 'extremity_share': return r['arm_share'] + r['hand_share'] + r['leg_share'] + r['foot_share']
    if k == 'shin_over_thigh': return r['shin_share'] / r['thigh_share']
    if k == 'foot_breadth_over_length': return m['mean']['foot_breadth'] / m['mean']['foot_len']
    if k == 'neck_over_torso': return r['neck_share'] / r['torso_share']
    if k == 'joint_mean': return np.mean([r[x] for x in ('elbow_over_humerus', 'wrist_over_forearm', 'knee_over_femur', 'ankle_over_shin')])
    raise KeyError(k)
GROUPS = {'torso': ['torso_share', 'thorax_depth_share', 'thorax_breadth_share', 'thorax_d_over_b', 'thoracic_vertical_share', 'waist_interval_over_torso'],
          'shoulder / clavicle': ['shoulder_joint_share', 'shoulder_breadth_share'],
          'arm': ['arm_share', 'forearm_over_upperarm', 'hand_over_arm'],
          'leg': ['leg_share', 'shin_over_thigh', 'shin_over_leg'],
          'joint scale': ['elbow_over_humerus', 'wrist_over_forearm', 'knee_over_femur', 'ankle_over_shin'],
          'hand': ['hand_share', 'palm_breadth_over_hand', 'finger_over_hand'],
          'foot': ['foot_share', 'foot_breadth_over_length'],
          'head / neck': ['neck_share', 'cranial_vertical_share', 'HH_share', 'neck_over_torso'],
          'pelvis (skin)': ['bitroch_over_crest', 'pelvic_depth_share', 'pelvic_vertical_share', 'crest_share']}
KEYS = [k for g in GROUPS.values() for k in g]
CFG = {'c1': dict(HV='HVC1', MF='MFM178', SG='SGM178', SK='SKM178', FN='FNM178', AE='AEM178', VA='VAM178'),
       'c2': dict(HV='HVF178', MF='MFF178', SG='SGF178', SK='SKF178', FN='FNF178', AE='AEF178', VA='VAF178')}
SRC = ('MF', 'SG', 'SK', 'FN', 'AE', 'VA'); PAIRS = [('MF', 'FN'), ('MF', 'AE'), ('MF', 'VA'), ('SG', 'FN'), ('SK', 'VA')]
pct = lambda a, b: 100 * (a / b - 1)
res = dict(order='reviews/chatgpt-rac-rp3-halvren-central-anchor-order.md (2026-10-29)', groups=GROUPS, configs={},
           notes=['Skarn comparators are SK / SKF208 records re-solved to 178 cm, below the accepted 183-229 cm Skarn envelope: diagnostic only (order §9 "where supported")',
                  'material = |difference| >= 1 % and > 2x the human-human baseline |SG - MF| for that metric (the convention of the Vael gates)'])
for cfg, C in CFG.items():
    v = {k: {s: R(C[s], k) for s in ('HV',) + SRC} for k in KEYS}; hb = {k: abs(pct(v[k]['SG'], v[k]['MF'])) for k in KEYS}
    mat = lambda k, a, b: abs(pct(a, b)) >= 1.0 and abs(pct(a, b)) > 2 * hb[k]
    rows = {}
    for k in KEYS:
        rows[k] = dict(values={s: round(x, 5) for s, x in v[k].items()}, human_baseline_pct=round(hb[k], 2),
                       HV_vs_pct={s: round(pct(v[k]['HV'], v[k][s]), 2) for s in SRC}, HV_material_vs={s: bool(mat(k, v[k]['HV'], v[k][s])) for s in SRC},
                       nearest=min(SRC, key=lambda s: abs(v[k]['HV'] - v[k][s])))
    prot = {s: dict(material_metrics=sum(rows[k]['HV_material_vs'][s] for k in KEYS), of=len(KEYS), groups_with_material={g: sum(rows[k]['HV_material_vs'][s] for k in ks) for g, ks in GROUPS.items()},
                    rms_pct=round(float(np.sqrt(np.mean([rows[k]['HV_vs_pct'][s] ** 2 for k in KEYS]))), 2)) for s in SRC}
    avg = {}
    for H, E_ in PAIRS:
        ts = {}; X = []; Y = []
        for k in KEYS:
            gap = v[k][E_] - v[k][H]
            if abs(pct(v[k][E_], v[k][H])) >= 1.0 and abs(pct(v[k][E_], v[k][H])) > 2 * hb[k]:
                ts[k] = (v[k]['HV'] - v[k][H]) / gap; X.append(gap / v[k][H]); Y.append((v[k]['HV'] - v[k][H]) / v[k][H])
        X = np.array(X); Y = np.array(Y); a = float((X @ Y) / (X @ X)) if len(X) else float('nan'); res_ = Y - a * X
        r2 = float(1 - (res_ @ res_) / (Y @ Y)) if len(X) and (Y @ Y) > 0 else float('nan')
        tv = np.array(list(ts.values())); near_mid = int(np.sum(np.abs(tv - 0.5) <= 0.15)) if len(tv) else 0
        bygroup = {g: [round(ts[k], 2) for k in ks if k in ts] for g, ks in GROUPS.items()}
        avg['%s-%s' % (H, E_)] = dict(metrics_with_material_gap=len(ts), t=ts and {k: round(x, 3) for k, x in ts.items()}, t_by_group=bygroup, t_median=round(float(np.median(tv)), 3) if len(tv) else None,
                                      t_iqr=[round(float(np.percentile(tv, 25)), 3), round(float(np.percentile(tv, 75)), 3)] if len(tv) else None,
                                      near_midpoint_0p35_0p65=near_mid, near_human_end_abs_t_le_0p15=int(np.sum(np.abs(tv) <= 0.15)), outside_pair_t_lt0_or_gt1=int(np.sum((tv < 0) | (tv > 1))),
                                      scalar_blend_fit=dict(alpha=round(a, 3), r2=round(r2, 3), residual_rms_pct=round(float(np.sqrt(np.mean(res_ ** 2)) * 100), 3) if len(X) else None),
                                      groups_with_t_in_0p35_0p65={g: sum(1 for t in x if 0.35 <= t <= 0.65) for g, x in bygroup.items()})
    near = Counter(rows[k]['nearest'] for k in KEYS)
    res['configs'][cfg] = dict(bodies=C, stature={s: M[C[s]]['stature'] for s in C}, rows=rows, source_protection=prot, arithmetic_average_audit=avg, nearest_source_count=dict(near))
# configuration consistency: HVF178 - HVC1 vs the human-family configuration architecture
cons = []
for k in KEYS:
    dH = R('HVF178', k) - R('HVC1', k); dM = R('MFF178', k) - R('MFM178', k); dS = R('SGF178', k) - R('SGM178', k)
    cons.append(dict(key=k, d_HV=round(dH, 5), d_MF=round(dM, 5), d_SG=round(dS, 5), same_sign_as_MF=bool(np.sign(dH) == np.sign(dM) or abs(dM) < 1e-4), within_human_pattern=bool(min(dM, dS) - 0.003 <= dH <= max(dM, dS) + 0.003)))
res['configuration_consistency'] = dict(rows=cons, same_sign=sum(c['same_sign_as_MF'] for c in cons), within_human_pattern=sum(c['within_human_pattern'] for c in cons), of=len(cons))
# the design offset (Halvren - Marchfolk of the same configuration) carried by both configurations
res['shared_design'] = {k: dict(c1_HV_minus_MF_pct=round(pct(R('HVC1', k), R('MFM178', k)), 2), c2_HV_minus_MF_pct=round(pct(R('HVF178', k), R('MFF178', k)), 2)) for k in KEYS}
# pelvis report on the skeletal proxy (REPORT ONLY)
SKP = {n: json.load(open('%s/skp/%s_skp.json' % (PA, n))) for c in CFG.values() for n in c.values()}
def sk(n, k, t):
    b = SKP[n]['by_t'][t]; r = b['ratio']; H = SKP[n]['stature_r6']
    if k == 'leg_share': return SKP[n]['leg_share']
    if k == 'hip_joint_scale_share': return b['extra']['prox_femur'] / H
    return r[k]
PK = [('hip-joint height / stature', 'leg_share'), ('bitrochanteric / crest', 'bitroch_over_crest'), ('pelvic vertical contribution (pelvic vertical / stature)', 'pelvic_vertical_share'),
      ('pelvic vertical / crest', 'pelvic_vertical_over_crest'), ('AP depth / stature', 'pelvic_depth_share'), ('waist interval / torso', 'waist_interval_over_torso'),
      ('hip-joint scale proxy (proximal femur / stature)', 'hip_joint_scale_share'), ('crest breadth / stature', 'crest_share')]
pel = {}
for cfg, C in CFG.items():
    rows = []
    for lab, k in PK:
        by = {}
        for t in SKP[C['HV']]['by_t']:
            try: val = {s: sk(C[s], k, t) for s in ('HV',) + SRC}
            except KeyError: val = None
            if val is None: continue
            by[t] = dict(values={s: round(x, 5) for s, x in val.items()}, HV_vs_pct={s: round(pct(val['HV'], val[s]), 2) for s in SRC}, nearest=min(SRC, key=lambda s: abs(val['HV'] - val[s])))
        rows.append(dict(measure=lab, key=k, by_t=by))
    pel[cfg] = rows
res['pelvis_report'] = pel
res['pelvis_note'] = 'REPORT ONLY: Halvren pelvic inheritance is OPEN (HALVREN_V1 Part 2 §15-19); no rule is applied. HVC1 carries no pelvis-specific target (Marchfolk pelvis construction).'
b1 = json.load(open(PA + '/build/HVF178_build.json')); b2 = json.load(open(PA + '/build2/HVF178_build.json')); z1 = np.load(PA + '/build/HVF178_r6.npz'); z2 = np.load(PA + '/build2/HVF178_r6.npz')
h1 = np.load(PA + '/ref/HVC1_r6.npz'); h0 = np.load(RA + '/r6/HVC1_r6.npz'); bc = json.load(open(RA + '/builds/HVC1_build.json'))['cfg']
res['determinism'] = dict(HVF178_height_macro=[b1['height_macro'], b2['height_macro']], HVF178_second_resolve_max_abs_dV_cm=float(np.abs(z1['V'].astype(float) - z2['V'].astype(float)).max()),
                          HVF178_faces_identical=bool(np.array_equal(z1['F'], z2['F'])), HVF178_stature_r6=[b1['stature_r6'], b2['stature_r6']],
                          HVC1_record_rebuild_max_abs_dV_cm=float(np.abs(h1['V'].astype(float) - h0['V'].astype(float)).max()), HVC1_faces_identical=bool(np.array_equal(h1['F'], h0['F'])),
                          cfg_differs_from_HVC1=sorted(k for k in set(b1['cfg']) | set(bc) if b1['cfg'].get(k) != bc.get(k)), targets_identical_to_HVC1=b1['cfg']['targets'] == bc['targets'])
res['envelope'] = dict(central_cm=[152, 213], HV152N_NAT=M['HV152N-NAT']['stature'], HVC1=M['HVC1']['stature'], HVF178=M['HVF178']['stature'], HV213M=M['HV213M']['stature'], inside=bool(152 <= M['HVF178']['stature'] <= 213))
if os.path.exists(PA + '/regen/HVF178_native.npz'): res['native_integrity'] = integrity(PA + '/regen/HVF178_native.npz')
json.dump(res, open(OUT, 'w'), indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
for cfg, r in res['configs'].items():
    print(cfg, 'nearest', r['nearest_source_count'], '| material vs', {s: '%d/%d' % (x['material_metrics'], x['of']) for s, x in r['source_protection'].items()}, '| rms%', {s: x['rms_pct'] for s, x in r['source_protection'].items()})
    for p, a in r['arithmetic_average_audit'].items(): print('  ', p, a['metrics_with_material_gap'], 't med', a['t_median'], a['t_iqr'], 'mid', a['near_midpoint_0p35_0p65'], 'humanend', a['near_human_end_abs_t_le_0p15'], 'outside', a['outside_pair_t_lt0_or_gt1'], a['scalar_blend_fit'])
print('consistency', res['configuration_consistency']['same_sign'], res['configuration_consistency']['within_human_pattern'], '/', res['configuration_consistency']['of'], '| det', res['determinism'], '| env', res['envelope'])
