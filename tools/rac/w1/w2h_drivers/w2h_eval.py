# RAC W2H (short-race family) evaluation: the W2G evaluator plus extra skin / cranial readings and 'ranges' rows; the W1 slot references use the
# accepted Cogling CGJ7 (skin and S7-normalized skeletal) in place of the as-built CG-NAT. NON-CANON diagnostics throughout.
# Values: skin layer (run_candidate 'combined' ratios), skeletal proxy (CIB grid, exact-plane S7, t = 0 / 0.5 / 1.0), joints (EXACT-PLANE SECTION,
# w2c1_drivers/joint_section.py; per stature and per adjacent segment, RAC-05 L32).
# G rows: the accepted W1 rows of the body's own population - directional (directional_checks.py) and skin pelvic (w1e_checks via the same run)
# with the body in its population slot, and skeletal pelvic rows (skeletal_checks.py on the S7-normalized base with the body's skeletal proxy in
# its slot); the other populations stay at their accepted W1 references (Marchfolk 173, W1 elves). Away from the reference stature these are
# fixed-reference rows (boundary-stature rule): the stature-matched rows in the spec govern.
# Comparison rows come from the spec (w2g_spec.py). Classes: AD-G10.
# 'spans': the body's reading lies inside [min, max] of the named matched-height source bodies (Halvren 'source-plausible' rows); margin = distance to
#   the nearest bound in % of the bound (negative = outside); position = 0 at the minimum, 1 at the maximum.
# 'passing': body-only source-passing (neutralized: no ears, pigmentation, hair, clothing, presentation in these meshes; head / ear readings excluded):
#   count of the listed readings that separate the body from the source by >= 1 %; 'NEAR-DUPLICATE' when fewer than 'min_sep' separate.
# Usage: python3 w2h_eval.py REGISTRY.json SPEC.json OUT.json JOINTS.json ...
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
        ("femoral shaft breadth / femur", "shaft_b_over_femur"), ("pelvic vertical / crest", "pelvic_vertical_over_crest")]
SKIN += ["hand_over_arm", "finger_over_palm", "palm_depth_over_hand", "pelvic_depth_share", "crest_share", "hip_joint_breadth_share", "pelvis_over_thorax_breadth",
         "pelvic_vertical_share", "pelvic_vertical_over_thoracic_vertical", "pelvic_depth_over_thorax_depth", "waist_interval_over_torso", "thorax_d_over_b", "wrist_over_forearm"]
J = ("elbow", "wrist", "knee", "ankle")
def cls(op, va, vb):
    if op == "~": return "PASS" if abs(va - vb) <= 0.010 else "FAIL"
    if op == "vs": return "REPORT"
    rel = abs(va - vb) / abs(vb) if vb else 1.0; holds = {">": va > vb, "<": va < vb, ">=": va >= vb, "<=": va <= vb}[op]
    if op in (">", "<"): return ("PASS" if rel >= 0.01 else "NOT DEMONSTRATED") if holds else "FAIL"
    return "PASS" if holds else ("MARGINAL" if rel < 0.01 else "FAIL")
V = {}
for b, e in REG.items():
    if not os.path.exists(e["meas"] + '_meas.json'): print("missing", b); continue
    m = json.load(open(e["meas"] + '_meas.json'))["combined"]; r = m["ratio"]; v = {"stature (cm)": m["stature"]}
    for k in SKIN: v[k] = r.get(k)
    v["neck / torso"] = m["neck_len"] / m["torso_len"]; v["forearm_over_upperarm"] = r.get("forearm_over_upperarm")
    mm = m["mean"]; st_ = m["stature"]; cr = m["cranio"]
    v.update({"hip-joint height / stature": mm["hip_height"] / st_, "palm breadth / stature": mm["palm_breadth"] / st_, "foot breadth / stature": mm["foot_breadth"] / st_,
              "arm (cm)": mm["arm"], "arm to wrist / stature": (mm["arm"] - mm["hand"]) / st_, "thoracic vertical / stature": m["thoracic_vertical"] / st_, "HH (cm)": cr["HH"], "ORB height / HH": cr.get("ORB_height_over_HH"),
              "aperture height / orbit height": cr.get("aperture_height_over_orbit_height"), "IOD": cr.get("IOD")})
    for k in ("FVB", "FVI", "FDH", "CBH", "MPI", "MdPI", "FPI"): v[k] = cr.get(k)
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
CAND = os.environ.get('W2H_CAND', S + '/w2h/cand0'); SKB = os.environ.get('W2H_SKB', S + '/w2h/skb0')   # W2H1: slot references with the D1-corrected Durrim
if not os.path.exists(CAND):      # W1 slot references with the accepted Cogling CGJ7 (W1r ruling) instead of the as-built CG-NAT
    shutil.copytree(S + '/w1g/cand', CAND); shutil.copy(S + '/w1r/probe/CGJ7_meas.json', CAND + '/CG_meas.json')
