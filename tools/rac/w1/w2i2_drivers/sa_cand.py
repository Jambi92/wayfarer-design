# RAC W2I2 candidate-study warps (order §4-§12). COPIES ONLY: the frozen SA-M / SA-F, the accepted tool chain files and the repo sources are
# never modified; every candidate is a smooth displacement applied in memory after the accepted creator-biology build.
#
# (1) ROOT CARRIAGE (§12): the accepted vary.warp tail-path step is extended IN MEMORY by one term: an upward pitch theta of the free-tail
#     segment directions that ramps smoothly (smoothstep) from 0 at the caudal-base landmark (S_ROOT) to theta over the proximal LP cm, then
#     stays constant - a distributed articulated bend, no hinge. The caudal base, the root zone above S_ROOT, every section shape (base, taper,
#     mass) and every non-tail vertex are untouched by construction; the distal 'tail_curv' stays at its neutral 0 unless set.
#     Parameters: 'tail_root_pitch' (deg, + = lift), 'tail_root_len' (LP, cm).
# (2) LEG / STATURE-BUDGET CANDIDATE (§4-§5): a monotone vertical remap of the body column (base-frame bands, as vary.warp's segment-length
#     step): THIGH band (u 63-85, between the knee fields and the crotch / pelvis) stretched by G cm; THORACIC band (u 124-151, above the
#     costal station so the lower axial trunk 91-123 is untouched) and NECK band (u 157-170, above the shoulder tops and below the chin) compressed so that standing height
#     is unchanged (thorax supplies FT x G, neck (1-FT) x G). Pelvis, lower trunk, caudal base and tail translate rigidly with the hip (+G);
#     arms translate rigidly with the shoulder; head translates rigidly (head length / depth / rostrum unchanged); foot, ankle, shin and knee
#     fields unchanged. The candidate hip joint is the accepted PELVIC hip-joint station (u 91 on the frozen body, the station of the canon
#     lower-trunk accounting; order §5 "hip station consistent with the accepted pelvis"); the Gate 4 B1-axis hip (u 86) is reported beside it.
# (3) FOREARM CANDIDATE (§8): within-arm redistribution along each shoulder -> wrist chord: the upper-arm band compressed and the forearm band
#     stretched so the elbow moves DELTA cm toward the shoulder; shoulder, wrist, hand and arm-to-wrist chord unchanged; the elbow zone
#     (+/- 6 % of the chord) translates rigidly (olecranon / epicondyle fields intact). Weight smoothstep((arm - 0.4) / 0.4): the axillary blend
#     tapers to zero before any torso-labelled vertex, so thoracic / shoulder readings are untouched.
import sys, os, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(D), 'w2i_drivers'))
import sa_build as B, sa_joints as SJ
C = B.C; vary = C.vary; L = B.L; V0 = C.V; H0 = B.H0; ss = vary.ss; band = vary.band
# --- (1) in-memory extension of the accepted vary.warp (textual, asserted) ---
_src = open(vary.__file__).read()
_old = "ang=np.radians(curv)*np.clip((S_ROOT-np.arange(len(C))*0.5)/S_ROOT,0,1)  # rotation grows toward the tip"
assert _src.count(_old) == 1
_new = _old + "\n    ang=ang-np.radians(p.get('tail_root_pitch',0.0))*ss(np.clip((S_ROOT-np.arange(len(C))*0.5)/p.get('tail_root_len',20.0),0,1))   # W2I2 root pitch (+ = lift)"
_ns = {}; exec(compile(_src.replace(_old, _new), vary.__file__ + '[w2i2]', 'exec'), _ns); vary.warp = _ns['warp']
# --- (2) leg / thorax / neck vertical remap ---
GRID = np.linspace(0, 200, 4001)
THIGH = (63.0, 66.0, 82.0, 85.0); THOR = (124.0, 127.0, 148.0, 151.0); NECK = (157.0, 160.0, 167.0, 170.0)
def _bint(b): return np.trapz(band(GRID, *b), GRID)
BI = {k: _bint(b) for k, b in (("thigh", THIGH), ("thor", THOR), ("neck", NECK))}
def leg_density(G, FT):
    """density on the base-frame grid: +G cm over the thigh band, -FT*G thorax, -(1-FT)*G neck (net 0)"""
    if not G: return np.ones_like(GRID)
    return 1 + G / BI["thigh"] * band(GRID, *THIGH) - FT * G / BI["thor"] * band(GRID, *THOR) - (1 - FT) * G / BI["neck"] * band(GRID, *NECK)
