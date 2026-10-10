# RAC W3A1 (Halvren tail closure) comparison specification for w2g_eval.py. Order reviews/chatgpt-rac-w3a1-halvren-tail-closure-order.md.
# Reading sets = W2G (CANON: accepted W1 Halvren source-plausible readings; BODY: the 24 body-only readings of the neutralized protocol).
# AD-W3A-3: the scored tail coherence rule is the BOUNDARY-STATURE SPAN (matched supporting source(s) where valid + nearest valid adult of every other
# span source); the matched-supporting-source-only span is a diagnostic source-relationship REPORT. Aelari above 221 cm = D1 ENDPOINT, never matched.
# Codes: A coupled upper-tail family (AD-W3A-1), O coupling onset at 213 cm, Z coupling-strength sweep, F / M endpoint frame / composition stress,
# Q collision guards, C continuity series. NON-CANON diagnostics.   Usage: python3 w3a1_spec.py OUT.json
import sys, json, importlib.util
spec = importlib.util.spec_from_file_location("w2gs", "/home/claude/wayfarer-design/tools/rac/w1/w2g_drivers/w2g_spec.py")
G = {}; exec(open(spec.origin).read().split("# U: allometry")[0].replace("sys.argv[1]", "'/dev/null'"), G)
CANON, BODY, JP, sk, T0 = G["CANON"], G["BODY"], G["JP"], G["sk"], G["T0"]
TB, TD, SJ = sk("thoracic breadth / stature"), sk("thoracic depth / stature"), sk("shoulder-joint breadth / stature")
rows, inv, mv, spans, passing = [], [], [], [], []
def tg(h): return ("%g" % h).replace('.', 'p')
def r(code, chk, a, op, b, k, note="", report=False): rows.append({"code": code, "check": chk, "a": a, "op": op, "b": b, "k": k, "note": note, "report": report})
def passrow(code, chk, a, b, report=False): passing.append({"code": code, "check": chk, "a": a, "b": b, "keys": BODY, "min_sep": 2, "report": report})
AEM = {215: "AE215", 217: "AE217", 219: "AE219", 220.8: "AE220p8", 221: "AE221"}
FAM = {"Sc": ((215, 217, 219, 221, 223, 225, 227, 228.8), "Skarn-expressed, Skarn-supported, coupled"),
       "Cc": ((217, 221, 225, 228.8), "central Halvren anatomy, Skarn-supported, coupled"),
       "Ac": ((215, 217, 219, 220.8, 221), "Aelari-expressed, Aelari-supported, coupled"),
       "Ca": ((221,), "central Halvren anatomy, Aelari-supported, coupled"),
       "SAc": ((221, 225, 228.8), "Skarn + Aelari, Skarn stature support, coupled")}
for c, (hs, nm) in FAM.items():
    for h in hs:
        a = "HU%s%s" % (tg(h), c); s = "SK%s" % tg(h); ae = AEM.get(h); aem = ae or "AE221"
        passrow("A", "%g cm %s: not a matched-height Skarn duplicate (%s)" % (h, nm, s), a, s)
        if ae: passrow("A", "%g cm %s: not a matched-height Aelari duplicate (%s)" % (h, nm, ae), a, ae)
        else: passrow("A", "%g cm %s vs Aelari 221 - D1 ENDPOINT source-family diagnostic (never matched height)" % (h, nm), a, "AE221")
        srcs = [s, aem, "FN211", "SG208", "MF203", "VA203"]
        for k in CANON: spans.append({"code": "A", "check": "%g cm %s inside the boundary-stature span (%s + %s%s + nearest valid FN211 / SG208 / MF203 / VA203): %s" % (h, nm, s, aem, "" if ae else " [D1 endpoint]", k), "a": a, "srcs": srcs, "k": k})
        for k in [x for x in BODY if x not in CANON]: spans.append({"code": "A", "check": "%g cm %s vs the boundary-stature span (report): %s" % (h, nm, k.replace(T0, "")), "a": a, "srcs": srcs, "k": k, "report": True})
        for k in CANON: spans.append({"code": "A", "check": "%g cm %s vs the matched supporting-source span only (%s, %s; diagnostic source-relationship report): %s" % (h, nm, s, aem, k), "a": a, "srcs": [s, aem], "k": k, "report": True})
        sup = ae if c in ("Ac", "Ca") else s
        r("A", "%g cm %s: coupling does not copy the supporting source's lower-leg share (shin / leg below %s)" % (h, nm, sup), a, "<", sup, "shin_over_leg", "no source-body copying")
        r("A", "%g cm %s: lower-leg share not below the Halvren's accepted central-ceiling value HV213 (report; the coupling target)" % (h, nm), a, ">=", "HV213", "shin_over_leg", "", True)
        for k in (TB, TD, SJ, "torso_share", JP("knee"), JP("wrist")): r("K", "%g cm %s vs %s: %s (Skarn guard, report)" % (h, nm, s, k.replace(T0, "")), a, "<", s, k, "", True)
