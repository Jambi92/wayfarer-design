# neck splice seam (Gate 6 head-patch boundary) traced through the provenance chain onto the cleanup mesh
import numpy as np, sys
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra
G='/tmp/claude-0/rodin/g1/'
g9=np.load(G+'g9_body.npz')['origin']; g11=np.load(G+'g11_body.npz')['origin']; g13a=np.load('g13a_body.npz')['origin']; b=np.load('g13b_body.npz')
V=b['V'].astype(float); F=b['F'].astype(np.int64); keep=b['KEEP']; n=len(V)
o=g13a[keep]                        # -> g12 index (g12 = g11 indexing, tail fix kept indices)
new6=np.zeros(n,bool); k=o>=0; o2=g11[o[k]]; kk=o2>=0; t=np.zeros(k.sum(),bool); t[kk]=g9[o2[kk]]<0; new6[np.where(k)[0]]=t
x,f,u=V.T; E=np.concatenate([F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]); seamE=E[new6[E[:,0]]!=new6[E[:,1]]]; sv=np.unique(seamE.ravel()); neck=sv[(u[sv]>150)&(u[sv]<176)]
w=np.linalg.norm(V[E[:,0]]-V[E[:,1]],axis=1); Gm=coo_matrix((w,(E[:,0],E[:,1])),shape=(n,n)).tocsr()
ds=dijkstra(Gm,indices=neck,min_only=True,limit=6.0); np.save('neckseam13.npy',ds); print('neck seam verts',len(neck))
