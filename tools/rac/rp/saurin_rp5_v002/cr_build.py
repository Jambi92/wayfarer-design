import numpy as np; np.trapz = np.trapezoid
import sys, os; sys.path.insert(0, 'w2i4_drivers'); sys.path.insert(0, 'w2i_drivers'); sys.path.insert(0, 'w3b_drivers')
import sa_build as B, sa_finish as FN
states = {'BRD': dict(B.BRD), 'T80': B.tail(80, 1.22), 'FAHI': {'fat': 1.0}, 'MUHI': {'muscle': 1.0}}
for k, p in states.items():
    f = '/tmp/claude-0/rt/sa/cr_%s.npy' % k
    if os.path.exists(f): continue
    P, q, kk, info = FN.build_f(dict(p)); np.save(f, P.astype(np.float32)); print(k, P.shape, flush=True)
