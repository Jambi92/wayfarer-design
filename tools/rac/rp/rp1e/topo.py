import numpy as np, sys, collections
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
z=np.load(sys.argv[1]); V=z['V']; F=[list(map(int,f[f>=0])) for f in z['F']]
E=collections.Counter(); D=collections.Counter()
for f in F:
    for i in range(len(f)): a,b=f[i],f[(i+1)%len(f)]; E[(min(a,b),max(a,b))]+=1; D[(a,b)]+=1
r=[a for a,b in E]; c=[b for a,b in E]; n,_=connected_components(coo_matrix((np.ones(len(r)),(r,c)),shape=(len(V),len(V))),directed=False)
print('V',len(V),'F',len(F),'quads',sum(len(f)==4 for f in F),'tris',sum(len(f)==3 for f in F),'bnd',sum(v==1 for v in E.values()),'nm',sum(v>2 for v in E.values()),
 'orient_bad',sum(1 for (a,b),k in D.items() if k>1 or (b,a) not in D),'comp',n,'euler',len(V)-len(E)+len(F),'min_edge',round(min(np.linalg.norm(V[a]-V[b]) for a,b in E),4),
 'unused',len(V)-len(set(i for f in F for i in f)))
