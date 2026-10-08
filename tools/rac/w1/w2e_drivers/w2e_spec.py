# RAC W2E (Sagekin W2) comparison-row specification (canon sources in each 'note'; SG = specs/sagekin/SAGEKIN_V1.md line).
# Sagekin tendencies are POPULATION tendencies (order §7): a matched-height row that misses is reported per AD-G10, never a body failure by itself.
# Usage: python3 w2e_spec.py OUT.json
import sys, json
rows, inv, mv = [], [], []
def r(code, chk, a, op, b, k, note="", report=False): rows.append({"code": code, "check": chk, "a": a, "op": op, "b": b, "k": k, "note": note, "report": report})
T0 = " [t=0.0]"
sk = lambda x: "skeletal %s%s" % (x, T0)
TB, TD, DB, SJ, BI, CR, PD, PV, HS, BC = map(sk, ("thoracic breadth / stature", "thoracic depth / stature", "thoracic depth / breadth", "shoulder-joint breadth / stature", "biacromial / stature",
                                               "crest breadth / stature", "AP pelvic depth / stature", "pelvic vertical / stature", "hip-joint spacing / stature", "bitrochanteric / crest"))
PELV = [CR, PD, PV, HS, BC, sk("crest / thoracic breadth"), sk("pelvic AP / thoracic depth"), sk("waist interval / torso"), sk("pelvic vertical / thoracic vertical")]
JT = ["%s breadth / stature (exact-plane section)" % j for j in ("elbow", "wrist", "knee", "ankle")]
JSG = ["%s breadth / adjacent segment (exact-plane section)" % j for j in ("elbow", "wrist", "knee", "ankle")]
OT = [("torso_share", "<", "SG L137–141, L155 (slightly lower torso share)"), ("leg_share", ">", "SG L137–141 (slightly greater leg share)"),
      ("forearm_over_arm", ">", "SG L138 (forearm trends longer)"), ("hand_share", ">", "SG L155–157 (hands trend longer)"), ("finger_over_hand", ">", "SG L155–157 (fingers trend longer)"),
      ("palm_breadth_over_hand", "<", "SG L155–157 (hands may trend slightly narrower)"), ("thorax_depth_share", "<", "SG L89, L141 (reduced ribcage depth; skin reading)")]
def ot(code, sg_, mf, tag, report=False, skel=True):
    for k, op, src in OT: r(code, "%s: Sagekin %s Marchfolk: %s" % (tag, op, k), sg_, op, mf, k, src, report)
    if skel: r(code, "%s: Sagekin < Marchfolk: skeletal thoracic depth / stature" % tag, sg_, "<", mf, TD, "SG L89, L141; RAC-03 (reduced ribcage depth, skeletal)", report)
    for k, note in (("arm_share", "no arm-share direction authored"), ("span_der", "no span direction authored"), ("thorax_breadth_share", "v1.1 §1: reduced depth, not an undefined breadth reduction")):
        r(code, "%s: Sagekin vs Marchfolk: %s" % (tag, k), sg_, ">", mf, k, note, True)
    if skel: r(code, "%s: Sagekin vs Marchfolk: skeletal thoracic breadth / stature" % tag, sg_, "<", mf, TB, "breadth not authored (v1.1 §1)", True)
# U: allometry
r("U", "head share allometric: 152 > 178", "SG152", ">", "SG178", "HH_share", "RM-UB-02"); r("U", "head share allometric: 208 < 178", "SG208", "<", "SG178", "HH_share", "RM-UB-02")
for k in ("hand_share", "foot_share", "neck_share"):
    r("U", "%s: 152 vs 178" % k, "SG152", ">", "SG178", k, "RM-UB-02 diagnostic", True); r("U", "%s: 208 vs 178" % k, "SG208", "<", "SG178", k, "RM-UB-02 diagnostic", True)
# O: RM-OT-01 at matched height (real Marchfolk overlap 152-203)
for h in ("152", "163", "173", "178", "190", "203"): ot("O", "SG" + h, "MF" + h, "%s cm" % h)
ot("O", "SG208", "MF203", "Sagekin 208 vs the tallest accepted Marchfolk (203; no Marchfolk at 208)", report=True)
ot("O", "SG163N", "MF163N", "163 cm native-route cross-check (both populations on the native route)", report=True, skel=False)
# P: pelvis / axial (RM-UB-06; pelvic shape OPEN: report only; obstetric firewall - external skeletal landmarks only)
for h in ("152", "173", "178", "203"):
    for k in PELV: r("P", "%s cm: Sagekin vs Marchfolk: %s" % (h, k.replace(T0, "")), "SG" + h, ">", "MF" + h, k, "RM-UB-06 diagnostic; Sagekin pelvic shape OPEN (SG L155; RAC-03)", True)
