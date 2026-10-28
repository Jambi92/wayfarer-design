"""RAC RP3 Vael custom body-deformation order (reviews/chatgpt-rac-rp3-vael-custom-body-deformation-order.md): the VAEL BODY FIELD (VDF1).

A bounded, deterministic, parameterised displacement field on the SOURCE rest mesh (after MPFB targets and bone scales are baked, before
posing), defined only in the body's own joint frames and skin-weight regions, so it is identical in construction for configuration 1 and
configuration 2 and transports to R-6 through the unchanged rig (joint centres never move; stature, hip-joint height, segment lengths and the
head / face are untouched by construction). It is applied by tools/rac/w1/arm_lib.build when cfg["vael_field"] is present (the full field
definition and its magnitude ride in the build record, so regen.py / build_variant.py / the skeletal-envelope builds reproduce it exactly).

Coordinates: analysis frame, cm (x = subject's left, y = forward, u = up). s = H / 173.14 (stature normalisation). Every region has an explicit
vertex mask (skin weights), coordinate frame (joints), displacement axis, magnitude (spec * magnitude) and falloff; magnitudes are FRACTIONS of
the body's own local dimension (trunk half-breadth at the waist, palm-root half-breadth, heel half-breadth) or cm x s, which is the c1 / c2
normalisation rule. Regions (order §4 / §6):
  rib      lower-thorax side wall (costal margin): lateral outward, Gaussian in height about the spine_02 -> spine_03 joint segment, lateral
           side-wall azimuth only (breast, abdomen and spine excluded)
  flank    torso-to-pelvis continuity: lateral fill of the lumbar side wall (spine_01 -> spine_02 segment), zero at the iliac crest
  asis     pelvis / hip silhouette: anterolateral iliac (ASIS) definition, radial outward, Gaussian in height about r_asis and in azimuth
  clav     shoulder / clavicle integration: forward-up relief on the front skin along the clavicle line (sternal end -> shoulder joint), Gaussian in height
  palm     wrist-to-hand base: palm-root broadening across the palm (pinky -> index axis) between the wrist line and mid-palm
  heel     ankle-to-foot base: heel / proximal-foot broadening across the foot below the malleoli
The field is mesh-smoothed (Laplacian, body vertices only) so no crease forms at weight seams. Ears, head and neck carry zero by mask."""
import json, hashlib, numpy as np

DEFAULT = {"version": "VDF1.2",
           "rib":   {"k": -0.070, "at": [1.0, 1.0], "sigma_seg": 0.85, "phi_min_deg": 62.0},
           "flank": {"k": -0.030, "at": [0.0, 0.6], "sigma_seg": 0.55, "phi_min_deg": 55.0, "crest_r": 0.16},
           "asis":  {"k": 0.030, "r": 0.10, "sigma_r": 0.06, "phi_deg": 50.0, "sigma_phi_deg": 22.0},
           "clav":  {"k_cm": 0.35, "sigma_cm": 1.4, "dz_cm": 0.5, "t0": 0.12, "t1": 0.85, "dir": [0.0, 0.8, 0.6]},
           "palm":  {"k": 0.080, "t0": 0.22, "t1": 0.65},
           "heel":  {"k": 0.080, "t0": 0.45, "zfade_cm": 3.0},
           "smooth_iters": 8}

def spec_hash(spec):
    return hashlib.sha256(json.dumps(spec, sort_keys=True).encode()).hexdigest()

def _ss(x): x = np.clip(x, 0.0, 1.0); return x * x * (3 - 2 * x)
def _g(x, m, s): return np.exp(-0.5 * ((x - m) / s) ** 2)

def _edges(F, n):
    F = np.asarray(F); E = np.vstack([F[:, [i, (i + 1) % F.shape[1]]] for i in range(F.shape[1])]); E = np.sort(E, 1)
    return np.unique(E, axis=0)

def _smooth(D, E, n, mask, iters):
    if iters <= 0: return D
    import scipy.sparse as sp
    A = sp.coo_matrix((np.ones(2 * len(E)), (np.r_[E[:, 0], E[:, 1]], np.r_[E[:, 1], E[:, 0]])), shape=(n, n)).tocsr()
    deg = np.asarray(A.sum(1)).ravel(); deg[deg == 0] = 1
    for _ in range(iters):
        D = np.where(mask[:, None], 0.5 * D + 0.5 * (A @ D) / deg[:, None], D)
    return D

