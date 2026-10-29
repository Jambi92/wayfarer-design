# va_freeze_record.py WORK EVIDIR : Vael final consolidation / freeze order §23 -- writes VAEL_RP3_FREEZE.json (freeze by record; the production blends
# are not re-saved). Reads VAEL_RP3_freeze_readback.json (va_freeze_verify.py on the PC copies) and VAEL_FINAL_gates.json (va_final_gates.py).
import sys, os, json, hashlib
W, E = sys.argv[1:3]; sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest(); REPO = '/home/claude/wayfarer-design'; RA = REPO + '/reviews/reference-assets'; EVD = REPO + '/reviews/rac-rp3-evidence'
EVR = EVD + '/vael_rp3_ear_root_integration'; EVF = EVD + '/vael_rp3_elf_frame'; FZF = EVD + '/fenn_rp3_freeze/FENN_RP3_FREEZE.json'; FZA = EVD + '/aelari_rp3_freeze/AELARI_RP3_FREEZE.json'
RB = json.load(open(E + '/VAEL_RP3_freeze_readback.json')); G = json.load(open(E + '/VAEL_FINAL_gates.json')); F5 = EVD + '/mpfb_family_base_v005_freeze/MPFB_FAMILY_BASE_v005_FREEZE.json'
B5 = '/mnt/user-data/outputs/rp5'; T2 = json.load(open(EVR + '/topology/VAEL_EAR_BRANCH_TOPOLOGY_v002.json')); FF = json.load(open(FZF)); FA = json.load(open(FZA)); c1 = G['configurations']['c1']
VDEF = json.load(open(EVF + '/VF_definitions.json')); VDD = json.load(open(EVD + '/vael_rp3_custom_deformation/VD_definitions.json')); VC = EVD + '/vael_rp3_source/vb_vc_definitions/iter2_3'
refs = {}
for n, role in (('VAL4', 'configuration-1 ancestry (immutable)'), ('VALF178', 'configuration-2 route ancestry (immutable)'), ('VAL4-R1', 'R1 = VB2g body + VC2 face (configuration 1)'), ('VALF178-R1', 'R1 = VB2g body + VC2 face (configuration 2)'),
                ('VAL4-R1-VD2', 'VD2 custom body deformation (VDF1.2)'), ('VALF178-R1-VD2', 'VD2 custom body deformation (VDF1.2)'), ('VAL4-R1-VD2-VF2', 'accepted final configuration-1 body source (VD2 + VEF1 elf frame VF2)'),
                ('VALF178-R1-VD2-VF2', 'accepted final configuration-2 body source (VD2 + VEF1 elf frame VF2)')):
    r6, bj = RA + '/r6/%s_r6.npz' % n, RA + '/builds/%s_build.json' % n
    if os.path.exists(r6) or os.path.exists(bj): refs[n] = dict(role=role, r6_sha256=sha(r6) if os.path.exists(r6) else None, build_sha256=sha(bj) if os.path.exists(bj) else None)