# K: Skarn guard (canon silent on Sagekin vs Skarn directions: REPORT)
for g, s in (("SG190", "SK190"), ("SG203", "SK203"), ("SG208", "SK208"), ("SGB208", "SKB208"), ("SGB208", "SK208")):
    for k in (TB, TD, SJ, CR, "torso_share", "thorax_breadth_share", "thorax_depth_share") + tuple(JSG):
        r("K", "%s vs %s: %s" % (g, s, k.replace(T0, "")), g, "<", s, k, "Skarn guard (order §9): report; SK L291 large-scale powerful human organization", True)
# E: PROVISIONAL anti-elf sanity (accepted W1 Fenn / Aelari; SG L147, L435, L465; FN L151; AE L183); not final elf boundaries. A row is scored only
# where the W1 elf is beyond matched-height Marchfolk (181 / 190) by >= 1 % on that reading (the 'gate'); single readings may overlap (SG L465).
EF = [("leg_share", "<"), ("arm_share", "<"), ("span_der", "<"), ("shin_over_leg", "<"), ("forearm_over_arm", "<"), ("finger_over_hand", "<"), ("hand_share", "<"), ("foot_share", "<"),
      ("thorax_depth_share", ">"), ("thorax_breadth_share", ">"), ("elbow breadth / adjacent segment (exact-plane section)", ">"), ("wrist breadth / adjacent segment (exact-plane section)", ">"),
      ("knee breadth / adjacent segment (exact-plane section)", ">"), ("ankle breadth / adjacent segment (exact-plane section)", ">")]
def elf(g, tag, e, mf, h, report=False):
    for k, op in EF: rows.append({"code": "E", "check": "PROVISIONAL: %s %s %s W1 (%s): %s" % (tag, op, {"FN181": "Fenn", "AE190": "Aelari"}[e], h, k), "a": g, "op": op, "b": e, "k": k,
                                  "note": "never elven in limb proportion / light bones (SG L147, L435, L465; FN L151; AE L183); W1 elf only", "report": report, "gate": [e, mf]})
for g, tag in (("SG181", "Sagekin 181 (matched)"), ("SG178", "Sagekin reference 178"), ("SG04", "SG-04 long-limbed 178"), ("SGN178", "Narrow Sagekin 178")): elf(g, tag, "FN181", "MF181", "181")
elf("SG190", "Sagekin 190 (matched)", "AE190", "MF190", "190")
elf("SG04x200", "SG-04 probe x2.0 (178)", "FN181", "MF181", "181", report=True)
for g, tag in (("SG04", "SG-04 long-limbed 178 (cross-height)"), ("SGN208", "Narrow Sagekin 208 (cross-height)")): elf(g, tag, "AE190", "MF190", "190", report=True)
# F: frames (accepted human W2A1 frame writes): domain moves, lengths kept, at 178 and at both boundaries
for c, n, b, tag in (("SG178", "SGN178", "SGB178", "reference 178"), ("SG152", "SGN152", "SGB152", "152 cm"), ("SG208", "SGN208", "SGB208", "208 cm")):
    for k in (TB, SJ, BI, CR, HS):
        mv.append({"code": "F", "kind": "D", "sign": -1, "a": n, "b": c, "k": k, "check": "Narrow (%s) reduces %s by >= 1 %%" % (tag, k.replace(T0, ""))})
        mv.append({"code": "F", "kind": "D", "sign": 1, "a": b, "b": c, "k": k, "check": "Broad (%s) increases %s by >= 1 %%" % (tag, k.replace(T0, ""))})
    for k in ("stature (cm)", "torso_share", "leg_share", "arm_share", "forearm_over_arm", "shin_over_leg", "HH_share", "hand_share", "finger_over_hand"):
        for x in (n, b): mv.append({"code": "F", "kind": "L", "tol": 0.005, "a": x, "b": c, "k": k, "check": "%s keeps lengths (0.5 %%): %s" % (x, k)})
    for x in (n, b):
        for k in [TD] + JSG: mv.append({"code": "F", "kind": "L", "tol": 0.01, "a": x, "b": c, "k": k, "report": True, "check": "%s vs Balanced: %s (frame write includes depth x0.975 / x1.025 and long-bone cross-section)" % (x, k.replace(T0, ""))})
ot("F", "SGB178", "MFB173", "Broad Sagekin 178 vs Broad Marchfolk 173 (Broad may resemble Marchfolk)", report=True)
ot("F", "SGN178", "MFN173", "Narrow Sagekin 178 vs Narrow Marchfolk 173", report=True)
for x, m in (("SGB178", "MFB173"), ("SGN178", "MFN173"), ("SG178", "MF173")):
    for k in (sk("crest / thoracic breadth"), sk("thoracic depth / breadth")):
        r("F", "human alignment: %s vs %s: %s" % (x, m, k.replace(T0, "")), x, ">", m, k, "frame keeps human shoulder / thorax / pelvis relationships (order §10)", True)
