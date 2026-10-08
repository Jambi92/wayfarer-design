# RAC W2G (Halvren central envelope) comparison specification. Canon: specs/halvren/HALVREN_V1.md (HV L = line), the accepted W1 Halvren rows
# ('source-plausible': inside the span of MF, SG, FN, AE, VA), order reviews/chatgpt-rac-w2f-final-acceptance-w2g-halvren-order.md (§ = section).
# Only the canon's own pass / fail directions are scored; every other comparison is REPORT. Usage: python3 w2g_spec.py OUT.json
import sys, json
rows, inv, mv, spans, passing = [], [], [], [], []
def r(code, chk, a, op, b, k, note="", report=False): rows.append({"code": code, "check": chk, "a": a, "op": op, "b": b, "k": k, "note": note, "report": report})
T0 = " [t=0.0]"
sk = lambda x: "skeletal %s%s" % (x, T0)
JP = lambda j: "%s breadth / adjacent segment (exact-plane section)" % j
JS = lambda j: "%s breadth / stature (exact-plane section)" % j
TB, TD, SJ, BI, CR, PD, PV, HS, BC, WI = map(sk, ("thoracic breadth / stature", "thoracic depth / stature", "shoulder-joint breadth / stature", "biacromial / stature",
                                               "crest breadth / stature", "AP pelvic depth / stature", "pelvic vertical / stature", "hip-joint spacing / stature",
                                               "bitrochanteric / crest", "waist interval / torso"))
# the accepted W1 Halvren source-plausible readings (directional_checks.py HV rows), wrist read on the exact plane
CANON = ["torso_share", "leg_share", "arm_share", "forearm_over_arm", "shin_over_leg", "thorax_depth_share", "finger_over_hand", JP("wrist")]
BODY = ["torso_share", "leg_share", "arm_share", "span_der", "forearm_over_arm", "shin_over_leg", "neck_share", "hand_share", "finger_over_hand", "palm_breadth_over_hand",
        "foot_share", "thorax_breadth_share", "thorax_depth_share", JP("elbow"), JP("wrist"), JP("knee"), JP("ankle"), TB, TD, SJ, CR, PD, PV, WI]
AXIAL = [TB, TD, SJ, BI, CR, PD, PV, HS, BC, WI, sk("pelvic AP / thoracic depth"), sk("pelvic vertical / thoracic vertical"), sk("crest / thoracic breadth")]
# matched-height accepted W2 source bodies (canon span sources MF, SG, FN, AE, VA; Skarn listed separately as the large-human source)
SRC = {152: ["MF152", "SG152"], 163: ["MF163", "SG163", "FN163", "VA163"], 173: ["MF173", "SG173", "FN173", "AE173", "VA173"],
       178: ["MF178", "SG178", "FN178", "AE178", "VA178"], 181: ["MF181", "SG181", "FN181", "AE181", "VA181"], 190: ["MF190", "SG190", "FN190", "AE190", "VA190"],
       203: ["MF203", "SG203", "FN203", "AE203", "VA203"]}
SKAT = {190: "SK190", 203: "SK203", 213: "SK208"}
HV = {h: "HV%d" % h for h in (152, 163, 173, 178, 181, 190, 203, 213)}
# U: allometry
r("U", "head share: 152 > 178", "HV152", ">", "HV178", "HH_share", "RM-UB-02; HV-11"); r("U", "head share: 213 < 178", "HV213", "<", "HV178", "HH_share", "RM-UB-02; HV-12")
for k in ("hand_share", "foot_share", "neck_share", "neck / torso", JS("knee"), "femoral S7 breadth / stature" + T0):
    r("U", "%s: 152 vs 178" % k.replace(T0, ""), "HV152", ">", "HV178", k, "RM-UB-02 diagnostic", True); r("U", "%s: 213 vs 178" % k.replace(T0, ""), "HV213", "<", "HV178", k, "RM-UB-02 diagnostic", True)
