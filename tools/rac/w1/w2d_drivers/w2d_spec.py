# RAC W2D (Gorrund W2) comparison-row specification (canon sources in each 'note'; GO = specs/gorrund/GORRUND_V1.md line, GR = GRASK_V1).
# Writes the spec JSON read by w2d_eval.py.   Usage: python3 w2d_spec.py OUT.json
import sys, json
rows, inv, mv = [], [], []
def r(code, chk, a, op, b, k, note="", report=False): rows.append({"code": code, "check": chk, "a": a, "op": op, "b": b, "k": k, "note": note, "report": report})
T0 = " [t=0.0]"
TB, TD, SJ, BI, CR, DB, PV, HS = ["skeletal %s%s" % (x, T0) for x in ("thoracic breadth / stature", "thoracic depth / stature", "shoulder-joint breadth / stature", "biacromial / stature",
                                                                   "crest breadth / stature", "thoracic depth / breadth", "pelvic vertical / stature", "hip-joint spacing / stature")]
BC = "skeletal bitrochanteric / crest" + T0
ALPC7 = ["skeletal ALPC %s%s" % (x, T0) for x in ("lower-thorax breadth / thorax (S3/S2 b)", "lumbar breadth / thorax (S4/S2 b)", "lower-thorax depth / thorax (S3/S2 d)",
                                                 "lumbar depth / thorax (S4/S2 d)", "crest / thorax breadth (S5/S2 b)", "hip-level / thorax breadth (S6/S2 b)", "pelvic AP / thoracic depth")]
JT = ["%s breadth / stature (exact-plane section)" % j for j in ("elbow", "wrist", "knee", "ankle")]
JS = ["%s breadth / adjacent segment (exact-plane section)" % j for j in ("elbow", "wrist", "knee", "ankle")]
LIMB = [("torso_share", ">", "GO L259, L276 (greater torso / axial contribution than Grask)"), ("leg_share", "<", "GO L208 GO-P2b, L276 (lower lower-limb contribution)"),
        ("arm_share", "<", "GO L300; GR L164 (Grask greater proportional arm length)"), ("span_der", "<", "GO L300; GR L243 (Grask greater span)")]
EMPH = [("forearm_over_arm", "<", "GO L259; GR L59, L247 (Grask forearm emphasis)"), ("shin_over_leg", "<", "GO L259; GR L320 (Grask lower-leg emphasis)")]
def vs_grask(code, go, gr, tag, joints=True, emph=True):
    for k, op, src in LIMB + (EMPH if emph else []): r(code, "%s: Gorrund %s Grask: %s" % (tag, op, k), go, op, gr, k, src)
    for k, src in ((TB, "GO L41 (thoracic breadth > Grask at matched height)"), (TD, "GO L259 (thoracic depth)"), (SJ, "GO-G7 / AD-G6 (girdle breadth > Grask)"), (DB, "GO-G7 / AD-G7")):
        r(code, "%s: Gorrund > Grask: %s" % (tag, k.replace(T0, "")), go, ">", gr, k, src)
    r(code, "%s: Gorrund >= Grask: pelvic vertical / stature (GO-P3)" % tag, go, ">=", gr, PV, "GO L209 GO-P3 (vertical contribution >= Grask relative to stature)")
    if joints:
        for k in JS: r(code, "%s: Gorrund > Grask: %s" % (tag, k), go, ">", gr, k, "RAC-05 L32 joint scale (joint / adjacent bone; the W1 'joint scale GO > GR' metric); GO L259; exact-plane section (REFERENCE_ANATOMY_V1 §10)")
        for k in JT: r(code, "%s: Gorrund > Grask: %s" % (tag, k), go, ">", gr, k, "GO L259 (joint presence), L276 (substantial joint scale) read per stature; exact-plane section")
