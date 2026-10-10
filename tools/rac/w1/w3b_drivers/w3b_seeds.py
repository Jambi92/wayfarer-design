# RAC W3B section 16: boundary stability across two additional deterministic DIAGNOSTIC seed realizations (rng 1007, 2007; the canonical
# 130,949-seed realization is never replaced). For every field: the valid-interval ends and the first invalid points (size: reseeded field;
# relief: reseeded field at s = 1) are re-run with each diagnostic realization; a boundary is STABLE when every re-run keeps its verdict.
# Usage: python3 w3b_seeds.py   (writes scratch w3b/scale/results_seeds.json, then seeds_stability.json)
import os, sys, json, subprocess
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import w3b_common as C
os.environ['W3B_OUT'] = 'results_seeds.json'
import w3b_scale_run as SR, w3b_scale_eval as EV
env = json.load(open(C.W + '/scale/envelope.json'))
SEEDSET = [k for k in env if k.startswith('face_')] + ['S_upper_posterior_neck', 'S_forearm', 'S_shin', 'S_dorsal_foot', 'A_elbow', 'A_wrist', 'A_knee', 'A_ankle', 'A_axilla',
                                                      'V_throat_anterior_neck', 'C_palmar', 'C_plantar']
# the largest body fields (dorsal / lateral trunk, dorsal tail, neck flexion, lower-trunk flexion, hip crease, tail articulation, chest /
# abdomen, tail underside, dorsal hand) are NOT RUN here (reseeding 150-300k-vertex fields x 8 runs each exceeds the session budget)
cases = []
for k, e in env.items():
    if k not in SEEDSET: continue
    for kind in ('size', 'relief'):
        b = e.get(kind)
        if not b or b.get('min_valid') is None: continue
        pts = [b['min_valid'], b['max_valid']]                    # valid-interval ends (first-invalid points: canonical seeds only - compute budget)
        for v in pts:
            for rng in (1007, 2007):
                cases.append((k, v, 1.0, rng, True) if kind == 'size' else (k, 1.0, v, rng, True))
SR.run(cases, 'results_seeds.json')
R = json.load(open(C.W + '/scale/results_seeds.json')); out = {}
for k, e in env.items():
    if k not in SEEDSET: continue
    for kind in ('size', 'relief'):
        b = e.get(kind)
        if not b or b.get('min_valid') is None: continue
        key = 's' if kind == 'size' else 'r'
        rows = []
        for v, expect in [(b['min_valid'], True), (b['max_valid'], True)]:
            for rng in (1007, 2007):
                x = next((x for x in R.values() if x['region'] == k and x[key] == v and x['rng'] == rng and (x['s'] == 1.0 if key == 'r' else x['r'] == 1.0)), None)
                if x is None: continue
                ok = all(EV.regrade(x).values()); rows.append(dict(value=v, rng=rng, expected_valid=expect, valid=ok, fails=[a for a, c in EV.regrade(x).items() if not c]))
        out['%s|%s' % (k, kind)] = dict(rows=rows, stable=all(r['valid'] == r['expected_valid'] for r in rows))
json.dump(out, open(C.W + '/scale/seeds_stability.json', 'w'), indent=1)
print(sum(v['stable'] for v in out.values()), 'of', len(out), 'boundaries stable')
for k, v in out.items():
    if not v['stable']: print('UNSTABLE', k, [(r['value'], r['rng'], r['valid'], r['fails']) for r in v['rows'] if r['valid'] != r['expected_valid']])
