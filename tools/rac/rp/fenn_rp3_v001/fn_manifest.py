# fn_manifest.py WORK EVIDIR : order 57dc328 §18 -- Fenn body-family sidecars, propagation manifest, topology identity proof, FNF181 sidecar, hashes.
import sys, os, json, shutil, hashlib, numpy as np, scipy.sparse as sp
W, E = sys.argv[1:3]; os.makedirs(E, exist_ok=True); sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
REPO = '/home/claude/wayfarer-design'; RA = REPO + '/reviews/reference-assets'; B5 = '/mnt/user-data/outputs/rp5'; FACE = 'ec768ae210ea3ee1c053d0c4cd3256d57dad6db35d515502706b74f64281bee0'
csr = lambda z: sp.csr_matrix((z['M_data'], z['M_indices'], z['M_indptr']), shape=tuple(z['M_shape'])); fm = np.load(B5 + '/MF_M_REF_RP3_retopo_v005_hm08_map.npz'); Mf = csr(fm)
fam0 = np.load('/tmp/claude-0/rt/v5/cand/MF-M-R_v005.npz'); PH = {os.path.basename(json.loads(l)['file']): json.loads(l) for l in open(W + '/prod_hashes.jsonl')}
F5 = REPO + '/reviews/rac-rp3-evidence/mpfb_family_base_v005_freeze/MPFB_FAMILY_BASE_v005_FREEZE.json'
man = dict(record='FENN RP3 body-family propagation manifest v001 (DIAGNOSTIC body candidates; family human ear, not final Fenn ear)', order='reviews/chatgpt-rac-rp3-fenn-body-and-ear-branch-order.md (57dc328)',
           status='BODY-FAMILY DIAGNOSTIC CANDIDATES - NOT FROZEN', active_family_base=dict(record='MPFB_FAMILY_BASE_v005_FREEZE.json', record_sha256=sha(F5), base_blend_sha256=sha(B5 + '/MF_M_REF_RP3_retopo_v005.blend'),
           hm08_map_sha256=sha(B5 + '/MF_M_REF_RP3_retopo_v005_hm08_map.npz'), face_topology_hash=FACE), validator='D1 + D3 + D4 + D5 + D6 (authoritative)', configurations={}, topology_identity_proof={})
