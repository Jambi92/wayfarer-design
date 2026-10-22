import numpy as np
def grid_cap(loop, X, nv0, nquads=None):
    """quad grid fill of an even boundary loop. loop: vertex ids (any orientation), X: positions lookup (callable or array),
    nv0: first new vertex id. Returns (new positions, quads) — quads use loop ids + new ids; orientation fixed by caller."""
    L=np.array(loop); n=len(L); assert n%2==0 and n>=4
    a=n//4; b=n//2-a
    if nquads is not None:
        # grid corners take one cap quad: put them on loop vertices that already have >=2 patch quads (no valence-2 doublets)
        ok=np.array([nquads[v]>=2 for v in L])
        best=None
        for aa in range(max(1,n//4-3),n//4+4):
            bb=n//2-aa
            if bb<1: continue
            for sh in range(n):
                c=[(sh)%n,(sh+aa)%n,(sh+aa+bb)%n,(sh+2*aa+bb)%n]
                if ok[c].all(): best=(abs(aa-bb),aa,bb,sh); break
            if best and best[0]<=2: break
        assert best is not None, 'no valid cap corner placement'
        _,a,b,sh=best; L=np.roll(L,-sh)
    # perimeter of an a x b grid, counter-clockwise: (i,0) i=0..a-1, (a,j) j=0..b-1, (a-i,b) i=0..a-1, (0,b-j) j=0..b-1
    per=[(i,0) for i in range(a)]+[(a,j) for j in range(b)]+[(a-i,b) for i in range(a)]+[(0,b-j) for j in range(b)]
    gid={}; P=np.asarray(X)[L]
    for t,(i,j) in enumerate(per): gid[(i,j)]=L[t]
    # Coons patch for interior positions
    def bnd(i,j): return P[per.index((i,j))]
    newp=[]; nid=nv0
    for i in range(1,a):
        for j in range(1,b):
            u=i/a; v=j/b
            p=(1-v)*bnd(i,0)+v*bnd(a-0 if False else i,b)+(1-u)*bnd(0,j)+u*bnd(a,j)-((1-u)*(1-v)*bnd(0,0)+u*(1-v)*bnd(a,0)+(1-u)*v*bnd(0,b)+u*v*bnd(a,b))
            gid[(i,j)]=nid; nid+=1; newp.append(p)
    quads=[[gid[(i,j)],gid[(i+1,j)],gid[(i+1,j+1)],gid[(i,j+1)]] for i in range(a) for j in range(b)]
    return np.array(newp).reshape(-1,3), np.array(quads,int)
def orient_like(Qpatch, Qcap):
    """flip cap quads if their shared boundary edges have the same direction as the patch's (must be opposite)"""
    pe=set()
    for q in Qpatch:
        for i in range(4): pe.add((q[i],q[(i+1)%4]))
    same=opp=0
    for q in Qcap:
        for i in range(4):
            e=(q[i],q[(i+1)%4])
            if e in pe: same+=1
            elif (e[1],e[0]) in pe: opp+=1
    return Qcap[:,::-1] if same>opp else Qcap, same, opp
