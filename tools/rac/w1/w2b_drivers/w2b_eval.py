# RAC W2B (Skarn boundary foundation): measurement table and checks for Skarn at 183 / 208 / 229 cm (both configurations), the Marchfolk
# overlap tests (190 cm equal height; 203 cm upper-overlap edge), the Skarn frames at 208 cm, composition invariance, named extremes SK-02 / 03 /
# 04 / 05 / 07 / 08 and the large-race bridge (Broad Skarn vs accepted minimum Gorrund GO-H208; ALPC-7 re-check).
# Routes: generator height macro re-solved from the accepted SK ARM (configuration 1) and from a configuration-2 SK at 208 cm (SK targets on the
# accepted MF-F-R base). Skeletal readings: CIB grids (t = 0 / 0.5 / 1.0). Joints: stature-scaled slab. Matched-stature joint comparisons use the
# generator adult allometry slopes with central controls. NON-CANON diagnostics throughout.
# Usage: python3 w2b_eval.py JBW.json  -> reviews/rac-w2b-sk-evidence/w2b.json
import sys, os, json
R = '/home/claude/wayfarer-design'; S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; W = S + '/w2b'; A2 = S + '/w2a'
EV = R + '/reviews/rac-w2b-sk-evidence'; os.makedirs(EV, exist_ok=True); BS = R + '/reviews/rac-w1i-evidence/skeletal'
JB = json.load(open(sys.argv[1])); AL = json.load(open(R + '/tools/rac/w1/native_short_allometry.json'))["slopes"]
G = lambda i, sid: (W + '/g/%s/skp' % i, sid)
B = {"SK-M183": (W + '/st/SKM183',) + G("SKM183", "MF-M-R"), "SK-M208": (S + '/w1f/final/SK', BS, 'SK'), "SK-M229": (W + '/st/SKM229',) + G("SKM229", "MF-M-R"),
     "SK-F183": (W + '/st/SKF183',) + G("SKF183", "MF-F-R"), "SK-F208": (W + '/st/SKF208',) + G("SKF208", "MF-F-R"), "SK-F229": (W + '/st/SKF229N-NAT',) + G("SKF229", "MF-F-R"),   # macro maximum (1.0) + native regional extension: generator bound
     "SK-M190": (W + '/st/SKM190',) + G("SKM190", "MF-M-R"), "SK-F190": (W + '/st/SKF190',) + G("SKF190", "MF-F-R"),
     "SK-M203": (W + '/st/SKM203',) + G("SKM203", "MF-M-R"), "SK-F203": (W + '/st/SKF203',) + G("SKF203", "MF-F-R"),
     "MF-M190": (W + '/st/MFM190K8',) + G("MFM190", "MF-M-R"), "MF-F190": (W + '/st/MFF190K3',) + G("MFF190", "MF-F-R"),   # W2A knee rule applied at 190 (trunk grid from the macro body)
     "MF-M190 macro only": (W + '/st/MFM190', None, None), "MF-F190 macro only": (W + '/st/MFF190', None, None),
     "MF-M203": (A2 + '/kp/MFM203K6', A2 + '/g/MFM203/skp', 'MF-M-R'), "MF-F203": (A2 + '/kp/MFF203K3', A2 + '/g/MFF203/skp', 'MF-F-R'),
     "MF-M173": (S + '/w1f/final/MF-M-R', BS, 'MF-M-R'), "MF-F173": (S + '/w1f/final/MF-F-R', BS, 'MF-F-R'),
     "SK-M Narrow": (W + '/fr/SKMNarrow',) + G("SKMNarrow", "MF-M-R"), "SK-M Broad": (W + '/fr/SKMBroad',) + G("SKMBroad", "MF-M-R"),
     "SK-F Narrow": (W + '/fr/SKFNarrow',) + G("SKFNarrow", "MF-F-R"), "SK-F Broad": (W + '/fr/SKFBroad',) + G("SKFBroad", "MF-F-R"),
     "SK W1 Broad (SKB208)": (W + '/ref/SKB208', BS, 'SKB208'), "GO-H208": (W + '/ref/GO-H208', S + '/w1g/true208/skp_GO-H208', 'GO-H208'),
     "SK-02": (W + '/nx/SK02',) + G("SK02", "MF-M-R"), "SK-04": (W + '/nx/SK04',) + G("SK04", "MF-M-R"),
     "SG": (S + '/w1f/final/SG', BS, 'SG')}