if not os.path.exists(SKB):
    shutil.copytree(S + '/s7n/w1i_base', SKB, symlinks=True)
    for t in ("0.0", "0.5", "1.0"):
        d = SKB + '/t%s/CG_meas.json' % t
        if os.path.lexists(d): os.remove(d)
        shutil.copy(S + '/s7n/w1r_cgj7/t%s/CG-NAT_meas.json' % t, d)
def mine(x, race): return x.get("cand") == race or x.get("b") == race or x.get("a") == race
for b, e in REG.items():
    race = e.get("race")
    if not race or b not in V: continue
    tmp = S + '/w2h/cand_' + b + os.environ.get('W2H_TAG', '')
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
        tk = S + '/w2h/skc_' + b + os.environ.get('W2H_TAG', '')
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
    else: res = "REPORT" if row.get("report") else ("PASS" if abs(d) < row["tol"] else "FAIL")
    C.append({"code": row["code"], "check": row["check"], "a": a, "b": b, "reading": k, "va": V[a][k], "op": row["kind"], "vb": V[b][k], "margin_pct": 100 * d, "result": res, "note": "%+.2f %%" % (100 * d)})
for row in SPEC.get("spans", []):
    a = row["a"]; k = row["k"]; srcs = [x for x in row["srcs"] if V.get(x, {}).get(k) is not None]
    if V.get(a, {}).get(k) is None or len(srcs) < 2:
        C.append({"code": row["code"], "check": row["check"], "a": a, "b": ",".join(row["srcs"]), "reading": k, "va": None, "op": "in", "vb": None, "result": "NOT RUN", "note": "reading or sources unavailable"}); continue
    vals = [V[x][k] for x in srcs]; lo, hi = min(vals), max(vals); va = V[a][k]
    inside = lo <= va <= hi; m = 100 * min(va / lo - 1, 1 - va / hi) if inside else 100 * ((va / lo - 1) if va < lo else (1 - va / hi))
    pos = (va - lo) / (hi - lo) if hi > lo else 0.5
    C.append({"code": row["code"], "check": row["check"], "a": a, "b": ",".join(srcs), "reading": k, "va": va, "op": "in", "vb": [lo, hi], "margin_pct": m, "position": pos,
              "result": "REPORT" if row.get("report") else ("PASS" if inside else ("MARGINAL" if abs(m) < 1.0 else "FAIL")), "note": "span %s (%s .. %s); position %.2f" % ("/".join(srcs), min(srcs, key=lambda x: V[x][k]), max(srcs, key=lambda x: V[x][k]), pos)})
for row in SPEC.get("passing", []):
    a, b = row["a"], row["b"]
    ks = [k for k in row["keys"] if V.get(a, {}).get(k) is not None and V.get(b, {}).get(k) is not None]
    if a not in V or b not in V or not ks: continue
    sep = [(k, 100 * (V[a][k] / V[b][k] - 1)) for k in ks if abs(V[a][k] / V[b][k] - 1) >= 0.01]
    C.append({"code": row["code"], "check": row["check"], "a": a, "b": b, "reading": "%d body readings" % len(ks), "va": len(sep), "op": ">=", "vb": row.get("min_sep", 2),
              "result": "REPORT" if row.get("report") else ("PASS" if len(sep) >= row.get("min_sep", 2) else "NEAR-DUPLICATE"),
              "note": "%d / %d readings separate by >= 1 %%: %s" % (len(sep), len(ks), "; ".join("%s %+.1f" % (k.replace(" (exact-plane section)", "").replace(" [t=0.0]", ""), d) for k, d in sorted(sep, key=lambda z: -abs(z[1]))[:6]))})
