# hv_ear_collect.py EVIDIR : Halvren central-accept + mixed-ear order -- collect the ear records into the evidence folder:
#   HV_ear_summary.json    technical + one-auricle record of HE1 / HE2 / HE3 (c1, c2), the four diagnostics, the mosaic pair, the frozen-elf references on
#                          the common head, and the TOPOLOGY AUDIT matrix (stress bounds and HE1-3 on the rigid Fenn v002 cuff / exact Vael RI3 root geometry /
#                          Halvren HR1 root geometry; rest-state-only exploration builds); body / face / pelvis regression (outside-branch identity)
#   HV_ear_domains.json    measured ear-domain coordinates (MF, FN, AE, VA, HE1-3, diagnostics) on the common c1 head
#   determinism            independent rebuild of HE2 (c1, c2) vs the guarded realization
import sys, os, json, glob, subprocess, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import hv_ear_summary as S; import hv_ear_domains as D
EV = sys.argv[1]; os.makedirs(EV, exist_ok=True); EW = '/tmp/claude-0/rt/hv/ear'; jl = lambda p: json.load(open(p)); HP = '/tmp/claude-0/rt/hv/hpe'
H1, H2 = 'HVC1-HB2HF2-HPB', 'HVF178-HB2HF2-HPB'; HEADS = {'c1': H1, 'c2': H2}
R = dict(order='chatgpt-rac-rp3-halvren-central-accept-ear-architecture-order', items={}, topology_audit={}, regression={})
for c, h in HEADS.items():
    for k in ('HE1', 'HE2', 'HE3'): R['items']['%s %s' % (k, c)] = S.summ(EW + '/he', k, h)
for k in ('HV-DFN', 'HV-DAE', 'HV-DVA', 'HV-DHU'): R['items']['%s c1' % k] = S.summ(EW + '/he', k, H1)
R['items']['HE3 on HB2HF1 c1'] = S.summ(EW + '/mos', 'HE3', 'HVC1-HB2HF1-HPB'); R['items']['HE1 on HB2HF3 c1'] = S.summ(EW + '/mos', 'HE1', 'HVC1-HB2HF3-HPB')
for lab, w, k in (('frozen Fenn E2', 'ref/FN', 'E2'), ('frozen Aelari AE-E2', 'ref/FN', 'AE-E2'), ('frozen Vael VA-E2-RI3', 'ref/RI3', 'VA-E2-RI3')): R['items']['%s on Halvren c1' % lab] = S.summ('%s/%s' % (EW, w), k, H1)
TA = R['topology_audit']
TA['guarded'] = {}
for lab, w, k in (('Marchfolk-proportion bound / Fenn v002 rigid cuff', 'topo/FN', 'HVT-HUM-R'), ('Marchfolk-proportion bound / Vael RI3 root geometry', 'topo/RI3', 'HVT-HUM-S'),
                  ('elf-forward bound / Fenn v002 rigid cuff', 'topo/FN', 'HVT-ELF-R'), ('elf-forward bound / Vael RI3 root geometry', 'topo/RI3', 'HVT-ELF-S'),
                  ('HE1 / Fenn v002 rigid cuff', 'topo/FN', 'HE1-R'), ('HE2 / Fenn v002 rigid cuff', 'topo/FN', 'HE2-R'), ('HE3 / Fenn v002 rigid cuff', 'topo/FN', 'HE3-R'),
                  ('HE1 / Vael RI3 root geometry', 'topo/RI3', 'HE1-V'), ('HE2 / Vael RI3 root geometry', 'topo/RI3', 'HE2-V'), ('HE3 / Vael RI3 root geometry', 'topo/RI3', 'HE3-V'),
                  ('HE1 / Halvren HR1 root geometry', 'he', 'HE1'), ('HE2 / Halvren HR1 root geometry', 'he', 'HE2'), ('HE3 / Halvren HR1 root geometry', 'he', 'HE3')):
    x = S.summ('%s/%s' % (EW, w), k, H1); TA['guarded'][lab] = dict(cand=k, technical_pass=x['technical_pass'], failed=[g for g, v in x['gates'].items() if not v], one_auricle_metrics_pass=x['one_auricle_metrics_pass'],
                                                                    T4=x['T4'], T4_cuff=x['T4_by_part'].get('cuff'), min_angle=round(x['min_angle'], 1), aspect_max=round(x['aspect_max'], 2), branch_selfx=x['integrity']['branch_selfx'],
                                                                    anterior_cuff_mound_p90_cm=round(x['root_concha']['anterior_cuff_mound_p90_cm'], 3), junction_anterior_cm=round(x['root_concha']['junction_anterior_height_mean_cm'], 3),
                                                                    length_over_HH=round(x['measure']['length_over_HH'], 3))
