# Gate 1 assembly: cut original B1 and the re-surfaced edit zone along the SAME iso-line of a zone scalar, then zip.
import numpy as np, sys, igl
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra, connected_components
z=np.load("src.npz"); P1=z["P1"].astype(np.float64); f1=z["f1"].astype(np.int64)[:,[0,2,1]]   # flip: canonical axis swap mirrored the winding
mask=np.load("b1_mask.npy")
m=np.load(sys.argv[1] if len(sys.argv)>1 else "edit_mc.npz"); Vm=m["v"].astype(np.float64); Fm=m["f"].astype(np.int64)
_k=np.round(Vm/1e-4).astype(np.int64); _u,_inv=np.unique(_k,axis=0,return_inverse=True); _inv=_inv.ravel()
Vw=np.zeros((len(_u),3)); Vw[_inv]=Vm; Fm=_inv[Fm]; Fm=Fm[(Fm[:,0]!=Fm[:,1])&(Fm[:,1]!=Fm[:,2])&(Fm[:,0]!=Fm[:,2])]; Vm=Vw
print("welded MC verts",len(Vm))
# signed geodesic zone scalar on B1: + inside the mask, - outside, zero on the mask border
E_=np.concatenate([f1[:,[0,1]],f1[:,[1,2]],f1[:,[2,0]]]); w=np.linalg.norm(P1[E_[:,0]]-P1[E_[:,1]],axis=1)
G=coo_matrix((w,(E_[:,0],E_[:,1])),shape=(len(P1),)*2).tocsr(); G=G.maximum(G.T)
border_in=np.unique(E_[mask[E_[:,0]]&~mask[E_[:,1]]][:,0]); border_out=np.unique(E_[~mask[E_[:,0]]&mask[E_[:,1]]][:,0])
din=dijkstra(G,indices=border_out,min_only=True,limit=60); dout=dijkstra(G,indices=border_in,min_only=True,limit=60)
g=np.where(mask,np.minimum(din,60),-np.minimum(dout,60))
g=np.where(mask,g-0.5*np.median(w),g+0.5*np.median(w))            # put the zero between the two border rings
# zone scalar for MC vertices: interpolate g at the closest point on B1; new geometry far from B1 is inside
sqd,fi,cp=igl.point_mesh_squared_distance(Vm,P1,f1); d=np.sqrt(sqd)
tri=f1[fi]; bc=igl.barycentric_coordinates(cp,P1[tri[:,0]],P1[tri[:,1]],P1[tri[:,2]]) if hasattr(igl,"barycentric_coordinates") else None
if bc is None: raise SystemExit("no barycentric")
gm=(g[tri]*bc).sum(1); gm=np.where(d>1.5,np.maximum(gm,5.0),gm)
def clip(V,F,s,keep_pos=True):
    s=s if keep_pos else -s; s=np.where(np.abs(s)<1e-7,1e-7,s)
    pos=s[F]>0; npos=pos.sum(1); out=[F[npos==3]]; newV=[]; key={}
    def ev(a,b):
        k=(min(a,b),max(a,b))
        if k not in key:
            t=s[a]/(s[a]-s[b]); key[k]=len(V)+len(newV); newV.append(V[a]+t*(V[b]-V[a]))
        return key[k]
    for tri,p in zip(F[npos==1],pos[npos==1]):
        r=np.argmax(p); a,b,c=tri[r],tri[(r+1)%3],tri[(r+2)%3]; out.append(np.array([[a,ev(a,b),ev(a,c)]]))
    for tri,p in zip(F[npos==2],pos[npos==2]):
        r=np.argmin(p); a,b,c=tri[r],tri[(r+1)%3],tri[(r+2)%3]       # a is the negative vertex
        pab,pac=ev(a,b),ev(a,c); out.append(np.array([[pab,b,c],[pab,c,pac]]))
    V2=np.concatenate([V,np.array(newV).reshape(-1,3)]); F2=np.concatenate(out); u=np.unique(F2)
    rm=-np.ones(len(V2),int); rm[u]=np.arange(len(u)); return V2[u],rm[F2]
