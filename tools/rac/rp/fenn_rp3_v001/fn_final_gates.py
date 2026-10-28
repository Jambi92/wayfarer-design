# fn_final_gates.py WORK OUT_DIR : order 6d2eadc §5-§14 -- one record of every final gate for the two Fenn RP3 production bodies, from the clean-rebuild
# folder (run_fnfinal.sh + run_fnfinal_eval.sh + fn_make_prod.py + fn_final_anatomy.py). Writes FENN_FINAL_gates.json and FENN_FINAL_deformation_summary.json.
import sys, os, json, glob, hashlib, numpy as np
W, O = sys.argv[1:3]; os.makedirs(O, exist_ok=True); jl = lambda p: json.load(open(p)); sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
REPO = '/home/claude/wayfarer-design'; EV2 = REPO + '/reviews/rac-rp3-evidence/fenn_ear_v002'; MFD = REPO + '/reviews/rac-rp3-evidence/mpfb_family_base_final_toe2/deformation'
CFG = {'c1': ('FNL4-CF2', 'FN_M_REF_RP3_v001', 'MF-M-R'), 'c2': ('FNF181-CF2', 'FN_F_REF_RP3_v001', 'MF-F-R')}
G = dict(order='6d2eadc', work=W, configurations={}); DS = {}
def geo_diff(h, P):                               # committed geometry record (root-frame patch coordinates + transition ring xyz) vs the rebuilt production candidate
    g = np.load('%s/geometry/%s_E2_branch_geometry_v002.npz' % (EV2, h)); d = [float(np.abs(P['V'][g['transition_index']] - g['transition_xyz']).max())]
    for s in ('l', 'r'):
        fr = g['frame_' + s].reshape(4, 3); O, bb, u, n = fr; X = O + g['patch_' + s] @ np.stack([bb, u, n]); d.append(float(np.abs(P['V'][P['side'] == s] - X).max()))
    return max(d)
