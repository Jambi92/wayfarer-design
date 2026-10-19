# edgeloop.py CAGE u v : walk the edge loop through edge (u,v) (valence-4 continuation), print vertex loop
import numpy as np, sys, collections, json
def edgeloop(F,u,v,maxn=200):
    e2f=collections.defaultdict(list); vf=collections.defaultdict(list)
    for k,f in enumerate(F):
        for i in range(len(f)): e2f[frozenset((f[i],f[(i+1)%len(f)]))].append(k)
        for i in f: vf[i].append(k)
    loop=[u,v]
    while len(loop)<maxn:
        a,b=loop[-2],loop[-1]
        fs=vf[b]
        if len(fs)!=4: return loop,'pole at %d'%b
        # faces adjacent to edge (a,b)
        fab=set(e2f[frozenset((a,b))])
        # next vertex: neighbor of b not sharing a face with edge (a,b)
        nb=set()
        for k in fs:
            f=F[k]; i=f.index(b); nb|={f[(i+1)%len(f)],f[(i-1)%len(f)]}
        cand=[]
        for c in nb:
            if c==a: continue
            fbc=set(e2f[frozenset((b,c))])
            if not (fbc & fab): cand.append(c)
        if len(cand)!=1: return loop,'ambiguous at %d %s'%(b,cand)
        c=cand[0]
        if c==loop[0]: return loop,'closed'
        loop.append(c)
    return loop,'maxn'
if __name__=='__main__':
    z=np.load(sys.argv[1]); V=z['V']; F=[list(map(int,f[f>=0])) for f in z['F']]
    L,st=edgeloop(F,int(sys.argv[2]),int(sys.argv[3]))
    print(st,len(L)); print(L)
    for i in L: print(i,V[i].round(1))
