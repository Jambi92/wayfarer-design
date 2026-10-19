# blender-python selfx_pairs.py -- mesh.npz : saves _pairs.npy (i,j face ids of intersecting quads)
import sys, numpy as np, bpy, mathutils
from mathutils.bvhtree import BVHTree
for p in sys.argv[sys.argv.index('--') + 1:]:
    z = np.load(p); V = z['V']; P = z['Q'] if 'Q' in z.files else z['F']
    polys = [list(map(int, q[q >= 0])) for q in P]
    t = BVHTree.FromPolygons(V.tolist(), polys, all_triangles=False, epsilon=0.0)
    sv = [set(q) for q in polys]
    real = [(i, j) for i, j in t.overlap(t) if i < j and not (sv[i] & sv[j])]
    np.save(p.replace('.npz', '_pairs.npy'), np.array(real, int).reshape(-1, 2)); print('PAIRS', p, len(real))
