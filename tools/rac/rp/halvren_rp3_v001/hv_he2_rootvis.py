# hv_he2_rootvis.py EVIDIR : Halvren root visual-integration order -- consolidated record HE2_root_visual_record.json:
#   technical regression of the HR2 family (hr2f: HE1 / HE2 / HE3, c1 / c2; guarded Halvren path) next to the HR1 realization of 29f2c16 (he3);
#   secondary-silhouette measures (pedestal above the extrapolated head, root-loop crease, raised cuff tab beside the lobe) per sector, before / after;
#   auricle-sheet preservation (rigid fit HR1 -> HR2 sheet: rotation / seat translation / non-rigid residual);
#   measured ear domains + the HE2 arithmetic firewall (common c1 head, sources MF / FN / AE / VA), before (HR1) / after (HR2);
#   HE2 determinism (independent rebuild with the recorded guard set incl. the cuff repair); outside-root identity (v005 vertices moved by HR2 = root loop +
#   skin within the fall-off band only; body / face / pelvis byte-identical); frozen-ear rebuild identity (Fenn E2 / Aelari AE-E2 / Vael VA-E2-RI3 with the
#   final ear_build on the common head, recorded guard sets).
import sys, os, json, subprocess, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import hv_ear_summary as S; import hv_ear_domains as D; import hv_root_sectors as RS
from scipy.spatial import cKDTree
EV = sys.argv[1]; os.makedirs(EV, exist_ok=True); E = '/tmp/claude-0/rt/hv/ear'; HP = '/tmp/claude-0/rt/hv/hpe'; jl = lambda p: json.load(open(p))
H = {'c1': 'HVC1-HB2HF2-HPB', 'c2': 'HVF178-HB2HF2-HPB'}; T = '/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001'; BP = '/home/claude/stc/bin/python3'
R = dict(order='chatgpt-rac-rp3-halvren-ear-root-visual-integration-correction-order', technical={}, silhouette={}, sheet_preservation={}, domains={}, firewall={})
def tech(x): return dict(technical_pass=x['technical_pass'], failed=[g for g, v in x['gates'].items() if not v], components=x['integrity']['components'], boundary=x['integrity']['boundary'],
                         nonmanifold=x['integrity']['nonmanifold'], degenerate=x['integrity']['degenerate'], outward=x['integrity']['outward'], branch_selfx=x['integrity']['branch_selfx'],
                         min_angle=round(x['min_angle'], 1), aspect_max=round(x['aspect_max'], 2), T4=x['T4'], density_pct=round(x['density_pct'], 3), root_valence=x['root_valence'],
                         mound_p90_cm=round(x['root_concha']['anterior_cuff_mound_p90_cm'], 3), junction_cm=round(x['root_concha']['junction_anterior_height_mean_cm'], 3),
                         concha_floor_cm=round(x['root_concha']['concha_floor_min_vs_skin_cm'], 2), clearance_min_cm=round(x['clearance_min_cm'], 2), poses=x['poses'],
                         poses_clean=x['gates']['poses_clean'], guard_iterations=len(x['guard'] or []) - 1, faces_sha=x['face_topology_sha256'], length_over_HH_measure=round(x['measure']['length_over_HH'], 3))
for c, h in H.items():
    for k in ('HE1', 'HE2', 'HE3'):
        R['technical']['%s %s' % (k, c)] = tech(S.summ(E + '/hr2f', k, h)); R['technical']['%s %s' % (k, c)]['cuff_repair'] = jl('%s/hr2f/build/%s_%s_branch.json' % (E, h, k)).get('hv_cuff_repair')
        R['technical']['%s %s HR1' % (k, c)] = tech(S.summ(E + '/he3', k, h))
for c, h in H.items():
    for k in ('HE1', 'HE2', 'HE3'):
        for lab, w in (('HR1', 'he3'), ('HR2', 'hr2f')):
            s_ = RS.sectors('%s/%s/build/%s_%s_branch.npz' % (E, w, h, k), h); R['silhouette']['%s %s %s' % (k, c, lab)] = {q: s_['l'][q] for q in ('pedestal_vs_true_head', 'loop_crease_deg', 'inferior_fork')}
def rigid(A, B):
    ca, cb = A.mean(0), B.mean(0); U, S_, Vt = np.linalg.svd((A - ca).T @ (B - cb)); d = np.sign(np.linalg.det(U @ Vt)); Rm = (U @ np.diag([1, 1, d]) @ Vt).T; return Rm, cb - ca @ Rm.T
