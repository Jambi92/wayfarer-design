# RAC W2A (Marchfolk boundary foundation, RM-UB-07): measurement table and checks for Marchfolk at 147 / 173 / 203 cm in both ordinary
# human sex-related configurations (MF-M-R = configuration 1, MF-F-R = configuration 2).
# Routes: 203 cm = generator height macro re-solved (MPFB adult allometry, valid >= ~159 cm); 147 cm = native short-adult regional route
# (native_short.py; the generator macro below ~159 cm has an implausible femur and is excluded, native_short_allometry.json); 173 cm = accepted
# W1 ARMs. No uniform scaling. Skeletal pelvic / thoracic / femoral readings from CIB grids (t = 0, 0.5, 1.0). Joint readings: stature-scaled slab.
# Checks (order W2A items 2-3; MARCHFOLK L19-21, L64, L249; RAC-04 §2.2):
#   U  not uniformly scaled (head share allometric: 147 > 173 > 203; at least one body share departs from the central body by >= 1 %)
#   C  continuity 147 -> 173 -> 203 (monotonic or flat within 1 % per reading; non-monotonic readings reported)
#   J  not juvenile at 147 (vs a 147 cm generator human-child proxy, age ~11 y; head share, face, waist, pelvis) — report + head share < child
#   G  not giant-like / Skarn-like at 203 (structural readings stay below accepted Skarn: thoracic depth, wrist, knee, shoulder-joint breadth / stature)
#   E  not elf-like at 203 (joint presence stays above accepted Aelari and Fenn: elbow, wrist, knee / stature; thoracic breadth > AE)
#   P  segment plausibility (femur / tibia ratio within the adult range of the accepted bodies)
# Usage: python3 w2a_eval.py JBW.json  -> reviews/rac-w2a-mf-evidence/boundary.json
import sys, os, json
R = '/home/claude/wayfarer-design'; S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; W = S + '/w2a'
EV = R + '/reviews/rac-w2a-mf-evidence'; os.makedirs(EV, exist_ok=True); BS = R + '/reviews/rac-w1i-evidence/skeletal'
JB = json.load(open(sys.argv[1]))
B = {"M147": (W + '/st/MFM147-NAT', W + '/g/MFM147/skp', 'MF-M-R'), "M173": (S + '/w1f/final/MF-M-R', BS, 'MF-M-R'), "M203": (W + '/kp/MFM203K6', W + '/g/MFM203/skp', 'MF-M-R'),
     "F147": (W + '/st/MFF147B-NAT', W + '/g/MFF147B/skp', 'MF-F-R'), "F173": (S + '/w1f/final/MF-F-R', BS, 'MF-F-R'), "F203": (W + '/kp/MFF203K3', W + '/g/MFF203/skp', 'MF-F-R'),
     "SK": (S + '/w1f/final/SK', BS, 'SK'), "AE": (S + '/w1m/legs/AEL1', S + '/w1m/ael1/skp', 'AE'), "FN": (S + '/w1p/cand/FNL4', S + '/w1p/fnl4/skp', 'FN'),
     "CHILD147": (W + '/child/CHILD11', None, None), "M203N": (W + '/st/MFM203N-NAT', None, None), "F203N": (W + '/st/MFF203N-NAT', None, None), "M147X": (W + '/st/MFM147X', None, None),
     "M203G": (W + '/st/MFM203', None, None), "F203G": (W + '/st/MFF203', None, None), "F147A": (W + '/st/MFF147-NAT', None, None), "F203NB": (W + '/st/MFF203NB-NAT', None, None)}
# W2A boundary construction (route rule): 147 cm = native regional route from each configuration's accepted base macro (MF-M-R 0.5, MF-F-R 0.606);
# 203 cm = generator height macro + knee-circ-incr restoring knee breadth / stature to the generator's own adult allometric slope from the accepted
# central body (M 0.6, F 0.3; the macro alone drops the knee 9-16 % below that slope). Skeletal trunk readings at 203 cm come from the macro grids
# (the knee target does not touch the trunk). Route-comparison bodies: M203G / F203G (macro only), F147A (female native from base macro 0.5),
# M203N / F203NB (native route at 203), M147X (macro at 147, excluded: implausible femur).
def cls(op, va, vb):
    rel = abs(va - vb) / abs(vb) if vb else 1.0; holds = {">": va > vb, "<": va < vb, ">=": va >= vb, "<=": va <= vb}[op]
    if op in (">", "<"): return ("PASS" if rel >= 0.01 else "NOT DEMONSTRATED") if holds else "FAIL"
    return "PASS" if holds else ("MARGINAL" if rel < 0.01 else "FAIL")
