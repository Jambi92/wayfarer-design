# ear_summaries.py WORK EVIDENCE_DIR : order bdcd6a6 -- summary records rebuilt from a run_earbranch.sh work folder:
#   FENN_EAR_hidden_ear_CF2_regression.json  (§4 / §14: descriptor landmarks outside the branch and byte-identical in every realization)
#   probes/FENN_EAR_shape_probes.json        (§13 ear-shape readiness, geometry-only probes on configuration 1 E2)
#   audit/FENN_EAR_root_deviation_by_ring.json (§12: cuff skin vs the hidden-ear CF2 skull, by graph ring from the root loop)
#   FENN_EAR_technical_summary.json          (one table of the per-realization audit / deformation numbers used by the gate)
import sys, os, json, glob, numpy as np
from scipy.spatial import cKDTree
import scipy.sparse as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fn_face_metrics as FM
W_, EV = sys.argv[1], sys.argv[2]; CF = '/tmp/claude-0/rt/fn/cf'; R6 = '/home/claude/wayfarer-design/reviews/reference-assets/r6'
HEADS = ('FNL4-CF2', 'FNF181-CF2'); CANDS = ('E1', 'E2', 'E3')
jl = lambda p: json.load(open(p))
dump = lambda o, p: json.dump(o, open(p, 'w'), indent=1, default=lambda x: x.tolist() if hasattr(x, 'tolist') else float(x))
# ---------------- hidden-ear CF2 regression
H = dict(order='bdcd6a6 §4 / §14 hidden-ear CF2 identity with the ear branch',
         rule='hidden-ear body + face identity is evaluated on the accepted R-6 sources with the external ear excluded; the branch changes no source and no production vertex outside the branch',
         heads={}, CF2_hidden_ear_eval_reference='reviews/rac-rp3-evidence/fenn_craniofacial_v001/CF_hidden_ear_eval.json')
ok_all = True
for h in HEADS:
    src = FM.load(os.path.join(R6, h + '_r6.npz')); desc = FM.descriptors(src['V']); fam = np.load(os.path.join(CF, 'fam', h + '_fam.npz')); Vf = fam['V']
    t = cKDTree(Vf); lmv = sorted({int(t.query(src['V'][i])[1]) for i in FM.LM.values()}); per = {}
    for c in CANDS:
        z = np.load(os.path.join(W_, 'build', '%s_%s_branch.npz' % (h, c))); v2b = z['v005_to_branch']; part = z['part']
        inb = [v for v in lmv if v2b[v] < 0 or part[v2b[v]] != 'v005']
        keep = np.nonzero(v2b >= 0)[0]; outside = keep[part[v2b[keep]] == 'v005']
        lm_ident = bool(all(v2b[v] >= 0 and np.array_equal(z['V'][v2b[v]], Vf[v]) for v in lmv))
        out_ident = bool(np.array_equal(z['V'][v2b[outside]], Vf[outside]))
        tr = keep[part[v2b[keep]] == 'transition']; dtr = np.linalg.norm(z['V'][v2b[tr]] - Vf[tr], axis=1)
        per[c] = dict(landmark_nearest_family_vertices_in_branch=inb, landmark_family_vertices_byte_identical=lm_ident, outside_branch_byte_identical=out_ident,
                      transition_ring_max_displacement_cm=float(dtr.max()))
        ok_all &= (not inb) and lm_ident and out_ident
    H['heads'][h] = dict(source_descriptors=desc, landmark_family_vertices=len(lmv), per_candidate=per)
H['verdict'] = ('hidden-ear CF2 identity PASS unchanged (sources unchanged; every descriptor landmark is outside the branch and byte-identical in every E realization)' if ok_all
                else 'CHECK: a descriptor landmark touches the branch or changed')
dump(H, os.path.join(EV, 'FENN_EAR_hidden_ear_CF2_regression.json'))
# ---------------- probes
P = dict(order='bdcd6a6 §13 ear-shape readiness (geometry-only, same topology, configuration 1 E2 base; not production morphs)', base='FNL4-CF2 E2', probes={})
base_q = np.load(os.path.join(W_, 'build/FNL4-CF2_E2_branch.npz'))['Q']
for d in sorted(glob.glob(os.path.join(W_, 'probe', '*'))):
    nm = os.path.basename(d); a = jl(os.path.join(d, 'audit.json')); m = jl(os.path.join(d, 'measure.json'))['sides']['l']
    arg = open(os.path.join(d, 'build.log')).read(); pv = jl(glob.glob(os.path.join(d, '*_branch.json'))[0]).get('probe', {})
    P['probes'][nm] = dict(probe=pv, same_topology_as_base=bool(np.array_equal(np.load(glob.glob(os.path.join(d, '*_branch.npz'))[0])['Q'], base_q)),
                           self_intersection_pairs_touching_branch=a['self_intersection_pairs_touching_branch'], boundary_edges=a['boundary_edges'], nonmanifold_edges=a['nonmanifold_edges'],
                           aspect_max=a['T4']['aspect_max'], aspect_gt10=a['T4']['aspect_gt10'], T4_angle_violations=a['T4']['angle_violations'],
                           ear_to_head_clearance_min_cm=a['ear_to_head_clearance']['min_cm'],
                           measured=dict(chord_cm=m['length_lobe_to_tip_cm'], auricle_body_angle_deg=m['auricle_body_angle_deg'], upper_axis_deg=m['side_view_upper_extension_deg'],
                                         sweep_cm=m['sweep_max_axis_deviation_cm'], tip_angle_deg=m['tip_in_plane_angle_deg_at_1cm'], extent_cm=m['total_lateral_extent_from_root_plane_cm']))