# O: source-plausible spans at matched height (accepted W1 Halvren rows, read at matched height against the accepted W2 families)
for h, srcs in SRC.items():
    for k in CANON: spans.append({"code": "O", "check": "%d cm: Halvren inside the matched source span: %s" % (h, k), "a": HV[h], "srcs": srcs, "k": k})
    for k in [x for x in BODY if x not in CANON]: spans.append({"code": "O", "check": "%d cm: Halvren vs matched source span: %s" % (h, k.replace(T0, "")), "a": HV[h], "srcs": srcs, "k": k, "report": True})
    for k in AXIAL: spans.append({"code": "A", "check": "%d cm: axial / pelvic reading vs matched source span: %s" % (h, k.replace(T0, "")), "a": HV[h], "srcs": srcs, "k": k, "report": True})
# 152 cm: the elves' accepted floor is 157 cm (no elf body at 152); report span with the nearest accepted elf bodies FN157 / VA157 (boundary-stature rule)
for k in CANON + [x for x in BODY if x not in CANON]: spans.append({"code": "O", "check": "152 cm vs MF152 / SG152 + nearest accepted elves FN157 / VA157 (report): %s" % k.replace(T0, ""), "a": "HV152", "srcs": ["MF152", "SG152", "FN157", "VA157"], "k": k, "report": True})
for h in (213,):
    for k in CANON: spans.append({"code": "O", "check": "213 cm vs the tallest accepted sources (MF203, SG208, FN211, AE211; report)", "a": "HV213", "srcs": ["MF203", "SG208", "FN211", "AE211"], "k": k, "report": True})
# P: body-only source passing at matched height (§6): exact duplication = fewer than 2 of the 24 body readings separate by >= 1 %
for h, srcs in SRC.items():
    for s in srcs + ([SKAT[h]] if h in SKAT else []):
        passing.append({"code": "P", "check": "%d cm: Halvren central body vs %s (body-only, neutralized)" % (h, s), "a": HV[h], "b": s, "keys": BODY, "min_sep": 2})
passing.append({"code": "P", "check": "213 cm: Halvren vs Skarn 208 (nearest accepted Skarn; report)", "a": "HV213", "b": "SK208", "keys": BODY, "report": True})
# X: source-influenced expression (§7; HV-13...17 body portions) at 178 cm: tendency moves vs HVC1, and no exact duplication of the source
# the named readings per influence (canon systems, §7; HV-13...17); a tendency = the expression moves from HVC1 TOWARD the matched source on that reading
EXPR = {"HVXFN": ("FN178", ["forearm_over_arm", "shin_over_leg", "hand_share", "finger_over_hand", "foot_share", JP("wrist"), JP("knee"), JP("ankle"), "thorax_depth_share"], "Fenn-influenced: extremities, forearm / lower leg, gracility, shallower thorax (§7)"),
        "HVXAE": ("AE178", ["neck_share", "neck / torso", "arm_share", "leg_share", "forearm_over_arm", "shin_over_leg", "thorax_depth_share", JP("wrist"), JP("knee"), JP("ankle")], "Aelari-influenced: vertical continuity, neck, even elongation, gracility (§7)"),
        "HVXVA": ("VA178", ["thorax_depth_share", "palm_breadth_over_hand", "hand_share", "shin_over_leg", TD], "Vael-influenced: deeper thorax, compact torso-pelvis, stronger base (§7)"),
        "HVXSK": ("SK183", ["thorax_depth_share", TD, SJ, "torso_share", JP("knee"), JP("wrist"), JP("ankle"), "hand_share"], "Skarn-influenced: structural presence, depth, joints, hand / foot scale (§7)"),
        "HVXSG": ("SG178", ["leg_share", "torso_share", "forearm_over_arm", "shin_over_leg", "finger_over_hand", "thorax_depth_share"], "Sagekin-influenced: linear human-family relationships (§7)"),
        "HVXMF": ("MF178", [], "Marchfolk-influenced: broad human-family distribution (§7)")}
