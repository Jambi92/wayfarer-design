# sxfinal.py IN OUT : last-resort micro-fold cleanup -- vertices of still-intersecting faces (+1 ring) are Laplacian-smoothed
# without re-projection (sub-millimetre moves in sharp web cusps) until the BVH overlap test is clean.
import sys, numpy as np
sys.path.insert(0,'/tmp/claude-0/rt')
import bpy
from mathutils.bvhtree import BVHTree
from subproj import neighbors
a=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:]
z=np.load(a[0]); V=z['V'].copy(); V0=V.copy(); Q=z['Q']; FP=z['FP']
A=neighbors(Q,len(V)); deg=np.asarray(A.sum(1)).ravel()
def pairs(V):
    t=BVHTree.FromPolygons(V.tolist(),Q.tolist(),all_triangles=False,epsilon=0.0)
    pr=np.array(t.overlap(t),int).reshape(-1,2); pr=pr[pr[:,0]<pr[:,1]]
    if len(pr): Aq=Q[pr[:,0]];Bq=Q[pr[:,1]]; pr=pr[~(Aq[:,:,None]==Bq[:,None,:]).any((1,2))]
    return pr
for r in range(40):
    pr=pairs(V); print('round',r,'pairs',len(pr),flush=True)
    if len(pr)==0: break
    reg=np.zeros(len(V),bool); reg[Q[pr.ravel()].ravel()]=True
    for _ in range(1+r//10): reg|=(A@reg.astype(float))>0
    idx=np.nonzero(reg)[0]
    for it in range(3):
        avg=(A@V)/deg[:,None]; V[idx]=0.5*V[idx]+0.5*avg[idx]
mv=np.linalg.norm(V-V0,axis=1)*10
print('final pairs',len(pairs(V)),'moved verts',int((mv>1e-6).sum()),'max move mm',round(float(mv.max()),3))
np.savez(a[1],V=V,Q=Q,FP=FP)
