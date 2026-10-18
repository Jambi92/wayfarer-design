# 05AW2 gate: python3 aw2gate.py STATE_VF.npz SUPPORT.npy OUT.json  (AW1_TOPO = subdivided topology base, AW1_ALLOWNEW=1)
import sys, os, json, numpy as np, pymeshlab, scipy.sparse as sp
sys.path.insert(0,'/home/claude/av'); sys.path.insert(0,'/home/claude/aw1')
import aw1lib as L
from avlib import measure, ringmask
from scipy.spatial import cKDTree
D=np.load(sys.argv[1]); V=D['V'].astype(float); F=D['F']; sup=np.load(sys.argv[2]); out=sys.argv[3]; R={}
assert F.shape==L.F.shape and (F==L.F).all(),'topology differs from base'
k,iv=np.unique(np.round(V,7),axis=0,return_inverse=True); iv=iv.ravel(); Fw=iv[F]; R['welded_vertices']=int(len(k)); R['vertices']=int(len(V)); R['new_vertices_from_subdivision']=int(L.isnew.sum())
ms=pymeshlab.MeshSet(); ms.add_mesh(pymeshlab.Mesh(k,Fw)); ms.compute_selection_by_self_intersections_per_face(); R['self_intersecting_faces']=int(ms.current_mesh().face_selection_array().sum())
E=np.sort(np.vstack([Fw[:,[0,1]],Fw[:,[1,2]],Fw[:,[2,0]]]),1); ue,cnt=np.unique(E,axis=0,return_counts=True)
R['boundary_edges']=int((cnt==1).sum()); R['nonmanifold_edges']=int((cnt>2).sum())
from scipy.sparse.csgraph import connected_components
G=sp.coo_matrix((np.ones(len(ue)),(ue[:,0],ue[:,1])),shape=(len(k),len(k))); R['components']=int(connected_components(G,directed=False)[0])
chi=len(k)-len(ue)+len(Fw); R['genus']=int((2-chi)//2)
kb=np.unique(np.round(L.V0,7),axis=0); R['pairs_opened']=int(len(k)-len(kb))
n=lambda X: np.cross(X[F[:,1]]-X[F[:,0]],X[F[:,2]]-X[F[:,0]]); N1=n(V); A=np.linalg.norm(N1,axis=1)/2; R['degenerate_faces']=int((A<1e-10).sum()); R['min_face_area_mm2']=float(A.min()*1e6)
# reference outward surface: smoothed normals of the T (pre-subdivision) source, sampled at nearest source vertex
T=np.load('/home/claude/aw1/real/T_VF.npz'); VT,FT=T['V'],T['F']
nt=np.zeros_like(VT); fnT=np.cross(VT[FT[:,1]]-VT[FT[:,0]],VT[FT[:,2]]-VT[FT[:,0]])
for i in range(3): np.add.at(nt,FT[:,i],fnT)
ET=np.concatenate([FT[:,[0,1]],FT[:,[1,2]],FT[:,[2,0]]]); AT=sp.coo_matrix((np.ones(len(ET)),(ET[:,0],ET[:,1])),shape=(len(VT),)*2).tocsr(); AT=((AT+AT.T)>0).astype(float); AT=sp.diags(1/np.asarray(AT.sum(1)).ravel())@AT
nt/=np.linalg.norm(nt,axis=1)[:,None]
for _ in range(10): nt=AT@nt
nt/=np.linalg.norm(nt,axis=1)[:,None]
_,ni=cKDTree(VT).query(L.V0); ref=nt[ni][F].mean(1)
mv=np.linalg.norm(V-L.V0,axis=1)>1e-9; fm=(mv|L.isnew)[F].any(1)
vc=L.vnormals(V)
for _ in range(20): vc=L.Avg@vc
vc/=np.linalg.norm(vc,axis=1)[:,None]
fold=((N1*vc[F].mean(1)).sum(1)<0)
R['folded_faces_vs_local_surface']=int(fold[fm].sum()); R['folded_face_ids']=np.where(fm&fold)[0].tolist()[:50]
R['inverted_faces_vs_source_surface']=int(((N1*ref).sum(1)<0)[fm].sum()); R['inverted_face_ids']=np.where(fm&((N1*ref).sum(1)<0))[0].tolist()[:50]
d=np.linalg.norm(V-L.V0,axis=1)*1000; R['moved_vertices']=int((d>1e-4).sum()); R['moved_outside_support']=int(((d>1e-4)&~sup).sum()); R['max_move_mm']=float(d.max())
old=~L.isnew; R['old_vertices_moved_outside_support_max_mm']=float(d[old&~sup].max()) if (old&~sup).any() else 0.0
R['new_vertices_outside_support']=int((L.isnew&~sup).sum())
Vo=L.Vold.copy(); kk,ii=np.unique(np.round(L.Vold,7),axis=0,return_inverse=True); ii=ii.ravel()
rep=np.full(len(kk),-1); oi=np.where(old)[0]; rep[ii[L.new2old[oi]]]=oi; m=rep[ii]>=0; Vo[m]=V[rep[ii][m]]
R['ankle_ring_centroid_drift_mm']={s:float(np.linalg.norm(Vo[ringmask(s)].mean(0)-L.Vold[ringmask(s)].mean(0))*1000) for s in 'LR'}
R['stature_cm']=[float(np.ptp(L.Vold[:,2])*100),float(np.ptp(V[:,2])*100)]
R['lowest_moved_vertex_mm']=float(V[mv,2].min()*1000) if mv.any() else None; R['ground_min_mm']=float(V[:,2].min()*1000)
fb={s:measure(L.Vold,s) for s in 'LR'}; fa={s:measure(Vo,s) for s in 'LR'}
# foot length uses the old-index foot set; add the true toe-tip extent including new vertices
R['feet_delta']={s:{q:round(fa[s][q]-fb[s][q],4) for q in ('length','width_fp','heel_lift','heel')} for s in 'LR'}
for s in 'LR':
    ax=np.array(json.load(open('/home/claude/aw1/footframes.json'))[s]['a']); side=(np.sign(V[:,0])==(1 if s=='L' else -1))&(V[:,2]<0.2)
    R['feet_delta'][s]['toe_tip_extent_mm']=round(float((V[side]@ax).max()-(L.Vold[(np.sign(L.Vold[:,0])==(1 if s=='L' else -1))&(L.Vold[:,2]<0.2)]@ax).max())*1000,3)
json.dump(R,open(out,'w'),indent=1,default=float); print(json.dumps(R,indent=1,default=float))
