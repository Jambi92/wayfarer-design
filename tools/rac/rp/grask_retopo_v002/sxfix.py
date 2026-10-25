# sxfix.py IN.npz OUT.npz [ROUNDS] : (bpy python) resolve self-intersections introduced by projection: intersecting faces
# + neighbour rings get full Laplacian smoothing and guarded re-projection, repeated until the BVH overlap test is clean.
import sys, numpy as np
sys.path.insert(0,'/tmp/claude-0/rt')
import bpy
from mathutils.bvhtree import BVHTree
from subproj import Projector, vertex_part, neighbors, vnormals
a=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:]
z=np.load(a[0]); V=z['V'].copy(); Q=z['Q']; FP=z['FP']; R=int(a[2]) if len(a)>2 else 12
PR=Projector(); vp,M=vertex_part(Q,FP,len(V)); band=np.asarray((M>0).sum(1)).ravel()>1
A=neighbors(Q,len(V)); deg=np.asarray(A.sum(1)).ravel()
def pairs(V):
    t=BVHTree.FromPolygons(V.tolist(),Q.tolist(),all_triangles=False,epsilon=0.0)
    pr=np.array(t.overlap(t),int).reshape(-1,2); pr=pr[pr[:,0]<pr[:,1]]
    if len(pr): Aq=Q[pr[:,0]];Bq=Q[pr[:,1]]; pr=pr[~(Aq[:,:,None]==Bq[:,None,:]).any((1,2))]
    return pr
grow=2; hist=[1e9,1e9]
for r in range(R):
    pr=pairs(V); print('round',r,'pairs',len(pr),flush=True)
    if len(pr)==0: break
    reg=np.zeros(len(V),bool); reg[Q[pr.ravel()].ravel()]=True
    for _ in range(grow): reg|=(A@reg.astype(float))>0
    idx=np.nonzero(reg)[0]
    stuck=r>=2 and len(pr)>=hist[-2]*0.9
    for it in range(6):
        avg=(A@V)/deg[:,None]; V[idx]=0.4*V[idx]+0.6*avg[idx]
        N=vnormals(V,Q); Pp=PR.project(V[idx],vp[idx],band[idx],N[idx])
        V[idx]=Pp if not stuck else 0.5*(V[idx]+Pp)      # stuck: relax toward a fair surface before re-snapping
    if stuck:
        N=vnormals(V,Q); V[idx]=PR.project(V[idx],vp[idx],band[idx],N[idx])
    hist.append(len(pr)); grow=min(grow+1,8)
np.savez(a[1],V=V,Q=Q,FP=FP); print('final pairs',len(pairs(V)))
