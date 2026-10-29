# va_ri_summary.py RI_WORK EVIDIR : Vael VA-E2 root-integration order records -- per alternative (current VA-E2, RI1, RI2, RI3) x configuration:
# integrity / T-4 / aspect / min corner / zones / density / self-intersection / root valence / crease / transition / clearance / deformation / guard;
# the ROOT / CONCHA audit (cuff skin deviation = height of the new skin inside the root above the hidden-ear skull, cuff mound away from the junction,
# junction height above the skin, concha-floor level); outer-silhouette preservation (sheet shape vs current VA-E2 after removing the rigid lateral
# shift); projection / stand-off (auricle-body angle, mean / median free-ear lateral stand-off, tip stand-off; vs frozen Fenn E2 and Aelari AE-E2);
# anatomy relief presence; probes on the selected alternative; hidden-ear regression (outside the branch vs the VF2 family body).
import sys, os, json, glob, hashlib, subprocess, numpy as np
os.environ.setdefault('EAR_TOPO', 'v002')
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001')
import ear_branch_lib as E
import scipy.sparse as sp
from scipy.spatial import cKDTree
W, EV = sys.argv[1:3]; os.makedirs(EV, exist_ok=True); jl = lambda p: json.load(open(p)); T = '/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001'
CF = os.environ.get('VA_CF', '/tmp/claude-0/rt/vf/prod'); SEL = os.environ.get('VA_RI_SEL', 'RI3'); CUR = '/tmp/claude-0/rt/va/ear'
HEADS = {'c1': 'VAL4-R1-VD2-VF2', 'c2': 'VALF178-R1-VD2-VF2'}
ALT = {'current': (CUR, 'VA-E2'), 'RI1': (W + '/RI1', 'VA-E2-RI1'), 'RI2': (W + '/RI2', 'VA-E2-RI2'), 'RI3': (W + '/RI3', 'VA-E2-RI3')}
FROZEN = {'Fenn E2': {'c1': ('/tmp/claude-0/rt/fn/final/ear', 'FNL4-CF2_E2'), 'c2': ('/tmp/claude-0/rt/fn/final/ear', 'FNF181-CF2_E2')},
          'Aelari AE-E2': {'c1': ('/tmp/claude-0/rt/ae/final/ear', 'AEL1-R1_AE-E2'), 'c2': ('/tmp/claude-0/rt/ae/final/ear', 'AELF190-R1_AE-E2')}}
Lo = E.canonical_layout(); st = Lo['st']; ns = len(st); SHEET = np.isin(Lo['part'][:ns], ['front', 'back', 'rim']); FRONT = Lo['part'][:ns] == 'front'; J = np.asarray(Lo['J'])
Qf = np.asarray(np.load('/tmp/claude-0/rt/fn/final/ear/build/FNL4-CF2_E2_branch.npz')['Q'])
SK = {}
def skull(h, sd):                                            # hidden-ear skull field of the VF2 family head (as ear_build / ear_audit)
    if (h, sd) not in SK:
        fz = np.load('%s/fam/%s_fam.npz' % (CF, h)); V0 = fz['V'].astype(float); Q0 = np.asarray(fz['Q']); si = fz['src_index']
        M0 = sp.csr_matrix((fz['M_data'], fz['M_indices'], fz['M_indptr']), shape=tuple(fz['M_shape'])); z6 = np.load('/home/claude/wayfarer-design/reviews/reference-assets/r6/%s_r6.npz' % h)
        we = M0 @ z6['w_ears'][si].astype(float); rd = E.root_data(V0, Q0, we, 1 if sd == 'l' else -1); SK[(h, sd)] = E.skull_field(V0, Q0, rd, 1 if sd == 'l' else -1)[0]
    return SK[(h, sd)]
def standoff(npz, rec):
    z = np.load(npz); o = []
    for sd in ('l', 'r'):
        f0 = np.nonzero(z['side'] == sd)[0][0]; X = z['V'][f0:f0 + ns]; fr = rec['sides'][sd]['frame']; O, n, b, u = [np.array(fr[k]) for k in ('O', 'n', 'b', 'u')]
        bu = np.c_[(X - O) @ b, (X - O) @ u]; free = SHEET & (E._inside_dist(bu[J], bu) < 0); lat = (X - O) @ n
        o.append((lat[free].mean(), np.median(lat[free]), lat[SHEET].max()))
    return np.mean(o, 0)