TA['rest_state_exploration'] = {}
for n, lab in (('b4', 'HE1 at L 6.2 (near-human length) / HR1'), ('c5', 'Marchfolk-proportion bound with the Halvren root attachment (tauA 10, phi0 30) / HR1'), ('b6', 'elf-forward bound (L 9.4, proj 42) / HR1'),
               ('e1L62', 'HE1 at L 6.2 / HR1 without the lobe lift'), ('k12', 'HE1 / RI3 + corner fade 1.2 only'), ('e1c7', 'HE1 / concha seat -0.70 (too deep)')):
    a = '%s/x/p_%s/a.json' % (EW, n)
    if os.path.exists(a):
        A = jl(a); TA['rest_state_exploration'][lab] = dict(min_angle=round(A['T4']['min_angle'], 1), aspect_max=round(A['T4']['aspect_max'], 2), branch_selfx=A['self_intersection_pairs_touching_branch'], T4=A['T4']['angle_violations'],
                                                             clean=bool(A['T4']['min_angle'] >= 10 and A['T4']['aspect_max'] < 10 and A['self_intersection_pairs_touching_branch'] == 0))
# regression: outside-branch identity vs the family realization, every HE item
for lab, x in R['items'].items():
    if lab.startswith('HE'): R['regression'][lab] = x['outside_identical']
# determinism: independent rebuild of HE2 with the recorded guard set
det = {}
for c, h in HEADS.items():
    d = EW + '/det_' + c; os.makedirs(d, exist_ok=True); g = '%s/he/build/%s_HE2_deform_guard.json' % (EW, h)
    env = dict(os.environ, EAR_CF=HP, EAR_TOPO='v002', EAR_UNT_MODE='contacts', EAR_Q3_FREEZE=g, EAR_Q3_FREEZE_RINGS=str(json.load(open('%s/he/build/%s_HE2_deform_guard_log.json' % (EW, h)))[-1]['iteration'] >= 2 and 2 or 1))
    subprocess.run(['/home/claude/stc/bin/python3', '/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001/ear_build.py', h, 'HE2', d, '--canon', EW + '/he/canon_branch_topology.json'], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    a = np.load('%s/he/build/%s_HE2_branch.npz' % (EW, h)); b = np.load('%s/%s_HE2_branch.npz' % (d, h)); det[c] = dict(max_abs_dV_cm=float(np.abs(a['V'] - b['V']).max()), faces_identical=bool(np.array_equal(a['Q'], b['Q'])))
R['determinism_HE2'] = det
R['face_topology_identical_HE_c1_c2'] = len({R['items']['%s %s' % (k, c)]['face_topology_sha256'] for k in ('HE1', 'HE2', 'HE3') for c in HEADS} | {R['items'][k]['face_topology_sha256'] for k in R['items'] if k.startswith('HV-D')}) == 1
json.dump(R, open(EV + '/HV_ear_summary.json', 'w'), indent=1)
items = ['MF:fam:%s/fam/%s_fam.npz:%s' % (HP, H1, H1), 'FN:branch:%s/ref/FN/build/%s_E2_branch.npz:%s' % (EW, H1, H1), 'AE:branch:%s/ref/FN/build/%s_AE-E2_branch.npz:%s' % (EW, H1, H1),
         'VA:branch:%s/ref/RI3/build/%s_VA-E2-RI3_branch.npz:%s' % (EW, H1, H1)] + ['%s:branch:%s/he/build/%s_%s_branch.npz:%s' % (k, EW, H1, k, H1) for k in ('HE1', 'HE2', 'HE3', 'HV-DFN', 'HV-DAE', 'HV-DVA', 'HV-DHU')] \
        + ['CTRL-%s:branch:%s/topo/%s/build/%s_HVT-%s_branch.npz:%s' % (k, EW, w, H1, k, H1) for k, w in (('HUM-R', 'FN'), ('HUM-S', 'RI3'), ('ELF-R', 'FN'), ('ELF-S', 'RI3'))]
subprocess.run(['python3', os.path.dirname(os.path.abspath(__file__)) + '/hv_ear_domains.py', EV + '/HV_ear_domains.json'] + items, check=True)
for lab, x in R['items'].items(): print(lab, 'TECH', x['technical_pass'], [g for g, v in x['gates'].items() if not v], 'one-auricle', x['one_auricle_metrics_pass'], 'outside identical', x['outside_identical'])
print(json.dumps(TA, indent=0)[:3000]); print('det', det, 'topo identical', R['face_topology_identical_HE_c1_c2'])
