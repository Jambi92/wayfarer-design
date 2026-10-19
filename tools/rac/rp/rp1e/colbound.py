# colbound.py COL a b : ordered boundary loop(s) between source colour a and b (midpoints of crossing edges)
import numpy as np, sys, collections
w=np.load('/home/claude/stc/rp1/weld.npz'); S=w['V']; F=w['F']
def boundary_loops(c,a,b):
    T=F[(np.isin(c[F],[a]).any(1))&(np.isin(c[F],[b]).any(1))]
    key=lambda i,j:(min(i,j),max(i,j)); adj=collections.defaultdict(list); pos={}
    for t in T:
        es=[key(t[i],t[(i+1)%3]) for i in range(3) if {c[t[i]],c[t[(i+1)%3]]}=={a,b}]
        for e in es: pos[e]=(S[e[0]]+S[e[1]])/2
        if len(es)==2: adj[es[0]].append(es[1]); adj[es[1]].append(es[0])
    seen=set(); loops=[]
    for e0 in list(adj):
        if e0 in seen: continue
        l=[e0]; seen.add(e0)
        while True:
            nx=[e for e in adj[l[-1]] if e not in seen]
            if not nx: break
            l.append(nx[0]); seen.add(nx[0])
        loops.append(np.array([pos[e] for e in l]))
    return sorted(loops,key=len,reverse=True)
if __name__=='__main__':
    c=np.load(sys.argv[1]); a,b=int(sys.argv[2]),int(sys.argv[3])
    L=boundary_loops(c,a,b)
    for l in L[:5]: print(len(l),'closed?',np.linalg.norm(l[0]-l[-1]).round(2),'z %.1f..%.1f'%(l[:,2].min(),l[:,2].max()),'centroid',l.mean(0).round(1))
    np.save('J0_%d_%d.npy'%(a,b),L[0])
