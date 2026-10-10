# RAC W3B RM-UF-04 ridge envelope evaluation (diagnostic guards; values in ridge/results.json):
#  NAKED-SKULL LOWER: L1 every required family keeps a positive strength (ridges never reach zero); L3 0 new folds (non-sliver);
#                     L4 edge strain p1 >= 0.67. Visual: naked skull still reads Saurin (renders).
#  SCALED-FACE LEGIBILITY (relationship clamp, reported per family): strength >= 1.0 x the canonical scale-relief amplitude around the ridge.
#  UPPER: U1 0 new folds; U2 edge strain p99 <= 1.5 (razor / pinched crest); U3 ridge flank slope p95 <= 45 deg (fin / blade);
#         U4 frontal eye visibility (0 and 10 deg) >= 90 % of canonical (no scowl). Visual: armor / facet / caricature (renders).
import os, sys, json, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import w3b_common as C
REQ = ['canthal', 'supraorbital', 'temporal', 'jugal', 'occipital', 'mandibular']
def grade(r, ref, fams):
    q = r['quality']; g = {}
    g['L1_present'] = all(r['metric'][k]['strength_cm'] > 0 for k in fams)
    g['fold'] = q.get('flipped_nonsliver', q['flipped']) == 0
    g['strain'] = q['strain_pct'][1] >= 0.67 and q['strain_pct'][3] <= 1.5
    g['U3_slope'] = all(r['flank_slope_p95_deg'][k] <= 45 for k in fams)
    g['U4_scowl'] = r['eye_vis_0'] >= 0.9 * ref['eye_vis_0'] and r['eye_vis_10'] >= 0.9 * ref['eye_vis_10']
    return g
if __name__ == '__main__':
    R = json.load(open(C.W + '/ridge/results.json')); ref = R['g1.00']; out = {}
    groups = {'global': ('g', REQ)} ; groups.update({k: (k, [k]) for k in REQ})
    for name, (pre, fams) in groups.items():
        rows = sorted([(float(t[len(pre):]), t) for t in R if t.startswith(pre) and t[len(pre):].replace('.', '').isdigit()] + ([(1.0, 'g1.00')] if pre != 'g' else []))
        res = []
        for m, t in rows:
            g = grade(R[t], ref, fams); leg = {k: R[t]['legibility_ratio'][k] for k in fams}
            res.append(dict(m=m, ok=all(g.values()), fails=[a for a, b in g.items() if not b], legibility=leg, strength={k: R[t]['metric'][k]['strength_cm'] for k in fams},
                            strain=[R[t]['quality']['strain_pct'][1], R[t]['quality']['strain_pct'][3]], folds=R[t]['quality'].get('flipped_nonsliver')))
        i0 = [i for i, x in enumerate(res) if x['m'] == 1.0][0]; lo = hi = i0
        while lo - 1 >= 0 and res[lo - 1]['ok']: lo -= 1
        while hi + 1 < len(res) and res[hi + 1]['ok']: hi += 1
        # legibility clamp: lowest m with every family's legibility >= 1.0 (linear interpolation between tested points)
        legmin = {}
        for k in fams:
            pts = sorted((x['m'], x['legibility'][k]) for x in res); ms = [p[0] for p in pts]; ls = [p[1] for p in pts]
            mm = None
            for (m0, l0), (m1, l1) in zip(pts, pts[1:]):
                if l0 < 1.0 <= l1: mm = m0 + (1.0 - l0) * (m1 - m0) / (l1 - l0)
            legmin[k] = mm if mm is not None else (ms[0] if ls[0] >= 1.0 else None)
        out[name] = dict(min_valid=res[lo]['m'], max_valid=res[hi]['m'], first_invalid_low=(res[lo - 1]['m'], res[lo - 1]['fails']) if lo else 'not reached',
                         first_invalid_high=(res[hi + 1]['m'], res[hi + 1]['fails']) if hi + 1 < len(res) else 'not reached (max tested)', legibility_min_m=legmin, rows=res)
        print(name, 'valid [%s, %s]' % (res[lo]['m'], res[hi]['m']), 'low-fail', out[name]['first_invalid_low'], 'high-fail', out[name]['first_invalid_high'], 'legibility m_min', {k: (round(v, 2) if v else v) for k, v in legmin.items()})
    json.dump(out, open(C.W + '/ridge/envelope.json', 'w'), indent=1)