REV = {'FNL4-CF2': '/tmp/claude-0/rt/fn/ear/v002_r3', 'FNF181-CF2': '/tmp/claude-0/rt/fn/ear/v002_r3'}
for c, (h, nm, mf) in CFG.items():
    g = {}; P = np.load('%s/ear/build/%s_E2_branch.npz' % (W, h)); F = np.load('%s/fam/%s_fam.npz' % (W, h))
    # ---- §5 clean rebuild
    v_ = P['v005_to_branch']; ok_ = (v_ >= 0); ok_[ok_] = P['part'][v_[ok_]] == 'v005'   # kept v005 vertices outside the branch (transition ring excluded)
    rc = jl('%s/src/%s_regen_check.json' % (W, h)); R2 = np.load('%s/build/%s_E2_branch.npz' % (REV[h], h))
    g['rebuild'] = dict(regen_geometry_identical=rc['geometry_identical'], regen_max_abs_dV_cm=rc['max_abs_dV_cm'], committed_r6_sha256=rc['committed_sha256'], build_sha256=rc['build_sha256'],
                        family_realization_sha256=sha('%s/fam/%s_fam.npz' % (W, h)), family_equals_reviewed=bool(sha('%s/fam/%s_fam.npz' % (W, h)) == sha('/tmp/claude-0/rt/fn/cf/fam/%s_fam.npz' % h)),
                        branch_arrays_equal_reviewed_v002=bool(all(np.array_equal(P[k], R2[k]) for k in P.files)),
                        branch_geometry_max_abs_diff_vs_committed_record_cm=geo_diff(h, P),
                        outside_branch_equals_family=bool(np.array_equal(P['V'][P['v005_to_branch'][ok_]], F['V'][ok_])), transition_ring_vertices=int((P['part'] == 'transition').sum()))
    # ---- production file + local read-back
    pr = jl('%s/prod/%s.json' % (W, nm)); rb = jl('%s/readback_local/%s_readback.json' % (W, nm)); g['production'] = dict(sidecar=pr, readback_local=rb)
    # ---- §6 integrity (production read-back + Standard audit + ear audit)
    au = jl('%s/audit/%s_final_audit.json' % (W, h)); af = jl('%s/audit/%s_fam_audit.json' % (W, h)); ea = jl('%s/ear/audit/%s_E2_audit.json' % (W, h))
    v2b = P['v005_to_branch']; Qf = np.asarray(F['Q']); key = {tuple(sorted(v2b[q])): i for i, q in enumerate(Qf) if (v2b[q] >= 0).all()}
    SIp = np.load('%s/audit/%s_final_loops.npz' % (W, h), allow_pickle=True)['SI']; SIf = np.load('%s/audit/%s_fam_loops.npz' % (W, h), allow_pickle=True)['SI']; Qp = np.asarray(P['Q'])
    mp = lambda f: key.get(tuple(sorted(Qp[f])), -1); sp_ = {tuple(sorted((mp(a), mp(b)))) for a, b in SIp}; sf = {tuple(sorted(map(int, p))) for p in SIf}
    ct_prev = jl(REPO + '/reviews/rac-rp3-evidence/fenn_rp3_v001/contact/%s_contact.json' % h.split('-')[0])
    g['integrity'] = dict(quads_pct=au['quads_pct'], components=au['components'], boundary_edges=au['boundary_edges'], nonmanifold_edges=au['nonmanifold_edges'], nonmanifold_vertices=au['nonmanifold_vertices'],
                          degenerate_faces=au['degenerate_faces'], winding_consistent=au['winding_consistent'], normals_outward=au['normals_outward'], coincident_vertex_pairs=au['coincident_vertex_pairs'],
                          self_intersection_pairs=au['self_intersection_face_pairs'], family_self_intersection_pairs=af['self_intersection_face_pairs'],
                          contact_pairs_equal_family_set=bool(sp_ == sf), contact_pairs_on_branch_faces=int(sum(1 for a, b in sp_ if a < 0 or b < 0)),
                          family_contact_class=dict(source=ct_prev['classes']['source'], new=ct_prev['classes']['new'], note='Fenn body-family contact record (order 57dc328); CF2 changes only the head, the pair set is identical'),
                          branch_self_intersections=ea['self_intersection_pairs_touching_branch'], root_valence=ea['root_valence'], root_seam_float_burial=dict(boundary=ea.get('boundary_edges', au['boundary_edges']), clearance_min_cm=ea['ear_to_head_clearance']['min_cm']),
                          transition_displacement_max_cm=ea['transition_ring']['displacement_max_cm'])
    # ---- §7 validator
    va = jl('%s/val/%s_final_validator_v2_D1-D6.json' % (W, h)); vf = jl('%s/val/%s_fam_validator_v2_D1-D6.json' % (W, h))
    same = [s for s in va['stations'] if va['stations'][s]['loops_v2'] == vf['stations'][s]['loops_v2'] and va['stations'][s]['margin'] == vf['stations'][s]['margin']
            and va['stations'][s]['valid_sides'] == vf['stations'][s]['valid_sides'] and va['stations'][s]['D5_undefined_sides'] == vf['stations'][s]['D5_undefined_sides'] and va['stations'][s]['D6_undefined_sides'] == vf['stations'][s]['D6_undefined_sides']]
    lab = {s: [vf['stations'][s]['status_D1_D3'], va['stations'][s]['status_D1_D3']] for s in va['stations'] if va['stations'][s]['status_D1_D3'] != vf['stations'][s]['status_D1_D3']}
    g['validator'] = dict(rules='D1 + D3 + D4 + D5 + D6 (validator_v2.py --scale-ref 173.143 --d5 --d6-native)', firm=va['summary']['firm_pass_count'], stations=va['summary']['stations'], firm_fail=va['summary']['D1_D3_firm_fail'],
                          margin_zero=va['summary']['margin_zero'], fallback_statuses=va['summary']['D1_D3_non_plain'], D5_exclusions={s: v['D5_undefined_sides'] for s, v in va['stations'].items() if v['D5_undefined_sides']},
                          D6_exclusions={s: v['D6_undefined_sides'] for s, v in va['stations'].items() if v['D6_undefined_sides']}, family_firm=vf['summary']['firm_pass_count'],
                          stations_identical_to_family=len(same), status_label_differences_vs_family=lab,
                          note='loops, margins, valid sides and D5 / D6 exclusions are identical to the CF2 family realization at every station; the label differences are fallback annotations driven by the raw loop count of an already-excluded (undefined) side, which depends on vertex order (the branch re-indexes the mesh); no verdict changes')
    # ---- §8 anatomy / identity / hidden ear
    an = jl('%s/anat/%s_final_anatomy_earexcl.json' % (W, h)); a0 = jl('%s/anat/%s_final_anatomy.json' % (W, h)); fa = jl('%s/anat/%s_fam_anatomy.json' % (W, h))
    idn = jl('%s/anat/%s_identity.json' % (W, h)); he = jl('%s/he/FN_hidden_ear_identity_CF2.json' % W)['configs'][c]; ce = jl('%s/he/CF_hidden_ear_eval_final.json' % W)['configs'][c]['CF2']
    ce0 = jl(REPO + '/reviews/rac-rp3-evidence/fenn_craniofacial_v001/CF_hidden_ear_eval.json')['configs'][c]['CF2']
    g['anatomy'] = dict(final_ear_excluded=dict(T1=an['T1_pass'], T2=an['T2_pass'], T3=an['T3_pass'], T7=an['T7_pass'], stature_diff_mm=an['stature_diff_mm'], bbox_diff_mm=an['bbox_diff_mm'],
                                               iou=an['silhouette_iou'], prod_to_source=an['deviation_prod_to_source'], source_to_prod=an['deviation_source_to_prod']),
                        final_unmasked_anatomy_py=dict(T1_T2=a0['T1_T2_pass'], T3=a0['T3_pass'], T7=a0['T7_pass'], iou=a0['silhouette_iou'], ears_prod_to_source=a0['deviation_prod_to_source']['ears'],
                                                       note='fails only because the R-6 source still carries the MPFB human auricle and the production body carries the accepted E2 ear branch'),
                        family_anatomy_py=dict(T1_T2=fa['T1_T2_pass'], T3=fa['T3_pass'], T7=fa['T7_pass'], iou_min=min(fa['silhouette_iou'].values()), body=fa['deviation_prod_to_source']['body']),
                        identity=dict(holds_all_zones=idn['identity_holds_all_zones'], verdict=idn['verdict']),
                        hidden_ear_body=dict(regions={r: dict(FN_vs_MF_mm=v['FN_vs_MF_rms_mm'], human_baseline_mm=v['SG_vs_MF_rms_mm_human_baseline'], ratio=v['ratio_FNMF_over_human']) for r, v in he['body'].items()},
                                             pass_=all(v['ratio_FNMF_over_human'] > 1.5 for v in he['body'].values())),
                        hidden_ear_face=dict(regions_material={r: v.get('departure_material') for r, v in he['face'].items()}, canon_descriptors_direction_holds={k: v['direction_holds'] for k, v in he['canon_descriptors'].items()},
                                             cf_eval_systems_material=ce['systems_material'], cf_eval_systems_direction_ok=ce['systems_direction_ok'], cf_eval_equals_accepted_CF2=bool(ce['descriptors'] == ce0['descriptors'] and ce['region_rms_vs_MF_mm'] == ce0['region_rms_vs_MF_mm']),
                                             pass_=bool(ce['systems_material'] == 6 and ce['systems_direction_ok'] == 6)))
    # ---- §9 face / UFCA
    fr = jl('%s/audit/%s_final_face.json' % (W, h)); ff = jl('%s/audit/%s_fam_face.json' % (W, h))
    g['face'] = dict(mouth_rings=fr['mouth_rings']['count'], orbit_rings=[fr['orbit_rings_l']['count'], fr['orbit_rings_r']['count']], poles_at_mouth_corners=fr['poles_at_mouth_corners'], poles_within_2cm_of_mouth=fr['poles_within_2cm_of_mouth'],
                     poles_within_2cm_of_eyes=[fr['poles_within_2cm_of_eye_l'], fr['poles_within_2cm_of_eye_r']], mouth_pass=fr['mouth_pass'], orbit_pass=fr['orbit_pass'], face_density_pct=au['density_pct_of_stature']['face'],
                     equals_family=bool(all(fr[k] == ff[k] for k in ('poles_at_mouth_corners', 'poles_within_2cm_of_mouth', 'poles_within_2cm_of_eye_l', 'poles_within_2cm_of_eye_r', 'mouth_pass', 'orbit_pass')) and fr['mouth_rings']['count'] == ff['mouth_rings']['count'] and fr['orbit_rings_l']['count'] == ff['orbit_rings_l']['count']))
    # ---- §10 ear final gate (ear_audit / ear_measure / ear_deform / zone report)
    em = jl('%s/ear/meas/%s_E2_measure.json' % (W, h))['sides']['l']; em0 = jl('%s/measure/%s_E2_measure.json' % (EV2, h))['sides']['l']; ed = jl('%s/ear/deform/%s_E2_deform.json' % (W, h))
    g['ear'] = dict(T4=ea['T4']['angle_violations'], branch_faces=ea['T4']['branch_faces'], T4_rate=ea['T4']['angle_violations'] / ea['T4']['branch_faces'], aspect_max=ea['T4']['aspect_max'], aspect_gt10=ea['T4']['aspect_gt10'],
                    min_angle=ea['T4']['min_angle'], density=ea['density'], root_dihedral=ea['root_dihedral'], transition=ea['transition_ring'], root_deviation=ea['root_deviation'], clearance=ea['ear_to_head_clearance'],
                    measures_equal_reviewed_v002=bool(em == em0), measures={k: em[k] for k in ('length_lobe_to_tip_cm', 'auricle_height_cm', 'max_width_cm', 'auricle_body_angle_deg', 'total_lateral_extent_from_root_plane_cm', 'side_view_upper_extension_deg', 'sweep_max_axis_deviation_cm', 'tip_in_plane_angle_deg_at_1cm')},
                    thickness_cm=em['thickness_cm'], deform={p: [v['new_selfx_pairs_touching_branch'], v['flipped_branch_faces'], v['root_band_inverted']] for p, v in ed['poses'].items()})
    # ---- §11 density
    g['density'] = dict(zones={k: dict(mean=v['mean'], limit=v['limit'], pass_=v['pass_mean']) for k, v in au['density_pct_of_stature'].items()}, all_pass=all(v['pass_mean'] for v in au['density_pct_of_stature'].values()),
                        ear_branch_mean_pct=ea['density']['branch_mean_edge_pct_stature'], ear_branch_p95_pct=ea['density']['p95_pct'],
                        family_zones_equal_except_ear_head=[k for k in au['density_pct_of_stature'] if au['density_pct_of_stature'][k] != af['density_pct_of_stature'][k]])
    # ---- §12 deformation
    dn = jl('%s/def/deform_%s_native.json' % (W, h)); dfm = jl('%s/def/deform_%s_fam.json' % (W, h)); dp = jl('%s/def/deform_%s_final.json' % (W, h)); dm = jl('%s/deform_%s_v005.json' % (MFD, mf))
    P_ = {}
    for p in dp['poses']:
        P_[p] = dict(final_flipped=dp['poses'][p]['flipped_faces'], family_flipped=dfm['poses'][p]['flipped_faces'], native_flipped=dn['poses'][p]['flipped_faces'], marchfolk_v005_flipped=dm['poses'][p]['flipped_faces'],
                     final_new_selfx=dp['poses'][p]['new_selfx_pairs'], family_new_selfx=dfm['poses'][p]['new_selfx_pairs'], final_new_folds=dp['poses'][p]['new_folds'], family_new_folds=dfm['poses'][p]['new_folds'])
    DS[c] = dict(head=h, reference_marchfolk=mf + ' v005', poses=P_, final_minus_family_flipped_max=max(v['final_flipped'] - v['family_flipped'] for v in P_.values()),
                 final_minus_family_selfx_max=max(v['final_new_selfx'] - v['family_new_selfx'] for v in P_.values()), final_minus_marchfolk_flipped_max=max(v['final_flipped'] - v['marchfolk_v005_flipped'] for v in P_.values()),
                 poses_worse_than_family=[p for p, v in P_.items() if v['final_flipped'] > v['family_flipped'] or v['final_new_selfx'] > v['family_new_selfx'] or v['final_new_folds'] > v['family_new_folds']])
    g['deformation'] = dict(standard_v1=DS[c], ear_readiness=dict(poses=list(ed['poses']), all_zero=all(v[0] == 0 and v[1] == 0 and v[2] == 0 for v in g['ear']['deform'].values())))
    # ---- §13 probes
    pz = jl('%s/probes/FENN_EAR_shape_probes.json' % EV2) if c == 'c1' else None
    if c == 'c1':
        pr_eq = {}
        for d in sorted(glob.glob('%s/ear/probe/*/' % W)):
            n = d.rstrip('/').split('/')[-1]; a = np.load(d + 'FNL4-CF2_E2_branch.npz'); b = np.load('%s/probe/%s/FNL4-CF2_E2_branch.npz' % (REV[h], n)); A = jl(d + 'audit.json')
            pr_eq[n] = dict(geometry_equals_reviewed=bool(np.array_equal(a['V'], b['V']) and np.array_equal(a['Q'], b['Q'])), T4=A['T4']['angle_violations'], aspect_max=A['T4']['aspect_max'], aspect_gt10=A['T4']['aspect_gt10'],
                            self_intersection_branch=A['self_intersection_pairs_touching_branch'], boundary=A['boundary_edges'])
        g['probes'] = dict(rebuilt=pr_eq, reviewed_record=pz['summary'])
    G['configurations'][c] = g