pp = P['probes'].values()
P['summary'] = dict(n=len(P['probes']), all_same_topology=all(p['same_topology_as_base'] for p in pp), all_self_intersection_0=all(p['self_intersection_pairs_touching_branch'] == 0 for p in pp),
                    all_closed_manifold=all(p['boundary_edges'] == 0 and p['nonmanifold_edges'] == 0 for p in pp), aspect_max=max(p['aspect_max'] for p in pp),
                    clearance_min_cm=min(p['ear_to_head_clearance_min_cm'] for p in pp))
os.makedirs(os.path.join(EV, 'probes'), exist_ok=True); dump(P, os.path.join(EV, 'probes/FENN_EAR_shape_probes.json'))
# ---------------- root deviation by ring + technical summary
RD = dict(note='distance of cuff skin from the hidden-ear CF2 skull (v005 ear zone harmonically collapsed onto its root loop), by graph ring inside the root loop; '
               'the root loop itself is unchanged (0). The transition ring lies outside the root and is reported as its displacement from v005.', realizations={})
TS = dict(order='bdcd6a6 per-realization technical summary (from audit / deform / measure / build records)', realizations={})
for h in HEADS:
    for c in CANDS:
        k = '%s_%s' % (h, c); z = np.load(os.path.join(W_, 'build', k + '_branch.npz')); rec = jl(os.path.join(W_, 'build', k + '_branch.json'))
        a = jl(os.path.join(W_, 'audit', k + '_audit.json')); dfm = jl(os.path.join(W_, 'deform', k + '_deform.json')); m = jl(os.path.join(W_, 'meas', k + '_measure.json'))
        cd = np.load(os.path.join(W_, 'audit', k + '_audit_cuffdev.npy')); dev = dict(zip(cd[:, 0].astype(int), cd[:, 1]))
        Q = z['Q']; nV = len(z['V']); part = z['part']
        Ei = np.unique(np.sort(np.concatenate([Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]]), 1), axis=0)
        A = sp.coo_matrix((np.ones(2 * len(Ei)), (np.r_[Ei[:, 0], Ei[:, 1]], np.r_[Ei[:, 1], Ei[:, 0]])), shape=(nV, nV)).tocsr()
        rr = {}
        for s in ('l', 'r'):
            root = z['v005_to_branch'][np.array(rec['sides'][s]['root_loop_v005'])]; cur = set(root.tolist()); seen = set(cur)
            for ring in (1, 2, 3):
                nb = set(A[list(cur)].indices.tolist()) - seen; nb = {v for v in nb if part[v] == 'cuff'}; seen |= nb; cur = nb
                rr.setdefault(ring, []).extend(dev[v] for v in nb if v in dev)
        tr = a['transition_ring']
        RD['realizations'][k] = dict(**{'ring%d_mean_cm' % r: float(np.mean(v)) for r, v in rr.items()}, **{'ring%d_max_cm' % r: float(np.max(v)) for r, v in rr.items()},
                                     cuff_all=a['root_deviation'], transition_ring_displacement_from_v005=tr)
        pol = a['poles_branch']; T4 = a['T4']; dn = a['density']
        dsum = dfm.get('summary', dfm)
        TS['realizations'][k] = dict(verts=a['verts'], faces=a['faces'], boundary=a['boundary_edges'], nonmanifold=a['nonmanifold_edges'], components=a['components'],
                                     degenerate=a['degenerate_faces'], outward=a['normals_outward'], si_total=a['self_intersection_pairs_total'], si_v005_baseline=a['self_intersection_pairs_cf2_family_v005'],
                                     si_branch=a['self_intersection_pairs_touching_branch'], outside_identical=a['outside_branch_byte_identical'], T4=T4, poles=pol, poles_total=a['poles_branch_total'],
                                     density=dn, root_valence=a['root_valence'], root_dihedral=a['root_dihedral'], clearance=a['ear_to_head_clearance'], deform=dsum,
                                     measure_l={kk: m['sides']['l'][kk] for kk in ('length_lobe_to_tip_cm', 'auricle_height_cm', 'max_width_cm', 'auricle_body_angle_deg',
                                                'total_lateral_extent_from_root_plane_cm', 'side_view_upper_extension_deg', 'sweep_max_axis_deviation_cm', 'tip_in_plane_angle_deg_at_1cm')},
                                     thickness_median_cm=m['sides']['l']['thickness_cm']['median'],
                                     min_margin_cm=min(rec['sides'][s]['min_margin_cm'] for s in ('l', 'r')))
Qs = {k: np.load(os.path.join(W_, 'build', k + '_branch.npz'))['Q'] for k in TS['realizations']}; q0 = next(iter(Qs.values()))
TS['identical_topology_all_six'] = bool(all(np.array_equal(q, q0) for q in Qs.values()))
dump(RD, os.path.join(EV, 'audit/FENN_EAR_root_deviation_by_ring.json')); dump(TS, os.path.join(EV, 'FENN_EAR_technical_summary.json'))
print('summaries written; hidden-ear ok', ok_all, 'identical topology', TS['identical_topology_all_six'], 'probes', P['summary'])
