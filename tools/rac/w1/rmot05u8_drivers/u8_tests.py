# RM-OT-05U8: focused DISPOSABLE tests for the U8 protection / safety verifier (order 05U8 section 4).
# Every edit is synthetic, on a COPY of the pinned U7 cp2 return arrays: validator fixtures only, never a sculpt or candidate.
# Usage: python3 u8_tests.py --s3 GO-05S-S3.obj --f1 F1_working.obj --base_check DIR_OF_U8_CHECK_ON_U7CP2 --work DIR --out SUMMARY.json
import argparse, json, os, subprocess, sys, numpy as np
here = os.path.dirname(os.path.abspath(__file__)); RI = os.path.join(here, 'u8_reintegrate.py'); G8 = os.path.join(here, 'u8_guards.py'); AG = os.path.join(here, 'u8_aggregate.py')
G6 = os.path.join(here, '..', 'rmot05u6_drivers', 'u6_guards.py'); G7 = os.path.join(here, '..', 'rmot05u7_drivers', 'u7_guards.py'); CK = os.path.join(here, 'check_return_u8.sh')
CP2 = 'reviews/rac-rmot05u7-evidence/return/checks/return.npz'; CP3 = 'reviews/rac-rmot05u6-evidence/return_u6a/checks/return.npz'
SETS = 'reviews/rac-rmot05u8-evidence/readiness'; SETS7 = 'reviews/rac-rmot05u7-evidence/readiness'; REF = 'reviews/rac-rmot05u4-readiness/crease_reference_v1.json'
U6SETS = 'reviews/rac-rmot05u6-evidence/readiness/u6_sets_v1.json'
ap = argparse.ArgumentParser(); [ap.add_argument(k) for k in ('--s3', '--f1', '--base_check', '--work', '--out')]; a = ap.parse_args(); os.makedirs(a.work, exist_ok=True)
B = dict(np.load(CP2)); pos = {int(k): i for i, k in enumerate(B['s3_vid1'] - 1)}; SE = json.load(open(os.path.join(SETS, 'u8_sets_v1.json')))
def npz(name, fn):
    dd = {k: (v.copy() if isinstance(v, np.ndarray) else v) for k, v in B.items()}; fn(dd); p = os.path.join(a.work, name + '.npz'); np.savez(p, **dd); return p
def run(ret, name):
    o = os.path.join(a.work, name); subprocess.run([sys.executable, RI, '--ret', ret, '--s3', a.s3, '--f1', a.f1, '--cp3', CP2, '--sets', SETS, '--out', o], capture_output=True)
    subprocess.run([sys.executable, G6, '--s3', a.s3, '--ret', ret, '--sets', U6SETS, '--out', o + '_guards_u6.json'], capture_output=True)
    subprocess.run([sys.executable, G7, '--s3', a.s3, '--ret', ret, '--cp3', CP3, '--sets', SETS7, '--out', o + '_guards_u7.json'], capture_output=True)
    subprocess.run([sys.executable, G8, '--s3', a.s3, '--ret', ret, '--cp2', CP2, '--sets', SETS, '--out', o + '_guards_u8.json'], capture_output=True)
    b = a.base_check; ri = json.load(open(o + '_u8_reintegrate.json'))
    verify = os.path.join(b, 'result_verify.json') if ri['verdict'] == 'ACCEPTED_FOR_VERIFICATION_U8' else os.path.join(a.work, 'none.json')   # s_verify only runs after protection acceptance
    q = subprocess.run([sys.executable, AG, '--reint', o + '_u8_reintegrate.json', '--verify', verify, '--crease', os.path.join(b, 'crease_measure.json'), '--guards6', o + '_guards_u6.json',
                        '--guards7', o + '_guards_u7.json', '--guards8', o + '_guards_u8.json', '--ref', REF, '--out', o + '_aggregate_u8.json'], capture_output=True)
    return ri, json.load(open(o + '_guards_u8.json')), q.returncode, json.load(open(o + '_aggregate_u8.json'))
