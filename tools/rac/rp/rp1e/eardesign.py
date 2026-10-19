"""Ear sub-cage design (cloud). Usage: python3 eardesign.py SIDE CAGE_IN CAGECOL_IN OUT R [OFF]
Hole = cage faces with centroid within R cm of the ear axis (through the concha floor, towards the mouth); its boundary loop B is the
base ring. For each B_i, the radial half-plane section (axis, direction of B_i) of the source gives a chain from the concha floor
up the dish, over the rim (max height), down the back to the head; rings sampled: dish 3 (arc fractions .2 .45 .7 floor->rim), rim,
back 2 (1/3, 2/3 rim->point nearest B_i). Floor ring at 0.06 of the chain; floor cap."""
import numpy as np, sys, collections, json
s,cin,colin,out=sys.argv[1:5]; R=float(sys.argv[5]); OFF=float(sys.argv[6]) if len(sys.argv)>6 else 0.0
z=np.load(cin); V=z['V'].tolist(); F=[list(map(int,f[f>=0])) for f in z['F']]; cc=np.load(colin).tolist()
w=np.load('/home/claude/stc/rp1/weld.npz'); S=w['V'].astype(float); SF=w['F'].astype(np.int64)
e=np.load('ear_%s.npy'%s); d=np.load('sim_b4_L3_dsp.npy'); P=S[e]; floor=P[d[e]>=np.percentile(d[e],95)].mean(0)
mouth=S[np.load('earroot_%s.npy'%s)].mean(0); A=mouth-floor; A/=np.linalg.norm(A)
u=np.cross(A,[0,0,1.0]); u/=np.linalg.norm(u); v=np.cross(A,u)
Vn=np.array(V); fc=np.array([Vn[f].mean(0) for f in F]); X=fc-floor; h=X@A; rr=np.linalg.norm(X-np.outer(h,A),axis=1)
reg=[k for k in range(len(F)) if rr[k]<R and -12<h[k]<12 and abs(fc[k][0]-floor[0])<9]
ed=collections.Counter()
for k in reg:
    f=F[k]
    for i in range(len(f)): ed[(f[i],f[(i+1)%len(f)])]+=1
bnd={a:b for (a,b),n in ed.items() if (b,a) not in ed}
st=next(iter(bnd)); loop=[st]
while bnd[loop[-1]]!=st: loop.append(bnd[loop[-1]])
N=len(loop); B=Vn[loop]; th=np.arctan2((B-floor)@v,(B-floor)@u)
box=(abs(S-floor)<[11,13,11]).all(1); Fb=SF[box[SF].all(1)]
# vertex normals for offset
fn=np.cross(S[SF[:,1]]-S[SF[:,0]],S[SF[:,2]]-S[SF[:,0]]); fn/=np.linalg.norm(fn,axis=1,keepdims=True)+1e-12
vn=np.zeros_like(S)
for k in range(3): np.add.at(vn,SF[:,k],fn)
vn/=np.linalg.norm(vn,axis=1,keepdims=True)+1e-12
def chain(t,Bi):
    e1=np.cos(t)*u+np.sin(t)*v; n=np.cross(A,e1); dd=(S-floor)@n; sgn=np.sign(dd[Fb]); T=Fb[(sgn.min(1)<0)&(sgn.max(1)>0)]
    segs=[]
    for tri in T:
        q=[];nq=[]
        for i,j in ((0,1),(1,2),(2,0)):
            if dd[tri[i]]*dd[tri[j]]<0:
                al=dd[tri[i]]/(dd[tri[i]]-dd[tri[j]]); q.append(S[tri[i]]+(S[tri[j]]-S[tri[i]])*al); nq.append(vn[tri[i]]*(1-al)+vn[tri[j]]*al)
        if len(q)==2:
            q=np.array(q)
            if (((q-floor)@e1)>-0.3).all(): segs.append((q,np.array(nq)))
    # chain the segments: graph on rounded endpoints
    key=lambda p:tuple(np.round(p,4)); adj=collections.defaultdict(list); pos={}; nor={}
    for q,nq in segs:
        a,b=key(q[0]),key(q[1]); adj[a].append(b); adj[b].append(a); pos[a]=q[0]; pos[b]=q[1]; nor[a]=nq[0]; nor[b]=nq[1]
    ks=list(pos); Pk=np.array([pos[k] for k in ks])
    start=ks[int(np.argmin(np.linalg.norm(Pk-floor,axis=1)))]
    # BFS longest path from start (graph is near-linear)
    import heapq
    dist={start:0.0}; prev={start:None}; pq=[(0.0,start)]
    while pq:
        dcur,k0=heapq.heappop(pq)
        if dcur>dist[k0]: continue
        for k1 in adj[k0]:
            nd=dcur+np.linalg.norm(pos[k1]-pos[k0])
            if nd<dist.get(k1,1e9): dist[k1]=nd; prev[k1]=k0; heapq.heappush(pq,(nd,k1))
    # end = chain point nearest B_i (among reached)
    rk=list(dist); Pr=np.array([pos[k] for k in rk]); end=rk[int(np.argmin(np.linalg.norm(Pr-Bi,axis=1)))]
    path=[end]
    while prev[path[-1]] is not None: path.append(prev[path[-1]])
    path=path[::-1]; C=np.array([pos[k] for k in path]); Nn=np.array([nor[k] for k in path])
    return C,Nn
