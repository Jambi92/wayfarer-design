import sys, numpy as np, bpy
from mathutils.bvhtree import BVHTree
a=sys.argv[sys.argv.index('--')+1:]
z=np.load(a[0]);V=z['V'];F=z['F']
polys=[list(map(int,f[f>=0])) for f in F];sv=[set(p) for p in polys]
t=BVHTree.FromPolygons(V.tolist(),polys,all_triangles=False,epsilon=0.0)
pairs=[(i,j) for i,j in t.overlap(t) if i<j and not (sv[i]&sv[j])]
print('SELFX',len(pairs))
import json;json.dump(pairs,open(a[1],'w'))
cs=np.array([V[polys[i]].mean(0) for i,_ in pairs]) if pairs else np.zeros((0,3))
for c in cs[:40]: print(c.round(1))