toward = []
for x, (src, ks, note) in EXPR.items():
    for k in ks: toward.append({"code": "X", "check": "%s moves from HVC1 toward %s: %s" % (x, src, k.replace(T0, "")), "a": x, "base": "HV178", "src": src, "k": k, "note": note})
    passing.append({"code": "X", "check": "%s is not an exact duplicate of %s (body-only)" % (x, src), "a": x, "b": src, "keys": BODY, "min_sep": 2})
    # the influencing source joins the span it is allowed to lean toward (Skarn is not one of the five W1 span sources); the five-source span is then REPORT
    xs = SRC[178] + ([src] if src not in SRC[178] else [])
    for k in CANON: spans.append({"code": "X", "check": "%s stays inside the 178 cm source span%s: %s" % (x, " + " + src if src not in SRC[178] else "", k), "a": x, "srcs": xs, "k": k})
    if src not in SRC[178]:
        for k in CANON: spans.append({"code": "X", "check": "%s vs the five-source W1 span only (report): %s" % (x, k), "a": x, "srcs": SRC[178], "k": k, "report": True})
# probe HVXAEc (REPORT): HVXAE bounded in reading space (neck 0.10, wrist kept at HVC1, upper leg 0.06)
for k in EXPR["HVXAE"][1]: toward.append({"code": "X", "check": "probe HVXAEc moves from HVC1 toward AE178 (report): %s" % k.replace(T0, ""), "a": "HVXAEc", "base": "HV178", "src": "AE178", "k": k, "report": True})
for k in CANON: spans.append({"code": "X", "check": "probe HVXAEc inside the 178 cm source span (report): %s" % k, "a": "HVXAEc", "srcs": SRC[178], "k": k, "report": True})
passing.append({"code": "X", "check": "probe HVXAEc is not an exact duplicate of AE178 (report)", "a": "HVXAEc", "b": "AE178", "keys": BODY, "report": True})
for x in ("W1HVH3", "W1HVE3"):
    for k in CANON: spans.append({"code": "X", "check": "accepted W1 panel %s inside the 178 cm source span: %s (report)" % (x, k), "a": x, "srcs": SRC[178], "k": k, "report": True})
# frames (§10): breadth-only writes at 152 / 178 / 213; lengths, neck, depth, joints unchanged; Broad / Narrow not ancestry
for c, n, b, tag in (("HV152", "HVN152", "HVB152", "152"), ("HV178", "HVN178", "HVB178", "178"), ("HV213", "HVN213", "HVB213", "213")):
    for k in (TB, SJ, BI, CR, HS):
        mv.append({"code": "F", "kind": "D", "sign": -1, "a": n, "b": c, "k": k, "check": "Narrow (%s) reduces %s by >= 1 %%" % (tag, k.replace(T0, ""))})
        mv.append({"code": "F", "kind": "D", "sign": 1, "a": b, "b": c, "k": k, "check": "Broad (%s) increases %s by >= 1 %%" % (tag, k.replace(T0, ""))})
    for x in (n, b):
        for k in ("stature (cm)", "torso_share", "leg_share", "arm_share", "forearm_over_arm", "shin_over_leg", "HH_share", "hand_share", "neck_share"):
            mv.append({"code": "F", "kind": "L", "tol": 0.005, "a": x, "b": c, "k": k, "check": "%s keeps lengths (0.5 %%): %s" % (x, k)})
        mv.append({"code": "F", "kind": "L", "tol": 0.01, "a": x, "b": c, "k": TD, "check": "%s keeps thoracic depth (breadth-only frame; 1 %%)" % x})
        for j in ("elbow", "wrist", "knee", "ankle"): mv.append({"code": "F", "kind": "L", "tol": 0.01, "a": x, "b": c, "k": JP(j), "check": "%s keeps joint scale: %s (1 %%)" % (x, JP(j))})
        mv.append({"code": "F", "kind": "L", "tol": 0.02, "a": x, "b": c, "k": BC, "check": "%s carries the hip joints with the crest (Broad pelvis x1.12): bitrochanteric / crest within 2 %%" % x, "report": True})
