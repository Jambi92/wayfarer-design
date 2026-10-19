"""Generic cavity pocket for the cage (design only, cloud).
Usage: python3 pocket.py CAGE_IN CAGECOL_IN DSP.npy OUT NAME BOX(x0,x1,y0,y1,z0,z1) [THR NFACE OFF FRACS COLOUR]
- pocket = largest connected source component with deviation > THR mm inside BOX; mouth = its longest boundary loop;
- axis = mouth centroid -> centroid of the deepest 10 % (by deviation);
- cage region = NFACE cage faces nearest the mouth centroid (connected); its boundary loop is inset onto the mouth contour
  (same angles about the axis), then rings at FRACS of the depth fitted to source sections (+OFF cm into the flesh), cap.
Writes OUT (cage), OUT_col.npy, OUT_NAME.json (loop, rings)."""
import numpy as np, sys, collections, json
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
a=sys.argv[1:]; cin,colin,dspp,out,name,boxs=a[:6]; THR=float(a[6]) if len(a)>6 else 1.0; NFACE=int(a[7]) if len(a)>7 else 2
OFF=float(a[8]) if len(a)>8 else 0.3; FR=[float(x) for x in a[9].split(',')] if len(a)>9 else [0.25,0.55,0.82]; COL=int(a[10]) if len(a)>10 else -1
z=np.load(cin); V=z['V'].tolist(); F=[list(map(int,f[f>=0])) for f in z['F']]; cc=np.load(colin).tolist()
w=np.load('/home/claude/stc/rp1/weld.npz'); S=w['V'].astype(float); SF=w['F'].astype(np.int64); d=np.load(dspp)
box=np.array([float(x) for x in boxs.split(',')]).reshape(3,2)
m=((S>box[:,0])&(S<box[:,1])).all(1)&(d>THR)
Fm=SF[m[SF].all(1)]; E=np.concatenate([Fm[:,[0,1]],Fm[:,[1,2]],Fm[:,[2,0]]])
k,lab=connected_components(coo_matrix((np.ones(len(E)),(E[:,0],E[:,1])),shape=(len(S),len(S))),directed=False)
big=np.bincount(lab[m]).argmax(); em=(lab==big)&m; e=np.where(em)[0]
Fe=SF[em[SF].all(1)]; ed=collections.Counter()
for f in Fe:
    for x,y in ((f[0],f[1]),(f[1],f[2]),(f[2],f[0])): ed[(min(x,y),max(x,y))]+=1
adj=collections.defaultdict(list)
for (x,y),n in ed.items():
    if n==1: adj[x].append(y); adj[y].append(x)
seen=set(); loops=[]
for st in adj:
    if st in seen: continue
    loop=[st]; seen.add(st); prev=None; cur=st
    while True:
        nx=[q for q in adj[cur] if q!=prev and q not in seen]
        if not nx: break
        prev,cur=cur,nx[0]; loop.append(cur); seen.add(cur)
    loops.append(loop)
root=np.array(max(loops,key=len)); Rr=S[root]; c=Rr.mean(0)
de=d[e]; deep=S[e][de>=np.percentile(de,90)].mean(0); ax=deep-c; depth=np.linalg.norm(ax); ax/=depth
u=np.cross(ax,[0,0,1.0]); 
if np.linalg.norm(u)<0.3: u=np.cross(ax,[1.0,0,0])
u/=np.linalg.norm(u); v=np.cross(ax,u)
# cage region: NFACE nearest faces (grown connected from the nearest)
fc=np.array([np.mean([V[i] for i in f],0) for f in F]); dist=np.linalg.norm(fc-c,axis=1)
e2f=collections.defaultdict(list)
for kf,f in enumerate(F):
    for i in range(len(f)): e2f[tuple(sorted((f[i],f[(i+1)%len(f)])))].append(kf)
from matplotlib.path import Path as MPath
def bloop(reg):
    ed2=collections.Counter()
    for kf in reg:
        f=F[kf]
        for i in range(len(f)): ed2[(f[i],f[(i+1)%len(f)])]+=1
    bnd={x:y for (x,y),n in ed2.items() if (y,x) not in ed2}
    st=next(iter(bnd)); lp=[st]
    while bnd[lp[-1]]!=st:
        lp.append(bnd[lp[-1]])
        if len(lp)>200: return None
    return lp
