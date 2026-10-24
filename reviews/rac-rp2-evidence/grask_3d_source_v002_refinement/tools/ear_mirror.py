# ear_mirror.py IN OUT : shrinkwrap the left (x>0) ear onto the mirrored right ear (the anatomically complete one), with tangential relaxation
import sys, numpy as np, igl, scipy.sparse as sp
sys.path.insert(0,'/tmp/claude-0/src3d/tools'); sys.path.insert(0,'/tmp/claude-0/rp2/tools')
from lowpass import lowpass
from cotfair import ss
d=np.load(sys.argv[1]); X=d['V'].astype(float).copy(); F=d['Q'].astype(np.int64); n=len(X); Q4=np.c_[F,F[:,0]]
x,f,z=X.T
core=((x>8.8)&(z>190)&(z<214)&(f>-10)&(f<4)).astype(float)
e0=np.r_[F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]; w=core.copy(); ring=core.copy()
for r in range(1,10):
    s_=np.zeros(n); np.maximum.at(s_,e0[:,0],ring[e0[:,1]]); np.maximum.at(s_,e0[:,1],ring[e0[:,0]]); ring=np.maximum(ring,s_)
    w=np.maximum(w,ring*(1-r/10.0))
w=lowpass(Q4,n,w[:,None],1.0)[:,0]
T=X*np.array([-1,1,1]); TF=F[:,[0,2,1]]
# restrict target to the right-ear region only
xt,ft,zt=T.T; keepf=(xt[F].min(1)>4.0)&(zt[F].min(1)>186)&(ft[F].max(1)<8)
TF=TF[keepf]
e=np.r_[F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]
A=sp.coo_matrix((np.ones(len(e)*2),(np.r_[e[:,0],e[:,1]],np.r_[e[:,1],e[:,0]])),(n,n)).tocsr(); A.data[:]=1; deg=np.asarray(A.sum(1)).ravel()
X0=X.copy()
for it in range(12):
    N=igl.per_vertex_normals(X,F)
    _,I,C=igl.point_mesh_squared_distance(X,T,TF)
    Nt=igl.per_face_normals(T,TF,np.array([0,0,1.0]))[I]
    ok=(np.einsum('ij,ij->i',N,Nt)>0.3)&(w>0.01)
    D=lowpass(Q4,n,(C-X)*ok[:,None],1.0,w=ok*1.0+0.05)
    X=X+w[:,None]*D
    N=igl.per_vertex_normals(X,F); U=A@X/deg[:,None]-X; U-=np.einsum('ij,ij->i',U,N)[:,None]*N
    X=X+0.5*w[:,None]*U
    print(it,'ok %.2f mean |D| %.3f'%(ok[w>0.5].mean(),np.linalg.norm(D[w>0.5],axis=1).mean()))
out={k:d[k] for k in d.files}; out['V']=X; out['ear_mirror_move_mm']=np.linalg.norm(X-X0,axis=1)*10
np.savez(sys.argv[2],**out); print('max move mm',out['ear_mirror_move_mm'].max())
