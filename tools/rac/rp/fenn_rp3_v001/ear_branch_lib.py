# ear_branch_lib.py : order bdcd6a6 -- Fenn-only local production EAR TOPOLOGY BRANCH from MPFB Family Base v005.
#
# One shared all-quad ear patch per side, replacing the v005 ear-zone interior (hm08 w_ears > 0.5 faces; 1,206 faces / 1,181 interior
# vertices per side) and attached to the unchanged 52-vertex v005 root loop. Nothing outside the root loop moves or changes topology.
#
# TOPOLOGY v001 as built (integers only; identical for c1 / c2 and E1 / E2 / E3): layout2() + cuff_build3() + root_band(); TOPO2 below.
#   root band  root loop (52, v005) -> ring 1 (52): each root vertex keeps its v005 valence 4 (inner_faces_v005 - 1 spokes; convex / concave
#              root corners become 3-5 pole pairs one ring inside the root)
#   cuff       ring 1 .. ring 5 (52 / 56 / 60 / 64 / 68) -> junction ring J (70); count changes by DP-matched +/-2 transition quads (canonical,
#              per side, stored in topology/FENN_EAR_BRANCH_CUFF_CANON_v001.json); positions: 2-D smoothed annulus + rho^2 rise, then the
#              biharmonic fairing / relaxation / untangling in ear_build.py (with the one bounded v005 transition ring)
#   front      bridge block (attachment A | notch U, j_f rows; attached concha floor / tragus) + F1 crescent (U lower | posterior rim) +
#              F2 upper-extension kite (U upper | posterior upper rim, anterior helix | cut); Winslow TFI then angle-based optimisation
#   back       F1 + F2 (same grids as the front; the back of the concha is attached through the cuff)
#   rim        K_r rows round the free outline (helix roll); J = A + B_att + rim end + U + rim end + D_att = 2 (n_a + j_f + K_r) = 70
#   (layout(), rim_fill(), cuff_topology(), cuff_build() below are the superseded first-pass variants, kept for the record only)
#
# TOPOLOGY v002 (order 0d9c70b; the default, EAR_TOPO=v002; EAR_TOPO=v001 reproduces v001 exactly): ear_layout3.layout3() replaces the
#   front / back sheet partition: bridge (unchanged) + crescent F1' (whole notch U, 28 x 12, to a cut c1f -> P_up) + tapered leaf (rows across the
#   upper extension, columns 12 -> 2 by staggered 3 -> 1 templates, one diamond cap), rim strip on the new outline path. Junction ring J, root band and
#   the cuff transition rule are unchanged; attachment-line ends A_EX 0.7 -> 1.5 (LAYOUT3_KW a_ex); attached lobe front GEO_V2 (target D).
#   Cuff positions: biharmonic fairing -> tangential pre-smoothing -> protected untangling -> 3-D quality pass (ear_quality3d.py) with root-crease
#   term, rest-contact / clearance guard and (run_ear_v002_head.sh) a deformation-aware guard -> local aspect repair (ear_build.py).
#
# GEOMETRY (per head / side / candidate, deterministic):
#   W1e FN-elven outline + relief laws (tools/rac/w1/ear_families_v2.py), evaluated at each vertex's fixed (s, t) ear parameters;
#   in-plane: W1e plate -> W1e tilt -> the attachment + lobe are rotated about the helix root (c1) to the attachment angle tauA so the
#   attached region fits the v005 root footprint; the free upper ear keeps the W1e tilt and sweep;
#   out of plane: isometric bend about the attachment hinge line (flare angle phi0 at the root rising to the projection angle);
#   root frame: root-loop centroid O, root-plane normal n (lateral), up u (world up projected), b = posterior; ear scaled by HH / HH(MF-M-R).
import numpy as np, json
from scipy.spatial import cKDTree

HH_MF = 22.51                                                   # MF-M-R HH (W1c accepted reference; W1e attachment scale rule)
TOPO = dict(n_a=28, m=15, j_f=3, K_r=4, NC=4, INS=(0, 3, 3, 3, 0))  # superseded first-pass layout() integers (see TOPO2)
S0, S1, S3 = 0.20, 0.55, 0.08                                    # attachment s-range (anterior edge) and the posterior corner c3
ROT = (0.30, 0.95)                                               # s-range over which the attachment rotation fades into the W1e upper ear
A_BOW, A_EX, A_END = 0.45, 0.7, 0.0                              # attachment line bows forward of the plate edge (t units), end grading off
DATT_D = 0.90                                                    # attached lobe front below A (cm, canonical E2)
DATT = 0.35                                                      # attached front length along D and B beyond A (cm, canonical E2)
U_T, U_EX = 0.30, 0.55                                           # notch curve U: max t behind the concha, profile exponent

# W1e FN-elven base (ear_families.py FAM + ear_families_v2.py DET, proj 50 per E-D3); candidates per order bdcd6a6 §10
W1E = dict(L=8.6, wb=1.80, taper=("continuous", 0.30, 1.05), lobe=0.15, proj=50, tilt=32, sweep=1.6, thick=0.27,
           ah=0.24, crura=1.0, concha=0.72, crus=0.12, trag=0.24, atrag=0.18, helix=(0.26, 0.26))
GEO = dict(tauA=12.0, phi0=35.0, d_r=1.25, clear=0.05, lift_lobe=0.45, lift_top=0.35, corner_dip=0.0)          # attachment angle, root flare, bend ramp length, concha clearance (cm)
CAND = {'E1': dict(W1E, L=7.6, wb=1.75, proj=42, tilt=28, sweep=1.2),
        'E2': dict(W1E),
        'E3': dict(W1E, L=9.4, wb=1.85, proj=55, tilt=35, sweep=1.9)}

def smooth(t):
    t = np.clip(t, 0, 1); return t * t * (3 - 2 * t)

def width(s, p):
    s = np.asarray(s, float); lobe = np.sqrt(np.clip(s / p["lobe"], 0, 1)) * 0.82 + 0.18 * smooth(s / p["lobe"])
    w = p["wb"] * np.minimum(1.0, lobe); law, st, ex = p["taper"]; t = np.clip((s - st) / (1 - st), 0, 1)
    f = np.where(s < st, 1.0, np.cos(t * np.pi / 2) ** ex); return w * f + 0.02

def w1e_plate(s, t, p):
    """W1e plate coordinates (y backward, z up) before orientation"""
    w = width(s, p); o = np.where(t >= 0, t * w, t * 0.38 * w); return p["sweep"] * s ** 2 + o, p["L"] * s

def _pd(Y, Z, pts):
    best = np.full(np.shape(Y), 1e9)
    for (y0, z0), (y1, z1) in zip(pts, pts[1:]):
        dy, dz = y1 - y0, z1 - z0; L2 = dy * dy + dz * dz + 1e-12; t = np.clip(((Y - y0) * dy + (Z - z0) * dz) / L2, 0, 1)
        best = np.minimum(best, np.hypot(Y - (y0 + t * dy), Z - (z0 + t * dz)))
    return best

def relief(S, T, p):
    """W1e v2 sculpt-detail relief (front-surface offset along the plate normal, cm) and cartilage+skin thickness, at (s, t)"""
    S = np.asarray(S, float); T = np.asarray(T, float); L = p["L"]; w = width(S, p); Y, Z = w1e_plate(S, T, p)
    def pt(ss, tt):
        ww = float(width(np.array(ss), p)); return (p["sweep"] * ss ** 2 + (tt * ww if tt >= 0 else tt * 0.38 * ww), L * ss)
    edge = 1 - np.abs(T); hh, hw = p["helix"]; ew = hw / np.maximum(w, 0.05); lobe_gate = smooth((S - p["lobe"]) / 0.10)
    helix = hh * (np.exp(-(edge / ew) ** 2) - 0.5 * np.exp(-((edge - 2.3 * ew) / ew) ** 2)) * lobe_gate * smooth((T + 0.3) / 0.3 + (S - 0.55) / 0.08)
    top_s = min(0.97, p["taper"][1] + 0.55 * (1 - p["taper"][1]))
    stem = [pt(0.24, 0.35), pt(0.36, 0.42), pt(0.50, 0.40)]; sup = [pt(0.50, 0.40), pt(0.62, 0.36), pt(top_s * 0.92, 0.18)]
    inf = [pt(0.50, 0.40), pt(0.56, 0.05), pt(0.58, -0.40)]; aw = 0.22 * (L / 6.4) ** 0.5
    ah_stem = p["ah"] * np.exp(-(_pd(Y, Z, stem) / aw) ** 2); ah_sup = p["ah"] * p["crura"] * np.exp(-(_pd(Y, Z, sup) / (0.85 * aw)) ** 2)
    ah_inf = p["ah"] * 0.8 * p["crura"] * np.exp(-(_pd(Y, Z, inf) / (0.75 * aw)) ** 2); ah = np.minimum(ah_stem + ah_sup + ah_inf, p["ah"] * 1.15)
    fc = pt(0.60, 0.12); fos = -0.35 * p["concha"] * np.exp(-((Y - fc[0]) ** 2 + (Z - fc[1]) ** 2) / (0.35 * L / 6.4) ** 2)
    cav = pt(0.33, -0.05); cym = pt(0.47, -0.05); rc = 0.62 * (L / 6.4) ** 0.6
    cavum = -p["concha"] * np.exp(-((Y - cav[0]) ** 2 / (rc * 0.9) ** 2 + (Z - cav[1]) ** 2 / rc ** 2))
    cymba = -0.55 * p["concha"] * np.exp(-((Y - cym[0]) ** 2 / (rc * 0.8) ** 2 + (Z - cym[1]) ** 2 / (rc * 0.45) ** 2)); concha = cavum + cymba
    crus = p["crus"] * np.exp(-(_pd(Y, Z, [pt(0.42, -0.95), pt(0.42, -0.35), pt(0.43, 0.05)]) / (0.12 * L / 6.4)) ** 2)
    trag = p["trag"] * np.exp(-(_pd(Y, Z, [pt(0.27, -0.90), pt(0.33, -0.85)]) / (0.17 * L / 6.4)) ** 2)
    a0 = pt(0.22, 0.40); atrag = p["atrag"] * np.exp(-((Y - a0[0]) ** 2 + (Z - a0[1]) ** 2) / (0.20 * L / 6.4) ** 2)
    n0 = pt(0.20, -0.30); notch = -0.15 * p["concha"] * np.exp(-((Y - n0[0]) ** 2 + (Z - n0[1]) ** 2) / (0.18 * L / 6.4) ** 2)
    lobe = 0.20 * (1 - smooth(S / (p["lobe"] * 1.2)))
    parts = dict(helix=helix, antihelix=ah, antihelix_stem=ah_stem, superior_crus=ah_sup, inferior_crus=ah_inf, triangular_fossa=fos, concha=concha,
                 cavum=cavum, cymba=cymba, crus_of_helix=crus, tragus=trag, antitragus=atrag, intertragic_notch=notch, lobe_thickening=lobe)
    return helix + ah + fos + concha + crus + trag + atrag + notch, p["thick"] + lobe, parts

