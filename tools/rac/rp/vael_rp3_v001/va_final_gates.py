# va_final_gates.py WORK OUT_DIR : Vael final consolidation / freeze order §4-§20 -- one record of every final gate for the two Vael RP3 production bodies,
# from the clean-rebuild folder (run_vafinal.sh + run_vafinal_eval.sh + run_vafinal_prod.sh). Writes VAEL_FINAL_gates.json and VAEL_FINAL_deformation_summary.json.
# Reviewed references: VF2 family realization / validator (/tmp/claude-0/rt/vf/prod = VA_{M,F}_REF_RP3_bodyfam_v004), reviewed RI3 candidate
# (/tmp/claude-0/rt/va/ri_final/RI3, commit f25b345), committed evidence of the elf-frame gate (VF_candidate_eval / VF_pelvis_VF2 / VF_hidden_ear_identity /
# VF_expression_sanity) and of the root-integration gate.
import sys, os, json, glob, hashlib, numpy as np
os.environ.setdefault('EAR_TOPO', 'v002')
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001')
import ear_branch_lib as E
W, O = sys.argv[1:3]; os.makedirs(O, exist_ok=True); jl = lambda p: json.load(open(p)); sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
REPO = '/home/claude/wayfarer-design'; RA = REPO + '/reviews/reference-assets'; EVF = REPO + '/reviews/rac-rp3-evidence/vael_rp3_elf_frame'; EVR = REPO + '/reviews/rac-rp3-evidence/vael_rp3_ear_root_integration'
MFD = REPO + '/reviews/rac-rp3-evidence/mpfb_family_base_final_toe2/deformation'; REVF = '/tmp/claude-0/rt/vf/prod'; REVR = '/tmp/claude-0/rt/va/ri_final/RI3'; CAN = 'VA-E2-RI3'; EW = W + '/ear/RI3'
CFG = {'c1': ('VAL4-R1-VD2-VF2', 'VA_M_REF_RP3_v001', 'MF-M-R'), 'c2': ('VALF178-R1-VD2-VF2', 'VA_F_REF_RP3_v001', 'MF-F-R')}
ACC = dict(face_topology_sha256='f8367ab09385d218559b6d3cac52ed159a9249cf12d91807e93e3b095d9ac297', map_sha256='ad312c8028642f6a0f4df4d6b307ec5db23c589b19a6f9b88503832d79e3bdbb',
           canon_sha256='1a0b070b42e84846d1b7beebfd153fec8d1ddf4e5a1d2ecc54a0d4351549a779',
           r6={'VAL4-R1-VD2-VF2': 'fec300953b2306c326e738c0606a9d7218668592d12d616324a7b78c8a0f8fd0', 'VALF178-R1-VD2-VF2': 'c338d97240c29129fef85578818eba84f632f99918fc9ed6861325937444e1e8'},
           build={'VAL4-R1-VD2-VF2': '32fd7ffa80519380caf94b94eca91174be97476f585ee3c9a654242047f6d470', 'VALF178-R1-VD2-VF2': '0e32948a4c9fc3f648602a07f28983456b462669693c5fbe08740bf69ebd6aa1'},
           geometry={'VAL4-R1-VD2-VF2': 'a800b533b3f847af599a99a358cf1339968eec4d21af2497b4fa02bfe5a6be77', 'VALF178-R1-VD2-VF2': '1db646d28f0eb625e2dd501b58374edb9a3adbfdbbbd3816b27ae52a29ff75ad'})
