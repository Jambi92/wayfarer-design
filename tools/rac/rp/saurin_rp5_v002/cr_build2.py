import numpy as np; np.trapz = np.trapezoid
import sys, os; os.chdir('/home/claude/wayfarer-design/tools/rac/w1'); sys.path.insert(0, 'w2i4_drivers'); sys.path.insert(0, 'w2i_drivers')
import sa_build as B, sa_finish as FN
states = {'LT90': ({'trunk_len': 0.90}, None), 'T55': (B.tail(55, 0.83), None), 'MIN': ({'muscle': -1.0, 'fat': -1.0}, None), 'MUFAHI': ({'muscle': 1.0, 'fat': 1.0}, None),
          'B-T80': (B.Mx(B.BRD, B.tail(80, 1.16)), None), 'M168': ({}, 168.0), 'M208-B': (dict(B.BRD), 208.0), 'F-N': (B.Mx(B.CEN, B.NAR), None)}
for k, (p, h) in states.items():
    f = '/tmp/claude-0/rt/sa/cr_%s.npy' % k
    if os.path.exists(f): continue
    P, q, kk, info = FN.build_f(dict(p), h); np.save(f, P.astype(np.float32)); print(k, P.shape, flush=True)
