# RAC W2A1 (Marchfolk frame closure): Narrow / Balanced / Broad at the accepted 173 cm anchors, both configurations. Skeletal-layer readings
# (CIB stations, t = 0 / 0.5 / 1.0) for frame decisions; skin readings as diagnostics. Checks (order W2A1 items 1-10; MARCHFOLK L25, v1.1 §2):
#   D  every canonical frame domain moves in the frame's direction by >= 2 % (twice the AD-G10 1 % resolution): shoulder-joint breadth, skeletal
#      thoracic breadth, skeletal thoracic depth, crest breadth, hip-joint spacing, joint scale (mean of four joints), femoral S7 section
#   L  stature, segment lengths, head and composition inputs unchanged (within 0.5 %)
#   H  coherent transitions: inter-domain ratios (crest / thorax, shoulder / thorax, hip spacing / crest, bitrochanteric / crest, thoracic depth /
#      breadth) stay inside the span of the accepted human references (MF config 1 and 2, SK, SG) +/- 1 % — no independently scaled part
#   S  Broad not Skarn-like (config 1 vs accepted Skarn; config 2 report)
#   E  Narrow not elf- / Sagekin-like (config 1 vs FN, AE, SG; joints at matched stature by generator allometry, with central control)
# Usage: python3 w2a1_eval.py SET JBW.json   (SET = frame-set tag, e.g. A)  -> reviews/rac-w2a1-mf-frame-evidence/frames_<SET>.json
import sys, os, json
R = '/home/claude/wayfarer-design'; S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; W = S + '/w2a1'
EV = R + '/reviews/rac-w2a1-mf-frame-evidence'; os.makedirs(EV, exist_ok=True); BS = R + '/reviews/rac-w1i-evidence/skeletal'
SET, JB = sys.argv[1], json.load(open(sys.argv[2]))
AL = json.load(open(R + '/tools/rac/w1/native_short_allometry.json'))["slopes"]
B = {"M Narrow": (W + '/p/MN%s' % SET, W + '/g/MN%s/skp' % SET, 'MF-M-R', 'MN%s' % SET), "M Balanced": (S + '/w1f/final/MF-M-R', BS, 'MF-M-R', 'MF-M-R'),
     "M Broad": (W + '/p/MB%s' % SET, W + '/g/MB%s/skp' % SET, 'MF-M-R', 'MB%s' % SET),
     "F Narrow": (W + '/p/FN%s' % SET, W + '/g/FN%s/skp' % SET, 'MF-F-R', 'FN%s' % SET), "F Balanced": (S + '/w1f/final/MF-F-R', BS, 'MF-F-R', 'MF-F-R'),
     "F Broad": (W + '/p/FB%s' % SET, W + '/g/FB%s/skp' % SET, 'MF-F-R', 'FB%s' % SET),
     "SK": (S + '/w1f/final/SK', BS, 'SK', 'SK'), "SG": (S + '/w1f/final/SG', BS, 'SG', 'SG'), "FN": (S + '/w1p/cand/FNL4', S + '/w1p/fnl4/skp', 'FN', 'FN'),
     "AE": (S + '/w1m/legs/AEL1', S + '/w1m/ael1/skp', 'AE', 'AE')}
def cls(op, va, vb):
    rel = abs(va - vb) / abs(vb); holds = {">": va > vb, "<": va < vb, ">=": va >= vb, "<=": va <= vb}[op]
    if op in (">", "<"): return ("PASS" if rel >= 0.01 else "NOT DEMONSTRATED") if holds else "FAIL"
    return "PASS" if holds else ("MARGINAL" if rel < 0.01 else "FAIL")
