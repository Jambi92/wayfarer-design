# ae_freeze_record.py WORK EVIDIR : Aelari final consolidation (order 2026-10-28) §22 -- writes AELARI_RP3_FREEZE.json (freeze by record; the production
# blends are not re-saved). Reads AELARI_RP3_freeze_readback.json (ae_freeze_verify.py on the PC copies) and AELARI_FINAL_gates.json (ae_final_gates.py).
import sys, json, hashlib
W, E = sys.argv[1:3]; sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest(); REPO = '/home/claude/wayfarer-design'; RA = REPO + '/reviews/reference-assets'
EV2 = REPO + '/reviews/rac-rp3-evidence/fenn_ear_v002'; FZ = REPO + '/reviews/rac-rp3-evidence/fenn_rp3_freeze/FENN_RP3_FREEZE.json'
RB = json.load(open(E + '/AELARI_RP3_freeze_readback.json')); G = json.load(open(E + '/AELARI_FINAL_gates.json')); F5 = REPO + '/reviews/rac-rp3-evidence/mpfb_family_base_v005_freeze/MPFB_FAMILY_BASE_v005_FREEZE.json'
B5 = '/mnt/user-data/outputs/rp5'; T2 = json.load(open(EV2 + '/topology/FENN_EAR_BRANCH_TOPOLOGY_v002.json')); FR = json.load(open(FZ))
c1 = G['configurations']['c1']
rec = dict(record='AELARI RP3 FINAL PASS — AUTHOR ACCEPTED / FROZEN', date='2026-10-28',
           authority='reviews/chatgpt-rac-rp3-aelari-final-consolidation-freeze-order.md (author review of Claude return 7d2f734)',
           freeze_method='freeze-by-record: both production .blend files are preserved byte-identical (not re-saved); this record is authoritative over the sidecar / embedded RAC_status strings',
           family_base=dict(record='MPFB_FAMILY_BASE_v005_FREEZE.json', record_sha256=sha(F5), blend='MF_M_REF_RP3_retopo_v005.blend', blend_sha256=sha(B5 + '/MF_M_REF_RP3_retopo_v005.blend'),
                            hm08_map='MF_M_REF_RP3_retopo_v005_hm08_map.npz', hm08_map_sha256=sha(B5 + '/MF_M_REF_RP3_retopo_v005_hm08_map.npz'), face_topology_hash='ec768ae210ea3ee1c053d0c4cd3256d57dad6db35d515502706b74f64281bee0',
                            verts=57842, quads=57840, unchanged=True, note='active family base unchanged; Aelari uses it everywhere outside the ear branch'),
           ear_branch=dict(description='accepted Aelari-specific external-ear branch = AE-E2 Aelari geometry + reused Fenn ear topology v002 (ENGINEERING TOPOLOGY ONLY; not a universal elf ear topology, not Fenn ear geometry)',
                           geometry='AE-E2 (W1e AE-elven; accepted as the canonical central Aelari ear, order 2026-10-28 §1.5)', params=c1['rebuild']['params'],
                           engineering_topology='FENN_EAR_BRANCH_TOPOLOGY_v002 (frozen with Fenn, 6d2eadc; reuse accepted 2026-10-28 §1.6)', topology_json_sha256=sha(EV2 + '/topology/FENN_EAR_BRANCH_TOPOLOGY_v002.json'),
                           topology_npz_sha256=sha(EV2 + '/topology/FENN_EAR_BRANCH_TOPOLOGY_v002.npz'), cuff_canon_sha256=sha(EV2 + '/topology/FENN_EAR_BRANCH_CUFF_CANON_v002.json'),
                           map_v005_v002_npz_sha256=sha(EV2 + '/mapping/FENN_EAR_BRANCH_MAP_v005_v002.npz'), per_side=T2['per_side'], whole_mesh=T2['whole_mesh'],
                           face_list_equals_frozen_fenn=all(G['configurations'][c]['rebuild']['face_list_equals_frozen_fenn_v002'] for c in ('c1', 'c2')), shared_by='configuration 1 and configuration 2 (identical face list)'),
           lineage=dict(c1='AEL1 (ancestry, W1 accepted) -> AEL1-R1 (accepted corrected central body, 0f6aba8 / 2026-10-28 §1.1) -> AE_M_REF_RP3_v001',
                        c2='AELF190 (MF-F route + Aelari design, fd71f15) -> AELF190-R1 (accepted corrected central body) -> AE_F_REF_RP3_v001',
                        ear='AE-E2 geometry + reused Fenn-v002 engineering topology = accepted Aelari-specific external-ear branch',
                        body_correction=dict(spine_03_Y=[0.9704, 0.99], LR_thigh_Y=[0.9875, 1.01], LR_calf_Y=[1.0523, 1.03], height_macro='re-solved to ~190 cm')),
           references={n: dict(role=role, r6_sha256=sha(RA + '/r6/%s_r6.npz' % n), build_sha256=sha(RA + '/builds/%s_build.json' % n)) for n, role in
                       (('AEL1', 'configuration-1 ancestry (immutable)'), ('AELF190', 'configuration-2 ancestry (immutable)'), ('AEL1-R1', 'accepted configuration-1 central body source'), ('AELF190-R1', 'accepted configuration-2 central body source'))},
           fenn_comparison=dict(freeze_record='reviews/rac-rp3-evidence/fenn_rp3_freeze/FENN_RP3_FREEZE.json', freeze_record_sha256=sha(FZ), FN_M_REF_RP3_v001_sha256=FR['files']['FN_M_REF_RP3_v001.blend']['sha256'],
                                FN_F_REF_RP3_v001_sha256=FR['files']['FN_F_REF_RP3_v001.blend']['sha256'], comparators='FNM190 / FNF190 (frozen Fenn route at 190 cm, body comparisons); FNL4-CF2 E2 (visible-ear firewall)', unchanged=True),
           validator=dict(rules='D1 + D3 + D4 + D5 + D6 (authoritative)', implementation='tools/rac/rp/marchfolk_rp3_v001/validator_v2.py --scale-ref 173.143 --d5 --d6-native', files={}),
           files={}, accepted_diagnostic_notes=['skin wrist / knee / ankle gracility rows are diagnostic only (skin breadth unstable across the stature macro; order §19)',
                                                'unmasked anatomy.py T-1 / T-2 / T-7 differences are the expected source-vs-new-ear anatomy divergence (R-6 source carries the MPFB human auricle)',
                                                'accepted narrower R1 margins: leg share > MF ~+0.34 / +0.35 %, waist interval / torso > Fenn ~+1.33 % / +0.62 %',
                                                'ear branch faces carry a zero placeholder UV (UV / materials out of scope)'],
           carry_forward=dict(register='specs/RAC_PRODUCTION_RIG_CARRY_FORWARD_REGISTER.md', new_ids=[]),
           gates=dict(record='AELARI_FINAL_gates.json', report='reviews/claude-rac-rp3-aelari-final-freeze-report.md', parents=['reviews/claude-rac-rp3-aelari-body-face-ear-gate.md', 'reviews/claude-rac-rp3-aelari-body-source-correction-gate.md'],
                      firewall_all_hold=G['firewall']['all_hold'], probes_all_clean=c1['probes']['all_clean']),
           readback=dict(file='AELARI_RP3_freeze_readback.json', all_pass=RB['all_pass'], c1_c2_face_topology_identical=RB['c1_c2_face_topology_identical']),
           provenance=['AEL1-R1 / AELF190-R1 R-6 regenerated from reviews/reference-assets/builds (regen.py: geometry identical, max |dV| 0) and fully re-built from the record (max |dV| 0)', 'native hm08 export',
                       'propagate.py onto MPFB Family Base v005 -> family realization (byte-identical to the reviewed bodyfam_v002 candidate)',
                       'AE-E2 on the reused Fenn ear topology v002 from the committed cuff canon (run_ae_ear.sh; arrays identical to the reviewed corrected AE-E2 prototype)',
                       'fn_make_prod.py production frame (m, Z up, faces -Y, subject left +X, origin pelvis root on ground)', 'E: copies read back byte-identical; validator recomputed from the read-back candidate'],
           freezes=['Aelari RP3 configuration-1 / configuration-2 final production bodies', 'AE-E2 on the reused Fenn-v002 engineering topology as the accepted Aelari-specific external-ear branch'],
           not_done=['production ear rigging', 'creator morphs', 'final UV / materials', 'LODs', 'UE5 integration', 'Vael / Halvren (not started)', 'no universal elf anatomy / topology declared'])
