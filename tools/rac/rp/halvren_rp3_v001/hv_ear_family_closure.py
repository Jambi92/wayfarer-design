# hv_ear_family_closure.py EVIDIR : Halvren ear family closure order (after HR2) -- consolidated record HV_ear_family_closure_record.json:
#   HE2 + HR2 freeze read-back (frozen ee0e98c realizations vs the final-code rebuild); technical regression of the final family (fam6: HE1 HVEAR4 L 5.6,
#   frozen HE2, HE3 HVEAR4; c1 / c2; guarded Halvren path) next to HE3-before (HVEAR3 on HR2) and HE1-HVEAR3 (L 6.3) and the HE1 L 5.3 edge build;
#   HE3 firewall decomposition (R2 / alpha / n / residual per domain / driving domains) before / after for MF<->FN / AE / VA; measured domains; family
#   composite / ordering / non-monotone domains; distinctness counts; HR2 secondary-silhouette measures; HE1 size sweep (shared layout; human-scale layout
#   metric) and HE3 calibration trials; determinism (HE1 / HE3 c1 / c2 rebuild with the recorded guard sets + repair); frozen-ear rebuild identity.
import sys, os, json, glob, subprocess, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import hv_ear_summary as S; import hv_ear_domains as D; import hv_root_sectors as RS
EV = sys.argv[1]; os.makedirs(EV, exist_ok=True); E = '/tmp/claude-0/rt/hv/ear'; HP = '/tmp/claude-0/rt/hv/hpe'; jl = lambda p: json.load(open(p))
H = {'c1': 'HVC1-HB2HF2-HPB', 'c2': 'HVF178-HB2HF2-HPB'}; T = '/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001'; BP = '/home/claude/stc/bin/python3'
R = dict(order='chatgpt-rac-rp3-halvren-ear-family-closure-after-hr2-order', technical={}, silhouette={}, domains={}, firewall={}, decomposition={})
fr = {}
for c, h in H.items():
    a = np.load('%s/hr2f/build/%s_HE2_branch.npz' % (E, h)); b = np.load('%s/fam6/build/%s_HE2_branch.npz' % (E, h))
    fr[c] = dict(max_abs_dV_cm=float(np.abs(a['V'] - b['V']).max()), faces_identical=bool(np.array_equal(a['Q'], b['Q'])))
R['HE2_freeze_readback'] = fr
def tech(x): return dict(technical_pass=x['technical_pass'], failed=[g for g, v in x['gates'].items() if not v], components=x['integrity']['components'], boundary=x['integrity']['boundary'],
                         nonmanifold=x['integrity']['nonmanifold'], degenerate=x['integrity']['degenerate'], outward=x['integrity']['outward'], branch_selfx=x['integrity']['branch_selfx'],
                         min_angle=round(x['min_angle'], 1), aspect_max=round(x['aspect_max'], 3), T4=x['T4'], density_pct=round(x['density_pct'], 3), root_valence=x['root_valence'],
                         root_valence_ok=all(v == {'4': 52} for v in x['root_valence'].values()), mound_p90_cm=round(x['root_concha']['anterior_cuff_mound_p90_cm'], 3),
                         junction_cm=round(x['root_concha']['junction_anterior_height_mean_cm'], 3), clearance_min_cm=round(x['clearance_min_cm'], 2), poses=x['poses'], poses_clean=x['gates']['poses_clean'],
                         guard_log=x['guard'], guard_iterations=len(x['guard'] or []) - 1, faces_sha=x['face_topology_sha256'], length_over_HH_measure=round(x['measure']['length_over_HH'], 3))
ITEMS = {}
for c, h in H.items():
    for k in ('HE1', 'HE2', 'HE3'): ITEMS['%s %s' % (k, c)] = ('fam6', k, h)
    ITEMS['HE3-before %s' % c] = ('hr2f', 'HE3', h); ITEMS['HE1-HVEAR3 %s' % c] = ('hr2f', 'HE1', h); ITEMS['HE1-L5.3 %s' % c] = ('he1L53', 'HE1', h); ITEMS['HE1-L5.6size %s' % c] = ('he1L56', 'HE1', h)
for lab, (w, k, h) in ITEMS.items():
    R['technical'][lab] = tech(S.summ('%s/%s' % (E, w), k, h)); R['technical'][lab]['repair'] = jl('%s/%s/build/%s_%s_branch.json' % (E, w, h, k)).get('hv_cuff_repair')
    if lab.split()[0] in ('HE1', 'HE3', 'HE3-before', 'HE2'):
        s_ = RS.sectors('%s/%s/build/%s_%s_branch.npz' % (E, w, h, k), h); R['silhouette'][lab] = {q: s_['l'][q] for q in ('pedestal_vs_true_head', 'loop_crease_deg', 'inferior_fork')}
