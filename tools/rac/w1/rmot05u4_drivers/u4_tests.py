# RM-OT-05U4: focused DISPOSABLE regression tests for the fixed crease reference and the aggregate result.
# Every edit is synthetic, on a COPY of the 05U baseline return arrays: validator fixtures only, not a sculpt or candidate.
# Usage: python3 u4_tests.py --s3 GO-05S-S3.obj --work DIR --out SUMMARY.json
import argparse, json, os, shutil, subprocess, sys, hashlib, numpy as np
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(here, '..', 'rmot05s_drivers')); import s_lib
CR = os.path.join(here, 'u4_crease_ref.py'); AG = os.path.join(here, 'u4_aggregate.py'); CK = os.path.join(here, 'check_return_u2.sh')
U3C = os.path.join(here, '..', 'rmot05u3_drivers', 'u3_crease.py')
BASE = 'reviews/rac-rmot05u-evidence/checks/return/return.npz'; PR = 'reviews/rac-rmot05u2-proposal'; REF = 'reviews/rac-rmot05u4-readiness/crease_reference_v1.json'
ap = argparse.ArgumentParser(); ap.add_argument('--s3'); ap.add_argument('--work'); ap.add_argument('--out'); a = ap.parse_args(); os.makedirs(a.work, exist_ok=True)
ref = json.load(open(REF)); fr = s_lib.Frame('reviews/rac-rmot05q-evidence/plan/patch_selection.json'); d = np.asarray(fr.d, float)
B = dict(np.load(BASE)); ids0 = B['s3_vid1'] - 1; pos = {int(k): i for i, k in enumerate(ids0)}
E = set(np.load(os.path.join(PR, 'proposal_sets.npz'))['proposed_editable'].tolist())
def npz(name, fn):
    dd = {k: (v.copy() if isinstance(v, np.ndarray) else v) for k, v in B.items()}; fn(dd); p = os.path.join(a.work, name + '.npz'); np.savez(p, **dd); return p
def measure(ret, name, refp=REF, ref_sha=None):
    o = os.path.join(a.work, name + '_crease.json'); cmd = [sys.executable, CR, 'measure', '--s3', a.s3, '--proposal', PR, '--ret', ret, '--ref', refp, '--out', o] + (['--ref_sha', ref_sha] if ref_sha else [])
    p = subprocess.run(cmd, capture_output=True, text=True); return p.returncode, json.load(open(o))
def full(ret, name):
    o = os.path.join(a.work, 'full_' + name); p = subprocess.run(['bash', CK, '--npz', ret, o], capture_output=True, text=True)
    return p.returncode, json.load(open(os.path.join(o, 'aggregate.json')))
T = []
def rec(test, expect, ok, **kw): T.append(dict(test=test, expected=expect, as_expected=bool(ok), **kw)); print(test, 'OK' if ok else 'UNEXPECTED')
# T1 unchanged baseline (full aggregate)
rc, ag = full(BASE, 'T1_unchanged')
m = ag['mandatory']
rec('T1_unchanged_baseline', 'protection PASS, crease A/B PASS at frozen sections with baseline depths, roughness FAIL (expected baseline failure), exit nonzero',
    m['protection_U2_reintegration']['status'] == 'PASS' and m['crease_depth_A']['status'] == 'PASS' and m['crease_depth_B']['status'] == 'PASS'
    and abs(m['crease_depth_A']['depth_cm'] - ref['sections']['A']['baseline_depth_cm']) < 1e-12 and abs(m['crease_depth_B']['depth_cm'] - ref['sections']['B']['baseline_depth_cm']) < 1e-12
    and m['roughness_guard_b']['status'] == 'FAIL' and rc == 3, exit_code=rc, numerical_stop_conditions=ag['numerical_stop_conditions'], failed_or_missing=ag['failed_or_missing'],
    depth_A=m['crease_depth_A']['depth_cm'], depth_B=m['crease_depth_B']['depth_cm'])
# T2 move each named editable anchor +0.02 cm along the arm axis: frozen planes / anchors / chords / thresholds invariant
for anc, sid in ((61581, 'A'), (61580, 'B')):
    def mv(dd, v=anc): dd['V'][pos[v]] = (dd['V'][pos[v]].astype(np.float64) + 0.02 * d).astype(np.float32)
    p = npz('T2_move_%d' % anc, mv); rc, r = measure(p, 'T2_%d' % anc)
    o3 = os.path.join(a.work, 'T2_u3_%d' % anc); subprocess.run([sys.executable, U3C, '--s3', a.s3, '--baseline', p, '--proposal', PR, '--out', o3], capture_output=True)
    old = {x['name']: x['s0_cm'] for x in json.load(open(os.path.join(o3, 'crease_baseline.json')))['results']}
    inv = all(r['sections'][k]['s0_cm'] == ref['sections'][k]['s0_cm'] and r['sections'][k]['threshold_cm'] == ref['sections'][k]['threshold_cm']
              and r['sections'][k].get('endpoint_deviation_cm') == [0.0, 0.0] for k in ('A', 'B'))
    rec('T2_move_%d_along_axis_+0.02' % anc, 'fixed planes, anchors, chords and thresholds invariant (depth may change)', inv and r['status'] in ('PASS', 'FAIL'),
        fixed_s0={k: r['sections'][k]['s0_cm'] for k in ('A', 'B')}, measured_depth={k: r['sections'][k].get('depth_cm') for k in ('A', 'B')},
        endpoint_deviation_cm={k: r['sections'][k].get('endpoint_deviation_cm') for k in ('A', 'B')}, historical_u3_moving_plane_s0=old)
