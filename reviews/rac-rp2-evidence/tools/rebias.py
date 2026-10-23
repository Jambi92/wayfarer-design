# rebias.py IN OUT lam [clip_mm] : remove the low-frequency signed offset (fairing shrink) against S*.
# Signed distance to S* per vertex -> screened Laplacian low-pass -> move along vertex normal by -smooth(d).
# Vertices whose nearest S* face is a resolution-zone face (crotch slot / axillae) or whose |d| > clip get weight 0 in the data
# term (their offset is intentional), so the field there is interpolated from the surroundings.
import sys, numpy as np, igl, scipy.sparse as sp
from scipy.sparse.linalg import factorized
R='/tmp/claude-0/rp2/'
P=np.load(sys.argv[1]); V=P['V'].astype(float); Q=P['Q']; lam=float(sys.argv[3]); clip=float(sys.argv[4])/10 if len(sys.argv)>4 else 0.08
S=np.load(R+'sstar.npz'); SV=S['V'].astype(float); SQ=S['Q']; ST=np.r_[SQ[:,[0,1,2]],SQ[:,[0,2,3]]]
ex=np.load(R+'excl_quads.npy'); exT=np.zeros(len(ST),bool); nq=len(SQ); ex=np.nonzero(ex)[0] if ex.dtype==bool else ex; exT[ex]=True; exT[ex+nq]=True
T=np.r_[Q[:,[0,1,2]],Q[:,[0,2,3]]]
d2,fi,cp=igl.point_mesh_squared_distance(V,SV,ST); FN=-igl.per_face_normals(SV,ST,np.array([0.,0,1]))
d=np.sqrt(d2)*np.sign(((V-cp)*FN[fi]).sum(1))   # + = physically outside S*
w=np.where(exT[fi]|(np.abs(d)>clip),0.0,1.0)
n=len(V); e=np.r_[Q[:,[0,1]],Q[:,[1,2]],Q[:,[2,3]],Q[:,[3,0]]]
A=sp.coo_matrix((np.ones(len(e)*2),(np.r_[e[:,0],e[:,1]],np.r_[e[:,1],e[:,0]])),(n,n)).tocsr(); A.data[:]=1
L=sp.diags(np.asarray(A.sum(1)).ravel())-A
M=(sp.diags(w+1e-6)+lam*L).tocsc(); sm=factorized(M)(w*d)
N=-igl.per_vertex_normals(V,T)   # physical outward
V2=V-sm[:,None]*N
print('signed d (mm): median %.3f mean %.3f | smooth field median %.3f p5 %.3f p95 %.3f'%(np.median(d[w>0])*10,d[w>0].mean()*10,np.median(sm)*10,np.percentile(sm,5)*10,np.percentile(sm,95)*10))
np.savez(sys.argv[2],**{k:P[k] for k in P.files if k!='V'},V=V2)
