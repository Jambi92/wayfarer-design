# subproj.py CAGE.npz OUT.npz LEVELS : Catmull-Clark (pure quads, numpy) with face-part propagation, then guarded projection
# onto the frozen v005 source (each vertex projects only onto source faces of its own part, or its part + adjacent parts in
# junction bands), with tangential relaxation between projections.
import numpy as np, sys, json, igl, scipy.sparse as sp
sys.path.insert(0,'/tmp/claude-0/rt')
from common import *
def compact(V,Q,retmap=False):
    used=np.unique(Q); m=-np.ones(len(V),int); m[used]=np.arange(len(used))
    return (V[used],m[Q],m) if retmap else (V[used],m[Q])
def cc(V,Q,FP):
    nV=len(V); nF=len(Q)
    E=np.concatenate([Q[:,[0,1]],Q[:,[1,2]],Q[:,[2,3]],Q[:,[3,0]]]); Es=np.sort(E,1)
    ue,inv=np.unique(Es,axis=0,return_inverse=True); nE=len(ue)
    fe=inv.reshape(4,nF).T                    # face -> 4 edge ids (edge k between corner k and k+1)
    fp=V[Q].mean(1)
    # edge faces
    ef=np.zeros((nE,2),int); cnt=np.zeros(nE,int)
    for k in range(4):
        e=fe[:,k];
        for fi,ei in zip(range(nF),e):
            ef[ei,cnt[ei]]=fi; cnt[ei]+=1
    assert (cnt==2).all(),'non-manifold or boundary'
    ep=(V[ue[:,0]]+V[ue[:,1]]+fp[ef[:,0]]+fp[ef[:,1]])/4
    # vertex update
    vf=sp.coo_matrix((np.ones(nF*4),(Q.ravel(),np.repeat(np.arange(nF),4))),shape=(nV,nF)).tocsr()
    n=np.asarray(vf.sum(1)).ravel()
    Fa=(vf@fp)/n[:,None]
    ve=sp.coo_matrix((np.ones(nE*2),(ue.ravel(),np.repeat(np.arange(nE),2))),shape=(nV,nE)).tocsr()
    mid=(V[ue[:,0]]+V[ue[:,1]])/2; Ra=(ve@mid)/np.asarray(ve.sum(1)).ravel()[:,None]
    Vn=(Fa+2*Ra+(n[:,None]-3)*V)/n[:,None]
    NV=np.concatenate([Vn,ep,fp]); eo=nV; fo=nV+nE
    NQ=[]; NP=[]
    for k in range(4):
        a=Q[:,k]; e1=fe[:,k]; e0=fe[:,(k-1)%4]
        NQ.append(np.stack([a,eo+e1,fo+np.arange(nF),eo+e0],1)); NP.append(FP)
    return NV,np.concatenate(NQ),np.concatenate(NP)
def vertex_part(Q,FP,nV):
    """part per vertex = majority part of incident faces (ties -> first)"""
    out=np.zeros(nV,int);
    M=sp.coo_matrix((np.ones(Q.size),(Q.ravel(),np.repeat(FP,4))),shape=(nV,FP.max()+1)).tocsr()
    return np.asarray(M.argmax(1)).ravel(), M
class Projector:
    def __init__(s):
        s.SV,s.SF=load_src(); s.flab=np.load('/tmp/claude-0/rt/flab.npy'); s.cache={}
    def sub(s,ids):
        k=tuple(sorted(ids))
        if k not in s.cache: s.cache[k]=s.SF[np.isin(s.flab,list(k))]
        return s.cache[k]
    def project(s,P,vpart,band,N=None):
        out=P.copy()
        if not hasattr(s,'SN'):
            fn=np.cross(s.SV[s.SF[:,1]]-s.SV[s.SF[:,0]],s.SV[s.SF[:,2]]-s.SV[s.SF[:,0]]); s.SN=fn/np.maximum(np.linalg.norm(fn,axis=1),1e-12)[:,None]
        groups={}
        for i,(p,b) in enumerate(zip(vpart,band)): groups.setdefault(p,[]).append(i)
        for p,idx in groups.items():
            nm=PARTS[p]; idx=np.array(idx)
            Fo=np.nonzero(s.flab==p)[0]
            d,fi,C=igl.point_mesh_squared_distance(P[idx],s.SV,s.SF[Fo]); out[idx]=C
            ids={p}|{PID[q] for q in ADJ.get(nm,())}
            Fw=np.nonzero(np.isin(s.flab,list(ids)))[0]
            d2,fi2,C2=igl.point_mesh_squared_distance(P[idx],s.SV,s.SF[Fw])
            better=d2<d-1e-9
            if N is not None:
                better&=(s.SN[Fw[fi2]]*N[idx]).sum(1)>0.3
            else:
                better&=band[idx]
            out[idx[better]]=C2[better]
        return out
def neighbors(Q,nV):
    E=np.concatenate([Q[:,[0,1]],Q[:,[1,2]],Q[:,[2,3]],Q[:,[3,0]]]); E=np.unique(np.sort(E,1),axis=0)
    A=sp.coo_matrix((np.ones(len(E)*2),(np.r_[E[:,0],E[:,1]],np.r_[E[:,1],E[:,0]])),shape=(nV,nV)).tocsr()
    return A
def vnormals(V,Q):
    n=np.cross(V[Q[:,2]]-V[Q[:,0]],V[Q[:,3]]-V[Q[:,1]]); N=np.zeros_like(V)
    for k in range(4): np.add.at(N,Q[:,k],n)
    return N/np.maximum(np.linalg.norm(N,axis=1),1e-12)[:,None]
def run(cagefile,out,levels,relax=4):
    z=np.load(cagefile); V=z['V']; Q=z['Q']; FPn=z['FP']
    FP=np.array([PID[p] for p in FPn]) if FPn.dtype.kind in 'US' else FPn
    V,Q,cmap=compact(V,Q,True)
    PR=Projector()
    for L in range(levels):
        V,Q,FP=cc(V,Q,FP)
        vp,M=vertex_part(Q,FP,len(V)); band=np.asarray((M>0).sum(1)).ravel()>1
        A=neighbors(Q,len(V)); deg=np.asarray(A.sum(1)).ravel()
        # grow junction band by 2 rings
        for _ in range(2): band=band|((A@band.astype(float))>0)
        V=PR.project(V,vp,band,vnormals(V,Q))
        for it in range(relax if L==levels-1 else 2):
            N=vnormals(V,Q); avg=(A@V)/deg[:,None]; dlt=avg-V; dlt-=(dlt*N).sum(1)[:,None]*N
            V=PR.project(V+0.6*dlt,vp,band,N)
    np.savez(out,V=V,Q=Q,FP=FP,cmap=cmap,tags=z['tags'] if 'tags' in z else '{}')
    return V,Q,FP
if __name__=='__main__':
    V,Q,FP=run(sys.argv[1],sys.argv[2],int(sys.argv[3]))
    print('V',len(V),'Q',len(Q))
