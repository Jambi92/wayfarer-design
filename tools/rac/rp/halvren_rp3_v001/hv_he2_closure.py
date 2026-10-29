# hv_he2_closure.py EVIDIR : Halvren HE2 closure order -- consolidated record HE2_closure_record.json:
#   technical / one-auricle summaries of the corrected family (he3: HE1 / HE2 / HE3, c1 / c2) and of the corrected HE2 on the rigid Fenn cuff / exact Vael RI3
#   root (topo3); measured ear domains (common c1 head; MF, FN, AE, VA, HE1, HE2, HE3, HE2-before = HVEAR2) and the measured-domain arithmetic firewall per
#   item with the domains driving each fit; HE3 re-check; HE1 size-floor evidence; HE2 determinism (independent rebuild with the recorded guard set,
#   incl. the cuff repair); outside-branch identity (body / face / pelvis regression).
import sys, os, json, subprocess, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import hv_ear_summary as S; import hv_ear_domains as D
EV = sys.argv[1]; os.makedirs(EV, exist_ok=True); E = '/tmp/claude-0/rt/hv/ear'; HP = '/tmp/claude-0/rt/hv/hpe'; jl = lambda p: json.load(open(p)); H = {'c1': 'HVC1-HB2HF2-HPB', 'c2': 'HVF178-HB2HF2-HPB'}
R = dict(order='chatgpt-rac-rp3-halvren-he2-realization-ear-architecture-closure-order', technical={}, topology_audit={}, domains={}, firewall={})
def tech(x): return dict(technical_pass=x['technical_pass'], failed=[g for g, v in x['gates'].items() if not v], min_angle=round(x['min_angle'], 1), aspect_max=round(x['aspect_max'], 2), T4=x['T4'],
                         branch_selfx=x['integrity']['branch_selfx'], density_pct=round(x['density_pct'], 3), root_valence=x['root_valence'], mound_p90_cm=round(x['root_concha']['anterior_cuff_mound_p90_cm'], 3),
                         junction_cm=round(x['root_concha']['junction_anterior_height_mean_cm'], 3), concha_floor_cm=round(x['root_concha']['concha_floor_min_vs_skin_cm'], 2), clearance_min_cm=round(x['clearance_min_cm'], 2),
                         poses=x['poses'], guard_iterations=len(x['guard'] or []) - 1, outside_identical=x['outside_identical'], faces_sha=x['face_topology_sha256'], one_auricle_metrics_pass=x['one_auricle_metrics_pass'],
                         length_over_HH_measure=round(x['measure']['length_over_HH'], 3))
for c, h in H.items():
    for k in ('HE1', 'HE2', 'HE3'):
        x = S.summ(E + '/he3', k, h); R['technical']['%s %s' % (k, c)] = tech(x)
        rp = '%s/he3/build/%s_%s_repair.log' % (E, h, k); R['technical']['%s %s' % (k, c)]['cuff_repair'] = json.load(open(h and '%s/he3/build/%s_%s_branch.json' % (E, h, k))).get('hv_cuff_repair')
for lab, w, k in (('HE2 rigid', 'topo3/FN', 'HE2-R'), ('HE2 RI3', 'topo3/RI3', 'HE2-V')): R['topology_audit'][lab] = tech(S.summ('%s/%s' % (E, w), k, H['c1']))
R['topology_audit']['HE2'] = R['technical']['HE2 c1']
SRC = {'MF': ('fam', '%s/fam/%s_fam.npz' % (HP, H['c1'])), 'FN': ('branch', '%s/ref/FN/build/%s_E2_branch.npz' % (E, H['c1'])), 'AE': ('branch', '%s/ref/FN/build/%s_AE-E2_branch.npz' % (E, H['c1'])),
       'VA': ('branch', '%s/ref/RI3/build/%s_VA-E2-RI3_branch.npz' % (E, H['c1'])), 'HE2-before': ('branch', '%s/he/build/%s_HE2_branch.npz' % (E, H['c1']))}
for k in ('HE1', 'HE2', 'HE3'): SRC[k] = ('branch', '%s/he3/build/%s_%s_branch.npz' % (E, H['c1'], k))
M = {k: D.measure(kind, p, H['c1']) for k, (kind, p) in SRC.items()}; DOM = D.DOM; R['domain_list'] = DOM
X = {k: np.array([M[k][q] for q in DOM]) for k in M}; sd = np.maximum(np.array([X[s] for s in ('MF', 'FN', 'AE', 'VA')]).std(0), [D.FLOOR[q] for q in DOM]); em = np.mean([X[e] for e in ('FN', 'AE', 'VA')], 0)
for k in M: R['domains'][k] = dict(values={q: round(float(v), 4) for q, v in zip(DOM, X[k])}, t={q: round(float(v), 3) for q, v in zip(DOM, (X[k] - X['MF']) / np.where(np.abs(em - X['MF']) > 1e-9, em - X['MF'], 1))})
for k in ('HE2-before', 'HE1', 'HE2', 'HE3'):
    pr = {}
    for e in ('FN', 'AE', 'VA'):
        dx = (X[e] - X['MF']) / sd; y = (X[k] - X['MF']) / sd; m = np.abs(dx) > 0.5; a = float(dx[m] @ y[m] / (dx[m] @ dx[m])); r = y[m] - a * dx[m]; r2 = float(1 - r @ r / (y[m] @ y[m]))
        drv = sorted(zip(np.array(DOM)[m], a * dx[m] * y[m]), key=lambda z_: -z_[1])[:4]          # domains carrying the fitted alpha (largest alpha x dx x y terms)
        pr['MF-' + e] = dict(n=int(m.sum()), r2=round(r2, 3), alpha=round(a, 3), passes=bool(not (r2 >= 0.8 and m.sum() >= 6)), driving_domains=[d_ for d_, _ in drv],
                             t={q: round(float(v), 2) for q, v in zip(np.array(DOM)[m], (X[k] - X['MF'])[m] / (X[e] - X['MF'])[m])})
    best = max(pr, key=lambda p_: pr[p_]['r2']); R['firewall'][k] = dict(pairs=pr, best_pair=best, best_r2=pr[best]['r2'], passes=all(v['passes'] for v in pr.values()),
                                                                          distinct_domains_vs={e: int(np.sum(np.abs((X[k] - X[e]) / sd) > 0.5)) for e in ('MF', 'FN', 'AE', 'VA')})
