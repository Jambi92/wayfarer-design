# Rebuild the full-resolution Saurin Gate 7 surface (4,477,610 verts / 8,955,216 tris) from the Gate 6 closed mesh.
# Usage: python rebuild_gate7.py saurin_gate6_closed.npz saurin_gate7_surface_delta.npz out.npz [out.obj]
# Needs: numpy, libigl (pip install libigl). Units: cm, canonical frame x (right), f (forward), u (up).
import sys, numpy as np, igl
g6=np.load(sys.argv[1]); V,F=igl.upsample(g6['v'].astype(np.float64),g6['f'].astype(np.int64))
V=V+np.load(sys.argv[2])['d'].astype(np.float64)
np.savez_compressed(sys.argv[3],v=V.astype(np.float32),f=F.astype(np.int32))
if len(sys.argv)>4:
    with open(sys.argv[4],'w') as o:
        o.write(''.join('v %.5f %.5f %.5f\n'%(x,f,u) for x,f,u in V)); o.write(''.join('f %d %d %d\n'%tuple(t+1) for t in F))
print('Gate 7 surface:',len(V),'verts',len(F),'tris; height %.2f cm'%np.ptp(V[:,2]))