rec = dict(record='VAEL RP3 FINAL PASS — AUTHOR ACCEPTED / FROZEN', date='2026-10-28',
           authority='reviews/chatgpt-rac-rp3-vael-final-consolidation-freeze-order.md (author review of Claude return f25b345)',
           freeze_method='freeze-by-record: both production .blend files are preserved byte-identical (not re-saved); this record is authoritative over the sidecar / embedded RAC_status strings',
           family_base=dict(record='MPFB_FAMILY_BASE_v005_FREEZE.json', record_sha256=sha(F5), blend='MF_M_REF_RP3_retopo_v005.blend', blend_sha256=sha(B5 + '/MF_M_REF_RP3_retopo_v005.blend'),
                            hm08_map='MF_M_REF_RP3_retopo_v005_hm08_map.npz', hm08_map_sha256=sha(B5 + '/MF_M_REF_RP3_retopo_v005_hm08_map.npz'), face_topology_hash='ec768ae210ea3ee1c053d0c4cd3256d57dad6db35d515502706b74f64281bee0',
                            verts=57842, quads=57840, unchanged=True, note='active family base unchanged; Vael uses it everywhere outside the ear branch'),
           ear_branch=dict(description='accepted Vael-specific external-ear branch = VA-E2 Vael ear geometry + RI3 root / concha integration on VAEL_EAR_BRANCH_TOPOLOGY_v002 (a Vael-specific local cuff derivative of the Fenn / Aelari engineering topology; ENGINEERING TOPOLOGY ONLY, not a universal elf ear topology)',
                           geometry='VA-E2 (W1V) with RI3 (geo clear -0.30, skin-hugging six-ring cuff, presmooth 0)', params=c1['rebuild']['params'], geo=c1['rebuild']['geo'],
                           topology='VAEL_EAR_BRANCH_TOPOLOGY_v002', topology_json_sha256=sha(EVR + '/topology/VAEL_EAR_BRANCH_TOPOLOGY_v002.json'), topology_npz_sha256=sha(EVR + '/topology/VAEL_EAR_BRANCH_TOPOLOGY_v002.npz'),
                           cuff_canon='VAEL_EAR_CUFF_CANON_v001.json', cuff_canon_sha256=sha(EVR + '/topology/VAEL_EAR_CUFF_CANON_v001.json'), map_v005_v002_npz_sha256=sha(EVR + '/mapping/VAEL_EAR_BRANCH_MAP_v005_v002.npz'),
                           per_side=T2.get('per_side'), whole_mesh=T2.get('whole_mesh'), face_topology_sha256=c1['rebuild']['face_topology_sha256'],
                           face_topology_identical_c1_c2=G['configurations']['c1']['rebuild']['face_topology_sha256'] == G['configurations']['c2']['rebuild']['face_topology_sha256'], shared_by='configuration 1 and configuration 2 (identical face list)'),
           lineage=dict(c1='VAL4 ancestry -> R1 (VB2g + VC2) -> VD2 (VDF1.2) -> VF2 (VEF1) -> VA_M_REF_RP3_v001', c2='VALF178 route -> R1 (VB2g + VC2) -> VD2 (VDF1.2) -> VF2 (VEF1) -> VA_F_REF_RP3_v001',
                        ear='VA-E2 -> RI3 -> VAEL_EAR_BRANCH_TOPOLOGY_v002'),
           references=refs,
           definitions=dict(VDF1_2_VEF1=dict(file='reviews/rac-rp3-evidence/vael_rp3_elf_frame/VF_definitions.json', file_sha256=sha(EVF + '/VF_definitions.json'), definition_sha256=VDEF['definition_sha256'],
                                             module=VDEF['module'], module_sha256=VDEF['module_sha256'], versions=[VDEF['definition']['version'], VDEF['definition']['vef']['version']], VF2_magnitude=VDEF['candidates'].get('VF2')),
                            VDF1_2_VD=dict(file='reviews/rac-rp3-evidence/vael_rp3_custom_deformation/VD_definitions.json', file_sha256=sha(EVD + '/vael_rp3_custom_deformation/VD_definitions.json'), definition_sha256=VDD['definition_sha256']),
                            VC2=dict(note='VC2 face (iteration 3 final) carried unchanged from R1 through VD2 / VF2 into production', VC_definitions_final_sha256=sha(VC + '/VC_definitions_final.json'),
                                     c1_VB2gVC2_sha256=sha(VC + '/c1_VB2gVC2.json'), c2_VB2gVC2_sha256=sha(VC + '/c2_VB2gVC2.json'))),
           frozen_comparisons=dict(fenn=dict(freeze_record='reviews/rac-rp3-evidence/fenn_rp3_freeze/FENN_RP3_FREEZE.json', freeze_record_sha256=sha(FZF), FN_M_REF_RP3_v001_sha256=FF['files']['FN_M_REF_RP3_v001.blend']['sha256'],
                                             FN_F_REF_RP3_v001_sha256=FF['files']['FN_F_REF_RP3_v001.blend']['sha256'], comparators='FNM178 / FNF178 (frozen Fenn route at 178 cm, body / face); FNL4-CF2 / FNF181-CF2 E2 (visible-ear firewall)', unchanged=True),
                                   aelari=dict(freeze_record='reviews/rac-rp3-evidence/aelari_rp3_freeze/AELARI_RP3_FREEZE.json', freeze_record_sha256=sha(FZA), AE_M_REF_RP3_v001_sha256=FA['files']['AE_M_REF_RP3_v001.blend']['sha256'],
                                               AE_F_REF_RP3_v001_sha256=FA['files']['AE_F_REF_RP3_v001.blend']['sha256'], comparators='AEM178 / AEF178 (frozen Aelari route at 178 cm); AEL1-R1 / AELF190-R1 AE-E2 (visible-ear firewall)', unchanged=True)),
           validator=dict(rules='D1 + D3 + D4 + D5 + D6 (authoritative)', implementation='tools/rac/rp/marchfolk_rp3_v001/validator_v2.py --scale-ref 173.143 --d5 --d6-native', files={}),
           files={},
           accepted_residuals=dict(c1_standoff=dict(note='c1 mean / tip normalised free-ear stand-off a few thousandths HH above frozen Fenn (order §2; accepted secondary measurement residual; RI3 not deformed to chase it)',
                                                    measured=G['ear_firewall']['configs']['c1']['standoff_residual'], c2=G['ear_firewall']['configs']['c2']['standoff_residual'])),
           accepted_diagnostic_notes=['unmasked anatomy.py differences are the expected source-vs-new-ear divergence localised to the ear (R-6 source carries the MPFB human auricle; production carries VA-E2-RI3)',
                                      'hidden-ear 7-system face read: 5 of 7 material in c1 (the jaw / mandible guard reading is the accepted VF2 result); the order face gate (6 / 6 systems, 9 / 9 elf rows) is the va2_eval record',
                                      'VA-P2c and VA-P3 pelvis rows are report-only (as accepted); gating 9 / 9',
                                      'ear branch faces carry a zero placeholder UV (UV / materials out of scope)'],
           carry_forward=dict(register='specs/RAC_PRODUCTION_RIG_CARRY_FORWARD_REGISTER.md', carried=['VAEL-CF-SHOULDER-1'], new_ids=[],
                              VAEL_CF_SHOULDER_1={c: dict(shoulder_flex90_final=G['configurations'][c]['deformation']['standard_v1']['poses']['shoulder_flex90_l']['final_flipped'],
                                                          family=G['configurations'][c]['deformation']['standard_v1']['poses']['shoulder_flex90_l']['family_flipped'],
                                                          marchfolk_v005=G['configurations'][c]['deformation']['standard_v1']['poses']['shoulder_flex90_l']['marchfolk_v005_flipped']) for c in ('c1', 'c2')}),
           gates=dict(record='VAEL_FINAL_gates.json', report='reviews/claude-rac-rp3-vael-final-freeze-report.md',
                      parents=['reviews/claude-rac-rp3-vael-ear-root-integration-gate.md', 'reviews/claude-rac-rp3-vael-ear-prototype-gate.md', 'reviews/claude-rac-rp3-vael-elf-frame-human-firewall-gate.md'],
                      ear_firewall_all_hold=G['ear_firewall']['all_hold'], probes_all_clean=c1['probes']['all_clean'], probes=c1['probes']['count']),
           readback=dict(file='VAEL_RP3_freeze_readback.json', all_pass=RB['all_pass'], c1_c2_face_topology_identical=RB['c1_c2_face_topology_identical'], validator='recomputed from the read-back geometry'),
           provenance=['VAL4-R1-VD2-VF2 / VALF178-R1-VD2-VF2 R-6 regenerated from reviews/reference-assets/builds (regen.py: geometry identical, max |dV| 0) and fully re-built from the record (max |dV| 0, measures equal)',
                       'native hm08 export', 'propagate.py onto MPFB Family Base v005 -> family realization (byte-identical to the reviewed VA_{M,F}_REF_RP3_bodyfam_v004)',
                       'VA-E2-RI3 on VAEL_EAR_BRANCH_TOPOLOGY_v002 from the committed cuff canon (run_va_ri.sh; arrays identical to the reviewed RI3, max |dV| 0, faces identical)',
                       'fn_make_prod.py production frame (m, Z up, faces -Y, subject left +X, origin pelvis root on ground)', 'E: copies read back byte-identical; validator recomputed from the read-back geometry'],
           freezes=['Vael RP3 configuration-1 / configuration-2 final production bodies', 'VA-E2-RI3 on VAEL_EAR_BRANCH_TOPOLOGY_v002 as the accepted Vael-specific external-ear branch'],
           not_done=['production ear rigging', 'creator morphs', 'final UV / materials', 'LODs', 'UE5 integration', 'low-light physiology (not decided)', 'Halvren (not started)', 'no universal elf anatomy / topology declared'])
