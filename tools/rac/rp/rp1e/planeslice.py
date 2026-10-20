# planeslice.py: closed loops of the source cut by an arbitrary plane (p0, n); uses earsl.S/SF (so a rotated earsl.S is honoured)
import numpy as np, collections, earsl
def plane_loops(p0,n,near=None,rad=None):
    S=earsl.S; SF=earsl.SF; n=np.asarray(n,float); n/=np.linalg.norm(n)
    d=(S-np.asarray(p0,float))@n
    if near is not None:
        m=np.linalg.norm(S[SF[:,0]]-near,axis=1)<rad; cand=SF[m]
    else: cand=SF
    sg=np.sign(d[cand]); T=cand[(sg.min(1)<0)&(sg.max(1)>0)]
    key=lambda i,j:(min(i,j),max(i,j)); adj=collections.defaultdict(list); pos={}
    for t in T:
        ks=[]
        for i,j in ((0,1),(1,2),(2,0)):
            if d[t[i]]*d[t[j]]<0:
                k=key(t[i],t[j]); al=d[k[0]]/(d[k[0]]-d[k[1]]); pos[k]=S[k[0]]+(S[k[1]]-S[k[0]])*al; ks.append(k)
        if len(ks)==2: adj[ks[0]].append(ks[1]); adj[ks[1]].append(ks[0])
    seen=set(); out=[]
    for k0 in list(adj):
        if k0 in seen: continue
        l=[k0]; seen.add(k0); closed=False
        while True:
            nx=[k for k in adj[l[-1]] if k not in seen]
            if not nx: closed=l[0] in adj[l[-1]] and len(l)>2; break
            l.append(nx[0]); seen.add(nx[0])
        out.append((np.array([pos[k] for k in l]),closed))
    return out
def axis_rings(seed,t0,h,maxn=12,minr=0.25,rad=6.0,smooth=0.5,maxjump=1.5):
    # march along a digit: plane through c with normal t, nearest closed loop, recentre, step
    c=np.asarray(seed,float); t=np.asarray(t0,float); t/=np.linalg.norm(t); out=[]
    for k in range(maxn):
        L=[P for P,cl in plane_loops(c,t,near=c,rad=rad) if cl]
        if not L: break
        P=min(L,key=lambda P:np.linalg.norm(P.mean(0)-c)); cen=P.mean(0)
        if np.linalg.norm(cen-c)>maxjump: break
        r=np.sqrt(np.mean(np.sum((P-cen)**2,axis=1)))
        if r<minr: break
        out.append((cen,t.copy(),P,r))
        if len(out)>1:
            nt=out[-1][0]-out[-2][0]; nt/=np.linalg.norm(nt)+1e-12; t=(1-smooth)*t+smooth*nt; t/=np.linalg.norm(t)
        c=cen+t*h
    return out
