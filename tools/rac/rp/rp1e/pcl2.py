import sys,numpy as np, bpy, json
from mathutils.bvhtree import BVHTree
from scipy.sparse.csgraph import connected_components
from scipy.sparse import coo_matrix
sys.path.insert(0,'/home/claude/stc/rp1e'); from l4map2 import l4face
a=sys.argv[sys.argv.index('--')+1:]
z=np.load(a[0]); V=z['V']; Q=z['Q']; polys=[list(map(int,q[q>=0])) for q in Q]; sv=[set(q) for q in polys]
cg=np.load(a[1]); col=np.load(a[1].replace('.npz','_col.npy')); fm=l4face(cg['F'])
fcol=np.array([np.bincount(col[f[f>=0]]).argmax() for f in cg['F']])[fm]
t=BVHTree.FromPolygons(V.tolist(),polys,all_triangles=False,epsilon=0.0); pr=np.array([(i,j) for i,j in t.overlap(t) if i<j and not (sv[i]&sv[j])])
print('pairs',len(pr))
if len(pr)==0: sys.exit()
C=V[np.array(polys)[pr[:,0]]].mean(1)
from scipy.spatial import cKDTree
kd=cKDTree(C); e=np.array(list(kd.query_pairs(1.0)))
n=len(C); g=coo_matrix((np.ones(len(e)),(e[:,0],e[:,1])),shape=(n,n)) if len(e) else coo_matrix((n,n))
k,lab=connected_components(g,directed=False)
out=[]
for c in range(k):
    m=lab==c; cc=C[m].mean(0)*np.array([1,-1,1]); cols=sorted(set(fcol[pr[m,0]].tolist())|set(fcol[pr[m,1]].tolist()))
    out.append((int(m.sum()),cc.round(2).tolist(),cols))
for o in sorted(out,reverse=True): print(o)
np.save(a[0].replace('.npz','_prs.npy'),pr)
