import numpy as np, sys, json
from edgeloop import edgeloop
z=np.load(sys.argv[1]); V=z['V']; F=[list(map(int,f[f>=0])) for f in z['F']]
zs=[float(t) for t in sys.argv[2].split(',')]; out={}
edges=set()
for f in F:
    for i in range(len(f)): edges.add((f[i],f[(i+1)%len(f)]))
for side,cond in (('R',lambda p:p[0]<1.5),('L',lambda p:p[0]>1.5)):
    for z0 in zs:
        found=None
        for u,v in edges:
            if all(abs(V[w][2]-z0)<1.8 and cond(V[w]) and -62<V[w][1]<-25 for w in (u,v)):
                L,st=edgeloop(F,u,v)
                if st=='closed' and len(L)>=10 and all(abs(V[w][2]-z0)<2.5 for w in L): found=L; break
        out['%s%g'%(side,z0)]=found; print(side,z0,None if found is None else len(found))
json.dump(out,open(sys.argv[3],'w'))
