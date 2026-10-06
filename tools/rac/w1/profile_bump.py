"""RAC W1f: anterior trunk-profile bump (contour smoothness diagnostic for AD-G14 envelopes and skeletons).
Anterior profile = most-forward central-trunk point (|x| < 12 cm x H/173, arms excluded) in 1.2 cm slabs at 40 levels from the
crest proxy to 2 cm below the suprasternal proxy; bump = max height of a local peak above BOTH profile points 4 levels
(about 1.5-2 cm x H/173) away, / stature. A shelf or belly-type protrusion raises it; a smooth barrel or flat trunk does not.
Builder-chosen diagnostic; the reference values are MF-M-R and the accepted Skarn."""
import numpy as np
from arm_measure import load
def bump(path):
    d = load(path); V = d["V"].astype(float); keep = d["keep"]; J = d["joints"]; w = lambda k: d["w_" + k]
    armw = np.maximum.reduce([w(x) for x in ("upperarm_l", "upperarm_r", "lowerarm_l", "lowerarm_r", "hand_l", "hand_r", "fingers_l", "fingers_r")])
    H = V[keep, 2].max(); T = keep & (armw < 0.2) & (np.abs(V[:, 0]) < 12 * H / 173)
    s01 = J["spine_01"][0][2]; sst = (J["clavicle_l"][0][2] + J["clavicle_r"][0][2]) / 2
    zs = np.linspace(s01, sst - 2, 40); fa = np.array([V[T & (np.abs(V[:, 2] - z) < 0.6), 1].max() for z in zs]); k = 4
    return float(max(fa[i] - max(fa[i - k], fa[i + k]) for i in range(k, len(fa) - k)) / H)
if __name__ == "__main__":
    import sys
    for p in sys.argv[1:]: print(p.split("/")[-1], round(bump(p), 4))

def chest_lead(path):
    """(anterior chest maximum - anterior maximum of the lower thorax / abdomen) / stature, on the central trunk (|x| < 8 cm x H/173):
    chest band = 52-85 % of hip-joint -> suprasternal height, abdomen band = 15-48 %. > 0 means the chest leads (human-like; a deep
    barrel trunk still leads with the chest); < 0 means the abdomen / lower thorax protrudes beyond the chest (pot-belly read)."""
    d = load(path); V = d["V"].astype(float); keep = d["keep"]; J = d["joints"]; w = lambda k: d["w_" + k]
    armw = np.maximum.reduce([w(x) for x in ("upperarm_l", "upperarm_r", "lowerarm_l", "lowerarm_r", "hand_l", "hand_r", "fingers_l", "fingers_r")])
    H = V[keep, 2].max(); T = keep & (armw < 0.05) & (np.abs(V[:, 0]) < 8 * H / 173)
    hip = (J["thigh_l"][0][2] + J["thigh_r"][0][2]) / 2; sst = (J["clavicle_l"][0][2] + J["clavicle_r"][0][2]) / 2
    r = (V[:, 2] - hip) / (sst - hip)
    ch = T & (r >= 0.52) & (r <= 0.85); ab = T & (r >= 0.15) & (r <= 0.48)
    return float((V[ch, 1].max() - V[ab, 1].max()) / H)

def buttock_lead(path):
    """(posterior-most point of the gluteal band - posterior-most point of the lumbar band) / stature, central trunk (|x| < 8 cm x
    H/173). Gluteal band r = -0.25..0.05, lumbar band r = 0.15..0.35 (r as chest_lead). > 0 = the buttock projects behind the
    lumbar back by that share of stature. Compared with the references; the rejected W1e skin trial is the failure example."""
    d = load(path); V = d["V"].astype(float); keep = d["keep"]; J = d["joints"]; w = lambda k: d["w_" + k]
    armw = np.maximum.reduce([w(x) for x in ("upperarm_l", "upperarm_r", "lowerarm_l", "lowerarm_r", "hand_l", "hand_r", "fingers_l", "fingers_r")])
    H = V[keep, 2].max(); T = keep & (armw < 0.05) & (np.abs(V[:, 0]) < 8 * H / 173)
    hip = (J["thigh_l"][0][2] + J["thigh_r"][0][2]) / 2; sst = (J["clavicle_l"][0][2] + J["clavicle_r"][0][2]) / 2
    r = (V[:, 2] - hip) / (sst - hip)
    gl = T & (r >= -0.25) & (r <= 0.05); lu = T & (r >= 0.15) & (r <= 0.35)
    return float((V[lu, 1].min() - V[gl, 1].min()) / H)

def flank_flare(path):
    """W1h (AD-W1H-2) diagnostic: crest-flank flare = (S5 crest breadth - the breadth the straight waist-to-hip line would have at the
    crest level) / stature, the line running from S4 (waist minimum, its own level) to the hip-joint level breadth (the S6 slab);
    same slabs as the ALPC stations (arm_measure). > 0 = the crest flank stands out of the waist-to-hip line (the flare-dominant /
    independently widened read); <= 0 = the crest lies on or inside a continuous waist-to-hip taper. Diagnostic, builder-chosen."""
    d = load(path); V = d["V"].astype(float); keep = d["keep"]; J = d["joints"]; w = lambda k: d["w_" + k]
    armw = np.maximum.reduce([w(x) for x in ("upperarm_l", "upperarm_r", "lowerarm_l", "lowerarm_r", "hand_l", "hand_r", "fingers_l", "fingers_r")])
    T = keep & (armw < 0.2); H = V[keep, 2].max() - V[keep, 2].min()
    def sb(z): m = T & (np.abs(V[:, 2] - z) < 1.0); return float(np.ptp(V[m, 0]))
    hip = (J["thigh_l"][0][2] + J["thigh_r"][0][2]) / 2; s01 = J["spine_01"][0][2]; s02 = J["spine_03"][0][2]
    zs = np.linspace(s01, s02, 9); bz = [sb(z) for z in zs]; k = int(np.argmin(bz)); z4, b4 = zs[k], bz[k]
    bt = T & (np.abs(V[:, 2] - hip) < 3); b6 = float(np.ptp(V[bt, 0])); b5 = sb(s01)
    if z4 <= s01 + 1e-6: return {"flank_flare": 0.0, "S4_at_crest": True}
    line = b6 + (b4 - b6) * (s01 - hip) / (z4 - hip)
    return {"flank_flare": (b5 - line) / H, "S4_at_crest": False}
