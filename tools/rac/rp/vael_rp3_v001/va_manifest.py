# va_manifest.py WORK EVIDIR : Vael order (2026-10-28) Part A / B records (from ae_manifest.py) -- Vael body-family sidecars + propagation manifest, topology identity proof, VALF178
# central-reference sidecar, native hm08 integrity, deformation comparison against the frozen Marchfolk v005 realization of the same configuration class.
import sys, os, json, shutil, hashlib, numpy as np, scipy.sparse as sp
W, E = sys.argv[1:3]; os.makedirs(E, exist_ok=True); sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest(); jl = lambda p: json.load(open(p))
REPO = '/home/claude/wayfarer-design'; RA = REPO + '/reviews/reference-assets'; B5 = '/mnt/user-data/outputs/rp5'; FACE = 'ec768ae210ea3ee1c053d0c4cd3256d57dad6db35d515502706b74f64281bee0'
csr = lambda z: sp.csr_matrix((z['M_data'], z['M_indices'], z['M_indptr']), shape=tuple(z['M_shape'])); fm = np.load(B5 + '/MF_M_REF_RP3_retopo_v005_hm08_map.npz'); Mf = csr(fm)
fam0 = np.load('/tmp/claude-0/rt/v5/cand/MF-M-R_v005.npz'); PH = {os.path.basename(json.loads(l)['file']): json.loads(l) for l in open(W + '/prod_hashes.jsonl')}
sys.path.insert(0, REPO + '/tools/rac/rp/fenn_rp3_v001'); src = open(REPO + '/tools/rac/rp/fenn_rp3_v001/fenn_partA.py').read()
from collections import Counter
from scipy.spatial import cKDTree
exec(src[src.index('def integrity'):src.index('meas = lambda')])
F5 = REPO + '/reviews/rac-rp3-evidence/mpfb_family_base_v005_freeze/MPFB_FAMILY_BASE_v005_FREEZE.json'
man = dict(record='VAEL RP3 body-family propagation manifest v001 (DIAGNOSTIC body candidates; family human ear, not final Vael ear)', order='reviews/chatgpt-rac-rp3-vael-body-face-ear-order.md (2026-10-28)',
           status='BODY-FAMILY DIAGNOSTIC CANDIDATES - NOT FROZEN', active_family_base=dict(record='MPFB_FAMILY_BASE_v005_FREEZE.json', record_sha256=sha(F5), base_blend_sha256=sha(B5 + '/MF_M_REF_RP3_retopo_v005.blend'),
           hm08_map_sha256=sha(B5 + '/MF_M_REF_RP3_retopo_v005_hm08_map.npz'), face_topology_hash=FACE), validator='D1 + D3 + D4 + D5 + D6 (authoritative)', configurations={}, topology_identity_proof={})
DEF = {}
ENV = os.environ.get; C1, C2 = ENV('VA_C1', 'VAL4'), ENV('VA_C2', 'VALF178'); V_ = ENV('VA_PROD_VER', 'v001')   # body / face source order: VAL4-R1 / VALF178-R1, v002
R1 = C1 != 'VAL4'
if R1:   # body / face source order: provisional VB2g + VC2 sources (VAL4-R1 / VALF178-R1) -> VA_*_REF_RP3_bodyfam_v002
    man['order'] = ENV('VA_ORDER_DOC', 'reviews/chatgpt-rac-rp3-vael-body-face-source-order.md (2026-10-28)')
    man['record'] = ENV('VA_MAN_RECORD', 'VAEL RP3 body + craniofacial source propagation manifest %s (PROVISIONAL source candidates VB2g + VC2; family human ear, not final Vael ear)' % V_)
    man['status'] = 'PROVISIONAL BODY + CRANIOFACIAL SOURCE CANDIDATES - NOT FROZEN'
