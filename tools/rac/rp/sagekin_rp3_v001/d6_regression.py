# d6_regression.py OUTDIR CID=CAND=NATIVE=LOOPS ... : order d921903 §5 -- D6 blast-radius verification on every validated family realization.
# For each configuration: authoritative D1+D3+D4+D5 vs D1+D3+D4+D5+D6 (verdict, loops, status per station; nothing may be lowered), and an
# audit of EVERY non-digit band side at neck / shoulder / elbow / wrist / hip / knee / ankle:
#   endpoint dominant skin bones + weights, D6 decision, the side path's audit-zone composition, endpoint distance to the station centre;
#   false positive  = a side D6 excludes although its path lies in the station's own body region (own zones table below) -> STOP condition;
#   residual foreign = a side D6 keeps although its path lies mostly outside the own region (reported; cannot lower a verdict).
import sys, os, json, numpy as np, scipy.sparse as sp
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001')
from val2lib import evaluate, REF_STATURE_CM, D6_OWN
OWNZ = {'neck': {'neck', 'head', 'trunk', 'face'}, 'shoulder': {'arm', 'trunk', 'neck'}, 'elbow': {'arm'}, 'wrist': {'arm', 'hand'}, 'hip': {'trunk', 'leg'}, 'knee': {'leg'}, 'ankle': {'leg', 'foot'}}
O = sys.argv[1]; os.makedirs(O, exist_ok=True); summ = {}
for arg in sys.argv[2:]:
    cid, cp, npth, lp = arg.split('='); cz = np.load(cp); nz = np.load(npth); zone = np.load(lp, allow_pickle=True)['zone']
    M = sp.csr_matrix((cz['M_data'], cz['M_indices'], cz['M_indptr']), shape=tuple(cz['M_shape'])); assert np.array_equal(nz['src_index'], cz['src_index'])
    V = cz['V'].astype(float); Q = np.asarray(cz['Q']); meta = json.loads(str(cz['meta']))
    A = evaluate(V, Q, meta, REF_STATURE_CM, d5=True); B = evaluate(V, Q, meta, REF_STATURE_CM, d5=True, d6=(np.asarray(M @ nz['W']), [str(b) for b in nz['bones']]))
    json.dump(B, open('%s/%s_validator_v2_D4_D5_D6.json' % (O, cid), 'w'), indent=1)
    rows, fp, rf, lowered, changed = [], [], [], [], []
    for nm, b in B['stations'].items():
        a = A['stations'][nm]
        if b['loops_v2'] < a['loops_v2'] or (a['firm_D1_D3'] and not b['firm_D1_D3']): lowered.append(nm)
        if b['loops_v2'] != a['loops_v2'] or b['firm_D1_D3'] != a['firm_D1_D3'] or b['status_D1_D3'] != a['status_D1_D3']: changed.append(dict(station=nm, loops=[a['loops_v2'], b['loops_v2']], firm=[a['firm_D1_D3'], b['firm_D1_D3']], status=[a['status_D1_D3'], b['status_D1_D3']]))
        key = nm.split('_')[0]
        if key not in D6_OWN: continue
        c = np.array([0, 0, 0.0])
        for sd in b['sides']:
            if 'endpoint_dominant_bone' not in sd: continue
            pz = [str(zone[v]) for v in sd.get('path', sd['endpoints'])]; frac_own = float(np.mean([z in OWNZ[key] for z in pz]))
            r = dict(station=nm, side=sd['side'], d6_excluded=bool(sd.get('D6_undefined')), defined_before_d6=bool(sd['defined'] or sd.get('D6_undefined')), endpoint_bones=sd['endpoint_dominant_bone'], endpoint_weights=sd['endpoint_dominant_weight'],
                     path_zones=sorted(set(pz)), path_own_zone_fraction=round(frac_own, 3), loops=sd.get('loops'))
            rows.append(r)
            if r['d6_excluded'] and frac_own >= 0.5: fp.append(r)
            if r['defined_before_d6'] and not r['d6_excluded'] and frac_own < 0.5: rf.append(r)
    ex = [r for r in rows if r['d6_excluded']]
    by_joint = {}
    for r in rows:
        k = r['station'].split('_')[0]; by_joint.setdefault(k, dict(sides_audited=0, d6_excluded=0, false_positive=0)); by_joint[k]['sides_audited'] += 1; by_joint[k]['d6_excluded'] += r['d6_excluded']; by_joint[k]['false_positive'] += r in fp
    summ[cid] = dict(firm_D1_D3_D4_D5=A['summary']['firm_pass_count'], firm_D1_D3_D4_D5_D6=B['summary']['firm_pass_count'], fails_D6=B['summary']['D1_D3_firm_fail'], lowered=lowered, changed=changed,
                     d6_excluded=[(r['station'], r['side'], r['endpoint_bones'], r['path_zones']) for r in ex], false_positives=fp, residual_foreign_kept=rf, by_joint=by_joint)
    json.dump(dict(config=cid, sides=rows, summary=summ[cid]), open('%s/%s_D6_side_audit.json' % (O, cid), 'w'), indent=1)
    print(cid, 'firm', summ[cid]['firm_D1_D3_D4_D5'], '->', summ[cid]['firm_D1_D3_D4_D5_D6'], 'lowered', lowered, 'excluded', summ[cid]['d6_excluded'], 'FP', len(fp), 'residual', [(r['station'], r['side'], r['path_zones']) for r in rf], flush=True)
ok = all(s['firm_D1_D3_D4_D5_D6'] == 69 and not s['lowered'] and not s['false_positives'] for s in summ.values())
json.dump(dict(order='d921903 §5', rule='D6 non-digit foreign-segment ownership (val2lib.D6_OWN)', own_bones=D6_OWN, own_zones={k: sorted(v) for k, v in OWNZ.items()}, configurations=summ, regression_pass=ok), open(O + '/D6_regression_summary.json', 'w'), indent=1)
print('D6 REGRESSION PASS' if ok else 'D6 REGRESSION FAIL')
