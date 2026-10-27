# freeze_sg_verify.py WORK PCDIR OUT.json : order d921903 §6-§8 -- read-back verification of the Sagekin RP3 production bodies (the PC copies) before the
# freeze by record. Nothing is re-saved. Checks: file / sidecar / landmark sha256 vs the propagation manifest; Blender read-back (freeze_check.py: geometry and
# face hash, integrity, normals, UVs, geometry == candidate); map compatibility (PC hm08 map == active family map, arrays identical; candidate V == M @ race
# hm08 exactly); authoritative validator D1 + D3 + D4 + D5 + D6 recomputed (69 / 69); source hashes; gate evidence.
import sys, os, json, hashlib, subprocess, numpy as np, scipy.sparse as sp
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001')
from val2lib import evaluate, REF_STATURE_CM
W, PC, OUT = sys.argv[1:4]; sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest(); BP = '/home/claude/stc/bin/python3'; T = '/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001'
REPO = '/home/claude/wayfarer-design'; RA = REPO + '/reviews/reference-assets'; EV = REPO + '/reviews/rac-rp3-evidence/sagekin_rp3_v001'; FAMMAP = '/mnt/user-data/outputs/rp5/MF_M_REF_RP3_retopo_v005_hm08_map.npz'
FACE = 'ec768ae210ea3ee1c053d0c4cd3256d57dad6db35d515502706b74f64281bee0'
man = json.load(open(PC + '/SAGEKIN_RP3_family_propagation_manifest.json')); csr = lambda z: sp.csr_matrix((z['M_data'], z['M_indices'], z['M_indptr']), shape=tuple(z['M_shape']))
fm = np.load(FAMMAP); Mf = csr(fm); os.makedirs(W + '/freeze', exist_ok=True)
R = dict(manifest_sha256=sha(PC + '/SAGEKIN_RP3_family_propagation_manifest.json'), family_map_sha256=sha(FAMMAP), files={})
for cid, nm in (('SG', 'SG_M_REF_RP3_retopo_v001'), ('SGF178', 'SG_F_REF_RP3_retopo_v001')):
    bl = '%s/%s.blend' % (PC, nm); mp = '%s/%s_hm08_map.npz' % (PC, nm); sc = '%s/%s.json' % (PC, nm); lmj = '%s/%s_landmarks.json' % (PC, nm.replace('_retopo', '')); cz = '%s/cand/%s_fam.npz' % (W, cid)
    subprocess.run([BP, T + '/freeze_check.py', bl, cz, lmj, '%s/freeze/%s_FREEZE_readback.json' % (W, nm)], capture_output=True, text=True)
    rb = json.load(open('%s/freeze/%s_FREEZE_readback.json' % (W, nm))); m = man['configurations'][cid]
    c = np.load(cz); M = csr(c); nz = np.load('%s/src/%s_native.npz' % (W, cid)); mz = np.load(mp)
    e = evaluate(c['V'].astype(float), np.asarray(c['Q']), json.loads(str(c['meta'])), REF_STATURE_CM, d5=True, d6=(np.asarray(M @ nz['W']), [str(b) for b in nz['bones']]))
    an = json.load(open('%s/anat/%s_fam_anatomy.json' % (W, cid))); au = json.load(open('%s/audit/%s_fam_audit.json' % (W, cid))); fr = json.load(open('%s/audit/%s_fam_face.json' % (W, cid)))
    ct = json.load(open('%s/audit/%s_contact.json' % (W, cid))); idn = json.load(open('%s/anat/%s_identity.json' % (W, cid))); rc = json.load(open('%s/src/%s_regen_check.json' % (W, cid)))
    f = dict(file=nm + '.blend', sha256=sha(bl), sha256_matches_manifest=sha(bl) == m['sha256'], geometry_hash=rb['geometry_hash'], geometry_hash_matches_manifest=rb['geometry_hash'] == m['geometry_hash'],
             face_topology_hash=rb['face_topology_hash'], face_hash_is_family=rb['face_topology_hash'] == FACE, verts=rb['verts'], quads=rb['faces'], quads_pct=rb['quads_pct'], mesh_objects=rb['mesh_objects'], uv_layers=rb['uv_layers'],
             components=rb['components'], boundary_edges=rb['boundary_edges'], nonmanifold_edges=rb['nonmanifold_edges'], nonmanifold_vertices=rb['nonmanifold_vertices'], degenerate_faces=rb['degenerate_faces'], normals_outward=rb['normals_outward'],
             max_abs_diff_vs_candidate_m=rb['max_abs_diff_vs_candidate_m'], faces_equal_candidate=rb['faces_equal_candidate'], embedded_status=rb['properties'].get('RAC_status'),
             sidecar_sha256=sha(sc), sidecar_matches_manifest=sha(sc) == m['sidecar_sha256'], landmarks_sha256=sha(lmj), landmarks_equal_repo=sha(lmj) == sha('%s/%s_landmarks.json' % (EV, nm.replace('_retopo', ''))),
             map_sha256=sha(mp), map_equals_family_map=sha(mp) == sha(FAMMAP), map_arrays_equal=bool(abs(csr(mz) - Mf).max() == 0 and np.array_equal(mz['Q'], fm['Q']) and np.array_equal(mz['src_index'], fm['src_index']) and np.array_equal(mz['hm08_Q'], fm['hm08_Q'])),
             candidate_V_eq_M_race_hm08_max_abs_cm=float(np.abs(Mf @ nz['V'].astype(float) - c['V'].astype(float)).max()),
             validator=dict(rules='D1 + D3 + D4 + D5 + D6 (authoritative, d921903)', firm=e['summary']['firm_pass_count'], stations=e['summary']['stations'], fails=e['summary']['D1_D3_firm_fail'], margin_zero=e['summary']['margin_zero'],
                            D6_undefined={k: v['D6_undefined_sides'] for k, v in e['stations'].items() if v['D6_undefined_sides']}),
             source=dict(r6_sha256=sha('%s/r6/%s_r6.npz' % (RA, cid)), r6_sha256_unchanged=sha('%s/r6/%s_r6.npz' % (RA, cid)) == rc['committed_sha256'], build_sha256=sha('%s/builds/%s_build.json' % (RA, cid)),
                         build_sha256_unchanged=sha('%s/builds/%s_build.json' % (RA, cid)) == rc['build_sha256'], regen_geometry_identical=rc['geometry_identical'], regen_max_abs_dV_cm=rc['max_abs_dV_cm']),
             gates=dict(T1_T2=an['T1_T2_pass'], T3=an['T3_pass'], T7=an['T7_pass'], iou_min=min(an['silhouette_iou'].values()), body_dev_mm=an['deviation_prod_to_source']['body'],
                        density_all_pass=all(v['pass_mean'] for v in au['density_pct_of_stature'].values()), density_zones=len(au['density_pct_of_stature']),
                        face=dict(mouth_rings=fr['mouth_rings']['count'], orbit_rings=[fr['orbit_rings_l']['count'], fr['orbit_rings_r']['count']], poles_at_mouth_corners=fr['poles_at_mouth_corners'], poles_within_2cm_of_mouth=fr['poles_within_2cm_of_mouth'], mouth_pass=fr['mouth_pass'], orbit_pass=fr['orbit_pass']),
                        contact_new=ct['classes']['new'], identity_holds_all_zones=idn['identity_holds_all_zones']))
    f['all_pass'] = all([f['sha256_matches_manifest'], f['geometry_hash_matches_manifest'], f['face_hash_is_family'], f['verts'] == 57842, f['quads'] == 57840, f['quads_pct'] == 100.0, f['components'] == 1, f['boundary_edges'] == 0,
                         f['nonmanifold_edges'] == 0, f['nonmanifold_vertices'] == 0, f['degenerate_faces'] == 0, f['normals_outward'], f['faces_equal_candidate'], f['max_abs_diff_vs_candidate_m'] < 1e-6, f['sidecar_matches_manifest'],
                         f['landmarks_equal_repo'], f['map_equals_family_map'], f['map_arrays_equal'], f['candidate_V_eq_M_race_hm08_max_abs_cm'] == 0.0, f['validator']['firm'] == 69, f['source']['r6_sha256_unchanged'], f['source']['build_sha256_unchanged'],
                         f['source']['regen_geometry_identical'], f['gates']['T1_T2'], f['gates']['T3'], f['gates']['T7'], f['gates']['density_all_pass'], f['gates']['contact_new'] == 0, f['gates']['identity_holds_all_zones'],
                         f['gates']['face']['mouth_pass'], f['gates']['face']['orbit_pass'], f['gates']['face']['poles_at_mouth_corners'] == 0])
    R['files'][cid] = f; print(cid, 'ALL PASS' if f['all_pass'] else 'FAIL', f['sha256'][:8], f['validator']['firm'], flush=True)
R['all_pass'] = all(f['all_pass'] for f in R['files'].values()); json.dump(R, open(OUT, 'w'), indent=1); print('ALL CHECKS PASS' if R['all_pass'] else 'CHECK FAILURE')
