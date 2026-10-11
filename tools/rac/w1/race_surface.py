"""RAC RM-OT-05B: race-specific MUSCULOSKELETAL / SURFACE-ANATOMY stage for Grask and Gorrund.

Order position (RM-OT-05B §7):  accepted skeleton -> 05A architecture (arch_sculpt) -> THIS STAGE -> composition (tissue amount) -> surface.

What it changes: WHERE the soft-tissue field sits, never how much of it there is. The composition layer of the AD-G14 route is a per-vertex
tissue field T = donor(m, w) - donor_lean (skeleton_envelope.make). This stage re-maps that field's topology over the race skeleton:
  * LIMB BELLY / TENDON REMAP ("limbs"): along a limb segment the radial tissue thickness profile m(t, theta) is resampled from a source
    position t_src = map(t) (pchip), so muscle bellies move (e.g. Grask calf / forearm bellies high and short with a long distal tendon run),
    or a profile is low-passed along the segment (Gorrund columnar thigh / shank, no human calf bulge). Each remap is renormalized per
    angular sector so the segment's tissue VOLUME (integral of 2 r m dt over the sector) is conserved.
  * TRUNK RELIEF REDISTRIBUTION ("trunk"): within a trunk band (height range in r = (u - hip) / (sst - hip), angular sector about the section
    centre) the radial tissue thickness is low-passed along height with a Gaussian of sigma cm and renormalized to the band's mean, so a local
    human relief feature (gluteal shelf, lumbar hollow, abdominal bulge, deltoid cap) is redistributed over its own region at constant volume.
Because the same remap is applied to every composition state's tissue field (grid, CIB, composition bodies: the spec rides in the skeleton's
meta), the composition system stays free to vary amount independently and AD-G15 holds: no step adds or removes tissue volume.
Default OFF (spec None): every accepted body rebuilds unchanged."""
import json, numpy as np

def _ss(x): x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)

def _smooth(D, F, iters):
    n = len(D); E = np.r_[F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]]; E = np.r_[E, E[:, ::-1]]
    deg = np.bincount(E[:, 0], minlength=n).astype(float); deg[deg == 0] = 1
    for _ in range(iters):
        nb = np.zeros_like(D); np.add.at(nb, E[:, 0], D[E[:, 1]]); D = 0.5 * D + 0.5 * nb / deg[:, None]
    return D

def _pchip(xn, yn, x):
    from scipy.interpolate import PchipInterpolator as P
    return P(xn, yn)(np.clip(x, xn[0], xn[-1]))

def _bin2(t, th, val, w, nt, nth):
    """weighted mean table over (t in [0,1], theta in [-pi, pi)); empty bins filled along t then theta"""
    it = np.clip((t * nt).astype(int), 0, nt - 1); ih = np.clip(((th + np.pi) / (2 * np.pi) * nth).astype(int), 0, nth - 1)
    S = np.zeros((nt, nth)); W = np.zeros((nt, nth)); np.add.at(S, (it, ih), val * w); np.add.at(W, (it, ih), w)
    M = np.where(W > 1e-6, S / np.maximum(W, 1e-9), np.nan)
    for j in range(nth):
        c = M[:, j]; ok = ~np.isnan(c)
        M[:, j] = np.interp(np.arange(nt), np.where(ok)[0], c[ok]) if ok.any() else np.nan
    for i in range(nt):
        r = M[i]; ok = ~np.isnan(r)
        M[i] = np.interp(np.arange(nth), np.where(ok)[0], r[ok], period=nth) if ok.any() else 0.0
    return M

def _lookup(M, t, th):
    nt, nth = M.shape; x = np.clip(t * nt - 0.5, 0, nt - 1); y = ((th + np.pi) / (2 * np.pi) * nth - 0.5) % nth
    x0 = np.floor(x).astype(int); x1 = np.minimum(x0 + 1, nt - 1); fx = x - x0
    y0 = np.floor(y).astype(int) % nth; y1 = (y0 + 1) % nth; fy = y - np.floor(y)
    return (M[x0, y0] * (1 - fx) * (1 - fy) + M[x1, y0] * fx * (1 - fy) + M[x0, y1] * (1 - fx) * fy + M[x1, y1] * fx * fy)

BONES = {"thigh": "thigh", "shank": "calf", "upperarm": "upperarm", "forearm": "lowerarm"}

