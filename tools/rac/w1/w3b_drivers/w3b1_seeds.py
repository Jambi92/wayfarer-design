# RAC W3B1 section 5: seed-stability closure (diagnostic realizations only; the canonical 130,949 seeds are never replaced).
#  (a) the six W3B seed-sensitive size ends: the W3B seed-robust inward step on rng 1007 / 2007 / 3007 / 4007 and the original end on
#      rng 3007 / 4007 (bracket the stable end);
#  (b) the ten large fields NOT RUN in W3B: the proposed creator-safe endpoints (size max capped at x1.5 unless a measured failure is lower,
#      relief max capped at x1.5 where W3B did not reach a failure) + one neighbouring stress point (next size step), on rng 1007 / 2007.
# Usage: python3 w3b1_seeds.py   (scratch w3b/scale/results_w3b1_seeds.json, w3b/w3b1_seeds.json)
import os, sys, json
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import w3b_common as C
import w3b_scale_run as SR, w3b_scale_eval as EV
env = json.load(open(C.W + '/scale/envelope.json'))
SIX = {'face_orbital_eyelid': ('size', 1.3, 1.5), 'face_auricular': ('size', 1.5, 1.75), 'face_cranial_structural': ('size', 2.0, 2.5),
       'S_shin': ('size', 0.6, 0.5), 'A_axilla': ('size', 1.2, 1.3), 'C_palmar': ('size', 1.2, 1.3)}
LARGE = ['S_dorsal_trunk', 'S_lateral_trunk', 'S_dorsal_tail', 'A_neck_flexion', 'A_lower_trunk_flexion', 'A_hip_crease', 'A_tail_articulation',
         'V_chest_abdomen', 'V_tail_underside', 'S_dorsal_hand']
STEP = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.5, 1.75, 2.0, 2.5]
cases = []; plan = {}
for k, (kind, inward, end) in SIX.items():
    plan[k] = dict(kind=kind, inward=inward, end=end)
    cases += [(k, inward, 1.0, g, True) for g in (1007, 2007, 3007, 4007)] + [(k, end, 1.0, g, True) for g in (3007, 4007)]
for k in LARGE:
    smax = min(env[k]['size']['max_valid'], 1.5); stress = STEP[STEP.index(smax) + 1]; rmax = min(env[k]['relief']['max_valid'], 1.5)
    plan[k] = dict(size_cap=smax, size_stress=stress, relief_cap=rmax)
    for g in (1007, 2007): cases += [(k, smax, 1.0, g, True), (k, stress, 1.0, g, True), (k, 1.0, rmax, g, True)]
SR.run(cases, 'results_w3b1_seeds.json')
R = json.load(open(C.W + '/scale/results_w3b1_seeds.json')); out = {}
def find(k, s, r, g): return next((x for x in R.values() if x['region'] == k and x['s'] == s and x['r'] == r and x['rng'] == g), None)
for k, p in plan.items():
    rows = []
    for (s, r, g) in [(c[1], c[2], c[3]) for c in cases if c[0] == k]:
        x = find(k, s, r, g)
        if x: gr = EV.regrade(x); rows.append(dict(s=s, r=r, rng=g, valid=all(gr.values()), fails=[a for a, b in gr.items() if not b], size_cm=x['metrics'].get('size_cm'), relief_cm=x['metrics'].get('relief_cm')))
    out[k] = dict(plan=p, rows=rows)
json.dump(out, open(C.W + '/w3b1_seeds.json', 'w'), indent=1)
for k, v in out.items(): print(k, v['plan'], [(r['s'], r['r'], r['rng'], r['valid'], r['fails']) for r in v['rows']])
