# Refinement surgery on the CURRENT Gate 1 mesh: re-surface only where the refined field differs; zip; relax a narrow band.
import numpy as np, sys, igl
from scipy.sparse import coo_matrix, diags
from scipy.sparse.csgraph import dijkstra, connected_components
from helpers import clip, largest, loops
import g1
base=np.load("/tmp/claude-0/rodin/p9/g12_body.npz"); VB0=base["V"].astype(np.float64); FB0=base["F"].astype(np.int64); nA=0
m=np.load("/tmp/claude-0/rodin/c10/hb4.npz"); Vm=m["v"].astype(np.float64); Fm=m["f"].astype(np.int64)
k=np.round(Vm/1e-4).astype(np.int64); u,inv=np.unique(k,axis=0,return_inverse=True); inv=inv.ravel(); Vw=np.zeros((len(u),3)); Vw[inv]=Vm
Fm=inv[Fm]; Fm=Fm[(Fm[:,0]!=Fm[:,1])&(Fm[:,1]!=Fm[:,2])&(Fm[:,0]!=Fm[:,2])]; Vm=Vw
# ---- which base vertices does the refinement change?
# Gate 6 pass 2: tail, pelvis, head, upper arms and thighs all move -> take the re-meshed surface everywhere except the
# feet (U < 17) and forearms/hands (|x| > 31, U < 112), where the field is unchanged so the seams close cleanly.
# Gate 6 closure: only where the field actually changes (head +8 %, posterior-pelvic closure): |new - old| > 0.08 cm
e1=np.load("e15_old.npy"); e2=np.load("e15_new.npy"); inbox=np.isfinite(e1)&np.isfinite(e2)
edited=inbox&(np.abs(e2-e1)>0.08)
print("field-changed verts",edited.sum())
LOCK_TAIL=~inbox          # locked: feet   # locked: tail, everything above U80, arms/hands, tail between legs   # locked: tail, neck/head, Gate-1 pelvis below U100, arms
print("edited base verts",edited.sum(),"of which in locked free tail:",(edited&LOCK_TAIL).sum())
E_=np.concatenate([FB0[:,[0,1]],FB0[:,[1,2]],FB0[:,[2,0]]]); w=np.linalg.norm(VB0[E_[:,0]]-VB0[E_[:,1]],axis=1)
G=coo_matrix((w,(E_[:,0],E_[:,1])),shape=(len(VB0),)*2).tocsr(); G=G.maximum(G.T)
d=dijkstra(G,indices=np.where(edited)[0],min_only=True,limit=2.0); mask=np.isfinite(d)&(d<=1.5)
mask&=~LOCK_TAIL
idx=np.where(mask)[0]; n,l=connected_components(G[idx][:,idx],directed=False); cnt=np.bincount(l)
keepc=cnt>=30; mask[:]=False; mask[idx[keepc[l]]]=True
idx=np.where(~mask)[0]; n,l=connected_components(G[idx][:,idx],directed=False); cnt=np.bincount(l)
for c in range(n):
    if cnt[c]<300: mask[idx[l==c]]=True                # fill only small holes (body and locked tail stay separate unmasked parts)
