# ae_ear_summary.py WORK EVIDIR : order fd71f15 Part C records -- Aelari ear-branch prototype: topology reuse record (face list vs frozen Fenn), per
# realization technical gates (ear_audit / ear_measure / ear_deform), zone T-4 (ear_zones, identical definitions to the Fenn v002 report), probes
# (direction of the intended measure), and the Fenn E2 vs Aelari AE-E2 visible-ear firewall measures (head-height normalised).
import sys, os, json, glob, hashlib, subprocess, numpy as np
W, EV = sys.argv[1:3]; EW = W + '/ear'; jl = lambda p: json.load(open(p)); sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest(); os.makedirs(EV, exist_ok=True)
T = '/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001'; HEADS = {'c1': 'AEL1', 'c2': 'AELF190'}; CANDS = ['AE-E1', 'AE-E2', 'AE-E3']
FNP = '/tmp/claude-0/rt/fn/final/ear/build/FNL4-CF2_E2_branch.npz'; FNM = '/tmp/claude-0/rt/fn/final/ear/meas/FNL4-CF2_E2_measure.json'
keys = ['%s_%s' % (h, c) for h in HEADS.values() for c in CANDS]
out = os.path.join(EV, '_zones.json'); subprocess.run(['python3', T + '/ear_zones.py', EW, out] + keys, env=dict(os.environ, EAR_TOPO='v002'), check=True, stdout=subprocess.DEVNULL); ZR = jl(out); os.remove(out)
R = dict(order='fd71f15', topology_reuse={}, realizations={}, probes={}, firewall={})
zf = np.load(FNP); Qf = np.asarray(zf['Q'])
for k in keys:
    z = np.load('%s/build/%s_branch.npz' % (EW, k)); a = jl('%s/audit/%s_audit.json' % (EW, k)); m = jl('%s/meas/%s_measure.json' % (EW, k))['sides']['l']; d = jl('%s/deform/%s_deform.json' % (EW, k))
    b = jl('%s/build/%s_branch.json' % (EW, k)); g = jl('%s/build/%s_deform_guard_log.json' % (EW, k)) if os.path.exists('%s/build/%s_deform_guard_log.json' % (EW, k)) else None
    R['realizations'][k] = dict(verts=a['verts'], faces=a['faces'], face_list_equals_frozen_fenn=bool(np.array_equal(np.asarray(z['Q']), Qf)), T4=a['T4']['angle_violations'], branch_faces=a['T4']['branch_faces'],
                                T4_rate=round(a['T4']['angle_violations'] / a['T4']['branch_faces'], 4), T4_by_part=a['T4']['angle_violations_by_part'], aspect_max=a['T4']['aspect_max'], aspect_gt10=a['T4']['aspect_gt10'],
                                min_angle=a['T4']['min_angle'], zones={g_: (v['angle_viol'], v['faces']) for g_, v in ZR[k]['groups'].items()}, density=a['density'], self_intersection_branch=a['self_intersection_pairs_touching_branch'],
                                self_intersection_total=a['self_intersection_pairs_total'], self_intersection_family_baseline=a['self_intersection_pairs_cf2_family_v005'], outside_identical=a['outside_branch_byte_identical'],
                                root_valence=a['root_valence'], root_dihedral=a['root_dihedral'], transition=a['transition_ring'], root_deviation=a['root_deviation'], clearance=a['ear_to_head_clearance'],
                                integrity=dict(boundary=a['boundary_edges'], nonmanifold=a['nonmanifold_edges'], components=a['components'], degenerate=a['degenerate_faces_branch'], outward=a['normals_outward']),
                                measure={x: m[x] for x in ('length_lobe_to_tip_cm', 'auricle_height_cm', 'max_width_cm', 'auricle_body_angle_deg', 'total_lateral_extent_from_root_plane_cm', 'side_view_upper_extension_deg', 'sweep_max_axis_deviation_cm', 'tip_in_plane_angle_deg_at_1cm')},
                                thickness_cm=m['thickness_cm'], HH_cm=b['HH_cm'], head_scale=b['head_scale'], params=b['params'],
                                deform={p: [v['new_selfx_pairs_touching_branch'], v['flipped_branch_faces'], v['root_band_inverted']] for p, v in d['poses'].items()}, guard=g)
