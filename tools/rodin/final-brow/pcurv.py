import numpy as np, igl, sys
from scipy.sparse import coo_matrix, diags
z=np.load(sys.argv[1]); V=z['v'].astype(float); F=z['f'].astype(np.int64)
k=np.round(V/1e-4).astype(np.int64); u,inv=np.unique(k,axis=0,return_inverse=True); inv=inv.ravel(); W=np.zeros((len(u),3)); W[inv]=V; V=W; F=inv[F]
F=F[(F[:,0]!=F[:,1])&(F[:,1]!=F[:,2])&(F[:,0]!=F[:,2])]
np.savez(sys.argv[1].replace('p_','pn_'),P=V.astype(np.float32),f=F)
L=igl.cotmatrix(V,F); M=igl.massmatrix(V,F,igl.MASSMATRIX_TYPE_VORONOI)
Hn=-diags(1/np.maximum(M.diagonal(),1e-12))@(L@V); N=igl.per_vertex_normals(V,F); H=0.5*np.einsum('ij,ij->i',Hn,N)
n=len(V); E=np.concatenate([F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]); A=coo_matrix((np.ones(len(E)),(E[:,0],E[:,1])),shape=(n,n)).tocsr(); A=((A+A.T)>0).astype(float)
Lu=diags(1/np.asarray(A.sum(1)).ravel())@A
for _ in range(6): H=Lu@H
t=np.clip(H/1.2,-1,1); C=np.zeros((n,3),np.float32); C[:]=0.6
C[t>0]=np.stack([0.6+0.4*t[t>0],0.6-0.4*t[t>0],0.6-0.4*t[t>0]],1); C[t<0]=np.stack([0.6+0.4*t[t<0],0.6+0*t[t<0],0.6-0.4*t[t<0]],1)
np.savez(sys.argv[2],P=V.astype(np.float32),f=F,C=C)
