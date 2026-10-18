# 05AW1 gate (topology-aware): python3 aw1gate.py STATE_VF.npz SUPPORT.npy OUT.json   (AW1_TOPO = topology base; vs frozen 05AV)
import sys, os, json, numpy as np, pymeshlab, scipy.sparse as sp
sys.path.insert(0,'/home/claude/av'); sys.path.insert(0,'/home/claude/aw1')
import aw1lib as L
from avlib import measure, ringmask, leg
D=np.load(sys.argv[1]); V=D['V'].astype(float); F=D['F']; sup=np.load(sys.argv[2]); out=sys.argv[3]; R={}
assert F.shape==L.F.shape and (F==L.F).all(), 'topology differs from base'
Vold=L.Vold; F0=np.load('/home/claude/av/real/final.npz')['F'] if 'F' in np.load('/home/claude/av/real/final.npz').files else None
# welded meshes
k,iv=np.unique(np.round(V,7),axis=0,return_inverse=True); iv=iv.ravel(); Fw=iv[F]
R['welded_vertices']=int(len(k))
def si_count(K,FF):
    ms=pymeshlab.MeshSet(); ms.add_mesh(pymeshlab.Mesh(K,FF)); ms.compute_selection_by_self_intersections_per_face(); return np.flatnonzero(ms.current_mesh().face_selection_array())
si=si_count(k,Fw); R['self_intersecting_faces']=int(len(si))
E=np.sort(np.vstack([Fw[:,[0,1]],Fw[:,[1,2]],Fw[:,[2,0]]]),1); ue,cnt=np.unique(E,axis=0,return_counts=True)
R['boundary_edges']=int((cnt==1).sum()); R['nonmanifold_edges']=int((cnt>2).sum())
from scipy.sparse.csgraph import connected_components
G=sp.coo_matrix((np.ones(len(ue)),(ue[:,0],ue[:,1])),shape=(len(k),len(k))); R['components']=int(connected_components(G,directed=False)[0])
chi=len(k)-len(ue)+len(Fw); R['euler']=int(chi); R['genus']=int((2-chi)//2)
# opened seams: any still-duplicated position pair in base whose copies no longer coincide
kb,ib=np.unique(np.round(L.V0,7),axis=0,return_inverse=True); ib=ib.ravel()
R['pairs_opened']=int(len(k)-len(kb))
# flips / degenerates vs the source surface (moved faces only, vs source normal at the same base vertices)
n=lambda X: np.cross(X[F[:,1]]-X[F[:,0]],X[F[:,2]]-X[F[:,0]])
N1=n(V); N0=n(L.V0); A=np.linalg.norm(N1,axis=1)/2; R['degenerate_faces']=int((A<1e-10).sum())
mv=np.linalg.norm(V-L.V0,axis=1)>1e-9; fm=mv[F].any(1)
vn0=L.vnormals(L.V0)
for _ in range(10): vn0=L.Avg@vn0
vn0/=np.linalg.norm(vn0,axis=1)[:,None]
R['flipped_faces_vs_base_face']=int(((N0*N1).sum(1)<0)[fm].sum())
R['flipped_faces_vs_source_surface']=int(((N1*vn0[F].mean(1)).sum(1)<0)[fm].sum())
R['flipped_faces_vs_source_surface_in_base']=int(((N0*vn0[F].mean(1)).sum(1)<0)[fm].sum())
# movement: base vertices outside support must not move; removed (dissolved) old vertices must lie in support
d=np.linalg.norm(V-L.V0,axis=1)*1000
R['moved_vertices']=int((d>1e-4).sum()); R['moved_outside_support']=int(((d>1e-4)&~sup).sum()); R['max_move_mm']=float(d.max())
present=np.zeros(len(Vold),bool); present[L.new2old]=True
kO,iO=np.unique(np.round(Vold,7),axis=0,return_inverse=True); iO=iO.ravel(); pw=np.zeros(len(kO),bool); pw[iO[L.new2old]]=True; present=pw[iO]
from scipy.spatial import cKDTree
dsup,_=cKDTree(L.V0[sup]).query(Vold[~present]) if (~present).any() else (np.zeros(0),None)
R['removed_old_vertices']=int((~present).sum()); R['removed_outside_support']=int((dsup>0.002).sum())
# full old-index state for measurements
Vo=Vold.copy(); Vo[L.new2old]=V
kk,ii=np.unique(np.round(Vold,7),axis=0,return_inverse=True); ii=ii.ravel()
rep=np.full(len(kk),-1); rep[ii[L.new2old]]=np.arange(len(V)); m=rep[ii]>=0; Vo[m]=V[rep[ii][m]]
R['ankle_ring_centroid_drift_mm']={s:float(np.linalg.norm(Vo[ringmask(s)].mean(0)-Vold[ringmask(s)].mean(0))*1000) for s in 'LR'}
R['stature_cm']=[float(np.ptp(Vold[:,2])*100),float(np.ptp(V[:,2])*100)]
R['lowest_moved_vertex_mm']=float(V[mv,2].min()*1000) if mv.any() else None; R['ground_min_mm']=float(V[:,2].min()*1000)
R['feet_before']={s:measure(Vold,s) for s in 'LR'}; R['feet_after']={s:measure(Vo,s) for s in 'LR'}
R['feet_delta']={s:{q:round(R['feet_after'][s][q]-R['feet_before'][s][q],4) for q in ('length','width_fp','heel_lift','heel')} for s in 'LR'}
# toe/toe contact: SI covers intersection; minimum clearance between different toes' moved verts not computed here
fw=fm
def q(X):
    a=np.linalg.norm(X[F[:,1]]-X[F[:,0]],axis=1); b=np.linalg.norm(X[F[:,2]]-X[F[:,1]],axis=1); c=np.linalg.norm(X[F[:,0]]-X[F[:,2]],axis=1)
    return 4*np.sqrt(3)*(np.linalg.norm(n(X),axis=1)/2)/(a*a+b*b+c*c+1e-30)
R['moved_tri_quality_min']=[float(q(L.V0)[fw].min()),float(q(V)[fw].min())]
json.dump(R,open(out,'w'),indent=1,default=float); print(json.dumps({x:R[x] for x in R if not x.startswith('feet_b') and not x.startswith('feet_a')},indent=1,default=float))
