# RAC W3A: route / continuity derivative audit, lower-tail non-uniform-scaling check, separation-vs-stature invariance, and the upper-tail
# coherence crossing (where the lower-leg share leaves the scored boundary-stature span by 1 %), from the evaluator values. NON-CANON diagnostics.
# Usage: python3 w3a_audit.py W3A.json OUT.json
import sys, json, numpy as np
D = json.load(open(sys.argv[1])); V = D["values"]; C = D["checks"]; OUT = {}
st = lambda b: V[b]["stature (cm)"]
SERIES = json.load(open('/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w3a/spec.json'))["series"]
# 1. derivative audit: per-cm rate of each reading per step; a step is a DERIVATIVE OUTLIER when |change| >= 1 % and |rate| > 3x the series median
#    |rate| for that reading (sub-1 % steps are below the measurement class threshold and never flagged)
AUD = {}
for name, ser in SERIES.items():
    ser = [b for b in ser if b in V]; out = []
    for k in V[ser[0]]:
        if k.startswith("stature") or "[t=0.5]" in k or "[t=1.0]" in k: continue
        vals = [V[b].get(k) for b in ser]
        if any(v is None for v in vals): continue
        ch = [vals[i + 1] / vals[i] - 1 for i in range(len(vals) - 1)]; dh = [st(ser[i + 1]) - st(ser[i]) for i in range(len(ser) - 1)]
        rate = [c / max(h, 1e-6) for c, h in zip(ch, dh)]; med = np.median(np.abs(rate)) or 1e-9
        for i, (c, r_) in enumerate(zip(ch, rate)):
            if abs(c) >= 0.01 and abs(r_) > 3 * med: out.append({"reading": k, "step": "%s->%s" % (ser[i], ser[i + 1]), "change_pct": 100 * c, "rate_pct_per_cm": 100 * r_, "median_rate": 100 * med})
    AUD[name] = out
OUT["derivative_outliers"] = AUD
# 2. lower tail is not a uniformly scaled 152 cm Halvren: every ratio of a uniformly scaled body equals HV152's; report the changes
K = [k for k in V["HV152"] if not k.startswith("stature") and "[t=0.5]" not in k and "[t=1.0]" not in k and V.get("HL147p2C", {}).get(k) is not None]
d = {k: 100 * (V["HL147p2C"][k] / V["HV152"][k] - 1) for k in K}
OUT["non_uniform_147p2_vs_152"] = {"n_readings": len(K), "n_changed_ge_0p25pct": sum(abs(v) >= 0.25 for v in d.values()), "n_changed_ge_0p5pct": sum(abs(v) >= 0.5 for v in d.values()),
                                   "largest": sorted(d.items(), key=lambda kv: -abs(kv[1]))[:10], "head_share_pct": d.get("HH_share"),
                                   "native_len_factor_ratio": None}
# 3. Halvren-vs-matched-Marchfolk separation as a function of stature (central and Marchfolk-expressed classes)
sep = {}
for c in C:
    if c["code"] == "L" and "duplicate" in c["check"]: sep[c["a"]] = {"vs": c["b"], "sep": c["va"], "of": int(c["reading"].split()[0]), "result": c["result"]}
OUT["lower_separation_by_stature"] = sep
# 4. upper-tail coherence crossing: lower-leg share vs the scored boundary-stature span floor (SG208 = nearest valid Sagekin adult) - 1 %
floor = V["SG208"]["shin_over_leg"]; thr = floor * 0.99
cross = {}
for cls, ser in (("central", ["HV213", "HU217C", "HU219C", "HU221C", "HU225C", "HU228p8C"]), ("Skarn-expressed", ["HU217S", "HU219S", "HU221S", "HU225S", "HU228p8S"]),
                 ("Aelari-expressed", ["HU217A", "HU219A", "HU220p8A"]), ("Skarn + Aelari", ["HU221SA", "HU225SA", "HU228p8SA"]),
                 ("PROBE Skarn + Skarn leg development", ["HU221SD", "HU225SD", "HU228p8SD"])):
    pts = [(st(b), V[b]["shin_over_leg"]) for b in ser if b in V]; x = None
    for (h0, v0), (h1, v1) in zip(pts, pts[1:]):
        if (v0 - thr) * (v1 - thr) <= 0 and v0 != v1: x = h0 + (thr - v0) * (h1 - h0) / (v1 - v0); break
    marg = None
    for (h0, v0), (h1, v1) in zip(pts, pts[1:]):
        if (v0 - floor) * (v1 - floor) <= 0 and v0 != v1: marg = h0 + (floor - v0) * (h1 - h0) / (v1 - v0); break
    cross[cls] = {"points": pts, "leaves_span_at_cm": marg, "fail_threshold_crossed_at_cm": x, "first_value_below_floor": pts[0][1] < floor}
OUT["upper_shin_crossing"] = {"span_floor_SG208": floor, "fail_threshold": thr, "classes": cross,
                              "matched_supporting_sources": {b: V[b]["shin_over_leg"] for b in ("SK217", "SK219", "SK221", "SK225", "SK228p8", "AE217", "AE219", "AE220p8", "AE221") if b in V}}
json.dump(OUT, open(sys.argv[2], "w"), indent=1)
for n, a in AUD.items(): print(n, len(a), [(x["reading"][:30], x["step"], round(x["change_pct"], 1)) for x in a][:12])
print("non-uniform:", OUT["non_uniform_147p2_vs_152"]["n_changed_ge_0p5pct"], "of", len(K), OUT["non_uniform_147p2_vs_152"]["largest"][:5])
print("crossing:", {k: (v["leaves_span_at_cm"], v["fail_threshold_crossed_at_cm"]) for k, v in cross.items()})
