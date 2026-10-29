# hv_ear_summary.py OUT.json LABEL:WORK:CAND:HEAD ... : Halvren mixed-ear order §9-§10 / §20-§22 technical + root / concha record of ear realizations
# (hv_ear.sh outputs): integrity, T-4 / aspect / min corner by part, density, branch self-intersections, root valence / crease, transition ring, ear-head
# clearance, 8-pose head / neck readiness (contacts / flips / root inversions touching the branch), guard iterations, and the ONE-AURICLE root / concha
# audit of the Vael root-integration order (cuff height above the hidden-ear skull, anterior cuff mound away from the junction fillet, junction height
# above the skin, concha-floor level), plus ear_measure dimensions. Gates (§21): 100 % quads, 1 component, 0 boundary / non-manifold / degenerate,
# outward, 0 branch self-intersections, aspect < 10, density < 0.25 % stature, root valence 4 x 52, min corner >= 10 deg, 0 posed contacts / flips /
# root inversions; one auricle = anterior cuff mound p90 <= 0.20 cm and anterior junction <= 0.40 cm above the skin (Vael RI3 class: 0.17 / 0.31).
import sys, os, json, hashlib, numpy as np
os.environ.setdefault('EAR_TOPO', 'v002')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import hv_ear_domains as D
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001'); import ear_branch_lib as E
from scipy.spatial import cKDTree
jl = lambda p: json.load(open(p)); Lo = E.canonical_layout(); st = Lo['st']; ns = len(st); FRONT = Lo['part'][:ns] == 'front'; J = np.asarray(Lo['J'])
def root_concha(z, rec, head):
    V = z['V']; part = z['part']; side = z['side']; out = {}
    for sd in ('l', 'r'):
        fr = rec['sides'][sd]['frame']; O, n, b, u = [np.array(fr[q]) for q in ('O', 'n', 'b', 'u')]; sk = D.frame(head, sd)['skull']; f0 = np.nonzero(side == sd)[0][0]
        bu = lambda X: np.c_[(X - O) @ b, (X - O) @ u]; hgt = lambda X: (X - O) @ n - sk(bu(X))
        cv = np.nonzero((part == 'cuff') & (side == sd))[0]; Jx = V[f0 + J]; dJ, iJ = cKDTree(bu(Jx)).query(bu(V[cv])); hc = hgt(V[cv]); hj = hgt(Jx)
        ant = (Lo['part'][J][iJ] == 'front') & (dJ > 0.3); X = V[f0:f0 + ns]; inJ = FRONT & (E._inside_dist(bu(Jx), bu(X)) > 0); hf = hgt(X[inJ])
        out[sd] = dict(cuff_height_above_skin_mean_cm=float(hc.mean()), cuff_height_above_skin_p95_cm=float(np.percentile(hc, 95)),
                       anterior_cuff_mound_p90_cm=float(np.percentile(hc[ant], 90)), anterior_cuff_mound_max_cm=float(hc[ant].max()),
                       junction_height_above_skin_mean_cm=float(hj.mean()), junction_anterior_height_mean_cm=float(hj[Lo['part'][J] == 'front'].mean()),
                       concha_floor_min_vs_skin_cm=float(hf.min()), sheet_rigid_lift_h0_cm=rec['sides'][sd]['h0_cm'], place_offset_cm=rec['sides'][sd].get('place_offset_cm'),
                       place_min_margin_cm=rec['sides'][sd].get('min_margin_cm'))
    return {q: (float(np.mean([out[s][q] for s in out])) if not isinstance(out['l'][q], list) else out['l'][q]) for q in out['l']}
