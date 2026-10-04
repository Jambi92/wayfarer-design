# carry the polish scale seeds onto the cleanup mesh (same scales; carried with every local correction = re-projection);
# only seeds whose base triangle no longer exists (re-meshed postorbital patch, collapsed seam slivers) are re-filled locally.
import numpy as np, igl, sys
sys.path.insert(0,'/tmp/claude-0/rodin/g1'); import seedpd
from scipy.spatial import cKDTree
P9='/tmp/claude-0/rodin/p9/'
Vu0=np.load(P9+'g12up.npz')['V'].astype(float); S_old=np.load(P9+'seeds12.npy')
b0=np.load(P9+'g12_body.npz'); VB0=b0['V'].astype(float); FB0=b0['F'].astype(np.int64)
a=np.load('g13a_body.npz'); org=a['origin']; b=np.load('g13b_body.npz'); keep=b['KEEP']; VB=np.load('g13_body.npz')['V'].astype(float)
o=org[keep]                                   # new base index -> g12 base index (or -1)
inv=-np.ones(len(VB0),np.int64); inv[o[o>=0]]=np.where(o>=0)[0]
sq,fi,cp=igl.point_mesh_squared_distance(Vu0[S_old],VB0,FB0); tri=FB0[fi]
bc=igl.barycentric_coordinates(cp,VB0[tri[:,0]],VB0[tri[:,1]],VB0[tri[:,2]])
nt=inv[tri]; ok=(nt>=0).all(1)
Pn=(VB[np.clip(nt,0,None)]*bc[:,:,None]).sum(1)
up=np.load('g13up.npz'); Vu=up['V'].astype(float); r1=np.load('g13reg.npz'); R1=r1['R'].astype(float); FAM1=r1['FAM']
d,j=cKDTree(Vu).query(Pn); ok&=(d<0.02)
S_map=np.unique(j[ok]); print('carried',len(S_map),'dropped',int((~ok).sum()),'snap max %.4f'%d[ok].max())
scaly=(FAM1!=6)&(FAM1!=7)
dd,_=cKDTree(Vu0[S_old[~ok]]).query(Vu) if (~ok).any() else (np.full(len(Vu),99.0),None)
patch=dd<0.8; print('fill region verts',int(patch.sum()))
S_new=seedpd.poisson_seeds(Vu,R1,scaly&patch,np.random.default_rng(9),c=0.50,init=S_map[scaly[S_map]])
np.save('seeds13.npy',S_new); print('final seeds',len(S_new),'new',len(S_new)-int(scaly[S_map].sum()))