for c, h in H.items():
    for k in ('HE1', 'HE2', 'HE3'):
        a = np.load('%s/he3/build/%s_%s_branch.npz' % (E, h, k)); z = np.load('%s/hr2f/build/%s_%s_branch.npz' % (E, h, k)); rec = jl('%s/he3/build/%s_%s_branch.json' % (E, h, k)); o = {}
        for sd in ('l', 'r'):
            m = np.isin(a['part'], ('front', 'back', 'rim')) & (a['side'] == sd); A_, B_ = a['V'][m], z['V'][m]; Rm, t = rigid(A_, B_); res = np.linalg.norm(A_ @ Rm.T + t - B_, axis=1)
            n = np.array(rec['sides'][sd]['frame']['n']); sh = (B_ - A_).mean(0)
            o[sd] = dict(rotation_deg=round(float(np.degrees(np.arccos(np.clip((np.trace(Rm) - 1) / 2, -1, 1)))), 2), seat_translation_cm=round(float(np.linalg.norm(sh)), 3),
                         seat_along_root_normal_cm=round(float(sh @ n), 3), nonrigid_residual_mean_cm=round(float(res.mean()), 3), nonrigid_residual_p95_cm=round(float(np.percentile(res, 95)), 3),
                         nonrigid_residual_max_cm=round(float(res.max()), 3))
        R['sheet_preservation']['%s %s' % (k, c)] = o
SRC = {'MF': ('fam', '%s/fam/%s_fam.npz' % (HP, H['c1'])), 'FN': ('branch', '%s/ref/FN/build/%s_E2_branch.npz' % (E, H['c1'])), 'AE': ('branch', '%s/ref/FN/build/%s_AE-E2_branch.npz' % (E, H['c1'])),
       'VA': ('branch', '%s/ref/RI3/build/%s_VA-E2-RI3_branch.npz' % (E, H['c1']))}
for k in ('HE1', 'HE2', 'HE3'): SRC[k] = ('branch', '%s/hr2f/build/%s_%s_branch.npz' % (E, H['c1'], k)); SRC[k + '-HR1'] = ('branch', '%s/he3/build/%s_%s_branch.npz' % (E, H['c1'], k))
SRC['HE2 c2'] = ('branch', '%s/hr2f/build/%s_HE2_branch.npz' % (E, H['c2'])); SRC['HE2-HR1 c2'] = ('branch', '%s/he3/build/%s_HE2_branch.npz' % (E, H['c2']))
M = {k: D.measure(kind, p, H['c1'] if ' c2' not in k else H['c2']) for k, (kind, p) in SRC.items()}; DOM = D.DOM; R['domain_list'] = DOM
X = {k: np.array([M[k][q] for q in DOM]) for k in M}; sd = np.maximum(np.array([X[s] for s in ('MF', 'FN', 'AE', 'VA')]).std(0), [D.FLOOR[q] for q in DOM]); em = np.mean([X[e] for e in ('FN', 'AE', 'VA')], 0)
for k in M: R['domains'][k] = dict(values={q: round(float(v), 4) for q, v in zip(DOM, X[k])}, t={q: round(float(v), 3) for q, v in zip(DOM, (X[k] - X['MF']) / np.where(np.abs(em - X['MF']) > 1e-9, em - X['MF'], 1))})
for k in ('HE1', 'HE2', 'HE3', 'HE1-HR1', 'HE2-HR1', 'HE3-HR1', 'HE2 c2', 'HE2-HR1 c2'):
    pr = {}
    for e in ('FN', 'AE', 'VA'):
        dx = (X[e] - X['MF']) / sd; y = (X[k] - X['MF']) / sd; m = np.abs(dx) > 0.5; a = float(dx[m] @ y[m] / (dx[m] @ dx[m])); r = y[m] - a * dx[m]; r2 = float(1 - r @ r / (y[m] @ y[m]))
        drv = sorted(zip(np.array(DOM)[m], a * dx[m] * y[m]), key=lambda z_: -z_[1])[:4]
        pr['MF-' + e] = dict(n=int(m.sum()), r2=round(r2, 3), alpha=round(a, 3), passes=bool(not (r2 >= 0.8 and m.sum() >= 6)), driving_domains=[d_ for d_, _ in drv])
    best = max(pr, key=lambda p_: pr[p_]['r2']); R['firewall'][k] = dict(pairs=pr, best_pair=best, best_r2=pr[best]['r2'], passes=all(v['passes'] for v in pr.values()))