for x, s in (("HVB178", "SK183"), ("HVB213", "SK208"), ("HVB213", "SKB208")): passing.append({"code": "F", "check": "Broad Halvren %s is not a Skarn duplicate (%s)" % (x, s), "a": x, "b": s, "keys": BODY, "min_sep": 2})
for x in ("HVN178",):
    for s in ("FN178", "AE178", "VA178"): passing.append({"code": "F", "check": "Narrow Halvren is not an elf duplicate (%s)" % s, "a": x, "b": s, "keys": BODY, "min_sep": 2})
    for k in CANON: spans.append({"code": "F", "check": "Narrow Halvren 178 inside the source span: %s" % k, "a": x, "srcs": SRC[178], "k": k})
for x in ("HVB178",):
    for k in CANON: spans.append({"code": "F", "check": "Broad Halvren 178 inside the source span: %s" % k, "a": x, "srcs": SRC[178], "k": k})
# M: composition at 173 cm - invariance and the source-plausible rows at matched composition (Marchfolk 173, Sagekin 173, Fenn 173, Aelari 173, Vael 173 states)
for c in ("LOWMUS", "HIMUS", "HIFAT", "HIBOTH", "LOW", "MIN"):
    a = "HV173-" + c
    inv.append({"code": "M", "check": "%s: composition does not redefine proportions (torso, leg, arm, forearm, lower-leg, hand, neck within 1 %%)" % a, "a": a, "b": "HV173",
                "keys": ["torso_share", "leg_share", "arm_share", "forearm_over_arm", "shin_over_leg", "hand_share", "neck_share"]})
    for k in CANON[:7]: spans.append({"code": "M", "check": "%s inside the same-composition source span: %s" % (a, k), "a": a, "srcs": ["MF-" + c, "SG173-" + c, "FN173-" + c, "AE173-" + c, "VA173-" + c], "k": k})
# S: HV-36...43 / HV-08 / HV-09 stress bodies keep their skeleton's proportions; stress bodies inside the source span where matched
for x, b in (("HV36", "HVN178"), ("HV37", "HVN178"), ("HV38", "HVB178"), ("HV39", "HVB178"), ("HV40", "HVB178"), ("HV41", "HV213"), ("HV42", "HV152"), ("HV43", "HVXFN"), ("HV08", "HV178"), ("HV09", "HV178")):
    inv.append({"code": "S", "check": "%s: composition on %s does not redefine proportions (within 1 %%)" % (x, b), "a": x, "b": b,
                "keys": ["torso_share", "leg_share", "arm_share", "forearm_over_arm", "shin_over_leg", "hand_share", "neck_share"]})
# K: large-human guard at the upper envelope (report)
for a, s in (("HV190", "SK190"), ("HV203", "SK203"), ("HV213", "SK208"), ("HVB213", "SK208")):
    for k in (TB, TD, SJ, "torso_share", JP("knee"), JP("wrist")): r("K", "%s vs %s: %s" % (a, s, k.replace(T0, "")), a, "<", s, k, "Skarn guard (report)", True)
# D: route check at 152 / 163 (macro builds vs the native builds used)
for h in (152, 163):
    for k in ("femur_over_leg", "leg_share", "torso_share", "neck_share", "HH_share", JP("knee")): r("D", "route check HV%d: native vs macro build: %s" % (h, k), "HV%d" % h, ">", "HV%dM" % h, k, "W2F R2 (macro 0.19 / 0.34 < 0.40)", True)
json.dump({"rows": rows, "invariance": inv, "moves": mv, "spans": spans, "passing": passing, "toward": toward,
           "series": {"HV": ["HV152", "HV163", "HV173", "HV178", "HV181", "HV190", "HV203", "HV213"]}}, open(sys.argv[1], "w"), indent=1)
print(len(rows), "rows", len(inv), "invariance", len(mv), "moves", len(spans), "spans", len(passing), "passing")
