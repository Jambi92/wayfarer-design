# blender-python sxpairs.py -- mesh.npz : prints intersecting polygon pairs with centres
import sys, numpy as np, bpy
from mathutils.bvhtree import BVHTree
p=sys.argv[sys.argv.index('--')+1]
z=np.load(p); V=z['V']*np.array([1,-1,1]); P=z['Q'] if 'Q' in z.files else z['F']
polys=[list(map(int,q[q>=0])) for q in P]
t=BVHTree.FromPolygons(V.tolist(),polys,all_triangles=False,epsilon=0.0)
sv=[set(q) for q in polys]
for i,j in t.overlap(t):
    if i<j and not (sv[i]&sv[j]): print('PAIR',i,j,V[polys[i]].mean(0).round(1).tolist(),V[polys[j]].mean(0).round(1).tolist())