# ------------------------------------------------------------------ in-plane map (posterior y, up z; cm, before head scale / placement)
class InPlane:
    def __init__(self, p, g=GEO):
        self.p = p; self.g = g; ss = np.linspace(0.15, 0.6, 50); Ry, Rz = w1e_plate(ss, -np.ones_like(ss), p); self.R = (Ry.mean(), Rz.mean())
        self.tl = np.radians(p["tilt"]); c0 = self._tilt(*w1e_plate(np.array(S0), np.array(-1.0), p)); c1 = self._tilt(*w1e_plate(np.array(S1), np.array(-1.0), p))
        self.c1 = np.array([float(c1[0]), float(c1[1])]); angA = np.arctan2(float(c1[0] - c0[0]), float(c1[1] - c0[1]))
        self.th_low = np.radians(g["tauA"]) - angA
        h = self.flat(np.array([S1]), np.array([-1.0]))[0] - self.flat(np.array([S0]), np.array([-1.0]))[0]; self.h = h / np.linalg.norm(h)
        self.k = np.array([self.h[1], -self.h[0]]); self.hinge = self.flat(np.array([S1]), np.array([-1.0]))[0]
        dd = np.linspace(-4, 8, 6001); phi = np.radians(np.where(dd < 0, g["phi0"], g["phi0"] + (p["proj"] - g["phi0"]) * smooth(dd / g["d_r"])))
        i0 = np.searchsorted(dd, 0.0); cy = np.r_[0, np.cumsum(0.5 * (np.cos(phi[1:]) + np.cos(phi[:-1])) * np.diff(dd))]
        cx = np.r_[0, np.cumsum(0.5 * (np.sin(phi[1:]) + np.sin(phi[:-1])) * np.diff(dd))]; self.dd = dd; self.Yb = cy - cy[i0]; self.Xb = cx - cx[i0]; self.phi = phi
    def _tilt(self, Y, Z):
        y = Y - self.R[0]; z = Z - self.R[1]; return y * np.cos(self.tl) + z * np.sin(self.tl), -y * np.sin(self.tl) + z * np.cos(self.tl)
    def flat(self, s, t):
        """in-plane (posterior, up) after W1e tilt and the attachment rotation; no bend"""
        y1, z1 = self._tilt(*w1e_plate(s, t, self.p)); th = self.th_low * (1 - smooth((np.asarray(s) - ROT[0]) / (ROT[1] - ROT[0])))
        dy = y1 - self.c1[0]; dz = z1 - self.c1[1]
        return np.stack([self.c1[0] + dy * np.cos(th) + dz * np.sin(th), self.c1[1] - dy * np.sin(th) + dz * np.cos(th)], -1)
    def bent(self, s, t):
        """(lateral X, posterior y, up z) of the front base surface after the isometric hinge bend, and the base normal"""
        x = self.flat(s, t) - self.hinge; a = x @ self.h; d = x @ self.k
        Yb = np.interp(d, self.dd, self.Yb); Xb = np.interp(d, self.dd, self.Xb); ph = np.interp(d, self.dd, self.phi)
        ss = np.asarray(s, float); g = self.g
        le = g.get('lobe_lift_end'); lw = g.get('lobe_lift_w', 0.04); tw = g.get('lobe_lift_tw', 0.5)
        lobe_f = smooth((S0 - ss) / 0.10)
        if le is not None:                                                     # v002 (target D): no lobe lift on the attached lobe front (Datt, c0f)
            tt_ = np.asarray(t, float); att = (1 - smooth((tt_ + 1) / tw)) * smooth((ss - (le - lw)) / lw); lobe_f = lobe_f * (1 - g.get('lobe_lift_att', 1.0) * att)
        lift = (g.get('lift_lobe', 0.0) * lobe_f + g.get('lift_top', 0.0) * smooth((ss - S1) / 0.08) * (1 - smooth((ss - S1 - 0.25) / 0.2))) \
               * np.exp(-(np.maximum(d, 0) / 1.2) ** 2)
        Xb = Xb + lift                                              # free lobe and helix-root edges stand off the skin beyond the attachment
        P2 = self.hinge + a[..., None] * self.h + Yb[..., None] * self.k
        N = np.stack([np.cos(ph), -np.sin(ph) * self.k[0] * np.ones_like(ph), -np.sin(ph) * self.k[1] * np.ones_like(ph)], -1)
        return np.stack([Xb, P2[..., 0], P2[..., 1]], -1), N, d

# ------------------------------------------------------------------ canonical structured layout in (s, t)
def _curve_st(segs, n_dense=4000):
    """concatenate (s, t) polylines; returns dense (s, t) samples"""
    out = []
    for (sa, ta, sb, tb) in segs:
        u = np.linspace(0, 1, n_dense); out.append(np.c_[sa + (sb - sa) * u, ta + (tb - ta) * u])
    return np.concatenate(out)

def _resample(st, ip, n, grade=None):
    """n edges along a dense (s, t) curve, uniform in in-plane arc length (optionally graded: grade = ratio last / first edge)"""
    X = ip.flat(st[:, 0], st[:, 1]); c = np.r_[0, np.cumsum(np.linalg.norm(np.diff(X, axis=0), axis=1))]; c /= c[-1]
    u = np.linspace(0, 1, n + 1)
    if grade is not None:
        r = grade ** (1.0 / max(n - 1, 1)); e = r ** np.arange(n); u = np.r_[0, np.cumsum(e)] / e.sum()
    return np.c_[np.interp(u, c, st[:, 0]), np.interp(u, c, st[:, 1])]

def _tfi(A, C, D, B):
    """discrete transfinite interpolation; A[i] (j=0), C[i] (j=m), D[j] (i=0), B[j] (i=n)"""
    n = len(A) - 1; m = len(D) - 1; xi = np.linspace(0, 1, n + 1)[:, None, None]; et = np.linspace(0, 1, m + 1)[None, :, None]
    X = (1 - et) * A[:, None] + et * C[:, None] + (1 - xi) * D[None] + xi * B[None] \
        - ((1 - xi) * (1 - et) * A[0] + xi * (1 - et) * A[-1] + (1 - xi) * et * C[0] + xi * et * C[-1])
    return X

def _winslow(X, it=4000):
    X = X.copy()
    for _ in range(it):
        xe = 0.5 * (X[2:, 1:-1] - X[:-2, 1:-1]); xn = 0.5 * (X[1:-1, 2:] - X[1:-1, :-2])
        a = (xn ** 2).sum(-1, keepdims=True); g = (xe ** 2).sum(-1, keepdims=True); b = (xe * xn).sum(-1, keepdims=True)
        xen = 0.25 * (X[2:, 2:] - X[2:, :-2] - X[:-2, 2:] + X[:-2, :-2])
        new = (a * (X[2:, 1:-1] + X[:-2, 1:-1]) + g * (X[1:-1, 2:] + X[1:-1, :-2]) - 2 * b * xen) / (2 * (a + g) + 1e-12)
        X[1:-1, 1:-1] = 0.5 * X[1:-1, 1:-1] + 0.5 * new
    return X

def _invert(P, ip, guess_tree, guess_st):
    """in-plane points -> (s, t) by nearest dense sample + damped Newton"""
    _, i = guess_tree.query(P); st = guess_st[i].copy()
    for _ in range(30):
        f = ip.flat(st[:, 0], st[:, 1]) - P; e = 1e-5
        Js = (ip.flat(st[:, 0] + e, st[:, 1]) - ip.flat(st[:, 0] - e, st[:, 1])) / (2 * e)
        Jt = (ip.flat(st[:, 0], st[:, 1] + e) - ip.flat(st[:, 0], st[:, 1] - e)) / (2 * e)
        J = np.stack([Js, Jt], -1); det = J[:, 0, 0] * J[:, 1, 1] - J[:, 0, 1] * J[:, 1, 0]; det = np.where(np.abs(det) < 1e-10, 1e-10, det)
        ds = (J[:, 1, 1] * f[:, 0] - J[:, 0, 1] * f[:, 1]) / det; dt = (-J[:, 1, 0] * f[:, 0] + J[:, 0, 0] * f[:, 1]) / det
        st[:, 0] = np.clip(st[:, 0] - 0.8 * ds, 0, 1); st[:, 1] = np.clip(st[:, 1] - 0.8 * dt, -1.6, 1)
    return st, np.linalg.norm(ip.flat(st[:, 0], st[:, 1]) - P, axis=1)

