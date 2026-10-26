# lrepair.py IN OUT [K] : local patch re-layout for residual sliver quads. Each cluster of hard quads (+K rings) is cut out as a
# disk, flattened with positive mean-value weights (geometry-aware, bijective), re-laid with a uniform Tutte embedding of the quad
# graph (grid-like quads), mapped back onto the patch surface and re-projected (part-guarded) onto v005. Accepted per patch only if
# the patch's worst quad improves and no quad folds.
import numpy as np, sys, os, scipy.sparse as sp, scipy.sparse.linalg as sla, collections
sys.path.insert(0,'/tmp/claude-0/rt')
from subproj import Projector, vertex_part, neighbors, vnormals
z=np.load(sys.argv[1]); V=z['V'].copy(); Q=z['Q']; FP=z['FP']; K=int(sys.argv[3]) if len(sys.argv)>3 else 3
PR=Projector(); import igl as _igl; from scipy.spatial import cKDTree as _KD; _SKD=_KD(PR.SV); DMAX=float(os.environ.get('LDEV','0.08')); vp,M=vertex_part(Q,FP,len(V)); band=np.asarray((M>0).sum(1)).ravel()>1
nV=len(V); nF=len(Q); A=neighbors(Q,nV)
VF=sp.coo_matrix((np.ones(4*nF),(Q.ravel(),np.repeat(np.arange(nF),4))),shape=(nV,nF)).tocsr()
def qual(X,F):
    ang=[]
    for i in range(4):
        a=X[Q[F,(i-1)%4]]-X[Q[F,i]]; b=X[Q[F,(i+1)%4]]-X[Q[F,i]]
        ang.append(np.degrees(np.arccos(np.clip((a*b).sum(1)/np.maximum(np.linalg.norm(a,axis=1)*np.linalg.norm(b,axis=1),1e-12),-1,1))))
    ang=np.stack(ang,1); el=np.stack([np.linalg.norm(X[Q[F,(i+1)%4]]-X[Q[F,i]],axis=1) for i in range(4)],1)
    asp=(el[:,0]+el[:,2])/np.maximum(el[:,1]+el[:,3],1e-12); asp=np.maximum(asp,1/np.maximum(asp,1e-12))
    bad=np.maximum(0,45-ang.min(1))/45+np.maximum(0,ang.max(1)-135)/45+np.maximum(0,asp-4)/4
    hard=(ang.min(1)<20)|(ang.max(1)>160)|(asp>8)
    return bad,hard,ang
def fn(X,F):
    n=np.cross(X[Q[F,2]]-X[Q[F,0]],X[Q[F,3]]-X[Q[F,1]]); return n/np.maximum(np.linalg.norm(n,axis=1),1e-12)[:,None]

def devok(Vo,Vn,F,gi):
    # deviation guard: source points under the patch must stay covered (src->prod) and moved vertices must stay on the source
    pv_=np.unique(Q[F].ravel()); ctr=Vo[pv_]; rad=np.linalg.norm(Vo[Q[F,0]]-Vo[Q[F,2]],axis=1).max()
    ids=np.unique(np.concatenate([np.array(x,int) for x in _SKD.query_ball_point(ctr,rad)]+[np.zeros(0,int)]))
    if len(ids)==0: return True
    Tq=np.r_[Q[F][:,[0,1,2]],Q[F][:,[0,2,3]]]
    d0=np.sqrt(_igl.point_mesh_squared_distance(PR.SV[ids],Vo,Tq)[0]); d1=np.sqrt(_igl.point_mesh_squared_distance(PR.SV[ids],Vn,Tq)[0])
    # only source points that the patch actually covers before (closest to it) are judged
    m=d0<rad*0.5
    if m.any() and d1[m].max()>max(d0[m].max(),DMAX)+0.005: return False
    dp=np.sqrt(_igl.point_mesh_squared_distance(Vn[gi],PR.SV,PR.SF)[0])
    return dp.max()<=max(DMAX,np.sqrt(_igl.point_mesh_squared_distance(Vo[gi],PR.SV,PR.SF)[0]).max())+0.005
