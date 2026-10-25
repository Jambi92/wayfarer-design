# foldfix.py IN OUT : remove folded faces (dihedral > 120 deg, or facing against the source normal): local Laplacian
# smoothing of the fold vertices (+ rings) with guarded re-projection, then a projection-free pass if still folded.
import numpy as np, sys, igl
sys.path.insert(0,'/tmp/claude-0/rt')
from subproj import Projector, vertex_part, neighbors, vnormals
from common import load_src
z=np.load(sys.argv[1]); V=z['V'].copy(); Q=z['Q']; FP=z['FP']
PR=Projector(); vp,M=vertex_part(Q,FP,len(V)); band=np.asarray((M>0).sum(1)).ravel()>1
A=neighbors(Q,len(V)); deg=np.asarray(A.sum(1)).ravel(); SV,SF=PR.SV,PR.SF
fn=np.cross(SV[SF[:,1]]-SV[SF[:,0]],SV[SF[:,2]]-SV[SF[:,0]]); fn/=np.maximum(np.linalg.norm(fn,axis=1),1e-12)[:,None]
E=np.concatenate([Q[:,[0,1]],Q[:,[1,2]],Q[:,[2,3]],Q[:,[3,0]]]); F=np.tile(np.arange(len(Q)),4)
Es=np.sort(E,1); o=np.lexsort((Es[:,1],Es[:,0])); F=F[o]; f0=F[0::2]; f1=F[1::2]
def folds(V):
    n=np.cross(V[Q[:,2]]-V[Q[:,0]],V[Q[:,3]]-V[Q[:,1]]); n/=np.maximum(np.linalg.norm(n,axis=1),1e-12)[:,None]
    bad=np.zeros(len(Q),bool); d=(n[f0]*n[f1]).sum(1); bad[f0[d<-0.5]]=True; bad[f1[d<-0.5]]=True
    _,fi,_=igl.point_mesh_squared_distance(V[Q].mean(1),SV,SF); bad|=(n*fn[fi]).sum(1)<0
    return bad
for r in range(30):
    b=folds(V); print('round',r,'folded faces',int(b.sum()),flush=True)
    if not b.any(): break
    reg=np.zeros(len(V),bool); reg[Q[b].ravel()]=True
    for _ in range(1+r//5): reg|=(A@reg.astype(float))>0
    idx=np.nonzero(reg)[0]
    for it in range(4):
        avg=(A@V)/deg[:,None]; V[idx]=0.5*V[idx]+0.5*avg[idx]
        if r<15: N=vnormals(V,Q); V[idx]=PR.project(V[idx],vp[idx],band[idx],N[idx])
np.savez(sys.argv[2],V=V,Q=Q,FP=FP); print('final folded',int(folds(V).sum()))
