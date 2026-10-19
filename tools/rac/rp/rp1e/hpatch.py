"""Harmonic radial patch (design aid, cloud). Usage:
python3 hpatch.py CAGE_IN CAGECOL_IN OUT NAME CENTER(x,y,z) GEO_R K [HOLEFACES_JSON]
- source region = verts within geodesic radius GEO_R of the source vertex nearest CENTER (Dijkstra on the source edge graph);
- cage hole = cage faces whose centroid's nearest source vertex is in the region; filled to a disk; boundary loop B (N verts);
- B_i -> nearest source b_i; consecutive b_i joined by shortest source paths -> closed cut loop; the source patch = the side
  containing CENTER; harmonic map of the patch to the unit disk (cut loop -> circle by arc length);
- rings: p_ik = c* + (1 - k/K) (b*_i - c*), k = 1..K-1 (c* = image of CENTER), mapped back by barycentric lookup;
- cage: hole faces removed, B kept, K-1 new rings, centre cap (quad strip)."""
import numpy as np, sys, json, collections, igl
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra, connected_components
from scipy.spatial import cKDTree
a=sys.argv[1:]; cin,colin,out,name,cs,GR,K=a[:7]; cen=np.array([float(x) for x in cs.split(',')]); GR=float(GR); K=int(K)
z=np.load(cin); V=z['V'].astype(float); F=[list(map(int,f[f>=0])) for f in z['F']]; cc=np.load(colin).tolist()
w=np.load('/home/claude/stc/rp1/weld.npz'); S=w['V'].astype(float); SF=w['F'].astype(np.int64)
loc=(np.linalg.norm(S-cen,axis=1)<GR*1.6); idl=np.where(loc)[0]; mp=-np.ones(len(S),int); mp[idl]=np.arange(len(idl))
Fl=mp[SF[loc[SF].all(1)]]; X=S[idl]
E=np.unique(np.sort(np.concatenate([Fl[:,[0,1]],Fl[:,[1,2]],Fl[:,[2,0]]]),1),axis=0); wt=np.linalg.norm(X[E[:,0]]-X[E[:,1]],axis=1)
G=coo_matrix((wt,(E[:,0],E[:,1])),shape=(len(X),len(X))).tocsr()
c0=int(np.argmin(np.linalg.norm(X-cen,axis=1))); D=dijkstra(G,directed=False,indices=c0)
inreg=D<GR
# cage hole
fc=np.array([V[f].mean(0) for f in F]); _,ni=cKDTree(X).query(fc); import os
HR=float(os.environ.get('HOLER','0'))
hole=set(k for k in range(len(F)) if (np.linalg.norm(fc[k]-cen)<HR if HR>0 else (inreg[ni[k]] and np.linalg.norm(fc[k]-X[ni[k]])<3.0)))
if len(a)>7: hole=set(json.load(open(a[7])))
e2f=collections.defaultdict(list)
for k,f in enumerate(F):
    for i in range(len(f)): e2f[tuple(sorted((f[i],f[(i+1)%len(f)])))].append(k)
# fill to disk: complement components not containing a far face -> add
comp=set(range(len(F)))-hole; far=max(comp,key=lambda k:np.linalg.norm(fc[k]-cen)); seen={far}; st=[far]
while st:
    k=st.pop(); f=F[k]
    for i in range(len(f)):
        for q in e2f[tuple(sorted((f[i],f[(i+1)%len(f)])))]:
            if q in comp and q not in seen: seen.add(q); st.append(q)
hole|=comp-seen
# keep the hole component containing the face nearest cen
hl=list(hole); start=min(hl,key=lambda k:np.linalg.norm(fc[k]-cen)); seen={start}; st=[start]
while st:
    k=st.pop(); f=F[k]
    for i in range(len(f)):
        for q in e2f[tuple(sorted((f[i],f[(i+1)%len(f)])))]:
            if q in hole and q not in seen: seen.add(q); st.append(q)
hole=seen
ed=collections.Counter()
for k in hole:
    f=F[k]
    for i in range(len(f)): ed[(f[i],f[(i+1)%len(f)])]+=1
bnd={x:y for (x,y),n in ed.items() if (y,x) not in ed}
loops=[]; sn=set()
for x in list(bnd):
    if x in sn: continue
    l=[x]; sn.add(x)
    while bnd.get(l[-1],x)!=x and len(l)<400: l.append(bnd[l[-1]]); sn.add(l[-1])
    loops.append(l)
