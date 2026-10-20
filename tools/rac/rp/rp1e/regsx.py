import sys,numpy as np, bpy
from mathutils.bvhtree import BVHTree
a=sys.argv[sys.argv.index('--')+1:]; z=np.load(a[0]); c=np.array(eval(a[1]))*np.array([1,-1,1]); R=float(a[2])
V=z['V']; Q=z['Q']; QC=V[Q].mean(1); sel=np.where(np.linalg.norm(QC-c,axis=1)<R+0.5)[0]
polys=[list(map(int,Q[i][Q[i]>=0])) for i in sel]; sv=[set(p) for p in polys]
t=BVHTree.FromPolygons(V.tolist(),polys,all_triangles=False,epsilon=0.0)
pr=[(i,j) for i,j in t.overlap(t) if i<j and not (sv[i]&sv[j])]
pc=[(QC[sel[i]]*np.array([1,-1,1])).round(2).tolist() for i,j in pr if np.linalg.norm(QC[sel[i]]-c)<R]
print('region pairs',len(pc)); 
from collections import Counter
print(Counter(tuple(np.round(np.array(p)/0.3)*0.3) for p in pc).most_common(8))