SRC = {'MF': ('fam', '%s/fam/%s_fam.npz' % (HP, H['c1'])), 'FN': ('branch', '%s/ref/FN/build/%s_E2_branch.npz' % (E, H['c1'])), 'AE': ('branch', '%s/ref/FN/build/%s_AE-E2_branch.npz' % (E, H['c1'])),
       'VA': ('branch', '%s/ref/RI3/build/%s_VA-E2-RI3_branch.npz' % (E, H['c1']))}
for lab, (w, k, h) in ITEMS.items():
    if h == H['c1']: SRC[lab.replace(' c1', '')] = ('branch', '%s/%s/build/%s_%s_branch.npz' % (E, w, h, k))
SRC['HE3 c2'] = ('branch', '%s/fam6/build/%s_HE3_branch.npz' % (E, H['c2'])); SRC['HE1 c2'] = ('branch', '%s/fam6/build/%s_HE1_branch.npz' % (E, H['c2']))
M = {k: D.measure(kind, p, H['c2'] if k.endswith(' c2') else H['c1']) for k, (kind, p) in SRC.items()}; DOM = D.DOM; R['domain_list'] = DOM
X = {k: np.array([M[k][q] for q in DOM]) for k in M}; sd = np.maximum(np.array([X[s] for s in ('MF', 'FN', 'AE', 'VA')]).std(0), [D.FLOOR[q] for q in DOM]); em = np.mean([X[e] for e in ('FN', 'AE', 'VA')], 0)
for k in M: R['domains'][k] = dict(values={q: round(float(v), 4) for q, v in zip(DOM, X[k])}, t={q: round(float(v), 3) for q, v in zip(DOM, (X[k] - X['MF']) / np.where(np.abs(em - X['MF']) > 1e-9, em - X['MF'], 1))})
for k in [q for q in M if q not in ('MF', 'FN', 'AE', 'VA')]:
    pr = {}
    for e in ('FN', 'AE', 'VA'):
        dx = (X[e] - X['MF']) / sd; y = (X[k] - X['MF']) / sd; m = np.abs(dx) > 0.5; a = float(dx[m] @ y[m] / (dx[m] @ dx[m])); r = y[m] - a * dx[m]; r2 = float(1 - r @ r / (y[m] @ y[m]))
        drv = sorted(zip(np.array(DOM)[m], a * dx[m] * y[m]), key=lambda z_: -z_[1])[:4]
        pr['MF-' + e] = dict(n=int(m.sum()), r2=round(r2, 3), alpha=round(a, 3), passes=bool(not (r2 >= 0.8 and m.sum() >= 6)), driving_domains=[d_ for d_, _ in drv])
        if k in ('HE3', 'HE3-before'):
            R['decomposition'].setdefault(k, {})['MF-' + e] = dict(n=int(m.sum()), r2=round(r2, 3), alpha=round(a, 3), domains={q: dict(y_sd=round(float(yy), 2), elf_dx_sd=round(float(dd), 2), fit=round(float(a * dd), 2), residual=round(float(rr), 2), fit_share=round(float(a * dd * yy / (y[m] @ y[m])), 3))
                                                                                                                      for q, yy, dd, rr in zip(np.array(DOM)[m], y[m], dx[m], r)}, driving_domains=[d_ for d_, _ in drv])
    best = max(pr, key=lambda p_: pr[p_]['r2']); R['firewall'][k] = dict(pairs=pr, best_pair=best, best_r2=pr[best]['r2'], passes=all(v['passes'] for v in pr.values()),
                                                                        distinct_domains_vs={e: int(np.sum(np.abs((X[k] - X[e]) / sd) > 0.5)) for e in ('MF', 'FN', 'AE', 'VA', 'HE2') if e in X})
cm = np.abs(em - X['MF']) > 0.5 * sd; comp = lambda k: round(float(np.mean(((X[k] - X['MF']) / (em - X['MF']))[cm])), 3)
R['family'] = dict(composite_domains=list(np.array(DOM)[cm]), composite_elfward={k: comp(k) for k in ('HE1', 'HE2', 'HE3', 'HE3-before', 'HE1-HVEAR3', 'HE1-L5.3', 'HE1-L5.6size')})
c_ = R['family']['composite_elfward']; R['family']['order_ok'] = bool(c_['HE1'] < c_['HE2'] < c_['HE3'])
P3 = np.array([X[k] for k in ('HE1', 'HE2', 'HE3')]); R['family']['non_monotone_domains'] = [q for i, q in enumerate(DOM) if not ((P3[0, i] <= P3[1, i] <= P3[2, i]) or (P3[0, i] >= P3[1, i] >= P3[2, i]))]
R['family']['HE1_length_vs_MF_pct'] = {k: round(100 * (X[k][0] / X['MF'][0] - 1), 1) for k in ('HE1', 'HE1-HVEAR3', 'HE1-L5.3', 'HE1-L5.6size', 'HE2', 'HE3')}
tr = lambda pat: [dict(name=t['name'], probe=t['probe'], tech=t['tech'], firewall={k: v['r2'] for k, v in t['firewall'].items()}, length_over_HH=t['domains']['length_over_HH'],
                       composite=round(float(np.mean(((np.array([t['domains'][q] for q in DOM]) - X['MF']) / (em - X['MF']))[cm])), 3)) for t in map(jl, sorted(glob.glob(pat)))]
