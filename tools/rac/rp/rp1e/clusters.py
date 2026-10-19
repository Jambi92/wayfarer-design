# clusters.py DSP zone_name limit : connected clusters (by proximity 1.0) of source points over limit
import numpy as np, sys
from scipy.spatial import cKDTree
from scipy.sparse.csgraph import connected_components
from scipy.sparse import coo_matrix
S=np.load('/home/claude/stc/rp1/weld.npz')['V']; z=np.load('/home/claude/stc/rp1/zones.npz'); zone=z['zone']; names=list(z['names'])
d=np.load(sys.argv[1]); zn=sys.argv[2]; lim=float(sys.argv[3])
m=(d>lim)&(zone==names.index(zn)) if zn!='all' else (d>lim)
idx=np.where(m)[0]; P=S[idx]
T=cKDTree(P); pr=T.query_pairs(1.0,output_type='ndarray')
A=coo_matrix((np.ones(len(pr)),(pr[:,0],pr[:,1])),shape=(len(P),len(P)))
n,lab=connected_components(A,directed=False)
cl=sorted([(np.sum(lab==k),k) for k in range(n)],reverse=True)
print(zn,'over',lim,'pts',len(P),'clusters',n)
for c,k in cl[:int(sys.argv[4]) if len(sys.argv)>4 else 25]:
    Q=P[lab==k]; dd=d[idx[lab==k]]
    print('%6d  max %5.1f  med %4.1f  centre %s  bbox %s..%s'%(c,dd.max(),np.median(dd),Q.mean(0).round(1),Q.min(0).round(0),Q.max(0).round(0)))
