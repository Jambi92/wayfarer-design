# finalize.py IN OUT : ground + uniform scale to 218 cm, flatten the donor's upper-anterior-thigh mound, light fair
import sys, numpy as np, igl, json
sys.path.insert(0,'/tmp/claude-0/src3d/tools'); sys.path.insert(0,'/tmp/claude-0/rp2/tools')
from region_fair import region_fair
d=np.load(sys.argv[1]); V=d['V'].copy(); F=d['Q'].astype(np.int64)
z0=V[:,2].min(); V[:,2]-=z0; s=218.0/V[:,2].max(); V*=s
ank=V[(V[:,2]>7)&(V[:,2]<10)]; V[:,1]+=0.4-ank[:,1].mean()
N=igl.per_vertex_normals(V,F); D=np.zeros_like(V)
for sg in (1,-1):
    q=(V-np.array([sg*11.5,13.0,103.0]))/np.array([5.5,4.0,7.5]); D+=(-2.6*np.exp(-0.5*(q*q).sum(1)))[:,None]*N
X=V+D; r=np.clip(np.linalg.norm(D,axis=1)/0.5,0,1); X=region_fair(X,np.c_[F,F[:,0]],r,8.0,it=2)
X[:,2]-=X[:,2].min(); X*=218.0/X[:,2].max()
np.savez(sys.argv[2],V=X,Q=F,thigh_mound_mask=r)
json.dump(dict(ground_shift_cm=float(-z0),uniform_scale=float(s)),open(sys.argv[2].replace('.npz','_finalize.json'),'w'))
print('final bbox',X.min(0).round(3),X.max(0).round(3))
