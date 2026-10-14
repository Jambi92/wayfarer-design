# RM-OT-05U6: focused DISPOSABLE tests for the corrected R1 / R2 guard logic and the U6 aggregate.
# Every edit is synthetic, on a COPY of the frozen 05U baseline return arrays: validator fixtures only, never a sculpt or candidate.
# Usage: python3 u6_tests.py --s3 GO-05S-S3.obj --base_check DIR_OF_U6_CHECK_ON_BASELINE --work DIR --out SUMMARY.json
import argparse, json, os, shutil, subprocess, sys, numpy as np
here = os.path.dirname(os.path.abspath(__file__)); G6 = os.path.join(here, 'u6_guards.py'); AG = os.path.join(here, 'u6_aggregate.py')
BASE = 'reviews/rac-rmot05u-evidence/checks/return/return.npz'; SETS = 'reviews/rac-rmot05u6-evidence/readiness/u6_sets_v1.json'; REF = 'reviews/rac-rmot05u4-readiness/crease_reference_v1.json'
ap = argparse.ArgumentParser(); [ap.add_argument(k) for k in ('--s3', '--base_check', '--work', '--out')]; a = ap.parse_args(); os.makedirs(a.work, exist_ok=True)
B = dict(np.load(BASE)); pos = {int(k): i for i, k in enumerate(B['s3_vid1'] - 1)}; SE = json.load(open(SETS))
E = np.load('reviews/rac-rmot05u2-proposal/proposal_sets.npz')['proposed_editable']
def npz(name, fn):
    dd = {k: (v.copy() if isinstance(v, np.ndarray) else v) for k, v in B.items()}; fn(dd); p = os.path.join(a.work, name + '.npz'); np.savez(p, **dd); return p
def guards(ret, name, sets=SETS):
    o = os.path.join(a.work, name + '_guards_u6.json'); p = subprocess.run([sys.executable, G6, '--s3', a.s3, '--ret', ret, '--sets', sets, '--out', o], capture_output=True, text=True)
    g = json.load(open(o)) if os.path.exists(o) else {}
    o2 = os.path.join(a.work, name + '_aggregate_u6.json'); b = a.base_check
    q = subprocess.run([sys.executable, AG, '--reint', os.path.join(b, 'result_u2_reintegrate.json'), '--verify', os.path.join(b, 'result_verify.json'),
                        '--crease', os.path.join(b, 'crease_measure.json'), '--guards6', o, '--ref', REF, '--out', o2], capture_output=True, text=True)
    return p.returncode, g, q.returncode, json.load(open(o2))
def mv(v, dvec):
    def f(dd): dd['V'][pos[v]] = (dd['V'][pos[v]].astype(np.float64) + np.asarray(dvec)).astype(np.float32)
    return f
T = []
def rec(test, expect, ok, **kw): T.append(dict(test=test, expected=expect, as_expected=bool(ok), **kw)); print(test, 'OK' if ok else 'UNEXPECTED')
# T1 unchanged baseline (U6 aggregate from the real full check run)
ag = json.load(open(os.path.join(a.base_check, 'aggregate_u6.json')))
rec('T1_unchanged_baseline_full_check', 'NOT MET on exactly R1 target roughness (4 in-target offenders) and R2 (face 130139 6.24 < 10); all other U6 gates PASS',
    sorted(ag['failed_or_missing']) == ['R1_target_roughness', 'R2_local_cap_quality'] and [x['s3_face'] for x in ag['mandatory']['R2_local_cap_quality']['below_min_angle']] == [130139],
    failed=ag['failed_or_missing'], target_over=ag['mandatory']['R1_target_roughness']['over_limit'])
# T2 baseline-exception identity: each exception moved 1e-3 cm -> identity FAIL (protection unaffected: they are inside the 365)
for v in SE['baseline_exception_vertices']:
    p = npz('T2_exception_%d' % v, mv(v, [1e-3, 0, 0])); rc, g, arc, ag = guards(p, 'T2_%d' % v)
    rec('T2_move_baseline_exception_%d' % v, 'R1 exception identity FAIL, aggregate nonzero', g['R1_baseline_exception_identity']['pass_'] is False and g['R1_baseline_exception_identity']['moved'] == [v] and arc == 3,
        moved=g['R1_baseline_exception_identity']['moved'], aggregate_exit=arc)
# T3 in-target offenders are not grandfathered: an edit elsewhere in the target leaves 61303 / 61581 above 36.3 -> FAIL
p = npz('T3_edit_target_offenders_remain', mv(62061, [0.002, 0, 0])); rc, g, arc, ag = guards(p, 'T3')
rec('T3_in_target_offender_still_fails', 'R1 target roughness FAIL (61303, 61581 > 36.3) although the file was edited', g['R1_target_roughness']['pass_'] is False and
    {x['s3_vertex'] for x in g['R1_target_roughness']['over_limit']} >= {61303, 61581} and arc == 3, over=g['R1_target_roughness']['over_limit'])
