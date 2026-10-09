# RAC W2I5 §6 scale-field continuity after the thigh sculpt: the accepted W2I4 sa_fieldcheck metric (vertical / horizontal correlation-length
# ratio of the scale relief, in units of the local scale size R; seed nearest-neighbour spacing / R) for the frozen control, the accepted
# W2I4 field and the W2I5 field regenerated with the SAME saved W2I4 seeds; plus the per-vertex identity check of the reuse (seed indices
# identical; relief outside the sculpted thigh identical to W2I4). Usage: python3 sa_fieldcheck5.py OUT.json
import sys, os, json, numpy as np, igl
from scipy.spatial import cKDTree
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D); sys.path.insert(0, os.path.join(os.path.dirname(D), 'w2i4_drivers'))
import sa_fieldcheck as FC                                     # loads the frozen control and the accepted W2I4 field
S = FC.S; nb = FC.nb; F = FC.F; R = FC.R; FAM = FC.FAM
V5 = np.load(S + '/w2i5/surf/fin_up.npz')['V'].astype(float); N5 = igl.per_vertex_normals(V5, F)
s5 = (np.load(S + '/w2i5/surf/saurin_w2i5_surface_delta.npz')['d'].astype(float) * N5).sum(1)
seeds4 = np.load(S + '/w2i4/surf/fin_seeds.npy'); seeds5 = np.load(S + '/w2i5/surf/fin_seeds.npy')
res = dict(seed_reuse=dict(identical=bool(np.array_equal(seeds4, seeds5)), n=int(len(seeds5))))
moved = np.linalg.norm(V5 - FC.Vf, axis=1) > 1e-6
res['relief_identity'] = dict(vertices_geometry_moved=int(moved.sum()), relief_max_abs_diff_unmoved_cm=float(np.abs(s5 - FC.s_new)[~moved].max()) if (~moved).any() else 0.0,
                              relief_rms_diff_all_cm=float(np.sqrt(((s5 - FC.s_new) ** 2).mean())))
ts = cKDTree(V5[seeds5]); dd, _ = ts.query(V5[seeds5], k=2); nn = dd[:, 1] / R[seeds5]
for nm, m in FC.REG.items():
    idx = np.where(m & ((FAM[:nb] != 6) & (FAM[:nb] != 7)))[0]
    r = dict(n=int(len(idx)), median_R_cm=float(np.median(R[idx])))
    for fld, V, Nrm, s in (('frozen', FC.V0u, FC.N0, FC.s_froz), ('W2I4', FC.Vf, FC.Nf, FC.s_new), ('W2I5', V5, N5, s5)): r[fld] = FC.corrlen(V, Nrm, s, idx, np.random.default_rng(3))
    ins = seeds5[seeds5 < nb]; ins = ins[np.isin(ins, idx)]; r['W2I5_seed_nn_over_R_median'] = float(np.median(nn[np.isin(seeds5, ins)])) if len(ins) else None
    res[nm] = r; print(nm, {k: (round(v['v_over_h'], 3) if isinstance(v, dict) else v) for k, v in r.items()}, flush=True)
res['all_seeds_nn_over_R'] = dict(p10=float(np.percentile(nn, 10)), p50=float(np.median(nn)), p90=float(np.percentile(nn, 90)))
print(res['seed_reuse'], res['relief_identity']); json.dump(res, open(sys.argv[1], 'w'), indent=1)
