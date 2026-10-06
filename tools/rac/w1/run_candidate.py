"""Post-build processing of one candidate: measurements (anatomy on the generator-authored rest geometry, stature in R-6),
pose-invariance record, pitch sensitivity, evidence sheet. Usage: python3 run_candidate.py outdir ID [eye_ref_npz]"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from arm_measure import measure, load
import invariance, evidence
from eyefit import eyefit
out, cid = sys.argv[1], sys.argv[2]
ref = sys.argv[3] if len(sys.argv) > 3 else os.path.join(out, "MF-M-R_rest.npz")
ext = float(np.load(ref)["helper_eye_ext"])
_cfgp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cfg", cid + ".json")
_ov = json.load(open(_cfgp)).get("eye_diam_cm") if os.path.exists(_cfgp) else None
if _ov:   # author ruling (W1c acceptance §2): fitting ordinary human landmark globe instead of the generator-derived size
    ext = 2.4 * float(np.load(os.path.join(out, cid + "_rest.npz"))["helper_eye_ext"]) / _ov
rest, r6 = os.path.join(out, cid + "_rest.npz"), os.path.join(out, cid + "_r6.npz")
mr = measure(rest, 0.0, ext); m6 = measure(r6, 0.0, ext)
H = m6["stature"]
res = {"id": cid, "stature_r6": H, "stature_rest": mr["stature"], "rest": mr, "r6": m6}
# combined record: anatomy from rest, shares to the R-6 stature
comb = {k: v for k, v in mr.items() if k not in ("ratio",)}
comb["stature"] = H
rat = dict(mr["ratio"])
for k in list(rat):
    pass
# recompute stature shares with R-6 stature
share_keys = {"torso_share": "torso_len", "neck_share": "neck_len"}
rat["torso_share"] = mr["torso_len"] / H; rat["neck_share"] = mr["neck_len"] / H
rat["leg_share"] = m6["mean"]["hip_height"] / H            # hip-joint height is stance-dependent: R-6
M = mr["mean"]
for k, num in (("arm_share", M["arm"]), ("thigh_share", M["thigh"]), ("shin_share", M["shin"]), ("hand_share", M["hand"]),
               ("foot_share", M["foot_len"]), ("thorax_depth_share", mr["thorax_depth_max"]), ("shoulder_breadth_share", mr["bideltoid_breadth"]),
               ("shoulder_joint_share", mr["shoulder_joint_breadth"]), ("thorax_breadth_share", mr["thorax_breadth_max"]),
               ("crest_share", mr["iliac_crest_breadth"]), ("bitroch_share", mr["bitrochanteric_breadth"]), ("pelvic_depth_share", mr["pelvic_depth"]),
               ("pelvic_vertical_share", mr["pelvic_vertical"]), ("HH_share", mr["cranio"]["HH"]), ("HL_share", mr["cranio"]["HL"])):
    rat[k] = num / H
rat["span_der"] = (2 * M["arm"] + mr["shoulder_joint_breadth"]) / H
comb["ratio"] = rat
res["combined"] = comb
res["pitch"] = {p: {k: measure(rest, p, ext)["cranio"][k] for k in ("FPI", "MPI", "MdPI", "HL", "HH")} for p in (-3.0, 3.0)}
dd = load(rest); dd_e = float(mr["cranio"]["eye_diam_cm"])
res["eyefit"] = {"at_derived_diameter": eyefit(dd, dd_e), "at_plus_0.2cm": eyefit(dd, dd_e + 0.2)}
res["invariance"] = invariance.main(rest, r6, os.path.join(out, cid + "_inv.json"))
json.dump(res, open(os.path.join(out, cid + "_meas.json"), "w"), indent=1, default=float)
evidence.make(r6, os.path.join(out, cid + "_evidence.jpg"), "%s  R-6 measurement stance  stature %.2f cm  (orthographic; neutral surface; eyeballs = landmark spheres)" % (cid, H))
print("DONE", cid, round(H, 2))
