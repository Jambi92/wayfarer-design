# split.py IN.obj x0 x1 OUTPREFIX : remove faces in the slab x0<cx<x1, find components, reassign slab faces to the nearest big component
import sys, numpy as np, scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree
V=np.array([[float(t) for t in l.split()[1:4]] for l in open(sys.argv[1]) if l.startswith('v ')])
F=np.array([[int(t)-1 for t in l.split()[1:4]] for l in open(sys.argv[1]) if l.startswith('f ')])
x0,x1=float(sys.argv[2]),float(sys.argv[3]); C=V[F].mean(1); slab=(C[:,0]>x0)&(C[:,0]<x1)
q=np.round(V*1e3).astype(np.int64); _,inv=np.unique(q,axis=0,return_inverse=True); inv=inv.ravel(); Fm=inv[F]; n=inv.max()+1
K=Fm[~slab]; A=sp.coo_matrix((np.ones(len(K)*3),(np.r_[K[:,0],K[:,1],K[:,2]],np.r_[K[:,1],K[:,2],K[:,0]])),shape=(n,n))
nc,lab=connected_components(A,directed=False); fl=np.full(len(F),-1); fl[~slab]=lab[Fm[~slab,0]]
cnt=np.bincount(fl[fl>=0]); big=np.argsort(-cnt)[:2]; print('components',nc,'top',cnt[np.argsort(-cnt)[:6]])
# assign slab + small comps to nearest of the two big ones (by face centroid)
for b in big: pass
tree=[cKDTree(C[fl==b]) for b in big]
rest=~np.isin(fl,big); d=np.stack([t.query(C[rest])[0] for t in tree]); fl[rest]=big[np.argmin(d,0)]
for i,b in enumerate(big):
    m=fl==b; sub=F[m]; vi=np.unique(sub); mp=-np.ones(len(V),int); mp[vi]=np.arange(len(vi))
    with open('%s_%d.obj'%(sys.argv[4],i),'w') as o:
        for v in V[vi]: o.write('v %.4f %.4f %.4f\n'%tuple(v))
        for t in mp[sub]: o.write('f %d %d %d\n'%tuple(t+1))
    print(i, m.sum(), V[vi].min(0).round(1), V[vi].max(0).round(1))
