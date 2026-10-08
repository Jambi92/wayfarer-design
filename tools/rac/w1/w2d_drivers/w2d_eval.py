# RAC W2D (Gorrund W2) evaluation. NON-CANON diagnostics throughout.
# Values: skin layer (run_candidate 'combined' ratios), skeletal proxy (CIB, exact-plane S7, t = 0 / 0.5 / 1.0), joints (EXACT-PLANE SECTION
# through the joint centre, w2c1_drivers/joint_section.py; the authority for newly scored joint rows, REFERENCE_ANATOMY_V1 §10).
# Canonical Gorrund rows per body: skeletal rows (w1g_drivers/gn3.checks: skeletal_checks on the S7-normalized base, the body in the GO
# slot) and the directional / skin rows (go_search.ev: directional_checks + w1e_checks, the body in the GO slot).
# Comparison rows come from the spec (w2d_spec.py). Classes: AD-G10 (strict rows need >= 1 %, else NOT DEMONSTRATED; >= / <= rows missing
# by < 1 % are MARGINAL; mixed across t is T-SENSITIVE).   Usage: python3 w2d_eval.py REGISTRY.json SPEC.json OUT.json JOINTS.json ...
import sys, os, json
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; R = '/home/claude/wayfarer-design'
SKPBASE = S + '/s7n/w1i_base'     # S7-normalized comparator base (set on gn3 after import: gn6 reads the pre-normalization cand dir at import)
for p in ('', '/w1g_drivers', '/w2d_drivers'): sys.path.insert(0, R + '/tools/rac/w1' + p)
REG = json.load(open(sys.argv[1])); SPEC = json.load(open(sys.argv[2])); OUT = sys.argv[3]
JS = {}
for f in sys.argv[4:]: JS.update(json.load(open(f)))
SKIN = ["torso_share", "leg_share", "arm_share", "span_der", "upperarm_over_arm", "forearm_over_arm", "femur_over_leg", "shin_over_leg", "neck_share", "HH_share",
        "hand_share", "foot_share", "finger_over_palm", "thorax_breadth_share", "thorax_depth_share", "shoulder_joint_share"]
SKEL = [("thoracic breadth / stature", "thorax_breadth_share"), ("thoracic depth / stature", "thorax_depth_share"), ("shoulder-joint breadth / stature", "shoulder_joint_share"),
        ("biacromial / stature", "biacromial_share"), ("crest breadth / stature", "crest_share"), ("AP pelvic depth / stature", "pelvic_depth_share"),
        ("pelvic vertical / stature", "pelvic_vertical_share"), ("hip-joint spacing / stature", "hip_joint_breadth_share"), ("bitrochanteric / crest", "bitroch_over_crest"),
        ("shoulder-joint / thoracic breadth", "S1_over_S2_b"), ("thoracic depth / breadth", "thorax_d_over_b"), ("hip-joint scale / crest", "hipjoint_scale_over_crest"),
        ("ALPC lower-thorax breadth / thorax (S3/S2 b)", "S3_over_S2_b"), ("ALPC lumbar breadth / thorax (S4/S2 b)", "S4_over_S2_b"),
        ("ALPC lower-thorax depth / thorax (S3/S2 d)", "S3_over_S2_d"), ("ALPC lumbar depth / thorax (S4/S2 d)", "S4_over_S2_d"),
        ("ALPC crest / thorax breadth (S5/S2 b)", "S5_over_S2_b"), ("ALPC hip-level / thorax breadth (S6/S2 b)", "S6_over_S2_b"),
        ("ALPC pelvic AP / thoracic depth", "pelvic_depth_over_thorax_depth"), ("ribcage vertical / breadth", "ribcage_vertical_over_S2_b")]
J = ("elbow", "wrist", "knee", "ankle")
def cls(op, va, vb):
    if op == "~": return "PASS" if abs(va - vb) <= 0.010 else "FAIL"     # W1c absolute method tolerance (w1e_checks APPROX)
    rel = abs(va - vb) / abs(vb) if vb else 1.0; holds = {">": va > vb, "<": va < vb, ">=": va >= vb, "<=": va <= vb}[op]
    if op in (">", "<"): return ("PASS" if rel >= 0.01 else "NOT DEMONSTRATED") if holds else "FAIL"
    return "PASS" if holds else ("MARGINAL" if rel < 0.01 else "FAIL")
