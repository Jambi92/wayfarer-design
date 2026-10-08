# RAC W2F (Elf family W2) comparison-row specification. Canon sources in each 'note' (FN = FENN_V1, AE = AELARI_V1, VA = VAEL_V1 line; PV-D / E-A
# = accepted RAC pelvic / elf rules as encoded in the accepted W1 check code). Only directions the canon states are scored; the rest are REPORT.
# Usage: python3 w2f_spec.py OUT.json
import sys, json
rows, inv, mv = [], [], []
def r(code, chk, a, op, b, k, note="", report=False, gate=None):
    d = {"code": code, "check": chk, "a": a, "op": op, "b": b, "k": k, "note": note, "report": report}
    if gate: d["gate"] = gate
    rows.append(d)
T0 = " [t=0.0]"
sk = lambda x: "skeletal %s%s" % (x, T0)
TB, TD, DB, SJ, BI, CR, PD, PV, HS, BC, WI = map(sk, ("thoracic breadth / stature", "thoracic depth / stature", "thoracic depth / breadth", "shoulder-joint breadth / stature",
                                                   "biacromial / stature", "crest breadth / stature", "AP pelvic depth / stature", "pelvic vertical / stature", "hip-joint spacing / stature",
                                                   "bitrochanteric / crest", "waist interval / torso"))
PVC = sk("pelvic vertical / thoracic vertical")
JP = lambda j: "%s breadth / adjacent segment (exact-plane section)" % j
JS = lambda j: "%s breadth / stature (exact-plane section)" % j
REF = {"FN": "FN181", "AE": "AE190", "VA": "VA178"}
# canonical direction of each population against humans (vs Marchfolk), as authored (directional_checks / w1e_checks sources)
HUM = {"FN": [("torso_share", "<", "FN L32–52"), ("thorax_depth_share", "<", "FN L32–52"), ("thorax_breadth_share", "<", "FN L32–52"), ("arm_share", ">", "FN L32–52"),
              ("leg_share", ">", "FN L32–52; E-A2"), ("forearm_over_arm", ">", "FN L32–52"), ("shin_over_leg", ">", "FN L32–52"), ("hand_share", ">", "FN L32–52"),
              ("foot_share", ">", "FN L36"), (JP("wrist"), "<", "FN L32–52 (narrow wrists; exact-plane)"), (JP("knee"), "<", "FN L110–137 (joints small for limb length; exact-plane)"),
              (TD, "<", "FN L32–52 (skeletal)"), (BC, ">=", "E-A2 (bitrochanteric / crest not lower)")],
       "AE": [("neck_share", ">", "AE L50"), ("arm_share", ">", "AE L33–58 (even elongation)"), ("leg_share", ">", "AE L33–58; E-A2"), ("thorax_depth_share", "<", "AE L123–168"),
              ("hand_share", ">", "AE L57, L166"), ("foot_share", ">", "AE L168"), (JP("elbow"), "<", "AE L123–168 (gracile; exact-plane)"), (JP("wrist"), "<", "AE L123–168 (exact-plane)"),
              (JP("knee"), "<", "AE L123–168 (exact-plane)"), (TD, "<", "AE L123–168 (skeletal)"), (BC, ">=", "E-A2"), (WI, ">=", "AE-P6")],
       "VA": [("leg_share", ">", "E-A2 (hip-joint height > MF)"), (BC, ">=", "E-A2"), (PD, ">=", "VA-P4 (AP pelvic depth >= MF minimum)")]}
MFAT = {157: "MF157", 163: "MF163", 168: "MF168", 173: "MF173", 178: "MF178", 181: "MF181", 190: "MF190", 203: "MF203"}
SGAT = {173: "SG173", 178: "SG178", 181: "SG181", 190: "SG190", 203: "SG203"}
FAM = {"FN": (157, 163, 173, 178, 181, 190, 203, 211), "AE": (168, 173, 178, 181, 190, 203, 211, 221), "VA": (157, 163, 173, 178, 181, 190, 203)}
nm = lambda p, h: REF[p] if REF[p] == "%s%d" % (p, h) else "%s%d" % (p, h)
# U: head allometry per population (min > ref > max)
for p, (lo, hi) in (("FN", (157, 211)), ("AE", (168, 221)), ("VA", (157, 203))):
    r("U", "%s head share: minimum > reference" % p, nm(p, lo), ">", REF[p], "HH_share", "RM-UB-02"); r("U", "%s head share: maximum < reference" % p, nm(p, hi), "<", REF[p], "HH_share", "RM-UB-02")
    for k in ("hand_share", "foot_share", "neck_share", "neck / torso"):
        r("U", "%s %s: minimum vs reference" % (p, k), nm(p, lo), ">", REF[p], k, "RM-UB-02 diagnostic", True); r("U", "%s %s: maximum vs reference" % (p, k), nm(p, hi), "<", REF[p], k, "RM-UB-02 diagnostic", True)