def encloses(reg):
    lp=bloop(reg)
    if lp is None: return False
    B=np.array([V[i] for i in lp]); P2=np.c_[(B-c)@u,(B-c)@v]; M2=np.c_[(Rr-c)@u,(Rr-c)@v]
    return MPath(P2).contains_points(M2).mean()>0.97
reg=[int(np.argmin(dist))]
while len(reg)<NFACE:
    cand=set()
    for kf in reg:
        f=F[kf]
        for i in range(len(f)): cand|=set(e2f[tuple(sorted((f[i],f[(i+1)%len(f)])))])
    cand-=set(reg); reg.append(min(cand,key=lambda q:dist[q]))
ed2=collections.Counter()
for kf in reg:
    f=F[kf]
    for i in range(len(f)): ed2[(f[i],f[(i+1)%len(f)])]+=1
bnd={x:y for (x,y),n in ed2.items() if (y,x) not in ed2}
st=next(iter(bnd)); loop=[st]
while bnd[loop[-1]]!=st: loop.append(bnd[loop[-1]])
nb=len(loop); B=np.array([V[i] for i in loop]); th=np.arctan2((B-c)@v,(B-c)@u)
def contour_ring(o,th,off):
    dd=(S-o)@ax; sg=np.sign(dd[Fe]); T=Fe[(sg.min(1)<0)&(sg.max(1)>0)]; pts=[]
    for t in T:
        q=[]
        for i,j in ((0,1),(1,2),(2,0)):
            if dd[t[i]]*dd[t[j]]<0: al=dd[t[i]]/(dd[t[i]]-dd[t[j]]); q.append(S[t[i]]+(S[t[j]]-S[t[i]])*al)
        if len(q)==2: pts+=q
    if len(pts)<6: return None
    P=np.array(pts); cen=P.mean(0); X=P-cen; ang=np.arctan2(X@v,X@u); rad=np.hypot(X@u,X@v); R=[]
    for t in th:
        mm=abs(np.angle(np.exp(1j*(ang-t))))<0.35
        R.append(cen+((rad[mm].max() if mm.any() else rad.mean())+off)*(np.cos(t)*u+np.sin(t)*v))
    return np.array(R)
INS=float(__import__('os').environ.get('INS','0.35'))
Bc=B.mean(0); rings=[B+INS*(Bc-B)+float(__import__('os').environ.get('SINK','0.3'))*ax]
for fr in FR:
    r=contour_ring(c+fr*depth*ax,th,OFF)
    if r is not None: rings.append(r)
col0=COL if COL>0 else int(np.bincount([cc[i] for i in loop]).argmax())
F=[f for kf,f in enumerate(F) if kf not in set(reg)]; prev=loop; ids=[]
for R in rings:
    cur=[]
    for p in R: V.append(p.tolist()); cc.append(col0); cur.append(len(V)-1)
    for i in range(nb): F.append([prev[i],prev[(i+1)%nb],cur[(i+1)%nb],cur[i]])
    prev=cur; ids.append(cur)
if nb==4: F.append(prev[::-1])
elif nb==6: F.append([prev[3],prev[2],prev[1],prev[0]]); F.append([prev[0],prev[5],prev[4],prev[3]])
elif nb==8: F.append([prev[3],prev[2],prev[1],prev[0]]); F.append([prev[7],prev[4],prev[3],prev[0]]); F.append([prev[7],prev[6],prev[5],prev[4]])
else: F.append(prev[::-1])
Fa=np.full((len(F),max(len(f) for f in F)),-1)
for kf,f in enumerate(F): Fa[kf,:len(f)]=f
np.savez_compressed(out,V=np.array(V),F=Fa); np.save(out.replace('.npz','_col.npy'),np.array(cc))
info=dict(name=name,region_faces=reg,loop=[int(x) for x in loop],rings=ids,axis=ax.tolist(),depth=float(depth),mouth=c.tolist(),colour=col0)
json.dump(info,open(out.replace('.npz','_%s.json'%name),'w'))
print(name,'enclosed',encloses(reg),'pocket src verts',em.sum(),'mouth loop',len(root),'depth %.1f'%depth,'axis',ax.round(2),'region faces',reg,'nb',nb,'rings',len(rings),'colour',col0)
