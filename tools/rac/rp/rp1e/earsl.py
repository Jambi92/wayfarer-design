import numpy as np, collections
w=np.load('/home/claude/stc/rp1/weld.npz'); S=w['V'].astype(float); SF=w['F'].astype(np.int64)
def slice_loops(axis, val, win=None):
    d=S[:,axis]-val; sg=np.sign(d[SF]); T=SF[(sg.min(1)<0)&(sg.max(1)>0)]
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
            if not nx:
                closed = l[0] in adj[l[-1]] and len(l)>2; break
            l.append(nx[0]); seen.add(nx[0])
        P=np.array([pos[k] for k in l])
        if win is None or win(P).all(): out.append((P,closed))
    return out
def resample(P,K,start):
    Q=np.vstack([P,P[:1]]); L=np.r_[0,np.cumsum(np.linalg.norm(np.diff(Q,axis=0),axis=1))]
    i0=start; L0=L[i0]; t=(L0+np.arange(K)*L[-1]/K)%L[-1]; out=[]
    for tv in t:
        k=int(np.clip(np.searchsorted(L,tv),1,len(L)-1)); al=(tv-L[k-1])/max(L[k]-L[k-1],1e-12); out.append(Q[k-1]+(Q[k]-Q[k-1])*al)
    return np.array(out)
