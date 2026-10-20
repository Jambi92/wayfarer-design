# blender-python srcgapf.py -- cx,cy,cz R OUT.npy : outward-ray air gap (cm) at source face centroids (blender frame) in a ball
import sys, numpy as np, bpy, mathutils
from mathutils.bvhtree import BVHTree
a=sys.argv[sys.argv.index('--')+1:]; c=np.array([float(x) for x in a[0].split(',')]); R=float(a[1]); out=a[2]
w=np.load('/home/claude/stc/rp1/weld.npz'); S=w['V'].astype(float); SF=w['F'].astype(np.int64)
C=S[SF].mean(1); fm=np.linalg.norm(C-c,axis=1)<R+1.0
fn=np.cross(S[SF[:,1]]-S[SF[:,0]],S[SF[:,2]]-S[SF[:,0]]); fn/=np.linalg.norm(fn,axis=1,keepdims=True)+1e-15
bvh=BVHTree.FromPolygons(S.tolist(),SF[fm].tolist())
idx=np.where(np.linalg.norm(C-c,axis=1)<R)[0]; g=np.full(len(idx),9.0)
for k,i in enumerate(idx):
    o=mathutils.Vector((C[i]+fn[i]*0.001).tolist()); h=bvh.ray_cast(o,mathutils.Vector(fn[i].tolist()),3.0)
    if h[0] is not None: g[k]=h[3]+0.001
np.save(out,np.c_[idx,g]); print('n',len(idx),'gap<0.06',(g<0.06).sum())
