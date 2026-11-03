# sa6_summary.py WORKDIR : print the report tables (markdown) from the run outputs (ev_M/F.json, wa.json, ca.json, pd2.json, rb_M/F.json, rig-prep, tail study).
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa6_common as C
WD = sys.argv[1]; ev = {c: json.load(open(WD + '/ev_%s.json' % c))['poses'] for c in 'MF'}
def worst(p, k): return max(v[k] for v in p['fractions'].values())
print('| pose | c1 RP5 s1/s3 | c1 LBS | c1 corr (max over 0.25-1.0) | c1 pen | c2 LBS | c2 corr | c2 pen | c1 class | c2 class |'); print('|---|---|---|---|---|---|---|---|---|---|')
tot = dict(rig=0, topo=0, topo_only=0, pen=0)
for pn in ev['M']:
    a, b = ev['M'][pn], ev['F'][pn]; s2 = a['step2_rp5_scaffold']; s2s = '%d / %d' % (s2['step1_cage_flips'], s2['step3_improved']) if isinstance(s2, dict) else 'n/a'
    print('| %s | %s | %d | %d | %d | %d | %d | %d | %s | %s |' % (pn, s2s, worst(a, 'lbs_flips'), worst(a, 'corrected_flips'), worst(a, 'corrected_new_penetration_vertices'), worst(b, 'lbs_flips'), worst(b, 'corrected_flips'),
                                                          worst(b, 'corrected_new_penetration_vertices'), a['classification'][:70], b['classification'][:70]))
    for x in (a, b):
        tot['rig'] += (x['rig_owned_folds_after_correctives'] or 0); tot['topo'] += 'TOPOLOGY' in x['classification'].split('+')[0]; tot['topo_only'] += (x['topology_only_flips'] or 0)
        tot['pen'] += 0 if pn == 'jaw_open_20_rp5lit' else worst(x, 'corrected_new_penetration_vertices')
print('\nTOTALS', tot)
# metrics ranges
for c in 'MF':
    vr = [(pn, b, m['volume_ratio_corrected'], m['volume_ratio_lbs']) for pn, p in ev[c].items() if pn != 'jaw_open_20_rp5lit' for b, m in p.get('joint_metrics', {}).items()]
    st = [(pn, b, m['stretch_corrected'][0], m['stretch_corrected'][3]) for pn, p in ev[c].items() if pn != 'jaw_open_20_rp5lit' for b, m in p.get('joint_metrics', {}).items()]
    vv = np.array([x[2] for x in vr]); vl = np.array([x[3] for x in vr])
    print(c, 'volume ratio corrected min %.3f (%s) max %.3f (%s) | LBS min %.3f max %.3f' % (vv.min(), vr[vv.argmin()][:2], vv.max(), vr[vv.argmax()][:2], vl.min(), vl.max()))
    smin = min(st, key=lambda x: x[2]); smax = max(st, key=lambda x: x[3]); print(c, 'stretch corrected min', smin, 'max', smax)
    lm = [(pn, p['landmarks']['max_rigid_cm']) for pn, p in ev[c].items()]; print(c, 'rigid landmark max', max(lm, key=lambda x: x[1]))
    tg = {pn: p['gate_metrics'] for pn, p in ev[c].items() if p.get('gate_metrics')}
    print(c, 'tail', {pn: (g['tail']['ring_area_ratio_min'], g['tail']['kink_ratio_max'], g['tail']['turning_deg_max']) for pn, g in tg.items() if 'tail' in g})
    print(c, 'palm', {pn: g['palm_volume_ratio'] for pn, g in tg.items() if 'palm_volume_ratio' in g})
    print(c, 'foot', {pn: (g['foot_volume_ratio'], g['sole_down_facing_fraction'], g['sole_down_facing_fraction_rest']) for pn, g in tg.items() if 'foot_volume_ratio' in g})
    print(c, 'opp', {pn: g['thumb_tip_to_finger_tip_cm'] for pn, g in tg.items() if 'thumb_tip_to_finger_tip_cm' in g})
    print(c, 'jaw/head', {pn: (g.get('head_rigid_err_rostrum_tip_cm'), g.get('mouth_slit_edge_stretch_max'), g.get('upper_head_rigid_vertices_max_err_cm')) for pn, g in tg.items() if 'mouth_slit_edge_stretch_max' in g})
    srcs = [(pn, p['step1_source_flip_area_permille'], p['step3_lbs_flip_area_permille']) for pn, p in ev[c].items()]; print(c, 'source>=LBS poses', [x[0] for x in srcs if x[1] > 0 and x[1] >= x[2]])
