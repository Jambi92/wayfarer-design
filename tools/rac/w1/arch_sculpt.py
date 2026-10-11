"""RAC RM-OT-05A: race-specific BODY-ARCHITECTURE SCULPT on the skeletal-envelope surface (AD-G14 skeleton, before soft tissue).

The accepted W2 Grask / Gorrund routes re-proportion and re-thicken the MPFB human surface; RM-OT-05 showed that this cannot make the authored
non-human architecture legible (readability FAIL). The author authorized (RM-OT-05A §1, §3) reconstructing race-specific girdle, pelvis, axial
chain, joint and limb-transition geometry beyond the MPFB human surface. This module does that as smooth, low-strain displacement fields on the
skeleton surface, so soft tissue is added afterwards unchanged by skeleton_envelope.make (composition firewall AD-G15 holds by construction)
and every grid / CIB / skeletal-proxy / ALPC validator measures the rebuilt skeleton.

Field families (all in the body's own joint frames, so they transport across stature and pose: rest and R-6 are sculpted separately):
  1. TRUNK VERTICAL REDISTRIBUTION ("vz"): monotone remap of trunk height between the hip-joint level and the shoulder line, both held fixed
     (stature, hip-joint height, shoulder height, arm and leg lengths unchanged). Nodes are r = (u - hip) / (sst - hip); "vz" = target r of
     each node. Spine joints follow the same remap. Arms and free legs are excluded by weight.
  2. TRUNK SECTION SHAPING ("trunk"): per-height factors about each trunk section's own centre (as skeleton_envelope.trunk_sculpt) with
     separate anterior / posterior depth (ka, kp) and separate anterior-half / posterior-half breadth (kba, kbp) so section SHAPE changes
     (e.g. posterolaterally broad ribcage), not only its size.
  3. LIMB CHAIN SECTION SHAPING ("leg", "arm"): along each limb chain (leg: hip 0 - knee 1 - ankle 2 - ball 3; arm: shoulder 0 - elbow 1 -
     wrist 2 - knuckles 3) per-station factors on the four half-sections about the bone axis: lateral, medial, anterior, posterior
     (klat, kmed, kant, kpost). This shapes joints (condylar / epicondylar / malleolar breadth), shaft cross-section and taper, i.e. joint
     STRUCTURE, not uniform circumference. Blended over bones by skin weight; never moves joint centres.
The displacement field is mesh-smoothed (as trunk_sculpt) so no crease forms at weight seams."""
import json, numpy as np

ARMK = ("upperarm_l", "upperarm_r", "lowerarm_l", "lowerarm_r", "hand_l", "hand_r", "fingers_l", "fingers_r")
LEGK = ("thigh_l", "thigh_r", "calf_l", "calf_r", "foot_l", "foot_r", "ball_l", "ball_r")

def _ss(x): x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)

def _edges(F, n):
    E = np.r_[F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]]; E = np.r_[E, E[:, ::-1]]
    deg = np.bincount(E[:, 0], minlength=n).astype(float); deg[deg == 0] = 1
    return E, deg

def _smooth(D, F, iters, mask=None):
    E, deg = _edges(F, len(D))
    for _ in range(iters):
        nb = np.zeros_like(D); np.add.at(nb, E[:, 0], D[E[:, 1]]); Dn = 0.5 * D + 0.5 * nb / deg[:, None]
        D = Dn if mask is None else D + (Dn - D) * mask[:, None]
    return D

def _levels(L):
    J = json.loads(str(L["joints"])); hip = (J["thigh_l"][0][2] + J["thigh_r"][0][2]) / 2
    sst = (J["clavicle_l"][0][2] + J["clavicle_r"][0][2]) / 2
    return J, hip, sst

def _trunk_w(V, L, hip, sst, lo=-0.25, hi=1.15):
    armw = np.maximum.reduce([L["w_" + k] for k in ARMK]); legw = np.maximum.reduce([L["w_" + k] for k in LEGK[:6]])
    r = (V[:, 2] - hip) / (sst - hip)
    wt = np.clip(1 - armw / 0.3, 0, 1) * np.clip(1 - np.maximum(legw - 0.5, 0) / 0.3, 0, 1) * L["keep"] * (r > lo) * (r < hi)
    return r, wt, armw, legw

