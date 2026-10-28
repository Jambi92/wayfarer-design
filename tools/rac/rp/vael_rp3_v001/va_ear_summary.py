# va_ear_summary.py WORK EVIDIR : Vael ear-prototype order records -- topology reuse (face list vs frozen Fenn E2 / frozen Aelari AE-E2), per-realization
# technical gates (ear_audit / ear_measure / ear_deform / deformation guard), zone T-4 (ear_zones, the Fenn v002 definitions), the twelve VA-E2 readiness
# probes (direction of the intended measure), the three-elf visible-ear firewall (Vael VA-E1/E2/E3 vs frozen Fenn E2 vs frozen Aelari AE-E2, per
# configuration, head-height / length normalised), and the hidden-ear regression (everything outside the ear branch vs the accepted VF2 family body).
import sys, os, json, glob, hashlib, subprocess, numpy as np
W, EV = sys.argv[1:3]; jl = lambda p: json.load(open(p)); os.makedirs(EV, exist_ok=True)
T = '/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001'; CF = os.environ.get('VA_CF', '/tmp/claude-0/rt/vf/prod')
HEADS = {'c1': 'VAL4-R1-VD2-VF2', 'c2': 'VALF178-R1-VD2-VF2'}; CANDS = ['VA-E1', 'VA-E2', 'VA-E3']
FROZEN = {'Fenn E2': {'c1': ('/tmp/claude-0/rt/fn/final/ear', 'FNL4-CF2_E2'), 'c2': ('/tmp/claude-0/rt/fn/final/ear', 'FNF181-CF2_E2')},
          'Aelari AE-E2': {'c1': ('/tmp/claude-0/rt/ae/final/ear', 'AEL1-R1_AE-E2'), 'c2': ('/tmp/claude-0/rt/ae/final/ear', 'AELF190-R1_AE-E2')}}
keys = ['%s_%s' % (h, c) for h in HEADS.values() for c in CANDS]
out = os.path.join(EV, '_zones.json'); subprocess.run(['python3', T + '/ear_zones.py', W, out] + keys, env=dict(os.environ, EAR_TOPO='v002'), check=True, stdout=subprocess.DEVNULL); ZR = jl(out); os.remove(out)
R = dict(order='chatgpt-rac-rp3-vael-ear-prototype-order', topology_reuse={}, realizations={}, probes={}, firewall={}, hidden_ear_regression={})
Qf = np.asarray(np.load('/tmp/claude-0/rt/fn/final/ear/build/FNL4-CF2_E2_branch.npz')['Q']); Qa = np.asarray(np.load('/tmp/claude-0/rt/ae/final/ear/build/AEL1-R1_AE-E2_branch.npz')['Q'])
def stand(npz, rec):                                         # lateral stand-off of the auricle (front / back / rim sheet) from the root plane, both sides
    sys.path.insert(0, T); os.environ['EAR_TOPO'] = 'v002'; import ear_branch_lib as E
    Lo = E.canonical_layout(); ns = len(Lo['st']); ear = np.isin(Lo['part'][:ns], ['front', 'back', 'rim']); z = np.load(npz); o = []
    for sd in ('l', 'r'):
        f0 = np.nonzero(z['side'] == sd)[0][0]; X = z['V'][f0:f0 + ns]; fr = rec['sides'][sd]['frame']; lat = (X[ear] - np.array(fr['O'])) @ np.array(fr['n']); o.append((lat.mean(), lat.max()))
    return np.mean(o, 0)
