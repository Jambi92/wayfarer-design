# RAC RM-OT-05A: measurement deltas, rebuild vs accepted W2 (skin-layer run_candidate ratios + exact-plane joint sections from the rerun
# W2D values) and the cross-race matched-height orderings. Usage: python3 a_tables.py EVALDIR OUT.json
import sys, json
E = sys.argv[1]; V = json.load(open(E + '/w2d.json'))['values']; VC = json.load(open(E + '/w2c.json'))['values']
K = ["stature (cm)", "torso_share", "leg_share", "arm_share", "upperarm_over_arm", "forearm_over_arm", "femur_over_leg", "shin_over_leg", "hand_share", "foot_share",
     "thorax_breadth_share", "thorax_depth_share", "shoulder_joint_share",
     "skeletal thoracic depth / breadth [t=0.5]", "skeletal crest breadth / stature [t=0.5]", "skeletal AP pelvic depth / stature [t=0.5]",
     "skeletal ALPC lumbar depth / thorax (S4/S2 d) [t=0.5]", "skeletal ALPC pelvic AP / thoracic depth [t=0.5]",
     "elbow breadth / adjacent segment (exact-plane section)", "wrist breadth / adjacent segment (exact-plane section)",
     "knee breadth / adjacent segment (exact-plane section)", "ankle breadth / adjacent segment (exact-plane section)",
     "knee breadth / stature (exact-plane section)", "ankle breadth / stature (exact-plane section)"]
PAIRS = [("GR208", "GR208-W2"), ("GR218", "GR218-W2"), ("GR229", "GR229-W2"), ("GO208", "GO208-W2"), ("GO229", "GO229-W2"), ("GOREF", "GOREF-W2"), ("GO251", "GO251-W2")]
out = {"delta": {}, "matched": {}}
for a, b in PAIRS:
    out["delta"][a] = {k: {"new": V[a].get(k), "w2": V[b].get(k), "pct": (100 * (V[a][k] / V[b][k] - 1)) if V[a].get(k) and V[b].get(k) else None} for k in K}
for h, ids in ((208, ["MF203", "SK208", "GR208", "GO208"]), (218, ["SK218", "GR218", "GO218"]), (229, ["SK229", "GR229", "GO229"])):
    out["matched"][h] = {i: {k: V.get(i, {}).get(k) for k in K} for i in ids}
json.dump(out, open(sys.argv[2], 'w'), indent=1)
for a in out["delta"]:
    print(a, " ".join("%s %+.1f%%" % (k.split(' (')[0].replace('skeletal ', 's.')[:22], d["pct"]) for k, d in out["delta"][a].items() if d["pct"] is not None and abs(d["pct"]) >= 1.0))
for h, m in out["matched"].items():
    print(h, {i: {k[:18]: round(v, 3) for k, v in d.items() if v and k in ("torso_share", "leg_share", "forearm_over_arm", "shin_over_leg", "hand_share", "foot_share", "knee breadth / adjacent segment (exact-plane section)", "skeletal thoracic depth / breadth [t=0.5]")} for i, d in m.items()})
