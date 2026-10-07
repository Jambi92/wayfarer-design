# RAC W1i method attribution (order §11: prove a method issue before acting on it): re-read the skin ALPC stations S2-S6 of a
# measurement JSON on exact plane sections (W1h CIB section method) at the measurement layer's own levels and masks, and recompute the
# ALPC ratios with arm_measure's formulas. Everything else in the JSON is unchanged. Used ONLY for the ALPC-6 skin-half attribution
# table; the official measurement layer is not changed.
# Usage: python3 restation.py in_meas.json rest.npz out_meas.json
import sys, json, numpy as np
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1'); sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/w1i_drivers')
from arm_measure import load
import trunk_profile as TP

def restation(meas_p, rest_p, out_p):
    M = json.load(open(meas_p)); c = M["combined"]; d = load(rest_p); V = d["V"].astype(float); J = d["joints"]; hd = lambda n: np.asarray(J[n][0], float)
    armw = np.maximum.reduce([d["w_" + k] for k in ("upperarm_l", "upperarm_r", "lowerarm_l", "lowerarm_r", "hand_l", "hand_r", "fingers_l", "fingers_r")])
    trunk = d["keep"] & (armw < 0.2); TF = d["F"][trunk[d["F"]].all(1)]; sec = lambda z: TP.section(V, TF, z)
    sh_u = (hd("upperarm_l")[2] + hd("upperarm_r")[2]) / 2; hipc = (hd("thigh_l") + hd("thigh_r")) / 2
    s01, s02 = hd("spine_01")[2], hd("spine_03")[2]
    vals = [sec(z) for z in np.linspace(hd("spine_02")[2], sh_u - 2, 12)]
    st = dict(c["alpc_stations"])
    st["S2"] = [float(np.nanmax([v[0] for v in vals])), float(np.nanmax([v[1] for v in vals]))]
    st["S3"] = list(sec(s02))
    vv = [sec(z) for z in np.linspace(s01, s02, 9)]; k = int(np.nanargmin([v[0] for v in vv])); st["S4"] = list(vv[k])
    st["S5"] = [sec(s01)[0], sec(s01)[1]]
    st["S6"] = [c["alpc_stations"]["S6"][0], sec(hipc[2])[1]]          # S6 breadth = bitrochanteric (max over +/-3 cm band, not a slab) unchanged
    r = c["ratio"]
    r.update({"S3_over_S2_b": st["S3"][0] / st["S2"][0], "S4_over_S2_b": st["S4"][0] / st["S2"][0], "S5_over_S2_b": st["S5"][0] / st["S2"][0],
              "S6_over_S2_b": st["S6"][0] / st["S2"][0], "S3_over_S2_d": st["S3"][1] / st["S2"][1], "S4_over_S2_d": st["S4"][1] / st["S2"][1],
              "S6_over_S2_d": st["S6"][1] / st["S2"][1], "S5_over_S4_b": st["S5"][0] / st["S4"][0], "S6_over_S4_b": st["S6"][0] / st["S4"][0],
              "S1_over_S2_b": st["S1"][0] / st["S2"][0], "pelvic_depth_over_thorax_depth": st["S6"][1] / st["S2"][1]})
    c["alpc_stations"] = st; c["station_method"] = "W1i re-read: plane sections (restation.py)"; json.dump(M, open(out_p, "w"), indent=1)
    return st

if __name__ == "__main__":
    print(restation(*sys.argv[1:4]))