G = dict(order='reviews/chatgpt-rac-rp3-vael-final-consolidation-freeze-order.md (2026-10-28, db01617)', work=W, configurations={}); DS = {}
PEL = jl(W + '/gates/VA_final_pelvis.json'); PELR = jl(EVF + '/VF_pelvis_VF2.json'); HE = jl(W + '/he/VA_hidden_ear_identity_final.json'); HER = jl(EVF + '/VF_hidden_ear_identity.json')
EX = jl(W + '/gates/VA_final_expression_sanity.json'); EXR = jl(EVF + '/VF_expression_sanity.json')
LOC = jl(W + '/anat/VAEL_unmasked_anatomy_localisation.json')
Lo = E.canonical_layout(); ns = len(Lo['st']); SHEET = np.isin(Lo['part'][:ns], ['front', 'back', 'rim']); J = np.asarray(Lo['J'])
def ear_meas(build_npz, meas_json):
    z = np.load(build_npz); rec = jl(build_npz.replace('.npz', '.json')); m = jl(meas_json); s = m['sides']; HH = m['head_HH_cm']; av = lambda x: float(np.mean([s[q][x] for q in ('l', 'r')])); L = av('length_lobe_to_tip_cm'); st = []
    for sd in ('l', 'r'):
        f0 = np.nonzero(z['side'] == sd)[0][0]; X = z['V'][f0:f0 + ns]; fr = rec['sides'][sd]['frame']; Ov, n, b, u = [np.array(fr[k]) for k in ('O', 'n', 'b', 'u')]
        bu = np.c_[(X - Ov) @ b, (X - Ov) @ u]; free = SHEET & (E._inside_dist(bu[J], bu) < 0); lat = (X - Ov) @ n; st.append((lat[free].mean(), np.median(lat[free]), lat[SHEET].max()))
    st = np.mean(st, 0)
    return dict(length_over_HH=L / HH, body_angle_deg=av('auricle_body_angle_deg'), max_width_over_length=av('max_width_cm') / L, max_width_over_HH=av('max_width_cm') / HH, side_view_chord_deg=av('side_view_chord_lobe_to_tip_deg'),
                upper_extension_axis_deg=av('side_view_upper_extension_deg'), tip_above_root_over_HH=av('tip_above_root_cm') / HH, tip_angle_deg=av('tip_in_plane_angle_deg_at_1cm'),
                free_standoff_mean_over_HH=st[0] / HH, free_standoff_median_over_HH=st[1] / HH, tip_standoff_over_HH=st[2] / HH)
FROZEN = {'Fenn E2': {'c1': '/tmp/claude-0/rt/fn/final/ear/%s/FNL4-CF2_E2_%s', 'c2': '/tmp/claude-0/rt/fn/final/ear/%s/FNF181-CF2_E2_%s'},
          'Aelari AE-E2': {'c1': '/tmp/claude-0/rt/ae/final/ear/%s/AEL1-R1_AE-E2_%s', 'c2': '/tmp/claude-0/rt/ae/final/ear/%s/AELF190-R1_AE-E2_%s'}}