# S: matched-height Gorrund vs Grask at the real overlap 208 / 218 / 229 / 239 (no Gorrund below 208: GO L29)
for h in ("208", "218", "229", "239"): vs_grask("S", "GO" + h, "GR" + h, "%s cm" % h)
# K: matched-height Gorrund vs Skarn 208 / 218 / 229 (architecture rows directional; torso / limb shares and joints REPORT: AD-4, GO L700, L260)
for h in ("208", "218", "229"):
    g, s = "GO" + h, "SK" + h
    for k, src in ((TD, "RM-LR-02 (b); GO L260 (greater axial depth)"), (TB, "RM-LR-02 (a); GO L41 (greater axial breadth than Skarn at equal height)"), (DB, "GO-G7 / AD-G7")):
        r("K", "%s cm: Gorrund > Skarn: %s" % (h, k.replace(T0, "")), g, ">", s, k, src)
    for k in ALPC7: r("K", "%s cm: Gorrund vs Skarn: %s" % (h, k.replace(T0, "")), g, ">", s, k, "ALPC-7 is defined against Broad Skarn (code B); ordinary Skarn shown for context", report=True)
    r("K", "%s cm: Gorrund vs Skarn: shoulder-joint breadth / stature" % h, g, ">", s, SJ, "GO-G7: Gorrund vs Skarn girdle breadth undetermined (AD-4)", report=True)
    for k, op, src in LIMB: r("K", "%s cm: Gorrund vs Skarn: %s" % (h, k), g, op, s, k, "AD-4: Skarn-Gorrund torso / limb separation undetermined by design", report=True)
    for k in JT + JS: r("K", "%s cm: Gorrund vs Skarn: %s" % (h, k), g, ">", s, k, "GO L260 'distinct joint relationships' (no direction authored); RM-LR-05", report=True)
# B: AD-1 Cross-Population Boundary Test: 208 cm Gorrund vs Broad Skarn at equal and greater Skarn height through 229 (GO L292, L761 ALPC-7)
for s in ("SKB208", "SKB218", "SKB229"):
    r("B", "AD-1: Gorrund 208 > %s: thoracic depth / stature" % s, "GO208", ">", s, TD, "GO L292 (thoracic depth relative to stature)")
    r("B", "AD-1: Gorrund 208 > %s: thoracic depth / breadth" % s, "GO208", ">", s, DB, "GO L292 (thoracic depth relative to breadth)")
    for k in ALPC7: r("B", "AD-1 / ALPC-7: Gorrund 208 > %s: %s" % (s, k.replace(T0, "")), "GO208", ">", s, k, "GO L761 (ALPC-1 / ALPC-2a > Broad Skarn beyond the marginal threshold)")
    r("B", "Gorrund 208 vs %s: thoracic breadth / stature (no arbitrary breadth inflation)" % s, "GO208", ">", s, TB, "order §4: distinct without forcing breadth", report=True)
for g, s, h in (("GO218", "SKB218", "218"), ("GO229", "SKB229", "229")):
    for k in ALPC7: r("B", "ALPC-7 at %s cm: Gorrund > Broad Skarn: %s" % (h, k.replace(T0, "")), g, ">", s, k, "GO L761")
    r("B", "%s cm: Gorrund > Broad Skarn: thoracic depth / breadth" % h, g, ">", s, DB, "GO-G7 / AD-G7")
    r("B", "%s cm: Gorrund > Broad Skarn: thoracic depth / stature" % h, g, ">", s, TD, "RM-LR-02 (b)")
    r("B", "%s cm: Gorrund vs Broad Skarn: thoracic breadth / stature" % h, g, ">", s, TB, "no arbitrary breadth inflation", report=True)
    for k in JT + JS: r("B", "%s cm: Gorrund vs Broad Skarn: %s" % (h, k), g, ">", s, k, "large-race review L61: Skarn vs Gorrund joint scale n.d.; exact-plane section", report=True)
