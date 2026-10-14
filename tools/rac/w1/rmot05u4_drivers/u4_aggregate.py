# RM-OT-05U4: machine-readable aggregate for the opt-in U2 return check. Exit status 0 ONLY if the numerical stop conditions
# pass; any failed, missing or ambiguous mandatory item gives a nonzero status. It never implies author acceptance.
#   mandatory (numerical stop conditions): protection / U2 reintegration ACCEPTED; s_verify V1-U2 pass and no s_verify FAIL
#   verdict (existing hard rule); fixed-reference crease depth A and B PASS (sections compared BY IDENTITY against the frozen
#   reference); roughness guard (b) PASS; sliver guard (e) PASS.
#   reported, not waived (geometry gates with known unresolved status): V4, V6c-1, V6c-2 (and V6 historical).
#   pending (never automated): author visual review; real desktop mask / brush / protection fixtures.
import argparse, hashlib, json, os, sys
ap = argparse.ArgumentParser(); [ap.add_argument(k) for k in ('--reint', '--verify', '--crease', '--guards', '--ref', '--out')]; a = ap.parse_args()
def load(p):
    try: return json.load(open(p)) if p and os.path.exists(p) else None
    except Exception: return None
R, V, C, G, REF = (load(x) for x in (a.reint, a.verify, a.crease, a.guards, a.ref))
agg = dict(tool='RM-OT-05U4 aggregate', author_visual_review='PENDING', desktop_fixtures='PENDING (required after boundary approval, before production strokes)',
           note='ACCEPTED_FOR_VERIFICATION_U2 is protection only; it is not satisfaction of the stop conditions and not author acceptance.')
mand = {}
mand['protection_U2_reintegration'] = dict(status='PASS' if R and R.get('verdict') == 'ACCEPTED_FOR_VERIFICATION_U2' else 'FAIL', verdict=(R or {}).get('verdict', 'MISSING'), errors=(R or {}).get('errors', []))
if V:
    mand['V1_U2'] = dict(status='PASS' if V['V1_outside_anatomy']['pass_'] and V['V1_outside_anatomy'].get('mode') == 'U2 opt-in' else 'FAIL')
    mand['s_verify_no_FAIL_verdict'] = dict(status='PASS' if V.get('verdict_automated') != 'FAIL' else 'FAIL', verdict=V.get('verdict_automated'))
else:
    mand['V1_U2'] = dict(status='MISSING'); mand['s_verify_no_FAIL_verdict'] = dict(status='MISSING')
# crease, by identity
ref_secs = (REF or {}).get('sections', {}); fp = {k: hashlib.sha256(json.dumps(v, sort_keys=True).encode()).hexdigest() for k, v in ref_secs.items()}
for sid in ('A', 'B'):
    key = 'crease_depth_%s' % sid
    if not REF or sid not in ref_secs: mand[key] = dict(status='MISSING', error='frozen reference missing or lacks section %s' % sid); continue
    s = ((C or {}).get('sections') or {}).get(sid)
    if s is None: mand[key] = dict(status='MISSING', error='measurement lacks section %s' % sid); continue
    if s.get('section_id') != sid or s.get('fingerprint') != fp[sid] or s.get('anchor_s3_vertex') != ref_secs[sid]['anchor_s3_vertex'] or s.get('s0_cm') != ref_secs[sid]['s0_cm'] or s.get('threshold_cm') != ref_secs[sid]['threshold_cm']:
        mand[key] = dict(status='FAIL', error='section identity / reference fingerprint mismatch'); continue
    st = s.get('status', 'MISSING'); mand[key] = dict(status='PASS' if st == 'PASS' else st, depth_cm=s.get('depth_cm'), threshold_cm=s['threshold_cm'], error=s.get('error'))
if C and C.get('errors'): mand['crease_measurement_errors'] = dict(status='FAILED_MEASUREMENT', errors=C['errors'])
for g, k in (('b_roughness', 'roughness_guard_b'), ('e_sliver_guard', 'sliver_guard_e')):
    x = (G or {}).get(g); mand[k] = dict(status='MISSING') if x is None else dict(status='PASS' if x.get('pass_') else 'FAIL', **{kk: vv for kk, vv in x.items() if kk not in ('pass_', 'over_limit_examples')})
agg['mandatory'] = mand
agg['numerical_stop_conditions'] = 'PASS' if all(v['status'] == 'PASS' for v in mand.values()) else 'NOT MET'
agg['failed_or_missing'] = [k for k, v in mand.items() if v['status'] != 'PASS']
if V:
    agg['geometry_gates_reported'] = {k: v['pass_'] for k, v in V.items() if isinstance(v, dict) and 'pass_' in v}
    agg['geometry_gates_unresolved_disclosed_not_waived'] = {k: agg['geometry_gates_reported'].get(k) for k in ('V4_triangle_quality', 'V6c_1_garment_ledge_removed', 'V6c_2_taper_termination', 'V6_historical_05Q')}
    agg['s_verify_verdict'] = V.get('verdict_automated')
json.dump(agg, open(a.out, 'w'), indent=1)
print('numerical stop conditions:', agg['numerical_stop_conditions'], '| failed/missing:', agg['failed_or_missing'], '| author visual review: PENDING | desktop fixtures: PENDING')
sys.exit(0 if agg['numerical_stop_conditions'] == 'PASS' else 3)
