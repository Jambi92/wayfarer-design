import sys, json
import b_preview as P
sys.path.insert(0, P.W1 + '/rmot05_drivers'); import ot05r_package as PK
S = P.S; A = json.load(open(sys.argv[1])); tag = sys.argv[2]
print('GR', P.envelope(S + '/w2c/b/GRA218/GRA218', A['GR'], 'GRB' + tag)['max_change_cm'])
print('GO', P.envelope(S + '/w2d/b/GOA229/GOA229', A['GO'], 'GOB' + tag)['max_change_cm'])
PK.R = S + '/rmot05b/rend'; import os; os.makedirs(PK.R, exist_ok=True); PK.SH = P.PREV
for k, p, l in (('SK', S + '/w2c/sk/SKM218', 'SK 218'), ('GRW', S + '/w2c/b/GR218R/GR218R', 'GR 218 W2'), ('GRA', S + '/w2c/b/GRA218/GRA218', 'GR 218 05A'),
                ('GRB' + tag, P.PREV + '/GRB' + tag, 'GR 218 05B ' + tag), ('GOW', S + '/w2d/b/GO229/GO229', 'GO 229 W2'), ('GOA', S + '/w2d/b/GOA229/GOA229', 'GO 229 05A'),
                ('GOB' + tag, P.PREV + '/GOB' + tag, 'GO 229 05B ' + tag)):
    PK.BODIES[k] = (p, l)
for b in ('GRB' + tag, 'GOB' + tag):
    for v in PK.VIEWS:
        f = '%s/%s_nh_%s.png' % (PK.R, b, v[0])
        if os.path.exists(f): os.remove(f)
for v in ('F', 'P', 'Q', 'RQ'):
    PK.row_sheet('p_%s_%s.jpg' % (tag, v), 'RM-OT-05B preview %s %s body only' % (tag, v), '', ['SK', 'GRW', 'GRA', 'GRB' + tag, 'GOW', 'GOA', 'GOB' + tag], v, headless=True)
