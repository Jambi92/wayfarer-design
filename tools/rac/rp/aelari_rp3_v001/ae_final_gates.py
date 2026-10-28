# ae_final_gates.py WORK OUT_DIR : Aelari final consolidation (order 2026-10-28) §4-§19 -- one record of every final gate for the two Aelari RP3 production
# bodies, from the clean-rebuild folder (run_aefinal.sh + run_aefinal_eval.sh + run_aefinal_prod.sh). Writes AELARI_FINAL_gates.json and
# AELARI_FINAL_deformation_summary.json. Reviewed references: /tmp/claude-0/rt/ae/r1 (order 0f6aba8 corrected candidates).
import sys, os, json, glob, hashlib, numpy as np
W, O = sys.argv[1:3]; os.makedirs(O, exist_ok=True); jl = lambda p: json.load(open(p)); sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
REPO = '/home/claude/wayfarer-design'; RA = REPO + '/reviews/reference-assets'; EVC = REPO + '/reviews/rac-rp3-evidence/aelari_rp3_correction'; MFD = REPO + '/reviews/rac-rp3-evidence/mpfb_family_base_final_toe2/deformation'
REV = '/tmp/claude-0/rt/ae/r1'; CAN = 'AE-E2'
CFG = {'c1': ('AEL1-R1', 'AE_M_REF_RP3_v001', 'MF-M-R'), 'c2': ('AELF190-R1', 'AE_F_REF_RP3_v001', 'MF-F-R')}
FNB = '/tmp/claude-0/rt/fn/final/ear/build/FNL4-CF2_E2_branch.npz'; FNM = '/tmp/claude-0/rt/fn/final/ear/meas/FNL4-CF2_E2_measure.json'; FNJ = '/tmp/claude-0/rt/fn/final/ear/build/FNL4-CF2_E2_branch.json'
G = dict(order='reviews/chatgpt-rac-rp3-aelari-final-consolidation-freeze-order.md (2026-10-28)', work=W, configurations={}); DS = {}
PA = jl('%s/anat/AE_final_canon_pelvis.json' % W); MX = jl('%s/anat/AE_final_metrics_vs_FN_MF.json' % W); HE = jl('%s/he/AE_hidden_ear_identity_final.json' % W); HER = jl(REV + '/AE_hidden_ear_identity_R1.json')
Qfenn = np.asarray(np.load(FNB)['Q'])
for c, (h, nm, mf) in CFG.items():
    g = {}; P = np.load('%s/ear/build/%s_%s_branch.npz' % (W, h, CAN)); F = np.load('%s/fam/%s_fam.npz' % (W, h)); bj = jl('%s/ear/build/%s_%s_branch.json' % (W, h, CAN))
    # ---- §4 clean rebuild
    v_ = P['v005_to_branch']; ok_ = (v_ >= 0); ok_[ok_] = P['part'][v_[ok_]] == 'v005'
    rc = jl('%s/src/%s_regen_check.json' % (W, h)); R2 = np.load('%s/ear/build/%s_%s_branch.npz' % (REV, h, CAN)); rbj = jl('%s/ear/build/%s_%s_branch.json' % (REV, h, CAN))
    full = np.load('%s/full/%s_r6.npz' % (W, h)); com = np.load('%s/r6/%s_r6.npz' % (RA, h))
    g['rebuild'] = dict(regen_geometry_identical=rc['geometry_identical'], regen_max_abs_dV_cm=rc['max_abs_dV_cm'], committed_r6_sha256=rc['committed_sha256'], build_sha256=rc['build_sha256'],
                        full_record_rebuild_max_abs_dV_cm=float(np.abs(full['V'].astype(float) - com['V'].astype(float)).max()),
                        family_realization_sha256=sha('%s/fam/%s_fam.npz' % (W, h)), family_equals_reviewed_v002_candidate=bool(sha('%s/fam/%s_fam.npz' % (W, h)) == sha('%s/fam/%s_fam.npz' % (REV, h))),
                        branch_arrays_equal_reviewed_AE_E2=bool(all(np.array_equal(P[k], R2[k]) for k in P.files)),
                        branch_max_abs_diff_vs_reviewed_cm=float(np.abs(P['V'].astype(float) - R2['V'].astype(float)).max()), params_equal_reviewed=bj['params'] == rbj['params'], params=bj['params'],
                        face_list_equals_frozen_fenn_v002=bool(np.array_equal(np.asarray(P['Q']), Qfenn)),
                        outside_branch_equals_family=bool(np.array_equal(P['V'][P['v005_to_branch'][ok_]], F['V'][ok_])), transition_ring_vertices=int((P['part'] == 'transition').sum()))
    # ---- production file + local read-back
    pr = jl('%s/prod/%s.json' % (W, nm)); rb = jl('%s/readback_local/%s_readback.json' % (W, nm)); g['production'] = dict(sidecar=pr, readback_local=rb)
    # ---- §6 integrity
    au = jl('%s/audit/%s_final_audit.json' % (W, h)); af = jl('%s/audit/%s_fam_audit.json' % (W, h)); ea = jl('%s/ear/audit/%s_%s_audit.json' % (W, h, CAN))
    v2b = P['v005_to_branch']; Qf = np.asarray(F['Q']); key = {tuple(sorted(v2b[q])): i for i, q in enumerate(Qf) if (v2b[q] >= 0).all()}
    SIp = np.load('%s/audit/%s_final_loops.npz' % (W, h), allow_pickle=True)['SI']; SIf = np.load('%s/audit/%s_fam_loops.npz' % (W, h), allow_pickle=True)['SI']; Qp = np.asarray(P['Q'])
    mp = lambda f: key.get(tuple(sorted(Qp[f])), -1); sp_ = {tuple(sorted((mp(a), mp(b)))) for a, b in SIp}; sf = {tuple(sorted(map(int, p))) for p in SIf}
    ct = jl('%s/contact/%s_contact.json' % (EVC, h))
    g['integrity'] = dict(quads_pct=au['quads_pct'], components=au['components'], boundary_edges=au['boundary_edges'], nonmanifold_edges=au['nonmanifold_edges'], nonmanifold_vertices=au['nonmanifold_vertices'],
                          degenerate_faces=au['degenerate_faces'], winding_consistent=au['winding_consistent'], normals_outward=au['normals_outward'], coincident_vertex_pairs=au['coincident_vertex_pairs'],
                          family_coincident_vertex_pairs=af['coincident_vertex_pairs'], self_intersection_pairs=au['self_intersection_face_pairs'], family_self_intersection_pairs=af['self_intersection_face_pairs'],
                          contact_pairs_equal_family_set=bool(sp_ == sf), contact_pairs_on_branch_faces=int(sum(1 for a, b in sp_ if a < 0 or b < 0)),
                          family_contact_class=dict(source=ct['classes']['source'], family=ct['classes']['family'], new=ct['classes']['new'], record='aelari_rp3_correction/contact/%s_contact.json (order 0f6aba8)' % h),
                          branch_self_intersections=ea['self_intersection_pairs_touching_branch'], root_valence=ea['root_valence'], root_valence_4=all(v.get('4', 0) == 52 for v in ea['root_valence'].values()),
                          root_seam_float_burial=dict(boundary=ea['boundary_edges'], clearance_min_cm=ea['ear_to_head_clearance']['min_cm'], root_deviation=ea['root_deviation']),
                          transition_displacement_max_cm=ea['transition_ring']['displacement_max_cm'])
    # ---- §7 validator
    va = jl('%s/val/%s_final_validator_v2_D1-D6.json' % (W, h)); vf = jl('%s/val/%s_fam_validator_v2_D1-D6.json' % (W, h)); vr = jl('%s/val/%s_fam_validator_v2_D1-D6.json' % (REV, h))
    same = [s for s in va['stations'] if all(va['stations'][s][k] == vf['stations'][s][k] for k in ('loops_v2', 'margin', 'valid_sides', 'D5_undefined_sides', 'D6_undefined_sides'))]
    lab = {s: [vf['stations'][s]['status_D1_D3'], va['stations'][s]['status_D1_D3']] for s in va['stations'] if va['stations'][s]['status_D1_D3'] != vf['stations'][s]['status_D1_D3']}
    g['validator'] = dict(rules='D1 + D3 + D4 + D5 + D6 (validator_v2.py --scale-ref 173.143 --d5 --d6-native)', firm=va['summary']['firm_pass_count'], stations=va['summary']['stations'], firm_fail=va['summary']['D1_D3_firm_fail'],
                          margin_zero=va['summary']['margin_zero'], fallback_statuses=va['summary']['D1_D3_non_plain'], D5_exclusions={s: v['D5_undefined_sides'] for s, v in va['stations'].items() if v['D5_undefined_sides']},
                          D6_exclusions={s: v['D6_undefined_sides'] for s, v in va['stations'].items() if v['D6_undefined_sides']}, family_firm=vf['summary']['firm_pass_count'],
                          stations_identical_to_family=len(same), status_label_differences_vs_family=lab, family_equals_reviewed_candidate=bool(vf['stations'] == vr['stations']),
                          note='loops, margins, valid sides and D5 / D6 exclusions compared station by station against the family realization; label differences (if any) are vertex-order fallback annotations of an already-undefined side')
    # ---- §8 anatomy, §9 identity / canon, §11 hidden-ear face
    an = jl('%s/anat/%s_final_anatomy_earexcl.json' % (W, h)); a0 = jl('%s/anat/%s_final_anatomy.json' % (W, h)); fa = jl('%s/anat/%s_fam_anatomy.json' % (W, h)); idn = jl('%s/anat/%s_identity.json' % (W, h))
    he = HE['configs'][c]; her = HER['configs'][c]
    unm_fail = [k for k in ('T1_T2_pass', 'T3_pass', 'T7_pass') if not a0[k]]
    unm_zones_fail = sorted({z for d in ('deviation_prod_to_source', 'deviation_source_to_prod') for z, v in a0[d].items() if z != 'ears' and any(v[k] > lim[k] for lim in [dict(median_mm=0.5, p95_mm=1.5, max_mm=3.0) if z == 'body' else dict(median_mm=0.3, p95_mm=0.8, max_mm=1.5)] for k in lim)})
    g['anatomy'] = dict(final_ear_excluded=dict(T1=an['T1_pass'], T2=an['T2_pass'], T3=an['T3_pass'], T7=an['T7_pass'], stature_diff_mm=an['stature_diff_mm'], bbox_diff_mm=an['bbox_diff_mm'], iou=an['silhouette_iou'],
                                               prod_to_source=an['deviation_prod_to_source'], source_to_prod=an['deviation_source_to_prod']),
                        final_unmasked_anatomy_py=dict(T1_T2=a0['T1_T2_pass'], T3=a0['T3_pass'], T7=a0['T7_pass'], iou=a0['silhouette_iou'], failing=unm_fail, zones_over_limit=unm_zones_fail,
                                                       body=a0['deviation_prod_to_source']['body'], head=a0['deviation_prod_to_source']['head'], ears_prod_to_source=a0['deviation_prod_to_source']['ears'],
                                                       classification='expected source-vs-new-ear anatomy divergence (R-6 source carries the MPFB human auricle; production carries AE-E2)' if unm_fail else 'none'),
                        family_anatomy_py=dict(T1_T2=fa['T1_T2_pass'], T3=fa['T3_pass'], T7=fa['T7_pass'], iou_min=min(fa['silhouette_iou'].values()), body=fa['deviation_prod_to_source']['body']),
                        identity=dict(holds_all_zones=idn['identity_holds_all_zones'], verdict=idn['verdict']))
    rows = {r['key']: r for r in PA['configs'][c]['canon']}
    REQ_FN = ['central_vertical_share', 'torso_share', 'neck_share', 'thoracic_vertical_share', 'waist_interval_over_torso', 'cranial_vertical_share', 'extremity_share', 'shin_over_leg']
    REQ_H = ['leg_share', 'arm_share', 'hand_share', 'foot_share', 'finger_over_hand', 'forearm_over_upperarm', 'elbow_breadth_share', 'thorax_depth_share']
    g['body_identity'] = dict(vs_fenn={k: dict(AE=rows[k]['AE'], FN=rows[k]['FN'], AE_vs_FN_pct=rows[k]['AE_vs_FN_pct'], holds=rows[k]['holds']) for k in REQ_FN},
                              vs_humans={k: dict(AE=rows[k]['AE'], MF=rows[k]['MF'], SG=rows[k]['SG'], AE_vs_MF_pct=rows[k]['AE_vs_MF_pct'], holds=rows[k]['holds']) for k in REQ_H},
                              skin_gracility_diagnostic_only={k: dict(AE=rows[k]['AE'], MF=rows[k]['MF'], FN=rows[k]['FN'], holds=rows[k]['holds']) for k in ('wrist_breadth_share', 'knee_breadth_share', 'ankle_breadth_share')},
                              canon_holds='%d / %d' % (PA['configs'][c]['holds'], PA['configs'][c]['of']), shin_over_leg_gap_to_MF=MX[('AEL1' if c == 'c1' else 'AELF190')]['shin_over_leg_gap_to_MF'],
                              fenn_shin_over_leg_gap_to_MF=MX[('AEL1' if c == 'c1' else 'AELF190')]['FN_shin_over_leg_gap_to_MF'], thoracic_vs_FN_pct=MX[('AEL1' if c == 'c1' else 'AELF190')]['thoracic_vs_FN_pct'],
                              hidden_ear_body_regions={r: dict(AE_vs_FN_mm=v['AE_vs_FN_rms_mm'], AE_vs_MF_mm=v['AE_vs_MF_rms_mm'], AE_vs_SG_mm=v['AE_vs_SG_rms_mm'], human_baseline_mm=v['SG_vs_MF_rms_mm_human_baseline']) for r, v in he['body'].items()},
                              hidden_ear_body_equals_reviewed_R1=bool(he['body'] == her['body']),
                              pass_=all(rows[k]['holds'] for k in REQ_FN + REQ_H))
    g['pelvis'] = dict(rules=[dict(rule=r['rule'], by_t=r['by_t'], holds_all_t=r['holds_all_t'], align_resid_cm=r['align_resid_cm']) for r in PA['pelvis_skeletal_proxy'][c]],
                       all_hold=all(r['holds_all_t'] for r in PA['pelvis_skeletal_proxy'][c]), pelvis_bone_scales=jl('%s/builds/%s_build.json' % (RA, h))['cfg']['bone_scales']['pelvis'])
    dsc = {k: (v['AE'], her['canon_descriptors'][k]['AE']) for k, v in he['canon_descriptors'].items()}
    g['hidden_ear_face'] = dict(systems_direction_ok=he['systems_direction_ok'], systems_material=he['systems_material'], of=he['of'], systems=he['systems'], fenn_relations=he['fenn_relations'],
                                descriptors_equal_reviewed_R1=bool(all(a == b for a, b in dsc.values())), face_regions={r: dict(AE_vs_MF_mm=v['AE_vs_MF_rms_mm'], AE_vs_FN_mm=v['AE_vs_FN_rms_mm'], material_vs_humans=v['departure_from_humans_material'], material_vs_fenn=v['departure_from_fenn_material']) for r, v in he['face'].items()},
                                pass_=bool(he['systems_material'] == 7 and he['systems_direction_ok'] == 7 and all(he['fenn_relations'].values())))
    # ---- §12 face / UFCA
    fr = jl('%s/audit/%s_final_face.json' % (W, h)); ff = jl('%s/audit/%s_fam_face.json' % (W, h))
    KF = ('poles_at_mouth_corners', 'poles_within_2cm_of_mouth', 'poles_within_2cm_of_eye_l', 'poles_within_2cm_of_eye_r', 'mouth_pass', 'orbit_pass')
    g['face'] = dict(mouth_rings=fr['mouth_rings']['count'], orbit_rings=[fr['orbit_rings_l']['count'], fr['orbit_rings_r']['count']], poles_at_mouth_corners=fr['poles_at_mouth_corners'], poles_within_2cm_of_mouth=fr['poles_within_2cm_of_mouth'],
                     poles_within_2cm_of_eyes=[fr['poles_within_2cm_of_eye_l'], fr['poles_within_2cm_of_eye_r']], mouth_pass=fr['mouth_pass'], orbit_pass=fr['orbit_pass'], face_density_pct=au['density_pct_of_stature']['face'],
                     equals_family=bool(all(fr[k] == ff[k] for k in KF) and fr['mouth_rings']['count'] == ff['mouth_rings']['count'] and fr['orbit_rings_l']['count'] == ff['orbit_rings_l']['count'] and fr['orbit_rings_r']['count'] == ff['orbit_rings_r']['count']),
                     topology_outside_branch_unchanged=g['rebuild']['outside_branch_equals_family'])
    # ---- §13 ear final gate
    em = jl('%s/ear/meas/%s_%s_measure.json' % (W, h, CAN))['sides']['l']; em0 = jl('%s/ear/meas/%s_%s_measure.json' % (REV, h, CAN))['sides']['l']; ed = jl('%s/ear/deform/%s_%s_deform.json' % (W, h, CAN))
    MK = ('length_lobe_to_tip_cm', 'auricle_height_cm', 'max_width_cm', 'auricle_body_angle_deg', 'total_lateral_extent_from_root_plane_cm', 'side_view_upper_extension_deg', 'sweep_max_axis_deviation_cm', 'tip_in_plane_angle_deg_at_1cm')
    g['ear'] = dict(T4=ea['T4']['angle_violations'], branch_faces=ea['T4']['branch_faces'], T4_rate=ea['T4']['angle_violations'] / ea['T4']['branch_faces'], aspect_max=ea['T4']['aspect_max'], aspect_gt10=ea['T4']['aspect_gt10'],
                    min_angle=ea['T4']['min_angle'], density=ea['density'], root_dihedral=ea['root_dihedral'], transition=ea['transition_ring'], root_deviation=ea['root_deviation'], clearance=ea['ear_to_head_clearance'],
                    outside_branch_byte_identical=ea['outside_branch_byte_identical'], measures_equal_reviewed=bool(em == em0), measures={k: em[k] for k in MK}, HH_cm=bj['HH_cm'], thickness_cm=em['thickness_cm'],
                    guard_iterations=len(jl('%s/ear/build/%s_%s_deform_guard_log.json' % (W, h, CAN))), deform={p: [v['new_selfx_pairs_touching_branch'], v['flipped_branch_faces'], v['root_band_inverted']] for p, v in ed['poses'].items()})
    # ---- §15 density
    g['density'] = dict(zones={k: dict(mean=v['mean'], limit=v['limit'], pass_=v['pass_mean']) for k, v in au['density_pct_of_stature'].items()}, all_pass=all(v['pass_mean'] for v in au['density_pct_of_stature'].values()),
                        ear_branch_mean_pct=ea['density']['branch_mean_edge_pct_stature'], ear_branch_p95_pct=ea['density']['p95_pct'], ear_branch_pass=ea['density']['branch_mean_edge_pct_stature'] <= 0.25,
                        zones_differing_from_family=[k for k in au['density_pct_of_stature'] if au['density_pct_of_stature'][k] != af['density_pct_of_stature'][k]])
    # ---- §16 deformation
    dn = jl('%s/def/deform_%s_native.json' % (W, h)); dfm = jl('%s/def/deform_%s_fam.json' % (W, h)); dp = jl('%s/def/deform_%s_final.json' % (W, h)); dm = jl('%s/deform_%s_v005.json' % (MFD, mf))
    P_ = {}
    for p in dp['poses']:
        P_[p] = dict(final_flipped=dp['poses'][p]['flipped_faces'], family_flipped=dfm['poses'][p]['flipped_faces'], native_flipped=dn['poses'][p]['flipped_faces'], marchfolk_v005_flipped=dm['poses'][p]['flipped_faces'],
                     final_new_selfx=dp['poses'][p]['new_selfx_pairs'], family_new_selfx=dfm['poses'][p]['new_selfx_pairs'], marchfolk_new_selfx=dm['poses'][p]['new_selfx_pairs'], final_new_folds=dp['poses'][p]['new_folds'], family_new_folds=dfm['poses'][p]['new_folds'])
    DS[c] = dict(head=h, reference_marchfolk=mf + ' v005', poses=P_, final_minus_family_flipped_max=max(v['final_flipped'] - v['family_flipped'] for v in P_.values()),
                 final_minus_family_selfx_max=max(v['final_new_selfx'] - v['family_new_selfx'] for v in P_.values()), final_minus_marchfolk_flipped_max=max(v['final_flipped'] - v['marchfolk_v005_flipped'] for v in P_.values()),
                 poses_worse_than_family=[p for p, v in P_.items() if v['final_flipped'] > v['family_flipped'] or v['final_new_selfx'] > v['family_new_selfx'] or v['final_new_folds'] > v['family_new_folds']],
                 classification='remaining flips / contacts equal the family realization pose by pose (known family rig class: source rig + carried MPFB weights, plain LBS; no topology-class defect added by the ear branch)')
    g['deformation'] = dict(standard_v1=DS[c], ear_readiness=dict(poses=list(ed['poses']), all_zero=all(v[0] == 0 and v[1] == 0 and v[2] == 0 for v in g['ear']['deform'].values()),
                                                                   root_loop_edge_strain_pct={p: [v['root_loop_edge_strain_pct'], v['v005_root_loop_edge_strain_pct']] for p, v in ed['poses'].items()},
                                                                   root_band_area_ratio={p: [v['root_band_area_ratio_min'], v['root_band_area_ratio_max']] for p, v in ed['poses'].items()},
                                                                   ear_to_nonhead_clearance_cm={p: v['ear_to_nonhead_clearance_cm'] for p, v in ed['poses'].items()},
                                                                   note='root strain listed as [branch root loop, same loop on the v005 family body]'))
    # ---- §18 probes (configuration 1)
    if c == 'c1':
        base = em; EXP = {'proj': 'auricle_body_angle_deg', 'tilt': 'side_view_upper_extension_deg', 'sweep': 'sweep_max_axis_deviation_cm', 'len': 'length_lobe_to_tip_cm', 'tip': 'tip_in_plane_angle_deg_at_1cm'}; pr = {}
        for d in sorted(glob.glob('%s/ear/probe/*/' % W)):
            n = d.rstrip('/').split('/')[-1]; A = jl(d + 'audit.json'); m = jl(d + 'measure.json')['sides']['l']; k = EXP[n.split('_')[0]]; zz = np.load(d + '%s_%s_branch.npz' % (h, CAN))
            sgn = (-1 if ('_m' in n or 'blunt' in n) else 1) * (-1 if n.startswith('tip') else 1); dv = m[k] - base[k]
            pr[n] = dict(same_topology=bool(np.array_equal(np.asarray(zz['Q']), Qfenn)), T4=A['T4']['angle_violations'], aspect_max=A['T4']['aspect_max'], aspect_gt10=A['T4']['aspect_gt10'],
                         self_intersection_branch=A['self_intersection_pairs_touching_branch'], boundary=A['boundary_edges'], root_valence_ok=all(v.get('4', 0) == 52 for v in A['root_valence'].values()),
                         measure=k, value=m[k], base=base[k], moves_intended=bool(np.sign(dv) == sgn and abs(dv) > 1e-3))
        g['probes'] = dict(rebuilt=pr, all_clean=all(v['same_topology'] and v['self_intersection_branch'] == 0 and v['aspect_gt10'] == 0 and v['root_valence_ok'] and v['moves_intended'] and v['boundary'] == 0 for v in pr.values()),
                           T4_max=max(v['T4'] for v in pr.values()), T4_base=g['ear']['T4'])
    G['configurations'][c] = g
