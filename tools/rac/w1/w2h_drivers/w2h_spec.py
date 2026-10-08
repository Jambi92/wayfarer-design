# RAC W2H (short-race family) comparison specification. Canon: specs/durrim/DURRIM_V1.md (DU-P2...P6, L156), specs/pipkin/PIPKIN_V1.md (PK-P3...P5,
# PIP-BODY-14...16), specs/cogling/COGLING_V1.md (COG-BODY-02...13, L1589), the accepted W1 rows (directional_checks.py, W1r cg_eval.py, W1t du_bnd.py),
# order reviews/chatgpt-rac-w2g-final-acceptance-w2h-short-race-order.md (§ = section). Only canon / order directions are scored; everything else REPORT.
# Comparisons: REAL matched height where adult ranges overlap (Pipkin-Durrim 122; Cogling-Pipkin 91 / 107; Durrim-Marchfolk-Sagekin 152);
# NORMALIZED (ratios to stature / segment, i.e. displayed height normalized; labelled) everywhere else, against Marchfolk 173 (MF-M-R) - never a
# biologically valid same-height Marchfolk adult. Usage: python3 w2h_spec.py OUT.json
import sys, json
rows, inv, mv, spans, passing, ranges = [], [], [], [], [], []
def r(code, chk, a, op, b, k, note="", report=False): rows.append({"code": code, "check": chk, "a": a, "op": op, "b": b, "k": k, "note": note, "report": report})
T0 = " [t=0.0]"
sk = lambda x: "skeletal %s%s" % (x, T0)
JP = lambda j: "%s breadth / adjacent segment (exact-plane section)" % j
JS = lambda j: "%s breadth / stature (exact-plane section)" % j
TB, TD, SJ, CR, PD, PV, HS, BC, WI, CT, PVT, PDT, PVC, SH = map(sk, ("thoracic breadth / stature", "thoracic depth / stature", "shoulder-joint breadth / stature",
    "crest breadth / stature", "AP pelvic depth / stature", "pelvic vertical / stature", "hip-joint spacing / stature", "bitrochanteric / crest", "waist interval / torso",
    "crest / thoracic breadth", "pelvic vertical / thoracic vertical", "pelvic AP / thoracic depth", "pelvic vertical / crest", "femoral shaft breadth / femur"))
S7B, S7D = "femoral S7 breadth / stature" + T0, "femoral S7 depth / stature" + T0
JOINTS = ("elbow", "wrist", "knee", "ankle")
BODY = ["torso_share", "leg_share", "arm_share", "upperarm_over_arm", "forearm_over_arm", "hand_over_arm", "femur_over_leg", "shin_over_leg", "neck_share", "hand_share",
        "finger_over_hand", "palm_breadth_over_hand", "foot_share", "thorax_breadth_share", "thorax_depth_share"] + [JS(j) for j in JOINTS] + [TB, TD, SJ, CR, PD, PV, HS, CT, PVT, PDT, WI, SH]
FAM = {"DU": ["DU122", "DU137", "DU152"], "PK": ["PK91", "PK107", "PK122"], "CG": ["CG76", "CG91", "CG107"]}
NAME = {"DU": "Durrim", "PK": "Pipkin", "CG": "Cogling"}
# ---------------- U: Cogling head height (menton-vertex) roughly 11-13 cm (COGLING L1589, W1-A1); head-share allometry (report)
for b in FAM["CG"] + ["CGN91", "CGB91", "COG12", "COG13"]: ranges.append({"code": "U", "check": "%s head height (menton-vertex) roughly 11-13 cm (CG L1589, W1-A1)" % b, "a": b, "k": "HH (cm)", "lo": 11.0, "hi": 13.0})
for race, fam in FAM.items():
    r("U", "%s head share: minimum > maximum stature (allometry; never enlargement)" % NAME[race], fam[0], ">", fam[2], "HH_share", "RAC-04 L44; order §10", True)
    for b in fam: r("U", "%s head share vs Marchfolk 173 (normalized)" % b, b, ">", "MF173", "HH_share", "PK L33 / DU L181 / CG L280 (allometry only)", True)
