# RAC W1i: dense trunk profile (AD W1i §2): trunk-only plane-section breadth and depth at r = (u - hip joint) / (suprasternal - hip joint),
# r = -0.05 ... 1.0, normalised by stature. Same trunk mask and section method as bony_envelope.fast_stations (W1h).
# Usage (library): profile(path) -> {"r": [...], "b": [...], "d": [...], "H": H}
import sys, json, numpy as np
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1')
from arm_measure import load
R = np.round(np.arange(-0.05, 1.0001, 0.05), 3)

def section(V, TF, z):
    A, B, C = V[TF[:, 0]], V[TF[:, 1]], V[TF[:, 2]]; pts = []
    for a, b in ((A, B), (B, C), (C, A)):
        m = (a[:, 2] - z) * (b[:, 2] - z) < 0; t = (z - a[m, 2]) / (b[m, 2] - a[m, 2]); pts.append(a[m, :2] + (b[m, :2] - a[m, :2]) * t[:, None])
    P = np.vstack(pts)
    return (float(np.ptp(P[:, 0])), float(np.ptp(P[:, 1]))) if len(P) > 5 else (np.nan, np.nan)

def profile(path, rs=R):
    d = load(path); V = d["V"].astype(float); J = d["joints"]; w = lambda k: d["w_" + k]; head = lambda n: np.asarray(J[n][0], float)
    armw = np.maximum.reduce([w(k) for k in ("upperarm_l", "upperarm_r", "lowerarm_l", "lowerarm_r", "hand_l", "hand_r", "fingers_l", "fingers_r")])
    legw = np.maximum.reduce([w(k) for k in ("thigh_l", "thigh_r", "calf_l", "calf_r", "foot_l", "foot_r")])
    trunk = d["keep"] & (armw < 0.2) & (legw < 0.5)
    TF = d["F"][trunk[d["F"]].all(1)]
    hip = (head("thigh_l")[2] + head("thigh_r")[2]) / 2; sst = (head("clavicle_l")[2] + head("clavicle_r")[2]) / 2
    H = float(V[:, 2].max() - V[:, 2].min()); out = {"r": [float(x) for x in rs], "b": [], "d": [], "H": H}
    for r in rs:
        b, dd = section(V, TF, hip + r * (sst - hip)); out["b"].append(b / H); out["d"].append(dd / H)
    return out

if __name__ == "__main__":
    res = {}
    for a in sys.argv[2:]:
        k, p = a.split("=", 1); res[k] = profile(p)
    json.dump(res, open(sys.argv[1], "w"), indent=1)
    print("r     " + " ".join("%6.2f" % r for r in R))
    for k, v in res.items():
        print("%-14s b " % k[:14] + " ".join("%6.4f" % x for x in v["b"]))
        print("%-14s d " % "" + " ".join("%6.4f" % x for x in v["d"]))