# ---- §14 visible-ear firewall: Aelari AE-E2 (each configuration) vs frozen Fenn E2 (FN_M_REF_RP3_v001), head-height / length normalised
fm = jl(FNM)['sides']['l']; HHf = jl(FNJ)['HH_cm']; FW = {}
for c, (h, nm, mf) in CFG.items():
    a = G['configurations'][c]['ear']['measures']; HHa = G['configurations'][c]['ear']['HH_cm']
    r = dict(length_over_HH=[a['length_lobe_to_tip_cm'] / HHa, fm['length_lobe_to_tip_cm'] / HHf], width_over_length=[a['max_width_cm'] / a['length_lobe_to_tip_cm'], fm['max_width_cm'] / fm['length_lobe_to_tip_cm']],
             projection_body_angle_deg=[a['auricle_body_angle_deg'], fm['auricle_body_angle_deg']], lateral_extent_over_length=[a['total_lateral_extent_from_root_plane_cm'] / a['length_lobe_to_tip_cm'], fm['total_lateral_extent_from_root_plane_cm'] / fm['length_lobe_to_tip_cm']],
             upper_extension_deg=[a['side_view_upper_extension_deg'], fm['side_view_upper_extension_deg']], sweep_over_length=[a['sweep_max_axis_deviation_cm'] / a['length_lobe_to_tip_cm'], fm['sweep_max_axis_deviation_cm'] / fm['length_lobe_to_tip_cm']],
             tip_angle_deg=[a['tip_in_plane_angle_deg_at_1cm'], fm['tip_in_plane_angle_deg_at_1cm']])
    r = {k: [round(x, 4) for x in v] for k, v in r.items()}
    r['checks'] = dict(less_lateral_projection=r['projection_body_angle_deg'][0] < r['projection_body_angle_deg'][1], closer_to_skull=r['lateral_extent_over_length'][0] < r['lateral_extent_over_length'][1],
                       more_upward_trajectory=r['upper_extension_deg'][0] > r['upper_extension_deg'][1], longer_relative_length=r['length_over_HH'][0] > r['length_over_HH'][1], narrower=r['width_over_length'][0] < r['width_over_length'][1],
                       distinct_trajectory=abs(r['sweep_over_length'][0] - r['sweep_over_length'][1]) > 0.01 or abs(r['upper_extension_deg'][0] - r['upper_extension_deg'][1]) > 3)
    r['note'] = '[Aelari, frozen Fenn E2]'; FW[c] = r
