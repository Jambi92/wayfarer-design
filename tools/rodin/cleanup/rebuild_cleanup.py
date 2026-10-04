# Rebuild the full-resolution final-cleanup surface (Gate 7 closure surface on the polished anatomy).
# Usage: python rebuild_cleanup.py saurin_cleanup_base.npz saurin_cleanup_surface_delta.npz out.npz [out.obj]
# Needs numpy + libigl (pip install libigl). Units cm; frame x right, f forward, u up.
import sys, numpy as np, igl
b=np.load(sys.argv[1]); V,F=igl.upsample(b['v'].astype(np.float64),b['f'].astype(np.int64))
V=V+np.load(sys.argv[2])['d'].astype(np.float64)
np.savez_compressed(sys.argv[3],v=V.astype(np.float32),f=F.astype(np.int32))
if len(sys.argv)>4:
    with open(sys.argv[4],'w') as o:
        o.write(''.join('v %.5f %.5f %.5f\n'%tuple(p) for p in V)); o.write(''.join('f %d %d %d\n'%tuple(t+1) for t in F))
print('cleanup surface:',len(V),'verts',len(F),'tris; height %.2f cm'%np.ptp(V[:,2]))
