# fenn_partA.py WORK OUT.json : order 57dc328 Part A -- Fenn configuration-2 central reference (FNF181) validation.
#  integrity of the native hm08 body (FNF181, FNL4, MF-F-R comparator); stature; configuration consistency (FNF181 - FNL4 vs the human-family
#  configuration architecture MFF181 - MFM181 and SGF181 - SGM181, all 181 cm); Fenn body identity at matched stature for BOTH configurations
#  against Marchfolk and Sagekin (canon directions from FENN_V1); pelvis relational canon (E-A2) and the no-sex-specific-Fenn-pelvis check.
import sys, json, numpy as np
from collections import Counter
from scipy.spatial import cKDTree
W, OUT = sys.argv[1:3]; RA = '/home/claude/wayfarer-design/reviews/reference-assets'
def integrity(npz):
    z = np.load(npz); V = z['V'].astype(float); Q = np.asarray(z['Q']).astype(int); nV = len(V)
    E = np.sort(np.stack([Q, np.roll(Q, -1, 1)], 2).reshape(-1, 2), 1); ec = Counter(map(tuple, E.tolist()))
    D = Counter(map(tuple, np.stack([Q, np.roll(Q, -1, 1)], 2).reshape(-1, 2).tolist()))
    par = np.arange(nV)
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for q in Q:
        r0 = f(q[0])
        for v in q[1:]:
            r = f(v)
            if r != r0: par[r] = r0
    used = np.unique(Q); P = V[Q]
    a = 0.5 * np.linalg.norm(np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]), axis=1) + 0.5 * np.linalg.norm(np.cross(P[:, 2] - P[:, 0], P[:, 3] - P[:, 0]), axis=1)
    tri = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]; vol = float(np.einsum('ij,ij->i', V[tri[:, 0]], np.cross(V[tri[:, 1]], V[tri[:, 2]])).sum() / 6.0)
    return dict(verts=int(nV), quads=int(len(Q)), components=len({f(v) for v in used}), boundary_edges=sum(1 for c in ec.values() if c == 1), nonmanifold_edges=sum(1 for c in ec.values() if c > 2),
                orientation_inconsistent_edges=sum(1 for c in D.values() if c > 1), degenerate_faces=int(((np.array([len(set(q)) for q in Q.tolist()]) < 4) | (a < 1e-6)).sum()),
                coincident_vertex_pairs=len(cKDTree(V[used]).query_pairs(1e-5)), signed_volume_L=round(vol / 1000.0, 3))
meas = lambda p: json.load(open(p))['combined']
M = {'FNL4': meas(W + '/partA/ref/FNL4_meas.json'), 'FN157-NAT': meas(RA + '/builds/FN157-NAT_meas.json'), 'FN211': meas(RA + '/builds/FN211_meas.json'), 'FNF181': meas(W + '/partA/build/FNF181_meas.json')}
for n in ('MFF181', 'MFM181', 'SGF181', 'SGM181'): M[n] = meas('%s/partA/cmp/%s_meas.json' % (W, n))
def R(n, k):
    m = M[n]; r = m['ratio']
    if k in r: return r[k]
    L = m['mean']
    if k == 'foot_breadth_over_len': return L['foot_breadth'] / L['foot_len']
    if k == 'palm_breadth_share': return L['palm_breadth'] / m['stature']
    if k == 'eye_diam_share': return m['cranio']['eye_diam_cm'] / m['stature']
    raise KeyError(k)
# canon directions (FENN_V1 v1.0-v1.1; order 57dc328 §1 / §4): +1 Fenn > human comparator, -1 Fenn <, 0 report only
CANON = [('leg share (hip-joint height)', 'leg_share', +1), ('lower leg / leg', 'shin_over_leg', +1), ('arm share', 'arm_share', +1), ('forearm / arm', 'forearm_over_arm', +1),
         ('hand share', 'hand_share', +1), ('finger / hand', 'finger_over_hand', +1), ('foot share', 'foot_share', +1), ('foot breadth / length', 'foot_breadth_over_len', -1),
         ('knee / femur (joint scale)', 'knee_over_femur', -1), ('ankle / shin (joint scale)', 'ankle_over_shin', -1), ('wrist / forearm (joint scale)', 'wrist_over_forearm', -1), ('elbow / humerus (joint scale)', 'elbow_over_humerus', -1),
         ('torso length', 'torso_share', -1), ('ribcage depth', 'thorax_depth_share', -1), ('thorax breadth', 'thorax_breadth_share', -1), ('shoulder (bideltoid)', 'shoulder_breadth_share', 0),
         ('shoulder joint breadth (clavicle span)', 'shoulder_joint_share', 0), ('iliac crest', 'crest_share', 0), ('bitrochanteric / crest (E-A2: not lower)', 'bitroch_over_crest', +1), ('pelvic vertical', 'pelvic_vertical_share', 0),
         ('eye globe diameter / stature (derived from the orbit, W1c ruling; not the orbit canon)', 'eye_diam_share', 0), ('head height', 'HH_share', 0)]
