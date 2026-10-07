# RAC W1j: how much of the upper-thorax tolerance limit (interior_analysis.py) comes from the search bounds / gap / trust region rather
# than from the competing relations. Re-runs maxmin.lp_two (12 robust values at full +/-2 % tolerance, maximal joint tolerance for the
# upper-thorax group) with: (a) the 2 % gap, (b) no gap, (c) all search bounds widened by 0.5 and trust 0.25. Lists the active limits.
# Usage: python3 interior_bounds.py out.json label=point.json:J.npy ...
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gn7, maxmin
N = gn7.NAMES; S4 = [N.index(k) for k in ("s03Y", "kb60", "kb80", "thorX")]; S12 = [i for i in range(len(N)) if i not in S4]; out = {}
LO0, HI0 = list(gn7.LO), list(gn7.HI)
for a in sys.argv[2:]:
    k, pj = a.split("=", 1); p, j = pj.split(":"); P = json.load(open(p)); J = np.load(j); x0 = np.array(P["x"]); m0 = np.array(P["m"]); lab = P["labels"]; rec = {}
    for case, gap, trust, widen in (("2 % gap, trust 0.08", 0.02, 0.08, 0.0), ("no gap, trust 0.08", 0.0, 0.08, 0.0), ("bounds widened by 0.5, trust 0.25", 0.0, 0.25, 0.5)):
        gn7.LO[:] = [v - widen for v in LO0]; gn7.HI[:] = [v + widen for v in HI0]
        t2, x, b = maxmin.lp_two(x0, m0, lab, J, S12, S4, gap=gap, trust=trust)
        act = []
        if x is not None:
            for i, n in enumerate(N):
                lo = gn7.LO[i] + gap * (gn7.HI[i] - gn7.LO[i]); hi = gn7.HI[i] - gap * (gn7.HI[i] - gn7.LO[i])
                if abs(x[i] - lo) < 1e-6 or abs(x[i] - hi) < 1e-6: act.append(n + " (search bound)")
                elif abs(abs(x[i] - x0[i]) - trust) < 1e-6: act.append(n + " (trust limit)")
        rec[case] = {"joint_tolerance_fraction_of_2pct": t2, "x": x, "active_limits": act, "binding_relations": b}
        print(k, '|', case, '| t2 %.3f' % t2, '| active', act, '| binding', [(round(t, 3), l[:50]) for t, l in (b or [])[:3]])
    gn7.LO[:] = LO0; gn7.HI[:] = HI0; out[k] = rec
json.dump(out, open(sys.argv[1], "w"), indent=1)