for c in ("M", "F"):
    for comp in ("LOWMUS", "HIMUS", "HIFAT", "HIBOTH"): B["SK-%s %s" % (c, comp)] = (W + '/comp/SK%s-%s' % (c, comp), None, None)
JK = {"MF-M190": "MFM190K8", "MF-F190": "MFF190K3", "MF-M190 macro only": "MFM190", "MF-F190 macro only": "MFF190", "SK-F229": "SKF229N-NAT", "SK-M208": "SK", "MF-M203": "MFM203K6", "MF-F203": "MFF203K3", "MF-M173": "MF-M-R", "MF-F173": "MF-F-R", "SK W1 Broad (SKB208)": "SKB208", "GO-H208": "GO-H208", "SG": "SG"}
def jkey(b): return JK.get(b, b.replace("SK-M", "SKM").replace("SK-F", "SKF").replace("MF-M", "MFM").replace("MF-F", "MFF").replace(" ", "").replace("SK-0", "SK0"))
def cls(op, va, vb):
    rel = abs(va - vb) / abs(vb) if vb else 1.0; holds = {">": va > vb, "<": va < vb, ">=": va >= vb, "<=": va <= vb}[op]
    if op in (">", "<"): return ("PASS" if rel >= 0.01 else "NOT DEMONSTRATED") if holds else "FAIL"
    return "PASS" if holds else ("MARGINAL" if rel < 0.01 else "FAIL")
V = {}
for b, (p, skd, sid) in B.items():
    if not os.path.exists(p + '_meas.json'): print('missing', b); continue
    c = json.load(open(p + '_meas.json'))["combined"]; r, m, s = c["ratio"], c["mean"], c["stature"]
    v = {"stature (cm)": s, "torso / stature": r["torso_share"], "neck / stature": r["neck_share"], "head height / stature": r["HH_share"], "arm / stature": r["arm_share"],
         "leg / stature": r["leg_share"], "upper arm / arm": r["upperarm_over_arm"], "forearm / arm": r["forearm_over_arm"], "femur / leg": r["femur_over_leg"],
         "hand / stature": r["hand_share"], "palm breadth / stature": m["palm_breadth"] / s, "foot / stature": r["foot_share"], "foot breadth / stature": m["foot_breadth"] / s,
         "skin thoracic breadth / stature": r["thorax_breadth_share"], "skin thoracic depth / stature": r["thorax_depth_share"], "shoulder-joint breadth / stature (skin)": r["shoulder_joint_share"]}
    jk = jkey(b)
    if jk in JB:
        for j in ("elbow", "wrist", "knee", "ankle"): v["%s breadth / stature (scaled slab)" % j] = JB[jk]["scaled"][j]
    if skd and os.path.exists(skd + '/t0.0/%s_meas.json' % sid):
        for t in ("0.0", "0.5", "1.0"):
            q = json.load(open(skd + '/t%s/%s_meas.json' % (t, sid)))["combined"]; qr = q["ratio"]; st = q["stature"]; b7, d7 = q["alpc_stations"]["S7"]
            for k, val in (("thoracic breadth / stature", qr["thorax_breadth_share"]), ("thoracic depth / stature", qr["thorax_depth_share"]), ("shoulder-joint breadth / stature", qr["shoulder_joint_share"]),
                           ("biacromial / stature", qr["biacromial_share"]), ("crest breadth / stature", qr["crest_share"]), ("AP pelvic depth / stature", qr["pelvic_depth_share"]),
                           ("pelvic vertical / stature", qr["pelvic_vertical_share"]), ("hip-joint spacing / stature", qr["hip_joint_breadth_share"]),
                           ("femoral S7 breadth / stature", b7 / st), ("femoral S7 depth / stature", d7 / st), ("crest / thoracic breadth", qr["pelvis_over_thorax_breadth"]),
                           ("thoracic depth / breadth", qr["thorax_d_over_b"]), ("shoulder-joint / thoracic breadth", qr["S1_over_S2_b"]), ("bitrochanteric / crest", qr["bitroch_over_crest"])):
                v["%s [t=%s]" % (k, t)] = val
            for k in ("S3_over_S2_b", "S4_over_S2_b", "S3_over_S2_d", "S4_over_S2_d", "S5_over_S2_b", "S6_over_S2_b", "pelvic_depth_over_thorax_depth"):
                v["ALPC %s [t=%s]" % (k, t)] = qr[k]
    V[b] = v