for cid, nm, mf, role in ((C1, 'VA_M_REF_RP3_bodyfam_' + V_, 'MF-M-R', ('configuration 1 (accepted VAL4, W1n / W1o)' if C1 == 'VAL4' else 'configuration 1 (%s: VAL4 + shared Vael body correction + craniofacial source, body / face source order)' % C1)),
                          (C2, 'VA_F_REF_RP3_bodyfam_' + V_, 'MF-F-R', ('configuration 2 (VALF178 central-reference candidate, Part A)' if C2 == 'VALF178' else 'configuration 2 (%s: VALF178 foundation + the identical Vael body correction + craniofacial source)' % C2))):
    rc = jl('%s/src/%s_regen_check.json' % (W, cid)); cz = np.load('%s/fam/%s_fam.npz' % (W, cid)); nz = np.load('%s/src/%s_native.npz' % (W, cid)); ph = PH[nm + '.blend']
    rb = jl('%s/readback/%s_readback.json' % (W, nm)); va = jl('%s/val/%s_fam_validator_v2_D1-D6.json' % (W, cid)); v45 = jl('%s/val/%s_fam_validator_v2_D4_D5.json' % (W, cid))
    an = jl('%s/anat/%s_fam_anatomy.json' % (W, cid)); au = jl('%s/audit/%s_fam_audit.json' % (W, cid)); fr = jl('%s/audit/%s_fam_face.json' % (W, cid)); ct = jl('%s/contact/%s_contact.json' % (W, cid)); lm = jl('%s/lm/%s_fam_landmarks.json' % (W, cid))
    pr = dict(face_hash_equal=ph['face_topology_hash'] == FACE == rb['face_topology_hash'], faces_equal=bool(np.array_equal(cz['Q'], fam0['Q'])), uv_equal=bool(np.array_equal(cz['UV'], fam0['UV'])),
              map_equal=bool(abs(csr(cz) - Mf).max() == 0), V_eq_M_hm08=float(np.abs(Mf @ nz['V'].astype(float) - cz['V'].astype(float)).max()))
    man['topology_identity_proof'][cid] = pr
    dn = jl('%s/def/deform_%s_native.json' % (W, cid)); dfm = jl('%s/def/deform_%s_fam.json' % (W, cid)); dm = jl(REPO + '/reviews/rac-rp3-evidence/mpfb_family_base_final_toe2/deformation/deform_%s_v005.json' % mf)
    P_ = {p: dict(aelari_family=dfm['poses'][p]['flipped_faces'], aelari_native=dn['poses'][p]['flipped_faces'], marchfolk_v005=dm['poses'][p]['flipped_faces'], selfx_family=dfm['poses'][p]['new_selfx_pairs'], selfx_mf=dm['poses'][p]['new_selfx_pairs']) for p in dfm['poses']}
    DEF[cid] = dict(reference=mf + ' v005', poses=P_, worst_flip_excess=max(v['aelari_family'] - v['marchfolk_v005'] for v in P_.values()), poses_worse_by_more_than_5=[p for p, v in P_.items() if v['aelari_family'] - v['marchfolk_v005'] > 5])
    side = dict(file=nm + '.blend', sha256=ph['sha256'], geometry_hash=ph['geometry_hash'], face_topology_hash=ph['face_topology_hash'], verts=ph['verts'], quads=ph['quads'], race='Vael', configuration=cid, role=role,
                status=('PROVISIONAL BODY + CRANIOFACIAL SOURCE CANDIDATE - NOT FROZEN (carries the family human auricle; the final Vael ear is a later branch)' if R1 else 'BODY-FAMILY DIAGNOSTIC CANDIDATE - NOT FROZEN (carries the family human auricle; the final Vael ear is a later branch)'),
                source=dict(id=cid, r6='reviews/reference-assets/r6/%s_r6.npz' % cid, r6_sha256=rc['committed_sha256'], build_sha256=rc['build_sha256'], regen_geometry_identical=rc['geometry_identical'], regen_max_abs_dV_cm=rc['max_abs_dV_cm']),
                mapping=dict(hm08_map='family map MF_M_REF_RP3_retopo_v005_hm08_map.npz (arrays identical)'), frame=dict(origin_translation_cm=lm['frame']['origin_translation_cm']),
                readback=dict(max_abs_diff_vs_candidate_m=rb['max_abs_diff_vs_candidate_m'], faces_equal_candidate=rb['faces_equal_candidate'], normals_outward=rb['normals_outward']),
                validator=dict(rules='D1 + D3 + D4 + D5 + D6', firm=va['summary']['firm_pass_count'], fails=va['summary']['D1_D3_firm_fail'], margin_zero=va['summary']['margin_zero'], without_D6=v45['summary']['firm_pass_count'],
                               fallback=va['summary']['D1_D3_non_plain'], D5_exclusions={s: v['D5_undefined_sides'] for s, v in va['stations'].items() if v['D5_undefined_sides']}, D6_exclusions={s: v['D6_undefined_sides'] for s, v in va['stations'].items() if v['D6_undefined_sides']}),
                anatomy=dict(T1_T2=an['T1_T2_pass'], T3=an['T3_pass'], T7=an['T7_pass'], iou_min=min(an['silhouette_iou'].values()), body=an['deviation_prod_to_source']['body'], head=an['deviation_prod_to_source']['head'],
                             ears_zone_note='ear zone reported separately: non-final source anatomy (MPFB human auricle) - NOT a final Vael-ear PASS', ears=an['deviation_prod_to_source']['ears']),
                density={k: round(v['mean'], 3) for k, v in au['density_pct_of_stature'].items()}, density_all_pass=all(v['pass_mean'] for v in au['density_pct_of_stature'].values()),
                face=dict(mouth_rings=fr['mouth_rings']['count'], orbit_rings=[fr['orbit_rings_l']['count'], fr['orbit_rings_r']['count']], poles_at_mouth_corners=fr['poles_at_mouth_corners'], mouth_pass=fr['mouth_pass'], orbit_pass=fr['orbit_pass']),
                integrity=dict(components=au['components'], boundary=au['boundary_edges'], nonmanifold=au['nonmanifold_edges'], degenerate=au['degenerate_faces'], outward=au['normals_outward'], self_intersection_pairs=au['self_intersection_face_pairs']),
                contact=ct['classes'], contact_by_zone=ct['by_zone'], deformation=dict(worst_flip_excess_vs_marchfolk_v005=DEF[cid]['worst_flip_excess'], poses_worse_by_more_than_5=DEF[cid]['poses_worse_by_more_than_5']),
                native_integrity=integrity('%s/src/%s_native.npz' % (W, cid)))
    json.dump(side, open('%s/%s.json' % (E, nm), 'w'), indent=1); shutil.copy('%s/lm/%s_fam_landmarks.json' % (W, cid), '%s/%s_landmarks.json' % (E, nm))
    man['configurations'][cid] = dict(production=nm + '.blend', sha256=ph['sha256'], geometry_hash=ph['geometry_hash'], sidecar_sha256=sha('%s/%s.json' % (E, nm)), source=side['source'], validator=side['validator']['firm'])