emc = lambda k: float(np.mean([R['domains'][k]['t'][q] for q in DOM if abs(em[DOM.index(q)] - X['MF'][DOM.index(q)]) > 0.5 * sd[DOM.index(q)]]))
R['family'] = dict(composite_elfward={k: round(emc(k), 3) for k in ('HE1', 'HE2', 'HE3')}); c_ = R['family']['composite_elfward']; R['family']['order_ok'] = bool(c_['HE1'] < c_['HE2'] < c_['HE3'])
P3 = np.array([X[k] for k in ('HE1', 'HE2', 'HE3')]); R['family']['non_monotone_domains'] = [q for i, q in enumerate(DOM) if not ((P3[0, i] <= P3[1, i] <= P3[2, i]) or (P3[0, i] >= P3[1, i] >= P3[2, i]))]
ex = lambda n: jl('%s/x/p_%s/a.json' % (E, n)) if os.path.exists('%s/x/p_%s/a.json' % (E, n)) else None
fl = {}
for n, L in (('e1L58', 5.8), ('b4', 6.2), ('f63', 6.3), ('f65', 6.5)):
    a = ex(n)
    if a: fl['L %.1f' % L] = dict(min_angle=round(a['T4']['min_angle'], 1), aspect=round(a['T4']['aspect_max'], 2), selfx=a['self_intersection_pairs_touching_branch'], clean=bool(a['T4']['min_angle'] >= 10 and a['T4']['aspect_max'] < 10 and a['self_intersection_pairs_touching_branch'] == 0))
R['HE1_size_floor'] = dict(rest_state_length_sweep=fl, HE1_measured_length_over_HH=R['domains']['HE1']['values']['length_over_HH'], Marchfolk_measured=R['domains']['MF']['values']['length_over_HH'],
                           Marchfolk_parameter_control_on_topology=jl(EV + '/../ear/HV_ear_domains.json')['items'].get('CTRL-HUM-R', {}).get('length_over_HH') if os.path.exists(EV + '/../ear/HV_ear_domains.json') else None)
det = {}
for c, h in H.items():
    d = '%s/det3_%s' % (E, c); os.makedirs(d, exist_ok=True); g = '%s/he3/build/%s_HE2_deform_guard.json' % (E, h); lg = jl('%s/he3/build/%s_HE2_deform_guard_log.json' % (E, h))
    env = dict(os.environ, EAR_CF=HP, EAR_TOPO='v002', EAR_UNT_MODE='contacts', EAR_Q3_FREEZE=g, EAR_Q3_FREEZE_RINGS=str(2 if lg[-1]['iteration'] >= 2 else 1))
    subprocess.run(['/home/claude/stc/bin/python3', '/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001/ear_build.py', h, 'HE2', d, '--canon', E + '/he3/canon_branch_topology.json'], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['python3', os.path.dirname(os.path.abspath(__file__)) + '/hv_cuff_repair.py', '%s/%s_HE2_branch.npz' % (d, h), h], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    a = np.load('%s/he3/build/%s_HE2_branch.npz' % (E, h)); b_ = np.load('%s/%s_HE2_branch.npz' % (d, h)); det[c] = dict(max_abs_dV_cm=float(np.abs(a['V'] - b_['V']).max()), faces_identical=bool(np.array_equal(a['Q'], b_['Q'])))
R['determinism_HE2'] = det
json.dump(R, open(EV + '/HE2_closure_record.json', 'w'), indent=1)
for k, v in R['technical'].items(): print(k, v['technical_pass'], v['failed'], 'min %.1f asp %.2f mound %.2f junc %.2f guard %d' % (v['min_angle'], v['aspect_max'], v['mound_p90_cm'], v['junction_cm'], v['guard_iterations']))
for k, v in R['topology_audit'].items(): print('TOPO', k, v['technical_pass'], v['failed'], v['mound_p90_cm'])
for k, v in R['firewall'].items(): print('FW', k, {p: (x['n'], x['r2'], x['alpha']) for p, x in v['pairs'].items()}, v['distinct_domains_vs'])
print(R['family'], R['HE1_size_floor'], det)
