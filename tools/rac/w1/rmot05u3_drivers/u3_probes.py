# RM-OT-05U3: DISPOSABLE VALIDATOR PROBES for the opt-in U2 adapter. Each probe is a synthetic edit of a COPY of the 05U
# baseline return arrays (no Blender, no scene, no production file). They test the validator only; they are not anatomical
# repairs or candidates and do not substitute for the real desktop mask/brush fixtures required after boundary approval.
# Usage: python3 u3_probes.py --proposal reviews/rac-rmot05u2-proposal --baseline <05U return.npz> --s3 GO-05S-S3.obj --f1 F1_working.obj --work DIR --out SUMMARY.json
import argparse, json, os, shutil, subprocess, sys, hashlib, numpy as np
here = os.path.dirname(os.path.abspath(__file__)); RE = os.path.join(here, 'u3_reintegrate.py'); SV = os.path.join(here, '..', 'rmot05s_drivers', 's_verify.py')
TR = os.path.join(here, '..', 'rmot05t_drivers', 't_reintegrate.py'); S = 'reviews/rac-rmot05s-evidence/'
ap = argparse.ArgumentParser(); [ap.add_argument(k) for k in ('--proposal', '--baseline', '--s3', '--f1', '--work', '--out')]; a = ap.parse_args(); os.makedirs(a.work, exist_ok=True)
B = dict(np.load(a.baseline)); ids0 = B['s3_vid1'] - 1; pos = {int(k): i for i, k in enumerate(ids0)}
def mk(name, fn):
    d = {k: (v.copy() if isinstance(v, np.ndarray) else v) for k, v in B.items()}; fn(d); p = os.path.join(a.work, name + '.npz'); np.savez(p, **d); return p
def move(v, dz=0.02):
    def f(d): d['V'][pos[v], 2] = np.float32(d['V'][pos[v], 2] + dz)
    return f
def drop_face(j):            # remove one protected face (by S3 face index, mapped through the export order)
    def f(d):
        import trimesh
        Fs = np.asarray(trimesh.load(a.s3, process=False).faces); key = tuple(sorted(Fs[j])); Fm = np.sort(ids0[d['F']], 1)
        k = int(np.where((Fm == key).all(1))[0][0]); d['F'] = np.delete(d['F'], k, 0)
    return f
def reverse_face(j):
    def f(d):
        import trimesh
        Fs = np.asarray(trimesh.load(a.s3, process=False).faces); key = tuple(sorted(Fs[j])); Fm = np.sort(ids0[d['F']], 1)
        k = int(np.where((Fm == key).all(1))[0][0]); d['F'][k] = d['F'][k][[0, 2, 1]]
    return f
def swap_ids(x, y):
    def f(d): i, j = pos[x], pos[y]; d['s3_vid1'][i], d['s3_vid1'][j] = d['s3_vid1'][j], d['s3_vid1'][i]
    return f
def dup_id(x, y):
    def f(d): d['s3_vid1'][pos[x]] = y + 1
    return f
def run_u2(name, ret, proposal):
    o = os.path.join(a.work, name); subprocess.run([sys.executable, RE, '--ret', ret, '--proposal', proposal, '--s3', a.s3, '--baseline', a.baseline, '--f1', a.f1, '--out', o], check=True, capture_output=True)
    return o, json.load(open(o + '_u2_reintegrate.json'))
def run_sv(o):
    subprocess.run([sys.executable, SV, '--src', a.f1, '--q05', 'reviews/rac-rmot05q-evidence', '--plan', S + 'plan', '--res', o + '.obj', '--maps', o + '_maps.npz', '--labels', o + '_face_labels.npy',
                    '--nprot', '139772', '--prot_sha', '25ffe5ac83d60e81b1026baf91bf3dbc07d7dc7136a8495f77f5581920328ffd',
                    '--prot_faces_file', os.path.join(a.proposal, 'P05U2_preview.npz') + ':P05U2_src_ordered', '--src_exempt', o + '_src_exempt_f1.npy', '--out', o], check=True, capture_output=True)
    return json.load(open(o + '_verify.json'))
