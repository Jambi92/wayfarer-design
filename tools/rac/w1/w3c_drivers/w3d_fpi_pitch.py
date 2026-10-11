# RAC W3D: r3 FPI with head pitch +-3 deg about the eye midpoint for the human comparators (W1c cranio convention)
import os, sys, json, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(D))
import arm_measure as AM
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; R = '/home/claude/wayfarer-design/reviews'
B = {'MF-M-R': R + '/rac-w1c-evidence/geometry/MF-M-R', 'MF-F-R': R + '/rac-w1c-evidence/geometry/MF-F-R', 'MF-FACE-PROJ-MAX': R + '/rac-w1c-evidence/geometry/MF-FACE-PROJ-MAX',
     'GR (central)': R + '/rac-w1h-evidence/geometry/GR', 'GR239 (W2 body max)': S + '/w2c/b/GR239/GR239', 'GO (central)': R + '/rac-w1i-evidence/geometry/GO', 'GO251 (W2 body max)': S + '/w2d/b/GO251/GO251',
     'SK208-C1R': S + '/w3d/b/SK208-C1R', 'SKM190-C1R': S + '/w3d/b/SKM190-C1R', 'SKF190-C1R': S + '/w3d/b/SKF190-C1R', 'SKM190-C2': S + '/w3c/b/SKM190-C2', 'SKM190-C3 (rejected)': S + '/w3c/b/SKM190-C3',
     'MFF-PROJ-SENS (builder-chosen sensitivity)': S + '/w3d/b/MFF-PROJ-SENS', 'MFF203 (W2)': S + '/w2a/st/MFF203'}
out = {}
for k, p in B.items():
    d = np.load(p + '_r6.npz', allow_pickle=True); V = d['V'].astype(float); F = d['F']; keep = d['keep'].astype(bool)
    r = {a: AM.cranio(d, V, F, keep, a) for a in (0.0, -3.0, 3.0)}
    out[k] = dict(path=p.replace(S, '$S').replace(R, 'reviews'), FPI=r[0.0]['FPI'], FPI_m3=r[-3.0]['FPI'], FPI_p3=r[3.0]['FPI'], HL=r[0.0]['HL'])
    print(k.ljust(44), 'FPI %.4f  pitch %.4f / %.4f  HL %.2f' % (out[k]['FPI'], out[k]['FPI_m3'], out[k]['FPI_p3'], out[k]['HL']), flush=True)
json.dump(out, open(S + '/w3d/human_fpi.json', 'w'), indent=1)
