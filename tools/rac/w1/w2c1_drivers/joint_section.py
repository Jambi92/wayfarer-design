# RAC W2C1 joint-breadth normalization: elbow, wrist, knee and ankle breadth read on an EXACT PLANE SECTION through the joint centre,
# perpendicular to the same limb axis and over the same vertex set as the accepted slab reading (am_win.jb: elbow — upper arm + forearm,
# axis shoulder->wrist; wrist — forearm + hand, axis elbow->wrist; knee — thigh + calf, axis hip->ankle; ankle — calf + foot, axis
# knee->ankle), faces whose three vertices are in that set; breadth = extent along the section's principal axis (the slab reading's
# metric). Rest anatomy, normalized by the R-6 stature (jbw.py convention). The slab readings (absolute +/-1 cm and stature-scaled) are
# recomputed alongside as the control.   Usage: python3 joint_section.py MODDIR OUT.json PREFIX ...
import sys, os, json, numpy as np
sys.path.insert(0, sys.argv[1]); import am_win as A
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from arm_measure import load
MF = 173.1428; J = ("elbow", "wrist", "knee", "ankle")
def section(V, F, on, c, ax):
    TF = F[on[F].all(1)]; t = (V - c) @ ax; pts = []
    for i, j in ((0, 1), (1, 2), (2, 0)):
        a, b = TF[:, i], TF[:, j]; m = t[a] * t[b] < 0; u = t[a[m]] / (t[a[m]] - t[b[m]]); pts.append(V[a[m]] + (V[b[m]] - V[a[m]]) * u[:, None])
    P = np.vstack(pts) - c; Q = P - np.outer(P @ ax, ax)
    if len(Q) < 4: return float('nan')
    ev, evec = np.linalg.eigh(np.cov(Q.T)); wd = evec[:, -1]; return float((Q @ wd).max() - (Q @ wd).min())
out = {}
for p in sys.argv[3:]:
    A.JBWIN[0] = 1.0; st = A.measure(p + "_r6.npz")["stature"]; r = {"stature": st}
    for mode, win in (("slab_abs", 1.0), ("slab_scaled", st / MF)):
        A.JBWIN[0] = win; m = A.measure(p + "_rest.npz")["mean"]; r[mode] = {k: m[k + "_breadth"] / st for k in J}
    d = load(p + "_rest.npz"); V = d["V"].astype(float); F = d["F"]; keep = d["keep"]; Jt = d["joints"]; w = lambda k: d["w_" + k]; h = lambda n: np.asarray(Jt[n][0], float)
    sec = {k: [] for k in J}
    for s in ("l", "r"):
        sh, el, wr, hp, kn, an = h("upperarm_" + s), h("lowerarm_" + s), h("hand_" + s), h("thigh_" + s), h("calf_" + s), h("foot_" + s)
        u = lambda v: v / np.linalg.norm(v)
        sec["elbow"].append(section(V, F, keep & ((w("upperarm_" + s) + w("lowerarm_" + s)) > 0.3), el, u(wr - sh)))
        sec["wrist"].append(section(V, F, keep & ((w("lowerarm_" + s) + w("hand_" + s)) > 0.3), wr, u(wr - el)))
        sec["knee"].append(section(V, F, keep & ((w("thigh_" + s) + w("calf_" + s)) > 0.3), kn, u(an - hp)))
        sec["ankle"].append(section(V, F, keep & ((w("calf_" + s) + w("foot_" + s)) > 0.3), an, u(an - kn)))
    r["section"] = {k: float(np.mean(v)) / st for k, v in sec.items()}
    out[os.path.basename(p)] = r
    print("%-14s %6.1f | " % (os.path.basename(p)[:14], st) + "  ".join("%s sec %.4f slab %.4f (%.3f)" % (k[:2], r["section"][k], r["slab_scaled"][k], r["slab_scaled"][k] / r["section"][k]) for k in J), flush=True)
json.dump(out, open(sys.argv[2], "w"), indent=1)
