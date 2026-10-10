# RAC W3B RM-UF-03: Saurin orbital spacing (IOD) metric and spacing boundary study. NON-CANON diagnostics on copies.
# METRIC (measurement-only landmark proxy, REFERENCE_ANATOMY measurement stance; bony orbit, never pupil / iris / lid margin):
#   ORBITAL MARGIN RING = for 36 angular sectors around the visual axis (yaw 24 deg from forward, through the orbit centre estimate), the
#   head-surface vertex of maximum mean convexity (principal curvature on the base mesh, 2-ring smoothed) inside the annulus
#   1.15 er ... 1.6 er (er = canonical orbit radius x head scale) from the centre estimate, excluding the eye surface (FAM 7) (annulus chosen
#   for ring stability: fit rms 0.16 cm vs 0.24-0.45 cm for 1.8-2.2 er, which reach the jugal / temporal crests). This is the skull's orbital frame crest (supraorbital crest above, postorbital bar behind, jugal below,
#   canthal / rostral root in front) - the orbit's BONY margin on a skin-continuous mesh.
#   ORBIT CENTRE = centre of the least-squares circle fitted to the ring in its best-fit plane. Centre estimate for the sectors = centroid of
#   the FAM 7 eye surface (only used to define sectors; iterated once with the fitted centre).
#   IOD = |c_R - c_L| (cm, world); IOD_x = frontal-plane (x) separation. Normalizers: CRANIAL WIDTH = bitemporal breadth, 2 max|x| of the
#   skull at head-local 2 < u < 8, -8 < f < -3 (behind the platform, independent of the orbit complex); ORBITAL-PLATFORM BREADTH = 2 max|x| at head-local u in
#   [eye_u + 1.0, eye_u + 2.5], f in [-2, 8].
#   Companions: medial margin separation (2 min|x| of the rings), lateral margin span (2 max|x|), orbit centre -> rostral dorsal midline
#   (distance to the dorsal midline point 4 cm head-local ahead of the orbit centre), lateral support breadth (skull |x| extent beside the
#   ring's lateral point minus the ring's |x|), ring circularity (fit rms / radius), aperture-fit (eye-surface radius / ring radius).
import os, sys, json, numpy as np, igl
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import w3b_common as C
_fam = None
def fam0():
    global _fam
    if _fam is None: _fam = np.load(C.CAN + '/saurin_w2_regfields.npz')['FAM'][:len(C.V0)]   # upsampled mesh keeps the base vertices first
    return _fam
HV = np.where(C.HEADM)[0]
_sub = None
def head_sub():
    global _sub
    if _sub is None:
        m = np.zeros(len(C.V0), bool); m[HV] = True; keep = m[C.F0].all(1); Fh = C.F0[keep]
        loc = np.full(len(C.V0), -1); loc[HV] = np.arange(len(HV)); _sub = loc[Fh]
    return _sub
ER = C.EYE0['r'] * C.HS
def curvature(P):
    Ph = P[HV]; Fh = head_sub()
    _, _, k1, k2, _ = igl.principal_curvature(Ph, Fh, radius=4)
    H = 0.5 * (k1 + k2)
    A = igl.adjacency_matrix(Fh).astype(float); deg = np.asarray(A.sum(1)).ravel()
    for _ in range(2): H = (H + A @ H) / (1 + deg)
    N = igl.per_vertex_normals(Ph, Fh); return H, N
def ring(P, side, Hc, centre=None, nsec=36):
    Ph = P[HV]; fam = fam0()[HV]
    sg = 1.0 if side > 0 else -1.0
    eye = (fam == 7) & (np.sign(Ph[:, 0]) == sg)
    c = Ph[eye].mean(0) if centre is None else centre
    yaw = C.EYE0['yaw']; ax = np.array([np.sin(yaw) * sg, np.cos(yaw), 0.0]); ax /= np.linalg.norm(ax)
    e1 = np.cross(np.array([0, 0, 1.0]), ax); e1 /= np.linalg.norm(e1); e2 = np.cross(ax, e1)
    Q = Ph - c; r = np.linalg.norm(Q, axis=1); a = (Q @ ax)
    cand = (r > 1.15 * ER) & (r < 1.6 * ER) & (fam != 7) & (a > -0.6 * ER) & (np.sign(Ph[:, 0]) == sg)
    ang = np.arctan2(Q @ e2, Q @ e1); sec = ((ang + np.pi) / (2 * np.pi) * nsec).astype(int) % nsec
    idx = np.where(cand)[0]; pts = []
    for s in range(nsec):
        k = idx[sec[idx] == s]
        if len(k): pts.append(k[np.argmax(Hc[k])])         # convex = positive mean curvature here (checked: skull roof apex H > 0)
    pts = np.array(pts); R = Ph[pts]
    # plane + circle fit
    m = R.mean(0); _, _, vt = np.linalg.svd(R - m); n = vt[2]; u1 = vt[0]; u2 = vt[1]
    x = (R - m) @ u1; y = (R - m) @ u2
    A_ = np.c_[2 * x, 2 * y, np.ones(len(x))]; sol = np.linalg.lstsq(A_, x * x + y * y, rcond=None)[0]
    cx, cy = sol[0], sol[1]; rad = np.sqrt(sol[2] + cx * cx + cy * cy)
    ctr = m + cx * u1 + cy * u2; rms = float(np.sqrt(np.mean((np.sqrt((x - cx) ** 2 + (y - cy) ** 2) - rad) ** 2)))
    return ctr, rad, rms, HV[pts], R, Ph[eye]
