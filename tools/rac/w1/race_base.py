"""RAC RM-OT-05C: dedicated race-specific BASE SURFACE / soft-tissue organization for Grask and Gorrund.

Order route (RM-OT-05C §3):
    accepted race skeleton -> accepted 05A architecture (arch_sculpt) -> THIS BASE-SURFACE ORGANIZATION -> composition amount -> surface.

WHY. In the AD-G14 route the "skeleton" surface (-LEAN) is the MPFB body at muscle 0 / weight 0, and every body is that surface plus a
composition tissue field (donor(m, w) - donor_lean). Both layers carry human soft organization: calf belly, deltoid cap, pectoral shelf,
nipples, navel, waist hollow, lumbar hollow, gluteal shelf and fold. 05B remapped only the tissue layer, under a guard that kept the
-LEAN surface, so the human organization of the base could not change. This module REPLACES the soft organization of the whole composed
surface (base + tissue) with authored race anatomy, while the bony support is held.

organize(V, L, J, spec) is applied to EVERY composition state's composed surface (skeleton_envelope.make(base=spec); the spec rides in the
skeleton's meta, so grid / CIB / composition bodies all get it). The raw skeleton (-LEAN) is never rewritten: the composition-infimum bony
envelope still contains the unchanged accepted skeleton, and joints / bone scales / stature are untouched. Operations are relative to the
surface they act on and the limb sections are volume-conserving per segment, so composition keeps setting the amount (AD-G15 firewall).

LIMB SEGMENTS ("limbs"): each segment section r(t, phi) about its own bone axis (t 0 proximal joint -> 1 distal joint; phi 0 anterior,
  +90 lateral, 180 posterior, -90 medial) is rebuilt as bony floor + authored musculature:
    - joint zones t < j0, t > j1 are held exactly (condyles, malleoli, epicondyles, wrist keep their breadths);
    - shaft floor = fb x the narrowest section between them, joined to the held joint sections over tr0 / tr1; "tendon" bands narrow the
      floor to a cord over [t0, t1] (long tendon runs);
    - muscle primitives ("belly": t0 -> peak tp -> t1; "plateau": flat t0..t1) in angular sectors; amplitudes solved so the segment volume
      equals the incoming segment volume (x vol, default 1): the race organization changes WHERE the mass is, never how much.
TRUNK LOFT ("loft"): the trunk (and the buttock shell above the crotch) is re-lofted. First the human relief is removed by non-shrinking
  Taubin smoothing ("taubin" iterations, residual "detail"). Then every section is rebuilt as a periodic cubic through 9 authored control
  radii (0, 22.5 ... 180 deg about the section centre) along r = (u - hip) / (sst - hip). The control curves start from the strongly
  smoothed incoming section, so the bony breadths and depths are the support, and are edited by curve ops over angle ranges:
    - hull (fill concavity: no waist / lumbar hollow);
    - line (straight wall);
    - smooth (low-pass: no pectoral shelf / gluteal apex);
    - bump (authored muscle mass, cm);
    - scale.
  "hold" restores the incoming section at listed bony stations.
GLUTEAL FOLD ("fold"): posterior hip-thigh junction filled to the posterior hull per sagittal column (sacral-hamstring continuity).
YOKE ("yoke"): frontal shoulder outline pulled toward a neck-base -> lateral-arm line within soft-tissue limits (max_in / max_out cm).
TRUNK ADD ("trunk"): authored ridges / masses in sectors (e.g. Grask sternal keel).

Default OFF (spec None): every accepted body rebuilds unchanged."""
import json, numpy as np

ARMK = ("upperarm_l", "upperarm_r", "lowerarm_l", "lowerarm_r", "hand_l", "hand_r", "fingers_l", "fingers_r")
BONES = {"thigh": "thigh", "shank": "calf", "upperarm": "upperarm", "forearm": "lowerarm"}

def _ss(x): x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)

def _smooth(D, F, iters, mask=None):
    n = len(D); E = np.r_[F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]]; E = np.r_[E, E[:, ::-1]]
    deg = np.bincount(E[:, 0], minlength=n).astype(float); deg[deg == 0] = 1
    for _ in range(iters):
        nb = np.zeros_like(D); np.add.at(nb, E[:, 0], D[E[:, 1]]); Dn = 0.5 * D + 0.5 * nb / deg[:, None]
        D = Dn if mask is None else D + (Dn - D) * mask[:, None]
    return D

def _onormals(V, L):
    """outward vertex normals"""
    import race_surface as RS
    n = RS._normals(V, L["F"]); kk = L["keep"].astype(bool)
    return -n if np.mean(np.einsum('ij,ij->i', n[kk], V[kk] - V[kk].mean(0))) < 0 else n

def _wrap(d): return (d + 180.0) % 360.0 - 180.0

def _sector(phi, c, hw):
    d = np.abs(_wrap(phi - c)); return 0.5 * (1 + np.cos(np.pi * np.clip(d / hw, 0, 1)))