def read_meas(d, k):
    m = jl('%s/meas/%s_measure.json' % (d, k)); s = m['sides']; HH = m['head_HH_cm']; b = jl('%s/build/%s_branch.json' % (d, k)); mean_, max_ = stand('%s/build/%s_branch.npz' % (d, k), b)
    av = lambda x: float(np.mean([s[q][x] for q in ('l', 'r')])); L = av('length_lobe_to_tip_cm')
    return dict(HH_cm=HH, length_cm=L, length_over_HH=L / HH, body_angle_deg=av('auricle_body_angle_deg'), standoff_max_over_HH=max_ / HH, standoff_mean_over_HH=mean_ / HH,
                lateral_extent_over_length=av('total_lateral_extent_from_root_plane_cm') / L, tip_above_root_over_HH=av('tip_above_root_cm') / HH, tip_above_root_over_length=av('tip_above_root_cm') / L,
                max_width_over_length=av('max_width_cm') / L, max_width_over_HH=av('max_width_cm') / HH, side_view_chord_deg=av('side_view_chord_lobe_to_tip_deg'),
                upper_extension_axis_deg=av('side_view_upper_extension_deg'), tip_behind_root_over_length=av('tip_back_of_root_cm') / L, sweep_over_length=av('sweep_max_axis_deviation_cm') / L,
                tip_angle_deg=av('tip_in_plane_angle_deg_at_1cm'), thickness_median_cm=float(np.mean([s[q]['thickness_cm']['median'] for q in ('l', 'r')])),
                thickness_p05_cm=float(np.mean([s[q]['thickness_cm']['p05'] for q in ('l', 'r')])), upper_thickness_median_cm=float(np.mean([s[q]['thickness_cm']['upper_extension_median'] for q in ('l', 'r')])))
for k in keys:
    z = np.load('%s/build/%s_branch.npz' % (W, k)); a = jl('%s/audit/%s_audit.json' % (W, k)); d = jl('%s/deform/%s_deform.json' % (W, k)); b = jl('%s/build/%s_branch.json' % (W, k))
    gp = '%s/build/%s_deform_guard_log.json' % (W, k); g = jl(gp) if os.path.exists(gp) else None; Q = np.asarray(z['Q'])
    R['realizations'][k] = dict(verts=a['verts'], faces=a['faces'], face_list_equals_frozen_fenn_E2=bool(np.array_equal(Q, Qf)), face_list_equals_frozen_aelari_AE_E2=bool(np.array_equal(Q, Qa)),
        T4=a['T4']['angle_violations'], branch_faces=a['T4']['branch_faces'], T4_rate=round(a['T4']['angle_violations'] / a['T4']['branch_faces'], 4), T4_by_part=a['T4']['angle_violations_by_part'],
        aspect_max=a['T4']['aspect_max'], aspect_gt10=a['T4']['aspect_gt10'], min_angle=a['T4']['min_angle'], zones={g_: (v['angle_viol'], v['faces']) for g_, v in ZR[k]['groups'].items()},
        density=a['density'], self_intersection_branch=a['self_intersection_pairs_touching_branch'], self_intersection_total=a['self_intersection_pairs_total'],
        self_intersection_family_baseline=a['self_intersection_pairs_cf2_family_v005'], outside_identical=a['outside_branch_byte_identical'], root_valence=a['root_valence'],
        root_dihedral=a['root_dihedral'], transition=a['transition_ring'], root_deviation=a['root_deviation'], clearance=a['ear_to_head_clearance'],
        integrity=dict(boundary=a['boundary_edges'], nonmanifold=a['nonmanifold_edges'], components=a['components'], degenerate=a['degenerate_faces_branch'], outward=a['normals_outward'], all_quads=bool(Q.shape[1] == 4)),
        measure=read_meas(W, k), HH_cm=b['HH_cm'], head_scale=b['head_scale'], params=b['params'],
        deform={p: [v['new_selfx_pairs_touching_branch'], v['flipped_branch_faces'], v['root_band_inverted']] for p, v in d['poses'].items()}, guard=g)