V = {}
for b, e in REG.items():
    if not os.path.exists(e["meas"] + '_meas.json'): print("missing", b); continue
    m = json.load(open(e["meas"] + '_meas.json'))["combined"]; r = m["ratio"]; v = {"stature (cm)": m["stature"]}
    for k in SKIN: v[k] = r.get(k)
    if e.get("skp"):
        for t in ("0.0", "0.5", "1.0"):
            q = json.load(open('%s/t%s/%s_meas.json' % (e["skp"], t, e["skp_id"])))["combined"]; qr = q["ratio"]; st = q["stature"]; b7, d7 = q["alpc_stations"]["S7"]
            for nm, k in SKEL: v["skeletal %s [t=%s]" % (nm, t)] = qr.get(k)
            v["femoral S7 breadth / stature [t=%s]" % t] = b7 / st; v["femoral S7 depth / stature [t=%s]" % t] = d7 / st
    jk = e.get("joint")
    if jk and jk in JS:
        for j in J: v["%s breadth / stature (exact-plane section)" % j] = JS[jk]["section"][j]
        # RAC-05 L32 joint scale = joint / adjacent bone (the W1 'joint scale GO > GR' metric), read with the exact-plane section;
        # segment lengths from the same body's skin-layer shares (upper arm, forearm, femur, lower leg / stature)
        seg = {"elbow": (r.get("upperarm_over_arm"), r.get("arm_share")), "wrist": (r.get("forearm_over_arm"), r.get("arm_share")),
               "knee": (r.get("femur_over_leg"), r.get("leg_share")), "ankle": (r.get("shin_over_leg"), r.get("leg_share"))}
        for j, (a_, b_) in seg.items():
            if a_ and b_: v["%s breadth / adjacent segment (exact-plane section)" % j] = JS[jk]["section"][j] / (a_ * b_)
    V[b] = v
C = []
def add(code, chk, a, op, b, k, note="", report=False, va=None, vb=None):
    va = V.get(a, {}).get(k) if va is None else va; vb = V.get(b, {}).get(k) if vb is None else vb
    if va is None or vb is None: C.append({"code": code, "check": chk, "a": a, "b": b, "reading": k, "va": None, "op": op, "vb": None, "result": "NOT RUN", "note": "reading unavailable"}); return
    C.append({"code": code, "check": chk + (" — REPORT ONLY" if report else ""), "a": a, "b": b, "reading": k, "va": va, "op": op, "vb": vb,
              "margin_pct": 100 * (va / vb - 1), "result": "REPORT" if report else cls(op, va, vb), "note": note})
def tsweep(code, chk, a, op, b, k, note="", report=False):
    """skeletal rows over t = 0 / 0.5 / 1.0: PASS only when every t passes; mixed -> T-SENSITIVE"""
    ks = [k.replace("[t=0.0]", "[t=%s]" % t) for t in ("0.0", "0.5", "1.0")]
    if not all(V.get(a, {}).get(x) is not None and V.get(b, {}).get(x) is not None for x in ks): add(code, chk, a, op, b, k, note, report); return
    res = [cls(op, V[a][x], V[b][x]) for x in ks]; va = [V[a][x] for x in ks]; vb = V[b][ks[1]]
    out = res[0] if len(set(res)) == 1 else "T-SENSITIVE"
    C.append({"code": code, "check": chk + (" — REPORT ONLY" if report else ""), "a": a, "b": b, "reading": k.replace(" [t=0.0]", " [t=0 / 0.5 / 1]"), "va": va, "op": op, "vb": vb,
              "margin_pct": 100 * (V[a][ks[1]] / vb - 1), "result": "REPORT" if report else out, "note": note + ("; by t: " + "/".join(res) if len(set(res)) > 1 else "")})
# A. stature foundation: continuity 208 -> 218 -> 229 -> 239 -> 251, head allometry
SER = ["GO208", "GO218", "GO229", "GO239", "GO251"]
if all(x in V for x in SER):
    add("U", "head share allometric: 208 > 229", "GO208", ">", "GO229", "HH_share"); add("U", "head share allometric: 251 < 229", "GO251", "<", "GO229", "HH_share")
    for k in V["GO229"]:
        if k.startswith("stature") or "[t=0.5]" in k or "[t=1.0]" in k: continue
        vals = [V[x].get(k) for x in SER]
        if any(v is None for v in vals): continue
        rev = [100 * (vals[i + 1] / vals[i] - 1) for i in range(4)]; up = sum(r > 0 for r in rev); dn = sum(r < 0 for r in rev)
        ok = not (up and dn) or max(abs(r) for r in rev if (r > 0) != (up >= dn)) < 1.0
        C.append({"code": "C", "check": "continuity 208 -> 218 -> 229 -> 239 -> 251: %s" % k, "a": "GO208", "b": "GO251", "reading": k, "va": vals, "op": "trend", "vb": None,
                  "result": "PASS" if ok else "NON-MONOTONIC (>= 1 % reversal)", "note": " / ".join("%+.1f" % r for r in rev) + " % per step"})
