# Gate 7: regional scale surface by anisotropic, size-weighted Voronoi cells over the frozen Gate 6 base (normal displacement only).
import numpy as np, sys, igl
from scipy.spatial import cKDTree
import g7geo as G
SRC=sys.argv[1] if len(sys.argv)>1 else 'g7up.npz'; REG=sys.argv[2] if len(sys.argv)>2 else 'g7reg.npz'; OUT=sys.argv[3] if len(sys.argv)>3 else 'g7_surf.npz'
z=np.load(SRC); V=z['V'].astype(np.float64); F=z['F'].astype(np.int64)
r=np.load(REG); FAM=r['FAM']; R=r['R'].astype(np.float64); H=r['H'].astype(np.float64); EL=r['EL'].astype(np.float64); T=r['T'].astype(np.float64); N=r['N'].astype(np.float64)
n=len(V); rng=np.random.default_rng(7)
scaly=(FAM!=6)&(FAM!=7)
# ---- seeds: stochastic grid per size bin (one random vertex per occupied cell of size ~ local spacing)
bins=np.round(R/0.05)*0.05; seeds=[]
for b in np.unique(bins[scaly]):
    idx=np.where(scaly&(bins==b))[0]
    if len(idx)==0: continue
    off=rng.uniform(0,b,3); cell=np.floor((V[idx]+off)/(b*0.92)).astype(np.int64)
    key=cell[:,0]*73856093^cell[:,1]*19349663^cell[:,2]*83492791
    perm=rng.permutation(len(idx)); _,first=np.unique(key[perm],return_index=True); seeds.append(idx[perm[first]])
S=np.concatenate(seeds); print('seeds',len(S))
SP=V[S]; SR=R[S]; SH=H[S]; SE=EL[S]; ST=T[S]; SF=FAM[S]
tree=cKDTree(SP); disp=np.zeros(n); edge=np.zeros(n)
K=12
for i0 in range(0,n,400000):
    sl=slice(i0,min(n,i0+400000)); P=V[sl]
    _,nb=tree.query(P,k=K)
    D=P[:,None,:]-SP[nb]; along=np.einsum('ijk,ijk->ij',D,ST[nb]); perp=np.sqrt(np.maximum((D*D).sum(-1)-along**2,0))
    d=np.sqrt((along/SE[nb])**2+perp**2)/SR[nb]                           # size-weighted anisotropic distance
    o=np.argsort(d,1); d1=np.take_along_axis(d,o[:,:1],1)[:,0]; d2=np.take_along_axis(d,o[:,1:2],1)[:,0]
    j=np.take_along_axis(nb,o[:,:1],1)[:,0]; a1=np.take_along_axis(along,o[:,:1],1)[:,0]
    w=(d2-d1)/(d2+d1+1e-9)                                                # 0 at a cell border -> ~1 at the centre
    groove=np.clip(w/0.16,0,1); groove=groove*groove*(3-2*groove)
    dome=1-0.45*np.clip(d1,0,1.4)**2
    fam=SF[j]; h=SH[j]
    tilt=np.where((fam==1)|(fam==2),0.38*np.clip(a1/(SR[j]*SE[j]),-1,1),0.0)   # imbrication: distal free edge stands proud (overlap read)
    disp[sl]=h*(groove*(dome+tilt)-0.35); edge[sl]=1-groove
disp[~scaly]=0.0
disp[scaly]-=disp[scaly].mean()                                    # zero-mean relief: no net inflation
# ---- localized pad-like thickening on palmar/plantar contact fields (not mammalian paw pads)
segs,pads=G.world_claws_pads(); cont=FAM==5
for c,rp,kind in pads:
    dd=np.linalg.norm(V-c,axis=1); m=cont&(dd<rp*1.6)
    disp[m]+=0.16*np.exp(-(dd[m]/rp)**2*1.6)
# ---- eyes: vertically elliptical pupil (slit) and a resting nictitating fold at the anterior canthus
eyes,er,yaw=G.eyes_world()
for k,c in enumerate(eyes):
    sg=1 if c[0]>0 else -1; ax_=np.array([np.sin(yaw)*sg,np.cos(yaw),0.0]); ax_/=np.linalg.norm(ax_)
    m=FAM==7; Q=V[m]-c; q=Q/np.linalg.norm(Q,axis=1,keepdims=True)
    up=np.array([0,0,1.0]); side=np.cross(up,ax_); side/=np.linalg.norm(side)
    cosg=q@ax_; ps=q@side; pu=q@up
    slit=np.exp(-(ps/0.075)**4-(pu/0.50)**4)*(cosg>0.55)                 # vertical ellipse pupil (flat-bottomed slit)
    ed=np.zeros(m.sum()); ed-=0.11*slit
    ant=np.array([0,1.0,0])-ax_*(ax_@np.array([0,1.0,0])); ant/=np.linalg.norm(ant)+1e-9
    pa=q@ant; nict=np.exp(-((pa-0.60)/0.10)**2)*(cosg>0.15)                # thin nictitating-membrane fold, retracted at the rostral corner
    ed+=0.06*nict; disp[np.where(m)[0]]+=ed
gc=V[:,2]<1.0                                                        # ground contact: relief never lowers the sole (stance/height unchanged)
dn=np.einsum('ij,j->i',N,np.array([0,0,-1.0]))
disp[gc&(dn>0.3)]=np.minimum(disp[gc&(dn>0.3)],0.0)
Vn=V+N*disp[:,None]
Vn[:,2]=np.where(gc,np.maximum(Vn[:,2],V[:,2].min()),Vn[:,2])
np.savez_compressed(OUT,V=Vn.astype(np.float32),F=F.astype(np.int32),disp=disp.astype(np.float32),edge=edge.astype(np.float16))
print('disp cm: min %.3f max %.3f mean %.3f'%(disp.min(),disp.max(),disp.mean()))