# T3 synthetic flattening inside the allowed region crossing the fixed 75 % limit of section A
S = ref['sections']['A']; A_ = np.array(S['chord_A']); n = np.array(S['inward_n'])
def flat(dd):
    for k in E:
        i = pos[k]; x = dd['V'][i].astype(np.float64); s = (x - fr.O) @ d - S['s0_cm']; dep = (x - A_) @ n
        if abs(s) < 1.5 and dep > 0: dd['V'][i] = (x - 0.6 * dep * n).astype(np.float32)
p = npz('T3_flatten_A', flat); rc, ag = full(p, 'T3_flatten_A'); m = ag['mandatory']
rec('T3_flattening_crosses_fixed_75pct_A', 'protection PASS (allowed region only), crease A FAIL at the same fixed section, nonzero exit',
    m['protection_U2_reintegration']['status'] == 'PASS' and m['crease_depth_A']['status'] == 'FAIL' and rc == 3,
    exit_code=rc, crease_A=m['crease_depth_A'], crease_B=m['crease_depth_B'], s0_A_used=json.load(open(os.path.join(a.work, 'full_T3_flatten_A', 'crease_measure.json')))['sections']['A']['s0_cm'])
# T4 failed measurement cases
rc, r = measure(BASE, 'T4a_missing_ref', refp=os.path.join(a.work, 'no_such_ref.json'))
rec('T4a_missing_reference', 'FAILED_MEASUREMENT, nonzero', r['status'] == 'FAILED_MEASUREMENT' and rc != 0, errors=r['errors'])
bad = os.path.join(a.work, 'ref_altered.json'); j = json.load(open(REF)); j['sections']['A']['threshold_cm'] = 0.1; json.dump(j, open(bad, 'w'), sort_keys=True, indent=1)
rc, r = measure(BASE, 'T4b_altered_ref', refp=bad)
rec('T4b_altered_reference_hash', 'FAILED_MEASUREMENT (hash mismatch), nonzero', r['status'] == 'FAILED_MEASUREMENT' and rc != 0, errors=r['errors'])
run_faces = ref['sections']['A']['baseline_run_faces']
import trimesh
Fs = np.asarray(trimesh.load(a.s3, process=False).faces); runv = sorted(set(int(v) for f in run_faces for v in Fs[f]) & E)
def nanv(dd): dd['V'][pos[runv[0]], 0] = np.float32('nan')
p = npz('T4c_nonfinite', nanv); rc, r = measure(p, 'T4c_nonfinite'); rc2, ag = full(p, 'T4c_nonfinite')
rec('T4c_non_finite_geometry_in_run', 'FAILED_MEASUREMENT for A, protection REJECTED (non-finite), aggregate NOT MET, nonzero', r['sections']['A']['status'] == 'FAILED_MEASUREMENT' and rc != 0 and rc2 == 3 and ag['mandatory']['protection_U2_reintegration']['status'] == 'FAIL',
    section_A=r['sections']['A'], aggregate=ag['numerical_stop_conditions'], protection=ag['mandatory']['protection_U2_reintegration']['verdict'])
# T4d unexpected entry/exit geometry. With the frozen ring bit-exact, exactly two region-boundary edges cross each frozen plane
# (verified at build), so the run cannot exit elsewhere unless frozen geometry moves; these fixtures therefore simulate a
# protection breach and check that the MEASUREMENT fails on its own (independently of the protection verdict).
Sx = ref['sections']['A']
def breach_entry(dd): v = Sx['entry_edge'][0]; dd['V'][pos[v]] = (dd['V'][pos[v]].astype(np.float64) + 0.01 * np.array(Sx['inward_n'])).astype(np.float32)
p = npz('T4d1_entry_vertex_moved', breach_entry); rc, r = measure(p, 'T4d1'); rc2, ag = full(p, 'T4d1')
rec('T4d1_frozen_entry_vertex_moved_0.01', 'measurement FAILED (chord endpoint moved), protection REJECTED, aggregate NOT MET', r['sections']['A']['status'] == 'FAILED_MEASUREMENT' and rc != 0 and rc2 == 3
    and ag['mandatory']['protection_U2_reintegration']['status'] == 'FAIL', section_A={k: r['sections']['A'].get(k) for k in ('status', 'error')})
