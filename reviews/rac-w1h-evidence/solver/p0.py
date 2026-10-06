import sys, json, numpy as np, time
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/w1h_drivers')
import gn5
x0 = [1.0315,1.045,1.2644,1.1941,0.9368,1.186,0.9608,1.1122,1.6,1.65,0.92,1.1619,1.4,1.2688,0.95,1.05,1.02]
t = time.time(); m, lab, H, C = gn5.slacks(np.array(x0), 'P0')
print('time %.0f H %.2f sumneg %.4f' % (time.time() - t, H, -m[m < 0].sum()))
for k in np.where(m < 0)[0]: print('  neg', lab[k], round(m[k], 4))
for l in lab:
    if 'clearance' in l or 'flare' in l or 'TB' in l: print('  ', l)