def layout(p=CAND['E2'], topo=TOPO):
    """canonical ear-sheet layout: (s, t) for every front / back / rim vertex + face lists (local indices)"""
    na, m, jf, Kr = topo['n_a'], topo['m'], topo['j_f'], topo['K_r']; ip = InPlane(p)
    A = _resample(_curve_st([(S0, -1, S1, -1)]), ip, na)
    side = lambda st: ip.flat(st[:, 0], st[:, 1])
    def split(st_dense, n_att, n_free, grade_free):
        """first n_att edges cover DATT cm (attached), then n_free edges to the end"""
        X = side(st_dense); c = np.r_[0, np.cumsum(np.linalg.norm(np.diff(X, axis=0), axis=1))]; k = np.searchsorted(c, DATT)
        return np.r_[_resample(st_dense[:k + 1], ip, n_att)[:-1], _resample(st_dense[k:], ip, n_free, grade=grade_free)]
    Bst = np.r_[_curve_st([(S1, -1, 1.0, -1)]), [[1.0, 0.0]]]; B = split(Bst, jf, m - jf, 0.8)
    Cst = np.r_[_curve_st([(S3, 1, 1.0, 1)]), [[1.0, 0.0]]]; C = _resample(Cst, ip, na, grade=0.6)
    D = split(_curve_st([(S0, -1, 0.0, -1), (0.0, 1, S3, 1)]), jf, m - jf, 1.0)          # c0 -> lobe front -> lobe bottom -> c3
    # notch curve U from D[jf] (lobe front) behind the concha to B[jf] (helix root): row jf of the front grid, first row of the back grid
    sa, sb = D[jf, 0], B[jf, 0]; lam = np.linspace(0, 1, 4000)
    Ust = np.c_[sa + (sb - sa) * lam, -1 + (U_T + 1) * np.sin(np.pi * lam) ** U_EX]; U = _resample(Ust, ip, na); U[0] = D[jf]; U[-1] = B[jf]
    Xbr = _winslow(_tfi(side(A), side(U), side(D[:jf + 1]), side(B[:jf + 1])))         # bridge block (attached, front only)
    XB = _winslow(_tfi(side(U), side(C), side(D[jf:]), side(B[jf:])))                  # free block (front and back share it)
    XF = np.concatenate([Xbr[:, :-1], XB], 1)
    # (s, t) of the interior vertices (boundary vertices keep their exact curve parameters)
    sd = np.linspace(0, 1, 801); td = np.linspace(-1, 1, 401); SS, TT = np.meshgrid(sd, td, indexing='ij'); G = np.c_[SS.ravel(), TT.ravel()]
    tree = cKDTree(ip.flat(G[:, 0], G[:, 1]))
    stF = np.zeros(XF.shape[:2] + (2,)); stB = np.zeros(XB.shape[:2] + (2,))
    stF[:, 1:-1], errF = [a.reshape(na + 1, m - 1, *a.shape[1:]) for a in _invert(XF[:, 1:-1].reshape(-1, 2), ip, tree, G)]
    stB[:, 1:-1], errB = [a.reshape(na + 1, m - jf - 1, *a.shape[1:]) for a in _invert(XB[:, 1:-1].reshape(-1, 2), ip, tree, G)]
    stF[:, 0] = A; stF[:, -1] = C; stF[0, :] = D; stF[-1, :] = B; stF[:, jf] = U
    stB[:, 0] = U; stB[:, -1] = C; stB[0, :] = D[jf:]; stB[-1, :] = B[jf:]
    # interior inversions for i = 0 / n_a rows were overwritten by exact boundary values above
    # --- vertex numbering (local): front, back, rim interior rows
    idx = {}; st = []; part = []
    def add(key, v, pt):
        idx[key] = len(st); st.append(v); part.append(pt)
    for i in range(na + 1):
        for j in range(m + 1): add(('F', i, j), stF[i, j], 'front')
    for i in range(na + 1):
        for j in range(m - jf + 1): add(('G', i, j), stB[i, j], 'back')
    # rim path over outline points: D[jf..m] -> C[1..na] -> B[m-1..jf]
    path = [('D', j) for j in range(jf, m + 1)] + [('C', i) for i in range(1, na + 1)] + [('B', j) for j in range(m - 1, jf - 1, -1)]
    def fkey(pk):
        s_, k = pk; return ('F', 0, k) if s_ == 'D' else (('F', k, m) if s_ == 'C' else ('F', na, k))
    def gkey(pk):
        s_, k = pk; return ('G', 0, k - jf) if s_ == 'D' else (('G', k, m - jf) if s_ == 'C' else ('G', na, k - jf))
    for q, pk in enumerate(path):
        for r in range(1, Kr): add(('R', r, q), st[idx[fkey(pk)]], 'rim')
    F = []
    for i in range(na):
        for j in range(m): F.append([idx[('F', i, j)], idx[('F', i + 1, j)], idx[('F', i + 1, j + 1)], idx[('F', i, j + 1)]])
    for i in range(na):
        for j in range(m - jf): F.append([idx[('G', i, j)], idx[('G', i, j + 1)], idx[('G', i + 1, j + 1)], idx[('G', i + 1, j)]])
    rowkey = lambda r, q: idx[fkey(path[q])] if r == 0 else (idx[gkey(path[q])] if r == Kr else idx[('R', r, q)])
    for q in range(len(path) - 1):
        for r in range(Kr): F.append([rowkey(r, q), rowkey(r, q + 1), rowkey(r + 1, q + 1), rowkey(r + 1, q)])
    # junction ring J (closed, 52): A, B_att, rim end (B side), U reversed, rim end (D side), D_att reversed
    J = [idx[('F', i, 0)] for i in range(na + 1)] + [idx[('F', na, j)] for j in range(1, jf + 1)]
    J += [rowkey(r, len(path) - 1) for r in range(1, Kr + 1)] + [idx[('G', i, 0)] for i in range(na - 1, -1, -1)]
    J += [rowkey(r, 0) for r in range(Kr - 1, -1, -1)] + [idx[('F', 0, j)] for j in range(jf - 1, 0, -1)]
    Jseg = ['A'] * (na + 1) + ['Batt'] * jf + ['rimB'] * (Kr - 1) + ['U'] * (na + 1) + ['rimD'] * (Kr - 1) + ['Datt'] * jf
    # interior directions at J (local neighbour pairs: (from, to) into the sheet)
    Jdir = []
    for k, v in enumerate(J):
        key = [kk for kk, vv in idx.items() if vv == v][0]
        if key == ('F', 0, 0): Jdir.append([v, idx[('F', 1, 1)]])
        elif key == ('F', na, 0): Jdir.append([v, idx[('F', na - 1, 1)]])
        elif key[0] == 'F' and key[2] == 0: Jdir.append([v, idx[('F', key[1], 1)]])
        elif key[0] == 'F' and key[1] == na: Jdir.append([v, idx[('F', na - 1, key[2])]])
        elif key[0] == 'F' and key[1] == 0: Jdir.append([v, idx[('F', 1, key[2])]])
        elif key[0] == 'G': Jdir.append([v, idx[('G', key[1], 1)]])
        else:
            q = key[2]; Jdir.append([v, idx[('R', key[1], 1 if q == 0 else q - 1)]])
    info = dict(path=[list(x) for x in path], inv_err_front_max=float(errF.max()), inv_err_back_max=float(errB.max()),
                corners=dict(c0=idx[('F', 0, 0)], c1=idx[('F', na, 0)], c3=idx[('F', 0, m)], tip=idx[('F', na, m)], c3b=idx[('G', 0, m - jf)], tipb=idx[('G', na, m - jf)],
                             c0f=idx[('F', 0, jf)], c1f=idx[('F', na, jf)], c0b=idx[('G', 0, 0)], c1b=idx[('G', na, 0)]))
    assert len(J) == 2 * (na + jf + Kr) and len(set(J)) == len(J), len(J)
    return dict(st=np.array(st), part=np.array(part), F=np.array(F), J=np.array(J), Jseg=Jseg, Jdir=np.array(Jdir), idx=idx, info=info, topo=dict(topo),
                rim_rows={idx[('R', r, q)]: r for r in range(1, Kr) for q in range(len(path))}, path_len=len(path))

# ------------------------------------------------------------------ root band (keeps every v005 root vertex at valence 4)
def root_band(inner_counts):
    """inner_counts[k] = v005 ear-zone faces at root vertex k (loop order). Returns ring1 size, band faces with root index ('r', k)
    and ring1 index ('e', j), and the root anchors (list of root k per ring1 vertex)."""
    nL = len(inner_counts); spokes = [k for k in range(nL) for _ in range(inner_counts[k] - 1)]
    # ring1 vertices: one per spoke; consecutive spokes across a zero-spoke (convex) root vertex share their end; two spokes from one
    # (concave) root vertex get an extra ring vertex between them
    ring = []; end = [None] * len(spokes); faces = []
    for i, k in enumerate(spokes):
        if i > 0 and (k - spokes[i - 1]) % nL == 2: end[i] = end[i - 1]
        else:
            if i > 0 and k == spokes[i - 1]: ring.append(('x', k))
            ring.append(('s', i)); end[i] = len(ring) - 1
    # wrap-around checks
    k0, kl = spokes[0], spokes[-1]
    if (k0 - kl) % nL == 2:                      # merge last into first
        last = end[-1]; ring.pop(last); end = [e if e != last else 0 for e in end]; end = [e - 1 if e > last else e for e in end]
    if k0 == kl: ring.append(('x', k0))
    anchors = []
    for r in ring:
        if r[0] == 'x': anchors.append([r[1]])
        else:
            ks = [spokes[i] for i in range(len(spokes)) if end[i] == ring.index(r)]; anchors.append(sorted(set(ks)))
    xpos = {r[1]: j for j, r in enumerate(ring) if r[0] == 'x'}
    for i in range(len(spokes)):
        i2 = (i + 1) % len(spokes); ka, kb = spokes[i], spokes[i2]; ea, eb = end[i], end[i2]
        if ka == kb: faces.append([('r', ka), ('e', eb), ('e', xpos[ka]), ('e', ea)])
        elif (kb - ka) % nL == 1: faces.append([('r', ka), ('r', kb), ('e', eb), ('e', ea)])
        elif (kb - ka) % nL == 2: faces.append([('r', ka), ('r', (ka + 1) % nL), ('r', kb), ('e', ea)])
        else: raise ValueError('gap %d' % ((kb - ka) % nL))
    return len(ring), faces, anchors

