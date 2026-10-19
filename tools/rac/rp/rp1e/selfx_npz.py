# usage: blender-python selfx_npz.py -- mesh.npz [mesh2.npz ...]  (V analysis cm, Q quads or F tris); prints self-intersecting pair count + zone summary
import sys, numpy as np, bpy, mathutils, json
from mathutils.bvhtree import BVHTree
for p in sys.argv[sys.argv.index('--') + 1:]:
    z = np.load(p); V = z['V']; P = z['Q'] if 'Q' in z.files else z['F']
    polys = [list(map(int, q[q >= 0])) for q in P]
    t = BVHTree.FromPolygons(V.tolist(), polys, all_triangles=False, epsilon=0.0)
    pairs = t.overlap(t)
    sv = [set(q) for q in polys]
    real = [(i, j) for i, j in pairs if i < j and not (sv[i] & sv[j])]
    C = np.array([V[polys[i]].mean(0) for i, j in real]) if real else np.zeros((0, 3))
    np.save(p.replace('.npz', '_sx.npy'), C)
    print('SELFX', p, len(real))
