# handlift.py -- IN.npz OUT.npz "m1,m2,..." [MF] [MAXUP] : move hand crotch midpoints up (+z) to the source web floor
# (first exit of a downward ray cast from inside the palm, z0 = m.z + 3 cm, at the midpoint's x,y)
import sys, numpy as np, bpy, mathutils
from mathutils.bvhtree import BVHTree
a=sys.argv[sys.argv.index('--')+1:]; z=np.load(a[0]); V=z['V'].astype(float).copy(); F=z['F']
ms=[int(t) for t in a[2].split(',')]; MF=float(a[3]) if len(a)>3 else 1.0; MU=float(a[4]) if len(a)>4 else 1.2
w=np.load('/home/claude/stc/rp1/weld.npz'); S=w['V'].astype(float); SF=w['F']
for m in ms:
    p=V[m]; sel=np.linalg.norm(S[SF].mean(1)-p,axis=1)<6
    bvh=BVHTree.FromPolygons(S.tolist(),SF[sel].tolist())
    o=mathutils.Vector((p[0],p[1],p[2]+3.0)); hits=[]; cur=o; d=mathutils.Vector((0,0,-1))
    for k in range(8):
        h=bvh.ray_cast(cur,d,10.0)
        if h[0] is None: break
        hits.append(h[0].z); cur=h[0]+d*1e-4
    # hits from top: entering/exiting; floor = lowest hit above p.z-0.2 that is <= p.z+MU
    DN=float(a[5]) if len(a)>5 else 0.2; cand=[hz for hz in hits if p[2]-DN<hz<=p[2]+MU]
    if not cand: print(m,'no floor',np.round(hits,2)); continue
    fz=max(cand) if len(cand)==1 else min(cand)
    nz=p[2]+MF*(fz-p[2]); print(m,'z',round(p[2],2),'hits',np.round(hits,2),'floor',round(fz,2),'->',round(nz,2)); V[m,2]=nz
np.savez_compressed(a[1],V=V,F=F)
