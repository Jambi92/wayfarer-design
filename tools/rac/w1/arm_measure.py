"""RAC W1 continuation: diagnostic measurement of an MPFB ARM candidate (numpy; reads *_r6.npz from build_arm.py).

Frame: x = subject's left, f = forward, u = up, cm, feet at u = 0. Head measures use the body frame as the FH*-equivalent
frame (head at the generator's neutral carriage, no rotation), with a +/-3 deg pitch sensitivity, as for Saurin (W1 D-1).
Every landmark method below is a MEASURER METHOD CHOICE, recorded in the W1c report; canon defines the landmarks (r3) but
not their surface-mesh extraction.
"""
import json, sys, numpy as np

def load(path):
    D = np.load(path, allow_pickle=True)
    d = {k: D[k] for k in D.files}
    d["joints"] = {k: (np.array(v[0]), np.array(v[1])) for k, v in json.loads(str(D["joints"])).items()}
    d["meta"] = json.loads(str(D["meta"]))
    return d

def ray_hits(V, F, o, d):
    A = V[F[:, 0]]; B = V[F[:, 1]]; C = V[F[:, 2]]; e1 = B - A; e2 = C - A
    p = np.cross(d, e2); det = (e1 * p).sum(1); ok = np.abs(det) > 1e-12
    inv = np.where(ok, 1 / np.where(ok, det, 1), 0); t_ = o - A; u = (t_ * p).sum(1) * inv
    q = np.cross(t_, e1); v = (q * d).sum(1) * inv; t = (e2 * q).sum(1) * inv
    m = ok & (u >= 0) & (v >= 0) & (u + v <= 1) & (t > 1e-9)
    return np.sort(t[m])

def volume(V, F):
    A = V[F[:, 0]]; B = V[F[:, 1]]; C = V[F[:, 2]]
    return float(np.einsum('ij,ij->i', A, np.cross(B, C)).sum() / 6.0)

def section(V, F, axis, level):
    """Polyline segments of the mesh cut by plane coordinate[axis] == level. Returns (n,2,3) segment endpoints."""
    s = V[:, axis] - level; S = s[F]
    segs = []
    for (i, j, k) in ((0, 1, 2), (1, 2, 0), (2, 0, 1)):
        pass
    sgn = np.sign(S); cross_ = ~((sgn[:, 0] == sgn[:, 1]) & (sgn[:, 1] == sgn[:, 2]))
    T = F[cross_]; St = S[cross_]
    pts = []
    for a, b in ((0, 1), (1, 2), (2, 0)):
        sa, sb = St[:, a], St[:, b]; m = (sa * sb) < 0
        t = sa[m] / (sa[m] - sb[m]); P = V[T[m, a]] + (V[T[m, b]] - V[T[m, a]]) * t[:, None]
        pts.append((np.where(m)[0], P))
    # pair the two crossing points of each triangle
    out = {}
    for idx, P in pts:
        for i, p in zip(idx, P): out.setdefault(i, []).append(p)
    return np.array([v[:2] for v in out.values() if len(v) >= 2])

