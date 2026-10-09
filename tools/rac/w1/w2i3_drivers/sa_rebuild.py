# RAC W2I3 reference-quality rebuild candidate (order §3-§8). COPIES ONLY: frozen SA-M / SA-F, tool-chain files and canon are never written.
#
# Accepted target (author rulings 1A-1C): L1 legs (+9.2 cm thigh at 188, funded 40 % thorax / 60 % neck, hip = pelvic station) and F2 forearm
# (elbow 4.2 cm toward the shoulder). W2I2 numbers are TARGET MEASUREMENTS; the geometry is regenerated with low-strain fields instead of the
# W2I2 narrow-band study warp:
#   - THIGH: the full thigh between the knee fields and the hip crease (u 63-86 core 67-81) carries the gain with a flat core, so the thigh
#     lengthens uniformly (cross-sections unchanged) instead of peaking in a narrow band;
#   - THORAX: costal -> below the shoulder line (u 124-151), unchanged lower trunk;
#   - NECK: the whole free neck from the thoracic inlet to below the chin (u 151-171), not a 13-cm band (W2I2 x0.45 -> here ~x0.66);
#   - SHOULDER CAP: arm vertices above the shoulder line (u0 > 146) follow the trunk / neck field (smoothstep blend), so the deltoid cap and the
#     trapezial slope move together (no morph-band crease); the arm below is carried rigidly (arm length unchanged);
#   - FOREARM: within-arm redistribution over the upper arm below the axilla (chord 0.12-0.18 ramp; an 0.06 start folded 148 axillary faces
#     and was rejected) and the whole forearm (elbow and wrist zones rigid), axillary taper
#     (arm weight <= 0.4 untouched) as W2I2.
# CAUDAL-BASE CONTOUR (order §5-§8): local redistribution of VENTRAL projection to the DORSAL side at the posterior-pelvic / caudal-base blend
# and proximal tail, in the accepted tail frame (axis C2, in-plane normal): ventral offsets x (1 - a w), dorsal offsets x (1 + b_k w) with
# b_k = a v_k / d_k per axis station so the section's ventral + dorsal half-depth sum (and its area, to first order) is conserved. Zone weight w:
# 0 at the caudal-base landmark (sacral origin / landmark / pelvis untouched), rising over 6 cm distal, flat to LC cm, fading over 10 cm; only
# vertices within 24 cm of the axis and posterior of the hip plane. Caudal-base landmark, axis, length, carriage and every vertex outside the
# zone are unchanged by construction. a = 0 (C0) ... a3 (C3).
import sys, os, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(D), 'w2i2_drivers')); sys.path.insert(0, os.path.join(os.path.dirname(D), 'w2i_drivers'))
import sa_cand as SC, sa_build as B, sa_joints as SJ
C = B.C; vary = C.vary; L = B.L; V0 = C.V; F0 = C.F; H0 = B.H0; ss = vary.ss; band = vary.band
GRID = SC.GRID
THIGH = (63.0, 67.0, 81.0, 86.0); THOR = (124.0, 127.0, 148.0, 151.0); NECK = (151.0, 155.0, 167.0, 171.0)
BI = {k: np.trapz(band(GRID, *b), GRID) for k, b in (("thigh", THIGH), ("thor", THOR), ("neck", NECK))}
TARGET = dict(G=9.2, FT=0.4, fa_delta=4.2)
def leg_rebuild(P, q, G, FT):
    dg = 1 + G / BI["thigh"] * band(GRID, *THIGH) - FT * G / BI["thor"] * band(GRID, *THOR) - (1 - FT) * G / BI["neck"] * band(GRID, *NECK)
    Phi = np.concatenate([[0], np.cumsum(0.5 * (dg[1:] + dg[:-1]) * np.diff(GRID))]); u0 = V0[:, 2]
    dU = np.interp(u0, GRID, Phi) - u0; dSh = np.interp(146.0, GRID, Phi) - 146.0; dRoot = np.interp(96.0, GRID, Phi) - 96.0
    cap = ss((u0 - 146.0) / 6.0); dArm = dSh * (1 - cap) + dU * cap                 # shoulder cap follows the trunk / neck field
    P = P.copy(); wb = np.clip(1 - L.arm - L.tail, 0, 1); P[:, 2] += dU * wb + dArm * L.arm + dRoot * L.tail
    q = dict(q); C2 = q['_C2'].copy(); i = np.arange(len(C2)); wa = ss((vary.S_ROOT + 3 - i * 0.5) / 8.0)
    C2[:, 2] += dRoot * wa + (np.interp(C2[:, 2], GRID, Phi) - C2[:, 2]) * (1 - wa); q['_C2'] = C2
    return P, q, dict(dU_top=float(Phi[-1] - GRID[-1]), dShoulder=float(dSh), dRoot=float(dRoot), peak_density={"thigh": float(dg.max()), "thorax_neck_min": float(dg.min())})