R['HE3_trials'] = tr('%s/he3c/*/try.json' % E) + [t for t in tr('%s/he3d/*/try.json' % E) if t['name'][0] not in 'kn'] + tr('%s/he3e/*/try.json' % E); R['HE1_size_trials'] = tr('%s/he1s/*/try.json' % E); R['HE1_identity_trials'] = [t for t in tr('%s/he3d/*/try.json' % E) if t['name'][0] in 'kn'] + tr('%s/he1t/*/try.json' % E) + tr('%s/he1u/*/try.json' % E) + tr('%s/he1v/*/try.json' % E)
R['HE1_size_trials_note'] = ('L*: shared E2-metric layout (no sheet stretch repair at trial time); H*: human-scale layout metric EAR_LAYOUT_METRIC=HE1-HS (same connectivity); C*: length-scaled concha seat; '
                             'stage-3 sheet stretch repair applied afterwards to copies RL50 / RL53 / RL56 (aspect 9.99 / 9.97 / 9.94); guarded builds HE1-L5.6size and HE1-L5.3 (HVEAR3 body, edge) in technical; he3d / k* / n* = family-identity trials after the blind review; he1u T* / U* = HE1 human-outline trials after blind review round 3 (U3 selected); he1v V* = round-4 rim-to-lobe polish (V3 selected: lobe 0.24, helix roll 0.38)')
det = {}
for c, h in H.items():
    for k in ('HE1', 'HE3'):
        d = '%s/det_fam_%s_%s' % (E, k, c); os.makedirs(d, exist_ok=True); g = '%s/fam6/build/%s_%s_deform_guard.json' % (E, h, k); lg = jl('%s/fam6/build/%s_%s_deform_guard_log.json' % (E, h, k))
        env = dict(os.environ, EAR_CF=HP, EAR_TOPO='v002', EAR_UNT_MODE='contacts', EAR_Q3_FREEZE=g, EAR_Q3_FREEZE_RINGS=str(2 if lg[-1]['iteration'] >= 2 else 1))
        subprocess.run([BP, T + '/ear_build.py', h, k, d, '--canon', E + '/fam6/canon_branch_topology.json'], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(['python3', os.path.dirname(os.path.abspath(__file__)) + '/hv_cuff_repair.py', '%s/%s_%s_branch.npz' % (d, h, k), h], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        a = np.load('%s/fam6/build/%s_%s_branch.npz' % (E, h, k)); b_ = np.load('%s/%s_%s_branch.npz' % (d, h, k)); det['%s %s' % (k, c)] = dict(max_abs_dV_cm=float(np.abs(a['V'] - b_['V']).max()), faces_identical=bool(np.array_equal(a['Q'], b_['Q'])))
R['determinism'] = det
frz = {}
for lab, w, k in (('Fenn E2', 'ref/FN', 'E2'), ('Aelari AE-E2', 'ref/FN', 'AE-E2'), ('Vael VA-E2-RI3', 'ref/RI3', 'VA-E2-RI3')):
    d = '%s/frz_fam/%s' % (E, k); os.makedirs(d, exist_ok=True); g = '%s/%s/build/%s_%s_deform_guard.json' % (E, w, H['c1'], k); lg = jl(g.replace('.json', '_log.json'))
    env = dict(os.environ, EAR_CF=HP, EAR_TOPO='v002', EAR_UNT_MODE='contacts', EAR_Q3_FREEZE=g, EAR_Q3_FREEZE_RINGS=str(2 if lg[-1]['iteration'] >= 2 else 1))
    subprocess.run([BP, T + '/ear_build.py', H['c1'], k, d, '--canon', '%s/%s/canon_branch_topology.json' % (E, w)], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    a = np.load('%s/%s/build/%s_%s_branch.npz' % (E, w, H['c1'], k)); b_ = np.load('%s/%s_%s_branch.npz' % (d, H['c1'], k))
    frz[lab] = dict(max_abs_dV_cm=float(np.abs(a['V'] - b_['V']).max()), faces_identical=bool(np.array_equal(a['Q'], b_['Q'])))
R['frozen_ear_rebuild'] = frz
json.dump(R, open(EV + '/HV_ear_family_closure_record.json', 'w'), indent=1, default=float)
print('FREEZE', fr)
for k, v in R['technical'].items(): print(k, v['technical_pass'], v['failed'], 'min %.1f asp %.3f selfx %d T4 %d clear %.2f guard %d' % (v['min_angle'], v['aspect_max'], v['branch_selfx'], v['T4'], v['clearance_min_cm'], v['guard_iterations']))
for k, v in R['firewall'].items(): print('FW', k, {p: (x['n'], x['r2'], x['alpha']) for p, x in v['pairs'].items()}, v['distinct_domains_vs'])
print(R['family']); print('DET', det); print('FRZ', frz)
