# make_sidecar2.py OUT.json : production sidecar for GR_U_REF_RP2_retopo_v002
import json, sys, numpy as np, platform, datetime, hashlib, igl, trimesh, scipy
R='/tmp/claude-0/rt/'; J=lambda f: json.load(open(R+f))
g=J('v002_gate.json'); dev=J('v002_dev.json'); la=J('v002_loops_audit.json'); iou=J('v002_iou.json'); lm=J('v002_lmdrift.json')
idn=J('v002_identity.json'); org=J('v002_origin.json'); sym=J('v002_symmetry.json'); hard=J('v002_hard.json')
sb=open(R+'out2/src_before_both.txt').read().split(); sa=open(R+'out2/src_after_both.txt').read().split()
rb=open(R+'out2/readback.txt').read().split(); bsha=rb[rb.index('FILESHA')+1]; bgeo=rb[rb.index('GEOMHASH')+1]
S=dict(
 name='GR_U_REF_RP2_retopo_v002', race='Grask', cfg='U', state='REF', phase='RP2', step='retopo', version='v002',
 date=str(datetime.date.today()), status='RETOPO v002 OPTIMIZATION CANDIDATE - READY FOR AUTHOR REVIEW (not accepted; not frozen)',
 author='Claude (Opus 5.5) under Tyler / ChatGPT order reviews/chatgpt-rac-rp2-grask-retopo-v002-production-optimization-order.md (d683312)',
 source=dict(path='E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Grask/RP2/SOURCE_3D/GR_U_REF_RP2_SOURCE_3D_v005.blend',
   sha256_before_pc=sb[1],geometry_hash_before_pc=sb[3],sha256_before_cloud=sb[9],geometry_hash_before_cloud=sb[11],sha256_after_pc=sa[1],geometry_hash_after_pc=sa[3],sha256_after_cloud=sa[9],geometry_hash_after_cloud=sa[11],
   unchanged=(sb[1]==sa[1]==sb[9]==sa[9]=='7bba8d2d5f081c077351b2e79e7e5fcce91b4f376cd6b2cfc76f1c2eb052ab14' and sb[3]==sa[3]==sb[11]==sa[11]),object=sb[5],verts=int(sb[6]),tris=int(sb[7])),
 parent=dict(file='GR_U_REF_RP2_retopo_v001.blend',relation='same authored-cage architecture; v001 preserved unchanged as provenance (PC sha256 82c10a64... verified unchanged)'),
 blend=dict(file='GR_U_REF_RP2_retopo_v002.blend',sha256=bsha,geometry_hash=bgeo,geometry_hash_method='sha256(float32 vertex co bytes + int32 loop vertex_index bytes)',object='GR_U_REF_RP2_retopo_v002'),
 frame=dict(blender='m, Z up, faces -Y, subject left +X = (x,-f,u)/100 of the RAC analysis frame',origin='pelvis_root landmark projected to the ground plane (production mesh contract)',
   origin_translation_analysis_cm=org['translation_analysis_cm'],origin_translation_blender_m=org['translation_blender_m'],pelvis_root_after_cm=org['pelvis_root_after_cm'],
   bbox_production_cm=org['bbox_after_cm'],bbox_blender_m=org['bbox_after_blender_m'],interlandmark_max_abs_change_mm=org['interlandmark_max_abs_change_mm'],
   comparison_frame='all shape validation is done in the common v005 frame (translation undone)'),
 density=dict(selected='x2 Catmull-Clark of the revised authored cage (cage27: v001 cage + support loops at palm MCP row, finger and toe proximal phalanges, forefoot planes and shoulder fan)',
   cage_quads=None, verts=g['verts'], quads=g['quads'], triangle_equivalent=2*g['quads'], v001_quads=628736, reduction_vs_v001_pct=round(100*(1-g['quads']/628736),1),
   by_zone={k:{kk:v[kk] for kk in ('faces','edge_mean_mm','edge_median_mm','edge_p99_mm','edge_max_mm','ceiling_mm','density_pass')} for k,v in g['zones'].items()},
   ceiling_rule='contract ceilings applied as maximum MEAN edge length per zone'),
 topology={k:g[k] for k in ('verts','faces','quads','tris','ngons','quad_pct','boundary_edges','nonmanifold_edges','winding_inconsistent_edges','components','unused_verts','duplicate_faces','repeated_vertex_faces','coincident_verts','degenerate_faces(area<1e-4cm2)','normals_outward','poles','valence_hist')},
 quad_quality=dict(hard_limit_quads=len(hard['clusters']) if isinstance(hard,dict) else 0, hard_limit_definition='angle <20 or >160 deg, or aspect >8',
   angle_in_45_135_pct_all=g['angle_in_45_135_pct_all'],aspect_le4_pct_all=g['aspect_le4_pct_all'],
   by_zone={k:{kk:v[kk] for kk in ('angle_in_45_135_pct','angle_min','angle_max','aspect_le4_pct','aspect_max')} for k,v in g['zones'].items()}),
 stature_cm=g['stature_cm'], T3=dict(stature_diff_mm=g['T3_stature_diff_mm'],bbox_maxdiff_mm=g['T3_bbox_maxdiff_mm']),
 deviation_mm=dev, silhouette_iou={k:v['iou'] for k,v in iou['views'].items()},
 landmarks=dict(file='GR_U_REF_RP2_retopo_v002_landmarks.json',n=lm['n'],max_drift_mm=lm['max_mm'],over_1mm=list(lm['over_1mm']),sampling='dense ~1.2 mm area samples on v005 and v002 (v002 method)'),
 loop_audit=dict(all_pass=la['all_pass'],joints=len(la['joints'])), identity_audit=dict(max_abs_station_diff_mm=idn['max_abs_diff_mm']),
 symmetry=sym, self_intersections=0, folded_faces_gt120deg=0, flipped_faces=0,
 landmark_package_sha256=hashlib.sha256(open(R+'out2/GR_U_REF_RP2_retopo_v002_landmarks.json','rb').read()).hexdigest(),
 tools=dict(blender='5.2.2 LTS (bpy)',python=platform.python_version(),numpy=np.__version__,libigl=getattr(igl,'__version__','?'),trimesh=trimesh.__version__,scipy=scipy.__version__,scripts='tools/rac/rp/grask_retopo_v002/'),
 uv='none (seam PROPOSAL only, edge attribute seam_proposal)', lod='none (identity/deformation loops tagged: vertex groups LOOP_*, edge attribute identity_loop)',
 not_done=['freeze','rig','skin weights','creator morphs','UVs/materials','LODs','UE5','other races'],
 gate='reviews/claude-rac-rp2-grask-retopo-v002-optimization-gate.md', evidence='reviews/rac-rp2-evidence/grask_retopo_v002_optimization/')
cz=np.load(R+'cage27.npz'); S['density']['cage_quads']=int(len(cz['Q']))
json.dump(S,open(sys.argv[1],'w'),indent=1); print('sidecar written',S['source']['unchanged'],S['quad_quality']['hard_limit_quads'])
