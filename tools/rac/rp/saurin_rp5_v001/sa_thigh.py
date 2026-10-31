# sa_thigh.py SRC_DIR LM_DIR OUT_DIR : RP5 Saurin deferred medial / posterior thigh art-debt DIAGNOSIS (order 53976fb §6) -- read-only on the canonical files.
# Region: the W2I4 §5 mid-thigh band (u 66-84 cm, leg-labelled, tail excluded) on SA-M188 and SA-F188 (same base topology). Sector by the W2I4 rule
# (sa_thighrelief.py): per side, quadratic fits of |x|(u) and f(u) over the band; al = (ox + of) / sqrt(2) / |(ox, of)| -> anterolateral (al > 0.35, the
# W2I4 re-modelled face) / medial-posterior (al < -0.35, the faired W2I3 form kept) / transition (|al| <= 0.35).
# Relief = base minus heat-diffused base (implicit (M - t L) solve on the leg sub-mesh, t = sigma^2 / 2, sigma = 1.5 cm; normal component).
# Reported per sector: relief rms / p99 (mm), relief anisotropy (vertical vs horizontal gradient energy, the W2I4 'sector marks' read as horizontal
# banding / vertical streaks), and the surfaced scale delta |d| (SA-M188 only: the canonical delta is defined on the SA-M188 upsample).
# TIMING criterion (recommendation): a defect is corrected BEFORE retopology (on a derived working source) iff its base-level amplitude exceeds the
# production cage's capture tolerance (T-1 p95 1.5 mm / T-2 0.8 mm) -- otherwise the cage cannot carry it and it belongs to the surface / detail layer
# after the cage is established.
import sys, os, json, numpy as np, igl, scipy.sparse as sp
from scipy.sparse.linalg import spsolve
SRC, LMD, OUT = sys.argv[1:4]; os.makedirs(OUT, exist_ok=True)
b = np.load(SRC + '/saurin_w2_final_base.npz'); F = b['f'].astype(np.int64)
lab = np.load(LMD + '/SA-M188_regions.npz')['label']
res = {}
for bid, Vb in (('SA-M188', b['v'].astype(float)), ('SA-F188', np.load(SRC + '/saurin_w2_SA-F188_realization.npz')['v'].astype(float))):
    leg = np.isin(lab, ['leg_xneg', 'leg_xpos']); sub = np.nonzero(leg & (Vb[:, 2] > 55) & (Vb[:, 2] < 95))[0]
    keepF = np.all(np.isin(F, sub), 1); Fs = F[keepF]; sub = np.unique(Fs); mp = -np.ones(len(Vb), int); mp[sub] = np.arange(len(sub)); Fs = mp[Fs]; Vs = Vb[sub]
    Lc = igl.cotmatrix(Vs, Fs); M = igl.massmatrix(Vs, Fs, igl.MASSMATRIX_TYPE_VORONOI); t = 1.5 ** 2 / 2
    S = (M - t * Lc).tocsc(); Sm = np.column_stack([spsolve(S, M @ Vs[:, k]) for k in range(3)])
    N = igl.per_vertex_normals(Vs, Fs); rel = np.einsum('ij,ij->i', Vs - Sm, N)
    band = (Vs[:, 2] > 66) & (Vs[:, 2] < 84); out = {}; al = np.zeros(len(Vs)); side = np.sign(Vs[:, 0])
    for sd in (1, -1):
        m = np.where(band & (side == sd))[0]; A0 = Vs[m]
        cx = np.polyfit(A0[:, 2], np.abs(A0[:, 0]), 2); cf = np.polyfit(A0[:, 2], A0[:, 1], 2)
        ox = np.abs(A0[:, 0]) - np.polyval(cx, A0[:, 2]); of = A0[:, 1] - np.polyval(cf, A0[:, 2]); al[m] = (ox + of) / np.sqrt(2) / (np.hypot(ox, of) + 1e-9)
    G = igl.grad(Vs, Fs); gr = (G @ rel).reshape(3, -1).T                 # per-face relief gradient
    fz = np.c_[np.zeros(len(Fs)), np.zeros(len(Fs)), np.ones(len(Fs))]; vert_e = (gr[:, 2]) ** 2; horiz_e = (gr ** 2).sum(1) - vert_e
    fal = al[Fs].mean(1); fband = band[Fs].all(1)
    for nm, m, fm in (('anterolateral', band & (al > 0.35), fband & (fal > 0.35)), ('transition', band & (np.abs(al) <= 0.35), fband & (np.abs(fal) <= 0.35)),
                      ('medial_posterior', band & (al < -0.35), fband & (fal < -0.35))):
        out[nm] = dict(verts=int(m.sum()), relief_rms_mm=round(float(np.sqrt((rel[m] ** 2).mean()) * 10), 3), relief_p99_mm=round(float(np.percentile(np.abs(rel[m]), 99) * 10), 3),
                       relief_max_mm=round(float(np.abs(rel[m]).max() * 10), 3), gradient_vertical_over_horizontal=round(float(vert_e[fm].mean() / horiz_e[fm].mean()), 3))
    # localized defects: relief extremes in the medial / posterior sector (tear / transition-mark candidates): connected clusters of |rel| > p99.5 of the band
    thr = np.percentile(np.abs(rel[band]), 99.5); hot = band & (al < 0.35) & (np.abs(rel) > thr)
    out['hotspot_threshold_mm'] = round(float(thr * 10), 3); out['hotspot_vertices'] = int(hot.sum())
    hv = sub[hot]; out['hotspot_bbox_cm'] = [np.round(Vb[hv].min(0), 1).tolist(), np.round(Vb[hv].max(0), 1).tolist()] if len(hv) else None
    np.savez_compressed(OUT + '/%s_thigh_relief.npz' % bid, sub=sub, rel=rel.astype(np.float32), al=al.astype(np.float32), Fs=Fs)
    res[bid] = out; print(bid, json.dumps(out))
# surfaced delta in the band (SA-M188): sample the canonical delta at the upsampled vertices nearest the base band vertices (upsample keeps base vertices first)
d = np.load(SRC + '/saurin_w2_final_surface_delta.npz')['d'].astype(float); dm = np.linalg.norm(d, axis=1)
z = np.load(OUT + '/SA-M188_thigh_relief.npz'); sub = z['sub']; al = z['al']; Vb = b['v'].astype(float)
band = (Vb[sub, 2] > 66) & (Vb[sub, 2] < 84)
for nm, m in (('anterolateral', band & (al > 0.35)), ('medial_posterior', band & (al < -0.35))):
    res['SA-M188'][nm]['surface_delta_mean_mm'] = round(float(dm[sub[m]].mean() * 10), 3); res['SA-M188'][nm]['surface_delta_p95_mm'] = round(float(np.percentile(dm[sub[m]], 95) * 10), 3)
mp = res['SA-M188']['medial_posterior']; tr = res['SA-M188']['transition']
res['timing_recommendation'] = dict(
    criterion='correct before retopology iff the base-level defect amplitude exceeds the cage capture tolerance (T-1 p95 1.5 mm, T-2 p95 0.8 mm)',
    medial_posterior_relief_p99_mm=mp['relief_p99_mm'], transition_relief_p99_mm=tr['relief_p99_mm'])
json.dump(res, open(OUT + '/SAURIN_thigh_artdebt_diagnosis.json', 'w'), indent=1)
