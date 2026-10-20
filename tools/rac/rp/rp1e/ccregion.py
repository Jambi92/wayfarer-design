# ccregion.py IN.npz OUT.npz "faceexpr" : one Catmull-Clark step on a face region R (faces whose vertex positions satisfy the
# python expression in P (n,3 array of that face's verts), e.g. "(P[:,1]<-53).all() and (P[:,0]>19).all()").
# Region-boundary edges get midpoints, region-boundary verts stay fixed; outside faces touching split edges are re-tiled
# (pentagon -> quad+tri, hexagon -> 2 quads). Colours: new verts take the colour of a parent vertex.
import sys, numpy as np
from collections import defaultdict
sys.path.insert(0,'/home/claude/stc/rp1e')
from orient import check
inp,out,expr=sys.argv[1:4]
z=np.load(inp); V=z['V'].astype(float); F=[list(map(int,f[f>=0])) for f in z['F']]; col=np.load(inp.replace('.npz','_col.npy'))
R=set(k for k,f in enumerate(F) if eval(expr,{'np':np},{'P':V[f]}))
ef=defaultdict(list); vf=defaultdict(list)
for k,f in enumerate(F):
    for i in range(len(f)): ef[frozenset((f[i],f[(i+1)%len(f)]))].append(k); vf[f[i]].append(k)
NV=[list(p) for p in V]; NC=list(col)
def add(p,c): NV.append(list(p)); NC.append(c); return len(NV)-1
fp={k:add(V[F[k]].mean(0),col[F[k][0]]) for k in R}
ep={}
for e,ks in ef.items():
    kin=[k for k in ks if k in R]
    if not kin: continue
    a,b=tuple(e)
    if len(kin)==2: p=(V[a]+V[b]+NVa(kin) if False else (V[a]+V[b]+np.array(NV[fp[kin[0]]])+np.array(NV[fp[kin[1]]]))/4)
    else: p=(V[a]+V[b])/2
    ep[e]=add(p,col[a])
interior=[v for v in vf if all(k in R for k in vf[v])]
for v in interior:
    ks=vf[v]; n=len(set(u for k in ks for u in F[k] if frozenset((u,v)) in ef and u!=v and frozenset((u,v)) in ep))
    es=[e for e in ef if v in e]
    n=len(es); Q=np.mean([NV[fp[k]] for k in ks],axis=0); Rm=np.mean([(V[list(e)[0]]+V[list(e)[1]])/2 for e in es],axis=0)
    NV[v]=list((Q+2*Rm+(n-3)*V[v])/n)
G=[]
for k,f in enumerate(F):
    m=len(f)
    if k in R:
        for i in range(m):
            a=f[i]; G.append([a,ep[frozenset((a,f[(i+1)%m]))],fp[k],ep[frozenset((a,f[(i-1)%m]))]])
    else:
        g=[]
        for i in range(m):
            g.append(f[i]); e=frozenset((f[i],f[(i+1)%m]))
            if e in ep: g.append(ep[e])
        if len(g)==m: G.append(g); continue
        if len(g)==5:
            # quad+tri: tri on the split edge's far side
            j=[i for i,x in enumerate(g) if x>=len(V)][0]
            r=g[j:]+g[:j]  # r[0]=mid
            G.append([r[0],r[1],r[2],r[3]]); G.append([r[0],r[3],r[4]])
        elif len(g)==6:
            j=[i for i,x in enumerate(g) if x>=len(V)][0]; r=g[j:]+g[:j]
            G.append([r[0],r[1],r[2],r[3]]); G.append([r[0],r[3],r[4],r[5]])
        elif len(g)==4: G.append(g)   # triangle with one split edge -> quad
        else:
            c=add(V[f].mean(0),col[f[0]]); 
            for i in range(len(g)): G.append([c,g[i],g[(i+1)%len(g)]])
d,b=check(G); assert not d and not b,(d,b)
Fa=np.full((len(G),4),-1)
for k,g in enumerate(G):
    assert len(g)<=4,len(g); Fa[k,:len(g)]=g
np.savez_compressed(out,V=np.array(NV),F=Fa); np.save(out.replace('.npz','_col.npy'),np.array(NC))
print('region faces',len(R),'V',len(NV),'F',len(G),'tris',sum(len(g)==3 for g in G))
