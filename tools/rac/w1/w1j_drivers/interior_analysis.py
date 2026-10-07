# RAC W1j: first-order interior analysis (order §4: demonstrate whether a materially more interior solution exists). For a gn7 point
# (slacks of every W1j constraint, ordinary thresholds) and its Jacobian: (1) the greedy largest set of values whose single +/-2 % steps
# can ALL be tolerated together (linear programme maxmin.lp_set, t >= 1); (2) with that set held at full tolerance, the largest
# tolerance (fraction of 2 %) reachable for the remaining values, jointly and one at a time, and the relations that bind it.
# Usage: python3 interior_analysis.py out.json label=point.json:J.npy ...
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gn7, maxmin
N = gn7.NAMES; out = {}
for a in sys.argv[2:]:
    k, pj = a.split("=", 1); p, j = pj.split(":"); P = json.load(open(p)); J = np.load(j); x0 = np.array(P["x"]); m0 = np.array(P["m"]); lab = P["labels"]
    S, t, x = maxmin.greedy(x0, m0, lab, J, gap=0.02)
    rest = [i for i in range(len(N)) if i not in S]
    t2, x2, b2 = maxmin.lp_two(x0, m0, lab, J, S, rest, gap=0.02)
    single = {}
    for i in rest:
        ti, xi, bi = maxmin.lp_two(x0, m0, lab, J, S, [i], gap=0.02); single[N[i]] = {"tolerance_fraction_of_2pct": ti, "binding": bi[:3] if bi else None}
    out[k] = {"point": dict(zip(N, x0.tolist())), "robust_together": [N[i] for i in S], "not_robust": [N[i] for i in rest],
              "joint_tolerance_of_rest": t2, "joint_binding": b2, "single": single}
    print(k, "robust set", out[k]["robust_together"], "rest", out[k]["not_robust"], "joint t2 %.3f" % t2, {n: round(v["tolerance_fraction_of_2pct"], 3) for n, v in single.items()})
json.dump(out, open(sys.argv[1], "w"), indent=1)