def largest(V,F):
    e=np.concatenate([F[:,[0,1]],F[:,[1,2]]]); A=coo_matrix((np.ones(len(e)),(e[:,0],e[:,1])),shape=(len(V),)*2)
    n,l=connected_components(A,directed=False); lf=l[F[:,0]]; big=np.bincount(lf).argmax(); F=F[lf==big]
    u=np.unique(F); rm=-np.ones(len(V),int); rm[u]=np.arange(len(u)); return V[u],rm[F]
VA,FA=clip(P1,f1,g,keep_pos=False); VB,FB=clip(Vm,Fm,gm,keep_pos=True); VB,FB=largest(VB,FB)
def loops(F):
    e=np.concatenate([F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]); k=np.sort(e,1); u,inv,c=np.unique(k,axis=0,return_inverse=True,return_counts=True)
    b=e[c[inv.ravel()]==1]; nxt={}
    for a,bb in b: nxt.setdefault(a,[]).append(bb)
    out=[]; used=set()
    for a0,b0 in b:
        if (a0,b0) in used: continue
        L=[a0]; x=b0; used.add((a0,b0))
        while x!=a0:
            L.append(x); cand=[y for y in nxt[x] if (x,y) not in used]
            if not cand: break
            used.add((x,cand[0])); x=cand[0]
        out.append(np.array(L))
    return out
LA=loops(FA); LB=loops(FB); print("loops A",sorted(len(l) for l in LA)[-5:],"B",sorted(len(l) for l in LB)[-5:], "counts",len(LA),len(LB))
nA=len(VA); V=np.concatenate([VA,VB]); FB2=FB+nA; LB=[l+nA for l in LB]
def zipper(a,b):
    b=b[::-1]; j0=np.argmin(np.linalg.norm(V[b]-V[a[0]],axis=1)); b=np.roll(b,-j0)
    na,nb=len(a),len(b); i=j=0; F=[]
    while i<na or j<nb:
        ai,ai1=a[i%na],a[(i+1)%na]; bj,bj1=b[j%nb],b[(j+1)%nb]
        if j>=nb or (i<na and np.linalg.norm(V[ai1]-V[bj])<np.linalg.norm(V[bj1]-V[ai])): F.append([ai,ai1,bj]); i+=1
        else: F.append([ai,bj1,bj]); j+=1
    return np.array(F)
br=[]; small=[]
bigA=max(LA,key=len); bigB=max(LB,key=len)
Z=zipper(bigA,bigB)[:,[0,2,1]]                      # flip: bridge faces must run against both borders
gap=np.linalg.norm(V[Z[:,0]]-V[Z[:,2]],axis=1); print("bridge",len(bigA),len(bigB),"gap mean %.3f p99 %.3f max %.3f"%(gap.mean(),np.percentile(gap,99),gap.max()))
k=np.argmax(gap); print("max gap at",V[Z[k,0]].round(1))
br.append(Z)
extraV=[]
for l in [l for l in LA+LB if len(l)<=12 and l is not bigA and l is not bigB]:
    if len(l)<3: continue
    c=len(V)+len(extraV); extraV.append(V[l].mean(0))
    small.append(np.array([[l[(i+1)%len(l)],l[i],c] for i in range(len(l))]))
V=np.concatenate([V,np.array(extraV).reshape(-1,3)]); br+=small
F=np.concatenate([FA,FB2]+br)
e=np.sort(np.concatenate([F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]),1); u,c=np.unique(e,axis=0,return_counts=True)
de=np.concatenate([F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]); ud,cd=np.unique(de,axis=0,return_counts=True)
print("faces",len(F),"boundary",(c==1).sum(),"nonmanifold",(c>2).sum(),"orientation conflicts",(cd>1).sum())
a,b,cc=V[F[:,0]],V[F[:,1]],V[F[:,2]]; print("volume",np.einsum("ij,ij->i",a,np.cross(b,cc)).sum()/6)
np.savez("g1_body_raw.npz",V=V,F=F,nA=nA,nFA=len(FA),nFB=len(FB),seam=np.concatenate([np.unique(z) for z in br]) if br else np.zeros(0,int))
for l in loops(FB):
    if len(l)>=6: p=VB[l]; print("B loop",len(l),"centroid",p.mean(0).round(1),"min",p.min(0).round(1),"max",p.max(0).round(1))
for l in loops(FA):
    if len(l)>=6: p=VA[l]; print("A loop",len(l),"centroid",p.mean(0).round(1),"min",p.min(0).round(1),"max",p.max(0).round(1))
