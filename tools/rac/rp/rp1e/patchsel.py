import numpy as np, json, sys
from collections import defaultdict
z=np.load(sys.argv[1]);V=z['V'];F=[[int(x) for x in f if x>=0] for f in z['F']]
L=np.array(json.load(open(sys.argv[2]))['line']); R=float(sys.argv[3])
def dseg(P,a,b):
    t=np.clip(((P-a)@(b-a))/((b-a)@(b-a)),0,1); return np.linalg.norm(P-(a+t[:,None]*(b-a)),axis=1)
def dl(P): return np.min([dseg(P,L[i],L[i+1]) for i in range(len(L)-1)],axis=0)
C=np.array([V[f].mean(0) for f in F]); dv=dl(V)
sel=[k for k,f in enumerate(F) if dl(C[k][None])[0]<R or min(dv[f])<R*0.6]
de=defaultdict(int)
for k in sel:
    f=F[k]
    for i in range(len(f)): de[(f[i],f[(i+1)%len(f)])]+=1
bd=[(a,b) for (a,b) in de if (b,a) not in de]; outs=defaultdict(int)
for a,b in bd: outs[a]+=1
print('faces',len(sel),'bnd edges',len(bd),'simple',max(outs.values())==1, 'interior verts',len(set(i for k in sel for i in F[k])-set(outs)))
print(json.dumps([F[k] for k in sel]))