# ------------------------------------------------------------------ cuff topology (ring1 -> J with +2 inserts), defined on J indices only
def cuff_topology(nJ, J_seg, ins=TOPO['INS']):
    """rings from J (top) down to ring1. J_seg[k] = segment label of J vertex k ('A','Batt','rimB','U','rimD','Datt').
    Returns rings (list, bottom first; each a list of chain ids = J indices whose chain the vertex lies on), band faces as
    ((ring, pos), ...) tuples, and chain start ring (lowest ring index where each J chain exists)."""
    nb = len(ins); rings = [None] * (nb + 1); rings[nb] = list(range(nJ)); faces = []; start = {c: nb for c in range(nJ)}
    elig = [k for k in range(nJ) if J_seg[k] in ('A', 'U')]
    for b in range(nb - 1, -1, -1):                        # band b joins ring b (bottom) and ring b+1 (top)
        top = rings[b + 1]; k = ins[b]; bottom = []; trip = set()
        if k:
            el = [i for i, c in enumerate(top) if c in elig]; ph = (b % 3) / 3.0
            cen = sorted({el[int((q + 0.5 + ph) / k * len(el)) % len(el)] for q in range(k)})
            for c_ in cen: trip.add(c_)
        i = 0; n = len(top); mapping = []                 # mapping: bottom vertex -> list of top positions it connects to
        skip = set()
        for c_ in trip: skip.update({(c_ - 1) % n, (c_ + 1) % n})
        for i in range(n):
            if i in skip: continue
            if i in trip: bottom.append(top[i]); mapping.append(((i - 1) % n, i, (i + 1) % n))
            else: bottom.append(top[i]); mapping.append((i,))
        for tri in [m_ for m_ in mapping if len(m_) == 3]:
            start[top[tri[0]]] = b + 1; start[top[tri[2]]] = b + 1
        rings[b] = bottom; nbm = len(bottom)
        for j in range(nbm):
            a, c = mapping[j], mapping[(j + 1) % nbm]
            ta = a[-1]; tc = c[0]                             # right-most top of a, left-most top of c
            faces.append([(b, j), (b, (j + 1) % nbm), (b + 1, tc), (b + 1, ta)])
            if len(a) == 3: faces.append([(b, j), (b + 1, a[2]), (b + 1, a[1]), (b + 1, a[0])])
    return rings, faces, start

# ------------------------------------------------------------------ per-head root data (v005 family realization)
def root_data(V, Q, we, sg):
    fe = np.nonzero((we[Q] > 0.5).all(1) & (np.sign(V[Q].mean(1)[:, 0]) == sg))[0]
    E = {}
    for q in Q[fe]:
        for k in range(4): E[(q[k], q[(k + 1) % 4])] = 1
    nxt = {a: b for (a, b) in E if (b, a) not in E}; s0 = min(nxt); L = [s0]
    while nxt[L[-1]] != s0: L.append(nxt[L[-1]])
    L = np.array(L); zone_v = np.unique(Q[fe]); interior = np.setdiff1d(zone_v, L)
    inn = np.zeros(len(V), int); np.add.at(inn, Q[fe].ravel(), 1)
    P = V[L]; O = P.mean(0); _, _, vt = np.linalg.svd(P - O); n = vt[2] * np.sign(vt[2][0] * sg)
    up = np.array([0, 0, 1.0]); u = up - n * (up @ n); u /= np.linalg.norm(u); b = np.cross(u, n); b = b if b[1] < 0 else -b   # posterior = -forward (y)
    # outer neighbours (v005 edges leaving the loop away from the ear zone)
    nb = {}
    for q in Q:
        for k in range(4):
            a, c = q[k], q[(k + 1) % 4]; nb.setdefault(a, set()).add(c); nb.setdefault(c, set()).add(a)
    Ls = set(L.tolist()); zs = set(zone_v.tolist()); T = []; fz_ = set(fe.tolist()); vf = {}
    for fi in np.nonzero(np.isin(Q, L).any(1))[0]:
        if fi in fz_: continue
        for w in Q[fi]: vf.setdefault(int(w), set()).update(int(x) for x in Q[fi])
    for v in L:
        out = [w for w in nb[v] if w not in zs] or [w for w in vf[int(v)] if w not in Ls]
        t = V[v] - V[out].mean(0); T.append(t / np.linalg.norm(t))
    return dict(loop=L, inner=inn[L], interior=interior, faces=fe, O=O, n=n, b=b, u=u, T=np.array(T), nb=nb)

def skull_field(V, Q, rd, sg, radius=4.0):
    """thin-plate height field (lateral offset from the root plane) over the root-plane coordinates, fitted on the root loop and the
    head skin outside the ear zone within `radius` cm of the root centroid"""
    from scipy.interpolate import RBFInterpolator
    zone = set(np.unique(Q[rd['faces']]).tolist()) - set(rd['loop'].tolist())
    d = V - rd['O']; cand = np.nonzero((np.linalg.norm(d, axis=1) < radius) & (sg * V[:, 0] > 0) & ((d @ rd['n']) > -2.5))[0]
    cand = np.array([v for v in cand if v not in zone]); bu = np.c_[d[cand] @ rd['b'], d[cand] @ rd['u']]; h = d[cand] @ rd['n']
    return RBFInterpolator(bu, h, kernel='thin_plate_spline', smoothing=0.01), cand

def _inside_dist(poly, pts):
    """signed distance of pts to a closed polygon (positive inside)"""
    from matplotlib.path import Path
    inside = Path(poly).contains_points(pts); a = poly; b = np.roll(poly, -1, 0); best = np.full(len(pts), 1e9)
    for p0, p1 in zip(a, b):
        e = p1 - p0; t = np.clip(((pts - p0) @ e) / (e @ e), 0, 1); best = np.minimum(best, np.linalg.norm(pts - (p0 + t[:, None] * e), axis=1))
    return np.where(inside, best, -best)

# ------------------------------------------------------------------ realization
def head_scale(r6_path):
    import importlib.util, sys as _s
    _s.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001'); import fn_face_metrics as FM
    t = FM.load(r6_path); V = t['V']; HH = float(V[FM.LM['vertex'], 2] - V[FM.LM['menton'], 2]); return HH, HH / HH_MF

def ear_sheet(Lo, p, sc):
    """front / back / rim positions in the ear frame (lateral X, posterior y, up z), cm at head scale; h0 not yet applied"""
    ip = InPlane(p); st = Lo['st']; part = Lo['part']; S, T = st[:, 0], st[:, 1]
    base, N, d = ip.bent(S, T); rel, th, parts = relief(S, T, p)
    g = ip.g
    if g.get('lobe_lift_end') is not None and g.get('lobe_thin', 0.0) > 0:    # v002 target D: the attached lobe front thins into the skin
        att = (1 - smooth((T + 1) / g.get('lobe_lift_tw', 0.5))) * smooth((S - (g['lobe_lift_end'] - g.get('lobe_lift_w', 0.04))) / g.get('lobe_lift_w', 0.04)) * smooth((S0 - S) / 0.05)
        th = th * (1 - g['lobe_thin'] * att)
    X = np.zeros((len(st), 3)); fr = part == 'front'; bk = part == 'back'
    X[fr] = base[fr] + rel[fr, None] * N[fr]; rb = np.minimum(rel, BACK_RIDGE * rel); X[bk] = base[bk] + (rb[bk] - th[bk])[:, None] * N[bk]
    X *= sc
    return X, N, d, rel, th, parts, ip

def rim_fill(Lo, X, N):
    """rim interior rows: half-round from the front row to the back row, bulging outward along the outline"""
    idx = Lo['idx']; na, m, jf, Kr = [Lo['topo'][k] for k in ('n_a', 'm', 'j_f', 'K_r')]; path = Lo['info']['path']
    fk = lambda pk: idx[('F', 0, pk[1])] if pk[0] == 'D' else (idx[('F', pk[1], m)] if pk[0] == 'C' else idx[('F', na, pk[1])])
    gk = lambda pk: idx[('G', 0, pk[1] - jf)] if pk[0] == 'D' else (idx[('G', pk[1], m - jf)] if pk[0] == 'C' else idx[('G', na, pk[1] - jf)])
    ik = lambda pk: idx[('F', 1, pk[1])] if pk[0] == 'D' else (idx[('F', pk[1], m - 1)] if pk[0] == 'C' else idx[('F', na - 1, pk[1])])
    P = [X[fk(pk)] for pk in path]
    for q, pk in enumerate(path):
        f, g = X[fk(pk)], X[gk(pk)]; mid = 0.5 * (f + g); r = 0.5 * np.linalg.norm(f - g)
        tq = P[min(q + 1, len(P) - 1)] - P[max(q - 1, 0)]; nn = f - g; nn /= np.linalg.norm(nn) + 1e-12
        o = np.cross(nn, tq); o /= np.linalg.norm(o) + 1e-12
        if o @ (f - X[ik(pk)]) < 0: o = -o
        for rr in range(1, Kr):
            th_ = np.pi * rr / Kr; X[idx[('R', rr, q)]] = mid + np.cos(th_) * (f - mid) + np.sin(th_) * r * o
    return X

def hermite(P0, T0, P1, T1, u, k0=1.0, k1=1.0):
    L = np.linalg.norm(P1 - P0, axis=-1, keepdims=True); u = np.asarray(u, float)[..., None]
    h00 = 2 * u ** 3 - 3 * u ** 2 + 1; h10 = u ** 3 - 2 * u ** 2 + u; h01 = -2 * u ** 3 + 3 * u ** 2; h11 = u ** 3 - u ** 2
    return h00 * P0 + h10 * (k0 * L) * T0 + h01 * P1 + h11 * (k1 * L) * T1

