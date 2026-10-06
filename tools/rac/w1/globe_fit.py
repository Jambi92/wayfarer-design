"""RAC W1e: S-D3 globe-fit test. Does an ordinary adult-human landmark globe (2.2-2.4 cm; MF-M-R 2.40, MF-F-R 2.30) fit the
authored PK / CG socket at the generator eye centre? Socket capacity = 2 x distance from the eye centre to the nearest kept skin
vertex (largest centred globe that touches no skin). Counts skin vertices inside a centred globe of each adult size (0.02 cm
tolerance, as eyefit.py). Reads <id>_r6.npz (head rigid in R-6) and <id>_meas.json.
Usage: python3 globe_fit.py cand_dir out.json ID..."""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def fit(cd, i):
    D = np.load(os.path.join(cd, i + "_r6.npz"), allow_pickle=True); V = D["V"].astype(float)[D["keep"]]
    c = json.load(open(os.path.join(cd, i + "_meas.json")))["combined"]["cranio"]
    r = {}; caps = []; ins = {}
    for s in ("l", "r"):
        e = D["eye_" + s].astype(float); dist = np.linalg.norm(V - e, axis=1); caps.append(2 * dist.min())
        for g in (2.2, 2.3, 2.4): ins[str(g)] = ins.get(str(g), 0) + int((dist < g / 2 - 0.02).sum())
    cap = float(min(caps))
    return {"socket_capacity_cm": cap, "HH": c["HH"], "HL": c["HL"], "landmark_globe_cm": c["eye_diam_cm"],
            "skin_verts_inside_at": {k: v // 2 for k, v in ins.items()}, "adult_globe_2.3_over_HH": 2.3 / c["HH"],
            "capacity_over_HH": cap / c["HH"], "interocular_cm": float(np.linalg.norm(D["eye_l"] - D["eye_r"]))}

if __name__ == "__main__":
    res = {i: fit(sys.argv[1], i) for i in sys.argv[3:]}
    json.dump(res, open(sys.argv[2], "w"), indent=1)
    for i, r in res.items(): print(i, {k: (round(v, 3) if isinstance(v, float) else v) for k, v in r.items()})
