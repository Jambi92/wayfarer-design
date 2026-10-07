# RAC W1j femur-robusticity / margin trade study (order §3, §7.1). For each femur ceiling c, the linear model of the latest gn7 iterate
# (Jacobian + slacks of every constraint at that point) is re-optimised with femur <= c: first with the +/-2 % robustness term, then -
# if that cannot be met - with the ordinary thresholds only. The predicted point is then BUILT and checked with the ordinary rule on the
# reference, true 208, 215, 222 and 251 cm bodies and every ALPC-7 pair (sens6.evaluate with the W1j stature series), plus the
# low-composition readings. Usage: python3 femur_trade.py point.json J.npy out.json c1 c2 ...
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gn7, gn6, sens6
from scipy.optimize import minimize

def solve(x0, m0, lab, J, c, robust_on):
    NAMES = gn7.NAMES; i_f = NAMES.index("thigh"); LO, HI = list(gn7.LO), list(gn7.HI); HI[i_f] = c
    def obj(d):
        xn = x0 + d; mm = m0 + J @ d
        rn = gn7.robust(mm, lab, J, xn)[0] if robust_on else mm
        return (np.minimum(0, rn) ** 2).sum() * 1e4 + 0.05 * (d ** 2).sum() + 0.001 * ((xn - 1) ** 2).sum()
    bnds = [(LO[i] - x0[i], HI[i] - x0[i]) for i in range(len(x0))]
    d = minimize(obj, np.zeros(len(x0)), method='L-BFGS-B', bounds=bnds).x
    mm = m0 + J @ d; rn = gn7.robust(mm, lab, J, x0 + d)[0]
    return x0 + d, float(-mm[mm < 0].sum()), float(-rn[rn < 0].sum())

if __name__ == "__main__":
    P = json.load(open(sys.argv[1])); J = np.load(sys.argv[2]); out = sys.argv[3]; cs = [float(c) for c in sys.argv[4:]]
    x0 = np.array(P["x"]); m0 = np.array(P["m"]); lab = P["labels"]; res = {"point": P["x"], "rows": []}
    if os.path.exists(out): res = json.load(open(out))
    for c in cs:
        rec = {"femur_ceiling": c}
        for rb in (True, False):
            x, ord_neg, rob_neg = solve(x0, m0, lab, J, c, rb)
            rec["robust" if rb else "ordinary"] = {"x": x.tolist(), "predicted_ordinary_shortfall": ord_neg, "predicted_robust_shortfall": rob_neg}
        pick = "robust" if rec["robust"]["predicted_ordinary_shortfall"] < 1e-4 else "ordinary"
        x = np.array(rec[pick]["x"]); rec["built"] = pick
        ev = sens6.evaluate(x.tolist(), 'F%d' % round(c * 1000))
        rec["evaluation"] = ev; rec["not_pass_count"] = sum(len(a) for a in ev["not_pass"].values())
        nm = 'F%d' % round(c * 1000); wd = gn6.G + '/sens6'
        rec["low_comp"] = {b: {**gn6.cont(wd + '/grid_%s/%s-C025025_rest.npz' % (b, b)), "waist_rise": gn6.waist_rise(wd + '/grid_%s/%s-C025025_rest.npz' % (b, b))} for b in (nm, nm + '-208')}
        rec["femur"] = float(x[gn7.NAMES.index("thigh")])
        res["rows"].append(rec); json.dump(res, open(out, "w"), indent=1, default=float)
        print(c, pick, 'pred ord %.4f rob %.4f' % (rec[pick]["predicted_ordinary_shortfall"], rec[pick]["predicted_robust_shortfall"]), 'actual not-pass', rec["not_pass_count"], 'TB %.2f' % (100 * ev["skin_TB_vs_SK"]), {k: v for k, v in ev["not_pass"].items() if v}, flush=True)
