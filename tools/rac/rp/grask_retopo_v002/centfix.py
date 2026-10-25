# centfix.py IN OUT [thr_mm] : pull quads whose centroid floats off v005 (thin quads straddling a narrow crease) onto the
# surface: shift their corners toward the centroid's closest source point, guarded re-projection; revert per-vertex if the
# local quad quality collapses.
import numpy as np, sys, igl
sys.path.insert(0,'/tmp/claude-0/rt')
from subproj import Projector, vertex_part, vnormals
z=np.load(sys.argv[1]); V=z['V'].copy(); Q=z['Q']; FP=z['FP']; thr=float(sys.argv[3])/10 if len(sys.argv)>3 else 0.10
PR=Projector(); vp,M=vertex_part(Q,FP,len(V)); band=np.asarray((M>0).sum(1)).ravel()>1
def minang(X,F):
    out=np.full(len(F),180.0)
    for i in range(4):
        a=X[Q[F,(i-1)%4]]-X[Q[F,i]]; b=X[Q[F,(i+1)%4]]-X[Q[F,i]]
        ang=np.degrees(np.arccos(np.clip((a*b).sum(1)/np.maximum(np.linalg.norm(a,axis=1)*np.linalg.norm(b,axis=1),1e-12),-1,1)))
        out=np.minimum(out,np.minimum(ang,180-ang))
    return out
for it in range(6):
    C=V[Q].mean(1); d,fi,P=igl.point_mesh_squared_distance(C,PR.SV,PR.SF); d=np.sqrt(d)
    bad=np.nonzero(d>thr)[0]; print('iter',it,'off-surface centroids',len(bad),'max mm %.2f'%(d.max()*10),flush=True)
    if not len(bad): break
    acc=np.zeros_like(V); w=np.zeros(len(V))
    for f in bad:
        for v in Q[f]: acc[v]+=0.6*(P[f]-C[f]); w[v]+=1
    mv=np.nonzero(w>0)[0]; Vn=V.copy(); Vn[mv]+=acc[mv]/w[mv][:,None]
    N=vnormals(Vn,Q); Vn[mv]=PR.project(Vn[mv],vp[mv],band[mv],N[mv])
    near=np.nonzero(np.isin(Q,mv).any(1))[0]
    a0=minang(V,near); a1=minang(Vn,near)
    worse=near[(a1<np.minimum(a0,12.0))]
    rv=np.unique(Q[worse].ravel()); Vn[rv]=V[rv]; V=Vn
np.savez(sys.argv[2],V=V,Q=Q,FP=FP)