for c, (h, nm) in (('c1', ('VAL4-R1-VD2-VF2', 'VA_M_REF_RP3_v001')), ('c2', ('VALF178-R1-VD2-VF2', 'VA_F_REF_RP3_v001'))):
    f = RB['files'][h]; g = G['configurations'][c]; ds = g['deformation']['standard_v1']
    rec['files'][f['file']] = dict(race='Vael', configuration=c, source=h, path='E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Vael/RP3/' + f['file'], sha256=f['sha256'], geometry_hash=f['geometry_hash'],
                                   face_topology_hash=f['face_topology_hash'], verts=f['verts'], quads=f['quads'], sidecar=nm + '.json', sidecar_sha256=f['sidecar_sha256'], branch_map=nm + '_branch_map.npz', branch_map_sha256=f['branch_map_sha256'],
                                   landmarks=nm + '_landmarks.json', landmarks_sha256=f['landmarks_sha256'], embedded_status=f['embedded_status'], readback_all_pass=f['all_pass'], readback_validator=f['validator_from_readback'],
                                   rebuild={k: g['rebuild'][k] for k in ('regen_geometry_identical', 'regen_max_abs_dV_cm', 'geometry_hash_equals_accepted', 'full_record_rebuild_max_abs_dV_cm', 'full_record_faces_identical', 'full_record_meas_equals_committed',
                                                                         'family_equals_reviewed_bodyfam_v004', 'branch_arrays_equal_reviewed_RI3', 'branch_max_abs_diff_vs_reviewed_cm', 'params_equal_reviewed', 'geo_equal_reviewed',
                                                                         'face_topology_equals_accepted', 'cuff_canon_equals_accepted', 'outside_branch_equals_family', 'committed_r6_equals_accepted', 'build_equals_accepted')},
                                   integrity={k: g['integrity'][k] for k in ('verts', 'quads', 'quads_pct', 'components', 'boundary_edges', 'nonmanifold_edges', 'nonmanifold_vertices', 'degenerate_faces', 'winding_consistent', 'normals_outward',
                                                                             'coincident_vertex_pairs', 'self_intersection_pairs', 'family_self_intersection_pairs', 'contact_pairs_equal_family_set', 'branch_self_intersections', 'root_valence_4')},
                                   validator=dict(firm=g['validator']['firm'], stations=g['validator']['stations'], margin_zero=g['validator']['margin_zero'], stations_identical_to_family=g['validator']['stations_identical_to_family'],
                                                  family_equals_reviewed_v004=g['validator']['family_equals_reviewed_v004']),
                                   anatomy=dict(T1=g['anatomy']['final_ear_excluded']['T1'], T2=g['anatomy']['final_ear_excluded']['T2'], T3=g['anatomy']['final_ear_excluded']['T3'], T7=g['anatomy']['final_ear_excluded']['T7'],
                                                unmasked_failing=g['anatomy']['final_unmasked_anatomy_py']['failing'], unmasked_localised_within_T1_outside_ear=g['anatomy']['final_unmasked_anatomy_py']['localised_within_T1_outside_ear'],
                                                unmasked_classification=g['anatomy']['final_unmasked_anatomy_py']['classification']),
                                   firewalls=dict(canon=g['vael_canon_firewalls']['canon'], canon_failing=g['vael_canon_firewalls']['canon_failing'], body_systems_vs_humans=g['vael_canon_firewalls']['body_systems_material_vs_humans'],
                                                  face_systems=g['vael_canon_firewalls']['face_systems_material'], elf_face_rows=g['vael_canon_firewalls']['elf_face_rows'], equals_accepted_VF2=g['vael_canon_firewalls']['equals_accepted_VF2']),
                                   pelvis=dict(gating=g['pelvis']['gating'], equals_accepted_VF2=g['pelvis']['equals_accepted_VF2']),
                                   hidden_ear=dict(face_systems_material='%d / %d' % (g['hidden_ear']['face_systems_material'], g['hidden_ear']['of']), direction_ok='%d / %d' % (g['hidden_ear']['face_systems_direction_ok'], g['hidden_ear']['of']),
                                                   equals_accepted_VF2=g['hidden_ear']['equals_accepted_VF2']),
                                   face=dict(mouth_rings=g['face']['mouth_rings'], orbit_rings=g['face']['orbit_rings'], poles_at_mouth_corners=g['face']['poles_at_mouth_corners'], mouth_pass=g['face']['mouth_pass'], orbit_pass=g['face']['orbit_pass'],
                                             equals_family=g['face']['equals_family'], expressions_equal_accepted_VF2=g['face']['expressions_equal_accepted_VF2']),
                                   density=dict(all_9_zones_pass=g['density']['all_pass'], ear_branch_mean_pct_stature=g['density']['ear_branch_mean_pct'], zones_differing_from_family=g['density']['zones_differing_from_family']),
                                   ear=dict(T4=g['ear']['T4'], branch_faces=g['ear']['branch_faces'], aspect_max=g['ear']['aspect_max'], aspect_gt10=g['ear']['aspect_gt10'], min_angle=g['ear']['min_angle'],
                                            root_crease_max_deg=max(v['max_deg'] for v in g['ear']['root_dihedral'].values()), measures_equal_reviewed=g['ear']['measures_equal_reviewed'], audit_equals_reviewed=g['root_integration']['audit_equals_reviewed'],
                                            root_concha=g['root_integration']['reviewed_root_concha']),
                                   deformation=dict(final_minus_family_flipped_max=ds['final_minus_family_flipped_max'], final_minus_family_selfx_max=ds['final_minus_family_selfx_max'], poses_worse_than_family=ds['poses_worse_than_family'],
                                                    excess_over_marchfolk_gt5=ds['excess_over_marchfolk_gt5'], worse_than_family_detail=ds['worse_than_family_detail'], family_equals_reviewed_v004=all(ds['family_equals_reviewed_v004'].values()), new_rest_contact_class=g['integrity']['family_contact_class']['new'],
                                                    ear_readiness_all_zero=g['deformation']['ear_readiness']['all_zero']))
    rec['validator']['files'][f['file']] = '%d / %d (read-back %d / %d)' % (g['validator']['firm'], g['validator']['stations'], f['validator_from_readback']['firm'], f['validator_from_readback']['stations'])
