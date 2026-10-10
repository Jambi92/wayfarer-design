# RAC W3B RM-UF-04 (facial) / RM-UB-08 (body) scale-field engine. NON-CANON diagnostics on copies of the canonical W2 surface.
# Reference = canonical W2 region fields (saurin_w2_regfields.npz: FAM, R spacing, H relief, EL, T, PL, IMB, ATT, TYM) + canonical seeds
# (saurin_w2_seeds.npy, 130,949 upsampled-vertex indices) + canonical scalar relief (normal component of the W2 surface delta).
# Relief formula = W2 generator g7surfc.py exactly (anisotropic size-weighted Voronoi cells, K = 12, groove / dome / imbrication tilt), so
#   relief_new = relief_canon + ATT * (core(new fields, new seeds) - core(canonical fields, canonical seeds))   on the affected vertices,
# which reproduces the canonical surface bit-for-bit outside the tested field and keeps its tympanic / eye / pad extras.
# A TEST changes ONE named field (or field class): size multiplier s on R and relief multiplier r on H, blended by the field's own smooth
# membership weight (indicator diffused over the surface, so the generator's graded transitions are kept; boundaries / roles unchanged).
# SEEDS: canonical seeds are kept wherever the weight is ~0; inside the field they are re-drawn by the W2 variable-radius Poisson-disk
# sampler (seedpd, c = 0.50) from the kept boundary seeds outward, with a FIXED rng per field (seed 7 = canonical generator seed), for every
# test value INCLUDING s = 1 ("reseeded reference"), so neighbouring test values differ only by the requested parameter. Diagnostic seed
# realizations for the seed-stability check use rng 1007 / 2007 (never replacing the canonical 130,949).
# METRICS per field core (weight >= 0.9): characteristic size = median nearest-neighbour seed spacing (cm); relief amplitude =
# p95 - p5 of the pure scale relief (ATT x generator core; tympanic / contact-pad / eye extras excluded) (cm); aspect = amplitude / size; CV of the nearest-neighbour spacing (crowding).
import os, sys, json, numpy as np, igl
from scipy.spatial import cKDTree
from scipy import sparse
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import w3b_common as C
sys.path.insert(0, C.S + '/w2i/rodin/g1'); import seedpd
_Z = {}
def ref():
    if not _Z:
        r = np.load(C.CAN + '/saurin_w2_regfields.npz'); _Z.update({k: r[k] for k in r.files})
        Vu, Fu = igl.upsample(C.V0, C.F0); _Z['Vu'] = Vu; _Z['Fu'] = Fu
        _Z['seeds'] = np.load(C.CAN + '/saurin_w2_seeds.npy').astype(np.int64); _Z['disp'] = C.canon_disp()
        _Z['scaly'] = (_Z['FAM'] != 6) & (_Z['FAM'] != 7)
    return _Z
_A = None
def adj():
    global _A
    if _A is None:
        F = ref()['Fu']; n = len(ref()['Vu']); E = np.vstack([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]])
        A = sparse.coo_matrix((np.ones(len(E), np.float32), (E[:, 0], E[:, 1])), shape=(n, n)).tocsr(); A = ((A + A.T) > 0).astype(np.float32)
        _A = sparse.diags(1 / np.asarray(A.sum(1)).ravel()) @ A
    return _A
def weight(mask, iters=60):
    """smooth membership weight of a field: indicator diffused over the surface (60 uniform-Laplacian iterations ~ 1-2 cm on the
    upsampled mesh), renormalized so the field interior is 1"""
    Z = ref(); w = mask.astype(np.float32); L = adj()
    for _ in range(iters): w = L @ w
    w = np.clip(w / max(np.percentile(w[mask], 90), 1e-6), 0, 1); w[~Z['scaly']] = 0; return w
def core_relief(V, idx, seeds, R, H, EL, T, PL, IMB, FAMs):
    """g7surfc core (before ATT / zero-mean / extras) on vertices idx"""
    SP = V[seeds]; tree = cKDTree(SP); out = np.zeros(len(idx)); jout = np.zeros(len(idx), np.int64); K = 12
    SR = R[seeds]; SH = H[seeds]; SE = EL[seeds]; ST = T[seeds]; SPL = PL[seeds]; SIM = IMB[seeds]
    for i0 in range(0, len(idx), 300000):
        ii = idx[i0:i0 + 300000]; P = V[ii]; _, nb = tree.query(P, k=K)
        Dd = P[:, None, :] - SP[nb]; along = np.einsum('ijk,ijk->ij', Dd, ST[nb]); perp = np.sqrt(np.maximum((Dd * Dd).sum(-1) - along ** 2, 0))
        d = np.sqrt((along / SE[nb]) ** 2 + perp ** 2) / SR[nb]
        o = np.argsort(d, 1); d1 = np.take_along_axis(d, o[:, :1], 1)[:, 0]; d2 = np.take_along_axis(d, o[:, 1:2], 1)[:, 0]
        j = np.take_along_axis(nb, o[:, :1], 1)[:, 0]; a1 = np.take_along_axis(along, o[:, :1], 1)[:, 0]
        w = (d2 - d1) / (d2 + d1 + 1e-9); groove = np.clip(w / 0.16, 0, 1); groove = groove * groove * (3 - 2 * groove)
        dome = 1 - 0.45 * (1 - 0.75 * SPL[j]) * np.clip(d1, 0, 1.4) ** 2
        tilt = 0.38 * SIM[j] * (1 - 0.6 * SPL[j]) * np.clip(a1 / (SR[j] * SE[j]), -1, 1)
        out[i0:i0 + len(ii)] = SH[j] * (groove * (dome + tilt) - 0.35); jout[i0:i0 + len(ii)] = j
    return (out, jout) if RETJ else out
