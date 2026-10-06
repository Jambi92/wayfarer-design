"""RAC W1f: SKELETAL PROXY (SKP) readings for one candidate (PV-D16, AD-G10, AD-G14 validation layer).

Method (BUILDER-CHOSEN, declared under R-14; measurer method, not canon):
1. Skeletal-envelope body: the same candidate rebuilt with the SAME skeleton construction (same height macro or native factors,
   same targets and bone scales) at the generator's MINIMUM composition (muscle 0, weight 0) — build_variant.py "-LEAN".
   It is aligned to the reference body's rig joints by a least-squares similarity (uniform scale + translation); the residual
   joint mismatch is reported (W1f: <= 0.27 cm).
2. Skeleton = rig joint centres (hip = femoral-head / acetabular centre, spine column, clavicles) + the skeletal-envelope surface
   inset by a residual soft-tissue allowance t (skin + minimal fascia/muscle over bone). t is NOT a measured anatomical value:
   every reading is computed at t = 0, 0.5 and 1.0 cm x (stature / 173.14) and a direction counts only if it holds at all three.
3. Anatomical girdle landmarks (AD-G10): glenohumeral centre = least-squares sphere fitted to the skeletal-envelope shoulder cap
   around the rig shoulder joint; acromion = highest skeletal-envelope point over the shoulder (arm_measure rule) - biacromial.
4. Proximal femur (ALPC-3 / GO-P2a): femoral head/neck scale proxy = hip-joint centre -> greater-trochanter distance (trochanter
   = most lateral skeletal-envelope point within +/-3 cm x H/173 of the hip-joint height), minus t; subtrochanteric shaft
   proxy = skeletal-envelope thigh section at 20 % of femur length, inset 2t.
5. Soft tissue at the reference composition = (reference skin - skeletal envelope) per station, reported per side / stature.
Anatomy on rest geometry, leg share on R-6 (D-W1c-1). External skeletal landmarks only (obstetric firewall, RA).
W1g (AD-W1G-1): optional 5th argument = a bony_envelope.py CIB json. The ALPC stations S2...S7 are then the COMPOSITION-INFIMUM
bony values (min over the {0, .25, .5}^2 composition grid of the same skeleton; inside every tested composition by construction)
instead of the single minimum-composition body; the proximal-femur scale is reduced by half the S6-breadth correction. Girdle
landmarks (GH sphere fit, acromion), joints and vertical intervals are unchanged. The W1f stations are kept in the output
("w1f_stations") for before/after.
Usage: python3 skeletal_proxy.py ref_dir lean_dir ID out_dir [cib.json]"""
import sys, os, json, tempfile, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from arm_measure import measure, load

T_SET = (0.0, 0.5, 1.0)
JK = ["pelvis", "spine_01", "spine_02", "spine_03", "neck_01", "head", "thigh_l", "thigh_r", "calf_l", "calf_r", "foot_l", "foot_r",
      "clavicle_l", "clavicle_r", "upperarm_l", "upperarm_r", "lowerarm_l", "lowerarm_r", "hand_l", "hand_r"]

def align(lean_path, ref_path, out_path):
    L = dict(np.load(lean_path, allow_pickle=True)); R = load(ref_path)
    jl = json.loads(str(L["joints"])); P = np.array([R["joints"][k][0] for k in JK]); Q = np.array([jl[k][0] for k in JK])
    pc, qc = P.mean(0), Q.mean(0); s = ((P - pc) * (Q - qc)).sum() / ((Q - qc) ** 2).sum()
    f = lambda X: (np.asarray(X, float) - qc) * s + pc
    resid = float(np.abs(f(Q) - P).max())
    L["V"] = f(L["V"]).astype(np.float32); L["eye_l"] = f(L["eye_l"]); L["eye_r"] = f(L["eye_r"])
    L["joints"] = json.dumps({k: [f(v[0]).tolist(), f(v[1]).tolist()] for k, v in jl.items()})
    np.savez_compressed(out_path, **L)
    return s, resid

def sphere_fit(P):
    A = np.c_[2 * P, np.ones(len(P))]; b = (P ** 2).sum(1); x, *_ = np.linalg.lstsq(A, b, rcond=None)
    c = x[:3]; r = np.sqrt(x[3] + c @ c); return c, float(r)