# F: frames (GO L80, L200 GO-G6, L245): Narrow GON5 / Broad GOB7 vs Balanced GOREF at the reference; and at 218 cm (GON5_218 / GOB7_218 vs GO218)
for n, b, c, tag in (("GON5", "GOB7", "GOREF", "reference"), ("GON5_218", "GOB7_218", "GO218", "218 cm")):
    for k, wh in ((TB, "both"), (SJ, "both"), (BI, "both"), (CR, "both"), (HS, "both")):
        mv.append({"code": "F", "kind": "D", "sign": -1, "a": n, "b": c, "k": k, "check": "Narrow (%s) reduces %s by >= 1 %% (GO-G6)" % (tag, k.replace(T0, ""))})
        if k != TB: mv.append({"code": "F", "kind": "D", "sign": 1, "a": b, "b": c, "k": k, "check": "Broad (%s) increases %s by >= 1 %% (GO L245)" % (tag, k.replace(T0, ""))})
    mv.append({"code": "F", "kind": "L", "tol": 0.01, "a": b, "b": c, "k": TB, "check": "Broad (%s) thoracic breadth / stature (bounded by AD-G7 / ALPC-4; see the frame probes)" % tag, "report": True})
    for k in ("stature (cm)", "torso_share", "leg_share", "arm_share", "forearm_over_arm", "shin_over_leg", "HH_share"):
        for x in (n, b): mv.append({"code": "F", "kind": "L", "tol": 0.005, "a": x, "b": c, "k": k, "check": "%s keeps lengths (0.5 %%): %s" % (x, k)})
    for x in (n, b): mv.append({"code": "F", "kind": "L", "tol": 0.005, "a": x, "b": c, "k": "span_der", "report": True,
                                "check": "%s derived span (includes girdle breadth, so it follows the frame; arm / stature is the length row)" % x})
    for x, lab in ((n, "Narrow keeps axial depth (GO L80, GO-G6)"), (b, "Broad never hard-links to depth (GO L245)")):
        mv.append({"code": "F", "kind": "L", "tol": 0.01, "a": x, "b": c, "k": TD, "check": "%s: %s — thoracic depth / stature within 1 %%" % (x, lab)})
    for k in JT + JS:
        mv.append({"code": "F", "kind": "L", "tol": 0.01, "a": n, "b": c, "k": k, "check": "Narrow (%s) keeps joint scale (GO-G6): %s within 1 %%" % (tag, k)})
        mv.append({"code": "F", "kind": "L", "tol": 0.01, "a": b, "b": c, "k": k, "check": "Broad (%s): %s vs Balanced" % (tag, k), "report": True})
# frames do not collapse: Broad Gorrund vs Broad Skarn (229) and thick (Broad) Grask (218); Narrow Gorrund vs Grask / Narrow Grask (218); vs enlarged Marchfolk 203
for k in ALPC7: r("F", "Broad Gorrund (reference) > Broad Skarn 229: %s" % k.replace(T0, ""), "GOB7", ">", "SKB229", k, "GO L761 ALPC-7; order §4 (not Broad Skarn)")
r("F", "Broad Gorrund (reference) > Broad Skarn 229: thoracic depth / breadth", "GOB7", ">", "SKB229", DB, "GO-G7")
r("F", "Broad Gorrund (reference) > Broad Skarn 229: thoracic depth / stature", "GOB7", ">", "SKB229", TD, "RM-LR-02 (b)")
vs_grask("F", "GOB7_218", "GRB2", "Broad Gorrund 218 vs Broad (thick) Grask 218")
vs_grask("F", "GON5_218", "GR218", "Narrow Gorrund 218 vs Balanced Grask 218 (GO L245: GOR-BODY-04 never converges on Grask)")
vs_grask("F", "GON5_218", "GRN5", "Narrow Gorrund 218 vs Narrow Grask 218")
for x in ("GON5", "GOB7"):
    for k, op, src in ((TD, ">", "GO L41, L276 (depth signal; not an enlarged human)"), (DB, ">", "GO-G7 (depth vs breadth)")):
        r("F", "%s > Marchfolk 203 (largest accepted Marchfolk): %s" % (x, k.replace(T0, "")), x, op, "MF203", k, src)
    for k in ALPC7[:4]: r("F", "%s > Marchfolk 203: %s" % (x, k.replace(T0, "")), x, ">", "MF203", k, "GO ALPC-1 (vs MF profile shape), compared with the largest Marchfolk")
# M: composition (GO L82, L249, L264; ALPC-6): shares unchanged; skeleton shared by construction; same-composition comparisons
for c in ("GOR-BODY-06", "GOR-BODY-07", "GOR-BODY-08", "GOR-BODY-09", "GOR-BODY-10", "GOR-BODY-11", "GOR-BODY-16"):
    inv.append({"code": "M", "check": "%s: composition does not redefine anatomy (torso, leg, arm, span, forearm, lower-leg within 1 %%)" % c, "a": c, "b": "GOREF",
                "keys": ["torso_share", "leg_share", "arm_share", "span_der", "forearm_over_arm", "shin_over_leg"]})