print("unmasked components",sorted(cnt)[-3:])
mask&=~LOCK_TAIL                                   # never take locked vertices (incl. tiny internal specks) into the patch
print("mask verts",mask.sum(),"components kept",keepc.sum())
# ---- signed geodesic zone scalar on the base mesh, transferred to the refinement surface
bi=np.unique(E_[mask[E_[:,0]]&~mask[E_[:,1]]][:,0]); bo=np.unique(E_[~mask[E_[:,0]]&mask[E_[:,1]]][:,0])
din=dijkstra(G,indices=bo,min_only=True,limit=40); dout=dijkstra(G,indices=bi,min_only=True,limit=40)
gz=np.where(mask,np.minimum(din,40),-np.minimum(dout,40)); hw=0.5*np.median(w); gz=np.where(mask,gz-hw,gz+hw)
sqd,fi,cp=igl.point_mesh_squared_distance(Vm,VB0,FB0); dd=np.sqrt(sqd); tri=FB0[fi]
bc=igl.barycentric_coordinates(cp,VB0[tri[:,0]],VB0[tri[:,1]],VB0[tri[:,2]]); gm=(gz[tri]*bc).sum(1)
gm=np.where(dd>1.0,np.maximum(gm,np.where(mask[tri].any(1),5.0,gm)),gm)
VA,FA=clip(VB0,FB0,gz,keep_pos=False); VB,FB=clip(Vm,Fm,gm,keep_pos=True)
# keep refinement components that border the hole (there may be several hole patches)
LA=[l for l in loops(FA) if len(l)>=3]
e=np.concatenate([FB[:,[0,1]],FB[:,[1,2]]]); A=coo_matrix((np.ones(len(e)),(e[:,0],e[:,1])),shape=(len(VB),)*2)
n,lb=connected_components(A,directed=False); lf=lb[FB[:,0]]; sizes=np.bincount(lf); FB=FB[sizes[lf]>200]
uu=np.unique(FB); rm=-np.ones(len(VB),int); rm[uu]=np.arange(len(uu)); VB=VB[uu]; FB=rm[FB]
LB=[l for l in loops(FB) if len(l)>=3]
print("hole loops",[len(l) for l in LA],"patch loops",[len(l) for l in LB])
nAa=len(VA); V=np.concatenate([VA,VB]); FB2=FB+nAa; LB=[l+nAa for l in LB]
def zipper(a,b):
    b=b[::-1]; j0=np.argmin(np.linalg.norm(V[b]-V[a[0]],axis=1)); b=np.roll(b,-j0); na,nb=len(a),len(b); i=j=0; out=[]
    while i<na or j<nb:
        ai,ai1=a[i%na],a[(i+1)%na]; bj,bj1=b[j%nb],b[(j+1)%nb]
        if j>=nb or (i<na and np.linalg.norm(V[ai1]-V[bj])<np.linalg.norm(V[bj1]-V[ai])): out.append([ai,ai1,bj]); i+=1
        else: out.append([ai,bj1,bj]); j+=1
    return np.array(out)[:,[0,2,1]]
br=[]; usedB=set(); extra=[]
for la in LA:
    if len(la)<30: extra.append(la); continue
    c=V[la].mean(0); cand=[(np.linalg.norm(V[lb_].mean(0)-c),k) for k,lb_ in enumerate(LB) if k not in usedB and len(lb_)>=30]
    if not cand: extra.append(la); continue
    dist,k=min(cand)
    if dist>8.0: extra.append(la); continue
    usedB.add(k); Z=zipper(la,LB[k]); g_=np.linalg.norm(V[Z[:,0]]-V[Z[:,1]],axis=1); print("zip",len(la),len(LB[k]),"gap mean %.2f max %.2f"%(g_.mean(),g_.max())); br.append(Z)
for la in extra+[LB[k] for k in range(len(LB)) if k not in usedB]:
    c=len(V); V=np.concatenate([V,V[la].mean(0)[None]]); br.append(np.array([[la[(i+1)%len(la)],la[i],c] for i in range(len(la))])); print("fan-filled loop",len(la))