rings={k:[] for k in ('floor','d1','d2','d3','rim','b1','b2')}
for t,Bi in zip(th,B):
    C,Nn=chain(t,Bi)
    L=np.r_[0,np.cumsum(np.linalg.norm(np.diff(C,axis=0),axis=1))]
    hh=(C-floor)@A; ir=int(np.argmax(hh)); sr=L[ir]; se=L[-1]
    def at(sv):
        i=int(np.clip(np.searchsorted(L,sv),1,len(L)-1)); al=(sv-L[i-1])/max(L[i]-L[i-1],1e-9)
        p=C[i-1]+(C[i]-C[i-1])*al; nn=Nn[i-1]+(Nn[i]-Nn[i-1])*al; nn/=np.linalg.norm(nn)+1e-12
        return p-OFF*nn
    rings['floor'].append(at(0.06*sr)); rings['d1'].append(at(0.25*sr)); rings['d2'].append(at(0.5*sr)); rings['d3'].append(at(0.75*sr))
    rings['rim'].append(at(sr)); rings['b1'].append(at(sr+(se-sr)/3)); rings['b2'].append(at(sr+2*(se-sr)/3))
order=['b2','b1','rim','d3','d2','d1','floor']
F=[f for k,f in enumerate(F) if k not in set(reg)]; prev=loop; ids={}
col0=int(np.bincount([cc[i] for i in loop]).argmax())
for nm in order:
    cur=[]
    for p in rings[nm]: V.append(np.asarray(p).tolist()); cc.append(col0); cur.append(len(V)-1)
    for i in range(N): F.append([prev[i],prev[(i+1)%N],cur[(i+1)%N],cur[i]])
    prev=cur; ids[nm]=cur
# cap: N even -> strip of quads
p=prev; caps=[]
lo,hi=0,N-1
caps.append([p[0],p[1],p[N-2],p[N-1]]) if False else None
i,j=1,N-2
F.append([p[N-1],p[0],p[1],p[2]]) if N==4 else None
if N>4:
    a_,b_=0,N-1
    while b_-a_>=3:
        F.append([p[a_],p[a_+1],p[b_-1],p[b_]]); a_+=1; b_-=1
    if b_-a_==2: F.append([p[a_],p[a_+1],p[a_+2]])
Fa=np.full((len(F),max(len(f) for f in F)),-1)
for k,f in enumerate(F): Fa[k,:len(f)]=f
np.savez_compressed(out,V=np.array(V),F=Fa); np.save(out.replace('.npz','_col.npy'),np.array(cc))
json.dump(dict(side=s,hole=reg,loop=[int(x) for x in loop],rings=ids,floor=floor.tolist(),axis=A.tolist()),open(out.replace('.npz','_ear%s.json'%s),'w'))
print(s,'hole faces',len(reg),'N',N,'new verts',len(V)-len(z['V']),'colour',col0)
