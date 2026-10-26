# sidecars.py WORK OUTDIR EVIDIR : RP3 Marchfolk production sidecars (one JSON per production .blend) + manifest + evidence bundle.
#   WORK   = RP3 workspace (src/ cand/ audit/ lm/ anat/ def/ sheets/ prod_hashes.jsonl)
#   OUTDIR = folder holding the production .blend files (sidecars written next to them)
#   EVIDIR = repo evidence folder (reviews/rac-rp3-evidence/marchfolk_baseline_v001)
import sys, os, json, shutil, hashlib, numpy as np
W, O, E = sys.argv[1:4]; os.makedirs(E, exist_ok=True)
for sd in ('regen', 'audit', 'anatomy', 'landmarks', 'deformation', 'sheets', 'mapping'): os.makedirs(os.path.join(E, sd), exist_ok=True)
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
PH = {os.path.basename(json.loads(l)['file']): json.loads(l) for l in open(W + '/prod_hashes.jsonl')}
REF = '/home/claude/wayfarer-design/reviews/reference-assets/r6'
man = dict(order='reviews/chatgpt-rac-rp2-closure-and-rp3-marchfolk-baseline-order.md (d18ff2a)', status='PRODUCTION CANDIDATES - not accepted; awaiting ChatGPT review / author acceptance', files={})
for C in ('M', 'F'):
    cid = 'MF-%s-R' % C; rc = json.load(open('%s/src/%s_regen_check.json' % (W, cid))); lm = json.load(open('%s/lm/%s_landmarks.json' % (W, cid)))
    for ver in ('v001', 'v002'):
        nm = 'MF_%s_REF_RP3_retopo_%s' % (C, ver); ph = PH[nm + '.blend']; tag = 'native' if ver == 'v001' else 'v002'
        au = json.load(open('%s/audit/%s_%s_audit.json' % (W, cid, tag))); an = json.load(open('%s/anat/%s_%s_anatomy.json' % (W, cid, tag))); fr = json.load(open('%s/audit/%s_%s_face.json' % (W, cid, tag)))
        df = json.load(open('%s/def/deform_%s_%s.json' % (W, cid, tag)))
        sc = dict(file=nm + '.blend', sha256=ph['sha256'], geometry_hash=ph['geometry_hash'], geometry_hash_method='sha256(float32 vertex co (m, production frame) + int32 loop vertex_index)',
                  face_topology_hash=ph['face_topology_hash'], face_topology_hash_method='sha256(int32 loop vertex_index)', verts=ph['verts'], quads=ph['quads'],
                  status='PRODUCTION CANDIDATE (RP3 Marchfolk) - not accepted', role=('native hm08 reference (helpers removed; no topology change) - FAILS contract §7 / §8' if ver == 'v001' else
                                                                                       'recommended Marchfolk production candidate (common family topology)'),
                  source=dict(id=cid, r6_npz='reviews/reference-assets/r6/%s_r6.npz' % cid, r6_sha256=rc['committed_sha256'], r6_geometry_hash=rc['committed_geom'], build_record=rc['build'], build_sha256=rc['build_sha256'],
                              regenerated_geometry_hash=rc['regen_geom'], regeneration_geometry_identical=rc['geometry_identical'], generator='MPFB 2.0.17 / Blender 5.2.2 (bpy), tools/rac/w1/arm_lib.py build -> ground -> pose_r6 -> ground'),
                  operations=(['regenerate MPFB source from the build record (geometry identical to the committed R-6)', 'remove MPFB helper geometry (joint cubes, eye / tongue / teeth / tights / skirt / hair helpers): keep the hm08 body faces',
                               'translate to the production origin (pelvis bone head projected to the ground) and convert to Blender frame (m, Z up, faces -Y, subject left +X)'] +
                              ([] if ver == 'v001' else ['one level of LINEAR (non-smoothing) quad subdivision: every new vertex is an edge midpoint or face centre of the hm08 surface',
                                                        'insert 98 closed edge rings around thighs and calves (midpoint splits of existing quad strips) to meet the leg density ceiling',
                                                        'UVs, MPFB targets and weights carry over through the recorded linear map (NAME_hm08_map.npz)'])),
                  frame=lm['frame'], landmarks='landmarks/%s_landmarks.json' % cid,
                  topology=dict(quads_pct=au['quads_pct'], components=au['components'], boundary_edges=au['boundary_edges'], nonmanifold_edges=au['nonmanifold_edges'], nonmanifold_vertices=au['nonmanifold_vertices'],
                                degenerate_faces=au['degenerate_faces'], coincident_vertex_pairs=au['coincident_vertex_pairs'], winding_consistent=au['winding_consistent'], normals_outward=au['normals_outward'],
                                self_intersection_face_pairs=au['self_intersection_face_pairs'], self_intersection_zones=au['self_intersection_zones'], poles=au['poles'],
                                T4_angle_violations=au['angle_45_135_violations'], T4_aspect_violations=au['aspect_gt4_violations'],
                                density_pct_of_stature={k: v['mean'] for k, v in au['density_pct_of_stature'].items()}, density_pass=all(v['pass_mean'] for v in au['density_pct_of_stature'].values()),
                                s7_failing_firm=au['s7_failing_firm'], s7_failing_strict=au['s7_failing_strict'], mouth_rings=fr['mouth_rings']['count'], orbit_rings=[fr['orbit_rings_l']['count'], fr['orbit_rings_r']['count']]),
                  anatomy=dict(stature_diff_mm=an['stature_diff_mm'], bbox_diff_mm=an['bbox_diff_mm'], prod_to_source=an['deviation_prod_to_source'], source_to_prod=an['deviation_source_to_prod'], silhouette_iou=an['silhouette_iou'],
                               T1_T2_pass=an['T1_T2_pass'], T3_pass=an['T3_pass'], T7_pass=an['T7_pass']),
                  deformation='deformation/deform_%s_%s.json' % (cid, tag), gate='reviews/claude-rac-rp3-marchfolk-production-baseline-gate.md')
        if ver == 'v002': sc['common_topology_map'] = dict(file=nm + '_hm08_map.npz', sha256=sha(os.path.join(O, nm + '_hm08_map.npz')), note='production vertex i = sum_j M[i, j] * hm08 body vertex j; identical M for both configurations')
        json.dump(sc, open(os.path.join(O, nm + '.json'), 'w'), indent=1); man['files'][nm] = dict(blend_sha256=ph['sha256'], geometry_hash=ph['geometry_hash'], face_topology_hash=ph['face_topology_hash'], sidecar=nm + '.json')
    for f_ in ('%s_regen_check.json' % cid,): shutil.copy('%s/src/%s' % (W, f_), '%s/regen/' % E)
    for t in ('native', 'v002'):
        for f_ in ('%s_%s_audit.json' % (cid, t), '%s_%s_face.json' % (cid, t)): shutil.copy('%s/audit/%s' % (W, f_), '%s/audit/' % E)
        shutil.copy('%s/anat/%s_%s_anatomy.json' % (W, cid, t), '%s/anatomy/' % E); shutil.copy('%s/def/deform_%s_%s.json' % (W, cid, t), '%s/deformation/' % E)
    shutil.copy('%s/lm/%s_landmarks.json' % (W, cid), '%s/landmarks/' % E); shutil.copy('%s/lm/%s_joint_centring.json' % (W, cid), '%s/landmarks/' % E)
