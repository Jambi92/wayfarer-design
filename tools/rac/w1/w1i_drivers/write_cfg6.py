# RAC W1i: write tools/rac/w1/cfg/w1i/GO.json from the final build (GO_params.json written by final6.sh) and its measurement.
# Usage: python3 write_cfg6.py GO_params.json GO_meas.json run_note
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gn6
CFG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cfg")
p = json.load(open(sys.argv[1])); m = json.load(open(sys.argv[2])); note = sys.argv[3]
g = json.load(open(os.path.join(CFG, "w1h", "GO.json")))
g["w1i"] = {"bone_scales": p["bone_scales"], "sculpt": p["sculpt"], "solver_x": dict(zip(gn6.NAMES, p["x"])),
            "solver_bounds": {n: [lo, hi] for n, lo, hi in zip(gn6.NAMES, gn6.LO, gn6.HI)},
            "solver": "tools/rac/w1/w1i_drivers/gn6.py; " + note,
            "sculpt_note": "PCHIP (C1 monotone cubic) sculpt profile between nodes; confine_legs as W1h"}
g["stature_r6"] = m["stature_r6"]; g["status"] = "CONSTRAINED construction values; nothing here is canon"
os.makedirs(os.path.join(CFG, "w1i"), exist_ok=True); json.dump(g, open(os.path.join(CFG, "w1i", "GO.json"), "w"), indent=1); print("cfg written", g["stature_r6"])