def _tprof(t, m):
    if m.get("kind", "belly") == "plateau":
        e = m.get("ramp", 0.06); return _ss((t - m["t0"]) / e) * _ss((m["t1"] - t) / e)
    up = _ss((t - m["t0"]) / max(m["tp"] - m["t0"], 1e-3)); dn = _ss((m["t1"] - t) / max(m["t1"] - m["tp"], 1e-3))
    return np.where(t <= m["tp"], up, dn)

def _table(t, ph, val, w, nt, nph):
    it = np.clip((t * nt).astype(int), 0, nt - 1); ih = np.clip(((ph + 180.0) / 360.0 * nph).astype(int), 0, nph - 1)
    S = np.zeros((nt, nph)); W = np.zeros((nt, nph)); np.add.at(S, (it, ih), val * w); np.add.at(W, (it, ih), w)
    M = np.where(W > 1e-6, S / np.maximum(W, 1e-9), np.nan)
    for j in range(nph):
        c = M[:, j]; ok = ~np.isnan(c)
        M[:, j] = np.interp(np.arange(nt), np.where(ok)[0], c[ok]) if ok.any() else np.nan
    for i in range(nt):
        r = M[i]; ok = ~np.isnan(r)
        M[i] = np.interp(np.arange(nph), np.where(ok)[0], r[ok], period=nph) if ok.any() else 0.0
    return M

def _lookup(M, t, ph, periodic=True):
    nt, nph = M.shape; x = np.clip(t * nt - 0.5, 0, nt - 1); y = (ph + 180.0) / 360.0 * nph - 0.5
    y = y % nph if periodic else np.clip(y, 0, nph - 1)
    x0 = np.floor(x).astype(int); x1 = np.minimum(x0 + 1, nt - 1); fx = x - x0
    y0 = np.floor(y).astype(int) % nph; y1 = (y0 + 1) % nph if periodic else np.minimum(y0 + 1, nph - 1); fy = y - np.floor(y)
    return M[x0, y0] * (1 - fx) * (1 - fy) + M[x1, y0] * fx * (1 - fy) + M[x0, y1] * (1 - fx) * fy + M[x1, y1] * fx * fy

def _tsmooth(M, sg):
    if sg <= 0: return M
    k = np.exp(-0.5 * (np.arange(-3 * int(sg + 1), 3 * int(sg + 1) + 1) / sg) ** 2); k /= k.sum(); p = len(k) // 2
    return np.stack([np.convolve(np.pad(M[:, j], p, mode='edge'), k, 'valid') for j in range(M.shape[1])], 1)

def _frame(J, bn, side):
    h = np.array(J["%s_%s" % (bn, side)][0]); tl = np.array(J["%s_%s" % (bn, side)][1]); ax = tl - h; ln = np.linalg.norm(ax); ax = ax / ln
    ea = np.array([0, 1.0, 0]); ea = ea - (ea @ ax) * ax; ea /= np.linalg.norm(ea)
    lat = np.array([1.0 if (J["thigh_l"][0][0] > 0) == (side == "l") else -1.0, 0, 0])
    el = np.cross(ax, ea); el = el * (1 if el @ lat > 0 else -1)
    return h, ax, ln, ea, el

def _coords(P, h, ax, ln, ea, el):
    t = (P - h) @ ax / ln; tc = np.clip(t, 0, 1); rv = P - (h + np.outer(tc * ln, ax)); r = np.linalg.norm(rv, axis=1)
    u = rv / np.maximum(r, 1e-6)[:, None]; ph = np.degrees(np.arctan2(rv @ el, rv @ ea))
    return t, tc, r, u, ph

NT, NPH = 48, 24

def _muscle(spec, tg, pg):
    Mm = np.zeros((len(tg), len(pg)))
    for m in spec["muscles"]:
        Mm += m.get("a", 1.0) * np.outer(_tprof(tg, m), _sector(pg, m.get("phi", 0.0), m.get("hw", 180.0)))
    return Mm

