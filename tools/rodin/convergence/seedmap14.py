# carry the cleanup scale seeds onto the convergence mesh. Kept: every seed whose base triangle survives AND whose local scale
# size did not change (>10 %). Re-seeded (Poisson, locally): the re-meshed orbital patch, the forearm seam ring and the new
# structural-scute fields (where the second, larger scale order replaces the fine field).
import numpy as np, igl, sys
sys.path.insert(0,'/tmp/claude-0/rodin/g1'); import seedpd
from scipy.spatial import cKDTree
C10='/tmp/claude-0/rodin/c10/'
Vu0=np.load(C10+'g13up.npz')['V'].astype(float); S_old=np.load(C10+'seeds13.npy'); R0=np.load(C10+'g13reg.npz')['R'].astype(float)
b0=np.load(C10+'g13_body.npz'); VB0=b0['V'].astype(float); FB0=b0['F'].astype(np.int64)
org=np.load('g14a_body.npz')['origin']; keep=np.load('g14b_body.npz')['KEEP']; VB=np.load('g14_body.npz')['V'].astype(float)
o=org[keep]; inv=-np.ones(len(VB0),np.int64); inv[o[o>=0]]=np.where(o>=0)[0]
sq,fi,cp=igl.point_mesh_squared_distance(Vu0[S_old],VB0,FB0); tri=FB0[fi]
bc=igl.barycentric_coordinates(cp,VB0[tri[:,0]],VB0[tri[:,1]],VB0[tri[:,2]]); nt=inv[tri]; ok=(nt>=0).all(1)
Pn=(VB[np.clip(nt,0,None)]*bc[:,:,None]).sum(1)
up=np.load('g14up.npz'); Vu=up['V'].astype(float); r1=np.load('g14reg.npz'); R1=r1['R'].astype(float); FAM1=r1['FAM']
d,j=cKDTree(Vu).query(Pn); ok&=(d<0.02)
rel=np.abs(R1[j]-R0[S_old])/R0[S_old]; changed_seed=rel>0.10; okc=ok&~changed_seed
S_map=np.unique(j[okc]); print('carried',len(S_map),'dropped (no triangle)',int((~ok).sum()),'dropped (scale order changed)',int((ok&changed_seed).sum()))
_,nn=cKDTree(Vu0).query(Vu); relv=np.abs(R1-R0[nn])/R0[nn]
dd,_=cKDTree(Vu0[S_old[~okc]]).query(Vu)
patch=(relv>0.08)|(dd<0.8); scaly=(FAM1!=6)&(FAM1!=7)
S_new=seedpd.poisson_seeds(Vu,R1,scaly&patch,np.random.default_rng(10),c=0.50,init=S_map[scaly[S_map]&~patch[S_map]])
np.save('seeds14.npy',S_new); print('fill region verts',int(patch.sum()),'final seeds',len(S_new))
