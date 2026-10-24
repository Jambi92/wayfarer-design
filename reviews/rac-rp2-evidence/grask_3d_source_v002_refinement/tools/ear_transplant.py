# ear_transplant.py IN OUT : replace the under-formed left ear (x>0) by a mirrored copy of the anatomically complete right ear, zippered on the scalp
import sys, numpy as np, scipy.sparse as sp, trimesh
sys.path.insert(0,'/tmp/claude-0/src3d/tools'); sys.path.insert(0,'/tmp/claude-0/rp2/tools')
from region_fair import region_fair
d=np.load(sys.argv[1]); V=d['V'].astype(float); F=d['Q'].astype(np.int64); n=len(V)
e=np.r_[F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]
def dil(m,k):
    m=m.copy()
    for _ in range(k):
        s=np.zeros(n,bool); s[e[m[e[:,1]],0]]=True; m|=s
    return m
def region(sg):
    x,f,z=V.T; xs=sg*x
    core=(xs>8.8)&(z>190)&(z<214)&(f>-10)&(f<4)
    return dil(core,int(sys.argv[3]) if len(sys.argv)>3 else 4)
from scipy.sparse.csgraph import connected_components
def fill(fm):
    idx=np.nonzero(~fm)[0]; sub=F[idx]
    rows=np.repeat(np.arange(len(idx)),3); Am=sp.coo_matrix((np.ones(len(rows)),(rows,sub.ravel())),(len(idx),n)).tocsr()
    nc,lab=connected_components(Am@Am.T,directed=False); big=np.bincount(lab).argmax()
    fm=fm.copy(); fm[idx[lab!=big]]=True; return fm
RL=region(1); RR=region(-1)
def largest(fm):
    idx=np.nonzero(fm)[0]; sub=F[idx]
    rows=np.repeat(np.arange(len(idx)),3); Am=sp.coo_matrix((np.ones(len(rows)),(rows,sub.ravel())),(len(idx),n)).tocsr()
    nc,lab=connected_components(Am@Am.T,directed=False); big=np.bincount(lab).argmax()
    out=np.zeros_like(fm); out[idx[lab==big]]=True; return out
fL=fill(largest(RL[F].all(1))); fR=fill(largest(RR[F].all(1)))
print('region faces',fL.sum(),fR.sum())
Fkeep=F[~fL]; P=F[fR]
# patch: mirrored right ear
u=np.unique(P); mp=-np.ones(n,int); mp[u]=np.arange(len(u)); PV=V[u]*np.array([-1,1,1]); PF=mp[P][:,[0,2,1]]
def loops(F_):
    ee=np.r_[F_[:,[0,1]],F_[:,[1,2]],F_[:,[2,0]]]; es=np.sort(ee,1); uu,inv,c=np.unique(es,axis=0,return_inverse=True,return_counts=True)
    be=ee[c[inv]==1]; nxt={a:b for a,b in be}; seen=set(); L=[]
    for a in nxt:
        if a in seen: continue
        lp=[a]; seen.add(a); b=nxt[a]
        while b!=a and b not in seen and b in nxt: lp.append(b); seen.add(b); b=nxt[b]
        L.append(np.array(lp))
    return L
Lk=[l for l in loops(Fkeep) if len(l)>10]; Lp=[l for l in loops(PF) if len(l)>10]
print('hole loops',[len(l) for l in Lk],'patch loops',[len(l) for l in Lp])
assert len(Lk)==1 and len(Lp)==1
lk=Lk[0]; lp=Lp[0]
# fit patch to hole: offset at boundary (nearest point on hole polyline), diffused inward
A=V[lk]; B=np.roll(A,-1,0)
def proj(q):
    dd=B-A; t=np.clip(((q-A)*dd).sum(1)/((dd*dd).sum(1)+1e-12),0,1); pp=A+t[:,None]*dd; return pp[np.argmin(np.linalg.norm(pp-q,axis=1))]
