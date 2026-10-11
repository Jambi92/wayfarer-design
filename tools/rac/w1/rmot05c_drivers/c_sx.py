# RM-OT-05C search: self-intersection count + dominant region of preview bodies. Usage: python3 c_sx.py ID...
import sys, collections, numpy as np, c_guard as G, c_preview as P
for n in sys.argv[1:]:
    p = n if n.startswith('/') else P.PREV + '/' + n
    B = np.load(p + '_r6.npz', allow_pickle=True); print(n, G.self_x(B['V'].astype(float), B['F'], B['keep'].astype(bool)), flush=True)
