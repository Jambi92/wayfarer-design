import numpy as np, sys
from scipy.spatial import cKDTree
from scipy.cluster.hierarchy import fcluster, linkage
a,b,L=sys.argv[1],sys.argv[2],sys.argv[3] if len(sys.argv)>3 else 'L4'
A=np.load('sim_%s_%s_sx.npy'%(a,L))[:,:3]*np.array([1,-1,1]); B=np.load('sim_%s_%s_sx.npy'%(b,L))[:,:3]*np.array([1,-1,1])
d,_=cKDTree(A).query(B); N=B[d>0.3]
print('new pairs (not near base)',len(N),'of',len(B))
if len(N)>1:
    P=N[np.random.default_rng(0).choice(len(N),min(len(N),3000),replace=False)]
    lab=fcluster(linkage(P,'single'),0.6,'distance'); r=sorted([((lab==k).sum(),P[lab==k].mean(0).round(1).tolist()) for k in set(lab)],reverse=True)[:10]
    for x in r: print(x)
