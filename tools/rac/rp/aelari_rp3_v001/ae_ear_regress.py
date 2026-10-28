# ae_ear_regress.py OUT.json : order 0f6aba8 §13 -- AE-E2 ear-branch regression on the corrected heads (AEL1-R1 / AELF190-R1) against the AE-E2
# realizations on the original heads (AEL1 / AELF190, order fd71f15): parameters identical, face list identical to frozen Fenn v002, technical gates
# (T-4, aspect, self-intersection, integrity, root valence / crease, transition, clearance, outside-branch identity), measures, 8-pose deformation.
import sys, json, numpy as np
OUT = sys.argv[1]; O = '/tmp/claude-0/rt/ae/ear'; N = '/tmp/claude-0/rt/ae/r1/ear'; jl = lambda p: json.load(open(p))
Qf = np.asarray(np.load('/tmp/claude-0/rt/fn/final/ear/build/FNL4-CF2_E2_branch.npz')['Q'])
MK = ('length_lobe_to_tip_cm', 'auricle_height_cm', 'max_width_cm', 'auricle_body_angle_deg', 'total_lateral_extent_from_root_plane_cm', 'side_view_upper_extension_deg', 'sweep_max_axis_deviation_cm', 'tip_in_plane_angle_deg_at_1cm')
def rec(W, h):
    k = '%s_AE-E2' % h; a = jl('%s/audit/%s_audit.json' % (W, k)); m = jl('%s/meas/%s_measure.json' % (W, k))['sides']['l']; d = jl('%s/deform/%s_deform.json' % (W, k)); b = jl('%s/build/%s_branch.json' % (W, k))
    z = np.load('%s/build/%s_branch.npz' % (W, k)); g = jl('%s/build/%s_deform_guard_log.json' % (W, k))
    return dict(head=h, params=b['params'], HH_cm=b['HH_cm'], head_scale=b['head_scale'], verts=a['verts'], faces=a['faces'], face_list_equals_frozen_fenn=bool(np.array_equal(np.asarray(z['Q']), Qf)),
                T4=a['T4']['angle_violations'], branch_faces=a['T4']['branch_faces'], aspect_max=a['T4']['aspect_max'], aspect_gt10=a['T4']['aspect_gt10'], min_angle=a['T4']['min_angle'],
                self_intersection_branch=a['self_intersection_pairs_touching_branch'], integrity=dict(boundary=a['boundary_edges'], nonmanifold=a['nonmanifold_edges'], components=a['components'], degenerate=a['degenerate_faces_branch'], outward=a['normals_outward']),
                outside_identical=a['outside_branch_byte_identical'], root_valence_ok=all(v.get('4', 0) == 52 for v in a['root_valence'].values()), root_crease_max_deg=max(v['max_deg'] for v in a['root_dihedral'].values()),
                transition_max_cm=a['transition_ring']['displacement_max_cm'], clearance_min_cm=a['ear_to_head_clearance']['min_cm'], measure={x: m[x] for x in MK},
                measure_over_HH={x: round(m[x] / b['HH_cm'], 5) for x in MK if x.endswith('_cm')}, deform_all_clean=all(v['new_selfx_pairs_touching_branch'] == 0 and v['flipped_branch_faces'] == 0 and v['root_band_inverted'] == 0 for v in d['poses'].values()),
                deform_poses=len(d['poses']), guard_iterations=len(g))
R = dict(order='0f6aba8', note='AE-E2 parameters, topology and root unchanged; regression on the corrected body sources', pairs={})
for c, (ho, hn) in dict(c1=('AEL1', 'AEL1-R1'), c2=('AELF190', 'AELF190-R1')).items():
    a, b = rec(O, ho), rec(N, hn)
    R['pairs'][c] = dict(original=a, corrected=b, params_identical=a['params'] == b['params'], measure_delta={x: round(b['measure'][x] - a['measure'][x], 4) for x in MK},
                         measure_over_HH_delta_pct={x: round(100 * (b['measure_over_HH'][x] / a['measure_over_HH'][x] - 1), 2) for x in a['measure_over_HH']})
    print(c, 'params identical', R['pairs'][c]['params_identical'], '| T4 %d -> %d  asp %.2f -> %.2f  >10 %d  SI %d -> %d  face=Fenn %s  outside %s  rootval %s  crease %.1f -> %.1f  tr %.3f  clr %.2f -> %.2f  deform %s/%s' % (
        a['T4'], b['T4'], a['aspect_max'], b['aspect_max'], b['aspect_gt10'], a['self_intersection_branch'], b['self_intersection_branch'], b['face_list_equals_frozen_fenn'], b['outside_identical'], b['root_valence_ok'],
        a['root_crease_max_deg'], b['root_crease_max_deg'], b['transition_max_cm'], a['clearance_min_cm'], b['clearance_min_cm'], a['deform_all_clean'], b['deform_all_clean']), b['integrity'])
    print('   measure delta', R['pairs'][c]['measure_delta'], 'HH', a['HH_cm'], b['HH_cm'])
json.dump(R, open(OUT, 'w'), indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