_,hard,_=qual(V,np.arange(nF)); H=np.nonzero(hard)[0]; print('hard',len(H))
# clusters of hard faces by shared vertices
FA=((VF.T@VF)>0).tocsr()
seen=set(); clusters=[]
for f in H:
    if f in seen: continue
    st=[f]; c=[]; seen.add(f)
    while st:
        g=st.pop(); c.append(g)
        for h in FA[g].indices:
            if hard[h] and h not in seen: seen.add(h); st.append(h)
    clusters.append(c)
acc=0; n0=fn(V,np.arange(nF))
for c in clusters:
    ok=False
    for k in (K,K+1,K-1,K+2):
        vs=np.zeros(nV,bool); vs[Q[c].ravel()]=True
        for _ in range(k): vs|=(A@vs.astype(float))>0
        F=np.nonzero(np.asarray(VF[vs].sum(0)).ravel()==4)[0]          # faces fully inside
        pv=np.unique(Q[F].ravel())
        # boundary edges of patch
        E=collections.Counter()
        for q in Q[F]:
            for i in range(4): E[tuple(sorted((q[i],q[(i+1)%4])))]+=1
        be=[e for e,n in E.items() if n==1]
        if not be: continue
        adj=collections.defaultdict(list)
        for a,b in be: adj[a].append(b); adj[b].append(a)
        if any(len(v)!=2 for v in adj.values()): continue
        # single loop?
        start=be[0][0]; loop=[start]; prev=None; cur=start
        while True:
            nx=[w for w in adj[cur] if w!=prev][0]
            if nx==start: break
            loop.append(nx); prev,cur=cur,nx
        if len(loop)!=len(adj): continue
        nE=len(E); 
        if len(pv)-nE+len(F)!=1: continue
        ok=True; break
    if not ok: print('cluster',len(c),'no disk patch'); continue
    loc={v:i for i,v in enumerate(pv)}; L=np.array([loc[v] for v in loop]); X=V[pv]
    inner=np.setdiff1d(np.arange(len(pv)),L)
    if os.environ.get('LMODE','smooth')=='smooth':
        gi=pv[inner]; Vn=V.copy(); Ain=A[gi]; dg=np.asarray(Ain.sum(1)).ravel()
        for _ in range(int(os.environ.get('LIT','30'))):
            N=vnormals(Vn,Q)
            Tp=np.zeros_like(Vn); Wp=np.zeros(nV)
            for kk in range(4):
                t_=Vn[Q[F,(kk-1)%4]]+Vn[Q[F,(kk+1)%4]]-Vn[Q[F,(kk+2)%4]]; np.add.at(Tp,Q[F,kk],t_); np.add.at(Wp,Q[F,kk],1)
            par=Tp[gi]/np.maximum(Wp[gi],1)[:,None]; lap=(Ain@Vn)/dg[:,None]
            dl=0.5*lap+0.5*par-Vn[gi]; dl-=(dl*N[gi]).sum(1)[:,None]*N[gi]
            X_=Vn[gi]+0.5*dl; Pj_=PR.project(X_,vp[gi],band[gi],N[gi])
            LOFF=float(os.environ.get('LOFF','0'))
            if LOFF>0:
                off_=X_-Pj_; ln_=np.linalg.norm(off_,axis=1); Vn[gi]=Pj_+off_*np.minimum(1.0,LOFF/np.maximum(ln_,1e-12))[:,None]
            else: Vn[gi]=Pj_
        b0,h0,a0=qual(V,F); b1,h1,a1=qual(Vn,F)
        w0=np.minimum(a0.min(1),180-a0.max(1)).min(); w1=np.minimum(a1.min(1),180-a1.max(1)).min()
        flip=((fn(Vn,F)*n0[F]).sum(1)<0.2).any()
        if h1.sum()<h0.sum() and w1>=w0 and not flip and devok(V,Vn,F,gi):
            V=Vn; acc+=1; print('cluster',len(c),'k',k,'patch',len(F),'hard %d->%d worst %.1f->%.1f'%(h0.sum(),h1.sum(),w0,w1))
        else: print('cluster',len(c),'rejected hard %d->%d worst %.1f->%.1f flip %s'%(h0.sum(),h1.sum(),w0,w1,flip))
        continue
    # boundary to circle by arclength
    seg=np.linalg.norm(X[L]-X[np.roll(L,-1)],axis=1); t=np.r_[0,np.cumsum(seg)[:-1]]/seg.sum()*2*np.pi
    UVb=np.c_[np.cos(t),np.sin(t)]
    T=np.r_[Q[F][:,[0,1,2]],Q[F][:,[0,2,3]]]; T=np.vectorize(loc.get)(T)
    def solve(W):
        W=W.tocsr(); d=np.asarray(W.sum(1)).ravel(); Lp=sp.diags(d)-W
        U=np.zeros((len(pv),2)); U[L]=UVb
        Aii=Lp[inner][:,inner]; Aib=Lp[inner][:,L]
        U[inner]=np.c_[sla.spsolve(Aii.tocsc(),-Aib@UVb[:,0]),sla.spsolve(Aii.tocsc(),-Aib@UVb[:,1])]
        return U
    # mean-value weights on triangles
    r,cl,w=[],[],[]
    for tri in T:
        for j in range(3):
            i0,i1,i2=tri[j],tri[(j+1)%3],tri[(j+2)%3]
            e1=X[i1]-X[i0]; e2=X[i2]-X[i0]; l1=np.linalg.norm(e1)+1e-9; l2=np.linalg.norm(e2)+1e-9
            ang=np.arccos(np.clip(e1@e2/(l1*l2),-1,1)); tt=np.tan(ang/2)
            r+= [i0,i0]; cl+=[i1,i2]; w+=[tt/l1,tt/l2]
    Wm=sp.coo_matrix((w,(r,cl)),shape=(len(pv),len(pv)))
    Um=solve(Wm)
    # uniform Tutte on quad edges
    r,cl=[],[]
    for q in Q[F]:
        for i in range(4): a,b=loc[q[i]],loc[q[(i+1)%4]]; r+=[a,b]; cl+=[b,a]
    Wu=sp.coo_matrix((np.ones(len(r)),(r,cl)),shape=(len(pv),len(pv))); Wu.sum_duplicates(); Wu.data[:]=1
    Uu=solve(Wu)
    # map Uu back through Um triangles
    from matplotlib.tri import Triangulation, TrapezoidMapTriFinder
    try:
        tf=TrapezoidMapTriFinder(Triangulation(Um[:,0],Um[:,1],T))
    except Exception as e: print('cluster',len(c),'trifinder fail'); continue
    ti=tf(Uu[inner,0],Uu[inner,1])
    if (ti<0).any(): print('cluster',len(c),'outside'); continue
    P=Um[T[ti]]; 
    Mtx=np.stack([P[:,1]-P[:,0],P[:,2]-P[:,0]],2); bc=np.linalg.solve(Mtx,(Uu[inner]-P[:,0])[...,None])[...,0]
    Xn=X.copy(); Xn[inner]=X[T[ti,0]]*(1-bc.sum(1))[:,None]+X[T[ti,1]]*bc[:,[0]]+X[T[ti,2]]*bc[:,[1]]
    gi=pv[inner]; Vn=V.copy(); Vn[gi]=Xn[inner]
    N=vnormals(Vn,Q); Vn[gi]=PR.project(Vn[gi],vp[gi],band[gi],N[gi])
    b0,h0,a0=qual(V,F); b1,h1,a1=qual(Vn,F)
    w0=max(a0.max()-180+0, 0); worst0=np.maximum(180-a0.max(1),a0.min(1)).min(); worst1=np.maximum(180-a1.max(1),a1.min(1)).min()
    w0=np.minimum(a0.min(1),180-a0.max(1)).min(); w1=np.minimum(a1.min(1),180-a1.max(1)).min()
    flip=((fn(Vn,F)*n0[F]).sum(1)<0.2).any()
    if (h1.sum()<h0.sum() or (h1.sum()==h0.sum() and w1>w0+2)) and not flip and b1.sum()<=b0.sum()*1.05:
        V=Vn; acc+=1; print('cluster',len(c),'k',k,'patch',len(F),'hard %d->%d worst %.1f->%.1f'%(h0.sum(),h1.sum(),w0,w1))
    else: print('cluster',len(c),'rejected hard %d->%d worst %.1f->%.1f flip %s'%(h0.sum(),h1.sum(),w0,w1,flip))
_,hard,ang=qual(V,np.arange(nF)); print('accepted',acc,'of',len(clusters),'final hard',hard.sum())
np.savez(sys.argv[2],V=V,Q=Q,FP=FP)
