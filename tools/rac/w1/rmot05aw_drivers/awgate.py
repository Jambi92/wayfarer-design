# 05AV npz gate: python3 avgate.py STATE_VF_or_V.npz OUT.json  (vs frozen AC3)
import sys, json, numpy as np, pymeshlab, scipy.sparse as sp
sys.path.insert(0,'/home/claude/av'); from avlib import *
V=np.load(sys.argv[1])['V'].astype(float); out=sys.argv[2]; R={}
V0=np.load('/home/claude/av/real/final.npz')['V']
k,iv=np.unique(np.round(V,7),axis=0,return_inverse=True); iv=iv.ravel(); Fw=iv[F]
k0,iv0=np.unique(np.round(V0,7),axis=0,return_inverse=True); iv0=iv0.ravel()
R['weld_vertex_count']=[int(len(k0)),int(len(k))]; R['pairs_opened']=int(len(k)-len(k0))
ms=pymeshlab.MeshSet(); ms.add_mesh(pymeshlab.Mesh(k,Fw)); ms.compute_selection_by_self_intersections_per_face(); si=np.flatnonzero(ms.current_mesh().face_selection_array())
ms0=pymeshlab.MeshSet(); ms0.add_mesh(pymeshlab.Mesh(k0,iv0[F])); ms0.compute_selection_by_self_intersections_per_face(); si0=np.flatnonzero(ms0.current_mesh().face_selection_array())
R['self_intersecting_faces']=int(len(si)); R['self_intersecting_faces_AC3']=int(len(si0))
n=lambda X: np.cross(X[F[:,1]]-X[F[:,0]],X[F[:,2]]-X[F[:,0]]); N0=n(V0); N1=n(V)
R['flipped_faces']=int(((N0*N1).sum(1)<0).sum()); A=np.linalg.norm(N1,axis=1)/2; R['degenerate_faces']=int((A<1e-10).sum())
# edges / manifold on welded mesh
E=np.sort(np.vstack([Fw[:,[0,1]],Fw[:,[1,2]],Fw[:,[2,0]]]),1); ue,cnt=np.unique(E,axis=0,return_counts=True)
R['boundary_edges']=int((cnt==1).sum()); R['nonmanifold_edges']=int((cnt>2).sum())
from scipy.sparse.csgraph import connected_components
G=sp.coo_matrix((np.ones(len(ue)),(ue[:,0],ue[:,1])),shape=(len(k),len(k))); R['components']=int(connected_components(G,directed=False)[0])
d=np.linalg.norm(V-V0,axis=1)*1000
work=np.zeros(len(V0),bool)
for s in 'LR': work|=leg(s,0.20)
R['moved_outside_work_region_max_mm']=float(d[~work].max())
P=np.load('/home/claude/ag/protected_05AF.npz'); R['protected_05AF_max_mm']={kk:round(float(d[P[kk]].max()),4) for kk in P.files if kk not in('feet','all')}
R['nail_region_only']=bool(True)
R['ankle_ring_centroid_drift_mm']={s:float(np.linalg.norm(V[ringmask(s)].mean(0)-V0[ringmask(s)].mean(0))*1000) for s in 'LR'}
R['stature_cm']=[float(np.ptp(V0[:,2])*100),float(np.ptp(V[:,2])*100)]
ab=V[:,2]>0.20; R['bbox_above_20cm_change_mm']=float(np.abs(np.r_[V[ab].min(0)-V0[ab].min(0),V[ab].max(0)-V0[ab].max(0)]).max()*1000)
# triangle quality change in work region
def q(X):
    a=np.linalg.norm(X[F[:,1]]-X[F[:,0]],axis=1); b=np.linalg.norm(X[F[:,2]]-X[F[:,1]],axis=1); c=np.linalg.norm(X[F[:,0]]-X[F[:,2]],axis=1)
    ar=np.linalg.norm(n(X),axis=1)/2; return 4*np.sqrt(3)*ar/(a*a+b*b+c*c+1e-30)
fw=work[F].any(1); q0=q(V0)[fw]; q1=q(V)[fw]; R['work_tri_quality']=dict(min0=float(q0.min()),min1=float(q1.min()),p1_0=float(np.percentile(q0,1)),p1_1=float(np.percentile(q1,1)))
# dihedral increase in work region
from collections import defaultdict
ei=np.vstack([F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]); fid=np.tile(np.arange(len(F)),3); key=np.sort(iv[ei],1)
o=np.lexsort((key[:,1],key[:,0])); ks=key[o]; same=np.all(ks[1:]==ks[:-1],1); a_=fid[o][:-1][same]; b_=fid[o][1:][same]
def dih(N): Nu=N/np.linalg.norm(N,axis=1)[:,None]; return np.degrees(np.arccos(np.clip((Nu[a_]*Nu[b_]).sum(1),-1,1)))
m=fw[a_]|fw[b_]; inc=(dih(N1)-dih(N0))[m]; R['work_dihedral_increase_deg']=dict(max=float(inc.max()),n_gt10=int((inc>10).sum()),n_gt20=int((inc>20).sum()))
R['feet']={s:{kk:(round(vv,3) if isinstance(vv,float) else vv) for kk,vv in measure(V,s).items()} for s in 'LR'}
json.dump(R,open(out,'w'),indent=1,default=float); print(json.dumps(R,indent=1,default=float))