json.dump(man, open(E + '/VAEL_RP3_bodyfam_propagation_manifest.json', 'w'), indent=1); json.dump(DEF, open(E + '/VAEL_deformation_comparison.json', 'w'), indent=1)
if R1:   # source sidecars for the provisional R1 sources (both configurations): construction, determinism (rebuild under the versioned id), regen identity
    DT = jl(ENV('VA_R1_DET')); EVb = {c: jl(ENV('VA_R1_EVAL_' + c.upper())) for c in ('c1', 'c2')}
    for cfg, cid in (('c1', C1), ('c2', C2)):
        b = jl(RA + '/builds/%s_build.json' % cid); rc = jl(W + '/src/%s_regen_check.json' % cid); x = EVb[cfg]['items'][ENV('VA_R1_TAG', 'VB2gVC2h')]
        cen = dict(id=cid, race='Vael', role='PROVISIONAL Vael configuration-%s source (body / face source order): %s + shared body correction VB2g + craniofacial VC2; ancestry kept unchanged' % (cfg[1], 'VAL4' if cfg == 'c1' else 'VALF178'),
                   construction='tools/rac/w1/build_variant.py: %s + overrides %s (tools/rac/rp/vael_rp3_v001/build_va_r1.sh); stature 178 re-solved' % ('VAL4_build.json' if cfg == 'c1' else 'MF-F-R_build.json (full Vael cfg)', 'c%s_VB2gVC2h.json (evidence vb_vc_definitions/)' % cfg[1]),
                   mpfb='MPFB 2.0.17 / Blender 5.2.2 LTS', cfg=b['cfg'], height_macro=b['height_macro'], pose=b['pose'], stature_r6_cm=b['stature_r6'],
                   r6='reviews/reference-assets/r6/%s_r6.npz' % cid, r6_sha256=sha(RA + '/r6/%s_r6.npz' % cid), build_sha256=sha(RA + '/builds/%s_build.json' % cid), geometry_hash=rc['regen_geom'],
                   rebuild_identity=dict(regen=dict(geometry_identical=rc['geometry_identical'], max_abs_dV_cm=rc['max_abs_dV_cm']), versioned_rebuild_vs_candidate=DT.get(cid, {k: v for k, v in DT.items() if k.startswith(cid)})),
                   identity=dict(canon_holds=x['canon_holds'], canon_of=x['canon_of'], canon_failing=x['canon_failing'], body_systems_material=x['body_systems_material'], face_systems_material=x['face_systems_material'], face_vs_elves_holds=x['face_canon_vs_elves_holds']),
                   ear_limitation='carries the MPFB human auricle; not canonical Vael ear anatomy (ear branch locked, order §19)')
        if '-VD' in cid:   # custom body-deformation order: R1 + the deterministic Vael body field
            vf = b['cfg'].get('vael_field', {})
            cen['role'] = 'PROVISIONAL Vael configuration-%s source (custom body-deformation order): %s + Vael body field %s at magnitude %s; R1 kept unchanged as ancestry' % (cfg[1], cid.rsplit('-', 1)[0], vf.get('spec', {}).get('version'), vf.get('magnitude'))
            cen['construction'] = 'tools/rac/w1/build_variant.py: %s_build.json + overrides {"vael_field": definition + magnitude} (tools/rac/rp/vael_rp3_v001/build_vd.sh), height macro held; field applied by arm_lib.build (tools/rac/w1/vael_body_field.py)' % cid.rsplit('-', 1)[0]
            cen['field_definition_sha256'] = vf.get('spec_sha256'); cen['field_magnitude'] = vf.get('magnitude')
        json.dump(cen, open(E + '/%s_source_sidecar.json' % cid, 'w'), indent=1)
    print(man['topology_identity_proof']); print({c: (d['worst_flip_excess'], d['poses_worse_by_more_than_5']) for c, d in DEF.items()}); sys.exit(0)
