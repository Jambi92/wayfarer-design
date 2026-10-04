# post-Gate-8 polish: carry the Gate 7 closure scale seeds onto the corrected mesh so every scale outside the brow-surgery
# patch is the SAME scale (tail scales are carried with the taper deformation = re-projection); only the re-meshed brow
# patch is filled with new seeds (Poisson fill around the carried ones).
import numpy as np, igl, sys
sys.path.insert(0,'/tmp/claude-0/rodin/g1'); import seedpd
from scipy.spatial import cKDTree
G='/tmp/claude-0/rodin/g1/'
up0=np.load(G+'g7up.npz'); Vu0=up0['V'].astype(float); r0=np.load(G+'g7regc.npz'); R0=r0['R'].astype(float); F0fam=r0['FAM']
S_old=seedpd.poisson_seeds(Vu0,R0,(F0fam!=6)&(F0fam!=7),np.random.default_rng(7),c=0.50); print('old seeds',len(S_old))
b0=np.load(G+'g9_body.npz'); VB0=b0['V'].astype(float); FB0=b0['F'].astype(np.int64)
b11=np.load(G+'g11_body.npz'); org=b11['origin']; b12=np.load('g12_body.npz'); VB12=b12['V'].astype(float)
inv=-np.ones(len(VB0),np.int64); inv[org[org>=0]]=np.where(org>=0)[0]
sq,fi,cp=igl.point_mesh_squared_distance(Vu0[S_old],VB0,FB0); tri=FB0[fi]
bc=igl.barycentric_coordinates(cp,VB0[tri[:,0]],VB0[tri[:,1]],VB0[tri[:,2]])
nt=inv[tri]; ok=(nt>=0).all(1)
Pn=(VB12[np.clip(nt,0,None)]*bc[:,:,None]).sum(1)
up=np.load('g12up.npz'); Vu=up['V'].astype(float); r1=np.load('g12reg.npz'); R1=r1['R'].astype(float); FAM1=r1['FAM']
d,j=cKDTree(Vu).query(Pn); ok&=(d<0.02)
S_map=np.unique(j[ok]); print('carried',len(S_map),'dropped',int((~ok).sum()),'snap max %.4f'%d[ok].max())
scaly=(FAM1!=6)&(FAM1!=7)
dn,_=cKDTree(Vu0).query(Vu); x,f,u=Vu.T; tailz=(f<-26)&(u>40)&(u<120)
newsurf=(dn>1e-4)&~tailz                                      # vertices of the re-meshed brow patch (+ relaxed seam band)
dd,_=cKDTree(Vu[newsurf]).query(Vu); patch=dd<0.5             # dilate 5 mm
print('fill region verts',int(patch.sum()))
S_new=seedpd.poisson_seeds(Vu,R1,scaly&patch,np.random.default_rng(8),c=0.50,init=S_map[scaly[S_map]])
np.save('seeds12.npy',S_new); print('final seeds',len(S_new),'new (brow patch fill)',len(S_new)-int(scaly[S_map].sum()))
