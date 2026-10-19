import numpy as np, sys, json
from scipy.spatial import cKDTree
d=np.load(sys.argv[1]); u=np.load(sys.argv[2])
Vd,Fd=d['V'],d['F']; Vu,Fu=u['V'],u['F']
t=cKDTree(Vd); dist,idx=t.query(Vu)
print('V',len(Vd),len(Vu),'F',len(Fd),len(Fu))
print('max dev mm',dist.max()*10,'bijective',len(set(idx))==len(Vu))
# topology under mapping
def fs(F,m=None):
    S=set()
    for f in F:
        f=[x for x in f if x>=0]
        if m is not None: f=[m[x] for x in f]
        S.add(frozenset(f))
    return S
same=fs(Fd)==fs(Fu,idx); print('topology identical',same)
# edges
from collections import Counter
E=Counter()
for f in Fu:
    f=[x for x in f if x>=0]
    for i in range(len(f)): E[tuple(sorted((f[i],f[(i+1)%len(f)])))]+=1
b=sum(1 for c in E.values() if c==1); nm=sum(1 for c in E.values() if c>2)
chi=len(Vu)-len(E)+len(Fu); print('boundary',b,'nonmanifold',nm,'euler',chi)
# orientation consistency: each edge used once in each direction
D=Counter()
for f in Fu:
    f=[x for x in f if x>=0]
    for i in range(len(f)): D[(f[i],f[(i+1)%len(f)])]+=1
bad=sum(1 for (a,b2),c in D.items() if c>1 or D.get((b2,a),0)!=1); print('orientation bad directed edges',bad)
# components
import scipy.sparse as sp, scipy.sparse.csgraph as cg
r=[];c=[]
for (a,b2) in E: r.append(a);c.append(b2)
n,_=cg.connected_components(sp.coo_matrix((np.ones(len(r)),(r,c)),shape=(len(Vu),)*2)); print('components',n)
json.dump(dict(maxdev_mm=float(dist.max()*10),topology_identical=bool(same),boundary=b,nonmanifold=nm,euler=chi,orient_bad=bad,components=int(n),V=len(Vu),F=len(Fu)),open(sys.argv[3],'w'),indent=1)
