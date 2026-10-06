"""RAC W1e: landmark orbital-margin rings (author decision O-1): purpose-built S-surrogate for the bony orbital aperture.
NOT a skull. The ring is an ellipse (breadth Ec-Mf x height) in a plane facing anterolaterally, centred in front of the globe.

MF source (documented adult-human dry-skull orbit, O-D2): Alsaykhan & Abozaid 2025, Int J Morphol 43(3):843-851, males (n=22):
orbital height 35.59 +/- 1.72 mm, breadth 42.16 +/- 1.85 mm; females (n=20): 34.83 +/- 1.57 mm, 41.00 +/- 1.66 mm.
(Corroborating values cited there: Fetouh & Mandour 2014, 35.57 / 43.25 mm male, 35.12 / 42.37 mm female.)
BUILDER-CHOSEN placement: centre 0.8 cm anterior of the globe centre; plane turned 20 deg so the lateral margin lies posterior;
breadth axis horizontal; ring in the plane. FN: MF ring x head-size ratio (HL for breadth, HH for height) x (1 + delta).
Usage: python3 orbit_ring.py meas_dir out.json [delta]"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from arm_measure import load, ray_hits

SRC = {"male": (4.216, 3.559), "female": (4.100, 3.483)}     # cm (breadth, height)
FWD, TURN = 0.8, 20.0

def ring(oc, side, B, H, n=72):
    sgn = 1 if side == "l" else -1                          # +x = subject's left
    ub = np.array([np.cos(np.radians(TURN)) * sgn, -np.sin(np.radians(TURN)), 0.0])   # lateral, turned back laterally
    uh = np.array([0.0, 0.0, 1.0])
    c = oc + np.array([0.0, FWD, 0.0])
    a = np.linspace(0, 2 * np.pi, n, endpoint=False)
    P = c + np.outer(np.cos(a) * B / 2, ub) + np.outer(np.sin(a) * H / 2, uh)
    return P, c, ub

def inside(V, F, p, sgn):
    """closed-mesh parity test along the outward lateral direction (avoids crossing the opposite orbit pocket)"""
    return len(ray_hits(V, F, p, np.array([1.0 * sgn, 0.0, 0.0]))) % 2 == 1

def fit(d, P, oc, R, sgn):
    V = d["V"].astype(float); F = d["F"]
    near = np.where(np.linalg.norm(V - oc, axis=1) < 8)[0]; Fm = F[np.isin(F, near).all(1)]
    ins = [inside(V, Fm, p, sgn) for p in P]
    clear = np.linalg.norm(P - oc, axis=1).min() - R
    return {"ring_points_inside_skin_frac": float(np.mean(ins)), "min_clearance_to_globe_cm": float(clear)}

def main(md, out, delta):
    res = {"source": "Alsaykhan & Abozaid 2025, Int J Morphol 43(3):843-851 (dry adult skulls)", "placement": {"forward_cm": FWD, "turn_deg": TURN}}
    M = {i: json.load(open(os.path.join(md, i + "_meas.json"))) for i in ("MF-M-R", "MF-F-R", "FN")}
    for i, srcsex, base in (("MF-M-R", "male", None), ("MF-F-R", "female", None), ("FN", None, "MF-M-R")):
        c = M[i]["combined"]["cranio"]; HL, HH = c["HL"], c["HH"]
        if base is None:
            B, H = SRC[srcsex]
        else:
            cb = M[base]["combined"]["cranio"]; B0, H0 = SRC["male"]
            B = B0 * HL / cb["HL"] * (1 + delta); H = H0 * HH / cb["HH"] * (1 + delta)
        d = load(os.path.join(md, i + "_rest.npz")) if os.path.exists(os.path.join(md, i + "_rest.npz")) else None
        r = {"breadth_cm": B, "height_cm": H, "HL": HL, "HH": HH, "ORB_breadth_over_HL": B / HL, "ORB_height_over_HH": H / HH}
        if d is not None:
            for s in ("l", "r"):
                oc = d["eye_" + s].astype(float); P, cc, ub = ring(oc, s, B, H)
                r["fit_" + s] = fit(d, P, oc, c["eye_diam_cm"] / 2, 1 if s == "l" else -1)
                r["ring_" + s] = P.tolist()
        res[i] = r
    mf = res["MF-M-R"]; fn = res["FN"]
    res["FN_vs_MF"] = {"breadth_ratio": fn["ORB_breadth_over_HL"] / mf["ORB_breadth_over_HL"], "height_ratio": fn["ORB_height_over_HH"] / mf["ORB_height_over_HH"], "delta": delta}
    # measurement uncertainty of the normalised readings (ring exact): HL from FAL/Op repeatability, HH from Me placement
    res["uncertainty"] = {"HL_rel": 0.03 / mf["HL"], "HH_rel": 0.10 / mf["HH"],
                          "note": "FAL/Op top-20 spread ~0.02-0.03 cm (W1c evidence); Me placement +/-0.1 cm (chin-contour sampling). Ring geometry itself is exact."}
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps({k: v for k, v in res.items() if k in ("FN_vs_MF", "uncertainty")}, indent=1))
    for i in ("MF-M-R", "MF-F-R", "FN"):
        print(i, {k: (round(v, 4) if isinstance(v, float) else v) for k, v in res[i].items() if not k.startswith("ring")})

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 0.02)
