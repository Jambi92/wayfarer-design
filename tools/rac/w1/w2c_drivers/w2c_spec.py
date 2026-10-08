# RAC W2C comparison-row specification (canon sources in the 'note'); writes the spec JSON read by w2c_eval.py (W2C_SPEC).
# Usage: python3 w2c_spec.py OUT.json [extremes.json]
import sys, json
rows, inv = [], []
import os
FN, FB = os.environ.get('W2C_FRAMES', 'GRN,GRB').split(',')
def r(code, chk, a, op, b, k, note="", report=False, adj=None): rows.append({"code": code, "check": chk, "a": a, "op": op, "b": b, "k": k, "note": note, "report": report, **({"adj_joint": adj} if adj else {})})
TB, SJ, BI, CR, TD = ("skeletal thoracic breadth / stature [t=0.0]", "skeletal shoulder-joint breadth / stature [t=0.0]", "skeletal biacromial / stature [t=0.0]",
                      "skeletal crest breadth / stature [t=0.0]", "skeletal thoracic depth / stature [t=0.0]")
PROP = [("torso_share", "<", "GR L198"), ("leg_share", ">", "GR L198, L233"), ("arm_share", ">", "GR L164, L241"), ("span_der", ">", "GR L243 (derived span)"),
        ("forearm_over_arm", ">", "GR L59, L247"), ("shin_over_leg", ">", "GR L320 (lower-leg emphasis)")]
# S: matched-height Grask vs Skarn (GR L104, L285; neutral composition 0.5 / 0.5 both)
for h, g, s in (("198", "GR198", "SK198"), ("208", "GR208", "SK208"), ("218", "GR218", "SK218"), ("229", "GR229", "SK229")):
    for k, op, src in PROP: r("S", "%s cm: Grask %s Skarn: %s" % (h, op, k), g, op, s, k, src)
    for k, src in ((TB, "GR L203; RM-LR-02 (a)"), (SJ, "GR L42; RM-LR-02 (d)"), (BI, "GR L42 (girdle breadth)"), ("thorax_breadth_share", "GR L203 (skin)")):
        r("S", "%s cm: Grask < Skarn: %s" % (h, k), g, "<", s, k, src)
    r("S", "%s cm: Grask > Skarn: finger / palm" % h, g, ">", s, "finger_over_palm", "GR L255")
    r("S", "%s cm: non-human pelvic organization, crest / stature < Skarn" % h, g, "<", s, CR, "GR-P5 (vs MF); vs SK report", report=True)
    r("S", "%s cm: thoracic depth / stature vs Skarn (undetermined by design)" % h, g, "<", s, TD, "RMQ RM-LR-02: SK vs GR depth undetermined", report=True)
    for j in ("elbow", "wrist", "knee", "ankle"): r("S", "%s cm: %s breadth / stature vs Skarn" % (h, j), g, "<", s, "%s breadth / stature (scaled slab)" % j, "RM-LR-05: SK vs GR joints undetermined", report=True)
# B: span vs Broad Skarn (W1 NOT DEMONSTRATED diagnostic) with the accepted W2 frames
for g in ("GR218", FB, FN):
    r("B", "%s span (derived) > Broad Skarn 218 (W2B frame)" % g, g, ">", "SKB218", "span_der", "GR L243; W1k / W1l diagnostic")
    r("B", "%s arm / stature > Broad Skarn 218" % g, g, ">", "SKB218", "arm_share", "GR L164")
# F: frames stay Grask (GR L270): Broad not Skarn / Gorrund; Narrow rangy, not fragile
for k, op, src in PROP[:4]: r("F", "Broad Grask %s Broad Skarn 218: %s" % (op, k), FB, op, "SKB218", k, src)
r("F", "Broad Grask < Broad Skarn 218: skeletal thoracic breadth", FB, "<", "SKB218", TB, "GR L270 (not Skarn)")
r("F", "Broad Grask < Broad Skarn 218: skeletal shoulder-joint breadth", FB, "<", "SKB218", SJ, "GR L42, L270")
for go in ("GO217", "GO224"):
    for k, op, src in PROP[:4]: r("F", "Broad Grask %s accepted Gorrund %s: %s" % (op, go, k), FB, op, go, k, "GR L270 (no Gorrund assumptions); GO L221")
    r("F", "Broad Grask < accepted Gorrund %s: skin thoracic depth / stature" % go, FB, "<", go, "thorax_depth_share", "RM-LR-02 (b)")
    r("F", "Broad Grask < accepted Gorrund %s: skin shoulder-joint breadth / stature" % go, FB, "<", go, "shoulder_joint_share", "AD-G6")
