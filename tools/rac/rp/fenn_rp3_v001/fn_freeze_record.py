# fn_freeze_record.py WORK EVIDIR : order 6d2eadc §16 -- writes FENN_RP3_FREEZE.json (freeze by record; the production blends are not re-saved).
import sys, json, hashlib
W, E = sys.argv[1:3]; sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest(); REPO = '/home/claude/wayfarer-design'; RA = REPO + '/reviews/reference-assets'; EV2 = REPO + '/reviews/rac-rp3-evidence/fenn_ear_v002'
RB = json.load(open(E + '/FENN_RP3_freeze_readback.json')); G = json.load(open(E + '/FENN_FINAL_gates.json')); F5 = REPO + '/reviews/rac-rp3-evidence/mpfb_family_base_v005_freeze/MPFB_FAMILY_BASE_v005_FREEZE.json'
B5 = '/mnt/user-data/outputs/rp5'; T2 = json.load(open(EV2 + '/topology/FENN_EAR_BRANCH_TOPOLOGY_v002.json'))
rec = dict(record='FENN RP3 FINAL PASS — AUTHOR ACCEPTED / FROZEN', date='2026-10-27',
           authority='reviews/chatgpt-rac-rp3-fenn-final-consolidation-freeze-order.md (6d2eadc), author review of Claude return 96c41d0',
           freeze_method='freeze-by-record: both production .blend files are preserved byte-identical (not re-saved); this record is authoritative over the sidecar / embedded RAC_status strings',
           family_base=dict(record='MPFB_FAMILY_BASE_v005_FREEZE.json', record_sha256=sha(F5), blend='MF_M_REF_RP3_retopo_v005.blend', blend_sha256=sha(B5 + '/MF_M_REF_RP3_retopo_v005.blend'),
                            hm08_map='MF_M_REF_RP3_retopo_v005_hm08_map.npz', hm08_map_sha256=sha(B5 + '/MF_M_REF_RP3_retopo_v005_hm08_map.npz'), face_topology_hash='ec768ae210ea3ee1c053d0c4cd3256d57dad6db35d515502706b74f64281bee0',
                            verts=57842, quads=57840, unchanged=True, note='active family base unchanged; Fenn uses it everywhere outside the ear branch'),
           ear_branch=dict(topology='FENN_EAR_BRANCH_TOPOLOGY_v002 (accepted 6d2eadc §1.4)', topology_json_sha256=sha(EV2 + '/topology/FENN_EAR_BRANCH_TOPOLOGY_v002.json'), topology_npz_sha256=sha(EV2 + '/topology/FENN_EAR_BRANCH_TOPOLOGY_v002.npz'),
                           cuff_canon_sha256=sha(EV2 + '/topology/FENN_EAR_BRANCH_CUFF_CANON_v002.json'), map_v005_v002_npz_sha256=sha(EV2 + '/mapping/FENN_EAR_BRANCH_MAP_v005_v002.npz'), map_v005_v002_json_sha256=sha(EV2 + '/mapping/FENN_EAR_BRANCH_MAP_v005_v002.json'),
                           geometry_record_sha256=sha(EV2 + '/geometry/FENN_EAR_BRANCH_GEOMETRY_v002.json'), geometry='E2 (W1e FN-elven balanced; accepted 6d2eadc §1.3)', per_side=T2['per_side'], whole_mesh=T2['whole_mesh'],
                           shared_by='configuration 1 and configuration 2 (identical face list)'),
           references=dict(FNL4=dict(role='configuration-1 body ancestry', r6_sha256=sha(RA + '/r6/FNL4_r6.npz')), FNF181=dict(role='configuration-2 body ancestry', r6_sha256=sha(RA + '/r6/FNF181_r6.npz')),
                           **{h: dict(role='accepted configuration-%s craniofacial reference (CF2)' % ('1' if h == 'FNL4-CF2' else '2'), r6_sha256=sha(RA + '/r6/%s_r6.npz' % h), build_sha256=sha(RA + '/builds/%s_build.json' % h),
                                      regen_geometry_identical=G['configurations']['c1' if h == 'FNL4-CF2' else 'c2']['rebuild']['regen_geometry_identical'],
                                      family_realization_sha256=G['configurations']['c1' if h == 'FNL4-CF2' else 'c2']['rebuild']['family_realization_sha256']) for h in ('FNL4-CF2', 'FNF181-CF2')}),
           validator=dict(rules='D1 + D3 + D4 + D5 + D6 (authoritative)', implementation='tools/rac/rp/marchfolk_rp3_v001/validator_v2.py --scale-ref 173.143 --d5 --d6-native', files={}),
           files={}, accepted_residuals=dict(topology_quality=['1-2 sharp root-band cells per configuration (min corner c1 7.9 deg, c2 12.7 deg; locked root-band topology)', '17 / 19 branch quads with aspect between 6 and 10 (none > 10)',
                                                               'small obtuse-cell cluster at the bridge / concha-floor corner'], accepted_by='6d2eadc §2', note='accepted topology-quality residuals, NOT rig carry-forward items'),
           carry_forward=dict(register='specs/RAC_PRODUCTION_RIG_CARRY_FORWARD_REGISTER.md', ids=['FENN-CF-1 (configuration-2 CF2 mouth-corner expression units; facial rig / corrective stage; unchanged)'], new_ids=[]),
           gates=dict(record='FENN_FINAL_gates.json', report='reviews/claude-rac-rp3-fenn-final-freeze-report.md', parent='reviews/claude-rac-rp3-fenn-ear-v002-refinement-gate.md'),
           readback=dict(file='FENN_RP3_freeze_readback.json', all_pass=RB['all_pass'], c1_c2_face_topology_identical=RB['c1_c2_face_topology_identical']),
           provenance=['FNL4-CF2 / FNF181-CF2 R-6 regenerated from reviews/reference-assets/builds (regen.py: geometry identical, max |dV| 0)', 'native hm08 export', 'propagate.py onto MPFB Family Base v005 (frozen blend + hm08 map) -> CF2 family realization (byte-identical to the reviewed one)',
                       'Fenn ear branch topology v002, E2, from the committed cuff canon (run_earbranch_v002.sh; byte-identical arrays to the reviewed v002 candidate; 10 probes identical)', 'fn_make_prod.py production frame (m, Z up, faces -Y, origin pelvis root on ground)', 'E: copies read back byte-identical'],
           freezes=['Fenn RP3 configuration-1 / configuration-2 final production bodies', 'Fenn ear branch topology v002 + E2 as the accepted Fenn external-ear branch (Fenn only; not a universal elf ear)'],
           not_done=['production ear rigging', 'creator morphs', 'final UV / materials (branch faces carry a zero placeholder UV)', 'LODs', 'UE5 integration'])
