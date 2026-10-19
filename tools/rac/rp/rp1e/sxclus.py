import numpy as np, sys
from scipy.cluster.hierarchy import fcluster, linkage
C=np.load(sys.argv[1])*np.array([1,-1,1]); lo=np.array([float(x) for x in sys.argv[2].split(',')]); hi=np.array([float(x) for x in sys.argv[3].split(',')])
C=C[((C>lo)&(C<hi)).all(1)]
if len(C)<2: print(len(C)); sys.exit()
idx=np.random.RandomState(0).choice(len(C),min(len(C),4000),replace=False); Cs=C[idx]
L=fcluster(linkage(Cs,'single'),1.0,'distance')
for k in np.unique(L):
    m=L==k; print(k,m.sum(),Cs[m].mean(0).round(1),Cs[m].min(0).round(1),Cs[m].max(0).round(1))
