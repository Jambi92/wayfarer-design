# hv_ear_prodtri_collect.py PRODTRI_DIR SNAP_DIR EVIDIR : collect the Halvren ear production-gate evidence
#   records/<mesh>_prodtri.json (full per-mesh audit), baked/<mesh>_TRI-HV1.npz (the baked diagonal choice per quad + triangle list hash, so the same
#   surface is reproduced downstream), HV_ear_production_gate_summary.json, post_audit_hashes.json (snapshot re-hashed after every test)
import sys, os, json, glob, hashlib, shutil, numpy as np
PT, SN, EV = sys.argv[1:4]; os.makedirs(EV + '/records', exist_ok=True); os.makedirs(EV + '/baked', exist_ok=True)
S = {}
for p in sorted(glob.glob(PT + '/*_prodtri.json')):
    lab = os.path.basename(p).replace('_prodtri.json', ''); r = json.load(open(p)); shutil.copy(p, '%s/records/%s_prodtri.json' % (EV, lab))
    z = np.load('%s/%s_tri.npz' % (PT, lab), allow_pickle=True)
    np.savez_compressed('%s/baked/%s_TRI-HV1.npz' % (EV, lab), diagonal_choice=z['choice'].astype(np.int8), flagged_quads=z['flagged'].astype(np.int32),
                        triangles_sha256=np.array(r['triangulation']['triangles_sha256']), note=np.array('quad (a,b,c,d) -> 0: (a,b,c)+(a,c,d), 1: (a,b,d)+(b,c,d); quad order = snapshot Q'))
    P = r.get('poses', {}); L = r['lod']; f = r['flagged']; iv = r['intersection_validation']; ex = r['export_fbx']; nt = r['normals_tangents']
    S[lab] = dict(snapshot_V_float32_sha256=r['snapshot_V_float32_sha256'], triangles_sha256=r['triangulation']['triangles_sha256'], branch_quads=r['triangulation']['branch_quads'],
                  branch_tri_min_angle=r['triangulation']['branch_tri_min_angle'], branch_tri_max_aspect=r['triangulation']['branch_tri_max_aspect'],
                  order_invariance_mismatches=sum(v for k, v in r['order_invariance_mismatched_quads'].items() if k != 'note'),
                  rebuild_triangles_identical=r.get('rebuild', {}).get('triangles_identical'), rebuild_max_dV=r.get('rebuild', {}).get('max_abs_dV_cm'),
                  flagged=f['count'], flagged_folded=f['folded'], flagged_by_region=f['by_region'], defect_flags=f['defect_flags'], fold_chosen_max=f['fold_chosen_max'],
                  deviation_max_cm=f['deviation_max_cm'], crossings_fixed_ac_total=sum(iv['fixed_split_ac_crossings'].values()), crossings_steps1_4_total=sum(iv['rule_steps1_4_crossings'].values()),
                  crossings_final_total=sum(iv['final_crossings'].values()), step5_flips=iv['flipped_quads'], step5_flip_regions=iv.get('flipped_regions'),
                  rest_contacts_baked=r.get('rest_contacts_touching_branch_on_baked_triangles'),
                  poses_contacts=sum(v['new_contacts'] for v in P.values()), poses_triangle_inversions=sum(v['triangle_inversions'] for v in P.values()),
                  poses_vertex_normal_flips=sum(v['vertex_normal_flips'] for v in P.values()), poses_root_inversions=sum(v['root_band_triangle_inversions'] for v in P.values()),
                  poses_baked_diagonal_changes=sum(v['baked_diagonal_changes'] for v in P.values()), poses_rule_reevaluation_changes_max=max([v['rule_reevaluated_at_pose_would_change_diagonal_branch'] for v in P.values()] or [0]),
                  poses_flagged_max_normal_change_deg=max([v['flagged_max_local_normal_change_deg'] for v in P.values()] or [0]),
                  poses_folded_across_baked_rest_vs_max=[max([v['folded_across_baked_diagonal_rest'] for v in P.values()] or [0]), max([v['folded_across_baked_diagonal_pose'] for v in P.values()] or [0])],
                  worst_two_poses=r.get('worst_two_poses'),
                  normals_blender_vs_numpy_deg=nt['blender_vs_numpy_vertex_normal_max_deg_branch'], quad_vs_tri_normal_max_deg=nt['quad_vs_baked_triangle_vertex_normal_max_deg_branch'],
                  tangents_degenerate=nt['degenerate_or_nan_tangents_branch'], tangent_spread_max_deg=nt['tangent_spread_per_vertex_max_deg_branch'], bitangent_sign_mixed=nt['bitangent_sign_mixed_vertices_branch'],
                  fbx_triangles_identical=ex['triangles_identical'], fbx_max_dV_cm=ex['max_abs_dV_cm'], fbx_normal_max_deg=ex['normal_max_deg_branch'], fbx_tangent_max_deg=ex['tangent_recomputed_max_deg_branch'],
                  fbx_bitangent_sign_identical=ex['bitangent_sign_identical'], fbx_ear_boundary_edges=ex['ear_region_boundary_or_nonmanifold_edges'],
                  importer_retriangulation=r['importer_retriangulation_if_exported_as_quads'], mirroring_mismatches=r['mirroring']['diagonal_choice_mismatched'], mirroring_pairs=r['mirroring']['sheet_quad_pairs'],
                  lod={m: {k: {q: L[m][k][q] for q in ('ear_region_nonmanifold_edges', 'ear_region_zero_area_triangles', 'ear_region_self_intersection_pairs', 'ear_max_drift_source_to_lod_cm',
                                                     'root_region_max_drift_cm', 'flagged_max_drift_cm', 'flagged_regions_lod_normal_over_60deg')} for k in ('0.5', '0.25')} for m in ('protected', 'unconstrained')})
json.dump(S, open(EV + '/HV_ear_production_gate_summary.json', 'w'), indent=1)
pre = json.load(open(EV + '/pre_audit_hashes.json')); post = {}
for k, v in pre['meshes'].items():
    p = '%s/%s_branch.npz' % (SN, k); z = np.load(p)
    post[k] = dict(npz_sha256=hashlib.sha256(open(p, 'rb').read()).hexdigest(), V_float32_sha256=hashlib.sha256(z['V'].astype(np.float32).tobytes()).hexdigest(),
                   Q_sha256=hashlib.sha256(np.ascontiguousarray(z['Q']).astype(np.int64).tobytes()).hexdigest())
    post[k]['unchanged'] = all(post[k][q] == v[q] for q in ('npz_sha256', 'V_float32_sha256', 'Q_sha256'))
    lab = {'HVC1-HB2HF2-HPB': 'c1', 'HVF178-HB2HF2-HPB': 'c2'}[k.split('_')[0]]; post[k]['baked_triangles_sha256'] = S['%s_%s' % (k.split('_')[1], lab)]['triangles_sha256']
json.dump(dict(note='snapshot re-hashed after all production tests; no vertex or connectivity edit was made (validation only); baked triangles = TRI-HV1 on that snapshot', meshes=post), open(EV + '/post_audit_hashes.json', 'w'), indent=1)
print('COLLECT_DONE', {k: v['unchanged'] for k, v in post.items()})
