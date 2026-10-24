# stitch_part.py BASE PART OUT ox oy oz nx ny nz "region-expr(x,f,z) on base" : replace base surface on the +n side of the plane
# (inside region) by PART's surface on the +n side, zipper the two cut loops, diffuse the snap offset, fair the seam band.
import sys, numpy as np, scipy.sparse as sp, trimesh
sys.path.insert(0,'/tmp/claude-0/rp2/tools'); from region_fair import region_fair
B=np.load(sys.argv[1]); BV=B['V'].astype(float); BF=B['Q'].astype(np.int64)
P=np.load(sys.argv[2]); PV=P['V'].astype(float); PF=P['Q'].astype(np.int64)
o=np.array([float(v) for v in sys.argv[4:7]]); nrm=np.array([float(v) for v in sys.argv[7:10]]); nrm/=np.linalg.norm(nrm)
x,f,z=BV.T; reg=eval(sys.argv[10])
gB=(BV-o)@nrm; gP=(PV-o)@nrm
# restrict the region to the connected piece (inside the box) nearest to the plane origin
from scipy.sparse.csgraph import connected_components
fr=reg[BF].all(1); FR=BF[fr]; nB=len(BV)
Ar=sp.coo_matrix((np.ones(FR.size),(np.repeat(FR[:,0],3),FR.ravel())),(nB,nB))
Ar=sp.coo_matrix((np.ones(len(FR)*3),(np.r_[FR[:,0],FR[:,1],FR[:,2]],np.r_[FR[:,1],FR[:,2],FR[:,0]])),(nB,nB))
nc,lab=connected_components(Ar,directed=False)
cand=np.nonzero(reg)[0]; near=cand[np.argmin(np.abs(gB[cand])+0.2*np.linalg.norm(BV[cand]-o,axis=1))]
reg=reg&(lab==lab[near]); print('region verts',reg.sum())
# exact plane split of base faces near the cut (keep the -n side)
kill_any=((gB>0)&reg)[BF].any(1); cross=kill_any&((gB<=0)[BF].any(1))
full=kill_any&~cross
keepF=BF[~kill_any]
_r=trimesh.intersections.slice_faces_plane(BV,BF[cross],plane_normal=-nrm,plane_origin=o); sv,sf=_r[0],_r[1]
Bm=trimesh.Trimesh(np.r_[BV,sv],np.r_[keepF,sf+len(BV)],process=False); Bm.merge_vertices(digits_vertex=7); Bm.remove_unreferenced_vertices()
BV=np.asarray(Bm.vertices); BF=np.asarray(Bm.faces); Bk=BF
gB=(BV-o)@nrm

keepP=(gP>0)[PF].all(1); Pk=PF[keepP]
def loops(F_):
    ee=np.r_[F_[:,[0,1]],F_[:,[1,2]],F_[:,[2,0]]]; es=np.sort(ee,1); uu,inv,c=np.unique(es,axis=0,return_inverse=True,return_counts=True)
    be=ee[c[inv]==1]; nxt={a:b for a,b in be}; seen=set(); L=[]
    for a in nxt:
        if a in seen: continue
        lp=[a]; seen.add(a); b=nxt[a]
        while b!=a and b not in seen and b in nxt: lp.append(b); seen.add(b); b=nxt[b]
        L.append(np.array(lp))
    return L
LB=loops(Bk); LP=loops(Pk)
# pick the loops nearest the plane inside the region
def pick(L,V):
    sc=[(np.abs((V[l]-o)@nrm).mean(),len(l),l) for l in L if len(l)>20]
    sc.sort(key=lambda t:t[0]); return sc[0][2], [(round(s,3),n) for s,n,_ in sc]
lb,infoB=pick(LB,BV); lp,infoP=pick(LP,PV); print('base loops',infoB[:4],'part loops',infoP[:4])
# keep only the part component attached to lp (drop stray pieces)
mp=trimesh.Trimesh(PV,Pk,process=False); comps=mp.split(only_watertight=False)
# snap part loop onto base loop polyline, diffuse offset into the part
A=BV[lb]; Bn=np.roll(A,-1,0)
def proj(q):
    dd=Bn-A; t=np.clip(((q-A)*dd).sum(1)/((dd*dd).sum(1)+1e-12),0,1); pp=A+t[:,None]*dd; return pp[np.argmin(np.linalg.norm(pp-q,axis=1))]
