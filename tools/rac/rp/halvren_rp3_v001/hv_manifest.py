# hv_manifest.py WORK EVIDIR : Halvren central-anchor order (2026-10-29) Part B records (from va_manifest.py) -- Halvren body-family sidecars + propagation
# manifest, topology identity proof (exact v005 topology, V = M @ hm08), HVF178 central-anchor source sidecar, native hm08 integrity, deformation comparison
# against the frozen Marchfolk v005 realization of the same configuration class.
import sys, os, json, shutil, hashlib, numpy as np, scipy.sparse as sp
W, E = sys.argv[1:3]; os.makedirs(E, exist_ok=True); sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest(); jl = lambda p: json.load(open(p))
REPO = '/home/claude/wayfarer-design'; RA = REPO + '/reviews/reference-assets'; B5 = '/mnt/user-data/outputs/rp5'; FACE = 'ec768ae210ea3ee1c053d0c4cd3256d57dad6db35d515502706b74f64281bee0'
csr = lambda z: sp.csr_matrix((z['M_data'], z['M_indices'], z['M_indptr']), shape=tuple(z['M_shape'])); fm = np.load(B5 + '/MF_M_REF_RP3_retopo_v005_hm08_map.npz'); Mf = csr(fm)
fam0 = np.load('/tmp/claude-0/rt/v5/cand/MF-M-R_v005.npz'); PH = {os.path.basename(json.loads(l)['file']): json.loads(l) for l in open(W + '/prod_hashes.jsonl')}
src = open(REPO + '/tools/rac/rp/fenn_rp3_v001/fenn_partA.py').read()
from collections import Counter
from scipy.spatial import cKDTree
exec(src[src.index('def integrity'):src.index('meas = lambda')])
F5 = REPO + '/reviews/rac-rp3-evidence/mpfb_family_base_v005_freeze/MPFB_FAMILY_BASE_v005_FREEZE.json'
man = dict(record='HALVREN RP3 body-family propagation manifest v001 (DIAGNOSTIC central-anchor body candidates; family human ear = non-final Halvren ear anatomy)',
           order='reviews/chatgpt-rac-rp3-halvren-central-anchor-order.md (2026-10-29)', status='BODY-FAMILY DIAGNOSTIC CANDIDATES - NOT FROZEN; technical propagation PASS does not approve Halvren biology',
           active_family_base=dict(record='MPFB_FAMILY_BASE_v005_FREEZE.json', record_sha256=sha(F5), base_blend_sha256=sha(B5 + '/MF_M_REF_RP3_retopo_v005.blend'), hm08_map_sha256=sha(B5 + '/MF_M_REF_RP3_retopo_v005_hm08_map.npz'), face_topology_hash=FACE),
           validator='D1 + D3 + D4 + D5 + D6 (authoritative)', configurations={}, topology_identity_proof={})
