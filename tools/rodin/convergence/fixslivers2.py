# repair degenerate zip-seam triangles by link-condition-safe edge collapses (vertex indices preserved; collapsed
# vertices become unreferenced), then flip remaining folded edges.  argv: in.npz out.npz
import numpy as np, igl, sys
from collections import defaultdict
import os
def ZSEL(c):   # authorized seam rings: SEAMZONE=forearm -> forearm zip ring (u 100-120, |x|>25); ankle -> u<25
    return ((c[:,2]>100)&(c[:,2]<120)&(np.abs(c[:,0])>25)) if os.environ.get('SEAMZONE','ankle')=='forearm' else (c[:,2]<25)
z=np.load(sys.argv[1]); V=z['V'].astype(np.float64).copy(); F=z['F'].astype(np.int64).copy(); V0=V.copy()
def quality(V,F):
    a_,b_,c_=V[F[:,0]],V[F[:,1]],V[F[:,2]]
    la=np.linalg.norm(b_-c_,axis=1); lb=np.linalg.norm(a_-c_,axis=1); lc=np.linalg.norm(a_-b_,axis=1)
    area=0.5*np.linalg.norm(np.cross(b_-a_,c_-a_),axis=1); q=4*np.sqrt(3)*area/(la**2+lb**2+lc**2+1e-12)
    return q,area,np.stack([la,lb,lc],1)
def flipped(V,F):
    FN=igl.per_face_normals(V,F,np.array([0,0,1.0])); N2=igl.per_vertex_normals(V,F); return np.einsum('ij,ij->i',FN,N2[F].mean(1))<0.2
for rnd in range(25):
    q,area,Ls=quality(V,F); fl=flipped(V,F)
    bad=np.where(((q<0.05)|fl)&ZSEL(V[F].mean(1)))[0]          # ankle zip-seam rings only (authorized defect repair)
    if len(bad)==0: break
    nbr=defaultdict(set); vf=defaultdict(set)
    for i,(a,b,c) in enumerate(F):
        nbr[a].update((b,c)); nbr[b].update((a,c)); nbr[c].update((a,b)); vf[a].add(i); vf[b].add(i); vf[c].add(i)
    used=set(); kill=set(); ncol=0
    for fi in bad[np.argsort(q[bad])]:
        tri=F[fi]; e=np.argmin(Ls[fi])             # shortest edge is opposite vertex e
        a,b=[tri[k] for k in range(3) if k!=e]
        if a in used or b in used: continue
        if len(nbr[a]&nbr[b])!=2: continue        # link condition (manifold-safe)
        mid=0.5*(V[a]+V[b]); V[a]=mid; used.update(nbr[a]|nbr[b]|{a,b})
        for g in vf[b]:
            F[g][F[g]==b]=a
        ncol+=1
    keep=~((F[:,0]==F[:,1])|(F[:,1]==F[:,2])|(F[:,0]==F[:,2])); F=F[keep]
    ek=np.sort(np.concatenate([F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]),1); _,cc=np.unique(ek,axis=0,return_counts=True)
    print('round',rnd,'bad',len(bad),'collapsed',ncol,'faces',len(F),'boundary',(cc==1).sum(),'nonmanifold',(cc>2).sum(),flush=True)
q,area,_=quality(V,F); fl=flipped(V,F)
mv=np.linalg.norm(V-V0,axis=1); ref=np.unique(F.ravel())
print('final sliver(q<0.05)',int((q<0.05).sum()),'flipped',int(fl.sum()),'max move %.3f mm'%(mv[ref].max()*10),'unreferenced verts',len(V)-len(ref))
np.savez(sys.argv[2],V=V,F=F,MVS=mv.astype(np.float32))
# seam-ring band: shape-preserving Taubin smoothing (removes the zip line and residual folds)
from scipy.sparse import coo_matrix, diags
from scipy.sparse.csgraph import dijkstra
n=len(V); E=np.concatenate([F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]])
A=coo_matrix((np.ones(len(E)),(E[:,0],E[:,1])),shape=(n,n)).tocsr(); A=((A+A.T)>0).astype(np.float32)
deg=np.asarray(A.sum(1)).ravel(); L=diags(1/np.maximum(deg,1))@A
z0=np.load(sys.argv[1]); F0=z0['F'].astype(np.int64); q0,_,_=quality(V0,F0); fl0=flipped(V0,F0)
seed=np.unique(F0[((q0<0.08)|fl0)&ZSEL(V0[F0].mean(1))].ravel()); seed=seed[deg[seed]>0]
w=np.linalg.norm(V[E[:,0]]-V[E[:,1]],axis=1); G=coo_matrix((w,(E[:,0],E[:,1])),shape=(n,n)).tocsr()
dd=dijkstra(G,indices=seed,min_only=True,limit=1.5); wb=np.where(np.isfinite(dd),np.clip(1-dd/1.2,0,1),0.0); wb[deg==0]=0
for _ in range(30): V=V+(0.5*wb)[:,None]*((L@V)-V); V=V+(-0.53*wb)[:,None]*((L@V)-V)
q,area,_=quality(V,F); fl=flipped(V,F); mv=np.linalg.norm(V-V0,axis=1); ref=np.unique(F.ravel())
print('after band smoothing: sliver',int((q<0.05).sum()),'flipped',int(fl.sum()),'max move %.3f mm'%(mv[ref].max()*10),'band verts',int((wb>0).sum()))
keep=np.unique(F.ravel()); rm=-np.ones(n,np.int64); rm[keep]=np.arange(len(keep))      # drop collapsed (unreferenced) vertices
np.savez(sys.argv[2],V=V[keep],F=rm[F],KEEP=keep,MVS=mv[keep].astype(np.float32),WSEAM=wb[keep].astype(np.float32))
print('compacted verts',len(keep))
