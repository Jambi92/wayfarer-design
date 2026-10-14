# RM-OT-05U7: aggregate for the minimal upper-crease facet extension. Exit 0 ONLY if every U7 safety gate passes; otherwise 3.
# Additive; the U4 / U6 aggregates are unchanged (crease identity logic reused verbatim from u4_aggregate.py).
#   mandatory: U7 protection vs cp3 (topology unchanged; every vertex outside the 5-vertex target bit-exact to cp3, incl. the U7 frozen
#              ring and the 16 U6 target vertices); V1-U7 (P05U7 protected prefix hash + source correspondence, exempt = cp3 + target);
#              no s_verify FAIL verdict; V2; V3; V5; V6c-3; crease A; crease B; U7 local quality; U6 no-regression: R1 target roughness
#              <= 36.3, R1 baseline-exception identity, U6 locus, R2 cap quality (4 U7 faces are U2 cap faces)
#   reported, not waived: V4, V6 historical, V6c-1, V6c-2 (global); U7 facet diagnostic (no threshold)
#   pending (never automated): author visual review
import argparse, hashlib, json, os, sys
ap = argparse.ArgumentParser(); [ap.add_argument(k) for k in ('--reint', '--verify', '--crease', '--guards6', '--guards7', '--ref', '--out')]; a = ap.parse_args()
def load(p):
    try: return json.load(open(p)) if p and os.path.exists(p) else None
    except Exception: return None
R, V, C, G6, G7, REF = (load(x) for x in (a.reint, a.verify, a.crease, a.guards6, a.guards7, a.ref))
agg = dict(tool='RM-OT-05U7 aggregate', author_visual_review='PENDING', note='A U7 PASS is technical safety for the bounded upper-crease task only; the visual result decides, and it is never author acceptance.')
m = {}
m['protection_U7_vs_cp3'] = dict(status='PASS' if R and R.get('verdict') == 'ACCEPTED_FOR_VERIFICATION_U7' else 'FAIL', verdict=(R or {}).get('verdict', 'MISSING'), errors=(R or {}).get('errors', []))
pc = (R or {}).get('protection_vs_cp3'); tp = (R or {}).get('topology')
m['topology_unchanged'] = dict(status='MISSING') if not tp else dict(status='PASS' if tp['missing_faces'] == 0 and tp['extra_faces'] == 0 and tp['duplicate_faces'] == 0 and tp['face_count_matches'] else 'FAIL')
m['outside_target_bit_exact_to_cp3'] = dict(status='MISSING') if not pc else dict(status='PASS' if pc['moved_outside_target'] == 0 else 'FAIL', moved=pc['moved_outside_target'])
m['u7_frozen_ring_unmoved'] = dict(status='MISSING') if not pc else dict(status='PASS' if not pc['u7_frozen_ring_moved'] else 'FAIL', moved=pc['u7_frozen_ring_moved'])
m['u6a_lower_repair_unchanged'] = dict(status='MISSING') if not pc else dict(status='PASS' if not pc['u6_target_moved'] else 'FAIL', moved=pc['u6_target_moved'])
if V:
    m['V1_U7_prefix_and_correspondence'] = dict(status='PASS' if V['V1_outside_anatomy']['pass_'] else 'FAIL')
    m['s_verify_no_FAIL_verdict'] = dict(status='PASS' if V.get('verdict_automated') != 'FAIL' else 'FAIL', verdict=V.get('verdict_automated'))
    for k in ('V2_boundary_manifold', 'V3_intersections', 'V5_seam_continuity', 'V6c_3_no_folds'): m[k] = dict(status='PASS' if (V.get(k) or {}).get('pass_') is True else 'FAIL')
else:
    for k in ('V1_U7_prefix_and_correspondence', 's_verify_no_FAIL_verdict', 'V2_boundary_manifold', 'V3_intersections', 'V5_seam_continuity', 'V6c_3_no_folds'): m[k] = dict(status='MISSING')
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
x = (G7 or {}).get('local_quality'); m['u7_local_quality'] = dict(status='MISSING') if x is None else dict(status='PASS' if x['pass_'] else 'FAIL', **{k: v for k, v in x.items() if k != 'pass_'})
if G7 and G7.get('errors'): m['u7_guard_errors'] = dict(status='FAILED_MEASUREMENT', errors=G7['errors'])
for g in ('R1_target_roughness', 'R1_baseline_exception_identity', 'locus_outside_target_unchanged', 'R2_local_cap_quality'):
    x = (G6 or {}).get(g); m['u6_no_regression_' + g] = dict(status='MISSING') if x is None else dict(status='PASS' if x.get('pass_') else 'FAIL', **{kk: vv for kk, vv in x.items() if kk in ('max_now', 'over_limit', 'moved', 'min_angle_now', 'below_min_angle')})
agg['mandatory'] = m
agg['u7_safety_gates'] = 'PASS' if all(v['status'] == 'PASS' for v in m.values()) else 'NOT MET'
agg['failed_or_missing'] = [k for k, v in m.items() if v['status'] != 'PASS']
agg['target_moved'] = (pc or {}).get('target_moved'); agg['facet_diagnostic'] = (G7 or {}).get('facet_diagnostic')
if V:
    agg['global_unresolved_disclosed_not_waived'] = {k: V[k]['pass_'] for k in ('V4_triangle_quality', 'V6_historical_05Q', 'V6c_1_garment_ledge_removed', 'V6c_2_taper_termination')}
    agg['s_verify_verdict'] = V.get('verdict_automated')
json.dump(agg, open(a.out, 'w'), indent=1)
print('U7 safety gates:', agg['u7_safety_gates'], '| failed/missing:', agg['failed_or_missing'], '| author visual review: PENDING')
sys.exit(0 if agg['u7_safety_gates'] == 'PASS' else 3)