DEF = {}
for cid, nm, mf, role in (('HVC1', 'HV_M_REF_RP3_bodyfam_v001', 'MF-M-R', 'configuration 1 (HVC1 accepted W1s diagnostic central anchor)'), ('HVF178', 'HV_F_REF_RP3_bodyfam_v001', 'MF-F-R', 'configuration 2 (HVF178 central-anchor candidate, Part A)')):
    rc = jl('%s/src/%s_regen_check.json' % (W, cid)); cz = np.load('%s/fam/%s_fam.npz' % (W, cid)); nz = np.load('%s/src/%s_native.npz' % (W, cid)); ph = PH[nm + '.blend']
    rb = jl('%s/readback/%s_readback.json' % (W, nm)); va = jl('%s/val/%s_fam_validator_v2_D1-D6.json' % (W, cid)); v45 = jl('%s/val/%s_fam_validator_v2_D4_D5.json' % (W, cid))
    an = jl('%s/anat/%s_fam_anatomy.json' % (W, cid)); au = jl('%s/audit/%s_fam_audit.json' % (W, cid)); fr = jl('%s/audit/%s_fam_face.json' % (W, cid)); ct = jl('%s/contact/%s_contact.json' % (W, cid)); lm = jl('%s/lm/%s_fam_landmarks.json' % (W, cid))
    pr = dict(face_hash_equal=ph['face_topology_hash'] == FACE == rb['face_topology_hash'], faces_equal=bool(np.array_equal(cz['Q'], fam0['Q'])), uv_equal=bool(np.array_equal(cz['UV'], fam0['UV'])),
              map_equal=bool(abs(csr(cz) - Mf).max() == 0), V_eq_M_hm08_max_abs_cm=float(np.abs(Mf @ nz['V'].astype(float) - cz['V'].astype(float)).max()), quads_pct=au['quads_pct'])
    man['topology_identity_proof'][cid] = pr
    dn = jl('%s/def/deform_%s_native.json' % (W, cid)); dfm = jl('%s/def/deform_%s_fam.json' % (W, cid)); dm = jl(REPO + '/reviews/rac-rp3-evidence/mpfb_family_base_final_toe2/deformation/deform_%s_v005.json' % mf)
    P_ = {p: dict(halvren_family=dfm['poses'][p]['flipped_faces'], halvren_native=dn['poses'][p]['flipped_faces'], marchfolk_v005=dm['poses'][p]['flipped_faces'], selfx_family=dfm['poses'][p]['new_selfx_pairs'], selfx_mf=dm['poses'][p]['new_selfx_pairs'],
                  folds_family=dfm['poses'][p]['new_folds'], folds_mf=dm['poses'][p]['new_folds']) for p in dfm['poses']}
    DEF[cid] = dict(reference=mf + ' v005', poses=P_, worst_flip_excess=max(v['halvren_family'] - v['marchfolk_v005'] for v in P_.values()), poses_worse_by_more_than_5=[p for p, v in P_.items() if v['halvren_family'] - v['marchfolk_v005'] > 5],
                    worst_selfx_excess=max(v['selfx_family'] - v['selfx_mf'] for v in P_.values()))
    side = dict(file=nm + '.blend', sha256=ph['sha256'], geometry_hash=ph['geometry_hash'], face_topology_hash=ph['face_topology_hash'], verts=ph['verts'], quads=ph['quads'], race='Halvren', configuration=cid, role=role,
                status='BODY-FAMILY DIAGNOSTIC CANDIDATE - NOT FROZEN (carries the family human auricle = non-final Halvren ear anatomy; technical PASS does not approve Halvren biology)',
                source=dict(id=cid, r6='reviews/reference-assets/r6/%s_r6.npz' % cid, r6_sha256=rc['committed_sha256'], build_sha256=rc['build_sha256'], regen_geometry_identical=rc['geometry_identical'], regen_max_abs_dV_cm=rc['max_abs_dV_cm']),
                mapping=dict(hm08_map='family map MF_M_REF_RP3_retopo_v005_hm08_map.npz (arrays identical)'), frame=dict(origin_translation_cm=lm['frame']['origin_translation_cm']),
                readback=dict(max_abs_diff_vs_candidate_m=rb['max_abs_diff_vs_candidate_m'], faces_equal_candidate=rb['faces_equal_candidate'], normals_outward=rb['normals_outward']),
                validator=dict(rules='D1 + D3 + D4 + D5 + D6', firm=va['summary']['firm_pass_count'], stations=va['summary']['stations'], fails=va['summary']['D1_D3_firm_fail'], margin_zero=va['summary']['margin_zero'], without_D6=v45['summary']['firm_pass_count'],
                               fallback=va['summary']['D1_D3_non_plain'], D5_exclusions={s: v['D5_undefined_sides'] for s, v in va['stations'].items() if v['D5_undefined_sides']}, D6_exclusions={s: v['D6_undefined_sides'] for s, v in va['stations'].items() if v['D6_undefined_sides']}),
                anatomy=dict(T1_T2=an['T1_T2_pass'], T3=an['T3_pass'], T7=an['T7_pass'], iou_min=min(an['silhouette_iou'].values()), stature_diff_mm=an['stature_diff_mm'], body=an['deviation_prod_to_source']['body'], head=an['deviation_prod_to_source']['head'],
                             ears_zone_note='ear zone reported separately: non-final source anatomy (MPFB human auricle) - NOT a Halvren-ear PASS', ears=an['deviation_prod_to_source']['ears']),
                density={k: round(v['mean'], 3) for k, v in au['density_pct_of_stature'].items()}, density_all_pass=all(v['pass_mean'] for v in au['density_pct_of_stature'].values()),
                face=dict(mouth_rings=fr['mouth_rings']['count'], orbit_rings=[fr['orbit_rings_l']['count'], fr['orbit_rings_r']['count']], poles_at_mouth_corners=fr['poles_at_mouth_corners'], poles_within_2cm_of_mouth=fr['poles_within_2cm_of_mouth'],
                          poles_within_2cm_of_eyes=[fr['poles_within_2cm_of_eye_l'], fr['poles_within_2cm_of_eye_r']], mouth_pass=fr['mouth_pass'], orbit_pass=fr['orbit_pass'], face_density_pct=au['density_pct_of_stature']['face']['mean']),
                integrity=dict(components=au['components'], boundary=au['boundary_edges'], nonmanifold=au['nonmanifold_edges'], nonmanifold_vertices=au['nonmanifold_vertices'], degenerate=au['degenerate_faces'], coincident=au['coincident_vertex_pairs'],
                               outward=au['normals_outward'], winding=au['winding_consistent'], self_intersection_pairs=au['self_intersection_face_pairs']),
                contact=ct['classes'], contact_by_zone=ct['by_zone'], deformation=dict(worst_flip_excess_vs_marchfolk_v005=DEF[cid]['worst_flip_excess'], poses_worse_by_more_than_5=DEF[cid]['poses_worse_by_more_than_5'], worst_selfx_excess=DEF[cid]['worst_selfx_excess']),
                native_integrity=integrity('%s/src/%s_native.npz' % (W, cid)))
    json.dump(side, open('%s/%s.json' % (E, nm), 'w'), indent=1); shutil.copy('%s/lm/%s_fam_landmarks.json' % (W, cid), '%s/%s_landmarks.json' % (E, nm))
    man['configurations'][cid] = dict(production=nm + '.blend', sha256=ph['sha256'], geometry_hash=ph['geometry_hash'], sidecar_sha256=sha('%s/%s.json' % (E, nm)), source=side['source'], validator=side['validator']['firm'])
