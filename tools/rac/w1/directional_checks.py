"""RAC W1c directional checks: canon directions (quoted in reviews/claude-rac-w1c-*.md) tested between measured candidates.
Strict inequalities on unrounded values. '≈' uses one declared method tolerance for every '≈' check (APPROX = 0.010 in ratio units),
which is a MEASURER METHOD CHOICE, not canon. Usage: python3 directional_checks.py outdir out.json"""
import sys, json, os
APPROX = 0.010
ids = ["MF-M-R", "MF-F-R", "MF-FACE-PROJ-MAX", "SK", "SG", "FN", "AE", "VA", "HV", "DU", "GR", "GO", "PK", "CG"]

def run(outdir):
    M = {i: json.load(open(os.path.join(outdir, i + "_meas.json")))["combined"] for i in ids}
    r = lambda i, k: M[i]["ratio"][k]
    c = lambda i, k: M[i]["cranio"][k]
    m = lambda i, k: M[i]["mean"][k]
    eye = lambda i: M[i]["cranio"]["eye_diam_cm"]
    aph = lambda i: (M[i]["cranio"]["aperture"]["l"]["height"] + M[i]["cranio"]["aperture"]["r"]["height"]) / 2
    apw = lambda i: (M[i]["cranio"]["aperture"]["l"]["width"] + M[i]["cranio"]["aperture"]["r"]["width"]) / 2
    C = []
    def gt(cid, desc, src, a, b, la, lb): C.append({"cand": cid, "check": desc, "canon": src, "a": la, "va": a, "b": lb, "vb": b, "op": ">", "pass": a > b})
    def lt(cid, desc, src, a, b, la, lb): C.append({"cand": cid, "check": desc, "canon": src, "a": la, "va": a, "b": lb, "vb": b, "op": "<", "pass": a < b})
    def ap(cid, desc, src, a, b, la, lb, tol=APPROX): C.append({"cand": cid, "check": desc, "canon": src, "a": la, "va": a, "b": lb, "vb": b, "op": "≈(±%.3f)" % tol, "pass": abs(a - b) <= tol})
    def rng(cid, desc, src, v, lo, hi, l): C.append({"cand": cid, "check": desc, "canon": src, "a": l, "va": v, "b": "range", "vb": [lo, hi], "op": "in", "pass": lo <= v <= hi})
    MF = "MF-M-R"
    for k, d in (("torso_share", "torso share slightly > MF"),):
        gt("SK", d, "SK L75", r("SK", k), r(MF, k), "SK", "MF")
    gt("SK", "greater torso (thoracic) depth / stature than MF", "SK L22, L75", r("SK", "thorax_depth_share"), r(MF, "thorax_depth_share"), "SK", "MF")
    gt("SK", "broader clavicles (shoulder-joint breadth / stature) than MF", "SK L20", r("SK", "shoulder_joint_share"), r(MF, "shoulder_joint_share"), "SK", "MF")
    for k, n in (("elbow_over_humerus", "elbow"), ("wrist_over_forearm", "wrist"), ("knee_over_femur", "knee")):
        gt("SK", "heavier %s joint (breadth / adjacent bone) than MF" % n, "SK L24, L78", r("SK", k), r(MF, k), "SK", "MF")
    gt("SK", "larger absolute hands than MF (hand length cm)", "SK L25, L79", m("SK", "hand"), m(MF, "hand"), "SK", "MF")
    gt("SK", "larger absolute feet than MF (foot length cm)", "SK L25, L79", m("SK", "foot_len"), m(MF, "foot_len"), "SK", "MF")
    gt("SG", "leg share slightly > MF", "SG L137–141", r("SG", "leg_share"), r(MF, "leg_share"), "SG", "MF")
    lt("SG", "torso share slightly < MF", "SG L137–141", r("SG", "torso_share"), r(MF, "torso_share"), "SG", "MF")
    gt("SG", "forearm / arm > MF", "SG L138", r("SG", "forearm_over_arm"), r(MF, "forearm_over_arm"), "SG", "MF")
    gt("SG", "hand / stature > MF", "SG L155–157", r("SG", "hand_share"), r(MF, "hand_share"), "SG", "MF")
    gt("SG", "finger / hand > MF", "SG L155–157", r("SG", "finger_over_hand"), r(MF, "finger_over_hand"), "SG", "MF")
    lt("SG", "hands slightly narrower (palm breadth / hand) than MF", "SG L155–157", r("SG", "palm_breadth_over_hand"), r(MF, "palm_breadth_over_hand"), "SG", "MF")
    lt("SG", "ribcage depth / stature < MF", "SG L89, L141", r("SG", "thorax_depth_share"), r(MF, "thorax_depth_share"), "SG", "MF")
    lt("FN", "smaller torso share than MF", "FN L32–52", r("FN", "torso_share"), r(MF, "torso_share"), "FN", "MF")
    lt("FN", "shallower ribcage (depth / stature) than MF", "FN L32–52", r("FN", "thorax_depth_share"), r(MF, "thorax_depth_share"), "FN", "MF")
    lt("FN", "moderately narrow ribcage (breadth / stature) than MF", "FN L32–52", r("FN", "thorax_breadth_share"), r(MF, "thorax_breadth_share"), "FN", "MF")
    gt("FN", "longer arms (arm / stature) than MF", "FN L32–52", r("FN", "arm_share"), r(MF, "arm_share"), "FN", "MF")
    gt("FN", "longer legs (leg / stature) than MF", "FN L32–52", r("FN", "leg_share"), r(MF, "leg_share"), "FN", "MF")
    gt("FN", "greater forearm share of arm than MF", "FN L32–52", r("FN", "forearm_over_arm"), r(MF, "forearm_over_arm"), "FN", "MF")
    gt("FN", "greater lower-leg share of leg than MF", "FN L32–52", r("FN", "shin_over_leg"), r(MF, "shin_over_leg"), "FN", "MF")
    gt("FN", "longer palms and fingers (hand / stature) than MF", "FN L32–52", r("FN", "hand_share"), r(MF, "hand_share"), "FN", "MF")
    lt("FN", "narrow wrists (wrist breadth / forearm) vs MF", "FN L32–52", r("FN", "wrist_over_forearm"), r(MF, "wrist_over_forearm"), "FN", "MF")
    lt("FN", "joints smaller relative to limb length (knee / femur) vs MF", "FN L110–124", r("FN", "knee_over_femur"), r(MF, "knee_over_femur"), "FN", "MF")
    gt("FN", "bony orbit slightly larger: ORB breadth / HL (E proxy) > MF", "FN L173", c("FN", "ORB_breadth_over_HL"), c(MF, "ORB_breadth_over_HL"), "FN", "MF")
    gt("FN", "bony orbit slightly larger: ORB height / HH (E proxy) > MF", "FN L173", c("FN", "ORB_height_over_HH"), c(MF, "ORB_height_over_HH"), "FN", "MF")
    gt("FN", "aperture slightly more open (aperture height cm) than MF", "FN L173", aph("FN"), aph(MF), "FN", "MF")
    gt("AE", "neck longer than FN (neck / stature)", "AE L33–58", r("AE", "neck_share"), r("FN", "neck_share"), "AE", "FN")
    gt("AE", "neck longer relative to torso than VA (neck / torso)", "VA L123", M["AE"]["neck_len"] / M["AE"]["torso_len"], M["VA"]["neck_len"] / M["VA"]["torso_len"], "AE", "VA")
    gt("AE", "longer arms (even elongation) than MF", "AE L33–58", r("AE", "arm_share"), r(MF, "arm_share"), "AE", "MF")
    gt("AE", "longer legs (even elongation) than MF", "AE L33–58", r("AE", "leg_share"), r(MF, "leg_share"), "AE", "MF")
    ap("AE", "upper-arm / forearm relation even (forearm / upper arm ≈ MF)", "AE L33–58", r("AE", "forearm_over_upperarm"), r(MF, "forearm_over_upperarm"), "AE", "MF")
    lt("AE", "relatively shallow ribcage (depth / stature) vs MF", "AE L123–155", r("AE", "thorax_depth_share"), r(MF, "thorax_depth_share"), "AE", "MF")
    for k, n in (("elbow_over_humerus", "elbow"), ("wrist_over_forearm", "wrist"), ("knee_over_femur", "knee")):
        lt("AE", "gracile %s joint vs MF" % n, "AE L123–155", r("AE", k), r(MF, k), "AE", "MF")
    gt("AE", "longer hands (hand / stature) than MF", "AE L57, L153", r("AE", "hand_share"), r(MF, "hand_share"), "AE", "MF")
    gt("AE", "somewhat longer feet (foot / stature) than MF", "AE L155", r("AE", "foot_share"), r(MF, "foot_share"), "AE", "MF")
    gt("FN", "longer feet (foot / stature) than MF", "FN L36", r("FN", "foot_share"), r(MF, "foot_share"), "FN", "MF")
    lt("FN", "somewhat narrower feet (foot breadth / length) than MF", "FN L36", m("FN", "foot_breadth") / m("FN", "foot_len"), m(MF, "foot_breadth") / m(MF, "foot_len"), "FN", "MF")
    for o in ("FN", "AE"):
        lt("VA", "somewhat smaller leg share than %s" % o, "VA L46, L140", r("VA", "leg_share"), r(o, "leg_share"), "VA", o)
    gt("AE", "somewhat longer face (FVB) than MF", "AE L214", c("AE", "FVB"), c(MF, "FVB"), "AE", "MF")
    gt("VA", "greater torso share than FN", "VA L35–46", r("VA", "torso_share"), r("FN", "torso_share"), "VA", "FN")
    for o in ("FN", "AE"):
        gt("VA", "deeper ribcage (depth / stature) than %s" % o, "VA L35–46", r("VA", "thorax_depth_share"), r(o, "thorax_depth_share"), "VA", o)
        gt("VA", "broader palms (palm breadth / hand) than %s" % o, "VA L114–141", r("VA", "palm_breadth_over_hand"), r(o, "palm_breadth_over_hand"), "VA", o)
        for k, n in (("elbow_over_humerus", "elbow"), ("wrist_over_forearm", "wrist"), ("knee_over_femur", "knee")):
            gt("VA", "more %s joint presence than %s" % (n, o), "VA L114–141", r("VA", k), r(o, k), "VA", o)
    gt("DU", "greater torso contribution than MF", "DU L11–40", r("DU", "torso_share"), r(MF, "torso_share"), "DU", "MF")
    lt("DU", "lower leg contribution than MF", "DU L11–40", r("DU", "leg_share"), r(MF, "leg_share"), "DU", "MF")
    gt("DU", "broad thorax (breadth / stature) vs MF", "DU L11–40", r("DU", "thorax_breadth_share"), r(MF, "thorax_breadth_share"), "DU", "MF")
    gt("DU", "deep thorax (depth / stature) vs MF", "DU L11–40", r("DU", "thorax_depth_share"), r(MF, "thorax_depth_share"), "DU", "MF")
    for k, n in (("elbow_over_humerus", "elbow"), ("wrist_over_forearm", "wrist"), ("knee_over_femur", "knee")):
        gt("DU", "substantial %s joint vs MF" % n, "DU L11–40", r("DU", k), r(MF, k), "DU", "MF")
    lt("DU", "arms lower in proportional contribution (shoulder joint-fingertip / stature) than MF", "DU L38, L113", r("DU", "arm_share"), r(MF, "arm_share"), "DU", "MF")
    lt("DU", "arms shorter in absolute length (shoulder joint-fingertip, cm) than MF", "DU L38, L113", m("DU", "arm"), m(MF, "arm"), "DU", "MF")
    gt("DU", "hands large for stature (hand / stature) vs MF", "DU L44, L115", r("DU", "hand_share"), r(MF, "hand_share"), "DU", "MF")
    lt("DU", "short neck (neck / stature) vs MF", "DU L107", r("DU", "neck_share"), r(MF, "neck_share"), "DU", "MF")
    gt("DU", "head share somewhat > MF (allometry)", "DU L170; RAC-04 L44", r("DU", "HH_share"), r(MF, "HH_share"), "DU", "MF")
    gt("DU", "cranial breadth / height (CBH) > MF", "DU L170", c("DU", "CBH"), c(MF, "CBH"), "DU", "MF")
    for o in (MF, "SK"):
        lt("GR", "lower torso share than %s" % o, "GR L198", r("GR", "torso_share"), r(o, "torso_share"), "GR", o)
        gt("GR", "greater leg share than %s" % o, "GR L213", r("GR", "leg_share"), r(o, "leg_share"), "GR", o)
        gt("GR", "greater arm / stature than %s" % o, "GR L221", r("GR", "arm_share"), r(o, "arm_share"), "GR", o)
        gt("GR", "greater span (DER) / stature than %s" % o, "GR L223", r("GR", "span_der"), r(o, "span_der"), "GR", o)
        gt("GR", "forearm / arm emphasized vs %s" % o, "GR L227", r("GR", "forearm_over_arm"), r(o, "forearm_over_arm"), "GR", o)
        gt("GR", "lower leg / leg emphasized vs %s" % o, "GR L215", r("GR", "shin_over_leg"), r(o, "shin_over_leg"), "GR", o)
        gt("GR", "finger / palm > %s" % o, "GR L235", r("GR", "finger_over_palm"), r(o, "finger_over_palm"), "GR", o)
        gt("GR", "facial vertical / breadth (FVB) > %s" % o, "GR L351", c("GR", "FVB"), c(o, "FVB"), "GR", o)
        gt("GR", "midface vertical (MVI) > %s" % o, "GR L360", c("GR", "MVI"), c(o, "MVI"), "GR", o)
    lt("GR", "thoracic breadth / stature less than SK", "GR L203", r("GR", "thorax_breadth_share"), r("SK", "thorax_breadth_share"), "GR", "SK")
    lt("GR", "thoracic depth never approaching DU proportional depth", "GR L204", r("GR", "thorax_depth_share"), r("DU", "thorax_depth_share"), "GR", "DU")
    ap("GR", "central anterior projection ≈ MF central (FPI)", "GR L362", c("GR", "FPI"), c(MF, "FPI"), "GR", "MF")
    gt("GO", "torso share > GR", "GO L169", r("GO", "torso_share"), r("GR", "torso_share"), "GO", "GR")
    lt("GO", "leg share < GR", "GO L196", r("GO", "leg_share"), r("GR", "leg_share"), "GO", "GR")
    lt("GO", "arm / stature < GR", "GO L200", r("GO", "arm_share"), r("GR", "arm_share"), "GO", "GR")
    lt("GO", "span < GR (span GR > GO)", "RA L131", r("GO", "span_der"), r("GR", "span_der"), "GO", "GR")
    gt("GO", "thoracic breadth GO > SK", "RAC-05 L32", r("GO", "thorax_breadth_share"), r("SK", "thorax_breadth_share"), "GO", "SK")
    gt("SK", "thoracic breadth SK > GR", "RAC-05 L32", r("SK", "thorax_breadth_share"), r("GR", "thorax_breadth_share"), "SK", "GR")
    for o in ("SK", "GR", MF):
        gt("GO", "thoracic depth / stature > %s" % o, "RAC-05 L32; GO L42", r("GO", "thorax_depth_share"), r(o, "thorax_depth_share"), "GO", o)
    for k, n in (("elbow_over_humerus", "elbow"), ("wrist_over_forearm", "wrist"), ("knee_over_femur", "knee")):
        gt("GO", "joint scale GO > GR (%s)" % n, "RAC-05 L32", r("GO", k), r("GR", k), "GO", "GR")
    gt("GO", "palm breadth / hand substantial (> MF)", "GO L210", r("GO", "palm_breadth_over_hand"), r(MF, "palm_breadth_over_hand"), "GO", "MF")
    gt("GO", "palm depth / hand substantial (> MF)", "GO L210", r("GO", "palm_depth_over_hand"), r(MF, "palm_depth_over_hand"), "GO", "MF")
    gt("GO", "cranial breadth / height (CBH) > MF", "GO L447", c("GO", "CBH"), c(MF, "CBH"), "GO", "MF")
    lt("PK", "central trunk share < MF (modest)", "RAC-04 L72 (T-2)", r("PK", "torso_share"), r(MF, "torso_share"), "PK", "MF")
    gt("PK", "pelvic vertical contribution / stature > MF", "RAC-04 L72; RAC-03 L35", r("PK", "pelvic_vertical_share"), r(MF, "pelvic_vertical_share"), "PK", "MF")
    gt("PK", "pelvis structurally important relative to thorax (crest / thorax breadth) > MF", "RAC-03 L35", r("PK", "pelvis_over_thorax_breadth"), r(MF, "pelvis_over_thorax_breadth"), "PK", "MF")
    C.append({"cand": "PK", "check": "legs never automatically exceed ordinary human proportions (leg share ≤ MF)", "canon": "RAC-04 L72",
              "a": "PK", "va": r("PK", "leg_share"), "b": "MF", "vb": r(MF, "leg_share"), "op": "≤", "pass": r("PK", "leg_share") <= r(MF, "leg_share")})
    gt("PK", "head share somewhat > MF only as allometry", "PK L33; RAC-04 L44", r("PK", "HH_share"), r(MF, "HH_share"), "PK", "MF")
    for k in ("torso_share", "arm_share", "leg_share"):
        ap("CG", "%s ≈ MF" % k, "CG L558", r("CG", k), r(MF, k), "CG", "MF")
    lt("CG", "narrow-to-moderate thorax (thoracic breadth / stature) vs MF", "CG L98, L102", r("CG", "thorax_breadth_share"), r(MF, "thorax_breadth_share"), "CG", "MF")
    lt("CG", "upper arm / arm < MF", "CG L571–575", r("CG", "upperarm_over_arm"), r(MF, "upperarm_over_arm"), "CG", "MF")
    gt("CG", "forearm / arm > MF", "CG L571–575", r("CG", "forearm_over_arm"), r(MF, "forearm_over_arm"), "CG", "MF")
    gt("CG", "hand / arm > MF", "CG L571–575", r("CG", "hand_over_arm"), r(MF, "hand_over_arm"), "CG", "MF")
    gt("CG", "finger / hand > MF", "CG L571–575", r("CG", "finger_over_hand"), r(MF, "finger_over_hand"), "CG", "MF")
    lt("CG", "femur / leg < MF", "CG L619–622", r("CG", "femur_over_leg"), r(MF, "femur_over_leg"), "CG", "MF")
    rng("CG", "head height (menton–vertex) roughly 11–13 cm", "CG L1585 (W1-A1)", c("CG", "HH"), 11.0, 13.0, "CG")
    C.append({"cand": "CG", "check": "face-to-vault (FVI) at or slightly above MF", "canon": "CG L1131", "a": "CG", "va": c("CG", "FVI"), "b": "MF",
              "vb": c(MF, "FVI"), "op": "≥", "pass": c("CG", "FVI") >= c(MF, "FVI")})
    # structural-mass axis Cogling -> Pipkin -> Durrim (joint breadth / adjacent bone)
    for k, n in (("wrist_over_forearm", "wrist"), ("knee_over_femur", "knee")):
        lt("CG", "structural-mass axis CG < PK (%s)" % n, "RAC-05 L32", r("CG", k), r("PK", k), "CG", "PK")
        lt("PK", "structural-mass axis PK < DU (%s)" % n, "RAC-05 L32; PK L68", r("PK", k), r("DU", k), "PK", "DU")
    gt("MF-FACE-PROJ-MAX", "projects more than the MF central face (FPI)", "MF L340 (AD-R40)", c("MF-FACE-PROJ-MAX", "FPI"), c(MF, "FPI"), "MAX", "MF")
    lt("MF-FACE-PROJ-MAX", "stays below the Saurin coupled-corner FPI (r3, 0.2920; W1 pass 1)", "SA floor (Part 7 0.255 = r3 0.292)", c("MF-FACE-PROJ-MAX", "FPI"), 0.29196, "MAX", "SA coupled corner")
    # Halvren: no-lineage general envelope must be source-plausible: inside the range spanned by its sources (MF, SG, FN, AE, VA)
    for k in ("torso_share", "leg_share", "arm_share", "forearm_over_arm", "shin_over_leg", "thorax_depth_share", "finger_over_hand", "wrist_over_forearm"):
        vals = [r(s, k) for s in (MF, "SG", "FN", "AE", "VA")]
        rng("HV", "%s within source span (MF, SG, FN, AE, VA)" % k, "HV L13, L31, L41 (source-plausible)", r("HV", k), min(vals), max(vals), "HV")
    return C

if __name__ == "__main__":
    C = run(sys.argv[1]); json.dump(C, open(sys.argv[2], "w"), indent=1, default=float)
    f = [c for c in C if not c["pass"]]
    print(len(C), "checks;", len(f), "fail")
    for c in f: print("FAIL", c["cand"], c["check"], c["va"], c["op"], c["vb"])
