# RAC W2I4 §14 asset-quality measures: (1) surface strain / flipped faces of the finished asset vs the frozen body and vs the W2I3 rebuild
# (SA-M188, SA-F188); (2) topology of the finished surfaced mesh (manifold edges, boundary edges, degenerate faces, flipped faces vs the frozen
# surfaced mesh); (3) thigh fine-relief (Gaussian 1.5 cm split) vertical / horizontal correlation-length ratio: frozen vs W2I3 vs W2I4;
# (4) finish-delta magnitude by zone and girth / station changes W2I3 -> W2I4. Usage: python3 sa_quality.py OUT.json
import sys, os, json, numpy as np, igl
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import sa_finish as FN, sa_fieldcheck as FC
sys.path.insert(0, os.path.join(os.path.dirname(D), 'w2i2_drivers'))
RB = FN.RB; B = FN.B; L = FN.L; V0 = FN.V0; F0 = FN.F0; S = FN.C.S
out = {}
for bid, p in (("SA-M188", {}), ("SA-F188", B.CEN)):
    P0 = RB.build_r(p, {})[0]; Pr = RB.build_r(p, RB.TARGET)[0]; Pf, q, k, info = FN.build_f(p)
    out[bid] = dict(finished_vs_frozen=RB.strain(P0, Pf), finished_vs_W2I3=RB.strain(Pr, Pf), W2I3_vs_frozen=RB.strain(P0, Pr))
    _, qr, kr, _ = RB.build_r(p, RB.TARGET); Mr = B.measure(Pr, qr, kr); Mf = B.measure(Pf, q, k)
    num = {kk: (Mr[kk], Mf[kk]) for kk in Mr if isinstance(Mr[kk], (int, float)) and not isinstance(Mr[kk], bool)}
    out[bid]['W2I3_to_W2I4_max_abs_rel_change_pct'] = max(abs(b / a - 1) * 100 for a, b in num.values() if abs(a) > 1e-6)
    out[bid]['W2I3_to_W2I4_changes_over_0.05pct'] = {kk: [a, b] for kk, (a, b) in num.items() if abs(a) > 1e-6 and abs(b / a - 1) > 5e-4}
    print(bid, 'flipped', out[bid]['finished_vs_frozen']['flipped_faces'], 'max rel change %.4f %%' % out[bid]['W2I3_to_W2I4_max_abs_rel_change_pct'], flush=True)
# topology of the final surfaced SA-M188 mesh
Vu = np.load(S + '/w2i4/surf/fin_up.npz')['V'].astype(float); Fu = np.load(S + '/w2i4/surf/fin_up.npz')['F'].astype(np.int64)
d = np.load(S + '/w2i4/surf/saurin_w2i4_surface_delta.npz')['d'].astype(float); Vs = Vu + d
up0 = np.load(S + '/w2i/rodin/c12/g15up.npz'); Vs0 = up0['V'].astype(float) + np.load('/mnt/attach/outputs/racebodies_v35/saurin_final_surface_delta.npz')['d'].astype(float)
E = np.sort(np.vstack([Fu[:, [0, 1]], Fu[:, [1, 2]], Fu[:, [2, 0]]]), 1); _, cnt = np.unique(E, axis=0, return_counts=True)
ar = igl.doublearea(Vs, Fu) / 2; nr = lambda P: np.cross(P[Fu[:, 1]] - P[Fu[:, 0]], P[Fu[:, 2]] - P[Fu[:, 0]])
out['topology_SA-M188_surfaced'] = dict(vertices=int(len(Vs)), faces=int(len(Fu)), edges=int(len(cnt)), boundary_edges=int((cnt == 1).sum()), nonmanifold_edges=int((cnt > 2).sum()),
    degenerate_faces=int((ar < 1e-10).sum()), flipped_vs_frozen_surfaced=int((np.einsum('ij,ij->i', nr(Vs0), nr(Vs)) < 0).sum()),
    flipped_vs_finished_base=int((np.einsum('ij,ij->i', nr(Vu), nr(Vs)) < 0).sum()), frozen_surfaced_flipped_vs_frozen_base=int((np.einsum('ij,ij->i', nr(up0['V'].astype(float)), nr(Vs0)) < 0).sum()),
    euler_characteristic=int(len(Vs) - len(cnt) + len(Fu)))
print(out['topology_SA-M188_surfaced'], flush=True)
# thigh fine relief anisotropy
idx = np.where((L.leg > 0.6) & (V0[:, 2] > 66) & (V0[:, 2] < 84) & (L.tail < 0.05))[0]
Dl, finf = FN.finish_delta(); Pr = RB.build_r({}, RB.TARGET)[0]; Pf = Pr + Dl; FC.R[:] = 1.0
rel = {}
for nm, P in (('frozen', V0.astype(float)), ('W2I3', Pr), ('W2I4', Pf)):
    Nn = igl.per_vertex_normals(P, F0); sm = FN.gsmooth(P, idx, 1.5); r = np.zeros(len(P)); r[idx] = np.einsum('ij,ij->i', P[idx] - sm, Nn[idx])
    FC.DEL[:] = np.array([0.15, 0.3, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 5.5, 7.0, 9.0]); c = FC.corrlen(P, Nn, r, idx, np.random.default_rng(3))
    rel[nm] = c; print('thigh relief', nm, c, flush=True)
out['thigh_fine_relief_corrlen_cm'] = rel; out['finish_delta'] = finf
zm, zz = FN.zones(); out['finish_delta_by_zone_max_cm'] = {k: float(np.linalg.norm(Dl[m], axis=1).max()) for k, m in zz.items()}
out['finish_delta_outside_zones_and_thigh_max_cm'] = float(np.linalg.norm(Dl[~zm & ~((L.leg > 0.3) & (V0[:, 2] > 54) & (V0[:, 2] < 96))], axis=1).max())
# flip census over the whole W2I body list: faces flipped by the finish (vs the W2I3 rebuild of the same body) and new flips vs the frozen
# body that the W2I3 rebuild did not already have
import sa_w2i2_build as WB
nr = lambda P: np.cross(P[F0[:, 1]] - P[F0[:, 0]], P[F0[:, 2]] - P[F0[:, 0]]); cen = {}
for bid, p, h, note in WB.ALL:
    a = nr(RB.build_r(p, {}, h)[0]); b = nr(RB.build_r(p, RB.TARGET, h)[0]); c = nr(FN.build_f(p, h)[0])
    pre = np.einsum('ij,ij->i', a, b) < 0
    cen[bid] = dict(W2I3_vs_frozen=int(pre.sum()), W2I4_vs_W2I3=int((np.einsum('ij,ij->i', b, c) < 0).sum()), W2I4_new_vs_frozen=int(((np.einsum('ij,ij->i', a, c) < 0) & ~pre).sum()))
out['flip_census'] = cen; out['flip_census_totals'] = {k: sum(v[k] for v in cen.values()) for k in ('W2I3_vs_frozen', 'W2I4_vs_W2I3', 'W2I4_new_vs_frozen')}
print(out['flip_census_totals'])
json.dump(out, open(sys.argv[1], 'w'), indent=1, default=float)