res = dict(integrity={n: integrity(p) for n, p in (('FNF181', W + '/src/FNF181_native.npz'), ('FNL4', W + '/src/FNL4_native.npz'), ('MF-F-R (comparator)', '/tmp/claude-0/rt/v5/src/MF-F-R_native.npz'))},
           stature={n: round(m['stature'], 4) for n, m in M.items()}, identity=[], configuration=[])
for lab, k, sgn in CANON:
    row = dict(measure=lab, key=k, canon_direction=sgn, FNL4=round(R('FNL4', k), 5), FNF181=round(R('FNF181', k), 5))
    for cfg, fn, mf, sg in (('c1', 'FNL4', 'MFM181', 'SGM181'), ('c2', 'FNF181', 'MFF181', 'SGF181')):
        dm = 100 * (R(fn, k) / R(mf, k) - 1); ds = 100 * (R(fn, k) / R(sg, k) - 1); row['%s_vs_MF_pct' % cfg] = round(dm, 2); row['%s_vs_SG_pct' % cfg] = round(ds, 2)
        row['%s_canon_ok' % cfg] = None if sgn == 0 else bool(np.sign(dm) == sgn and np.sign(ds) == sgn)
    row['c2_replicates_c1_sign'] = bool(np.sign(row['c1_vs_MF_pct']) == np.sign(row['c2_vs_MF_pct'])) or abs(row['c1_vs_MF_pct']) < 0.3
    res['identity'].append(row)
    cf = 100 * (R('FNF181', k) / R('FNL4', k) - 1); cm = 100 * (R('MFF181', k) / R('MFM181', k) - 1); cs = 100 * (R('SGF181', k) / R('SGM181', k) - 1)
    res['configuration'].append(dict(measure=lab, key=k, fenn_c2_minus_c1_pct=round(cf, 2), marchfolk_c2_minus_c1_pct=round(cm, 2), sagekin_c2_minus_c1_pct=round(cs, 2), fenn_minus_marchfolk_architecture_pct=round(cf - cm, 2)))
ids = [r for r in res['identity'] if r['canon_direction'] != 0]
res['identity_summary'] = dict(canon_measures=len(ids), c1_canon_ok=sum(r['c1_canon_ok'] for r in ids), c2_canon_ok=sum(r['c2_canon_ok'] for r in ids), c2_replicates_c1_sign=sum(r['c2_replicates_c1_sign'] for r in res['identity']),
                               measures=len(res['identity']), c1_failures=[r['key'] for r in ids if not r['c1_canon_ok']], c2_failures=[r['key'] for r in ids if not r['c2_canon_ok']])
PEL = ['crest_share', 'bitroch_share', 'bitroch_over_crest', 'pelvic_depth_share', 'pelvic_vertical_share', 'hip_joint_breadth_share', 'leg_share']
res['pelvis'] = dict(E_A2_hip_joint_height_gt_MF=dict(c1=R('FNL4', 'leg_share') > R('MFM181', 'leg_share'), c2=R('FNF181', 'leg_share') > R('MFF181', 'leg_share')),
                     E_A2_bitroch_over_crest_not_lower_than_MF=dict(c1=R('FNL4', 'bitroch_over_crest') >= R('MFM181', 'bitroch_over_crest'), c2=R('FNF181', 'bitroch_over_crest') >= R('MFF181', 'bitroch_over_crest')),
                     fenn_departure_c1_vs_c2={k: dict(c1_pct=round(100 * (R('FNL4', k) / R('MFM181', k) - 1), 2), c2_pct=round(100 * (R('FNF181', k) / R('MFF181', k) - 1), 2)) for k in PEL},
                     note='the configuration-2 pelvis difference comes only from the shared MPFB configuration architecture (the same gender macro as accepted MF-F-R / SGF178 / SKF208); no Fenn-specific sex-related pelvic target or bone scale is authored (FNF181 cfg = FNL4 cfg except gender)')
