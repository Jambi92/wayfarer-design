# thick.py IN.npz OUT.npy : per-vertex inward thickness (distance along -normal to the next surface), cm
import sys, numpy as np, bpy
import bpy
from mathutils.bvhtree import BVHTree
from mathutils import Vector
d=np.load(sys.argv[1]); V=d['V'].astype(float); F=d['Q']
T=BVHTree.FromPolygons(V.tolist(),F.tolist(),all_triangles=True,epsilon=0.0)
fn=np.cross(V[F[:,1]]-V[F[:,0]],V[F[:,2]]-V[F[:,0]]); vn=np.zeros_like(V)
for k in range(3): np.add.at(vn,F[:,k],fn)
vn/=np.linalg.norm(vn,axis=1)[:,None]+1e-12
th=np.full(len(V),99.0)
for i in range(len(V)):
    o=Vector(V[i]-vn[i]*0.02); dr=Vector(-vn[i])
    hit=T.ray_cast(o,dr,30.0)
    if hit[0] is not None: th[i]=hit[3]+0.02
np.save(sys.argv[2],th); np.save(sys.argv[2].replace('.npy','_n.npy'),vn)
print('thin<1cm',(th<1).sum(),'thin<0.6',(th<0.6).sum())
