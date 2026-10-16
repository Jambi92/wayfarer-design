# RM-OT-05AC: sculpt PROTECTION mask for the 05AB1 clean baseline (same vertex order as the donor / AA baseline): 1 = protected
# (hands and feet by the 05AB rig groups, head above the neck minimum, free tail incl. its fused root as hidden by the shared body-only
# mask), feathered to 0 over FEATHER cm. Order 05AC s5 allows scripts to generate masks; this file only defines WHERE not to sculpt.
# Usage: python3 ac_protect_mask.py BASE_V_F.npz BASE_GLTF.npz BASE_BODYONLY.npz WEIGHTS_cp2.npz OUT.npy [FEATHER_CM=2]
import sys, json, numpy as np
from scipy.spatial import cKDTree
bp, gp, bop, wp, out = sys.argv[1:6]; FE = float(sys.argv[6]) if len(sys.argv) > 6 else 2.0
B = np.load(bp); V = B['V'].astype(float) * 100
W = np.load(wp); names = [str(x) for x in W['names']]; Wt = W['weights_welded'][W['welded_index']]
p = np.zeros(len(V))
for g in ('hand_L', 'hand_R', 'foot_L', 'foot_R'): p = np.maximum(p, (Wt[:, names.index(g)] > 0.02).astype(float))
p[V[:, 2] > 168.3] = 1.0
G = np.load(gp)['V'].astype(float); bo = np.load(bop)['V'].astype(float)              # glTF frame, metres
d, _ = cKDTree(bo).query(G); tail = (d > 1e-6) & (V[:, 2] <= 168.3)                      # removed by the body-only mask, below the neck
p[tail] = 1.0
core = p >= 1.0; dd, _ = cKDTree(V[core]).query(V[~core]); p[~core] = np.clip(1 - dd / FE, 0, 1)
np.save(out, p.astype(np.float32))
print(json.dumps(dict(vertices=len(V), protected=int(core.sum()), feathered=int(((p > 0) & ~core).sum()), tail_vertices=int(tail.sum()))))