def meas(d, k):
    m = jl('%s/meas/%s_measure.json' % (d, k)); s = m['sides']; HH = m['head_HH_cm']; b = jl('%s/build/%s_branch.json' % (d, k))
    av = lambda x: float(np.mean([s[q][x] for q in ('l', 'r')])); L = av('length_lobe_to_tip_cm'); mean_, med_, tip_ = standoff('%s/build/%s_branch.npz' % (d, k), b)
    return dict(HH_cm=HH, length_over_HH=L / HH, body_angle_deg=av('auricle_body_angle_deg'), free_standoff_mean_cm=mean_, free_standoff_median_cm=med_, tip_standoff_cm=tip_,
                free_standoff_mean_over_HH=mean_ / HH, free_standoff_median_over_HH=med_ / HH, tip_standoff_over_HH=tip_ / HH, max_width_over_length=av('max_width_cm') / L,
                tip_above_root_over_HH=av('tip_above_root_cm') / HH, side_view_chord_deg=av('side_view_chord_lobe_to_tip_deg'), upper_extension_axis_deg=av('side_view_upper_extension_deg'),
                tip_angle_deg=av('tip_in_plane_angle_deg_at_1cm'), thickness_median_cm=float(np.mean([s[q]['thickness_cm']['median'] for q in ('l', 'r')])),
                anatomy_relief_peak_cm=m['anatomy_relief_peak_cm'])
def root_concha(d, k, h):
    z = np.load('%s/build/%s_branch.npz' % (d, k)); rec = jl('%s/build/%s_branch.json' % (d, k)); V = z['V']; part = z['part']; side = z['side']; out = {}
    for sd in ('l', 'r'):
        fr = rec['sides'][sd]['frame']; O, n, b, u = [np.array(fr[q]) for q in ('O', 'n', 'b', 'u')]; sk = skull(h, sd); f0 = np.nonzero(side == sd)[0][0]
        bu = lambda X: np.c_[(X - O) @ b, (X - O) @ u]; hgt = lambda X: (X - O) @ n - sk(bu(X))
        cv = np.nonzero((part == 'cuff') & (side == sd))[0]; Jx = V[f0 + J]; dJ, iJ = cKDTree(bu(Jx)).query(bu(V[cv])); hc = hgt(V[cv]); hj = hgt(Jx)
        ant = (Lo['part'][J][iJ] == 'front') & (dJ > 0.3)              # anterior cuff (front-sheet attachment side) away from the junction fillet
        X = V[f0:f0 + ns]; inJ = FRONT & (E._inside_dist(bu(Jx), bu(X)) > 0); hf = hgt(X[inJ])
        out[sd] = dict(cuff_height_above_skin_mean_cm=float(hc.mean()), cuff_height_above_skin_p95_cm=float(np.percentile(hc, 95)),
                       anterior_cuff_mound_max_cm=float(hc[ant].max()), anterior_cuff_mound_p90_cm=float(np.percentile(hc[ant], 90)), anterior_cuff_mound_mean_cm=float(hc[ant].mean()),
                       junction_height_above_skin_mean_cm=float(hj.mean()), junction_height_above_skin_max_cm=float(hj.max()),
                       junction_anterior_height_mean_cm=float(hj[Lo['part'][J] == 'front'].mean()),
                       concha_floor_min_vs_skin_cm=float(hf.min()), concha_floor_p10_vs_skin_cm=float(np.percentile(hf, 10)), sheet_rigid_lift_h0_cm=rec['sides'][sd]['h0_cm'])
    return {q: float(np.mean([out[s][q] for s in out])) for q in out['l']}
