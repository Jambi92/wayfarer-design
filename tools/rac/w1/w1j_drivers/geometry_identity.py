# RAC W1j: max |dV| between the retained candidate's W1j rebuilds (sens7 base 'W0*') and the committed W1i meshes.
import sys, json, numpy as np
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; R = '/home/claude/wayfarer-design/reviews/rac-w1i-evidence'
pairs = {"reference": (S + '/w1g/sens6/W0_r6.npz', R + '/geometry/GO_r6.npz'), "true 208 cm": (S + '/w1g/sens6/W0-208_r6.npz', R + '/go-variants/GO-H208_r6.npz'),
         "215 donor": (S + '/w1g/sens6/W0-215_r6.npz', R + '/go-variants/GO-H215_r6.npz'), "222 donor": (S + '/w1g/sens6/W0-222_r6.npz', R + '/go-variants/GO-H222_r6.npz'),
         "251 donor (GOR-BODY-03)": (S + '/w1g/sens6/W0-03_r6.npz', R + '/go-variants/GOR-BODY-03_r6.npz'), "skeleton": (S + '/w1g/sens6/W0-LEAN_r6.npz', R + '/skeleton/GO-LEAN_r6.npz')}
out = {k: float(np.abs(np.load(a)['V'] - np.load(b)['V']).max()) for k, (a, b) in pairs.items()}
json.dump(out, open(sys.argv[1], 'w'), indent=1); print(out)