for row in SPEC.get("ranges", []):
    a, k = row["a"], row["k"]; va = V.get(a, {}).get(k)
    if va is None: C.append({"code": row["code"], "check": row["check"], "a": a, "b": "range", "reading": k, "va": None, "op": "in", "vb": None, "result": "NOT RUN", "note": "reading unavailable"}); continue
    lo, hi = row["lo"], row["hi"]; inside = lo <= va <= hi; m = 100 * min(va / lo - 1, 1 - va / hi) if inside else 100 * ((va / lo - 1) if va < lo else (1 - va / hi))
    C.append({"code": row["code"], "check": row["check"], "a": a, "b": "range", "reading": k, "va": va, "op": "in", "vb": [lo, hi], "margin_pct": m,
              "result": "PASS" if inside else ("MARGINAL" if abs(m) < 1.0 else "FAIL"), "note": "%.2f in [%.1f, %.1f]" % (va, lo, hi)})
# spans follow AD-G10: outside the span by < 1 % = MARGINAL, >= 1 % = FAIL
# X tendency (§7): the expression moves from HVC1 toward the influencing source. Source not >= 1 % from HVC1 on the reading -> REPORT (nothing to
# express); move >= 1 % toward -> PASS (beyond the source by >= 1 % -> OVERSHOOT); < 1 % -> NOT DEMONSTRATED; >= 1 % away -> FAIL
for row in SPEC.get("toward", []):
    a, b, s_, k = row["a"], row["base"], row["src"], row["k"]
    va, vb, vs = (V.get(x, {}).get(k) for x in (a, b, s_))
    if None in (va, vb, vs):
        C.append({"code": row["code"], "check": row["check"], "a": a, "b": s_, "reading": k, "va": None, "op": "toward", "vb": None, "result": "NOT RUN", "note": "reading unavailable"}); continue
    gap = vs / vb - 1; mv_ = va / vb - 1; tw = mv_ * (1 if gap > 0 else -1); frac = mv_ / gap if gap else None
    if abs(gap) < 0.01 or row.get("report"): res = "REPORT" if abs(gap) < 0.01 else "REPORT (%s)" % ("PASS" if tw >= 0.01 and (va / vs - 1) * (1 if gap > 0 else -1) < 0.01 else "OVERSHOOT" if tw >= 0.01 else "NOT DEMONSTRATED" if tw > -0.01 else "FAIL")
    elif tw >= 0.01: res = "OVERSHOOT" if (va / vs - 1) * (1 if gap > 0 else -1) >= 0.01 else "PASS"
    elif tw > -0.01: res = "NOT DEMONSTRATED"
    else: res = "FAIL"
    C.append({"code": row["code"], "check": row["check"] + (" — REPORT ONLY (source within 1 % of HVC1)" if res == "REPORT" else ""), "a": a, "b": s_, "reading": k, "va": va, "op": "toward", "vb": vs,
              "base": vb, "margin_pct": 100 * tw, "fraction": frac, "result": res, "note": "HVC1 %.4f -> %s %.4f (%+.2f %%); source %.4f (gap %+.2f %%); fraction of gap %s" % (vb, a, va, 100 * mv_, vs, 100 * gap, "%.2f" % frac if frac is not None else "-")})
json.dump({"values": V, "checks": C, "canonical_rows": CANON}, open(OUT, 'w'), indent=1, default=float)
import collections
print(len(C), "checks", collections.Counter((c["code"], c["result"] if c["result"] in ("PASS", "REPORT") else c["result"][:16]) for c in C))
for c in C:
    if c["result"] not in ("PASS", "REPORT"): print(" ", c["code"], c["check"][:120], "|", str(c.get("note", ""))[:220], c["result"])
