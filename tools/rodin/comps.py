import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
z=np.load('mesh.npz'); v=z['v']; f=z['f']; n=len(v)
r=np.concatenate([f[:,0],f[:,1],f[:,2]]); c=np.concatenate([f[:,1],f[:,2],f[:,0]])
A=coo_matrix((np.ones(len(r)),(r,c)),shape=(n,n))
nc,lab=connected_components(A,directed=False)
cnt=np.bincount(lab); order=np.argsort(-cnt)
print("components",nc)
fl=lab[f[:,0]]; fc=np.bincount(fl,minlength=nc)
rows=[]
for i in order:
    m=lab==i; p=v[m]; lo,hi=p.min(0),p.max(0)
    rows.append((i,cnt[i],fc[i],*lo,*hi))
for rw in rows[:60]:
    print("%5d v=%7d f=%7d  X %.3f..%.3f  Y %.3f..%.3f  Z %.3f..%.3f"%(rw[0],rw[1],rw[2],rw[3],rw[6],rw[4],rw[7],rw[5],rw[8]))
print("small comps (<200v):",(cnt<200).sum(),"verts in them",cnt[cnt<200].sum())
np.save('lab.npy',lab)
