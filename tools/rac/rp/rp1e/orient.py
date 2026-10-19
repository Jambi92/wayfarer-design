import collections
def orient_patch(F_fixed, Fn):
    """flip patch faces so the whole mesh is consistently oriented; returns oriented Fn or raises"""
    Fn=[list(q) for q in Fn]
    fixed=collections.Counter((f[i],f[(i+1)%len(f)]) for f in F_fixed for i in range(len(f)))
    e2p=collections.defaultdict(list)
    for k,q in enumerate(Fn):
        for i in range(len(q)): e2p[frozenset((q[i],q[(i+1)%len(q)]))].append(k)
    state=[None]*len(Fn)
    def edges(q): return [(q[i],q[(i+1)%len(q)]) for i in range(len(q))]
    # seeds: patch faces sharing an edge with fixed faces
    from collections import deque
    dq=deque()
    for k,q in enumerate(Fn):
        for (a,b) in edges(q):
            if (a,b) in fixed: state[k]=True; break      # same direction as fixed -> must flip
            if (b,a) in fixed: state[k]=False; break
        if state[k] is not None: dq.append(k)
    while dq:
        k=dq.popleft(); q=Fn[k][::-1] if state[k] else Fn[k]
        for (a,b) in edges(q):
            for g in e2p[frozenset((a,b))]:
                if g==k or state[g] is not None: continue
                r=Fn[g]; dirs=edges(r)
                state[g]=((a,b) in dirs)   # neighbour must traverse (b,a); if it has (a,b), flip
                dq.append(g)
    if any(s is None for s in state): raise SystemExit('unreached patch faces %d'%sum(s is None for s in state))
    return [q[::-1] if s else q for q,s in zip(Fn,state)]
def check(Fs):
    de=collections.Counter((f[i],f[(i+1)%len(f)]) for f in Fs for i in range(len(f)))
    dup=sum(1 for n in de.values() if n>1); bnd=sum(1 for (x,y) in de if (y,x) not in de)
    return dup,bnd