def limb_base(V, L, J, spec, info):
    """rebuild one limb segment's section as bony floor + authored musculature (both sides); returns displacement"""
    bn = BONES[spec["seg"]]; D = np.zeros_like(V); j0, j1 = spec["j0"], spec["j1"]
    tg = (np.arange(NT) + 0.5) / NT; pg = (np.arange(NPH) + 0.5) / NPH * 360.0 - 180.0
    for side in ("l", "r"):
        w = L["w_%s_%s" % (bn, side)].astype(float) * L["keep"]; m = w > spec.get("wmin", 0.05)
        h, ax, ln, ea, el = _frame(J, bn, side)
        t, tc, r, u, ph = _coords(V[m], h, ax, ln, ea, el)
        RL = _tsmooth(_table(tc, ph, r, w[m] ** 2, NT, NPH), spec.get("tsmooth", 1.0))
        # bony floor: held joint sections at j0 / j1, shaft = fb * narrowest interior lean section, smooth transitions
        a = int(j0 * NT); b = int(j1 * NT) - 1
        shaft = spec.get("fb", 0.8) * RL[a + 1:b].min(0)
        e0, e1 = spec.get("tr0", 0.1), spec.get("tr1", 0.1)
        g0 = _ss((tg - j0) / e0)[:, None]; g1 = _ss((j1 - tg) / e1)[:, None]
        Rb = RL[a][None, :] * (1 - g0) + shaft[None, :] * g0
        Rb = Rb * g1 + RL[b][None, :] * (1 - g1)
        for td in spec.get("tendon", []):         # long tendon run: the floor narrows to a cord over [t0, t1] (k = fractional narrowing)
            tw = _tprof(tg, {"kind": "plateau", "t0": td["t0"], "t1": td["t1"], "ramp": td.get("ramp", 0.08)})[:, None] * _sector(pg, td.get("phi", 0), td.get("hw", 180))[None, :]
            Rb = Rb * (1 - td["k"] * tw)
        band = ((tg >= j0) & (tg <= j1))[:, None]
        Mm = _muscle(spec, tg, pg) * band * (g0 * g1) ** spec.get("mfade", 1.0)    # musculature fades into the held joint transitions
        # amplitude s: sum (Rb + s Mm)^2 = vol * sum RL^2 over the interior band (equal-area bins)
        A = np.sum(Mm ** 2 * band); B = 2 * np.sum(Rb * Mm * band); C = np.sum((Rb ** 2 - spec.get("vol", 1.0) * RL ** 2) * band)
        disc = B * B - 4 * A * C; s = (-B + np.sqrt(max(disc, 0))) / (2 * A) if A > 1e-9 else 0.0; s = max(s, 0.0)
        RA = np.where(band, Rb + s * Mm, RL)
        for fl in spec.get("flats", []):         # straight profile between ta and tb inside a sector (e.g. Grask: no human deltoid cap)
            ia, ib = int(fl["ta"] * NT), min(int(fl["tb"] * NT), NT - 1); x = (tg - tg[ia]) / (tg[ib] - tg[ia])
            lin = RL[ia][None, :] * (1 - x[:, None]) + RL[ib][None, :] * x[:, None] + fl.get("convex", 0.0) * np.sin(np.pi * np.clip(x, 0, 1))[:, None]
            wsec = _sector(pg, fl["phi"], fl["hw"])[None, :] * ((tg >= tg[ia]) & (tg <= tg[ib]))[:, None] * fl.get("strength", 1.0)
            RA = RA + (lin - RA) * wsec
        st = spec.get("strength", 1.0)
        Dt = (RA - RL) * st
        d = _lookup(Dt, tc, ph) * ((t >= 0) & (t <= 1)).astype(float)
        D[m] += (d * w[m])[:, None] * u
        info["%s_%s" % (spec["seg"], side)] = {"amp_cm": float(s), "vol_ratio": float(np.sum(np.where(band, RA, RL) ** 2) / np.sum(RL ** 2)),
                                               "max_in_cm": float(-Dt.min()), "max_out_cm": float(Dt.max())}
    return D

def _trunk_frame(V, L, J):
    hip = (J["thigh_l"][0][2] + J["thigh_r"][0][2]) / 2; sst = (J["clavicle_l"][0][2] + J["clavicle_r"][0][2]) / 2
    armw = np.maximum.reduce([L["w_" + k] for k in ARMK])
    legw = np.maximum.reduce([L["w_" + k] for k in ("calf_l", "calf_r", "foot_l", "foot_r")])
    thw = np.maximum(L["w_thigh_l"], L["w_thigh_r"])
    rz = (V[:, 2] - hip) / (sst - hip)
    trunk = L["keep"] & (armw < 0.05) & (legw < 0.05)
    core = trunk & (thw < 0.5)
    zs = np.linspace(V[core, 2].min(), V[core, 2].max(), 140); cy = []
    for z in zs:
        mm = core & (np.abs(V[:, 2] - z) < 0.8); cy.append(0.5 * (V[mm, 1].max() + V[mm, 1].min()) if mm.sum() > 3 else np.nan)
    cy = np.array(cy); ok = ~np.isnan(cy); cy = np.interp(zs, zs[ok], cy[ok])
    cy = _tsmooth(cy[:, None], 6.0 / (zs[1] - zs[0]))[:, 0]          # section-centre line smoothed over ~6 cm: no centre jumps -> no creases
    c = np.interp(V[:, 2], zs, cy)
    rv = np.stack([V[:, 0], V[:, 1] - c, np.zeros(len(V))], 1); rr = np.linalg.norm(rv, axis=1); u = rv / np.maximum(rr, 1e-6)[:, None]
    ph = np.degrees(np.arctan2(np.abs(V[:, 0]), V[:, 1] - c))
    wt = trunk * np.clip(1 - armw / 0.05, 0, 1)
    return hip, sst, rz, rr, u, ph, wt, thw

def _upper_hull(x, y):
    """upper concave envelope of the profile y(x) (fills hollows), evaluated at x"""
    pts = []
    for xi, yi in zip(x, y):
        while len(pts) >= 2:
            (x1, y1), (x2, y2) = pts[-2], pts[-1]
            if (x2 - x1) * (yi - y1) - (y2 - y1) * (xi - x1) >= 0: pts.pop()
            else: break
        pts.append((xi, yi))
    px, py = np.array(pts).T
    return np.interp(x, px, py)