def leg_remap(P, q, G, FT):
    dg = leg_density(G, FT); Phi = np.concatenate([[0], np.cumsum(0.5 * (dg[1:] + dg[:-1]) * np.diff(GRID))]); u0 = V0[:, 2]
    dU = np.interp(u0, GRID, Phi) - u0; dSh = np.interp(150.0, GRID, Phi) - 150.0; dRoot = np.interp(96.0, GRID, Phi) - 96.0   # dSh = the trapezius / neck-base (154-157) displacement: the neck band starts above it
    P = P.copy(); wb = np.clip(1 - L.arm - L.tail, 0, 1); P[:, 2] += dU * wb + dSh * L.arm + dRoot * L.tail
    q = dict(q); C2 = q['_C2'].copy(); i = np.arange(len(C2)); wa = ss((vary.S_ROOT + 3 - i * 0.5) / 8.0)
    C2[:, 2] += dRoot * wa + (np.interp(C2[:, 2], GRID, Phi) - C2[:, 2]) * (1 - wa); q['_C2'] = C2
    return P, q, dict(dU_top=float(Phi[-1] - GRID[-1]), dShoulder=float(dSh), dRoot=float(dRoot))
# --- (3) forearm redistribution ---
def _fa_density(sE, a_, b_):
    s = np.linspace(-1.0, 2.0, 6001); up = band(s, 0.10, 0.16, sE - 0.10, sE - 0.06); fo = band(s, sE + 0.06, sE + 0.10, 0.84, 0.90)
    return s, up, fo
def fa_remap(P, J, delta):
    if not delta: return P, {}
    P = P.copy(); info = {}
    for sd, nm in ((1, 'L'), (-1, 'R')):
        S_, E_, W_ = J['S' + nm], J['E' + nm], J['W' + nm]; ch = W_ - S_; Lc = np.linalg.norm(ch); a = ch / Lc; sE = float((E_ - S_) @ a / Lc)
        s, up, fo = _fa_density(sE, 0, 0); ds = s[1] - s[0]; Iu = up.sum() * ds; If = fo.sum() * ds; d = delta / Lc
        rho = 1 - d / Iu * up + d / If * fo; Phi = s[0] + np.concatenate([[0], np.cumsum(0.5 * (rho[1:] + rho[:-1]) * ds)])
        m = (L.side == sd) & (L.arm > 0.01); X = P[m]; sv = (X - S_) @ a / Lc; disp = (np.interp(sv, s, Phi) - sv) * Lc
        wa = ss((L.arm[m] - 0.4) / 0.4)          # zero for arm weight <= 0.4: torso-labelled vertices (torso > 0.6) and every trunk reading stay exactly unchanged
        P[m] = X + (wa * disp)[:, None] * a
        info[nm] = dict(chord_cm=float(Lc), s_elbow=float(sE), elbow_shift_cm=float(np.interp(sE, s, Phi) - sE) * Lc)
    return P, info
def anchors_limb(J):
    """W2I2 anchors: as sa_joints.anchors, but the mid / distal joints (E, W, M, K, A) use only their own limb's vertices (arm / leg weight > 0.5)
    so the hanging hand and the thigh never share an anchor ring; shoulder and hip rings keep the trunk."""
    W = SJ.anchors(J)
    for key, p in J.items():
        j, nm = key[0], key[1]
        if j not in 'EWMKA': continue
        ax = SJ.axis_of(J, j, nm); lw = L.arm if j in 'EWM' else L.leg
        m = (np.abs((V0 - p) @ ax) < 1.0) & (np.linalg.norm(V0 - p, axis=1) < 12.0) & (lw > 0.5) & (L.side == (1 if nm == 'L' else -1))
        idx = np.where(m)[0]; X = V0[idx]; n = len(idx); A = np.vstack([X.T, np.ones(n)]); b = np.append(p, 1.0); w0 = np.full(n, 1.0 / n)
        w = w0 + A.T @ np.linalg.solve(A @ A.T, b - A @ w0); W[key] = (idx, w, float(np.abs(A @ w - b).max()), p - X.mean(0))
    return W
JW = anchors_limb(SJ.base_joints())
def build_c(p, cand, h=None):
    """accepted build (state p) + candidate warps at the reference stature, then the accepted regional stature route to h"""
    p = dict(p); cand = cand or {}
    for k in ('tail_root_pitch', 'tail_root_len'):
        if k in cand: p[k] = cand[k]
    P, q = C.build(p); info = {}
    if cand.get('fa_delta'):
        J, _ = SJ.transport(P, JW); P, info['fa'] = fa_remap(P, J, cand['fa_delta'])
    if cand.get('G'):
        P, q, info['leg'] = leg_remap(P, q, cand['G'], cand.get('FT', 0.4))
    h = H0 if h is None else h
    P2, q2, k = B.at_stature(P, q, h)
    return P2, q2, k, info
def joints_c(P):
    """J-2 joints transported to the candidate; candidate hip = pelvic hip-joint station height (x / f from the transported B1 axis)"""
    J, U = SJ.transport(P, JW); J = dict(J); ui = P[B.ST['hip'], 2]
    for nm in ('L', 'R'): J['HB' + nm] = J['H' + nm].copy(); J['H' + nm] = np.array([J['H' + nm][0], J['H' + nm][1], ui])
    return J, U