C = []
def add(code, chk, va, op, vb, a, b, note="", report=False):
    C.append({"code": code, "check": chk + (" — REPORT ONLY" if report else ""), "a": a, "b": b, "va": va, "op": op, "vb": vb, "result": "REPORT" if report else cls(op, va, vb), "note": note})
def adj(val, frm, to, j):      # carry a joint / stature value from stature frm to stature to by the generator adult allometry slope
    return val * (to / frm) ** (AL[j] - 1)
# A. stature foundation
for c in ("M", "F"):
    lo, ce, hi = "SK-%s183" % c, "SK-%s208" % c, "SK-%s229" % c
    if not all(x in V for x in (lo, ce, hi)): continue
    add("U", "%s head share allometric: 183 > 208" % c, V[lo]["head height / stature"], ">", V[ce]["head height / stature"], lo, ce)
    add("U", "%s head share allometric: 229 < 208" % c, V[hi]["head height / stature"], "<", V[ce]["head height / stature"], hi, ce)
    for k in V[ce]:
        if k.startswith("stature") or k.startswith("ALPC") or k not in V[lo] or k not in V[hi]: continue
        a, b_, d = V[lo][k], V[ce][k], V[hi][k]
        ok = (a <= b_ <= d) or (a >= b_ >= d) or min(abs(a / b_ - 1), abs(d / b_ - 1)) < 0.01
        C.append({"code": "C", "check": "%s continuity 183 -> 208 -> 229: %s" % (c, k), "a": lo, "b": hi, "va": [a, b_, d], "op": "trend", "vb": None,
                  "result": "PASS" if ok else "NON-MONOTONIC (>= 1 % reversal)", "note": "%+.1f %% / %+.1f %% vs 208" % (100 * (a / b_ - 1), 100 * (d / b_ - 1))})
    for x in (lo, hi):
        for j in ("elbow", "wrist", "knee", "ankle"):
            k = "%s breadth / stature (scaled slab)" % j
            if k in V[x] and k in V[ce]:
                e = adj(V[ce][k], V[ce]["stature (cm)"], V[x]["stature (cm)"], j); d = V[x][k] / e - 1
                C.append({"code": "K", "check": "%s %s vs the generator allometric expectation from the 208 cm anchor" % (x, k), "a": x, "b": "expected", "va": V[x][k], "op": "~", "vb": e,
                          "result": "PASS" if abs(d) < 0.03 else "REPORT (>= 3 % off slope)", "note": "%+.1f %%" % (100 * d)})
# B. Marchfolk overlap (equal height): Skarn directions SKARN L17-24, v1.1 §1
DIR = [("thoracic depth / stature [t=0.0]", ">"), ("thoracic breadth / stature [t=0.0]", ">"), ("shoulder-joint breadth / stature [t=0.0]", ">"), ("crest breadth / stature [t=0.0]", ">"),
       ("AP pelvic depth / stature [t=0.0]", ">"), ("femoral S7 breadth / stature [t=0.0]", ">"), ("femoral S7 depth / stature [t=0.0]", ">"), ("elbow breadth / stature (scaled slab)", ">"),
       ("wrist breadth / stature (scaled slab)", ">"), ("knee breadth / stature (scaled slab)", ">"), ("ankle breadth / stature (scaled slab)", ">"), ("hand / stature", ">"),
       ("palm breadth / stature", ">"), ("foot / stature", ">"), ("foot breadth / stature", ">")]