def measure(path, pitch_deg=0.0, eye_ref_ext=None):
    d = load(path)
    if eye_ref_ext and 'helper_eye_ext' in d: d['eye_diam'] = np.array(2.4 * float(d['helper_eye_ext']) / eye_ref_ext)
    V = d["V"].astype(float); F = d["F"]; keep = d["keep"]; J = d["joints"]
    out = {"id": d["meta"].get("id"), "state": d["meta"].get("state")}
    Vb = V[keep]
    H = Vb[:, 2].max() - Vb[:, 2].min(); out["stature"] = H
    head = lambda n: J[n][0]; tail = lambda n: J[n][1]
    w = lambda k: d["w_" + k]
    # --- joints and segments (generator joint centres = rig bone heads; MakeHuman joint-cube centroids) ---
    seg = {}
    for s in ("l", "r"):
        sh, el, wr = head("upperarm_" + s), head("lowerarm_" + s), head("hand_" + s)
        hp, kn, an = head("thigh_" + s), head("calf_" + s), head("foot_" + s)
        mcp = head("middle_01_" + s)
        fv = np.where(keep & (w("fingers_" + s) > 0.5))[0]
        hax = (mcp - wr) / np.linalg.norm(mcp - wr)
        tip = V[fv][np.argmax((V[fv] - wr) @ hax)]
        hand_len = float((tip - wr) @ hax); palm_len = float((mcp - wr) @ hax)
        fo = np.where(keep & ((w("foot_" + s) + w("ball_" + s)) > 0.5))[0]
        seg[s] = {"upperarm": np.linalg.norm(el - sh), "forearm": np.linalg.norm(wr - el), "hand": hand_len, "palm": palm_len,
                  "finger": hand_len - palm_len, "thigh": np.linalg.norm(kn - hp), "shin": np.linalg.norm(an - kn),
                  "hip_height": hp[2], "ankle_height": an[2], "foot_len": V[fo, 1].max() - V[fo, 1].min(),
                  "foot_breadth": V[fo, 0].max() - V[fo, 0].min()}
        seg[s]["arm"] = seg[s]["upperarm"] + seg[s]["forearm"] + seg[s]["hand"]
        seg[s]["leg_joint"] = seg[s]["thigh"] + seg[s]["shin"]
        # palm breadth (across the MCP heads, perpendicular to hand axis) and depth (mid-palm thickness)
        hv = np.where(keep & (w("hand_" + s) > 0.5))[0]
        loc = (V[hv] - wr) @ hax
        sl = hv[np.abs(loc - 0.85 * palm_len) < 0.6]
        if len(sl) > 3:
            P = V[sl] - wr; P = P - np.outer(P @ hax, hax)
            # principal width direction in the plane
            C = np.cov(P.T); ev, evec = np.linalg.eigh(C); wdir = evec[:, -1]; ddir = np.cross(hax, wdir)
            seg[s]["palm_breadth"] = float((P @ wdir).max() - (P @ wdir).min()); seg[s]["palm_depth"] = float((P @ ddir).max() - (P @ ddir).min())
        # joint breadths: maximum extent perpendicular to the limb axis within +/-1 cm of the joint centre
        def jb(c, axis_vec, vids):
            ax = axis_vec / np.linalg.norm(axis_vec); P = V[vids] - c; t = P @ ax; m = np.abs(t) < 1.0
            Q = P[m] - np.outer(t[m], ax)
            if len(Q) < 4: return float('nan')
            ev, evec = np.linalg.eigh(np.cov(Q.T)); wd = evec[:, -1]
            return float((Q @ wd).max() - (Q @ wd).min())
        armv = np.where(keep & ((w("upperarm_" + s) + w("lowerarm_" + s)) > 0.3))[0]
        wrv = np.where(keep & ((w("lowerarm_" + s) + w("hand_" + s)) > 0.3))[0]
        legv = np.where(keep & ((w("thigh_" + s) + w("calf_" + s)) > 0.3))[0]
        ankv = np.where(keep & ((w("calf_" + s) + w("foot_" + s)) > 0.3))[0]
        seg[s]["elbow_breadth"] = jb(el, wr - sh, armv); seg[s]["wrist_breadth"] = jb(wr, wr - el, wrv)
        seg[s]["knee_breadth"] = jb(kn, an - hp, legv); seg[s]["ankle_breadth"] = jb(an, an - kn, ankv)
    for s_ in ("l", "r"):
        sh = head("upperarm_" + s_); mm = keep & (np.abs(V[:, 0] - sh[0]) < 2.5) & (np.abs(V[:, 1] - sh[1]) < 3)
        ac = V[mm][np.argmax(V[mm, 2])]
        seg[s_]["acromion_u"] = ac[2]; seg[s_]["acromion_to_elbow_joint"] = np.linalg.norm(head("lowerarm_" + s_) - ac)
        seg[s_]["acromion_minus_shoulder_joint"] = ac[2] - sh[2]
    out["L"] = {k: float(v) for k, v in seg["l"].items()}; out["R"] = {k: float(v) for k, v in seg["r"].items()}
    M = {k: (out["L"][k] + out["R"][k]) / 2 for k in out["L"]}
    # --- trunk ---
    sst = (head("clavicle_l") + head("clavicle_r")) / 2           # suprasternal proxy: sternoclavicular joint midpoint
    hipc = (head("thigh_l") + head("thigh_r")) / 2
    out["suprasternal_u"] = float(sst[2]); out["torso_len"] = float(sst[2] - hipc[2])
    neck = head("neck_01"); hj = head("head")
    out["neck_len"] = float(hj[2] - neck[2])
    shj = np.linalg.norm(head("upperarm_l") - head("upperarm_r"))
    out["shoulder_joint_breadth"] = float(shj); out["hip_joint_breadth"] = float(np.linalg.norm(head("thigh_l") - head("thigh_r")))
    armw = np.maximum.reduce([w(k) for k in ("upperarm_l", "upperarm_r", "lowerarm_l", "lowerarm_r", "hand_l", "hand_r", "fingers_l", "fingers_r")])
    trunk = keep & (armw < 0.2)
    def slab(level, mask, half=1.0):
        m = mask & (np.abs(V[:, 2] - level) < half)
        P = V[m]
        return (float(P[:, 0].max() - P[:, 0].min()), float(P[:, 1].max() - P[:, 1].min())) if len(P) > 5 else (np.nan, np.nan)
    sh_u = (head("upperarm_l")[2] + head("upperarm_r")[2]) / 2
    band = keep & (np.abs(V[:, 2] - (sh_u + 2)) < 4)
    out["bideltoid_breadth"] = float(V[band, 0].max() - V[band, 0].min())
    chest_u = head("spine_03")[2]
    out["thorax_breadth"], out["thorax_depth"] = slab(chest_u, trunk)
    # thorax maxima over the thoracic span (spine_02 .. 2 cm below the shoulder joints)
    lv = np.linspace(head("spine_02")[2], sh_u - 2, 12); vals = [slab(z, trunk) for z in lv]
    out["thorax_breadth_max"] = float(np.nanmax([v[0] for v in vals])); out["thorax_depth_max"] = float(np.nanmax([v[1] for v in vals]))
    # pelvis (external landmarks only): crest breadth = trunk width at the pelvis-bone head level (iliac crest proxy);
    # bitrochanteric = max width over +/-3 cm around the hip joints (thigh soft tissue included); AP depth at hip joint level
    crest_u = head("spine_01")[2]          # iliac-crest level proxy: generator lumbar joint L4/L5 region (method choice)
    out["iliac_crest_breadth"] = slab(crest_u, keep & (armw < 0.2))[0]
    bt = keep & (armw < 0.2) & (np.abs(V[:, 2] - hipc[2]) < 3)
    out["bitrochanteric_breadth"] = float(V[bt, 0].max() - V[bt, 0].min())
    out["pelvic_depth"] = slab(hipc[2], keep & (armw < 0.2))[1]
    out["pelvic_vertical"] = float(crest_u - hipc[2])
    out["waist_breadth"], out["waist_depth"] = slab(head("spine_01")[2] + 0.5 * (head("spine_02")[2] - head("spine_01")[2]), trunk)
    # --- W1e: pelvic / lower-trunk / ALPC station readings (SKIN surface; composition-inclusive DIAGNOSTICS, PV-D16) ---
    s02 = head("spine_03")[2]; s01 = head("spine_01")[2]; hipz = hipc[2]
    out["waist_interval"] = float(s02 - s01)                 # costal-margin proxy (spine_03 joint, lower thorax) -> crest proxy (spine_01 joint)
    out["thoracic_vertical"] = float(sst[2] - s02)           # suprasternal proxy -> costal-margin proxy
    def sec(z): return slab(z, trunk)
    st = {}
    st["S1"] = (float(shj), sec(sh_u - 2)[1])
    st["S2"] = (out["thorax_breadth_max"], out["thorax_depth_max"])
    st["S3"] = sec(s02)
    zs = np.linspace(s01, s02, 9); vals = [sec(z) for z in zs]; k = int(np.nanargmin([v[0] for v in vals])); st["S4"] = vals[k]
    st["S5"] = (out["iliac_crest_breadth"], sec(s01)[1])
    st["S6"] = (out["bitrochanteric_breadth"], out["pelvic_depth"])
    th = [] 
    for sd in ("l", "r"):
        hp_, kn_ = head("thigh_" + sd), head("calf_" + sd); ax = (kn_ - hp_) / np.linalg.norm(kn_ - hp_)
        tv = np.where(keep & (w("thigh_" + sd) > 0.5))[0]; P = V[tv] - hp_; t = P @ ax
        m_ = np.abs(t - 0.2 * np.linalg.norm(kn_ - hp_)) < 0.8; Q = P[m_] - np.outer(t[m_], ax)
        th.append((float(Q[:, 0].max() - Q[:, 0].min()), float(Q[:, 1].max() - Q[:, 1].min())))
    st["S7"] = tuple(np.mean(th, axis=0))
    out["alpc_stations"] = {k: [float(a), float(b)] for k, (a, b) in st.items()}
    # --- ratios to stature ---
    R = {"torso_share": out["torso_len"] / H, "leg_share": M["hip_height"] / H, "arm_share": M["arm"] / H,
         "span_der": (2 * M["arm"] + shj) / H, "upperarm_over_arm": M["upperarm"] / M["arm"], "forearm_over_arm": M["forearm"] / M["arm"],
         "hand_over_arm": M["hand"] / M["arm"], "forearm_over_upperarm": M["forearm"] / M["upperarm"],
         "finger_over_hand": M["finger"] / M["hand"], "finger_over_palm": M["finger"] / M["palm"],
         "femur_over_leg": M["thigh"] / M["leg_joint"], "shin_over_leg": M["shin"] / M["leg_joint"],
         "thigh_share": M["thigh"] / H, "shin_share": M["shin"] / H, "hand_share": M["hand"] / H, "foot_share": M["foot_len"] / H,
         "neck_share": out["neck_len"] / H, "thorax_depth_share": out["thorax_depth_max"] / H,
         "thorax_d_over_b": out["thorax_depth_max"] / out["thorax_breadth_max"], "shoulder_breadth_share": out["bideltoid_breadth"] / H,
         "shoulder_joint_share": shj / H, "thorax_breadth_share": out["thorax_breadth_max"] / H,
         "elbow_over_humerus": M["elbow_breadth"] / M["upperarm"], "wrist_over_forearm": M["wrist_breadth"] / M["forearm"],
         "knee_over_femur": M["knee_breadth"] / M["thigh"], "ankle_over_shin": M["ankle_breadth"] / M["shin"],
         "palm_breadth_over_hand": M.get("palm_breadth", np.nan) / M["hand"], "palm_depth_over_hand": M.get("palm_depth", np.nan) / M["hand"],
         "crest_share": out["iliac_crest_breadth"] / H, "bitroch_share": out["bitrochanteric_breadth"] / H,
         "pelvic_depth_share": out["pelvic_depth"] / H, "pelvic_vertical_share": out["pelvic_vertical"] / H,
         "pelvis_over_thorax_breadth": out["iliac_crest_breadth"] / out["thorax_breadth_max"],
         "pelvic_vertical_over_crest": out["pelvic_vertical"] / out["iliac_crest_breadth"],
         "bitroch_over_crest": out["bitrochanteric_breadth"] / out["iliac_crest_breadth"],
         "pelvic_depth_over_thorax_depth": out["pelvic_depth"] / out["thorax_depth_max"],
         "pelvic_depth_over_crest": out["pelvic_depth"] / out["iliac_crest_breadth"],
         "pelvic_vertical_over_thoracic_vertical": out["pelvic_vertical"] / out["thoracic_vertical"],
         "waist_interval_over_torso": out["waist_interval"] / out["torso_len"],
         "hip_joint_breadth_share": out["hip_joint_breadth"] / H,
         "S3_over_S2_b": st["S3"][0] / st["S2"][0], "S4_over_S2_b": st["S4"][0] / st["S2"][0], "S5_over_S2_b": st["S5"][0] / st["S2"][0],
         "S6_over_S2_b": st["S6"][0] / st["S2"][0], "S3_over_S2_d": st["S3"][1] / st["S2"][1], "S4_over_S2_d": st["S4"][1] / st["S2"][1],
         "S6_over_S2_d": st["S6"][1] / st["S2"][1], "S5_over_S4_b": st["S5"][0] / st["S4"][0], "S6_over_S4_b": st["S6"][0] / st["S4"][0],
         "S1_over_S2_b": st["S1"][0] / st["S2"][0]}
    out["mean"] = M; out["ratio"] = {k: float(v) for k, v in R.items()}
    out["volume_L"] = abs(volume(V, F)) / 1000.0
    out["cranio"] = cranio(d, V, F, keep, pitch_deg)
    out["ratio"]["HH_share"] = out["cranio"]["HH"] / H; out["ratio"]["HL_share"] = out["cranio"]["HL"] / H
    return out

