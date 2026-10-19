# blender-python hmap.py -- side y0 y1 z0 z1 step out.png : lateral height map (first hit of rays cast toward the midline)
import bpy, numpy as np, sys, mathutils
from mathutils.bvhtree import BVHTree
a=sys.argv[sys.argv.index('--')+1:]; side=a[0]; y0,y1,z0,z1,st=map(float,a[1:6]); out=a[6]
w=np.load('/home/claude/stc/rp1/weld.npz'); S=w['V'].astype(float); SF=w['F']
C=S[SF].mean(1); m=(C[:,1]>y0-2)&(C[:,1]<y1+2)&(C[:,2]>z0-2)&(C[:,2]<z1+2)&((C[:,0]>5) if side=='L' else (C[:,0]<-1))
bvh=BVHTree.FromPolygons(S.tolist(),SF[m].tolist())
ys=np.arange(y0,y1,st); zs=np.arange(z0,z1,st); H=np.full((len(zs),len(ys)),np.nan)
x0=25.0 if side=='L' else -21.0; d=mathutils.Vector((-1,0,0) if side=='L' else (1,0,0))
for i,z in enumerate(zs):
    for j,y in enumerate(ys):
        h=bvh.ray_cast(mathutils.Vector((x0,y,z)),d,30.0)
        if h[0] is not None: H[i,j]=h[0][0]
np.savez(out.replace('.png','.npz'),H=H,ys=ys,zs=zs)
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
plt.figure(figsize=(9,8)); plt.imshow(H if side=='L' else -H,origin='lower',extent=[y0,y1,z0,z1],cmap='viridis'); plt.colorbar()
plt.contour(ys,zs,H,levels=30,colors='k',linewidths=0.4); plt.savefig(out,dpi=90)
