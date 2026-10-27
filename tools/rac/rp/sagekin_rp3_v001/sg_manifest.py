# sg_manifest.py WORK EVIDIR : order c6c7940 §21 -- Sagekin RP3 sidecars, family propagation manifest, topology identity proof, margin table,
# deformation comparison against the frozen Marchfolk v005 realizations, SGF178 central-reference sidecar, hashes.
import sys, os, json, shutil, hashlib, numpy as np, scipy.sparse as sp
W, E = sys.argv[1:3]; os.makedirs(E, exist_ok=True); sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
REPO = '/home/claude/wayfarer-design'; RA = REPO + '/reviews/reference-assets'; B5 = '/mnt/user-data/outputs/rp5'
FR = json.load(open(REPO + '/reviews/rac-rp3-evidence/mpfb_family_base_v005_freeze/MPFB_FAMILY_BASE_v005_FREEZE.json'))
PH = {os.path.basename(json.loads(l)['file']): json.loads(l) for l in open(W + '/prod_hashes.jsonl')}
csr = lambda z: sp.csr_matrix((z['M_data'], z['M_indices'], z['M_indptr']), shape=tuple(z['M_shape']))
fm = np.load(B5 + '/MF_M_REF_RP3_retopo_v005_hm08_map.npz'); Mf = csr(fm)
ENT = [('SG', 'SG_M_REF_RP3_retopo_v001', 'configuration 1 (accepted SG, W1c)', 'MF-M-R'), ('SGF178', 'SG_F_REF_RP3_retopo_v001', 'configuration 2 (SGF178 central reference candidate, Part A PASS)', 'MF-F-R')]
fam0 = np.load('/tmp/claude-0/rt/v5/cand/MF-M-R_v005.npz')
man = dict(record='SAGEKIN RP3 MPFB family propagation manifest v001', order='reviews/chatgpt-rac-rp3-sagekin-config2-reference-and-propagation-order.md (c6c7940)', standard='specs/RAC_MPFB_FAMILY_PROPAGATION_STANDARD_v1.md (AUTHOR-ACCEPTED v1)',
           status='CANDIDATE - NOT FROZEN (awaiting ChatGPT / author review)',
           active_family_base=dict(record='MPFB_FAMILY_BASE_v005_FREEZE.json', record_sha256=sha(REPO + '/reviews/rac-rp3-evidence/mpfb_family_base_v005_freeze/MPFB_FAMILY_BASE_v005_FREEZE.json'),
                                   base_blend='MF_M_REF_RP3_retopo_v005.blend', base_blend_sha256=sha(B5 + '/MF_M_REF_RP3_retopo_v005.blend'), hm08_map='MF_M_REF_RP3_retopo_v005_hm08_map.npz',
                                   hm08_map_sha256=sha(B5 + '/MF_M_REF_RP3_retopo_v005_hm08_map.npz'), face_topology_hash=FR['topology']['face_topology_hash'] if 'face_topology_hash' in FR['topology'] else FR['topology']),
           configurations={})
