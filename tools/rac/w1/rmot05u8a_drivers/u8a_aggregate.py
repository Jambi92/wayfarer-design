# RM-OT-05U8A: aggregate for the controlled crease-anchor release. Exit 0 ONLY if every U8A safety gate passes; otherwise 3.
# Additive copy of u8_aggregate.py; the U4 / U6 / U7 / U8 aggregates are unchanged (crease identity logic reused verbatim; frozen reference).
#   mandatory: U8A protection vs U8 cp1 (topology unchanged; every vertex outside {61580, 61581} bit-exact to cp1 incl. the 12-vertex ring,
#              the U8 cp1 edits, the U6/U7 edits except released 61581, the U6 target outside the anchors); anchor displacement within the
#              order's step limits (61581 <= 0.06 cm, 61580 <= 0.04 cm vs U8 cp1); V1-U8A; no s_verify FAIL verdict; V2; V3; V5; V6c-3;
#              crease A >= 0.6712880840904568 and crease B >= 0.27434876590971574 (frozen reference, by identity); U8A local quality;
#              U6 no-regression (target roughness <= 36.3, exception identity, locus, cap quality >= 10); U7 and U8 local quality >= 10
#   reported, not waived: V4, V6 historical, V6c-1, V6c-2 (global); U8A dihedral diagnostic (no threshold)
import argparse, hashlib, json, os, sys
ap = argparse.ArgumentParser(); [ap.add_argument(k) for k in ('--reint', '--verify', '--crease', '--guards6', '--guards7', '--guards8', '--guards8a', '--ref', '--out')]; a = ap.parse_args()
def load(p):
    try: return json.load(open(p)) if p and os.path.exists(p) else None
    except Exception: return None
R, V, C, G6, G7, G8, GA, REF = (load(x) for x in (a.reint, a.verify, a.crease, a.guards6, a.guards7, a.guards8, a.guards8a, a.ref))
agg = dict(tool='RM-OT-05U8A aggregate', author_visual_review='PENDING', note='A U8A PASS is technical safety for the controlled crease-anchor release only; the visual result decides; never author acceptance.')
m = {}
m['protection_U8A_vs_u8cp1'] = dict(status='PASS' if R and R.get('verdict') == 'ACCEPTED_FOR_VERIFICATION_U8A' else 'FAIL', verdict=(R or {}).get('verdict', 'MISSING'), errors=(R or {}).get('errors', []))
pc = (R or {}).get('protection_vs_u8cp1'); tp = (R or {}).get('topology')
m['topology_unchanged'] = dict(status='MISSING') if not tp else dict(status='PASS' if tp['missing_faces'] == 0 and tp['extra_faces'] == 0 and tp['duplicate_faces'] == 0 and tp['face_count_matches'] else 'FAIL')
for k, key, ok in (('outside_anchors_bit_exact_to_u8cp1', 'moved_outside_target', lambda x: x == 0), ('u8a_frozen_ring_unmoved', 'u8a_frozen_ring_moved', lambda x: not x),
                   ('u8_cp1_edits_unmoved', 'u8_edited_moved', lambda x: not x), ('u6_edited_unmoved_except_61581', 'u6_edited_moved', lambda x: not x),
                   ('u7_edited_unmoved', 'u7_edited_moved', lambda x: not x), ('u6_target_outside_anchors_unmoved', 'u6_target_moved', lambda x: not x)):
    m[k] = dict(status='MISSING') if not pc else dict(status='PASS' if ok(pc[key]) else 'FAIL', value=pc[key])
if V:
    m['V1_U8A_prefix_and_correspondence'] = dict(status='PASS' if V['V1_outside_anatomy']['pass_'] else 'FAIL')
    m['s_verify_no_FAIL_verdict'] = dict(status='PASS' if V.get('verdict_automated') != 'FAIL' else 'FAIL', verdict=V.get('verdict_automated'))
    for k in ('V2_boundary_manifold', 'V3_intersections', 'V5_seam_continuity', 'V6c_3_no_folds'): m[k] = dict(status='PASS' if (V.get(k) or {}).get('pass_') is True else 'FAIL')