G['firewall'] = dict(fenn='FNL4-CF2 E2 (frozen FN_M_REF_RP3_v001)', configs=FW, all_hold=all(all(v['checks'].values()) for v in FW.values()))
json.dump(G, open(os.path.join(O, 'AELARI_FINAL_gates.json'), 'w'), indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
json.dump(DS, open(os.path.join(O, 'AELARI_FINAL_deformation_summary.json'), 'w'), indent=1); json.dump(DS, open(os.path.join(W, 'AELARI_FINAL_deformation_summary.json'), 'w'), indent=1)
for c, g in G['configurations'].items():
    print(c, 'rebuild', g['rebuild']['family_equals_reviewed_v002_candidate'], g['rebuild']['branch_arrays_equal_reviewed_AE_E2'], g['rebuild']['outside_branch_equals_family'], g['rebuild']['face_list_equals_frozen_fenn_v002'],
          '| val', g['validator']['firm'], g['validator']['stations_identical_to_family'], '| anat', [g['anatomy']['final_ear_excluded'][k] for k in ('T1', 'T2', 'T3', 'T7')], 'unmasked fail', g['anatomy']['final_unmasked_anatomy_py']['failing'], g['anatomy']['final_unmasked_anatomy_py']['zones_over_limit'],
          '| id', g['anatomy']['identity']['holds_all_zones'], '| body', g['body_identity']['pass_'], g['body_identity']['canon_holds'], '| pelvis', g['pelvis']['all_hold'], '| face', g['hidden_ear_face']['pass_'], g['hidden_ear_face']['descriptors_equal_reviewed_R1'],
          '| ufca', g['face']['mouth_pass'], g['face']['orbit_pass'], g['face']['equals_family'], '| dens', g['density']['all_pass'], round(g['density']['ear_branch_mean_pct'], 3), '| int', g['integrity']['contact_pairs_equal_family_set'], g['integrity']['branch_self_intersections'],
          '| def', DS[c]['final_minus_family_flipped_max'], DS[c]['final_minus_family_selfx_max'], DS[c]['poses_worse_than_family'], '| ear', g['ear']['T4'], round(g['ear']['aspect_max'], 2), g['ear']['measures_equal_reviewed'], g['deformation']['ear_readiness']['all_zero'])
print('firewall', G['firewall']['all_hold'], {c: v['checks'] for c, v in FW.items()}); print('probes', G['configurations']['c1']['probes']['all_clean'], G['configurations']['c1']['probes']['T4_max'])
