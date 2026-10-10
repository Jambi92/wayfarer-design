# RAC W3A: evidence tables (markdown) from the evaluator output (w2g_eval.py on the W3A registry / spec), the emulator output (w3a_emul.py) and
# the build records.   Usage: python3 w3a_tables.py W3A.json EMUL.json REGISTRY.json OUT.md CONSTRUCTION.json
import sys, json, os, collections
D = json.load(open(sys.argv[1])); E = json.load(open(sys.argv[2])); R = json.load(open(sys.argv[3])); OUT = sys.argv[4]; CON = sys.argv[5]; RS = json.load(open(sys.argv[6])); AU = json.load(open(sys.argv[7]))
V, C = D["values"], D["checks"]
L = []
def f(x, n=4):
    if isinstance(x, float): return ("%%.%df" % n) % x
    if isinstance(x, list): return "[" + ", ".join(f(y, n) for y in x) + "]"
    return str(x)
def table(head, rows):
    L.append("| " + " | ".join(head) + " |"); L.append("|" + "---|" * len(head))
    for r in rows: L.append("| " + " | ".join(str(x).replace("|", "/") for x in r) + " |")
    L.append("")
# construction record
con = {}
for n, e in R.items():
    p = e["meas"] + "_build.json" if not e["meas"].endswith("-NAT") else e["meas"] + "_build.json"
    if "/w3a/" not in e["meas"] or not os.path.exists(p): continue
    b = json.load(open(p)); cfg = b["cfg"]
    con[n] = {"stature_r6": b.get("stature_r6"), "route": "native short-adult (native_short.py)" if "native_factors" in b else (b.get("route") or "variant"), "height_macro": b.get("height_macro"),
              "native_factors": b.get("native_factors"), "base": os.path.basename(b["base"]) if b.get("base") else None, "overrides": b.get("overrides"), "targets": cfg.get("targets"),
              "bone_scales": cfg.get("bone_scales"), "muscle": cfg.get("muscle"), "weight": cfg.get("weight")}
json.dump(con, open(CON, "w"), indent=1)
L.append("# RAC W3A — Halvren genealogy-tail evidence tables (NON-CANON diagnostics)\n")
L.append("## 1. Bodies built (route, stature, generator height macro)\n")
table(["body", "stature (cm)", "route", "macro", "native len factor", "base / class"],
      [(n, f(c["stature_r6"], 2), c["route"][:40], f(c["height_macro"], 3) if c["height_macro"] else "-", f(c["native_factors"]["len"], 4) if c["native_factors"] else "-", c["base"] or "-") for n, c in sorted(con.items())])
# checks grouped by code
NAMES = collections.OrderedDict([("L", "Lower tail (HV-49) — Marchfolk-supported search"), ("U", "Lower tail — allometry vs HV152 (report)"), ("H", "Upper tail (HV-50) — Skarn / Aelari supported search, probes"),
                                 ("K", "Upper tail — Skarn guard (report)"), ("N", "Negative controls (H-1; report)"), ("F", "Frame stress at the proposed endpoints"), ("M", "Composition stress at the proposed endpoints"),
                                 ("Q", "Collision guards (§17 Q6 / Q7 / Q8)"), ("C", "Route / continuity series"), ("G", "Accepted W1 Halvren rows (fixed W1 references; report-level for tail statures)")])
for code, title in NAMES.items():
    cc = [c for c in C if c["code"] == code]
    if not cc: continue
    L.append("## %s — %s\n" % (code, title))
    cnt = collections.Counter(c["result"] for c in cc); L.append("Results: " + ", ".join("%s %d" % kv for kv in sorted(cnt.items())) + "\n")
    rows = []
    for c in cc:
        if code in ("F",) and c["result"] == "PASS" and c["op"] == "L": continue          # length-keeping rows: summarized
        rows.append((c["check"][:150], c["reading"][:60], f(c.get("va")), c["op"], f(c.get("vb")), c["result"], str(c.get("note", ""))[:160]))
    table(["check", "reading", "a", "op", "b", "result", "note"], rows)
    if code == "F":
        lk = [c for c in cc if c["op"] == "L"]; L.append("Length / joint-keeping rows: %d of %d PASS.\n" % (sum(c["result"] == "PASS" for c in lk), len(lk)))