proof = {}; margin = {}; dcmp = {}
for cid, nm, role, mfref in ENT:
    rc = json.load(open('%s/src/%s_regen_check.json' % (W, cid))); cz = np.load('%s/cand/%s_fam.npz' % (W, cid)); ph = PH[nm + '.blend']; rb = json.load(open('%s/readback/%s_readback.json' % (W, 'SG_M' if cid == 'SG' else 'SG_F')))
    au = json.load(open('%s/audit/%s_fam_audit.json' % (W, cid))); an = json.load(open('%s/anat/%s_fam_anatomy.json' % (W, cid))); fr = json.load(open('%s/audit/%s_fam_face.json' % (W, cid)))
    va = json.load(open('%s/val/%s_fam_validator_v2_D4_D5.json' % (W, cid))); ct = json.load(open('%s/audit/%s_contact.json' % (W, cid))); idn = json.load(open('%s/anat/%s_identity.json' % (W, cid)))
    d6 = json.load(open('%s/d6/%s_D4_D5_D6.json' % (W, cid))); lm = json.load(open('%s/lm/%s_fam_landmarks.json' % (W, cid))); nz = np.load('%s/src/%s_native.npz' % (W, cid))
    mp = '%s/prod/%s_hm08_map.npz' % (W, nm); mz = np.load(mp)
    pr = dict(face_topology_hash=ph['face_topology_hash'], equals_family=ph['face_topology_hash'] == fam0 is not None and ph['face_topology_hash'] == rb['face_topology_hash'], verts=ph['verts'], quads=ph['quads'],
              faces_equal_family_base=bool(np.array_equal(cz['Q'], fam0['Q'])), uv_equal_family_base=bool(np.array_equal(cz['UV'], fam0['UV'])), map_file_sha256=sha(mp), map_equal_family=sha(mp) == sha(B5 + '/MF_M_REF_RP3_retopo_v005_hm08_map.npz'),
              map_arrays_equal=bool(abs(csr(mz) - Mf).max() == 0 and np.array_equal(mz['Q'], fm['Q']) and np.array_equal(mz['hm08_Q'], fm['hm08_Q']) and np.array_equal(mz['src_index'], fm['src_index'])),
              V_equals_M_at_race_hm08_max_abs_cm=float(np.abs(Mf @ nz['V'].astype(float) - cz['V'].astype(float)).max()), hm08_faces_equal=bool(np.array_equal(nz['Q'], fm['hm08_Q'])), src_index_equal=bool(np.array_equal(nz['src_index'], fm['src_index'])),
              readback=rb)
    pr['equals_family'] = ph['face_topology_hash'] == 'ec768ae210ea3ee1c053d0c4cd3256d57dad6db35d515502706b74f64281bee0' and rb['face_topology_hash'] == ph['face_topology_hash']
    proof[cid] = pr
    S = va['stations']
    margin[cid] = {k: dict(loops=v['loops_v2'], required=v['required'], margin=v['margin'], firm=v['firm_D1_D3'], status=v['status_D1_D3'], mode=v['loop_mode'], D5_undefined_sides=v['D5_undefined_sides'], valid_sides=v['valid_sides'],
                           crease_poles_own_digit=v['crease_poles_own_digit'], proposed_D6=dict(loops=d6['stations'][k]['loops_v2'], firm=d6['stations'][k]['firm_D1_D3'], status=d6['stations'][k]['status_D1_D3'], D6_undefined_sides=d6['stations'][k]['D6_undefined_sides'])) for k, v in S.items()}
    Fs = json.load(open('%s/def/deform_%s_fam.json' % (W, cid)))['poses']; Ns = json.load(open('%s/def/deform_%s_native.json' % (W, cid)))['poses']; Fm = json.load(open('/tmp/claude-0/rt/v5/def/deform_%s_v005.json' % mfref))['poses']
    dcmp[cid] = dict(reference=mfref + ' v005 (frozen, same topology, accepted)', poses={p: dict(sagekin_family=dict(flipped=Fs[p]['flipped_in_zone'], selfx=Fs[p]['new_selfx_in_zone'], folds=Fs[p]['new_folds_in_zone']),
                                                                                                    sagekin_native_hm08=dict(flipped=Ns[p]['flipped_in_zone'], selfx=Ns[p]['new_selfx_in_zone'], folds=Ns[p]['new_folds_in_zone']),
                                                                                                    marchfolk_v005_family=dict(flipped=Fm[p]['flipped_in_zone'], selfx=Fm[p]['new_selfx_in_zone'], folds=Fm[p]['new_folds_in_zone'])) for p in Fs})
    dcmp[cid]['sagekin_minus_marchfolk_flipped_max'] = max(Fs[p]['flipped_in_zone'] - Fm[p]['flipped_in_zone'] for p in Fs)
    dcmp[cid]['poses_worse_than_marchfolk_by_more_than_5_flips'] = [p for p in Fs if Fs[p]['flipped_in_zone'] - Fm[p]['flipped_in_zone'] > 5]
    side = dict(file=nm + '.blend', sha256=ph['sha256'], geometry_hash=ph['geometry_hash'], face_topology_hash=ph['face_topology_hash'], verts=ph['verts'], quads=ph['quads'], race='Sagekin', configuration=cid, role=role,
                status='PRODUCTION CANDIDATE (RP3 Sagekin, MPFB Family Base v005) - CANDIDATE - NOT FROZEN',
                source=dict(id=cid, r6='reviews/reference-assets/r6/%s_r6.npz' % cid, r6_sha256=rc['committed_sha256'], build='reviews/reference-assets/builds/%s_build.json' % cid, build_sha256=rc['build_sha256'], regen_geometry_identical=rc['geometry_identical'], regen_max_abs_dV_cm=rc['max_abs_dV_cm']),
                mapping=dict(hm08_map=nm + '_hm08_map.npz', hm08_map_sha256=sha(mp), family_map='MF_M_REF_RP3_retopo_v005_hm08_map.npz (byte-identical)'),
                frame=dict(analysis='cm, x subject left, f forward, u up (R-6)', blender='m, Z up, faces -Y, subject left +X, origin = pelvis root projected to ground', origin_translation_cm=lm['frame']['origin_translation_cm']),
                landmarks=nm.replace('_retopo', '') + '_landmarks.json', readback=dict(max_abs_diff_vs_candidate_m=rb['max_abs_diff_vs_candidate_m'], faces_equal_candidate=rb['faces_equal_candidate'], normals_outward=rb['normals_outward']),
                topology=dict(components=au['components'], boundary_edges=au['boundary_edges'], nonmanifold_edges=au['nonmanifold_edges'], nonmanifold_vertices=au['nonmanifold_vertices'], degenerate_faces=au['degenerate_faces'], self_intersection_face_pairs=au['self_intersection_face_pairs'],
                              density={k: round(v['mean'], 3) for k, v in au['density_pct_of_stature'].items()}),
                validator=dict(authoritative='D1 + D3 + D4 + D5', firm=va['summary']['firm_pass_count'], stations=69, fails=va['summary']['D1_D3_firm_fail'], margin_zero=va['summary']['margin_zero'],
                               proposed_D6_firm=sum(v['firm_D1_D3'] for v in d6['stations'].values())),
                anatomy=dict(T1_T2=an['T1_T2_pass'], T3=an['T3_pass'], T7=an['T7_pass'], stature_cm=an['stature_prod_cm'], stature_diff_mm=an['stature_diff_mm'], iou=an['silhouette_iou'], body=an['deviation_prod_to_source']['body']),
                face=dict(mouth_rings=fr['mouth_rings']['count'], orbit_rings=[fr['orbit_rings_l']['count'], fr['orbit_rings_r']['count']], poles_at_mouth_corners=fr['poles_at_mouth_corners'], poles_within_2cm_of_mouth=fr['poles_within_2cm_of_mouth']),
                contact=dict(classes=ct['classes'], new_hand_foot_defects=ct['new_hand_foot_groin_defects']), identity=dict(holds_all_zones=idn['identity_holds_all_zones']))
    json.dump(side, open('%s/%s.json' % (E, nm), 'w'), indent=1); shutil.copy('%s/lm/%s_fam_landmarks.json' % (W, cid), '%s/%s_landmarks.json' % (E, nm.replace('_retopo', '')))
    man['configurations'][cid] = dict(production=nm + '.blend', sha256=ph['sha256'], geometry_hash=ph['geometry_hash'], sidecar=nm + '.json', sidecar_sha256=sha('%s/%s.json' % (E, nm)), source=side['source'], validator=side['validator'])
