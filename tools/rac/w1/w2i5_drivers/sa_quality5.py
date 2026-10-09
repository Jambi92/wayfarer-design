# RAC W2I5 §7 topology / fold / strain guards after the thigh sculpt, against the accepted W2I4 candidate: (1) SA-M188 / SA-F188 strain and
# flips vs W2I4 and vs frozen, with the sculpted-thigh edge statistics (band-wide stretch / compression check); (2) 62-body flip census
# (W2I5 vs W2I4; new vs frozen beyond what W2I4 already had); (3) topology of the surfaced SA-M188 (closed, manifold, degenerate faces,
# self-orientation vs its own base, compared with W2I4); (4) sculpt-delta magnitude and where it acts. Usage: python3 sa_quality5.py OUT.json
import sys, os, json, numpy as np, igl
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D); sys.path.insert(0, os.path.join(os.path.dirname(D), 'w2i4_drivers')); sys.path.insert(0, os.path.join(os.path.dirname(D), 'w2i2_drivers'))
import sa_sculpt as SC5; import sa_finish as FN
RB = FN.RB; B = FN.B; L = FN.L; V0 = FN.V0; F0 = FN.F0; S = FN.C.S
D5, i5 = SC5.final_delta(); act = np.linalg.norm(D5, axis=1) > 1e-6
E = np.vstack([F0[:, [0, 1]], F0[:, [1, 2]], F0[:, [2, 0]]]); eact = act[E[:, 0]] | act[E[:, 1]]
nr = lambda P: np.cross(P[F0[:, 1]] - P[F0[:, 0]], P[F0[:, 2]] - P[F0[:, 0]])
out = dict(sculpt_info={k: v for k, v in i5.items() if k != 'fold_guard'}, fold_guard_rounds=[r['total'] for r in i5.get('fold_guard', [])])
out['sculpt_delta'] = dict(vertices_moved=int(act.sum()), max_cm=float(np.linalg.norm(D5, axis=1).max()), p99_cm=float(np.percentile(np.linalg.norm(D5[act], axis=1), 99)),
                           u0_range=[float(V0[act, 2].min()), float(V0[act, 2].max())], leg_label_min=float(L.leg[act].min()), tail_label_max=float(L.tail[act].max()))
for bid, p in (("SA-M188", {}), ("SA-F188", B.CEN)):
    P0 = RB.build_r(p, {})[0]; P4, q4, k4, _ = FN.build_f(p); P5, q5, k5, _ = SC5.build_s(p)
    la = np.linalg.norm(P4[E[:, 0]] - P4[E[:, 1]], axis=1); lb = np.linalg.norm(P5[E[:, 0]] - P5[E[:, 1]], axis=1); r = (lb / la)[eact]
    M4 = B.measure(P4, q4, k4); M5 = B.measure(P5, q5, k5); num = {kk: (M4[kk], M5[kk]) for kk in M4 if isinstance(M4[kk], (int, float)) and not isinstance(M4[kk], bool) and abs(M4[kk]) > 1e-6}
    out[bid] = dict(W2I5_vs_W2I4=RB.strain(P4, P5), W2I5_vs_frozen=RB.strain(P0, P5), W2I4_vs_frozen=RB.strain(P0, P4),
                    sculpt_edges=dict(n=int(eact.sum()), p1=float(np.percentile(r, 1)), p50=float(np.median(r)), p99=float(np.percentile(r, 99)), min=float(r.min()), max=float(r.max()),
                                      frac_outside_0p8_1p25=float(((r < 0.8) | (r > 1.25)).mean()), n_outside_0p8_1p25=int(((r < 0.8) | (r > 1.25)).sum())),
                    max_abs_rel_measure_change_pct=max(abs(b / a - 1) * 100 for a, b in num.values()),
                    measures_changed_over_0p01pct={kk: [a, b] for kk, (a, b) in num.items() if abs(b / a - 1) > 1e-4})
    print(bid, 'flips vs W2I4', out[bid]['W2I5_vs_W2I4']['flipped_faces'], 'vs frozen', out[bid]['W2I5_vs_frozen']['flipped_faces'], 'sculpt edges', out[bid]['sculpt_edges'], flush=True)