# endpoint anatomy
EP = ["HL147p2C", "HL147p2M", "MF147p2", "HV152", "HV213", "HU217C", "HU219C", "HU219S", "HU219A", "HU228p8S", "SK228p8", "HU220p8A", "AE220p8", "HU228p8SA", "AE221", "HU228p8SD", "HU220p8AD", "HU228p8SAD"]
KEYS = ["stature (cm)", "torso_share", "leg_share", "arm_share", "neck_share", "HH_share", "forearm_over_arm", "shin_over_leg", "femur_over_leg", "hand_share", "foot_share", "finger_over_hand",
        "palm_breadth_over_hand", "thorax_breadth_share", "thorax_depth_share", "span_der"] + ["%s breadth / adjacent segment (exact-plane section)" % j for j in ("elbow", "wrist", "knee", "ankle")] + \
       ["skeletal %s [t=0.0]" % k for k in ("thoracic breadth / stature", "thoracic depth / stature", "shoulder-joint breadth / stature", "biacromial / stature", "crest breadth / stature",
                                            "AP pelvic depth / stature", "pelvic vertical / stature", "hip-joint spacing / stature", "bitrochanteric / crest", "waist interval / torso")]
L.append("## Endpoint / bracket anatomy (complete readings)\n")
eps = [e for e in EP if e in V]
table(["reading"] + eps, [[k.replace(" (exact-plane section)", "").replace(" [t=0.0]", "")] + [f(V[e].get(k), 4 if "stature" not in k or "/" in k else 2) for e in eps] for k in KEYS])
# emulator
L.append("## RM-OT-03 linear response emulator — REJECTED by its own validation (its rates are not used)\n")
val = E["validation"]
table(["reading", "rms rel. error %", "max abs rel. error %"], [(k.replace(" (exact-plane section)", ""), "%.2f" % (100 * v), "%.2f" % (100 * val["max_abs_rel_err"][k])) for k, v in val["rms_rel_err"].items()])
table(["source", "n-sep exact agreement", "class agreement", "n"], [(s, a["exact"], a["class_same"], a["n"]) for s, a in val["nsep_agreement"].items()])
table(["validation body", "stratum", "stature", "hidden coordinates", "n-sep real (MF FN AE VA SK SG)", "n-sep emulated"],
      [(v["id"], v["stratum"], "%.2f" % v["h"], ", ".join("%s %.2f" % kv for kv in v["e"].items()), " ".join(str(v["nsep_real"][s]) for s in ("MF", "FN", "AE", "VA", "SK", "SG")),
        " ".join(str(v["nsep_emul"][s]) for s in ("MF", "FN", "AE", "VA", "SK", "SG"))) for v in val["bodies"]])
table(["probe (not fitted)", "coordinates", "max abs rel. error %", "worst reading"], [(p["id"], ", ".join("%s %.2f" % kv for kv in p["e"].items()), "%.2f" % (100 * max(abs(x) for x in p["rel_err"].values())),
                                                                                     max(p["rel_err"], key=lambda k: abs(p["rel_err"][k])).replace(" (exact-plane section)", "")) for p in val["probes"]])