R['topology_reuse'] = dict(template='frozen Fenn ear branch topology v002 -- ENGINEERING connectivity only (52-vertex root interface, cuff, tapered-leaf block layout, guard)',
    cuff_canon='FENN_EAR_BRANCH_CUFF_CANON_v002.json (read-only)', sheet_layout='Fenn v002 canonical layout (connectivity and (s, t) parameterisation) unchanged; no Fenn vertex geometry carried',
    geometry='wholly Vael: ear_branch_lib.W1V / CAND VA-E1..E3 (order targets; W1e VA-elven relief), Vael VF2 + VC2 heads',
    engineering_setting='EAR_UNT_MODE=contacts (contacts-only untangling before the unchanged v002 3-D quality pass / aspect repair)',
    all_face_lists_equal_frozen_fenn=all(r['face_list_equals_frozen_fenn_E2'] for r in R['realizations'].values()),
    all_face_lists_equal_frozen_aelari=all(r['face_list_equals_frozen_aelari_AE_E2'] for r in R['realizations'].values()),
    face_topology_sha256=hashlib.sha256(Qf.astype(np.int32).tobytes()).hexdigest(), verts=int(len(np.load('%s/build/%s_branch.npz' % (W, keys[0]))['V'])), faces=int(len(Qf)))
# probes (VA-E2, configuration 1)
base = R['realizations']['%s_VA-E2' % HEADS['c1']]['measure']
EXP = {'proj': 'body_angle_deg', 'tilt': 'side_view_chord_deg', 'sweep': 'sweep_over_length', 'len': 'length_cm', 'tip': 'tip_angle_deg', 'wb': 'max_width_over_length'}
for dd in sorted(glob.glob('%s/probe/*/' % W)):
    n = dd.rstrip('/').split('/')[-1]; a = jl(dd + 'audit.json'); h = HEADS['c1']
    m = jl(dd + 'measure.json'); s = m['sides']; HH = m['head_HH_cm']; av = lambda x: float(np.mean([s[q][x] for q in ('l', 'r')])); L = av('length_lobe_to_tip_cm')
    mm = dict(body_angle_deg=av('auricle_body_angle_deg'), side_view_chord_deg=av('side_view_chord_lobe_to_tip_deg'), sweep_over_length=av('sweep_max_axis_deviation_cm') / L, length_cm=L,
              tip_angle_deg=av('tip_in_plane_angle_deg_at_1cm'), max_width_over_length=av('max_width_cm') / L)
    key = EXP[n.split('_')[0]]; sgn = (-1 if ('_m' in n or 'blunt' in n) else 1) * (-1 if n.startswith('tip') else 1); dv = mm[key] - base[key]
    R['probes'][n] = dict(T4=a['T4']['angle_violations'], aspect_max=a['T4']['aspect_max'], aspect_gt10=a['T4']['aspect_gt10'], min_angle=a['T4']['min_angle'],
        self_intersection_branch=a['self_intersection_pairs_touching_branch'], boundary=a['boundary_edges'], nonmanifold=a['nonmanifold_edges'],
        root_valence_ok=all(v.get('4', 0) == 52 for v in a['root_valence'].values()), face_list_equal=bool(np.array_equal(np.asarray(np.load(glob.glob(dd + '*_branch.npz')[0])['Q']), Qf)),
        measure=key, value=mm[key], base=base[key], moves_intended=bool(np.sign(dv) == sgn and abs(dv) > 1e-3))
