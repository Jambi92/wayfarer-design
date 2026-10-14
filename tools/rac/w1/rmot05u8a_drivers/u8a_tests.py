# RM-OT-05U8A: focused DISPOSABLE tests for the U8A protection / safety verifier (order 05U8A section 4).
# Every edit is synthetic, on a COPY of the pinned U8 cp1 return arrays: validator fixtures only, never a sculpt or candidate.
# Usage: python3 u8a_tests.py --s3 GO-05S-S3.obj --f1 F1_working.obj --base_check DIR_OF_U8A_CHECK_ON_U8CP1 --work DIR --out SUMMARY.json
import argparse, json, os, subprocess, sys, numpy as np
here = os.path.dirname(os.path.abspath(__file__)); RI = os.path.join(here, 'u8a_reintegrate.py'); GA = os.path.join(here, 'u8a_guards.py'); AG = os.path.join(here, 'u8a_aggregate.py')
W1 = os.path.join(here, '..'); G6 = os.path.join(W1, 'rmot05u6_drivers', 'u6_guards.py'); G7 = os.path.join(W1, 'rmot05u7_drivers', 'u7_guards.py'); G8 = os.path.join(W1, 'rmot05u8_drivers', 'u8_guards.py')
CR = os.path.join(W1, 'rmot05u4_drivers', 'u4_crease_ref.py'); CK = os.path.join(here, 'check_return_u8a.sh')
CP1 = 'reviews/rac-rmot05u8-evidence/return/checks/return.npz'; CP2 = 'reviews/rac-rmot05u7-evidence/return/checks/return.npz'; CP3 = 'reviews/rac-rmot05u6-evidence/return_u6a/checks/return.npz'
SETSA = 'reviews/rac-rmot05u8a-evidence/readiness'; SETS8 = 'reviews/rac-rmot05u8-evidence/readiness'; SETS7 = 'reviews/rac-rmot05u7-evidence/readiness'
REF = 'reviews/rac-rmot05u4-readiness/crease_reference_v1.json'; U6SETS = 'reviews/rac-rmot05u6-evidence/readiness/u6_sets_v1.json'; PR = 'reviews/rac-rmot05u2-proposal'
ap = argparse.ArgumentParser(); [ap.add_argument(k) for k in ('--s3', '--f1', '--base_check', '--work', '--out')]; a = ap.parse_args(); os.makedirs(a.work, exist_ok=True)
B = dict(np.load(CP1)); pos = {int(k): i for i, k in enumerate(B['s3_vid1'] - 1)}; ref = json.load(open(REF))
base_cr = json.load(open(os.path.join(a.base_check, 'crease_measure.json')))['sections']
def npz(name, fn):
    dd = {k: (v.copy() if isinstance(v, np.ndarray) else v) for k, v in B.items()}; fn(dd); p = os.path.join(a.work, name + '.npz'); np.savez(p, **dd); return p
def run(ret, name):
    o = os.path.join(a.work, name); subprocess.run([sys.executable, RI, '--ret', ret, '--s3', a.s3, '--f1', a.f1, '--cp3', CP1, '--sets', SETSA, '--out', o], capture_output=True)
    subprocess.run([sys.executable, G6, '--s3', a.s3, '--ret', ret, '--sets', U6SETS, '--out', o + '_guards_u6.json'], capture_output=True)
    subprocess.run([sys.executable, G7, '--s3', a.s3, '--ret', ret, '--cp3', CP3, '--sets', SETS7, '--out', o + '_guards_u7.json'], capture_output=True)
    subprocess.run([sys.executable, G8, '--s3', a.s3, '--ret', ret, '--cp2', CP2, '--sets', SETS8, '--out', o + '_guards_u8.json'], capture_output=True)
    subprocess.run([sys.executable, GA, '--s3', a.s3, '--ret', ret, '--cp2', CP1, '--sets', SETSA, '--out', o + '_guards_u8a.json'], capture_output=True)
    subprocess.run([sys.executable, CR, 'measure', '--s3', a.s3, '--proposal', PR, '--ret', ret, '--ref', REF, '--out', o + '_crease.json'], capture_output=True)
    b = a.base_check; ri = json.load(open(o + '_u8a_reintegrate.json'))
    verify = os.path.join(b, 'result_verify.json') if ri['verdict'] == 'ACCEPTED_FOR_VERIFICATION_U8A' else os.path.join(a.work, 'none.json')   # s_verify runs only after protection acceptance
    q = subprocess.run([sys.executable, AG, '--reint', o + '_u8a_reintegrate.json', '--verify', verify, '--crease', o + '_crease.json', '--guards6', o + '_guards_u6.json', '--guards7', o + '_guards_u7.json',
                        '--guards8', o + '_guards_u8.json', '--guards8a', o + '_guards_u8a.json', '--ref', REF, '--out', o + '_aggregate_u8a.json'], capture_output=True)
    return ri, json.load(open(o + '_guards_u8a.json')), json.load(open(o + '_crease.json')), q.returncode, json.load(open(o + '_aggregate_u8a.json'))
def mv(v, d):
    def f(dd): dd['V'][pos[v]] = (dd['V'][pos[v]].astype(np.float64) + np.asarray(d)).astype(np.float32)
    return f
