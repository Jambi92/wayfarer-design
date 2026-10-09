# RAC W2I5 §6 (copy of the W2I4 sa_surface.py run on the W2I5 base; REUSES the accepted saved W2I4 seed file copied to $S/w2i5/surf/fin_seeds.npy). W2I4 header:
# RAC W2I4 §7: regenerate the Saurin scale / surface field on the FINISHED L1 + F2 base (SA-M188 reference frame). COPIES ONLY.
# Route (mirrors final-brow build15.sh: upsample -> region fields -> g7surfc -> final delta), with two documented differences:
#  * region fields: the accepted g15reg labels (FAM / R / H / EL / PL / IMB / ATT / TYM; g7regs with HEAD_SCALE 1.08 on the upsampled frozen
#    base) are CARRIED by vertex correspondence (identical topology), so every vertex keeps its accepted scale family, size (cm), relief height,
#    elongation and imbrication; only the geometry-dependent fields are recomputed on the finished base: N (vertex normals) and the flow
#    direction T (transported through the per-face deformation gradient frozen -> finished and re-projected to the tangent plane).
#    Re-running g7regs on the finished base is NOT used: its band / joint construction points are the frozen g7geo ones and would mislabel
#    the moved knee / elbow / neck bands.
#  * seeds: the accepted carried seed file (seeds15.npy) is not available (not in the repo or on the PC) and could not be recovered from the
#    frozen delta (sa_seeds.py: cell-centroid and local-maximum recovery give corr 0.20-0.23 with the frozen field, no better than independent
#    seeds, 0.26). The field is therefore regenerated with fresh variable-radius Poisson seeds (seedpd, c 0.50, rng 7) on the finished base
#    and the seed file is now SAVED with the asset, so the regenerated realization is exactly reproducible.
# Outputs ($S/w2i4/surf): fin_up.npz (upsampled finished base), fin_reg.npz (fields), fin_seeds.npy, fin_surf.npz (g7surfc), and
# saurin_w2i5_surface_delta.npz (key 'd', normal-only: final surface = igl.upsample(base) + d), plus 'before' = frozen delta carried by index.
import sys, os, json, subprocess, numpy as np, igl
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D); sys.path.insert(0, os.path.join(os.path.dirname(D), 'w2i4_drivers'))
import sa_sculpt as SC5; import sa_finish as FN; _BUILD4 = FN.build_f; FN.build_f = SC5.build_s   # W2I5: final route = W2I4 route + W2I5 sculpt delta
S = FN.C.S; G1 = S + '/w2i/rodin/g1'; OUT = S + '/w2i5/surf'; os.makedirs(OUT, exist_ok=True)
FROZ_D = '/mnt/attach/outputs/racebodies_v35/saurin_final_surface_delta.npz'
def transport_T(V0, V1, F, T0):
    e1 = V0[F[:, 1]] - V0[F[:, 0]]; e2 = V0[F[:, 2]] - V0[F[:, 0]]; E1 = V1[F[:, 1]] - V1[F[:, 0]]; E2 = V1[F[:, 2]] - V1[F[:, 0]]
    Tf = (T0[F[:, 0]] + T0[F[:, 1]] + T0[F[:, 2]]) / 3
    g11 = (e1 * e1).sum(1); g12 = (e1 * e2).sum(1); g22 = (e2 * e2).sum(1); b1 = (Tf * e1).sum(1); b2 = (Tf * e2).sum(1); det = g11 * g22 - g12 ** 2 + 1e-20
    a = (b1 * g22 - b2 * g12) / det; b = (b2 * g11 - b1 * g12) / det; Tn = a[:, None] * E1 + b[:, None] * E2
    T1 = np.zeros_like(T0)
    for k in range(3): np.add.at(T1, F[:, k], Tn)
    return T1
def main():
    Pf = FN.build_f({})[0].astype(np.float64); F0 = FN.F0.astype(np.int64)
    Vu, Fu = igl.upsample(Pf, F0); up0 = np.load(S + '/w2i/rodin/c12/g15up.npz'); V0u = up0['V'].astype(np.float64)
    assert np.array_equal(Fu, up0['F'].astype(np.int64)); reg = dict(np.load(S + '/w2i/rodin/c12/g15reg.npz'))
    N = igl.per_vertex_normals(Vu, Fu); T = transport_T(V0u, Vu, Fu, reg['T'].astype(np.float64))
    T = T - N * (T * N).sum(1)[:, None]; nt = np.linalg.norm(T, axis=1); bad = nt < 1e-6; T[~bad] /= nt[~bad, None]; T[bad] = reg['T'][bad]
    reg['N'] = N.astype(np.float32); reg['T'] = T.astype(np.float32)
    np.savez(OUT + '/fin_up.npz', V=Vu.astype(np.float32), F=Fu.astype(np.int32)); np.savez(OUT + '/fin_reg.npz', **reg)
    sys.path.insert(0, G1); import seedpd
    FAM = reg['FAM']; scaly = (FAM != 6) & (FAM != 7)
    if os.path.exists(OUT + '/fin_seeds.npy'): sd = np.load(OUT + '/fin_seeds.npy')
    else: sd = seedpd.poisson_seeds(Vu.astype(np.float64), reg['R'].astype(np.float64), scaly, np.random.default_rng(7), c=0.50); np.save(OUT + '/fin_seeds.npy', sd)
    r = subprocess.run(['python3', os.path.join(os.path.dirname(D), 'w2i4_drivers', 'g7surfc_moved.py'), S + '/w2i/rodin/c12/g15up.npz', OUT + '/fin_up.npz', OUT + '/fin_reg.npz', OUT + '/fin_surf.npz'], cwd=G1, env=dict(os.environ, SEEDS=OUT + '/fin_seeds.npy'), capture_output=True, text=True)
    print(r.stdout[-400:], r.stderr[-400:]); assert r.returncode == 0
    z = np.load(OUT + '/fin_surf.npz'); d = z['V'].astype(np.float64) - Vu
    np.savez_compressed(OUT + '/saurin_w2i5_surface_delta.npz', d=d.astype(np.float32))
    # before: the frozen (accepted) delta carried by vertex index along the new normals = the stretched old field
    N0 = igl.per_vertex_normals(V0u, Fu); s0 = (np.load(FROZ_D)['d'].astype(np.float64) * N0).sum(1)
    np.savez_compressed(OUT + '/before_surface_delta.npz', d=(s0[:, None] * N).astype(np.float32))
    # geometry-anchored features of g7surfc (eyes, claws / pads) use frozen g7geo positions: report how far the finished base moved there
    sys.path.insert(0, G1); import g7geo as GG
    pts = [c for c, rp, kind in GG.world_claws_pads()[1]] + list(GG.eyes_world()[0])   # (frozen anchor positions; carried by g7surfc_moved)
    tr = __import__('scipy.spatial', fromlist=['cKDTree']).cKDTree(V0u); mv = [float(np.linalg.norm(Vu[tr.query(p)[1]] - V0u[tr.query(p)[1]])) for p in pts]
    info = dict(n_seeds=int(len(sd)), n_vertices=int(len(Vu)), disp_min=float(z['disp'].min()), disp_max=float(z['disp'].max()), disp_rms=float(z['disp'].std()),
                anchor_feature_max_move_cm_carried=max(mv), T_degenerate=int(bad.sum()))
    json.dump(info, open(OUT + '/surface_info.json', 'w'), indent=1); print(info)
if __name__ == '__main__': main()