def breach_exit(dd):
    for v in Sx['exit_edge']:
        x = dd['V'][pos[v]].astype(np.float64); s_ = (x - fr.O) @ d - Sx['s0_cm']; dd['V'][pos[v]] = (x - (s_ + 0.05) * d).astype(np.float32)
p = npz('T4d2_exit_edge_across_plane', breach_exit); rc, r = measure(p, 'T4d2')
rec('T4d2_frozen_exit_edge_moved_across_plane', 'measurement FAILED (unexpected exit / no crossing); no substitute section', r['sections']['A']['status'] == 'FAILED_MEASUREMENT' and rc != 0,
    section_A={k: r['sections']['A'].get(k) for k in ('status', 'error')})
def far(dd):
    for k in runv: dd['V'][pos[k]] = (dd['V'][pos[k]].astype(np.float64) + 3.0 * d).astype(np.float32)
p = npz('T4e_gross_axial_push', far); rc, ag = full(p, 'T4e_gross_axial_push'); m = ag['mandatory']
rec('T4e_gross_push_of_run_vertices_informative', 'depth alone may still pass at the fixed section; the aggregate must NOT pass (other mandatory guards)', rc == 3 and ag['numerical_stop_conditions'] == 'NOT MET',
    crease_A=m['crease_depth_A'].get('status'), crease_A_depth=m['crease_depth_A'].get('depth_cm'), failed_or_missing=ag['failed_or_missing'])
# T5 identity: sections omitted / swapped / truncated in the measurement handed to the aggregate
_, good = measure(BASE, 'T5_good'); gp = os.path.join(a.work, 'T5_good_crease.json')
def agg_with(name, mutate):
    j = json.load(open(gp)); mutate(j); p = os.path.join(a.work, name + '.json'); json.dump(j, open(p, 'w'))
    o = os.path.join(a.work, name + '_agg.json'); rr = subprocess.run([sys.executable, AG, '--reint', os.path.join(a.work, 'full_T1_unchanged', 'result_u2_reintegrate.json'), '--verify', os.path.join(a.work, 'full_T1_unchanged', 'result_verify.json'),
                                                                     '--crease', p, '--guards', os.path.join(a.work, 'full_T1_unchanged', 'guards.json'), '--ref', REF, '--out', o], capture_output=True)
    return rr.returncode, json.load(open(o))['mandatory']
rc, mm = agg_with('T5a_omit_B', lambda j: j['sections'].pop('B'))
rec('T5a_section_B_omitted', 'crease_depth_B MISSING, nonzero', mm['crease_depth_B']['status'] == 'MISSING' and rc != 0, crease_B=mm['crease_depth_B'])
def swap(j): j['sections']['A'], j['sections']['B'] = j['sections']['B'], j['sections']['A']
rc, mm = agg_with('T5b_swapped', swap)
rec('T5b_sections_swapped', 'identity / fingerprint mismatch FAIL for both, nonzero', mm['crease_depth_A']['status'] == 'FAIL' and mm['crease_depth_B']['status'] == 'FAIL' and rc != 0, A=mm['crease_depth_A'], B=mm['crease_depth_B'])
rc, mm = agg_with('T5c_truncated', lambda j: j.update(sections={}))
rec('T5c_sections_truncated', 'both MISSING, nonzero', mm['crease_depth_A']['status'] == 'MISSING' and mm['crease_depth_B']['status'] == 'MISSING' and rc != 0)
def relabel(j): j['sections']['A']['threshold_cm'] = 0.01
rc, mm = agg_with('T5d_threshold_tampered', relabel)
rec('T5d_threshold_tampered_in_result', 'FAIL (does not match frozen reference), nonzero', mm['crease_depth_A']['status'] == 'FAIL' and rc != 0)
_, r_alt = measure(BASE, 'T4b2_altered_ref_selfpinned', refp=bad, ref_sha=hashlib.sha256(open(bad, 'rb').read()).hexdigest())
alt = json.load(open(os.path.join(a.work, 'T4b2_altered_ref_selfpinned_crease.json')))
rc, mm = agg_with('T4b2_result_from_altered_ref', lambda j: j.update(sections=alt['sections']))
rec('T4b2_measurement_made_with_altered_reference', 'aggregate (checked against the pinned frozen reference) FAIL by fingerprint, nonzero',
    mm['crease_depth_A']['status'] == 'FAIL' and rc != 0, crease_A=mm['crease_depth_A'], note='--ref_sha is a test hook; check_return_u2.sh never passes it')
summ = dict(note='Disposable validator fixtures on copies of the 05U baseline arrays; NOT a sculpt, NOT a candidate, NOT a substitute for real desktop fixtures.',
            reference=REF, reference_sha256=hashlib.sha256(open(REF, 'rb').read()).hexdigest(), tests=T, all_as_expected=all(t['as_expected'] for t in T))
json.dump(summ, open(a.out, 'w'), indent=1); print('all_as_expected', summ['all_as_expected'])