# ---------------- O: real-height overlaps (§4) and normalized Cogling-Durrim context
DU_PK = [("thorax_depth_share", ">"), ("thorax_breadth_share", ">"), (TD, ">"), (TB, ">"), ("torso_share", ">"), ("leg_share", "<"), ("arm_share", "<"), (CT, "<"),
         ("hand_share", ">"), ("palm breadth / stature", ">"), ("foot breadth / stature", ">"), ("neck_share", "<"), (SH, ">"), (S7B, ">")] + [(JS(j), ">") for j in JOINTS]
def pair(code, tag, a, b, dirs, note, rep=()):
    for k, op in dirs: r(code, "%s: %s %s %s: %s" % (tag, a, op, b, k.replace(T0, "")), a, op, b, k, note, k in rep)
pair("O", "122 cm Pipkin max / Durrim min (real height)", "DU122", "PK122", DU_PK, "SR-COMP-03; DURRIM L156; order §4A")
pair("O", "PIP-BODY-14 Narrow Durrim vs Broad Pipkin 122 cm (real height)", "DUN122", "PKB122", DU_PK, "PIP-BODY-14; order §4A",
     rep=("thorax_breadth_share", TB))   # W1t ruling: Broad PK vs Narrow DU accepted despite thoracic-breadth convergence
CG_PK = [(CT, "<"), (PVT, "<"), (PDT, "<"), (SH, "<"), (S7B, "<"), ("upperarm_over_arm", "<"), ("forearm_over_arm", ">"), ("hand_over_arm", ">"), ("femur_over_leg", "<")] + [(JS(j), "<") for j in JOINTS]
for h, a, b, tag in ((91, "CG91", "PK91", "COG-BODY-09: Cogling reference / Pipkin minimum 91 cm (real height)"), (107, "CG107", "PK107", "COG-BODY-09A: Cogling maximum / Pipkin reference 107 cm (real height)")):
    pair("O", tag, a, b, CG_PK, "COG-BODY-09 / 09A; CG L102, L258-262, L685-687 (less pelvis-led); SRR structural axis; order §4B (distal redistribution vs preserved limbs)")
DU_CG = [("thorax_depth_share", ">"), ("thorax_breadth_share", ">"), ("leg_share", "<"), ("arm_share", "<"), ("upperarm_over_arm", ">"), ("forearm_over_arm", "<"), ("finger_over_palm", "<"),
         ("palm_breadth_over_hand", ">"), ("foot breadth / stature", ">"), ("neck_share", "<"), (SH, ">")] + [(JS(j), ">") for j in JOINTS]
pair("O", "COG-BODY-10A actual height: Durrim min 122 vs Cogling max 107", "DU122", "CG107", DU_CG, "COG-BODY-10A; DURRIM L156 (stature differs: ratios = normalized readings)")
pair("O", "COG-BODY-10 NORMALIZED: Narrow Durrim 137 vs Broad high-muscle Cogling 91", "DUN137", "COG05", DU_CG, "COG-BODY-10; SR-COMP-10 (normalized displayed height; diagnostic)")
# ---------------- P: body-only collision / passing (complete package; isolated scalar overlap allowed). Failure = fewer than 3 of the body readings separate by >= 1 %
for a, b, note in (("DU122", "PK122", "real height"), ("DUN122", "PKB122", "real height (PIP-BODY-14)"), ("CG91", "PK91", "real height (COG-BODY-09)"), ("CG107", "PK107", "real height (COG-BODY-09A)"),
                   ("DU122", "CG107", "actual-height context (COG-BODY-10A)"), ("DUN137", "COG05", "normalized (COG-BODY-10)"), ("DU152", "MF152", "real height"), ("DU152", "SG152", "real height"),
                   ("PK107", "MF173", "normalized (PIP-BODY-16)"), ("CG91", "MF173", "normalized"), ("DU137", "MF173", "normalized"),
                   ("PK107-HIMUS", "DU137", "normalized: high-muscle Pipkin vs Durrim"), ("CG91-HIFAT", "PK91", "real height: high-fat Cogling vs Pipkin"), ("CG91-HIBOTH", "PK91", "real height: high muscle + fat Cogling vs Pipkin"),
                   ("COG05", "PKB107", "normalized: Broad high-muscle Cogling vs Broad Pipkin"), ("DUNLOW", "PKB122", "Narrow low Durrim 137 vs Broad Pipkin 122 (normalized)")):
    passing.append({"code": "P", "check": "%s vs %s (%s; body-only)" % (a, b, note), "a": a, "b": b, "keys": BODY, "min_sep": 3})