else:
    for k in ('V1_U8A_prefix_and_correspondence', 's_verify_no_FAIL_verdict', 'V2_boundary_manifold', 'V3_intersections', 'V5_seam_continuity', 'V6c_3_no_folds'): m[k] = dict(status='MISSING')
ref_secs = (REF or {}).get('sections', {}); fp = {k: hashlib.sha256(json.dumps(v, sort_keys=True).encode()).hexdigest() for k, v in ref_secs.items()}
for sid in ('A', 'B'):
    key = 'crease_depth_%s' % sid
    if not REF or sid not in ref_secs: m[key] = dict(status='MISSING'); continue
    s = ((C or {}).get('sections') or {}).get(sid)
    if s is None: m[key] = dict(status='MISSING'); continue
    if s.get('section_id') != sid or s.get('fingerprint') != fp[sid] or s.get('anchor_s3_vertex') != ref_secs[sid]['anchor_s3_vertex'] or s.get('s0_cm') != ref_secs[sid]['s0_cm'] or s.get('threshold_cm') != ref_secs[sid]['threshold_cm']:
        m[key] = dict(status='FAIL', error='section identity / reference fingerprint mismatch'); continue
    m[key] = dict(status='PASS' if s.get('status') == 'PASS' else s.get('status', 'MISSING'), depth_cm=s.get('depth_cm'), threshold_cm=s['threshold_cm'], error=s.get('error'))
if C and C.get('errors'): m['crease_measurement_errors'] = dict(status='FAILED_MEASUREMENT', errors=C['errors'])
x = (GA or {}).get('local_quality'); m['u8a_local_quality'] = dict(status='MISSING') if x is None else dict(status='PASS' if x['pass_'] else 'FAIL', **{k: v for k, v in x.items() if k != 'pass_'})
x = (GA or {}).get('anchor_steps'); m['anchor_steps_within_limits'] = dict(status='MISSING') if x is None else dict(status='PASS' if x['pass_'] else 'FAIL', displacement_cm=x['displacement_vs_u8cp1_cm'], limits_cm=x['limits_cm'])
if GA and GA.get('errors'): m['u8a_guard_errors'] = dict(status='FAILED_MEASUREMENT', errors=GA['errors'])
x = (G8 or {}).get('local_quality'); m['u8_no_regression_local_quality'] = dict(status='MISSING') if x is None else dict(status='PASS' if x['pass_'] else 'FAIL', min_angle_now=x.get('min_angle_now'))
x = (G7 or {}).get('local_quality'); m['u7_no_regression_local_quality'] = dict(status='MISSING') if x is None else dict(status='PASS' if x['pass_'] else 'FAIL', min_angle_now=x.get('min_angle_now'))
for g in ('R1_target_roughness', 'R1_baseline_exception_identity', 'locus_outside_target_unchanged', 'R2_local_cap_quality'):
    x = (G6 or {}).get(g); m['u6_no_regression_' + g] = dict(status='MISSING') if x is None else dict(status='PASS' if x.get('pass_') else 'FAIL', **{kk: vv for kk, vv in x.items() if kk in ('max_now', 'over_limit', 'moved', 'min_angle_now', 'below_min_angle')})
agg['mandatory'] = m
agg['u8a_safety_gates'] = 'PASS' if all(v['status'] == 'PASS' for v in m.values()) else 'NOT MET'
agg['failed_or_missing'] = [k for k, v in m.items() if v['status'] != 'PASS']
agg['target_moved'] = (pc or {}).get('target_moved'); agg['facet_diagnostic'] = (GA or {}).get('facet_diagnostic'); agg['face_130139_min_angle'] = (GA or {}).get('face_130139_min_angle')
if V:
    agg['global_unresolved_disclosed_not_waived'] = {k: V[k]['pass_'] for k in ('V4_triangle_quality', 'V6_historical_05Q', 'V6c_1_garment_ledge_removed', 'V6c_2_taper_termination')}
    agg['s_verify_verdict'] = V.get('verdict_automated')
json.dump(agg, open(a.out, 'w'), indent=1)
print('U8A safety gates:', agg['u8a_safety_gates'], '| failed/missing:', agg['failed_or_missing'], '| author visual review: PENDING')
sys.exit(0 if agg['u8a_safety_gates'] == 'PASS' else 3)