# G. canonical Gorrund rows on every Gorrund body (skeletal on own skeleton; directional / skin on own skin)
CANON = {}
if os.environ.get("W2D_CANON", "1") == "1":
    import gn3, go_search as GS
    gn3.SKP = SKPBASE
    for b, e in REG.items():
        if not e.get("gorrund") or b not in V: continue
        rows = []
        if e.get("skp"):
            for x in gn3.checks("GO", b, wd=e["dir"]):
                if not (x['cand'] == 'GO' or x.get('b') == 'GO'): continue
                rows.append({"kind": "skeletal", "check": x["check"], "op": x["op"], "result": x["result"], "by_t": {t: {"va": w.get("va"), "vb": w.get("vb")} for t, w in x["by_t"].items()}})
        kd = "directional/skin" if not e.get("comp") else "directional/skin vs neutral-composition comparators (REPORT)"
        for x in GS.ev(b, e["dir"]): rows.append({"kind": kd, "check": x["check"], "op": x["op"], "result": x["result"], "va": x["va"], "vb": x["vb"]})
        if e.get("comp") and b.startswith("GOR-BODY-16"):
            # ALPC-6 skin half at matched low composition (as alpc_invariance.py): MF and SK comparators replaced by their 0.25 / 0.25 states
            import shutil, w1e_checks as WC, alpc_invariance as AI
            tmp = GS.S + '/w2d/alpc6_' + b
            if os.path.exists(tmp): shutil.rmtree(tmp)
            shutil.copytree(GS.GB.G + '/cand', tmp)
            for src, idn in ((e["meas"], "GO"), (REG["MF-LOW"]["meas"], "MF-M-R"), (REG["SK-LOW"]["meas"], "SK")):
                if os.path.lexists(tmp + '/%s_meas.json' % idn): os.remove(tmp + '/%s_meas.json' % idn)
                shutil.copy(src + '_meas.json', tmp + '/%s_meas.json' % idn)
            for x in WC.run(tmp):
                if x["cand"] == "GO" and AI.keep_row(x["check"]) and "ALPC-3" not in x["check"]:
                    rows.append({"kind": "ALPC-6 skin half (matched low composition)", "check": x["check"], "op": x["op"], "result": x["result"], "va": x["va"], "vb": x["vb"]})
        CANON[b] = rows
    # the accepted reference (GOREF reproduces the accepted W1 Gorrund exactly) already carries documented skin-layer pelvic diagnostics;
    # a row that is non-PASS on GOREF is listed as 'shared with the accepted reference', and only rows that are new on a body count
    BASE = {(x["kind"], x["check"]) for x in CANON.get("GOREF", []) + CANON.get("GOR-BODY-16", []) if x["result"] not in ("PASS", "REPORT", "NOT RUN")}
    for b, rows in CANON.items():
        for kind in ("skeletal", "directional/skin", "ALPC-6 skin half (matched low composition)"):
            rr = [x for x in rows if x["kind"] == kind and x["result"] not in ("REPORT", "NOT RUN")]
            if not rr: continue
            bad = [x for x in rr if x["result"] != "PASS"]; new = [x for x in bad if (kind, x["check"]) not in BASE]
            C.append({"code": "G", "check": "%s: canonical Gorrund %s rows" % (b, kind), "a": b, "b": "accepted comparators", "reading": "rows", "va": len(rr) - len(bad), "op": "of", "vb": len(rr),
                      "result": "PASS" if not new else "NOT ALL PASS", "shared_with_reference": len(bad) - len(new),
                      "note": ("%d non-PASS shared with the accepted reference; " % (len(bad) - len(new)) if len(bad) > len(new) else "") + "; ".join("%s %s" % (x["result"], x["check"][:90]) for x in new)})
# spec rows
for row in SPEC.get("rows", []):
    (tsweep if "[t=0.0]" in row["k"] else add)(row["code"], row["check"], row["a"], row["op"], row["b"], row["k"], row.get("note", ""), row.get("report", False))
for row in SPEC.get("invariance", []):
    a, b = row["a"], row["b"]
    if a not in V or b not in V: continue
    moved = [k for k in row["keys"] if V[a].get(k) and V[b].get(k) and abs(V[a][k] / V[b][k] - 1) >= row.get("tol", 0.01)]
    C.append({"code": row["code"], "check": row["check"], "a": a, "b": b, "reading": "shares", "va": len(moved), "op": "=", "vb": 0,
              "result": "PASS" if not moved else "FAIL", "note": "; ".join("%s %+.2f %%" % (k, 100 * (V[a][k] / V[b][k] - 1)) for k in moved) or "none"})
for row in SPEC.get("moves", []):     # frame domains: a frame moves a reading by >= 1 % in its direction (D), or keeps it within tol (L)
    a, b, k = row["a"], row["b"], row["k"]
    if V.get(a, {}).get(k) is None or V.get(b, {}).get(k) is None: continue
    d = V[a][k] / V[b][k] - 1
    if row["kind"] == "D": res = "PASS" if row["sign"] * d >= 0.01 else "NOT DEMONSTRATED"
    else: res = "PASS" if abs(d) < row["tol"] else ("REPORT" if row.get("report") else "FAIL")
    C.append({"code": row["code"], "check": row["check"], "a": a, "b": b, "reading": k, "va": V[a][k], "op": row["kind"], "vb": V[b][k], "margin_pct": 100 * d, "result": res, "note": "%+.2f %%" % (100 * d)})
json.dump({"values": V, "checks": C, "canonical_rows": CANON}, open(OUT, 'w'), indent=1, default=float)
import collections
print(len(C), "checks", collections.Counter(c["result"] if c["result"] in ("PASS", "REPORT") else c["result"][:16] for c in C))
for c in C:
    if c["result"] not in ("PASS", "REPORT"): print(" ", c["code"], c["check"][:120], "|", str(c.get("note", ""))[:200], c["result"])