# O: coupling onset (k = 0 at 213 cm): the coupled family joins the uncoupled 213 cm body without a step
for a, b in (("HU215Cc", "HV213"), ("HU215Sc", "HU213S"), ("HU215Ac", "HU213A")):
    for k in ("torso_share", "leg_share", "arm_share", "shin_over_leg", "femur_over_leg", "forearm_over_arm", "HH_share", "neck_share", JP("knee"), JP("ankle")):
        mv.append({"code": "O", "kind": "L", "tol": 0.01, "a": a, "b": b, "k": k, "check": "onset %s vs %s (k = 0 at 213 cm): %s within 1 %%" % (a, b, k)})
# Z: coupling-strength sweep at 228.8 cm (Skarn-expressed): source protection at every strength; no source copying even at full strength (report)
for nid, kk in (("HU228p8S", 0.0), ("HU228p8Sk25", 0.25), ("HU228p8Sc", 0.4644), ("HU228p8SD", 0.5), ("HU228p8Sk75", 0.75), ("HU228p8Sk100", 1.0)):
    passrow("Z", "k = %.4g at 228.8 cm (%s): not a Skarn duplicate (SK228p8)%s" % (kk, nid, "" if kk <= 0.5 else " - beyond the rule (report)"), nid, "SK228p8", kk > 0.5)
    r("Z", "k = %.4g (%s): shin / leg vs SK228p8 (report)" % (kk, nid), nid, "<", "SK228p8", "shin_over_leg", "", True)
    for k in CANON: spans.append({"code": "Z", "check": "k = %.4g (%s) inside the boundary-stature span: %s (report)" % (kk, nid, k), "a": nid, "srcs": ["SK228p8", "AE221", "FN211", "SG208", "MF203", "VA203"], "k": k, "report": True})
