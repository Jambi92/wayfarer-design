import numpy as np, collections, sys, json
def hole_loops(F,reg):
    ed=collections.Counter()
    for k in reg:
        f=F[k]
        for i in range(len(f)): ed[(f[i],f[(i+1)%len(f)])]+=1
    bnd={a:b for (a,b) in ed if (b,a) not in ed}; seen=set(); L=[]
    for a in list(bnd):
        if a in seen: continue
        l=[a]; seen.add(a)
        while bnd.get(l[-1],a)!=a and len(l)<500: l.append(bnd[l[-1]]); seen.add(l[-1])
        L.append(l)
    return L
if __name__=='__main__':
    z=np.load(sys.argv[1]); V=z['V']; F=[list(map(int,f[f>=0])) for f in z['F']]
    reg=[int(t) for t in sys.argv[2].split(',')]
    L=hole_loops(F,reg); print([len(l) for l in L])
    for l in L:
        for i in l: print(i,V[i].round(1))
    inner=set(i for k in reg for i in F[k])-set(i for l in L for i in l); print('interior verts',sorted(inner))
