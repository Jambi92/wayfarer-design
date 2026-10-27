# sidecars3.py WORK OUTDIR EVIDIR : RP3 v003 sidecars (order 103c832 §14), manifest, mapping proof, evidence bundle.
import sys, os, json, shutil, hashlib, numpy as np
W, O, E = sys.argv[1:4]; os.makedirs(E, exist_ok=True)
for sd in ('audit', 'anatomy', 'landmarks', 'deformation', 'sheets', 'mapping', 'knee'): os.makedirs(os.path.join(E, sd), exist_ok=True)
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
PH = {os.path.basename(json.loads(l)['file']): json.loads(l) for l in open(W + '/prod_hashes.jsonl')}
REP = json.load(open(W + '/v3/v3_report.json')); core = np.load(W + '/v3/core_final.npz'); lg = json.loads(str(core['log']))
man = dict(order='reviews/chatgpt-rac-rp3-marchfolk-family-core-v003-order.md (103c832)', status='PRODUCTION CANDIDATE v003 - not frozen; awaiting ChatGPT / author review', files={})
mapf = {C: os.path.join(O, 'MF_%s_REF_RP3_retopo_v003_hm08_map.npz' % C) for C in 'MF'}; m23 = os.path.join(O, 'MF_REF_RP3_v002_to_v003_map.npz')
for C in 'MF':
    cid = 'MF-%s-R' % C; rc = json.load(open('%s/src/%s_regen_check.json' % (W, cid))); nm = 'MF_%s_REF_RP3_retopo_v003' % C; ph = PH[nm + '.blend']; p2 = PH['MF_%s_REF_RP3_retopo_v002.blend' % C]
    au = json.load(open('%s/audit/%s_v003_audit.json' % (W, cid))); an = json.load(open('%s/anat/%s_v003_anatomy.json' % (W, cid))); fr = json.load(open('%s/audit/%s_v003_face.json' % (W, cid))); r = REP['configs'][C]
    lm = json.load(open('%s/lm/%s_v003_landmarks.json' % (W, cid)))
    sc = dict(file=nm + '.blend', sha256=ph['sha256'], geometry_hash=ph['geometry_hash'], face_topology_hash=ph['face_topology_hash'], verts=ph['verts'], quads=ph['quads'],
              status='PRODUCTION CANDIDATE (RP3 Marchfolk v003 shared family core) - not frozen',
              source=dict(id=cid, r6_sha256=rc['committed_sha256'], build_sha256=rc['build_sha256'], r6_geometry_hash=rc['committed_geom']),
              parent_v002=dict(file='MF_%s_REF_RP3_retopo_v002.blend' % C, sha256=p2['sha256'], geometry_hash=p2['geometry_hash'], face_topology_hash=p2['face_topology_hash']),
              operations=['v002 topology and vertex order kept; %d closed root rings inserted (%s), new vertices appended (%d -> %d)' % (len(lg['rings']), ', '.join(x['name'] for x in lg['rings']), r['verts_v002'], r['verts_v003']),
                          'junction-pole relocation (palm MCP roots, pinky / hypothenar, ankle crease, MTP fan, toe IP) by surface-constrained slide on the configuration-average hm08 source surface',
                          'T-4 outlier relaxation (tangential Laplacian + parallelogram completion) in face / hands / feet, accepted only without station, envelope or contact regression',
                          'envelope / contact repair: relocated vertices restored where a source vertex left the surface by > 0.8 mm or a new hand / foot self-intersection appeared',
                          'shoulder-region T-4 relaxation restored (band-ray tie-order sensitivity); no other region change'],
              changed_zones={z: {k: v for k, v in d.items() if k in ('changed_vertices', 'added_vertices', 'changed_faces', 'relocation_max_mm', 't4_v002', 't4_v003', 'reason')} for z, d in r['zones'].items()},
              mapping=dict(hm08_map=os.path.basename(mapf[C]), hm08_map_sha256=sha(mapf[C]), v002_to_v003_map=os.path.basename(m23), v002_to_v003_map_sha256=sha(m23),
                           note='every v003 vertex = fixed linear combination of hm08 vertices (relocated vertices: 3 barycentric weights on one source triangle); weights / UVs / MPFB targets transfer through the same map'),
              topology=dict(quads_pct=au['quads_pct'], components=au['components'], boundary_edges=au['boundary_edges'], nonmanifold_edges=au['nonmanifold_edges'], degenerate_faces=au['degenerate_faces'],
                            winding_consistent=au['winding_consistent'], normals_outward=au['normals_outward'], self_intersection_face_pairs=au['self_intersection_face_pairs'], poles=au['poles'],
                            T4_angle=au['angle_45_135_violations'], T4_aspect=au['aspect_gt4_violations'], T4_union=r['t4_union_v003'], density={k: v['mean'] for k, v in au['density_pct_of_stature'].items()},
                            s7_failing_firm=au['s7_failing_firm'], s7_failing_strict=au['s7_failing_strict'], mouth_rings=fr['mouth_rings']['count'], orbit_rings=[fr['orbit_rings_l']['count'], fr['orbit_rings_r']['count']]),
              anatomy=dict(T1_T2_pass=an['T1_T2_pass'], T3_pass=an['T3_pass'], T7_pass=an['T7_pass'], stature_diff_mm=an['stature_diff_mm'], prod_to_source=an['deviation_prod_to_source'], source_to_prod=an['deviation_source_to_prod'], silhouette_iou=an['silhouette_iou']),
              frame=lm['frame'], landmarks='MF_%s_REF_RP3_v003_landmarks.json' % C, gate='reviews/claude-rac-rp3-marchfolk-family-core-v003-gate.md', gate_state='FAMILY BASE FAIL / NEEDS AUTHOR DECISION')
    json.dump(sc, open(os.path.join(O, nm + '.json'), 'w'), indent=1); shutil.copy('%s/lm/%s_v003_landmarks.json' % (W, cid), os.path.join(O, 'MF_%s_REF_RP3_v003_landmarks.json' % C))
    man['files'][nm] = dict(blend_sha256=ph['sha256'], geometry_hash=ph['geometry_hash'], face_topology_hash=ph['face_topology_hash'], sidecar=nm + '.json')
    for t in ('v003',):
        for f_ in ('%s_%s_audit.json' % (cid, t), '%s_%s_face.json' % (cid, t)): shutil.copy('%s/audit/%s' % (W, f_), E + '/audit/')
        shutil.copy('%s/anat/%s_%s_anatomy.json' % (W, cid, t), E + '/anatomy/'); shutil.copy('%s/def/deform_%s_%s.json' % (W, cid, t), E + '/deformation/'); shutil.copy('%s/lm/%s_v003_landmarks.json' % (W, cid), E + '/landmarks/')
