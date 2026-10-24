# symmetrize.py IN OUT : mirror-average symmetrization (closest-point on the reflected surface), hands excluded, displacement low-passed
import sys, numpy as np, igl
sys.path.insert(0,'/tmp/claude-0/src3d/tools'); sys.path.insert(0,'/tmp/claude-0/rp2/tools')
from lowpass import lowpass
from cotfair import ss
d=np.load(sys.argv[1]); X=d['V'].astype(float); F=d['Q'].astype(np.int64)
Q4=np.c_[F,F[:,0]]
# hands: below the wrist, lateral (|x|>22, z<112)
hand=ss((np.abs(X[:,0])-21.0)/2.0)*ss((112-X[:,2])/4.0)
w=1-hand
for it in range(4):
    M=X*np.array([-1,1,1]); MF=F[:,[0,2,1]]
    d2,fi,cp=igl.point_mesh_squared_distance(X,M,MF)
    D=(cp-X)*0.5; dist=np.sqrt(d2)
    D[dist>4.0]=0       # no correspondence -> no move
    D=lowpass(Q4,len(X),D,8.0)
    X=X+D*w[:,None]
    print('iter',it,'mean move %.3f max %.3f cm'%(np.linalg.norm(D*w[:,None],axis=1).mean(),np.linalg.norm(D*w[:,None],axis=1).max()))
np.savez(sys.argv[2],V=X,Q=F)