# F / M: frames and composition at the final coupled endpoints
EP = {"HU228p8Sc": ("SK228p8", "AE221"), "HU221Ac": ("SK221", "AE221"), "HU228p8SAc": ("SK228p8", "AE221")}
for e, (s1, s2) in EP.items():
    for tag_, sgn in (("N", -1), ("B", 1)):
        x = e + "-" + tag_
        for k in (TB, SJ, sk("biacromial / stature"), sk("crest breadth / stature"), sk("hip-joint spacing / stature")):
            mv.append({"code": "F", "kind": "D", "sign": sgn, "a": x, "b": e, "k": k, "check": "%s %s breadth: %s by >= 1 %%" % (x, "reduces" if sgn < 0 else "increases", k.replace(T0, ""))})
        for k in ("stature (cm)", "torso_share", "leg_share", "arm_share", "forearm_over_arm", "shin_over_leg", "femur_over_leg", "HH_share", "hand_share", "neck_share"):
            mv.append({"code": "F", "kind": "L", "tol": 0.005, "a": x, "b": e, "k": k, "check": "%s keeps lengths / coupling (0.5 %%): %s" % (x, k)})
        for j in ("elbow", "wrist", "knee", "ankle"): mv.append({"code": "F", "kind": "L", "tol": 0.01, "a": x, "b": e, "k": JP(j), "check": "%s keeps joint scale: %s (1 %%)" % (x, JP(j))})
        passrow("F", "%s not a duplicate of %s" % (x, s1), x, s1)
        passrow("F", "%s not a duplicate of %s%s" % (x, s2, " (D1 endpoint)" if "228" in e else ""), x, s2)
        for k in CANON: spans.append({"code": "F", "check": "%s inside the boundary-stature span: %s" % (x, k), "a": x, "srcs": [s1, s2, "FN211", "SG208", "MF203", "VA203"], "k": k})
    for cs in ("LOWMUS", "HIMUS", "LOWFAT", "HIFAT"):
        x = "%s-%s" % (e, cs)
        inv.append({"code": "M", "check": "%s: composition does not redefine proportions or the coupling (within 1 %%)" % x, "a": x, "b": e, "keys": ["torso_share", "leg_share", "arm_share", "forearm_over_arm", "shin_over_leg", "femur_over_leg", "hand_share", "neck_share"]})
        if "228" in e: passrow("M", "%s not a duplicate of the same-composition SK228p8-%s" % (x, cs), x, "SK228p8-%s" % cs)
        else: passrow("M", "%s not a duplicate of the same-composition AE221-%s" % (x, cs), x, "AE221-%s" % cs)
        passrow("M", "%s vs reference-composition %s (report)" % (x, s1), x, s1, True)
        for k in CANON: spans.append({"code": "M", "check": "%s inside the boundary-stature span (reference-composition sources; report): %s" % (x, k), "a": x, "srcs": [s1, s2, "FN211", "SG208", "MF203", "VA203"], "k": k, "report": True})
for e in ("HU228p8Sc", "HU228p8SAc"):
    passrow("Q", "Q6 Broad %s vs Broad Skarn SKB228p8" % e, e + "-B", "SKB228p8")
    passrow("Q", "Q6 high-muscle %s vs high-muscle Skarn SK228p8-HIMUS" % e, e + "-HIMUS", "SK228p8-HIMUS")
for e in ("HU221Ac", "HU228p8Sc", "HU228p8SAc"):
    passrow("Q", "Q7 Narrow %s vs AE221%s" % (e, "" if "221" in e else " (D1 endpoint)"), e + "-N", "AE221")
    passrow("Q", "Q7 Narrow %s vs Narrow Aelari AEN221" % e, e + "-N", "AEN221")
    passrow("Q", "Q7 Narrow %s vs FN211 (tallest valid Fenn; report)" % e, e + "-N", "FN211", True)
passrow("Q", "Q7 low-fat HU221Ac vs AE221-LOWFAT", "HU221Ac-LOWFAT", "AE221-LOWFAT")
series = {"HV-Cc": ["HV190", "HV203", "HV213", "HU215Cc", "HU217Cc", "HU221Cc", "HU225Cc", "HU228p8Cc"],
          "HV-Sc": ["HU213S", "HU215Sc", "HU217Sc", "HU219Sc", "HU221Sc", "HU223Sc", "HU225Sc", "HU227Sc", "HU228p8Sc"],
          "HV-Ac": ["HU213A", "HU215Ac", "HU217Ac", "HU219Ac", "HU220p8Ac", "HU221Ac"], "HV-SAc": ["HU221SAc", "HU225SAc", "HU228p8SAc"],
          "Z-k": ["HU228p8S", "HU228p8Sk25", "HU228p8Sc", "HU228p8SD", "HU228p8Sk75", "HU228p8Sk100"],
          "SK": ["SK208", "SK215", "SK217", "SK219", "SK221", "SK223", "SK225", "SK227", "SK228p8"], "AE": ["AE211", "AE215", "AE217", "AE219", "AE220p8", "AE221"]}
json.dump({"rows": rows, "invariance": inv, "moves": mv, "spans": spans, "passing": passing, "toward": [], "series": series}, open(sys.argv[1], "w"), indent=1)
print(len(rows), "rows", len(inv), "invariance", len(mv), "moves", len(spans), "spans", len(passing), "passing")
