import numpy as np, sys, igl
from scipy.spatial import cKDTree
w=np.load('/home/claude/stc/rp1/weld.npz'); V=w['V'].astype(float); F=w['F'].astype(np.int64)
N=igl.per_vertex_normals(V,F)
lo=np.array([float(x) for x in sys.argv[1].split(',')]); hi=np.array([float(x) for x in sys.argv[2].split(',')]); thr=float(sys.argv[3])
m=((V>lo)&(V<hi)).all(1); idx=np.where(m)[0]; T=cKDTree(V[idx])
pairs=T.query_pairs(thr,output_type='ndarray')
a,b=idx[pairs[:,0]],idx[pairs[:,1]]
facing=(np.einsum('ij,ij->i',N[a],N[b])<-0.3)
# facing: normals opposed and the vector a->b along -N[a] (b is in front of a's outside)
d=V[b]-V[a]; facing&=(np.einsum("ij,ij->i",d,N[a])*float(sys.argv[5])>0)
S=np.unique(np.r_[a[facing],b[facing]])
print('slit/contact verts',len(S))
np.save(sys.argv[4],S)
from scipy.cluster.hierarchy import fcluster, linkage
P=V[S]
if len(P)>1:
    L=fcluster(linkage(P[np.random.RandomState(0).choice(len(P),min(len(P),5000),replace=False)],'single'),0.8,'distance')
    Ps=P[np.random.RandomState(0).choice(len(P),min(len(P),5000),replace=False)]
    for k in np.unique(L):
        mm=L==k
        if mm.sum()<5: continue
        print(k,mm.sum(),Ps[mm].mean(0).round(1),Ps[mm].min(0).round(1),Ps[mm].max(0).round(1))
