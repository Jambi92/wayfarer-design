# relaxg.py IN OUT R ITERS cx,cf,cu [cx,cf,cu ...] : guarded local surface relaxation at several centres. Each patch is
# kept only if (a) no hard-limit quad appears, (b) source coverage under the patch does not worsen past max(before, 0.8 mm),
# (c) no quad flips. Removes irregular quad flow (shading rumples) without changing the source shape.
import numpy as np, sys, igl, subprocess, os
sys.path.insert(0,'/tmp/claude-0/rt')
from subproj import Projector, vertex_part, neighbors, vnormals
from scipy.spatial import cKDTree
z=np.load(sys.argv[1]); V=z['V'].copy(); Q=z['Q']; FP=z['FP']; R=float(sys.argv[3]); IT=int(sys.argv[4])
PR=Projector(); SV,SF=PR.SV,PR.SF; KD=cKDTree(SV); vp,M=vertex_part(Q,FP,len(V)); band=np.asarray((M>0).sum(1)).ravel()>1
A=neighbors(Q,len(V)); deg=np.asarray(A.sum(1)).ravel(); Tq=np.r_[Q[:,[0,1,2]],Q[:,[0,2,3]]]
def qual(X,F):
    ang=[]
    for i in range(4):
        a=X[Q[F,(i-1)%4]]-X[Q[F,i]]; b=X[Q[F,(i+1)%4]]-X[Q[F,i]]
        ang.append(np.degrees(np.arccos(np.clip((a*b).sum(1)/np.maximum(np.linalg.norm(a,axis=1)*np.linalg.norm(b,axis=1),1e-12),-1,1))))
    ang=np.stack(ang,1); el=np.stack([np.linalg.norm(X[Q[F,(i+1)%4]]-X[Q[F,i]],axis=1) for i in range(4)],1)
    return ang.min(1),ang.max(1),el.max(1)/np.maximum(el.min(1),1e-12)
def fn(X,F):
    n=np.cross(X[Q[F,2]]-X[Q[F,0]],X[Q[F,3]]-X[Q[F,1]]); return n/np.maximum(np.linalg.norm(n,axis=1),1e-12)[:,None]
for cs in sys.argv[5:]:
    c=np.array([float(v) for v in cs.split(',')]); r=np.linalg.norm(V-c,axis=1); idx=np.nonzero(r<R)[0]; w=np.clip((R-r[idx])/(0.35*R),0,1)
    F=np.nonzero((np.linalg.norm(V[Q]-c,axis=2)<R+0.5).any(1))[0]; Vn=V.copy()
    for it in range(IT):
        N=vnormals(Vn,Q); T=np.zeros_like(V); W=np.zeros(len(V))
        for k in range(4):
            t=Vn[Q[F,(k-1)%4]]+Vn[Q[F,(k+1)%4]]-Vn[Q[F,(k+2)%4]]; np.add.at(T,Q[F,k],t); np.add.at(W,Q[F,k],1)
        par=T[idx]/np.maximum(W[idx],1)[:,None]; lap=(A[idx]@Vn)/deg[idx][:,None]
        dl=0.5*lap+0.5*par-Vn[idx]; dl-=(dl*N[idx]).sum(1)[:,None]*N[idx]
        Vn[idx]=PR.project(Vn[idx]+0.4*w[:,None]*dl,vp[idx],band[idx],N[idx])
    a0,b0,r0=qual(V,F); a1,b1,r1=qual(Vn,F)
    sids=np.array(KD.query_ball_point(c,R),int)
    d0=np.sqrt(igl.point_mesh_squared_distance(SV[sids],V,Tq)[0]); d1=np.sqrt(igl.point_mesh_squared_distance(SV[sids],Vn,Tq)[0])
    hard1=((a1<20)|(b1>160)).sum(); hard0=((a0<20)|(b0>160)).sum(); flip=((fn(Vn,F)*fn(V,F)).sum(1)<0.2).any()
    ok=hard1<=hard0 and d1.max()<=max(d0.max(),0.08)+0.005 and not flip and r1.max()<=max(r0.max(),6.0)
    print('patch',cs,'verts',len(idx),'hard %d->%d'%(hard0,hard1),'cover max mm %.2f->%.2f'%(d0.max()*10,d1.max()*10),'ratio max %.1f->%.1f'%(r0.max(),r1.max()),'KEEP' if ok else 'reject',flush=True)
    if ok: V=Vn
np.savez(sys.argv[2],V=V,Q=Q,FP=FP)