json.dump(proof, open(E + '/SAGEKIN_RP3_topology_identity_proof.json', 'w'), indent=1)
json.dump(margin, open(E + '/SAGEKIN_RP3_margin_table.json', 'w'), indent=1)
with open(E + '/SAGEKIN_RP3_margin_table.csv', 'w') as f:
    f.write('station,SG_loops,SG_required,SG_margin,SG_status,SG_D6_loops,SGF178_loops,SGF178_required,SGF178_margin,SGF178_status,SGF178_D6_loops\n')
    for k in sorted(margin['SG']):
        a, b = margin['SG'][k], margin['SGF178'][k]; f.write('%s,%d,%d,%d,%s,%d,%d,%d,%d,%s,%d\n' % (k, a['loops'], a['required'], a['margin'], a['status'], a['proposed_D6']['loops'], b['loops'], b['required'], b['margin'], b['status'], b['proposed_D6']['loops']))
json.dump(dcmp, open(E + '/SAGEKIN_RP3_deformation_comparison.json', 'w'), indent=1)
man['topology_identity_proof'] = {k: dict(face_hash_equal=v['equals_family'], faces_equal=v['faces_equal_family_base'], uv_equal=v['uv_equal_family_base'], map_equal=v['map_arrays_equal'], V_eq_M_hm08=v['V_equals_M_at_race_hm08_max_abs_cm']) for k, v in proof.items()}
json.dump(man, open(E + '/SAGEKIN_RP3_family_propagation_manifest.json', 'w'), indent=1)
# SGF178 central-reference sidecar
rc = json.load(open(W + '/src/SGF178_regen_check.json')); fr_ = json.load(open(W + '/partA/SGF178_full_resolve_identity.json')); pa = json.load(open(W + '/partA/SGF178_reference_validation.json'))
cen = dict(id='SGF178', race='Sagekin', role='configuration-2 CENTRAL REFERENCE CANDIDATE (order c6c7940 Part A: PASS - READY FOR PROPAGATION); not yet author-accepted',
           previous_role='configuration-2 construction base for SGF152-NAT / SGF208 (RM-OT-05A §2; reviews/reference-assets/manifest.json)',
           provenance=dict(built_in='RM-OT-05 §4 / RM-OT-05A (scratch $S/rmot05r/b/SGF178), committed with the reference assets in 7a7b016 (2026-10-19)', builder='tools/rac/w1/build_variant.py (route: height macro re-solved)',
                           base='MF-F-R_build.json (accepted Marchfolk configuration-2 reference)', overrides=json.load(open(RA + '/builds/SGF178_build.json'))['overrides'],
                           note='targets identical to the accepted configuration-1 SG; only the configuration (gender 0) and the stature re-solve differ; SGF152-NAT is built from its height macro, SGF208 by the same route at 208'),
           mpfb='MPFB 2.0.17 / Blender 5.2.2 LTS (tools/rac/w1/arm_lib.py)', cfg=json.load(open(RA + '/builds/SGF178_build.json'))['cfg'], height_macro=json.load(open(RA + '/builds/SGF178_build.json'))['height_macro'],
           pose=json.load(open(RA + '/builds/SGF178_build.json'))['pose'], pose_sequence='build -> ground -> pose_r6 (arm abduction 8 deg, palm twist) -> ground',
           r6='reviews/reference-assets/r6/SGF178_r6.npz', r6_sha256=rc['committed_sha256'], build_sha256=rc['build_sha256'], geometry_hash=rc['committed_geom'], stature_r6_cm=rc['stature_regen'],
           rebuild_identity=dict(regen_py=dict(geometry_identical=rc['geometry_identical'], max_abs_dV_cm=rc['max_abs_dV_cm']), full_height_resolve=dict(geometry_identical=fr_['geometry_identical'], max_abs_dV_cm=fr_['max_abs_dV_cm'], height_macro_equal=fr_['macro_equal'])),
           integrity=pa['integrity']['SGF178'], continuity=pa['continuity_summary'], identity=pa['identity_summary'], partA_verdict='SG CONFIG-2 CENTRAL REFERENCE PASS - READY FOR PROPAGATION')
json.dump(cen, open(E + '/SGF178_central_reference_sidecar.json', 'w'), indent=1); print('manifest written', {k: v for k, v in man['topology_identity_proof'].items()})
