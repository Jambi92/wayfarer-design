"""Ear concha pocket prototype (design only). Usage: python3 earpocket.py SIDE CAGE_IN CAGECOL_IN OUT FACES(comma) [OFF FRACS]"""
import numpy as np, sys, collections, json
s,cin,colin,out,fl=sys.argv[1:6]; OFF=float(sys.argv[6]) if len(sys.argv)>6 else 0.3
FR=[float(x) for x in sys.argv[7].split(',')] if len(sys.argv)>7 else [0.25,0.55,0.82]
z=np.load(cin); V=z['V'].tolist(); F=[list(map(int,f[f>=0])) for f in z['F']]; cc=np.load(colin).tolist()
w=np.load('/home/claude/stc/rp1/weld.npz'); S=w['V'].astype(float); SF=w['F'].astype(np.int64)
root=np.load('earroot_%s.npy'%s); e=np.load('ear_%s.npy'%s); em=np.zeros(len(S),bool); em[e]=True
c=S[root].mean(0); P=S[e]; deep=P[P[:,1]>np.percentile(P[:,1],95)].mean(0); ax=deep-c; depth=np.linalg.norm(ax); ax/=depth
u=np.cross(ax,[0,0,1.0]); u/=np.linalg.norm(u); v=np.cross(ax,u)
reg=[int(x) for x in fl.split(',')]
# boundary loop of the region (ordered)
ed=collections.Counter(); 
for k in reg:
    f=F[k]
    for i in range(len(f)): ed[(f[i],f[(i+1)%len(f)])]+=1
bnd={a:b for (a,b),n in ed.items() if (b,a) not in ed}
st=next(iter(bnd)); loop=[st]
while bnd[loop[-1]]!=st: loop.append(bnd[loop[-1]])
nb=len(loop); B=np.array([V[i] for i in loop])
th=np.arctan2((B-c)@v,(B-c)@u)
def contour_ring(o,th,off):
    # section of the pocket surface (ear faces) by plane through o normal ax; ray from section centroid at angles th
    Fe=SF[em[SF].all(1)]; d=(S-o)@ax; sgn=np.sign(d[Fe]); Fe=Fe[(sgn.min(1)<0)&(sgn.max(1)>0)]
    pts=[]
    for t in Fe:
        q=[]
        for i,j in ((0,1),(1,2),(2,0)):
            if d[t[i]]*d[t[j]]<0: a_=d[t[i]]/(d[t[i]]-d[t[j]]); q.append(S[t[i]]+(S[t[j]]-S[t[i]])*a_)
        if len(q)==2: pts.append(q)
    pts=np.array(pts); 
    if not len(pts): return None
    cen=pts.reshape(-1,3).mean(0); X=pts.reshape(-1,3)-cen; ang=np.arctan2(X@v,X@u); rad=np.sqrt((X@u)**2+(X@v)**2)
    R=[]
    for t in th:
        dd=np.angle(np.exp(1j*(ang-t))); m=abs(dd)<0.35
        r=rad[m].max() if m.any() else rad.mean()
        R.append(cen+(r+off)*(np.cos(t)*u+np.sin(t)*v))
    return np.array(R)
rings=[]
# mouth ring: on the mouth contour (source root loop) at the same angles, no offset
import os
INS=float(os.environ.get('INS','-1'))
if INS<0:
    Rr=S[root]; ang=np.arctan2((Rr-c)@v,(Rr-c)@u)
    M0=[Rr[np.argmin(abs(np.angle(np.exp(1j*(ang-t)))))] for t in th]; rings.append(np.array(M0))
else:
    Bc=B.mean(0); rings.append(B+INS*(Bc-B)+float(os.environ.get('SINK','0.3'))*ax)
for f in FR:
    r=contour_ring(c+f*depth*ax,th,OFF)
    if r is None: print('no section at',f); continue
    rings.append(r)
# build: delete region faces, add inset quads boundary->M0, ring quads, cap
F=[f for k,f in enumerate(F) if k not in set(reg)]
prev=loop; ids=[]
for R in rings:
    cur=[]
    for p in R: V.append(p.tolist()); cc.append(2); cur.append(len(V)-1)
    for i in range(nb): F.append([prev[i],prev[(i+1)%nb],cur[(i+1)%nb],cur[i]])
    prev=cur; ids.append(cur)
if nb==4: F.append(prev[::-1])
elif nb==6: F.append([prev[3],prev[2],prev[1],prev[0]]); F.append([prev[0],prev[5],prev[4],prev[3]])
else: F.append(prev[::-1])
Fa=np.full((len(F),max(len(f) for f in F)),-1)
for k,f in enumerate(F): Fa[k,:len(f)]=f
np.savez_compressed(out,V=np.array(V),F=Fa); np.save(out.replace('.npz','_col.npy'),np.array(cc))
json.dump(dict(loop=loop,rings=ids),open(out.replace('.npz','_ear.json'),'w'))
print(s,'boundary',nb,'rings',len(rings),'depth %.1f'%depth,'new verts',len(V)-len(z['V']),'faces',len(F))
for k,R in enumerate(rings): print('  ring',k,np.round(R,1).tolist())