REP = [("torso / stature", ">"), ("leg / stature", "<"), ("thoracic depth / breadth [t=0.0]", ">"), ("neck / stature", "vs")]
for c in ("M", "F"):
    for h in ("190", "203"):
        a, b = "SK-%s%s" % (c, h), "MF-%s%s" % (c, h)
        if a not in V or b not in V: continue
        for k, op in DIR:
            if k in V[a] and k in V[b]: add("O", "%s cm %s: Skarn %s Marchfolk: %s" % (h, c, op, k), V[a][k], op, V[b][k], a, b, "%+.1f %%" % (100 * (V[a][k] / V[b][k] - 1)))
        for k, op in REP:
            if k in V[a] and k in V[b]: add("O", "%s cm %s: %s (tendency only)" % (h, c, k), V[a][k], op if op != "vs" else ">", V[b][k], a, b, "%+.1f %%" % (100 * (V[a][k] / V[b][k] - 1)), report=True)
# canonical validation pair (SKARN v1.0 §10): Marchfolk maximum (203) vs Skarn minimum (183), stature-normalized readings; joints carried to 183 cm
for c in ("M", "F"):
    a, b = "SK-%s183" % c, "MF-%s203" % c
    if a in V and b in V:
        for k, op in DIR:
            if k not in V[a] or k not in V[b]: continue
            vb = adj(V[b][k], V[b]["stature (cm)"], V[a]["stature (cm)"], k.split()[0]) if "scaled slab" in k else V[b][k]
            add("P", "canonical pair %s: SK 183 %s MF 203: %s" % (c, op, k), V[a][k], op, vb, a, b + ("@183" if "scaled slab" in k else ""), "%+.1f %%" % (100 * (V[a][k] / vb - 1)))
# C. frames at 208
DOM = ["shoulder-joint breadth / stature [t=0.0]", "thoracic breadth / stature [t=0.0]", "thoracic depth / stature [t=0.0]", "crest breadth / stature [t=0.0]", "hip-joint spacing / stature [t=0.0]",
       "femoral S7 breadth / stature [t=0.0]", "femoral S7 depth / stature [t=0.0]", "knee breadth / stature (scaled slab)", "wrist breadth / stature (scaled slab)"]