# R: RM-OT-02 family matrix at matched heights (173 / 178 / 181 / 190 / 203 cm: all three populations exist)
for h in (173, 178, 181, 190, 203):
    F, A, Vv = nm("FN", h), nm("AE", h), nm("VA", h); t = "%d cm" % h
    r("R", "%s: Aelari > Fenn: neck / stature" % t, A, ">", F, "neck_share", "AE L33–58 (neck longer than Fenn)")
    r("R", "%s: Aelari > Fenn: torso / stature" % t, A, ">", F, "torso_share", "AE L40, L48, L58")
    r("R", "%s: Aelari > Vael: neck / torso" % t, A, ">", Vv, "neck / torso", "VA L123")
    r("R", "%s: Vael > Fenn: torso / stature" % t, Vv, ">", F, "torso_share", "VA L35–46")
    for o, on in ((F, "Fenn"), (A, "Aelari")):
        r("R", "%s: Vael < %s: leg / stature (hip-joint height, VA-P2a)" % (t, on), Vv, "<", o, "leg_share", "VA L46, L153; VA-P2a")
        r("R", "%s: Vael > %s: ribcage depth / stature (skin)" % (t, on), Vv, ">", o, "thorax_depth_share", "VA L35–46")
        r("R", "%s: Vael > %s: skeletal thoracic depth / stature" % (t, on), Vv, ">", o, TD, "VA L35–46 (skeletal)")
        r("R", "%s: Vael > %s: palm breadth / hand" % (t, on), Vv, ">", o, "palm_breadth_over_hand", "VA L114–154")
        for j in ("elbow", "wrist", "knee"): r("R", "%s: Vael > %s: %s (joint presence)" % (t, on, JP(j)), Vv, ">", o, JP(j), "VA L114–154; exact-plane")
        r("R", "%s: Vael > %s: skeletal AP pelvic depth / stature (VA-P4)" % (t, on), Vv, ">", o, PD, "PV-D6 a / VA-P4")
    for j in ("elbow", "knee"): r("R", "%s: Fenn < Aelari: %s (gracility order Fenn > Aelari, E-A1)" % (t, JP(j)), F, "<", A, JP(j), "E-A1 (FNL4 W1 ruling); exact-plane")
    r("R", "%s: Fenn < Aelari: skeletal waist interval / torso (FN-P6)" % t, F, "<", A, WI, "FN-P6")
    r("R", "%s: Aelari > Vael: skeletal waist interval / torso (AE-P6)" % t, A, ">", Vv, WI, "AE-P6")
    r("R", "%s: Aelari > Fenn: skeletal pelvic vertical / thoracic vertical (diagnostic for PV-D5)" % t, A, ">", F, PVC, "PV-D5 reads pelvic vertical / crest (G rows)", True)
    for k in ("arm_share", "forearm_over_arm", "shin_over_leg", "hand_share", "finger_over_hand", "foot_share", "thorax_breadth_share", TB):
        for a_, b_, lab in ((F, A, "Fenn vs Aelari"), (F, Vv, "Fenn vs Vael"), (A, Vv, "Aelari vs Vael")):
            r("R", "%s: %s: %s" % (t, lab, k.replace(T0, "")), a_, ">", b_, k, "no cross-elf direction authored", True)
# H: each population vs Marchfolk at matched height (the population's own canonical vs-human directions)
for p in ("FN", "AE", "VA"):
    for h in FAM[p]:
        if h not in MFAT: continue
        for k, op, src in HUM[p]: r("H", "%s %d cm vs Marchfolk %d: %s %s" % (p, h, h, op, k.replace(T0, "")), nm(p, h), op, MFAT[h], k, src)
    for h in (211, 221):
        if h in FAM[p]:
            for k, op, src in HUM[p]: r("H", "%s %d cm vs the tallest accepted Marchfolk (203): %s %s" % (p, h, op, k.replace(T0, "")), nm(p, h), op, "MF203", k, src + "; no Marchfolk above 203", True)
    if p == "AE":
        for h in (173, 178, 181, 190, 203):
            if h in MFAT: r("H", "AE %d cm vs Marchfolk: forearm / upper arm (even, approx MF; reported)" % h, nm(p, h), ">", MFAT[h], "forearm_over_upperarm", "AE L33–58 (≈ MF ±0.010 in W1)", True)