# T4 a cap face below 10 deg fails: (a) the source sliver 130139 at baseline; (b) NEW sub-10 faces created by pulling 61562 toward edge 61750-61580
#    (correction disclosed: the first expectation named face 129905, which stays at 13.07; its neighbours 130135 / 130137 drop below 10)
p = npz('T4b_new_sub10_face', lambda dd: dd['V'].__setitem__(pos[61562], (0.06 * dd['V'][pos[61562]].astype(np.float64) + 0.47 * (dd['V'][pos[61750]].astype(np.float64) + dd['V'][pos[61580]].astype(np.float64))).astype(np.float32)))
rc, g, arc, ag = guards(p, 'T4b'); low = [x['s3_face'] for x in g['R2_local_cap_quality']['below_min_angle']]
rec('T4_cap_face_below_10_fails', 'R2 FAIL listing 130139 at baseline (T1) and at least one newly created sub-10 face', g['R2_local_cap_quality']['pass_'] is False and any(f != 130139 for f in low) and arc == 3, below=g['R2_local_cap_quality']['below_min_angle'])
# T5 a safe cap face may lose some min angle while staying >= 10 without failing for that reason
p = npz('T5_safe_face_loses_angle', mv(62061, [0.0, 0.03, 0.0])); rc, g, arc, ag = guards(p, 'T5')
q = g['R2_local_cap_quality']; ret = g['historical_diagnostics']['retired_05U5_per_face_relative_sliver']['faces_worse_than_own_baseline']
safe_losers = [x for x in ret if x['now'] >= 10]
rec('T5_safe_face_loses_angle_not_failed_for_that', 'at least one cap face loses min angle but stays >= 10; R2 below-10 list is still only 130139 (no failure for the loss); the retired 05U5 rule would have flagged it',
    len(safe_losers) > 0 and [x['s3_face'] for x in q['below_min_angle']] == [130139] and not q['new_out_of_band_edges'] and not q['inverted'] and not q['degenerate'],
    safe_faces_losing_angle=safe_losers, R2_below_min=q['below_min_angle'])
# T6 an approved editable vertex outside the target moved -> locus FAIL (brush spill), although U2 protection would accept it
out = [int(v) for v in np.setdiff1d(E, SE['target_vertices']) if v not in SE['baseline_exception_vertices']][0]
p = npz('T6_outside_target', mv(out, [1e-3, 0, 0])); rc, g, arc, ag = guards(p, 'T6')
rec('T6_editable_outside_target_moved', 'locus FAIL', g['locus_outside_target_unchanged']['pass_'] is False and g['locus_outside_target_unchanged']['moved'] == [out] and arc == 3, vertex=out)
# T7 inverted cap face; T8 new out-of-band edge (> 2.5 cm)
def inv(dd):
    c = (dd['V'][pos[61750]].astype(np.float64) + dd['V'][pos[61580]].astype(np.float64)) / 2; x = dd['V'][pos[61562]].astype(np.float64); dd['V'][pos[61562]] = (2 * c - x).astype(np.float32)
p = npz('T7_inverted', inv); rc, g, arc, ag = guards(p, 'T7')
rec('T7_inverted_cap_face', 'R2 FAIL (inverted)', g['R2_local_cap_quality']['pass_'] is False and len(g['R2_local_cap_quality']['inverted']) > 0 and arc == 3, inverted=g['R2_local_cap_quality']['inverted'])
p = npz('T8_long_edge', mv(61562, [0, 0, 3.0])); rc, g, arc, ag = guards(p, 'T8')
rec('T8_new_out_of_band_edge', 'R2 FAIL (new edge > 2.5 cm)', g['R2_local_cap_quality']['pass_'] is False and len(g['R2_local_cap_quality']['new_out_of_band_edges']) > 0 and arc == 3,
    edges=g['R2_local_cap_quality']['new_out_of_band_edges'][:3])
# T9 tampered sets file; T10 non-finite coordinate in the target
bad = os.path.join(a.work, 'sets_tampered.json'); j = json.load(open(SETS)); j['min_angle_deg'] = 5.0; json.dump(j, open(bad, 'w'), indent=1, sort_keys=True)
rc, g, arc, ag = guards(BASE, 'T9', sets=bad)
rec('T9_tampered_sets_refused', 'guards refuse (nonzero), aggregate MISSING / FAILED_MEASUREMENT, nonzero', rc != 0 and arc == 3 and 'R2_local_cap_quality' in ag['failed_or_missing'], errors=g.get('errors'))
p = npz('T10_nan', lambda dd: dd['V'].__setitem__(pos[61581], np.array([np.nan, 0, 0], np.float32))); rc, g, arc, ag = guards(p, 'T10')
rec('T10_non_finite_target', 'R1 and R2 FAIL, nonzero', g['R1_target_roughness']['pass_'] is False and g['R2_local_cap_quality']['pass_'] is False and arc == 3)
json.dump(dict(tests=T, passed=sum(t['as_expected'] for t in T), total=len(T)), open(a.out, 'w'), indent=1)
print('%d / %d as expected' % (sum(t['as_expected'] for t in T), len(T)))
