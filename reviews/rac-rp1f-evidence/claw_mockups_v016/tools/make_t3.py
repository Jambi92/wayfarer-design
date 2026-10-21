# make_t3.py OUT.npz : rebuild the mockup base t3 = v014 production + v015 whisker pads + v015 toe claws, hands still v014
import sys, numpy as np, os
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, '..', '..', '..')
z = np.load(os.path.join(R, 'rac-rp1e-evidence/designs/design_v014_production_L4.npz')); d = np.load(os.path.join(H, '../params/t3_delta_from_v014.npz'))
V = z['V'].copy(); V[d['idx']] = d['V']; np.savez_compressed(sys.argv[1], V=V, F=z['F'], Q=z['Q'])