def _centres(V, L, armw, legw, nz=140):
    trunk = L["keep"] & (armw < 0.05) & (legw < 0.5)
    zs = np.linspace(V[trunk, 2].min(), V[trunk, 2].max(), nz); cy = []
    for z in zs:
        m = trunk & (np.abs(V[:, 2] - z) < 0.8)
        cy.append(0.5 * (V[m, 1].max() + V[m, 1].min()) if m.sum() > 3 else np.nan)
    cy = np.array(cy); ok = ~np.isnan(cy)
    return np.interp(V[:, 2], zs[ok], cy[ok])

def _pchip(xn, yn, x):
    from scipy.interpolate import PchipInterpolator as P
    return P(xn, yn)(np.clip(x, xn[0], xn[-1]))

def vz_remap(V, L, spec):
    """trunk vertical redistribution; returns (V', joint z-map function)"""
    J, hip, sst = _levels(L); r, wt, armw, legw = _trunk_w(V, L, hip, sst, lo=-0.05, hi=1.02)
    rn = np.asarray(spec["r"], float); tn = np.asarray(spec["to"], float)        # monotone, rn[0] = tn[0] = 0, rn[-1] = tn[-1] = 1
    rr = np.clip(r, 0, 1); r2 = _pchip(rn, tn, rr); dz = (r2 - rr) * (sst - hip)
    wv = np.clip(1 - armw / 0.15, 0, 1) * L["keep"] * ((r > 0) & (r < 1)) * np.clip(1 - legw / 0.5, 0, 1)
    D = np.zeros_like(V); D[:, 2] = dz * wv
    D = _smooth(D, L["F"], spec.get("smooth", 30))
    zmap = lambda z: z + (_pchip(rn, tn, np.clip((z - hip) / (sst - hip), 0, 1)) - np.clip((z - hip) / (sst - hip), 0, 1)) * (sst - hip) * ((z > hip) & (z < sst))
    return V + D, zmap

def trunk_shape(V, L, spec):
    J, hip, sst = _levels(L); r, wt, armw, legw = _trunk_w(V, L, hip, sst)
    rn = np.asarray(spec["r"], float); F = L["F"]; it = spec.get("smooth", 20)
    if spec.get("confine_legs", True): wt = wt * np.clip(1 - legw / 0.5, 0, 1)
    wt = _smooth(wt[:, None], F, it)[:, 0]                   # smooth the WEIGHT (a scalar), never the radial displacement (it cancels)
    ip = lambda k: 1 + (_pchip(rn, np.asarray(spec.get(k, [1.0] * len(rn)), float), r) - 1) * wt
    c = _centres(V, L, armw, legw)
    ka, kp, kba, kbp = ip("ka"), ip("kp"), ip("kba"), ip("kbp")
    ant = _ss((V[:, 1] - c) / 6.0 + 0.5)                     # 1 anterior, 0 posterior, smooth across the coronal plane
    kb = kba * ant + kbp * (1 - ant)
    X = V.copy(); X[:, 0] = V[:, 0] * kb
    X[:, 1] = c + (V[:, 1] - c) * np.where(V[:, 1] >= c, ka, kp)
    return X

CHAINS = {"leg": (("thigh", "calf", "foot", "ball"), ("thigh", "calf", "foot", "ball")),
          "arm": (("upperarm", "lowerarm", "hand", "fingers"), ("upperarm", "lowerarm", "hand", None))}

