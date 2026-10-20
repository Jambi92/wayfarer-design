# pick.py -- views.json picks.json out.json : ray-cast pixel picks (1000px renders) onto the v014 production; returns hit point + normal (blender cm)
import bpy, numpy as np, sys, json, mathutils
from mathutils.bvhtree import BVHTree
a=sys.argv[sys.argv.index('--')+1:]; views={v['n']:v for v in json.load(open(a[0]))}; picks=json.load(open(a[1]))
z=np.load('/home/claude/wayfarer-design/reviews/rac-rp1e-evidence/designs/design_v014_production_L4.npz'); V=z['V']*np.array([1,-1,1]); F=z['F']
out={}
cache={}
for name,(vn,px,py) in picks.items():
    v=views[vn]; t=mathutils.Vector(v['t']); d=mathutils.Vector(v['d']).normalized(); rot=(-d).to_track_quat('-Z','Y').to_matrix()
    right=rot.col[0]; up=rot.col[1]; s=v['s']
    if vn not in cache:
        c=np.array(t); m=np.linalg.norm(V[F].mean(1)-c,axis=1)<s; cache[vn]=BVHTree.FromPolygons(V.tolist(),F[m].tolist())
    o=t+d*400+right*((px/1000-0.5)*s)+up*((0.5-py/1000)*s)
    h=cache[vn].ray_cast(o,-d,1000)
    out[name]=None if h[0] is None else dict(p=[round(x,4) for x in h[0]],n=[round(x,4) for x in h[1]])
    print(name,out[name])
json.dump(out,open(a[2],'w'),indent=1)
