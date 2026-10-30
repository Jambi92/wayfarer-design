# hv_final_gates.py WORK OUT_DIR : Halvren final whole-character consolidation / freeze-readiness order §3-§8 -- one record of every final gate for the two
# Halvren RP3 production reference candidates, from the clean-rebuild folder (run_hvfinal.sh + run_hvfinal_eval.sh + run_hvfinal_prod.sh); adapted from
# vael_rp3_v001/va_final_gates.py. Writes HALVREN_FINAL_gates.json and HALVREN_FINAL_deformation_summary.json.
# Accepted references: HB2 + HF2 + HP-B family realization / validator / deformation (/tmp/claude-0/rt/hv/hpe, central-accept order), accepted HP-B source
# evaluation and pelvis package (reviews/.../halvren_rp3_central_accept_ear/hpb_validation, /tmp/claude-0/rt/hv/hp), the frozen ear family record
# (HALVREN_EAR_FAMILY_RP3_FREEZE.json) and its approved HE2 build (/tmp/claude-0/rt/hv/ear/fam6), the committed body / face expression record.
import sys, os, json, hashlib, numpy as np
W, O = sys.argv[1:3]; os.makedirs(O, exist_ok=True); jl = lambda p: json.load(open(p)); sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
REPO = '/home/claude/wayfarer-design'; RA = REPO + '/reviews/reference-assets'; EV = REPO + '/reviews/rac-rp3-evidence'; HPV = EV + '/halvren_rp3_central_accept_ear/hpb_validation'
MFD = EV + '/mpfb_family_base_final_toe2/deformation'; ACCF = '/tmp/claude-0/rt/hv/hpe'; ACCE = '/tmp/claude-0/rt/hv/ear/fam6'; HP = '/tmp/claude-0/rt/hv/hp'; EW = W + '/ear'; CAN = 'HE2'
FR = jl(EV + '/halvren_rp3_final/HALVREN_EAR_FAMILY_RP3_FREEZE.json'); ACC_CANON = '1a0b070b42e84846d1b7beebfd153fec8d1ddf4e5a1d2ecc54a0d4351549a779'; ACC_FACE = 'f8367ab09385d218559b6d3cac52ed159a9249cf12d91807e93e3b095d9ac297'
CFG = {'c1': ('HVC1-HB2HF2-HPB', 'HV_M_REF_RP3_v001', 'MF-M-R'), 'c2': ('HVF178-HB2HF2-HPB', 'HV_F_REF_RP3_v001', 'MF-F-R')}
G = dict(order='reviews/chatgpt-rac-rp3-halvren-final-whole-character-consolidation-freeze-readiness-order.md (2026-10-30, fd22665)', work=W, configurations={}); DS = {}
HE = jl(W + '/he/HV_hidden_ear_identity_final.json'); EX = jl(W + '/gates/HV_final_expression_sanity.json'); EXR = jl(EV + '/halvren_rp3_body_face_source/expression/HV_expression_sanity.json')
HPBV = jl(HPV + '/HV_HPB_validation.json')
for c, (h, nm, mf) in CFG.items():
    g = {}; P = np.load('%s/build/%s_%s_branch.npz' % (EW, h, CAN)); F = np.load('%s/fam/%s_fam.npz' % (W, h)); bj = jl('%s/build/%s_%s_branch.json' % (EW, h, CAN))
    R2 = np.load('%s/build/%s_%s_branch.npz' % (ACCE, h, CAN)); mem = FR['members']['HE2 %s' % c]
    v_ = P['v005_to_branch']; ok_ = (v_ >= 0); ok_[ok_] = P['part'][v_[ok_]] == 'v005'
    rc = jl('%s/src/%s_regen_check.json' % (W, h)); full = np.load('%s/full/%s_r6.npz' % (W, h)); com = np.load('%s/r6/%s_r6.npz' % (RA, h))
    mfull = jl('%s/full/%s_meas.json' % (W, h)); mcom = jl('%s/builds/%s_meas.json' % (RA, h)); tri = jl('%s/tri/HE2_%s_prodtri.json' % (W, c))
    Vsha = hashlib.sha256(P['V'].astype(np.float32).tobytes()).hexdigest(); Qsha = hashlib.sha256(np.ascontiguousarray(P['Q']).astype(np.int64).tobytes()).hexdigest()
    g['rebuild'] = dict(committed_r6_sha256=sha('%s/r6/%s_r6.npz' % (RA, h)), build_sha256=sha('%s/builds/%s_build.json' % (RA, h)),
                        regen_geometry_identical=rc['geometry_identical'], regen_max_abs_dV_cm=rc['max_abs_dV_cm'], regen_geometry_hash=rc['regen_geom'], committed_geometry_hash=rc['committed_geom'],
                        full_record_rebuild_max_abs_dV_cm=float(np.abs(full['V'].astype(float) - com['V'].astype(float)).max()), full_record_faces_identical=bool(np.array_equal(full['F'], com['F'])),
                        full_record_meas_equals_committed=bool(mfull['combined'] == mcom['combined']),
                        family_realization_sha256=sha('%s/fam/%s_fam.npz' % (W, h)), family_equals_accepted_hpe=bool(sha('%s/fam/%s_fam.npz' % (W, h)) == sha('%s/fam/%s_fam.npz' % (ACCF, h))),
                        he2_V_float32_sha256=Vsha, he2_Q_sha256=Qsha, he2_equals_frozen_record=Vsha == mem['V_float32_sha256'] and Qsha == mem['Q_sha256'],
                        he2_arrays_equal_approved_build=bool(all(np.array_equal(P[k], R2[k]) for k in P.files)), he2_guard_iterations=len(jl('%s/build/%s_%s_deform_guard_log.json' % (EW, h, CAN))),
                        tri_hv1_recomputed_sha256=tri['triangulation']['triangles_sha256'], tri_hv1_equals_frozen=tri['triangulation']['triangles_sha256'] == mem['tri_hv1_triangles_sha256'],
                        tri_hv1_step5_flips=tri['intersection_validation']['flipped_quads'], tri_hv1_final_crossings=tri['intersection_validation']['final_crossings'],
                        params_equal_frozen_definition=bj['params'] == jl('%s/build/%s_%s_branch.json' % (ACCE, h, CAN))['params'],
                        face_topology_sha256=hashlib.sha256(np.asarray(P['Q']).astype(np.int32).tobytes()).hexdigest(),
                        cuff_canon_sha256=sha(EW + '/canon_branch_topology.json'), cuff_canon_equals_accepted=sha(EW + '/canon_branch_topology.json') == ACC_CANON,
                        outside_branch_equals_family=bool(np.array_equal(P['V'][P['v005_to_branch'][ok_]], F['V'][ok_])), transition_ring_vertices=int((P['part'] == 'transition').sum()))
    g['rebuild']['face_topology_equals_accepted'] = g['rebuild']['face_topology_sha256'] == ACC_FACE
    g['production'] = dict(sidecar=jl('%s/prod/%s.json' % (W, nm)), readback_local=jl('%s/readback_local/%s_readback.json' % (W, nm)), tri_readback_local=jl('%s/readback_local/%s_tri_readback.json' % (W, nm)),
                           second_write=dict((k, jl('%s/prod2/%s.json' % (W, nm))[k] == jl('%s/prod/%s.json' % (W, nm))[k]) for k in ('geometry_hash', 'face_topology_hash', 'branch_map_sha256', 'tri_hv1_triangles_sha256', 'landmarks_sha256')))
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
                          root_seam=dict(boundary=ea['boundary_edges'], clearance_min_cm=ea['ear_to_head_clearance']['min_cm']), stature_bbox=au.get('bbox_cm') or au.get('stature_cm'))
    va = jl('%s/val/%s_final_validator_v2_D1-D6.json' % (W, h)); vf = jl('%s/val/%s_fam_validator_v2_D1-D6.json' % (W, h)); vr = jl('%s/val/%s_fam_validator_v2_D1-D6.json' % (ACCF, h))
    same = [s for s in va['stations'] if all(va['stations'][s][k] == vf['stations'][s][k] for k in ('loops_v2', 'margin', 'valid_sides', 'D5_undefined_sides', 'D6_undefined_sides'))]
    lab = {s: [vf['stations'][s]['status_D1_D3'], va['stations'][s]['status_D1_D3']] for s in va['stations'] if va['stations'][s]['status_D1_D3'] != vf['stations'][s]['status_D1_D3']}
    g['validator'] = dict(rules='D1 + D3 + D4 + D5 + D6 (validator_v2.py --scale-ref 173.143 --d5 --d6-native)', firm=va['summary']['firm_pass_count'], stations=va['summary']['stations'], firm_fail=va['summary']['D1_D3_firm_fail'],
                          margin_zero=va['summary']['margin_zero'], family_firm=vf['summary']['firm_pass_count'], stations_identical_to_family=len(same), status_label_differences_vs_family=lab,
                          family_equals_accepted=bool(vf['stations'] == vr['stations']))
    an = jl('%s/anat/%s_final_anatomy_earexcl.json' % (W, h)); a0 = jl('%s/anat/%s_final_anatomy.json' % (W, h)); fa = jl('%s/anat/%s_fam_anatomy.json' % (W, h))
    g['anatomy'] = dict(final_ear_excluded=dict(T1=an['T1_pass'], T2=an['T2_pass'], T3=an['T3_pass'], T7=an['T7_pass'], stature_diff_mm=an['stature_diff_mm'], bbox_diff_mm=an['bbox_diff_mm'], iou=an['silhouette_iou']),
                        final_unmasked_anatomy_py=dict(T1_T2=a0['T1_T2_pass'], T3=a0['T3_pass'], T7=a0['T7_pass'], failing=[k for k in ('T1_T2_pass', 'T3_pass', 'T7_pass') if not a0[k]],
                                                       ears_prod_to_source=a0['deviation_prod_to_source']['ears'], body=a0['deviation_prod_to_source']['body'], head=a0['deviation_prod_to_source']['head'],
                                                       classification='expected source-vs-new-ear divergence localised to the ear (R-6 source carries the MPFB human auricle; production carries HE2 / HR2)'),
                        family_anatomy_py=dict(T1_T2=fa['T1_T2_pass'], T3=fa['T3_pass'], T7=fa['T7_pass']))
    ev = jl('%s/gates/HV_final_eval_%s.json' % (W, c))['items']['HB2HF2-HPB']; er = jl('%s/HPB_eval_%s.json' % (HPV, c))['items']['HB2HF2-HPB']
    bd, fc = ev['body'], ev['face']
    g['body_face_regression'] = dict(body_equals_accepted_HPB_eval=bool(ev['body'] == er['body']), face_equals_accepted_HPB_eval=bool(ev['face'] == er['face']), stature_equal=ev['stature'] == er['stature'],
                                     body=dict(material_vs={s: v['material'] for s, v in bd['source_protection'].items()}, groups_with_signal_vs_MF=bd['groups_with_signal_vs_MF'], scalar_blend_firewall=bd['scalar_blend_firewall'],
                                               distinct_from_elves=bd['distinct_from_elves']),
                                     face=dict(regions_departing_from_MF=fc.get('regions_departing_from_MF'), regions_distinct_from=fc.get('regions_distinct_from'), anti_beauty_vs_MF_pct=fc.get('anti_beauty_indicators_vs_MF_pct')),
                                     meas_equals_committed=g['rebuild']['full_record_meas_equals_committed'])
    sk1 = jl('%s/skp/%s_skp.json' % (W, h)); sk0 = jl('%s/skp/%s_skp.json' % (HP, h)); hv = HPBV['sources'][h]
    g['pelvis_regression'] = dict(skeletal_proxy_equals_accepted_HPB=bool(sk1 == sk0), accepted_skeletal_proxy_t05=hv['skeletal_proxy_t05'], hip_joint_leg_share_vs_MF_pct=hv['hip_joint_height_leg_share_vs_MF_pct'],
                                  accepted_verdict=HPBV['verdict'][h], lean_r6_equal=bool(np.array_equal(np.load('%s/lean/%s-LEAN_r6.npz' % (W, h))['V'], np.load('%s/lean/%s-LEAN_r6.npz' % (HP, h))['V'])) if os.path.exists('%s/lean/%s-LEAN_r6.npz' % (HP, h)) else None)
    he = HE['configs'][c]
    g['hidden_ear'] = dict(body_regions=he['body'], face_systems_material=he.get('systems_material'), face_systems_direction_ok=he.get('systems_direction_ok'), of=he.get('of'), guards=he.get('guards'),
                           note='ears excluded / collapsed (hm08 w_ears > 0.05); the accepted HB2 + HF2 + HP-B ear-excluded body / face gates are the HPB_eval rows (equal above)')
    fr = jl('%s/audit/%s_final_face.json' % (W, h)); ff = jl('%s/audit/%s_fam_face.json' % (W, h))
    KF = ('poles_at_mouth_corners', 'poles_within_2cm_of_mouth', 'poles_within_2cm_of_eye_l', 'poles_within_2cm_of_eye_r', 'mouth_pass', 'orbit_pass')
    g['face_topology'] = dict(mouth_rings=fr['mouth_rings']['count'], orbit_rings=[fr['orbit_rings_l']['count'], fr['orbit_rings_r']['count']], poles_at_mouth_corners=fr['poles_at_mouth_corners'], poles_within_2cm_of_mouth=fr['poles_within_2cm_of_mouth'],
                              poles_within_2cm_of_eyes=[fr['poles_within_2cm_of_eye_l'], fr['poles_within_2cm_of_eye_r']], mouth_pass=fr['mouth_pass'], orbit_pass=fr['orbit_pass'], face_density_pct=au['density_pct_of_stature']['face'],
                              equals_family=bool(all(fr[k] == ff[k] for k in KF) and fr['mouth_rings']['count'] == ff['mouth_rings']['count'] and fr['orbit_rings_l']['count'] == ff['orbit_rings_l']['count'] and fr['orbit_rings_r']['count'] == ff['orbit_rings_r']['count']),
                              expressions=EX['bodies'][h], expressions_accepted=EXR['bodies'].get(h), expressions_equal_accepted=EXR['bodies'].get(h) == EX['bodies'][h] if h in EXR['bodies'] else 'accepted record has no HP-B entry')
    em = jl('%s/meas/%s_%s_measure.json' % (EW, h, CAN)); em0 = jl('%s/meas/%s_%s_measure.json' % (ACCE, h, CAN)); ed = jl('%s/deform/%s_%s_deform.json' % (EW, h, CAN)); ea0 = jl('%s/audit/%s_%s_audit.json' % (ACCE, h, CAN))
    g['ear'] = dict(definition='HE2 HVEAR3 + HR2 (frozen central production ear)', T4=ea['T4']['angle_violations'], aspect_max=ea['T4']['aspect_max'], min_angle=ea['T4']['min_angle'], density=ea['density'],
                    clearance=ea['ear_to_head_clearance'], outside_branch_byte_identical=ea['outside_branch_byte_identical'], audit_equals_approved=bool(ea['T4'] == ea0['T4'] and ea['root_valence'] == ea0['root_valence']),
                    measures_equal_approved=bool(em == em0), deform={p: [v['new_selfx_pairs_touching_branch'], v['flipped_branch_faces'], v['root_band_inverted']] for p, v in ed['poses'].items()},
                    firewall_frozen='R2 0.51 / 0.44 / 0.23 (MF <-> Fenn / Aelari / Vael): arrays identical to the frozen HE2, so the measured firewall is unchanged')
    g['density'] = dict(zones={k: dict(mean=v['mean'], limit=v['limit'], pass_=v['pass_mean']) for k, v in au['density_pct_of_stature'].items()}, all_pass=all(v['pass_mean'] for v in au['density_pct_of_stature'].values()),
                        ear_branch_mean_pct=ea['density']['branch_mean_edge_pct_stature'], zones_differing_from_family=[k for k in au['density_pct_of_stature'] if au['density_pct_of_stature'][k] != af['density_pct_of_stature'][k]])
    dn = jl('%s/def/deform_%s_native.json' % (W, h)); dfm = jl('%s/def/deform_%s_fam.json' % (W, h)); dp = jl('%s/def/deform_%s_final.json' % (W, h)); dm = jl('%s/deform_%s_v005.json' % (MFD, mf))
    dr = jl('%s/def/deform_%s_fam.json' % (ACCF, h)); P_ = {}
    for p in dp['poses']:
        P_[p] = dict(final_flipped=dp['poses'][p]['flipped_faces'], family_flipped=dfm['poses'][p]['flipped_faces'], native_flipped=dn['poses'][p]['flipped_faces'], marchfolk_v005_flipped=dm['poses'][p]['flipped_faces'],
                     final_new_selfx=dp['poses'][p]['new_selfx_pairs'], family_new_selfx=dfm['poses'][p]['new_selfx_pairs'], marchfolk_new_selfx=dm['poses'][p]['new_selfx_pairs'], final_new_folds=dp['poses'][p]['new_folds'], family_new_folds=dfm['poses'][p]['new_folds'])
    DS[c] = dict(head=h, reference_marchfolk=mf + ' v005', poses=P_, final_minus_family_flipped_max=max(v['final_flipped'] - v['family_flipped'] for v in P_.values()),
                 final_minus_family_selfx_max=max(v['final_new_selfx'] - v['family_new_selfx'] for v in P_.values()), final_minus_marchfolk_flipped_max=max(v['final_flipped'] - v['marchfolk_v005_flipped'] for v in P_.values()),
                 poses_worse_than_family=[p for p, v in P_.items() if v['final_flipped'] > v['family_flipped'] or v['final_new_selfx'] > v['family_new_selfx'] or v['final_new_folds'] > v['family_new_folds']],
                 family_equals_accepted={p: dfm['poses'][p]['flipped_faces'] == dr['poses'][p]['flipped_faces'] and dfm['poses'][p]['new_selfx_pairs'] == dr['poses'][p]['new_selfx_pairs'] for p in dfm['poses']},
                 excess_over_marchfolk_gt5={p: v['final_flipped'] - v['marchfolk_v005_flipped'] for p, v in P_.items() if v['final_flipped'] - v['marchfolk_v005_flipped'] > 5})
    worse = {}
    for p in DS[c]['poses_worse_than_family']:
        X = np.load('%s/def/%s_%s_final.npz' % (W, p, h)); fe = X['fold'] if 'fold' in X.files else np.zeros((0, 2), int)
        worse[p] = dict(new_fold_face_pairs=np.asarray(fe).tolist(), parts=[sorted(set(P['part'][Qp[f]].tolist())) for f in np.asarray(fe).ravel()], sides=[sorted(set(P['side'][Qp[f]].tolist())) for f in np.asarray(fe).ravel()],
                        edge_lengths_mm=[np.round(10 * np.linalg.norm(P['V'][Qp[f]] - np.roll(P['V'][Qp[f]], -1, 0), axis=1), 3).tolist() for f in np.asarray(fe).ravel()])
    DS[c]['worse_than_family_detail'] = worse
    g['deformation'] = dict(standard_v1=DS[c], ear_readiness=dict(poses=list(ed['poses']), all_zero=all(v[0] == 0 and v[1] == 0 and v[2] == 0 for v in g['ear']['deform'].values())),
                            ear_on_tri_hv1=dict(contacts=sum(v['new_contacts'] for v in tri['poses'].values()), triangle_inversions=sum(v['triangle_inversions'] for v in tri['poses'].values()),
                                                root_inversions=sum(v['root_band_triangle_inversions'] for v in tri['poses'].values())))
    G['configurations'][c] = g