# S: Sagekin W2E dependency (order §9) - each elf vs Sagekin at matched height on the readings W2E exposed; scored in the elf's canonical
# direction vs humans where the canon gives one (complete-anatomy test: isolated overlap allowed, see the gate)
SGK = ["forearm_over_arm", "arm_share", "hand_share", "finger_over_hand", "span_der", "thorax_breadth_share", "thorax_depth_share", "leg_share", "shin_over_leg", "foot_share",
       JP("elbow"), JP("wrist"), JP("knee"), JP("ankle"), TD, "neck_share", "torso_share"]
for p in ("FN", "AE", "VA"):
    dirs = {k: (op, src) for k, op, src in HUM[p]}
    for h in (173, 178, 181, 190, 203):
        if h not in FAM[p]: continue
        for k in SGK:
            if k in dirs: r("S", "%s %d vs Sagekin %d: %s %s" % (p, h, h, dirs[k][0], k.replace(T0, "")), nm(p, h), dirs[k][0], SGAT[h], k, dirs[k][1] + "; Sagekin W2E dependency")
            else: r("S", "%s %d vs Sagekin %d: %s" % (p, h, h, k.replace(T0, "")), nm(p, h), ">", SGAT[h], k, "no direction vs humans authored for this population", True)
# K: large-human guard (Aelari upper statures; Broad Aelari) - report
for a_, s_ in (("AE203", "SK203"), ("AE211", "SK208"), ("AE221", "SK229"), ("AEB221", "SK229"), ("AEB190", "SK190"), ("FN211", "SK208"), ("VA203", "SK203")):
    for k in (TB, TD, SJ, CR, "torso_share", JP("knee"), JP("wrist"), JP("elbow")):
        r("K", "%s vs %s: %s" % (a_, s_, k.replace(T0, "")), a_, "<", s_, k, "Skarn guard (order §5, §11): report", True)
# F: frames (accepted elf breadth-only rule) at min / reference / max for each population
MINH = {"FN": 157, "AE": 168, "VA": 157}; MAXH = {"FN": 211, "AE": 221, "VA": 203}; REFH = {"FN": 181, "AE": 190, "VA": 178}
for p in ("FN", "AE", "VA"):
    for h in (MINH[p], REFH[p], MAXH[p]):
        c, n, b = nm(p, h), "%sN%d" % (p, h), "%sB%d" % (p, h); tag = "%s %d" % (p, h)
        for k in (TB, SJ, BI, CR, HS):
            mv.append({"code": "F", "kind": "D", "sign": -1, "a": n, "b": c, "k": k, "check": "Narrow (%s) reduces %s by >= 1 %%" % (tag, k.replace(T0, ""))})
            mv.append({"code": "F", "kind": "D", "sign": 1, "a": b, "b": c, "k": k, "check": "Broad (%s) increases %s by >= 1 %%" % (tag, k.replace(T0, ""))})
        for k in ("stature (cm)", "torso_share", "leg_share", "arm_share", "forearm_over_arm", "shin_over_leg", "HH_share", "hand_share", "neck_share"):
            for x in (n, b): mv.append({"code": "F", "kind": "L", "tol": 0.005, "a": x, "b": c, "k": k, "check": "%s keeps lengths (0.5 %%): %s" % (x, k)})
        for x in (n, b):
            mv.append({"code": "F", "kind": "L", "tol": 0.01, "a": x, "b": c, "k": TD, "check": "%s keeps thoracic depth (breadth-only frame; within 1 %%)" % x})
            for j in ("elbow", "wrist", "knee", "ankle"): mv.append({"code": "F", "kind": "L", "tol": 0.01, "a": x, "b": c, "k": JP(j), "check": "%s keeps joint scale (frame does not set gracility): %s within 1 %%" % (x, JP(j))})
            mv.append({"code": "F", "kind": "L", "tol": 0.02, "a": x, "b": c, "k": BC, "check": "%s keeps the hip joints with the crest: bitrochanteric / crest within 2 %%" % x, "report": True})
    for k, op, src in HUM[p]:
        for x in ("%sN%d" % (p, REFH[p]), "%sB%d" % (p, REFH[p])):
            h = REFH[p]
            if h in MFAT: r("F", "%s vs Marchfolk %d: %s %s (frame keeps the population direction)" % (x, h, op, k.replace(T0, "")), x, op, MFAT[h], k, src + "; frame vs unmatched central MF is a W1-ruled non-veto for breadth rows", k in ("thorax_breadth_share", TB))
