"""RAC W1f: accepted pelvic / girdle / ALPC relations on the SKELETAL PROXY (PV-D16, AD-G10), combined over the soft-tissue
allowance sweep t = 0, 0.5, 1.0 cm x H/173.14 (skeletal_proxy.py).
Per-t evaluation reuses the W1e check logic (w1e_checks.run, same AD-G10 / PV-D10 result rule) on the skeletal readings, plus the
skeletal-only items the skin route could not run (GO-P2a, ALPC-3). Combination: a row is PASS / MARGINAL / NOT DEMONSTRATED / FAIL
only if every t gives that result; mixed results are reported as T-SENSITIVE (the direction depends on the unmeasured soft-tissue
allowance; counted as not demonstrated).
Usage: python3 skeletal_checks.py skp_dir out.json"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import w1e_checks as W

TS = ("0.0", "0.5", "1.0")

def extra(d):
    L = lambda i: json.load(open(os.path.join(d, i + "_meas.json")))["combined"]
    M = {i: L(i) for i in ("MF-M-R", "SK", "GO", "GR")}
    r = lambda i, k: M[i]["ratio"][k]
    C = []
    def add(c, chk, src, va, op, vb, b):
        rel = abs(va - vb) / max(abs(vb), 1e-9); holds = {">": va > vb, ">=": va >= vb, "<=": va <= vb}[op]
        if op == ">": res = ("PASS" if rel >= 0.01 else "NOT DEMONSTRATED") if holds else "FAIL"
        else: res = "PASS" if holds else ("MARGINAL" if rel < 0.01 else "FAIL")
        C.append({"cand": c, "check": chk, "canon": src, "va": va, "op": op, "vb": vb, "b": b, "result": res, "pass": res != "FAIL", "marginal": res in ("NOT DEMONSTRATED", "MARGINAL")})
    for o in ("MF-M-R", "SK"):
        add("GO", "hip-joint scale (proximal-femur proxy) / crest breadth >= %s (GO-P2a)" % o, "GO-P2a (PV-D14)", r("GO", "hipjoint_scale_over_crest"), ">=", r(o, "hipjoint_scale_over_crest"), o)
    add("GO", "ALPC-3 proximal-femur proxy / S6 breadth >= MF", "GO ALPC-3", r("GO", "prox_femur_over_S6_b"), ">=", r("MF-M-R", "prox_femur_over_S6_b"), "MF")
    add("GO", "ALPC-3 subtrochanteric shaft breadth / femur length >= MF", "GO ALPC-3", r("GO", "shaft_b_over_femur"), ">=", r("MF-M-R", "shaft_b_over_femur"), "MF")
    add("GO", "thoracic breadth / stature > SK (RM-LR-02 a)", "R2 L54; RAC-05 L32", r("GO", "thorax_breadth_share"), ">", r("SK", "thorax_breadth_share"), "SK")
    add("SK", "thoracic breadth / stature > GR (RM-LR-02 a)", "R2 L54", r("SK", "thorax_breadth_share"), ">", r("GR", "thorax_breadth_share"), "GR")
    for o in ("SK", "GR"):
        add("GO", "thoracic depth / stature > %s (RM-LR-02 b)" % o, "R2 L55; RAC-05 L32; GO L42", r("GO", "thorax_depth_share"), ">", r(o, "thorax_depth_share"), o)
    add("GR", "biacromial / thoracic breadth <= MF (GR-G1, acromial landmarks)", "GR-G1 (AD-G10)", r("GR", "biacromial_over_S2_b"), "<=", r("MF-M-R", "biacromial_over_S2_b"), "MF")
    add("GO", "biacromial / thoracic breadth <= MF (ALPC-4, acromial landmarks)", "GO ALPC-4 (AD-G10)", r("GO", "biacromial_over_S2_b"), "<=", r("MF-M-R", "biacromial_over_S2_b"), "MF")
    return C

def run(skp_dir, ids_dir_fmt="t%s"):
    per = {}
    for t in TS:
        d = os.path.join(skp_dir, ids_dir_fmt % t)
        rows = [x for x in W.run(d) if not x["check"].startswith(("hip-joint scale / crest breadth >= MF and >= SK (GO-P2a)", "ALPC-3 pelvis"))]
        per[t] = rows + extra(d)
    out = []
    for i, x in enumerate(per[TS[0]]):
        res = [per[t][i]["result"] for t in TS]
        if len(set(res)) == 1: comb = res[0]
        elif "FAIL" in res or "NOT DEMONSTRATED" in res or "MARGINAL" in res: comb = "T-SENSITIVE"
        else: comb = res[0]
        y = dict(x); y["result"] = comb; y["by_t"] = {t: {"va": per[t][i]["va"], "vb": per[t][i]["vb"], "result": per[t][i]["result"]} for t in TS}
        y["va"] = per["0.5"][i]["va"]; y["vb"] = per["0.5"][i]["vb"]; y["pass"] = None if comb in ("NOT RUN", "REPORT") else comb != "FAIL"
        y["marginal"] = comb in ("NOT DEMONSTRATED", "MARGINAL", "T-SENSITIVE"); y["layer"] = "skeletal proxy (t sweep)"
        out.append(y)
    return out

if __name__ == "__main__":
    C = run(sys.argv[1]); json.dump(C, open(sys.argv[2], "w"), indent=1, default=float)
    from collections import Counter
    print(len(C), "rows;", dict(Counter(c["result"] for c in C)))
    for c in C:
        if c["result"] != "PASS":
            bt = " / ".join("%s:%s" % (t, (round(v["va"], 4) if v["va"] is not None else "-")) for t, v in c["by_t"].items())
            print(c["result"], "|", c["cand"], "|", c["check"], "|", bt, c["op"], None if c["vb"] is None else round(c["vb"], 4))
