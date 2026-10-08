# RAC W2F (Elf family W2: Fenn / Aelari / Vael) evaluation. NON-CANON diagnostics throughout.
# Values: skin layer (run_candidate 'combined' ratios), skeletal proxy (CIB grid, exact-plane S7, t = 0 / 0.5 / 1.0), joints (EXACT-PLANE SECTION,
# w2c1_drivers/joint_section.py; per stature and per adjacent segment, RAC-05 L32).
# G rows: the accepted W1 rows of the body's own population - directional (directional_checks.py) and skin pelvic (w1e_checks via the same run)
# with the body in its population slot, and skeletal pelvic rows (skeletal_checks.py on the S7-normalized base with the body's skeletal proxy in
# its slot); the other populations stay at their accepted W1 references (Marchfolk 173, W1 elves). Away from the reference stature these are
# fixed-reference rows (boundary-stature rule): the stature-matched rows in the spec govern.
# Comparison rows come from the spec (w2f_spec.py). Classes: AD-G10.   Usage: python3 w2f_eval.py REGISTRY.json SPEC.json OUT.json JOINTS.json ...
import sys, os, json, shutil
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; R = '/home/claude/wayfarer-design'
sys.path.insert(0, R + '/tools/rac/w1')
REG = json.load(open(sys.argv[1])); SPEC = json.load(open(sys.argv[2])); OUT = sys.argv[3]
JS = {}
for f in sys.argv[4:]: JS.update(json.load(open(f)))
SKIN = ["torso_share", "leg_share", "arm_share", "span_der", "upperarm_over_arm", "forearm_over_arm", "femur_over_leg", "shin_over_leg", "neck_share", "HH_share",
        "hand_share", "finger_over_hand", "palm_breadth_over_hand", "foot_share", "thorax_breadth_share", "thorax_depth_share", "shoulder_joint_share"]     # joints: exact-plane sections only (slab ratios are historical)
SKEL = [("thoracic breadth / stature", "thorax_breadth_share"), ("thoracic depth / stature", "thorax_depth_share"), ("thoracic depth / breadth", "thorax_d_over_b"),
        ("shoulder-joint breadth / stature", "shoulder_joint_share"), ("biacromial / stature", "biacromial_share"), ("crest breadth / stature", "crest_share"),
        ("AP pelvic depth / stature", "pelvic_depth_share"), ("pelvic vertical / stature", "pelvic_vertical_share"), ("hip-joint spacing / stature", "hip_joint_breadth_share"),
        ("bitrochanteric / crest", "bitroch_over_crest"), ("crest / thoracic breadth", "pelvis_over_thorax_breadth"), ("pelvic AP / thoracic depth", "pelvic_depth_over_thorax_depth"),
        ("waist interval / torso", "waist_interval_over_torso"), ("pelvic vertical / thoracic vertical", "pelvic_vertical_over_thoracic_vertical"), ("ribcage vertical / breadth", "ribcage_vertical_over_S2_b"),
        ("femoral shaft breadth / femur", "shaft_b_over_femur")]
J = ("elbow", "wrist", "knee", "ankle")
def cls(op, va, vb):
    if op == "~": return "PASS" if abs(va - vb) <= 0.010 else "FAIL"
    rel = abs(va - vb) / abs(vb) if vb else 1.0; holds = {">": va > vb, "<": va < vb, ">=": va >= vb, "<=": va <= vb}[op]
    if op in (">", "<"): return ("PASS" if rel >= 0.01 else "NOT DEMONSTRATED") if holds else "FAIL"
    return "PASS" if holds else ("MARGINAL" if rel < 0.01 else "FAIL")
