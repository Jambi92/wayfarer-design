import numpy as np, collections, sys
z=np.load('cage_g5b.npz'); V=z['V']; F=[list(f[f>=0]) for f in z['F']]
e2f=collections.defaultdict(list)
for k,f in enumerate(F):
    for i in range(len(f)): e2f[tuple(sorted((f[i],f[(i+1)%len(f)])))].append(k)
adj=collections.defaultdict(set)
for (a,b) in e2f: adj[a].add(b); adj[b].add(a)
def opp_edge(face,a,b):
    f=F[face]; i=f.index(a); j=f.index(b)
    # quad: edge opposite to (a,b)
    n=len(f)
    if n!=4: return None
    k=[x for x in range(4) if x not in (i,j)]
    return (f[k[0]],f[k[1]])
def ring_from_edge(a,b,maxn=60):
    # walk a face loop (ring of quads) starting with edge (a,b) -> collect the 'rung' edges = ring of vertices on one side? 
    # here: edge loop walk: continue through valence-4 vertices
    loop=[a,b]
    while len(loop)<maxn:
        p,c=loop[-2],loop[-1]
        if len(adj[c])!=4: return loop,False
        fs=set(e2f[tuple(sorted((p,c)))])
        # next = neighbour of c not sharing a face with edge (p,c)
        cand=[n for n in adj[c] if n!=p and not (set(e2f[tuple(sorted((c,n)))])&fs)]
        if len(cand)!=1: return loop,False
        nx=cand[0]
        if nx==loop[0]: return loop,True
        loop.append(nx)
    return loop,False
s=sys.argv[1]; sg=-1 if s=='R' else 1; zz=float(sys.argv[2])
# start vertex: arm vertex near given z on the outer side (max |x|)
cand=[i for i in range(len(V)) if abs(V[i,2]-zz)<3 and V[i,0]*sg>20 and V[i,0]*sg<45 and -40<V[i,1]<-10]
st=max(cand,key=lambda i:V[i,0]*sg)
for n in adj[st]:
    loop,closed=ring_from_edge(st,n)
    zs=V[loop,2]
    print('start',st,'via',n,'closed',closed,'len',len(loop),'z %.1f..%.1f'%(zs.min(),zs.max()),'x %.1f..%.1f'%(V[loop,0].min(),V[loop,0].max()))

def next_ring(cur,prev):
    cs=set(cur); ps=set(prev); nxt=[]
    for v in cur:
        ns=[n for n in adj[v] if n not in cs and n not in ps]
        if len(ns)!=1: return None
        nxt.append(ns[0])
    return nxt
cc=np.load(sys.argv[3]) if len(sys.argv)>3 else None
r0,_=ring_from_edge(st,[n for n in adj[st] if ring_from_edge(st,n)[1]][0])
# previous ring = the one below
below=next_ring(r0,[]) 
# choose direction upward
r1a=next_ring(r0,[])
rings=[r0]; prev=[]
# figure up direction: neighbours of r0 with larger z
up=[]
for v in r0:
    ns=[n for n in adj[v] if n not in set(r0)]
    up.append(max(ns,key=lambda n:V[n,2]) if ns else None)
cur=r0; prev=[v for v in [min([n for n in adj[x] if n not in set(r0)],key=lambda n:V[n,2]) for x in r0]]
for step in range(int(sys.argv[4]) if len(sys.argv)>4 else 8):
    nx=next_ring(cur,prev)
    if nx is None: print('ring stops after', step); break
    print('ring',step+1,'z %.1f..%.1f'%(V[nx,2].min(),V[nx,2].max()),'verts',nx, 'cols',cc[nx].tolist() if cc is not None else '')
    prev,cur=cur,nx
