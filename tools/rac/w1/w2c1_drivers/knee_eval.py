# RAC W2C1 knee normalization evaluation (exact-plane knee section; the slab-derived 0.575 slope is NOT used).
# Per population: log-log fit of knee breadth / stature on stature over the UNCORRECTED bodies (no knee-correction writes); each
# questioned knee correction is judged leave-one-out (the fit excludes every body at the judged stature): residual of the uncorrected
# and of the corrected body against the fitted expectation. Then re-checks the knee rows of accepted decisions with section knees.
# Usage: python3 knee_eval.py JOINTS.json [JOINTS2.json ...] OUT.json
import sys, json, math
J = {}
for p in sys.argv[1:-1]: J.update(json.load(open(p)))
OUT = sys.argv[-1]
k = lambda n: J[n]["section"]["knee"]; H = lambda n: J[n]["stature"]
POP = {"Marchfolk config 1": ["MFM147-NAT", "MF-M-R", "MFM190", "MFM203"], "Marchfolk config 2": ["MFF147B-NAT", "MF-F-R", "MFF190", "MFF203"],
       "Skarn config 1": ["SKM183", "SKM190", "SKM198", "SKM203", "SK", "SKM218", "SKM229"], "Skarn config 2": ["SKF183", "SKF190", "SKF203", "SKF208", "SKF229N-NAT"],
       "Grask": ["GR198", "GR208", "GR218R", "GR229", "GR239"], "Gorrund (W1 donors / central; diagnostic)": ["GO-H208", "GO217", "GO224", "GO"]}
def fit(names):
    x = [math.log(H(n)) for n in names]; y = [math.log(k(n)) for n in names]; mx, my = sum(x) / len(x), sum(y) / len(y)
    b = sum((a - mx) * (c - my) for a, c in zip(x, y)) / sum((a - mx) ** 2 for a in x); a0 = my - b * mx
    res = [100 * (math.exp(c) / math.exp(a0 + b * a) - 1) for a, c in zip(x, y)]
    return {"slope_share": b, "exponent_absolute": b + 1, "intercept": a0, "n": len(names), "bodies": names, "residual_pct": dict(zip(names, res)), "max_abs_residual_pct": max(abs(r) for r in res)}
pred = lambda f, h: math.exp(f["intercept"] + f["slope_share"] * math.log(h))
out = {"values": {n: {"stature": H(n), "knee_section": k(n), "knee_slab_scaled": J[n]["slab_scaled"]["knee"], "slab_over_section": J[n]["slab_scaled"]["knee"] / k(n)} for n in J}, "fits": {}, "corrections": {}, "rechecks": []}
for p, names in POP.items():
    names = [n for n in names if n in J]; out["fits"][p] = fit(names)
Q = [("MF190 configuration 1 (knee target 0.8)", "Marchfolk config 1", "MFM190", "MFM190K8"), ("MF203 configuration 1 (K6, knee target 0.6)", "Marchfolk config 1", "MFM203", "MFM203K6"),
     ("MF190 configuration 2 (knee target 0.3)", "Marchfolk config 2", "MFF190", "MFF190K3"), ("MF203 configuration 2 (K3, knee target 0.3)", "Marchfolk config 2", "MFF203", "MFF203K3"),
     ("SK229 configuration 1 (W2B1: knee incr 1.0 -> decr 0.5)", "Skarn config 1", "SKM229", "SKM229KD5")]
for name, p, pre, cor in Q:
    names = [n for n in POP[p] if n in J and abs(H(n) - H(pre)) > 0.5]; f = fit(names); e = pred(f, H(pre))
    rp, rc = 100 * (k(pre) / e - 1), 100 * (k(cor) / e - 1)
    verdict = "SUPPORTED (correction moves the knee onto the normalized trend)" if abs(rc) < abs(rp) and abs(rc) < 3 else \
              ("UNNECESSARY / REVERT (the uncorrected body is the more coherent one)" if abs(rp) <= abs(rc) else "PARTIAL (correction closer, but beyond 3 %)")
    out["corrections"][name] = {"population": p, "fit_bodies (leave-one-out)": names, "slope_share": f["slope_share"], "expected_knee": e, "uncorrected": pre, "uncorrected_knee": k(pre), "uncorrected_residual_pct": rp,
                                "corrected": cor, "corrected_knee": k(cor), "corrected_residual_pct": rc, "verdict": verdict}
