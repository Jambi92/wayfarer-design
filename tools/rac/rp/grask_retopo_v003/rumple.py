# rumple.py PROD.npz [thr_deg] : shading-artefact detector -- angle between the production smooth (vertex) normal and the
# v005 surface normal at the closest point; clusters above thr are listed (a rumpled / faceted patch shades wrongly even
# when its deviation is small).
import numpy as np, sys, igl, json
sys.path.insert(0,'/tmp/claude-0/rt'); from common import *; from subproj import vnormals
SV,SF=load_src(); SN=igl.per_vertex_normals(SV,SF)
z=np.load(sys.argv[1]); V=z['V']; Q=z['Q']; FP=z['FP']; thr=float(sys.argv[2]) if len(sys.argv)>2 else 8
N=vnormals(V,Q); d,fi,C=igl.point_mesh_squared_distance(V,SV,SF)
T=SF[fi]; a_=SV[T[:,0]]; b_=SV[T[:,1]]; c_=SV[T[:,2]]; v0=b_-a_; v1=c_-a_; v2=C-a_
d00=(v0*v0).sum(1); d01=(v0*v1).sum(1); d11=(v1*v1).sum(1); d20=(v2*v0).sum(1); d21=(v2*v1).sum(1); den=np.maximum(d00*d11-d01*d01,1e-18)
bv=(d11*d20-d01*d21)/den; bw=(d00*d21-d01*d20)/den; B=np.stack([1-bv-bw,bv,bw],1)
n_src=(SN[T]*B[:,:,None]).sum(1); n_src/=np.linalg.norm(n_src,axis=1)[:,None]
ang=np.degrees(np.arccos(np.clip((N*n_src).sum(1),-1,1)))
vp=np.zeros(len(V),int); vp[Q.ravel()]=np.repeat(FP,4)
print('vertex-normal deviation deg: median %.2f p95 %.2f p99 %.2f max %.2f'%(np.median(ang),np.percentile(ang,95),np.percentile(ang,99),ang.max()))
from scipy.sparse.csgraph import connected_components
sys.path.insert(0,'/tmp/claude-0/rt'); from subproj import neighbors
A=neighbors(Q,len(V)); m=ang>thr; idx=np.nonzero(m)[0]
if len(idx):
    nc,lab=connected_components(A[idx][:,idx]); out=[]
    for k in range(nc):
        g=idx[lab==k]; out.append(dict(n=int(len(g)),max_deg=round(float(ang[g].max()),1),part=PARTS[np.bincount(vp[g]).argmax()],centre=np.round(V[g].mean(0),2).tolist()))
    out.sort(key=lambda o:-o['max_deg']*o['n']**0.5)
    for o in out[:25]: print(o)
    json.dump(dict(stats=dict(median=float(np.median(ang)),p95=float(np.percentile(ang,95)),p99=float(np.percentile(ang,99)),max=float(ang.max())),thr=thr,clusters=out),open(sys.argv[1].replace('.npz','_rumple.json'),'w'),indent=1)
np.save(sys.argv[1].replace('.npz','_nang.npy'),ang)
