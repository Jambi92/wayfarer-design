# RM-OT-05U7: focused DISPOSABLE tests for the U7 protection / safety verifier (order 05U7 section 3).
# Every edit is synthetic, on a COPY of the pinned U6A cp3 return arrays: validator fixtures only, never a sculpt or candidate.
# Usage: python3 u7_tests.py --s3 GO-05S-S3.obj --f1 F1_working.obj --base_check DIR_OF_U7_CHECK_ON_CP3 --work DIR --out SUMMARY.json
import argparse, json, os, subprocess, sys, numpy as np, trimesh
from collections import defaultdict
here = os.path.dirname(os.path.abspath(__file__)); RI = os.path.join(here, 'u7_reintegrate.py'); G7 = os.path.join(here, 'u7_guards.py'); AG = os.path.join(here, 'u7_aggregate.py')
G6 = os.path.join(here, '..', 'rmot05u6_drivers', 'u6_guards.py'); CK = os.path.join(here, 'check_return_u7.sh')
CP3 = 'reviews/rac-rmot05u6-evidence/return_u6a/checks/return.npz'; SETS = 'reviews/rac-rmot05u7-evidence/readiness'; REF = 'reviews/rac-rmot05u4-readiness/crease_reference_v1.json'
U6SETS = 'reviews/rac-rmot05u6-evidence/readiness/u6_sets_v1.json'
ap = argparse.ArgumentParser(); [ap.add_argument(k) for k in ('--s3', '--f1', '--base_check', '--work', '--out')]; a = ap.parse_args(); os.makedirs(a.work, exist_ok=True)
B = dict(np.load(CP3)); pos = {int(k): i for i, k in enumerate(B['s3_vid1'] - 1)}; SE = json.load(open(os.path.join(SETS, 'u7_sets_v1.json')))
F = np.asarray(trimesh.load(a.s3, process=False).faces); nb = defaultdict(set)
for f in F:
    for x in f: nb[int(x)].update(int(y) for y in f if y != x)
def npz(name, fn):
    dd = {k: (v.copy() if isinstance(v, np.ndarray) else v) for k, v in B.items()}; fn(dd); p = os.path.join(a.work, name + '.npz'); np.savez(p, **dd); return p
def run(ret, name):
    o = os.path.join(a.work, name); subprocess.run([sys.executable, RI, '--ret', ret, '--s3', a.s3, '--f1', a.f1, '--cp3', CP3, '--sets', SETS, '--out', o], capture_output=True)
    subprocess.run([sys.executable, G6, '--s3', a.s3, '--ret', ret, '--sets', U6SETS, '--out', o + '_guards_u6.json'], capture_output=True)
    subprocess.run([sys.executable, G7, '--s3', a.s3, '--ret', ret, '--cp3', CP3, '--sets', SETS, '--out', o + '_guards_u7.json'], capture_output=True)
    b = a.base_check; ri = json.load(open(o + '_u7_reintegrate.json'))
    verify = os.path.join(b, 'result_verify.json') if ri['verdict'] == 'ACCEPTED_FOR_VERIFICATION_U7' else os.path.join(a.work, 'none.json')   # s_verify only runs after protection acceptance
    q = subprocess.run([sys.executable, AG, '--reint', o + '_u7_reintegrate.json', '--verify', verify, '--crease', os.path.join(b, 'crease_measure.json'),
                        '--guards6', o + '_guards_u6.json', '--guards7', o + '_guards_u7.json', '--ref', REF, '--out', o + '_aggregate_u7.json'], capture_output=True)
    return ri, json.load(open(o + '_guards_u7.json')), q.returncode, json.load(open(o + '_aggregate_u7.json'))
def mv(v, d):
    def f(dd): dd['V'][pos[v]] = (dd['V'][pos[v]].astype(np.float64) + np.asarray(d)).astype(np.float32)
    return f