def ok(c, v):
    exc = set(v['deformation']['excess_over_marchfolk_gt5']) - ({'shoulder_flex90_l'} if c == 'c1' else set())
    return all([v['readback_all_pass'], v['validator']['firm'] == 69, v['readback_validator']['firm'] == 69, v['anatomy']['T1'], v['anatomy']['T2'], v['anatomy']['T3'], v['anatomy']['T7'], v['anatomy']['unmasked_localised_within_T1_outside_ear'],
                v['firewalls']['canon'] == '20 / 20', v['firewalls']['equals_accepted_VF2'], v['firewalls']['face_systems'] == '6 / 6', v['firewalls']['elf_face_rows'] == '9 / 9', v['pelvis']['gating'] == '9 / 9', v['pelvis']['equals_accepted_VF2'],
                v['hidden_ear']['equals_accepted_VF2'], v['face']['mouth_pass'], v['face']['orbit_pass'], v['face']['poles_at_mouth_corners'] == 0, v['face']['equals_family'], v['face']['expressions_equal_accepted_VF2'],
                v['density']['all_9_zones_pass'], v['density']['ear_branch_mean_pct_stature'] <= 0.25, v['ear']['aspect_gt10'] == 0, v['ear']['aspect_max'] < 10, v['ear']['measures_equal_reviewed'], v['ear']['audit_equals_reviewed'],
                v['integrity']['branch_self_intersections'] == 0, v['integrity']['contact_pairs_equal_family_set'], v['integrity']['root_valence_4'], v['integrity']['verts'] == 59076, v['integrity']['quads'] == 59074,
                v['deformation']['ear_readiness_all_zero'], not v['deformation']['poses_worse_than_family'], v['deformation']['new_rest_contact_class'] == 0, v['deformation']['family_equals_reviewed_v004'], not exc,
                all(x for k_, x in v['rebuild'].items() if isinstance(x, bool)), v['rebuild']['regen_max_abs_dV_cm'] == 0, v['rebuild']['full_record_rebuild_max_abs_dV_cm'] == 0, v['rebuild']['branch_max_abs_diff_vs_reviewed_cm'] == 0])