loop=max(loops,key=len); N=len(loop)
print(name,'hole faces',len(hole),'loops',[len(l) for l in loops],'N',N)
if len(loops)>1: print('WARNING: hole not a disk')
# cut loop on source
_,bi=cKDTree(X).query(V[loop]); cut=[]
for i in range(N):
    p,q=bi[i],bi[(i+1)%N]
    d_,pred=dijkstra(G,directed=False,indices=p,return_predecessors=True)
    path=[q]
    while path[-1]!=p: path.append(pred[path[-1]])
    path=path[::-1]
    cut+=path[:-1]
# patch = flood from c0 not crossing the cut vertices
cutset=set(cut); Ec=E[~(np.isin(E[:,0],list(cutset))|np.isin(E[:,1],list(cutset)))]
G2=coo_matrix((np.ones(len(Ec)),(Ec[:,0],Ec[:,1])),shape=(len(X),len(X)))
_,lab=connected_components(G2,directed=False); inside=(lab==lab[c0]); inside[list(cutset)]=True
Fp=Fl[inside[Fl].all(1)]; used=np.unique(Fp); m2=-np.ones(len(X),int); m2[used]=np.arange(len(used)); Fp2=m2[Fp]; Xp=X[used]
bl=igl.boundary_loop(Fp2)
print('patch verts',len(used),'faces',len(Fp2),'patch boundary',len(bl),'cut',len(cut), 'patch area %.0f'%(0.5*np.linalg.norm(np.cross(Xp[Fp2[:,1]]-Xp[Fp2[:,0]],Xp[Fp2[:,2]]-Xp[Fp2[:,0]]),axis=1).sum()))
bc=igl.map_vertices_to_circle(Xp,bl); UV=igl.harmonic(Xp,Fp2,bl,bc,1)
# images: c*, b*_i (b_i are on the cut = boundary)
cstar=UV[m2[c0]] if m2[c0]>=0 else UV.mean(0)
bstar=np.array([UV[m2[b]] if m2[b]>=0 else UV[bl[np.argmin(np.linalg.norm(Xp[bl]-X[b],axis=1))]] for b in bi])
# barycentric lookup
print('patch boundary loops',[len(l) for l in igl.boundary_loop_all(Fp2)] if hasattr(igl,'boundary_loop_all') else '?')
A2=UV[Fp2]; ar=0.5*((A2[:,1,0]-A2[:,0,0])*(A2[:,2,1]-A2[:,0,1])-(A2[:,2,0]-A2[:,0,0])*(A2[:,1,1]-A2[:,0,1]))
print('flipped uv tris',int((ar*np.sign(np.median(ar))<0).sum()),'of',len(ar))
CT=cKDTree(A2.mean(1))
def back(pt):
    _,cand=CT.query(pt,k=40); best=None
    for t in cand:
        A3=A2[t]; M=np.c_[A3[1]-A3[0],A3[2]-A3[0]]
        try: l=np.linalg.solve(M,pt-A3[0])
        except np.linalg.LinAlgError: continue
        bw=np.array([1-l.sum(),l[0],l[1]]); e=-min(bw.min(),0)
        if best is None or e<best[0]: best=(e,t,bw)
        if e==0: break
    e,t,bw=best; bw=np.clip(bw,0,None); bw/=bw.sum()
    return bw@Xp[Fp2[t]]
rings=[]
for k in range(1,K):
    tk=1-k/K; R=[]
    for i in range(N):
        p=back(cstar+tk*(bstar[i]-cstar)); R.append(p if p is not None else X[bi[i]])
    rings.append(np.array(R))
Vl=V.tolist(); col0=int(np.bincount([cc[i] for i in loop]).argmax())
F2=[f for k,f in enumerate(F) if k not in hole]; prev=loop; ids=[]
for R in rings:
    cur=[]
    for p in R: Vl.append(p.tolist()); cc.append(col0); cur.append(len(Vl)-1)
    for i in range(N): F2.append([prev[i],prev[(i+1)%N],cur[(i+1)%N],cur[i]])
    prev=cur; ids.append(cur)
p=prev; a_,b_=0,N-1
while b_-a_>=3: F2.append([p[a_],p[a_+1],p[b_-1],p[b_]]); a_+=1; b_-=1
if b_-a_==2: F2.append([p[a_],p[a_+1],p[a_+2]])
Fa=np.full((len(F2),4),-1)
for k,f in enumerate(F2): Fa[k,:len(f)]=f
np.savez_compressed(out,V=np.array(Vl),F=Fa); np.save(out.replace('.npz','_col.npy'),np.array(cc))
json.dump(dict(name=name,hole=sorted(hole),loop=loop,rings=ids),open(out.replace('.npz','_%s.json'%name),'w'))
print('new verts',len(Vl)-len(V),'faces',len(F2))