L.append("## RM-OT-03 — real-build source-passing statistics (17 readings; conservative)\n")
for st, S in RS["strata"].items():
    L.append("### Stratum %s (n = %d real builds)\n" % (st, S["n"]))
    L.append("Accepted %d (95 %% CI %s); rejected as near-duplicate of a matched-height source %d (CI %s); adult-read rejections %d; accepted but ambiguous (2-3 readings) %d (CI %s). Duplication bracket on the supporting-source coordinate: lowest duplicate %s, highest non-duplicate %s. Logistic 50 %% point %s (bootstrap 95 %% %s).\n" % (
        S["accepted"], f(S["accept_ci95"], 3), S["rejected_duplicate_matched"], f(S["dup_ci95"], 3), S["rejected_adult_read"], S["accepted_ambiguous"], f(S["amb_ci95"], 3),
        f(S["duplication_bracket"]["lowest_e_support_duplicate"], 3), f(S["duplication_bracket"]["highest_e_support_non_duplicate"], 3),
        f(S["logistic"]["e50"], 3) if S.get("logistic") else "not estimable (no duplicates or separable)", f(S["logistic"]["e50_boot95"], 3) if S.get("logistic") and S["logistic"].get("e50_boot95") else "-"))
    table(["source", "comparison", "near-duplicate", "95 % CI", "ambiguous 2-3", "distinct >= 4", "n-sep quantiles 0/25/50/75/100"],
          [(s_, p["comparison"], p["near_duplicate"], f(p["near_duplicate_ci95"], 3), p["ambiguous_2_3"], p["distinct"], "/".join("%g" % q for q in p["nsep_quantiles"])) for s_, p in S["per_source"].items()])
    table(["first n samples", "accept", "duplicate (matched)", "95 % CI", "ambiguous"], [(n, "%.3f" % c["accept"], "%.3f" % c["dup_matched"], f(c["dup_ci95"], 3), "%.3f" % c["ambiguous"]) for n, c in S["convergence"].items()])
    table(["supporting-source coordinate", "n", "duplicate (matched)", "ambiguous", "accepted"], [(k, v["n"], v["dup_matched"], v["ambiguous"], v["accepted"]) for k, v in S["frontier"].items()])
L.append("### Real samples\n")
table(["sample", "stratum", "stature", "hidden coordinates", "n-sep MF FN AE VA SK SG", "status"],
      [(x["id"], x["stratum"], "%.2f" % x["h"], ", ".join("%s %.2f" % kv for kv in x["e"].items()), " ".join(str(x["per_source"][s_]["nsep"]) for s_ in ("MF", "FN", "AE", "VA", "SK", "SG")),
        ("REJECT duplicate " + "/".join(x["dup_matched"])) if x["dup_matched"] else ("REJECT adult-read" if x["adult_read_fail"] else ("ACCEPT ambiguous" if x["ambiguous"] else "ACCEPT"))) for x in RS["samples"]])
L.append("## Route / continuity derivative audit\n")
for n, a in AU["derivative_outliers"].items():
    if a: table(["series " + n, "step", "change %", "rate %/cm", "median %/cm"], [(x["reading"][:60], x["step"], "%+.2f" % x["change_pct"], "%+.3f" % x["rate_pct_per_cm"], "%.3f" % x["median_rate"]) for x in a])
L.append("## Upper-tail lower-leg share vs the scored span floor (SG208 %.4f; FAIL threshold %.4f)\n" % (AU["upper_shin_crossing"]["span_floor_SG208"], AU["upper_shin_crossing"]["fail_threshold"]))
table(["class", "points (stature, shin / leg)", "leaves span at", "crosses -1 % at"], [(k, "; ".join("%.1f: %.4f" % tuple(p) for p in v["points"]), f(v["leaves_span_at_cm"], 1) if v["leaves_span_at_cm"] else ("below at first point" if v["first_value_below_floor"] else "-"), f(v["fail_threshold_crossed_at_cm"], 1) if v["fail_threshold_crossed_at_cm"] else "-") for k, v in AU["upper_shin_crossing"]["classes"].items()])
table(["matched supporting source", "shin / leg"], [(k, "%.4f" % v) for k, v in AU["upper_shin_crossing"]["matched_supporting_sources"].items()])
open(OUT, "w").write("\n".join(L)); print("tables", len(L), "lines;", len(con), "construction records")