off=np.zeros_like(PV); fixed=np.zeros(len(PV),bool)
for i in lp: off[i]=proj(PV[i])-PV[i]; fixed[i]=True
print('snap offset mm mean %.2f max %.2f'%(np.linalg.norm(off[lp],axis=1).mean()*10,np.linalg.norm(off[lp],axis=1).max()*10))
e=np.r_[Pk[:,[0,1]],Pk[:,[1,2]],Pk[:,[2,0]]]; n=len(PV)
Ad=sp.coo_matrix((np.ones(len(e)*2),(np.r_[e[:,0],e[:,1]],np.r_[e[:,1],e[:,0]])),(n,n)).tocsr(); Ad.data[:]=1; deg=np.maximum(np.asarray(Ad.sum(1)).ravel(),1)
for _ in range(40):
    o2=Ad@off/deg[:,None]; o2[fixed]=off[fixed]; off=o2*np.where(fixed,1,0.95)[:,None]
PV=PV+off
# zipper in the cut plane
c=BV[lb].mean(0); e1=np.cross(nrm,[0,0,1.0] if abs(nrm[2])<0.9 else [1.0,0,0]); e1/=np.linalg.norm(e1); e2=np.cross(nrm,e1)
ang=lambda Q: np.arctan2((Q-c)@e2,(Q-c)@e1)
def dirn(Q): xx=(Q-c)@e1; yy=(Q-c)@e2; return np.sign(np.sum(xx*np.roll(yy,-1)-np.roll(xx,-1)*yy))
S_=lb.copy(); D_=lp.copy()
if dirn(BV[S_])<0: S_=S_[::-1]
if dirn(PV[D_])<0: D_=D_[::-1]
i0=np.argmin(ang(BV[S_])); S_=np.roll(S_,-i0); j0=np.argmin(np.linalg.norm(PV[D_]-BV[S_[0]],axis=1)); D_=np.roll(D_,-j0)
nS=len(BV); i=j=0; ns=len(S_); nd=len(D_); tri=[]
while i<ns or j<nd:
    a=S_[i%ns]; b=D_[j%nd]; an=S_[(i+1)%ns]; bn=D_[(j+1)%nd]
    if i>=ns: tri.append((a,bn+nS,b+nS)); j+=1; continue
    if j>=nd: tri.append((a,an,b+nS)); i+=1; continue
    if np.linalg.norm(BV[an]-PV[b])<np.linalg.norm(PV[bn]-BV[a]): tri.append((a,an,b+nS)); i+=1
    else: tri.append((a,bn+nS,b+nS)); j+=1
VV=np.r_[BV,PV]; FF=np.r_[Bk,Pk+nS,np.array(tri)]
m=trimesh.Trimesh(VV,FF,process=False); m.remove_unreferenced_vertices(); trimesh.repair.fix_winding(m)
parts=m.split(only_watertight=False)
if len(parts)>1: m=max(parts,key=lambda q:len(q.faces))
trimesh.repair.fix_normals(m)
X=np.asarray(m.vertices).copy(); Fo=np.asarray(m.faces)
from scipy.spatial import cKDTree
t=cKDTree(X); _,idx=t.query(np.r_[BV[lb],PV[lp]]); r=np.zeros(len(X)); r[idx]=1
ee=np.r_[Fo[:,[0,1]],Fo[:,[1,2]],Fo[:,[2,0]]]
for _ in range(4):
    s_=np.zeros(len(X)); np.maximum.at(s_,ee[:,0],r[ee[:,1]]); np.maximum.at(s_,ee[:,1],r[ee[:,0]]); r=np.maximum(r,0.75*s_)
X=region_fair(X,np.c_[Fo,Fo[:,0]],r,10.0,it=3)
es=np.sort(ee,1); uu,cc=np.unique(es,axis=0,return_counts=True)
print('V',len(X),'F',len(Fo),'boundary',(cc==1).sum(),'nonmanifold',(cc>2).sum(),'euler',len(X)-len(uu)+len(Fo),'pieces',len(parts))
_,pi=t.query(PV); newmask=np.zeros(len(X)); newmask[pi]=1
np.savez(sys.argv[3],V=X,Q=Fo,replaced=newmask,seam=r)