F=np.concatenate([FA,FB2]+br)
ek=np.sort(np.concatenate([F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]),1); _,cc=np.unique(ek,axis=0,return_counts=True)
de=np.concatenate([F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]); _,cd=np.unique(de,axis=0,return_counts=True)
print("faces",len(F),"boundary",(cc==1).sum(),"nonmanifold",(cc>2).sum(),"orientation conflicts",(cd>1).sum())
# ---- provenance of every output vertex: map kept base vertices back to their base index (exact copies)
kd=igl.point_mesh_squared_distance  # not needed; use exact coordinate match
from scipy.spatial import cKDTree
dd0,ii0=cKDTree(VB0).query(V[:nAa]); is_base=(dd0<1e-9)
origin=np.full(len(V),-1); origin[:nAa][is_base]=ii0[is_base]
seam=np.unique(np.concatenate([z.ravel() for z in br]))
# ---- narrow relaxation band around the new seam; locked free tail never moves
E2=np.concatenate([F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]); w2=np.linalg.norm(V[E2[:,0]]-V[E2[:,1]],axis=1)
G2=coo_matrix((w2,(E2[:,0],E2[:,1])),shape=(len(V),)*2).tocsr(); G2=G2.maximum(G2.T)
A2=coo_matrix((np.ones(len(E2)),(E2[:,0],E2[:,1])),shape=(len(V),)*2).tocsr(); A2=((A2+A2.T)>0).astype(float)
deg=np.asarray(A2.sum(1)).ravel(); L=diags(1/np.maximum(deg,1))@A2
BAND=1.8; ds=dijkstra(G2,indices=seam,min_only=True,limit=BAND+0.5); wb=np.where(np.isfinite(ds),np.clip(1-ds/BAND,0,1),0.0)
locked=np.zeros(len(V),bool); locked[:nAa]=is_base&LOCK_TAIL[np.clip(origin[:nAa],0,None)]
wb[locked]=0; V0=V.copy()
for _ in range(25): V=V+(0.5*wb)[:,None]*((L@V)-V)
# light Taubin clean-up of the NEW patch interior only (meshing noise); copied Gate-1 vertices never move here
newv=np.zeros(len(V),bool); newv[nAa:]=True; wt=newv*np.clip(1-wb,0,1)
for _ in range(6): V=V+(0.5*wt)[:,None]*((L@V)-V); V=V+(-0.53*wt)[:,None]*((L@V)-V)
mv=np.linalg.norm(V-V0,axis=1)
# drop floating debris (tiny disconnected pieces inherited from earlier surgeries)
e_=np.concatenate([F[:,[0,1]],F[:,[1,2]]]); A_=coo_matrix((np.ones(len(e_)),(e_[:,0],e_[:,1])),shape=(len(V),)*2)
nc_,lab_=connected_components(A_,directed=False); big_=np.argmax(np.bincount(lab_)); keepv=lab_==big_
print("components",nc_,"dropped debris verts",(~keepv).sum())
F=F[keepv[F[:,0]]]; rm_=-np.cumsum(~keepv); newidx=np.arange(len(V))+rm_; newidx[~keepv]=-1
V=V[keepv]; F=newidx[F]; origin=origin[keepv]; mv=mv[keepv]; nAa=int(keepv[:nAa].sum())
ek=np.sort(np.concatenate([F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]),1); _,cc=np.unique(ek,axis=0,return_counts=True)
print("after cleanup faces",len(F),"boundary",(cc==1).sum(),"nonmanifold",(cc>2).sum())
np.savez("/tmp/claude-0/rodin/c10/g13a_body.npz",V=V,F=F,origin=origin,nAa=nAa,moved=mv)
# ---- accounting vs the current Gate 1 mesh
kept=origin>=0; unchanged=kept&(mv<1e-9)
print("output verts",len(V),"| identical copies of Gate-1 verts:",unchanged.sum(),"| copied then relaxed:",(kept&(mv>=1e-9)).sum(),"(max %.2f cm)"%mv[kept].max(),"| new:",(~kept).sum())
gone=np.setdiff1d(np.arange(len(VB0)),origin[kept]); print("Gate-1 verts replaced:",len(gone),"of which locked free tail:",LOCK_TAIL[gone].sum(),"of which original B1 (idx<nA):",(gone<nA).sum())
moved_base=origin[kept&(mv>=1e-9)]; print("relaxed copies in locked tail:",LOCK_TAIL[moved_base].sum(),"; relaxed copies that are original B1:",(moved_base<nA).sum())
np.save("/tmp/claude-0/rodin/c10/a13_gone.npy",gone)
