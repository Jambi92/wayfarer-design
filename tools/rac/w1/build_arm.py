"""Build one ARM candidate from a JSON config: native-stature solve, rest + R-6 exports. Usage: python3 build_arm.py cfg.json outdir"""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import arm_lib as A
cfg = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
t0 = time.time(); tag = cfg["id"]
if cfg.get("proxy_scale"):
    hm, info = cfg.get("height_macro", 0.0), {"reachable": False, "note": "below generator adult range; uniform-scale proxy (R-2 non-compliant)"}
else:
    hm, info = A.solve_height(cfg, cfg["stature"])
rec = {"id": tag, "cfg": cfg, "height_solve": info, "height_macro": hm}
if hm is None:
    json.dump(rec, open(os.path.join(out, tag + "_build.json"), "w"), indent=1); print("UNREACHABLE", info); sys.exit(0)
c = dict(cfg); c["height_macro"] = hm
b, r = A.build(c)
A.ground(b, r)
k_scale = None
if cfg.get("proxy_scale"):
    A.pose_r6(r); A.ground(b, r); h6 = A.stature(b)
    b, r = A.build(c); A.ground(b, r)
    k_scale = cfg["stature"] / h6
    r.scale = (k_scale,) * 3; A.bpy.context.view_layer.update(); A.ground(b, r)
    rec["proxy_uniform_scale"] = k_scale
meta = {"id": tag, "inputs": c, "proxy_uniform_scale": k_scale, "age_years": cfg.get("age_years", 35), "eye_diam_cm": A.EYE_DIAM_CM, "state": "rest (generator A-pose)"}
A.export(b, r, os.path.join(out, tag + "_rest.npz"), meta)
pose = A.pose_r6(r); A.ground(b, r)
meta.update({"state": "R-6", "pose": pose})
A.export(b, r, os.path.join(out, tag + "_r6.npz"), meta)
rec.update({"pose": pose, "stature_r6": A.stature(b), "secs": round(time.time() - t0, 1)})
bpy = A.bpy
if cfg.get("save_blend"):
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out, tag + ".blend"), compress=True)
json.dump(rec, open(os.path.join(out, tag + "_build.json"), "w"), indent=1)
print("BUILT", tag, rec["stature_r6"], rec["secs"])