# M: composition
for c in ("LOWMUS", "HIMUS", "HIFAT", "HIBOTH", "LOW", "MIN"):
    inv.append({"code": "M", "check": "SG173-%s: composition does not redefine proportions (torso, leg, arm, forearm, lower-leg, hand, finger within 1 %%)" % c, "a": "SG173-" + c, "b": "SG173",
                "keys": ["torso_share", "leg_share", "arm_share", "forearm_over_arm", "shin_over_leg", "hand_share", "finger_over_hand"]})
    for k, op, src in OT[:5]: r("M", "same composition %s at 173 cm: Sagekin %s Marchfolk: %s" % (c, op, k), "SG173-" + c, op, "MF-" + c, k, src + "; composition-matched")
    r("M", "same composition %s at 173 cm: Sagekin < Marchfolk: skin thoracic depth / stature" % c, "SG173-" + c, "<", "MF-" + c, "thorax_depth_share", "SG L89; composition-matched")
for x, src in (("SG06", "SGB178"), ("SG07", "SGB178"), ("SG08", "SGN178")):
    inv.append({"code": "M", "check": "%s: composition on the %s frame does not redefine proportions (within 1 %%)" % (x, src), "a": x, "b": src,
                "keys": ["torso_share", "leg_share", "arm_share", "forearm_over_arm", "shin_over_leg", "hand_share", "finger_over_hand"]})
# X: named validators SG-04 / -09 / -10
ot("X", "SG04", "MF178", "SG-04 long-limbed near the boundary (178)")
for k in ("leg_share", "forearm_over_arm", "finger_over_hand", "hand_share"): r("X", "SG-04 > Sagekin reference: %s (moves toward the boundary)" % k, "SG04", ">", "SG178", k, "SG L189")
r("X", "SG-09 long torso > Sagekin reference: torso share", "SG09", ">", "SG178", "torso_share", "SG L155 (longer-torso Sagekin valid)")
ot("X", "SG09", "MF178", "SG-09 long torso vs Marchfolk 178 (valid even where it reaches Marchfolk; RAC-03)", report=True)
ot("X", "SG10", "MF178", "SG-10 Marchfolk-overlap edge (178)", report=True)
inv.append({"code": "X", "check": "SG-10 within 2 % of Marchfolk 178 on torso, leg, arm, forearm, lower-leg (ambiguity accepted, SG L195)", "a": "SG10", "b": "MF178",
            "keys": ["torso_share", "leg_share", "arm_share", "forearm_over_arm", "shin_over_leg"], "tol": 0.02, "report": True})
# J: joints / long bone (RM-UB-03; canon silent vs Marchfolk -> REPORT)
for h in ("152", "173", "178", "203"):
    for k in JT + JSG + [sk("femoral shaft breadth / femur"), "femoral S7 breadth / stature" + T0]:
        r("J", "%s cm: Sagekin vs Marchfolk: %s" % (h, k.replace(T0, "")), "SG" + h, ">", "MF" + h, k, "RM-UB-03 diagnostic; no Sagekin joint / robusticity direction authored (order §13)", True)
# D: the 152 cm Durrim-Marchfolk-Sagekin dependency (RAC-04): report only; DU-P4 stays with Durrim W2
for k in ("torso_share", "leg_share", "neck_share", "hand_share", "thorax_breadth_share", TB, SJ, CR, PD, "knee breadth / adjacent segment (exact-plane section)", "wrist breadth / adjacent segment (exact-plane section)"):
    r("D", "152 cm: Durrim vs Sagekin: %s" % k.replace(T0, ""), "DU152", ">", "SG152", k, "RAC-04 152 cm three-way comparison; report", True)
    r("D", "152 cm: Durrim vs Marchfolk: %s" % k.replace(T0, ""), "DU152", ">", "MF152", k, "RAC-04; DU-P4 carried to Durrim W2", True)
for k in ("torso_share", "leg_share", "arm_share", "forearm_over_arm", "hand_share", "thorax_depth_share", "HH_share"):
    r("D", "route cross-check: Sagekin 152 from base macro 0.537 (W2E) vs from 0.5 (W1t proxy): %s" % k, "SG152", ">", "SG152-W1T", k, "W2A base_height_macro rule", True)
for k in ("femur_over_leg", "leg_share", "torso_share", "hand_share", "thorax_depth_share"):
    r("D", "route seam at 163 cm: macro vs native route (Sagekin): %s" % k, "SG163", ">", "SG163N", k, "generator short-stature femur behaviour reaches 163 cm", True)
    r("D", "route seam at 163 cm: macro vs native route (Marchfolk): %s" % k, "MF163", ">", "MF163N", k, "same effect in Marchfolk", True)
json.dump({"rows": rows, "invariance": inv, "moves": mv, "series": ["SG152", "SG163", "SG173", "SG178", "SG190", "SG203", "SG208"]}, open(sys.argv[1], "w"), indent=1)
print(len(rows), "rows", len(inv), "invariance", len(mv), "moves")
