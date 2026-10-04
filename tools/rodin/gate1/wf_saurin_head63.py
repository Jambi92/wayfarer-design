# Dedicated Saurin head: signed-distance construction of Layered Rostral-Cranial Integration, meshed by marching cubes.
# Frame: centimetres, origin at the head joint (atlas). X lateral, F forward, U up. Designed for a 188 cm Saurin.
import numpy as np

def smin(a, b, k):
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0, 1)
    return b * (1 - h) + a * h - k * h * (1 - h)

def smax(a, b, k):
    return -smin(-a, -b, k)

def ellipsoid(X, F, U, c, r):
    px, pf, pu = (X - c[0]) / r[0], (F - c[1]) / r[1], (U - c[2]) / r[2]
    k0 = np.sqrt(px * px + pf * pf + pu * pu)
    k1 = np.sqrt((px / r[0]) ** 2 + (pf / r[1]) ** 2 + (pu / r[2]) ** 2) + 1e-9
    return k0 * (k0 - 1) / k1

def capsule(X, F, U, a, b, r):
    a = np.array(a, float); b = np.array(b, float); ba = b - a
    px, pf, pu = X - a[0], F - a[1], U - a[2]
    h = np.clip((px * ba[0] + pf * ba[1] + pu * ba[2]) / ba.dot(ba), 0, 1)
    return np.sqrt((px - ba[0] * h) ** 2 + (pf - ba[1] * h) ** 2 + (pu - ba[2] * h) ** 2) - r

def sweep(X, F, U, F0, F1, uc, w, h, cap1, cap0=None, n=2.0):
    """Tapered elliptical section along F: uc/w/h are (root, tip) pairs. Rounded tip cap."""
    t = np.clip((F - F0) / (F1 - F0), 0, 1)
    c = uc[0] + (uc[1] - uc[0]) * t; ww = w[0] + (w[1] - w[0]) * t; hh = h[0] + (h[1] - h[0]) * t
    e = np.where(F > F1, (F - F1) / cap1, 0.0)
    if cap0 is not None: e = np.where(F < F0, (F0 - F) / cap0, e)
    q = ((np.abs(X / ww) ** n + np.abs((U - c) / hh) ** n) ** (2.0 / n) + e * e) ** 0.5
    return (q - 1) * np.minimum(ww, hh)

def rotated_ellipsoid_about_U(X, F, U, c, r, ang):
    """ellipsoid whose local 'forward' axis is rotated by ang (radians) toward +X."""
    ca, sa = np.cos(ang), np.sin(ang)
    dx, df = X - c[0], F - c[1]
    lx = dx * ca - df * sa; lf = dx * sa + df * ca
    return ellipsoid(lx, lf, U, (0, 0, c[2]), r)

def torus_axis(X, F, U, c, axis_yaw, R, r, vscale):
    """torus around an axis lying in the X-F plane (yaw from forward toward +X); ring flattened vertically by vscale."""
    ca, sa = np.cos(axis_yaw), np.sin(axis_yaw)
    dx, df, du = X - c[0], F - c[1], U - c[2]
    along = dx * sa + df * ca                     # coordinate along the axis
    side = dx * ca - df * sa                      # horizontal across
    q = np.sqrt(side ** 2 + (du / vscale) ** 2) - R
    return np.sqrt(q ** 2 + along ** 2) - r

def seam_u(F):
    from scipy.interpolate import PchipInterpolator
    k = sorted(P["mouth"]["curve"])
    return PchipInterpolator([p[0] for p in k], [p[1] for p in k], extrapolate=True)(np.clip(F, k[0][0], k[-1][0]))