json.dump(G, open(os.path.join(O, 'FENN_FINAL_gates.json'), 'w'), indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
json.dump(DS, open(os.path.join(O, 'FENN_FINAL_deformation_summary.json'), 'w'), indent=1); json.dump(DS, open(os.path.join(W, 'FENN_FINAL_deformation_summary.json'), 'w'), indent=1)
for c, g in G['configurations'].items():
    print(c, 'rebuild', g['rebuild']['branch_arrays_equal_reviewed_v002'], g['rebuild']['outside_branch_equals_family'], '| val', g['validator']['firm'], g['validator']['stations_identical_to_family'],
          '| anat', [g['anatomy']['final_ear_excluded'][k] for k in ('T1', 'T2', 'T3', 'T7')], '| id', g['anatomy']['identity']['holds_all_zones'], '| he body', g['anatomy']['hidden_ear_body']['pass_'], 'face', g['anatomy']['hidden_ear_face']['pass_'],
          '| face', g['face']['mouth_pass'], g['face']['orbit_pass'], g['face']['equals_family'], '| dens', g['density']['all_pass'], '| contact', g['integrity']['contact_pairs_equal_family_set'],
          '| def', DS[c]['final_minus_family_flipped_max'], DS[c]['final_minus_family_selfx_max'], DS[c]['poses_worse_than_family'], '| ear', g['ear']['T4'], round(g['ear']['aspect_max'], 2), g['ear']['measures_equal_reviewed_v002'], g['deformation']['ear_readiness']['all_zero'])