N81 = np.array([0.62, -0.67, -0.41]); N81 /= np.linalg.norm(N81); N80 = np.array([0.62, -0.73, -0.28]); N80 /= np.linalg.norm(N80)   # cp1 vertex normals (diagnostics)
T = []
def rec(test, expect, ok, **kw): T.append(dict(test=test, expected=expect, as_expected=bool(ok), **kw)); print(test, 'OK' if ok else 'UNEXPECTED')
ag = json.load(open(os.path.join(a.base_check, 'aggregate_u8a.json')))
rec('T0_unchanged_u8cp1_full_check', 'all U8A safety gates PASS, exit 0', ag['u8a_safety_gates'] == 'PASS' and not ag['failed_or_missing'])
ri, g, c, rc, ag = run(npz('T1_other_vertex', mv(61562, [1e-3, 0, 0])), 'T1')
rec('T1_move_vertex_other_than_anchors_61562', 'protection REJECTED (U8 cp1 edit reported moved), aggregate nonzero', ri['verdict'] == 'REJECTED' and 61562 in ri['protection_vs_u8cp1']['u8_edited_moved'] and rc == 3)
def topo(dd): f = dd['F'].copy(); f[1000] = f[1000][[0, 2, 1]]; dd['F'] = f
ri, g, c, rc, ag = run(npz('T2_topology', topo), 'T2')
rec('T2_topology_change', 'protection REJECTED, aggregate nonzero', ri['verdict'] == 'REJECTED' and rc == 3 and ri['topology']['extra_faces'] >= 1)
def sub10(dd):
    m = (dd['V'][pos[61405]].astype(np.float64) + dd['V'][pos[61219]].astype(np.float64)) / 2; x = dd['V'][pos[61581]].astype(np.float64); dd['V'][pos[61581]] = (m + 0.05 * (x - m)).astype(np.float32)
ri, g, c, rc, ag = run(npz('T3_sub10', sub10), 'T3')
rec('T3_sub10_affected_face', 'protection ACCEPTED (anchor), U8A local quality FAIL (face 130139 below 10 deg), aggregate nonzero',
    ri['verdict'] == 'ACCEPTED_FOR_VERIFICATION_U8A' and g['local_quality']['pass_'] is False and any(x['s3_face'] == 130139 for x in g['local_quality']['below_10deg']) and rc == 3)
ri, g, c, rc, ag = run(npz('T4_legal_61581', mv(61581, 0.02 * N81)), 'T4')
rec('T4_legal_tiny_61581_move', 'protection ACCEPTED; crease A depth updates (differs from cp1) at the SAME frozen section; all gates PASS',
    ri['verdict'] == 'ACCEPTED_FOR_VERIFICATION_U8A' and c['sections']['A']['depth_cm'] != base_cr['A']['depth_cm'] and c['sections']['A']['s0_cm'] == ref['sections']['A']['s0_cm'] and rc == 0,
    depth_A=[base_cr['A']['depth_cm'], c['sections']['A']['depth_cm']], depth_B=[base_cr['B']['depth_cm'], c['sections']['B']['depth_cm']], exit_code=rc, failed=ag['failed_or_missing'])
ri, g, c, rc, ag = run(npz('T5_legal_61580', mv(61580, 0.02 * N80)), 'T5')
# correction disclosed: the first expectation required the B DEPTH to change; B's deepest point lies near 62086 (x ~29.43), away from 61580, so a
# 0.02 cm 61580 lift re-routes the measured section (run 9 -> 7 faces) while the maximum depth is unchanged. The measurement IS recomputed.
rec('T5_legal_tiny_61580_move', 'protection ACCEPTED; crease B re-measured at the SAME frozen section (section path / depth recomputed from the moved mesh); all gates PASS',
    ri['verdict'] == 'ACCEPTED_FOR_VERIFICATION_U8A' and c['sections']['B']['s0_cm'] == ref['sections']['B']['s0_cm'] and (c['sections']['B']['run_faces'] != base_cr['B']['run_faces'] or c['sections']['B']['depth_cm'] != base_cr['B']['depth_cm']) and rc == 0,
    run_faces_B=[base_cr['B']['run_faces'], c['sections']['B']['run_faces']],
    depth_A=[base_cr['A']['depth_cm'], c['sections']['A']['depth_cm']], depth_B=[base_cr['B']['depth_cm'], c['sections']['B']['depth_cm']], exit_code=rc, failed=ag['failed_or_missing'])
nA = np.array(ref['sections']['A']['inward_n'])
ri, g, c, rc, ag = run(npz('T6_crease_A_below', mv(61581, -0.2 * nA)), 'T6')
rec('T6_move_pushes_crease_A_below_threshold', 'protection ACCEPTED (anchor), crease A FAIL at the frozen threshold, aggregate nonzero',
    ri['verdict'] == 'ACCEPTED_FOR_VERIFICATION_U8A' and ag['mandatory']['crease_depth_A']['status'] == 'FAIL' and rc == 3,
    depth_A=c['sections']['A'].get('depth_cm'), threshold=ref['sections']['A']['threshold_cm'], failed=ag['failed_or_missing'])
json.dump(dict(tests=T, passed=sum(t['as_expected'] for t in T), total=len(T)), open(a.out, 'w'), indent=1)
print('%d / %d as expected' % (sum(t['as_expected'] for t in T), len(T)))
