# m1wall.py IN_L4.npz META.json OUT.npz r : explicit per-wall final-resolution remap for the R-hand slit (order section 8)
import sys, json, numpy as np, scipy.sparse as sp
from scipy.sparse.csgraph import dijkstra, connected_components
sys.path.insert(0,'/home/claude/stc/rp1e')
from remaplib import remap_core
inp,metap,out=sys.argv[1:4]; r=float(sys.argv[4])
z=np.load(inp); V=z['V'].astype(float).copy(); Q=z['Q'].astype(np.int64); nq=len(Q)
w=np.load('/home/claude/stc/rp1/weld_a.npz'); S=w['V'].astype(float); SF=w['F'].astype(np.int64)
MK='/home/claude/wayfarer-design/reviews/rac-rp1e-evidence/m1_masks/'
Bw=np.load(MK+'Rhand_B_wall_source_faces.npy'); Cw=np.load(MK+'Rhand_C_wall_source_faces.npy')
t=json.load(open(metap))['crease']; fl=np.array([1,-1,1])
c=V[t].mean(0)
E=np.vstack([np.c_[Q[:,i],Q[:,(i+1)%4]] for i in range(4)]); E=np.unique(np.sort(E,1),axis=0)
L=np.linalg.norm(V[E[:,0]]-V[E[:,1]],axis=1)
G=sp.coo_matrix((L,(E[:,0],E[:,1])),shape=(len(V),len(V))).tocsr(); G=G.maximum(G.T)
def path(a,b,Gm=G):
    d,pred=dijkstra(Gm,indices=a,return_predecessors=True,limit=3.0); p=[b]
    while p[-1]!=a: p.append(pred[p[-1]]); assert p[-1]>=0
    return p[::-1]
chain=[t[0]]
for i in range(4): chain+=path(t[i],t[i+1])[1:]
# extensions from the crease ends to the region edge along the slit mid-plane (analysis y = +40.85), penalising off-plane edges
ym=40.85
pen=1.0+20.0*np.abs((V[E[:,0],1]+V[E[:,1],1])/2-ym)
Gp=sp.coo_matrix((L*pen,(E[:,0],E[:,1])),shape=(len(V),len(V))).tocsr(); Gp=Gp.maximum(Gp.T)
dist=np.linalg.norm(V-c,axis=1); shell=np.where((dist>r-0.35)&(dist<r-0.02))[0]; print("shell",len(shell))
def ext(a,up):
    cand=shell[(V[shell,2]>V[a,2]) if up else (V[shell,2]<V[a,2])]
    cand=cand[np.argsort(np.abs(V[cand,1]-ym))[:40]]
    d,pred=dijkstra(Gp,indices=a,return_predecessors=True,limit=4.0); b=cand[np.argmin(d[cand])]
    p=[b]
    while p[-1]!=a: p.append(pred[p[-1]])
    return p[::-1]
top=ext(t[4],True); bot=ext(t[0],False)
cutv=bot[::-1][:-1]+chain+top[1:]
cutE=set(tuple(sorted((cutv[i],cutv[i+1]))) for i in range(len(cutv)-1))
QC=V[Q].mean(1); inR=np.linalg.norm(QC-c,axis=1)<r
# face adjacency inside region, not across cut edges
fe=np.vstack([np.sort(np.c_[Q[:,i],Q[:,(i+1)%4]],1) for i in range(4)]); ff=np.tile(np.arange(nq),4)
o=np.lexsort((fe[:,1],fe[:,0])); fes=fe[o]; ffs=ff[o]; sm=(fes[1:]==fes[:-1]).all(1)
ea=ffs[:-1][sm]; eb=ffs[1:][sm]; ek=fes[:-1][sm]
ok=inR[ea]&inR[eb]&np.array([tuple(k) not in cutE for k in ek])
A=sp.coo_matrix((np.ones(ok.sum()),(ea[ok],eb[ok])),shape=(nq,nq)); n,lab=connected_components(A,directed=False)
def seedface(p):
    p=np.array(p)*fl; return int(np.argmin(np.where(inR,np.linalg.norm(QC-p,axis=1),1e9)))
fB=seedface([-33.9,-41.25,93.0]); fC=seedface([-33.9,-40.45,93.1])
assert lab[fB]!=lab[fC],'cut does not separate B and C sides'
info={}
for nm,fs_,excl in (('B',fB,Cw),('C',fC,Bw)):
    P=(lab==lab[fs_])&inR
    # fill holes inside the side patch
    cidx=np.where(~P)[0]; Ac=sp.coo_matrix((np.ones(len(ea)),(ea,eb)),shape=(nq,nq)).tocsr(); sub=Ac[cidx][:,cidx]; sub=sub+sub.T
    n2,l2=connected_components(sub,directed=False)
    if n2>1:
        big=np.bincount(l2).argmax(); P[cidx[l2!=big]]=True
    pf=np.where(P)[0]; pv=np.unique(Q[pf])
    de={}
    for f in pf:
        q=Q[f]
        for i in range(4): de[(q[i],q[(i+1)%4])]=1
    bd=[(a,b) for (a,b) in de if (b,a) not in de]; nxt=dict(bd)
    Bl=[bd[0][0]]
    while nxt[Bl[-1]]!=Bl[0]: Bl.append(nxt[Bl[-1]])
    assert len(Bl)==len(bd),(nm,'side patch boundary not one loop')
    allow=np.ones(len(SF),bool); allow[excl]=False
    newV,inf=remap_core(V,Q,pf,pv,Bl,S,SF[allow],c,r); moved=pv[~np.isin(pv,Bl)]; V[moved]=newV[moved]; info[nm]=inf
np.savez_compressed(out,V=V,F=z['F'],Q=Q); print(info,'cut verts',len(cutv))
