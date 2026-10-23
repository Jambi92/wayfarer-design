import numpy as np
from collections import defaultdict
def region(V,Q,m,seed,rings):
    fs={frozenset(q):i for i,q in enumerate(Q.tolist())}
    R=seed.copy()
    vq=defaultdict(list)
    for i,q in enumerate(Q): 
        for v in q: vq[v].append(i)
    for _ in range(rings):
        vs=np.unique(Q[R]); 
        for v in vs: R[vq[v]]=True
    # mirror-close
    for i in np.where(R)[0]:
        j=fs.get(frozenset(m[Q[i]].tolist()))
        if j is not None: R[j]=True
    return R
def loops(Q,R):
    E=np.vstack([Q[R][:,[i,(i+1)%4]] for i in range(4)])
    key=[tuple(sorted(e)) for e in E.tolist()]
    from collections import Counter; c=Counter(key)
    directed=[tuple(e) for e,k in zip(E.tolist(),key) if c[k]==1]
    nxt={a:b for a,b in directed}
    if len(nxt)!=len(directed): return None
    out=[]; seen=set()
    for s in nxt:
        if s in seen: continue
        L=[s]; seen.add(s); c_=nxt[s]
        while c_!=s: L.append(c_); seen.add(c_); c_=nxt[c_]
        out.append(L)
    return out