for c, (h, nm) in (('c1', ('AEL1-R1', 'AE_M_REF_RP3_v001')), ('c2', ('AELF190-R1', 'AE_F_REF_RP3_v001'))):
    f = RB['files'][h]; g = G['configurations'][c]
    rec['files'][f['file']] = dict(race='Aelari', configuration=c, source=h, path='E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Aelari/RP3/' + f['file'], sha256=f['sha256'], geometry_hash=f['geometry_hash'],
                                   face_topology_hash=f['face_topology_hash'], verts=f['verts'], quads=f['quads'], sidecar=nm + '.json', sidecar_sha256=f['sidecar_sha256'], branch_map=nm + '_branch_map.npz', branch_map_sha256=f['branch_map_sha256'],
                                   landmarks=nm + '_landmarks.json', landmarks_sha256=f['landmarks_sha256'], embedded_status=f['embedded_status'], readback_all_pass=f['all_pass'], readback_validator=f['validator'],
                                   rebuild={k: g['rebuild'][k] for k in ('regen_geometry_identical', 'regen_max_abs_dV_cm', 'full_record_rebuild_max_abs_dV_cm', 'family_equals_reviewed_v002_candidate', 'branch_arrays_equal_reviewed_AE_E2', 'outside_branch_equals_family', 'face_list_equals_frozen_fenn_v002')},
                                   integrity={k: g['integrity'][k] for k in ('quads_pct', 'components', 'boundary_edges', 'nonmanifold_edges', 'nonmanifold_vertices', 'degenerate_faces', 'winding_consistent', 'normals_outward', 'coincident_vertex_pairs', 'self_intersection_pairs',
                                                                             'family_self_intersection_pairs', 'contact_pairs_equal_family_set', 'branch_self_intersections', 'root_valence_4')},
                                   validator=dict(firm=g['validator']['firm'], stations=g['validator']['stations'], margin_zero=g['validator']['margin_zero'], stations_identical_to_family=g['validator']['stations_identical_to_family']),
                                   anatomy=dict(T1=g['anatomy']['final_ear_excluded']['T1'], T2=g['anatomy']['final_ear_excluded']['T2'], T3=g['anatomy']['final_ear_excluded']['T3'], T7=g['anatomy']['final_ear_excluded']['T7'],
                                                unmasked_failing=g['anatomy']['final_unmasked_anatomy_py']['failing'], unmasked_classification=g['anatomy']['final_unmasked_anatomy_py']['classification'], identity_holds_all_zones=g['anatomy']['identity']['holds_all_zones']),
                                   body_identity=dict(pass_=g['body_identity']['pass_'], canon=g['body_identity']['canon_holds'], thoracic_vs_FN_pct=g['body_identity']['thoracic_vs_FN_pct'], shin_over_leg_gap_to_MF=g['body_identity']['shin_over_leg_gap_to_MF'], fenn_gap=g['body_identity']['fenn_shin_over_leg_gap_to_MF']),
                                   pelvis_all_rules_all_t=g['pelvis']['all_hold'], hidden_ear_face=dict(pass_=g['hidden_ear_face']['pass_'], systems_material=g['hidden_ear_face']['systems_material'], descriptors_equal_reviewed_R1=g['hidden_ear_face']['descriptors_equal_reviewed_R1']),
                                   face=dict(mouth_rings=g['face']['mouth_rings'], orbit_rings=g['face']['orbit_rings'], poles_at_mouth_corners=g['face']['poles_at_mouth_corners'], mouth_pass=g['face']['mouth_pass'], orbit_pass=g['face']['orbit_pass'], equals_family=g['face']['equals_family']),
                                   density=dict(all_9_zones_pass=g['density']['all_pass'], ear_branch_mean_pct_stature=g['density']['ear_branch_mean_pct']),
                                   ear=dict(T4=g['ear']['T4'], branch_faces=g['ear']['branch_faces'], T4_rate=round(g['ear']['T4_rate'], 4), aspect_max=g['ear']['aspect_max'], aspect_gt10=g['ear']['aspect_gt10'],
                                            root_crease_max_deg=max(v['max_deg'] for v in g['ear']['root_dihedral'].values()), measures_equal_reviewed=g['ear']['measures_equal_reviewed'], measures=g['ear']['measures']),
                                   deformation=dict(standard_v1_final_minus_family_flipped_max=g['deformation']['standard_v1']['final_minus_family_flipped_max'], standard_v1_final_minus_family_selfx_max=g['deformation']['standard_v1']['final_minus_family_selfx_max'],
                                                    standard_v1_poses_worse_than_family=g['deformation']['standard_v1']['poses_worse_than_family'], ear_readiness_all_zero=g['deformation']['ear_readiness']['all_zero']))
    rec['validator']['files'][f['file']] = '%d / %d' % (g['validator']['firm'], g['validator']['stations'])
