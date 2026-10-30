# cg_final_record.py EVIDENCE_FINAL_DIR : RP4 Cogling freeze-readiness record (order f58dbd9 §13 / §14) -- COGLING_RP4_FREEZE_CANDIDATE.json, written only if every
# gate holds (asserted). Reads the committed evidence copies (production json / read-back, validator summary, T-7 record, gate / deformation summaries, firewalls,
# immutables). CANDIDATE -- NOT FROZEN.
import sys, json, hashlib, os
E = sys.argv[1]; R = '/home/claude/wayfarer-design'; C = R + '/reviews/rac-rp4-evidence/cogling'
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest(); J = lambda p: json.load(open(p))
DEF = C + '/branch/MPFB_COGLING_COMPACT_BRANCH_v001.json'
toe = J(E + '/COGLING_toe_exception_validator_summary.json'); t7 = J(E + '/COGLING_T7_record.json'); g = J(E + '/CG_final_gates.json'); dfm = J(E + '/COGLING_final_deformation_vs_v005.json')
fw = J(C + '/firewalls/CG_firewalls.json'); pa = J(C + '/partA/CG_partA.json'); imm = open(E + '/immutable_hashes_final.txt').read().strip().splitlines()[-1]
cand = {}
for name, src, srcp in (('CG_M_REF_RP4_v001', 'CGJ7', 'reviews/reference-assets/r6/CGJ7_r6.npz'), ('CG_F_REF_RP4_v001', 'CGF91-NAT', 'reviews/rac-rp4-evidence/cogling/partA/CGF91-NAT_r6.npz')):
    p = J('%s/production/%s.json' % (E, name)); rb = J('%s/production/%s_readback.json' % (E, name)); fp = '%s/production/%s' % (E, name)
    assert sha(fp + '.blend') == p['file_sha256'] == rb['sha256'] and rb['geometry_hash'] == p['geometry_hash'] and rb['faces_equal_candidate']
    assert sha(fp + '_branch_map.npz') == p['branch_map_sha256'] and sha(fp + '_landmarks.json') == p['landmarks_sha256'] and p['branch_def_sha256'] == sha(DEF)
    assert rb['components'] == 1 and rb['boundary_edges'] == rb['nonmanifold_edges'] == rb['nonmanifold_vertices'] == rb['degenerate_faces'] == 0 and rb['normals_outward'] and rb['quads_pct'] == 100.0 and 'UVMap' in rb['uv_layers']
    cand[name] = dict(source=src, source_r6=srcp, source_r6_sha256=sha(R + '/' + srcp), file=fp[len(R) + 1:] + '.blend', file_sha256=p['file_sha256'], geometry_hash=p['geometry_hash'],
                      face_topology_hash=p['face_topology_hash'], verts=p['verts'], quads=p['quads'], branch_map=fp[len(R) + 1:] + '_branch_map.npz', branch_map_sha256=p['branch_map_sha256'],
                      landmarks=fp[len(R) + 1:] + '_landmarks.json', landmarks_sha256=p['landmarks_sha256'],
                      readback={k: rb[k] for k in ('geometry_hash', 'faces_equal_candidate', 'max_abs_diff_vs_candidate_m', 'components', 'boundary_edges', 'nonmanifold_edges', 'nonmanifold_vertices',
                                                     'degenerate_faces', 'quads_pct', 'normals_outward', 'uv_layers')}, embedded_status=p['embedded_status'])
