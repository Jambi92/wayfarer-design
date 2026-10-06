"""RAC W1f ocular reference work (order §4, §5, §9).
- O-1 landmark orbital-margin rings (orbit_ring.py method, source and placement unchanged) for every listed body:
  ring = MF-M-R source ring x (HL or HH ratio to MF-M-R) x (1 + delta);  delta = 0.03 for FN (O-D2a), 0 otherwise.
  For PK / CG this is the species-scaled adult orbit (Species-Scaled Adult Ocular Anatomy Rule): the MF human orbit carried
  with the population's own head size, i.e. never enlarged relative to the face.
- Physical fit: ring inside skin (parity test), ring-to-globe clearance; landmark globe vs socket skin (eyefit).
- Adult presentation (anti-"huge-eyed child"): landmark globe / HH and ring / head size vs MF-M-R (must not exceed MF by more than
  the 1 % marginal threshold), inter-orbital distance / HL vs MF (reported).
Usage: python3 ocular_w1f.py meas_dir out.json ID..."""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import orbit_ring as O
from arm_measure import load
from eyefit import eyefit

DELTA = {"FN": 0.03}

def main(md, out, ids):
    M = lambda i: json.load(open(os.path.join(md, i + "_meas.json")))["combined"]["cranio"]
    mf = M("MF-M-R"); B0, H0 = O.SRC["male"]
    res = {"source": "Alsaykhan & Abozaid 2025, Int J Morphol 43(3):843-851 (dry adult skulls), male means; placement %.1f cm forward at MF-M-R head size (carried with HH) / %.0f deg (builder-chosen, accepted O-D2a)" % (O.FWD, O.TURN), "bodies": {}}
    mf_iod = float(np.linalg.norm(np.array(mf["OC_l"]) - np.array(mf["OC_r"]))) if "OC_l" in mf else None
    for i in ["MF-M-R"] + [x for x in ids if x != "MF-M-R"]:
        c = M(i); d = load(os.path.join(md, i + "_rest.npz")); dl = DELTA.get(i, 0.0)
        B = B0 * c["HL"] / mf["HL"] * (1 + dl); H = H0 * c["HH"] / mf["HH"] * (1 + dl); g = float(c["eye_diam_cm"])
        r = {"delta": dl, "ring_breadth_cm": B, "ring_height_cm": H, "HL": c["HL"], "HH": c["HH"], "globe_cm": g,
             "ORB_breadth_over_HL": B / c["HL"], "ORB_height_over_HH": H / c["HH"], "globe_over_HH": g / c["HH"]}
        fits = {}; O.FWD = 0.8 * c["HH"] / mf["HH"]; r["ring_forward_cm"] = O.FWD      # placement carried with head size (species-scaled)
        for s in ("l", "r"):
            oc = d["eye_" + s].astype(float); P, cc, ub = O.ring(oc, s, B, H)
            fits[s] = O.fit(d, P, oc, g / 2, 1 if s == "l" else -1)
        r["ring_inside_skin_frac"] = min(fits["l"]["ring_points_inside_skin_frac"], fits["r"]["ring_points_inside_skin_frac"])
        r["ring_globe_clearance_cm"] = min(fits["l"]["min_clearance_to_globe_cm"], fits["r"]["min_clearance_to_globe_cm"])
        ef = eyefit(d, g); r["globe_skin_verts_inside"] = ef["l"]["skin_verts_inside_globe"] + ef["r"]["skin_verts_inside_globe"]
        r["globe_min_skin_clearance_cm"] = min(ef["l"]["min_skin_clearance_cm"], ef["r"]["min_skin_clearance_cm"])
        iod = float(np.linalg.norm(d["eye_l"].astype(float) - d["eye_r"].astype(float))); r["IOD_cm"] = iod; r["IOD_over_HL"] = iod / c["HL"]
        res["bodies"][i] = r
    m = res["bodies"]["MF-M-R"]
    for i, r in res["bodies"].items():
        r["vs_MF"] = {"ORB_breadth": r["ORB_breadth_over_HL"] / m["ORB_breadth_over_HL"], "ORB_height": r["ORB_height_over_HH"] / m["ORB_height_over_HH"],
                      "globe_over_HH": r["globe_over_HH"] / m["globe_over_HH"], "IOD_over_HL": r["IOD_over_HL"] / m["IOD_over_HL"]}
        r["fits"] = bool(r["ring_inside_skin_frac"] == 1.0 and r["ring_globe_clearance_cm"] > 0 and r["globe_skin_verts_inside"] == 0)
        r["globe_over_HH_above_MF_by_more_than_1pct"] = bool(r["vs_MF"]["globe_over_HH"] > 1.01)
        r["orbit_enlarged_vs_MF"] = bool(i != "FN" and (r["vs_MF"]["ORB_breadth"] > 1.01 or r["vs_MF"]["ORB_height"] > 1.01))
    if "MF-F-R" in res["bodies"] and "FN" in res["bodies"]:
        f, w = res["bodies"]["FN"], res["bodies"]["MF-F-R"]
        # MF-F-R ring uses the female source orbit (orbit_ring.py), not the male ring scaled
        wb, wh = O.SRC["female"]; res["FN_vs_MF-F-R"] = {"breadth": f["ORB_breadth_over_HL"] / (wb / w["HL"]), "height": f["ORB_height_over_HH"] / (wh / w["HH"])}
    json.dump(res, open(out, "w"), indent=1, default=float)
    for i, r in res["bodies"].items():
        print(i.ljust(8), "ring %.3f x %.3f  inside %.2f  clr %.2f  globe %.3f in %d  globe/HH x%.3f  ORB b x%.3f h x%.3f  IOD/HL x%.3f  fits %s  globe/HH>MF+1%% %s" % (
            r["ring_breadth_cm"], r["ring_height_cm"], r["ring_inside_skin_frac"], r["ring_globe_clearance_cm"], r["globe_cm"], r["globe_skin_verts_inside"],
            r["vs_MF"]["globe_over_HH"], r["vs_MF"]["ORB_breadth"], r["vs_MF"]["ORB_height"], r["vs_MF"]["IOD_over_HL"], r["fits"], r["globe_over_HH_above_MF_by_more_than_1pct"]))
    if "FN_vs_MF-F-R" in res: print("FN vs MF-F-R", res["FN_vs_MF-F-R"])

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3:])