R = dict(order='chatgpt-rac-rp3-vael-ear-root-integration-order', alternatives={}, projection={}, probes={}, hidden_ear_regression={}, silhouette={})
for a, (d, c) in ALT.items():
    keys = ['%s_%s' % (HEADS[q], c) for q in HEADS]; zp = os.path.join(EV, '_z_%s.json' % a)
    subprocess.run(['python3', T + '/ear_zones.py', d, zp] + keys, env=dict(os.environ, EAR_TOPO='v002'), check=True, stdout=subprocess.DEVNULL); ZR = jl(zp); os.remove(zp)
    for cfg, h in HEADS.items():
        k = '%s_%s' % (h, c); z = np.load('%s/build/%s_branch.npz' % (d, k)); A = jl('%s/audit/%s_audit.json' % (d, k)); D = jl('%s/deform/%s_deform.json' % (d, k)); b = jl('%s/build/%s_branch.json' % (d, k))
        gp = '%s/build/%s_deform_guard_log.json' % (d, k); Q = np.asarray(z['Q'])
        R['alternatives']['%s %s' % (a, cfg)] = dict(key=k, verts=A['verts'], faces=A['faces'], face_list_equals_frozen_fenn=bool(Q.shape == Qf.shape and np.array_equal(Q, Qf)),
            face_topology_sha256=hashlib.sha256(Q.astype(np.int32).tobytes()).hexdigest(), geo=b['geo'],
            T4=A['T4']['angle_violations'], branch_faces=A['T4']['branch_faces'], T4_by_part=A['T4']['angle_violations_by_part'], aspect_max=A['T4']['aspect_max'], aspect_gt10=A['T4']['aspect_gt10'],
            min_angle=A['T4']['min_angle'], zones={g: (v['angle_viol'], v['faces'], round(v['min_angle'], 1) if v.get('min_angle') is not None else None) for g, v in ZR[k]['groups'].items()},
            density=A['density'], self_intersection_branch=A['self_intersection_pairs_touching_branch'], outside_identical=A['outside_branch_byte_identical'], root_valence=A['root_valence'],
            root_dihedral=A['root_dihedral'], transition=A['transition_ring'], root_deviation=A['root_deviation'], clearance=A['ear_to_head_clearance'],
            integrity=dict(boundary=A['boundary_edges'], nonmanifold=A['nonmanifold_edges'], components=A['components'], degenerate=A['degenerate_faces_branch'], outward=A['normals_outward'], all_quads=bool(Q.shape[1] == 4)),
            root_concha=root_concha(d, k, h), measure=meas(d, k), deform={p: [v['new_selfx_pairs_touching_branch'], v['flipped_branch_faces'], v['root_band_inverted']] for p, v in D['poses'].items()},
            guard=jl(gp) if os.path.exists(gp) else None, fairing={q: v for q, v in b['fairing'].items() if q in ('cuff_skin', 'transition_ring_displacement_cm', 'untangle')})
    for cfg, h in HEADS.items():                             # outer silhouette: sheet shape vs current VA-E2 after removing the rigid lateral shift
        if a == 'current': continue
        z0 = np.load('%s/build/%s_VA-E2_branch.npz' % (CUR, h)); z1 = np.load('%s/build/%s_%s_branch.npz' % (d, h, c)); r0 = jl('%s/build/%s_VA-E2_branch.json' % (CUR, h)); o = {}
        for sd in ('l', 'r'):
            f0 = np.nonzero(z0['side'] == sd)[0][0]; f1 = np.nonzero(z1['side'] == sd)[0][0]; X0 = z0['V'][f0:f0 + ns][SHEET]; X1 = z1['V'][f1:f1 + ns][SHEET]
            n = np.array(r0['sides'][sd]['frame']['n']); sh = ((X1 - X0) @ n).mean(); dv = np.linalg.norm(X1 - X0 - sh * n, axis=1)
            o[sd] = dict(rigid_lateral_shift_cm=float(sh), residual_max_cm=float(dv.max()), residual_mean_cm=float(dv.mean()))
        R['silhouette']['%s %s' % (a, cfg)] = o
for cfg in HEADS:
    P = {nm: meas(*FROZEN[nm][cfg]) for nm in FROZEN}
    for a in ALT: P['Vael %s' % a] = R['alternatives']['%s %s' % (a, cfg)]['measure']
    R['projection'][cfg] = {nm: {q: v for q, v in m.items() if q != 'anatomy_relief_peak_cm'} for nm, m in P.items()}
# probes on the selected alternative (configuration 1)
d, c = ALT[SEL]; h = HEADS['c1']; base = R['alternatives']['%s c1' % SEL]['measure']; Qs = np.asarray(np.load('%s/build/%s_%s_branch.npz' % (d, h, c))['Q'])
EXP = {'proj': 'body_angle_deg', 'tilt': 'side_view_chord_deg', 'sweep': 'sweep', 'len': 'length', 'tip': 'tip_angle_deg', 'wb': 'w_over_L'}
mb = jl('%s/meas/%s_%s_measure.json' % (d, h, c))['sides']
avb = lambda s, x: float(np.mean([s[q][x] for q in ('l', 'r')]))
basev = dict(body_angle_deg=avb(mb, 'auricle_body_angle_deg'), side_view_chord_deg=avb(mb, 'side_view_chord_lobe_to_tip_deg'), sweep=avb(mb, 'sweep_max_axis_deviation_cm') / avb(mb, 'length_lobe_to_tip_cm'),
             length=avb(mb, 'length_lobe_to_tip_cm'), tip_angle_deg=avb(mb, 'tip_in_plane_angle_deg_at_1cm'), w_over_L=avb(mb, 'max_width_cm') / avb(mb, 'length_lobe_to_tip_cm'))
