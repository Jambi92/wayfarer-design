# RAC W3B1 section 5 follow-up: the W3B 'seed-robust' inward step itself flipped on one extra realization for eyelid size max (x1.3),
# auricular size max (x1.5) and shin size min (x0.6). Bracket one further step inward on all four extra seeds (rng 1007 / 2007 / 3007 / 4007).
import os, sys, json
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import w3b_common as C, w3b_scale_run as SR, w3b_scale_eval as EV
cases = [(k, s, 1.0, g, True) for k, s in (('face_orbital_eyelid', 1.2), ('face_auricular', 1.3), ('S_shin', 0.7)) for g in (1007, 2007, 3007, 4007)]
SR.run(cases, 'results_w3b1_seeds2.json')
R = json.load(open(C.W + '/scale/results_w3b1_seeds2.json')); out = []
for x in R.values():
    gr = EV.regrade(x); out.append(dict(region=x['region'], s=x['s'], rng=x['rng'], valid=all(gr.values()), fails=[a for a, b in gr.items() if not b]))
json.dump(out, open(C.W + '/w3b1_seeds2.json', 'w'), indent=1); [print(o) for o in out]
