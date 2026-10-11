# RAC RM-UF-05: build the first 8 faces of selected Skarn diagnostic batches (seed 101) on the accepted SKM190 body (height macro held),
# mapping anchor-scale DIR values to the MPFB targets used in W3C / W3D (C1R neck 0.30 held). Diagnostic only.
import os, sys, json, subprocess, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import uf05_spaces as SP
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; R = S + '/rmuf05'; os.makedirs(R + '/ov', exist_ok=True); os.makedirs(R + '/b', exist_ok=True)
def targets(v):
    t = {'neck-scale-horiz-incr': 0.30, 'head-scale-horiz-incr': max(v['head_w'], 0), 'head-scale-depth-incr': max(v['head_d'], 0), 'nose-scale-vert-incr': max(v['nose_v'], 0), 'chin-jaw-drop-incr': max(v['jaw_drop'], 0)}
    for k, inc, dec in (('brow', 'eyebrows-trans-forward', 'eyebrows-trans-backward'), ('cheek', 'LR:cheek-bones-incr', 'LR:cheek-bones-decr'), ('nose_h', 'nose-scale-horiz-incr', 'nose-scale-horiz-decr'),
                        ('nose_d', 'nose-scale-depth-incr', 'nose-scale-depth-decr'), ('jaw_w', 'chin-bones-incr', 'chin-bones-decr')):
        if v[k] >= 0: t[inc] = float(v[k])
        else: t[dec] = float(-v[k])
    return {k: round(float(x), 4) for k, x in t.items()}
todo = []
for cond in sys.argv[1:]:
    z = np.load('%s/batches/SK_%s_101.npz' % (R, cond)); names = list(z['names']); X = SP.denorm(SP.HUMAN, names, z['U'][:8])
    for i, x in enumerate(X):
        bid = 'SK-%s-%d' % (cond, i); ov = '%s/ov/%s.json' % (R, bid); json.dump({'targets': targets(dict(zip(names, x)))}, open(ov, 'w'), indent=1); todo.append((bid, ov))
for bid, ov in todo:
    if os.path.exists('%s/b/%s_r6.npz' % (R, bid)): continue
    subprocess.run(['python3', 'build_variant.py', S + '/w2b/st/SKM190_build.json', ov, R + '/b', bid], cwd=os.path.dirname(D), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print('built', bid, flush=True)
