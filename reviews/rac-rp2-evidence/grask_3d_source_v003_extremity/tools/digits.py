# digits.py : digit segmentation (merge tree of geodesic distance from a root seed) + per-digit centerline frames
import numpy as np, scipy.sparse as sp
from scipy.sparse.csgraph import dijkstra
def graph(V,F,idx):
    loc=-np.ones(len(V),int); loc[idx]=np.arange(len(idx))
    E=np.unique(np.sort(np.r_[F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]],1),axis=0); E=E[(loc[E]>=0).all(1)]; a,b=loc[E[:,0]],loc[E[:,1]]
    w=np.linalg.norm(V[E[:,0]]-V[E[:,1]],axis=1); m=len(idx)
    return sp.coo_matrix((np.r_[w,w],(np.r_[a,b],np.r_[b,a])),(m,m)).tocsr(), loc
def segment(V,F,idx,seed,min_pers=1.5,min_size=150,verbose=False):
    G,loc=graph(V,F,idx); s0=np.argmin(np.linalg.norm(V[idx]-seed,axis=1))
    d=dijkstra(G,indices=s0); fin=np.isfinite(d)
    if not fin.all():
        idx=idx[fin]; G,loc=graph(V,F,idx); s0=np.argmin(np.linalg.norm(V[idx]-seed,axis=1)); d=dijkstra(G,indices=s0)
    m=len(idx)
    order=np.argsort(-d); parent=np.arange(m); added=np.zeros(m,bool)
    tip={}; size={}; members={}
    def find(i):
        while parent[i]!=i: parent[i]=parent[parent[i]]; i=parent[i]
        return i
    digits=[]   # (tip_d, root_d, member list)
    absorbed={}
    indptr,ind=G.indptr,G.indices
    for v in order:
        added[v]=True; tip[v]=d[v]; members[v]=[v]
        for nb in ind[indptr[v]:indptr[v+1]]:
            if not added[nb]: continue
            ra,rb=find(v),find(nb)
            if ra==rb: continue
            # older = larger tip
            if tip[ra]<tip[rb]: ra,rb=rb,ra
            if verbose and tip[rb]-d[v]>0.5: print('merge tip %.1f at %.1f size %d'%(tip[rb],d[v],len(members[rb])),np.round(V[idx[max(members[rb],key=lambda i:d[i])]],1))
            if tip[rb]-d[v]>min_pers and len(members[rb])>min_size:
                digits.append((tip[rb],d[v],list(members[rb])))
                absorbed.setdefault(ra,[]).append(d[v])
                if len(absorbed[ra])==1: absorbed[(ra,'snap')]=list(members[ra])
            parent[rb]=ra; members[ra]+=members[rb]; del members[rb]
    # oldest digit: snapshot of its members at its first absorption
    r=find(order[0])
    if (r,'snap') in absorbed:
        lv=absorbed[r][0]; mem=[i for i in absorbed[(r,'snap')] if d[i]>=lv]
        digits.append((tip[r],lv,mem))
    out=[]
    for td,rd,mem in digits:
        mem=np.array(mem); out.append(dict(idx=idx[mem],d=d[mem],root=rd,tip=td,L=td-rd))
    return out,d
def frames(V,dg,step=0.2):
    """centerline by geodesic slices; per-vertex s (0 root..1 tip), radial unit u, radius rho, local mean radius R, tangent t"""
    P=V[dg['idx']]; s=(dg['d']-dg['root'])/dg['L']
    nb=max(8,int(dg['L']/step)); bins=np.clip((s*nb).astype(int),0,nb-1)
    C=np.array([P[bins==k].mean(0) if (bins==k).any() else np.nan*np.ones(3) for k in range(nb)])
    ok=~np.isnan(C[:,0]); kk=np.arange(nb); C=np.stack([np.interp(kk,kk[ok],C[ok,j]) for j in range(3)],1)
    for _ in range(3): C[1:-1]=0.25*C[:-2]+0.5*C[1:-1]+0.25*C[2:]
    T=np.gradient(C,axis=0); T/=np.linalg.norm(T,axis=1)[:,None]
    sc=(kk+0.5)/nb
    ci=np.stack([np.interp(s,sc,C[:,j]) for j in range(3)],1); ti=np.stack([np.interp(s,sc,T[:,j]) for j in range(3)],1); ti/=np.linalg.norm(ti,axis=1)[:,None]
    r=P-ci; r-=(r*ti).sum(1)[:,None]*ti; rho=np.linalg.norm(r,axis=1); u=r/np.maximum(rho,1e-9)[:,None]
    Rb=np.array([np.median(rho[bins==k]) if (bins==k).sum()>3 else np.nan for k in range(nb)]); okr=~np.isnan(Rb); Rb=np.interp(kk,kk[okr],Rb[okr])
    R=np.interp(s,sc,Rb)
    # curl (palmar) direction from centerline curvature
    K=np.gradient(T,axis=0); kv=K.sum(0); 
    return dict(s=s,u=u,rho=rho,R=R,t=ti,c=ci,C=C,T=T,curl=kv)
