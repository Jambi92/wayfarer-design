# RM-OT-05V: focused DISPOSABLE tests of the checkpoint verifier (v_verify.py). Synthetic edits on COPIES of a real step result
# (C1 +X lower-leg rebuild applied to the frozen U8 cp1 state); fixtures only, never candidates.
# Usage: python3 v_tests.py --u8 RETURN.npz --work DIR --out SUMMARY.json
import argparse, json, os, subprocess, sys, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import v_chain
from v_engine import eval_region, edges_of
ap = argparse.ArgumentParser(); [ap.add_argument(k) for k in ('--u8', '--work', '--out')]; a = ap.parse_args(); w = os.path.abspath(a.work); os.makedirs(w, exist_ok=True)
R = np.load(a.u8); n0 = os.path.join(w, 'N0.npz')
np.savez_compressed(n0, V=R['V'], F=R['F'].astype(np.int64), vid=R['s3_vid1'].astype(np.int64), fgrp=np.zeros(len(R['F']), np.int8))
st = v_chain.lower_leg(+1, 3000000); sp = os.path.join(w, 'step.json'); json.dump(st, open(sp, 'w'))
base = os.path.join(w, 'base.npz')
subprocess.run([sys.executable, os.path.join(HERE, 'v_rebuild.py'), '--state', n0, '--step', sp, '--out', base], check=True, capture_output=True)
B = dict(np.load(base)); P = np.load(n0); T = []
def verify(name, mut):
    d = {k: v.copy() for k, v in B.items() if k != 'meta'}; mut(d); p = os.path.join(w, name + '.npz'); np.savez_compressed(p, **d)
    r = subprocess.run([sys.executable, os.path.join(HERE, 'v_verify.py'), '--prev', n0, '--new', p, '--step', sp, '--out', p.replace('.npz', '_v.json')], capture_output=True, text=True)
    return r.returncode, json.load(open(p.replace('.npz', '_v.json')))
def rec(test, expect, ok, **kw): T.append(dict(test=test, expected=expect, as_expected=bool(ok), **kw)); print(test, 'OK' if ok else 'UNEXPECTED', flush=True)
g = eval_region(st['region'], B['V'].astype(float)); newv = np.where(B['vid'] >= 3000000)[0]
outv = np.where((g > 5) & (B['vid'] < 1000000))[0]
rc, v = verify('T0_unchanged', lambda d: None); rec('T0_real_step_result', 'PASS, exit 0', rc == 0 and v['verdict'] == 'PASS')
def m1(d): i = outv[0]; d['V'][i] = d['V'][i] + np.float32(1e-3)
rc, v = verify('T1_outside_vertex_moved', m1); rec('T1_move_one_outside_source_vertex_1e-3cm', 'P3 FAIL, exit 3', rc == 3 and 'P3_outside_vertices_bit_exact' in v['failed'])
def m2(d):
    far = np.where((g[B['F']] > 30).all(1))[0][:50]; d['F'] = np.delete(d['F'], far, 0); d['fgrp'] = np.delete(d['fgrp'], far)
rc, v = verify('T2_outside_faces_deleted', m2); rec('T2_delete_50_far_outside_faces', 'P1 FAIL (and new open boundary), exit 3', rc == 3 and 'P1_outside_faces_preserved' in v['failed'])
def m3(d):
    nf = np.where(d['fgrp'] == 3)[0][:1]; d['F'] = np.delete(d['F'], nf, 0); d['fgrp'] = np.delete(d['fgrp'], nf)
rc, v = verify('T3_hole_in_patch', m3); rec('T3_delete_one_inferred_face', 'T1 FAIL (new open boundary), exit 3', rc == 3 and 'T1_topology' in v['failed'])
def m4(d):
    i = newv[len(newv) // 2]; nb = d['F'][(d['F'] == i).any(1)]; c = d['V'][np.unique(nb)].mean(0)
    nrm = np.cross(d['V'][nb[0][1]] - d['V'][nb[0][0]], d['V'][nb[0][2]] - d['V'][nb[0][0]]); nrm /= np.linalg.norm(nrm)
    d['V'][i] = (d['V'][i] - 4.0 * nrm).astype(np.float32)
rc, v = verify('T4_spike_inward', m4); rec('T4_push_inferred_vertex_4cm_through_the_surface', 'T2 and/or Q1 FAIL, exit 3', rc == 3 and ('T2_self_intersection' in v['failed'] or 'Q1_step_face_quality' in v['failed']), failed=v['failed'])
def m5(d):
    f = np.where(d['fgrp'] == 3)[0][100]; a_, b_, c_ = d['F'][f]; d['V'][c_] = (0.5 * (d['V'][a_].astype(float) + d['V'][b_].astype(float)) + 0.001).astype(np.float32)
rc, v = verify('T5_sliver', m5); rec('T5_collapse_an_inferred_face_to_a_sliver', 'Q1 FAIL, exit 3', rc == 3 and 'Q1_step_face_quality' in v['failed'], failed=v['failed'])
def m6(d): d['fgrp'][np.where(d['fgrp'] == 3)[0][:10]] = 0
rc, v = verify('T6_unlabelled', m6); rec('T6_inferred_faces_unlabelled', 'L1 FAIL, exit 3', rc == 3 and 'L1_inferred_labels' in v['failed'])
def m7(d): j = newv[0]; d['V'][j] = np.array([60, 60, 200], np.float32)
rc, v = verify('T7_new_vertex_outside', m7); rec('T7_inferred_vertex_far_outside_region', 'P2 FAIL, exit 3', rc == 3 and 'P2_new_vertices_inside_region' in v['failed'], failed=v['failed'])
json.dump(dict(tests=T, passed=sum(t['as_expected'] for t in T), total=len(T)), open(a.out, 'w'), indent=1)
print('%d / %d as expected' % (sum(t['as_expected'] for t in T), len(T)))