# ---------------- D: Durrim 152 cm equal-height boundary vs Marchfolk / Sagekin (DU-P2...P6, RM-SR-06; permanent; DURRIM L19, L72, L156)
DU_MF = [("torso_share", ">", "RM-SR-06"), ("thorax_depth_share", ">", "RM-SR-06"), (TD, ">", "RM-SR-06 skeletal"), ("thorax_breadth_share", ">", ""), (TB, ">", ""), ("leg_share", "<", ""),
         ("arm_share", "<", ""), (SJ, ">", ""), ("hand_share", ">", ""), ("palm breadth / stature", ">", ""), ("foot breadth / stature", ">", ""), ("neck_share", "<", ""),
         ("hip-joint height / stature", "<", "DU-P2a"), (HS, ">", "DU-P2b"), (PVC, "<", "DU-P3"), (CR, ">", "DU-P5"), (CT, "<=", "DU-P6 thorax-led"), (SH, ">", "long bones")] + \
        [(JS(j), ">", "substantial joints") for j in JOINTS]
for o in ("MF152", "SG152"):
    for k, op, note in DU_MF: r("D", "152 cm: Durrim %s %s: %s" % (op, o, k.replace(T0, "")), "DU152", op, o, k, "DURRIM L19, L72, L156 %s" % note)
for k in ("HH_share",): r("D", "152 cm: Durrim head share vs MF152 (scope)", "DU152", ">", "MF152", k, "DU L181; order §10", True)
# ---------------- P4: DU-P4 (skeletal AP pelvic depth / stature > equal-height Marchfolk, continuous with the deep thorax), §6
r("P4", "DU-P4: skeletal AP pelvic depth / stature, Durrim 152 > Marchfolk 152", "DU152", ">", "MF152", PD, "DURRIM DU-P4 (PV-D8); order §6")
r("P4", "DU-P4 method cross-check: Durrim 152 vs Marchfolk 152 on the W1t S7-normalized grid (report)", "DU152", ">", "MF152s7n", PD, "W1 carried +0.8 %", True)
r("P4", "DU-P4 context: Durrim 152 vs Sagekin 152 (three-population context)", "DU152", ">", "SG152", PD, "order §6", True)
r("P4", "DU-P4 continuity with the deep thorax: pelvic AP / thoracic depth, Durrim 152 vs Marchfolk 152", "DU152", ">", "MF152", PDT, "DU-P4 'continuous with the deep thorax'", True)
for c in ("", "-LOW", "-MIN", "-HIBOTH"):
    r("P4", "DU-P4 skin (composition-inclusive diagnostic): AP pelvic depth / stature, DU152%s vs MF152%s" % (c, c), "DU152" + c, ">", "MF152" + c, "pelvic_depth_share", "PV-D16 / PV-D20: skin is a diagnostic only", True)
for x in ("DUN152", "DUB152"): r("P4", "DU-P4 frame invariance: %s skeletal AP pelvic depth vs Marchfolk 152" % x, x, ">", "MF152", PD, "frame is breadth-only", True)
for x, f in (("DU152P4", "x1.04"), ("DU152P6", "x1.06")):     # diagnostic probes, NOT applied
    for k in (PD, PDT, TD, CR, PV, HS, PVC, "pelvic_depth_share", "torso_share", "leg_share", "hip-joint height / stature"):
        r("P4", "probe %s (pelvis bone Z %s, NOT applied) vs Marchfolk 152: %s" % (x, f, k.replace(T0, "")), x, ">", "MF152", k, "diagnostic probe for the author decision", True)
    r("P4", "probe %s vs DU152: AP pelvic depth gain" % x, x, ">", "DU152", PD, "diagnostic probe", True)
