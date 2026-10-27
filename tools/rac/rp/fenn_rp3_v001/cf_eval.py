# cf_eval.py WORK OUT.json : order 2de0e28 §8 / §9 -- hidden-ear facial identity of the craniofacial source candidates (and the current sources) against
# matched-stature Marchfolk / Sagekin, the six canon systems, orbit dominance, configuration consistency, and the non-head (body) change.
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fn_face_metrics as F
W, OUT = sys.argv[1:3]; RA = '/home/claude/wayfarer-design/reviews/reference-assets/r6'; PA = W + '/partA'; CF = W + '/cf/cand'
COMP = {'c1': dict(MF=PA + '/cmp/MFM181_r6.npz', SG=PA + '/cmp/SGM181_r6.npz', SRC=RA + '/FNL4_r6.npz', ID='FNL4'), 'c2': dict(MF=PA + '/cmp/MFF181_r6.npz', SG=PA + '/cmp/SGF181_r6.npz', SRC=RA + '/FNF181_r6.npz', ID='FNF181')}
MAT = 1.0                                          # selection constraint (order §9; not canon): a material departure is >= 1.0 % AND > 2x the human-human baseline
res = dict(selection_constraint_pct=MAT, configs={})
for cfg, C in COMP.items():
    L = {k: F.load(C[k]) for k in ('MF', 'SG', 'SRC')}; dM = F.descriptors(L['MF']['V']); dS = F.descriptors(L['SG']['V']); base = {k: abs(100 * (dS[k] / dM[k] - 1)) for k in dM}
    nonhead = (L['SRC']['wh'] < 0.05) & ~F.EAR; out = {}
    for tag, p in [('source', C['SRC'])] + [('CF%d' % i, '%s/%s-CF%d/%s-CF%d_r6.npz' % (CF, C['ID'], i, C['ID'], i)) for i in (1, 2, 3)]:
        X = F.load(p); d = F.descriptors(X['V']); rm, _ = F.region_rms(X['V'], L['MF']['V']); rs, _ = F.region_rms(X['V'], L['SG']['V'])
        desc = {}
        for k, sg in F.CANON.items():
            pm = 100 * (d[k] / dM[k] - 1); ps = 100 * (d[k] / dS[k] - 1)
            desc[k] = dict(value=round(d[k], 4), vs_MF_pct=round(pm, 2), vs_SG_pct=round(ps, 2), human_baseline_pct=round(base[k], 2), canon=sg,
                           canon_direction_ok=None if sg == 0 else bool(np.sign(pm) == sg and np.sign(ps) == sg),
                           material=None if sg == 0 else bool(np.sign(pm) == sg and np.sign(ps) == sg and min(abs(pm), abs(ps)) >= MAT and min(abs(pm), abs(ps)) > 2 * base[k]))
        systems = {s: dict(descriptors=ks, material=all(desc[k]['material'] for k in ks) if len(ks) == 1 else (any(desc[k]['material'] for k in ks) and all(desc[k]['canon_direction_ok'] for k in ks)),
                           direction_ok=all(desc[k]['canon_direction_ok'] for k in ks)) for s, ks in F.SYSTEMS.items()}
        tot = sum(v ** 2 for v in rm.values()); orbit_share = rm['orbit_eye_region'] ** 2 / tot if tot else 0
        out[tag] = dict(file=os.path.relpath(p, W), descriptors=desc, systems=systems, systems_material=sum(v['material'] for v in systems.values()), systems_direction_ok=sum(v['direction_ok'] for v in systems.values()),
                        region_rms_vs_MF_mm=rm, region_rms_vs_SG_mm=rs, orbit_share_of_face_residual=round(orbit_share, 3), orbit_is_dominant=bool(orbit_share > 0.5),
                        nonhead_max_change_mm=round(float(np.linalg.norm(X['V'][nonhead] - L['SRC']['V'][nonhead], axis=1).max() * 10), 3),
                        stature_cm=round(float(X['V'][:, 2].max() - X['V'][:, 2].min()), 3), head_height_change_pct_vs_source=round(100 * (d['head_height_cm'] / F.descriptors(L['SRC']['V'])['head_height_cm'] - 1), 2))
        print(cfg, tag, 'systems material %d/6 direction %d/6' % (out[tag]['systems_material'], out[tag]['systems_direction_ok']), 'orbit share %.2f' % orbit_share,
              {k.split('_over')[0][:12]: v['vs_MF_pct'] for k, v in desc.items()}, 'RMS', {k[:7]: v for k, v in rm.items()}, 'nonhead %.2f mm' % out[tag]['nonhead_max_change_mm'], flush=True)
    res['configs'][cfg] = out
cons = {}
for tag in ('CF1', 'CF2', 'CF3'):
    a = res['configs']['c1'][tag]['descriptors']; b = res['configs']['c2'][tag]['descriptors']
    cons[tag] = dict(same_signs=all(np.sign(a[k]['vs_MF_pct']) == np.sign(b[k]['vs_MF_pct']) for k in a if F.CANON[k] != 0),
                     ratio_c2_over_c1={k: round(b[k]['vs_MF_pct'] / a[k]['vs_MF_pct'], 2) if abs(a[k]['vs_MF_pct']) > 0.05 else None for k in a if F.CANON[k] != 0},
                     identity_strength_c1=round(float(np.sqrt(sum(a[k]['vs_MF_pct'] ** 2 for k in a if F.CANON[k] != 0))), 2), identity_strength_c2=round(float(np.sqrt(sum(b[k]['vs_MF_pct'] ** 2 for k in b if F.CANON[k] != 0))), 2))
res['configuration_consistency'] = cons; print(json.dumps(cons, indent=0))
json.dump(res, open(OUT, 'w'), indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
