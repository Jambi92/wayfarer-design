# ccmat.py: Catmull-Clark subdivision as sparse matrices (closed manifold, polygons of any size)
import numpy as np, scipy.sparse as sp
def cc_step(n, F):
    # returns (M, F1): V1 = M @ V ; new verts ordered [orig verts | face points | edge points]
    nf=len(F); edges={}; vf=[[] for _ in range(n)]; ve=[set() for _ in range(n)]
    for k,f in enumerate(F):
        m=len(f)
        for i in range(m):
            a,b=f[i],f[(i+1)%m]; key=(min(a,b),max(a,b))
            edges.setdefault(key,[]).append(k); vf[a].append(k); ve[a].add(key); ve[b].add(key)
    ekeys=list(edges); eidx={e:i for i,e in enumerate(ekeys)}; ne=len(ekeys)
    R=[];C=[];D=[]
    def add(r,c,v): R.append(r); C.append(c); D.append(v)
    fo=n; eo=n+nf
    # face points
    for k,f in enumerate(F):
        for v in f: add(fo+k,v,1.0/len(f))
    # edge points: (a+b+fp1+fp2)/4
    for e,i in eidx.items():
        a,b=e; fs=edges[e]; assert len(fs)==2, 'non-manifold edge'
        add(eo+i,a,0.25); add(eo+i,b,0.25)
        for k in fs:
            for v in F[k]: add(eo+i,v,0.25/len(F[k]))
    # vertex points: (Q + 2R + (n-3)P)/n
    for v in range(n):
        val=len(ve[v]); fs=vf[v]
        for k in fs:
            for u in F[k]: add(v,u,1.0/len(F[k])/len(fs)/val)
        for (a,b) in ve[v]:
            add(v,a,2*0.5/len(ve[v])/val); add(v,b,2*0.5/len(ve[v])/val)
        add(v,v,(val-3)/val)
    M=sp.csr_matrix((D,(R,C)),shape=(n+nf+ne,n))
    F1=[]
    for k,f in enumerate(F):
        m=len(f)
        for i in range(m):
            a=f[i]; ep=eo+eidx[(min(a,f[(i+1)%m]),max(a,f[(i+1)%m]))]; em=eo+eidx[(min(a,f[(i-1)%m]),max(a,f[(i-1)%m]))]
            F1.append([a,ep,fo+k,em])
    return M,F1
def cc_matrix(n,F,L):
    M=sp.identity(n,format='csr'); cur=F; m=n
    for _ in range(L):
        S,cur=cc_step(m,cur); M=S@M; m=S.shape[0]
    return M,cur
def limit_matrix(n,F):
    # F: all-quad mesh (after >=1 CC step). v_lim = (n^2 v + 4 sum e_j + sum d_j) / (n(n+5))
    R=[];C=[];D=[]; nb=[set() for _ in range(n)]; diag=[[] for _ in range(n)]
    for f in F:
        for i in range(4):
            a=f[i]; nb[a].add(f[(i+1)%4]); nb[a].add(f[(i-1)%4]); diag[a].append(f[(i+2)%4])
    for v in range(n):
        k=len(nb[v]); den=k*(k+5.0)
        R.append(v);C.append(v);D.append(k*k/den)
        for u in nb[v]: R.append(v);C.append(u);D.append(4.0/den)
        for u in diag[v]: R.append(v);C.append(u);D.append(1.0/den)
    return sp.csr_matrix((D,(R,C)),shape=(n,n))
