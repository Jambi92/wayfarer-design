# RM-OT-05U6: machine-readable aggregate for the bounded posterior upper-notch repair. Exit 0 ONLY if every U6 mandatory gate passes
# (order reviews/chatgpt-rac-rm-ot-05u6-corrected-guards-targeted-desktop-repair-order.md section 5); any FAIL / MISSING -> exit 3.
# Additive: tools/rac/w1/rmot05u4_drivers/u4_aggregate.py is unchanged; its crease identity logic is reused verbatim here.
#   mandatory: U2 protection accepted; 0 moved outside the 365; 0 moved on the 106 frozen ring; no topology change; V1-U2; no s_verify FAIL
#              verdict (existing hard rule, retained); V2; V3; V5; V6c-3; crease A; crease B (frozen reference, by identity);
#              R1 target roughness; R1 baseline-exception identity; locus (editable outside target unchanged); R2 local cap quality
#   reported, not waived: V4, V6 historical, V6c-1, V6c-2 (global); 365-wide roughness and the retired 05U5 sliver rule (diagnostic)
#   pending (never automated): author visual review
import argparse, hashlib, json, os, sys
ap = argparse.ArgumentParser(); [ap.add_argument(k) for k in ('--reint', '--verify', '--crease', '--guards6', '--ref', '--out')]; a = ap.parse_args()
def load(p):
    try: return json.load(open(p)) if p and os.path.exists(p) else None
    except Exception: return None
R, V, C, G, REF = (load(x) for x in (a.reint, a.verify, a.crease, a.guards6, a.ref))
agg = dict(tool='RM-OT-05U6 aggregate', author_visual_review='PENDING',
           note='ACCEPTED_FOR_VERIFICATION_U2 is protection only. A U6 PASS is a technical result for the bounded posterior upper-notch task only; never author acceptance.')
m = {}
m['protection_U2_reintegration'] = dict(status='PASS' if R and R.get('verdict') == 'ACCEPTED_FOR_VERIFICATION_U2' else 'FAIL', verdict=(R or {}).get('verdict', 'MISSING'), errors=(R or {}).get('errors', []))
p1 = (R or {}).get('P1_U2_vertices_outside_365'); tp = (R or {}).get('topology')
m['outside_365_unmoved'] = dict(status='MISSING') if not p1 else dict(status='PASS' if p1['moved'] == 0 and p1['unchanged_bit_exact'] == p1['expected'] else 'FAIL', moved=p1['moved'])
m['frozen_ring_unmoved'] = dict(status='MISSING') if not p1 else dict(status='PASS' if p1['frozen_ring_moved'] == 0 else 'FAIL', moved=p1['frozen_ring_moved'])
m['topology_unchanged'] = dict(status='MISSING') if not tp else dict(status='PASS' if tp['missing_faces'] == 0 and tp['extra_faces'] == 0 and tp['duplicate_faces'] == 0 and tp['face_count_matches'] else 'FAIL',
                                                                   **{k: tp[k] for k in ('missing_faces', 'extra_faces', 'duplicate_faces', 'face_count_matches')})
if V:
    m['V1_U2'] = dict(status='PASS' if V['V1_outside_anatomy']['pass_'] and V['V1_outside_anatomy'].get('mode') == 'U2 opt-in' else 'FAIL')
    m['s_verify_no_FAIL_verdict'] = dict(status='PASS' if V.get('verdict_automated') != 'FAIL' else 'FAIL', verdict=V.get('verdict_automated'))
    for k in ('V2_boundary_manifold', 'V3_intersections', 'V5_seam_continuity', 'V6c_3_no_folds'):
        m[k] = dict(status='PASS' if (V.get(k) or {}).get('pass_') is True else ('MISSING' if k not in V else 'FAIL'))
else:
    for k in ('V1_U2', 's_verify_no_FAIL_verdict', 'V2_boundary_manifold', 'V3_intersections', 'V5_seam_continuity', 'V6c_3_no_folds'): m[k] = dict(status='MISSING')
ref_secs = (REF or {}).get('sections', {}); fp = {k: hashlib.sha256(json.dumps(v, sort_keys=True).encode()).hexdigest() for k, v in ref_secs.items()}
for sid in ('A', 'B'):
    key = 'crease_depth_%s' % sid
    if not REF or sid not in ref_secs: m[key] = dict(status='MISSING', error='frozen reference missing or lacks section %s' % sid); continue
    s = ((C or {}).get('sections') or {}).get(sid)
    if s is None: m[key] = dict(status='MISSING', error='measurement lacks section %s' % sid); continue
    if s.get('section_id') != sid or s.get('fingerprint') != fp[sid] or s.get('anchor_s3_vertex') != ref_secs[sid]['anchor_s3_vertex'] or s.get('s0_cm') != ref_secs[sid]['s0_cm'] or s.get('threshold_cm') != ref_secs[sid]['threshold_cm']:
        m[key] = dict(status='FAIL', error='section identity / reference fingerprint mismatch'); continue
    st = s.get('status', 'MISSING'); m[key] = dict(status='PASS' if st == 'PASS' else st, depth_cm=s.get('depth_cm'), threshold_cm=s['threshold_cm'], error=s.get('error'))
if C and C.get('errors'): m['crease_measurement_errors'] = dict(status='FAILED_MEASUREMENT', errors=C['errors'])
for g in ('R1_target_roughness', 'R1_baseline_exception_identity', 'locus_outside_target_unchanged', 'R2_local_cap_quality'):
    x = (G or {}).get(g); m[g] = dict(status='MISSING') if x is None else dict(status='PASS' if x.get('pass_') else 'FAIL', **{kk: vv for kk, vv in x.items() if kk != 'pass_'})
if G and G.get('errors'): m['u6_guard_errors'] = dict(status='FAILED_MEASUREMENT', errors=G['errors'])
agg['mandatory'] = m
agg['u6_technical_gates'] = 'PASS' if all(v['status'] == 'PASS' for v in m.values()) else 'NOT MET'
agg['failed_or_missing'] = [k for k, v in m.items() if v['status'] != 'PASS']
agg['changed_target_vertices'] = (G or {}).get('changed_target_vertices')
agg['historical_diagnostics'] = (G or {}).get('historical_diagnostics')
if V:
    agg['geometry_gates_reported'] = {k: v['pass_'] for k, v in V.items() if isinstance(v, dict) and 'pass_' in v}
    agg['global_unresolved_disclosed_not_waived'] = {k: agg['geometry_gates_reported'].get(k) for k in ('V4_triangle_quality', 'V6_historical_05Q', 'V6c_1_garment_ledge_removed', 'V6c_2_taper_termination')}
    agg['s_verify_verdict'] = V.get('verdict_automated')
json.dump(agg, open(a.out, 'w'), indent=1)
print('U6 technical gates:', agg['u6_technical_gates'], '| failed/missing:', agg['failed_or_missing'], '| author visual review: PENDING')
sys.exit(0 if agg['u6_technical_gates'] == 'PASS' else 3)
