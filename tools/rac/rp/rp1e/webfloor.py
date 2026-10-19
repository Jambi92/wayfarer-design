# blender-python webfloor.py -- cage.npz a b [z0] [ext] : web-floor profile under the cage edge a-b (rays straight down from z0)
import sys, numpy as np, bpy, mathutils
from mathutils.bvhtree import BVHTree
a_=sys.argv[sys.argv.index('--')+1:]; z=np.load(a_[0]); V=z['V']; a,b=int(a_[1]),int(a_[2])
z0=float(a_[3]) if len(a_)>3 else None; ext=float(a_[4]) if len(a_)>4 else 0.5
w=np.load('/home/claude/stc/rp1/weld.npz'); S=w['V'].astype(float); SF=w['F']
P,Q=V[a],V[b]; c=0.5*(P+Q); m=(np.linalg.norm(S[SF].mean(1)-c,axis=1)<8)
bvh=BVHTree.FromPolygons(S.tolist(),SF[m].tolist())
if z0 is None: z0=max(P[2],Q[2])+2.0
out=[]
for t in np.linspace(-ext,1+ext,15):
    p=P+t*(Q-P); o=mathutils.Vector((p[0],p[1],z0)); hits=[]; d=mathutils.Vector((0,0,-1)); cur=o
    for k in range(6):
        h=bvh.ray_cast(cur,d,20.0)
        if h[0] is None: break
        hits.append((round(h[0][2],2), round(h[1][2],2))); cur=h[0]+d*0.002
    out.append((round(t,2),p[:2].round(2).tolist(),hits[:4]))
for r in out: print(r)