def trunk_base(V, L, J, ops, info, hold=None):
    hip, sst, rz, rr, u, ph, wt, thw = _trunk_frame(V, L, J)
    D = np.zeros(len(V))
    Dv = np.zeros((len(V), 3))
    for k, op in enumerate(ops):
        z0, z1 = op["r"]; a0, a1 = op["sector"]
        if op["kind"] == "relief":               # human surface relief (pectoral shelf, nipples, navel, abdominal segmentation) smoothed away
            import race_surface as RS
            Dv += RS.trunk_redistribute(V, np.zeros_like(V), L, J, {"r": op["r"], "sector": op["sector"], "sigma_cm": op.get("sigma_cm", 6), "strength": op.get("strength", 1.0), "mode": "radius"})
            continue
        nz, nph = 56, 18
        sel = (wt > 0.5) & (rz > z0 - 0.05) & (rz < z1 + 0.05) & (thw < op.get("max_thigh_w", 0.5))
        zz = np.clip((rz[sel] - z0) / (z1 - z0), 0, 1)
        P = _table(zz, ph[sel] * 2 - 180.0, rr[sel], np.ones(sel.sum()), nz, nph)      # phi 0..180 mapped onto the table's -180..180
        zg = (np.arange(nz) + 0.5) / nz
        P = _tsmooth(P, 1.0)
        T = P.copy(); kind = op["kind"]
        for j in range(nph):
            p = P[:, j]
            if kind == "hull": T[:, j] = _upper_hull(zg, p)
            elif kind == "flat": T[:, j] = p[0] + (p[-1] - p[0]) * zg + op.get("convex", 0.0) * np.sin(np.pi * zg)
            elif kind == "shift": T[:, j] = np.interp(zg - op["dz"] / (z1 - z0), zg, p)
            elif kind == "add": T[:, j] = p + op["cm"] * np.sin(np.pi * np.clip((zg - op.get("p0", 0.0)) / (op.get("p1", 1.0) - op.get("p0", 0.0)), 0, 1)) ** 2
        Dt = (T - P) * op.get("strength", 1.0)
        pgc = (np.arange(nph) + 0.5) / nph * 180.0
        sw = (_ss((pgc - a0) / 15.0 + 0.5) * _ss((a1 - pgc) / 15.0 + 0.5))[None, :]
        zw = (np.sin(np.pi * zg) ** 0.35)[:, None] if op.get("taper", True) else 1.0
        Dt = Dt * sw * zw
        if op.get("vol"):                         # band volume conserved: remove the weighted mean radial change (r-weighted)
            Dt = Dt - (sw * zw) * (np.sum(Dt * P) / max(np.sum(sw * zw * P), 1e-9))
        d = np.zeros(len(V)); d[sel] = _lookup(Dt, zz, ph[sel] * 2 - 180.0, periodic=False) * wt[sel]
        if hold:                                  # pelvic bony stations: damp every op inside the held band
            hz = _ss((rz - hold[0]) / 0.04) * _ss((hold[1] - rz) / 0.04); d *= 1 - hold[2] * hz
        D += d
        info["trunk%d_%s" % (k, kind)] = {"max_out_cm": float(Dt.max()), "max_in_cm": float(-Dt.min())}
    return D[:, None] * u + Dv


def _curve_ops(z, y, ops):
    """authored edits of one section curve y(z) (cm radius at that angle): hull (fill concavity), line (straight), smooth (low-pass),
    bump (+cm Gaussian), scale (factor over a band)"""
    y = y.copy()
    for o in ops:
        a, b = o.get("r", [z[0], z[-1]]); m = (z >= a) & (z <= b); st = o.get("strength", 1.0)
        if not m.any(): continue
        if o["op"] == "hull": t = y.copy(); t[m] = _upper_hull(z[m], y[m])
        elif o["op"] == "line":
            t = y.copy(); t[m] = y[m][0] + (y[m][-1] - y[m][0]) * (z[m] - z[m][0]) / max(z[m][-1] - z[m][0], 1e-6) + o.get("convex", 0.0) * np.sin(np.pi * (z[m] - z[m][0]) / max(z[m][-1] - z[m][0], 1e-6))
        elif o["op"] == "smooth":
            sg = o["sigma"] / (z[1] - z[0]); t = y.copy(); t[m] = _tsmooth(y[:, None], sg)[:, 0][m]
        elif o["op"] == "bump": t = y + o["cm"] * np.exp(-0.5 * ((z - o["at"]) / o["w"]) ** 2); m = np.ones_like(z, bool)
        elif o["op"] == "scale": t = y * o["k"]
        w = np.zeros_like(z); w[m] = 1.0
        if o["op"] not in ("bump",):              # soft band edges
            e = o.get("edge", 0.04); w = _ss((z - a) / e + 0.5) * _ss((b - z) / e + 0.5)
        y = y + (t - y) * w * st
    return y

