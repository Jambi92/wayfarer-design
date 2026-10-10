# RAC W3A (Halvren genealogy-conditioned stature tails) comparison specification for w2g_eval.py (same row types: rows, spans, passing,
# moves, invariance, continuity series). Order reviews/chatgpt-rac-w2-final-acceptance-w3a-halvren-genealogy-tail-order.md (§ = section);
# canon specs/halvren/HALVREN_V1.md H-1...H-6. Reading sets = W2G (w2g_spec.CANON: accepted W1 Halvren source-plausible readings; BODY: the 24
# body-only readings of the neutralized source-passing protocol). NON-CANON diagnostics.
# Boundary-stature rule for tail spans: below 152 cm only Marchfolk has a valid adult (H-1); above 221 cm only Skarn. The scored span is the
# matched-height supporting source(s) + the NEAREST VALID ADULT of every other span source (labelled; never matched height). Aelari above
# 221 cm = W2G D1 ENDPOINT diagnostic (AE221), never matched height.   Usage: python3 w3a_spec.py OUT.json
import sys, json
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/w2g_drivers')
import importlib.util
spec = importlib.util.spec_from_file_location("w2gs", "/home/claude/wayfarer-design/tools/rac/w1/w2g_drivers/w2g_spec.py")
src = open(spec.origin).read().split("# U: allometry")[0]          # constants only (CANON, BODY, AXIAL, JP, JS, sk, ...)
G = {}; exec(src.replace("sys.argv[1]", "'/dev/null'"), G)
CANON, BODY, AXIAL, JP, JS, sk, T0 = G["CANON"], G["BODY"], G["AXIAL"], G["JP"], G["JS"], G["sk"], G["T0"]
TB, TD, SJ = sk("thoracic breadth / stature"), sk("thoracic depth / stature"), sk("shoulder-joint breadth / stature")
rows, inv, mv, spans, passing = [], [], [], [], []
def r(code, chk, a, op, b, k, note="", report=False): rows.append({"code": code, "check": chk, "a": a, "op": op, "b": b, "k": k, "note": note, "report": report})
def tg(h): return ("%g" % h).replace('.', 'p')
LO = (147.2, 147.5, 148, 149, 150); UP = (217, 219, 221, 225, 228.8)
LCL = {"C": LO, "M": (147.2, 148, 150), "X": (148,)}
UCL = {"C": UP, "S": UP, "A": (217, 219, 220.8), "SA": (221, 225, 228.8), "SD": (221, 225, 228.8), "AD": (220.8,), "SAD": (228.8,)}
AEM = {217: "AE217", 219: "AE219", 220.8: "AE220p8", 221: "AE221"}
NAME = {"C": "central Halvren anatomy", "M": "Marchfolk-expressed", "X": "mixed Marchfolk + Fenn", "S": "Skarn-expressed", "A": "Aelari-expressed", "SA": "Skarn + Aelari",
        "SD": "PROBE Skarn-expressed + Skarn leg development", "AD": "PROBE Aelari-expressed + Aelari leg development", "SAD": "PROBE Skarn + Aelari + leg development"}
def passrow(code, chk, a, b, report=False): passing.append({"code": code, "check": chk, "a": a, "b": b, "keys": BODY, "min_sep": 2, "report": report})
# L: lower tail (HV-49; Marchfolk-supported)
for c, hs in LCL.items():
    for h in hs:
        a = "HL%s%s" % (tg(h), c); m = "MF%s" % tg(h)
        passrow("L", "%g cm %s (Marchfolk-supported): not a matched-height Marchfolk duplicate (%s; body-only, N3/N4)" % (h, NAME[c], m), a, m)
        passrow("L", "%g cm %s vs Marchfolk 147 (W2A shortest accepted adult; report)" % (h, NAME[c]), a, "MF147", True)
        for k in CANON: spans.append({"code": "L", "check": "%g cm %s inside the boundary-stature source span (%s + nearest valid SG152 / FN157 / VA157): %s" % (h, NAME[c], m, k), "a": a, "srcs": [m, "SG152", "FN157", "VA157"], "k": k})
        for k in [x for x in BODY if x not in CANON]: spans.append({"code": "L", "check": "%g cm %s vs the boundary-stature span (report): %s" % (h, NAME[c], k.replace(T0, "")), "a": a, "srcs": [m, "SG152", "FN157", "VA157"], "k": k, "report": True})
        r("L", "%g cm %s adult read: head share not above matched-height Marchfolk (%s)" % (h, NAME[c], m), a, "<=", m, "HH_share", "adult-read (§7 test 7; no child proportions)")
        r("L", "%g cm %s adult read: head share vs Marchfolk 147 (report)" % (h, NAME[c]), a, "<=", "MF147", "HH_share", "", True)