T = []
def rec(test, expect, ok, **kw): T.append(dict(test=test, expected=expect, as_expected=bool(ok), **kw)); print(test, 'OK' if ok else 'UNEXPECTED')
tgt = set(SE['target_vertices']); ring = set(SE['frozen_ring'])
# T0 unchanged cp3 (real full check run)
ag = json.load(open(os.path.join(a.base_check, 'aggregate_u7.json')))
rec('T0_unchanged_cp3_full_check', 'all U7 safety gates PASS, exit 0', ag['u7_safety_gates'] == 'PASS' and not ag['failed_or_missing'])
# T1 a vertex just outside the U7 target and its frozen ring (second topological ring)
out = sorted(v for r in ring for v in nb[r] if v not in tgt and v not in ring)[0]
ri, g, rc, ag = run(npz('T1_outside_target', mv(out, [1e-3, 0, 0])), 'T1')
rec('T1_move_vertex_just_outside_U7_target', 'protection REJECTED (moved outside target), aggregate nonzero', ri['verdict'] == 'REJECTED' and rc == 3, vertex=out, errors=ri.get('errors'))
# T2 a U7 frozen-ring vertex
rv = 61735; ri, g, rc, ag = run(npz('T2_ring', mv(rv, [1e-3, 0, 0])), 'T2')
rec('T2_move_U7_frozen_ring_vertex', 'protection REJECTED, aggregate nonzero', rv in ring and ri['verdict'] == 'REJECTED' and rc == 3, vertex=rv, errors=ri.get('errors'))
# T2b the held seed 61522 (frozen crease-B entry endpoint, in the U7 ring)
ri, g, rc, ag = run(npz('T2b_seed61522', mv(61522, [1e-3, 0, 0])), 'T2b')
rec('T2b_move_held_seed_61522', 'protection REJECTED (61522 is frozen)', ri['verdict'] == 'REJECTED' and rc == 3)
# T3 an old U6 cp3 vertex (no U7 overlap exists)
ri, g, rc, ag = run(npz('T3_u6_vertex', mv(61581, [1e-3, 0, 0])), 'T3')
rec('T3_move_U6_cp3_vertex_61581', 'protection REJECTED, aggregate nonzero', ri['verdict'] == 'REJECTED' and rc == 3, errors=ri.get('errors'))
# T4 a sub-10 deg U7 face: 61183 pulled onto edge 61146-60910 of face 129671
def sub10(dd):
    m = (dd['V'][pos[61146]].astype(np.float64) + dd['V'][pos[60910]].astype(np.float64)) / 2; x = dd['V'][pos[61183]].astype(np.float64); dd['V'][pos[61183]] = (m + 0.05 * (x - m)).astype(np.float32)
ri, g, rc, ag = run(npz('T4_sub10', sub10), 'T4')
rec('T4_sub10_U7_face', 'protection ACCEPTED (target vertex), U7 local quality FAIL (face below 10 deg), aggregate nonzero',
    ri['verdict'] == 'ACCEPTED_FOR_VERIFICATION_U7' and g['local_quality']['pass_'] is False and any(x['s3_face'] == 129671 for x in g['local_quality']['below_10deg']) and rc == 3,
    below=g['local_quality']['below_10deg'][:4])
# T5 topology change: one face reversed in the export
def topo(dd): f = dd['F'].copy(); f[1000] = f[1000][[0, 2, 1]]; dd['F'] = f
ri, g, rc, ag = run(npz('T5_topology', topo), 'T5')
rec('T5_topology_change', 'protection REJECTED (face set differs), aggregate nonzero', ri['verdict'] == 'REJECTED' and rc == 3 and ri['topology']['extra_faces'] >= 1, errors=ri.get('errors'))
# T6 positive: a small legal move of one target vertex (61586, 0.02 cm) is accepted by protection and the local guards (full check)
p = npz('T6_legal_target_move', mv(61586, [0.0, -0.02, 0.0])); o = os.path.join(a.work, 'full_T6'); q = subprocess.run(['bash', CK, '--npz', p, o], capture_output=True, text=True)
ag = json.load(open(os.path.join(o, 'aggregate_u7.json')))
rec('T6_legal_small_target_move_full_check', 'protection ACCEPTED, all U7 safety gates PASS, exit 0', q.returncode == 0 and ag['u7_safety_gates'] == 'PASS' and ag['target_moved'] == [61586],
    exit_code=q.returncode, failed=ag['failed_or_missing'])
json.dump(dict(tests=T, passed=sum(t['as_expected'] for t in T), total=len(T)), open(a.out, 'w'), indent=1)
print('%d / %d as expected' % (sum(t['as_expected'] for t in T), len(T)))
