# RAC W2I4 wrapper: runs the accepted gate-1 g7surfc.py UNCHANGED on the finished base, with the g7geo construction anchors it reads (claw /
# palmar-plantar pad centres, eye centres) carried to the finished base by the displacement of the nearest frozen upsampled vertex (the F2 /
# L1 rebuild raises the hands by ~6 cm; feet and eyes do not move). Usage (cwd = gate-1 dir): python3 g7surfc_moved.py FROZEN_UP FIN_UP REG OUT
import sys, os, numpy as np, runpy
sys.path.insert(0, os.getcwd())
from scipy.spatial import cKDTree
import g7geo as G
A = np.load(sys.argv[1])['V'].astype(float); Bv = np.load(sys.argv[2])['V'].astype(float); tr = cKDTree(A)
mv = lambda c: np.asarray(c, float) + (Bv[tr.query(c)[1]] - A[tr.query(c)[1]])
_cp = G.world_claws_pads; _ey = G.eyes_world
def claws_pads():
    segs, pads = _cp()
    segs2 = [tuple(mv(x) if (hasattr(x, '__len__') and len(np.shape(x)) == 1 and len(x) == 3) else x for x in s) for s in segs]
    return segs2, [(mv(c), rp, kind) for c, rp, kind in pads]
def eyes():
    e, er, yaw = _ey(); return [mv(c) for c in e], er, yaw
G.world_claws_pads = claws_pads; G.eyes_world = eyes
sys.argv = ['g7surfc.py'] + sys.argv[2:]
runpy.run_path('g7surfc.py', run_name='__main__')