def fa_rebuild(P, J, delta):
    P = P.copy(); info = {}
    for sd, nm in ((1, 'L'), (-1, 'R')):
        S_, E_, W_ = J['S' + nm], J['E' + nm], J['W' + nm]; ch = W_ - S_; Lc = np.linalg.norm(ch); a = ch / Lc; sE = float((E_ - S_) @ a / Lc)
        s = np.linspace(-1.0, 2.0, 6001); up = band(s, 0.12, 0.18, sE - 0.09, sE - 0.05); fo = band(s, sE + 0.05, sE + 0.09, 0.90, 0.95)
        ds = s[1] - s[0]; d = delta / Lc; rho = 1 - d / (up.sum() * ds) * up + d / (fo.sum() * ds) * fo
        Phi = s[0] + np.concatenate([[0], np.cumsum(0.5 * (rho[1:] + rho[:-1]) * ds)])
        m = (L.side == sd) & (L.arm > 0.01); X = P[m]; sv = (X - S_) @ a / Lc; disp = (np.interp(sv, s, Phi) - sv) * Lc
        P[m] = X + (ss((L.arm[m] - 0.4) / 0.4) * disp)[:, None] * a
        info[nm] = dict(chord_cm=float(Lc), s_elbow=float(sE), peak_forearm_density=float(rho.max()), min_upperarm_density=float(rho.min()))
    return P, info
def tail_frame(P, q):
    C2 = q['_C2']; T2 = np.gradient(C2, axis=0); T2 /= np.linalg.norm(T2, axis=1)[:, None]; N2 = np.stack([np.zeros(len(T2)), -T2[:, 2], T2[:, 1]], 1)
    N2 = N2 * np.sign(N2[:, 2:3] + 1e-12)                                              # dorsal-positive (upward) in-plane normal
    k = L.k; o = np.einsum('ij,ij->i', P - C2[k], N2[k]); return C2, N2, k, o
LC_DEF = 30.0
def caudal_weight(P, q, LC=LC_DEF):
    C2, N2, k, o = tail_frame(P, q); s = k * 0.5 + L.ot; Sr = vary.S_ROOT                 # continuous axis position (no section quantization)
    t = np.clip((Sr - s) / 8.0, 0, 1); fade = ss((s - (Sr - LC - 12.0)) / 12.0)
    wz = ss(t) * fade                                                                      # 0 at the landmark, ramps over 8 cm, flat to LC, fades over 12 cm
    r = np.linalg.norm(P - C2[k], axis=1); wr = ss((24.0 - r) / 6.0) * (1 - ss((L.leg - 0.5) / 0.3)) * ss((-V0[:, 1] - 4.0) / 4.0)
    return wz * wr, C2, N2, k, o, s
