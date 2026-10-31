# sa_thigh_v001.py SRC LM OUT : RP5 full-cage order (ad9cb85) §2 / §22 -- SA_RP5_WORK_v001 = SA_RP5_WORK_v000 (canonical W2I6 base arrays, read-only) + ONE
# bounded medial / posterior mid-thigh art-pass, applied with the SAME vertex weights to SA-M188 and SA-F188 (shared base face list; geometry measured per body).
# Deterministic rule (no randomness):
#   patch weight w = s(u; 63-66 up, 84-87 down) * s(al; 0.40 -> 0.10 full)   (s = smoothstep; al = the W2I4 sector coordinate of the diagnosis: medial /
#     posterior < -0.35, sector-transition band |al| <= 0.35 where the W2I4 marks sit; the re-modelled anterolateral face al > 0.40 is never touched);
#     u in cm on SA-M188; full strength over the diagnosed band u 66-84.
#   (1) sector marks / striations: fine normal smoothing  d1 = w ((H_0.7 V - V) . n), with its sigma-1.5-cm heat-smoothed part removed (d1 <- w (d1 - H_1.5 d1)), 3 passes:
#       only sub-1.5-cm relief changes; the hamstring / adductor FORM, girth and volume stay put.
#   (2) Rodin tear / crumple: seeds = vertices whose normal deviates > 10 deg from the 3-ring averaged normal (folded micro-geometry), inside w > 0.1;
#       mask m = seeds dilated 8 rings, softened 6 passes, x1.6 clipped, x w; there the surface is replaced by a 3D uniform-Laplacian implicit smoothing
#       (I - 12 L_u) V' = V (unfolds the tear tangentially; cotan weights are unreliable on folded triangles).  V_new = (1 - m)(V + d1 n) + m V'.
# Weights (w, m) are computed ONCE on SA-M188 and used for SA-F188 (one identical changed vertex set). Everything outside w > 0 is bit-identical to v000.
import sys, os, json, hashlib, numpy as np, igl, scipy.sparse as sp
from scipy.sparse.linalg import factorized
SRC, LMD, OUT = sys.argv[1:4]; os.makedirs(OUT, exist_ok=True)
b = np.load(SRC + '/saurin_w2_final_base.npz'); F = b['f'].astype(np.int64)
lab = np.load(LMD + '/SA-M188_regions.npz')['label']
SIG, SIG_F, ANG, TU, PASSES = 1.5, 0.7, 10.0, 12.0, 3
def ss(x): x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)
def relief(Vb, sub0=None):
    leg = np.isin(lab, ['leg_xneg', 'leg_xpos']); sub = np.nonzero(leg & (Vb[:, 2] > 55) & (Vb[:, 2] < 95))[0] if sub0 is None else sub0
    keepF = np.all(np.isin(F, sub), 1); Fs = F[keepF]; sub = np.unique(Fs); mp = -np.ones(len(Vb), int); mp[sub] = np.arange(len(sub)); Fs = mp[Fs]; Vs = Vb[sub]
    Lc = igl.cotmatrix(Vs, Fs); M = igl.massmatrix(Vs, Fs, igl.MASSMATRIX_TYPE_VORONOI)
    def heat(sig):
        s = factorized((M - sig ** 2 / 2 * Lc).tocsc()); return lambda X: np.column_stack([s(M @ X[:, k]) for k in range(X.shape[1])]) if X.ndim == 2 else s(M @ X)
    H15 = heat(SIG); Sm = H15(Vs); N = igl.per_vertex_normals(Vs, Fs); rel = np.einsum('ij,ij->i', Vs - Sm, N)
    band = (Vs[:, 2] > 60) & (Vs[:, 2] < 90); al = np.zeros(len(Vs)); side = np.sign(Vs[:, 0]); b66 = (Vs[:, 2] > 66) & (Vs[:, 2] < 84)
    for sd in (1, -1):
        m = np.where(b66 & (side == sd))[0]; A0 = Vs[m]
        cx = np.polyfit(A0[:, 2], np.abs(A0[:, 0]), 2); cf = np.polyfit(A0[:, 2], A0[:, 1], 2)
        mm = np.where(band & (side == sd))[0]; B0 = Vs[mm]
        ox = np.abs(B0[:, 0]) - np.polyval(cx, B0[:, 2]); of = B0[:, 1] - np.polyval(cf, B0[:, 2]); al[mm] = (ox + of) / np.sqrt(2) / (np.hypot(ox, of) + 1e-9)
    n = len(Vs); E = igl.edges(Fs); A = sp.coo_matrix((np.ones(len(E)), (E[:, 0], E[:, 1])), shape=(n, n)); A = (A + A.T).tocsr()
    return dict(sub=sub, Fs=Fs, Vs=Vs, N=N, rel=rel, al=al, H15=H15, Hf=heat(SIG_F), A=A)
