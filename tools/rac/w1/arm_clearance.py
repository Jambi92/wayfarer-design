"""RAC W1f GR-G3 support reading: does the hanging arm clear the thoracic wall at the R-6 stance (8 deg abduction, no added
abduction)? For each side: minimum distance from upper-arm surface vertices (weight > 0.5, below the shoulder joint) to the trunk
surface (arm weight < 0.05) in the same height band, and the share of upper-arm vertices lying medial of the trunk's lateral
surface at their height (interpenetration proxy). Skin and skeletal-envelope bodies. Diagnostic; GR-G3 itself is a render review.
Usage: python3 arm_clearance.py r6.npz [...]"""
import sys, numpy as np
from arm_measure import load
def clear(p):
    d = load(p); V = d["V"].astype(float); keep = d["keep"]; J = d["joints"]; w = lambda k: d["w_" + k]
    armw = np.maximum.reduce([w(x) for x in ("upperarm_l", "upperarm_r", "lowerarm_l", "lowerarm_r", "hand_l", "hand_r", "fingers_l", "fingers_r")])
    trunk = keep & (armw < 0.05); out = {}
    for s, sg in (("l", 1), ("r", -1)):
        sh = J["upperarm_" + s][0]; el = J["lowerarm_" + s][0]
        ua = keep & (w("upperarm_" + s) > 0.5) & (V[:, 2] < sh[2] - 2) & (V[:, 2] > el[2])
        P = V[ua]; Tz = V[trunk & (V[:, 2] < sh[2] - 2) & (V[:, 2] > el[2]) & (V[:, 0] * sg > 0)]
        from scipy.spatial import cKDTree
        dmin = float(cKDTree(Tz).query(P)[0].min())
        pen = 0
        for z in np.unique(np.round(P[:, 2])):
            tz = Tz[np.abs(Tz[:, 2] - z) < 0.6]; pz = P[np.abs(P[:, 2] - z) < 0.6]
            if len(tz) and len(pz): pen += int(((pz[:, 0] * sg) < (tz[:, 0] * sg).max() - 0.3).sum())
        out[s] = {"min_arm_trunk_gap_cm": dmin, "upperarm_verts_medial_of_trunk_wall": pen, "n_upperarm": int(ua.sum())}
    return out
if __name__ == "__main__":
    for p in sys.argv[1:]: print(p.split("/")[-1], clear(p))