M, K = {}, {}
for b, (p, skd, sid) in B.items():
    if not os.path.exists(p + '_meas.json'): print('missing', b); continue
    c = json.load(open(p + '_meas.json'))["combined"]; r, m, s = c["ratio"], c["mean"], c["stature"]
    v = {"stature (cm)": s, "torso / stature": r["torso_share"], "neck / stature": r["neck_share"], "head height / stature": r["HH_share"], "arm / stature": r["arm_share"],
         "leg / stature": r["leg_share"], "upper arm / arm": r["upperarm_over_arm"], "forearm / arm": r["forearm_over_arm"], "hand / arm": r["hand_over_arm"],
         "femur / leg": r["femur_over_leg"], "lower leg / leg": r["shin_over_leg"], "hand / stature": r["hand_share"], "palm breadth / stature": m["palm_breadth"] / s,
         "finger / palm": r["finger_over_palm"], "foot / stature": r["foot_share"], "foot breadth / stature": m["foot_breadth"] / s,
         "thoracic breadth / stature (skin)": r["thorax_breadth_share"], "thoracic depth / stature (skin)": r["thorax_depth_share"],
         "shoulder-joint breadth / stature": r["shoulder_joint_share"], "waist interval / torso": r["waist_interval_over_torso"], "face vertical / bizygomatic FVB": c["cranio"]["FVB"],
         "crest / thoracic breadth (skin)": r["pelvis_over_thorax_breadth"], "femur / tibia (plausibility)": m["thigh"] / m["shin"]}
    jk = {"M147": "MFM147-NAT", "M173": "MF-M-R", "M203": "MFM203K6", "F147": "MFF147B-NAT", "F173": "MF-F-R", "F203": "MFF203K3", "SK": "SK", "AE": "AE", "FN": "FN", "CHILD147": "CHILD11",
          "M203N": "MFM203N-NAT", "F203N": "MFF203N-NAT", "M147X": "MFM147X", "M203G": "MFM203", "F203G": "MFF203", "F147A": "MFF147-NAT", "F203NB": "MFF203NB-NAT"}[b]
    if jk in JB:
        for j in ("elbow", "wrist", "knee", "ankle"): v["%s breadth / stature (scaled slab)" % j] = JB[jk]["scaled"][j]
    if skd and os.path.exists(skd + '/t0.0/%s_meas.json' % sid):
        for t in ("0.0", "0.5", "1.0"):
            q = json.load(open(skd + '/t%s/%s_meas.json' % (t, sid)))["combined"]; qr = q["ratio"]; b7, d7 = q["alpc_stations"]["S7"]
            for k, val in (("skeletal thoracic breadth / stature", qr["thorax_breadth_share"]), ("skeletal thoracic depth / stature", qr["thorax_depth_share"]),
                           ("skeletal crest breadth / stature", qr["crest_share"]), ("skeletal AP pelvic depth / stature", qr["pelvic_depth_share"]),
                           ("skeletal pelvic vertical / crest", qr["pelvic_vertical_over_crest"]), ("skeletal hip-joint spacing / stature", qr["hip_joint_breadth_share"]),
                           ("skeletal crest / thoracic breadth", qr["pelvis_over_thorax_breadth"]), ("skeletal bitrochanteric / crest", qr["bitroch_over_crest"]),
                           ("skeletal pelvic vertical / stature", qr["pelvic_vertical_share"]), ("femoral S7 breadth / stature", b7 / q["stature"]), ("femoral S7 depth / stature", d7 / q["stature"])):
                v["%s [t=%s]" % (k, t)] = val
    M[b] = v
out = {"values": M, "checks": [], "envelope_candidates": {}}
def chk(code, name, va, op, vb, a, b, canon, report=False, note=""):
    out["checks"].append({"code": code, "check": name + (" — REPORT ONLY" if report else ""), "a": a, "b": b, "va": va, "op": op, "vb": vb,
                          "result": "REPORT" if report else cls(op, va, vb), "canon": canon, "note": note})
