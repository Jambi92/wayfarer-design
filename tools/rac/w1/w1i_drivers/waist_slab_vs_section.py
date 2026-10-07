# RAC W1i: measurement-layer waist levels read with +/-1 cm vertex slabs (arm_measure) vs exact plane sections (W1h CIB method),
# with the number of trunk vertices in each slab. Usage: python3 waist_slab_vs_section.py name=rest.npz ...
import sys, numpy as np
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1'); sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/w1i_drivers')
from arm_measure import load
import trunk_profile as TP
for a in sys.argv[1:]:
    k, p = a.split('=', 1); d = load(p); V = d['V'].astype(float); J = d['joints']; hd = lambda n: np.asarray(J[n][0], float)
    armw = np.maximum.reduce([d['w_' + q] for q in ('upperarm_l', 'upperarm_r', 'lowerarm_l', 'lowerarm_r', 'hand_l', 'hand_r', 'fingers_l', 'fingers_r')])
    trunk = d['keep'] & (armw < 0.2); TF = d['F'][trunk[d['F']].all(1)]; zs = np.linspace(hd('spine_01')[2], hd('spine_03')[2], 9)
    sl = [np.ptp(V[trunk & (np.abs(V[:, 2] - z) < 1)][:, 0]) for z in zs]; se = [TP.section(V, TF, z)[0] for z in zs]
    nv = [int((trunk & (np.abs(V[:, 2] - z) < 1)).sum()) for z in zs]
    print('%s levels spine_01 (crest, S5) -> spine_03, breadth cm' % k)
    print('  vertex slab  ' + ' '.join('%5.1f' % x for x in sl) + '   crest / narrowest above %.4f' % (sl[0] / min(sl[1:])))
    print('  plane section' + ' '.join('%5.1f' % x for x in se) + '   crest / narrowest above %.4f' % (se[0] / min(se[1:])))
    print('  vertices in slab ' + str(nv))