# M: composition at 173 cm (matched Marchfolk 173 / Sagekin 173 composition states) and frame x composition at the reference
for p in ("FN", "AE", "VA"):
    for c in ("LOWMUS", "HIMUS", "HIFAT", "HIBOTH", "LOW", "MIN"):
        a = "%s173-%s" % (p, c)
        inv.append({"code": "M", "check": "%s: composition does not redefine proportions (torso, leg, arm, forearm, lower-leg, hand, neck within 1 %%)" % a, "a": a, "b": "%s173" % p,
                    "keys": ["torso_share", "leg_share", "arm_share", "forearm_over_arm", "shin_over_leg", "hand_share", "neck_share"]})
        for k, op, src in HUM[p]:
            if k.startswith(("skeletal", "elbow", "wrist", "knee", "ankle")): continue
            r("M", "%s vs Marchfolk 173 same composition (%s): %s %s" % (a, c, op, k), a, op, "MF-" + c, k, src + "; composition-matched")
            r("M", "%s vs Sagekin 173 same composition (%s): %s %s" % (a, c, op, k), a, op, "SG173-" + c, k, src + "; composition-matched; Sagekin W2E dependency")
    for nm_, src in (("NLOW", "N"), ("BHM", "B"), ("NHM", "N"), ("BHF", "B"), ("HF", None)):
        x = "%s-%s" % (p, nm_); b = "%s%s%d" % (p, src, REFH[p]) if src else REF[p]
        inv.append({"code": "M", "check": "%s: composition on the %s body does not redefine proportions (within 1 %%)" % (x, b), "a": x, "b": b,
                    "keys": ["torso_share", "leg_share", "arm_share", "forearm_over_arm", "shin_over_leg", "hand_share", "neck_share"]})
# X: named validators (population's own targets scaled)
for x, base, ks, src in (("FN15", "FN181", (("arm_share", ">"), ("hand_share", ">"), ("forearm_over_arm", ">")), "FN-15 maximum arm + hand"),
                         ("FN16", "FN181", (("leg_share", ">"), ("foot_share", ">"), ("shin_over_leg", ">")), "FN-16 maximum leg + foot"),
                         ("FN09", "FN181", (("arm_share", "<"), ("leg_share", "<")), "FN-09 short-limbed near the racial boundary"),
                         ("FN08", "FN181", (("torso_share", ">"),), "FN-08 long torso"),
                         ("AE19", "AE190", (("hand_share", ">"),), "AE-19 maximum hand"), ("AE20", "AE190", (("leg_share", ">"), ("foot_share", ">")), "AE-20 maximum leg + foot"),
                         ("AE11", "AE190", (("torso_share", ">"),), "AE-11 long torso"),
                         ("VA09", "VA178", (("leg_share", ">"),), "VL-09 long-limbed near the boundary"), ("VA10", "VA178", (("leg_share", "<"), ("thorax_depth_share", ">")), "VL-10 compact"),
                         ("VA23", "VAN178", (("thorax_depth_share", ">"),), "VL-23 deep ribcage, Narrow frame")):
    for k, op in ks: r("X", "%s moves %s vs its base: %s" % (src, op, k), x, op, base, k, src)
p_of = {"FN": "FN", "AE": "AE", "VA": "VA"}
for x, p, h in (("FN15", "FN", 181), ("FN16", "FN", 181), ("FN09", "FN", 181), ("FN08", "FN", 181), ("AE19", "AE", 190), ("AE20", "AE", 190), ("AE11", "AE", 190), ("AE24", "AE", 221),
                ("VA09", "VA", 178), ("VA10", "VA", 178), ("VA23", "VA", 178), ("VA24", "VA", 203)):
    mf = MFAT.get(h, "MF203")
    for k, op, src in HUM[p]: r("X", "%s keeps the %s direction vs Marchfolk %s: %s %s" % (x, p, mf[2:], op, k.replace(T0, "")), x, op, mf, k, src, h not in MFAT)
for x, o in (("VA09", "FN181"), ("VA09", "AE181")):
    r("X", "VL-09 long-limbed Vael stays below %s: leg share (VA-P2a)" % o, x, "<", o, "leg_share", "VA L46, VA-P2a (Vael 178 vs elf at 181; near-matched)")
for x, o in (("FN09", "SG181"), ("FN09", "MF181")):
    for k, op, src in HUM["FN"]: r("X", "FN-09 short-limbed Fenn vs %s: %s %s (boundary)" % (o, op, k.replace(T0, "")), x, op, o, k, src)