def realize(Lo, rd, skull, p, sc, canon=None, geo=GEO, beta_r=3.0):
    """one side, one candidate. Returns dict with patch vertex positions (sheet + cuff rings), faces with global-ready refs, records.
    canon: dict(off=ring1 offset, place=(db,du)?) -- off is canonical (fixed); placement is per head (deterministic rule)."""
    n1, bfaces, anchors = root_band([int(c) for c in rd['inner']]); assert n1 == 52
    Xe, N, d, rel, th, parts, ip = ear_sheet(Lo, p, sc); Xe = rim_fill2(Lo, Xe)
    J = Lo['J']
    poly = np.c_[(rd['V_loop'] - rd['O']) @ rd['b'], (rd['V_loop'] - rd['O']) @ rd['u']]
    # placement: maximise the worst normalised margin of the junction ring inside the root footprint
    Jbu = Xe[J][:, 1:3]; Jh = np.maximum(Xe[J][:, 0] - Xe[J][:, 0].min(), 0)
    c_fp = poly.mean(0); c_J = Jbu.mean(0); best = None
    for db in np.arange(-1.5, 1.51, 0.05):
        for du in np.arange(-1.5, 1.51, 0.05):
            off = c_fp - c_J + np.array([db, du]); m_ = _inside_dist(poly, Jbu + off); sc_ = (m_ / (0.35 + Jh)).min()
            if best is None or sc_ > best[0]: best = (sc_, off, m_.min())
    off = best[1]; bu = Xe[:, 1:3] + off; cJ = Jbu.mean(0) + off
    r = np.linalg.norm(bu - cJ, axis=1); beta = np.exp(-(r / beta_r) ** 2); sh = skull(bu)
    # base height: concha / bridge clearance over the skull field (front sheet vertices within the footprint influence)
    fr = Lo['part'] == 'front'; lat0 = Xe[:, 0] - sh; w_ = fr & (beta > 0.4)          # rigid ear in the root frame; clearance vs the true skull
    h0 = geo['clear'] - lat0[w_].min()
    lat = h0 + Xe[:, 0]
    W = rd['O'] + bu[:, :1] * rd['b'] + bu[:, 1:] * rd['u'] + lat[:, None] * rd['n']
    for k_ in ('c0', 'c1'):                                   # attachment corners dip into the root crease: bridge corner quads stay convex in 3-D
        W[Lo['info']['corners'][k_]] -= geo.get('corner_dip', 0.0) * rd['n']
    # cuff chains: one curve per J vertex from its (virtual) root anchor to the J vertex
    Jw = W[J]; Jd = W[Lo['Jdir'][:, 1]] - W[Lo['Jdir'][:, 0]]; Jd /= np.linalg.norm(Jd, axis=1, keepdims=True)
    anc_P = np.array([rd['V_loop'][a].mean(0) for a in anchors]); anc_T = np.array([rd['T'][a].mean(0) for a in anchors]); anc_T /= np.linalg.norm(anc_T, axis=1, keepdims=True)
    rn = {}                                                    # root neighbours of each ring-1 vertex through the root band
    for f in bfaces:
        f = [tuple(v) for v in f]
        for a_ in range(4):
            p_, q_ = f[a_], f[(a_ + 1) % 4]
            if p_[0] == 'e' and q_[0] == 'r': rn.setdefault(p_[1], set()).add(q_[1])
            if q_[0] == 'e' and p_[0] == 'r': rn.setdefault(q_[1], set()).add(p_[1])
    xs = {j_ for j_ in range(52) if len(rn.get(j_, ())) == 0}; ms = {j_ for j_ in range(52) if len(rn.get(j_, ())) >= 2}
    ring_pos, ccanon, Jord = cuff_build3(rd, anc_P, anc_T, Jw, skull, canon=(canon or {}).get('cuff'), root_faces=bfaces, ring1_guard=(xs, ms))
    canon = dict(canon or {}, cuff=ccanon)
    rec = dict(place_offset_cm=off.tolist(), place_score=float(best[0]), min_margin_cm=float(best[2]), h0_cm=float(h0), scale=float(sc), canon=canon,
               junction_mean_height_cm=float((lat[J] - sh[J]).mean()))
    return dict(W=W, ring_pos=ring_pos, Jord=Jord, bfaces=bfaces, anchors=anchors, rec=rec, Xe=Xe, beta=beta, sh=sh, lat=lat, bu=bu, rel=rel, th=th, parts=parts, d=d, ip=ip)

def patch_mesh(Lo, R, loop):
    """local patch: vertex array (sheet + cuff rings) and faces with root refs as negative (-1 - k for loop index k)"""
    ns = len(Lo['st']); J = Lo['J']; nR = len(R['ring_pos']); base = {}; nxt = ns; P = [R['W']]
    for k in range(nR): base[k] = nxt; nxt += len(R['ring_pos'][k]); P.append(R['ring_pos'][k])
    P = np.concatenate(P); F = [list(map(int, f)) for f in Lo['F']]
    for k, bd in enumerate(R['rec']['canon']['cuff']['bands']):
        for f in bd['faces']:
            F.append([base[k] + i if t == 'b' else (base[k + 1] + i if k + 1 < nR else int(J[R['Jord'][i]])) for t, i in f])
    for f in R['bfaces']: F.append([(-1 - k) if t == 'r' else base[0] + k for t, k in f])
    return P, np.array(F), base

# ------------------------------------------------------------------ cuff v2: angular rings + DP-matched quad bands (+ / - 2 transitions)
CUFF_SIZES = (52, 56, 60, 64, 68)           # ring1 .. ring5; J (70) on top (v001)
# v002 cuff transition rule: the v001 DP rule is retained (sizes, pole penalty, valence guards). Order 0d9c70b R1 tested regular end bands
# (52/52/58/64/70), the minimum-transition DP (penalty 2.0) and angular staggering (0.2-1.0): every variant gave more skewed cells and more
# contacts after fairing, so the v002 cuff gain comes from the 3-D quality pass (ear_quality3d.py) on the unchanged transition rule.
CUFF_SIZES_V2 = (52, 56, 60, 64, 68)
POLE_PEN_V2 = 0.5; STAGGER_V2 = 0.0
_cv = json.loads(__import__('os').environ.get('EAR_CUFF', '{}'))
CUFF_SIZES_V2 = tuple(_cv.get('sizes', CUFF_SIZES_V2)); POLE_PEN_V2 = float(_cv.get('pen', POLE_PEN_V2)); STAGGER_V2 = float(_cv.get('stag', STAGGER_V2))
POLE_PEN = 0.5
BACK_RIDGE = 0.5                            # back (cranial) surface follows the front relief fully in hollows, half on ridges

def _ang(bu, c):
    a = np.unwrap(np.arctan2(bu[:, 1] - c[1], bu[:, 0] - c[0])); return a

def _quantile_angles(theta, n):
    """n angles following the distribution of the (monotone, unwrapped, period 2pi) sequence theta"""
    th = np.maximum.accumulate(theta - theta[0]) + theta[0]; m = len(th); x = np.r_[np.arange(m), m]; y = np.r_[th, th[0] + 2 * np.pi]
    return np.interp(np.arange(n) * m / n, x, y)

def _band_dp(tb, tt, pen=POLE_PEN, no_mid=frozenset(), no_src=frozenset(), avoid=(), stag=0.0, stag_w=0.35):
    """quad band between bottom angles tb (nb) and top angles tt (nt), both increasing, cyclic. Returns faces as (('b',i)|('t',j)) lists.
    Steps: (1,1) regular quad, (0,2) top-only quad (bottom source i gets 2 rungs), (2,0) bottom-only quad (bottom middle i+1 gets none).
    Valence guards: no two transition steps in a row; a bottom vertex in no_mid (already without a downward rung) is never a (2,0) middle,
    one in no_src (already carrying an extra downward rung) is never a (0,2) source -- so no valence-2 or valence-6 vertex is created."""
    nb, nt = len(tb), len(tt); tb2 = np.r_[tb, tb + 2 * np.pi, tb + 4 * np.pi]; best = None
    for j0 in range(nt):                                    # start rung b0 - t_j0 (shift tt by 2pi multiples to be near tb[0])
        tt2 = np.r_[tt, tt + 2 * np.pi, tt + 4 * np.pi] - 2 * np.pi * np.round((tt[j0] - tb[0]) / (2 * np.pi))
        if abs(tt2[j0] - tb2[0]) > 0.6: continue
        INF = 1e18; C = np.full((nb + 1, nt + 1, 2), INF); B = np.zeros((nb + 1, nt + 1, 2, 2), np.int8); C[0, 0, 1] = 0   # start as after a transition (wrap guard)
        for i in range(nb + 1):
            for j in range(nt + 1):
                for lt in (0, 1):
                    c0 = C[i, j, lt]
                    if c0 >= INF: continue
                    for st, (di, dj, pp) in enumerate(((1, 1, 0.0), (0, 2, pen), (2, 0, pen))):
                        if st and lt: continue
                        if st == 1 and (i % nb) in no_src: continue
                        if st == 2 and ((i + 1) % nb) in no_mid: continue
                        ii, jj = i + di, j + dj
                        if ii > nb or jj > nt: continue
                        nl = 1 if st else 0; c = c0 + pp + abs(tb2[ii] - tt2[j0 + jj])
                        if st and stag > 0 and len(avoid):                        # v002: stagger transitions against the previous band's
                            ang_ = tb2[min(i, len(tb2) - 1)] % (2 * np.pi); dd_ = np.abs((np.asarray(avoid) - ang_ + np.pi) % (2 * np.pi) - np.pi)
                            c += stag * float(np.exp(-(dd_ / stag_w) ** 2).sum())
                        if c < C[ii, jj, nl]: C[ii, jj, nl] = c; B[ii, jj, nl] = (st, lt)
        end = min((C[nb, nt, 0], 0), (C[nb, nt, 1], 1))
        if end[0] < INF and (best is None or end[0] < best[0]):
            i, j, lt = nb, nt, end[1]; steps = []
            while (i, j) != (0, 0):
                st, pl = B[i, j, lt]; steps.append((i, j, int(st))); di, dj = ((1, 1), (0, 2), (2, 0))[st]; i -= di; j -= dj; lt = pl
            best = (end[0], j0, steps[::-1])
    cost, j0, steps = best; faces = []
    for (i, j, st) in steps:
        bi = lambda k: ('b', k % nb); tj = lambda k: ('t', (j0 + k) % nt)
        if st == 0: faces.append([bi(i - 1), bi(i), tj(j), tj(j - 1)])
        elif st == 1: faces.append([bi(i), tj(j), tj(j - 1), tj(j - 2)])
        else: faces.append([bi(i - 2), bi(i - 1), bi(i), tj(j)])
    tr_ang = [float(tb2[min(i, len(tb2) - 1)] % (2 * np.pi)) for (i, j, st) in steps if st]
    return faces, dict(cost=float(cost), j0=int(j0), transitions=int(sum(1 for s in steps if s[2] != 0)), transition_angles=tr_ang)