M, F = cand['CG_M_REF_RP4_v001'], cand['CG_F_REF_RP4_v001']
assert M['face_topology_hash'] == F['face_topology_hash'] and M['branch_map_sha256'] == F['branch_map_sha256']
assert toe['all_adjusted_69'] and t7['all_adjusted_pass']
B = g['bodies']; assert g['identical_face_list_all_bodies'] and g['identical_S_all_bodies'] and g['definition_rebuild_identical']
assert all(b['T1_T2'] and b['T3'] and b['contact']['new'] == 0 and b['T4_branch']['aspect_gt4'] == 0 for b in B.values())
assert all(not d['new_class'] for d in dfm['bodies'].values()) and imm.startswith('# ') and imm.split()[1] == imm.split()[3]
rec = dict(record='COGLING_RP4_FREEZE_CANDIDATE', status='CANDIDATE - NOT FROZEN (freeze only by author acceptance record)', date='2026-10-30',
           orders=['reviews/chatgpt-rac-rp4-cogling-independent-compact-diagnosis-order.md (9424c72)', 'reviews/chatgpt-rac-rp4-cogling-author-rulings-final-production-order.md (f58dbd9)'],
           branch=dict(name='MPFB_COGLING_COMPACT_BRANCH_v001', definition=DEF[len(R) + 1:], sha256=sha(DEF), parent='MPFB Family Base v005',
                       content='thumb MCP two-direction compact support only (Cogling-solved placement); no neck reroute, no hip sector, no toe / foot branch, no face branch',
                       verts=58162, quads=58160, identical_topology_all_bodies=True, face_topology_hash=M['face_topology_hash'],
                       note='engineering face list identical to MPFB_PIPKIN_COMPACT_BRANCH_v001 (same v005 thumb grid rows); S / placement Cogling-only; Cogling-only branch, not a universal compact-race branch'),
           lineage=dict(c1='CGJ7 (accepted W1r central)', c2='CGF91-NAT (technical c2 anchor, order 9424c72 §4: MF-F-R base macro + exact CGJ7 targets / bone scales / girth beta 1.0 / CGJ7 head factor, 91.000 cm, rebuild identical)',
                        bounds='CG76H-NAT (canonical 76 cm, RM-OT-05A §2) / CG107-NAT (W2H)', provenance_only='CG76-NAT (superseded)'),
           candidates=cand,
           validator=dict(raw_authoritative={i: dict(file='reviews/rac-rp4-evidence/cogling/final/validator_raw/%s_cgb_validator_v2_D1-D6.json' % i, firm=b['raw_firm'], fail=b['raw_fail']) for i, b in toe['bodies'].items()},
                          author_adjusted={i: dict(firm=b['adjusted_firm'], exception_applied=b['exception_applied'], remaining_fail=b['adjusted_fail']) for i, b in toe['bodies'].items()},
                          toe_exception_record='reviews/rac-rp4-evidence/cogling/final/COGLING_toe_exception_validator_summary.json', toe_exception_label=toe['status_label'],
                          scope=toe['scope'], global_D4_changed=False, pipkin_label_reused=False, universal_compact_race_exception=False),
           T7=dict(record='reviews/rac-rp4-evidence/cogling/final/COGLING_T7_record.json', label=t7['status_label'], scope='CG76H-NAT only',
                   bodies={i: dict(raw_pass=b['raw_T7_pass'], raw_min_iou=min(b['raw_iou_branch'][k] for k in ('front', 'rear', 'profile_left', 'profile_right')), scaled_iou=b['scaled_iou_branch'], adjusted=b['adjusted_status'])
                           for i, b in t7['bodies'].items()}, global_T7_changed=False),
           c2_anchor_residual=dict(status='ACCEPTED C2 TECHNICAL-ANCHOR NARROWER-CORE RATIO RESIDUAL', reading=[n for n in pa['author_notes']],
                                   cause='thorax narrows more than the pelvis: c2 crest ~5.7-6.1 % and thorax ~6.6-7.2 % narrower than diagnostic Pipkin c2; pelvic vertical / thoracic vertical -9.8 %, pelvic AP / thoracic depth -4.6 %; every distal and narrow-core carrier intact'),
           T_gates={i: dict(T1_T2=b['T1_T2'], T3=b['T3'], T3_stature_diff_mm=b['T3_stature_diff_mm'], T4_branch=b['T4_branch'], T6_max_drift_mm=b['T6_max_drift_mm'], T7=t7['bodies'][i]['adjusted_status'],
                            deviation_body_mm=b['deviation_body_mm'], contact_new=b['contact']['new'], thumb=b['thumb']) for i, b in B.items()},
           deformation={i: dict(poses=d['poses'], identical=d['identical'], same_class=d['same_class'], new_class=d['new_class']) for i, d in dfm['bodies'].items()},
           firewalls=dict(record='reviews/rac-rp4-evidence/cogling/firewalls/CG_firewalls.json (source readings; production = source within T-1)',
                          pipkin_overlap={k: '%d / %d' % (v['hold'], v['of']) for k, v in fw['pipkin_overlap'].items()}, durrim_context='%d / %d' % (fw['durrim_context']['hold'], fw['durrim_context']['of']),
                          adult_vs_child={k: '%d / %d' % (v['separating'], v['of']) for k, v in fw['adult_vs_child'].items()}, marchfolk_normalized=fw['marchfolk_normalized']['counts'], hidden_identity=fw['hidden_identity']),
           accepted_notes=['Cogling c1 toe3/toe4 j1 raw validator failures are a documented D4 probe-geometry artifact accepted under the Cogling-specific exception',
                           'Cogling and Pipkin retain separate exception records; no universal compact-race exception exists yet', 'global D4 is unchanged',
                           'the 76 cm raw T-7 failure is a fixed-raster sampling artifact; the scale-consistent diagnostic passes and is the accepted production verdict for that boundary body',
                           'global T-7 is unchanged',
                           "CGF91-NAT's crest/thorax ratio inversion is an accepted technical-anchor residual caused by the thorax narrowing more than the pelvis; narrow-core and less-pelvis-led anatomy otherwise remain intact",
                           'Cogling sex-related anatomy remains OPEN', 'MPFB_COGLING_COMPACT_BRANCH_v001 is Cogling-only and is not a universal compact-race branch'],
           immutables=imm.lstrip('# ') + ' (reviews/rac-rp4-evidence/cogling/final/immutable_hashes_final.txt)')
json.dump(rec, open(E + '/COGLING_RP4_FREEZE_CANDIDATE.json', 'w'), indent=1, ensure_ascii=False); print('candidate written', rec['branch']['sha256'][:12])
