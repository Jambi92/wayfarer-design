# RAC W3B evidence tables (markdown) from the scratch results: orbit (RM-UF-03), ridges (RM-UF-04), facial / body scale fields (RM-UF-04 /
# RM-UB-08), body extremes, seed stability, ridge x scale interaction. Usage: python3 w3b_tables.py OUT.md
import os, sys, json, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import w3b_common as C
W = C.W; L = []
def T(head, rows): L.append('| ' + ' | '.join(head) + ' |'); L.append('|' + '---|' * len(head)); [L.append('| ' + ' | '.join(str(x) for x in r) + ' |') for r in rows]; L.append('')
f = lambda x, n=3: ('%.' + str(n) + 'f') % x if isinstance(x, (int, float)) and x is not None else str(x)
# ---- orbit
O = json.load(open(W + '/orbit/results.json')); G = json.load(open(W + '/orbit/guards.json'))
L.append('## RM-UF-03 orbital spacing - all cases\n')
T(['corner', 'dx local', 'dx world (cm/side)', 'IOD (cm)', 'IOD %', 'IOD / bitemporal', 'globe IOD', 'strain lo / hi', 'platform %', 'lat. support', 'folds', 'fit %', 'asym', 'verdict'],
  [[g['corner'], f(g['dx_local'], 2), f(g['dx_world'], 3), f(g['IOD']), f(g['IOD_pct'], 1), f(g['IOD_over_cranial']), f(g['IOD_globe']), '%s / %s' % (f(g['strain_lo']), f(g['strain_hi'])), f(g['platform_pct'], 2), f(g['support']), g['flips'], f(g['fit_pct'], 1), f(g['asym'], 2), 'VALID' if g['valid'] else 'FAIL ' + ','.join(g['fails'])]
   for g in sorted(G, key=lambda g: (g['corner'], g['dx_local']))])
r0 = O['dx+0.00_ref']
L.append('Reference companions: ' + ', '.join('%s %s' % (k, f(r0[k])) for k in ('IOD', 'IOD_x', 'IOD_globe', 'cranial_width', 'platform_breadth', 'IOD_over_cranial', 'IOD_over_platform', 'medial_margin_sep', 'lateral_margin_span', 'centre_to_rostral_midline', 'lateral_support', 'ring_radius', 'ring_rms', 'aperture_fit', 'asym_cm')) + '\n')
# ---- ridges
if os.path.exists(W + '/ridge/envelope.json'):
    RE = json.load(open(W + '/ridge/envelope.json')); RR = json.load(open(W + '/ridge/results.json')); ref = RR['g1.00']
    L.append('## RM-UF-04 structural ridges - reference by family\n')
    T(['family', 'strength (core - flank, cm)', 'core height (cm)', 'plane-transition angle p90 (deg)', 'ridge flank slope p95 (deg)', 'legibility vs canonical scale relief'],
      [[k, f(v['strength_cm']), f(v['core_h_cm']), f(v['transition_deg_p90'], 1), f(ref['flank_slope_p95_deg'][k], 1), f(ref['legibility_ratio'][k], 2)] for k, v in ref['metric'].items()])
    L.append('## RM-UF-04 structural ridges - envelopes (m = hidden normalized strength, 1 = canonical)\n')
    T(['group', 'min valid m', 'max valid m', 'first invalid low', 'first invalid high', 'scaled-face legibility m_min'],
      [[k, v['min_valid'], v['max_valid'], v['first_invalid_low'], v['first_invalid_high'], ', '.join('%s %s' % (a, f(b, 2) if b is not None else 'none') for a, b in v['legibility_min_m'].items())] for k, v in RE.items()])
    L.append('### global sweep rows\n')
    T(['m', 'verdict', 'folds', 'strain p1 / p99'] + ['%s strength' % k for k in ('canthal', 'supraorbital', 'temporal', 'jugal', 'occipital', 'mandibular')],
      [[r['m'], 'VALID' if r['ok'] else 'FAIL ' + ','.join(r['fails']), r['folds'], '%s / %s' % (f(r['strain'][0]), f(r['strain'][1]))] + [f(r['strength'][k]) for k in ('canthal', 'supraorbital', 'temporal', 'jugal', 'occipital', 'mandibular')] for r in RE['global']['rows']])
