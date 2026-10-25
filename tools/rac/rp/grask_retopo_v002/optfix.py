# optfix.py IN OUT : direct local optimisation of the last sliver clusters. Free vertices = corners of each hard quad (+1 ring);
# objective = angle-limit violations of the patch quads + off-surface penalty (> 0.3 mm) + loss of source coverage under the
# patch (> 1.0 mm); derivative-free (Powell). A cluster is kept only if its worst angle improves and nothing folds.
import numpy as np, sys, igl, scipy.optimize as so, scipy.sparse as sp
sys.path.insert(0,'/tmp/claude-0/rt'); from subproj import neighbors; from common import load_src
from scipy.spatial import cKDTree
z=np.load(sys.argv[1]); V=z['V'].copy(); Q=z['Q']; FP=z['FP']; SV,SF=load_src(); KD=cKDTree(SV)
nV=len(V); A=neighbors(Q,nV); VF=sp.coo_matrix((np.ones(Q.size),(Q.ravel(),np.repeat(np.arange(len(Q)),4))),shape=(nV,len(Q))).tocsr()
def angs(X,F):
    out=[]
    for i in range(4):
        a=X[Q[F,(i-1)%4]]-X[Q[F,i]]; b=X[Q[F,(i+1)%4]]-X[Q[F,i]]
        out.append(np.degrees(np.arccos(np.clip((a*b).sum(1)/np.maximum(np.linalg.norm(a,axis=1)*np.linalg.norm(b,axis=1),1e-12),-1,1))))
    return np.stack(out,1)
def nrm(X,F):
    n=np.cross(X[Q[F,2]]-X[Q[F,0]],X[Q[F,3]]-X[Q[F,1]]); return n/np.maximum(np.linalg.norm(n,axis=1),1e-12)[:,None]
a=angs(V,np.arange(len(Q))); hard=np.nonzero((a.min(1)<20)|(a.max(1)>160))[0]; print('hard',len(hard))
done=set()
for f in hard:
    if f in done: continue
    vs=np.zeros(nV,bool); vs[Q[f]]=True
    cl=[g for g in hard if vs[Q[g]].any()]; [done.add(g) for g in cl]
    for g in cl: vs[Q[g]]=True
    free=np.nonzero(vs)[0]; vs2=vs|((A@vs.astype(float))>0); F=np.nonzero(np.asarray(VF[vs2].sum(0)).ravel()>=1)[0]
    F=F[np.isin(Q[F],np.nonzero(vs2)[0]).all(1)|np.isin(Q[F],free).any(1)]
    Tq=np.r_[Q[F][:,[0,1,2]],Q[F][:,[0,2,3]]]
    ctr=V[free].mean(0); rad=np.linalg.norm(V[free]-ctr,axis=1).max()+0.3; sids=np.array(KD.query_ball_point(ctr,rad),int)
    d0=np.sqrt(igl.point_mesh_squared_distance(SV[sids],V,Tq)[0]) if len(sids) else np.zeros(0)
    lv=np.zeros(len(SV),bool); lv[KD.query_ball_point(ctr,rad+1.0)]=True; LF=SF[lv[SF].all(1)]
    n0=nrm(V,F); X0=V[free].copy()
    def obj(x):
        X=V.copy(); X[free]=x.reshape(-1,3); an=angs(X,F)
        e=np.sum(np.maximum(0,25-an.min(1))**2)+np.sum(np.maximum(0,an.max(1)-155)**2)
        ds=np.sqrt(igl.point_mesh_squared_distance(X[free],SV,LF)[0]); e+=1e5*np.sum(np.maximum(0,ds-0.03)**2)
        if len(sids):
            d1=np.sqrt(igl.point_mesh_squared_distance(SV[sids],X,Tq)[0]); e+=1e5*np.sum(np.maximum(0,d1-np.maximum(d0,0.10))**2)
        fl=(nrm(X,F)*n0).sum(1); e+=1e4*np.sum(np.maximum(0,0.3-fl)**2)
        return e
    w0=np.minimum(angs(V,F).min(1),180-angs(V,F).max(1)).min(); e0=obj(X0.ravel())
    r=so.minimize(obj,X0.ravel(),method='Powell',options=dict(maxiter=3000,xtol=1e-4,ftol=1e-6))
    X=V.copy(); X[free]=r.x.reshape(-1,3); an=angs(X,F); w1=np.minimum(an.min(1),180-an.max(1)).min()
    ds=np.sqrt(igl.point_mesh_squared_distance(X[free],SV,SF)[0]).max()*10; fl=((nrm(X,F)*n0).sum(1)<0.2).any()
    ok=(w1>w0+1) and not fl and ds<=0.35
    print('cluster',len(cl),'free',len(free),'worst %.1f -> %.1f'%(w0,w1),'offsurf mm %.2f'%ds,'obj %.1f->%.1f'%(e0,r.fun),'KEEP' if ok else 'reject',flush=True)
    if ok: V=X; np.savez(sys.argv[2],V=V,Q=Q,FP=FP)
a=angs(V,np.arange(len(Q))); print('final hard',int(((a.min(1)<20)|(a.max(1)>160)).sum()))
np.savez(sys.argv[2],V=V,Q=Q,FP=FP)
