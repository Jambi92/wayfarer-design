# RAC W1j: summarise a sens7 / sens6 sensitivity JSON (all-preserving count, FAIL count, per-perturbation losses)
import sys, json
def summ(p):
    d = json.load(open(p)); ok = 0; fails = []; lost = {}
    for k, v in d["perturb"].items():
        bad = {kk: a for kk, a in v["not_pass"].items() if a}; tb = v["skin_TB_vs_SK"]
        tbres = "PASS" if tb >= 0.01 else ("NOT DEMONSTRATED" if tb > 0 else "FAIL")    # AD-G10: strict > beyond 1 %; reversed = FAIL
        if any(s.startswith("FAIL") for a in bad.values() for s in a) or tbres == "FAIL": fails.append(k)
        if not bad and tbres == "PASS": ok += 1
        else: lost[k] = {"TB_vs_SK_pct": round(100 * tb, 2), "TB_result": tbres, "rows": bad}
    b = d["base"]; return {"all_preserving": ok, "n": len(d["perturb"]), "fail": fails, "base_not_pass": {k: v for k, v in b["not_pass"].items() if v}, "base_TB_pct": round(100 * b["skin_TB_vs_SK"], 2), "lost": lost}
if __name__ == "__main__":
    for p in sys.argv[1:]:
        s = summ(p); print(p.split('/')[-1], 'all-preserving %d/%d' % (s["all_preserving"], s["n"]), 'FAIL', s["fail"], 'base', s["base_not_pass"], 'TB', s["base_TB_pct"])
        for k, v in s["lost"].items(): print('   ', k, v["TB_vs_SK_pct"], {kk: [x[:55] for x in a] for kk, a in v["rows"].items()})
