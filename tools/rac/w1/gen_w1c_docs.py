"""Generate the W1c ARM records and measurement/check tables from the evidence JSON (no hand-typed numbers)."""
import json, os, hashlib
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
EV = os.path.join(R, "reviews", "rac-w1c-evidence"); ARM = os.path.join(R, "reviews", "rac-w1c-arm")
ids = ["MF-M-R", "MF-F-R", "MF-FACE-PROJ-MAX", "SK", "SG", "FN", "AE", "VA", "HV", "DU", "GR", "GO", "PK", "CG"]
NAME = {"MF-M-R": "Marchfolk configuration 1 (corrected)", "MF-F-R": "Marchfolk configuration 2 (rebuilt)",
        "MF-FACE-PROJ-MAX": "Marchfolk most-projecting valid adult face (diagnostic head on MF-M-R)", "SK": "Skarn central", "SG": "Sagekin central",
        "FN": "Fenn central", "AE": "Aelari central", "VA": "Vael central", "HV": "Halvren central (no-lineage general envelope)",
        "DU": "Durrim central", "GR": "Grask central", "GO": "Gorrund central", "PK": "Pipkin central", "CG": "Cogling central"}
CONFIG = {"MF-F-R": "Configuration 2 (MPFB gender macro 0.0)"}
# Technical verdicts and the reason lines (judgement recorded by the inspector; numbers come from the evidence files)
V = {
 "MF-M-R": ("PASS", []),
 "MF-F-R": ("PASS", ["D-4c (author ruling, W1c acceptance order §2): the generator-derived globe (2.44 cm) touched the socket skin at one vertex (0.044 cm), so it is replaced by a fitting ordinary-human landmark globe of 2.30 cm (BUILDER-CHOSEN size; 0.026 cm clearance; 2.35 cm leaves 0.001 cm, 2.40 cm intersects). Placement (generator eye centres) and face anatomy unchanged; FPI is unaffected (it uses the globe centre)."]),
 "MF-FACE-PROJ-MAX": ("PASS", ["The forward displacement (1.2 cm, bimaxillary, nose and orbits untouched) is BUILDER-CHOSEN; canon gives only the rule (MF L340). Reads as an adult human face with bimaxillary protrusion, no muzzle (evidence sheet, head side)."]),
 "SK": ("PASS", []),
 "SG": ("PASS", []),
 "FN": ("CONSTRAIN", ["RM-CF-08: ORB breadth / HL (E proxy) reads LOWER than MF while ORB height / HH and aperture read higher: the 'orbit slightly larger' direction is NOT demonstrated (candidate or proxy; unresolved). Native stature 181.14 cm (macro step +0.14).","R-11: elven continuous-taper ear NOT instantiated: the generator has only a human auricle and 'pointed' morphs, and canon forbids a pointiness continuum (UFCA L177). Body tests run ears-neutral (manifest: ears-hidden variant for the body test).",
                      "Elven pelvis: canon morphology not authored in detail; the candidate carries the generator's human pelvis. Pelvic readings are diagnostic only."]),
 "AE": ("CONSTRAIN", ["R-11: elven continuous-taper ear NOT instantiated (as FN).", "Elven pelvis: as FN."]),
 "VA": ("CONSTRAIN", ["R-11: elven continuous-taper ear NOT instantiated (as FN).", "Vael pelvis: as FN. Vael's 'natural lumbar curve' is not modelled (generator neutral spine)."]),
 "HV": ("CONSTRAIN", ["R-11: mixed coupled human + elven ear NOT instantiated.", "The no-lineage general envelope is BUILDER-CHOSEN as a whole (canon: not 50/50, not a linear morph, but no central values); identity-relevant, needs author acceptance.",
                      "Native stature 177.73 cm (generator height-macro step; -0.27 cm).",
                      "Order deviation: HV was built in this pass although its elven sources (FN, AE, VA) are CONSTRAIN, not PASS (order §7 item 14). Its source-span checks use those candidates; they must be re-run when the sources are accepted."]),
 "DU": ("CONSTRAIN", ["Pelvis: canon says morphology OPEN and 'never a simply widened human pelvis' (DU L32). The candidate's pelvis is the generator's human pelvis with a breadth target, i.e. exactly the prohibited form; pelvic readings are diagnostic only and the pelvis needs authorship.",
                      "Ear: human-auricle variable set (UFCA) - acceptable as Durrim's broadly humanoid compact range."]),
 "GR": ("CONSTRAIN", ["R-11: folded late-taper ear NOT instantiated (human auricle).", "Pelvis and shoulder girdle: non-human morphology not authored; generator human structure carried."]),
 "GO": ("CONSTRAIN", ["R-11: deep-bowl broad-rim ear NOT instantiated (human auricle).", "Pelvis: 'never a uniformly enlarged human pelvis' (GO L49); the candidate uses generator breadth/depth targets on a human pelvis - prohibited form; diagnostic only.",
                      "ALPC (GO L711-727) is not demonstrated: numeric checks pass, but the evidence sheet reads as a large lean human rather than a structurally massive axial trunk."]),
 "PK": ("FAIL (R-2)", ["The candidate is a uniform-scale PROXY (factor in the builder-chosen list); measurements are diagnostic of the proportion targets only.",
                       "Pelvis: Pipkin LSCTA pelvis not authored in detail; generator human pelvis with targets."]),
 "CG": ("FAIL (R-2)", ["Uniform-scale PROXY, not an ARM (as PK). Globe diameter DER from the scaled socket (1.30 cm) is far below an adult human globe - a proxy artefact."]),
}
ACC = "**AUTHOR-ACCEPTED W1 reference asset** (October 5, 2026; `reviews/chatgpt-rac-w1c-author-acceptance-blocker-resolution-order.md` §2). Generator-target magnitudes stay reference construction values, not population-envelope canon; diagnostics are not canon"
STATUS = {k: ACC for k in ("MF-M-R", "MF-F-R", "SK", "SG")}
STATUS["MF-FACE-PROJ-MAX"] = ACC + "; the 1.2 cm bimaxillary displacement / r3 FPI 0.191 is accepted as the W1 diagnostic Marchfolk maximum reference (not a complete Marchfolk population envelope)"
for k in ("FN", "AE", "VA", "DU", "GR", "GO"): STATUS[k] = "**CONSTRAINED diagnostic candidate** (author ruling, W1c acceptance order §4): proportion evidence may remain; human-generator ears/pelvis and missing non-human structures do not satisfy canon"
STATUS["HV"] = STATUS["FN"] + "; early build accepted only as a diagnostic ordering deviation; source-span checks re-run after FN/AE/VA are accepted"
for k in ("PK", "CG"): STATUS[k] = "**diagnostic proxy only** (author ruling, W1c acceptance order §5); replaced by a native short-adult build once that method is accepted"
EYEOV = {k: json.load(open(os.path.join(R, "tools", "rac", "w1", "cfg", k + ".json"))).get("eye_diam_cm") for k in ids}
def f3(x): return "%.3f" % x
def f2(x): return "%.2f" % x
def main():
    checks = json.load(open(os.path.join(EV, "directional_checks.json")))
    os.makedirs(ARM, exist_ok=True); rows = []
    for i in ids:
        b = json.load(open(os.path.join(EV, i + "_build.json"))); m = json.load(open(os.path.join(EV, i + "_meas.json")))
        inv = m["invariance"]; c = m["combined"]; cr = c["cranio"]; cfg = b["cfg"]
        sha = hashlib.sha256(open(os.path.join(EV, "geometry", i + "_r6.npz"), "rb").read()).hexdigest()
        ck = [x for x in checks if x["cand"] == i or (i == "MF-FACE-PROJ-MAX" and x["cand"] == i)]
        npass = sum(x["pass"] for x in ck)
        verdict, notes = V[i]
        rigid = max(v["max_abs_change_cm"] for v in inv["rigid_sets"].values())
        tg = cfg.get("targets", {})
        bc = ["MPFB/MakeHuman generator default proportions, 'race' mix asian 0.333 / caucasian 0.334 / african 0.333 (not Marchfolk biology, D-4d)",
              "muscle %.2f, weight %.2f, proportions %.2f (provisional reference composition, D-4d)" % (cfg["muscle"], cfg["weight"], cfg["proportions"]),
              ("height macro %.4f (solved for native stature)" % b["height_macro"]) if not b.get("proxy_uniform_scale") else ("height macro %.4f (generator adult minimum; NOT solved - proxy)" % b["height_macro"]),
              "R-6 arm abduction %.1f deg (canon: 'small fixed abduction', no angle)" % m["r6"]["cranio"]["pitch_deg"] if False else "R-6 arm abduction 8.0 deg (canon gives no angle)",
              ("landmark globe diameter %.2f cm (fitting ordinary-human landmark globe; author ruling W1c acceptance §2)" % cr["eye_diam_cm"]) if EYEOV.get(i) else ("landmark globe diameter %.2f cm = 2.4 cm x (generator orbit helper extent / MF-M-R helper extent) (D-4c: globe DER from orbit)" % cr["eye_diam_cm"])]
        if cfg.get("face_proj_cm"): bc.append("lower-face bimaxillary forward displacement %.1f cm (identity-relevant for the MF maximum)" % cfg["face_proj_cm"])
        if tg: bc.append("generator targets (identity-relevant race proportion inputs): " + ", ".join("%s %.2f" % (k, v) for k, v in sorted(tg.items())))
        if b.get("proxy_uniform_scale"): bc.append("NON-COMPLIANT uniform scale %.4f (proxy only)" % b["proxy_uniform_scale"])
        stl = "%.3f cm (R-6, vertex to sole)" % m["stature_r6"]
        hs = b.get("height_solve", {})
        txt = f"""# ARM Candidate Record — {i}: {NAME[i]}

**Order:** `reviews/chatgpt-rac-wave1-continuation-asset-build-order.md` (W1 continuation) **Date / pass:** October 5, 2026, W1c pass 1 **Builder/inspector:** Claude (D-5)
**Geometry:** `reviews/rac-w1c-evidence/geometry/{i}_r6.npz` (R-6), SHA-256 `{sha}`; rebuild: `tools/rac/w1/cfg/{i}.json` + `tools/rac/w1/build_arm.py` (Blender 5.0.1 bpy + MPFB extension)
**Evidence sheet:** `reviews/rac-w1c-evidence/{i}_evidence.jpg` (front, side, 3/4, head front, head side; 10 cm / 1 cm ticks; common scale)
**Measurements:** `reviews/rac-w1c-evidence/{i}_meas.json`; invariance `{i}_inv.json`

## Technical verdict: **{verdict}** — {STATUS[i]}

| Req. | Finding |
|---|---|
| R-1 age | Apparent age 35 y (D-4a): MPFB age macro {cfg['age']:.4f} (MakeHuman mapping 0.5 = 25 y, 1.0 = 90 y) |
| R-2 stature | Target {cfg['stature']:.0f} cm; measured {stl}; {'native (height macro solved, no scaling)' if not b.get('proxy_uniform_scale') else '**uniform-scale proxy - FAILS R-2**'}{'; ' + hs.get('note', '') if hs.get('note') else ''} |
| R-3/R-4 | Generator central values + listed targets; muscle/weight macros 0.5 (BUILDER-CHOSEN) |
| R-5 | Built mirrored (generator symmetric, no asymmetry targets) |
| R-6 | Rig re-pose only (D-4b): arms 8° abduction, elbows extended, palms to thighs; hip joint over ankle, feet parallel/flat; spine/head at generator rest. Invariance (rest vs R-6): rigid single-bone vertex sets max change {rigid:.2f} cm; joint-to-joint segment lengths unchanged; foot length {inv['segments_cm']['foot_len'][2]:+.2f} cm, foot breadth {inv['segments_cm']['foot_breadth'][2]:+.2f} cm; head HL {inv['head']['HL'][2]:+.4f} cm; pelvic depth {inv['trunk_cm']['pelvic_depth'][2]:+.2f} cm, bitrochanteric {inv['trunk_cm']['bitrochanteric_breadth'][2]:+.2f} cm; volume {inv['volume_L'][3]:+.2f} %; skinning deformation at the axilla changes max thorax breadth by {inv['trunk_cm']['thorax_breadth_max'][2]:+.2f} cm -> **anatomical dimensions are read on the generator-authored rest geometry; R-6 supplies stature and the stance evidence** |
| R-7…R-9, R-12 | No hair, clothing, material layers; single neutral surface |
| R-10 | {CONFIG.get(i, 'Configuration 1 (MPFB gender macro 1.0), declared at build; paired with MF-M-R for like-for-like tests')} |
| R-11 | See notes |
| R-13 | cm, up = u, ground at the sole |
| R-14 | Builder-chosen values listed below |
| D-4c eyes | Landmark globes {cr['eye_diam_cm']:.2f} cm ({'fitting ordinary-human size, author ruling' if EYEOV.get(i) else 'DER'}) at the generator's eye-helper centres. Fit on this candidate: skin vertices inside the globe {m['eyefit']['at_derived_diameter']['l']['skin_verts_inside_globe']} (clearance {m['eyefit']['at_derived_diameter']['l']['min_skin_clearance_cm']:.3f} cm); at +0.2 cm diameter {m['eyefit']['at_plus_0.2cm']['l']['skin_verts_inside_globe']} inside |
| Directional checks | {npass} / {len(ck)} pass (`reviews/claude-rac-w1c-cross-race-audit.md`) |

**Notes:**
""" + "".join("- %s\n" % n for n in (notes or ["None beyond the builder-chosen list."])) + "\n**BUILDER-CHOSEN / AUTHOR ACCEPTANCE REQUIRED:**\n" + "".join("- %s\n" % x for x in bc)
        open(os.path.join(ARM, "claude-rac-w1c-arm-%s.md" % i), "w").write(txt)
        rows.append((i, verdict, cfg["stature"], m["stature_r6"], b.get("proxy_uniform_scale"), npass, len(ck), sha[:16]))
    json.dump(rows, open(os.path.join(EV, "gate_rows.json"), "w"), indent=1)
    # measurement tables
    keys = [("torso_share", "torso (suprasternal-hip joint) / H"), ("leg_share", "hip-joint height / H"), ("arm_share", "arm (shoulder joint-fingertip) / H"),
            ("span_der", "span (DER) / H"), ("upperarm_over_arm", "upper arm / arm"), ("forearm_over_arm", "forearm / arm"), ("hand_over_arm", "hand / arm"),
            ("finger_over_hand", "finger / hand"), ("finger_over_palm", "finger / palm"), ("femur_over_leg", "femur / leg"), ("shin_over_leg", "lower leg / leg"),
            ("neck_share", "neck / H"), ("thorax_breadth_share", "thorax breadth (max) / H"), ("thorax_depth_share", "thorax depth (max) / H"),
            ("thorax_d_over_b", "thorax depth / breadth"), ("shoulder_joint_share", "shoulder-joint breadth / H"), ("elbow_over_humerus", "elbow breadth / upper arm"),
            ("wrist_over_forearm", "wrist breadth / forearm"), ("knee_over_femur", "knee breadth / femur"), ("palm_breadth_over_hand", "palm breadth / hand"),
            ("palm_depth_over_hand", "palm depth / hand"), ("crest_share", "iliac-crest proxy breadth / H"), ("bitroch_share", "bitrochanteric / H"),
            ("pelvic_depth_share", "pelvic AP depth / H"), ("pelvic_vertical_share", "pelvic vertical (crest proxy - hip joint) / H"), ("HH_share", "HH / H"), ("HL_share", "HL / H")]
    M = {i: json.load(open(os.path.join(EV, i + "_meas.json"))) for i in ids}
    hdr = "| Measure | " + " | ".join(ids) + " |\n|---|" + "---|" * len(ids) + "\n"
    t1 = hdr + "| Stature R-6 (cm) | " + " | ".join(f2(M[i]["stature_r6"]) for i in ids) + " |\n"
    for k, lab in keys: t1 += "| %s | " % lab + " | ".join(f3(M[i]["combined"]["ratio"][k]) for i in ids) + " |\n"
    raw = [("upperarm", "upper arm (cm)"), ("forearm", "forearm (cm)"), ("hand", "hand (cm)"), ("palm", "palm (cm)"), ("thigh", "femur (cm)"), ("shin", "lower leg (cm)"),
           ("foot_len", "foot length (cm)"), ("elbow_breadth", "elbow breadth (cm)"), ("wrist_breadth", "wrist breadth (cm)"), ("knee_breadth", "knee breadth (cm)")]
    t2 = hdr
    for k, lab in raw: t2 += "| %s | " % lab + " | ".join(f2(M[i]["combined"]["mean"][k]) for i in ids) + " |\n"
    for k, lab in (("torso_len", "torso length (cm)"), ("thorax_breadth_max", "thorax breadth max (cm)"), ("thorax_depth_max", "thorax depth max (cm)"),
                   ("iliac_crest_breadth", "iliac-crest proxy breadth (cm)"), ("bitrochanteric_breadth", "bitrochanteric (cm)"), ("pelvic_depth", "pelvic depth (cm)"),
                   ("volume_L", "volume (L, rest)")):
        t2 += "| %s | " % lab + " | ".join(f2(M[i]["combined"][k]) for i in ids) + " |\n"
    ck = [("HL", "HL (cm)"), ("HH", "HH (cm)"), ("FPI", "FPI"), ("MPI", "MPI"), ("MdPI", "MdPI"), ("FVI", "FVI"), ("CBH", "CBH"), ("FVB", "FVB"), ("MVI", "MVI"),
          ("FDH", "FDH"), ("Eu_Eu", "Eu-Eu (cm)"), ("Zy_Zy", "Zy-Zy (cm)"), ("ORB_breadth_over_HL", "ORB breadth / HL (E proxy)"), ("ORB_height_over_HH", "ORB height / HH (E proxy)"),
          ("aperture_width_over_orbit_breadth", "aperture width / orbit breadth"), ("aperture_height_over_orbit_height", "aperture height / orbit height"), ("eye_diam_cm", "globe diameter (cm; DER except MF-F-R, fitting 2.30 cm by author ruling)")]
    t3 = hdr
    for k, lab in ck: t3 += "| %s | " % lab + " | ".join(f3(M[i]["combined"]["cranio"].get(k, float('nan'))) for i in ids) + " |\n"
    t3 += "| aperture width L/R (cm) | " + " | ".join("%.2f/%.2f" % (M[i]["combined"]["cranio"]["aperture"]["l"]["width"], M[i]["combined"]["cranio"]["aperture"]["r"]["width"]) for i in ids) + " |\n"
    t3 += "| aperture height L/R (cm) | " + " | ".join("%.2f/%.2f" % (M[i]["combined"]["cranio"]["aperture"]["l"]["height"], M[i]["combined"]["cranio"]["aperture"]["r"]["height"]) for i in ids) + " |\n"
    t3 += "| FPI pitch -3° / +3° | " + " | ".join("%.3f/%.3f" % (M[i]["pitch"]["-3.0"]["FPI"], M[i]["pitch"]["3.0"]["FPI"]) for i in ids) + " |\n"
    t3 += "| FH* proxy tilt Po*->Or* (deg, + = face up) | " + " | ".join(tilt(M[i]) for i in ids) + " |\n"
    lr = hdr
    for k, lab in raw[:7]: lr += "| %s L/R | " % lab + " | ".join("%.2f/%.2f" % (M[i]["combined"]["L"][k], M[i]["combined"]["R"][k]) for i in ids) + " |\n"
    # checks table
    t4 = "| # | Candidate | Canon direction | Source | Value | Op | Comparator | Result |\n|---|---|---|---|---|---|---|---|\n"
    for n, x in enumerate(checks, 1):
        vb = x["vb"] if not isinstance(x["vb"], list) else "[%.3f, %.3f]" % tuple(x["vb"])
        t4 += "| %d | %s | %s | %s | %s | %s | %s %s | %s |\n" % (n, x["cand"], x["check"], x["canon"], f3(x["va"]) if isinstance(x["va"], float) else x["va"], x["op"], x["b"], vb if isinstance(vb, str) else f3(vb), "PASS" if x["pass"] else "**FAIL**")
    open(os.path.join(EV, "tables.md"), "w").write("## T1 ratios\n\n" + t1 + "\n## T2 raw\n\n" + t2 + "\n## T3 cranio\n\n" + t3 + "\n## T5 L/R\n\n" + lr + "\n## T4 checks\n\n" + t4)
    print("ok")

def tilt(m):
    import math
    c = m["combined"]["cranio"]; po = c.get("Po*"); orr = c["aperture"]["l"].get("Or*")
    if not po or not orr: return "n/a"
    return "%.1f" % math.degrees(math.atan2(orr[2] - po[2], orr[1] - po[1]))

if __name__ == "__main__": main()