def girdle_femur(d, H):
    V = d["V"].astype(float); keep = d["keep"]; J = d["joints"]; w = lambda k: d["w_" + k]; k = H / 173.14
    out = {}
    for s, sg in (("l", 1), ("r", -1)):
        sh = J["upperarm_" + s][0]; rad = 6.0 * k
        cap = keep & (np.linalg.norm(V - sh, axis=1) < rad) & ((w("upperarm_" + s) + w("clavicle_" + s)) > 0.2) & \
              (((V - sh) @ np.array([sg * 0.7, 0.0, 0.7])) > 0)
        c, r = sphere_fit(V[cap]); out["gh_" + s] = c.tolist(); out["gh_capfit_r_" + s] = r; out["gh_cap_n_" + s] = int(cap.sum())
        mm = keep & (np.abs(V[:, 0] - sh[0]) < 2.5 * k) & (np.abs(V[:, 1] - sh[1]) < 3 * k)
        out["acromion_" + s] = V[mm][np.argmax(V[mm, 2])].tolist()
        hp = J["thigh_" + s][0]; kn = J["calf_" + s][0]
        armw = np.maximum.reduce([w(x) for x in ("upperarm_l", "upperarm_r", "lowerarm_l", "lowerarm_r", "hand_l", "hand_r", "fingers_l", "fingers_r")])
        tz = keep & (armw < 0.2) & (np.abs(V[:, 2] - hp[2]) < 3 * k) & (np.abs(V[:, 1] - hp[1]) < 6 * k) & (V[:, 0] * sg > 0)
        tr = V[tz][np.argmax(V[tz, 0] * sg)]; out["trochanter_" + s] = tr.tolist()
        out["hip_to_trochanter_" + s] = float(np.linalg.norm((tr - hp)[[0, 2]]))   # frontal-plane head/neck span proxy
        out["femur_len_" + s] = float(np.linalg.norm(kn - hp))
    return out

def readings(m, g, mlean_stations, H, t):
    """skeletal readings at allowance t (cm, already size-scaled)"""
    st = {k: [v[0] - 2 * t, v[1] - 2 * t] for k, v in mlean_stations.items()}
    ghb = float(np.linalg.norm(np.array(g["gh_l"]) - np.array(g["gh_r"])))
    biac = float(abs(g["acromion_l"][0] - g["acromion_r"][0]) - 2 * t)
    st["S1"] = [ghb, st["S1"][1]]
    pf = np.mean([g["hip_to_trochanter_l"], g["hip_to_trochanter_r"]]) - t; fl = np.mean([g["femur_len_l"], g["femur_len_r"]])
    crest, bitroch, pdepth = st["S5"][0], st["S6"][0], st["S6"][1]
    TB, TD = st["S2"]
    R = {"crest_share": crest / H, "bitroch_share": bitroch / H, "pelvic_depth_share": pdepth / H,
         "pelvic_vertical_share": m["pelvic_vertical"] / H, "hip_joint_breadth_share": m["hip_joint_breadth"] / H,
         "pelvis_over_thorax_breadth": crest / TB, "pelvic_depth_over_crest": pdepth / crest, "bitroch_over_crest": bitroch / crest,
         "pelvic_depth_over_thorax_depth": pdepth / TD, "waist_interval_over_torso": m["waist_interval"] / m["torso_len"],
         "pelvic_vertical_over_crest": m["pelvic_vertical"] / crest,
         "pelvic_vertical_over_thoracic_vertical": m["pelvic_vertical"] / m["thoracic_vertical"],
         "thorax_breadth_share": TB / H, "thorax_depth_share": TD / H, "thorax_d_over_b": TD / TB,
         "shoulder_joint_share": ghb / H, "gh_breadth_share": ghb / H, "biacromial_share": biac / H, "S1_over_S2_b": ghb / TB,
         "biacromial_over_S2_b": biac / TB, "prox_femur_over_S6_b": pf / bitroch, "prox_femur_over_hipjoint_breadth": pf / m["hip_joint_breadth"],
         "hipjoint_scale_over_crest": pf / crest, "shaft_b_over_femur": st["S7"][0] / fl, "shaft_d_over_femur": st["S7"][1] / fl,
         "ribcage_vertical_over_S2_b": m["thoracic_vertical"] / TB, "torso_share": m["torso_len"] / H, "arm_share": m["mean"]["arm"] / H,
         "span_der": (2 * m["mean"]["arm"] + m["shoulder_joint_breadth"]) / H}
    for a in ("S3", "S4", "S5", "S6"):
        R[a + "_over_S2_b"] = st[a][0] / TB
    for a in ("S3", "S4", "S6"):
        R[a + "_over_S2_d"] = st[a][1] / TD
    R["S5_over_S4_b"] = st["S5"][0] / st["S4"][0]; R["S6_over_S4_b"] = st["S6"][0] / st["S4"][0]
    return st, R, {"gh_breadth": ghb, "biacromial": biac, "prox_femur": pf, "femur_len": fl}

