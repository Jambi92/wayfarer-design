# sa6_tail_criterion.py OUT.json TC_*.json ... : proposed tail-kink acceptance criterion applied to tail-calibration data (order 8e3b7b4d §3).
#   Input: sa6_tail_calib.py v2 outputs (neutral | plain LBS | packaged blend v004 | baked, every tail special-gate pose, every 0.025 fraction).
#   PROPOSED CRITERION (per body, pose, fraction, deformation column; frozen 181-ring tail, 11-junction window as the pilot audit):
#     C  = max over junctions k of [ (th_k - win(th)_k) - (th0_k - win(th0)_k) ]   (deg)  -- turning concentrated at one ring junction BEYOND what the neutral
#          tail already has there, i.e. a kink introduced or amplified by the deformation (inherited neutral curvature, e.g. the tip taper, cancels).
#     PASS        C <= 2.0 deg and ring-area retention >= 0.95
#     REVIEW      2.0 < C <= 2.5 deg  (visual review of centreline + shaded mesh at that frame)
#     FAIL        C > 2.5 deg, or area retention < 0.95
#     Folds / tears / inversion / contact stay with the existing RP6 gates; the raw kink ratio (pilot 2.51) is kept as a DIAGNOSTIC flag only.
#   Calibration evidence (renders): visible crease line at the tail root for plain LBS at C = 2.12, 2.53, 3.23 (tail_root_biased_60); no visible crease at
#   C = 1.15, 1.20 (distal), 1.62, 1.92, 1.99, 2.45 (tail_combined).  -> OUT.json: per-column counts, every REVIEW / FAIL frame, the worst frame per case,
#   and the raw-kink diagnostic counts for comparison.
import sys, json, collections
PASS, REVIEW, AREA = 2.0, 2.5, 0.95
out = dict(status='RP6 RIG PILOT / NOT FROZEN', criterion=dict(measure='max_k [(th_k - win_k) - (th0_k - win0_k)] deg, 181 frozen rings, 11-junction window', pass_deg=PASS, review_deg=REVIEW,
           area_retention_min=AREA, raw_kink_diagnostic=2.51), inputs=[], columns={}, flagged=[], worst_per_case=[])
W = {}
for f in sys.argv[2:]:
    r = json.load(open(f)); out['inputs'].append(dict(file=f.split('/')[-1], body=r['name'], artifact_sha256=r.get('artifact_sha256'), body_sha256=r.get('body_sha256')))
    for pn, v in r['poses'].items():
        for col, x in v.items():
            st = out['columns'].setdefault(col, collections.Counter())
            for fr, m in x['frames'].items():
                c = m['excess_change_from_neutral_max_deg']; a = m['area_retention_min']
                v_ = 'FAIL' if (c > REVIEW or a < AREA) else 'REVIEW' if c > PASS else 'PASS'; st[v_] += 1; st['frames'] += 1
                st['raw_kink_gt_2.51'] += int(m['kink_max'] > 2.51); st['raw_kink_gt_3.07'] += int(m['kink_max'] > 3.074)
                row = dict(body=r['name'], pose=pn, column=col, frac=float(fr), verdict=v_, concentration_deg=c, junction=m['excess_change_junction'], ring=m['excess_change_junction'] + 1,
                           area_retention_min=a, raw_kink=m['kink_max'], turning_deg=m['turning_deg'], neutral_turning_deg=m['neutral_turning_deg'], nearby_turning_deg=m['nearby_turning_deg'])
                if v_ != 'PASS': out['flagged'].append(row)
                k = (r['name'], pn, col)
                if k not in W or c > W[k]['concentration_deg']: W[k] = row
out['columns'] = {c: dict(s) for c, s in out['columns'].items()}
out['worst_per_case'] = sorted(W.values(), key=lambda x: -x['concentration_deg'])
json.dump(out, open(sys.argv[1], 'w'), indent=1)
for c, s in out['columns'].items(): print(c, s)
print('flagged frames', len(out['flagged']), 'by column', collections.Counter((x['column'], x['verdict']) for x in out['flagged']))