# ---- scale fields
if os.path.exists(W + '/scale/envelope.json'):
    E = json.load(open(W + '/scale/envelope.json')); CAN = json.load(open(W + '/scale_canon_metrics.json'))
    for cls, title in (('face', 'RM-UF-04 facial scale fields'), (None, 'RM-UB-08 body scale fields')):
        L.append('## %s (multipliers on the canonical W2 field; physical values in cm)\n' % title)
        rows = []
        for k, e in E.items():
            if (cls == 'face') != (e['class'] == 'face'): continue
            s = e.get('size') or {}; r = e.get('relief') or {}; c = CAN[k]
            rows.append([k, e['class'], f(c['size_cm']), f(c['relief_cm'], 4), f(c['aspect']), f(c['span_deg'], 1),
                         '%s - %s' % (s.get('min_valid'), s.get('max_valid')) if s else 'NOT RUN', '%s - %s cm' % (f(s.get('min_valid_abs')), f(s.get('max_valid_abs'))) if s.get('min_valid_abs') else '',
                         '%s / %s' % (s.get('first_invalid_low'), s.get('first_invalid_high')) if s else '',
                         '%s - %s' % (r.get('min_valid'), r.get('max_valid')) if r else 'NOT RUN', '%s - %s cm' % (f(r.get('min_valid_abs'), 4), f(r.get('max_valid_abs'), 4)) if r.get('min_valid_abs') else '',
                         '%s / %s' % (r.get('first_invalid_low'), r.get('first_invalid_high')) if r else ''])
        T(['field', 'class', 'ref size', 'ref relief', 'ref aspect', 'ref span deg', 'size x valid', 'size abs', 'size first invalid (low / high)', 'relief x valid', 'relief abs', 'relief first invalid (low / high)'], rows)
if os.path.exists(W + '/extremes.json'):
    X = json.load(open(W + '/extremes.json')); L.append('## RM-UB-08 body extremes (canonical relief carried)\n')
    keys = sorted(next(iter(X.values())).keys())
    T(['field'] + list(X.keys()), [[k] + ['s%.2f %.0fdeg f%d' % (X[b][k]['stretch'], X[b][k]['span_deg'] or -1, X[b][k]['flips_canonical_relief']) if k in X[b] else '' for b in X] for k in keys])
if os.path.exists(W + '/extremes_clamp.json'):
    XC = json.load(open(W + '/extremes_clamp.json')); L.append('## RM-UB-08 relationship-aware relief clamps on the body extremes (largest tested relief multiplier with excess folds within tolerance)\n')
    T(['body', 'clamped fields: reachable relief max (envelope max)'], [[b, '; '.join('%s %s (%s)' % (k, v['reachable_rmax'] if v['reachable_rmax'] is not None else '< 0.5 (folds at canonical relief)', v['envelope_rmax']) for k, v in res.items() if v['clamped']) or 'none'] for b, res in XC.items()])
if os.path.exists(W + '/scale/seeds_stability.json'):
    S = json.load(open(W + '/scale/seeds_stability.json')); L.append('## Seed stability (diagnostic realizations rng 1007 / 2007)\n')
    T(['field / kind', 'stable', 'unstable rows'], [[k.replace('|', ' / '), v['stable'], '; '.join('%s rng%d %s' % (r['value'], r['rng'], ','.join(r['fails'])) for r in v['rows'] if r['valid'] != r['expected_valid'])] for k, v in S.items()])
if os.path.exists(W + '/interact/results.json'):
    I = json.load(open(W + '/interact/results.json')); L.append('## Ridge x facial scale interaction\n')
    T(['corner', 'ridge m', 'facial relief', 'facial size', 'min legibility (6 families)', 'new folds', 'face relief cm', 'face aspect', 'eye vis 0 / 10'],
      [[k, v['m'], v['r'], v['s'], f(v['min_legibility_required'], 2), v['new_folds'], f(v['face_relief_cm'], 4), f(v['face_aspect']), '%s / %s' % (f(v['eye_vis_0']), f(v['eye_vis_10']))] for k, v in I.items()])
open(sys.argv[1], 'w').write('\n'.join(L)); print(len(L), 'lines')
