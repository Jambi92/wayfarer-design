"""RAC W1f: soft-tissue CONTOUR check for sculpted envelopes (AD-G14 'reject any result that recreates the W1e buttock / abdomen
bulge'). Reads the R-6 body; trunk vertices only (arms excluded); 1 cm height bins.
- abdomen index: max forward protrusion of the anterior trunk profile beyond the straight line joining the anterior chest maximum
  (between the costal-margin proxy and the girdle) and the anterior profile at hip-joint level, / stature (> 0 = belly beyond the
  chest-to-pelvis line);
- buttock index: max backward protrusion of the posterior profile between hip-joint level - 12 % H and the crest proxy beyond the
  line joining the posterior profile at the crest proxy and at hip-joint level - 12 % H (posterior thigh), / stature;
- anterior step: max change of the anterior profile between adjacent 1 cm bins / stature (abrupt shelf).
Indices are compared with the accepted references (MF-M-R, SK); they are contour diagnostics, not canon.
Usage: python3 contour_check.py r6.npz [...]"""
import sys, json, numpy as np
from arm_measure import load

def idx(path):
    d = load(path); V = d["V"].astype(float); keep = d["keep"]; J = d["joints"]; w = lambda k: d["w_" + k]
    armw = np.maximum.reduce([w(x) for x in ("upperarm_l", "upperarm_r", "lowerarm_l", "lowerarm_r", "hand_l", "hand_r", "fingers_l", "fingers_r")])
    T = keep & (armw < 0.2) & (np.abs(V[:, 0]) < 0.35 * np.ptp(V[keep & (armw < 0.2), 0]))
    H = V[keep, 2].max() - V[keep, 2].min()
    hip = (J["thigh_l"][0][2] + J["thigh_r"][0][2]) / 2; s03 = J["spine_03"][0][2]; s01 = J["spine_01"][0][2]
    sst = (J["clavicle_l"][0][2] + J["clavicle_r"][0][2]) / 2
    zs = np.arange(hip - 0.12 * H, sst, 1.0); fa, fp = [], []
    for z in zs:
        m = T & (np.abs(V[:, 2] - z) < 0.5)
        fa.append(V[m, 1].max() if m.any() else np.nan); fp.append(V[m, 1].min() if m.any() else np.nan)
    fa, fp = np.array(fa), np.array(fp)
    ch = (zs >= s03) & (zs <= sst - 2); i_ch = np.where(ch)[0][np.nanargmax(fa[ch])]; i_hip = int(np.argmin(np.abs(zs - hip)))
    seg = np.arange(i_hip, i_ch + 1); line = fa[i_hip] + (fa[i_ch] - fa[i_hip]) * (zs[seg] - zs[i_hip]) / (zs[i_ch] - zs[i_hip])
    abd = float(np.nanmax(fa[seg] - line)) / H
    i_lo = 0; i_cr = int(np.argmin(np.abs(zs - s01))); seg2 = np.arange(i_lo, i_cr + 1)
    line2 = fp[i_lo] + (fp[i_cr] - fp[i_lo]) * (zs[seg2] - zs[i_lo]) / (zs[i_cr] - zs[i_lo])
    but = float(np.nanmax(line2 - fp[seg2])) / H
    step = float(np.nanmax(np.abs(np.diff(fa[i_hip:i_ch + 1])))) / H
    return {"abdomen_index": abd, "buttock_index": but, "anterior_step": step, "stature": float(H)}

if __name__ == "__main__":
    for p in sys.argv[1:]:
        r = idx(p); print(p.split("/")[-1].ljust(28), {k: round(v, 4) for k, v in r.items()})