def limb_remap(V, T, L, J, spec):
    """spec: {"seg": thigh|shank|upperarm|forearm, "map": [[t_target...], [t_source...]] or "lowpass": sigma_t, "t_range": [a, b]}"""
    bn = BONES[spec["seg"]]; dT = np.zeros_like(T); info = {}
    for side in ("l", "r"):
        w = L["w_%s_%s" % (bn, side)].astype(float) * L["keep"]; m = w > 0.05
        h = np.array(J["%s_%s" % (bn, side)][0]); tl = np.array(J["%s_%s" % (bn, side)][1]); ax = tl - h; ln = np.linalg.norm(ax); ax /= ln
        P = V[m]; t = np.clip((P - h) @ ax / ln, 0, 1); c = h + np.outer(t * ln, ax); rv = P - c; r = np.linalg.norm(rv, axis=1); u = rv / np.maximum(r, 1e-6)[:, None]
        ex = np.array([1.0, 0, 0]); ex -= (ex @ ax) * ax; ex /= np.linalg.norm(ex); ey = np.cross(ax, ex)
        th = np.arctan2(rv @ ey, rv @ ex)
        rad = spec.get("mode") == "radius"                                        # base-surface route: remap the full section radius
        mag = r if rad else np.einsum('ij,ij->i', T[m], u)                        # radial tissue thickness (or section radius)
        nt, nth = 48, 16; M = _bin2(t, th, mag, w[m], nt, nth); R = np.zeros_like(M) if rad else _bin2(t, th, r, w[m], nt, nth)
        tg = (np.arange(nt) + 0.5) / nt
        if "map" in spec: src = _pchip(np.asarray(spec["map"][0], float), np.asarray(spec["map"][1], float), tg)
        else: src = tg
        M2 = np.stack([np.interp(src, tg, M[:, j]) for j in range(nth)], 1)
        if spec.get("lowpass"):
            sg = spec["lowpass"] * nt; k = np.exp(-0.5 * (np.arange(-3 * int(sg + 1), 3 * int(sg + 1) + 1) / max(sg, 1e-3)) ** 2); k /= k.sum()
            pad = len(k) // 2; M2 = np.stack([np.convolve(np.pad(M2[:, j], pad, mode='edge'), k, 'valid') for j in range(nth)], 1)
        a, b = spec.get("t_range", [0.0, 1.0]); band = (tg >= a) & (tg <= b)
        # volume conservation per angular sector over the band: integral (2 R m + m^2) dt equal before and after
        for j in range(nth):
            v0 = np.sum((2 * R[band, j] * M[band, j] + M[band, j] ** 2)); v1 = np.sum((2 * R[band, j] * M2[band, j] + M2[band, j] ** 2))
            if v1 > 1e-6 and v0 > 0: M2[band, j] *= np.sqrt(v0 / v1) if v0 / v1 > 0 else 1.0
        M2[~band] = M[~band]
        wb = _ss((t - a) / 0.04 + 1.0) * _ss((b - t) / 0.04 + 1.0) if (a > 0 or b < 1) else np.ones_like(t)
        new = mag + (_lookup(M2, t, th) - _lookup(M, t, th)) * wb
        dT[m] += ((new - mag) * w[m])[:, None] * u
        info[side] = {"vol_ratio": float(np.sum(2 * R * M2 + M2 ** 2) / max(np.sum(2 * R * M + M ** 2), 1e-9))}
    return dT, info