for c, (h, nm, mf) in CFG.items():
    g = {}; P = np.load('%s/build/%s_%s_branch.npz' % (EW, h, CAN)); F = np.load('%s/fam/%s_fam.npz' % (W, h)); bj = jl('%s/build/%s_%s_branch.json' % (EW, h, CAN))
    R2 = np.load('%s/build/%s_%s_branch.npz' % (REVR, h, CAN)); rbj = jl('%s/build/%s_%s_branch.json' % (REVR, h, CAN))
    v_ = P['v005_to_branch']; ok_ = (v_ >= 0); ok_[ok_] = P['part'][v_[ok_]] == 'v005'
    rc = jl('%s/src/%s_regen_check.json' % (W, h)); full = np.load('%s/full/%s_r6.npz' % (W, h)); com = np.load('%s/r6/%s_r6.npz' % (RA, h))
    mfull = jl('%s/full/%s_meas.json' % (W, h)); mcom = jl('%s/builds/%s_meas.json' % (RA, h))
    g['rebuild'] = dict(committed_r6_sha256=sha('%s/r6/%s_r6.npz' % (RA, h)), committed_r6_equals_accepted=sha('%s/r6/%s_r6.npz' % (RA, h)) == ACC['r6'][h],
                        build_sha256=sha('%s/builds/%s_build.json' % (RA, h)), build_equals_accepted=sha('%s/builds/%s_build.json' % (RA, h)) == ACC['build'][h],
                        regen_geometry_identical=rc['geometry_identical'], regen_max_abs_dV_cm=rc['max_abs_dV_cm'], regen_geometry_hash=rc['regen_geom'], committed_geometry_hash=rc['committed_geom'],
                        geometry_hash_equals_accepted=rc['regen_geom'] == rc['committed_geom'] == ACC['geometry'][h],
                        full_record_rebuild_max_abs_dV_cm=float(np.abs(full['V'].astype(float) - com['V'].astype(float)).max()), full_record_faces_identical=bool(np.array_equal(full['F'], com['F'])),
                        full_record_meas_equals_committed=bool(mfull['combined'] == mcom['combined']),
                        family_realization_sha256=sha('%s/fam/%s_fam.npz' % (W, h)), family_equals_reviewed_bodyfam_v004=bool(sha('%s/fam/%s_fam.npz' % (W, h)) == sha('%s/fam/%s_fam.npz' % (REVF, h))),
                        branch_arrays_equal_reviewed_RI3=bool(all(np.array_equal(P[k], R2[k]) for k in P.files)), branch_max_abs_diff_vs_reviewed_cm=float(np.abs(P['V'].astype(float) - R2['V'].astype(float)).max()),
                        params_equal_reviewed=bj['params'] == rbj['params'], geo_equal_reviewed=bj['geo'] == rbj['geo'], params=bj['params'], geo=bj['geo'],
                        face_topology_sha256=hashlib.sha256(np.asarray(P['Q']).astype(np.int32).tobytes()).hexdigest(),
                        cuff_canon_sha256=sha(EW + '/canon_branch_topology.json'), cuff_canon_equals_accepted=sha(EW + '/canon_branch_topology.json') == ACC['canon_sha256'],
                        outside_branch_equals_family=bool(np.array_equal(P['V'][P['v005_to_branch'][ok_]], F['V'][ok_])), transition_ring_vertices=int((P['part'] == 'transition').sum()))
    g['rebuild']['face_topology_equals_accepted'] = g['rebuild']['face_topology_sha256'] == ACC['face_topology_sha256']
    g['production'] = dict(sidecar=jl('%s/prod/%s.json' % (W, nm)), readback_local=jl('%s/readback_local/%s_readback.json' % (W, nm)))
    au = jl('%s/audit/%s_final_audit.json' % (W, h)); af = jl('%s/audit/%s_fam_audit.json' % (W, h)); ea = jl('%s/audit/%s_%s_audit.json' % (EW, h, CAN))
    v2b = P['v005_to_branch']; Qf = np.asarray(F['Q']); key = {tuple(sorted(v2b[q])): i for i, q in enumerate(Qf) if (v2b[q] >= 0).all()}
    SIp = np.load('%s/audit/%s_final_loops.npz' % (W, h), allow_pickle=True)['SI']; SIf = np.load('%s/audit/%s_fam_loops.npz' % (W, h), allow_pickle=True)['SI']; Qp = np.asarray(P['Q'])
    mp = lambda f: key.get(tuple(sorted(Qp[f])), -1); sp_ = {tuple(sorted((mp(a), mp(b)))) for a, b in SIp}; sf = {tuple(sorted(map(int, p))) for p in SIf}
    ct = jl('%s/contact/%s_contact.json' % (W, h))
    g['integrity'] = dict(verts=int(len(P['V'])), quads=int(len(P['Q'])), quads_pct=au['quads_pct'], components=au['components'], boundary_edges=au['boundary_edges'], nonmanifold_edges=au['nonmanifold_edges'],
                          nonmanifold_vertices=au['nonmanifold_vertices'], degenerate_faces=au['degenerate_faces'], winding_consistent=au['winding_consistent'], normals_outward=au['normals_outward'],
                          coincident_vertex_pairs=au['coincident_vertex_pairs'], family_coincident_vertex_pairs=af['coincident_vertex_pairs'], self_intersection_pairs=au['self_intersection_face_pairs'],
                          family_self_intersection_pairs=af['self_intersection_face_pairs'], contact_pairs_equal_family_set=bool(sp_ == sf), contact_pairs_on_branch_faces=int(sum(1 for a, b in sp_ if a < 0 or b < 0)),
                          family_contact_class=dict(source=ct['classes']['source'], family=ct['classes']['family'], new=ct['classes']['new']),
                          branch_self_intersections=ea['self_intersection_pairs_touching_branch'], root_valence=ea['root_valence'], root_valence_4=all(v.get('4', 0) == 52 for v in ea['root_valence'].values()),
                          root_seam_float_burial=dict(boundary=ea['boundary_edges'], clearance_min_cm=ea['ear_to_head_clearance']['min_cm'], root_deviation=ea['root_deviation']),
                          transition_displacement_max_cm=ea['transition_ring']['displacement_max_cm'])
    va = jl('%s/val/%s_final_validator_v2_D1-D6.json' % (W, h)); vf = jl('%s/val/%s_fam_validator_v2_D1-D6.json' % (W, h)); vr = jl('%s/val/%s_fam_validator_v2_D1-D6.json' % (REVF, h))
    same = [s for s in va['stations'] if all(va['stations'][s][k] == vf['stations'][s][k] for k in ('loops_v2', 'margin', 'valid_sides', 'D5_undefined_sides', 'D6_undefined_sides'))]
    lab = {s: [vf['stations'][s]['status_D1_D3'], va['stations'][s]['status_D1_D3']] for s in va['stations'] if va['stations'][s]['status_D1_D3'] != vf['stations'][s]['status_D1_D3']}
    g['validator'] = dict(rules='D1 + D3 + D4 + D5 + D6 (validator_v2.py --scale-ref 173.143 --d5 --d6-native)', firm=va['summary']['firm_pass_count'], stations=va['summary']['stations'], firm_fail=va['summary']['D1_D3_firm_fail'],
                          margin_zero=va['summary']['margin_zero'], family_firm=vf['summary']['firm_pass_count'], stations_identical_to_family=len(same), status_label_differences_vs_family=lab,
                          D5_exclusions={s: v['D5_undefined_sides'] for s, v in va['stations'].items() if v['D5_undefined_sides']}, D6_exclusions={s: v['D6_undefined_sides'] for s, v in va['stations'].items() if v['D6_undefined_sides']},
                          family_equals_reviewed_v004=bool(vf['stations'] == vr['stations']))
    an = jl('%s/anat/%s_final_anatomy_earexcl.json' % (W, h)); a0 = jl('%s/anat/%s_final_anatomy.json' % (W, h)); fa = jl('%s/anat/%s_fam_anatomy.json' % (W, h))
    unm_fail = [k for k in ('T1_T2_pass', 'T3_pass', 'T7_pass') if not a0[k]]
    unm_zones = sorted({z for d in ('deviation_prod_to_source', 'deviation_source_to_prod') for z, v in a0[d].items() if z != 'ears' and any(v[k] > lim[k] for lim in [dict(median_mm=0.5, p95_mm=1.5, max_mm=3.0) if z == 'body' else dict(median_mm=0.3, p95_mm=0.8, max_mm=1.5)] for k in lim)})
    g['anatomy'] = dict(final_ear_excluded=dict(T1=an['T1_pass'], T2=an['T2_pass'], T3=an['T3_pass'], T7=an['T7_pass'], stature_diff_mm=an['stature_diff_mm'], bbox_diff_mm=an['bbox_diff_mm'], iou=an['silhouette_iou'],
                                               prod_to_source=an['deviation_prod_to_source'], source_to_prod=an['deviation_source_to_prod']),
                        final_unmasked_anatomy_py=dict(T1_T2=a0['T1_T2_pass'], T3=a0['T3_pass'], T7=a0['T7_pass'], iou=a0['silhouette_iou'], failing=unm_fail, zones_over_limit_excluding_ears=unm_zones,
                                                       ears_prod_to_source=a0['deviation_prod_to_source']['ears'], body=a0['deviation_prod_to_source']['body'], head=a0['deviation_prod_to_source']['head'],
                                                       localisation=LOC[h], localised_within_T1_outside_ear=LOC[h]['within_T1_body_limits_outside_ear'],
                                                       classification='expected source-vs-new-ear divergence localised to the ear (R-6 source carries the MPFB human auricle; production carries VA-E2-RI3)' if unm_fail else 'none'),
                        family_anatomy_py=dict(T1_T2=fa['T1_T2_pass'], T3=fa['T3_pass'], T7=fa['T7_pass']))
    ev = jl('%s/gates/VA_final_eval_%s.json' % (W, c))['items']['VF2']; er = jl('%s/VF_candidate_eval_%s.json' % (EVF, c))['items']['VF2']
    KE = ('canon_holds', 'canon_of', 'canon_failing', 'body_systems_material', 'body_systems_strong', 'face_systems_material', 'face_canon_vs_elves_holds', 'face_desc', 'stature')
    g['vael_canon_firewalls'] = dict(canon='%d / %d' % (ev['canon_holds'], ev['canon_of']), canon_failing=ev['canon_failing'], body_systems_material_vs_humans='%d / 8' % ev['body_systems_material'],
                                     body_systems=ev['body_systems'], face_systems_material='%d / 6' % ev['face_systems_material'], elf_face_rows='%s / %d' % (ev['face_canon_vs_elves_holds'], len(ev['face_canon_vs_elves'])),
                                     equals_accepted_VF2=bool(all(ev[k] == er[k] for k in KE)), canon_rows=ev['canon'])
    he = HE['configs'][c]; her = HER['configs'][c]
    g['hidden_ear'] = dict(body_regions={r: v for r, v in he['body'].items()}, face_systems_material=he['systems_material'], face_systems_direction_ok=he['systems_direction_ok'], of=he['of'], guards=he['guards'],
                           equals_accepted_VF2=bool(he['body'] == her['body'] and he['face'] == her['face'] and he['systems'] == her['systems'] and he['canon_descriptors'] == her['canon_descriptors']))
    g['pelvis'] = dict(summary=PEL['summary'][c], rules=PEL['rules'][c], equals_accepted_VF2=bool(PEL['rules'][c] == PELR['rules'][c]), gating='%d / %d' % (PEL['summary'][c]['gating_hold'], PEL['summary'][c]['gating_of']))
    fr = jl('%s/audit/%s_final_face.json' % (W, h)); ff = jl('%s/audit/%s_fam_face.json' % (W, h))
    KF = ('poles_at_mouth_corners', 'poles_within_2cm_of_mouth', 'poles_within_2cm_of_eye_l', 'poles_within_2cm_of_eye_r', 'mouth_pass', 'orbit_pass')
    g['face'] = dict(mouth_rings=fr['mouth_rings']['count'], orbit_rings=[fr['orbit_rings_l']['count'], fr['orbit_rings_r']['count']], poles_at_mouth_corners=fr['poles_at_mouth_corners'], poles_within_2cm_of_mouth=fr['poles_within_2cm_of_mouth'],
                     poles_within_2cm_of_eyes=[fr['poles_within_2cm_of_eye_l'], fr['poles_within_2cm_of_eye_r']], mouth_pass=fr['mouth_pass'], orbit_pass=fr['orbit_pass'], face_density_pct=au['density_pct_of_stature']['face'],
                     equals_family=bool(all(fr[k] == ff[k] for k in KF) and fr['mouth_rings']['count'] == ff['mouth_rings']['count'] and fr['orbit_rings_l']['count'] == ff['orbit_rings_l']['count'] and fr['orbit_rings_r']['count'] == ff['orbit_rings_r']['count']),
                     expressions=EX['bodies'][h], expressions_equal_accepted_VF2=bool(EX['bodies'][h] == EXR['bodies'][h]))
    em = jl('%s/meas/%s_%s_measure.json' % (EW, h, CAN)); em0 = jl('%s/meas/%s_%s_measure.json' % (REVR, h, CAN)); ed = jl('%s/deform/%s_%s_deform.json' % (EW, h, CAN))
    g['ear'] = dict(topology='VAEL_EAR_BRANCH_TOPOLOGY_v002', T4=ea['T4']['angle_violations'], branch_faces=ea['T4']['branch_faces'], T4_by_part=ea['T4']['angle_violations_by_part'], aspect_max=ea['T4']['aspect_max'],
                    aspect_gt10=ea['T4']['aspect_gt10'], min_angle=ea['T4']['min_angle'], density=ea['density'], root_dihedral=ea['root_dihedral'], transition=ea['transition_ring'], root_deviation=ea['root_deviation'],
                    clearance=ea['ear_to_head_clearance'], outside_branch_byte_identical=ea['outside_branch_byte_identical'], measures_equal_reviewed=bool(em == em0), HH_cm=bj['HH_cm'],
                    guard_iterations=len(jl('%s/build/%s_%s_deform_guard_log.json' % (EW, h, CAN))), deform={p: [v['new_selfx_pairs_touching_branch'], v['flipped_branch_faces'], v['root_band_inverted']] for p, v in ed['poses'].items()},
                    cuff_skin=bj['fairing'].get('cuff_skin'))
    rs = jl(EVR + '/VAEL_EAR_root_integration_summary.json')['alternatives']['RI3 %s' % c]
    g['root_integration'] = dict(audit_equals_reviewed=bool(ea['T4'] == jl('%s/audit/%s_%s_audit.json' % (REVR, h, CAN))['T4'] and ea['root_deviation'] == jl('%s/audit/%s_%s_audit.json' % (REVR, h, CAN))['root_deviation']),
                                 reviewed_root_concha=rs['root_concha'], reviewed_T4=rs['T4'], reviewed_min_angle=rs['min_angle'],
                                 read='one continuous auricle -- final arrays identical to the reviewed RI3 (neutral clay / sections / overlay re-rendered from the final build in the freeze package)')
    g['density'] = dict(zones={k: dict(mean=v['mean'], limit=v['limit'], pass_=v['pass_mean']) for k, v in au['density_pct_of_stature'].items()}, all_pass=all(v['pass_mean'] for v in au['density_pct_of_stature'].values()),
                        ear_branch_mean_pct=ea['density']['branch_mean_edge_pct_stature'], ear_branch_p95_pct=ea['density']['p95_pct'], ear_branch_pass=ea['density']['branch_mean_edge_pct_stature'] <= 0.25,
                        zones_differing_from_family=[k for k in au['density_pct_of_stature'] if au['density_pct_of_stature'][k] != af['density_pct_of_stature'][k]])
    dn = jl('%s/def/deform_%s_native.json' % (W, h)); dfm = jl('%s/def/deform_%s_fam.json' % (W, h)); dp = jl('%s/def/deform_%s_final.json' % (W, h)); dm = jl('%s/deform_%s_v005.json' % (MFD, mf))
    dr = jl('%s/def/deform_%s_fam.json' % (REVF, h)); P_ = {}
    for p in dp['poses']:
        P_[p] = dict(final_flipped=dp['poses'][p]['flipped_faces'], family_flipped=dfm['poses'][p]['flipped_faces'], native_flipped=dn['poses'][p]['flipped_faces'], marchfolk_v005_flipped=dm['poses'][p]['flipped_faces'],
                     final_new_selfx=dp['poses'][p]['new_selfx_pairs'], family_new_selfx=dfm['poses'][p]['new_selfx_pairs'], marchfolk_new_selfx=dm['poses'][p]['new_selfx_pairs'], final_new_folds=dp['poses'][p]['new_folds'], family_new_folds=dfm['poses'][p]['new_folds'])
    over = {p: v['final_flipped'] - v['marchfolk_v005_flipped'] for p, v in P_.items() if v['final_flipped'] - v['marchfolk_v005_flipped'] > 5}
    DS[c] = dict(head=h, reference_marchfolk=mf + ' v005', poses=P_, final_minus_family_flipped_max=max(v['final_flipped'] - v['family_flipped'] for v in P_.values()),
                 final_minus_family_selfx_max=max(v['final_new_selfx'] - v['family_new_selfx'] for v in P_.values()), final_minus_marchfolk_flipped_max=max(v['final_flipped'] - v['marchfolk_v005_flipped'] for v in P_.values()),
                 poses_worse_than_family=[p for p, v in P_.items() if v['final_flipped'] > v['family_flipped'] or v['final_new_selfx'] > v['family_new_selfx'] or v['final_new_folds'] > v['family_new_folds']],
                 family_equals_reviewed_v004={p: dfm['poses'][p]['flipped_faces'] == dr['poses'][p]['flipped_faces'] for p in dfm['poses']}, excess_over_marchfolk_gt5=over,
                 carry_forward='VAEL-CF-SHOULDER-1' if c == 'c1' else None,
                 classification='remaining flips / contacts equal the family realization pose by pose (family rig class: source rig + carried MPFB weights, plain LBS); c1 shoulder_flex90 is the registered VAEL-CF-SHOULDER-1')
    worse = {}
    for p in DS[c]['poses_worse_than_family']:
        X = np.load('%s/def/%s_%s_final.npz' % (W, p, h)); fe = X['fold']; Qp_ = np.asarray(P['Q'])
        worse[p] = dict(new_fold_face_pairs=fe.tolist(), parts=[sorted(set(P['part'][Qp_[f]].tolist())) for f in fe.ravel()], sides=[sorted(set(P['side'][Qp_[f]].tolist())) for f in fe.ravel()],
                        edge_lengths_mm=[np.round(10 * np.linalg.norm(P['V'][Qp_[f]] - np.roll(P['V'][Qp_[f]], -1, 0), axis=1), 3).tolist() for f in fe.ravel()])
    rd = '%s/diag_earw/deform_rigidear.json' % W
    if worse and os.path.exists(rd):
        RG = jl(rd)['poses']; worse['diagnostic_rigid_head_ear_weights'] = dict(note='diagnostic only (not production): ear-branch vertices bound 100 % to the head bone; every Standard v1 pose then equals the family realization (folds / flips / contacts)',
                                                                         equals_family_all_poses=all(RG[q]['new_folds'] == dfm['poses'][q]['new_folds'] and RG[q]['flipped_faces'] == dfm['poses'][q]['flipped_faces'] and RG[q]['new_selfx_pairs'] == dfm['poses'][q]['new_selfx_pairs'] for q in RG),
                                                                         per_pose={q: [RG[q]['new_folds'], RG[q]['flipped_faces'], RG[q]['new_selfx_pairs']] for q in RG})
    DS[c]['worse_than_family_detail'] = worse
    g['deformation'] = dict(standard_v1=DS[c], ear_readiness=dict(poses=list(ed['poses']), all_zero=all(v[0] == 0 and v[1] == 0 and v[2] == 0 for v in g['ear']['deform'].values()),
                                                                   clearance_cm={p: v.get('ear_to_nonhead_clearance_cm') for p, v in ed['poses'].items()}))
    if c == 'c1':
        b0 = em['sides']; av0 = lambda s, x: float(np.mean([s[q][x] for q in ('l', 'r')])); Qs = np.asarray(P['Q']); pr = {}
        bv = dict(proj=av0(b0, 'auricle_body_angle_deg'), tilt=av0(b0, 'side_view_chord_lobe_to_tip_deg'), sweep=av0(b0, 'sweep_max_axis_deviation_cm') / av0(b0, 'length_lobe_to_tip_cm'),
                  len=av0(b0, 'length_lobe_to_tip_cm'), tip=av0(b0, 'tip_in_plane_angle_deg_at_1cm'), wb=av0(b0, 'max_width_cm') / av0(b0, 'length_lobe_to_tip_cm'))
        for d in sorted(glob.glob('%s/probe/*/' % EW)):
            n = d.rstrip('/').split('/')[-1]; A = jl(d + 'audit.json'); s = jl(d + 'measure.json')['sides']; zz = np.load(d + '%s_%s_branch.npz' % (h, CAN)); k = n.split('_')[0]
            val = dict(proj=av0(s, 'auricle_body_angle_deg'), tilt=av0(s, 'side_view_chord_lobe_to_tip_deg'), sweep=av0(s, 'sweep_max_axis_deviation_cm') / av0(s, 'length_lobe_to_tip_cm'),
                       len=av0(s, 'length_lobe_to_tip_cm'), tip=av0(s, 'tip_in_plane_angle_deg_at_1cm'), wb=av0(s, 'max_width_cm') / av0(s, 'length_lobe_to_tip_cm'))[k]
            sgn = (-1 if ('_m' in n or 'blunt' in n) else 1) * (-1 if n.startswith('tip') else 1); dv = val - bv[k]
            pr[n] = dict(same_topology=bool(np.array_equal(np.asarray(zz['Q']), Qs)), T4=A['T4']['angle_violations'], aspect_max=A['T4']['aspect_max'], aspect_gt10=A['T4']['aspect_gt10'], min_angle=A['T4']['min_angle'],
                         self_intersection_branch=A['self_intersection_pairs_touching_branch'], boundary=A['boundary_edges'], nonmanifold=A['nonmanifold_edges'],
                         root_valence_ok=all(v.get('4', 0) == 52 for v in A['root_valence'].values()), value=val, base=bv[k], moves_intended=bool(np.sign(dv) == sgn and abs(dv) > 1e-3))
        g['probes'] = dict(rebuilt=pr, all_clean=all(v['same_topology'] and v['self_intersection_branch'] == 0 and v['aspect_gt10'] == 0 and v['root_valence_ok'] and v['moves_intended'] and v['boundary'] == 0 and v['nonmanifold'] == 0 for v in pr.values()),
                           count='%d / %d' % (sum(v['moves_intended'] for v in pr.values()), len(pr)), T4_max=max(v['T4'] for v in pr.values()), aspect_max=max(v['aspect_max'] for v in pr.values()))
    G['configurations'][c] = g