b = jl(RA + '/builds/%s_build.json' % C2); rc = jl(W + '/src/%s_regen_check.json' % C2); pa = jl(W + '/partA/VALF178_reference_validation.json')
cen = dict(id=C2, race='Vael', role='configuration-2 CENTRAL REFERENCE CANDIDATE (Vael order 2026-10-28 Part A; pending author acceptance)',
           construction='tools/rac/w1/build_variant.py: base MF-F-R_build.json (accepted human-family configuration-2 route, as MF-F / SGF178 / FNF181 / AELF190-R1) + overrides = exactly the VAL4 targets and bone scales + stature 178 (resolve_stature); cfg identical to VAL4 except gender (and id)',
           mpfb='MPFB 2.0.17 / Blender 5.2.2 LTS', cfg=b['cfg'], height_macro=b['height_macro'], height_solve=b.get('height_solve'), pose=b['pose'], stature_r6_cm=b['stature_r6'],
           r6='reviews/reference-assets/r6/%s_r6.npz' % C2, r6_sha256=sha(RA + '/r6/%s_r6.npz' % C2), build_sha256=sha(RA + '/builds/%s_build.json' % C2), geometry_hash=rc['regen_geom'],
           rebuild_identity=dict(regen=dict(geometry_identical=rc['geometry_identical'], max_abs_dV_cm=rc['max_abs_dV_cm']), second_full_resolve=pa['determinism']),
           envelope=pa['envelope'], identity={c: dict(holds=v['holds'], of=v['of'], failures=[r['key'] for r in v['canon'] if not r['holds']]) for c, v in pa['configs'].items()},
           pelvis={c: [(r['rule'], r['holds_all_t']) for r in v] for c, v in pa['pelvis_skeletal_proxy'].items()}, configuration_consistency={k: v for k, v in pa['configuration_consistency'].items() if k != 'rows'},
           ear_limitation='carries the MPFB human auricle; not canonical Vael ear anatomy (order §13)', existing_local_c2_build='none found (searched /tmp/claude-0/rt and the repository before construction)')
json.dump(cen, open(E + '/%s_central_reference_sidecar.json' % C2, 'w'), indent=1); print(man['topology_identity_proof']); print({c: (d['worst_flip_excess'], d['poses_worse_by_more_than_5']) for c, d in DEF.items()})