A = {C: np.load('%s/cand/MF-%s-R_v003.npz' % (W, C)) for C in 'MF'}
mp = dict(v003_faces_identical=bool(np.array_equal(A['M']['Q'], A['F']['Q'])), v003_uv_identical=bool(np.array_equal(A['M']['UV'], A['F']['UV'])),
          v003_hm08_map_identical=bool(all(np.array_equal(A['M'][k], A['F'][k]) for k in ('M_data', 'M_indices', 'M_indptr', 'M_shape'))),
          verts_M=int(len(A['M']['V'])), verts_F=int(len(A['F']['V'])), quads=int(len(A['M']['Q'])), face_topology_hash={k: v['face_topology_hash'] for k, v in man['files'].items()},
          v002_vertex_order_kept=True, v002_vertices=int(core['n_v002']), appended_ring_vertices=int(len(A['M']['V']) - int(core['n_v002'])),
          map_files=dict(hm08_to_v003=[os.path.basename(mapf[C]) for C in 'MF'], v002_to_v003=os.path.basename(m23)), hm08_to_v003_sha256={C: sha(mapf[C]) for C in 'MF'}, v002_to_v003_sha256=sha(m23),
          weight_transfer='W_v003 = M3 @ W_hm08 (source MPFB game_engine weights), renormalised', uv_transfer='per-corner UV: unchanged corners keep v002 corner UVs; relocated vertices take the barycentric UV of their source triangle (same UV chart)',
          morph_transfer='any MPFB target D (hm08 vertex offsets) maps as M3 @ D; both configurations are M3 @ (their hm08 R-6 vertices)')
md, fd = np.load(mapf['M']), np.load(mapf['F']); mp['hm08_map_files_content_identical'] = bool(all(np.array_equal(md[k], fd[k]) for k in md.files))
man['common_topology'] = mp; json.dump(mp, open(E + '/mapping/MF_v003_common_topology.json', 'w'), indent=1)
json.dump(man, open(os.path.join(O, 'MF_RP3_v003_manifest.json'), 'w'), indent=1); shutil.copy(os.path.join(O, 'MF_RP3_v003_manifest.json'), E)
for C in 'MF': shutil.copy(os.path.join(O, 'MF_%s_REF_RP3_retopo_v003.json' % C), E + '/')
shutil.copy(W + '/v3/v3_report.json', E + '/'); shutil.copy(W + '/v3/residuals_final.json', E + '/')
for f_ in ('knee/deform_MF-M-R_v003_kneeC.json', 'knee/deform_MF-M-R_v002_kneeC.json'):
    if os.path.exists(os.path.join(W, f_)): shutil.copy(os.path.join(W, f_), E + '/knee/')
for f_ in os.listdir(W + '/sheets3'): shutil.copy('%s/sheets3/%s' % (W, f_), E + '/sheets/')
print(json.dumps(mp, indent=1))