for h, base in (("208", "GO208"), ("218", "GO218")):
    for c in ("06", "07", "09", "10", "16"):
        inv.append({"code": "M", "check": "GOR-BODY-%s at %s cm: composition does not redefine anatomy vs %s (within 1 %%)" % (c, h, base), "a": "GOR-BODY-%s_%s" % (c, h), "b": base,
                    "keys": ["torso_share", "leg_share", "arm_share", "span_der", "forearm_over_arm", "shin_over_leg"]})
# same composition AND matched height: Gorrund 208 vs Skarn 208 composition states (W2B), Gorrund 218 vs Grask 218 composition states (W1l)
for c, sk, gr, tag in (("06", "SK-LOWMUS", "GR-BODY-06", "low muscle"), ("07", "SK-HIMUS", "GR-BODY-07", "high muscle"), ("09", "SK-HIFAT", "GR-BODY-08", "higher fat"),
                       ("10", "SK-HIBOTH", "GR-BODY-09", "high muscle + fat"), ("16", "SK-LOW", "GR-LOW", "low muscle + low fat")):
    g8, g18 = "GOR-BODY-%s_208" % c, "GOR-BODY-%s_218" % c
    r("M", "208 cm, %s: Gorrund > Skarn same composition: skin thoracic depth / stature" % tag, g8, ">", sk, "thorax_depth_share", "GO L82, L260 (massive without muscle); RM-LR-02 (b)")
    r("M", "208 cm, %s: Gorrund > Skarn same composition: skin thoracic breadth / stature" % tag, g8, ">", sk, "thorax_breadth_share", "RM-LR-02 (a), skin directional reading")
    r("M", "218 cm, %s: Gorrund > Grask same composition: skin thoracic depth / stature" % tag, g18, ">", gr, "thorax_depth_share", "GO L259 (fails if the distinction depends on muscle or fat)")
    r("M", "218 cm, %s: Gorrund > Grask same composition: skin thoracic breadth / stature" % tag, g18, ">", gr, "thorax_breadth_share", "GO L41, L259")
    for k, op, src in LIMB: r("M", "218 cm, %s: Gorrund %s Grask same composition: %s" % (tag, op, k), g18, op, gr, k, src + "; same composition")
for k in ("thorax_depth_share", "thorax_breadth_share"):
    r("M", "low composition Gorrund 208 (0.25 / 0.25) vs Marchfolk low 173 (0.25 / 0.25): skin %s" % k, "GOR-BODY-16_208", ">", "MF-LOW", k, "GO L82 (low-muscle Gorrund stays structurally massive); ALPC-6", report=True)
# X: named extremes GOR-BODY-12 (lower axial breadth) and GOR-BODY-14 (lower thoracic depth) at the reference
for x, tag in (("GON5", "GOR-BODY-12 = lowest valid axial-breadth probe (Narrow magnitude)"), ("GOD14_9", "GOR-BODY-14 = lower thoracic-depth valid extreme (depth sculpt x0.90)")):
    r("X", "%s: thoracic depth / breadth > Grask (central 229)" % tag, x, ">", "GR229", DB, "GO-G7 / AD-G7")
    r("X", "%s: thoracic depth / stature > Grask (229)" % tag, x, ">", "GR229", TD, "GO L259")
    r("X", "%s: thoracic depth / stature > Skarn 229" % tag, x, ">", "SK229", TD, "RM-LR-02 (b)")
    r("X", "%s: thoracic depth / breadth > Skarn 229" % tag, x, ">", "SK229", DB, "GO-G7 / AD-G7 (ALPC-5 requires only the depth criteria vs MF on GOR-BODY-14, GO L759)")
