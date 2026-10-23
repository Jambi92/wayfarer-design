# shading_geo.py : geometric shading-band audit. Shading normals (vertex-normal interpolation = what a renderer uses) sampled on a
# fixed point set in the chest/abdomen band (production vertices, trunk, 118<=z<=152, |x|<=14 cm), each point and its mirror image.
# lr_normal_asym = angle between n(p) and the mirrored n(mirror p); roughness = angle between n(p) and the 3-cm low-passed normal.
import numpy as np, igl, json
R='/tmp/claude-0/rp2/'
P=np.load(R+'cand_v001.npz'); Wb=np.load(R+'weights_body.npz')
X=P['V'].astype(float); sel=(X[:,2]>=118)&(X[:,2]<=152)&(np.abs(X[:,0])<=14)&(np.abs(X[:,0])>=0.5)
X=X[sel][::3]; Xm=X*np.array([-1,1,1])
def shade(V,Q,pts):
    T=np.r_[Q[:,[0,1,2]],Q[:,[0,2,3]]]; N=igl.per_vertex_normals(V,T)
    _,fi,cp=igl.point_mesh_squared_distance(pts,V,T); B=igl.barycentric_coordinates(cp,V[T[fi,0]],V[T[fi,1]],V[T[fi,2]])
    n=(B[:,:,None]*N[T[fi]]).sum(1); return n/np.linalg.norm(n,axis=1)[:,None], np.sqrt(_)
from scipy.spatial import cKDTree
out={}
for nm,f in (('E3','e3_body.npz'),('S_star','sstar.npz'),('production_v001','cand_v001.npz')):
    D=np.load(R+f); n,d=shade(D['V'].astype(float),D['Q'],X); nm_,dm=shade(D['V'].astype(float),D['Q'],Xm)
    nmir=nm_*np.array([-1,1,1]); lr=np.degrees(np.arccos(np.clip((n*nmir).sum(1),-1,1)))
    t=cKDTree(X); nb=t.query_ball_point(X,3.0); ns=np.array([n[i].mean(0) for i in nb]); ns/=np.linalg.norm(ns,axis=1)[:,None]
    rough=np.degrees(np.arccos(np.clip((n*ns).sum(1),-1,1)))
    out[nm]=dict(lr_normal_asym_deg=dict(p50=float(np.median(lr)),p95=float(np.percentile(lr,95)),max=float(lr.max())),
                 roughness_vs_3cm_lowpass_deg=dict(p50=float(np.median(rough)),p95=float(np.percentile(rough,95))),n=int(len(X)))
    print(nm, json.dumps(out[nm]))
json.dump(out,open(R+'evpkg/shading_geo.json','w'),indent=1)
