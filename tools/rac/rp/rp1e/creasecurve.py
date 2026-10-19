import numpy as np, sys
from scipy.sparse.csgraph import minimum_spanning_tree, shortest_path
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
s=sys.argv[1]; C=np.load('crease_%s.npy'%s)[:,:3]
# keep main connected cluster
T=cKDTree(C); pairs=np.array(list(T.query_pairs(1.2)))
n=len(C); d=np.linalg.norm(C[pairs[:,0]]-C[pairs[:,1]],axis=1)
G=coo_matrix((d,(pairs[:,0],pairs[:,1])),shape=(n,n)).tocsr()
from scipy.sparse.csgraph import connected_components
k,lab=connected_components(G,directed=False); big=np.bincount(lab).argmax(); keep=np.where(lab==big)[0]
C2=C[keep]; G2=G[keep][:,keep]
M=minimum_spanning_tree(G2)
D=shortest_path(M,directed=False); a=np.unravel_index(np.argmax(np.where(np.isfinite(D),D,-1)),D.shape)
_,pred=shortest_path(M,directed=False,indices=a[0],return_predecessors=True)
path=[a[1]]
while path[-1]!=a[0]: path.append(pred[path[-1]])
P=C2[path]
# resample by arc length every 0.25 cm with light smoothing
L=np.r_[0,np.cumsum(np.linalg.norm(np.diff(P,axis=0),axis=1))]
t=np.arange(0,L[-1],0.25); Q=np.array([np.interp(t,L,P[:,i]) for i in range(3)]).T
from scipy.ndimage import uniform_filter1d
Q=uniform_filter1d(Q,5,axis=0,mode='nearest')
np.save('ccurve_%s.npy'%s,Q); print(s,'crease curve length %.1f cm, pts %d, ends'%(L[-1],len(Q)),Q[0].round(1),Q[-1].round(1),'cluster kept',len(keep),'/',n)
