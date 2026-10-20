# refine.py IN.npz SPEC.json OUT.npz : one local Catmull-Clark step on a face patch (graded support refinement).
# SPEC: {"centre":[x,y,z],"R":r} or {"line":[[..],..],"R":r} or {"facev":[[..]]}; "ccpos":true (CC positions) ; "holdbnd":true
# Patch faces split into quads (n-gon -> n quads via face point + edge points). Faces outside the patch that touch a split
# edge become polygons with the inserted edge points; they are split into quads/tris by a fan from their first inserted point.
import sys, json, numpy as np
from collections import defaultdict
inp,specp,out=sys.argv[1:4]; S=json.load(open(specp))
z=np.load(inp); V=z['V'].astype(float); F=[[int(x) for x in f if x>=0] for f in z['F']]; col=np.load(inp.replace('.npz','_col.npy'))
C=np.array([V[f].mean(0) for f in F])
if 'facev' in S: P=[k for k,f in enumerate(F) if any(set(f)==set(q) for q in S['facev'])]
elif 'line' in S:
    L=np.array(S['line'])
    def dl(X):
        return np.min([np.linalg.norm(X-(L[i]+np.clip(((X-L[i])@(L[i+1]-L[i]))/((L[i+1]-L[i])@(L[i+1]-L[i])),0,1)[:,None]*(L[i+1]-L[i])),axis=1) for i in range(len(L)-1)],axis=0)
    P=[k for k in range(len(F)) if dl(C[k][None])[0]<S['R']]
else: P=[k for k in range(len(F)) if np.linalg.norm(C[k]-np.array(S['centre']))<S['R']]
Ps=set(P)
ef=defaultdict(list)
for k,f in enumerate(F):
    for i in range(len(f)): ef[tuple(sorted((f[i],f[(i+1)%len(f)])))].append(k)
split=set(e for k in P for e in [tuple(sorted((F[k][i],F[k][(i+1)%len(F[k])]))) for i in range(len(F[k]))])
NV=[list(p) for p in V]; NC=list(col)
def add(p,c): NV.append(list(p)); NC.append(int(c)); return len(NV)-1
fp={k:add(C[k],np.bincount(col[F[k]]).argmax()) for k in P}
ep={}
for e in split:
    a,b=e; fs=ef[e]
    if S.get('ccpos',True) and all(k in Ps for k in fs) and len(fs)==2: p=(V[a]+V[b]+C[fs[0]]+C[fs[1]])/4
    else: p=(V[a]+V[b])/2
    ep[e]=add(p, col[a] if col[a]==col[b] else min(col[a],col[b]))
# CC vertex update for vertices whose whole star is in the patch
if S.get('ccpos',True):
    star=defaultdict(list)
    for k,f in enumerate(F):
        for v in f: star[v].append(k)
    for v,ks in star.items():
        if all(k in Ps for k in ks):
            n=len(ks); Q=np.mean([C[k] for k in ks],axis=0)
            nb=set()
            for k in ks:
                f=F[k]; i=f.index(v); nb.add(f[i-1]); nb.add(f[(i+1)%len(f)])
            R=np.mean([(V[v]+V[u])/2 for u in nb],axis=0); NV[v]=list((Q+2*R+(len(nb)-3)*V[v])/len(nb))
G=[]
for k,f in enumerate(F):
    n=len(f)
    if k in Ps:
        for i in range(n):
            a=f[i]; e1=ep[tuple(sorted((f[i-1],a)))]; e2=ep[tuple(sorted((a,f[(i+1)%n])))]
            G.append([a,e2,fp[k],e1])
    else:
        poly=[]
        for i in range(n):
            a,b=f[i],f[(i+1)%n]; poly.append(a); e=tuple(sorted((a,b)))
            if e in split: poly.append(ep[e])
        if len(poly)==n: G.append(f); continue
        # rotate to start at an inserted point, fan into quads/tris
        ins=[i for i,v in enumerate(poly) if v>=len(V)]; s0=ins[0]; poly=poly[s0:]+poly[:s0]
        rest=poly[1:]
        while len(rest)>=3: G.append([poly[0]]+rest[:3]); rest=rest[2:]
        if len(rest)==2: G.append([poly[0]]+rest)
NV=np.array(NV); Fa=np.full((len(G),4),-1)
for k,f in enumerate(G): Fa[k,:len(f)]=f
np.savez_compressed(out,V=NV,F=Fa); np.save(out.replace('.npz','_col.npy'),np.array(NC)); np.save(out.replace('.npz','_remap.npy'),np.arange(len(V)))
print('patch',len(P),'split edges',len(split),'V',len(NV),'F',len(G))
