import numpy as np, sys
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra, connected_components
import g1
P1=g1.P1; f1=g1.f1
e=g1.field(P1[:,0],P1[:,1],P1[:,2])
edited=np.abs(e)>0.08
print("edited verts",edited.sum())
E_=np.concatenate([f1[:,[0,1]],f1[:,[1,2]],f1[:,[2,0]]]); w=np.linalg.norm(P1[E_[:,0]]-P1[E_[:,1]],axis=1)
G=coo_matrix((w,(E_[:,0],E_[:,1])),shape=(len(P1),)*2).tocsr(); G=G.maximum(G.T)
d=dijkstra(G,indices=np.where(edited)[0],min_only=True,limit=2.5)
mask=np.isfinite(d)&(d<=2.0)
# clean: drop small masked islands, fill small unmasked holes
def comps(sel):
    idx=np.where(sel)[0]; sub=G[idx][:,idx]; n,l=connected_components(sub,directed=False); return idx,n,l
idx,n,l=comps(mask); cnt=np.bincount(l); keep=cnt==cnt.max(); mask[:]=False; mask[idx[keep[l]]]=True
idx,n,l=comps(~mask); cnt=np.bincount(l); big=cnt.argmax()
for k in range(n):
    if k!=big: mask[idx[l==k]]=True
print("mask verts",mask.sum(),"islands",n)
np.save("b1_mask.npy",mask); np.save("b1_edit_e.npy",e)
