# RAC W2C diagnostic: hanging-hand reach in the R-6 pose (arms at the small fixed abduction): lowest fingertip height vs knee-joint height
# and vs mid-thigh, as a fraction of stature. Canon: hands near the knees are not a mandatory Grask trait and arms never ape-like
# (GRASK L57, L279). Diagnostic only; no canonical threshold exists.   Usage: python3 reach_diag.py OUT.json NAME=R6.npz ...
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from arm_measure import load
out = {}
for a in sys.argv[2:]:
    n, p = a.split('=', 1); d = load(p); V = d["V"].astype(float); keep = d["keep"]; J = d["joints"]
    H = V[keep][:, 2].max() - V[keep][:, 2].min(); z0 = V[keep][:, 2].min()
    hand = keep & (np.maximum.reduce([d["w_" + k] for k in ("hand_l", "hand_r", "fingers_l", "fingers_r")]) > 0.5)
    tip = V[hand][:, 2].min() - z0; knee = np.mean([J["calf_l"][0][2], J["calf_r"][0][2]]) - z0; hip = np.mean([J["thigh_l"][0][2], J["thigh_r"][0][2]]) - z0
    out[n] = {"stature": float(H), "fingertip_h": float(tip / H), "knee_h": float(knee / H), "tip_above_knee_cm": float(tip - knee), "tip_fraction_hip_to_knee": float((hip - tip) / (hip - knee))}
    print("%-10s fingertip %.3f H, knee %.3f H, tip above knee %.1f cm, %.2f of hip->knee" % (n, out[n]["fingertip_h"], out[n]["knee_h"], out[n]["tip_above_knee_cm"], out[n]["tip_fraction_hip_to_knee"]))
json.dump(out, open(sys.argv[1], 'w'), indent=1)
