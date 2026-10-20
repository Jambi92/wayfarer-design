# blender-python srcgapr.py -- cx,cy,cz R OUT.npy : outward-ray air gap of source vertices (blender frame) in a ball
import sys, numpy as np, bpy, mathutils
from mathutils.bvhtree import BVHTree
a=sys.argv[sys.argv.index('--')+1:]; c=np.array([float(x) for x in a[0].split(',')]); R=float(a[1]); out=a[2]
w=np.load('/home/claude/stc/rp1/weld.npz'); S=w['V'].astype(float); SF=w['F'].astype(np.int64)
fm=np.linalg.norm(S[SF].mean(1)-c,axis=1)<R+1.0; SFl=SF[fm]
fn=np.cross(S[SF[:,1]]-S[SF[:,0]],S[SF[:,2]]-S[SF[:,0]]); vn=np.zeros_like(S)
for k in range(3): np.add.at(vn,SF[:,k],fn)
vn/=np.linalg.norm(vn,axis=1,keepdims=True)+1e-12
vol=np.einsum('ij,ij->i',S[SF[:,0]],np.cross(S[SF[:,1]],S[SF[:,2]])).sum(); sg=1 if vol>0 else -1; vn*=sg
bvh=BVHTree.FromPolygons(S.tolist(),SFl.tolist())
idx=np.where(np.linalg.norm(S-c,axis=1)<R)[0]; g=np.full(len(idx),9.0)
for k,i in enumerate(idx):
    o=mathutils.Vector((S[i]+vn[i]*0.002).tolist()); h=bvh.ray_cast(o,mathutils.Vector(vn[i].tolist()),3.0)
    if h[0] is not None: g[k]=h[3]+0.002
np.save(out,np.c_[idx,g]); print('signed vol sign',sg,'n',len(idx),'gap<0.03:',(g<0.03).sum(),'gap<0.01:',(g<0.01).sum())
