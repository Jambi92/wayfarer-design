# hv_hpb_validation.py OUT.json : Halvren central-accept order §5 / §6 -- HP-B validation of the versioned accepted-source candidates HVC1-HB2HF2-HPB /
# HVF178-HB2HF2-HPB before ear work: source integrity + determinism (independent hv_defs build vs the body / face order HP-B diagnostic build), skeletal
# proxy pelvic relations (build_hp.sh lean builds; identical geometry, dV 0), matched-stature source comparisons (hv_eval.py: body identity vs MF, scalar-
# blend firewall, distinct from elves, face departure, anti-beauty) vs the pelvis-held HB2HF2, v005 family propagation + D1-D6 + anatomy + contact +
# 18-pose deformation (hv_bf_technical.py) vs HB2HF2. Stop rule (§6): any coupled failure -> stop before ears.
import sys, json, numpy as np
OUT = sys.argv[1]; W = '/tmp/claude-0/rt/hv'; jl = lambda p: json.load(open(p))
TB = jl(W + '/hbe/HV_bf_technical.json'); TP = jl(W + '/hpe/HV_hpb_technical.json'); PK = jl(W + '/hp/HV_pelvis_package.json')
R = dict(order='chatgpt-rac-rp3-halvren-central-accept-ear-architecture-order §5 / §6', sources={}, verdict={})
for c, pre in (('c1', 'HVC1'), ('c2', 'HVF178')):
    i = pre + '-HB2HF2-HPB'; a = np.load('%s/hb/cand/%s_r6.npz' % (W, i)); b = np.load('%s/hp/cand/%s_r6.npz' % (W, i))
    ev = jl('%s/hpv/HPB_eval_%s.json' % (W, c))['items']; e0 = ev['HB2HF2']['body']; e1 = ev['HB2HF2-HPB']['body']; f0 = ev['HB2HF2']['face']; f1 = ev['HB2HF2-HPB']['face']
    t0 = TB[pre + '-HB2HF2']; t1 = TP[i]; sk = PK['hp']['HP-B %s' % c]['skeletal_proxy']
    rel = {k: sk[k]['0.5'] for k in ('pelvic_vertical_over_crest', 'crest_share', 'pelvic_depth_share', 'bitroch_over_crest', 'pelvic_vertical_share', 'leg_share')}
    R['sources'][i] = dict(
        determinism=dict(vs_body_face_order_HPB_diagnostic_max_abs_dV_cm=float(np.abs(a['V'].astype(float) - b['V'].astype(float)).max()), faces_identical=bool(np.array_equal(a['F'], b['F']))),
        skeletal_proxy_t05=rel, hip_joint_height_leg_share_vs_MF_pct=sk['leg_share']['0.5']['vs_MF_pct'],
        body=dict(material_vs={s: (e0['source_protection'][s]['material'], e1['source_protection'][s]['material']) for s in e1['source_protection']}, groups_with_signal_vs_MF=(e0['groups_with_signal_vs_MF'], e1['groups_with_signal_vs_MF']),
                  scalar_blend=(e0['scalar_blend_firewall'], e1['scalar_blend_firewall']), distinct_from_elves=e1['distinct_from_elves']),
        face=dict(regions_departing_MF=(f0.get('regions_departing_from_MF'), f1.get('regions_departing_from_MF')), anti_beauty_vs_MF_pct=f1.get('anti_beauty_indicators_vs_MF_pct')),
        technical=dict(pass_HB2HF2=t0['technical_pass'], pass_HPB=t1['technical_pass'], validator=t1['validator'], stations=t1['stations'], density_max_over_limit=t1['density_max_over_limit'],
                       worst_flip_excess=(t0['worst_flip_excess'], t1['worst_flip_excess']), worst_selfx_excess=(t0['worst_selfx_excess'], t1['worst_selfx_excess']), contact=t1['contact'],
                       hip_knee_poses_selfx={p: (t0['poses'][p]['selfx'], t1['poses'][p]['selfx'], t1['poses'][p]['selfx_mf']) for p in ('hip_flex90_l', 'knee_90_l', 'knee_140_l', 'trunk_twist30')},
                       hip_knee_poses_flips={p: (t0['poses'][p]['flips'], t1['poses'][p]['flips'], t1['poses'][p]['flips_mf']) for p in ('hip_flex90_l', 'knee_90_l', 'knee_140_l', 'trunk_twist30')},
                       integrity=t1['integrity'], regen=t1['regen'], anatomy=t1['anatomy']),
        note='tuples are (HB2HF2 pelvis held = HP-A, HB2HF2-HPB)')
    s = R['sources'][i]
    R['verdict'][i] = dict(deterministic=s['determinism']['vs_body_face_order_HPB_diagnostic_max_abs_dV_cm'] == 0 and s['determinism']['faces_identical'],
                           body_identity_kept=e1['source_protection']['MF']['material'] >= e0['source_protection']['MF']['material'] and e1['groups_with_signal_vs_MF'] >= e0['groups_with_signal_vs_MF'],
                           no_new_hip_leg_problem=t1['technical_pass'] and abs(sk['leg_share']['0.5']['vs_MF_pct']) < 1.0 and all(t1['poses'][p]['flips'] <= t0['poses'][p]['flips'] + 2 for p in ('hip_flex90_l', 'knee_90_l', 'knee_140_l')),
                           not_elf_duplicate=all(e1['distinct_from_elves'].values()), scalar_blend_firewall_pass=e1['scalar_blend_firewall']['passes'], technical_pass=t1['technical_pass'])
R['all_pass'] = all(all(v.values()) for v in R['verdict'].values())
json.dump(R, open(OUT, 'w'), indent=1); print(json.dumps(R['verdict'], indent=0), R['all_pass'])
