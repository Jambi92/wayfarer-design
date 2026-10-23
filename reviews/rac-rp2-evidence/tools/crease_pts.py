# crease_pts.py (bpy) BASE.npz REGION.npy OUT.npy : intersection points between arm and trunk sheets of the region neighbourhood
import sys, numpy as np, bpy, mathutils
from mathutils.bvhtree import BVHTree
a = sys.argv[sys.argv.index('--') + 1:]
z = np.load(a[0]); V = z['V']; Q = z['Q']; R = np.load(a[1]); arm = np.load(a[2]) > 0.5
# neighbourhood: region quads + 3 rings
nb = R.copy()
vq = {}
for i, q in enumerate(Q):
    for v in q: vq.setdefault(v, []).append(i)
for _ in range(3):
    for v in np.unique(Q[nb]): nb[vq[v]] = True
T = np.r_[Q[nb][:, [0, 1, 2]], Q[nb][:, [0, 2, 3]]]
aT = T[arm[T].all(1)]; tT = T[(~arm[T]).all(1)]
ba = BVHTree.FromPolygons(V.tolist(), aT.tolist()); bt = BVHTree.FromPolygons(V.tolist(), tT.tolist())
pts = []
def edges(TT): return np.unique(np.sort(np.r_[TT[:, [0, 1]], TT[:, [1, 2]], TT[:, [2, 0]]], 1), axis=0)
for TT, B in ((aT, bt), (tT, ba)):
    for e in edges(TT):
        p, q = mathutils.Vector(V[e[0]]), mathutils.Vector(V[e[1]]); d = q - p; L = d.length
        loc, nrm, idx, dist = B.ray_cast(p, d.normalized(), L)
        if loc is not None: pts.append(list(loc))
np.save(a[3], np.array(pts)); print('crease points', len(pts))
