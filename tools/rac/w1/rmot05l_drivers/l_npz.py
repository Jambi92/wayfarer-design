# RAC RM-OT-05L: wrap a concept OBJ for the neutralized body-only review / blind renderer (ot05r_package.ensure):
# V, F, keep = all vertices; w_head marks the head and neck above the neck-root cut (z > CUT), w_neck_01 = 0.
# The cut height is chosen on this body (neck root), the same body-only neutralization as the controls (head and neck removed).
# Usage: python3 l_npz.py IN.obj OUT_PREFIX [cut_z]   -> OUT_PREFIX_r6.npz
import sys, numpy as np
V = np.array([[float(t) for t in l.split()[1:4]] for l in open(sys.argv[1]) if l.startswith('v ')], np.float32)
F = np.array([[int(t) - 1 for t in l.split()[1:4]] for l in open(sys.argv[1]) if l.startswith('f ')], np.int32)
cut = float(sys.argv[3]) if len(sys.argv) > 3 else 195.0
np.savez(sys.argv[2] + '_r6.npz', V=V, F=F, keep=np.ones(len(V), bool), w_head=(V[:, 2] > cut).astype(np.float32), w_neck_01=np.zeros(len(V), np.float32))
print(sys.argv[2], len(V), 'cut', cut)