rec['gate_pass_by_file'] = {k: ok(v['configuration'], v) for k, v in rec['files'].items()}
rec['all_gates_pass'] = all(rec['gate_pass_by_file'].values()) and rec['readback']['all_pass'] and rec['gates']['ear_firewall_all_hold'] and rec['gates']['probes_all_clean'] and rec['ear_branch']['face_topology_identical_c1_c2']
if not rec['all_gates_pass']:      # §23: VAEL_RP3_FREEZE.json is written only if every gate passes; otherwise a candidate record for the author decision
    rec['record'] = 'VAEL FINAL CONSOLIDATION NEEDS AUTHOR DECISION — NOT FROZEN (freeze candidate record; becomes VAEL_RP3_FREEZE.json only on author acceptance)'
    rec['open_items'] = {k: v['deformation']['worse_than_family_detail'] for k, v in rec['files'].items() if v['deformation']['worse_than_family_detail']}
OUTF = E + ('/VAEL_RP3_FREEZE.json' if rec['all_gates_pass'] else '/VAEL_RP3_FREEZE_CANDIDATE.json')
json.dump(rec, open(OUTF, 'w'), indent=1); print('freeze record', os.path.basename(OUTF), rec['all_gates_pass'], rec['gate_pass_by_file'], sha(OUTF))