def main(ref_dir, lean_dir, cid, out_dir, cib=None):
    os.makedirs(out_dir, exist_ok=True)
    rest = os.path.join(ref_dir, cid + "_rest.npz"); r6 = os.path.join(ref_dir, cid + "_r6.npz")
    lean_rest = os.path.join(lean_dir, cid + "-LEAN_rest.npz"); lean_r6 = os.path.join(lean_dir, cid + "-LEAN_r6.npz")
    tmp = tempfile.mkdtemp(); al = os.path.join(tmp, "a_rest.npz"); al6 = os.path.join(tmp, "a_r6.npz")
    s, res_j = align(lean_rest, rest, al); s6, res_j6 = align(lean_r6, r6, al6)
    mref = measure(rest); m6 = measure(r6); mlean = measure(al)
    H = m6["stature"]; k = H / 173.14
    g = girdle_femur(load(al), H)
    w1f_st = {k: list(v) for k, v in mlean["alpc_stations"].items()}
    if cib:
        C = json.load(open(cib))
        for S, bv in C["bony"].items():
            if S not in w1f_st: mlean["alpc_stations"][S] = list(bv); continue
            mlean["alpc_stations"][S] = list(bv) if C.get("no_lean_clamp") else [min(bv[0], w1f_st[S][0]), min(bv[1], w1f_st[S][1])]
        dS6 = (w1f_st["S6"][0] - mlean["alpc_stations"]["S6"][0]) / 2
        for s_ in ("l", "r"): g["hip_to_trochanter_" + s_] -= dS6
        g["cib"] = {"file": os.path.basename(cib), "argmin": C["argmin"], "S6_half_correction_cm": dS6}
    out = {"id": cid, "stature_r6": H, "align_scale": s, "align_joint_resid_cm": res_j, "align_joint_resid_r6_cm": res_j6,
           "landmarks": g, "t_set_cm": [t * k for t in T_SET], "leg_share": m6["mean"]["hip_height"] / H,
           "tissue_per_side_over_H": {st: [(mref["alpc_stations"][st][0] - mlean["alpc_stations"][st][0]) / 2 / H,
                                           (mref["alpc_stations"][st][1] - mlean["alpc_stations"][st][1]) / 2 / H] for st in mref["alpc_stations"]},
           "w1f_stations": w1f_st, "station_method": (C.get("variant", "CIB (composition infimum, W1g)") if cib else None) if cib else "W1f minimum-composition proxy", "by_t": {}}
    for t in T_SET:
        stn, R, ex = readings(mlean, g, mlean["alpc_stations"], H, t * k)
        R["leg_share"] = out["leg_share"]
        # pseudo-meas record in the arm_measure 'combined' shape so the W1e check logic can run unchanged on skeletal values
        comb = {"stature": H, "alpc_stations": stn, "waist_interval": mlean["waist_interval"], "thoracic_vertical": mlean["thoracic_vertical"],
                "ratio": R, "extra": ex}
        out["by_t"]["%.1f" % t] = comb
        tdir = os.path.join(out_dir, "t%.1f" % t); os.makedirs(tdir, exist_ok=True)
        json.dump({"id": cid, "combined": comb}, open(os.path.join(tdir, cid + "_meas.json"), "w"), indent=1, default=float)
    json.dump(out, open(os.path.join(out_dir, cid + "_skp.json"), "w"), indent=1, default=float)
    import shutil; shutil.rmtree(tmp, ignore_errors=True)    # W1h: no temp build-up
    print("SKP", cid, "align s %.4f resid %.3f/%.3f" % (s, res_j, res_j6), "GH breadth %.2f biac %.2f" % (out["by_t"]["0.0"]["extra"]["gh_breadth"], out["by_t"]["0.0"]["extra"]["biacromial"]))

if __name__ == "__main__":
    main(*sys.argv[1:6])