for b in ("DU122", "DU137"): r("P4", "DU-P4 normalized context: %s vs Marchfolk 173" % b, b, ">", "MF173", PD, "normalized (no equal-height MF)", True)
# ---------------- R: RM-SR-01 Pipkin central trunk / pelvis vs Marchfolk 173 (NORMALIZED), family and frames (§7)
for b in FAM["PK"] + ["PKN91", "PKB91", "PKN107", "PKB107", "PKN122", "PKB122"]:
    r("R", "%s central trunk share < MF (modest; normalized)" % b, b, "<", "MF173", "torso_share", "RAC-04 L72 (T-2); PIPKIN L137-139")
    r("R", "%s pelvic vertical / stature >= MF (direction; normalized)" % b, b, ">=", "MF173", PV, "PK-P3 (PV-D10; 1 % marginal)")
    r("R", "%s pelvic vertical / thoracic vertical > MF (normalized)" % b, b, ">", "MF173", PVT, "PK-P3")
    r("R", "%s crest / thoracic breadth > MF: pelvis structurally important (normalized)" % b, b, ">", "MF173", CT, "PK-P5; RAC-03 L35")
    r("R", "%s pelvic AP / thoracic depth > MF (normalized)" % b, b, ">", "MF173", PDT, "PK-P4")
    r("R", "%s waist interval / torso < MF: compact lower trunk (normalized)" % b, b, "<", "MF173", WI, "PV-D15")
    r("R", "%s leg share <= MF (legs never automatically exceed human; normalized)" % b, b, "<=", "MF173", "leg_share", "RAC-04 L72; PK-P2a")
    for k in ("thoracic vertical / stature", PV, "torso_share"): r("R", "%s trunk split vs MF (report): %s" % (b, k.replace(T0, "")), b, "vs", "MF173", k, "RM-SR-01 magnitude (diagnostic)", True)
# ---------------- Q: RM-SR-02 Cogling segment distribution vs Marchfolk 173 (NORMALIZED), family, frames, COG-BODY-12 / 13 (§8)
for b in FAM["CG"] + ["CGN76", "CGB76", "CGN91", "CGB91", "CGN107", "CGB107", "COG12", "COG13"]:
    for k, op in (("upperarm_over_arm", "<"), ("forearm_over_arm", ">"), ("hand_over_arm", ">"), ("finger_over_hand", ">"), ("femur_over_leg", "<"), ("hand_share", ">")):
        r("Q", "%s %s %s MF (normalized)" % (b, k, op), b, op, "MF173", k, "CG L571-575, L619-622, L163-167")
    for k in ("torso_share", "arm_share", "leg_share"): r("Q", "%s %s ~ MF (near-human total; normalized; +/-0.010)" % (b, k), b, "~", "MF173", k, "CG L558")
    r("Q", "%s arm to wrist (without hand) / stature ~ MF (report: separates fingertip reach from total limb)" % b, b, "~", "MF173", "arm to wrist / stature", "CG L558 / L571-575", True)
    r("Q", "%s foot share ~ MF (report)" % b, b, "~", "MF173", "foot_share", "CG L217-232", True)
    r("Q", "%s shin / leg vs MF (report)" % b, b, ">", "MF173", "shin_over_leg", "within-limb distal", True)
    r("Q", "%s not a miniature Fenn: arm share < Fenn (normalized)" % b, b, "<", "FN181", "arm_share", "CG L935-951")
    r("Q", "%s not a miniature Grask: arm share < Grask (normalized)" % b, b, "<", "GR218", "arm_share", "CG L953-969")
    r("Q", "%s not a miniature Grask: leg share < Grask (normalized)" % b, b, "<", "GR218", "leg_share", "CG L953-969")
