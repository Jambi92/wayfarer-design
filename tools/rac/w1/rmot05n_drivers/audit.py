# REF<->LOW same-structure audit on the two fields: section breadth / depth / area at fixed heights (trunk, left leg, left arm),
# body volume. Usage: audit.py REF.npz LOW.npz OUT.json
import sys, json, numpy as np
from scipy import ndimage as ndi
R = {}
for tag, fn in [('REF', sys.argv[1]), ('LOW', sys.argv[2])]:
    d = np.load(fn); S = d['S']; lo = d['lo']; h = float(d['h']); xs = lo[0] + h * np.arange(S.shape[0]); ys = lo[1] + h * np.arange(S.shape[1])
    r = dict(volume_L=round(float((S < 0).sum() * h ** 3 / 1000), 1))
    for name, z, pick in [('thorax_170', 170, 'trunk'), ('lower_thorax_155', 155, 'trunk'), ('waist_138', 138, 'trunk'), ('pelvis_115', 115, 'trunk'),
                          ('thigh_85', 85, 'leg'), ('knee_58', 58, 'leg'), ('calf_42', 42, 'leg'), ('ankle_20', 20, 'leg'),
                          ('upper_arm_150', 150, 'arm'), ('elbow_140', 140, 'arm'), ('forearm_128', 128, 'arm'), ('wrist_114', 114, 'arm')]:
        k = int(round((z - lo[2]) / h)); s = S[:, :, k] < 0
        s = s & ((np.abs(xs) < 29)[:, None] if pick == 'trunk' else ((xs > 0) & (xs < 42))[:, None] if pick == 'leg' else (xs > 27)[:, None])
        L, n = ndi.label(s); best = None
        for i in range(1, n + 1):
            w = np.where(L == i); x = xs[w[0]]; y = ys[w[1]]; a = len(x) * h * h
            ok = True
            if ok and (best is None or a > best[2]): best = (x.max() - x.min() + h, y.max() - y.min() + h, a)
        r[name] = dict(breadth=round(best[0], 1), depth=round(best[1], 1), area=round(best[2])) if best else None
    R[tag] = r
json.dump(R, open(sys.argv[3], 'w'), indent=1)
for k in R['REF']:
    a, b = R['REF'][k], R['LOW'][k]
    if isinstance(a, dict): print('%-17s REF b%5.1f d%5.1f a%5d | LOW b%5.1f d%5.1f a%5d | area %+5.1f%%' % (k, a['breadth'], a['depth'], a['area'], b['breadth'], b['depth'], b['area'], 100 * (b['area'] - a['area']) / a['area']))
    else: print(k, a, b, '%+.1f%%' % (100 * (b - a) / a))