def _interp_loop(theta, X, q):
    """periodic linear interpolation of per-vertex data X (n x k) at angles q along increasing theta"""
    th = np.maximum.accumulate(theta - theta[0]) + theta[0]; x = np.r_[th, th[0] + 2 * np.pi]; Y = np.r_[X, X[:1]]
    qq = th[0] + np.mod(q - th[0], 2 * np.pi); return np.stack([np.interp(qq, x, Y[:, k]) for k in range(Y.shape[1])], 1)

def cuff_build(rd, anc_P, anc_T, Jw, Jd, skull, canon=None, smooth_it=6):
    """rings ring1 (= root-band ring, anchored) .. ring5 and DP bands up to the junction ring J.
    Topology (ring sizes, band faces, J orientation) is canonical when `canon` is given."""
    O, b_, u_, n_ = rd['O'], rd['b'], rd['u'], rd['n']; bu = lambda X: np.c_[(X - O) @ b_, (X - O) @ u_]
    c = bu(Jw).mean(0); Lw = rd['V_loop']; tL = _ang(bu(Lw), c); sense = np.sign(tL[-1] - tL[0])
    tJ = _ang(bu(Jw), c); rev = bool(np.sign(tJ[-1] - tJ[0]) != sense) if canon is None else canon['J_reversed']
    Jord = np.arange(len(Jw))[::-1] if rev else np.arange(len(Jw)); tJ = _ang(bu(Jw[Jord]), c) * sense
    tA = _ang(bu(anc_P), c) * sense; tLs = tL * sense
    # align branches of the unwrapped angles
    tJ = tJ - 2 * np.pi * np.round((tJ[0] - tLs[0]) / (2 * np.pi)); tA = tA - 2 * np.pi * np.round((tA[0] - tLs[0]) / (2 * np.pi))
    nR = len(CUFF_SIZES); us = [(k + 1) / (nR + 1) for k in range(nR)]
    Jdat = np.c_[Jw[Jord], Jd[Jord]]; Ldat = np.c_[Lw, rd['T']]
    ring_th = [tA]
    for k in range(1, nR):
        w = us[k]; qA = _quantile_angles(tA, CUFF_SIZES[k]); qJ = _quantile_angles(tJ, CUFF_SIZES[k])
        ring_th.append((1 - w) * qA + w * qJ)
    pos = []
    for k in range(nR):
        q = ring_th[k]; J_ = _interp_loop(tJ, Jdat, q)
        if k == 0: P0, T0 = anc_P, anc_T
        else: L_ = _interp_loop(tLs, Ldat, q); P0, T0 = L_[:, :3], L_[:, 3:]
        T0 = T0 / np.linalg.norm(T0, axis=1, keepdims=True); T1 = J_[:, 3:] / np.linalg.norm(J_[:, 3:], axis=1, keepdims=True)
        pos.append(hermite(P0, T0, J_[:, :3], T1, us[k]))
    if canon is None:
        bands = []
        for k in range(nR):
            tb = np.maximum.accumulate(ring_th[k]); tt = np.maximum.accumulate(ring_th[k + 1] if k + 1 < nR else tJ)
            f, info = _band_dp(tb, tt); bands.append(dict(faces=f, info=info))
        canon = dict(J_reversed=rev, sizes=list(CUFF_SIZES), bands=bands)
    # relax ring vertices (3D Laplacian on the cuff graph, root loop and J fixed), keep above the skull field
    allpos = pos; nbr = {}
    def key(k, i): return (k, i)
    for k, bd in enumerate(canon['bands']):
        for f in bd['faces']:
            ids = [(k, i) if t == 'b' else ((k + 1, i) if k + 1 < nR else ('J', int(Jord[i]))) for t, i in f]
            for a_ in range(4):
                p_, q_ = ids[a_], ids[(a_ + 1) % 4]; nbr.setdefault(p_, set()).add(q_); nbr.setdefault(q_, set()).add(p_)
    def get(idk):
        return Jw[idk[1]] if idk[0] == 'J' else allpos[idk[0]][idk[1]]
    # ring1 also touches the root loop through the root band: approximate with its anchor
    for it in range(smooth_it):
        new = [p.copy() for p in allpos]
        for k in range(nR):
            for i in range(len(allpos[k])):
                nb_ = list(nbr.get((k, i), []))
                if not nb_: continue
                m_ = np.mean([get(x) for x in nb_], 0)
                if k == 0: m_ = 0.5 * m_ + 0.5 * anc_P[i]
                new[k][i] = 0.5 * allpos[k][i] + 0.5 * m_
        allpos = new
    for k in range(nR):
        P_ = allpos[k]; d_ = P_ - O; la = d_ @ n_; sk = skull(np.c_[d_ @ b_, d_ @ u_]); allpos[k] = P_ + (np.maximum(la, sk + 0.01) - la)[:, None] * n_
    return allpos, canon, Jord

# ------------------------------------------------------------------ layout v2: bridge + crescent (F1) + upper-extension kite (F2)
TOPO2 = dict(n_a=28, u1=16, kb=12, j_f=3, K_r=4)        # kappa_a = n_a - u1 = 12; J = 2 (n_a + j_f + K_r) = 70
ANG_W = 0.5
UP_FREE, UP_SLIDE = True, 0.01
S_UP = 0.52                                              # posterior rim point where the upper extension starts (F1 / F2 cut)

def layout2(p=CAND['E2'], topo=TOPO2):
    na, u1, kb, jf, Kr = [topo[k] for k in ('n_a', 'u1', 'kb', 'j_f', 'K_r')]; ka = na - u1; ip = InPlane(p)
    side = lambda st: ip.flat(st[:, 0], st[:, 1])
    def arc_split(st_dense, L0):
        X = side(st_dense); c = np.r_[0, np.cumsum(np.linalg.norm(np.diff(X, axis=0), axis=1))]; return int(np.searchsorted(c, L0))
    lamA = np.linspace(0, 1, 4000); Ad = np.c_[S0 + (S1 - S0) * lamA, -1 - A_BOW * np.sin(np.pi * lamA) ** A_EX]
    XA = side_ = ip.flat(Ad[:, 0], Ad[:, 1]); cA = np.r_[0, np.cumsum(np.linalg.norm(np.diff(XA, axis=0), axis=1))]; cA /= cA[-1]
    wA = 1 + A_END * np.abs(2 * (np.arange(na) + 0.5) / na - 1) ** 3; uA = np.r_[0, np.cumsum(wA)] / wA.sum()   # coarser end edges at the corners
    A = np.c_[np.interp(uA, cA, Ad[:, 0]), np.interp(uA, cA, Ad[:, 1])]; A[0] = (S0, -1.0); A[-1] = (S1, -1.0)
    Bd = _curve_st([(S1, -1, 1.0, -1)]); k = arc_split(Bd, DATT); Batt = _resample(Bd[:k + 1], ip, jf)
    Dd = _curve_st([(S0, -1, 0.0, -1)]); k2 = arc_split(Dd, DATT_D); Datt = _resample(Dd[:k2 + 1], ip, jf)
    c0f, c1f = Datt[-1], Batt[-1]
    Ant = _resample(np.r_[Bd[k:], [[1.0, 0.0]]], ip, kb, grade=0.7)                        # c1f -> tip
    Dp = _resample(np.r_[Dd[k2:], _curve_st([(0.0, 1, S3, 1)])], ip, kb)                     # c0f -> lobe -> P_lo
    Plow = _resample(_curve_st([(S3, 1, S_UP, 1)]), ip, u1)                                 # P_lo -> P_up
    Pup = _resample(np.r_[_curve_st([(S_UP, 1, 1.0, 1)]), [[1.0, 0.0]]], ip, ka, grade=0.6)  # P_up -> tip
    lam = np.linspace(0, 1, 4000); Ust = np.c_[c0f[0] + (c1f[0] - c0f[0]) * lam, -1 + (U_T + 1) * np.sin(np.pi * lam) ** U_EX]
    U = _resample(Ust, ip, na); U[0] = c0f; U[-1] = c1f; Y = U[u1]
    cut = np.c_[np.linspace(Y[0], S_UP, 2000), np.linspace(Y[1], 1.0, 2000)]; Cut = _resample(cut, ip, kb); Cut[-1] = Plow[-1]
    blocks = dict(bridge=(A, U, Datt, Batt, ('front',)), F1=(U[:u1 + 1], Plow, Dp, Cut, ('front', 'back')), F2=(U[u1:], Pup, Cut, Ant, ('front', 'back')))
    sd = np.linspace(0, 1, 801); td = np.linspace(-1.6, 1, 521); SS, TT = np.meshgrid(sd, td, indexing='ij'); G = np.c_[SS.ravel(), TT.ravel()]
    tree = cKDTree(ip.flat(G[:, 0], G[:, 1])); grids = {}; err = 0.0
    for nm, (a_, c_, d_, b_, sh) in blocks.items():
        X = _winslow(_tfi(side(a_), side(c_), side(d_), side(b_))); st = np.zeros(X.shape[:2] + (2,))
        inner = X[1:-1, 1:-1].reshape(-1, 2)
        if len(inner):
            s_, e_ = _invert(inner, ip, tree, G); st[1:-1, 1:-1] = s_.reshape(X.shape[0] - 2, X.shape[1] - 2, 2); err = max(err, float(e_.max()))
        st[:, 0] = a_; st[:, -1] = c_; st[0, :] = d_; st[-1, :] = b_; grids[nm] = (st, sh)
    idx = {}; sts = []; part = []
    def vid(sheet, s_t):
        key = (sheet, round(float(s_t[0]), 9), round(float(s_t[1]), 9))
        if key not in idx: idx[key] = len(sts); sts.append(np.array(s_t, float)); part.append(sheet)
        return idx[key]
    F = []; FB = []
    for nm, (st, sh) in grids.items():
        for sheet in sh:
            ni, nj = st.shape[0] - 1, st.shape[1] - 1; ids = [[vid(sheet, st[i, j]) for j in range(nj + 1)] for i in range(ni + 1)]
            for i in range(ni):
                for j in range(nj): F.append([ids[i][j], ids[i + 1][j], ids[i + 1][j + 1], ids[i][j + 1]]); FB.append(nm + '_' + sheet)
    path = np.r_[Dp, Plow[1:], Pup[1:], Ant[::-1][1:]]                                   # c0f ... tip ... c1f
    fr = [vid('front', q) for q in path]; bk = [vid('back', q) for q in path]; rim = []
    for q in range(len(path)):
        row = [fr[q]]
        for r in range(1, Kr): idx[('rim', r, q)] = len(sts); sts.append(path[q].copy()); part.append('rim'); row.append(len(sts) - 1)
        row.append(bk[q]); rim.append(row)
    for q in range(len(path) - 1):
        for r in range(Kr): F.append([rim[q][r], rim[q + 1][r], rim[q + 1][r + 1], rim[q][r + 1]]); FB.append('rim_up' if min(path[q][0], path[q + 1][0]) >= S_UP and q >= len(Dp) - 1 else 'rim')
    J = [vid('front', q) for q in A] + [vid('front', q) for q in Batt[1:]] + rim[-1][1:] + [vid('back', q) for q in U[::-1][1:]]
    J += rim[0][1:][::-1][1:] + [vid('front', q) for q in Datt[::-1][:-1]]
    Jseg = ['A'] * (na + 1) + ['Batt'] * jf + ['rimB'] * (Kr - 1) + ['U'] * (na + 1) + ['rimD'] * (Kr - 1) + ['Datt'] * jf
    assert len(J) == 2 * (na + jf + Kr) and len(set(J)) == len(J), (len(J), len(set(J)))
    F = np.array(F); sts = np.array(sts); part = np.array(part)
    # interior direction at each J vertex: mean direction to its sheet neighbours that are not on J
    nb = {}
    for f in F:
        for a_ in range(4): nb.setdefault(f[a_], set()).update({f[(a_ + 1) % 4], f[(a_ - 1) % 4]})
    Js = set(J); Jdir = []
    for v in J:
        ws = [w for w in nb[v] if w not in Js]
        if not ws:                                            # block corner on J: use the diagonal of its face
            f = [f for f in F if v in f][0]; ws = [int(f[(list(f).index(v) + 2) % 4])]
        Jdir.append([v, ws[0]])
    Jnb = {int(v): [int(w) for w in nb[v] if w not in Js] for v in J}
    rimrow = np.array([[fr[q], bk[q]] for q in range(len(path))])
    inward = {}
    pathset = set(fr)
    for q, v in enumerate(fr):
        ws = [w for w in nb[v] if part[w] == 'front' and w not in pathset]; inward[q] = ws[0] if ws else (fr[q + 1] if q + 1 < len(fr) else fr[q - 1])
    corners = dict(c0=vid('front', A[0]), c1=vid('front', A[-1]), c0f=vid('front', c0f), c1f=vid('front', c1f), Y=vid('front', Y), P_lo=vid('front', Plow[0]),
                   P_up=vid('front', Plow[-1]), tip=vid('front', Pup[-1]), tip_b=vid('back', Pup[-1]))
    return dict(st=sts, part=part, F=F, J=np.array(J), Jseg=Jseg, Jdir=np.array(Jdir), Jnb=Jnb, rim=rim, rim_inward=inward, idx=idx,
                info=dict(corners=corners, inv_err_max=err, path_edges=len(path) - 1), topo=dict(topo, ka=ka), face_block_list=FB)

