# defold.py IN OUT [maxit] : locally fair folded/creased micro-triangles (dihedral > ~73 deg) on hands/feet until none remain
import sys, numpy as np, igl
sys.path.insert(0,'/tmp/claude-0/src3d/tools'); sys.path.insert(0,'/tmp/claude-0/rp2/tools')
from region_fair import region_fair
d=np.load(sys.argv[1]); X=d['V'].astype(float); F=d['Q'].astype(np.int64); n=len(X); Q4=np.c_[F,F[:,0]]
TT,_=igl.triangle_triangle_adjacency(F); e=np.r_[F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]
tot=np.zeros(n); thr_=float(sys.argv[4]) if len(sys.argv)>4 else 0.3
for it in range(int(sys.argv[3]) if len(sys.argv)>3 else 8):
    FN=igl.per_face_normals(X,F,np.array([0,0,1.0])); c=X[F].mean(1); ax=np.abs(c[:,0])
    ext=((ax>20)&(c[:,2]<112)&(c[:,2]>60))|(c[:,2]<15)
    sharp=(np.einsum('ij,ikj->ik',FN,FN[TT])<thr_).any(1)&ext
    print('iter',it,'sharp',sharp.sum())
    if sharp.sum()==0: break
    r=np.zeros(n); r[F[sharp].ravel()]=1
    for _ in range(3):
        s=np.zeros(n); np.maximum.at(s,e[:,0],r[e[:,1]]); r=np.maximum(r,0.7*s)
    X=region_fair(X,Q4,r,2.0,it=2); tot=np.maximum(tot,r)
out={k:d[k] for k in d.files}; out['V']=X; out['defold_weight']=tot
np.savez(sys.argv[2],**out)
