# freeze_v5_verify.py WORK PCDIR OUT.json : order 78a109f §5 / §6 -- read-back verification of the frozen MPFB Family Base v005 realizations (the PC copies),
# without re-saving anything: file sha256 vs the v005 manifest, blend read-back (freeze_check.py, bpy: geometry / face hash, integrity, normals, geometry ==
# candidate), map compatibility (PC hm08 map == manifest map, candidate V == M5 @ race hm08 exactly), D1+D3+D4+D5 69/69 recomputed from the blend-identical
# candidate, anatomy / density / face / identity evidence, source hashes.
import sys, os, json, hashlib, subprocess, numpy as np
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001')
from v004_lib import NAT, R6, csr
from val2lib import evaluate, REF_STATURE_CM
W, PC, OUT = sys.argv[1:4]; sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest(); BP = '/home/claude/stc/bin/python3'; T = '/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001'
man = json.load(open(PC + '/Marchfolk/RP3/MPFB_FAMILY_BASE_v005.json'))
ENT = [('MF-M-R', 'Marchfolk', 'MF_M_REF_RP3_retopo_v005'), ('MF-F-R', 'Marchfolk', 'MF_F_REF_RP3_retopo_v005'), ('SK208-C1R', 'Skarn', 'SK_M_REF_RP3_retopo_v003'), ('SKF208', 'Skarn', 'SK_F_REF_RP3_retopo_v003')]
R = dict(manifest_sha256=sha(PC + '/Marchfolk/RP3/MPFB_FAMILY_BASE_v005.json'), files={})
for cid, race, nm in ENT:
    bl = '%s/%s/RP3/%s.blend' % (PC, race, nm); mp = '%s/%s/RP3/%s_hm08_map.npz' % (PC, race, nm); cz = '%s/cand/%s_v005.npz' % (W, cid)
    out = subprocess.run([BP, T + '/freeze_check.py', bl, cz, '%s/lm/%s_v005_landmarks.json' % (W, cid), '%s/freeze/%s_FREEZE_readback.json' % (W, nm)], capture_output=True, text=True)
    rb = json.load(open('%s/freeze/%s_FREEZE_readback.json' % (W, nm)))
    c = np.load(cz); M = csr(c); Vh = np.load(NAT[cid])['V'].astype(float); mz = np.load(mp); Mp = csr(mz)
    e = evaluate(c['V'].astype(float), np.asarray(c['Q']), json.loads(str(c['meta'])), REF_STATURE_CM, d5=True)
    an = json.load(open('%s/anat/%s_v005_anatomy.json' % (W, cid))); au = json.load(open('%s/audit/%s_v005_audit.json' % (W, cid))); fr = json.load(open('%s/audit/%s_v005_face.json' % (W, cid)))
    m = man['configurations'][cid]
    R['files'][nm] = dict(sha256=sha(bl), sha256_matches_manifest=sha(bl) == m['sha256'], geometry_hash=rb['geometry_hash'], geometry_hash_matches_manifest=rb['geometry_hash'] == m['geometry_hash'],
                          face_topology_hash=rb['face_topology_hash'], face_topology_matches_family=rb['face_topology_hash'] == man['topology']['face_topology_hash'], verts=rb['verts'], quads=rb['faces'], quads_pct=rb['quads_pct'],
                          components=rb['components'], boundary_edges=rb['boundary_edges'], nonmanifold_edges=rb['nonmanifold_edges'], nonmanifold_vertices=rb['nonmanifold_vertices'], degenerate_faces=rb['degenerate_faces'],
                          normals_outward=rb['normals_outward'], blend_equals_candidate_max_m=rb['max_abs_diff_vs_candidate_m'], faces_equal_candidate=rb['faces_equal_candidate'],
                          hm08_map_sha256=sha(mp), hm08_map_matches_manifest=sha(mp) == man['maps']['hm08_to_v005']['sha256'], map_arrays_equal_candidate=bool(abs(Mp - M).max() == 0 and np.array_equal(mz['Q'], c['Q'])),
                          candidate_equals_map_times_source=float(np.abs(M @ Vh - c['V']).max()), validator_D1_D3_D4_D5=dict(firm=e['summary']['firm_pass_count'], stations=e['summary']['stations'], fail=e['summary']['D1_D3_firm_fail']),
                          anatomy=dict(T1_T2=an['T1_T2_pass'], T3=an['T3_pass'], T7=an['T7_pass']), density_all_pass=all(v['pass_mean'] for v in au['density_pct_of_stature'].values()),
                          face=dict(mouth=fr['mouth_rings']['count'], orbits=[fr['orbit_rings_l']['count'], fr['orbit_rings_r']['count']], corner_poles=fr['poles_at_mouth_corners'], near_mouth_poles=fr['poles_within_2cm_of_mouth']),
                          sidecar_sha256=sha('%s/%s/RP3/%s.json' % (PC, race, nm)) if os.path.exists('%s/%s/RP3/%s.json' % (PC, race, nm)) else None)
    print(nm, json.dumps({k: v for k, v in R['files'][nm].items() if k not in ('sha256', 'geometry_hash', 'face_topology_hash', 'hm08_map_sha256')}), flush=True)
ok = all(v['sha256_matches_manifest'] and v['geometry_hash_matches_manifest'] and v['face_topology_matches_family'] and v['verts'] == 57842 and v['quads'] == 57840 and v['quads_pct'] == 100.0 and v['components'] == 1 and
         v['boundary_edges'] == 0 and v['nonmanifold_edges'] == 0 and v['nonmanifold_vertices'] == 0 and v['degenerate_faces'] == 0 and v['normals_outward'] and v['faces_equal_candidate'] and v['blend_equals_candidate_max_m'] < 1e-6 and
         v['hm08_map_matches_manifest'] and v['map_arrays_equal_candidate'] and v['candidate_equals_map_times_source'] < 1e-9 and v['validator_D1_D3_D4_D5']['firm'] == 69 and all(v['anatomy'].values()) and v['density_all_pass'] for v in R['files'].values())
R['all_checks_pass'] = bool(ok); R['identity'] = json.load(open(W + '/anat/SK208-C1R_v005_face_identity.json'))
json.dump(R, open(OUT, 'w'), indent=1); print('ALL CHECKS PASS' if ok else 'MISMATCH')