for c in ("M", "F"):
    n, ce, br = "SK-%s Narrow" % c, "SK-%s208" % c, "SK-%s Broad" % c
    if not all(x in V for x in (n, ce, br)): continue
    for k in DOM:
        if k not in V[n] or k not in V[ce]: continue
        for x, sg in ((br, 1), (n, -1)):
            d = V[x][k] / V[ce][k] - 1
            C.append({"code": "D", "check": "%s moves %s Balanced by >= 1 %%: %s" % (x, "above" if sg > 0 else "below", k), "a": x, "b": ce, "va": V[x][k], "op": ">" if sg > 0 else "<", "vb": V[ce][k],
                      "result": "PASS" if sg * d >= 0.01 else "FAIL", "note": "%+.1f %%" % (100 * d)})
    for k in ("stature (cm)", "torso / stature", "leg / stature", "arm / stature", "head height / stature"):
        for x in (n, br):
            d = V[x][k] / V[ce][k] - 1
            C.append({"code": "L", "check": "%s unchanged vs Balanced (0.5 %%): %s" % (x, k), "a": x, "b": ce, "va": V[x][k], "op": "~", "vb": V[ce][k], "result": "PASS" if abs(d) < 0.005 else "FAIL", "note": "%+.2f %%" % (100 * d)})
    # Narrow stays Skarn: vs Marchfolk at the overlap edge (203) carried to 208 by allometry for joints; trunk shares compared directly
    mf = "MF-%s203" % c
    FX = json.load(open(R + '/reviews/rac-w2a1-mf-frame-evidence/frames_X.json'))["values"]      # accepted W2A1 Marchfolk frames (173 cm)
    if mf in V:
        for x, fr in ((n, "Narrow"), (br, "Broad")):
            for k, op in DIR[:7] + DIR[11:]:
                if k not in V[x] or k not in V[mf]: continue
                fk = FX.get("%s %s" % (c, fr), {}); fb = FX.get("%s Balanced" % c, {})
                ratio = fk[k] / fb[k] if (k in fk and k in fb) else 1.0
                vb = V[mf][k] * ratio      # Marchfolk at the 203 cm edge carried to the same frame by the accepted Marchfolk frame ratio (frame-matched pair, SKARN v1.0 §10)
                add("N", "%s stays Skarn: %s %s frame-matched MF %s %s (203 cm edge)" % (x, k, op, c, fr), V[x][k], op, vb, x, mf + " " + fr, "MF frame ratio %.3f; raw vs Balanced MF %+.1f %%" % (ratio, 100 * (V[x][k] / V[mf][k] - 1)))
        for j in ("elbow", "wrist", "knee", "ankle"):
            k = "%s breadth / stature (scaled slab)" % j
            if k in V[n] and k in V[mf]:
                e = adj(V[mf][k], V[mf]["stature (cm)"], V[n]["stature (cm)"], j)
                add("N", "%s stays Skarn: %s > MF %s carried to 208 cm" % (n, k, c), V[n][k], ">", e, n, mf + "@208", "Balanced control %+.1f %%" % (100 * (V[ce][k] / e - 1)))
    if c == "M" and "SG" in V:
        for k, op in (("thoracic depth / stature [t=0.0]", ">"), ("thoracic breadth / stature [t=0.0]", ">"), ("leg / stature", "<")):
            if k not in V[n] or k not in V["SG"]: continue
            fk, fb = FX.get("M Narrow", {}), FX.get("M Balanced", {})
            ratio = fk[k] / fb[k] if (k in fk and k in fb) else 1.0
            sl = {"thoracic breadth / stature [t=0.0]": AL["thorax_b"], "thoracic depth / stature [t=0.0]": AL["thorax_d"]}.get(k)
            st = (V[n]["stature (cm)"] / V["SG"]["stature (cm)"]) ** (sl - 1) if sl else 1.0     # SG (178 cm) carried to 208 cm by the generator allometry slope
            add("N", "%s not Sagekin-like: %s %s SG carried to Narrow (human frame ratio) and to 208 cm (allometry)" % (n, k, op), V[n][k], op, V["SG"][k] * ratio * st, n, "SG Narrow@208 (est.)",
                "frame ratio %.3f, stature factor %.3f; raw Balanced control %+.1f %%" % (ratio, st, 100 * (V[ce][k] / V["SG"][k] - 1)))
    # Broad stays human Skarn, not Gorrund (configuration 1 vs accepted GO-H208; configuration 2 report)
    rep = c == "F"
    # scored carriers are the authored Gorrund-vs-Skarn ones (GORRUND L201 GO-G7, L292): thoracic depth relative to stature and to breadth, plus ALPC-7
    # below; limb / joint / pelvic proportional separation is undetermined by design (AD-4), so those rows are reported only
    for k in ("thoracic depth / stature [t=0.0]", "thoracic depth / breadth [t=0.0]", "crest breadth / stature [t=0.0]", "AP pelvic depth / stature [t=0.0]", "femoral S7 breadth / stature [t=0.0]",
              "femoral S7 depth / stature [t=0.0]", "wrist breadth / stature (scaled slab)", "knee breadth / stature (scaled slab)", "hand / stature", "foot / stature"):
        if k in V[br] and "GO-H208" in V and k in V["GO-H208"]:
            carrier = k in ("thoracic depth / stature [t=0.0]", "thoracic depth / breadth [t=0.0]")
            add("G", "%s not Gorrund: %s < GO-H208%s" % (br, k, "" if carrier else " (AD-4: not an authored carrier)"), V[br][k], "<", V["GO-H208"][k], br, "GO-H208",
                "configuration 2 vs configuration-1 Gorrund" if rep else "", report=rep or not carrier)
    for t in ("0.0", "0.5", "1.0"):
        for k in ("S3_over_S2_b", "S4_over_S2_b", "S3_over_S2_d", "S4_over_S2_d", "S5_over_S2_b", "S6_over_S2_b", "pelvic_depth_over_thorax_depth"):
            kk = "ALPC %s [t=%s]" % (k, t)
            if c == "M" and kk in V.get(br, {}) and kk in V.get("GO-H208", {}):
                add("A7", "accepted W1 ALPC-7 re-check: GO-H208 > new Broad Skarn 208: %s t=%s" % (k, t), V["GO-H208"][kk], ">", V[br][kk], "GO-H208", br)
            if c == "M" and kk in V.get("SK W1 Broad (SKB208)", {}) and kk in V.get("GO-H208", {}) and t == "0.0":
                add("A7", "W1 reference: GO-H208 > W1 Broad Skarn SKB208: %s t=0" % k, V["GO-H208"][kk], ">", V["SK W1 Broad (SKB208)"][kk], "GO-H208", "SKB208", report=True)