def caudal(P, q, alpha, LC=LC_DEF):
    """ventral offsets x (1 - a w); dorsal offsets x (1 + b(s) w), b(s) = a v(s) / d(s) from smoothed (sigma 4 cm) section extents"""
    if not alpha: return P, {}
    w, C2, N2, k, o, s = caudal_weight(P, q, LC); z = w > 1e-4
    grid = np.arange(0, len(C2) * 0.5, 0.5); v = np.full(len(grid), np.nan); d = np.full(len(grid), np.nan)
    sb = np.round(s[z] / 0.5).astype(int); oz = o[z]
    for b in np.unique(sb):
        if 0 <= b < len(grid):
            mb = sb == b; v[b] = np.percentile(-oz[mb], 97); d[b] = np.percentile(oz[mb], 97)
    ok = ~np.isnan(v); ker = np.exp(-0.5 * (np.arange(-24, 25) * 0.5 / 4.0) ** 2); ker /= ker.sum()
    vi = np.interp(grid, grid[ok], v[ok]); di = np.interp(grid, grid[ok], d[ok]); vi = np.convolve(vi, ker, 'same'); di = np.convolve(di, ker, 'same')
    beta = alpha * np.clip(vi, 0, None) / np.maximum(di, 1.0); bv = np.interp(s, grid, beta)
    o2 = np.where(o < 0, o * (1 - alpha * w), o * (1 + bv * w))
    P = P.copy(); P += (o2 - o)[:, None] * N2[k]
    return P, dict(alpha=alpha, LC=LC, max_shift_cm=float(np.abs(o2 - o).max()), mean_beta=float(np.nanmean(beta[ok])))
JW = SC.JW
def build_r(p, cand, h=None):
    """accepted build (state p) -> F2 / L1 rebuild fields -> caudal-base contour (alpha) -> accepted regional stature route"""
    P, q = C.build(dict(p)); info = {}
    if cand.get('fa_delta'):
        J, _ = SJ.transport(P, JW); P, info['fa'] = fa_rebuild(P, J, cand['fa_delta'])
    if cand.get('G'): P, q, info['leg'] = leg_rebuild(P, q, cand['G'], cand.get('FT', 0.4))
    if cand.get('alpha'): P, info['caudal'] = caudal(P, q, cand['alpha'], cand.get('LC', LC_DEF))
    h = H0 if h is None else h
    P2, q2, k = B.at_stature(P, q, h)
    return P2, q2, k, info
REGIONS = {"thigh": lambda u: (u > 60) & (u < 90), "thorax": lambda u: (u > 120) & (u < 152), "neck": lambda u: (u > 150) & (u < 173), "arm": None, "caudal": None}
def strain(Pa, Pb):
    """per-triangle edge-length ratios (candidate / as-built at the same stature): stretch statistics by region"""
    E = np.vstack([F0[:, [0, 1]], F0[:, [1, 2]], F0[:, [2, 0]]]); la = np.linalg.norm(Pa[E[:, 0]] - Pa[E[:, 1]], axis=1); lb = np.linalg.norm(Pb[E[:, 0]] - Pb[E[:, 1]], axis=1)
    r = lb / np.maximum(la, 1e-9); u0 = V0[E[:, 0], 2]; out = {}
    masks = {"thigh": (u0 > 60) & (u0 < 90) & (L.leg[E[:, 0]] > 0.5), "thorax": (u0 > 120) & (u0 < 152) & (L.torso[E[:, 0]] > 0.5), "neck": (u0 > 150) & (u0 < 173) & (L.torso[E[:, 0]] > 0.3),
             "arm": L.arm[E[:, 0]] > 0.5, "caudal": L.tail[E[:, 0]] > 0.2, "all": np.ones(len(E), bool)}
    for nm, m in masks.items():
        x = r[m]; out[nm] = dict(p1=float(np.percentile(x, 1)), p50=float(np.percentile(x, 50)), p99=float(np.percentile(x, 99)), max=float(x.max()), min=float(x.min()))
    nr = lambda P: np.cross(P[F0[:, 1]] - P[F0[:, 0]], P[F0[:, 2]] - P[F0[:, 0]])
    out['flipped_faces'] = int((np.einsum('ij,ij->i', nr(Pa), nr(Pb)) < 0).sum())
    return out