V = {}
for b, (p, skd, sid, jk) in B.items():
    if not os.path.exists(p + '_meas.json'): print('missing', b); continue
    c = json.load(open(p + '_meas.json'))["combined"]; r = c["ratio"]
    v = {"stature (cm)": c["stature"], "torso / stature": r["torso_share"], "leg / stature": r["leg_share"], "arm / stature": r["arm_share"], "upper arm / arm": r["upperarm_over_arm"],
         "femur / leg": r["femur_over_leg"], "head height / stature": r["HH_share"], "hand / stature": r["hand_share"], "foot / stature": r["foot_share"],
         "skin thoracic breadth / stature": r["thorax_breadth_share"], "skin thoracic depth / stature": r["thorax_depth_share"], "skin waist interval / torso": r["waist_interval_over_torso"]}
    if os.path.exists(skd + '/t0.0/%s_meas.json' % sid):
        for t in ("0.0", "0.5", "1.0"):
            q = json.load(open(skd + '/t%s/%s_meas.json' % (t, sid)))["combined"]; qr = q["ratio"]; st = q["stature"]; b7, d7 = q["alpc_stations"]["S7"]; ex = q.get("extra", {})
            for k, val in (("shoulder-joint breadth / stature", qr["shoulder_joint_share"]), ("biacromial / stature", qr["biacromial_share"]),
                           ("thoracic breadth / stature", qr["thorax_breadth_share"]), ("thoracic depth / stature", qr["thorax_depth_share"]), ("crest breadth / stature", qr["crest_share"]),
                           ("hip-joint spacing / stature", qr["hip_joint_breadth_share"]), ("AP pelvic depth / stature", qr["pelvic_depth_share"]),
                           ("femoral S7 breadth / stature", b7 / st), ("femoral S7 depth / stature", d7 / st), ("crest / thoracic breadth", qr["pelvis_over_thorax_breadth"]),
                           ("shoulder-joint / thoracic breadth", qr["S1_over_S2_b"]), ("hip spacing / crest", qr["hip_joint_breadth_share"] / qr["crest_share"]),
                           ("bitrochanteric / crest", qr["bitroch_over_crest"]), ("thoracic depth / breadth", qr["thorax_d_over_b"])):
                v["%s [t=%s]" % (k, t)] = val
    if jk in JB:
        for j in ("elbow", "wrist", "knee", "ankle"): v["%s breadth / stature (scaled slab)" % j] = JB[jk]["scaled"][j]
        v["joint scale (mean of four, / stature)"] = sum(JB[jk]["scaled"][j] for j in ("elbow", "wrist", "knee", "ankle")) / 4
    V[b] = v
C = []
def add(code, chk, va, op, vb, a, b, note="", report=False):
    C.append({"code": code, "check": chk + (" — REPORT ONLY" if report else ""), "a": a, "b": b, "va": va, "op": op, "vb": vb, "result": "REPORT" if report else cls(op, va, vb), "note": note})
DOM = ["shoulder-joint breadth / stature [t=0.0]", "thoracic breadth / stature [t=0.0]", "thoracic depth / stature [t=0.0]", "crest breadth / stature [t=0.0]",
       "hip-joint spacing / stature [t=0.0]", "joint scale (mean of four, / stature)", "femoral S7 breadth / stature [t=0.0]", "femoral S7 depth / stature [t=0.0]"]
