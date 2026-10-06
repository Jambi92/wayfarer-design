"""Fenn bony-orbit packet: compare orbit proxies on MF-M-R vs FN (and other candidates). DIAGNOSTIC; no proxy here is bone.
P1 rim-crest proxy: frontal depth map of the skin around each eye; along 24 radial directions from the eye centre the orbital
   margin is taken as the most convex point (minimum second derivative of depth, smoothed) beyond the visible aperture edge.
   Orbit breadth = horizontal span of the rim at 0/180 deg; height = vertical span at 90/270 deg (mean of +/-15 deg rays).
P2 socket-capacity proxy: diameter of the largest globe that fits at the generator eye centre without skin intersection.
P3 generator socket helper extent (the generator's own eye-socket definition; drives the DER globe).
P4 the W1c Ec*/Mf* soft-tissue proxy (already reported).
Each is normalised by HL (breadth) or HH (height) from the candidate's W1c measurement.
Usage: python3 orbit_rim.py <evidence dir> ID [ID ...]"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from arm_measure import load

def depth_map(V, F, keep, c, half=3.6, step=0.05):
    near = np.where(keep & (np.linalg.norm(V[:, [0, 2]] - c[[0, 2]], axis=1) < half + 1.5) & (V[:, 1] > c[1] - 4))[0]
    Fm = F[np.isin(F, near).all(1)]
    A, B, C = V[Fm[:, 0]], V[Fm[:, 1]], V[Fm[:, 2]]
    xs = np.arange(c[0] - half, c[0] + half + 1e-9, step); zs = np.arange(c[2] - half, c[2] + half + 1e-9, step)
    D = np.full((len(zs), len(xs)), np.nan)
    # orthographic rays along -f: barycentric test in the x-z plane, take max f (front-most) per pixel
    for t in range(len(Fm)):
        a, b, cc = A[t], B[t], C[t]
        xmin, xmax = min(a[0], b[0], cc[0]), max(a[0], b[0], cc[0]); zmin, zmax = min(a[2], b[2], cc[2]), max(a[2], b[2], cc[2])
        i0, i1 = np.searchsorted(xs, xmin), np.searchsorted(xs, xmax, "right"); k0, k1 = np.searchsorted(zs, zmin), np.searchsorted(zs, zmax, "right")
        if i0 >= i1 or k0 >= k1: continue
        gx, gz = np.meshgrid(xs[i0:i1], zs[k0:k1])
        den = (b[2] - cc[2]) * (a[0] - cc[0]) + (cc[0] - b[0]) * (a[2] - cc[2])
        if abs(den) < 1e-12: continue
        w1 = ((b[2] - cc[2]) * (gx - cc[0]) + (cc[0] - b[0]) * (gz - cc[2])) / den
        w2 = ((cc[2] - a[2]) * (gx - cc[0]) + (a[0] - cc[0]) * (gz - cc[2])) / den; w3 = 1 - w1 - w2
        m = (w1 >= 0) & (w2 >= 0) & (w3 >= 0)
        if not m.any(): continue
        f = w1 * a[1] + w2 * b[1] + w3 * cc[1]
        sub = D[k0:k1, i0:i1]; cur = np.where(np.isnan(sub), -1e9, sub)
        sub[m] = np.maximum(cur[m], f[m]); D[k0:k1, i0:i1] = sub
    return xs, zs, D

def rim(d, side, R_globe, smooth=0.25):
    V = d["V"].astype(float); F = d["F"]; keep = d["keep"]; c = d["eye_" + side].astype(float)
    xs, zs, D = depth_map(V, F, keep, c)
    # globe visibility: the globe's front surface; pixels where skin is behind the globe front are 'aperture'
    rr = np.arange(0.4, 3.5, 0.05); out = {}
    ang = np.radians(np.arange(0, 360, 15))
    pts = []
    for th in ang:
        X = c[0] + rr * np.cos(th); Z = c[2] + rr * np.sin(th)
        ix = np.clip(np.round((X - xs[0]) / 0.05).astype(int), 0, len(xs) - 1); iz = np.clip(np.round((Z - zs[0]) / 0.05).astype(int), 0, len(zs) - 1)
        p = D[iz, ix]
        if np.isnan(p).any():
            good = ~np.isnan(p); p = np.interp(rr, rr[good], p[good]) if good.sum() > 3 else p
        # aperture edge: first r where the skin is in front of the globe surface position (or beyond the globe radius)
        g = c[1] + np.sqrt(np.clip(R_globe ** 2 - rr ** 2, 0, None))
        edge_i = np.argmax((p > g + 0.05) | (rr > R_globe))
        k = max(1, int(round(smooth / 0.05)))
        ps = np.convolve(np.pad(p, k, mode="edge"), np.ones(2 * k + 1) / (2 * k + 1), mode="valid")
        d2 = np.gradient(np.gradient(ps, 0.05), 0.05)
        lo = edge_i + 2 * k + 2; hi = len(rr) - 2 * k - 2
        if hi <= lo: pts.append(None); continue
        j = lo + int(np.argmin(d2[lo:hi]))
        pts.append((th, rr[j], X[j], Z[j], ps[j]))
    def span(deg_a, deg_b, axis):
        A = [p for p in pts if p and min(abs(np.degrees(p[0]) - deg_a), 360 - abs(np.degrees(p[0]) - deg_a)) <= 15]
        B = [p for p in pts if p and min(abs(np.degrees(p[0]) - deg_b), 360 - abs(np.degrees(p[0]) - deg_b)) <= 15]
        if not A or not B: return float("nan"), float("nan")
        va = [p[2 if axis == "x" else 3] for p in A]; vb = [p[2 if axis == "x" else 3] for p in B]
        vals = [abs(a - b) for a in va for b in vb]
        return float(np.mean(vals)), float(np.std(vals))
    br, br_sd = span(0, 180, "x"); ht, ht_sd = span(90, 270, "z")
    return {"rim_breadth": br, "rim_breadth_sd": br_sd, "rim_height": ht, "rim_height_sd": ht_sd,
            "rim_radii_cm": [round(p[1], 2) if p else None for p in pts]}

def capacity(d, side):
    V = d["V"].astype(float); k = d["keep"]; c = d["eye_" + side].astype(float)
    return float(2 * np.linalg.norm(V[k] - c, axis=1).min())

def main(ev, ids):
    res = {}
    for i in ids:
        d = load(os.path.join(ev, "geometry", i + "_r6.npz"))
        m = json.load(open(os.path.join(ev, i + "_meas.json")))["combined"]["cranio"]
        HL, HH, R = m["HL"], m["HH"], m["eye_diam_cm"] / 2
        r = {"HL": HL, "HH": HH}
        for s in ("l", "r"):
            r["P1_" + s] = rim(d, s, R)
            r["P2_socket_capacity_" + s] = capacity(d, s)
        r["P3_helper_ext"] = float(d["helper_eye_ext"])
        b = np.nanmean([r["P1_l"]["rim_breadth"], r["P1_r"]["rim_breadth"]]); h = np.nanmean([r["P1_l"]["rim_height"], r["P1_r"]["rim_height"]])
        r["P1_breadth_over_HL"] = b / HL; r["P1_height_over_HH"] = h / HH
        r["P2_over_HL"] = r["P2_socket_capacity_l"] / HL; r["P3_over_HL"] = r["P3_helper_ext"] / HL
        r["P4_breadth_over_HL"] = m["ORB_breadth_over_HL"]; r["P4_height_over_HH"] = m["ORB_height_over_HH"]
        ap = m["aperture"]; r["aperture_h"] = (ap["l"]["height"] + ap["r"]["height"]) / 2; r["aperture_w"] = (ap["l"]["width"] + ap["r"]["width"]) / 2
        res[i] = r
    return res

if __name__ == "__main__":
    ev = sys.argv[1]; res = main(ev, sys.argv[2:])
    json.dump(res, open(os.path.join(ev, "orbit_proxies.json"), "w"), indent=1, default=float)
    for i, r in res.items():
        print(i, "P1 b/HL %.4f (sd %.3f cm) h/HH %.4f (sd %.3f) | P2 %.3f cm /HL %.4f | P3/HL %.4f | P4 b/HL %.4f h/HH %.4f | ap %.2fx%.2f" % (
            r["P1_breadth_over_HL"], r["P1_l"]["rim_breadth_sd"], r["P1_height_over_HH"], r["P1_l"]["rim_height_sd"], r["P2_socket_capacity_l"], r["P2_over_HL"],
            r["P3_over_HL"], r["P4_breadth_over_HL"], r["P4_height_over_HH"], r["aperture_w"], r["aperture_h"]))
        print("   rim radii L", r["P1_l"]["rim_radii_cm"])