json.dump(man, open(E + '/HALVREN_RP3_bodyfam_propagation_manifest.json', 'w'), indent=1); json.dump(DEF, open(E + '/HALVREN_deformation_comparison.json', 'w'), indent=1)
b = jl(RA + '/builds/HVF178_build.json'); rc = jl(W + '/src/HVF178_regen_check.json'); pa = jl(W + '/partA/HV_partA.json')
cen = dict(id='HVF178', race='Halvren', role='configuration-2 CENTRAL MIXED-EXPRESSION ANCHOR CANDIDATE (Halvren central-anchor order 2026-10-29 Part A; pending author acceptance); not a separate ancestry phenotype',
           construction='tools/rac/w1/build_variant.py: base MF-F-R_build.json (accepted human-family configuration-2 route, as MF-F / SGF178 / VALF178) + overrides = exactly the HVC1 body targets + stature 178 (resolve_stature); cfg identical to HVC1 except gender (and id); no c2-specific Halvren package',
           mpfb='MPFB 2.0.17 / Blender 5.2.2 LTS', cfg=b['cfg'], height_macro=b['height_macro'], height_solve=b.get('height_solve'), pose=b['pose'], stature_r6_cm=b['stature_r6'],
           r6='reviews/reference-assets/r6/HVF178_r6.npz', r6_sha256=sha(RA + '/r6/HVF178_r6.npz'), build_sha256=sha(RA + '/builds/HVF178_build.json'), geometry_hash=rc['regen_geom'],
           rebuild_identity=dict(regen=dict(geometry_identical=rc['geometry_identical'], max_abs_dV_cm=rc['max_abs_dV_cm']), second_full_resolve=pa['determinism']),
           envelope=pa['envelope'], configuration_consistency={k: v for k, v in pa['configuration_consistency'].items() if k != 'rows'},
           ear_limitation='carries the MPFB human auricle; not Halvren ear anatomy (order §6)', existing_local_c2_build='none found (order §3; no HVF* record in reviews/reference-assets before construction)')
json.dump(cen, open(E + '/HVF178_central_anchor_sidecar.json', 'w'), indent=1); print(man['topology_identity_proof']); print({c: (d['worst_flip_excess'], d['poses_worse_by_more_than_5'], d['worst_selfx_excess']) for c, d in DEF.items()})
