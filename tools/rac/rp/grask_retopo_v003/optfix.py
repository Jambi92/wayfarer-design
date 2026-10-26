# optfix.py IN OUT : (v003: env OPT_RSEL / OPT_RMAX add the longest/shortest-edge ratio to the selection and objective)
# direct local optimisation of the last sliver clusters. Free vertices = corners of each hard quad (+1 ring);
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
import os
RSEL=float(os.environ.get('OPT_RSEL','1e9')); RMAX=float(os.environ.get('OPT_RMAX','1e9')); RING=int(os.environ.get('OPT_RING','0'))
def eratio(X,F):
    el=np.stack([np.linalg.norm(X[Q[F,(i+1)%4]]-X[Q[F,i]],axis=1) for i in range(4)],1); return el.max(1)/np.maximum(el.min(1),1e-12)
a=angs(V,np.arange(len(Q))); er=eratio(V,np.arange(len(Q)))
hard=np.nonzero((a.min(1)<20)|(a.max(1)>160)|(er>RSEL))[0]; print('selected',len(hard))
done=set()
import subprocess, os as _os
def fn_all(X,F):
    n=np.cross(X[Q[F,2]]-X[Q[F,0]],X[Q[F,3]]-X[Q[F,1]]); return n/np.maximum(np.linalg.norm(n,axis=1),1e-12)[:,None]
def nfold(F,Fn):
    E={}; n=0
    for i,f in enumerate(F):
        q=Q[f]
        for k in range(4):
            e=tuple(sorted((q[k],q[(k+1)%4])))
            if e in E:
                if (Fn[E[e]]*Fn[i]).sum()<-0.5: n+=1
            else: E[e]=i
    return n
def crop_pairs(X,c,r):
    m=(np.linalg.norm(X[Q]-c,axis=2)<r).any(1); tmp='/tmp/claude-0/rt/_crop_%d'%_os.getpid()
    np.savez(tmp+'.npz',V=X,Q=Q[m],FP=FP[m])
    o=subprocess.run(['/home/claude/stc/bin/python3','/tmp/claude-0/rp2/sxq.py',tmp+'.npz',tmp+'_s.npy'],capture_output=True,text=True).stdout
    for l in o.splitlines():
        if l.startswith('PAIRS'): return int(l.split()[1])
    return 0
for f in hard:
    if f in done: continue
    vs=np.zeros(nV,bool); vs[Q[f]]=True
    cl=[g for g in hard if vs[Q[g]].any()]; [done.add(g) for g in cl]
    for g in cl: vs[Q[g]]=True
    for _ in range(RING): vs|=(A@vs.astype(float))>0
    free=np.nonzero(vs)[0]; vs2=vs|((A@vs.astype(float))>0); F=np.nonzero(np.asarray(VF[vs2].sum(0)).ravel()>=1)[0]
    F=F[np.isin(Q[F],np.nonzero(vs2)[0]).all(1)|np.isin(Q[F],free).any(1)]
    Tq=np.r_[Q[F][:,[0,1,2]],Q[F][:,[0,2,3]]]
    ctr=V[free].mean(0); rad=np.linalg.norm(V[free]-ctr,axis=1).max()+0.3; sids=np.array(KD.query_ball_point(ctr,rad),int)
    d0=np.sqrt(igl.point_mesh_squared_distance(SV[sids],V,Tq)[0]) if len(sids) else np.zeros(0)
    lv=np.zeros(len(SV),bool); lv[KD.query_ball_point(ctr,rad+1.0)]=True; LF=SF[lv[SF].all(1)]
    n0=nrm(V,F); X0=V[free].copy()
    _E={}; PA=[]
    for i_,f_ in enumerate(F):
        q_=Q[f_]
        for k_ in range(4):
            e_=tuple(sorted((q_[k_],q_[(k_+1)%4])))
            if e_ in _E: PA.append((_E[e_],i_))
            else: _E[e_]=i_
    PA=np.array(PA,int).reshape(-1,2); base=(n0[PA[:,0]]*n0[PA[:,1]]).sum(1)>-0.5 if len(PA) else np.zeros(0,bool)
    def obj(x):
        X=V.copy(); X[free]=x.reshape(-1,3); an=angs(X,F)
        e=np.sum(np.maximum(0,25-an.min(1))**2)+np.sum(np.maximum(0,an.max(1)-155)**2)+400*np.sum(np.maximum(0,eratio(X,F)-RMAX)**2)
        ds=np.sqrt(igl.point_mesh_squared_distance(X[free],SV,LF)[0]); e+=1e5*np.sum(np.maximum(0,ds-float(_os.environ.get('OPT_OFF','0.03')))**2)
        if len(sids):
            d1=np.sqrt(igl.point_mesh_squared_distance(SV[sids],X,Tq)[0]); e+=1e5*np.sum(np.maximum(0,d1-np.maximum(d0,0.10))**2)
        nn=nrm(X,F); fl=(nn*n0).sum(1); e+=1e4*np.sum(np.maximum(0,0.3-fl)**2)
        if len(PA): dd=(nn[PA[:,0]]*nn[PA[:,1]]).sum(1); e+=1e4*np.sum(np.maximum(0,-0.4-dd[base])**2)
        return e
    w0=np.minimum(angs(V,F).min(1),180-angs(V,F).max(1)).min(); e0=obj(X0.ravel()); r0=eratio(V,F).max()
    r=so.minimize(obj,X0.ravel(),method='Powell',options=dict(maxiter=3000,xtol=1e-4,ftol=1e-6))
    X=V.copy(); X[free]=r.x.reshape(-1,3); an=angs(X,F); w1=np.minimum(an.min(1),180-an.max(1)).min()
    ds=np.sqrt(igl.point_mesh_squared_distance(X[free],SV,SF)[0]).max()*10; fl=((nrm(X,F)*n0).sum(1)<0.2).any()
    r1=eratio(X,F).max(); ok=(((w1>w0+1) and r1<=max(r0+0.05,6.5)) or (r1<r0-0.3 and w1>=min(w0,20))) and min(w1,20)>=min(w0,20) and not fl and ds<=float(_os.environ.get('OPT_OFF','0.03'))*10+0.05
    print('cluster',len(cl),'free',len(free),'worst %.1f -> %.1f'%(w0,w1),'ratio %.2f -> %.2f'%(r0,r1),'offsurf mm %.2f'%ds,'obj %.1f->%.1f'%(e0,r.fun),'KEEP' if ok else 'reject',flush=True)
    if ok:
        # fold guard: adjacent faces inside the patch must not fold (> 120 deg dihedral)
        ok=nfold(F,fn_all(X,F))<=nfold(F,fn_all(V,F))
        if not ok: print('   rejected: would add a fold',flush=True)
    if ok:
        # self-intersection guard on a crop around the patch (Blender BVH, same test as sxq.py)
        ok=crop_pairs(X,ctr,rad+1.5)<=crop_pairs(V,ctr,rad+1.5)
        if not ok: print('   rejected: would create a self-intersection',flush=True)
    if ok: V=X; np.savez(sys.argv[2],V=V,Q=Q,FP=FP)
a=angs(V,np.arange(len(Q))); print('final hard',int(((a.min(1)<20)|(a.max(1)>160)).sum()),'ratio>8',int((eratio(V,np.arange(len(Q)))>8).sum()))
np.savez(sys.argv[2],V=V,Q=Q,FP=FP)
