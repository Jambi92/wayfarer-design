import numpy as np, collections, sys, json
exec(open('loops.py').read().split("s=sys.argv[1]")[0])
from scipy.spatial import cKDTree
def arm_rings(s,zz=125):
    sg=-1 if s=='R' else 1
    cand=[i for i in range(len(V)) if abs(V[i,2]-zz)<3 and V[i,0]*sg>20 and V[i,0]*sg<45 and -40<V[i,1]<-10]
    st=max(cand,key=lambda i:V[i,0]*sg)
    r0,_=ring_from_edge(st,[n for n in adj[st] if ring_from_edge(st,n)[1]][0])
    def next_ring(cur,prev):
        cs=set(cur); ps=set(prev); nxt=[]
        for v in cur:
            ns=[n for n in adj[v] if n not in cs and n not in ps]
            if len(ns)!=1: return None
            nxt.append(ns[0])
        return nxt
    prev=[min([n for n in adj[x] if n not in set(r0)],key=lambda n:V[n,2]) for x in r0]
    rings=[r0]; cur=r0
    while True:
        nx=next_ring(cur,prev)
        if nx is None: break
        rings.append(nx); prev,cur=cur,nx
    return rings
if __name__=='__main__':
    s=sys.argv[1]; cc=np.load(sys.argv[2])
    rings=arm_rings(s); J=rings[-1]; R10=rings[-2]
    print(s,'n rings',len(rings),'junction ring',J)
    Cr=np.load('crease_%s.npy'%s)[:,:3]; T=cKDTree(Cr)
    out=set(J)|set(R10)
    for v in J:
        nb=[n for n in adj[v] if n not in out]
        d,_=T.query(V[v])
        print(v,V[v].round(1),'col',cc[v],'d_crease %.2f'%d,'val',len(adj[v]),'trunk-side nbrs',[(n,cc[n],V[n].round(1).tolist()) for n in nb])
