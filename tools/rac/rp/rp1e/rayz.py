import sys, numpy as np, bpy, mathutils
from mathutils.bvhtree import BVHTree
a=sys.argv[sys.argv.index('--')+1:]
w=np.load('/home/claude/stc/rp1/weld.npz'); S=w['V'].astype(float); SF=w['F']; bvh=BVHTree.FromPolygons(S.tolist(),SF.tolist())
x,y=float(a[0]),float(a[1])
cur=mathutils.Vector((x,y,-2.0)); d=mathutils.Vector((0,0,1))
for k in range(6):
    h=bvh.ray_cast(cur,d,30)
    if h[0] is None: break
    print(round(h[0][2],2),round(h[1][2],2)); cur=h[0]+d*0.002
