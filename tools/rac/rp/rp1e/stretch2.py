import numpy as np, sys
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
z=np.load(sys.argv[1]);V=z['V']*np.array([1,-1,1]);Q=z['Q']; r=float(sys.argv[2]) if len(sys.argv)>2 else 4
E=np.max([np.linalg.norm(V[Q[:,i]]-V[Q[:,(i+1)%4]],axis=1) for i in range(4)],axis=0)
Emin=np.min([np.linalg.norm(V[Q[:,i]]-V[Q[:,(i+1)%4]],axis=1) for i in range(4)],axis=0)
C=V[Q].mean(1); kd=cKDTree(C); _,nn=kd.query(C,k=40); loc=np.median(E[nn],axis=1)
m=(E>r*loc)&(E>0.15); print('stretched faces:',m.sum())
Cm=C[m]
if m.sum():
    pr=cKDTree(Cm).query_pairs(0.8,output_type='ndarray'); A=coo_matrix((np.ones(len(pr)),(pr[:,0],pr[:,1])),shape=(len(Cm),len(Cm))); n,lab=connected_components(A,directed=False)
    rows=sorted([( int((lab==k).sum()), Cm[lab==k].mean(0).round(2).tolist(), round(float(E[m][lab==k].max()),2)) for k in range(n)],reverse=True)
    for rr in rows[:30]: print(rr)
np.save(sys.argv[1].replace('.npz','_str.npy'),np.where(m)[0])
