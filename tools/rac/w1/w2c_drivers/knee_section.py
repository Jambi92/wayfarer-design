# RAC W2C DIAGNOSTIC (not an adopted method): knee breadth read on an EXACT PLANE SECTION through the knee joint centre, perpendicular to
# the hip->ankle axis (faces whose three vertices have thigh + calf weight > 0.3, as the slab reading's vertex set), breadth = extent
# along the section's principal axis and along the body's medio-lateral (x) axis. Compares with the accepted stature-scaled slab.
# Usage: python3 knee_section.py OUT.json PREFIX ...   (PREFIX = path without _rest.npz)
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from arm_measure import load
def knee(p):
    d = load(p + '_rest.npz'); V = d["V"].astype(float); F = d["F"]; keep = d["keep"]; J = d["joints"]; w = lambda k: d["w_" + k]; out = []
    H = float(V[keep][:, 2].max() - V[keep][:, 2].min())
    for s in ("l", "r"):
        hp, kn, an = (np.asarray(J[n + "_" + s][0], float) for n in ("thigh", "calf", "foot")); ax = (an - hp) / np.linalg.norm(an - hp)
        on = keep & ((w("thigh_" + s) + w("calf_" + s)) > 0.3); TF = F[on[F].all(1)]; t = (V - kn) @ ax; pts = []
        for i, j in ((0, 1), (1, 2), (2, 0)):
            a, b = TF[:, i], TF[:, j]; m = t[a] * t[b] < 0; u = t[a[m]] / (t[a[m]] - t[b[m]]); pts.append(V[a[m]] + (V[b[m]] - V[a[m]]) * u[:, None])
        P = np.vstack(pts) - kn; Q = P - np.outer(P @ ax, ax)
        ev, evec = np.linalg.eigh(np.cov(Q.T)); wd = evec[:, -1]
        out.append(((Q @ wd).max() - (Q @ wd).min(), np.ptp(Q[:, 0])))
    a = np.mean(out, axis=0); return {"principal_cm": float(a[0]), "ml_x_cm": float(a[1]), "stature_mesh_cm": H}
if __name__ == "__main__":
    res = {os.path.basename(p): knee(p) for p in sys.argv[2:]}
    json.dump(res, open(sys.argv[1], "w"), indent=1)
    for k, v in res.items(): print("%-14s principal %.2f  ml %.2f  /H %.4f %.4f" % (k, v["principal_cm"], v["ml_x_cm"], v["principal_cm"] / v["stature_mesh_cm"], v["ml_x_cm"] / v["stature_mesh_cm"]))