for c in ("M", "F"):
    lo, ce, hi = c + "147", c + "173", c + "203"
    if not all(x in M for x in (lo, ce, hi)): continue
    chk("U", "%s head share allometric: 147 > 173" % c, M[lo]["head height / stature"], ">", M[ce]["head height / stature"], lo, ce, "MF L19-21 (no uniform scaling); RAC-04 §2.2")
    chk("U", "%s head share allometric: 203 < 173" % c, M[hi]["head height / stature"], "<", M[ce]["head height / stature"], hi, ce, "MF L19-21")
    for x in (lo, hi):
        dev = [k for k in M[ce] if k in M[x] and not k.startswith("stature") and "[t=" not in k and abs(M[x][k] / M[ce][k] - 1) >= 0.01]
        chk("U", "%s: shares departing from the central body by >= 1 %%" % x, len(dev), ">", 0, x, ce, "MF L19-21", note="; ".join(dev))
    for k in M[ce]:
        if k.startswith("stature") or k not in M[lo] or k not in M[hi]: continue
        a, b_, d = M[lo][k], M[ce][k], M[hi][k]
        mono = (a <= b_ <= d) or (a >= b_ >= d)
        flat = min(abs(a / b_ - 1), abs(d / b_ - 1)) < 0.01   # the reversing step is below the 1 % AD-G10 resolution
        out["checks"].append({"code": "C", "check": "%s continuity 147 -> 173 -> 203: %s" % (c, k), "a": lo, "b": hi, "va": [a, b_, d], "op": "trend", "vb": None,
                              "result": "PASS" if (mono or flat) else "NON-MONOTONIC (>= 1 % reversal)", "canon": "W2A order item 3", "note": "%+.1f %% / %+.1f %% vs 173" % (100 * (a / b_ - 1), 100 * (d / b_ - 1))})
    for k in ("femur / tibia (plausibility)",):
        for x in (lo, ce, hi): chk("P", "%s %s (rig joint-to-joint thigh / shin; not an anatomical femur / tibia ratio)" % (x, k), M[x][k], "vs", M[ce][k], x, ce, "segment plausibility", report=True)
    if "CHILD147" in M:
        chk("J", "%s not juvenile: head share < 147 cm child proxy" % lo, M[lo]["head height / stature"], "<", M["CHILD147"]["head height / stature"], lo, "CHILD147", "W2A item 3; MF L13 (adult)")
        for k in ("face vertical / bizygomatic FVB", "waist interval / torso", "crest / thoracic breadth (skin)", "leg / stature", "hand / stature"):
            chk("J", "%s vs child proxy: %s" % (lo, k), M[lo][k], "vs", M["CHILD147"][k], lo, "CHILD147", "W2A item 3", report=True)
    for k in ([] if c == "F" else ["skeletal thoracic depth / stature [t=0.0]", "wrist breadth / stature (scaled slab)", "knee breadth / stature (scaled slab)", "shoulder-joint breadth / stature", "thoracic depth / stature (skin)"]):
        if k in M[hi] and k in M["SK"]: chk("G", "%s not Skarn-like: %s < SK" % (hi, k), M[hi][k], "<", M["SK"][k], hi, "SK", "W2A item 3; SK structural presence (SK L23-25)")
    AL = json.load(open('/home/claude/wayfarer-design/tools/rac/w1/native_short_allometry.json'))["slopes"]
    SL = {"elbow breadth / stature (scaled slab)": AL["elbow"], "wrist breadth / stature (scaled slab)": AL["wrist"], "knee breadth / stature (scaled slab)": AL["knee"],
          "thoracic breadth / stature (skin)": AL["thorax_b"]}
    for e in ("AE", "FN"):
        for k, sl in SL.items():
            if k not in M[hi] or k not in M[e]: continue
            adj = M[e][k] * (M[hi]["stature (cm)"] / M[e]["stature (cm)"]) ** (sl - 1)   # elf value carried to 203 cm by the generator's adult allometry slope
            ctl = M[ce][k] / (M[e][k] * (M[ce]["stature (cm)"] / M[e]["stature (cm)"]) ** (sl - 1)) - 1   # same row on the accepted central body
            nodisc = ctl < 0.01
            chk("E", "%s not elf-like: %s > %s at matched stature (allometry-adjusted %s value)" % (hi, k, e, e), M[hi][k], ">", adj, hi, e + "@203", "W2A item 3; ECR elven gracility",
                report=(c == "F" or nodisc), note=("configuration mismatch (elf references are configuration 1)" if c == "F" else
                ("NO VERDICT: the accepted central %s173 already reads %+.1f %% on this row, so it does not discriminate; " % (c, 100 * ctl) if nodisc else "central control %+.1f %%; " % (100 * ctl)) +
                "raw %s value %.4f at %.0f cm; slope %.3f" % (e, M[e][k], M[e]["stature (cm)"], sl)))
# route cross-checks at 203 (height macro vs native regional route) and the excluded macro at 147
for a, b in (("M203", "M203G"), ("F203", "F203G"), ("M203", "M203N"), ("F203", "F203NB"), ("F147", "F147A"), ("M147", "M147X")):
    if a in M and b in M:
        out.setdefault("route_crosscheck", {})["%s vs %s" % (a, b)] = {k: 100 * (M[a][k] / M[b][k] - 1) for k in M[a] if k in M[b] and "[t=" not in k}
# diagnostic envelope candidates (NON-CANON): min / max over the six boundary-set bodies per reading
six = [x for x in ("M147", "M173", "M203", "F147", "F173", "F203") if x in M]
for k in M["M173"]:
    vals = [(M[x][k], x) for x in six if k in M[x]]
    if len(vals) == len(six): out["envelope_candidates"][k] = {"min": min(vals)[0], "min_body": min(vals)[1], "max": max(vals)[0], "max_body": max(vals)[1], "status": "NON-CANON diagnostic candidate"}
json.dump(out, open(EV + '/boundary.json', 'w'), indent=1, default=float)
bad = [(c["code"], c["check"][:70], c["result"]) for c in out["checks"] if c["result"] not in ("PASS", "REPORT")]
print('bodies', list(M), '\nchecks', len(out["checks"]), 'non-PASS:'); [print('  ', b) for b in bad]