def alt_proposal(name, edit):
    d = os.path.join(a.work, 'proposal_' + name); shutil.rmtree(d, ignore_errors=True); shutil.copytree(a.proposal, d, ignore=shutil.ignore_patterns('views')); edit(d); return d
def add_face(d):
    z = dict(np.load(os.path.join(d, 'proposal_sets.npz'))); z['added_faces'] = np.r_[z['added_faces'], 60000]; np.savez(os.path.join(d, 'proposal_sets.npz'), **z)
def edit_json(d):
    p = os.path.join(d, 'proposal_region.json'); J = json.load(open(p)); J['proposed_added']['faces_sha256'] = '0' * 64; json.dump(J, open(p, 'w'))
def edit_preview(d):
    z = dict(np.load(os.path.join(d, 'P05U2_preview.npz'))); z['P05U2_positions_in_P05S'] = z['P05U2_positions_in_P05S'][1:]; np.savez(os.path.join(d, 'P05U2_preview.npz'), **z)
probes = [('U0_unchanged_baseline', None, 'ACCEPT', 'unchanged 05U baseline'),
          ('U1_allowed_added_source_61581', move(61581), 'ACCEPT', 'authorized added source vertex 61581 +0.02 cm z'),
          ('U1b_allowed_05U_interface_70402', move(70402), 'ACCEPT', 'existing editable interface vertex 70402 +0.02 cm z'),
          ('U2_just_outside_protected_61586', move(61586), 'REJECT', 'protected source vertex 61586 just outside the proposed boundary'),
          ('U3_new_frozen_ring_61771', move(61771), 'REJECT', 'new frozen-ring vertex 61771'),
          ('U4_retained_old_ring_70139', move(70139), 'REJECT', 'retained old frozen-ring vertex 70139'),
          ('U5a_missing_protected_face', drop_face(100000), 'REJECT', 'protected S3 face 100000 removed'),
          ('U5b_reversed_protected_face', reverse_face(100000), 'REJECT', 'protected S3 face 100000 winding reversed'),
          ('U6a_spoof_swap_ids', swap_ids(61586, 61581), 'REJECT', 'ids of protected 61586 and editable 61581 swapped, positions untouched'),
          ('U6b_spoof_duplicate_id', dup_id(61581, 61586), 'REJECT', 'editable vertex claims the id of protected 61586')]
summary = dict(note='Disposable validator probes on copies of the 05U baseline arrays; NOT anatomical repairs, NOT production, NOT a substitute for real desktop fixtures.',
               baseline_sha256=hashlib.sha256(open(a.baseline, 'rb').read()).hexdigest(), probes=[])
for name, fn, expect, desc in probes:
    ret = a.baseline if fn is None else mk(name, fn); o, r = run_u2(name, ret, a.proposal)
    row = dict(probe=name, edit=desc, expected=expect, verdict=r['verdict'], errors=r.get('errors', []))
    row['as_expected'] = (r['verdict'] == 'ACCEPTED_FOR_VERIFICATION_U2') == (expect == 'ACCEPT')
    if r['verdict'] == 'ACCEPTED_FOR_VERIFICATION_U2':
        v = run_sv(o); row['legacy_V1_diagnostic'] = {k: r['legacy_V1_diagnostic'][k] for k in ('original_V1_hash_matches', 'source_vertices_changed', 'P05S_faces_affected', 'all_changed_source_within_authorized_15', 'all_affected_faces_within_authorized_35')}
        row['editable_changes'] = r['editable_changes']; row['s_verify_U2'] = {k: (v[k]['pass_'] if isinstance(v[k], dict) and 'pass_' in v[k] else None) for k in v if k.startswith('V')}
        row['s_verify_U2']['verdict_automated'] = v.get('verdict_automated'); row['V1_U2_detail'] = {k: v['V1_outside_anatomy'][k] for k in v['V1_outside_anatomy'] if k != 'pass_'}
        row['V4_new_faces'] = v['V4_triangle_quality']['new_faces']; row['V5'] = {k: v['V5_seam_continuity'][k] for k in ('stitch_edges', 'frac_le_35')}
    else:
        row['detail'] = {k: r[k] for k in ('identity', 'topology', 'P1_U2_vertices_outside_365') if k in r}
    summary['probes'].append(row); print(name, r['verdict'], 'OK' if row['as_expected'] else 'UNEXPECTED')
