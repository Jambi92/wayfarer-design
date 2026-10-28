# ear_compare_v002.py V001_WORK V002_WORK EVIDENCE_DIR : order 0d9c70b §10 / §12 / §13 -- v001 E2 vs v002 E2 comparison records:
#   FENN_EAR_v001_v002_zone_report.json   T-4 / aspect per zone (identical zone definitions, ear_zones.py run once per topology version)
#   FENN_EAR_v001_v002_comparison.json    E2 identity measures, density, root integration, deformation, counts
import sys, os, json, subprocess, numpy as np
W1, W2, EV = sys.argv[1:4]; T = os.path.dirname(os.path.abspath(__file__)); HEADS = ('FNL4-CF2', 'FNF181-CF2'); KEYS = ['%s_E2' % h for h in HEADS]
zr = {}
for ver, W in (('v001', W1), ('v002', W2)):
    out = os.path.join(EV, '_zones_%s.json' % ver); env = dict(os.environ, EAR_TOPO=ver)
    subprocess.run(['python3', os.path.join(T, 'ear_zones.py'), W, out] + KEYS, env=env, check=True, stdout=subprocess.DEVNULL)
    d = json.load(open(out)); os.remove(out); zr[ver] = {k.replace('_E2', ''): d[k] for k in KEYS}
json.dump(zr, open(os.path.join(EV, 'FENN_EAR_v001_v002_zone_report.json'), 'w'), indent=1)
jl = lambda p: json.load(open(p))
MKEYS = ('length_lobe_to_tip_cm', 'auricle_height_cm', 'max_width_cm', 'auricle_body_angle_deg', 'total_lateral_extent_from_root_plane_cm', 'side_view_upper_extension_deg',
         'sweep_max_axis_deviation_cm', 'tip_in_plane_angle_deg_at_1cm')
C = dict(order='0d9c70b', note='v001 = order bdcd6a6 E2 (final run); v002 = this order, final R3 configuration; same CF2 heads, same E2 parameter set', heads={})
for h in HEADS:
    e = {}
    for ver, W in (('v001', W1), ('v002', W2)):
        a = jl('%s/audit/%s_E2_audit.json' % (W, h)); m = jl('%s/meas/%s_E2_measure.json' % (W, h))['sides']['l']; dfm = jl('%s/deform/%s_E2_deform.json' % (W, h)); b = jl('%s/build/%s_E2_branch.json' % (W, h))
        Z = zr[ver][h]
        e[ver] = dict(verts=a['verts'], faces=a['faces'], patch_verts_per_side=b['patch_verts'], patch_faces_per_side=b['patch_faces'], branch_faces=a['T4']['branch_faces'],
                      T4_angle_violations=a['T4']['angle_violations'], T4_rate=a['T4']['angle_violations'] / a['T4']['branch_faces'], T4_by_part=a['T4']['angle_violations_by_part'],
                      aspect_gt4=a['T4']['aspect_gt4'], aspect_gt6=a['T4']['aspect_gt6'], aspect_gt10=a['T4']['aspect_gt10'], aspect_max=a['T4']['aspect_max'], union=a['T4']['union_violations'],
                      min_angle=a['T4']['min_angle'], max_angle=a['T4']['max_angle'], zones=Z['groups'], poles=a['poles_branch_total'],
                      density=a['density'], self_intersection_branch=a['self_intersection_pairs_touching_branch'], self_intersection_total=a['self_intersection_pairs_total'],
                      self_intersection_v005_baseline=a['self_intersection_pairs_cf2_family_v005'], outside_identical=a['outside_branch_byte_identical'],
                      root_valence=a['root_valence'], root_dihedral=a['root_dihedral'], transition=a['transition_ring'], root_deviation=a['root_deviation'], clearance=a['ear_to_head_clearance'],
                      measure={k: m[k] for k in MKEYS}, thickness_median_cm=m['thickness_cm']['median'], thickness_min_cm=m['thickness_cm']['min'],
                      deform={p: dict(new_selfx=v['new_selfx_pairs_touching_branch'], flipped=v['flipped_branch_faces'], root_inverted=v['root_band_inverted'],
                                      root_strain_pct=v['root_loop_edge_strain_pct'], v005_root_strain_pct=v['v005_root_loop_edge_strain_pct'], clearance_cm=v['ear_to_nonhead_clearance_cm'])
                              for p, v in dfm['poses'].items()})
    e['delta_measure'] = {k: e['v002']['measure'][k] - e['v001']['measure'][k] for k in MKEYS}
    e['delta_measure']['thickness_median_cm'] = e['v002']['thickness_median_cm'] - e['v001']['thickness_median_cm']
    C['heads'][h] = e
json.dump(C, open(os.path.join(EV, 'FENN_EAR_v001_v002_comparison.json'), 'w'), indent=1, default=float)
for h in HEADS:
    e = C['heads'][h]; print(h, 'T4 %d -> %d' % (e['v001']['T4_angle_violations'], e['v002']['T4_angle_violations']), {k: round(v, 3) for k, v in e['delta_measure'].items()})
