# sg_freeze_record.py WORK EVIDIR : order d921903 §8 -- writes SAGEKIN_RP3_FREEZE.json (freeze by record; production blends not re-saved).
import sys, json, hashlib
W, E = sys.argv[1:3]; sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest(); REPO = '/home/claude/wayfarer-design'; RA = REPO + '/reviews/reference-assets'
RB = json.load(open(W + '/freeze/SAGEKIN_RP3_freeze_readback.json')); D6 = json.load(open(E + '/D6_regression/D6_regression_summary.json')); PA = json.load(open(REPO + '/reviews/rac-rp3-evidence/sagekin_rp3_v001/partA/SGF178_reference_validation.json'))
F5 = REPO + '/reviews/rac-rp3-evidence/mpfb_family_base_v005_freeze/MPFB_FAMILY_BASE_v005_FREEZE.json'
DC = json.load(open(REPO + '/reviews/rac-rp3-evidence/sagekin_rp3_v001/SAGEKIN_RP3_deformation_comparison.json'))
rec = dict(record='SAGEKIN RP3 — AUTHOR ACCEPTED / FROZEN — MPFB FAMILY PROPAGATION PASS', date='2026-10-27',
           authority='reviews/chatgpt-rac-rp3-sagekin-d6-acceptance-and-freeze-order.md (d921903), author review of Claude return 8ed659d',
           freeze_method='freeze-by-record: both production .blend files preserved byte-identical (not re-saved); this record is authoritative over the candidate sidecar / embedded RAC_status strings ("CANDIDATE - NOT FROZEN")',
           family_base=dict(record='MPFB_FAMILY_BASE_v005_FREEZE.json', record_sha256=sha(F5), face_topology_hash='ec768ae210ea3ee1c053d0c4cd3256d57dad6db35d515502706b74f64281bee0', verts=57842, quads=57840,
                            hm08_map=dict(file='MF_M_REF_RP3_retopo_v005_hm08_map.npz', sha256=RB['family_map_sha256'], identical_for_every_race=True)),
           references=dict(SG=dict(role='Sagekin configuration-1 central reference (accepted W1c)', r6='reviews/reference-assets/r6/SG_r6.npz', r6_sha256=sha(RA + '/r6/SG_r6.npz'), build_sha256=sha(RA + '/builds/SG_build.json'), stature_cm=PA['stature']['SG']),
                           SGF178=dict(role='Sagekin configuration-2 central reference — AUTHOR ACCEPTED (d921903 §1)', r6='reviews/reference-assets/r6/SGF178_r6.npz', r6_sha256=sha(RA + '/r6/SGF178_r6.npz'), build_sha256=sha(RA + '/builds/SGF178_build.json'),
                                       geometry_hash='7755a8f00de921dd8651a899c96e1050ff65b481a0ebf08025b0c82875359a25', stature_cm=PA['stature']['SGF178'], rebuild='regen + full height re-solve, max |dV| 0'),
                           SGF152_NAT=dict(role='accepted configuration-2 minimum bound', r6_sha256=sha(RA + '/r6/SGF152-NAT_r6.npz')), SGF208=dict(role='accepted configuration-2 maximum bound', r6_sha256=sha(RA + '/r6/SGF208_r6.npz'))),
           validator=dict(rules=['D1 undefined band-side fallback (85b7c1c)', 'D3 same-digit pole ownership (85b7c1c)', 'D4 stature-normalised station geometry, reference 173.143 cm (a18371c / 33a2dfe)', 'D5 interdigital endpoint validity (33a2dfe)',
                                 'D6 non-digit foreign-segment endpoint ownership (proposed c6c7940, accepted d921903)'], authoritative='D1 + D3 + D4 + D5 + D6',
                          implementation='tools/rac/rp/marchfolk_rp3_v001/val2lib.py (evaluate d5=True, d6=(M @ native W, bones)); CLI validator_v2.py CAND OUT --scale-ref 173.143 --d5 --d6-native NATIVE.npz',
                          D6_regression=dict(evidence='D6_regression/D6_regression_summary.json', pass_=D6['regression_pass'], firm={k: v['firm_D1_D3_D4_D5_D6'] for k, v in D6['configurations'].items()}, lowered={k: v['lowered'] for k, v in D6['configurations'].items()},
                                             false_positives={k: len(v['false_positives']) for k, v in D6['configurations'].items()})),
           files={}, carry_forward=dict(register='specs/RAC_PRODUCTION_RIG_CARRY_FORWARD_REGISTER.md', new_ids=[], note='Sagekin toe-extension behaviour reproduces the accepted family class (SGF178 58 vs MF-F v005 60 flips; SG 71 vs MF-M 70); covered by MPFB-CF-1 / CF-2 class, no new ID'),
           deformation=dict(evidence='reviews/rac-rp3-evidence/sagekin_rp3_v001/SAGEKIN_RP3_deformation_comparison.json', worst_flip_excess_vs_marchfolk_v005={k: v['sagekin_minus_marchfolk_flipped_max'] for k, v in DC.items()}, new_topology_class_failure=False),
           readback=dict(file='SAGEKIN_RP3_freeze_readback.json', all_pass=RB['all_pass'], manifest_sha256=RB['manifest_sha256']),
           gates='reviews/claude-rac-rp3-sagekin-config2-reference-and-propagation-gate.md; reviews/claude-rac-rp3-sagekin-family-freeze-report.md',
           provenance=['SG (W1c) / SGF178 (RM-OT-05A construction base, accepted d921903) R-6 sources regenerated identically', 'native hm08 export (helpers removed)', 'propagate.py onto MF_M_REF_RP3_retopo_v005.blend + family hm08 map (no topology change)',
                       'make_prod.py production frame (m, Z up, faces -Y, origin pelvis root on ground)', 'E: copies read back byte-identical'],
           freezes=['Sagekin configuration-1 / configuration-2 central realizations on the active v005 family topology', 'SGF178 as the accepted configuration-2 central reference'])
for cid, f in RB['files'].items():
    rec['files'][f['file']] = dict(race='Sagekin', configuration=cid, path='E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Sagekin/RP3/' + f['file'], sha256=f['sha256'], geometry_hash=f['geometry_hash'], face_topology_hash=f['face_topology_hash'],
                                    verts=f['verts'], quads=f['quads'], sidecar=f['file'].replace('.blend', '.json'), sidecar_sha256=f['sidecar_sha256'], landmarks_sha256=f['landmarks_sha256'], hm08_map_sha256=f['map_sha256'], source=f['source'],
                                    validator=f['validator'], gates=f['gates'], readback=dict(max_abs_diff_vs_candidate_m=f['max_abs_diff_vs_candidate_m'], normals_outward=f['normals_outward'], all_pass=f['all_pass']), embedded_status_superseded=f['embedded_status'])
json.dump(rec, open(E + '/SAGEKIN_RP3_FREEZE.json', 'w'), indent=1); print('freeze record', sha(E + '/SAGEKIN_RP3_FREEZE.json'))
