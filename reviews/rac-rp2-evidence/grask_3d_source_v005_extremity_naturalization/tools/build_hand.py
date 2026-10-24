# build_hand.py SIDE H TARGET OUT : SDF hand blended into the frozen v003 forearm (u<-1.5 -> pure v003), MC, remesh, largest piece
import sys, numpy as np, time, igl
sys.path.insert(0,'/tmp/claude-0/src3d/v5/tools'); sys.path.insert(0,'/tmp/claude-0/src3d/tools')
from hand_model import hand_sdf
from hand_frame import frame
from build_part import evaluate, polygonize, remesh
from cotfair import ss
side=sys.argv[1]; h=float(sys.argv[2]); tgt=float(sys.argv[3]); out=sys.argv[4]
B=np.load('/tmp/claude-0/src3d/v4/v003.npz'); BV=B['V']; BF=B['Q'].astype(np.int64)
sg=1 if side=='L' else -1
sel=np.nonzero((sg*BV[:,0]>15)&(BV[:,2]>95)&(BV[:,2]<130))[0]; fm=np.isin(BF,sel).all(1); SF=BF[fm]
uu=np.unique(SF); rmap=-np.ones(len(BV),int); rmap[uu]=np.arange(len(uu)); SV=BV[uu].copy(); SF=rmap[SF]
SD=lambda Q: igl.signed_distance(Q,SV,SF,sign_type=igl.SIGNED_DISTANCE_TYPE_PSEUDONORMAL)[0]
W,M=frame(side)
def fun(P):
    L=(P-W)@M; u=L[:,0]; d=np.empty(len(P))
    t=ss((-u-1.5)/3.5)
    a=t<1; b=t>0
    if a.any(): dh=hand_sdf(L[a])
    if b.any():
        S=SD(P[b])
    d[:]=0
    da=np.zeros(len(P)); db=np.zeros(len(P))
    if a.any(): da[a]=dh
    if b.any(): db[b]=S
    return np.where(t<=0,da,np.where(t>=1,db,(1-t)*da+t*db))
c=np.array([[u,v,w] for u in (-8.0,30) for v in (-8.5,13.5) for w in (-10.5,6.5)])
Pw=W+c@M.T; lo=Pw.min(0); hi=Pw.max(0)
t0=time.time(); D,lo,h,cnt=evaluate(fun,lo,hi,h); print('eval %.0fs'%(time.time()-t0),cnt)
V,F=polygonize(D,lo,h)
import trimesh as _t; _m=_t.Trimesh(V,F,process=False); _t.smoothing.filter_taubin(_m,lamb=0.5,nu=0.53,iterations=20); V=np.asarray(_m.vertices)
from build_part import genus; print('mc faces',len(F),'genus',genus(V,F)); V,F=remesh(V,F,tgt); print('decimated genus',genus(V,F))
import trimesh
m=trimesh.Trimesh(V,F,process=True); parts=m.split(only_watertight=False); m=max(parts,key=lambda q:len(q.faces))
V=np.asarray(m.vertices); F=np.asarray(m.faces)
np.savez(out,V=V,Q=F,u=((V-W)@M)[:,0]); print('hand',side,len(V),len(F),'parts',len(parts))
