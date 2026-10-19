# blender-python devopen.py -- TAG [OUT.npz] : openness (fraction of 26 rays from p+0.02n escaping 3 cm) of every over-limit source point
import sys, numpy as np, bpy, mathutils
from mathutils.bvhtree import BVHTree
a=sys.argv[sys.argv.index('--')+1:]; tag=a[0]; out=a[1] if len(a)>1 else 'devopen_%s.npz'%tag
w=np.load('/home/claude/stc/rp1/weld.npz'); S=w['V'].astype(float); SF=w['F'].astype(np.int64)
zz=np.load('/home/claude/stc/rp1/zones.npz'); zone=zz['zone']; names=list(zz['names'])
d=np.load('sim_%s_L4_dsp.npy'%tag)
lim=np.array([3.0 if n=='general' else 1.5 for n in names])[zone]
idx=np.where(d>lim)[0]
fn=np.cross(S[SF[:,1]]-S[SF[:,0]],S[SF[:,2]]-S[SF[:,0]]); vn=np.zeros_like(S)
for k in range(3): np.add.at(vn,SF[:,k],fn)
vn/=np.linalg.norm(vn,axis=1,keepdims=True)+1e-12
bvh=BVHTree.FromPolygons(S.tolist(),SF.tolist())
dirs=np.array([[x,y,q] for x in (-1,0,1) for y in (-1,0,1) for q in (-1,0,1) if (x,y,q)!=(0,0,0)],float); dirs/=np.linalg.norm(dirs,axis=1,keepdims=True)
op=np.zeros(len(idx))
for t,i in enumerate(idx):
    o=mathutils.Vector((S[i]+vn[i]*0.02).tolist()); n=0; m=0
    for dv in dirs:
        if dv@vn[i]<=0: continue
        m+=1; h=bvh.ray_cast(o,mathutils.Vector(dv.tolist()),3.0)
        if h[0] is None: n+=1
    op[t]=n/max(m,1)
np.savez_compressed(out,idx=idx,op=op,d=d[idx],zone=zone[idx])
for k,nm in enumerate(names):
    m=zone[idx]==k
    if m.sum()==0: continue
    o=op[m]; print('%-18s over %6d  sealed(op=0) %5.1f%%  low(<0.15) %5.1f%%  exposed(>=0.5) %5.1f%%'%(nm,m.sum(),(o==0).mean()*100,(o<0.15).mean()*100,(o>=0.5).mean()*100))
