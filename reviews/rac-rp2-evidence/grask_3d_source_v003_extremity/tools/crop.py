# crop.py IN OUT "numpy-expr on x,f,z" [largest] : keep faces whose 3 verts satisfy expr (optionally only the largest connected piece)
import sys,numpy as np, scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
d=np.load(sys.argv[1]); V=d['V']; F=d['Q']; x,f,z=V.T
m=eval(sys.argv[3]); k=m[F].all(1); F2=F[k]; u=np.unique(F2); r=-np.ones(len(V),int); r[u]=np.arange(len(u)); V2=V[u]; F2=r[F2]
if len(sys.argv)>4:
    n=len(V2); e=np.r_[F2[:,[0,1]],F2[:,[1,2]]]; A=sp.coo_matrix((np.ones(len(e)),(e[:,0],e[:,1])),(n,n))
    nc,lab=connected_components(A,directed=False); big=np.bincount(lab).argmax(); kf=lab[F2[:,0]]==big
    F2=F2[kf]; u=np.unique(F2); r=-np.ones(n,int); r[u]=np.arange(len(u)); V2=V2[u]; F2=r[F2]
np.savez(sys.argv[2],V=V2,Q=F2)