for c in ("M", "F"):
    n, ce, b = c + " Narrow", c + " Balanced", c + " Broad"
    if not all(x in V for x in (n, ce, b)): continue
    for k in DOM:
        if k not in V[n] or k not in V[ce]: continue
        for x, sg in ((b, 1), (n, -1)):
            d = V[x][k] / V[ce][k] - 1
            C.append({"code": "D", "check": "%s moves %s Balanced by >= 2 %%: %s" % (x, "above" if sg > 0 else "below", k), "a": x, "b": ce, "va": V[x][k], "op": ">" if sg > 0 else "<",
                      "vb": V[ce][k], "result": "PASS" if sg * d >= 0.02 else ("NOT DEMONSTRATED" if sg * d > 0 else "FAIL"), "note": "%+.1f %%" % (100 * d)})
    for k in ("stature (cm)", "torso / stature", "leg / stature", "arm / stature", "upper arm / arm", "femur / leg", "head height / stature"):
        for x in (n, b):
            d = V[x][k] / V[ce][k] - 1
            C.append({"code": "L", "check": "%s unchanged vs Balanced (within 0.5 %%): %s" % (x, k), "a": x, "b": ce, "va": V[x][k], "op": "~", "vb": V[ce][k], "result": "PASS" if abs(d) < 0.005 else "FAIL", "note": "%+.2f %%" % (100 * d)})
    HUM = ["MF-M-R", "MF-F-R", "SK", "SG"]
    for k in ("crest / thoracic breadth [t=0.0]", "shoulder-joint / thoracic breadth [t=0.0]", "hip spacing / crest [t=0.0]", "bitrochanteric / crest [t=0.0]", "thoracic depth / breadth [t=0.0]"):
        ref = [V[x][k] for x in ("M Balanced", "F Balanced", "SK", "SG") if k in V.get(x, {})]
        lo, hi = min(ref) * 0.99, max(ref) * 1.01
        for x in (n, b):
            C.append({"code": "H", "check": "%s coherent transition: %s inside the human-reference span +/- 1 %%" % (x, k), "a": x, "b": "MF1/MF2/SK/SG", "va": V[x][k], "op": "in",
                      "vb": [lo, hi], "result": "PASS" if lo <= V[x][k] <= hi else "FAIL", "note": "Balanced %.4f" % V[ce][k]})
    rep = c == "F"
    for k in ("thoracic depth / stature [t=0.0]", "shoulder-joint breadth / stature [t=0.0]", "femoral S7 depth / stature [t=0.0]", "wrist breadth / stature (scaled slab)",
              "knee breadth / stature (scaled slab)", "thoracic depth / breadth [t=0.0]"):
        if k in V[b] and k in V["SK"]:
            j = k.split()[0]
            vb = V["SK"][k] * ((V[b]["stature (cm)"] / V["SK"]["stature (cm)"]) ** (AL[j] - 1) if j in ("wrist", "knee") else 1.0)   # joints: Skarn carried to 173 cm by generator allometry
            add("S", "%s not Skarn-like: %s < SK%s" % (b, k, " at matched stature" if j in ("wrist", "knee") else ""), V[b][k], "<", vb, b, "SK", "configuration 2 vs configuration-1 Skarn" if rep else "", report=rep)
    SL = {"elbow": AL["elbow"], "wrist": AL["wrist"], "knee": AL["knee"]}
    if "SG" in V:
        for k in ("leg / stature", "upper arm / arm"):
            ctl = V[ce][k] / V["SG"][k] - 1
            add("E", "%s not Sagekin-like (linearity is lengths, which frames do not touch): %s vs SG" % (n, k), V[n][k], "<" if k == "leg / stature" else ">", V["SG"][k], n, "SG",
                "central control %+.1f %%" % (100 * ctl), report=rep or abs(ctl) < 0.01)
    for e in ("FN", "AE"):
        for k in ("thoracic depth / stature [t=0.0]", "thoracic depth / breadth [t=0.0]"):
            if k in V[n] and k in V[e]:
                ctl = V[ce][k] / V[e][k] - 1
                add("E", "%s not %s-like: %s > %s" % (n, e, k, e), V[n][k], ">", V[e][k], n, e, "central control %+.1f %%%s" % (100 * ctl, "; configuration 2 vs configuration-1 reference" if rep else ""),
                    report=rep or ctl < 0.01)
        for j, sl in SL.items():
            k = "%s breadth / stature (scaled slab)" % j
            if k not in V[n] or k not in V[e]: continue
            adj = V[e][k] * (V[n]["stature (cm)"] / V[e]["stature (cm)"]) ** (sl - 1)
            ctl = V[ce][k] / adj - 1
            add("E", "%s not %s-like: %s > %s at matched stature" % (n, e, k, e), V[n][k], ">", adj, n, e + "@173", "central control %+.1f %%%s" % (100 * ctl, "; configuration 2 vs configuration-1 reference" if rep else ""),
                report=rep or ctl < 0.01)
out = {"set": SET, "values": V, "checks": C}
json.dump(out, open(EV + '/frames_%s.json' % SET, 'w'), indent=1, default=float)
for c in C:
    if c["result"] not in ("PASS", "REPORT"): print(c["code"], c["check"][:96], c["note"][:40], c["result"])
print(SET, len(C), 'checks;', sum(c["result"] == "PASS" for c in C), 'PASS;', sum(c["result"] == "REPORT" for c in C), 'REPORT')
