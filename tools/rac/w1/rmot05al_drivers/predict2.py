# AK1-equivalent (one application, fade 0.78*(1-mask)) and 2x stress (8 sequential AK1-equivalent applications,
# cumulative median displacement ~2.0x AK1). Flags: flips (any step for stress) + faces adjacent to a flipped face with fold > 60 deg.
import sys; sys.path.insert(0,'/home/claude/al'); import numpy as np, dryrun as D, scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
F1=0.78; NSTRESS=8
def face_adj(F):
    E=np.concatenate([np.sort(F[:,[0,1]],1),np.sort(F[:,[1,2]],1),np.sort(F[:,[2,0]],1)]); fid=np.tile(np.arange(len(F)),3)
    o=np.lexsort(E.T[::-1]); E,fid=E[o],fid[o]; same=(E[1:]==E[:-1]).all(1); return fid[:-1][same],fid[1:][same]
def nrm(V,F):
    n=np.cross(V[F[:,1]]-V[F[:,0]],V[F[:,2]]-V[F[:,0]]); return n/np.maximum(np.linalg.norm(n,axis=1),1e-30)[:,None]
def adjfold(S,F,fa,fb,flset):
    n=nrm(S,F); ang=np.degrees(np.arccos(np.clip((n[fa]*n[fb]).sum(1),-1,1))); out=set()
    sel=ang>60; A=np.isin(fa,list(flset)); Bm=np.isin(fb,list(flset))
    for a,b in zip(fa[sel&A&~Bm],fb[sel&A&~Bm]): out.add(int(b))
    for a,b in zip(fa[sel&Bm&~A],fb[sel&Bm&~A]): out.add(int(a))
    return out
def predict(V,F,M):
    Avg=D.adjacency(F,len(V)); fa,fb=face_adj(F)
    S1=D.run(V,F,M,F1,Avg=Avg); f1=set(D.flips(V,S1,F).tolist()); a1=adjfold(S1,F,fa,fb,f1)
    S=V.copy(); f2=set(); a2=set()
    for k in range(NSTRESS):
        S=D.run(S,F,M,F1,Avg=Avg); fl=set(D.flips(V,S,F).tolist()); f2|=fl; a2|=adjfold(S,F,fa,fb,fl)
    d1=np.linalg.norm(S1-V,axis=1)*1000; d2=np.linalg.norm(S-V,axis=1)*1000; m1=d1>0.01; m2=d2>0.01
    stats=dict(ak1=dict(median=float(np.median(d1[m1])),p95=float(np.percentile(d1[m1],95)),max=float(d1.max())),x2=dict(median=float(np.median(d2[m2])),p95=float(np.percentile(d2[m2],95)),max=float(d2.max())))
    return dict(ak1_flips=sorted(f1),ak1_adj=sorted(a1-f1),x2_flips=sorted(f2),x2_adj=sorted(a2-f2),stats=stats)
def neighbourhoods(F,faces,n,rings=2):
    # 2-ring vertex sets around each flagged face; merge overlapping ones
    E=np.concatenate([F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]); A=sp.coo_matrix((np.ones(len(E)),(E[:,0],E[:,1])),shape=(n,n)).tocsr(); A=((A+A.T)>0)
    sets=[]
    for f in faces:
        s=np.zeros(n,bool); s[F[f]]=True
        for _ in range(rings): s=s|(A@s>0)
        sets.append(np.flatnonzero(s))
    if not sets: return [],np.zeros(n,bool)
    # merge by shared vertices
    rows=np.concatenate([np.full(len(s),i) for i,s in enumerate(sets)]); cols=np.concatenate(sets)
    H=sp.coo_matrix((np.ones(len(rows)),(rows,cols)),shape=(len(sets),n)).tocsr(); G=(H@H.T)>0
    k,lab=connected_components(G,directed=False); union=np.zeros(n,bool); union[cols]=True
    groups=[sorted(set(int(faces[i]) for i in np.flatnonzero(lab==j))) for j in range(k)]
    return groups,union
