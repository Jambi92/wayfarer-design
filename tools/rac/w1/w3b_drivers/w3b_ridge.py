# RAC W3B RM-UF-04 structural-ridge strength: contribution fields, geometric metric, diagnostic multiplier family. NON-CANON diagnostics.
# FAMILIES (accepted TS6 / BROW_INT 5 skull, w3b_head.py): canthus rostralis (dorsolateral rostral edge), supraorbital crest (orbital rim
# contribution), temporal line, jugal / maxillary ridge, occipital transition, mandibular lateral / inferior ridge; reported in addition:
# postorbital plane-change ridge, paired nasal ridges.
# CONTRIBUTION FIELD c_i = (phi(family i absent) - phi(reference)) x head scale: how far the family raises the canonical surface (cm, world).
# DIAGNOSTIC STRENGTH m_i (1 = canonical): the skull level set phi_m = phi_1 + (m - 1)(phi_1 - phi_0), applied to the canonical vertices by
# level-set transfer (w3b_common). For the tent-profile ridges this is exactly the TS6 amplitude x m; for the supraorbital crest (cones
# blended by smooth-min) it scales the crest's contribution. One hidden normalized strength (all m_i equal) is the default family.
# GEOMETRIC METRIC (scales off, naked base): ridge height h = (p - p_base) . n_base, with p_base = implicitly Laplacian-smoothed head surface ((M - 2.0 cm^2 L) p_base = M p:
# forms narrower than ~1.5-2 cm removed) - "ridge height above a local smoothed base surface". Per family: CORE = canonical vertices with c_i >= 0.6 max c_i;
# FLANK = vertices within 1.5 cm of the core with c_i <= 0.15 max c_i and no other family above that level. STRENGTH = mean h(core) - mean h(flank) (cm).
# Companion: PLANE-TRANSITION ANGLE = 90th-percentile angle (deg) between the vertex normal and the smoothed-base normal on core + flank
# (dihedral proxy: how sharply the planes break at the ridge).
import os, sys, json, numpy as np
from scipy.spatial import cKDTree
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import w3b_common as C
FAMS = ['canthal', 'supraorbital', 'temporal', 'jugal', 'occipital', 'mandibular', 'postorbital', 'nasal']
HV = np.where(C.HEADM)[0]
def contrib():
    p = C.W + '/ridge_contrib.npz'
    if os.path.exists(p): z = np.load(p); return {k: z[k] for k in z.files}
    ph1 = C.phi_ref(); Lq = C.L0[HV]; out = {}
    for k in FAMS: out[k] = (C.sdf(Lq, rm={k: 0.0}) - ph1) * C.HS
    np.savez(p, **out); return out
def phi_m(Lq, m):
    """m: dict family -> multiplier. Tent-profile families: their TS6 amplitude x m directly (exact); supraorbital crest (smooth-min cones):
    phi = phi_on + (m_s - 1)(phi_on - phi_off) at the same tent multipliers"""
    rm = {k: v for k, v in m.items() if k != 'supraorbital'}; ms = m.get('supraorbital', 1.0)
    ph1 = C.sdf(Lq, rm=rm)
    if ms == 1.0: return ph1
    return ph1 + (ms - 1.0) * (ph1 - C.sdf(Lq, rm=dict(rm, supraorbital=0.0)))
FAIR = 4       # deformation-field fairing: uniform-Laplacian iterations on the displacement (removes base-mesh transfer folds at the crest front)
_A = None
def fair(P):
    global _A
    import igl
    if _A is None: _A = igl.adjacency_matrix(C.F0).astype(float); _A = (_A, np.asarray(_A.sum(1)).ravel())
    A, deg = _A; Dd = P - C.V0
    for _ in range(FAIR): Dd = 0.5 * Dd + 0.5 * (A @ Dd) / deg[:, None]
    return C.V0 + Dd
def build(m):
    if all(v == 1.0 for v in m.values()): return C.V0.copy()
    return fair(C.level_set_transfer(lambda Q: phi_m(Q, m), along_normal=True))
