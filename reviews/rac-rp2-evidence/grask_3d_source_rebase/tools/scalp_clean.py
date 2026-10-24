# scalp_clean.py IN OUT : remove fine generator pits on the cranium / behind the ears; light fine-noise reduction on the ear (face untouched)
import sys, numpy as np, igl
from scipy.sparse.linalg import factorized
sys.path.insert(0,'/tmp/claude-0/src3d/tools'); sys.path.insert(0,'/tmp/claude-0/rp2/tools')
from lowpass import lowpass
from cotfair import ss
d=np.load(sys.argv[1]); X=d['V'].astype(float); F=d['Q'].astype(np.int64); n=len(X)
L=igl.cotmatrix(X,F); M=igl.massmatrix(X,F,igl.MASSMATRIX_TYPE_BARYCENTRIC)
s=factorized((M-0.5*L).tocsc()); B=M@X; S=X-np.stack([s(B[:,j]) for j in range(3)],1); bp=S-lowpass(np.c_[F,F[:,0]],n,S,100.0)
x,f,z=X.T; ax=np.abs(x)
head=ss((z-197)/3)
face=ss((f-4.0)/2.0)*(1-ss((ax-7.0)/2.0))            # front of the face: untouched
ear=ss((ax-7.0)/1.2)*ss((z-195)/2)*(1-ss((z-214)/2))*(1-ss((np.abs(f-1.5)-6)/2))
scalp=np.clip(head*(1-face)-ear,0,1)
r=0.85*scalp+0.4*ear
Y=X-r[:,None]*bp
extra=d['thigh_mound_mask'] if 'thigh_mound_mask' in d.files else None
np.savez(sys.argv[2],V=Y,Q=F,**({'thigh_mound_mask':extra} if extra is not None else {}),scalp_clean_weight=r)
print('scalp clean max move mm %.2f'%(np.linalg.norm(Y-X,axis=1).max()*10))
