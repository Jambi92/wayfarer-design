# relax.py IN OUT cx,cf,cu R ITERS : local surface-constrained relaxation (tangential Laplacian + parallelogram, guarded
# re-projection onto v005 each iteration, smooth falloff to the patch rim) to remove irregular quad flow that shades as
# rumples; the shape stays the source surface.
import numpy as np, sys
sys.path.insert(0,'/tmp/claude-0/rt')
from subproj import Projector, vertex_part, neighbors, vnormals
z=np.load(sys.argv[1]); V=z['V'].copy(); Q=z['Q']; FP=z['FP']
c=np.array([float(v) for v in sys.argv[3].split(',')]); R=float(sys.argv[4]); IT=int(sys.argv[5])
PR=Projector(); vp,M=vertex_part(Q,FP,len(V)); band=np.asarray((M>0).sum(1)).ravel()>1
A=neighbors(Q,len(V)); deg=np.asarray(A.sum(1)).ravel()
r=np.linalg.norm(V-c,axis=1); idx=np.nonzero(r<R)[0]; w=np.clip((R-r[idx])/(0.35*R),0,1)
for it in range(IT):
    N=vnormals(V,Q); T=np.zeros_like(V); W=np.zeros(len(V))
    for k in range(4):
        t=V[Q[:,(k-1)%4]]+V[Q[:,(k+1)%4]]-V[Q[:,(k+2)%4]]; np.add.at(T,Q[:,k],t); np.add.at(W,Q[:,k],1)
    par=T[idx]/W[idx][:,None]; lap=(A[idx]@V)/deg[idx][:,None]
    dl=0.5*lap+0.5*par-V[idx]; dl-=(dl*N[idx]).sum(1)[:,None]*N[idx]
    X=V[idx]+0.4*w[:,None]*dl; V[idx]=PR.project(X,vp[idx],band[idx],N[idx])
np.savez(sys.argv[2],V=V,Q=Q,FP=FP); print('relaxed',len(idx),'verts')