def summ(work, cand, head):
    k = '%s_%s' % (head, cand); z = np.load('%s/build/%s_branch.npz' % (work, k)); rec = jl('%s/build/%s_branch.json' % (work, k)); A = jl('%s/audit/%s_audit.json' % (work, k))
    Dd = jl('%s/deform/%s_deform.json' % (work, k)); M = jl('%s/meas/%s_measure.json' % (work, k)); gl = '%s/build/%s_deform_guard_log.json' % (work, k); Q = np.asarray(z['Q'])
    T4 = A['T4']; poses = {p: dict(contacts=len(v['new_pairs']), flips=len(v['flipped_faces']), root_inv=len(v['root_inverted_faces'])) for p, v in Dd['poses'].items()}
    rc = root_concha(z, rec, head); av = lambda q: float(np.mean([M['sides'][s][q] for s in ('l', 'r')]))
    r = dict(key=k, verts=A['verts'], faces=A['faces'], all_quads=bool(Q.shape[1] == 4), face_topology_sha256=hashlib.sha256(Q.astype(np.int32).tobytes()).hexdigest(),
             integrity=dict(components=A['components'], boundary=A['boundary_edges'], nonmanifold=A['nonmanifold_edges'], degenerate=A['degenerate_faces_branch'], outward=A['normals_outward'],
                            branch_selfx=A['self_intersection_pairs_touching_branch']),
             T4=T4['angle_violations'], branch_faces=T4['branch_faces'], T4_by_part=T4['angle_violations_by_part'], aspect_max=T4['aspect_max'], aspect_gt10=T4['aspect_gt10'], aspect_gt6=T4['aspect_gt6'],
             min_angle=T4['min_angle'], density_pct=A['density']['branch_mean_edge_pct_stature'], density_pass=A['density']['pass_mean'], root_valence=A['root_valence'],
             root_crease_max_deg=max(A['root_dihedral'][s]['max_deg'] for s in ('l', 'r')), transition=A.get('transition_ring'), outside_identical=A.get('outside_branch_byte_identical'),
             clearance_min_cm=A['ear_to_head_clearance']['min_cm'], poses=poses, guard=jl(gl) if os.path.exists(gl) else None, root_concha=rc,
             measure=dict(length_cm=av('length_lobe_to_tip_cm'), length_over_HH=av('length_lobe_to_tip_cm') / M['head_HH_cm'], max_width_cm=av('max_width_cm'), body_angle_deg=av('auricle_body_angle_deg'),
                          side_view_chord_deg=av('side_view_chord_lobe_to_tip_deg'), tip_angle_deg=av('tip_in_plane_angle_deg_at_1cm'), tip_above_root_cm=av('tip_above_root_cm'),
                          sweep_cm=av('sweep_max_axis_deviation_cm'), thickness_median_cm=float(np.mean([M['sides'][s]['thickness_cm']['median'] for s in ('l', 'r')])), relief_peak_cm=M['anatomy_relief_peak_cm']))
    rv = all(v == {'4': 52} for v in A['root_valence'].values())
    r['gates'] = dict(quads=r['all_quads'], one_component=A['components'] == 1, boundary0=A['boundary_edges'] == 0, nonmanifold0=A['nonmanifold_edges'] == 0, degenerate0=A['degenerate_faces_branch'] == 0,
                      outward=bool(A['normals_outward']), branch_selfx0=A['self_intersection_pairs_touching_branch'] == 0, aspect_lt10=T4['aspect_max'] < 10, density=bool(A['density']['pass_mean']),
                      root_valence=rv, min_corner_ge10=T4['min_angle'] >= 10.0, poses_clean=all(p['contacts'] == 0 and p['flips'] == 0 and p['root_inv'] == 0 for p in poses.values()))
    r['technical_pass'] = all(r['gates'].values())
    r['one_auricle_metrics_pass'] = bool(rc['anterior_cuff_mound_p90_cm'] <= 0.20 and rc['junction_anterior_height_mean_cm'] <= 0.40)
    return r
if __name__ == '__main__':
    R = {}
    for it in sys.argv[2:]:
        lab, w, c, h = it.split(':'); R[lab] = summ(w, c, h); x = R[lab]
        print(lab, 'TECH', x['technical_pass'], {g: v for g, v in x['gates'].items() if not v}, 'T4 %d min %.1f asp %.2f selfx %d' % (x['T4'], x['min_angle'], x['aspect_max'], x['integrity']['branch_selfx']),
              'mound p90 %.2f junc %.2f floor %.2f' % (x['root_concha']['anterior_cuff_mound_p90_cm'], x['root_concha']['junction_anterior_height_mean_cm'], x['root_concha']['concha_floor_min_vs_skin_cm']),
              'L/HH %.3f' % x['measure']['length_over_HH'], flush=True)
    json.dump(R, open(sys.argv[1], 'w'), indent=1)