# RM-LR-03 / LR-04: low-breadth Gorrund vs Broad Skarn at equal height (breadth may invert; depth, ALPC, joints, axial integration carry)
for x, tag in (("GON5", "GOR-BODY-12 (reference)"), ("GOD14_9", "GOR-BODY-14 (reference)")):
    for k in ALPC7: r("X", "RM-LR-03: %s > Broad Skarn 229: %s" % (tag, k.replace(T0, "")), x, ">", "SKB229", k, "GO L761 ALPC-7; LR-04")
    r("X", "RM-LR-03: %s > Broad Skarn 229: thoracic depth / stature" % tag, x, ">", "SKB229", TD, "LR-04 (depth carries)")
    r("X", "RM-LR-03: %s vs Broad Skarn 229: thoracic depth / breadth" % tag, x, ">", "SKB229", DB, "GO-G7", report=(x == "GOD14_9"))
    r("X", "RM-LR-03: %s vs Broad Skarn 229: thoracic breadth / stature (may invert, LR-04)" % tag, x, ">", "SKB229", TB, "LR-04", report=True)
    for k in JT + JS: r("X", "RM-LR-03: %s vs Broad Skarn 229: %s" % (tag, k), x, ">", "SKB229", k, "LR-04 lists joints as a carrier; Skarn vs Gorrund joints n.d. (large-race review L61)", report=True)
# AD3 (GO L253, L265; GR L259, L715; RAC-04 §2 Gorrund limb presence): limb-present Gorrund family stays below the shortest-limbed valid Grask
for go, tag in (("GOLP218", "limb-present Gorrund 218"), ("GO218", "central Gorrund 218")):
    for k, op, src in LIMB: r("AD3", "%s %s GR-BODY-10 (shortest-limbed valid Grask, 218): %s" % (tag, op, k), go, op, "GR-BODY-10", k, "AD-3 (a) / RM-LR-04: " + src)
for go, tag in (("GON5_218", "GOR-BODY-12 at 218"), ("GOD14_9_218", "GOR-BODY-14 at 218")):
    vs_grask("AD3", go, "GRB2", "%s vs Broad Grask 218 (AD-3 reciprocal)" % tag, emph=False)
    for k, op, src in LIMB: r("AD3", "%s %s GR-BODY-10: %s" % (tag, op, k), go, op, "GR-BODY-10", k, "AD-3: " + src)
# D: fixed-reference W1 rows at the boundaries (boundary-stature rule: REPORT; stature-matched comparisons above govern)
r("D", "GO-P2b bitrochanteric / crest ~ Marchfolk 203 (largest accepted Marchfolk) at Gorrund 208", "GO208", "~", "MF203", BC, "GO-P2b fixed reference is MF 173 (W1 row); stature-nearest accepted MF shown", report=True)
r("D", "GO-P2b bitrochanteric / crest ~ Marchfolk 173 (W1 fixed reference) at Gorrund 208", "GO208", "~", "MF173", BC, "W1 fixed-reference row", report=True)
r("D", "GO-P3 pelvic vertical / stature >= Grask at Gorrund 251 vs the tallest accepted Grask (239)", "GO251", ">=", "GR239", PV, "GO-P3; matched comparison impossible above 239", report=True)
r("D", "Narrow Gorrund 218: GO-P2b bitrochanteric / crest ~ Marchfolk 203", "GON5_218", "~", "MF203", BC, "fixed-reference row at a non-reference stature", report=True)
for h in ("208", "218", "229"): r("K", "%s cm: Gorrund > Skarn: skin thoracic breadth / stature (directional skin row, matched height)" % h, "GO" + h, ">", "SK" + h, "thorax_breadth_share", "RM-LR-02 (a), W1 directional reading")
for g in ("GO239", "GO251"):
    r("D", "%s skin thoracic breadth / stature vs Skarn 208 (W1 fixed reference)" % g, g, ">", "SK208", "thorax_breadth_share", "fixed-reference directional row", report=True)
    r("D", "%s skin thoracic breadth / stature vs the tallest accepted Skarn (229)" % g, g, ">", "SK229", "thorax_breadth_share", "no Skarn above 229", report=True)
json.dump({"rows": rows, "invariance": inv, "moves": mv}, open(sys.argv[1], "w"), indent=1); print(len(rows), "rows", len(inv), "invariance", len(mv), "moves")