LOFT_ANG = np.arange(0.0, 180.1, 22.5)        # loft control angles: 0 anterior, 90 lateral (half-breadth), 180 posterior

def _armfade(L, iters=10, k=0.03):
    """1 on the trunk, fading to 0 over ~a few cm around the arm attachment (axilla), so trunk relofting never folds into the arm"""
    armw = np.maximum.reduce([L["w_" + a] for a in ARMK]).astype(float)
    return np.clip(1 - _smooth(armw[:, None], L["F"], iters)[:, 0] / k, 0, 1)

def _crotch(V, L, rz, thw, hip, sst):
    """buttock / proximal-thigh shell above the crotch belongs to the trunk section (the legs are not yet separate there)"""
    mid = L["keep"] & (np.abs(V[:, 0]) < 1.5) & (rz < 0.2) & (rz > -0.6)
    rc = rz[mid].min() + 2.5 / (sst - hip) if mid.any() else 0.0
    return rc, np.where(rz > rc + 0.04, 0.0, np.where(rz > rc, thw * (1 - (rz - rc) / 0.04), thw))

def trunk_loft(V, L, J, spec, info):
    """dedicated trunk surface: every trunk section is re-lofted from authored section curves y_k(r) (radius about the section's own centre
    at 9 control angles, 0 / 22.5 / ... / 180 deg, along r = (u - hip) / (sst - hip)); the section between control angles is a periodic
    cubic through them, so the section SHAPE comes only from the authored curves. Curves start from the strongly smoothed section of the
    surface being organized (the bony breadths / depths are the support) and are edited by authored curve ops, each over an angle range
    ("ang": [a0, a1], default all). The human relief (pectoral shelf, nipples, navel, abdominal segmentation, gluteal fold) survives only
    as the fraction `detail`. `hold` = [[r, sigma], ...] restores the original section at pelvic bony stations."""
    from scipy.ndimage import map_coordinates
    from scipy.interpolate import CubicSpline
    hip, sst, rz, rr, u, ph, wt, thw = _trunk_frame(V, L, J)
    z0, z1 = spec.get("r", [-0.08, 1.06]); nz = 90; nph = 19
    rc, thw = _crotch(V, L, rz, thw, hip, sst)
    z0 = max(z0, rc + 0.02); info["loft_crotch_r"] = float(rc)
    sel = (wt > 0.5) & (thw < 0.5) & (rz > z0 - 0.06) & (rz < z1 + 0.06)
    zg = np.linspace(z0 - 0.06, z1 + 0.06, nz); pg = np.linspace(0, 180, nph)
    zi = np.clip(np.round((rz[sel] - zg[0]) / (zg[1] - zg[0])).astype(int), 0, nz - 1); pi_ = np.clip(np.round(ph[sel] / 10.0).astype(int), 0, nph - 1)
    S = np.zeros((nz, nph)); W = np.zeros((nz, nph)); np.add.at(S, (zi, pi_), rr[sel]); np.add.at(W, (zi, pi_), 1.0)
    RL = np.where(W > 0, S / np.maximum(W, 1e-9), np.nan)
    for j in range(nph):
        c = RL[:, j]; ok = ~np.isnan(c); RL[:, j] = np.interp(np.arange(nz), np.where(ok)[0], c[ok])
    for i in range(nz):
        r_ = RL[i]; ok = ~np.isnan(r_); RL[i] = np.interp(np.arange(nph), np.where(ok)[0], r_[ok])
    dz = zg[1] - zg[0]
    RLs = _tsmooth(RL, 1.0)                                                         # the surface's own section (fine relief kept)
    Y0 = _tsmooth(np.stack([np.interp(LOFT_ANG, pg, RL[i]) for i in range(nz)]), spec.get("zsmooth", 0.04) / dz)   # smoothed support curves
    Y = Y0.copy()
    for o in spec.get("ops", []):
        a0, a1 = o.get("ang", [0, 180]); ka = (LOFT_ANG >= a0 - 1e-6) & (LOFT_ANG <= a1 + 1e-6)
        for k in np.where(ka)[0]: Y[:, k] = _curve_ops(zg, Y[:, k], [o])
    for hz, hw in spec.get("hold", []):
        g = np.exp(-0.5 * ((zg - hz) / hw) ** 2)[:, None]; Y = Y + (Y0 - Y) * g; 
    # periodic cubic through the control radii (mirror about the sagittal plane)
    angs = np.r_[-LOFT_ANG[1:][::-1], LOFT_ANG]; TGT = np.zeros((nz, nph)); BASE = np.zeros((nz, nph))
    for i in range(nz):
        TGT[i] = CubicSpline(angs, np.r_[Y[i, 1:][::-1], Y[i]])(pg); BASE[i] = CubicSpline(angs, np.r_[Y0[i, 1:][::-1], Y0[i]])(pg)
    dk = spec.get("detail", 0.25)
    ci = np.clip((rz - zg[0]) / dz, 0, nz - 1); cj = np.clip(ph / 10.0, 0, nph - 1)
    tg = lambda M: map_coordinates(M, [ci, cj], order=1, mode='nearest')
    rnew = tg(TGT) + dk * (rr - tg(BASE))
    d = rnew - rr
    wz = _ss((rz - z0) / 0.06 + 0.5) * _ss((z1 - rz) / 0.06 + 0.5)
    wv = wt * np.clip(1 - (thw - 0.3) / 0.4, 0, 1) * wz * _armfade(L)
    info["loft"] = {"max_out_cm": float((d * wv).max()), "max_in_cm": float(-(d * wv).min())}
    return (d * wv)[:, None] * u

