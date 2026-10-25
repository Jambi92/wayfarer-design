# fixfold.py IN.npz OUT.npz : find folded / off-surface retopo faces (centre off the source, or facing against the source
# normal), take them plus a few neighbour rings, and untangle with full Laplacian smoothing + guarded nearest projection.
import numpy as np, sys, igl
sys.path.insert(0,'/tmp/claude-0/rt')
from subproj import Projector, vertex_part, neighbors, vnormals
from common import *
inp,out=sys.argv[1],sys.argv[2]; thr=float(sys.argv[3]) if len(sys.argv)>3 else 0.06; R=int(sys.argv[4]) if len(sys.argv)>4 else 3
z=np.load(inp); V=z['V'].copy(); Q=z['Q']; FP=z['FP']
PR=Projector(); SV,SF=PR.SV,PR.SF
fn=np.cross(SV[SF[:,1]]-SV[SF[:,0]],SV[SF[:,2]]-SV[SF[:,0]]); fn/=np.maximum(np.linalg.norm(fn,axis=1),1e-12)[:,None]
vp,M=vertex_part(Q,FP,len(V)); band=np.asarray((M>0).sum(1)).ravel()>1
A=neighbors(Q,len(V)); deg=np.asarray(A.sum(1)).ravel()
def bad(V):
    c=V[Q].mean(1); d,fi,_=igl.point_mesh_squared_distance(c,SV,SF)
    n=np.cross(V[Q[:,2]]-V[Q[:,0]],V[Q[:,3]]-V[Q[:,1]]); n/=np.maximum(np.linalg.norm(n,axis=1),1e-12)[:,None]
    return (np.sqrt(d)>thr)|((n*fn[fi]).sum(1)<0.0)
for rnd in range(6):
    b=bad(V); print('round',rnd,'bad faces',b.sum())
    if not b.any(): break
    reg=np.zeros(len(V),bool); reg[Q[b].ravel()]=True
    for _ in range(R): reg|=(A@reg.astype(float))>0
    idx=np.nonzero(reg)[0]
    for it in range(8):
        avg=(A@V)/deg[:,None]; V[idx]=0.5*V[idx]+0.5*avg[idx]
        V[idx]=PR.project(V[idx],vp[idx],band[idx],vnormals(V,Q)[idx])
    R+=1
np.savez(out,V=V,Q=Q,FP=FP)
