import sys, numpy as np, json, bpy
from mathutils.bvhtree import BVHTree
z=np.load(sys.argv[1]); V=z['V'].astype(float); Q=z['Q']
t=BVHTree.FromPolygons(V.tolist(),Q.tolist(),all_triangles=False,epsilon=0.0)
pr=np.array(t.overlap(t),int).reshape(-1,2); pr=pr[pr[:,0]<pr[:,1]]
if len(pr): A=Q[pr[:,0]];B=Q[pr[:,1]]; pr=pr[~(A[:,:,None]==B[:,None,:]).any((1,2))]
print('PAIRS',len(pr)); np.save(sys.argv[2],pr)
if len(pr):
    c=V[Q[pr]].mean((1,2))
    for nm,mk in (('crotch',np.abs(c[:,0])<6),('L',c[:,0]>=6),('R',c[:,0]<=-6)):
        if mk.any(): print(nm,mk.sum(),np.round(c[mk].mean(0),1))