def gluteal_fold(V, L, J, spec, info):
    """posterior hip-thigh junction: the human gluteal apex / shelf / fold / undercut is relaxed by masked Laplacian smoothing of the
    posterior hip-thigh shell (r0..r1 about the hip level, posterior half), so the sacrum, buttock and hamstring origin read as one
    continuous column. strength in [0, 1] scales the mask."""
    hip, sst, rz, rr, u, ph, wt, thw = _trunk_frame(V, L, J)
    r0, r1 = spec.get("r", [-0.45, 0.12]); st = spec.get("strength", 1.0)
    armw = np.maximum.reduce([L["w_" + k] for k in ARMK]); legw = np.maximum.reduce([L["w_" + k] for k in ("calf_l", "calf_r", "foot_l", "foot_r")])
    cy = np.median(V[L["keep"] & (armw < 0.05) & (np.abs(rz) < 0.1), 1])
    m = L["keep"] * (armw < 0.05) * np.clip(1 - legw / 0.3, 0, 1) * _ss((rz - r0) / 0.06 + 0.5) * _ss((r1 - rz) / 0.06 + 0.5) * _ss((cy - V[:, 1]) / 4.0)
    m = m * np.clip((-_onormals(V, L)[:, 1] - 0.05) / 0.35, 0, 1)                 # posterior-facing shell only (never the crotch / medial thigh)
    m = _smooth(m[:, None].astype(float), L["F"], 4)[:, 0] * st
    D = _smooth(V.copy(), L["F"], spec.get("iters", 60), mask=m) - V       # plain (shrinking) Laplacian: apex in, crease out
    info["fold"] = {"max_cm": float(np.linalg.norm(D, axis=1).max())}
    return D

def yoke(V, L, J, spec, info):
    """frontal shoulder contour (Grask integrated girdle): per side, the superolateral outline between the neck base (x = xn, at the
    shoulder-top height) and the lateral upper arm at `drop` cm below the shoulder joint is replaced by a straight / slightly convex line:
    the human deltoid cap above the line is pressed in, the trapezius concavity below it is filled. Moves only superolateral-facing
    surface (frontal-plane normal toward the line), in x / z; y untouched."""
    n = _onormals(V, L); D = np.zeros_like(V); st = spec.get("strength", 1.0)
    for side in ("l", "r"):
        sh = np.array(J["upperarm_%s" % side][0]); sx = np.sign(sh[0]); el = np.array(J["upperarm_%s" % side][1])
        xn = spec.get("xn", 7.0)
        nk = L["w_neck_01"] + L["w_head"]
        top = V[L["keep"] & (nk < 0.3) & (np.abs(V[:, 0]) < xn + 1.5) & (np.abs(V[:, 0]) > xn - 1.5) & (np.abs(V[:, 1] - sh[1]) < 8), 2]
        zA = np.percentile(top, 95) if len(top) else sh[2] + 6
        zB = sh[2] - spec.get("drop", 18.0)
        armw = L["w_upperarm_%s" % side]; q = L["keep"] & (armw > 0.5) & (np.abs(V[:, 2] - zB) < 1.0)
        xB = (np.abs(V[q, 0]).max() if q.any() else abs(sh[0]) + 5) + spec.get("out", 0.0)
        A = np.array([xn, zA]); B = np.array([xB, zB]); tdir = (B - A) / np.linalg.norm(B - A); nrm = np.array([tdir[1], -tdir[0]])
        if nrm[0] < 0: nrm = -nrm                                                    # outward (superolateral)
        P = np.stack([np.abs(V[:, 0]), V[:, 2]], 1); s_ = (P - A) @ tdir / np.linalg.norm(B - A)
        dist = (P - A) @ nrm - spec.get("convex", 0.0) * np.sin(np.pi * np.clip(s_, 0, 1))
        fn = np.stack([n[:, 0] * sx, n[:, 2]], 1) @ nrm
        w = (V[:, 0] * sx > 0) * _ss(s_ / 0.08 + 0.5) * _ss((1 - s_) / 0.12 + 0.5) * np.clip((fn - 0.2) / 0.4, 0, 1) * L["keep"]
        w = w * np.exp(-0.5 * (np.maximum(np.abs(dist) - 1.0, 0) / spec.get("reach", 4.0)) ** 2)  # only the outline band
        mv = np.clip(-dist * w * st, -spec.get("max_in", 2.5), spec.get("max_out", 2.5))     # soft cap only: the humeral head / acromion is bone
        D[:, 0] += mv * nrm[0] * sx; D[:, 2] += mv * nrm[1]
        info.setdefault("yoke_line", []).append([round(float(xn), 1), round(float(zA), 1), round(float(xB), 1), round(float(zB), 1), round(float(sh[0]), 1), round(float(sh[2]), 1)])
    D = _smooth(D, L["F"], spec.get("smooth", 6))
    info["yoke"] = {"max_cm": float(np.linalg.norm(D, axis=1).max())}
    return D