ok = lambda v: all([v['readback_all_pass'], v['validator']['firm'] == 69, v['readback_validator']['firm'] == 69, v['anatomy']['T1'], v['anatomy']['T2'], v['anatomy']['T3'], v['anatomy']['T7'], v['anatomy']['identity_holds_all_zones'],
                    v['body_identity']['pass_'], v['pelvis_all_rules_all_t'], v['hidden_ear_face']['pass_'], v['face']['mouth_pass'], v['face']['orbit_pass'], v['face']['poles_at_mouth_corners'] == 0, v['density']['all_9_zones_pass'],
                    v['density']['ear_branch_mean_pct_stature'] <= 0.25, v['ear']['aspect_gt10'] == 0, v['integrity']['branch_self_intersections'] == 0, v['integrity']['contact_pairs_equal_family_set'], v['integrity']['root_valence_4'],
                    v['deformation']['ear_readiness_all_zero'], not v['deformation']['standard_v1_poses_worse_than_family'],
                    all(x for k_, x in v['rebuild'].items() if isinstance(x, bool)), v['rebuild']['regen_max_abs_dV_cm'] == 0, v['rebuild']['full_record_rebuild_max_abs_dV_cm'] == 0])
rec['all_gates_pass'] = all(ok(v) for v in rec['files'].values()) and rec['readback']['all_pass'] and rec['gates']['firewall_all_hold'] and rec['gates']['probes_all_clean'] and rec['ear_branch']['face_list_equals_frozen_fenn']
json.dump(rec, open(E + '/AELARI_RP3_FREEZE.json', 'w'), indent=1); print('freeze record', rec['all_gates_pass'], {k: ok(v) for k, v in rec['files'].items()}, sha(E + '/AELARI_RP3_FREEZE.json'))
