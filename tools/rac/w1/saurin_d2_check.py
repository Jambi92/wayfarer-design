"""Invariance + bilateral limb readings for the Saurin D-2 measurement copy."""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import saurin_d2_copy as S
from scipy.spatial import cKDTree
def vol(V, F):
    A, B, C = V[F[:, 0]], V[F[:, 1]], V[F[:, 2]]; return abs(np.einsum('ij,ij->i', A, np.cross(B, C)).sum() / 6) / 1000
def regions(V):
    x, f, u = V[:, 0], V[:, 1], V[:, 2]
    return {'head': u > 170, 'tail': (f < -15) & (u < 110) & (u > 60) & (np.abs(x) < 15), 'torso': (u > 105) & (u <= 170) & (np.abs(x) < 20),
            'arms': (u > 80) & (np.abs(x) >= 20), 'legs': (u <= 95) & ~((f < -15) & (np.abs(x) < 15))}
def sym(V):
    M = V.copy(); M[:, 0] *= -1; d, _ = cKDTree(V).query(M, workers=-1); R = regions(V)
    return {k: {"median": float(np.median(d[m])), "p99": float(np.percentile(d[m], 99))} for k, m in R.items()}
def perp_width(V, C, frac, kind, side):
    p = C["prox"] + (C["mid"] - C["prox"]) * frac; ax = (C["mid"] - C["prox"]) / np.linalg.norm(C["mid"] - C["prox"])
    x = V[:, 0]; sel = (x * side > (4 if kind == "leg" else 24))
    q = V[sel] - p; t = q @ ax; q = q[np.abs(t) < 0.4]; q = q[np.linalg.norm(q - np.outer(q @ ax, ax), axis=1) < 12]
    q = q - np.outer(q @ ax, ax); ev, evec = np.linalg.eigh(np.cov(q.T)); w = evec[:, -1]
    return float((q @ w).max() - (q @ w).min())
src, out = sys.argv[1], sys.argv[2]
V0, V1, F, rec = S.main(src, out)
res = {"pose": rec}
res["stature"] = [float(np.ptp(V0[:, 2])), float(np.ptp(V1[:, 2]))]
res["volume_L"] = [vol(V0, F), vol(V1, F)]
R = regions(V0)
dv = np.linalg.norm(V1 - V0, axis=1)
res["max_displacement_cm"] = {k: float(dv[m].max()) for k, m in R.items()}
res["sym_before"] = sym(V0); res["sym_after"] = sym(V1)
read = {}
for kind in ("leg", "arm"):
    for side, nm in ((1, "L"), (-1, "R")):
        c0, c1 = S.chain(V0, side, kind), S.chain(V1, side, kind)
        read["%s_%s" % (kind, nm)] = {
            "seg1_len_before": float(np.linalg.norm(c0["mid"] - c0["prox"])), "seg1_len_after": float(np.linalg.norm(c1["mid"] - c1["prox"])),
            "seg2_len_before": float(np.linalg.norm(c0["dist"] - c0["mid"])), "seg2_len_after": float(np.linalg.norm(c1["dist"] - c1["mid"])),
            "seg1_midwidth_before": perp_width(V0, c0, 0.5, kind, side), "seg1_midwidth_after": perp_width(V1, c1, 0.5, kind, side),
            "dist_point_after": c1["dist"].tolist()}
res["limb_readings"] = read
H = res["stature"][1]
res["limb_shares_after"] = {k: {"seg1_share": v["seg1_len_after"] / H, "seg2_share": v["seg2_len_after"] / H} for k, v in read.items()}
json.dump(res, open(os.path.join(out, "saurin_d2_check.json"), "w"), indent=1)
print(json.dumps({k: res[k] for k in ("stature", "volume_L", "max_displacement_cm")}, indent=0))
for k, v in read.items(): print(k, {a: round(b, 3) for a, b in v.items() if not isinstance(b, list)})
print("sym before", {k: round(v["median"], 3) for k, v in res["sym_before"].items()})
print("sym after ", {k: round(v["median"], 3) for k, v in res["sym_after"].items()})
print({k: (round(v["rot1_deg"], 2), round(v["rot2_deg"], 2)) for k, v in rec["chains"].items()})
