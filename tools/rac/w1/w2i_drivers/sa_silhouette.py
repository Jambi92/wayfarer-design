# RAC W2I SAU-SILHOUETTE (measurable part): in the straight-front orthographic projection, how much of the free tail shows through the gap between
# the thighs below the crotch line. Crotch = highest point of the inter-thigh gap at x = 0 (lowest non-tail torso / leg vertex near the midline).
# For each 1-cm level below the crotch, the gap is the open interval between the inner thigh boundaries; the tail's projected x-extent inside that
# gap is counted. Reports covered gap area (cm^2), vertical extent and share of the gap area. Carriage variants use the validated §256.8 range
# (+8 deg lift ... +10 deg droop). Diagnostic only (the free tail carriage is later posture / animation work, §256.8 / §172).
# Usage: python3 sa_silhouette.py OUT.json
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_build as B
C = B.C; L = B.L; H0 = B.H0
def front_tail(P):
    x, f, u = P.T; tail = L.tail > 0.5; body = (L.tail < 0.2) & (L.arm < 0.2)
    near = body & (np.abs(x) < 3.0) & (u < 0.6 * u.max()) & (u > 0.25 * u.max())
    crotch = u[near].min() if near.any() else None
    out = dict(crotch_u=float(crotch)); A = 0.0; Ag = 0.0; lo = None
    for lev in np.arange(np.floor(crotch) - 1, 0, -1.0):
        m = body & (np.abs(u - lev) < 0.5)
        xl = x[m & (x > 0)]; xr = x[m & (x < 0)]
        if len(xl) < 5 or len(xr) < 5: continue
        gl, gr = xl.min(), xr.max()                 # inner thigh boundaries at this level
        if gl <= gr: continue
        Ag += gl - gr
        t = tail & (np.abs(u - lev) < 0.5) & (x < gl) & (x > gr)
        if t.any():
            w = min(x[t].max(), gl) - max(x[t].min(), gr); A += max(w, 0.0); lo = lev
    out.update(covered_area_cm2=A, gap_area_cm2=Ag, covered_share=A / Ag if Ag else None, lowest_visible_u=lo, visible_extent_cm=(crotch - lo) if lo is not None else 0.0)
    return out
CASES = [("SA-M188", {}, H0), ("SA-F188", B.CEN, H0), ("SA-M168", {}, 168.0), ("SA-M208", {}, 208.0), ("SA-M188-T55", B.tail(55, 0.85), H0), ("SA-M188-T78", B.tail(78, 1.15), H0),
         ("SA-M188-carriage-lift8", {'tail_curv': -8.0}, H0), ("SA-M188-carriage-droop10", {'tail_curv': 10.0}, H0), ("SA-M188-B", B.BRD, H0), ("SA-M188-N", B.NAR, H0)]
if __name__ == '__main__':
    R = {}
    for cid, p, h in CASES:
        P, q = C.build(p); P2, q2, k = B.at_stature(P, q, h); R[cid] = front_tail(P2); print(cid, {a: (round(b, 3) if isinstance(b, float) else b) for a, b in R[cid].items()}, flush=True)
    json.dump(R, open(sys.argv[1], 'w'), indent=1, default=float)
