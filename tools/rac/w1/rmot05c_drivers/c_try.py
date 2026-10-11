# RAC RM-OT-05C search: preview base-surface specs. Usage: python3 c_try.py SPECS.json TAG [comp]
# SPECS = {"GR": {cand: spec}, "GO": {cand: spec}}; renders a body-only row (F, P, Q, RQ) per race with Skarn + 05B + candidates.
import os, sys, json
import c_preview as P
sys.path.insert(0, P.W1 + '/rmot05_drivers'); import ot05r_package as PK
S = P.S; A = json.load(open(sys.argv[1])); tag = sys.argv[2]; comp = sys.argv[3] if len(sys.argv) > 3 else None
PK.R = S + '/rmot05c/rend_prev'; os.makedirs(PK.R, exist_ok=True); PK.SH = S + '/rmot05c/prevsheets'; os.makedirs(PK.SH, exist_ok=True)
GRB = S + '/w2c/b/GR5B218/GR5B218'; GOB = S + '/w2d/b/GO5BREF/GO5BREF'
PK.BODIES.update({'SK218': (S + '/w2c/sk/SKM218', 'SK 218'), 'SK229': (S + '/w3d/b/SKM229-C1R', 'SK 229'), 'GR5B': (GRB, 'GR 218 05B'), 'GO5B': (GOB, 'GO 230.9 05B')})
for race, base in (('GR', GRB), ('GO', GOB)):
    ids = ['SK218' if race == 'GR' else 'SK229', race + '5B']
    for c, spec in A.get(race, {}).items():
        bid = '%s_%s_%s' % (race, c, tag) + ('_' + comp if comp else '')
        info = P.envelope(base, spec, bid, comp)
        print(bid, json.dumps({k: v for k, v in info.items() if k != 'tissue'})[:900], flush=True)
        PK.BODIES[bid] = (P.PREV + '/' + bid, bid)
        for v in PK.VIEWS:
            f = '%s/%s_nh_%s.png' % (PK.R, bid, v[0])
            if os.path.exists(f): os.remove(f)
        ids.append(bid)
    if len(ids) > 2:
        for v in ('F', 'P', 'Q', 'RQ'):
            PK.row_sheet('p_%s_%s_%s%s.jpg' % (race, tag, v, '_' + comp if comp else ''), 'RM-OT-05C preview %s %s %s' % (race, tag, v), '', ids, v, headless=True)
