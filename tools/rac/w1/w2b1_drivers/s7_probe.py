# RAC W2B1 diagnostic: S7 (subtrochanteric, 20 % down the femur axis) section on a body's minimum-composition (LEAN) rest mesh, read with the
# accepted mask (thigh weight > 0.5, +/-0.8 cm band) and with sensitivity variants (weight threshold, band). Diagnostic only; no method change.
# Usage: python3 s7_probe.py OUT.json NAME=LEAN_REST.npz ...
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from arm_measure import load
def s7(d, thr=0.5, band=0.8, frac=0.2):
    V = d["V"].astype(float); keep = d["keep"]; J = d["joints"]; th = []
    for sd in ("l", "r"):
        hp, kn = np.asarray(J["thigh_" + sd][0], float), np.asarray(J["calf_" + sd][0], float); L = np.linalg.norm(kn - hp); ax = (kn - hp) / L
        tv = np.where(keep & (d["w_thigh_" + sd] > thr))[0]; P = V[tv] - hp; t = P @ ax; m = np.abs(t - frac * L) < band; Q = P[m] - np.outer(t[m], ax)
        th.append((np.ptp(Q[:, 0]), np.ptp(Q[:, 1]), int(m.sum())))
    a = np.mean(th, axis=0); return {"breadth": float(a[0]), "depth": float(a[1]), "n_vertices": float(a[2])}
out = {}
for arg in sys.argv[2:]:
    n, p = arg.split("=", 1); d = load(p); H = float(d["meta"].get("stature", 0) or 0)
    out[n] = {"%s thr %.1f band %.1f" % (n, t, b): s7(d, t, b) for t in (0.5, 0.4, 0.3) for b in (0.8, 1.5)}
json.dump(out, open(sys.argv[1], "w"), indent=1)
for n, v in out.items():
    print(n, "  ".join("%s: d %.2f (n %d)" % (k.split(" ", 1)[1], x["depth"], x["n_vertices"]) for k, x in v.items()))