_sets = None
def sets():
    global _sets
    if _sets is None:
        c = contrib(); P = C.V0[HV]; tr = cKDTree(P); _sets = {}
        for k in FAMS:
            core = np.where(c[k] >= 0.6 * c[k].max())[0]
            near = np.unique(np.concatenate(tr.query_ball_point(P[core], 1.5)))
            tot = sum(c[j] for j in FAMS); flank = near[(c[k][near] <= 0.15 * c[k].max()) & (tot[near] <= 0.15 * c[k].max())]   # no other ridge in the flank
            _sets[k] = (core, flank)
    return _sets
LAM = 2.0      # cm^2: implicit Laplacian smoothing (M - LAM L) Pb = M P removes forms narrower than ~1.5-2 cm (the ridges), keeps the skull planes
def smoothed(Ph, Nh):
    import igl, scipy.sparse.linalg as sla
    from w3b_orbit import head_sub
    Fh = head_sub(); Lc = igl.cotmatrix(Ph, Fh); M = igl.massmatrix(Ph, Fh, igl.MASSMATRIX_TYPE_VORONOI)
    A = (M - LAM * Lc).tocsc(); solve = sla.factorized(A); Pb = np.stack([solve(M @ Ph[:, k]) for k in range(3)], 1)
    Nb = igl.per_vertex_normals(Pb, Fh); return Pb, Nb
def metric(P):
    import igl
    from w3b_orbit import head_sub
    Ph = P[HV]; Nh = igl.per_vertex_normals(Ph, head_sub()); Pb, Nb = smoothed(Ph, Nh)
    h = ((Ph - Pb) * Nb).sum(1); ang = np.degrees(np.arccos(np.clip((Nh * Nb).sum(1), -1, 1))); out = {}
    for k, (core, flank) in sets().items():
        out[k] = {"strength_cm": float(h[core].mean() - h[flank].mean()), "core_h_cm": float(h[core].mean()), "transition_deg_p90": float(np.percentile(ang[np.concatenate([core, flank])], 90)),
                  "n_core": int(len(core))}
    return out, h
# ---- guards ---------------------------------------------------------------------------------------------------------------------------
_bases = {}
def family_base(k):
    """the same canonical skull with family k removed (m_k = 0): the exact local base for the ridge-flank slope"""
    if k not in _bases:
        p = C.W + '/ridge_base_%s.npy' % k
        if os.path.exists(p): _bases[k] = np.load(p)
        else: _bases[k] = build({k: 0.0}).astype(np.float32); np.save(p, _bases[k])
    return _bases[k].astype(float)
def flank_slope(P):
    """p95 angle (deg) between the candidate normal and the family-removed base normal over each family's core + flank: the slope the
    ridge itself adds to the skull planes (razor / fin read when the ridge flanks stand steeper than ~45 deg off the base plane)"""
    import igl
    from w3b_orbit import head_sub
    Fh = head_sub(); Nh = igl.per_vertex_normals(P[HV], Fh); out = {}
    for k, (core, flank) in sets().items():
        Nb = igl.per_vertex_normals(family_base(k)[HV], Fh); idx = np.concatenate([core, flank])
        out[k] = float(np.percentile(np.degrees(np.arccos(np.clip((Nh[idx] * Nb[idx]).sum(1), -1, 1))), 95))
    return out
def eye_visibility(P, elev_deg=0.0, cell=0.05):
    """fraction of the eye surface (FAM 7) visible in a frontal orthographic view (camera on +f, elevated elev_deg): z-buffer on a 0.5 mm grid"""
    from w3b_orbit import fam0
    Ph = P[HV]; e = np.radians(elev_deg); d = np.array([0.0, np.cos(e), np.sin(e)])       # toward the camera
    up = np.array([0.0, -np.sin(e), np.cos(e)]); x = Ph[:, 0]; y = Ph @ up; depth = Ph @ d
    ix = np.floor(x / cell).astype(int); iy = np.floor(y / cell).astype(int); key = ix * 100000 + iy
    order = np.argsort(key); ks = key[order]; ds = depth[order]; uniq, start = np.unique(ks, return_index=True)
    mx = np.maximum.reduceat(ds, start); front = dict(zip(uniq.tolist(), mx.tolist()))
    eye = np.where(fam0()[HV] == 7)[0]
    vis = np.array([depth[i] >= front[key[i]] - 0.08 for i in eye]); return float(vis.mean())