for c, (h, nm) in (('c1', ('FNL4-CF2', 'FN_M_REF_RP3_v001')), ('c2', ('FNF181-CF2', 'FN_F_REF_RP3_v001'))):
    f = RB['files'][h]; g = G['configurations'][c]; sc = json.load(open('%s/production/%s.json' % (E, nm)))
    rec['files'][f['file']] = dict(race='Fenn', configuration=c, head=h, path='E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Fenn/RP3/' + f['file'], sha256=f['sha256'], geometry_hash=f['geometry_hash'],
                                   face_topology_hash=f['face_topology_hash'], verts=f['verts'], quads=f['quads'], sidecar=nm + '.json', sidecar_sha256=f['sidecar_sha256'], branch_map=nm + '_branch_map.npz', branch_map_sha256=f['branch_map_sha256'],
                                   landmarks=nm + '_landmarks.json', landmarks_sha256=f['landmarks_sha256'], embedded_status=f['embedded_status'], readback_all_pass=f['all_pass'],
                                   integrity={k: g['integrity'][k] for k in ('quads_pct', 'components', 'boundary_edges', 'nonmanifold_edges', 'nonmanifold_vertices', 'degenerate_faces', 'normals_outward', 'self_intersection_pairs', 'family_self_intersection_pairs', 'contact_pairs_equal_family_set', 'branch_self_intersections')},
                                   validator=dict(firm=g['validator']['firm'], stations=g['validator']['stations'], margin_zero=g['validator']['margin_zero']),
                                   anatomy=dict(T1=g['anatomy']['final_ear_excluded']['T1'], T2=g['anatomy']['final_ear_excluded']['T2'], T3=g['anatomy']['final_ear_excluded']['T3'], T7=g['anatomy']['final_ear_excluded']['T7'],
                                                identity_holds_all_zones=g['anatomy']['identity']['holds_all_zones'], hidden_ear_body=g['anatomy']['hidden_ear_body']['pass_'], hidden_ear_face=g['anatomy']['hidden_ear_face']['pass_']),
                                   face=dict(mouth_rings=g['face']['mouth_rings'], orbit_rings=g['face']['orbit_rings'], poles_at_mouth_corners=g['face']['poles_at_mouth_corners'], mouth_pass=g['face']['mouth_pass'], orbit_pass=g['face']['orbit_pass']),
                                   density=dict(all_9_zones_pass=g['density']['all_pass'], ear_branch_mean_pct_stature=g['density']['ear_branch_mean_pct']),
                                   ear=dict(T4=g['ear']['T4'], branch_faces=g['ear']['branch_faces'], T4_rate=round(g['ear']['T4_rate'], 4), aspect_max=g['ear']['aspect_max'], aspect_gt10=g['ear']['aspect_gt10'], root_crease_max_deg=max(v['max_deg'] for v in g['ear']['root_dihedral'].values())),
                                   deformation=dict(standard_v1_final_minus_family_flipped_max=g['deformation']['standard_v1']['final_minus_family_flipped_max'], standard_v1_poses_worse_than_family=g['deformation']['standard_v1']['poses_worse_than_family'],
                                                    ear_readiness_all_zero=g['deformation']['ear_readiness']['all_zero']))
    rec['validator']['files'][f['file']] = '%d / %d' % (g['validator']['firm'], g['validator']['stations'])
rec['all_gates_pass'] = all(all([v['readback_all_pass'], v['validator']['firm'] == 69, v['anatomy']['T1'], v['anatomy']['T2'], v['anatomy']['T3'], v['anatomy']['T7'], v['anatomy']['identity_holds_all_zones'], v['anatomy']['hidden_ear_body'],
                                 v['anatomy']['hidden_ear_face'], v['face']['mouth_pass'], v['face']['orbit_pass'], v['face']['poles_at_mouth_corners'] == 0, v['density']['all_9_zones_pass'], v['ear']['aspect_gt10'] == 0,
                                 v['integrity']['branch_self_intersections'] == 0, v['integrity']['contact_pairs_equal_family_set'], v['deformation']['ear_readiness_all_zero'], not v['deformation']['standard_v1_poses_worse_than_family']]) for v in rec['files'].values())
json.dump(rec, open(E + '/FENN_RP3_FREEZE.json', 'w'), indent=1); print('freeze record', rec['all_gates_pass'], sha(E + '/FENN_RP3_FREEZE.json'))
