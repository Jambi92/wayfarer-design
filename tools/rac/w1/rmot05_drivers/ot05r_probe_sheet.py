import os, sys
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import ot05r_package as PK
S = PK.S; Q = S + '/rmot05r/q'
for k, p, l in (('SK218', S + '/w2c/sk/SKM218', 'Skarn 218'), ('GR218', S + '/w2c/b/GR218R/GR218R', 'Grask 218 current'), ('GRQ1', Q + '/GRQ1/GRQ1', 'Grask probe Q1'), ('GRQ2', Q + '/GRQ2/GRQ2', 'Grask probe Q2'),
                ('SK229', S + '/w3d/b/SKM229-C1R', 'Skarn 229'), ('GOREF', S + '/w2d/b/GOREF/GOREF', 'Gorrund 230.9 current'), ('GOQ1', Q + '/GOQ1/GOQ1', 'Gorrund probe Q1'), ('GOQ2', Q + '/GOQ2/GOQ2', 'Gorrund probe Q2')):
    PK.BODIES[k] = (p, l)
for v, n in (('F', 'front'), ('Q', 'front 3/4'), ('P', 'profile')):
    PK.row_sheet('probe_%s.jpg' % v, 'Correction probes vs current - %s - body only' % n, 'Quick probes on the accepted W2 routes (no composition grid); diagnostic.', ['SK218', 'GR218', 'GRQ1', 'GRQ2', 'SK229', 'GOREF', 'GOQ1', 'GOQ2'], v, headless=True)