# allometry / no uniform scaling: the tail is not a uniformly scaled 152 cm Halvren (head share rises as stature falls; the native route's adult allometry)
for h in LO:
    a = "HL%sC" % tg(h)
    r("U", "%g cm vs HV152: head share higher (adult allometry, not uniform scaling; report - the gate scores non-uniformity over all readings)" % h, a, ">", "HV152", "HH_share", "§8 no uniform scaling", True)
    for k in ("hand_share", "foot_share", "neck_share", JS("knee"), JS("ankle"), "thorax_breadth_share"): r("U", "%g cm vs HV152: %s (report)" % (h, k), a, ">", "HV152", k, "", True)
# H: upper tail (HV-50; Skarn / Aelari supported)
for c, hs in UCL.items():
    for h in hs:
        a = "HU%s%s" % (tg(h), c.replace("D", "") + ("D" if c.endswith("D") else "")); s = "SK%s" % tg(h); ae = AEM.get(h)
        passrow("H", "%g cm %s: not a matched-height Skarn duplicate (%s; body-only, N3/N4)" % (h, NAME[c], s), a, s)
        if ae: passrow("H", "%g cm %s: not a matched-height Aelari duplicate (%s)" % (h, NAME[c], ae), a, ae)
        else: passrow("H", "%g cm %s vs Aelari 221 — D1 ENDPOINT source-family diagnostic (never matched height)" % (h, NAME[c]), a, "AE221")
        aem = ae or "AE221"; srcs = [s, aem, "FN211", "SG208", "MF203", "VA203"]
        for k in CANON: spans.append({"code": "H", "check": "%g cm %s inside the boundary-stature source span (%s + %s%s + nearest valid FN211 / SG208 / MF203 / VA203): %s" % (h, NAME[c], s, aem, "" if ae else " [D1 endpoint]", k), "a": a, "srcs": srcs, "k": k})
        for k in CANON: spans.append({"code": "H", "check": "%g cm %s vs the supporting-source span only (%s, %s; report): %s" % (h, NAME[c], s, aem, k), "a": a, "srcs": [s, aem], "k": k, "report": True})
        for k in (TB, TD, SJ, "torso_share", JP("knee"), JP("wrist")): r("K", "%g cm %s vs %s: %s (Skarn guard, report)" % (h, NAME[c], s, k.replace(T0, "")), a, "<", s, k, "", True)
# Aelari beyond its valid range (source-first probe, §9 / §15): HU225A is NOT a matched-height test; report against SK225 and the D1 endpoint
passrow("H", "PROBE 225 cm Aelari-expressed (beyond the valid Aelari range; report) vs SK225", "HU225A", "SK225", True)
passrow("H", "PROBE 225 cm Aelari-expressed (beyond the valid Aelari range; report) vs AE221 D1 endpoint", "HU225A", "AE221", True)
# N: negative controls (H-1: Fenn / Vael / Sagekin do not extend a tail; Marchfolk does not extend the upper tail) - report
for c, near in (("FN", "FN157"), ("VA", "VA157"), ("SG", "SG152")):
    passrow("N", "control 148 cm %s-expressed (no Marchfolk support) vs MF148 (report)" % c, "HL148" + c, "MF148", True)
    passrow("N", "control 148 cm %s-expressed vs %s (nearest valid adult of the expressed source; report)" % (c, near), "HL148" + c, near, True)
for c, near in (("FN", "FN211"), ("VA", "VA203"), ("SG", "SG208"), ("MF", "MF203")):
    passrow("N", "control 221 cm %s-expressed (no Skarn / Aelari support) vs SK221 (report)" % c, "HU221" + c, "SK221", True)
    passrow("N", "control 221 cm %s-expressed vs %s (tallest valid adult of the expressed source; report)" % (c, near), "HU221" + c, near, True)
