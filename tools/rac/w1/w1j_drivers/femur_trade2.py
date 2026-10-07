# RAC W1j femur-robusticity / margin trade study (order §3, §7.1), linear model + verification builds.
# At the W1i point (Jacobian and slacks of every W1j constraint, gn7 run J1 iteration 0) the linear programme of maxmin.lp_two is solved
# with femur <= c, keeping every ordinary threshold, the largest first-order +/-2 % robustness t1 for the 12 lower-trunk / pelvis /
# femur / depth values that W1j found can be made robust together, and the largest tolerance t2 for the upper-thorax group (upper-thorax
# length, kb60, kb80, rib-cage breadth). The predicted point is then BUILT and checked with the ordinary rule on the reference,
# true 208, 215, 222 and 251 cm bodies and every ALPC-7 pair (sens6.evaluate with the W1j stature series), plus low composition.
# Usage: python3 femur_trade2.py point.json J.npy out.json gap trust c1 c2 ...
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gn7, gn6, sens6, maxmin
N = gn7.NAMES; S4 = [N.index(k) for k in ("s03Y", "kb60", "kb80", "thorX")]; S12 = [i for i in range(len(N)) if i not in S4]

if __name__ == "__main__":
    P = json.load(open(sys.argv[1])); J = np.load(sys.argv[2]); out = sys.argv[3]; gap = float(sys.argv[4]); trust = float(sys.argv[5])
    x0 = np.array(P["x"]); m0 = np.array(P["m"]); lab = P["labels"]
    res = json.load(open(out)) if os.path.exists(out) else {"point": P["x"], "gap": gap, "trust": trust, "rows": []}
    for c in [float(v) for v in sys.argv[6:]]:
        rec = {"femur_ceiling": c, "t1": None}
        for t1 in (1.0, 0.75, 0.5, 0.25, 0.0):
            t2, x, b = maxmin.lp_two(x0, m0, lab, J, S12, S4, c=c, gap=gap, t1=t1, trust=trust)
            if t2 >= 0: rec.update({"t1": t1, "t2": t2, "x": x, "predicted_binding": b}); break
        if rec["t1"] is None:
            rec["note"] = "linear model: no point meets every ordinary threshold with femur <= ceiling (gap %.2f, trust %.2f)" % (gap, trust)
            res["rows"].append(rec); json.dump(res, open(out, "w"), indent=1, default=float); print(c, rec["note"], flush=True); continue
        nm = 'F%d' % round(c * 1000); ev = sens6.evaluate(rec["x"], nm); wd = gn6.G + '/sens6'
        rec["evaluation"] = ev; rec["not_pass_count"] = sum(len(a) for a in ev["not_pass"].values()); rec["femur"] = rec["x"][N.index("thigh")]
        rec["low_comp"] = {b: {**gn6.cont(wd + '/grid_%s/%s-C025025_rest.npz' % (b, b)), "waist_rise": gn6.waist_rise(wd + '/grid_%s/%s-C025025_rest.npz' % (b, b))} for b in (nm, nm + '-208')}
        res["rows"].append(rec); json.dump(res, open(out, "w"), indent=1, default=float)
        print(c, 'femur %.3f t1 %.2f t2 %.3f' % (rec["femur"], rec["t1"], rec["t2"]), 'actual not-pass', rec["not_pass_count"], 'TB %.2f' % (100 * ev["skin_TB_vs_SK"]), {k: v for k, v in ev["not_pass"].items() if v}, flush=True)