def limb_shape(V, L, chain, spec):
    """per-station half-section factors along a limb chain (s = bone index + t); the factor FIELDS (scalars) are mesh-smoothed, then the
    section displacement is evaluated in each bone's frame and blended by skin weight (radial displacements are never smoothed: they cancel)"""
    J = json.loads(str(L["joints"])); wk, bones = CHAINS[chain]; sn = np.asarray(spec["s"], float); F = L["F"]
    prof = {k: np.asarray(spec.get(k, [1.0] * len(sn)), float) for k in ("klat", "kmed", "kant", "kpost")}
    n = len(V); recs = []; K = np.zeros((n, 4)); Wt = np.zeros(n)
    sgn = 1.0 if J["thigh_l"][0][0] > 0 else -1.0
    for side in ("l", "r"):
        sx = sgn if side == "l" else -sgn                        # lateral = +x for left limbs (MPFB: thigh_l at +x)
        for i, (wn, bn) in enumerate(zip(wk, bones)):
            bn = bn or "hand"
            w = L["w_%s_%s" % (wn, side)].astype(float); m = w > 1e-4
            if not m.any(): continue
            h = np.array(J["%s_%s" % (bn, side)][0]); tl = np.array(J["%s_%s" % (bn, side)][1]); ax = tl - h; ln = np.linalg.norm(ax); ax /= ln
            P = V[m]; t = np.clip((P - h) @ ax / ln, 0, 1.0); s = i + t
            if wn == "fingers": s = np.full(len(P), 3.0)
            ex = np.array([sx, 0.0, 0.0]); ex = ex - (ex @ ax) * ax; ex /= np.linalg.norm(ex)
            ey = np.cross(ax, ex); ey = ey * (np.sign(ey[1]) if abs(ey[1]) > 0.5 else np.sign(ey[2]))   # anterior +y; foot: dorsal +z
            K[m] += w[m, None] * np.stack([_pchip(sn, prof[k], s) for k in ("klat", "kmed", "kant", "kpost")], 1); Wt[m] += w[m]
            recs.append((m, w, h, ax, ln, ex, ey, wn in ("foot", "ball")))
    K = np.where(Wt[:, None] > 1e-6, K / np.maximum(Wt, 1e-6)[:, None], 1.0)
    Wt = np.clip(Wt, 0, 1) * L["keep"]
    it = spec.get("smooth", 12)
    K = 1 + _smooth((K - 1) * Wt[:, None], F, it) / np.maximum(_smooth(Wt[:, None], F, it), 1e-3)  # weight-normalized factor smoothing
    Ws = _smooth(Wt[:, None], F, it)[:, 0]
    D = np.zeros_like(V)
    for m, w, h, ax, ln, ex, ey, plant in recs:
        P = V[m]; t = np.clip((P - h) @ ax / ln, 0, 1.0); rv = P - (h + np.outer(t * ln, ax)); a = rv @ ex; b = rv @ ey; k = K[m]
        kl = np.where(a >= 0, k[:, 0], k[:, 1]); ka = np.where(b >= 0, k[:, 2], k[:, 3])
        if plant: ka = np.where(b < 0, 1.0, ka)                 # foot: the plantar half never moves (sole, ground contact and stature held)
        D[m] += (np.outer(a * (kl - 1), ex) + np.outer(b * (ka - 1), ey)) * (w[m] / np.maximum(Wt[m], 1e-6) * np.minimum(Ws[m], 1))[:, None] * L["keep"][m, None]
    return V + D

SEG = {"arm": ("upperarm", "lowerarm"), "leg": ("thigh", "calf")}
def seg_shift(V, L, J, chain, delta, smooth=8):
    """within-limb segment redistribution at held limb length: the middle joint (elbow / knee) moves delta cm toward the proximal joint;
    the proximal segment shortens and the distal segment lengthens by delta (shoulder / hip and wrist / ankle fixed). Joints updated."""
    up, lo = SEG[chain]; D = np.zeros_like(V); J = dict(J)
    for side in ("l", "r"):
        h, e = np.array(J["%s_%s" % (up, side)][0]), np.array(J["%s_%s" % (up, side)][1]); ax = (e - h) / np.linalg.norm(e - h)
        e2, w2 = np.array(J["%s_%s" % (lo, side)][0]), np.array(J["%s_%s" % (lo, side)][1])
        wu = L["w_%s_%s" % (up, side)].astype(float); wl = L["w_%s_%s" % (lo, side)].astype(float)
        tu = np.clip((V - h) @ ax / np.linalg.norm(e - h), 0, 1); al = (w2 - e2) / np.linalg.norm(w2 - e2); tl = np.clip((V - e2) @ al / np.linalg.norm(w2 - e2), 0, 1)
        mag = wu * tu + wl * (1 - tl)
        D += np.outer(-delta * mag, ax)
        ne = (e - delta * ax).tolist(); J["%s_%s" % (up, side)] = [h.tolist(), ne]; J["%s_%s" % (lo, side)] = [ne, w2.tolist()]
    return V + _smooth(D * L["keep"][:, None], L["F"], smooth), J