for cid, nm, r6, role in (('FNL4', 'FN_M_REF_RP3_bodyfam_v001', RA + '/r6/FNL4_r6.npz', 'configuration 1 (accepted FNL4, W1p)'), ('FNF181', 'FN_F_REF_RP3_bodyfam_v001', RA + '/r6/FNF181_r6.npz', 'configuration 2 (FNF181 central-reference candidate, Part A PASS)')):
    rc = json.load(open('%s/src/%s_regen_check.json' % (W, cid))); cz = np.load('%s/cand/%s_fam.npz' % (W, cid)); nz = np.load('%s/src/%s_native.npz' % (W, cid)); ph = PH[nm + '.blend']
    rb = json.load(open('%s/readback/%s_readback.json' % (W, 'FN_M' if cid == 'FNL4' else 'FN_F'))); mp = '%s/prod/%s_hm08_map.npz' % (W, nm); mz = np.load(mp)
    va = json.load(open('%s/val/%s_fam_validator_v2_D1-D6.json' % (W, cid))); an = json.load(open('%s/anat/%s_fam_anatomy.json' % (W, cid))); au = json.load(open('%s/audit/%s_fam_audit.json' % (W, cid)))
    fr = json.load(open('%s/audit/%s_fam_face.json' % (W, cid))); ct = json.load(open('%s/audit/%s_contact.json' % (W, cid))); lm = json.load(open('%s/lm/%s_fam_landmarks.json' % (W, cid)))
    pr = dict(face_hash_equal=ph['face_topology_hash'] == FACE == rb['face_topology_hash'], faces_equal=bool(np.array_equal(cz['Q'], fam0['Q'])), uv_equal=bool(np.array_equal(cz['UV'], fam0['UV'])),
              map_equal=sha(mp) == sha(B5 + '/MF_M_REF_RP3_retopo_v005_hm08_map.npz') and bool(abs(csr(mz) - Mf).max() == 0), V_eq_M_hm08=float(np.abs(Mf @ nz['V'].astype(float) - cz['V'].astype(float)).max()))
    man['topology_identity_proof'][cid] = pr
    side = dict(file=nm + '.blend', sha256=ph['sha256'], geometry_hash=ph['geometry_hash'], face_topology_hash=ph['face_topology_hash'], verts=ph['verts'], quads=ph['quads'], race='Fenn', configuration=cid, role=role,
                status='BODY-FAMILY DIAGNOSTIC CANDIDATE - NOT FROZEN (carries the family human auricle; the final Fenn ear is a later branch)',
                source=dict(id=cid, r6=os.path.relpath(r6, REPO), r6_sha256=rc['committed_sha256'], build_sha256=rc['build_sha256'], regen_geometry_identical=rc['geometry_identical'], regen_max_abs_dV_cm=rc['max_abs_dV_cm']),
                mapping=dict(hm08_map=nm + '_hm08_map.npz', hm08_map_sha256=sha(mp), family_map='MF_M_REF_RP3_retopo_v005_hm08_map.npz (byte-identical)'), frame=dict(origin_translation_cm=lm['frame']['origin_translation_cm']),
                readback=dict(max_abs_diff_vs_candidate_m=rb['max_abs_diff_vs_candidate_m'], faces_equal_candidate=rb['faces_equal_candidate'], normals_outward=rb['normals_outward']),
                validator=dict(rules='D1 + D3 + D4 + D5 + D6', firm=va['summary']['firm_pass_count'], fails=va['summary']['D1_D3_firm_fail'], margin_zero=va['summary']['margin_zero']),
                anatomy=dict(T1_T2=an['T1_T2_pass'], T3=an['T3_pass'], T7=an['T7_pass'], ears_zone_note='ear zone reported separately: non-final source anatomy (MPFB human auricle)', ears=an['deviation_prod_to_source']['ears']),
                density={k: round(v['mean'], 3) for k, v in au['density_pct_of_stature'].items()}, face=dict(mouth_rings=fr['mouth_rings']['count'], orbit_rings=[fr['orbit_rings_l']['count'], fr['orbit_rings_r']['count']], poles_at_mouth_corners=fr['poles_at_mouth_corners']),
                contact=ct.get('classes_after_reclassification', ct['classes']))
    json.dump(side, open('%s/%s.json' % (E, nm), 'w'), indent=1); shutil.copy('%s/lm/%s_fam_landmarks.json' % (W, cid), '%s/%s_landmarks.json' % (E, nm.replace('_retopo', '')))
    man['configurations'][cid] = dict(production=nm + '.blend', sha256=ph['sha256'], geometry_hash=ph['geometry_hash'], sidecar_sha256=sha('%s/%s.json' % (E, nm)), source=side['source'], validator=side['validator'])
json.dump(man, open(E + '/FENN_RP3_bodyfam_propagation_manifest.json', 'w'), indent=1)
b = json.load(open(RA + '/builds/FNF181_build.json')); rc = json.load(open(W + '/src/FNF181_regen_check.json')); pa = json.load(open(W + '/partA/FNF181_reference_validation.json'))
cen = dict(id='FNF181', race='Fenn', role='configuration-2 CENTRAL REFERENCE CANDIDATE (order 57dc328 Part A: PASS - READY FOR BODY PROPAGATION; pending author acceptance)',
           construction='tools/rac/w1/build_variant.py: base MF-F-R_build.json (accepted human-family configuration-2 architecture) + overrides = exactly the FNL4 targets and bone scales + stature 181 (resolve_stature); cfg identical to FNL4 except gender (and id)',
           mpfb='MPFB 2.0.17 / Blender 5.2.2 LTS', cfg=b['cfg'], height_macro=b['height_macro'], height_solve=b['height_solve'], pose=b['pose'], stature_r6_cm=b['stature_r6'],
           r6='reviews/reference-assets/r6/FNF181_r6.npz', r6_sha256=sha(RA + '/r6/FNF181_r6.npz'), build_sha256=sha(RA + '/builds/FNF181_build.json'), geometry_hash=rc['regen_geom'],
           rebuild_identity=dict(regen=dict(geometry_identical=rc['geometry_identical'], max_abs_dV_cm=rc['max_abs_dV_cm']), second_full_resolve='identical (max |dV| 0, same height macro 0.63916015625)'),
           integrity=pa['integrity']['FNF181'], identity=pa['identity_summary'], pelvis=pa['pelvis_skeletal_proxy']['E_A2'], configuration=pa['configuration_summary'],
           ear_limitation='carries the MPFB human auricle; not canonical Fenn ear anatomy (order 57dc328 §2)')
json.dump(cen, open(E + '/FNF181_central_reference_sidecar.json', 'w'), indent=1); print(man['topology_identity_proof'])