# ---------------- A: RM-SR-03 structural-mass axis Cogling < Pipkin < Durrim, by region (§9)
REG = [(JS(j), j + " (exact plane, per stature)") for j in JOINTS] + [(SH, "femoral shaft breadth / femur"), (S7B, "femoral S7 breadth / stature"), (S7D, "femoral S7 depth / stature")]
AXP = [("CG76", "PK91", "minimum statures (normalized)"), ("PK91", "DU122", "minimum statures (normalized)"), ("CG107", "PK122", "maximum statures (normalized)"), ("PK122", "DU152", "maximum statures (normalized)"),
       ("CG91", "PK107", "references (normalized)"), ("PK107", "DU137", "references (normalized)"), ("CG91", "PK91", "real height 91"), ("CG107", "PK107", "real height 107"),
                  ("PK122", "DU122", "real height 122"), ("CGB91", "PKN107", "frame stress: Broad Cogling vs Narrow Pipkin (normalized)"), ("PKB122", "DUN122", "frame stress PIP-BODY-14 (real height)"),
                  ("COG05", "DUN137", "frame + composition stress COG-BODY-10 (normalized)")] + \
                 [("CG91-%s" % c, "PK107-%s" % c, "same composition %s (normalized)" % c) for c in ("LOWMUS", "HIMUS", "HIFAT", "HIBOTH", "LOW", "MIN")] + \
                 [("PK107-%s" % c, "DU137-%s" % c, "same composition %s (normalized)" % c) for c in ("LOWMUS", "HIMUS", "HIFAT", "HIBOTH", "LOW", "MIN")] + \
                 [("CG91-HIMUS", "PK107-LOWMUS", "OPPOSED composition: high-muscle Cogling vs low-muscle Pipkin (normalized; soft-tissue stress, report)"),
                  ("PK107-HIMUS", "DU137-LOWMUS", "OPPOSED composition: high-muscle Pipkin vs low-muscle Durrim (normalized; soft-tissue stress, report)"),
                  ("CG91-HIBOTH", "PK107-MIN", "OPPOSED composition extreme (normalized; soft-tissue stress, report)"), ("PK107-HIBOTH", "DU137-MIN", "OPPOSED composition extreme (normalized; soft-tissue stress, report)")]
for a, b, ctx in AXP:
    for k, nm in REG:
        if (k in (SH, S7B, S7D)) and ("-" in a or "-" in b): continue      # skeletal proxy is composition-free: same as the skeleton rows
        r("A", "axis %s < %s [%s]: %s" % (a, b, ctx, nm), a, "<", b, k, "SRR L41-48; RAC-05 L32-34; RM-SR-03", "OPPOSED" in ctx)
    for j in JOINTS: r("A", "axis %s vs %s [%s]: %s per adjacent segment (report; confounded by Cogling redistribution)" % (a, b, ctx, j), a, "<", b, JP(j), "method comparison", True)
# ---------------- F: frames (§12) breadth-only; identity survives
for race, fam in FAM.items():
    for c in fam:
        n, b = race + "N" + c[2:], race + "B" + c[2:]
        base = {"DU137": "DU137", "PK107": "PK107", "CG91": "CG91"}.get(c, c)
        for k in (TB, SJ, CR, HS):
            mv.append({"code": "F", "kind": "D", "sign": -1, "a": n, "b": base, "k": k, "check": "Narrow %s reduces %s by >= 1 %%" % (c, k.replace(T0, ""))})
            mv.append({"code": "F", "kind": "D", "sign": 1, "a": b, "b": base, "k": k, "check": "Broad %s increases %s by >= 1 %%" % (c, k.replace(T0, ""))})
        for x in (n, b):
            for k in ("stature (cm)", "torso_share", "leg_share", "arm_share", "upperarm_over_arm", "forearm_over_arm", "femur_over_leg", "shin_over_leg", "HH_share", "hand_share", "neck_share"):
                mv.append({"code": "F", "kind": "L", "tol": 0.005, "a": x, "b": base, "k": k, "check": "%s keeps lengths (0.5 %%): %s" % (x, k)})
            for k in (TD, S7D):
                mv.append({"code": "F", "kind": "L", "tol": 0.01, "a": x, "b": base, "k": k, "check": "%s keeps %s (breadth-only frame; 1 %%)" % (x, k.replace(T0, ""))})
            # femoral shaft / S7 BREADTH is read on a horizontal section: a wider / narrower hip-joint spacing changes femoral obliquity and so the frontal
            # section breadth (S7 depth is unchanged) - geometry of the measurement plane, not shaft robusticity: report
            for k in (SH, S7B):
                mv.append({"code": "F", "kind": "L", "tol": 0.01, "a": x, "b": base, "k": k, "report": True, "check": "%s %s (report: horizontal-section breadth follows femoral obliquity)" % (x, k.replace(T0, ""))})
            for j in JOINTS: mv.append({"code": "F", "kind": "L", "tol": 0.01, "a": x, "b": base, "k": JP(j), "check": "%s keeps joint scale: %s (1 %%)" % (x, j)})
    # identity survival under frame (normalized vs MF173)