R['domain_change_HE2'] = {q: dict(HR1=R['domains']['HE2-HR1']['values'][q], HR2=R['domains']['HE2']['values'][q], t_HR1=R['domains']['HE2-HR1']['t'][q], t_HR2=R['domains']['HE2']['t'][q]) for q in DOM}
# outside-root identity: which v005 vertices did HR2 move (vs the family realization), how far from the root loop; every other vertex byte-identical
oi = {}
for c, h in H.items():
    z = np.load('%s/hr2f/build/%s_HE2_branch.npz' % (E, h)); rec = jl('%s/hr2f/build/%s_HE2_branch.json' % (E, h)); fz = np.load('%s/fam/%s_fam.npz' % (HP, h)); V0 = fz['V']
    vb = z['v005_to_branch']; keep = np.nonzero(vb >= 0)[0]; dv = np.linalg.norm(z['V'][vb[keep]].astype(float) - V0[keep].astype(float), axis=1); mv = keep[dv > 1e-6]
    lp = np.r_[[np.array(rec['sides'][s]['root_loop_v005']) for s in ('l', 'r')]].ravel(); dl = cKDTree(V0[lp]).query(V0[mv])[0] if len(mv) else np.zeros(1)
    oi[c] = dict(v005_kept=int(len(keep)), moved=int(len(mv)), moved_max_dist_from_root_loop_cm=round(float(dl.max()), 3), moved_max_displacement_cm=round(float(dv.max()), 3),
                 byte_identical_beyond_fall_band=bool(np.array_equal(z['V'][vb[keep[dv <= 1e-6]]], V0[keep[dv <= 1e-6]])), unmoved=int((dv <= 1e-6).sum()))
R['outside_root_identity'] = oi
det = {}
for c, h in H.items():
    d = '%s/det_rv_%s' % (E, c); os.makedirs(d, exist_ok=True); g = '%s/hr2f/build/%s_HE2_deform_guard.json' % (E, h); lg = jl('%s/hr2f/build/%s_HE2_deform_guard_log.json' % (E, h))
    env = dict(os.environ, EAR_CF=HP, EAR_TOPO='v002', EAR_UNT_MODE='contacts', EAR_Q3_FREEZE=g, EAR_Q3_FREEZE_RINGS=str(2 if lg[-1]['iteration'] >= 2 else 1))
    subprocess.run([BP, T + '/ear_build.py', h, 'HE2', d, '--canon', E + '/hr2f/canon_branch_topology.json'], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['python3', os.path.dirname(os.path.abspath(__file__)) + '/hv_cuff_repair.py', '%s/%s_HE2_branch.npz' % (d, h), h], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    a = np.load('%s/hr2f/build/%s_HE2_branch.npz' % (E, h)); b_ = np.load('%s/%s_HE2_branch.npz' % (d, h)); det[c] = dict(max_abs_dV_cm=float(np.abs(a['V'] - b_['V']).max()), faces_identical=bool(np.array_equal(a['Q'], b_['Q'])))
R['determinism_HE2'] = det
fr = {}
for lab, w, k in (('Fenn E2', 'ref/FN', 'E2'), ('Aelari AE-E2', 'ref/FN', 'AE-E2'), ('Vael VA-E2-RI3', 'ref/RI3', 'VA-E2-RI3')):
    d = '%s/frz_rv/%s' % (E, k); os.makedirs(d, exist_ok=True); g = '%s/%s/build/%s_%s_deform_guard.json' % (E, w, H['c1'], k); lg = jl(g.replace('.json', '_log.json'))
    env = dict(os.environ, EAR_CF=HP, EAR_TOPO='v002', EAR_UNT_MODE='contacts', EAR_Q3_FREEZE=g, EAR_Q3_FREEZE_RINGS=str(2 if lg[-1]['iteration'] >= 2 else 1))
    subprocess.run([BP, T + '/ear_build.py', H['c1'], k, d, '--canon', '%s/%s/canon_branch_topology.json' % (E, w)], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    a = np.load('%s/%s/build/%s_%s_branch.npz' % (E, w, H['c1'], k)); b_ = np.load('%s/%s_%s_branch.npz' % (d, H['c1'], k))
    fr[lab] = dict(max_abs_dV_cm=float(np.abs(a['V'] - b_['V']).max()), faces_identical=bool(np.array_equal(a['Q'], b_['Q'])), geo=jl('%s/%s_%s_branch.json' % (d, H['c1'], k))['geo'])
R['frozen_ear_rebuild'] = fr
json.dump(R, open(EV + '/HE2_root_visual_record.json', 'w'), indent=1, default=float)
for k, v in R['technical'].items(): print(k, v['technical_pass'], v['failed'], 'min %.1f asp %.2f selfx %d mound %.2f junc %.2f floor %.2f clear %.2f guard %d' % (v['min_angle'], v['aspect_max'], v['branch_selfx'], v['mound_p90_cm'], v['junction_cm'], v['concha_floor_cm'], v['clearance_min_cm'], v['guard_iterations']))
for k, v in R['silhouette'].items(): print('SIL', k, {s: v['pedestal_vs_true_head'][s]['p90_cm'] for s in v['pedestal_vs_true_head']}, {s: v['loop_crease_deg'][s]['mean'] for s in v['loop_crease_deg']}, v['inferior_fork'])
for k, v in R['sheet_preservation'].items(): print('SHEET', k, v['l'])
for k, v in R['firewall'].items(): print('FW', k, {p: (x['n'], x['r2'], x['alpha']) for p, x in v['pairs'].items()})
print('OUT', oi); print('DET', det); print('FRZ', {k: (v['max_abs_dV_cm'], v['faces_identical']) for k, v in fr.items()})