V = {}
for b, e in REG.items():
    if not os.path.exists(e["meas"] + '_meas.json'): print("missing", b); continue
    m = json.load(open(e["meas"] + '_meas.json'))["combined"]; r = m["ratio"]; v = {"stature (cm)": m["stature"]}
    for k in SKIN: v[k] = r.get(k)
    v["neck / torso"] = m["neck_len"] / m["torso_len"]; v["forearm_over_upperarm"] = r.get("forearm_over_upperarm")
    if e.get("skp") and os.path.exists('%s/t0.0/%s_meas.json' % (e["skp"], e["skp_id"])):
        for t in ("0.0", "0.5", "1.0"):
            q = json.load(open('%s/t%s/%s_meas.json' % (e["skp"], t, e["skp_id"])))["combined"]; qr = q["ratio"]; st = q["stature"]; b7, d7 = q["alpc_stations"]["S7"]
            for nm, k in SKEL: v["skeletal %s [t=%s]" % (nm, t)] = qr.get(k)
            v["femoral S7 breadth / stature [t=%s]" % t] = b7 / st; v["femoral S7 depth / stature [t=%s]" % t] = d7 / st
    jk = e.get("joint")
    if jk and jk in JS:
        for j in J: v["%s breadth / stature (exact-plane section)" % j] = JS[jk]["section"][j]
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
    ks = [k.replace("[t=0.0]", "[t=%s]" % t) for t in ("0.0", "0.5", "1.0")]
    if not all(V.get(a, {}).get(x) is not None and V.get(b, {}).get(x) is not None for x in ks): add(code, chk, a, op, b, k, note, report); return
    res = [cls(op, V[a][x], V[b][x]) for x in ks]; out = res[0] if len(set(res)) == 1 else "T-SENSITIVE"
    C.append({"code": code, "check": chk + (" — REPORT ONLY" if report else ""), "a": a, "b": b, "reading": k.replace(" [t=0.0]", " [t=0 / 0.5 / 1]"), "va": [V[a][x] for x in ks], "op": op,
              "vb": [V[b][x] for x in ks], "margin_pct": 100 * (V[a][ks[1]] / V[b][ks[1]] - 1), "result": "REPORT" if report else out, "note": note + ("; by t: " + "/".join(res) if len(set(res)) > 1 else "")})
# continuity over the stature family (route seam: 152 native / >= 163 macro)
SERIES = SPEC.get("series") or {}
if isinstance(SERIES, list): SERIES = {"": SERIES}
for _p, SER in SERIES.items():
  if all(x in V for x in SER):
      for k in V[SER[2]]:
          if k.startswith("stature") or "[t=0.5]" in k or "[t=1.0]" in k: continue
          vals = [V[x].get(k) for x in SER]
          if any(v is None for v in vals): continue
          rev = [100 * (vals[i + 1] / vals[i] - 1) for i in range(len(vals) - 1)]; up = sum(r > 0 for r in rev); dn = sum(r < 0 for r in rev)
          bad = [i for i, r in enumerate(rev) if up and dn and ((r > 0) != (up >= dn)) and abs(r) >= 1.0]
          C.append({"code": "C", "check": "continuity %s: %s" % (" -> ".join(x.replace("SG", "").replace("-NAT", "") for x in SER), k), "a": SER[0], "b": SER[-1], "reading": k, "va": vals, "op": "trend", "vb": None,
                    "result": "PASS" if not bad else "NON-MONOTONIC (>= 1 % reversal)", "note": " / ".join("%+.1f" % r for r in rev) + " % per step" + ("; reversal at step(s) %s" % ", ".join("%s->%s" % (SER[i], SER[i + 1]) for i in bad) if bad else "")})

# G. accepted W1 rows of the body's own population
CANON = {}
import directional_checks as DC, skeletal_checks as SCK
CAND = S + '/w1g/cand'; SKB = S + '/s7n/w1i_base'
def mine(x, race): return x.get("cand") == race or x.get("b") == race or x.get("a") == race
for b, e in REG.items():
    race = e.get("race")
    if not race or b not in V: continue
    tmp = S + '/w2f/cand_' + b
    if os.path.exists(tmp): shutil.rmtree(tmp)
    shutil.copytree(CAND, tmp); shutil.copy(e["meas"] + '_meas.json', tmp + '/%s_meas.json' % race)
    rows = []
    for x in DC.run(tmp):
        if not mine(x, race) or x.get("historical"): continue
        va, vb, op = x.get("va"), x.get("vb"), x.get("op")
        if isinstance(va, (int, float)) and isinstance(vb, (int, float)) and op in (">", "<"): res = cls(op, va, vb)
        else: res = "PASS" if x.get("pass") else "FAIL"
        rows.append({"layer": "directional (skin)", "check": x["check"], "cand": x.get("cand"), "op": op, "va": va, "vb": vb, "result": res})
    if e.get("skp") and os.path.exists('%s/t0.0/%s_meas.json' % (e["skp"], e["skp_id"])):
        tk = S + '/w2f/skc_' + b
        if os.path.exists(tk): shutil.rmtree(tk)
        shutil.copytree(SKB, tk, symlinks=True, ignore=shutil.ignore_patterns('*_skp.json', '*.jpg', 'skeletal_checks.json'))
        for t in ("0.0", "0.5", "1.0"):
            dst = tk + '/t%s/%s_meas.json' % (t, race)
            if os.path.lexists(dst): os.remove(dst)
            shutil.copy('%s/t%s/%s_meas.json' % (e["skp"], t, e["skp_id"]), dst)
        for x in SCK.run(tk):
            if (x.get("cand") == race or x.get("b") == race) and x["result"] not in ("NOT RUN", "REPORT"):
                rows.append({"layer": "skeletal (t sweep)", "check": x["check"], "cand": x.get("cand"), "op": x["op"], "va": x.get("va"), "vb": x.get("vb"), "result": x["result"],
                             "by_t": {t: {"va": w["va"], "vb": w["vb"]} for t, w in x["by_t"].items()}})
    CANON[b] = rows
    for layer in ("directional (skin)", "skeletal (t sweep)"):
        rr = [x for x in rows if x["layer"] == layer]
        if not rr: continue
        bad = [x for x in rr if x["result"] != "PASS"]
        C.append({"code": "G", "check": "%s: accepted W1 %s rows (%s slot; fixed W1 references)" % (b, layer, race), "a": b, "b": "W1 references", "reading": "rows", "va": len(rr) - len(bad), "op": "of", "vb": len(rr),
                  "result": "PASS" if not bad else "NOT ALL PASS", "note": "; ".join("%s %s (%s %s %s)" % (x["result"], x["check"][:70], "%.4f" % x["va"] if isinstance(x["va"], float) else x["va"], x["op"], "%.4f" % x["vb"] if isinstance(x["vb"], float) else x["vb"]) for x in bad)})
