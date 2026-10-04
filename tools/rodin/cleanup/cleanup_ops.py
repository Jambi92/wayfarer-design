# Saurin final "grown, not assembled" cleanup: local meso-scale geometry operators on the anatomical base mesh.
# Each authorized zone gets a band filter along the surface normal:  d_new = low(d) + alpha * blur(d) - low(d)
#   d = normal offset from a heavily smoothed reference; blur broadens features (fillets creases, widens strips),
#   alpha < 1 lowers them. Macro shape (low band) is untouched. alpha can differ for convex (+) and concave (-) relief.
# Plus: Taubin de-noise of the head/neck splice band, and tangential relaxation (+ projection back onto the surface)
# of degenerate zip-seam triangles (ankle speck). argv: in.npz(V,F) out.npz [neckseam_dist.npy]
import numpy as np, igl, sys, json
from scipy.sparse import coo_matrix, diags
from scipy.sparse.csgraph import dijkstra
sys.path.insert(0,'/tmp/claude-0/rodin/c10'); from zones import zones, ss
z=np.load(sys.argv[1]); V=z['V'].astype(np.float64); F=z['F'].astype(np.int64); n=len(V); V0=V.copy()
N=igl.per_vertex_normals(V,F)
E=np.concatenate([F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]); A=coo_matrix((np.ones(len(E)),(E[:,0],E[:,1])),shape=(n,n)).tocsr(); A=((A+A.T)>0).astype(np.float32)
L=diags(1/np.asarray(A.sum(1)).ravel())@A
def blur(a,k):
    for _ in range(k): a=L@a
    return a
Ns=N.copy()
for _ in range(40): Ns=L@Ns
Ns/=np.linalg.norm(Ns,axis=1,keepdims=True)+1e-12          # smoothed normals: displacement direction free of crease jaggies
Vl=V.copy()
for _ in range(300): Vl=L@Vl
d=np.einsum('ij,ij->i',V-Vl,Ns)
Z=zones(V,N); x,f,u=V.T
# per-zone settings: (blur its for broadening, alpha convex, alpha concave)
P={'sternum':(90,0.35,0.50),'dorsal_rod':(200,None,0.30),'shoulder':(120,0.90,0.40),'upper_arm':(90,0.65,0.50),'inguinal_hip':(120,0.95,0.40),'heel':(150,0.40,0.45),'ankle_front':(200,0.20,0.15)}
lowd=blur(d,600); lowd_big=blur(lowd.copy(),1900)          # heel lump / rod are wider than the default band
delta=np.zeros(n); W=np.zeros(n)
for k,(nb,ap,an) in P.items():
    w=blur(Z[k].copy(),20)                                   # soft zone edge
    lo=lowd_big if k in ('heel','dorsal_rod','ankle_front') else lowd
    hp=d-lo; b=blur(hp,nb)
    if k=='dorsal_rod':                                     # taper: full rod at the nape, progressively lowered toward its end
        ap=np.clip((u-135.0)/70.0,0.10,0.35)
    a=np.where(b>=0,ap,an)
    dn=lo+a*b
    delta+=w*(dn-d); W=np.maximum(W,w)
V=V+Ns*delta[:,None]
wz=np.clip(W*1.5,0,1)
for _ in range(8): V=V+(0.5*wz)[:,None]*((L@V)-V); V=V+(-0.53*wz)[:,None]*((L@V)-V)   # clean residual crease jaggies inside zones only
mv_zone=np.abs(delta)
# head/neck splice band (Gate 6 head-patch seam on the neck): Taubin de-noise, shape-preserving
if len(sys.argv)>3:
    ds=np.load(sys.argv[3])
    wb=np.where(np.isfinite(ds),ss(5.0,2.0,np.nan_to_num(ds,nan=99)),0.0)*ss(178,174,u)*ss(148,152,u)
    for _ in range(40):
        V=V+(0.5*wb)[:,None]*((L@V)-V); V=V+(-0.53*wb)[:,None]*((L@V)-V)
else: wb=np.zeros(n)
wr=np.zeros(n)
mv=np.linalg.norm(V-V0,axis=1)
rec={'zone_weight':{k:Z[k].astype(np.float32) for k in Z}}
np.savez(sys.argv[2],V=V,F=F,MV=mv.astype(np.float32),WZ=W.astype(np.float32),WB=wb.astype(np.float32),WR=wr.astype(np.float32))
for k in Z: m=Z[k]>0.5; print('%-13s verts %6d  max move %.2f mm  p99 %.2f mm'%(k,m.sum(),mv[m].max()*10,np.percentile(mv[m],99)*10))
print('splice band verts',int((wb>0.5).sum()),'max %.2f mm'%(mv[wb>0.1].max()*10 if (wb>0.1).any() else 0),'; defect repair verts',int((wr>0).sum()),'max %.3f mm'%(mv[wr>0].max()*10 if (wr>0).any() else 0))
print('outside all op weights: max move %.4f mm'%(mv[(W<1e-6)&(wb<1e-6)&(wr<1e-6)].max()*10))