for dd in sorted(glob.glob('%s/probe/*/' % d)):
    n = dd.rstrip('/').split('/')[-1]; A = jl(dd + 'audit.json'); s = jl(dd + 'measure.json')['sides']; L = avb(s, 'length_lobe_to_tip_cm')
    mm = dict(body_angle_deg=avb(s, 'auricle_body_angle_deg'), side_view_chord_deg=avb(s, 'side_view_chord_lobe_to_tip_deg'), sweep=avb(s, 'sweep_max_axis_deviation_cm') / L, length=L,
              tip_angle_deg=avb(s, 'tip_in_plane_angle_deg_at_1cm'), w_over_L=avb(s, 'max_width_cm') / L)
    key = EXP[n.split('_')[0]]; sgn = (-1 if ('_m' in n or 'blunt' in n) else 1) * (-1 if n.startswith('tip') else 1); dv = mm[key] - basev[key]
    zq = np.load(glob.glob(dd + '*_branch.npz')[0])
    R['probes'][n] = dict(T4=A['T4']['angle_violations'], aspect_max=A['T4']['aspect_max'], aspect_gt10=A['T4']['aspect_gt10'], min_angle=A['T4']['min_angle'],
        self_intersection_branch=A['self_intersection_pairs_touching_branch'], boundary=A['boundary_edges'], nonmanifold=A['nonmanifold_edges'],
        root_valence_ok=all(v.get('4', 0) == 52 for v in A['root_valence'].values()), face_list_equal_to_selected=bool(np.array_equal(np.asarray(zq['Q']), Qs)),
        root_deviation=A['root_deviation'], measure=key, value=mm[key], base=basev[key], moves_intended=bool(np.sign(dv) == sgn and abs(dv) > 1e-3))
# hidden-ear regression on the selected alternative
for cfg, h in HEADS.items():
    z = np.load('%s/build/%s_%s_branch.npz' % (d, h, c)); fz = np.load('%s/fam/%s_fam.npz' % (CF, h)); V0 = fz['V'].astype(float)
    m5 = np.asarray(z['v005_to_branch']); kept = np.nonzero(m5 >= 0)[0]; part = z['part'][m5[kept]]; Vb = z['V'][m5[kept]].astype(float); o_ = part == 'v005'; t_ = part == 'transition'
    R['hidden_ear_regression'][cfg] = dict(v005_vertices_outside_branch=int(o_.sum()), max_displacement_outside_branch_cm=float(np.linalg.norm(Vb[o_] - V0[kept[o_]], axis=1).max()),
        outside_branch_byte_identical=bool((Vb[o_] == V0[kept[o_]]).all()), transition_ring_vertices=int(t_.sum()), transition_ring_max_cm=float(np.linalg.norm(Vb[t_] - V0[kept[t_]], axis=1).max()))
json.dump(R, open(os.path.join(EV, 'VAEL_EAR_root_integration_summary.json'), 'w'), indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
for k, r in R['alternatives'].items():
    rc = r['root_concha']
    print('%-12s V %d T4 %d cuff %d asp %.2f min %.1f SI %d crease %s rootdev %.3f/%.3f antmound90 %.2f Jant %.2f conchamin %.2f deform0 %s guard %s faceFN %s' % (k, r['verts'], r['T4'], r['T4_by_part']['cuff'], r['aspect_max'], r['min_angle'], r['self_intersection_branch'],
          [round(v['max_deg']) for v in r['root_dihedral'].values()], r['root_deviation']['cuff_mean_cm'], r['root_deviation']['cuff_p95_cm'], rc['anterior_cuff_mound_p90_cm'], rc['junction_anterior_height_mean_cm'],
          rc['concha_floor_min_vs_skin_cm'], all(sum(v) == 0 for v in r['deform'].values()), [x['iteration'] for x in r['guard']] if r['guard'] else None, r['face_list_equals_frozen_fenn']))
for cfg, P in R['projection'].items():
    for nm, m in P.items(): print(cfg, '%-14s angle %.1f  mean %.3f  median %.3f  tip %.3f (HH)' % (nm, m['body_angle_deg'], m['free_standoff_mean_over_HH'], m['free_standoff_median_over_HH'], m['tip_standoff_over_HH']))
for n, p in R['probes'].items(): print(' probe', n, p['T4'], round(p['aspect_max'], 2), round(p['min_angle'], 1), p['self_intersection_branch'], p['moves_intended'])
print(R['silhouette']); print(R['hidden_ear_regression'])
