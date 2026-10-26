# origin.py PROD.npz PROD_LM.json SRC_LM.json OUT.json : production-origin correction record (single rigid translation).
# origin = production pelvis_root landmark projected onto the ground plane (u = 0). Frames: analysis cm (x left, f fwd, u up);
# Blender m = (x,-f,u)/100.
import numpy as np, json, sys, itertools
z=np.load(sys.argv[1]); V=z['V'].astype(float); L=json.load(open(sys.argv[2])); S=json.load(open(sys.argv[3]))
pr=np.array(L['pelvis_root']['p']); ground=0.0
T=np.array([-pr[0],-pr[1],0.0])                      # no vertical move: the ground plane u=0 stays the ground plane
Vt=V+T; bl=lambda p: [float(p[0])/100,-float(p[1])/100,float(p[2])/100]
names=sorted(L); P0=np.array([L[k]['p'] for k in names]); P1=P0+T
D0=np.linalg.norm(P0[:,None]-P0[None],axis=2); D1=np.linalg.norm(P1[:,None]-P1[None],axis=2)
R=dict(rule='origin = pelvis_root landmark (re-measured on the production mesh) projected onto the ground plane; one rigid translation, no rotation, no scale, no per-vertex change',
  old_origin_analysis_cm=[0.0,0.0,0.0], old_origin_note='v001 / v005 source frame origin (x=0 midline, f=0, u=0 ground)',
  pelvis_root_production_cm=pr.tolist(), pelvis_root_v005_cm=S['pelvis_root']['p'], ground_u_cm=ground,
  translation_analysis_cm=T.tolist(), translation_blender_m=bl(T),
  new_origin_in_old_frame_cm=[float(pr[0]),float(pr[1]),ground], pelvis_root_after_cm=(pr+T).tolist(),
  bbox_before_cm=[V.min(0).tolist(),V.max(0).tolist()], bbox_after_cm=[Vt.min(0).tolist(),Vt.max(0).tolist()],
  bbox_after_blender_m=[[Vt[:,0].min()/100,-Vt[:,1].max()/100,Vt[:,2].min()/100],[Vt[:,0].max()/100,-Vt[:,1].min()/100,Vt[:,2].max()/100]],
  stature_before_cm=float(V[:,2].max()-V[:,2].min()), stature_after_cm=float(Vt[:,2].max()-Vt[:,2].min()),
  min_u_after_cm=float(Vt[:,2].min()),
  landmarks=len(names), interlandmark_pairs=len(names)*(len(names)-1)//2, interlandmark_max_abs_change_mm=float(np.abs(D1-D0).max()*10),
  vertex_offset_check_mm=float(np.abs((Vt-V)-T).max()*10),
  comparison_frame='all shape validation (T-1/T-2/T-3/T-6/T-7, identity, symmetry) is computed in the common v005 source frame, i.e. with this translation undone')
json.dump(R,open(sys.argv[4],'w'),indent=1); print(json.dumps({k:R[k] for k in ('translation_analysis_cm','pelvis_root_after_cm','interlandmark_max_abs_change_mm','stature_after_cm','min_u_after_cm')}))