# three-elf visible-ear firewall
for c in HEADS:
    F = {nm: read_meas(*FROZEN[nm][c]) for nm in FROZEN}; row = {}
    for k in CANDS:
        v = R['realizations']['%s_%s' % (HEADS[c], k)]['measure']; fn, ae = F['Fenn E2'], F['Aelari AE-E2']
        chk = {'projection (body angle): Fenn > Vael > Aelari': fn['body_angle_deg'] > v['body_angle_deg'] > ae['body_angle_deg'],
               'upward extension (tip height / HH): Aelari > Vael': ae['tip_above_root_over_HH'] > v['tip_above_root_over_HH'],
               'upward extension: Vael within 25 % of Fenn (approximately Fenn)': abs(v['tip_above_root_over_HH'] / fn['tip_above_root_over_HH'] - 1) < 0.25,
               'base width / width:length: Vael broadest': v['max_width_over_length'] > max(fn['max_width_over_length'], ae['max_width_over_length']) and v['max_width_over_HH'] > max(fn['max_width_over_HH'], ae['max_width_over_HH']),
               'relative length: Vael shorter than Aelari': v['length_over_HH'] < ae['length_over_HH'],
               'orientation: Vael more backward than both (side-view chord)': v['side_view_chord_deg'] > max(fn['side_view_chord_deg'], ae['side_view_chord_deg']),
               'orientation: Vael more backward than both (upper-extension axis)': v['upper_extension_axis_deg'] > max(fn['upper_extension_axis_deg'], ae['upper_extension_axis_deg']),
               'shorter / blunter taper than Aelari (tip angle)': v['tip_angle_deg'] > ae['tip_angle_deg'],
               'REPORTED (not a canon rule): tip stand-off from the skull / HH below Fenn': v['standoff_max_over_HH'] < fn['standoff_max_over_HH']}
        row[k] = dict(vael=v, checks=chk)
    R['firewall'][c] = dict(frozen=F, vael=row, note='Fenn = frozen FN_*_REF_RP3_v001 ear (E2), Aelari = frozen AE_*_REF_RP3_v001 ear (AE-E2); same configuration; head-height / length normalised (matched presentation)')
# hidden-ear regression: everything outside the branch (and its one bounded transition ring) equals the accepted VF2 family body
for k in keys:
    h = k.rsplit('_', 1)[0]; z = np.load('%s/build/%s_branch.npz' % (W, k)); fz = np.load('%s/fam/%s_fam.npz' % (CF, h)); V0 = fz['V'].astype(float)
    m5 = np.asarray(z['v005_to_branch']); kept = np.nonzero(m5 >= 0)[0]; part = z['part'][m5[kept]]; Vb = z['V'][m5[kept]].astype(float)
    out_ = part == 'v005'; tr_ = part == 'transition'; d = np.linalg.norm(Vb[out_] - V0[kept[out_]], axis=1); dt = np.linalg.norm(Vb[tr_] - V0[kept[tr_]], axis=1)
    a = jl('%s/audit/%s_audit.json' % (W, k))
    R['hidden_ear_regression'][k] = dict(v005_vertices_outside_branch=int(out_.sum()), max_displacement_outside_branch_cm=float(d.max()), outside_branch_byte_identical=bool((Vb[out_] == V0[kept[out_]]).all()),
        audit_outside_branch_byte_identical=a['outside_branch_byte_identical'], transition_ring_vertices=int(tr_.sum()), transition_ring_max_cm=float(dt.max()),
        removed_v005_ear_zone_vertices=int((m5 < 0).sum()))
json.dump(R, open(os.path.join(EV, 'VAEL_EAR_prototype_summary.json'), 'w'), indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
for k, r in R['realizations'].items():
    print(k, 'T4 %d (%.1f%%) asp %.2f >10 %d minang %.1f SI %d faceFN %s faceAE %s clr %.2f tr %.3f deform0 %s guard %s' % (r['T4'], 100 * r['T4_rate'], r['aspect_max'], r['aspect_gt10'], r['min_angle'],
          r['self_intersection_branch'], r['face_list_equals_frozen_fenn_E2'], r['face_list_equals_frozen_aelari_AE_E2'], r['clearance']['min_cm'], r['transition']['displacement_max_cm'],
          all(sum(v) == 0 for v in r['deform'].values()), [x['iteration'] for x in r['guard']] if r['guard'] else None))
for n, p in R['probes'].items(): print(' probe', n, p['T4'], round(p['aspect_max'], 2), p['self_intersection_branch'], p['moves_intended'], round(p['value'], 3), round(p['base'], 3))
for c, f in R['firewall'].items():
    for k, v in f['vael'].items(): print(c, k, {kk: vv for kk, vv in v['checks'].items()})
for k, v in R['hidden_ear_regression'].items(): print(k, v)