def rim_fill2(Lo, X):
    Kr = Lo['topo']['K_r']; rim = Lo['rim']; P = np.array([X[r[0]] for r in rim])
    for q, row in enumerate(rim):
        f, g = X[row[0]], X[row[-1]]; mid = 0.5 * (f + g); r = 0.5 * np.linalg.norm(f - g)
        tq = P[min(q + 1, len(P) - 1)] - P[max(q - 1, 0)]; nn = (f - g) / (np.linalg.norm(f - g) + 1e-12)
        o = np.cross(nn, tq); o /= np.linalg.norm(o) + 1e-12
        if o @ (f - X[Lo['rim_inward'][q]]) < 0: o = -o
        for rr in range(1, Kr):
            th_ = np.pi * rr / Kr; X[row[rr]] = mid + np.cos(th_) * (f - mid) + np.sin(th_) * r * o
    return X

# ------------------------------------------------------------------ 2-D quad optimisation of the canonical sheet layout
def _cyc_neighbors(F, nV):
    """ordered one-ring (by angle later) neighbour lists"""
    nb = [set() for _ in range(nV)]
    for f in F:
        for k in range(4): nb[f[k]].update({f[(k + 1) % 4], f[(k - 1) % 4]})
    return [np.array(sorted(s)) for s in nb]

def _quad_angles2(X, F):
    P = X[F]; ang = []
    for k in range(4):
        u = P[:, (k - 1) % 4] - P[:, k]; w = P[:, (k + 1) % 4] - P[:, k]
        c = (u * w).sum(1) / (np.linalg.norm(u, axis=1) * np.linalg.norm(w, axis=1) + 1e-12); ang.append(np.degrees(np.arccos(np.clip(c, -1, 1))))
    return np.stack(ang, 1)

def optimise_sheet(Lo, p=CAND['E2'], it=400, verbose=False):
    """angle-based (Zhou-Shimada) + Laplacian smoothing of the FRONT sheet layout in the in-plane metric; outline vertices slide along the
    outline, block corners fixed. The back sheet shares the free-region positions. Updates Lo['st'] in place."""
    ip = InPlane(p); st = Lo['st']; part = Lo['part']; F = Lo['F']; fr = np.nonzero(part == 'front')[0]
    Ff = F[(part[F] == 'front').all(1)]; X = ip.flat(st[:, 0], st[:, 1]).copy()
    nb = _cyc_neighbors(Ff, len(st))
    # outline polyline (anterior t=-1 from s=0..1, tip, posterior t=+1 from 1..0) in (s,t) and in-plane
    so = np.linspace(0, 1, 3000); OL = np.r_[[[1.0, 0.0]], np.c_[so[::-1], -np.ones_like(so)], np.c_[so[1:], np.ones_like(so[1:])], [[1.0, 0.0]]]; OX = ip.flat(OL[:, 0], OL[:, 1])
    on_out = np.array([abs(abs(st[v, 1]) - 1) < 1e-9 or (abs(st[v, 0] - 1) < 1e-9) or st[v, 0] < 1e-9 for v in range(len(st))]) & (part == 'front')
    cs = Lo['info']['corners']; fixed = np.zeros(len(st), bool)
    for k in ('c0', 'c1', 'c0f', 'c1f', 'P_lo', 'P_up', 'tip'): fixed[cs[k]] = True
    upper = (st[:, 0] > S_UP - 1e-9) & on_out                       # upper-extension outline keeps its authored (tip-graded) spacing
    upper0 = upper.copy()
    if not UP_FREE: fixed |= upper
    ukeys = {(round(float(st[v, 0]), 9), round(float(st[v, 1]), 9)) for v, sg in zip(Lo['J'], Lo['Jseg']) if sg == 'U'}
    for v in Lo['J']: fixed[v] = True                                # the junction ring (attachment) is fixed
    for v in fr:                                                    # the attachment notch U (behind the concha) is a fixed feature line
        if (round(float(st[v, 0]), 9), round(float(st[v, 1]), 9)) in ukeys: fixed[v] = True
    free_in = np.array([v for v in fr if not on_out[v] and not fixed[v]]); slide = np.array([v for v in fr if on_out[v] and not fixed[v]])
    otree = cKDTree(OX); OC = np.r_[0, np.cumsum(np.linalg.norm(np.diff(OX, axis=0), axis=1))]
    tau = {v: OC[otree.query(X[v])[1]] for v in np.nonzero(on_out)[0]}; tau_n = dict(tau)
    def stats():
        a = _quad_angles2(X, Ff); return int(((a < 45) | (a > 135)).any(1).sum()), float(a.min()), float(a.max())
    s0 = stats()
    for k in range(it):
        Xn = X.copy()
        for v in free_in:
            ns = nb[v]; d = X[ns] - X[v]; order = np.argsort(np.arctan2(d[:, 1], d[:, 0])); ns = ns[order]; m = len(ns); cand = []
            for j in range(m):
                pj = X[ns[j]]; a1 = X[ns[(j - 1) % m]] - pj; a2 = X[ns[(j + 1) % m]] - pj; vv = X[v] - pj; L = np.linalg.norm(vv)
                bis = a1 / (np.linalg.norm(a1) + 1e-12) + a2 / (np.linalg.norm(a2) + 1e-12)
                if np.linalg.norm(bis) < 1e-9: cand.append(X[v]); continue
                bis /= np.linalg.norm(bis)
                if bis @ vv < 0: bis = -bis
                cand.append(pj + L * bis)
            Xn[v] = ANG_W * np.mean(cand, 0) + (1 - ANG_W) * X[ns].mean(0)
        for v in slide:                                              # sliding along the outline: spacing (arc midpoint) + weak orthogonal foot
            bnd = [w for w in nb[v] if on_out[w]]; ns = [w for w in nb[v] if not on_out[w]]
            tb = [(tau[w] if w != cs['tip'] else (0.0 if tau[v] < 0.5 * OC[-1] else OC[-1])) for w in bnd]; tm = 0.5 * (tb[0] + tb[1]) if len(tb) == 2 else tau[v]
            if ns: _, i = otree.query(X[ns].mean(0)); tf = OC[i]
            else: tf = tm
            wf_ = UP_SLIDE if upper0[v] else 0.15; tau_n[v] = (1 - wf_) * tm + wf_ * tf
        for v in slide:
            tau[v] = tau_n[v]; Xn[v] = np.array([np.interp(tau[v], OC, OX[:, 0]), np.interp(tau[v], OC, OX[:, 1])])
        X = Xn
        if verbose and k % 100 == 0: print(k, stats())
    s1 = stats()
    # back to (s, t); outline vertices take the outline parameters directly
    sd = np.linspace(0, 1, 801); td = np.linspace(-1.6, 1, 521); SS, TT = np.meshgrid(sd, td, indexing='ij'); G = np.c_[SS.ravel(), TT.ravel()]
    tree = cKDTree(ip.flat(G[:, 0], G[:, 1])); new = st.copy()
    if len(free_in): new[free_in], e = _invert(X[free_in], ip, tree, G)
    for v in slide: i = int(np.argmin(np.abs(OC - tau[v]))); new[v] = OL[i]
    # back-sheet and rim copies follow the front vertex at the same (old) parameter
    key = {('front', round(float(st[v, 0]), 9), round(float(st[v, 1]), 9)): v for v in fr}
    for v in np.nonzero(part == 'back')[0]:
        w = key.get(('front', round(float(st[v, 0]), 9), round(float(st[v, 1]), 9)))
        if w is not None: new[v] = new[w]
    for row in Lo['rim']:
        for r in row[1:-1]: new[r] = new[row[0]]
    Lo['st'] = new; Lo['info']['opt'] = dict(before=s0, after=s1, iterations=it); Lo['dbgX'] = X
    return Lo