for k, op, src in PROP: r("F", "Narrow Grask %s Marchfolk 173: %s (limb architecture kept)" % (op, k), FN, op, "MF173", k, src)
r("F", "Narrow Grask knee / femur vs Marchfolk (J-1 joint floor; not fragile)", FN, ">", "MF173", "knee_over_femur", "REFERENCE_ANATOMY J-1; GR L269", report=True)
r("F", "Narrow Grask elbow / humerus vs Marchfolk (J-1 joint floor; not fragile)", FN, ">", "MF173", "elbow_over_humerus", "REFERENCE_ANATOMY J-1; GR L269", report=True)
# H: minimum-height Grask vs maximum Marchfolk (GR L106), Sagekin report
for k, op, src in PROP: r("H", "Grask 198 %s Marchfolk 203 (accepted W2A): %s" % (op, k), "GR198", op, "MF203", k, src)
r("H", "Grask 198 > Marchfolk 203: finger / palm", "GR198", ">", "MF203", "finger_over_palm", "GR L255")
r("H", "Grask 198 <= Marchfolk 203: crest / stature (GR-P5)", "GR198", "<=", "MF203", CR, "GR-P5")
for k, op, src in PROP: r("H", "Grask 198 %s Sagekin W1 (178 cm): %s" % (op, k), "GR198", op, "SG", k, src + "; Sagekin W2 not run", report=True)
# M: composition (GR L271): shares unchanged; identity vs Skarn / Marchfolk at the same composition
for c in ("GR-BODY-06", "GR-BODY-07", "GR-BODY-08", "GR-BODY-09", "GR-LOW"):
    inv.append({"code": "M", "check": "%s: composition does not redefine anatomy (torso, leg, arm, span, forearm, lower-leg within 1 %%)" % c, "a": c, "b": "GR218",
                "keys": ["torso_share", "leg_share", "arm_share", "span_der", "forearm_over_arm", "shin_over_leg"]})
for g, s, tag in (("GR-BODY-06", "SK-LOWMUS", "low muscle: not a tall thin human / still Grask vs Skarn"), ("GR-BODY-07", "SK-HIMUS", "high muscle: not Skarn with longer arms"),
                  ("GR-BODY-08", "SK-HIFAT", "higher fat: not a generic fat giant"), ("GR-BODY-09", "SK-HIBOTH", "high muscle + fat keeps the long-limbed skeleton"), ("GR-LOW", "SK-LOW", "low composition")):
    for k, op, src in PROP[:4]: r("M", "%s — %s %s %s: %s" % (tag, g, op, s, k), g, op, s, k, src + "; same composition")
    r("M", "%s — %s < %s: skin thoracic breadth / stature" % (tag, g, s), g, "<", s, "thorax_breadth_share", "GR L203, L271")
    r("M", "%s — %s < %s: skin shoulder-joint breadth / stature" % (tag, g, s), g, "<", s, "shoulder_joint_share", "GR L42, L271")
for k, op, src in PROP[:4]: r("M", "low composition Grask %s Marchfolk low (0.25 / 0.25): %s" % (op, k), "GR-LOW", op, "MF-LOW", k, src + "; same composition")
for k, op, src in PROP[:4]: r("M", "low muscle Grask %s Marchfolk low: %s (not a tall thin human)" % (op, k), "GR-BODY-06", op, "MF-LOW", k, src + "; nearest human low-composition reference", report=True)
# X: named extremes (GRASK L131-132, L306-316, L279) and boundaries AD-2 / AD-3 (GR L736-737; GO L253)
G10 = "GR-BODY-10"
for k, src in ((TB, "AD-2: thoracic breadth / stature"), (SJ, "AD-2: shoulder breadth / stature"), (BI, "AD-2: girdle (acromial) breadth"), (CR, "AD-2: non-human pelvic organization (crest)"),
               ("thorax_breadth_share", "AD-2 (skin)")):
    r("AD2", "GR-BODY-10 < Skarn 218 (matched height): %s" % k, G10, "<", "SK218", k, src)
r("AD2", "GR-BODY-10 > Skarn 218: finger / palm (hand and digit relationship)", G10, ">", "SK218", "finger_over_palm", "AD-2: hand / digit")
r("AD2", "GR-BODY-10 vs Skarn 218: neck / stature (neck relationship; direction not authored)", G10, "<", "SK218", "neck_share", "AD-2: neck relationship", report=True)
for k, op, src in PROP: r("AD2", "GR-BODY-10 %s Skarn 218: %s (limb carrier, shown for context)" % (op, k), G10, op, "SK218", k, src, report=True)
for go in ("GO217", "GO224"):
    for k, op in (("leg_share", ">"), ("arm_share", ">"), ("span_der", ">"), ("torso_share", "<")):
        r("AD3", "GR-BODY-10 %s accepted Gorrund W1 %s: %s (Grask side of the floor; PROVISIONAL PENDING GORRUND W2)" % (op, go, k), G10, op, go, k, "AD-3 / RM-LR-04; comparator = accepted W1 Gorrund central family, not a limb-present family")