json.dump(G, open(os.path.join(O, 'HALVREN_FINAL_gates.json'), 'w'), indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
json.dump(DS, open(os.path.join(O, 'HALVREN_FINAL_deformation_summary.json'), 'w'), indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
for c, g in G['configurations'].items():
    r = g['rebuild']; print(c, 'regen', r['regen_geometry_identical'], r['regen_max_abs_dV_cm'], 'full', r['full_record_rebuild_max_abs_dV_cm'], r['full_record_meas_equals_committed'], 'fam=acc', r['family_equals_accepted_hpe'],
          'HE2=frozen', r['he2_equals_frozen_record'], r['he2_arrays_equal_approved_build'], 'TRI', r['tri_hv1_equals_frozen'], 'topo', r['face_topology_equals_accepted'], 'canon', r['cuff_canon_equals_accepted'], 'outside', r['outside_branch_equals_family'])
    i = g['integrity']; print('  int', i['verts'], i['quads'], i['components'], i['boundary_edges'], i['nonmanifold_edges'], i['nonmanifold_vertices'], i['degenerate_faces'], i['winding_consistent'], i['normals_outward'], 'SI=fam', i['contact_pairs_equal_family_set'], 'brSI', i['branch_self_intersections'], 'cls', i['family_contact_class'])
    print('  val', g['validator']['firm'], '/', g['validator']['stations'], 'same', g['validator']['stations_identical_to_family'], 'fam=acc', g['validator']['family_equals_accepted'], '| anat', [g['anatomy']['final_ear_excluded'][k] for k in ('T1', 'T2', 'T3', 'T7')], g['anatomy']['final_unmasked_anatomy_py']['failing'])
    print('  body/face', g['body_face_regression']['body_equals_accepted_HPB_eval'], g['body_face_regression']['face_equals_accepted_HPB_eval'], '| pelvis', g['pelvis_regression']['skeletal_proxy_equals_accepted_HPB'], g['pelvis_regression']['lean_r6_equal'], '| face', g['face_topology']['mouth_pass'], g['face_topology']['orbit_pass'], g['face_topology']['equals_family'], g['face_topology']['expressions_equal_accepted'])
    print('  ear', g['ear']['T4'], g['ear']['audit_equals_approved'], g['ear']['measures_equal_approved'], 'dens', g['density']['all_pass'], '| def', DS[c]['final_minus_family_flipped_max'], DS[c]['final_minus_family_selfx_max'], DS[c]['poses_worse_than_family'], DS[c]['excess_over_marchfolk_gt5'], all(DS[c]['family_equals_accepted'].values()), '| earready', g['deformation']['ear_readiness']['all_zero'], g['deformation']['ear_on_tri_hv1'])
    print('  prod', g['production']['readback_local']['faces_equal_candidate'], g['production']['tri_readback_local']['equals_sidecar_hash'], g['production']['second_write'])