def distal_scale(V, L, J, spec):
    """hand: scale about the wrist (3D); foot: horizontal (x, y) scale about the ankle's vertical line (ankle and sole heights held)"""
    D = np.zeros_like(V)
    for side in ("l", "r"):
        if spec.get("hand"):
            w = np.clip(L["w_hand_%s" % side] + L["w_fingers_%s" % side], 0, 1); c = np.array(J["hand_%s" % side][0])
            D += (V - c) * (spec["hand"] - 1) * w[:, None]
        if spec.get("foot"):
            w = np.clip(L["w_foot_%s" % side] + L["w_ball_%s" % side], 0, 1); c = np.array(J["foot_%s" % side][0])
            d = (V - c) * (spec["foot"] - 1); d[:, 2] = 0; D += d * w[:, None]
    return V + _smooth(D * L["keep"][:, None], L["F"], 4)

def girdle_top(V, L, J, spec):
    """superior shoulder contour (GR-G5 open girdle-neck transition / GO-G4 broad neck base): vertices above the shoulder-joint level and
    lateral of the neck base move vertically by dz(x) = drop * ramp(|x| from the neck base to the acromion); joints are not moved."""
    D = np.zeros_like(V); x0 = spec.get("x0", 6.0)
    for side, sg in (("l", 1.0), ("r", -1.0)):
        sh = np.array(J["upperarm_%s" % side][0]); xs = abs(sh[0])
        lat = _ss((V[:, 0] * sg * np.sign(sh[0]) - x0) / max(xs - x0, 1.0))
        up = _ss((V[:, 2] - (sh[2] - 4.0)) / 6.0) * (V[:, 0] * np.sign(sh[0]) > 0)
        D[:, 2] += -spec["drop"] * lat * up
    return V + _smooth(D * L["keep"][:, None], L["F"], 10)

def hip_band(V, L, J, spec):
    """pelvic-girdle breadth about the midline (GR-P5 / GO-P3: crest and hip region proportioned to the trunk): x-scale k over the band
    from below the crest to the upper thigh, fading to 1 by `fade` cm below the hip joint and above `top` (r); arms excluded. The hip-joint
    centres move with the band (x * k) so the skeleton stays consistent."""
    Jl, hip, sst = _levels(L); k = spec["k"]; fade = spec.get("fade", 25.0); top = spec.get("top", 0.3)
    armw = np.maximum.reduce([L["w_" + a] for a in ARMK]); z = V[:, 2]; r = (z - hip) / (sst - hip)
    w = _ss((z - (hip - fade)) / (fade * 0.8)) * (1 - _ss((r - top) / 0.15)) * np.clip(1 - armw / 0.1, 0, 1) * L["keep"]
    w = _smooth(w[:, None], L["F"], 10)[:, 0]
    X = V.copy(); X[:, 0] = V[:, 0] * (1 + (k - 1) * w)
    J = dict(J)
    for sd in ("l", "r"):
        a, b = J["thigh_%s" % sd]; J["thigh_%s" % sd] = [[a[0] * k, a[1], a[2]], b]
    return X, J

def apply(V, L, arch):
    """arch = {"vz": {...}, "trunk": {...}, "leg": {...}, "arm": {...}}; returns (V', joints')"""
    V = np.asarray(V, float).copy(); J = json.loads(str(L["joints"]))
    if arch.get("vz"):
        V, zmap = vz_remap(V, L, arch["vz"])
        for k in ("spine_01", "spine_02", "spine_03"):
            J[k] = [[a[0], a[1], float(zmap(np.array([a[2]]))[0])] for a in J[k]]
        J["pelvis"][1][2] = J["spine_01"][0][2]
    for ch in ("arm", "leg"):
        if arch.get("seg", {}).get(ch): V, J = seg_shift(V, L, J, ch, arch["seg"][ch])
    if arch.get("trunk"): V = trunk_shape(V, L, arch["trunk"])
    if arch.get("hip"): V, J = hip_band(V, L, J, arch["hip"])
    for ch in ("leg", "arm"):
        if arch.get(ch):
            L2 = dict(L); L2["joints"] = json.dumps(J); V = limb_shape(V, L2, ch, arch[ch])
    if arch.get("distal"): V = distal_scale(V, L, J, arch["distal"])
    if arch.get("girdle"): V = girdle_top(V, L, J, arch["girdle"])
    return V, J
