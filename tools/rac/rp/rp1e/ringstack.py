# ringstack.py CAGE v0 v1 dirsign : starting from the edge loop through (v0,v1), step ring by ring in the direction where z increases (dirsign=+1) and report
import numpy as np, sys, collections, json
from edgeloop import edgeloop
z=np.load(sys.argv[1]); V=z['V']; F=[list(map(int,f[f>=0])) for f in z['F']]
e2f=collections.defaultdict(list)
for k,f in enumerate(F):
    for i in range(len(f)): e2f[frozenset((f[i],f[(i+1)%len(f)]))].append(k)
L,st=edgeloop(F,int(sys.argv[2]),int(sys.argv[3])); sg=float(sys.argv[4]); rings=[L]; out=sys.argv[5] if len(sys.argv)>5 else None
for step in range(int(sys.argv[6]) if len(sys.argv)>6 else 20):
    r=rings[-1]; n=len(r); nxt=[]
    ok=True
    for i in range(n):
        a,b=r[i],r[(i+1)%n]; fs=e2f[frozenset((a,b))]
        prev=set(rings[-2]) if len(rings)>1 else set()
        cand=[F[k] for k in fs if len(F[k])==4 and not (set(F[k])&prev - {a,b})]
        # choose the face on the side away from the previous ring
        if len(rings)==1:
            cand=[q for q in cand if np.mean([V[v][2] for v in q if v not in (a,b)])*sg>np.mean([V[a][2],V[b][2]])*sg] or cand
        if len(cand)!=1: ok=False; break
        q=cand[0]; ia=q.index(a); ib=q.index(b)
        # opposite vertices: the one adjacent to a (not b) and adjacent to b (not a)
        na=q[(ia-1)%4] if q[(ia+1)%4]==b else q[(ia+1)%4]
        nxt.append(na)
    if not ok or len(set(nxt))!=n: print('stop at step',step,'ok',ok); break
    rings.append(nxt)
for k,r in enumerate(rings):
    P=V[r]; print(k,len(r),'centroid',P.mean(0).round(1),'z %.1f..%.1f'%(P[:,2].min(),P[:,2].max()))
if out: json.dump([[int(v) for v in r] for r in rings],open(out,'w'))
