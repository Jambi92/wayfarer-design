# RAC W1h: write tools/rac/w1/cfg/w1h/{GO,GR}.json from the final build (GO_params.json written by final.sh) and its measurement.
# Usage: python3 write_cfg.py GO_params.json GO_meas.json derivation_json
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gn5
CFG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cfg")
p = json.load(open(sys.argv[1])); m = json.load(open(sys.argv[2])); der = json.load(open(sys.argv[3])).get("derivation", "")
g = json.load(open(os.path.join(CFG, "w1g", "GO.json")))
g["w1h"] = {"bone_scales": p["bone_scales"], "sculpt": p["sculpt"], "solver_x": dict(zip(gn5.NAMES, p["x"])),
            "solver_bounds": {n: [lo, hi] for n, lo, hi in zip(gn5.NAMES, gn5.LO, gn5.HI)},
            "solver": "tools/rac/w1/w1h_drivers/gn5.py runs H1-H8 (logs reviews/rac-w1h-evidence/solver/gn5_H*.log), then " + der,
            "sculpt_note": "confine_legs: trunk sculpt displacement multiplied by clip(1 - leg weight / 0.5, 0, 1) (no trunk sculpt on the free thigh)"}
g["stature_r6"] = m["stature_r6"]; g["status"] = "CONSTRAINED construction values (AD-W1H-12); nothing here is canon"
os.makedirs(os.path.join(CFG, "w1h"), exist_ok=True); json.dump(g, open(os.path.join(CFG, "w1h", "GO.json"), "w"), indent=1)
r = json.load(open(os.path.join(CFG, "w1g", "GR.json")))
r["w1h"] = {"pelvis": [0.985, 1, 1], "LR:clavicle": [1, 0.98, 1], "spine_01": "removed (as W1g)",
            "note": "pelvis X re-tuned for GR-P6 under the W1h station method (fixed-level plane sections); W1g 1.12 was tuned under the W1g method. Method-sensitive; CONSTRAINED."}
json.dump(r, open(os.path.join(CFG, "w1h", "GR.json"), "w"), indent=1); print("cfg written", g["stature_r6"])