def trunk_redistribute(V, T, L, J, spec):
    """spec: {"r": [lo, hi], "sector": [deg_from, deg_to] (0 = anterior +y, 90 = left +x, 180 = posterior), "sigma_cm": s}"""
    hip = (J["thigh_l"][0][2] + J["thigh_r"][0][2]) / 2; sst = (J["clavicle_l"][0][2] + J["clavicle_r"][0][2]) / 2
    armw = np.maximum.reduce([L["w_" + k] for k in ("upperarm_l", "upperarm_r", "lowerarm_l", "lowerarm_r", "hand_l", "hand_r")])
    legw = np.maximum.reduce([L["w_" + k] for k in ("calf_l", "calf_r", "foot_l", "foot_r")])
    r = (V[:, 2] - hip) / (sst - hip); lo, hi = spec["r"]
    wz = _ss((r - lo) / 0.06) * _ss((hi - r) / 0.06)
    trunk = L["keep"] & (armw < 0.05) & (legw < 0.2)
    zs = np.linspace(V[trunk, 2].min(), V[trunk, 2].max(), 120); cy = []
    for z in zs:
        mm = trunk & (np.abs(V[:, 2] - z) < 0.8); cy.append(0.5 * (V[mm, 1].max() + V[mm, 1].min()) if mm.sum() > 3 else np.nan)
    cy = np.array(cy); ok = ~np.isnan(cy); c = np.interp(V[:, 2], zs[ok], cy[ok])
    rv = np.stack([V[:, 0], V[:, 1] - c, np.zeros(len(V))], 1); rr = np.linalg.norm(rv, axis=1); u = rv / np.maximum(rr, 1e-6)[:, None]
    ang = np.degrees(np.arctan2(np.abs(V[:, 0]), V[:, 1] - c))                 # 0 anterior, 90 lateral, 180 posterior (both sides)
    a0, a1 = spec["sector"]; wa = _ss((ang - a0) / 12.0 + 0.5) * _ss((a1 - ang) / 12.0 + 0.5)
    w = wz * wa * trunk * np.clip(1 - armw / 0.05, 0, 1)
    mag = rr if spec.get("mode") == "radius" else np.einsum('ij,ij->i', T, u)
    # continuous mesh-scalar relief flattening (no binning): m_s = mesh-Laplacian-smoothed magnitude; delta = strength * w * (m_s - m),
    # then the region's weighted mean delta is removed so the band volume is conserved
    it = spec.get("iters", int(2 * (spec.get("sigma_cm", 6) / 1.7) ** 2))
    ms = _smooth(mag[:, None], L["F"], it)[:, 0]
    w = _smooth(w[:, None], L["F"], 6)[:, 0]
    delta = spec.get("strength", 1.0) * w * (ms - mag)
    delta = delta - w * (np.sum(delta * w) / max(np.sum(w * w), 1e-9))
    dT = delta[:, None] * u
    return dT

def _normals(V, F):
    n = np.zeros_like(V); fn = np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]])
    for k in range(3): np.add.at(n, F[:, k], fn)
    return n / np.maximum(np.linalg.norm(n, axis=1), 1e-9)[:, None]

def apply(V, T, L, J, spec):
    """V: lean skeleton surface in the output frame; T: tissue field; J: joints in the output frame. Returns (T', info)"""
    if not spec: return T, {}
    T = np.asarray(T, float).copy(); info = {}
    if spec.get("relief"):        # race-specific BASE-SURFACE route (RM-OT-05B §7): the skeleton-envelope surface's own soft relief (surface minus
        import skeleton_envelope as SE   # a non-shrinking Taubin core) is remapped together with the composition tissue; the skeleton is not written
        core = SE.seam_smooth(V, L["F"], L["keep"].astype(float), iters=spec["relief"])
        R0 = V - core; T0 = T; T = R0 + T0
    dT = np.zeros_like(T)
    for i, s in enumerate(spec.get("limbs", [])):
        d, inf = limb_remap(V, T, L, J, s); dT += d; info["limb%d_%s" % (i, s["seg"])] = inf
    for s in spec.get("trunk", []): dT += trunk_redistribute(V, T, L, J, s)
    dT = _smooth(dT * L["keep"][:, None], L["F"], spec.get("smooth", 1))
    # RM-OT-05C provenance note (behaviour deliberately left unchanged so the 05B evidence reproduces): _normals() returns INWARD normals
    # on this mesh (negative signed volume; the chest-front normal points -y). The guard below therefore stops tissue moving further
    # OUTWARD than min(original, 0) and does not stop inward cuts. It is the opposite of the intent stated next. race_base.skeleton_guard
    # (05C) uses outward normals.
    # SKELETON GUARD: the surface layer never cuts into the skeletal-envelope surface (so the CIB / skeletal proxy, which are minima over
    # composition states that include the bare skeleton, read the 05A skeleton unchanged): (tissue') . n >= min(tissue . n, 0)
    Tb = T0 if spec.get("relief") else T
    n = _normals(V, L["F"]); s0 = np.einsum('ij,ij->i', Tb, n); s1 = np.einsum('ij,ij->i', Tb + dT, n)
    floor = np.minimum(s0, 0.0); deficit = np.maximum(floor - s1, 0.0); dT = dT + deficit[:, None] * n
    info["guard_clamped_vertices"] = int((deficit > 1e-4).sum()); info["guard_max_cm"] = float(deficit.max())
    if spec.get("relief"): return T0 + dT, info
    return T + dT, info
