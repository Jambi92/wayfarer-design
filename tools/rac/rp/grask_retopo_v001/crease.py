# crease.py IN.npz OUT.npz ITERS [thr_cm] : bidirectional fit -- source points the retopo does not reach (crease bottoms,
# ear folds, toe roots) attract their nearest retopo vertices; then light tangential relax and guarded re-projection.
import numpy as np, sys, igl, scipy.sparse as sp
sys.path.insert(0,'/tmp/claude-0/rt')
from subproj import Projector, vertex_part, neighbors, vnormals
from common import *
inp,out,IT=sys.argv[1],sys.argv[2],int(sys.argv[3]); thr=float(sys.argv[4]) if len(sys.argv)>4 else 0.04
z=np.load(inp); V=z['V'].copy(); Q=z['Q']; FP=z['FP']
PR=Projector(); SV,SF=PR.SV,PR.SF
vp,M=vertex_part(Q,FP,len(V)); band=np.asarray((M>0).sum(1)).ravel()>1
A=neighbors(Q,len(V)); deg=np.asarray(A.sum(1)).ravel()
T=np.r_[Q[:,[0,1,2]],Q[:,[0,2,3]]]; TQ=np.r_[np.arange(len(Q)),np.arange(len(Q))]
# dense source samples: vertices + face centroids
S=np.r_[SV,SV[SF].mean(1)]; SL=np.r_[np.load('/tmp/claude-0/rt/vlab.npy'),np.load('/tmp/claude-0/rt/flab.npy')]
import os
if os.environ.get('CREASE_BOX'):
    bx=[float(v) for v in os.environ['CREASE_BOX'].split(',')]   # |x|min,|x|max,fmin,fmax,zmin,zmax
    keep_=(np.abs(S[:,0])>=bx[0])&(np.abs(S[:,0])<=bx[1])&(S[:,1]>=bx[2])&(S[:,1]<=bx[3])&(S[:,2]>=bx[4])&(S[:,2]<=bx[5]); S=S[keep_]; SL=SL[keep_]
    _x=S[(np.abs(S[:,0])>=bx[0])&(np.abs(S[:,0])<=bx[1])&(S[:,1]>=bx[2])&(S[:,1]<=bx[3])&(S[:,2]>=bx[4])&(S[:,2]<=bx[5])]
    print('crease box samples',len(S))
for it in range(IT):
    d,fi,cp=igl.point_mesh_squared_distance(S,V,T); d=np.sqrt(d)
    m=d>thr; print('iter',it,'uncovered',m.sum(),'max %.3f'%d.max())
    if not m.any(): break
    q=Q[TQ[fi[m]]]; Pm=S[m]
    dd=np.linalg.norm(V[q]-Pm[:,None],axis=2); vi=q[np.arange(len(q)),dd.argmin(1)]
    w=d[m]
    # a sample may only attract a vertex of its own part or an adjacent part (never a sibling digit across a web slot)
    ok_=np.array([(sl==pv) or (PARTS[sl] in ADJ.get(PARTS[pv],())) or (PARTS[pv] in ADJ.get(PARTS[sl],())) for sl,pv in zip(SL[m],vp[vi])])
    vi=vi[ok_]; Pm=Pm[ok_]; w=w[ok_]
    acc=np.zeros_like(V); ws=np.zeros(len(V))
    np.add.at(acc,vi,Pm*w[:,None]); np.add.at(ws,vi,w)
    h=ws>0; tgt=acc[h]/ws[h][:,None]
    V[h]=V[h]+0.7*(tgt-V[h])
    # spread a little to neighbours so the fold is followed by a loop, not a spike
    moved=np.zeros(len(V)); moved[h]=1
    N=vnormals(V,Q); avg=(A@V)/deg[:,None]; dlt=avg-V; dlt-=(dlt*N).sum(1)[:,None]*N
    free=~h
    V[free]=V[free]+0.3*dlt[free]
    P2=PR.project(V,vp,band,N)
    # attracted vertices: keep if they already sit on the source (any part)
    P2[h]=PR.project(V[h],vp[h],band[h],N[h])     # own-part (guarded) snap: never onto a sibling digit's wall
    V=P2
np.savez(out,V=V,Q=Q,FP=FP)
