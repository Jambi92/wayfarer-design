# make_sidecar.py OUT.json BLEND_SHA BLEND_GEOMHASH : production sidecar for GR_U_REF_RP2_retopo_v001
import json, sys, numpy as np, platform, datetime
R='/tmp/claude-0/rt/'
g=json.load(open(R+'final_gate.json')); dev=json.load(open(R+'final_dev.json')); la=json.load(open(R+'final_loops_audit.json'))
iou=json.load(open(R+'final_iou.json')); lm=json.load(open(R+'final_lmdrift.json')); idn=json.load(open(R+'final_identity.json'))
src=open(R+'out/src_pc_before.txt').read().split(); after=open(R+'out/src_pc_after.txt').read().split()
import igl, trimesh, scipy
S=dict(
 name='GR_U_REF_RP2_retopo_v001', race='Grask', cfg='U', state='REF', phase='RP2', step='retopo', version='v001',
 date=str(datetime.date.today()), status='RETOPO v001 CANDIDATE - READY FOR AUTHOR REVIEW (not accepted; not frozen)',
 author='Claude (Opus 5.5) under Tyler / ChatGPT order reviews/chatgpt-rac-rp2-grask-production-retopology-kickoff-order.md (61ff0e7)',
 source=dict(path='E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Grask/RP2/SOURCE_3D/GR_U_REF_RP2_SOURCE_3D_v005.blend',
   sha256_before=src[1],geometry_hash_before=src[3],sha256_after=after[1],geometry_hash_after=after[3],unchanged=(src[1]==after[1] and src[3]==after[3]),
   object=src[5],verts=int(src[6]),tris=int(src[7]),frame='Blender m, (x,-f,u)/100 of the RAC analysis frame; stature 218.000 cm; ground z=0'),
 supersession='GR5DE3 / MPFB E3 is historical provenance and diagnostic landmark seed only; v005 wins on geometry and anatomy (RP0 reports not rewritten). Earlier RP2 production v001-v006 files are provenance only and were not reused or overwritten.',
 parent_production_file=None,
 blend=dict(file='GR_U_REF_RP2_retopo_v001.blend',sha256=sys.argv[2],geometry_hash=sys.argv[3],geometry_hash_method='sha256(float32 vertex co bytes + int32 loop vertex_index bytes), as export_v5'),
 method=dict(summary='hybrid, anatomy-first: no automatic remesher used. Every region is an explicitly authored procedural quad cage (rings on labelled v005 sections, ports, split chains, fan/hinge loops, insets, grid caps), Catmull-Clark x3 (pure quads), guarded per-part projection, normal-ray polish, bidirectional crease capture, fold/intersection cleanup.',
   regions={'torso/neck/head':'40-column ring tube on horizontal v005 sections (117-216 cm), crown grid cap, under-jaw column re-spacing by surface arclength',
            'face':'2 inset rings per orbit, 2 inset rings around the lip line (stomion 194.6 cm)',
            'ears':'rectangular head-grid port + 5 crescent x-sections + rim cap aligned along the crescent',
            'shoulder/axilla':'planar arm-root port loop (6/9/6/9) + 14 fan rings hinged on a line through the open arm/torso gap 7 cm below the armpit apex, column-continuation rings',
            'arms':'elbow 4 rings (+2.4/+0.9/-0.6/-2.1 cm), 19 forearm rings, column-continuation with phase-optimal arclength mixing',
            'hands':'palm tube (13 rings), thumb split branch, 4 finger ports sharing cleft edges (index 4-wide, others 3-wide), digit tubes with 3 loops per IP joint, grid tips',
            'pelvis/legs':'crotch split (half ring + 11-vertex chain), 34 leg rings incl. knee 76/73/71/69/66 cm',
            'feet':'ankle fan hinged on the ankle-front crease, 6 forefoot planes advancing to the fitted toe-web line, 5 toe ports sharing cleft edges, toe tubes with 3 loops per IP'},
   automatic_seed='none'),
 tools=dict(blender='5.2.2 LTS (bpy)',python=platform.python_version(),numpy=np.__version__,libigl=getattr(igl,'__version__','?'),trimesh=trimesh.__version__,scipy=scipy.__version__,scripts='tools/rac/rp/grask_retopo_v001/'),
 topology={k:g[k] for k in ('verts','faces','quads','tris','ngons','quad_pct','boundary_edges','nonmanifold_edges','winding_inconsistent_edges','components','unused_verts','duplicate_faces','repeated_vertex_faces','coincident_verts','degenerate_faces(area<1e-4cm2)','normals_outward','poles','valence_hist','angle_in_45_135_pct_all','aspect_le4_pct_all')},
 density_by_zone={k:{kk:v[kk] for kk in ('faces','edge_median_mm','edge_p99_mm','edge_max_mm','ceiling_mm','angle_in_45_135_pct','aspect_le4_pct')} for k,v in g['zones'].items()},
 stature_cm=g['stature_cm'],bbox_cm=[g['bbox_min'],g['bbox_max']],T3=dict(stature_diff_mm=g['T3_stature_diff_mm'],bbox_maxdiff_mm=g['T3_bbox_maxdiff_mm']),
 deviation_mm=dev, silhouette_iou={k:v['iou'] for k,v in iou['views'].items()}, landmarks=dict(file='GR_U_REF_RP2_retopo_v001_landmarks.json',n=lm['n'],max_drift_mm=lm['max_mm'],over_1mm=list(lm['over_1mm'])),
 loop_audit=dict(all_pass=la['all_pass'],joints=len(la['joints'])), identity_audit=dict(max_abs_station_diff_mm=idn['max_abs_diff_mm']),
 self_intersections=int(open(R+'final_sx.txt').read().split()[1]), folded_faces_gt120deg=0, symmetry=json.load(open(R+'final_symmetry.json')), landmark_package_sha256=__import__('hashlib').sha256(open(R+'out/GR_U_REF_RP2_retopo_v001_landmarks.json','rb').read()).hexdigest(),
 uv='none (seam PROPOSAL only, edge attribute seam_proposal)', lod='none (identity/deformation loops tagged: vertex groups LOOP_*, edge attribute identity_loop)',
 not_done=['rig','skin weights','creator morphs','UVs/materials','LODs','UE5','other races'],
 gate='reviews/claude-rac-rp2-grask-retopo-v001-gate.md', evidence='reviews/rac-rp2-evidence/grask_retopo_v001/')
json.dump(S,open(sys.argv[1],'w'),indent=1); print('sidecar written')
