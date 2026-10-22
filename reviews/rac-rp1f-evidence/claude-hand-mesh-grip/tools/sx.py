# sx.py IN.npz [OUT.npy] : production self-intersections (quad BVH overlap, pairs sharing no vertex) — bpy python
import sys,numpy as np,json
import bpy
from mathutils.bvhtree import BVHTree
z=np.load(sys.argv[1]); V=z['V']*np.array([1,-1,1]); Q=z['Q']
sel=None
if len(sys.argv)>3:  # optional region: x,y,z,r
    c=np.array([float(x) for x in sys.argv[3].split(',')]); sel=np.where(np.linalg.norm(V[Q].mean(1)-c[:3],axis=1)<c[3])[0]
Qs=Q if sel is None else Q[sel]
t=BVHTree.FromPolygons(V.tolist(),Qs.tolist(),all_triangles=False,epsilon=0.0)
pr=np.array(t.overlap(t),int).reshape(-1,2); pr=pr[pr[:,0]<pr[:,1]]
if len(pr):
    a=Qs[pr[:,0]]; b=Qs[pr[:,1]]
    share=(a[:,:,None]==b[:,None,:]).any((1,2)); pr=pr[~share]
if sel is not None and len(pr): pr=sel[pr]
print('self-intersecting quad pairs',len(pr))
if len(pr):
    C=V[Q[pr[:,0]]].mean(1); 
    from scipy.spatial import cKDTree
    import scipy.sparse as sp; from scipy.sparse.csgraph import connected_components
    e=np.array(list(cKDTree(C).query_pairs(0.5))); n=len(C)
    g=sp.coo_matrix((np.ones(len(e)),(e[:,0],e[:,1])),shape=(n,n)) if len(e) else sp.coo_matrix((n,n)); k,lab=connected_components(g,directed=False)
    for c in range(k):
        m=lab==c; print('  cluster',int(m.sum()),C[m].mean(0).round(2).tolist())
if len(sys.argv)>2: np.save(sys.argv[2],pr)