for row in SPEC.get("rows", []):
    if row.get("gate"):     # provisional anti-elf rows: scored only where the W1 elf is beyond matched-height Marchfolk by >= 1 % on that reading
        elf, mf = row["gate"]; ve, vm = V.get(elf, {}).get(row["k"]), V.get(mf, {}).get(row["k"])
        beyond = ve is not None and vm is not None and ((ve > vm * 1.01) if row["op"] == "<" else (ve < vm * 0.99))
        if not beyond: row = dict(row, report=True, note=row.get("note", "") + "; W1 elf not beyond matched Marchfolk (%s) by 1 %% on this reading" % mf)
    (tsweep if "[t=0.0]" in row["k"] else add)(row["code"], row["check"], row["a"], row["op"], row["b"], row["k"], row.get("note", ""), row.get("report", False))
    # W2F closure ruling R1 (reviews/chatgpt-rac-w2f-elf-family-closure-order.md §1): E-A2, VA-P2a and the Aelari longer-leg relation are
    # reference-state directional relations - at matched height a difference below 1 % in (or effectively equal to) the intended direction is accepted;
    # an isolated scalar overlap with Sagekin is an accepted complete-anatomy overlap (W2E rule). Rows keep their raw class in 'raw_result'.
    c = C[-1]
    if row.get("r1") and c["result"] in ("NOT DEMONSTRATED", "FAIL", "MARGINAL", "T-SENSITIVE"):
        c["raw_result"] = c["result"]; m = c.get("margin_pct")
        if row["r1"] == "ref" and m is not None and abs(m) < 1.0: c["result"] = "PASS (R1 reference-state)"
        elif row["r1"] == "overlap": c["result"] = "OVERLAP (R1 complete anatomy)"
for row in SPEC.get("invariance", []):
    a, b = row["a"], row["b"]
    if a not in V or b not in V: continue
    moved = [k for k in row["keys"] if V[a].get(k) and V[b].get(k) and abs(V[a][k] / V[b][k] - 1) >= row.get("tol", 0.01)]
    C.append({"code": row["code"], "check": row["check"], "a": a, "b": b, "reading": "shares", "va": len(moved), "op": "=", "vb": 0,
              "result": "PASS" if not moved else ("REPORT" if row.get("report") else "FAIL"), "note": "; ".join("%s %+.2f %%" % (k, 100 * (V[a][k] / V[b][k] - 1)) for k in moved) or "none"})
for row in SPEC.get("moves", []):
    a, b, k = row["a"], row["b"], row["k"]
    if V.get(a, {}).get(k) is None or V.get(b, {}).get(k) is None: continue
    d = V[a][k] / V[b][k] - 1
    if row["kind"] == "D": res = "PASS" if row["sign"] * d >= 0.01 else "NOT DEMONSTRATED"
    else: res = "PASS" if abs(d) < row["tol"] else ("REPORT" if row.get("report") else "FAIL")
    C.append({"code": row["code"], "check": row["check"], "a": a, "b": b, "reading": k, "va": V[a][k], "op": row["kind"], "vb": V[b][k], "margin_pct": 100 * d, "result": res, "note": "%+.2f %%" % (100 * d)})
json.dump({"values": V, "checks": C, "canonical_rows": CANON}, open(OUT, 'w'), indent=1, default=float)
import collections
print(len(C), "checks", collections.Counter((c["code"], c["result"] if c["result"] in ("PASS", "REPORT") else c["result"][:16]) for c in C))
for c in C:
    if c["result"] not in ("PASS", "REPORT"): print(" ", c["code"], c["check"][:120], "|", str(c.get("note", ""))[:220], c["result"])