off=np.zeros_like(PV); fixed=np.zeros(len(PV),bool)
for i in lp: off[i]=proj(PV[i])-PV[i]; fixed[i]=True
print('boundary offset mm mean %.2f max %.2f'%(np.linalg.norm(off[lp],axis=1).mean()*10,np.linalg.norm(off[lp],axis=1).max()*10))
pe=np.r_[PF[:,[0,1]],PF[:,[1,2]],PF[:,[2,0]]]; m_=len(PV)
Ad=sp.coo_matrix((np.ones(len(pe)*2),(np.r_[pe[:,0],pe[:,1]],np.r_[pe[:,1],pe[:,0]])),(m_,m_)).tocsr(); Ad.data[:]=1; deg=np.asarray(Ad.sum(1)).ravel()
for _ in range(60):
    o2=Ad@off/deg[:,None]; o2[fixed]=off[fixed]; off=o2*np.where(fixed,1,0.97)[:,None]
PV=PV+off
# zipper in the (f,z) plane around the loop centre
c=V[lk].mean(0); ang=lambda Q: np.arctan2(Q[:,2]-c[2],Q[:,1]-c[1])
def dirn(Q): x=Q[:,1]-c[1]; y=Q[:,2]-c[2]; return np.sign(np.sum(x*np.roll(y,-1)-np.roll(x,-1)*y))
S_=lk.copy(); D_=lp.copy()
if dirn(V[S_])<0: S_=S_[::-1]
if dirn(PV[D_])<0: D_=D_[::-1]
i0=np.argmin(ang(V[S_])); S_=np.roll(S_,-i0); j0=np.argmin(np.linalg.norm(PV[D_]-V[S_[0]],axis=1)); D_=np.roll(D_,-j0)
nS=n; i=j=0; ns=len(S_); nd=len(D_); tri=[]
while i<ns or j<nd:
    a=S_[i%ns]; b=D_[j%nd]; an=S_[(i+1)%ns]; bn=D_[(j+1)%nd]
    if i>=ns: tri.append((a,bn+nS,b+nS)); j+=1; continue
    if j>=nd: tri.append((a,an,b+nS)); i+=1; continue
    if np.linalg.norm(V[an]-PV[b])<np.linalg.norm(PV[bn]-V[a]): tri.append((a,an,b+nS)); i+=1
    else: tri.append((a,bn+nS,b+nS)); j+=1
VV=np.r_[V,PV]; FF=np.r_[Fkeep,PF+nS,np.array(tri)]
m=trimesh.Trimesh(VV,FF,process=False); m.remove_unreferenced_vertices(); trimesh.repair.fix_winding(m); trimesh.repair.fix_normals(m)
X=np.asarray(m.vertices).copy(); Fo=np.asarray(m.faces)
# seam fair: vertices near the zipper
seamv=np.zeros(len(X),bool)
k=np.isin(np.arange(len(VV)),np.r_[lk,lp+nS])
# map old->new index via KD on positions
from scipy.spatial import cKDTree
t=cKDTree(X); _,idx=t.query(VV[k]); seamv[idx]=True
ee=np.r_[Fo[:,[0,1]],Fo[:,[1,2]],Fo[:,[2,0]]]; r=seamv.astype(float)
for _ in range(3):
    s=np.zeros(len(X)); np.maximum.at(s,ee[:,0],r[ee[:,1]]); np.maximum.at(s,ee[:,1],r[ee[:,0]]); r=np.maximum(r,0.7*s)
X=region_fair(X,np.c_[Fo,Fo[:,0]],r,20.0,it=3)
es=np.sort(ee,1); uu,cc=np.unique(es,axis=0,return_counts=True)
print('V',len(X),'F',len(Fo),'boundary',(cc==1).sum(),'nonmanifold',(cc>2).sum(),'watertight',m.is_watertight,'euler',m.euler_number,'components',len(m.split(only_watertight=False)))
mask=np.zeros(len(X)); _,ii=t.query(PV); mask[ii]=1
np.savez(sys.argv[2],V=X,Q=Fo,ear_transplant_mask=mask,seam_fair=r)
