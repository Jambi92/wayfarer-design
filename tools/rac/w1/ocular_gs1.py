"""RAC W1g AD-W1G-10 / G-S1: smallest physically sound ADULT ocular geometry for Pipkin and Cogling (Species-Scaled Adult Ocular
Anatomy Rule): search over the landmark globe diameter g at the existing landmark eye centre (socket position unchanged).

Bounds (BUILDER-CHOSEN method, R-14; thresholds come only from the accepted MF-M-R reference and the race's own head size):
  g_max (collision):  largest g with no skin vertex inside the globe (eyefit; clearance >= 0).
  g_cap (adult presentation / anti-enlargement): globe / HH not above MF-M-R by more than the 1 % marginal threshold.
  g_min (aperture backing, species-scaled adult lid relation): the palpebral aperture is the cone of forward directions from the
        eye centre in which no skin is hit. Along N azimuths the aperture margin (lid margin) is found by bisection on the angle
        from the forward axis; its distance m(az) from the eye centre is read. The lids must rest on the globe as in the adult
        human reference: margin gap m(az) - R may not exceed MF-M-R's gap at the same azimuth carried with head height
        (s = HH / HH_MF).  R_min = max over az of [ m(az) - s * (m_MF(az) - R_MF) ].
The viable interval is [g_min, min(g_max, g_cap)]; the G-S1 solution is g_min (smallest physically sound). Globe position, socket
and lids are generator geometry; no anatomy is changed. Usage: python3 ocular_gs1.py meas_dir out.json ID..."""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from arm_measure import load, ray_hits
from eyefit import eyefit

NAZ = 16

def margin(d, side):
    V = d["V"].astype(float); k = d["keep"]; F = d["F"]; F = F[k[F].all(1)]
    e = d["eye_" + side].astype(float); out = []
    for a in np.linspace(0, 2 * np.pi, NAZ, endpoint=False):
        u = np.array([np.cos(a), 0.0, np.sin(a)])          # lateral / vertical component direction
        def ray(th):
            dv = np.array([0, np.cos(th), 0]) + np.sin(th) * u; h = ray_hits(V, F, e, dv / np.linalg.norm(dv)); return h[0] if len(h) else None
        lo, hi = 0.0, np.radians(85)
        if ray(lo) is not None or ray(hi) is None: out.append(None); continue
        for _ in range(22):
            mid = (lo + hi) / 2
            if ray(mid) is None: lo = mid
            else: hi = mid
        out.append(float(ray(hi)))
    return out

def gmax(d, g0):
    lo, hi = 0.2 * g0, 2.0 * g0
    for _ in range(30):
        mid = (lo + hi) / 2; ef = eyefit(d, mid)
        if ef["l"]["skin_verts_inside_globe"] + ef["r"]["skin_verts_inside_globe"] == 0 and min(ef["l"]["min_skin_clearance_cm"], ef["r"]["min_skin_clearance_cm"]) >= 0: lo = mid
        else: hi = mid
    return lo

def main(md, out, ids):
    C = lambda i: json.load(open(os.path.join(md, i + "_meas.json")))["combined"]["cranio"]
    D = lambda i: load(os.path.join(md, i + "_rest.npz"))
    mf = C("MF-M-R"); dmf = D("MF-M-R"); Rm = mf["eye_diam_cm"] / 2
    mm = {s: margin(dmf, s) for s in ("l", "r")}
    res = {"method": __doc__.split("\n\n")[0][:200], "MF-M-R": {"globe_cm": 2 * Rm, "margin_cm": mm, "gap_cm": {s: [None if x is None else x - Rm for x in mm[s]] for s in mm}}, "bodies": {}}
    for i in ids:
        c = C(i); d = D(i); g0 = float(c["eye_diam_cm"]); s = c["HH"] / mf["HH"]
        mi = {sd: margin(d, sd) for sd in ("l", "r")}
        rmin = max(mi[sd][a] - s * (mm[sd][a] - Rm) for sd in ("l", "r") for a in range(NAZ) if mi[sd][a] is not None and mm[sd][a] is not None)
        g_min = 2 * rmin; g_max = gmax(d, g0); g_cap = 1.01 * (mf["eye_diam_cm"] / mf["HH"]) * c["HH"]
        hi = min(g_max, g_cap); ok = g_min <= hi
        ef = eyefit(d, g_min) if ok else None
        r = {"HH": c["HH"], "head_scale_vs_MF": s, "globe_current_cm": g0, "g_min_cm": g_min, "g_max_collision_cm": g_max, "g_cap_adult_cm": g_cap,
             "viable_interval_cm": [g_min, hi] if ok else None, "solution_cm": g_min if ok else None,
             "solution_globe_over_HH_vs_MF": (g_min / c["HH"]) / (mf["eye_diam_cm"] / mf["HH"]) if ok else None,
             "solution_skin_clearance_cm": min(ef["l"]["min_skin_clearance_cm"], ef["r"]["min_skin_clearance_cm"]) if ok else None,
             "current_skin_clearance_cm": min(eyefit(d, g0)["l"]["min_skin_clearance_cm"], eyefit(d, g0)["r"]["min_skin_clearance_cm"]),
             "margin_cm": mi}
        res["bodies"][i] = r
        print(i, "g_min %.3f  g_max %.3f  cap %.3f  current %.3f  interval %s  globe/HH vs MF %.3f  clearance %.3f" % (
            g_min, g_max, g_cap, g0, None if not ok else "[%.3f, %.3f]" % (g_min, hi), r["solution_globe_over_HH_vs_MF"] or 0, r["solution_skin_clearance_cm"] or 0))
    json.dump(res, open(out, "w"), indent=1, default=float)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3:])
