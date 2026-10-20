import sys,numpy as np, bpy
from mathutils.bvhtree import BVHTree
from scipy.cluster.hierarchy import fcluster, linkage
z=np.load(sys.argv[sys.argv.index('--')+1]); V=z['V']; Q=z['Q']; polys=[list(map(int,q[q>=0])) for q in Q]; sv=[set(q) for q in polys]
t=BVHTree.FromPolygons(V.tolist(),polys,all_triangles=False,epsilon=0.0); pr=np.array([(i,j) for i,j in t.overlap(t) if i<j and not (sv[i]&sv[j])])
C=V[np.array(polys)[pr[:,0]]].mean(1)*np.array([1,-1,1]); print('pairs',len(pr))
idx=np.random.default_rng(0).choice(len(C),min(len(C),4000),replace=False); lab=fcluster(linkage(C[idx],'single'),0.5,'distance')
for n,c in sorted([((lab==k).sum(),C[idx][lab==k].mean(0).round(1).tolist()) for k in set(lab)],reverse=True)[:14]: print(n,c)