_CL = {}
import os as _os
TOPO_VERSION = _os.environ.get('EAR_TOPO', 'v002')          # 'v001' reproduces order bdcd6a6; 'v002' = order 0d9c70b (ear_layout3)
GEO_V2 = dict(lobe_lift_end=0.0974, lobe_lift_w=0.04, lobe_lift_tw=0.5, lobe_lift_att=0.4, lobe_thin=0.6)   # v002 target D: attached lobe front (c0f s = 0.0974)
#   stands off the skin less (lift x (1 - 0.4 att)) and thins into the skin (thickness x (1 - 0.6 att)); the free lobe is unchanged
GEO_V2.update(json.loads(_os.environ.get('EAR_GEO', '{}')))
if TOPO_VERSION != 'v001': GEO.update(GEO_V2)
LAYOUT3_KW = dict(h_red=0.9, cap=1.8, gap=2, stagger=1, a_ex=1.5,     # a_ex: attachment-line end shape (v001 0.7), target C
                  step_min=0.6, h_red_last=1.6, cap_d=0.35)          # R2: rows tighten to the tip; last 4 -> 2 reduction earlier; cap over the last 0.35 cm
LAYOUT3_KW.update(json.loads(_os.environ.get('EAR_L3', '{}')))
QUALITY_KW = dict(lo=55.0, hi=125.0, mu=0.02, iters=2000)
SLIDE_W = 0.05
def canonical_layout():
    """the one shared branch sheet layout in the E2 (W1e FN-elven) metric; cached.
    v001: layout v2 (kite upper extension) + angle optimisation. v002: layout v3 (crescent F1' + tapered leaf) + angle optimisation + corner-angle energy pass."""
    if 'L' not in _CL:
        if TOPO_VERSION == 'v001': _CL['L'] = optimise_sheet(layout2(CAND['E2'], TOPO2), CAND['E2'], it=400)
        else:
            import ear_layout3 as L3
            _CL['L'] = L3.quality_sheet(L3.optimise_sheet3(L3.layout3(CAND['E2'], **LAYOUT3_KW), CAND['E2'], it=600, slide_w=SLIDE_W), CAND['E2'], **QUALITY_KW)
        _CL['L']['version'] = TOPO_VERSION
    return _CL['L']

# ------------------------------------------------------------------ cuff v3 positions: 2-D smoothed annulus over the root plane + rho^2 rise above the skull
CUFF_IT = 150
def cuff_build3(rd, anc_P, anc_T, Jw, skull, canon=None, band_faces=None, root_faces=None, ring1_guard=((), ())):
    O, b_, u_, n_ = rd['O'], rd['b'], rd['u'], rd['n']; bu = lambda X: np.c_[(X - O) @ b_, (X - O) @ u_]
    Jb = bu(Jw); c = Jb.mean(0); Lw = rd['V_loop']; Lb = bu(Lw); tL = _ang(Lb, c); sense = np.sign(tL[-1] - tL[0])
    tJ = _ang(Jb, c); rev = bool(np.sign(tJ[-1] - tJ[0]) != sense) if canon is None else canon['J_reversed']
    Jord = np.arange(len(Jw))[::-1] if rev else np.arange(len(Jw)); tJ = _ang(Jb[Jord], c) * sense
    Ab = bu(anc_P); tA = _ang(Ab, c) * sense; tLs = tL * sense
    tJ = tJ - 2 * np.pi * np.round((tJ[0] - tLs[0]) / (2 * np.pi)); tA = tA - 2 * np.pi * np.round((tA[0] - tLs[0]) / (2 * np.pi))
    SZ = CUFF_SIZES if TOPO_VERSION == 'v001' else CUFF_SIZES_V2
    nR = len(SZ); rho = [(k + 1) / (nR + 1) for k in range(nR)]
    ring_th = [tA] + [(1 - rho[k]) * _quantile_angles(tA, SZ[k]) + rho[k] * _quantile_angles(tJ, SZ[k]) for k in range(1, nR)]
    P2 = []
    for k in range(nR):
        q = ring_th[k]; Jq = _interp_loop(tJ, Jb[Jord], q); Rq = Ab if k == 0 else _interp_loop(tLs, Lb, q)
        P2.append((1 - rho[k]) * Rq + rho[k] * Jq)
    if canon is None:
        bands = []; no_mid, no_src = set(ring1_guard[0]), set(ring1_guard[1]); prev_ang = []
        v2 = TOPO_VERSION != 'v001'
        for k in range(nR):
            tb = np.maximum.accumulate(ring_th[k]); tt = np.maximum.accumulate(ring_th[k + 1] if k + 1 < nR else tJ)
            f, info = _band_dp(tb, tt, pen=POLE_PEN_V2 if v2 else POLE_PEN, no_mid=frozenset(no_mid), no_src=frozenset(no_src),
                               avoid=prev_ang if v2 else (), stag=STAGGER_V2 if v2 else 0.0)
            bands.append(dict(faces=f, info=info)); prev_ang = prev_ang + info['transition_angles']
            no_mid, no_src = set(), set()                     # top-ring vertices of this band seen from the next band
            for q in f:
                tops = [i for t, i in q if t == 't']; bots = [i for t, i in q if t == 'b']
                if len(tops) == 3: no_mid.add(tops[1])        # top-only quad: its middle top vertex has no downward rung
                if len(bots) == 3: no_src.add(tops[0])        # bottom-only quad: its top vertex carries an extra downward rung
        canon = dict(J_reversed=rev, sizes=list(SZ), bands=bands)
    # graph over ring vertices (+ fixed J and root-loop neighbours) for 2-D smoothing
    off = np.cumsum([0] + [len(p) for p in P2]); nfree = off[-1]; X = np.concatenate(P2)
    fixedX = {}; nb = [set() for _ in range(nfree)]
    def gid(k, i): return ('J', int(Jord[i])) if k == nR else int(off[k] + i)
    for k, bd in enumerate(canon['bands']):
        for f in bd['faces']:
            ids = [gid(k, i) if t == 'b' else gid(k + 1, i) for t, i in f]
            for a_ in range(4):
                p_, q_ = ids[a_], ids[(a_ + 1) % 4]
                if isinstance(p_, int): nb[p_].add(q_)
                if isinstance(q_, int): nb[q_].add(p_)
    for f in root_faces:                                   # root band: ('r', k) loop vertex / ('e', j) ring1 vertex
        ids = [('R', k) if t == 'r' else int(off[0] + k) for t, k in f]
        for a_ in range(4):
            p_, q_ = ids[a_], ids[(a_ + 1) % 4]
            if isinstance(p_, int): nb[p_].add(q_)
            if isinstance(q_, int): nb[q_].add(p_)
    def pos(x, Xc): return Xc[x] if isinstance(x, (int, np.integer)) else (Jb[x[1]] if x[0] == 'J' else Lb[x[1]])
    nbl = [list(s) for s in nb]
    for it in range(CUFF_IT):
        Xn = X.copy()
        for v in range(nfree):
            P = np.array([pos(x, X) for x in nbl[v]]); d = P - X[v]; o = np.argsort(np.arctan2(d[:, 1], d[:, 0])); P = P[o]; m = len(P); cand = []
            for j in range(m):
                pj = P[j]; a1 = P[(j - 1) % m] - pj; a2 = P[(j + 1) % m] - pj; vv = X[v] - pj; L = np.linalg.norm(vv)
                bis = a1 / (np.linalg.norm(a1) + 1e-12) + a2 / (np.linalg.norm(a2) + 1e-12)
                if np.linalg.norm(bis) < 1e-9: cand.append(X[v]); continue
                bis /= np.linalg.norm(bis); bis = bis if bis @ vv >= 0 else -bis; cand.append(pj + L * bis)
            Xn[v] = 0.5 * np.mean(cand, 0) + 0.5 * P.mean(0)
        X = Xn
    # heights: rho^2 rise from the skull at the root to the junction height above the skull
    HJ = (Jw - O) @ n_ - skull(Jb); out = []
    for k in range(nR):
        Xk = X[off[k]:off[k + 1]]; qk = _ang(Xk, c) * sense
        Hq = _interp_loop(tJ, HJ[Jord][:, None], qk)[:, 0]; h = np.maximum(Hq, 0) * rho[k] ** 2 + skull(Xk)
        out.append(O + Xk[:, :1] * b_ + Xk[:, 1:] * u_ + h[:, None] * n_)
    return out, canon, Jord