R['topology_reuse'] = dict(template='Fenn ear branch topology v002 (frozen, 6d2eadc) -- engineering template only', cuff_canon='FENN_EAR_BRANCH_CUFF_CANON_v002.json (read-only)', sheet_layout='Fenn v002 canonical layout (connectivity and (s, t) parameterisation) unchanged',
                           geometry='wholly Aelari: W1e AE-elven parameters (ear_branch_lib.W1A / CAND AE-E1..E3), Aelari heads', all_face_lists_equal_frozen_fenn=all(r['face_list_equals_frozen_fenn'] for r in R['realizations'].values()),
                           face_topology_hash=hashlib.sha256(np.asarray(zf['Q']).astype(np.int32).tobytes()).hexdigest(), tested_alternative='EAR_LAYOUT_METRIC=AE-E2 (same connectivity, sheet positions re-optimised in the Aelari metric): AEL1 AE-E2 T-4 106 vs 117 strict -- not needed, strict reuse kept')
base = jl('%s/meas/AEL1_AE-E2_measure.json' % EW)['sides']['l']
EXP = {'proj': 'auricle_body_angle_deg', 'tilt': 'side_view_upper_extension_deg', 'sweep': 'sweep_max_axis_deviation_cm', 'len': 'length_lobe_to_tip_cm', 'tip': 'tip_in_plane_angle_deg_at_1cm'}
for d in sorted(glob.glob('%s/probe/*/' % EW)):
    n = d.rstrip('/').split('/')[-1]; a = jl(d + 'audit.json'); m = jl(d + 'measure.json')['sides']['l']; key = EXP[n.split('_')[0]]
    sgn = (-1 if ('_m' in n or 'blunt' in n) else 1) * (-1 if n.startswith('tip') else 1); dv = m[key] - base[key]
    R['probes'][n] = dict(T4=a['T4']['angle_violations'], aspect_max=a['T4']['aspect_max'], aspect_gt10=a['T4']['aspect_gt10'], self_intersection_branch=a['self_intersection_pairs_touching_branch'], boundary=a['boundary_edges'],
                          root_valence_ok=all(v.get('4', 0) == 52 for v in a['root_valence'].values()), measure=key, value=m[key], base=base[key], moves_intended=bool(np.sign(dv) == sgn and abs(dv) > 1e-3))
fm = jl(FNM)['sides']['l']; fb = jl('/tmp/claude-0/rt/fn/final/ear/build/FNL4-CF2_E2_branch.json')
for k in ('AEL1_AE-E1', 'AEL1_AE-E2', 'AEL1_AE-E3'):
    a = R['realizations'][k]['measure']; HHa = R['realizations'][k]['HH_cm']; HHf = fb['HH_cm']
    R['firewall'][k] = dict(fenn='FNL4-CF2 E2 (frozen FN_M_REF_RP3_v001)',
                            length_over_HH=[round(a['length_lobe_to_tip_cm'] / HHa, 4), round(fm['length_lobe_to_tip_cm'] / HHf, 4)], width_over_length=[round(a['max_width_cm'] / a['length_lobe_to_tip_cm'], 4), round(fm['max_width_cm'] / fm['length_lobe_to_tip_cm'], 4)],
                            projection_body_angle_deg=[a['auricle_body_angle_deg'], fm['auricle_body_angle_deg']], lateral_extent_over_length=[round(a['total_lateral_extent_from_root_plane_cm'] / a['length_lobe_to_tip_cm'], 4), round(fm['total_lateral_extent_from_root_plane_cm'] / fm['length_lobe_to_tip_cm'], 4)],
                            upper_extension_deg=[a['side_view_upper_extension_deg'], fm['side_view_upper_extension_deg']], sweep_over_length=[round(a['sweep_max_axis_deviation_cm'] / a['length_lobe_to_tip_cm'], 4), round(fm['sweep_max_axis_deviation_cm'] / fm['length_lobe_to_tip_cm'], 4)],
                            tip_angle_deg=[a['tip_in_plane_angle_deg_at_1cm'], fm['tip_in_plane_angle_deg_at_1cm']], note='[Aelari, Fenn]; head-height / length normalised so the comparison is at matched presentation')
json.dump(R, open(os.path.join(EV, 'AELARI_EAR_prototype_summary.json'), 'w'), indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
for k, r in R['realizations'].items(): print(k, 'T4 %d (%.1f%%) asp %.2f >10 %d SI %d face=Fenn %s crease %s tr %.3f clr %.2f deform0 %s' % (r['T4'], 100 * r['T4_rate'], r['aspect_max'], r['aspect_gt10'], r['self_intersection_branch'], r['face_list_equals_frozen_fenn'],
      [round(v['max_deg'], 1) for v in r['root_dihedral'].values()], r['transition']['displacement_max_cm'], r['clearance']['min_cm'], all(sum(v) == 0 for v in r['deform'].values())), r['measure']['length_lobe_to_tip_cm'], r['measure']['auricle_body_angle_deg'])
print({n: (p['T4'], round(p['aspect_max'], 2), p['self_intersection_branch'], p['moves_intended']) for n, p in R['probes'].items()}); print(json.dumps(R['firewall']['AEL1_AE-E2']))