def wedge(X, F, U, prof, n=2.2, cap_front=0.6, cap_back=0.5, oct_from=(3.0, 10.0), plane=None):
    """Head body swept along F with a hierarchy of planes: each section is a rounded polygon (dorsal, dorsolateral,
    lateral, ventrolateral, ventral faces) whose edge sharpness `p` rises from the cranium (broad, organic) to the
    rostrum (decisive). The rostrum ends in an anterior terminal plane rather than a rounded cap."""
    from scipy.interpolate import PchipInterpolator
    fs = [p_[0] for p_ in prof]; F0, F1 = fs[0], fs[-1]
    Fq = np.clip(F, F0, F1)
    top = PchipInterpolator(fs, [p_[1] for p_ in prof])(Fq); bot = PchipInterpolator(fs, [p_[2] for p_ in prof])(Fq)
    w = PchipInterpolator(fs, [p_[3] for p_ in prof])(Fq)
    c = (top + bot) / 2; h = (top - bot) / 2
    tz = np.clip((F - 5.0) / 6.0, 0, 1) * np.clip((U - c) / h, 0, 1)
    w = w * (1 - 0.17 * tz)                                     # canthus rostralis: rostrum narrows toward its dorsal face
    ax_, au = np.sqrt((X / w) ** 2 + 0.006), np.abs((U - c) / h)     # TS6.3: smooth across the midline (no gable crease)
    pl = plane or {}
    chamf = pl.get("chamfer", 0.80)
    s = np.clip((F - oct_from[0]) / (oct_from[1] - oct_from[0]), 0, 1); s = s * s * (3 - 2 * s)
    pexp = pl.get("p_cranium", 3.2) + (pl.get("p_rostrum", 7.0) - pl.get("p_cranium", 3.2)) * s
    ch = chamf * (ax_ + au)
    q = (ax_ ** pexp + au ** pexp + ch ** pexp) ** (1.0 / pexp)
    lower = np.clip((c - U) / (0.5 * h), 0, 1) * pl.get("round_below", 0.0)   # optional: rounder lower half
    q_round = (ax_ ** n + au ** n) ** (1.0 / n)
    q = q * (1 - lower) + q_round * lower
    e = np.where(F > F1, (F - F1) / cap_front, np.where(F < F0, (F0 - F) / cap_back, 0.0))
    pe = pl.get("p_tip", 4.0)
    q = np.where(F > F1, (q ** pe + e ** pe) ** (1.0 / pe), np.sqrt(q * q + e * e))
    return (q - 1) * np.minimum(w, h)

# ---- design parameters (cm) -----------------------------------------------------------------------------------------
# Targeted Sculpt 3: same integrated skull, now with layered skull anatomy around the eye (supraorbital ridge,
# postorbital bar, jugal arch), a planar rostrum, an articulated lower jaw under a curved oral margin, and a shaped neck.
EYE = dict(x=3.3, f=6.55, u=4.5, r=1.35, yaw=np.radians(24))
P = dict(
    # cranium + upper jaw (rostral-maxillary complex): F, top, bottom, half-width
    wedge=[(-12.6, 4.2, 0.4, 3.4), (-11.6, 5.8, -1.2, 5.0), (-10.5, 7.1, -1.0, 5.5), (-8.0, 8.8, -1.8, 6.0),   # pass 3: occiput slopes into the nuchal mass
           (-3.5, 9.8, -3.9, 6.8), (0.5, 9.3, -5.6, 7.0), (4.5, 7.8, -5.2, 6.6), (8.5, 5.3, -4.1, 5.2),
           (12.5, 2.9, -3.0, 3.45), (14.6, 1.15, -2.25, 2.35), (15.6, 0.3, -1.85, 1.75)],
    # mandible (lower jaw): F, top (ignored; the oral margin sets it), bottom, half-width -- narrower than the upper jaw
    mandible=[(-2.5, 0, -6.3, 5.7), (1.5, 0, -6.2, 5.8), (4.5, 0, -5.6, 5.6), (8.5, 0, -4.5, 4.75),
              (12.5, 0, -3.75, 3.3), (14.5, 0, -3.1, 2.3), (15.3, 0, -2.65, 1.65)],
    retroarticular=((5.0, -1.4, -0.9), (4.7, -3.2, -0.7), 0.5),
    jowl=((4.6, 0.4, -2.6), (0.75, 2.3, 1.8)),
    cervical_lat=((3.9, -2.4, -3.6), (3.8, -1.9, -8.5), 0.85),
    nuchal_lat=((3.2, -8.6, 0.8), (3.4, -6.2, -7.5), 1.6),
    rictal=((4.7, -0.6, -0.85), (0.45, 0.85, 0.6)),
    supraorbital=((3.1, 8.0, 4.95), (5.15, 3.2, 6.2), 0.62),
    postorbital=((5.0, 4.4, 6.1), (6.2, 3.6, 3.0), 0.78),
    jugal=((3.1, 9.0, 1.7), (6.0, 0.4, 1.7), 0.60),
    canthal=((2.3, 9.4, 5.4), (1.4, 13.9, 1.3), 0.22),
    temporal_line=((4.5, 4.3, 6.4), (4.3, -9.8, 7.0), 0.33),
    occipital=((-4.2, -10.9, 6.3), (4.2, -10.9, 6.3), 0.38),
    temporal_plane=(6.0, -0.8, -9.5, 3.5),
    orbitframe=((3.2, 6.3, 4.35), (1.5, 1.7, 1.35)),
    adductor=((4.6, 1.2, 3.0), (0.85, 3.2, 2.2)),          # jaw-closing muscle between orbit, temporal platform and hinge
    hinge=((4.8, -0.9, 0.3), (0.75, 1.3, 1.2)),             # quadrate / jaw articulation
    ramus=((4.7, -1.4, 0.3), (4.65, -0.8, -3.9), 0.95),      # posterior mandible rising to the hinge
    angle=((4.7, -1.4, -4.2), (1.15, 2.2, 1.8)),             # mandibular angle (posterior depth)
    nuchal=((0, -8.4, -3.2), (4.6, 3.8, 5.6)),
    gular=((0, -0.5, -6.6), (3.4, 4.0, 1.4)),                # throat under the mandibles
    mouth=dict(curve=[(-1.0, -0.75), (0.5, -1.15), (2.5, -1.55), (5.5, -1.95), (9.0, -2.05), (12.5, -1.9), (16.2, -2.05)],
               overhang=0.10),
    nostril=((1.35, 13.4, 0.75), (0.22, 0.42, 0.26)),
    ear=((6.75, -4.5, 2.6),),
)