for g, tag in (("GR-BODY-11", "longer-limbed"), ("GR-BODY-12", "forearm emphasis"), ("GR-BODY-13", "upper-arm emphasis"), ("GR-BODY-14", "long hand")):
    for k, op, src in PROP[:4]: r("X", "%s (%s) %s Skarn 218: %s" % (g, tag, op, k), g, op, "SK218", k, src)
for g in ("GR-BODY-12", "GR-BODY-13"):
    inv.append({"code": "X", "check": "%s: arm / stature held at the central value (within 1 %%)" % g, "a": g, "b": "GR218", "keys": ["arm_share"]})
for g, s, tag in (("GR-BODY-15", "SK-LOWMUS", "Broad + low muscle"), ("GR-BODY-16", "SK-HIMUS", "Narrow + high muscle")):
    for k, op, src in PROP[:4]: r("X", "%s (%s) %s %s: %s" % (g, tag, op, s, k), g, op, s, k, src + "; same composition")
    r("X", "%s (%s) < %s: skin thoracic breadth / stature" % (g, tag, s), g, "<", s, "thorax_breadth_share", "GR L270-271")
    r("X", "%s (%s) < %s: skin shoulder-joint breadth / stature" % (g, tag, s), g, "<", s, "shoulder_joint_share", "GR L42, L270")
    inv.append({"code": "X", "check": "%s: composition and frame do not redefine anatomy vs central" % g, "a": g, "b": "GR218", "keys": ["torso_share", "leg_share", "arm_share", "forearm_over_arm", "shin_over_leg"]})
for k, op, src in PROP: r("X", "GR-BODY-18 (198 Broad) %s Skarn 198: %s" % (op, k), "GR-BODY-18", op, "SK198", k, src)
for k, src in ((TB, "GR L270 (Broad not Skarn)"), (SJ, "GR L42, L270")): r("X", "GR-BODY-18 (198 Broad) < Skarn 198: %s" % k, "GR-BODY-18", "<", "SK198", k, src)
for k, op, src in PROP: r("X", "GR-BODY-18 (198 Broad) %s Marchfolk 203: %s" % (op, k), "GR-BODY-18", op, "MF203", k, src)
inv.append({"code": "X", "check": "GR-BODY-17 (239 Narrow): frame does not change lengths vs GR239", "a": "GR-BODY-17", "b": "GR239", "keys": ["torso_share", "leg_share", "arm_share", "forearm_over_arm", "shin_over_leg", "HH_share"], "tol": 0.005})
inv.append({"code": "X", "check": "GR-BODY-18 (198 Broad): frame does not change lengths vs GR198", "a": "GR-BODY-18", "b": "GR198", "keys": ["torso_share", "leg_share", "arm_share", "forearm_over_arm", "shin_over_leg", "HH_share"], "tol": 0.005})
r("X", "GR-BODY-17 (239 Narrow) < GR239: skeletal thoracic breadth (frame moves at maximum height)", "GR-BODY-17", "<", "GR239", TB, "GR L270")
r("X", "GR-BODY-18 (198 Broad) > GR198: skeletal thoracic breadth (frame moves at minimum height)", "GR-BODY-18", ">", "GR198", TB, "GR L270")
r("X", "Narrow Grask vs Aelari W1: skeletal thoracic breadth / stature (Aelari convergence; report)", FN, ">", "AE", TB, "GR L269", report=True)
r("X", "Narrow Grask > Aelari W1: arm / stature (limb- and reach-dominant)", FN, ">", "AE", "arm_share", "GR L286")
r("X", "Narrow Grask > Aelari W1: forearm / arm", FN, ">", "AE", "forearm_over_arm", "GR L286")
r("X", "Narrow Grask < Aelari W1: neck / stature (Aelari elongation vertically distributed)", FN, "<", "AE", "neck_share", "GR L174, L286")
X = json.load(open(sys.argv[2])) if len(sys.argv) > 2 else {}
rows += X.get("rows", []); inv += X.get("invariance", [])
json.dump({"rows": rows, "invariance": inv}, open(sys.argv[1], "w"), indent=1); print(len(rows), "rows", len(inv), "invariance")
