"""RAC W1f GR-G3 support reading: does the hanging arm clear the thoracic wall at the R-6 stance (8 deg abduction, no added
abduction)? For each side: minimum distance from upper-arm surface vertices (weight > 0.5, below the shoulder joint) to the trunk
surface (arm weight < 0.05) in the same height band, and the share of upper-arm vertices lying medial of the trunk's lateral
surface at their height (interpenetration proxy). Skin and skeletal-envelope bodies. Diagnostic; GR-G3 itself is a render review.
W1g (AD-W1G-4 / -11): adds an INTERPENETRATION test - each upper-arm vertex is tested for lying inside the trunk's own
cross-section polygon at its height (trunk faces = all three vertices with arm weight < 0.05, sliced by the horizontal plane;
2D even-odd rule over the section segments). It is only decidable where the section is CLOSED; near the axilla the trunk-only section
is open (the arm attachment), those vertices are reported as untestable (n_testable_closed_section, testable_band_cm) - the
interpenetration result covers the closed band only (a nearest-vertex normal-side test was tried for the open band and rejected: it
reports the accepted MF and SK as deeply "inside", i.e. it is not valid there). Above the closed band only the W1f vertex-to-vertex
gap (min_arm_trunk_gap_cm) is available. signed_clearance() = minimum over the closed band, both sides. "verts_inside_trunk_section" = 0 means no interpenetration in that band. The W1f "medial of trunk
wall" count compares against the trunk's lateral-most point anywhere at that height and over-reports (kept for before/after).
Usage: python3 arm_clearance.py r6.npz [...]"""
import sys, numpy as np
from arm_measure import load
def inside_section(V, F, trunk, P):
    return int((section_signed(V, F, trunk, P) < 0).sum())

def section(V, TF, z):
    """trunk cross-section at height z: list of 2D segments and whether the polygon is closed (every crossed mesh edge is shared
    by exactly two crossing faces). An open section (gap where the arm joins at the axilla) cannot decide inside / outside."""
    A, B, C = V[TF[:, 0]], V[TF[:, 1]], V[TF[:, 2]]; pts = {}; ekey = {}
    for (a, b, ia, ib) in ((A, B, TF[:, 0], TF[:, 1]), (B, C, TF[:, 1], TF[:, 2]), (C, A, TF[:, 2], TF[:, 0])):
        m = (a[:, 2] - z) * (b[:, 2] - z) < 0
        t = (z - a[m, 2]) / (b[m, 2] - a[m, 2]); q = a[m, :2] + (b[m, :2] - a[m, :2]) * t[:, None]
        for f, qq, e1, e2 in zip(np.where(m)[0], q, ia[m], ib[m]):
            pts.setdefault(f, []).append(qq); k = (min(e1, e2), max(e1, e2)); ekey[k] = ekey.get(k, 0) + 1
    S = np.array([v for v in pts.values() if len(v) == 2])
    closed = len(ekey) > 0 and all(c == 2 for c in ekey.values())
    return S, closed

def section_signed(V, F, trunk, P):
    """signed horizontal distance of each point to the trunk cross-section polygon at its height (negative = inside); NaN where the
    section is open (axilla / arm attachment) so the point cannot be tested"""
    TF = F[trunk[F].all(1)]; out = []; cache = {}
    for p in P:
        z = round(float(p[2]), 2)
        if z not in cache: cache[z] = section(V, TF, p[2])
        S, closed = cache[z]
        if not len(S) or not closed: out.append(np.nan); continue
        a, b = S[:, 0], S[:, 1]
        cr = ((a[:, 1] > p[1]) != (b[:, 1] > p[1]))
        xint = a[cr, 0] + (p[1] - a[cr, 1]) * (b[cr, 0] - a[cr, 0]) / (b[cr, 1] - a[cr, 1])
        ins = (xint > p[0]).sum() % 2 == 1
        ab = b - a; tt = np.clip(((p[:2] - a) * ab).sum(1) / np.maximum((ab ** 2).sum(1), 1e-12), 0, 1)
        dist = np.linalg.norm(a + ab * tt[:, None] - p[:2], axis=1).min()
        out.append(-dist if ins else dist)
    return np.array(out)

def signed_clearance(p):
    """min over both sides of the signed arm-to-trunk-section distance (cm; negative = interpenetration depth)"""
    d = load(p); V = d["V"].astype(float); keep = d["keep"]; J = d["joints"]; w = lambda k: d["w_" + k]
    armw = np.maximum.reduce([w(x) for x in ("upperarm_l", "upperarm_r", "lowerarm_l", "lowerarm_r", "hand_l", "hand_r", "fingers_l", "fingers_r")])
    trunk = keep & (armw < 0.05); r = []
    for s in ("l", "r"):
        sh = J["upperarm_" + s][0]; el = J["lowerarm_" + s][0]
        ua = keep & (w("upperarm_" + s) > 0.5) & (V[:, 2] < sh[2] - 2) & (V[:, 2] > el[2])
        r.append(float(np.nanmin(section_signed(V, d["F"], trunk, V[ua]))))
    return min(r)

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
        ss = section_signed(V, d["F"], trunk, P)
        out[s] = {"min_arm_trunk_gap_cm": dmin, "upperarm_verts_medial_of_trunk_wall": pen, "n_upperarm": int(ua.sum()),
                  "verts_inside_trunk_section": int((ss < 0).sum()),
                  "signed_section_clearance_cm": float(np.nanmin(ss)), "n_testable_closed_section": int(np.isfinite(ss).sum()),
                  "testable_band_cm": [float(np.nanmin(np.where(np.isfinite(ss), P[:, 2], np.nan))), float(np.nanmax(np.where(np.isfinite(ss), P[:, 2], np.nan)))],
                  "shoulder_joint_u": float(sh[2])}
    return out
if __name__ == "__main__":
    for p in sys.argv[1:]: print(p.split("/")[-1], clear(p))