# F / M: frame and composition stress at the proposed endpoints (§10)
EP = {"HL147p2C": ("MF147p2", None), "HU228p8S": ("SK228p8", "AE221"), "HU220p8A": ("SK220p8", "AE220p8"), "HU228p8SA": ("SK228p8", "AE221")}
for e, (s1, s2) in EP.items():
    for tag_, sgn in (("N", -1), ("B", 1)):
        x = e + "-" + tag_
        for k in (TB, SJ, sk("biacromial / stature"), sk("crest breadth / stature"), sk("hip-joint spacing / stature")):
            mv.append({"code": "F", "kind": "D", "sign": sgn, "a": x, "b": e, "k": k, "check": "%s %s breadth: %s by >= 1 %%" % (x, "reduces" if sgn < 0 else "increases", k.replace(T0, ""))})
        for k in ("stature (cm)", "torso_share", "leg_share", "arm_share", "forearm_over_arm", "shin_over_leg", "HH_share", "hand_share", "neck_share"):
            mv.append({"code": "F", "kind": "L", "tol": 0.005, "a": x, "b": e, "k": k, "check": "%s keeps lengths (0.5 %%): %s" % (x, k)})
        for j in ("elbow", "wrist", "knee", "ankle"): mv.append({"code": "F", "kind": "L", "tol": 0.01, "a": x, "b": e, "k": JP(j), "check": "%s keeps joint scale: %s (1 %%)" % (x, JP(j))})
        passrow("F", "%s not a duplicate of %s" % (x, s1), x, s1)
        if s2: passrow("F", "%s not a duplicate of %s%s" % (x, s2, " (D1 endpoint)" if s2 == "AE221" and "228" in e else ""), x, s2)
        for k in CANON: spans.append({"code": "F", "check": "%s inside the boundary-stature span: %s (report)" % (x, k), "a": x, "srcs": [s1] + ([s2] if s2 else []) + (["SG152", "FN157", "VA157"] if e.startswith("HL") else ["FN211", "SG208", "MF203", "VA203"]), "k": k, "report": True})
    for cs in ("LOWMUS", "HIMUS", "LOWFAT", "HIFAT"):
        x = "%s-%s" % (e, cs)
        inv.append({"code": "M", "check": "%s: composition does not redefine proportions (within 1 %%)" % x, "a": x, "b": e, "keys": ["torso_share", "leg_share", "arm_share", "forearm_over_arm", "shin_over_leg", "hand_share", "neck_share"]})
        passrow("M", "%s not a duplicate of the same-composition %s-%s" % (x, s1, cs), x, "%s-%s" % (s1, cs))
        if s2 and s2 != "AE221": passrow("M", "%s not a duplicate of the same-composition %s-%s" % (x, s2, cs), x, "%s-%s" % (s2, cs))
        passrow("M", "%s vs reference-composition %s (report)" % (x, s1), x, s1, True)
# collision guards (§17 Q6 / Q7): Broad high-muscle upper-tail Halvren vs Skarn (reference and Broad Skarn); Narrow low-mass vs Aelari / Fenn
for e in ("HU228p8S", "HU228p8SA"):
    passrow("Q", "Q6 Broad %s vs Broad Skarn SKB228p8" % e, e + "-B", "SKB228p8")
    passrow("Q", "Q6 high-muscle %s vs high-muscle Skarn SK228p8-HIMUS" % e, e + "-HIMUS", "SK228p8-HIMUS")
for e, aes in (("HU220p8A", "AE220p8"), ("HU228p8S", "AE221"), ("HU228p8SA", "AE221")):
    passrow("Q", "Q7 Narrow %s vs %s%s" % (e, aes, " (D1 endpoint)" if aes == "AE221" else ""), e + "-N", aes)
    passrow("Q", "Q7 Narrow %s vs FN211 (tallest valid Fenn; report)" % e, e + "-N", "FN211", True)
passrow("Q", "Q7/Q8 Narrow HL147p2C vs MF147p2", "HL147p2C-N", "MF147p2")
passrow("Q", "Q7 Narrow HL147p2C vs FN157 (nearest valid Fenn; report)", "HL147p2C-N", "FN157", True)
passrow("Q", "Q7 low-fat HL147p2C vs MF147p2-LOWFAT", "HL147p2C-LOWFAT", "MF147p2-LOWFAT")
# condition series run at constant expression only (the expression step from the central HV213 is anatomy, not stature; reported as the
# expression offset, not continuity). HV163 -> HV173 = the accepted W2G native <-> macro route junction (carried creator dependency).
series = {"HV-C": ["HL147p2C", "HL147p5C", "HL148C", "HL149C", "HL150C", "HV152", "HV163", "HV173", "HV178", "HV181", "HV190", "HV203", "HV213", "HU217C", "HU219C", "HU221C", "HU225C", "HU228p8C"],
          "HV-M": ["HL147p2M", "HL148M", "HL150M"], "HV-S": ["HU217S", "HU219S", "HU221S", "HU225S", "HU228p8S"], "HV-A": ["HU217A", "HU219A", "HU220p8A"],
          "HV-SA": ["HU221SA", "HU225SA", "HU228p8SA"], "MF": ["MF147", "MF147p2", "MF147p5", "MF148", "MF149", "MF150", "MF152"],
          "AE": ["AE203", "AE211", "AE217", "AE219", "AE220p8", "AE221"], "HV-SD": ["HU221SD", "HU225SD", "HU228p8SD"],
          "SK": ["SK208", "SK217", "SK219", "SK221", "SK225", "SK228p8", "SK229"]}
json.dump({"rows": rows, "invariance": inv, "moves": mv, "spans": spans, "passing": passing, "toward": [], "series": series}, open(sys.argv[1], "w"), indent=1)
print(len(rows), "rows", len(inv), "invariance", len(mv), "moves", len(spans), "spans", len(passing), "passing")