OPEN_DEG = 0.0
import os as _os
BROW_INT = float(_os.environ.get("BROW_INT", "0"))   # post-Gate-8 polish: supraorbital integration (0 = Gate 7 skull exactly)
def cone(X, F, U, a, b, ra, rb):
    a = np.asarray(a, float); b = np.asarray(b, float); ab = b - a; L2 = ab @ ab
    t = np.clip(((X - a[0]) * ab[0] + (F - a[1]) * ab[1] + (U - a[2]) * ab[2]) / L2, 0, 1)
    return np.sqrt((X - a[0] - t * ab[0]) ** 2 + (F - a[1] - t * ab[1]) ** 2 + (U - a[2] - t * ab[2]) ** 2) - (ra + t * (rb - ra))

def tent(dist, wdt): return np.clip(1 - np.abs(dist) / wdt, 0, 1) ** 1.6
def along(F, f0, f1, fade=1.2): return np.clip((F - f0) / fade, 0, 1) * np.clip((f1 - F) / fade, 0, 1)

def head_sdf(X, F, U, neck_rings, cut_u):
    Xa = np.sqrt(X * X + 0.30)          # TS6.3: smooth |X| so paired features meet without a midline knife edge
    m = seam_u(F)
    mouth_zone = np.clip((F + 1.0) / 1.5, 0, 1)                 # the oral boundary exists from the rictus forward
    # labial scale scalloping along the margin (subtle): keeps the edge from being a perfect line
    scal = 0.0 * F                                   # TS6.3 clay pass: no labial scalloping (below mesh resolution)
    # upper jaw: cranium wedge whose ventral face is the oral margin; lateral wall overhangs the mandible a little
    upper_edge = m - P["mouth"]["overhang"] * np.clip(Xa / 2.0, 0, 1) + scal
    upper_edge = upper_edge - 0.22 * np.clip((F - 13.8) / 1.6, 0, 1) * np.clip(1 - Xa / 2.0, 0, 1)   # premaxilla closes over the mandible tip
    upper = wedge(X, F, U, P["wedge"], cap_front=0.55, plane=dict(p_cranium=2.7, p_rostrum=4.0, p_tip=2.8, chamfer=0.80))
    upper = np.where(mouth_zone > 0, smax(upper, (upper_edge - U) * mouth_zone + (upper - 1.0) * (1 - mouth_zone), 0.45), upper)
    # mandible: its own volume, top at the oral margin, narrower, deepening posteriorly
    mp = [(f, -99.0, b, w * 0.93) for f, _, b, w in P["mandible"]]
    mand = wedge(X, F, U, [(f, 1.5, b, w) for f, _, b, w in mp], n=2.6, cap_front=0.35, cap_back=1.5, oct_from=(-2.0, 6.0),
                 plane=dict(p_cranium=2.8, p_rostrum=3.6, p_tip=2.8, chamfer=0.82, round_below=0.85))
    mand = smax(mand, U - (m + 0.02 - scal * 0.6), 0.45)
    mand = smin(mand, capsule(Xa, F, U, *P["ramus"]), 1.2)
    mand = smin(mand, ellipsoid(Xa, F, U, *P["angle"]), 1.0)
    mand = smin(mand, capsule(Xa, F, U, *P["retroarticular"]), 0.7)
    mand = smin(mand, ellipsoid(Xa, F, U, *P["jowl"]), 1.4)
    if OPEN_DEG:   # articulation diagnostic: mandible rotated about the quadrate hinge axis (no oral cavity modelled)
        hf, hu = P["hinge"][0][1], P["hinge"][0][2]; a = np.radians(OPEN_DEG)
        Fr = hf + (F - hf) * np.cos(a) - (U - hu) * np.sin(a); Ur = hu + (F - hf) * np.sin(a) + (U - hu) * np.cos(a)
        mr = seam_u(Fr)
        mand = wedge(X, Fr, Ur, [(f, 1.5, b, w) for f, _, b, w in mp], n=2.6, cap_front=0.35, cap_back=1.5, oct_from=(-2.0, 6.0),
                     plane=dict(p_cranium=3.4, p_rostrum=4.6, p_tip=3.0, chamfer=0.85))
        mand = smax(mand, Ur - (mr + 0.02), 0.18)
        mand = smin(mand, capsule(Xa, Fr, Ur, *P["ramus"]), 1.2); mand = smin(mand, ellipsoid(Xa, Fr, Ur, *P["angle"]), 1.0)
        mand = smin(mand, ellipsoid(Xa, F, U, *P["jowl"]), 1.4)
    skull = smin(upper, mand, 0.45)                            # jaws closed into one skull; the oral line is carved below
    skull = skull + 0.16 * tent(U - (m - 0.02), 0.38) * along(F, -0.6, 16.0, 1.2) * np.clip((Xa - 0.25) / 0.9, 0, 1)
    # supralabial / infralabial scale rows: margin thickness that varies along the jaw (not lips)
    lab = along(F, 0.0, 15.6, 2.5) * np.clip((Xa - 0.6) / 1.0, 0, 1) * (1 + 0.35 * np.sin(F * 0.9))
    pass   # TS6.3: labial scale rows removed (surface detail, later gate)
    # rictal fold: soft tissue where the oral opening ends, below the jugal, in front of the hinge
    skull = smin(skull, ellipsoid(Xa, F, U, *P["rictal"]), 0.5)
    if BROW_INT:
        # supraorbital ridge integrated: sharp crest kept (tapering cone), broad low root web into the frontal roof, and a
        # tapering continuation that runs into the temporal line instead of ending as a block (no slab termination)
        skull = smin(skull, ellipsoid(Xa, F, U, (3.55, 5.7, 5.3), (1.55, 3.3, 0.55)), 2.0)                   # broad biological root
        skull = smin(skull, cone(Xa, F, U, (3.1, 8.0, 4.95), (4.95, 2.6, 6.15), 0.60, 0.40), 1.5)            # crest
        skull = smin(skull, cone(Xa, F, U, (4.95, 2.6, 6.15), (4.6, -1.2, 6.45), 0.40, 0.16), 1.2)           # dissolves into temporal line
        if BROW_INT >= 2:   # lateral root web under the ridge's outer face: fills the concave crease so the ridge grows out of the
            skull = smin(skull, ellipsoid(Xa, F, U, (4.75, 3.4, 5.55), (0.85, 3.1, 0.65)), 1.4)              # temporal plane
    else:
        skull = smin(skull, capsule(Xa, F, U, *P["supraorbital"]), 1.5)
    # Craniofacial Ridge-and-Plane Architecture (TS6): structural transitions between regions
    # ridges are raised from the existing surface (tent profiles), so they always sit on the skull, never float
    # canthus rostralis: plan-view line from the orbit to the nostril, on the upper half of the rostrum
    xr = np.interp(F, [6.5, 14.2], [2.6, 1.45])
    skull = skull - 0.27 * tent(Xa - xr, 0.62) * along(F, 6.5, 14.4, 2.0) * np.clip(U / 0.8, 0, 1)
    # temporal line: dorsolateral cranial edge from the postorbital bar back to the occiput
    xt = np.interp(F, [-10.5, -6, 0, 4.5], [3.6, 4.6, 4.9, 4.6])
    skull = skull - 0.26 * tent(Xa - xt, 0.8) * along(F, -10.5, 4.6, 2.5) * np.clip((U - 3.6) / 1.0, 0, 1)   # pass 2: stronger temporal line
    # jugal/maxillary ridge: side-view line from the rostral base under the orbit to the jaw hinge (lateral surfaces)
    uj = np.interp(F, [-0.5, 3.0, 7.0, 11.5], [1.2, 1.9, 2.3, 1.2])
    skull = skull - 0.28 * tent(U - uj, 0.62) * along(F, -0.5, 11.5, 2.0) * np.clip((Xa - 2.0) / 1.2, 0, 1)
    # occipital transition: transverse ridge across the back of the cranial roof
    fo = -10.6 + 0.0 * X
    skull = skull - 0.20 * tent(F - fo, 0.95) * np.clip((U - 4.0) / 1.0, 0, 1)
    # mandibular lateral ridge (inferior-lateral edge), turning up behind toward the hinge
    um = np.interp(F, [-1.5, 2.0, 8.0, 14.0], [-3.2, -4.4, -3.6, -2.6])
    skull = skull - 0.05 * tent(U - um, 1.2) * along(F, -1.5, 14.0, 2.0) * np.clip((Xa - 2.0) / 1.2, 0, 1)   # TS6.3: soft (no lip edge)
    tp = (Xa - P["temporal_plane"][0]) * (U > P["temporal_plane"][1]) * (F > P["temporal_plane"][2]) * (F < P["temporal_plane"][3])
    pass   # pass 3: flat temporal-plane cut removed (it sliced an ear-like disk into the skull side)
    skull = smin(skull, ellipsoid(Xa, F, U, (3.15, 6.25, 4.3), (1.55, 1.72, 1.42)), 1.1)           # orbit / lids (thinner rim, sits under the brow shelf)
    skull = smin(skull, ellipsoid(X, F, U, (0.0, 5.6, 5.55), (2.55, 3.4, 0.95)), 1.3)            # interorbital roof: brow, orbits and rostrum share one roof
    if BROW_INT:   # postorbital bar grows out of the brow: tapered toward the brow, filleted root (no L-corner)
        if BROW_INT >= 3:   # final cleanup: postorbital bar = sharp descending ridge that sweeps back into the jugal/quadrate line
            skull = smin(skull, cone(Xa, F, U, (5.0, 4.2, 6.0), (6.05, 3.4, 3.5), 0.46, 0.50), 1.1)               # brow -> mid bar (sharp)
            skull = smin(skull, cone(Xa, F, U, (6.05, 3.4, 3.5), (6.15, 1.9, 2.15), 0.50, 0.36), 1.15)            # lower limb sweeps back into
            skull = smin(skull, cone(Xa, F, U, (6.15, 1.9, 2.15), (5.6, -0.2, 1.3), 0.36, 0.22), 1.0)             # the jugal / quadrate line
        else:
            skull = smin(skull, cone(Xa, F, U, (5.0, 4.2, 6.0), (6.2, 3.6, 3.0), 0.55 if BROW_INT >= 2 else 0.60, 0.78), 1.3 if BROW_INT >= 2 else 0.95)
    else:
        skull = smin(skull, capsule(Xa, F, U, *P["postorbital"]), 0.5)
    skull = smin(skull, capsule(Xa, F, U, (3.1, 9.0, 1.7), (5.7, 3.0, 1.8), 0.58), 0.55)      # pass 3: jugal flares under the orbit ...
    skull = smin(skull, capsule(Xa, F, U, (5.7, 3.0, 1.8), (4.9, -0.8, 0.6), 0.48), 0.6)       # ... and sweeps into the quadrate/hinge (no free end knob)
    skull = smin(skull, ellipsoid(Xa, F, U, *P["adductor"]), 1.8)
    skull = smin(skull, ellipsoid(Xa, F, U, *P["hinge"]), 0.9)
    # ---- TS6.3 naked-skull refinement (no display structures) ---------------------------------------------------
    # premaxillary tip boss and paired low nasal ridges framing a flat dorsal nasal plane
    skull = smin(skull, ellipsoid(Xa, F, U, (0.0, 14.5, 0.3), (1.0, 0.85, 0.7)), 0.45)
    skull = skull - 0.12 * tent(Xa - np.interp(F, [7.5, 14.5], [1.55, 0.95]), 0.42) * along(F, 7.5, 14.6, 1.6) * np.clip((U - 0.4) / 0.9, 0, 1)
    # maxillary swelling over the tooth row and a shallow suborbital/antorbital fossa above it
    skull = smin(skull, capsule(Xa, F, U, (2.35, 13.2, -0.9), (4.75, 1.8, -0.6), 0.62), 0.9)
    skull = smax(skull, -(ellipsoid(Xa, F, U, (3.15, 9.6, 1.9), (0.55, 1.9, 0.8)) + 0.22), 0.6)
    # orbital-temporal platform: broad flat shelf behind the brow, edged by the temporal line
    skull = smin(skull, ellipsoid(Xa, F, U, (4.5, 0.8, 6.0), (1.6, 3.8, 0.75)), 1.0)
    # supratemporal fossa: depression behind the postorbital bar, above the jaw adductor
    skull = smax(skull, -(ellipsoid(Xa, F, U, (3.5, -3.6, 7.1), (1.3, 2.8, 1.1)) + 0.42), 0.8)
    # occipital: paired occipital bosses and a short midline nuchal crest that runs into the nuchal mass
    skull = smin(skull, capsule(Xa, F, U, (1.7, -10.0, 5.6), (2.0, -11.6, 3.0), 0.7), 1.0)
    skull = smin(skull, capsule(Xa, F, U, (0.0, -8.6, 7.4), (0.0, -12.2, 3.6), 0.55), 0.8)
    # intermandibular groove on the underside (rami read as a V around a soft gular floor)
    skull = skull + 0.12 * tent(Xa, 0.55) * along(F, 2.5, 13.5, 2.0) * np.clip((m - 2.6 - U) / 0.8, 0, 1)
    # neck column fitted to the body's own neck cross-sections (exact match at the cut so the seam closes)
    us = np.array([n[0] for n in neck_rings]); order = np.argsort(us); rings = [neck_rings[i] for i in order]; us = us[order]
    uq = np.clip(U, us[0], us[-1])   # above the last ring the column keeps that section and ends inside the skull
    cx = np.interp(uq, us, [n[1] for n in rings]); cf = np.interp(uq, us, [n[2] for n in rings])
    ax = np.interp(uq, us, [n[3] for n in rings]); af = np.interp(uq, us, [n[4] for n in rings])
    below = np.clip(cut_u - U, 0, None)                     # under the cut the column hides 1-2 mm inside the body
    ax = ax - np.minimum(below, 1) * 0.15; af = af - np.minimum(below, 1) * 0.15
    neck = (np.sqrt(((X - cx) / ax) ** 2 + ((F - cf) / af) ** 2) - 1) * np.minimum(ax, af)
    neck = np.maximum(neck, (cut_u - 7.0) - U)              # bottom cap, well inside the body
    neck = np.maximum(neck, U - 3.0)                        # top cap, inside the skull
    taper = 1 - 0.06 * np.clip((U - cut_u) / 8.0, 0, 1)
    neck = (np.sqrt(((X - cx) / (ax * taper)) ** 2 + ((F - cf) / (af * taper)) ** 2) - 1) * np.minimum(ax, af) * taper
    neck = np.maximum(np.maximum(neck, (cut_u - 7.0) - U), U - 3.0)
    neck = smin(neck, ellipsoid(X, F, U, *P["nuchal"]), 3.0)
    neck = smin(neck, ellipsoid(X, F, U, *P["gular"]), 1.6)
    neck = smin(neck, capsule(Xa, F, U, *P["cervical_lat"]), 2.4)       # lateral cervical attachment (jaw angle -> neck)
    neck = smin(neck, capsule(Xa, F, U, *P["nuchal_lat"]), 1.8)         # dorsolateral nuchal mass (occiput -> neck)
    skull = smin(skull, neck, 2.4)
    # orbit: recess around the eye, a lid rim continuous with the skull, an almond aperture
    ex, ef, eu, er, yaw = EYE["x"], EYE["f"], EYE["u"], EYE["r"], EYE["yaw"]
    axv = (np.sin(yaw), np.cos(yaw))
    room = ellipsoid(Xa, F, U, (ex, ef, eu), (er * 0.97,) * 3)
    skull = smax(skull, -room, 0.12)
    ap_c = (ex + axv[0] * 1.35, ef + axv[1] * 1.35, eu)
    aperture = rotated_ellipsoid_about_U(Xa, F, U, ap_c, (1.22, 1.6, 0.72), yaw)
    skull = smax(skull, -aperture, 0.28)
    # contact shadow where the jaws meet (very shallow, only along the visible lateral margin)
    cw = 0.035 + 0.03 * np.clip((6.0 - F) / 7.0, 0, 1)
    contact = np.maximum(np.abs(U - (m - 0.04)) - cw, -0.3 - F)
    contact = np.maximum(contact, -skull - (0.06 + 0.08 * np.clip((6.0 - F) / 7.0, 0, 1)))
    pass   # TS6.3: contact shadow removed (the carved oral line replaces it)
    # nostrils: small openings belonging to the rostral tip
    nc = P["nostril"][0]
    skull = smin(skull, ellipsoid(Xa, F, U, (nc[0] + 0.05, nc[1] - 0.05, nc[2] + 0.02), (0.5, 0.85, 0.42)), 0.4)   # narial rim
    nost = rotated_ellipsoid_about_U(Xa, F, U, nc, (0.17, 0.50, 0.21), np.radians(28))
    skull = smax(skull, -nost, 0.10)
    narial = ellipsoid(Xa, F, U, (1.75, 13.4, 0.4), (0.45, 1.0, 0.45))     # shallow lateral narial fossa
    pass
    # recessed auricular opening: shallow recess + small canal, no pinna
    c = P["ear"][0]
    recess = ellipsoid(Xa, F, U, (c[0] + 0.2, c[1], c[2]), (0.25, 0.75, 0.75))
    canal = ellipsoid(Xa, F, U, (c[0] + 0.25, c[1] + 0.1, c[2] + 0.1), (0.7, 0.36, 0.48))
    pass   # pass 3: auricular recess removed (its rim read as an external ear)
    pass   # pass 3: no canal (small shallow auricular recess only)
    return skull