# D. composition invariance
for c in ("M", "F"):
    ce = "SK-%s208" % c
    for comp in ("LOWMUS", "HIMUS", "HIFAT", "HIBOTH"):
        x = "SK-%s %s" % (c, comp)
        if x not in V or ce not in V: continue
        moved = [k for k in ("torso / stature", "leg / stature", "arm / stature", "head height / stature") if abs(V[x][k] / V[ce][k] - 1) >= 0.01]
        C.append({"code": "M", "check": "%s: composition does not redefine anatomy (torso, leg, arm, head shares within 1 %%)" % x, "a": x, "b": ce, "va": len(moved), "op": "=", "vb": 0,
                  "result": "PASS" if not moved else "FAIL", "note": "; ".join("%s %+.1f %%" % (k, 100 * (V[x][k] / V[ce][k] - 1)) for k in moved) or "none"})
# E. named extremes
if "SK-02" in V and "MF-M190" in V:
    for k, op in DIR[:7] + DIR[11:]:
        if k in V["SK-02"] and k in V["MF-M190"]: add("X", "SK-02 (183 cm Narrow low muscle) vs MF 190 (Balanced): %s %s" % (k, op), V["SK-02"][k], op, V["MF-M190"][k], "SK-02", "MF-M190", report=True)
if "SK-04" in V and "SK-M208" in V:
    for k in ("leg / stature", "torso / stature", "femur / leg", "thoracic depth / stature [t=0.0]"):
        if k in V["SK-04"]: add("X", "SK-04 long-legged vs Balanced SK: %s" % k, V["SK-04"][k], "vs", V["SK-M208"][k], "SK-04", "SK-M208", "%+.1f %%" % (100 * (V["SK-04"][k] / V["SK-M208"][k] - 1)), report=True)
    for k, op in (("leg / stature", "<="), ("thoracic depth / stature [t=0.0]", ">")):
        if k in V["SK-04"] and "MF-M203" in V: add("X", "SK-04 stays Skarn and inside the human family: %s %s MF 203" % (k, op), V["SK-04"][k], op, V["MF-M203"][k], "SK-04", "MF-M203")
out = {"values": V, "checks": C, "envelope_candidates": {}}
six = [x for x in ("SK-M183", "SK-M208", "SK-M229", "SK-F183", "SK-F208", "SK-F229") if x in V]
for k in V.get("SK-M208", {}):
    vals = [(V[x][k], x) for x in six if k in V[x]]
    if len(vals) == len(six) and not k.startswith("ALPC"): out["envelope_candidates"][k] = {"min": min(vals)[0], "min_body": min(vals)[1], "max": max(vals)[0], "max_body": max(vals)[1], "status": "NON-CANON diagnostic candidate"}
json.dump(out, open(EV + '/w2b.json', 'w'), indent=1, default=float)
for c in C:
    if c["result"] not in ("PASS", "REPORT"): print(c["code"], c["check"][:100], c["note"][:40], c["result"])
print(len(C), 'checks;', sum(c["result"] == "PASS" for c in C), 'PASS;', sum(c["result"].startswith("REPORT") for c in C), 'REPORT')