def field(V, W, J, keep, F, spec, magnitude=1.0, return_parts=False, edges=None):
    """V (n x 3, cm analysis frame), W {bone: weights}, J {bone: [head, tail]}, keep (body vertices), F faces. Returns D (n x 3, cm)."""
    V = np.asarray(V, float); n = len(V); keep = np.asarray(keep, bool); m = float(magnitude)
    w = lambda k: np.asarray(W.get(k, np.zeros(n)), float)
    head = lambda b: np.asarray(J[b][0], float)
    H = V[keep, 2].max() - V[keep, 2].min(); s = H / 173.14
    wa = sum(w(k) for k in ('upperarm_l', 'upperarm_r', 'lowerarm_l', 'lowerarm_r', 'hand_l', 'hand_r', 'fingers_l', 'fingers_r'))
    wl = sum(w(k) for k in ('thigh_l', 'thigh_r', 'calf_l', 'calf_r', 'foot_l', 'foot_r', 'ball_l', 'ball_r'))
    wn = w('neck_01') + w('head') + w('ears')
    wt = np.clip(w('spine_01') + w('spine_02') + w('spine_03') + w('pelvis'), 0, 1)
    P = {}
    # ---------------- trunk frame: r = (u - hip) / (clavicle line - hip); section centre y per level; waist level r_w from the body itself
    hip = 0.5 * (head('thigh_l')[2] + head('thigh_r')[2]); cl = 0.5 * (head('clavicle_l')[2] + head('clavicle_r')[2]); r = (V[:, 2] - hip) / (cl - hip)
    tm = keep & (wt > 0.3) & (wa < 0.2) & (wl < 0.5)
    rg = np.linspace(-0.05, 1.0, 43); hb = np.full(len(rg), np.nan); cy = np.full(len(rg), np.nan)
    for i, rr in enumerate(rg):
        sl = tm & (np.abs(r - rr) < 0.02)
        if sl.sum() > 5: hb[i] = np.abs(V[sl, 0]).max(); cy[i] = 0.5 * (V[sl, 1].max() + V[sl, 1].min())
    ok = ~np.isnan(hb); hb = np.interp(rg, rg[ok], hb[ok]); cy = np.interp(rg, rg[ok], cy[ok]); hb = np.convolve(np.pad(hb, 2, mode='edge'), np.ones(5) / 5, 'valid')
    win = (rg > 0.25) & (rg < 0.62); r_w = float(rg[win][np.argmin(hb[win])]); hb_w = float(np.interp(r_w, rg, hb))
    yc = np.interp(r, rg, cy); dx = V[:, 0]; dy = V[:, 1] - yc; rad = np.hypot(dx, dy) + 1e-9; cosl = np.abs(dx) / rad
    trunk = tm.astype(float) * np.clip(1 - wa, 0, 1) * np.clip(1 - wn, 0, 1)
    D = np.zeros((n, 3))
    # joint-defined trunk levels: rib = between spine_02 and spine_03 heads (lower ribs / costal margin), flank = spine_01 -> spine_02 (lumbar waist)
    u1, u2, u3 = head('spine_01')[2], head('spine_02')[2], head('spine_03')[2]; seg = u3 - u2
    phi = np.degrees(np.arctan2(np.abs(dx), dy))                      # azimuth from the front (0) to lateral (90) to back (180)
    lat = lambda pmin: _ss((phi - pmin) / 20.0) * (1 - _ss((phi - 150.0) / 20.0))   # lateral side wall only (breast / abdomen / spine excluded)
    sp_ = spec['rib']; zc = u2 + sp_['at'][0] * seg
    a = sp_['k'] * m * hb_w * _g(V[:, 2], zc, sp_['sigma_seg'] * seg) * lat(sp_['phi_min_deg']) * trunk
    P['rib'] = np.c_[np.sign(dx) * a, 0 * a, 0 * a]
    sp_ = spec['flank']; zc = u1 + sp_['at'][1] * (u2 - u1)
    a = sp_['k'] * m * hb_w * _g(V[:, 2], zc, sp_['sigma_seg'] * (u2 - u1)) * _ss((r - sp_['crest_r']) / max((zc - hip) / (cl - hip) - sp_['crest_r'], 0.05)) * lat(sp_['phi_min_deg']) * trunk
    P['flank'] = np.c_[np.sign(dx) * a, 0 * a, 0 * a]
    # ASIS / anterolateral iliac definition
    sp_ = spec['asis']
    pel = keep & (wt + 0.5 * wl > 0.3) & (wa < 0.2)
    a = sp_['k'] * m * hb_w * _g(r, sp_['r'], sp_['sigma_r']) * _g(phi, sp_['phi_deg'], sp_['sigma_phi_deg']) * pel
    P['asis'] = np.c_[dx / rad * a, dy / rad * a, 0 * a]
    # clavicle relief
    sp_ = spec['clav']; d_ = np.asarray(sp_['dir'], float); d_ /= np.linalg.norm(d_); Pc = np.zeros((n, 3))
    for sd in ('l', 'r'):
        A0, B0 = head('clavicle_' + sd), head('upperarm_' + sd); ab = B0 - A0; L2 = ab @ ab
        t = np.clip(((V - A0) @ ab) / L2, 0, 1); C = A0 + t[:, None] * ab; dist = V[:, 2] - C[:, 2] - sp_.get('dz_cm', 0.5) * s   # height above the clavicle line on the front skin
        side = (np.sign(V[:, 0]) == np.sign(A0[0] if abs(A0[0]) > 1e-6 else B0[0]))
        front = _ss((V[:, 1] - C[:, 1] + 0.5 * s) / (1.0 * s))
        mk = keep & side & (wa < 0.5) & (wn < 0.3)
        a = sp_['k_cm'] * s * m * _g(dist, 0, sp_['sigma_cm'] * s) * _ss((t - sp_['t0']) / 0.1) * (1 - _ss((t - sp_['t1']) / 0.1)) * front * mk * np.clip(1 - wn, 0, 1)
        Pc += a[:, None] * d_[None, :]
    P['clav'] = Pc
    # palm root broadening
    sp_ = spec['palm']; Pp = np.zeros((n, 3))
    for sd in ('l', 'r'):
        wr, mid, ix, pk = head('hand_' + sd), head('middle_01_' + sd), head('index_01_' + sd), head('pinky_01_' + sd)
        ax = mid - wr; L = np.linalg.norm(ax); ax /= L; b = ix - pk; b -= (b @ ax) * ax; b /= np.linalg.norm(b)
        c0 = 0.5 * (ix + pk); off = (c0 - wr) @ b
        mk = keep & (w('hand_' + sd) > 0.5)
        t = ((V - wr) @ ax) / L; u = (V - wr) @ b - off * np.clip(t, 0, 1)
        Wt_ = _ss((t - sp_['t0']) / 0.12) * (1 - _ss((t - sp_['t1']) / 0.25))
        a = sp_['k'] * m * u * Wt_ * mk
        Pp += a[:, None] * b[None, :]
    P['palm'] = Pp
    # heel / proximal foot base broadening below the malleoli
    sp_ = spec['heel']; Ph = np.zeros((n, 3))
    for sd in ('l', 'r'):
        an, bl = head('foot_' + sd), head('ball_' + sd); ax = an - bl; ax[2] = 0; L = np.linalg.norm(ax); ax /= L; mh = np.array([-ax[1], ax[0], 0.0])
        mk = keep & ((w('foot_' + sd) + w('ball_' + sd)) > 0.5)
        t = ((V - bl) @ ax) / L; u = (V - bl) @ mh
        um = np.zeros(n)   # foot mid-line at each t (from the foot vertices themselves)
        tg = np.linspace(-0.3, 1.6, 39); mu = np.full(len(tg), np.nan)
        for i, tt in enumerate(tg):
            sl = mk & (np.abs(t - tt) < 0.04)
            if sl.sum() > 3: mu[i] = 0.5 * (u[sl].max() + u[sl].min())
        okm = ~np.isnan(mu); um = np.interp(t, tg[okm], mu[okm])
        zf = 1 - _ss((V[:, 2] - (an[2] - sp_['zfade_cm'] * s)) / (1.5 * s))
        a = sp_['k'] * m * (u - um) * _ss((t - sp_['t0']) / 0.3) * zf * mk
        Ph += a[:, None] * mh[None, :]
    P['heel'] = Ph
    E = np.asarray(edges) if edges is not None else _edges(F, n); it_ = int(spec.get('smooth_iters', 8))
    # trunk-family regions are smoothed and then held off the free arm (upper arm / forearm weight), so the trunk side wall never drags the
    # arm's inner surface into it; the hand / foot regions are smoothed on their own
    Dt = _smooth(P['rib'] + P['flank'] + P['asis'] + P['clav'], E, n, keep & (wn < 0.5), it_)
    warm = w('upperarm_l') + w('upperarm_r') + w('lowerarm_l') + w('lowerarm_r'); Dt *= np.clip(1 - 1.5 * warm, 0, 1)[:, None]
    Dl = _smooth(P['palm'] + P['heel'], E, n, keep & (wn < 0.5), it_)
    wf = w('fingers_l') + w('fingers_r'); Dl *= np.clip(1 - 3.0 * wf, 0, 1)[:, None]   # digits incl. the thumb ray (thumb_01) carry no palm-root displacement (finger / thumb loops untouched)
    D = Dt + Dl
    D[~keep] = 0.0; D[keep & (wn > 0.5)] = 0.0
    info = dict(H=float(H), s=float(s), hip_u=float(hip), clavicle_u=float(cl), r_waist=r_w, waist_half_breadth_cm=hb_w)
    if return_parts: return D, P, info
    return D, info

def npz_inputs(z):
    """weights / joints / keep / faces from an arm_lib.export npz (analysis frame)."""
    W = {k[2:]: z[k] for k in z.files if k.startswith('w_')}; J = json.loads(str(z['joints']))
    return W, J, z['keep'], z['F']