def normal_var(N, A):
    Nb = N.copy()
    for _ in range(3): Nb = A @ Nb + Nb
    Nb /= np.linalg.norm(Nb, axis=1)[:, None]; return np.degrees(np.arccos(np.clip((N * Nb).sum(1), -1, 1)))
out = {}; Vnew = {}; W1 = None
for bid, Vb in (('SA-M188', b['v'].astype(float)), ('SA-F188', np.load(SRC + '/saurin_w2_SA-F188_realization.npz')['v'].astype(float))):
    R = relief(Vb, None if W1 is None else W1['sub']); Vs, N, A = R['Vs'], R['N'], R['A']; n = len(Vs); deg = np.asarray(A.sum(1)).ravel()
    if W1 is None:
        u = Vs[:, 2]; w = ss((u - 63) / 3) * ss((87 - u) / 3) * ss((0.40 - R['al']) / 0.30)
        seed = (normal_var(N, A) > ANG) & (w > 0.1); m = seed.astype(float)
        for _ in range(8): m = np.maximum(m, (A @ m) / deg)
        for _ in range(6): m = 0.5 * m + 0.5 * (A @ m) / deg
        W1 = dict(sub=R['sub'], w=w, m=np.clip(m * 1.6, 0, 1) * w, seeds=int(seed.sum()))
    w, mt = W1['w'], W1['m']
    d1 = np.zeros(n); Vt = Vs.copy()
    for _p in range(PASSES):                                  # 3 passes of the fine relief smoothing (form part removed each pass)
        dd_ = w * np.einsum('ij,ij->i', R['Hf'](Vt) - Vt, N); dd_ = w * (dd_ - R['H15'](dd_)); d1 += dd_; Vt = Vs + d1[:, None] * N
    s3 = factorized((sp.identity(n) - TU * (A - sp.diags(deg))).tocsc()); S3 = np.column_stack([s3(Vs[:, k]) for k in range(3)])
    Vn = (1 - mt)[:, None] * (Vs + d1[:, None] * N) + mt[:, None] * S3
    V2 = Vb.copy(); V2[R['sub']] = Vn; Vnew[bid] = V2; pm = w > 0; ch = R['sub'][pm]; dd = np.linalg.norm(Vn - Vs, axis=1)
    out[bid] = dict(changed_vertices=int(pm.sum()), tear_mask_vertices_gt_0p5=int((mt > 0.5).sum()), tear_seed_vertices=W1['seeds'],
                    changed_bbox_cm=[np.round(Vb[ch].min(0), 2).tolist(), np.round(Vb[ch].max(0), 2).tolist()],
                    disp_max_mm=round(float(dd.max() * 10), 3), disp_p99_mm=round(float(np.percentile(dd[pm], 99) * 10), 3), disp_mean_mm=round(float(dd[pm].mean() * 10), 4))
    np.save(OUT + '/%s_changed_idx.npy' % bid, ch.astype(np.int32)); np.savez(OUT + '/SA_RP5_WORK_v001_weights.npz', sub=W1['sub'], w=W1['w'], m=W1['m']); print(bid, json.dumps(out[bid]), flush=True)
np.savez_compressed(OUT + '/SA_RP5_WORK_v001.npz', v_M=Vnew['SA-M188'].astype(np.float32), v_F=Vnew['SA-F188'].astype(np.float32), f=F.astype(np.int32))
h = lambda a: hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()
out['params'] = dict(relief_sigma_cm=SIG, fine_sigma_cm=SIG_F, fine_passes=PASSES, tear_normal_variation_deg=ANG, tear_uniform_smoothing_t_edge2=TU, u_full_band_cm=[66, 84], u_ramps_cm=[[63, 66], [84, 87]],
                     sector='al <= 0.10 full, ramp to 0 at al = 0.40 (anterolateral face untouched)')
out['same_changed_set_c1_c2'] = bool(np.array_equal(np.load(OUT + '/SA-M188_changed_idx.npy'), np.load(OUT + '/SA-F188_changed_idx.npy')))
out['array_sha256'] = {'v_M': h(Vnew['SA-M188'].astype(np.float32)), 'v_F': h(Vnew['SA-F188'].astype(np.float32)), 'f': h(F.astype(np.int32))}
json.dump(out, open(OUT + '/SA_RP5_WORK_v001_apply.json', 'w'), indent=1)
