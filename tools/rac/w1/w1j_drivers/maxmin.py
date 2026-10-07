# RAC W1j: most-interior solution of the linear model (order §4: "if no materially more interior solution exists ... demonstrate
# that"). With the Jacobian J and slacks m0 of a gn7 iterate (every constraint, ordinary thresholds), solve the linear programme
#     maximise t   subject to   m0 + J d >= t * R     for every accepted relation (R = max_i |J_ri| h_i, the first-order loss under
#                                                      the worst single +/-2 % step; h_i = 2 % of value i, ka amplitude 0.05)
#                               m0 + J d >= 0         for every other constraint (continuity, low composition, stature, clearance ...)
#                               LO + gap <= x0 + d <= HI - gap,   |d_i| <= trust
# t = 1 means every single +/-2 % step keeps every relation (to first order); t < 1 means the best possible tolerance is t x 2 %.
# The femur ceiling can be lowered (femur <= c) for the trade study. Usage: python3 maxmin.py point.json J.npy out.json [c] [trust] [gap]
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gn7
from scipy.optimize import linprog

def lp(x0, m0, lab, J, c=None, trust=0.08, gap=0.0, fix=None):
    n = len(x0); NAMES = gn7.NAMES; LO = np.array(gn7.LO, float); HI = np.array(gn7.HI, float)
    if c is not None: HI[NAMES.index("thigh")] = c
    R = np.max(np.abs(J) * gn7.hstep(x0)[None, :], axis=1); mask = np.array([gn7.robust_row(l) for l in lab])
    # variables [d (n), t]; maximise t -> minimise -t
    A = np.hstack([-J, np.where(mask, R, 0.0)[:, None]]); b = m0.copy()
    bounds = [(max(-trust, LO[i] + gap * (HI[i] - LO[i]) - x0[i]), min(trust, HI[i] - gap * (HI[i] - LO[i]) - x0[i])) for i in range(n)] + [(None, 5.0)]
    if fix:
        for k, v in fix.items(): i = NAMES.index(k); bounds[i] = (v - x0[i], v - x0[i])
    bounds = [(lo, hi) if (lo is None or hi is None or lo <= hi) else (hi, hi) for lo, hi in bounds]
    r = linprog(np.r_[np.zeros(n), -1.0], A_ub=A, b_ub=b, bounds=bounds, method="highs")
    if not r.success: return None
    d, t = r.x[:n], r.x[n]; mm = m0 + J @ d
    worst = sorted(((float(mm[k] / R[k]) if R[k] > 0 else 9.0, lab[k]) for k in range(len(lab)) if mask[k]))[:8]
    return {"t": float(t), "x": (x0 + d).tolist(), "binding_relations": worst}

if __name__ == "__main__":
    P = json.load(open(sys.argv[1])); J = np.load(sys.argv[2]); out = sys.argv[3]
    c = float(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[4] != "-" else None
    trust = float(sys.argv[5]) if len(sys.argv) > 5 else 0.08; gap = float(sys.argv[6]) if len(sys.argv) > 6 else 0.0
    r = lp(np.array(P["x"]), np.array(P["m"]), P["labels"], J, c, trust, gap)
    json.dump(r, open(out, "w"), indent=1); print(json.dumps({k: v for k, v in r.items() if k != "x"}, indent=1) if r else "infeasible")
    if r: print(dict(zip(gn7.NAMES, np.round(r["x"], 4).tolist())))

def lp_set(x0, m0, lab, J, S, c=None, trust=0.08, gap=0.02):
    """max t with the robustness term restricted to the parameters in S (one-at-a-time +/-2 % steps of those values only)"""
    Jm = np.zeros_like(J); Jm[:, S] = J[:, S]
    n = len(x0); NAMES = gn7.NAMES; LO = np.array(gn7.LO, float); HI = np.array(gn7.HI, float)
    if c is not None: HI[NAMES.index("thigh")] = c
    R = np.max(np.abs(Jm) * gn7.hstep(x0)[None, :], axis=1); mask = np.array([gn7.robust_row(l) for l in lab])
    A = np.hstack([-J, np.where(mask, R, 0.0)[:, None]])
    bounds = [(max(-trust, LO[i] + gap * (HI[i] - LO[i]) - x0[i]), min(trust, HI[i] - gap * (HI[i] - LO[i]) - x0[i])) for i in range(n)] + [(None, 3.0)]
    bounds = [(lo, hi) if (lo is None or hi is None or lo <= hi) else (hi, hi) for lo, hi in bounds]
    r = linprog(np.r_[np.zeros(n), -1.0], A_ub=A, b_ub=m0, bounds=bounds, method="highs")
    return (float(r.x[n]), (x0 + r.x[:n]).tolist()) if r.success else (-1.0, None)

def greedy(x0, m0, lab, J, c=None, trust=0.08, gap=0.02, need=1.0):
    """largest set S of values whose single +/-2 % steps can all be tolerated together (first order, t >= need)"""
    S = []; cand = list(range(len(x0)))
    while True:
        best = None
        for i in cand:
            t, x = lp_set(x0, m0, lab, J, S + [i], c, trust, gap)
            if t >= need and (best is None or t > best[0]): best = (t, i, x)
        if best is None: break
        S.append(best[1]); cand.remove(best[1])
    t, x = lp_set(x0, m0, lab, J, S, c, trust, gap) if S else (None, x0.tolist())
    return S, t, x

def lp_two(x0, m0, lab, J, S1, S2, c=None, trust=0.08, gap=0.02, t1=1.0, fix=None):
    """keep full +/-2 % first-order robustness (t1) for the values in S1 and maximise the tolerance t2 (fraction of 2 %) for S2"""
    n = len(x0); NAMES = gn7.NAMES; LO = np.array(gn7.LO, float); HI = np.array(gn7.HI, float)
    if c is not None: HI[NAMES.index("thigh")] = c
    mask = np.array([gn7.robust_row(l) for l in lab]); hs = gn7.hstep(x0)[None, :]
    def Rof(S): Jm = np.zeros_like(J); Jm[:, S] = J[:, S]; return np.where(mask, np.max(np.abs(Jm) * hs, axis=1), 0.0)
    R1, R2 = Rof(S1), Rof(S2)
    A = np.vstack([np.hstack([-J, np.zeros((len(m0), 1))]), np.hstack([-J, R2[:, None]])]); b = np.r_[m0 - t1 * R1, m0]
    bounds = [(max(-trust, LO[i] + gap * (HI[i] - LO[i]) - x0[i]), min(trust, HI[i] - gap * (HI[i] - LO[i]) - x0[i])) for i in range(n)] + [(None, 3.0)]
    if fix:
        for k, v in fix.items(): i = NAMES.index(k); bounds[i] = (v - x0[i], v - x0[i])
    bounds = [(lo, hi) if (lo is None or hi is None or lo <= hi) else (hi, hi) for lo, hi in bounds]
    r = linprog(np.r_[np.zeros(n), -1.0], A_ub=A, b_ub=b, bounds=bounds, method="highs")
    if not r.success: return -1.0, None, None
    d = r.x[:n]; mm = m0 + J @ d
    binding = sorted(((float(mm[k] / R2[k]) if R2[k] > 0 else 9.0, lab[k]) for k in range(len(lab)) if mask[k]))[:6]
    return float(r.x[n]), (x0 + d).tolist(), binding