def measure(P):
    Hc, _ = curvature(P); out = {}
    rings = {}
    for side, nm in ((1, 'R'), (-1, 'L')):
        ctr = None
        for _ in range(2): ctr, rad, rms, ids, R, eyep = ring(P, side, Hc, ctr)
        rings[nm] = (ctr, rad, rms, ids, R, eyep)
    cR, cL = rings['R'][0], rings['L'][0]
    Lh = C.head_local(P[HV])
    sk = (Lh[:, 2] > 2.0) & (Lh[:, 2] < 8.0) & (Lh[:, 1] > -8) & (Lh[:, 1] < -3)      # bitemporal cranial breadth behind the platform
    cran_w = 2 * np.abs(P[HV][sk, 0]).max()
    eu = C.EYE0['u']; pl = (Lh[:, 2] > eu + 1.0) & (Lh[:, 2] < eu + 2.5) & (Lh[:, 1] > -2) & (Lh[:, 1] < 8)
    plat_w = 2 * np.abs(P[HV][pl, 0]).max()
    RR, RL = rings['R'][4], rings['L'][4]
    med = np.abs(RR[:, 0]).min() + np.abs(RL[:, 0]).min(); lat = np.abs(RR[:, 0]).max() + np.abs(RL[:, 0]).max()
    # orbit centre -> rostral dorsal midline point 4 cm (head-local) ahead
    cl = C.head_local(((cR + cL) / 2)[None])[0]; mid = (np.abs(Lh[:, 0]) < 0.25) & (np.abs(Lh[:, 1] - (cl[1] + 4.0)) < 0.3)
    rp = P[HV][mid][np.argmax(P[HV][mid, 2])]
    ros = 0.5 * (np.linalg.norm(cR - rp) + np.linalg.norm(cL - rp))
    # lateral support breadth: skull |x| extent within 0.5 cm (u) and 1.5 cm behind the ring's lateral point, minus the ring |x|
    sup = []
    for nm in ('R', 'L'):
        R = rings[nm][4]; lp = R[np.argmax(np.abs(R[:, 0]))]
        k = (np.abs(P[HV][:, 2] - lp[2]) < 0.5) & (P[HV][:, 1] < lp[1]) & (P[HV][:, 1] > lp[1] - 1.5 * C.HS) & (np.sign(P[HV][:, 0]) == np.sign(lp[0]))
        sup.append(np.abs(P[HV][k, 0]).max() - abs(lp[0]))
    def sphere(Q):
        A_ = np.c_[2 * Q, np.ones(len(Q))]; sol = np.linalg.lstsq(A_, (Q * Q).sum(1), rcond=None)[0]; return sol[:3]
    gR = sphere(rings['R'][5]); gL = sphere(rings['L'][5])
    eyer = [np.linalg.norm(rings[nm][5] - rings[nm][5].mean(0), axis=1).mean() for nm in ('R', 'L')]
    out.update(IOD=float(np.linalg.norm(cR - cL)), IOD_x=float(abs(cR[0] - cL[0])), cranial_width=float(cran_w), platform_breadth=float(plat_w),
               IOD_over_cranial=float(np.linalg.norm(cR - cL) / cran_w), IOD_over_platform=float(np.linalg.norm(cR - cL) / plat_w),
               medial_margin_sep=float(med), lateral_margin_span=float(lat), centre_to_rostral_midline=float(ros),
               lateral_support=float(np.mean(sup)), lateral_support_min=float(np.min(sup)),
               ring_radius=float(0.5 * (rings['R'][1] + rings['L'][1])), ring_rms=float(max(rings['R'][2], rings['L'][2])),
               aperture_fit=float(np.mean(eyer) / (0.5 * (rings['R'][1] + rings['L'][1]))),
               centre_R=cR.round(3).tolist(), centre_L=cL.round(3).tolist(), asym_cm=float(abs(abs(cR[0]) - abs(cL[0])) + abs(cR[1] - cL[1]) + abs(cR[2] - cL[2])),
               IOD_globe=float(np.linalg.norm(gR - gL)), lateralization=float(0.5 * (abs(cR[0]) + abs(cL[0])) / (0.5 * cran_w)))
    return out, rings