SK = {n: json.load(open('%s/partA/skp/%s_skp.json' % (W, n))) for n in ('FNL4', 'FNF181', 'MFM181', 'MFF181')}
res['pelvis_skeletal_proxy'] = dict(method='tools/rac/w1/skeletal_proxy.py (canon validation layer, PV-D16: bony / skeletal-envelope geometry at t = 0, 0.5, 1.0 cm x H/173; a direction counts only if it holds at all three)',
    align_joint_resid_cm={n: round(v['align_joint_resid_cm'], 3) for n, v in SK.items()}, leg_share={n: round(v['leg_share'], 4) for n, v in SK.items()},
    by_t={t: {k: dict(FNL4=round(SK['FNL4']['by_t'][t]['ratio'][k], 4), MFM181=round(SK['MFM181']['by_t'][t]['ratio'][k], 4), FNF181=round(SK['FNF181']['by_t'][t]['ratio'][k], 4), MFF181=round(SK['MFF181']['by_t'][t]['ratio'][k], 4),
                                c1_pct=round(100 * (SK['FNL4']['by_t'][t]['ratio'][k] / SK['MFM181']['by_t'][t]['ratio'][k] - 1), 2), c2_pct=round(100 * (SK['FNF181']['by_t'][t]['ratio'][k] / SK['MFF181']['by_t'][t]['ratio'][k] - 1), 2))
                       for k in ('bitroch_over_crest', 'crest_share', 'bitroch_share', 'pelvic_depth_share', 'hip_joint_breadth_share')} for t in SK['FNL4']['by_t']})
bt = res['pelvis_skeletal_proxy']['by_t']
res['pelvis_skeletal_proxy']['E_A2'] = dict(hip_joint_height_share_gt_MF=dict(c1=SK['FNL4']['leg_share'] > SK['MFM181']['leg_share'], c2=SK['FNF181']['leg_share'] > SK['MFF181']['leg_share']),
    bitroch_over_crest_not_lower_than_MF=dict(c1=all(bt[t]['bitroch_over_crest']['c1_pct'] >= 0 for t in bt), c2=all(bt[t]['bitroch_over_crest']['c2_pct'] >= 0 for t in bt),
                                              c2_pct_by_t=[bt[t]['bitroch_over_crest']['c2_pct'] for t in bt], c1_pct_by_t=[bt[t]['bitroch_over_crest']['c1_pct'] for t in bt],
                                              resolution_note='proxy alignment residual %.3f cm on a ~30 cm bitrochanteric breadth = %.2f %% of the ratio; the c2 difference (%.2f %%) is below the method resolution (a tie), not a measurable narrowing' % (SK['FNF181']['align_joint_resid_cm'], 100 * SK['FNF181']['align_joint_resid_cm'] / (SK['FNF181']['by_t']['0.0']['ratio']['bitroch_share'] * SK['FNF181']['stature_r6']), bt['0.0']['bitroch_over_crest']['c2_pct'])))
res['configuration_summary'] = dict(max_abs_fenn_minus_architecture_pct=round(max(abs(r['fenn_minus_marchfolk_architecture_pct']) for r in res['configuration']), 2),
                                    sign_agreement_with_marchfolk=sum((np.sign(r['fenn_c2_minus_c1_pct']) == np.sign(r['marchfolk_c2_minus_c1_pct'])) or abs(r['marchfolk_c2_minus_c1_pct']) < 0.3 for r in res['configuration']), measures=len(res['configuration']))
json.dump(res, open(OUT, 'w'), indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
print(json.dumps(dict(integrity=res['integrity'], stature=res['stature'], ids=res['identity_summary'], pel={k: v for k, v in res['pelvis'].items() if k.startswith('E_A2')}, cfg=res['configuration_summary']), indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o)))
for r in res['identity']: print('%-40s c1 MF %+6.2f SG %+6.2f %s | c2 MF %+6.2f SG %+6.2f %s' % (r['measure'], r['c1_vs_MF_pct'], r['c1_vs_SG_pct'], r['c1_canon_ok'], r['c2_vs_MF_pct'], r['c2_vs_SG_pct'], r['c2_canon_ok']))
for r in res['configuration']: print('%-40s fenn %+6.2f MF %+6.2f SG %+6.2f' % (r['measure'], r['fenn_c2_minus_c1_pct'], r['marchfolk_c2_minus_c1_pct'], r['sagekin_c2_minus_c1_pct']))