for name, ed, desc in (('U7a_altered_added_face_list', add_face, 'one extra face appended to added_faces'), ('U7b_altered_region_json_hash', edit_json, 'faces_sha256 in proposal_region.json altered'),
                       ('U7c_altered_P05U2_preview', edit_preview, 'first position dropped from P05U2 preview')):
    d = alt_proposal(name, ed)
    try: o, r = run_u2(name, a.baseline, d); v_ = r['verdict']; er = r.get('errors', [])
    except subprocess.CalledProcessError as e: v_ = 'REJECTED (adapter aborted)'; er = [e.stderr.decode()[-300:]]
    row = dict(probe=name, edit=desc, expected='REJECT', verdict=v_, errors=er, as_expected=not v_.startswith('ACCEPTED')); summary['probes'].append(row); print(name, v_)
# U0 geometry equality with the committed 05U result (in S3 order) and active production rule unchanged (05T default path)
import trimesh
o0 = os.path.join(a.work, 'U0_unchanged_baseline'); Vu2 = np.asarray(trimesh.load(o0 + '.obj', process=False).vertices)
Fu2 = np.asarray(trimesh.load(o0 + '.obj', process=False).faces); ordr = np.load(o0 + '_maps.npz')['face_order_s3']
r05 = 'reviews/rac-rmot05u-evidence/checks/return/'; import gzip
V05 = np.asarray(trimesh.load(trimesh.util.wrap_as_stream(gzip.open(r05 + 'result.obj.gz').read()), file_type='obj', process=False).vertices)
m05 = ids0; V05s = np.zeros_like(V05); V05s[m05] = V05   # 05U result.obj vertices are in export order; export index -> S3 via rac_s3_vid1 (the 05U s3_vertex map is -1 for its 101 moved vertices)
Fs = np.asarray(trimesh.load(a.s3, process=False).faces)
summary['U0_equality'] = dict(coordinates_identical_to_committed_05U_result_float64=bool(np.array_equal(Vu2, V05s)), topology_identical_to_S3=bool(np.array_equal(Fu2, Fs[ordr])),
                              correspondence_src_vertex_identical_to_S3=bool(np.array_equal(np.load(o0 + '_maps.npz')['src_vertex'], np.load(S + 'repair/S3/GO-05S-S3_maps.npz')['src_vertex'])),
                              expected_metadata_differences='face order (P05U2 prefix) and labels: 35 added faces carry label 6 instead of 0; geometry identical')
hist = {}
for name in ('U0_unchanged_baseline', 'U1_allowed_added_source_61581'):
    ret = a.baseline if name.startswith('U0') else os.path.join(a.work, name + '.npz'); o = os.path.join(a.work, 'hist_' + name)
    subprocess.run([sys.executable, TR, '--ret', ret, '--s3', a.s3, '--s3maps', S + 'repair/S3/GO-05S-S3_maps.npz', '--s3labels', S + 'repair/S3/GO-05S-S3_face_labels.npy', '--out', o], check=True, capture_output=True)
    j = json.load(open(o + '_reintegrate.json')); hist[name] = dict(active_05T_default_verdict=j['verdict'], P1_moved=j['P1_protected_vertices']['missing_or_moved'], result_obj_sha256=j.get('result_obj_sha256'))
hist['note'] = 'Active (default) 05T/05U protection rule is unchanged: it accepts the unchanged 05U baseline and still REJECTS the U1 edit of 61581, which only the opt-in U2 path allows.'
hist['U0_default_result_equals_committed_05U'] = hist['U0_unchanged_baseline']['result_obj_sha256'] == '6046f0135cb250c1ac9f2209c2f2cdbb6fd101ec17b7ab06fd8bdc4ffeb20ab4'
summary['historical_default_path'] = hist; summary['all_as_expected'] = all(p['as_expected'] for p in summary['probes'])
json.dump(summary, open(a.out, 'w'), indent=1); print('all_as_expected', summary['all_as_expected'], json.dumps(summary['U0_equality']), json.dumps(hist))