FW = {}
for c, (h, nm, mf) in CFG.items():
    m = {'Vael VA-E2-RI3': ear_meas('%s/build/%s_%s_branch.npz' % (EW, h, CAN), '%s/meas/%s_%s_measure.json' % (EW, h, CAN))}
    for k, pth in FROZEN.items(): m[k] = ear_meas(pth[c] % ('build', 'branch.npz'), pth[c] % ('meas', 'measure.json'))
    v, fn, ae = m['Vael VA-E2-RI3'], m['Fenn E2'], m['Aelari AE-E2']
    chk = {'angular projection Fenn > Vael > Aelari': fn['body_angle_deg'] > v['body_angle_deg'] > ae['body_angle_deg'],
           'Vael broadest base (w/L and w/HH)': v['max_width_over_length'] > max(fn['max_width_over_length'], ae['max_width_over_length']) and v['max_width_over_HH'] > max(fn['max_width_over_HH'], ae['max_width_over_HH']),
           'Vael stronger backward trajectory (chord and upper-extension axis)': v['side_view_chord_deg'] > max(fn['side_view_chord_deg'], ae['side_view_chord_deg']) and v['upper_extension_axis_deg'] > max(fn['upper_extension_axis_deg'], ae['upper_extension_axis_deg']),
           'Vael shorter / blunter taper than Aelari': v['length_over_HH'] < ae['length_over_HH'] and v['tip_angle_deg'] > ae['tip_angle_deg'],
           'Aelari most upward (tip height / HH)': ae['tip_above_root_over_HH'] > max(fn['tip_above_root_over_HH'], v['tip_above_root_over_HH'])}
    resid = dict(mean_over_fenn_HH=v['free_standoff_mean_over_HH'] - fn['free_standoff_mean_over_HH'], median_over_fenn_HH=v['free_standoff_median_over_HH'] - fn['free_standoff_median_over_HH'], tip_over_fenn_HH=v['tip_standoff_over_HH'] - fn['tip_standoff_over_HH'],
                 stand_off_order_fenn_gt_vael_gt_aelari=bool(fn['free_standoff_mean_over_HH'] > v['free_standoff_mean_over_HH'] > ae['free_standoff_mean_over_HH'] and fn['tip_standoff_over_HH'] > v['tip_standoff_over_HH'] > ae['tip_standoff_over_HH']))
    FW[c] = dict(measures=m, checks=chk, standoff_residual=resid)