# J: exact-plane joint re-measurement of the W1 elf joint rows at the references (measurement normalization check)
for p, ref, mf in (("FN", "FN181", "MF181"), ("AE", "AE190", "MF190"), ("VA", "VA178", "MF178")):
    for j in ("elbow", "wrist", "knee", "ankle"):
        r("J", "%s reference vs matched Marchfolk: %s" % (p, JP(j)), ref, "<", mf, JP(j), "exact-plane; RM-UB-03", True)
        r("J", "%s reference vs matched Marchfolk: %s" % (p, JS(j)), ref, "<", mf, JS(j), "exact-plane; RM-UB-03", True)
        r("J", "%s reference vs Marchfolk 173 (W1 fixed reference): %s" % (p, JP(j)), ref, "<", "MF173", JP(j), "exact-plane vs the W1 slab rows (G)", True)
# P: pelvic / axial diagnostics at the boundaries (report)
for p in ("FN", "AE", "VA"):
    for h in (MINH[p], MAXH[p]):
        mf = MFAT.get(h, "MF203")
        for k in (CR, PD, PV, HS, BC, WI, PVC, sk("crest / thoracic breadth"), sk("pelvic AP / thoracic depth")):
            r("P", "%s %d vs Marchfolk %s: %s" % (p, h, mf[2:], k.replace(T0, "")), nm(p, h), ">", mf, k, "RM-UB-06 diagnostic", True)
# D: route cross-checks - native route where the re-solved macro falls in the generator's short-femur zone (macro < ~0.40)
for x, mf, h in (("AE168N", "MF168", 168), ("AE173N", "MF173", 173)):
    for k, op, src in HUM["AE"]:
        if not k.startswith("skeletal"): r("D", "route cross-check %s (native) vs Marchfolk %d: %s %s" % (x, h, op, k), x, op, mf, k, src + "; native route", True)
    r("D", "route cross-check %s vs macro-route AE%d: femur / leg" % (x, h), x, ">", "AE%d" % h, "femur_over_leg", "generator short-femur zone", True)
for x, b in (("FN163N", "FN163"), ("VA163N", "VA163")): r("D", "route cross-check %s vs macro-route %s: femur / leg" % (x, b), x, ">", b, "femur_over_leg", "generator short-femur zone", True)
# Q: diagnostic leg probes for the author ruling (NOT applied): Aelari leg-target strength x1.75 / x2.0 / x2.5, Vael lower-leg decrease removed
for x in ("AEP175_190", "AEP200_190", "AEP250_190"):
    r("Q", "%s vs Marchfolk 190: > leg share (AE L33–58, E-A2)" % x, x, ">", "MF190", "leg_share", "probe")
    r("Q", "%s vs Marchfolk 190: > arm share (AE L33–58)" % x, x, ">", "MF190", "arm_share", "probe")
    r("Q", "%s vs Fenn 190: > torso share (AE L40, L48, L58)" % x, x, ">", "FN190", "torso_share", "probe")
    r("Q", "%s vs Fenn 190: > neck share (AE L33–58)" % x, x, ">", "FN190", "neck_share", "probe")
    r("Q", "%s vs Sagekin 190: leg share" % x, x, ">", "SG190", "leg_share", "probe (Sagekin W2E dependency)", True)
    r("Q", "Vael 190 < %s: leg share (VA-P2a)" % x, "VA190", "<", x, "leg_share", "probe")
r("Q", "VAP0_190 vs Marchfolk 190: > leg share (E-A2)", "VAP0_190", ">", "MF190", "leg_share", "probe")
for o in ("AE190", "FN190"): r("Q", "VAP0_190 < %s: leg share (VA-P2a)" % o, "VAP0_190", "<", o, "leg_share", "probe")
for k, op, src in HUM["FN"]: r("X", "FN-09 at x0.75 keeps the Fenn direction vs Marchfolk 181: %s %s" % (op, k.replace(T0, "")), "FN09x75", op, "MF181", k, src)
for k, op in (("arm_share", "<"), ("leg_share", "<")): r("X", "FN-09 at x0.75 moves %s vs Fenn reference: %s" % (op, k), "FN09x75", op, "FN181", k, "FN-09")
json.dump({"rows": rows, "invariance": inv, "moves": mv, "series": {p: [nm(p, h) for h in FAM[p]] for p in FAM}}, open(sys.argv[1], "w"), indent=1)
print(len(rows), "rows", len(inv), "invariance", len(mv), "moves")