import sa_w2i2_build as WB
cen = {}; A, deg = FN.adjacency()
for bid, p, h, note in WB.ALL:
    P4 = FN.build_f(p, h)[0]; a = nr(RB.build_r(p, {}, h)[0]); b = nr(P4); c = nr(SC5.build_s(p, h)[0]); ns = SC5.smooth_face_normals(P4, A, deg)
    pre = np.einsum('ij,ij->i', a, b) < 0; fold4 = np.einsum('ij,ij->i', b, ns) < 0; foldc = np.einsum('ij,ij->i', c, ns) < 0; flip = np.einsum('ij,ij->i', b, c) < 0
    cs = lambda x, y: np.einsum('ij,ij->i', x, y) / (np.linalg.norm(x, axis=1) * np.linalg.norm(y, axis=1) + 1e-20); rep = flip & ~foldc & (cs(c, ns) > cs(b, ns))
    cen[bid] = dict(W2I4_vs_frozen=int(pre.sum()), W2I4_folds=int(fold4.sum()), W2I5_folds=int(foldc.sum()),
                    W2I5_vs_W2I4=int(flip.sum()), W2I5_vs_W2I4_repairs=int(rep.sum()), W2I5_vs_W2I4_new_flips=int((flip & ~rep).sum()),
                    W2I5_new_folds=int((foldc & ~fold4).sum()), W2I5_new_vs_frozen=int(((np.einsum('ij,ij->i', a, c) < 0) & ~pre).sum()))
KS = ('W2I4_vs_frozen', 'W2I4_folds', 'W2I5_folds', 'W2I5_vs_W2I4', 'W2I5_vs_W2I4_repairs', 'W2I5_vs_W2I4_new_flips', 'W2I5_new_folds', 'W2I5_new_vs_frozen')
out['flip_census'] = cen; out['flip_census_totals'] = {k: sum(v[k] for v in cen.values()) for k in KS}
print(out['flip_census_totals'], flush=True)
def topo(Vb, Fu, d):
    Vs = Vb + d; Es = np.sort(np.vstack([Fu[:, [0, 1]], Fu[:, [1, 2]], Fu[:, [2, 0]]]), 1); _, cnt = np.unique(Es, axis=0, return_counts=True)
    nrf = lambda P: np.cross(P[Fu[:, 1]] - P[Fu[:, 0]], P[Fu[:, 2]] - P[Fu[:, 0]])
    return dict(vertices=int(len(Vs)), faces=int(len(Fu)), boundary_edges=int((cnt == 1).sum()), nonmanifold_edges=int((cnt > 2).sum()), degenerate_faces=int((igl.doublearea(Vs, Fu) < 2e-10).sum()),
                flipped_vs_own_base=int((np.einsum('ij,ij->i', nrf(Vb), nrf(Vs)) < 0).sum()), euler_characteristic=int(len(Vs) - len(cnt) + len(Fu)))
T = {}
for nm in ('w2i4', 'w2i5'):
    z = np.load(S + '/%s/surf/fin_up.npz' % nm); Vb = z['V'].astype(float); Fu = z['F'].astype(np.int64)
    T[nm] = topo(Vb, Fu, np.load(S + '/%s/surf/saurin_%s_surface_delta.npz' % (nm, nm))['d'].astype(float))
z4 = np.load(S + '/w2i4/surf/fin_up.npz'); Fu = z4['F'].astype(np.int64)
Vs4 = z4['V'].astype(float) + np.load(S + '/w2i4/surf/saurin_w2i4_surface_delta.npz')['d']; Vs5 = np.load(S + '/w2i5/surf/fin_up.npz')['V'].astype(float) + np.load(S + '/w2i5/surf/saurin_w2i5_surface_delta.npz')['d']
nrf = lambda P: np.cross(P[Fu[:, 1]] - P[Fu[:, 0]], P[Fu[:, 2]] - P[Fu[:, 0]])
T['surfaced_W2I5_vs_W2I4_flipped'] = int((np.einsum('ij,ij->i', nrf(Vs4), nrf(Vs5)) < 0).sum())
out['topology_surfaced_SA-M188'] = T; print(T, flush=True)
json.dump(out, open(sys.argv[1], 'w'), indent=1, default=float)