G['ear_firewall'] = dict(configs=FW, all_hold=all(all(x['checks'].values()) for x in FW.values()),
                         accepted_residual='c1 mean / tip normalised stand-off a few thousandths HH above frozen Fenn (order §2; accepted secondary measurement residual, recorded, not chased)')
json.dump(G, open(os.path.join(O, 'VAEL_FINAL_gates.json'), 'w'), indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
json.dump(DS, open(os.path.join(O, 'VAEL_FINAL_deformation_summary.json'), 'w'), indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
for c, g in G['configurations'].items():
    r = g['rebuild']; print(c, 'rebuild regen', r['regen_geometry_identical'], r['regen_max_abs_dV_cm'], 'full', r['full_record_rebuild_max_abs_dV_cm'], r['full_record_meas_equals_committed'], 'fam=v004', r['family_equals_reviewed_bodyfam_v004'],
          'RI3=rev', r['branch_arrays_equal_reviewed_RI3'], 'topo', r['face_topology_equals_accepted'], 'canon', r['cuff_canon_equals_accepted'], 'outside', r['outside_branch_equals_family'], 'geomhash', r['geometry_hash_equals_accepted'])
    print('  int', g['integrity']['verts'], g['integrity']['quads'], g['integrity']['components'], g['integrity']['boundary_edges'], g['integrity']['nonmanifold_edges'], g['integrity']['nonmanifold_vertices'], g['integrity']['degenerate_faces'],
          g['integrity']['winding_consistent'], g['integrity']['normals_outward'], 'SIfam', g['integrity']['contact_pairs_equal_family_set'], 'brSI', g['integrity']['branch_self_intersections'], 'new', g['integrity']['family_contact_class']['new'])
    print('  val', g['validator']['firm'], g['validator']['stations_identical_to_family'], g['validator']['family_equals_reviewed_v004'], '| anat', [g['anatomy']['final_ear_excluded'][k] for k in ('T1', 'T2', 'T3', 'T7')], g['anatomy']['final_unmasked_anatomy_py']['failing'], g['anatomy']['final_unmasked_anatomy_py']['zones_over_limit_excluding_ears'])
    print('  canon', g['vael_canon_firewalls']['canon'], g['vael_canon_firewalls']['body_systems_material_vs_humans'], g['vael_canon_firewalls']['face_systems_material'], g['vael_canon_firewalls']['elf_face_rows'], g['vael_canon_firewalls']['equals_accepted_VF2'],
          '| he', g['hidden_ear']['equals_accepted_VF2'], '| pelvis', g['pelvis']['gating'], g['pelvis']['equals_accepted_VF2'], '| face', g['face']['mouth_pass'], g['face']['orbit_pass'], g['face']['equals_family'], g['face']['expressions_equal_accepted_VF2'])
    print('  ear', g['ear']['T4'], round(g['ear']['aspect_max'], 2), round(g['ear']['min_angle'], 1), g['ear']['measures_equal_reviewed'], g['root_integration']['audit_equals_reviewed'], 'dens', g['density']['all_pass'], round(g['density']['ear_branch_mean_pct'], 3),
          '| def', DS[c]['final_minus_family_flipped_max'], DS[c]['final_minus_family_selfx_max'], DS[c]['poses_worse_than_family'], DS[c]['excess_over_marchfolk_gt5'], all(DS[c]['family_equals_reviewed_v004'].values()), '| earready', g['deformation']['ear_readiness']['all_zero'])
print('probes', G['configurations']['c1']['probes']['all_clean'], G['configurations']['c1']['probes']['count'], 'firewall', G['ear_firewall']['all_hold'], {c: {k: round(x, 4) if isinstance(x, float) else x for k, x in v['standoff_residual'].items()} for c, v in FW.items()})