# accepted knee decisions re-checked with section knees (reverted bodies where the verdict is REVERT)
R = {n: (v["uncorrected"] if v["verdict"].startswith("UNNECESSARY") else v["corrected"]) for n, v in out["corrections"].items()}
mf190m, mf203m, mf190f, mf203f, sk229 = (R[q[0]] for q in Q)
def row(chk, a, op, b, vb=None, note=""):
    va = k(a); vb = k(b) if vb is None else vb; rel = abs(va - vb) / vb; holds = va > vb if op == ">" else va < vb
    out["rechecks"].append({"check": chk, "a": a, "b": b, "va": va, "op": op, "vb": vb, "margin_pct": 100 * (va / vb - 1), "result": ("PASS" if rel >= 0.01 else "NOT DEMONSTRATED") if holds else "FAIL", "note": note})
row("W2B overlap 190 cm config 1: Skarn knee > Marchfolk knee", "SKM190", ">", mf190m); row("W2B overlap 203 cm config 1: Skarn > Marchfolk", "SKM203", ">", mf203m)
row("W2B overlap 190 cm config 2: Skarn > Marchfolk", "SKF190", ">", mf190f); row("W2B overlap 203 cm config 2: Skarn > Marchfolk", "SKF203", ">", mf203f)
fm = out["fits"]["Marchfolk config 1"]; ff = out["fits"]["Marchfolk config 2"]
row("W2B canonical pair config 1: SK 183 > MF 203 carried to 183 cm (normalized MF trend)", "SKM183", ">", mf203m, k(mf203m) * (183 / H(mf203m)) ** fm["slope_share"])
row("W2B canonical pair config 2: SK 183 > MF 203 carried to 183 cm (normalized MF trend)", "SKF183", ">", mf203f, k(mf203f) * (183 / H(mf203f)) ** ff["slope_share"])
row("W2B Narrow Skarn: knee > MF 203 carried to 208 cm (normalized trend)", "SKM183", ">", mf203m, None, "see narrow body rows in W2B (report)") if False else None
row("Gorrund > Grask knee at 208 cm (GO-H208 vs GR 208)", "GO-H208", ">", "GR208"); row("Gorrund > Grask knee at 217-218 cm (GO 217 vs GR 218)", "GO217", ">", "GR218R")
row("W2A1 Narrow Marchfolk (173) knee > Aelari (190) at matched stature (MF carried to 190 cm, normalized MF trend)", "MNX", ">", "AEL1", None)
out["rechecks"][-1]["va"] = k("MNX") * (190 / H("MNX")) ** fm["slope_share"]; v = out["rechecks"][-1]; v["margin_pct"] = 100 * (v["va"] / v["vb"] - 1); v["result"] = "PASS" if v["margin_pct"] >= 1 else ("NOT DEMONSTRATED" if v["margin_pct"] > 0 else "FAIL")
row("Skarn 229 (resolved) knee > Grask 229", sk229, ">", "GR229"); row("Skarn 218 knee > Grask 218", "SKM218", ">", "GR218R")
json.dump(out, open(OUT, "w"), indent=1)
for p, f in out["fits"].items(): print("%-42s slope %+.3f (abs exponent %.3f) n=%d max |res| %.1f%%" % (p, f["slope_share"], f["exponent_absolute"], f["n"], f["max_abs_residual_pct"]))
for n, v in out["corrections"].items(): print("%-55s expected %.4f | uncorrected %.4f (%+.1f%%) | corrected %.4f (%+.1f%%) -> %s" % (n, v["expected_knee"], v["uncorrected_knee"], v["uncorrected_residual_pct"], v["corrected_knee"], v["corrected_residual_pct"], v["verdict"]))
for r in out["rechecks"]: print("%-95s %.4f %s %.4f %+.1f%% %s" % (r["check"][:95], r["va"], r["op"], r["vb"], r["margin_pct"], r["result"]))
