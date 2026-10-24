# build_foot.py SIDE H TARGET OUT : SDF forefoot+toes blended into the frozen v003 foot (a<9.5 pure v003), MC, remesh
import sys, numpy as np, time, igl, trimesh
sys.path.insert(0,'/tmp/claude-0/src3d/v5/tools'); sys.path.insert(0,'/tmp/claude-0/src3d/tools')
from foot_model import foot_sdf
from sdf import smin, smax
from build_part import evaluate, polygonize, remesh
from cotfair import ss
side=sys.argv[1]; h=float(sys.argv[2]); tgt=float(sys.argv[3]); out=sys.argv[4]
B=np.load('/tmp/claude-0/src3d/v4/v003.npz'); BV=B['V']; BF=B['Q'].astype(np.int64)
sg=1 if side=='L' else -1
sel=np.nonzero((sg*BV[:,0]>3)&(BV[:,2]<20))[0]; SF=BF[np.isin(BF,sel).all(1)]
uu=np.unique(SF); rmap=-np.ones(len(BV),int); rmap[uu]=np.arange(len(uu)); SV=BV[uu].copy(); SF=rmap[SF]
SD=lambda Q: igl.signed_distance(Q,SV,SF,sign_type=igl.SIGNED_DISTANCE_TYPE_PSEUDONORMAL)[0]
m=(sg*BV[:,0]>3)&(BV[:,2]<4)&(BV[:,1]>8)&(BV[:,1]<16); zg=float(BV[m,2].min()) if sg>0 else 0.0; print('ground under ball',zg)
toloc=lambda P: np.c_[sg*P[:,0],P[:,1],P[:,2]]
def fun(P):
    Lc=toloc(P); a=Lc[:,1]
    S=SD(P)
    t=ss((a-11.0)/2.0)
    out=S.copy(); k=t>0
    if k.any():
        acut=18.2+float(__import__('os').environ.get('AC','0'))-0.30*(Lc[k][:,0]-12.0)
        dn=smin(smax(S[k],a[k]-acut,2.8),foot_sdf(Lc[k],zg=zg),float(__import__('os').environ.get('FK','1.1')))
        out[k]=(1-t[k])*S[k]+t[k]*dn
    return out
lo=np.array([6,10.0,-0.6]); hi=np.array([32,29.5,10.0])
if sg<0: lo,hi=np.array([-hi[0],lo[1],lo[2]]),np.array([-lo[0],hi[1],hi[2]])
t0=time.time(); D,lo,h,cnt=evaluate(fun,lo,hi,h); print('eval %.0fs'%(time.time()-t0),cnt)
V,F=polygonize(D,lo,h)
import trimesh as _t; _m=_t.Trimesh(V,F,process=False); _t.smoothing.filter_taubin(_m,lamb=0.5,nu=0.53,iterations=20); V=np.asarray(_m.vertices)
from build_part import genus; print('mc faces',len(F),'genus',genus(V,F)); V,F=remesh(V,F,tgt); print('decimated genus',genus(V,F))
mm=trimesh.Trimesh(V,F,process=True); parts=mm.split(only_watertight=False); mm=max(parts,key=lambda q:len(q.faces))
V=np.asarray(mm.vertices); F=np.asarray(mm.faces)
np.savez(out,V=V,Q=F,a=V[:,1],zg=zg); print('foot',side,len(V),len(F),'parts',len(parts))