# common topology mapping evidence
A = {C: np.load('%s/cand/MF-%s-R_v002.npz' % (W, C)) for C in ('M', 'F')}
mp = dict(configurations=['MF-M-R (configuration 1)', 'MF-F-R (configuration 2)'], v002_faces_identical=bool(np.array_equal(A['M']['Q'], A['F']['Q'])), v002_uv_identical=bool(np.array_equal(A['M']['UV'], A['F']['UV'])),
          v002_map_identical=bool(all(np.array_equal(A['M'][k], A['F'][k]) for k in ('M_data', 'M_indices', 'M_indptr', 'M_shape'))), v002_src_index_identical=bool(np.array_equal(A['M']['src_index'], A['F']['src_index'])),
          v002_hm08_faces_identical=bool(np.array_equal(A['M']['hm08_Q'], A['F']['hm08_Q'])), verts=int(len(A['M']['V'])), quads=int(len(A['M']['Q'])),
          face_topology_hash={k: v['face_topology_hash'] for k, v in man['files'].items()},
          mapping='vertex i of configuration 1 corresponds to vertex i of configuration 2 (same index, same UV, same hm08 linear-map row); both derive from the MPFB hm08 base mesh, whose vertex order is the MPFB family order',
          map_file='MF_{M,F}_REF_RP3_retopo_v002_hm08_map.npz (identical content)')
md = np.load(os.path.join(O, 'MF_M_REF_RP3_retopo_v002_hm08_map.npz')); fd = np.load(os.path.join(O, 'MF_F_REF_RP3_retopo_v002_hm08_map.npz'))
mp['map_files_content_identical'] = bool(all(np.array_equal(md[k], fd[k]) for k in md.files)); man['common_topology'] = mp
json.dump(mp, open('%s/mapping/MF_common_topology.json' % E, 'w'), indent=1)
json.dump(man, open(os.path.join(O, 'MF_RP3_manifest.json'), 'w'), indent=1); shutil.copy(os.path.join(O, 'MF_RP3_manifest.json'), E)
for f_ in os.listdir(O):
    if f_.endswith('.json'): shutil.copy(os.path.join(O, f_), E + '/')
for f_ in os.listdir(W + '/sheets'): shutil.copy('%s/sheets/%s' % (W, f_), '%s/sheets/' % E)
print(json.dumps(mp, indent=1))