for c in FAM["DU"]:
    for x in ("DUN" + c[2:],):
        r("F", "%s Narrow keeps a Durrim minimum: crest / stature > MF (normalized)" % x, x, ">", "MF173", CR, "DU-P5 (Narrow keeps a Durrim minimum)")
        r("F", "%s Narrow stays broad-thoraxed: thoracic breadth / stature > MF (normalized)" % x, x, ">", "MF173", TB, "DU L11-40")
        r("F", "%s Narrow stays deep: thoracic depth / stature > MF (normalized)" % x, x, ">", "MF173", TD, "DU L11-40")
    r("F", "DUB%s Broad stays thorax-led: crest / thoracic breadth <= MF (normalized)" % c[2:], "DUB" + c[2:], "<=", "MF173", CT, "DU-P6; W1t frame rule (Broad pelvis x1.08)")
for c in FAM["CG"]:     # frame-matched (normalized) narrow-to-moderate thorax: Cogling frame vs the accepted Marchfolk frame of the same kind
    r("F", "CGN%s narrow-to-moderate thorax: thoracic breadth / stature < Narrow Marchfolk (frame-matched, normalized)" % c[2:], "CGN" + c[2:], "<", "MFN173", "thorax_breadth_share", "CG L98, L102")
    r("F", "CGB%s narrow-to-moderate thorax: thoracic breadth / stature < Broad Marchfolk (frame-matched, normalized)" % c[2:], "CGB" + c[2:], "<", "MFB173", "thorax_breadth_share", "CG L98, L102")
for c in FAM["DU"]:
    r("F", "DUN%s keeps DU-P2b against Narrow Marchfolk: skeletal hip-joint spacing / stature > MFN173 (frame-matched, normalized)" % c[2:], "DUN" + c[2:], ">", "MFN173", HS, "DU-P2b; DU-P5")
    r("F", "DUN%s keeps DU-P5 against Narrow Marchfolk: skeletal crest / stature > MFN173 (frame-matched, normalized)" % c[2:], "DUN" + c[2:], ">", "MFN173", CR, "DU-P5")
for c in FAM["PK"]:
    r("F", "PKB%s Broad Pipkin lighter than reference Durrim: knee / stature < DU137 (normalized)" % c[2:], "PKB" + c[2:], "<", "DU137", JS("knee"), "order §12 Pipkin")
    r("F", "PKB%s Broad Pipkin lighter than reference Durrim: femoral shaft / femur < DU137 (normalized)" % c[2:], "PKB" + c[2:], "<", "DU137", SH, "order §12 Pipkin")
for c in FAM["CG"]:
    r("F", "CGB%s Broad Cogling fine-scale vs Durrim: knee / stature < DU137 (normalized)" % c[2:], "CGB" + c[2:], "<", "DU137", JS("knee"), "order §12 Cogling")
    r("F", "CGB%s Broad Cogling keeps narrow core: crest / thoracic breadth < PK107 (normalized)" % c[2:], "CGB" + c[2:], "<", "PK107", CT, "CG L102 (less pelvis-led)")
