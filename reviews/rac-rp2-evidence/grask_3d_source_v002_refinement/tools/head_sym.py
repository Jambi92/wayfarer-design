# head_sym.py IN OUT : full bilateral averaging of the cranium/face (ears excluded; they are already a mirrored pair), 2 iterations
import sys, numpy as np, igl
sys.path.insert(0,'/tmp/claude-0/src3d/tools'); sys.path.insert(0,'/tmp/claude-0/rp2/tools')
from lowpass import lowpass
from cotfair import ss
d=np.load(sys.argv[1]); X=d['V'].astype(float); F=d['Q'].astype(np.int64); Q4=np.c_[F,F[:,0]]; n=len(X); X0=X.copy()
for it in range(3):
    x,f,z=X.T
    w=ss((z-186)/3)*(1-ss((np.abs(x)-7.9)/0.4))
    Xm=X*np.array([-1,1,1]); _,I,C=igl.point_mesh_squared_distance(X,Xm,F[:,[0,2,1]])
    N=igl.per_vertex_normals(X,F); Nm=igl.per_face_normals(Xm,F[:,[0,2,1]],np.array([0,0,1.0]))[I]
    ok=(np.einsum('ij,ij->i',N,Nm)>0.3)&(np.linalg.norm(C-X,axis=1)<2.0)
    D=lowpass(Q4,n,(C-X)*ok[:,None],4.0,w=ok*1.0+0.02)
    X=X+0.5*w[:,None]*D
    print(it,'move p95 %.2f max %.2f mm'%(np.percentile(np.linalg.norm(0.5*w[:,None]*D,axis=1)[w>0.5],95)*10,np.linalg.norm(0.5*w[:,None]*D,axis=1).max()*10))
out={k:d[k] for k in d.files}; out['V']=X; out['head_sym_move_mm']=np.linalg.norm(X-X0,axis=1)*10
np.savez(sys.argv[2],**out)
