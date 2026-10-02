import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
def clip(V,F,s,keep_pos=True):
    s=s if keep_pos else -s; s=np.where(np.abs(s)<1e-7,1e-7,s)
    pos=s[F]>0; npos=pos.sum(1); out=[F[npos==3]]; newV=[]; key={}
    def ev(a,b):
        k=(min(a,b),max(a,b))
        if k not in key:
            t=s[a]/(s[a]-s[b]); key[k]=len(V)+len(newV); newV.append(V[a]+t*(V[b]-V[a]))
        return key[k]
    for tri,p in zip(F[npos==1],pos[npos==1]):
        r=np.argmax(p); a,b,c=tri[r],tri[(r+1)%3],tri[(r+2)%3]; out.append(np.array([[a,ev(a,b),ev(a,c)]]))
    for tri,p in zip(F[npos==2],pos[npos==2]):
        r=np.argmin(p); a,b,c=tri[r],tri[(r+1)%3],tri[(r+2)%3]       # a is the negative vertex
        pab,pac=ev(a,b),ev(a,c); out.append(np.array([[pab,b,c],[pab,c,pac]]))
    V2=np.concatenate([V,np.array(newV).reshape(-1,3)]); F2=np.concatenate(out); u=np.unique(F2)
    rm=-np.ones(len(V2),int); rm[u]=np.arange(len(u)); return V2[u],rm[F2]
def largest(V,F):
    e=np.concatenate([F[:,[0,1]],F[:,[1,2]]]); A=coo_matrix((np.ones(len(e)),(e[:,0],e[:,1])),shape=(len(V),)*2)
    n,l=connected_components(A,directed=False); lf=l[F[:,0]]; big=np.bincount(lf).argmax(); F=F[lf==big]
    u=np.unique(F); rm=-np.ones(len(V),int); rm[u]=np.arange(len(u)); return V[u],rm[F]
def loops(F):
    e=np.concatenate([F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]); k=np.sort(e,1); u,inv,c=np.unique(k,axis=0,return_inverse=True,return_counts=True)
    b=e[c[inv.ravel()]==1]; nxt={}
    for a,bb in b: nxt.setdefault(a,[]).append(bb)
    out=[]; used=set()
    for a0,b0 in b:
        if (a0,b0) in used: continue
        L=[a0]; x=b0; used.add((a0,b0))
        while x!=a0:
            L.append(x); cand=[y for y in nxt[x] if (x,y) not in used]
            if not cand: break
            used.add((x,cand[0])); x=cand[0]
        out.append(np.array(L))
    return out