# ---------------- M: composition firewall (§13) - invariance + matched-composition normalized identity rows vs Marchfolk 173 in the same state
KEYS = ["torso_share", "leg_share", "arm_share", "upperarm_over_arm", "forearm_over_arm", "femur_over_leg", "shin_over_leg", "hand_share", "finger_over_hand", "neck_share"]
for race, ref in (("DU", "DU137"), ("PK", "PK107"), ("CG", "CG91")):
    for c in ("LOWMUS", "HIMUS", "HIFAT", "HIBOTH", "LOW", "MIN"):
        a = "%s-%s" % (ref, c)
        inv.append({"code": "M", "check": "%s: composition does not redefine proportions (shares within 1 %%)" % a, "a": a, "b": ref, "keys": KEYS})
        m = "MF173-" + c
        if race == "DU":
            for k, op in [("thorax_depth_share", ">"), ("thorax_breadth_share", ">"), ("torso_share", ">"), ("leg_share", "<"), ("arm_share", "<"), ("neck_share", "<")] + [(JS(j), ">") for j in JOINTS]:
                r("M", "%s vs Marchfolk 173 same composition (normalized): %s %s" % (a, k, op), a, op, m, k, "DU L11-40; L52 (low-muscle low-fat structural visibility)")
        if race == "PK":
            for k, op in [("torso_share", "<"), ("leg_share", "<="), ("pelvis_over_thorax_breadth", ">")]:
                r("M", "%s vs Marchfolk 173 same composition (normalized): %s %s" % (a, k, op), a, op, m, k, "PK-P5 (skin, composition-inclusive); RAC-04 L72")
        if race == "CG":
            for k, op in [("upperarm_over_arm", "<"), ("forearm_over_arm", ">"), ("hand_over_arm", ">"), ("finger_over_hand", ">"), ("femur_over_leg", "<"), ("thorax_breadth_share", "<")] + [(JS(j), "<") for j in JOINTS]:
                r("M", "%s vs Marchfolk 173 same composition (normalized): %s %s" % (a, k, op), a, op, m, k, "CG L571-575, L619-622")
for x, b in (("COG04", "CGN91"), ("COG05", "CGB91"), ("PKBHM", "PKB107"), ("DUNLOW", "DUN137")):
    inv.append({"code": "M", "check": "%s: composition on %s does not redefine proportions (within 1 %%)" % (x, b), "a": x, "b": b, "keys": KEYS})
# ---------------- K: RM-SR-04 adult read vs generator human-child proxies (diagnostic only; report) + minimum-height head scope
CH = ["HH_share", "FVB", "FVI", "ORB height / HH", "aperture height / orbit height", "IOD", "hand_share", "finger_over_palm", "foot_share", "torso_share", "leg_share", "arm_share",
      "forearm_over_arm", "shin_over_leg", "waist_interval_over_torso", "pelvis_over_thorax_breadth", "thorax_depth_share", "neck_share"]
for a, c, note in (("CG76", "CHILD1", "COG-BODY-11 (toddler ~1.5 y, 76 cm)"), ("CG91", "CHILD3", "SR-COMP-11 (~3 y, 91 cm)"), ("PK91", "CHILD3", "PIP-BODY-15 minimum (~3 y, 91 cm)"),
                   ("PK107", "CHILD6", "PIP-BODY-15 (~6 y, 107 cm)"), ("DU137", "CHILD9", "Durrim scope (~9 y, 137 cm)")):
    for k in CH: r("K", "adult %s vs child proxy %s: %s" % (a, c, k), a, "vs", c, k, note + "; generator child proxy (diagnostic only)", True)
    passing.append({"code": "K", "check": "%s is not a child duplicate: %s (body-only)" % (a, note), "a": a, "b": c, "keys": BODY, "min_sep": 3})
# ---------------- S5: RM-SR-05 Durrim craniofacial depth proxies at 152 cm (report; domains A-C have no implemented landmarks)
for k in ("FDH", "CBH", "MPI", "MdPI", "FVI", "FPI"):
    for o in ("MF152", "SG152"): r("S5", "RM-SR-05 proxy %s: Durrim 152 vs %s" % (k, o), "DU152", "vs", o, k, "DURRIM depth domains (D: MPI, E: MdPI proxies); FDH / CBH", True)
# ---------------- Z: route reproduction (the family route re-builds the accepted reference)
for a, b in (("DU137R", "DU137"), ("PK107R", "PK107"), ("CG91R", "CG91")):
    inv.append({"code": "Z", "check": "route reproduction: %s re-built on the family route equals the accepted %s (within 0.1 %%)" % (a, b), "a": a, "b": b, "keys": KEYS + ["HH_share", "thorax_breadth_share", "thorax_depth_share"], "tol": 0.001})
json.dump({"rows": rows, "invariance": inv, "moves": mv, "spans": spans, "passing": passing, "ranges": ranges,
           "series": {"DU": FAM["DU"], "PK": FAM["PK"], "CG": FAM["CG"]}}, open(sys.argv[1], "w"), indent=1)
print(len(rows), "rows", len(inv), "invariance", len(mv), "moves", len(passing), "passing", len(ranges), "ranges")