RETJ = False
_CACHE = {}
_AFF = {}
def variant(w, s=1.0, r=1.0, rng_seed=7, V=None, reseed=True):
    """field test: weight w (0..1), size multiplier s, relief multiplier r. Returns (relief, seeds, R, H, affected idx)"""
    Z = ref(); V = Z['Vu'] if V is None else V
    R = Z['R'].astype(np.float64) * (1 + (s - 1) * w); H = Z['H'].astype(np.float64) * (1 + (r - 1) * w)
    S0 = Z['seeds']; zone = (w > 0.02) & Z['scaly']
    if reseed:
        keep = S0[w[S0] <= 0.02]
        new = seedpd.poisson_seeds(V, R, zone, np.random.default_rng(rng_seed), c=0.50, init=keep, ncand=min(int(zone.sum()), 2_500_000))
        seeds = new
    else: seeds = S0
    # affected vertices: the zone plus a halo of 2.5x the local max spacing
    zi = np.where(zone)[0]; halo = 2.5 * max(R[zi].max(), Z['R'][zi].max())
    halo = max(halo, 2.5 * 2.5 * float(Z['R'][zi].max())) if halo <= 2.5 * 2.5 * float(Z['R'][zi].max()) else halo   # one cached halo per field (covers s <= 2.5)
    hk = (id(w), round(halo, 3), V is Z['Vu'])
    if hk not in _AFF:
        bb = (V > V[zi].min(0) - halo).all(1) & (V < V[zi].max(0) + halo).all(1); cand = np.where(bb)[0]     # bounding-box prefilter
        tr = cKDTree(V[zi]); dd, _ = tr.query(V[cand], k=1, distance_upper_bound=halo); _AFF[hk] = cand[np.isfinite(dd) & Z['scaly'][cand]]
    aff = _AFF[hk]
    T = Z['T'].astype(np.float64); EL = Z['EL'].astype(np.float64); PL = Z['PL'].astype(np.float64); IMB = Z['IMB'].astype(np.float64)
    global RETJ
    ck = (int(zone.sum()), float(w.sum()), int(aff[0]) if len(aff) else -1, len(aff))      # canonical core of this field (cached)
    if ck not in _CACHE:
        RETJ = True; _CACHE[ck] = core_relief(Z['Vu'], aff, S0, Z['R'].astype(np.float64), Z['H'].astype(np.float64), EL, T, PL, IMB, Z['FAM']); RETJ = False
    c_old, j_old = _CACHE[ck]
    if not reseed and (np.isscalar(s) and s == 1.0) and V is Z['Vu']:
        c_new = c_old * (H[S0[j_old]] / Z['H'].astype(np.float64)[S0[j_old]])        # relief-only test, same seeds: core is linear in the cell's H (exact)
    else:
        c_new = core_relief(V, aff, seeds, R, H, EL, T, PL, IMB, Z['FAM'])
    rel = Z['disp'].copy(); rel[aff] = Z['disp'][aff] + Z['ATT'][aff] * (c_new - c_old)
    pure = np.full(len(V), np.nan); pure[aff] = Z['ATT'][aff] * c_new          # scale relief only (no tympanic / pad / eye extras)
    return rel, seeds, R, H, aff, pure
def field_metrics(core_mask, rel, seeds, V=None):
    Z = ref(); V = Z['Vu'] if V is None else V
    sd = seeds[core_mask[seeds]]
    if len(sd) < 4: return {"size_cm": None, "relief_cm": None}
    tr = cKDTree(V[seeds]); d, _ = tr.query(V[sd], k=2); nn = d[:, 1]
    a = rel[core_mask]; a = a[np.isfinite(a)]; amp = float(np.percentile(a, 95) - np.percentile(a, 5))      # pass the PURE scale relief
    return {"size_cm": float(np.median(nn)), "size_cv": float(nn.std() / nn.mean()), "relief_cm": amp, "relief_rms": float(a.std()),
            "aspect": float(amp / np.median(nn)), "n_seeds": int(len(sd))}
def bend_radius(core_mask, V=None):
    """functional bend radius proxy: 10th percentile of 1/|k_max| (base-scale curvature, 2-ring) over the field core (cm)"""
    Z = ref(); V = Z['Vu'] if V is None else V
    idx = np.where(core_mask)[0][:: max(1, int(core_mask.sum() // 20000))]
    tr = cKDTree(C.V0); _, bi = tr.query(V[idx])                  # read on the base mesh (scale relief excluded)
    global _K
    if '_K' not in globals():
        _, _, k1, k2, _ = igl.principal_curvature(C.V0, C.F0, radius=3); globals()['_K'] = np.maximum(np.abs(k1), np.abs(k2))
    return float(np.percentile(1 / np.maximum(_K[bi], 1e-6), 10))
