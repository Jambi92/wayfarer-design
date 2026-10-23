# crease_box.py (bpy) MESH.npz ARM.npy OUT.npy x0 x1 f0 f1 u0 u1 : intersection points of arm vs trunk sheets inside a box
import sys, numpy as np, bpy, mathutils
from mathutils.bvhtree import BVHTree
a = sys.argv[sys.argv.index('--') + 1:]
z = np.load(a[0]); V = z['V']; Q = z['Q']; arm = np.load(a[1]) > 0.5; bx = [float(t) for t in a[3:9]]
C = V[Q].mean(1); inb = (C[:, 0] > bx[0]) & (C[:, 0] < bx[1]) & (C[:, 1] > bx[2]) & (C[:, 1] < bx[3]) & (C[:, 2] > bx[4]) & (C[:, 2] < bx[5])
T = np.r_[Q[inb][:, [0, 1, 2]], Q[inb][:, [0, 2, 3]]]
aT = T[arm[T].all(1)]; tT = T[(~arm[T]).all(1)]
ba = BVHTree.FromPolygons(V.tolist(), aT.tolist()); bt = BVHTree.FromPolygons(V.tolist(), tT.tolist())
def edges(TT): return np.unique(np.sort(np.r_[TT[:, [0, 1]], TT[:, [1, 2]], TT[:, [2, 0]]], 1), axis=0)
pts = []
for TT, B in ((aT, bt), (tT, ba)):
    for e in edges(TT):
        p, q = mathutils.Vector(V[e[0]]), mathutils.Vector(V[e[1]]); d = q - p
        loc = B.ray_cast(p, d.normalized(), d.length)[0]
        if loc is not None: pts.append(list(loc))
np.save(a[2], np.array(pts)); print('points', len(pts))