def cranio(d, V, F, keep, pitch_deg=0.0):
    hw = d["w_head"]; ew = d["w_ears"]; el, er = d["eye_l"].astype(float), d["eye_r"].astype(float); R = float(d["eye_diam"]) / 2
    oc = (el + er) / 2
    # pitch about the OC axis (sensitivity of FH*-equivalent orientation)
    a = np.radians(pitch_deg); c, s = np.cos(a), np.sin(a)
    def rot(P):
        P = P - oc; return np.c_[P[:, 0], c * P[:, 1] - s * P[:, 2], s * P[:, 1] + c * P[:, 2]] + oc
    Vr = rot(V); hv = keep & (hw > 0.5)
    out = {"pitch_deg": pitch_deg, "OC_l": el.tolist(), "OC_r": er.tolist(), "eye_diam_cm": 2 * R}
    # midline outer profile: section of the skin by the plane x = +0.013 cm (vertices lie on x = 0), sampled every 0.05 cm in
    # u; at each level the anterior-most crossing (excludes the oral cavity loop)
    Fk = F[keep[F].all(1)]
    S = section(Vr, Fk, 0, 0.013)
    S = S[(S[:, :, 2].mean(1) > oc[2] - 16) & (S[:, :, 2].mean(1) < oc[2] + 14) & (S[:, :, 1].mean(1) > oc[1] - 8)]
    zg = np.arange(S[:, :, 2].min() + 0.01, S[:, :, 2].max() - 0.01, 0.05); fg = np.full(len(zg), -1e9)
    za, zb_ = S[:, 0, 2], S[:, 1, 2]; fa, fb_ = S[:, 0, 1], S[:, 1, 1]
    for i, z in enumerate(zg):
        m = (np.minimum(za, zb_) <= z) & (np.maximum(za, zb_) >= z) & (np.abs(za - zb_) > 1e-9)
        if m.any():
            t = (z - za[m]) / (zb_[m] - za[m]); fg[i] = (fa[m] + t * (fb_[m] - fa[m])).max()
    ok_ = fg > -1e8; zg, fg = zg[ok_], fg[ok_]
    def at(z): return np.array([0.0, np.interp(z, zg, fg), z])
    def amax(mask): return np.where(mask)[0][np.argmax(fg[mask])]
    def amin(mask): return np.where(mask)[0][np.argmin(fg[mask])]
    i_prn = amax((zg > oc[2] - 7) & (zg < oc[2] - 1)); prn = at(zg[i_prn])          # pronasale
    i_g = amax((zg > oc[2] + 0.3) & (zg < oc[2] + 4)); gl = at(zg[i_g])                # glabella-equivalent G*
    i_n = amin((zg < zg[i_g]) & (zg > zg[i_prn] + 1.0)); nst = at(zg[i_n])             # N*: deepest point between G* and prn
    # below pronasale, walk down the profile through alternating turning points: subnasale (min), labrale superius (max),
    # stomion (min), labrale inferius (max), labiomental sulcus (min), pogonion (max); 0.03 cm hysteresis
    def walk(i0, want_min, tol=0.03, span=3.0):
        best = i0; i = i0
        while i > 0 and zg[i0] - zg[i - 1] <= span:
            i -= 1
            if want_min:
                if fg[i] < fg[best]: best = i
                elif fg[i] > fg[best] + tol: return best
            else:
                if fg[i] > fg[best]: best = i
                elif fg[i] < fg[best] - tol: return best
        return best
    i_sn = walk(i_prn, True); i_ls = walk(i_sn, False); i_st = walk(i_ls, True)
    i_li = walk(i_st, False); i_lm = walk(i_li, True); i_pg = walk(i_lm, False)
    sn, ls, st, pg = at(zg[i_sn]), at(zg[i_ls]), at(zg[i_st]), at(zg[i_pg])
    # FAL (r3 L40 E proxy, literal): "subnasale-upper alveolar region (the more anterior of the two)": the more anterior of
    # subnasale (first profile minimum below pronasale) and the soft-tissue alveolar point A' (deepest point of the upper-lip
    # concavity between subnasale and labrale superius). Pr: cutaneous upper lip at 75 % of the way from subnasale to
    # labrale superius (upper-lip base over the alveolus; vermilion excluded) - method choice.
    ab = (zg <= zg[i_sn]) & (zg >= zg[i_ls])
    i_a = amin(ab); fal = at(zg[i_sn]) if fg[i_sn] >= fg[i_a] else at(zg[i_a])
    pr = at(zg[i_sn] - 0.75 * (zg[i_sn] - zg[i_ls]))
    # Me: lowest point of the chin contour within 2.5 cm behind pogonion; Gn: point of that contour farthest along (f - u)/sqrt2
    chin = np.where(keep & hv & (np.abs(Vr[:, 0]) < 0.6) & (Vr[:, 2] < pg[2]) & (Vr[:, 1] > pg[1] - 2.5))[0]
    chin = chin[Vr[chin, 2] > pg[2] - 3.0]
    me = Vr[chin][np.argmin(Vr[chin, 2])] if len(chin) else pg
    gn = Vr[chin][np.argmax(Vr[chin, 1] - Vr[chin, 2])] if len(chin) else pg
    # vertex, opisthocranion (head surface, excluding ears)
    hsurf = np.where(hv & (ew < 0.2))[0]
    Vt = Vr[hsurf][np.argmax(Vr[hsurf, 2])]
    upper = hsurf[Vr[hsurf, 2] > oc[2] - 2]
    op = Vr[upper][np.argmin(Vr[upper, 1])]
    HL = fal[1] - op[1]; HH = Vt[2] - me[2]
    out.update({"FAL": fal.tolist(), "Pr": pr.tolist(), "N*": nst.tolist(), "G*": gl.tolist(), "prn": prn.tolist(), "sn": sn.tolist(),
                "A'": at(zg[i_a]).tolist(), "ls": ls.tolist(), "sto": st.tolist(), "Pg": pg.tolist(), "Me": me.tolist(), "Gn": gn.tolist(), "V": Vt.tolist(), "Op": op.tolist(),
                "HL": float(HL), "HH": float(HH),
                "FPI": float((fal[1] - oc[1]) / HL), "MPI": float((pr[1] - nst[1]) / HL), "MdPI": float((gn[1] - nst[1]) / HL),
                "pronasale_minus_FAL_cm": float(prn[1] - fal[1])})
    # Po* proxy: deepest (most medial) point of the concha = ear-group surface point closest to the MSP, near the tragus level
    poS = {}
    for sgn, nm in ((1, "l"), (-1, "r")):
        ev = np.where(keep & (ew > 0.5) & (Vr[:, 0] * sgn > 0))[0]
        if len(ev):
            q = Vr[ev]; zc = q[:, 2]; mid_ = (zc > np.percentile(zc, 25)) & (zc < np.percentile(zc, 75))
            poS[nm] = q[mid_][np.argmin(np.abs(q[mid_, 0]))]
    po = (poS["l"] + poS["r"]) / 2 if len(poS) == 2 else None
    # Eu (max cranial breadth above the ear region, ears excluded), Zy (max facial breadth between Or* level and subnasale,
    # anterior to the ear), Go
    vault = hsurf[Vr[hsurf, 2] > (po[2] if po is not None else oc[2]) + 1]
    eu = Vr[vault, 0].max() - Vr[vault, 0].min()
    face = hsurf[(Vr[hsurf, 2] < oc[2] - 1) & (Vr[hsurf, 2] > sn[2]) & (Vr[hsurf, 1] > (po[1] if po is not None else oc[1] - 6) + 1)]
    zy = Vr[face, 0].max() - Vr[face, 0].min()
    out.update({"Po*": po.tolist() if po is not None else None, "Eu_Eu": float(eu), "Zy_Zy": float(zy)})
    if po is not None:
        out["CBH"] = float(eu / (Vt[2] - po[2])); out["FVI"] = float((nst[2] - me[2]) / (Vt[2] - po[2]))
        out["FDH"] = float((fal[1] - po[1]) / (nst[2] - me[2]))
    out["FVB"] = float((nst[2] - me[2]) / zy); out["MVI"] = float((nst[2] - pr[2]) / HH)
    # aperture: frontal orthographic visibility of the eyeball through the lids (rays from the front)
    apt = {}
    for nm, e in (("l", el), ("r", er)):
        e2 = rot(e[None])[0]
        xs = np.arange(-1.6, 1.6001, 0.04); zs = np.arange(-1.2, 1.2001, 0.04); vis = []
        near = np.where(keep & (np.linalg.norm(Vr - e2, axis=1) < 4.0))[0]
        Fm = F[np.isin(F, near).all(1)]
        for dx in xs:
            for dz in zs:
                if dx * dx + dz * dz > R * R: continue
                o = np.array([e2[0] + dx, e2[1] + 10, e2[2] + dz]); dr = np.array([0, -1.0, 0])
                ts = ray_hits(Vr, Fm, o, dr)
                f_eye = e2[1] + np.sqrt(max(R * R - dx * dx - dz * dz, 0))
                t_eye = o[1] - f_eye
                if len(ts) == 0 or ts[0] > t_eye: vis.append((dx, dz))
        vis = np.array(vis)
        if len(vis): apt[nm] = {"width": float(vis[:, 0].max() - vis[:, 0].min() + 0.04), "height": float(vis[:, 1].max() - vis[:, 1].min() + 0.04),
                                "area_cm2": float(len(vis) * 0.04 * 0.04), "centre_offset": [float(vis[:, 0].mean()), float(vis[:, 1].mean())]}
        else: apt[nm] = {"width": 0.0, "height": 0.0, "area_cm2": 0.0}
        # orbit E proxies on the vertical section through OC: Or* = most posterior anterior-surface point 0.4..3 cm below
        # the aperture's lower edge (lid-cheek junction); Os* = same above the upper edge (lid-brow junction)
        col = np.where(keep & hv & (np.abs(Vr[:, 0] - e2[0]) < 0.3) & (Vr[:, 1] > e2[1] - 1.5))[0]
        q = Vr[col]
        lo_edge = e2[2] + (vis[:, 1].min() if len(vis) else -0.5); hi_edge = e2[2] + (vis[:, 1].max() if len(vis) else 0.5)
        def frontmost_bins(qq):
            b = {}
            for p in qq:
                k = int(round(p[2] / 0.1))
                if k not in b or p[1] > b[k][1]: b[k] = p
            return np.array([b[k] for k in sorted(b)])
        fb = frontmost_bins(q)
        below = fb[(fb[:, 2] < lo_edge - 0.4) & (fb[:, 2] > lo_edge - 3.0)]
        above = fb[(fb[:, 2] > hi_edge + 0.4) & (fb[:, 2] < hi_edge + 3.0)]
        orr = below[np.argmin(below[:, 1])] if len(below) else None
        osr = above[np.argmin(above[:, 1])] if len(above) else None
        # horizontal section through OC: Mf* = most posterior anterior-surface point between 0.6 cm from the midline and
        # the aperture's medial end; Ec* = first point lateral to the aperture's lateral end whose surface turns > 45 deg
        row = np.where(keep & hv & (np.abs(Vr[:, 2] - e2[2]) < 0.3) & (Vr[:, 1] > e2[1] - 3))[0]
        rb = {}
        for p in Vr[row]:
            k = int(round(p[0] / 0.1))
            if k not in rb or p[1] > rb[k][1]: rb[k] = p
        rr = np.array([rb[k] for k in sorted(rb)])
        sgn = np.sign(e2[0]); med_end = e2[0] + (vis[:, 0].min() if sgn > 0 else vis[:, 0].max()) if len(vis) else e2[0]
        lat_end = e2[0] + (vis[:, 0].max() if sgn > 0 else vis[:, 0].min()) if len(vis) else e2[0]
        medial = rr[(rr[:, 0] * sgn > 0.6) & (rr[:, 0] * sgn < med_end * sgn)]
        mf = medial[np.argmin(medial[:, 1])] if len(medial) else None
        lat = rr[rr[:, 0] * sgn > lat_end * sgn]; lat = lat[np.argsort(lat[:, 0] * sgn)]
        ec = None
        for i in range(1, len(lat)):
            dxx = abs(lat[i, 0] - lat[i - 1, 0]); dff = lat[i - 1, 1] - lat[i, 1]
            if dxx > 0 and dff / dxx > 1.0: ec = lat[i - 1]; break
        apt[nm].update({"Or*": orr.tolist() if orr is not None else None, "Os*": osr.tolist() if osr is not None else None,
                        "Mf*": mf.tolist() if mf is not None else None, "Ec*": ec.tolist() if ec is not None else None})
        if orr is not None and osr is not None: apt[nm]["orbit_height"] = float(osr[2] - orr[2])
        if mf is not None and ec is not None: apt[nm]["orbit_breadth"] = float(abs(ec[0] - mf[0]))
    out["aperture"] = apt
    def mean_lr(k):
        v = [apt[s].get(k) for s in ("l", "r") if apt[s].get(k) is not None]; return float(np.mean(v)) if v else float('nan')
    out["ORB_breadth_over_HL"] = mean_lr("orbit_breadth") / HL; out["ORB_height_over_HH"] = mean_lr("orbit_height") / HH
    out["aperture_width_over_orbit_breadth"] = mean_lr("width") / mean_lr("orbit_breadth")
    out["aperture_height_over_orbit_height"] = mean_lr("height") / mean_lr("orbit_height")
    out["IOD"] = float(abs(apt["l"]["Mf*"][0] - apt["r"]["Mf*"][0]) / zy) if apt["l"].get("Mf*") and apt["r"].get("Mf*") else float('nan')
    return out

if __name__ == "__main__":
    r = measure(sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else 0.0)
    print(json.dumps(r, indent=1, default=float))