def _cline(Vsk, L):
    """section centre line of the skeleton surface (y as a function of height; arms and lower legs excluded), smoothed"""
    armw = np.maximum.reduce([L["w_" + k] for k in ARMK]); legw = np.maximum.reduce([L["w_" + k] for k in ("calf_l", "calf_r", "foot_l", "foot_r")])
    m = L["keep"] & (armw < 0.05) & (legw < 0.05); zs = np.linspace(Vsk[m, 2].min(), Vsk[m, 2].max(), 160); cy = []
    for z in zs:
        q = m & (np.abs(Vsk[:, 2] - z) < 0.8); cy.append(0.5 * (Vsk[q, 1].max() + Vsk[q, 1].min()) if q.sum() > 3 else np.nan)
    cy = np.array(cy); ok = ~np.isnan(cy); cy = _tsmooth(np.interp(zs, zs[ok], cy[ok])[:, None], 4.0)[:, 0]
    return np.interp(Vsk[:, 2], zs, cy)

def skeleton_guard(Vn, V0, Vsk, L, J, info, region="trunk", mode="lean"):
    """the organized surface never cuts inside the accepted skeleton surface (-LEAN, Vsk, same frame) where the composition-infimum bony
    envelope / skeletal proxy is read: the trunk, pelvis and proximal thigh (ALPC stations S2...S7). Outward normals of the skeleton
    surface; floor = min(original tissue . n, 0), so a state that was already inside (none at reference) is not pushed out further."""
    if mode == "true":                           # RM-OT-05D: Vsk is the TRUE skeletal floor (true_envelope.floor): whole body, no restoration
        import true_envelope as TE
        n = TE.outward_normals(Vsk, L["F"], L["keep"]); s1 = np.einsum('ij,ij->i', Vn - Vsk, n)
        ext = np.clip(L["w_head"] + L["w_neck_01"] + L["w_hand_l"] + L["w_hand_r"] + L["w_fingers_l"] + L["w_fingers_r"], 0, 1)   # not organized; thin parts (ear) fold an inward offset
        deficit = np.maximum(-s1, 0.0) * L["keep"] * (ext < 0.3); Vn = Vn + deficit[:, None] * n
        info["guard_mode"] = "true-floor"; info["guard_clamped_vertices"] = int((deficit > 1e-3).sum()); info["guard_max_cm"] = float(deficit.max())
        return Vn
    n = _onormals(Vsk, L)
    hip, sst, rz, rr, u, ph, wt, thw = _trunk_frame(Vsk, L, J)
    armw = np.maximum.reduce([L["w_" + k] for k in ARMK]); legw = np.maximum.reduce([L["w_" + k] for k in ("calf_l", "calf_r", "foot_l", "foot_r")])
    tprox = np.zeros(len(Vsk))
    for sd in ("l", "r"):
        h, ax, ln, ea, el = _frame(J, "thigh", sd); t = (Vsk - h) @ ax / ln
        tprox = np.maximum(tprox, L["w_thigh_" + sd] * (1 - _ss((t - 0.3) / 0.1)))
    m = L["keep"] * np.clip(1 - armw / 0.3, 0, 1) * np.clip(1 - legw / 0.3, 0, 1) * np.maximum((rz > -0.6) * (rz < 1.1) * 1.0, tprox)
    m = np.clip(m, 0, 1)
    s0 = np.einsum('ij,ij->i', V0 - Vsk, n); s1 = np.einsum('ij,ij->i', Vn - Vsk, n)
    deficit = np.maximum(np.minimum(s0, 0.0) - s1, 0.0) * m
    Vn = Vn + deficit[:, None] * n
    # horizontal-section guard (the ALPC stations are horizontal plane sections): in the guarded region no vertex comes closer to the
    # skeleton's section centre line than its own skeleton vertex, unless the original composed state already was
    cl = _cline(Vsk, L); rr_s = np.hypot(Vsk[:, 0], Vsk[:, 1] - cl)
    r0 = np.hypot(V0[:, 0], V0[:, 1] - cl); r1 = np.hypot(Vn[:, 0], Vn[:, 1] - cl)
    need = np.minimum(rr_s, r0)                                       # floor: the skeleton radius (or the original if it was inside)
    sc = np.where((r1 < need) & (m > 0), (r1 + (need - r1) * m) / np.maximum(r1, 1e-6), 1.0)
    Vn[:, 0] *= sc; Vn[:, 1] = cl + (Vn[:, 1] - cl) * sc
    # where this composition state was ALREADY inside the skeleton surface (the donor's tissue difference is negative there, e.g. the crest of
    # some grid states), those vertices are the composition-infimum bony readings: they are restored exactly, so the organization neither
    # deepens nor relieves them and the CIB / skeletal-proxy stations stay those of the accepted route
    inside = np.clip(-np.minimum(s0, r0 - rr_s) / 0.3, 0, 1) * m
    Vn = Vn + (V0 - Vn) * inside[:, None]
    info["guard_clamped_vertices"] = int((deficit > 1e-3).sum() + (sc > 1 + 1e-5).sum()); info["guard_max_cm"] = float(max(deficit.max(), ((sc - 1) * r1).max()))
    info["guard_restored_inside_vertices"] = int((inside > 0.5).sum())
    return Vn

