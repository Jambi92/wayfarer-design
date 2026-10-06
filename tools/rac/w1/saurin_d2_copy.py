"""RAC W1 D-2: Saurin MEASUREMENT-ONLY re-posed copy (not an ARM; the frozen closure reference stays canonical).

Only articulated pose changes: each limb segment of each side is rotated rigidly about its proximal joint centre so that left
and right reach the same (mirror-mean) posture; rotations are blended over a band at each joint (skinning-like). Vertex
identity and topology are kept (same vertex order and faces). Head, torso, pelvis and tail vertices outside the blend bands
are untouched. Joint centres and segment axes come from horizontal-section centroids (method below; MEASURER METHOD CHOICE).
Usage: python3 saurin_d2_copy.py saurin_final_base.npz out_dir"""
import sys, os, json, numpy as np

def smooth(t):
    t = np.clip(t, 0, 1); return t * t * (3 - 2 * t)

def rot_between(a, b):
    a = a / np.linalg.norm(a); b = b / np.linalg.norm(b); v = np.cross(a, b); c = a @ b; s = np.linalg.norm(v)
    if s < 1e-12: return np.eye(3)
    K = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return np.eye(3) + K + K @ K * ((1 - c) / s ** 2)

def centroids(V, sel, zs, half=0.4):
    out = []
    for z in zs:
        q = V[sel & (np.abs(V[:, 2] - z) < half)]
        if len(q) > 20: out.append(q.mean(0))
    return np.array(out)

def fit_line(P):
    c = P.mean(0); u, s, vt = np.linalg.svd(P - c); d = vt[0]
    if d[2] > 0: d = -d          # point downward (proximal -> distal)
    return c, d

def point_at_u(c, d, u):
    return c + d * (u - c[2]) / d[2]

def closest(c1, d1, c2, d2):
    w = c1 - c2; a, b, cc, dd, e = d1 @ d1, d1 @ d2, d2 @ d2, d1 @ w, d2 @ w
    den = a * cc - b * b; t = (b * e - cc * dd) / den; s = (a * e - b * dd) / den
    return ((c1 + t * d1) + (c2 + s * d2)) / 2

def chain(V, side, kind):
    x, f, u = V[:, 0], V[:, 1], V[:, 2]
    if kind == "leg":
        sel = (x * side > 4) & (f > -25)
        P1 = centroids(V, sel, np.arange(50, 73, 2)); P2 = centroids(V, sel, np.arange(14, 37, 2))
        c1, d1 = fit_line(P1); c2, d2 = fit_line(P2)
        prox = point_at_u(c1, d1, 84.0); mid = closest(c1, d1, c2, d2); dist = point_at_u(c2, d2, 8.0)
    else:
        sel = (x * side > 24)
        P1 = centroids(V, sel, np.arange(112, 137, 2)); P2 = centroids(V, sel, np.arange(86, 107, 2))
        c1, d1 = fit_line(P1); c2, d2 = fit_line(P2)
        prox = point_at_u(c1, d1, 142.0); mid = closest(c1, d1, c2, d2); dist = point_at_u(c2, d2, 82.0)
    return {"prox": prox, "mid": mid, "dist": dist, "d1": d1, "d2": d2, "n1": len(P1), "n2": len(P2)}

def mirror(v): return v * np.array([-1, 1, 1])

def main(src, out):
    D = np.load(src); V0 = D["v"].astype(np.float64); F = D["f"]
    V = V0.copy(); x, f, u = V0[:, 0], V0[:, 1], V0[:, 2]
    tail = (f < -15) & (u > 55) & (u < 115) & (np.abs(x) < 16)
    rec = {"source_sha256_prefix": None, "chains": {}}
    for kind in ("leg", "arm"):
        CL, CR = chain(V0, 1, kind), chain(V0, -1, kind)
        tgt1 = CL["d1"] + mirror(CR["d1"]); tgt1 /= np.linalg.norm(tgt1)
        tgt2 = CL["d2"] + mirror(CR["d2"]); tgt2 /= np.linalg.norm(tgt2)
        for side, C in ((1, CL), (-1, CR)):
            t1 = tgt1 if side == 1 else mirror(tgt1); t2 = tgt2 if side == 1 else mirror(tgt2)
            R1 = rot_between(C["d1"], t1)
            if kind == "leg":
                region = (x * side > 2) & (u < 90) & ~tail
                w1 = smooth((86.0 - u) / 10.0) * region                     # hip band 76..86
                mid_u = C["mid"][2]; w2 = smooth((mid_u + 4 - u) / 8.0) * region
                w3 = smooth((12.0 - u) / 6.0) * region                     # foot keeps its orientation (plantigrade contact)
            else:
                region = (x * side > 22) & (u < 150) & (u > 60)
                w1 = smooth((146.0 - u) / 10.0) * region
                mid_u = C["mid"][2]; w2 = smooth((mid_u + 4 - u) / 8.0) * region
                w3 = np.zeros(len(V0))
            P = V0 - C["prox"]; Vr1 = C["prox"] + P @ R1.T
            mid1 = C["prox"] + (C["mid"] - C["prox"]) @ R1.T; d2r = R1 @ C["d2"]
            R2 = rot_between(d2r, t2)
            Vr2 = mid1 + (Vr1 - mid1) @ R2.T
            dist2 = mid1 + (C["prox"] + (C["dist"] - C["prox"]) @ R1.T - mid1) @ R2.T
            # foot: undo the combined rotation about the moved ankle (orientation preserved, position follows the shank)
            Rf = (R2 @ R1).T
            Vr3 = dist2 + (Vr2 - dist2) @ Rf.T
            Vn = V0 + w1[:, None] * (Vr1 - V0)
            Vn = Vn + w2[:, None] * (Vr2 - Vr1) * (w1[:, None] > 0)
            Vn = Vn + w3[:, None] * (Vr3 - Vr2) * (w2[:, None] > 0)
            m = region > 0
            V[m] = Vn[m]
            ang1 = np.degrees(np.arccos(np.clip(C["d1"] @ t1, -1, 1))); ang2 = np.degrees(np.arccos(np.clip(d2r @ t2, -1, 1)))
            rec["chains"]["%s_%s" % (kind, "L" if side == 1 else "R")] = {
                "prox": C["prox"].tolist(), "mid": C["mid"].tolist(), "dist": C["dist"].tolist(),
                "seg1_len": float(np.linalg.norm(C["mid"] - C["prox"])), "seg2_len": float(np.linalg.norm(C["dist"] - C["mid"])),
                "rot1_deg": float(ang1), "rot2_deg": float(ang2), "sections": [C["n1"], C["n2"]]}
    V[:, 2] -= V[:, 2].min()
    np.savez_compressed(os.path.join(out, "saurin_d2_measurement_copy.npz"), v=V.astype(np.float32), f=F)
    json.dump(rec, open(os.path.join(out, "saurin_d2_pose.json"), "w"), indent=1)
    return V0, V, F, rec

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