def mv(v, d):
    def f(dd): dd['V'][pos[v]] = (dd['V'][pos[v]].astype(np.float64) + np.asarray(d)).astype(np.float32)
    return f
T = []
def rec(test, expect, ok, **kw): T.append(dict(test=test, expected=expect, as_expected=bool(ok), **kw)); print(test, 'OK' if ok else 'UNEXPECTED')
ag = json.load(open(os.path.join(a.base_check, 'aggregate_u8.json')))
rec('T0_unchanged_u7cp2_full_check', 'all U8 safety gates PASS, exit 0', ag['u8_safety_gates'] == 'PASS' and not ag['failed_or_missing'])
ri, g, rc, ag = run(npz('T1_61580', mv(61580, [1e-3, 0, 0])), 'T1')
rec('T1_move_crease_B_anchor_61580', 'protection REJECTED; 61580 reported moved; aggregate nonzero', ri['verdict'] == 'REJECTED' and ri['protection_vs_u7cp2']['anchor_61580_moved'] is True and rc == 3, errors=ri.get('errors'))
rv = 61994; ri, g, rc, ag = run(npz('T2_ring', mv(rv, [1e-3, 0, 0])), 'T2')
rec('T2_move_U8_frozen_ring_vertex', 'protection REJECTED, aggregate nonzero', rv in SE['frozen_ring'] and ri['verdict'] == 'REJECTED' and rc == 3, vertex=rv, errors=ri.get('errors'))
ri, g, rc, ag = run(npz('T3_u7cp2_vertex', mv(61771, [1e-3, 0, 0])), 'T3')
rec('T3_move_U7_cp2_vertex_61771_outside_U8', 'protection REJECTED (U7-edited vertex reported), aggregate nonzero', ri['verdict'] == 'REJECTED' and 61771 in ri['protection_vs_u7cp2']['u7_edited_moved'] and rc == 3)
def topo(dd): f = dd['F'].copy(); f[1000] = f[1000][[0, 2, 1]]; dd['F'] = f
ri, g, rc, ag = run(npz('T4_topology', topo), 'T4')
rec('T4_topology_change', 'protection REJECTED (face set differs), aggregate nonzero', ri['verdict'] == 'REJECTED' and rc == 3 and ri['topology']['extra_faces'] >= 1, errors=ri.get('errors'))
def sub10(dd):
    m = (dd['V'][pos[62482]].astype(np.float64) + dd['V'][pos[62649]].astype(np.float64)) / 2; x = dd['V'][pos[61940]].astype(np.float64); dd['V'][pos[61940]] = (m + 0.05 * (x - m)).astype(np.float32)
ri, g, rc, ag = run(npz('T5_sub10', sub10), 'T5')
rec('T5_sub10_U8_face', 'protection ACCEPTED (target vertex), U8 local quality FAIL (face 129896 below 10 deg), aggregate nonzero',
    ri['verdict'] == 'ACCEPTED_FOR_VERIFICATION_U8' and g['local_quality']['pass_'] is False and any(x['s3_face'] == 129896 for x in g['local_quality']['below_10deg']) and rc == 3,
    below=g['local_quality']['below_10deg'][:4])
p = npz('T6_legal_target_move', mv(61940, [0.0, -0.02, 0.0])); o = os.path.join(a.work, 'full_T6'); q = subprocess.run(['bash', CK, '--npz', p, o], capture_output=True, text=True)
ag = json.load(open(os.path.join(o, 'aggregate_u8.json')))
rec('T6_legal_small_target_move_full_check', 'protection ACCEPTED, all U8 safety gates PASS, exit 0', q.returncode == 0 and ag['u8_safety_gates'] == 'PASS' and ag['target_moved'] == [61940],
    exit_code=q.returncode, failed=ag['failed_or_missing'])
json.dump(dict(tests=T, passed=sum(t['as_expected'] for t in T), total=len(T)), open(a.out, 'w'), indent=1)
print('%d / %d as expected' % (sum(t['as_expected'] for t in T), len(T)))