def build_mesh(neck_rings, cut_u, step=0.13, body_sdf=None, tilt=0.0, blend=1.5, band=2.6):
    """cut plane (head frame): U + tilt*F = cut_u. Below it the surface is the body's own neck (signed distance to the
    trimmed body), blended into the head over `blend` cm; the band continues `band` cm under the plane, 0.8 mm proud of the
    body so the body's trimmed edge is covered, fading back onto the body at the band's lower edge."""
    from skimage.measure import marching_cubes
    xs = np.arange(-12.5, 12.5 + step, step, dtype=np.float32)
    fs = np.arange(-20.5 if DISPLAY else -14.0, 19.0 + step, step, dtype=np.float32)
    u_lo = cut_u - tilt * max(0.0, 12.0) - band
    us = np.arange(u_lo, 16.5 if DISPLAY else 16.0 + step, step, dtype=np.float32)
    X, F, U = np.meshgrid(xs, fs, us, indexing="ij")
    d = head_sdf(X, F, U, neck_rings, cut_u).astype(np.float32)
    ss = U + tilt * F - cut_u                                   # signed height above the cut plane
    if body_sdf is not None:
        m = ss < 0.05
        bd = body_sdf(X[m], F[m], U[m]).astype(np.float32)
        bd = np.where(np.isnan(bd), d[m], bd)
        t = np.clip((ss[m] + blend) / blend, 0, 1); t = t * t * (3 - 2 * t)
        out = -0.08 * np.clip((-ss[m] - blend) / 0.6, 0, 1) * np.clip((ss[m] + band) / 1.5, 0, 1)
        d[m] = (bd + out) * (1 - t) + d[m] * t
    d = np.where(ss < -band, 1.0, d)                            # nothing below the band
    del X, F, U, ss
    v, f, _, _ = marching_cubes(d, 0.0, spacing=(step, step, step))
    v[:, 0] += xs[0]; v[:, 1] += fs[0]; v[:, 2] += us[0]
    return v, f

def eye_centers():
    return [(s * EYE["x"], EYE["f"], EYE["u"]) for s in (1, -1)], EYE["r"], EYE["yaw"]

