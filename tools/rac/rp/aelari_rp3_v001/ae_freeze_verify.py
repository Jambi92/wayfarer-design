# ae_freeze_verify.py (from fn_freeze_verify.py) WORK PCDIR OUT.json : Aelari final consolidation (2026-10-28) §21 -- read-back verification of the Aelari RP3 production bodies (the PC copies, staged back from
# E:) before the freeze by record. Nothing is re-saved. Checks: file / sidecar / branch-map / landmark sha256 vs the files written by fn_make_prod.py;
# Blender read-back (freeze_check.py: sha, geometry and face-topology hash, integrity, normals, UVMap, geometry == production candidate npz);
# branch-map arrays == production candidate; c1 / c2 face lists identical; authoritative validator D1 + D3 + D4 + D5 + D6 recomputed on the candidate.
import sys, os, json, hashlib, subprocess, numpy as np, scipy.sparse as sp
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001')
from val2lib import evaluate, REF_STATURE_CM
W, PC, OUT = sys.argv[1:4]; sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest(); BP = '/home/claude/stc/bin/python3'; T = '/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001'
csr = lambda z: sp.csr_matrix((z['M_data'], z['M_indices'], z['M_indptr']), shape=tuple(z['M_shape'])); os.makedirs(W + '/readback', exist_ok=True)
R = dict(order='aelari-final-2026-10-28', pc_dir='E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Aelari/RP3', files={})
for cid, nm in (('AEL1-R1', 'AE_M_REF_RP3_v001'), ('AELF190-R1', 'AE_F_REF_RP3_v001')):
    bl = '%s/%s.blend' % (PC, nm); cz = '%s/ear/build/%s_AE-E2_branch.npz' % (W, cid); lmj = '%s/%s_landmarks.json' % (PC, nm); loc = '%s/prod/%s' % (W, nm)
    subprocess.run([BP, T + '/freeze_check.py', bl, cz, lmj, '%s/readback/%s_FREEZE_readback.json' % (W, nm)], capture_output=True, text=True)
    rb = json.load(open('%s/readback/%s_FREEZE_readback.json' % (W, nm))); sc = json.load(open(loc + '.json')); c = np.load(cz); mz = np.load('%s/%s_branch_map.npz' % (PC, nm))
    nz = np.load('%s/src/%s_native.npz' % (W, cid)); M = csr(c)
    e = evaluate(c['V'].astype(float), np.asarray(c['Q']), json.loads(str(c['meta'])), REF_STATURE_CM, d5=True, d6=(np.asarray(M @ nz['W']), [str(b) for b in nz['bones']]))
    f = dict(file=nm + '.blend', sha256=sha(bl), sha256_equals_written=sha(bl) == sc['file_sha256'], geometry_hash=rb['geometry_hash'], geometry_hash_equals_written=rb['geometry_hash'] == sc['geometry_hash'],
             face_topology_hash=rb['face_topology_hash'], verts=rb['verts'], quads=rb['faces'], quads_pct=rb['quads_pct'], mesh_objects=rb['mesh_objects'], uv_layers=rb['uv_layers'], components=rb['components'],
             boundary_edges=rb['boundary_edges'], nonmanifold_edges=rb['nonmanifold_edges'], nonmanifold_vertices=rb['nonmanifold_vertices'], degenerate_faces=rb['degenerate_faces'], normals_outward=rb['normals_outward'],
             max_abs_diff_vs_candidate_m=rb['max_abs_diff_vs_candidate_m'], faces_equal_candidate=rb['faces_equal_candidate'], embedded_status=rb['properties'].get('RAC_status'),
             sidecar_sha256=sha('%s/%s.json' % (PC, nm)), sidecar_equals_written=sha('%s/%s.json' % (PC, nm)) == sha(loc + '.json'),
             branch_map_sha256=sha('%s/%s_branch_map.npz' % (PC, nm)), branch_map_equals_written=sha('%s/%s_branch_map.npz' % (PC, nm)) == sc['branch_map_sha256'],
             branch_map_arrays_equal_candidate=bool(abs(csr(mz) - M).max() == 0 and all(np.array_equal(mz[k], c[k]) for k in ('Q', 'src_index', 'hm08_Q', 'v005_to_branch', 'removed_v005', 'removed_faces_v005', 'part', 'side'))),
             landmarks_sha256=sha(lmj), landmarks_equal_written=sha(lmj) == sc['landmarks_sha256'],
             validator=dict(firm=e['summary']['firm_pass_count'], stations=e['summary']['stations'], fails=e['summary']['D1_D3_firm_fail'], margin_zero=e['summary']['margin_zero']))
    f['all_pass'] = all([f['sha256_equals_written'], f['geometry_hash_equals_written'], f['verts'] == 58944, f['quads'] == 58942, f['quads_pct'] == 100.0, f['mesh_objects'] == 1, f['uv_layers'] == ['UVMap'], f['components'] == 1,
                         f['boundary_edges'] == 0, f['nonmanifold_edges'] == 0, f['nonmanifold_vertices'] == 0, f['degenerate_faces'] == 0, f['normals_outward'], f['faces_equal_candidate'], f['max_abs_diff_vs_candidate_m'] < 1e-6,
                         f['sidecar_equals_written'], f['branch_map_equals_written'], f['branch_map_arrays_equal_candidate'], f['landmarks_equal_written'], f['validator']['firm'] == 69])
    R['files'][cid] = f; print(cid, 'ALL PASS' if f['all_pass'] else 'FAIL', f['sha256'][:8], f['validator']['firm'], flush=True)
R['c1_c2_face_topology_identical'] = R['files']['AEL1-R1']['face_topology_hash'] == R['files']['AELF190-R1']['face_topology_hash']
R['all_pass'] = all(f['all_pass'] for f in R['files'].values()) and R['c1_c2_face_topology_identical']
json.dump(R, open(OUT, 'w'), indent=1); print('ALL CHECKS PASS' if R['all_pass'] else 'CHECK FAILURE')
