"""RAC W1e: ear-family reference geometry, SCULPT-DETAIL PASS (author decisions E-D1...E-D6; order §4, §9 item 2).
Same accepted architecture laws and W1 reference-centre magnitudes as W1d (ear_families.py), with anatomical relief added:
helix rim + scapha, Y-shaped antihelix (stem, superior and inferior crura) bounding the triangular fossa, concha split by the
crus of the helix into cymba and cavum, tragus, antitragus and intertragic notch, fleshy lobe. Elven ears keep the same
human-homologous structures (FN L183) with the superior crus and helix carried up into the continuous taper; Grask adds the
folded-cartilage ridge system through the sustained upper body; Gorrund the deep bowl, strong antihelical fold system and broad
non-tapering rim. Adds PK compact-rounded and CG fine-folded (order §4 last paragraph).
Changes required by the author: E-D3 FN-VA projection gap widened (FN projection angle 42 -> 50 deg); E-D4 GO close-set read by
attachment / auricle-body angle (reported separately from the RA §11 total lateral extent).
Every parameter is BUILDER-CHOSEN (W1 reference centres, not population bounds).
Usage: python3 ear_families_v2.py outdir"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ear_families as E1

def smooth(t):
    t = np.clip(t, 0, 1); return t * t * (3 - 2 * t)

BASE = {k: dict(v) for k, v in E1.FAM.items()}
BASE["FN-elven"]["proj"] = 50                               # E-D3 widen FN over VA
# relief detail per family: (antihelix height, crura factor, concha depth, crus-helix height, tragus, antitragus, fold count/amp,
# helix roll height/width, cartilage thickness)
DET = {
 "MF-human":  dict(ah=0.30, crura=1.0, concha=0.85, crus=0.16, trag=0.30, atrag=0.24, folds=(0, 0), helix=(0.30, 0.30), thick=0.30),
 "FN-elven":  dict(ah=0.24, crura=1.0, concha=0.72, crus=0.12, trag=0.24, atrag=0.18, folds=(0, 0), helix=(0.26, 0.26), thick=0.26),
 "AE-elven":  dict(ah=0.23, crura=1.0, concha=0.70, crus=0.12, trag=0.24, atrag=0.18, folds=(0, 0), helix=(0.25, 0.25), thick=0.25),
 "VA-elven":  dict(ah=0.27, crura=1.0, concha=0.76, crus=0.14, trag=0.26, atrag=0.20, folds=(0, 0), helix=(0.28, 0.28), thick=0.29),
 "HV-mixed":  dict(ah=0.28, crura=1.0, concha=0.80, crus=0.15, trag=0.28, atrag=0.22, folds=(0, 0), helix=(0.29, 0.29), thick=0.29),
 "GR-folded": dict(ah=0.30, crura=1.0, concha=0.85, crus=0.16, trag=0.30, atrag=0.24, folds=(4, 0.20), helix=(0.34, 0.34), thick=0.36),
 "GO-bowl":   dict(ah=0.48, crura=1.3, concha=1.50, crus=0.20, trag=0.34, atrag=0.30, folds=(2, 0.14), helix=(0.44, 0.62), thick=0.34),
 "PK-compact": dict(ah=0.26, crura=1.0, concha=0.62, crus=0.14, trag=0.26, atrag=0.20, folds=(0, 0), helix=(0.27, 0.28), thick=0.28),
 "CG-finefolded": dict(ah=0.22, crura=1.1, concha=0.70, crus=0.13, trag=0.20, atrag=0.17, folds=(2, 0.07), helix=(0.20, 0.16), thick=0.18),
}
BASE["PK-compact"] = dict(L=5.0, wb=1.55, taper=None, top=0.48, lobe=0.17, bowl=0, rim=(0, 0), ah=0, folds=(0, 0), proj=18, tilt=12, sweep=0.3, thick=0.28, tragus=True)
BASE["CG-finefolded"] = dict(L=3.7, wb=1.08, taper=None, top=0.52, lobe=0.15, bowl=0, rim=(0, 0), ah=0, folds=(0, 0), proj=20, tilt=14, sweep=0.25, thick=0.18, tragus=True)

def polyline_dist(Y, Z, pts):
    """distance from grid points (Y,Z) to a polyline [(y,z),...] (cm)"""
    best = np.full(Y.shape, 1e9)
    for (y0, z0), (y1, z1) in zip(pts, pts[1:]):
        dy, dz = y1 - y0, z1 - z0; L2 = dy * dy + dz * dz + 1e-12
        t = np.clip(((Y - y0) * dy + (Z - z0) * dz) / L2, 0, 1)
        d = np.hypot(Y - (y0 + t * dy), Z - (z0 + t * dz)); best = np.minimum(best, d)
    return best

def build(name, ns=120, nt=61):
    p = BASE[name]; q = DET[name]
    s = np.linspace(0, 1, ns); t = np.linspace(-1, 1, nt)
    S, T = np.meshgrid(s, t, indexing="ij")
    L = p["L"]; w = E1.width(S, p); wf = 0.38 * w
    ay = p["sweep"] * S ** 2
    Y = ay + np.where(T < 0, T * wf, T * w); Z = L * S
    def pt(ss, tt):                                         # map normalized (s, t) to (y, z) cm
        ww = float(E1.width(np.array(ss), p)); return (p["sweep"] * ss ** 2 + (tt * ww if tt >= 0 else tt * 0.38 * ww), L * ss)
    r = np.abs(T); edge = 1 - r
    hh, hw = q["helix"]; ew = hw / np.maximum(w, 0.05)
    lobe_gate = smooth((S - p["lobe"]) / 0.10)
    helix = hh * (np.exp(-(edge / ew) ** 2) - 0.5 * np.exp(-((edge - 2.3 * ew) / ew) ** 2)) * lobe_gate * smooth((T + 0.3) / 0.3 + (S - 0.55) / 0.08)
    top_s = 0.86 if p["taper"] is None else min(0.97, p["taper"][1] + 0.55 * (1 - p["taper"][1]))
    # antihelix: stem from the antitragus up the posterior body, splitting into superior crus (toward the top) and inferior crus
    stem = [pt(0.24, 0.35), pt(0.36, 0.42), pt(0.50, 0.40)]
    sup = [pt(0.50, 0.40), pt(0.62, 0.36), pt(top_s * 0.92, 0.18)]
    inf = [pt(0.50, 0.40), pt(0.56, 0.05), pt(0.58, -0.40)]
    aw = 0.22 * (L / 6.4) ** 0.5
    ah = q["ah"] * (np.exp(-(polyline_dist(Y, Z, stem) / aw) ** 2) + q["crura"] * np.exp(-(polyline_dist(Y, Z, sup) / (0.85 * aw)) ** 2)
                    + 0.8 * q["crura"] * np.exp(-(polyline_dist(Y, Z, inf) / (0.75 * aw)) ** 2))
    ah = np.minimum(ah, q["ah"] * 1.15)
    # triangular fossa between the crura, scapha already in the helix term
    fossa_c = pt(0.60, 0.12); fos = -0.35 * q["concha"] * np.exp(-((Y - fossa_c[0]) ** 2 + (Z - fossa_c[1]) ** 2) / (0.35 * L / 6.4) ** 2)
    # concha: cavum (lower, larger) and cymba (upper, smaller), separated by the crus of the helix
    cav = pt(0.33, -0.05); cym = pt(0.47, -0.05)
    rc = 0.62 * (L / 6.4) ** 0.6 * (1.25 if name == "GO-bowl" else 1.0)
    concha = -q["concha"] * np.exp(-((Y - cav[0]) ** 2 / (rc * 0.9) ** 2 + (Z - cav[1]) ** 2 / rc ** 2)) \
             - 0.55 * q["concha"] * np.exp(-((Y - cym[0]) ** 2 / (rc * 0.8) ** 2 + (Z - cym[1]) ** 2 / (rc * 0.45) ** 2))
    crus = q["crus"] * np.exp(-(polyline_dist(Y, Z, [pt(0.42, -0.95), pt(0.42, -0.35), pt(0.43, 0.05)]) / (0.12 * L / 6.4)) ** 2)
    trag = q["trag"] * np.exp(-(polyline_dist(Y, Z, [pt(0.27, -0.90), pt(0.33, -0.85)]) / (0.17 * L / 6.4)) ** 2)
    atrag = q["atrag"] * np.exp(-((Y - pt(0.22, 0.40)[0]) ** 2 + (Z - pt(0.22, 0.40)[1]) ** 2) / (0.20 * L / 6.4) ** 2)
    notch = -0.15 * q["concha"] * np.exp(-((Y - pt(0.20, -0.30)[0]) ** 2 + (Z - pt(0.20, -0.30)[1]) ** 2) / (0.18 * L / 6.4) ** 2)
    nf, fa = q["folds"]; folds = 0.0
    if nf:
        folds = fa * np.sin(np.pi * nf * (T + 1) / 2 + 0.4) ** 2 * smooth((S - 0.45) / 0.15) * (1 - smooth((S - (top_s + 0.08)) / 0.06)) * smooth((T + 0.6) / 0.3)
    lobe = 0.20 * (1 - smooth(S / (p["lobe"] * 1.2)))
    X = helix + ah + fos + concha + crus + trag + atrag + notch + folds
    th = q["thick"] + lobe
    front = np.stack([X, Y, Z], -1); back = np.stack([X - th, Y, Z], -1)
    V = np.concatenate([front.reshape(-1, 3), back.reshape(-1, 3)])
    idx = lambda i, j, sd: sd * ns * nt + i * nt + j
    F = []
    for i in range(ns - 1):
        for j in range(nt - 1):
            a, b, c, d = idx(i, j, 0), idx(i + 1, j, 0), idx(i + 1, j + 1, 0), idx(i, j + 1, 0); F += [(a, b, c), (a, c, d)]
            a, b, c, d = idx(i, j, 1), idx(i + 1, j, 1), idx(i + 1, j + 1, 1), idx(i, j + 1, 1); F += [(a, c, b), (a, d, c)]
    ring = [(i, 0) for i in range(ns)] + [(ns - 1, j) for j in range(nt)] + [(i, nt - 1) for i in range(ns - 1, -1, -1)] + [(0, j) for j in range(nt - 1, -1, -1)]
    for (i0, j0), (i1, j1) in zip(ring, ring[1:]):
        a, b = idx(i0, j0, 0), idx(i1, j1, 0); c, d = idx(i1, j1, 1), idx(i0, j0, 1); F += [(a, d, c), (a, c, b)]
    V = np.array(V); F = np.array(F)
    root = front[:, 0][(s > 0.15) & (s < 0.6)].mean(0)
    pr = np.radians(p["proj"]); R = np.array([[np.cos(pr), np.sin(pr), 0], [-np.sin(pr), np.cos(pr), 0], [0, 0, 1]])
    Vr = (V - root) @ R.T
    tl = np.radians(p["tilt"]); Rt = np.array([[1, 0, 0], [0, np.cos(tl), np.sin(tl)], [0, -np.sin(tl), np.cos(tl)]])
    Vr = Vr @ Rt.T
    shift = -Vr[:, 0].min() if Vr[:, 0].min() < 0 else 0.0
    Vr[:, 0] += shift
    return Vr, F, p, q

def body_angle(V, nfront):
    """E-D4: auricle-body angle = angle between the best-fit plane of the front (lateral) surface and the skull plane x = 0."""
    P = V[:nfront]; c = P.mean(0); u, sv, vt = np.linalg.svd(P - c); n = vt[-1]
    return float(np.degrees(np.arccos(min(1.0, abs(n[0])))))

def main(out):
    from PIL import Image, ImageDraw
    os.makedirs(out, exist_ok=True); res = {}; tiles = []
    for name in DET:
        V, F, p, q = build(name)
        lm = E1.landmarks(V, p); lm["auricle_body_angle_deg"] = body_angle(V, len(V) // 2)
        tip = np.array(lm["tip"]); lm["tip_lateral_back_up_cm"] = [float(tip[0]), float(tip[1]), float(tip[2])]
        res[name] = {"outline_params": p, "relief_params": q, "landmarks": lm}
        with open(os.path.join(out, name + ".obj"), "w") as o:
            o.write("".join("v %.4f %.4f %.4f\n" % tuple(v) for v in V)); o.write("".join("f %d %d %d\n" % tuple(f + 1) for f in F))
        span = max(8.0, p["L"] * 1.35)
        lat, post, top = E1.render_views(V, F, size=360, span=span)
        tile = Image.new("RGB", (lat.width + post.width + 10, lat.height + top.height + 40), "white")
        tile.paste(lat, (0, 30)); tile.paste(post, (lat.width + 10, 30)); tile.paste(top, (0, 30 + lat.height + 5))
        ImageDraw.Draw(tile).text((5, 5), "%s  L %.1f cm  total lateral extent %.2f cm  auricle-body angle %.0f deg  (lateral | posterior | above; 1 cm ticks)" % (name, p["L"], lm["auricle_projection_cm"], lm["auricle_body_angle_deg"]), fill=(0, 0, 0))
        tiles.append(tile)
    W = max(t.width for t in tiles); cols = 3; rows = (len(tiles) + cols - 1) // cols; Ht = max(t.height for t in tiles)
    sheet = Image.new("RGB", (W * cols, rows * Ht), "white")
    for k, t in enumerate(tiles): sheet.paste(t, ((k % cols) * W, (k // cols) * Ht))
    sheet.save(os.path.join(out, "ear_families_v2_sheet.jpg"), quality=88)
    json.dump(res, open(os.path.join(out, "ear_families_v2.json"), "w"), indent=1)
    for k, v in res.items():
        lm = v["landmarks"]; print(k.ljust(14), "H %.2f tip %.2f extent %.2f angle %.1f tip(l/b/u) %s" % (lm["auricle_height_cm"], lm["tip_distance_from_root_cm"], lm["auricle_projection_cm"], lm["auricle_body_angle_deg"], [round(x, 2) for x in lm["tip_lateral_back_up_cm"]]))

if __name__ == "__main__":
    main(sys.argv[1])