def organize(V, L, J, spec, skel=None):
    """the race base surface / tissue organization applied to one surface (a composition state on the race skeleton, in its own frame).
    Relative and volume-conserving per limb segment, so the composition layer keeps setting the amount. Returns (V', info)."""
    if not spec: return V, {}
    V = np.asarray(V, float); info = {}; D = np.zeros_like(V)
    for s in spec.get("limbs", []): D += limb_base(V, L, J, s, info)
    D = _smooth(D * L["keep"][:, None], L["F"], spec.get("smooth", 3))      # limb section fields only (relief removal is never blurred)
    if spec.get("loft"):
        lf = spec["loft"]
        if lf.get("taubin"):                     # human trunk relief (pectoral shelf / fold, nipples, navel, abdominal segmentation) removed by
            import skeleton_envelope as SE       # non-shrinking Taubin smoothing of the trunk surface before it is re-lofted
            hip, sst, rz, rr, u, ph, wt, thw = _trunk_frame(V, L, J); z0, z1 = lf.get("r", [-0.08, 1.06])
            rc, thw = _crotch(V, L, rz, thw, hip, sst); z0 = max(z0, rc + 0.02)
            mw = wt * np.clip(1 - (thw - 0.3) / 0.4, 0, 1) * _ss((rz - z0) / 0.08 + 0.5) * _ss((z1 - rz) / 0.08 + 0.5)
            mw = _smooth(mw[:, None], L["F"], 4)[:, 0] * (1 - lf.get("detail", 0.25)) * _armfade(L)
            D += SE.seam_smooth(V, L["F"], mw, iters=lf["taubin"]) - V
        D += _smooth(trunk_loft(V + D, L, J, lf, info) * L["keep"][:, None], L["F"], lf.get("smooth", 8))   # section-scale field: smoothed
    if spec.get("yoke"): D += yoke(V + D, L, J, spec["yoke"], info)
    if spec.get("fold"): D += gluteal_fold(V + D, L, J, spec["fold"], info)
    if spec.get("trunk"): D += trunk_base(V + D, L, J, spec["trunk"], info, spec.get("hold_r"))
    info["max_disp_cm"] = float(np.linalg.norm(D, axis=1).max())
    Vn = V + D
    if skel is not None and spec.get("guard", True): Vn = skeleton_guard(Vn, V, skel, L, J, info, mode=spec.get("floor", "lean"))
    if spec.get("keep_volume"):                  # RM-OT-05D: the organization moves soft tissue, it does not change the composition amount
        import true_envelope as TE              # the volume lost by removing donor relief is returned as an even layer over the organized trunk / limbs
        keep = L["keep"].astype(bool); ext = np.clip(L["w_head"] + L["w_neck_01"] + L["w_hand_l"] + L["w_hand_r"] + L["w_fingers_l"] + L["w_fingers_r"]
                                                    + L["w_foot_l"] + L["w_foot_r"] + L["w_ball_l"] + L["w_ball_r"], 0, 1)
        armw = np.maximum.reduce([L["w_" + a] for a in ARMK])
        m = _smooth(((ext < 0.3) & keep).astype(float)[:, None], L["F"], 4)[:, 0] * _armfade(L, 14, 0.03) * np.clip(1 - armw / 0.3, 0, 1)
        v0 = TE.signed_volume(V, L["F"], keep)
        for _ in range(3):
            v1 = TE.signed_volume(Vn, L["F"], keep); n = TE.outward_normals(Vn, L["F"], keep)
            Fk = L["F"][keep[L["F"]].all(1)]; fa = 0.5 * np.linalg.norm(np.cross(Vn[Fk[:, 1]] - Vn[Fk[:, 0]], Vn[Fk[:, 2]] - Vn[Fk[:, 0]]), axis=1)
            va = np.zeros(len(Vn)); [np.add.at(va, Fk[:, k], fa / 3) for k in range(3)]
            dv = abs(v0) - abs(v1); A = float((va * m).sum())
            Vn = Vn + (dv / max(A, 1e-6)) * m[:, None] * n
        info["volume_restored_layer_cm"] = float(dv / max(A, 1e-6)); info["volume_ratio_after"] = float(abs(TE.signed_volume(Vn, L["F"], keep)) / abs(v0))
    return Vn, info

apply_base = organize
