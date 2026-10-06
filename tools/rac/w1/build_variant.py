"""RAC W1f: build a VARIANT of an existing candidate with the SAME skeleton construction (same height macro, or the same native
short-adult regional factors) and changed composition / frame / bone-scale inputs.

Used for: the skeletal-envelope body (generator minimum composition, muscle 0 / weight 0) behind the skeletal proxy; the
low-composition body (GOR-BODY-16); frame bodies (GOR-BODY-04/-12/-14); and AD-G14 skeleton bodies.
Overrides are merged into the base cfg: scalar keys replace; "targets" and "bone_scales" are merged key by key (a value of null
removes a key). The height is NOT re-solved (skeleton held fixed) unless overrides contain "resolve_stature": true.
Usage (bpy env): python3 build_variant.py base_build.json overrides.json outdir NEW_ID"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import arm_lib as A
bpy = A.bpy

def merged(cfg, ov):
    c = json.loads(json.dumps(cfg))
    for k, v in ov.items():
        if k in ("targets", "bone_scales"):
            d = dict(c.get(k, {}))
            for kk, vv in v.items():
                if vv is None: d.pop(kk, None)
                else: d[kk] = vv
            c[k] = d
        elif k not in ("resolve_stature",):
            c[k] = v
    return c

def main(basep, ovp, out, new_id):
    base = json.load(open(basep)); ov = json.load(open(ovp)); os.makedirs(out, exist_ok=True)
    cfg = merged(base["cfg"], ov); cfg["id"] = new_id
    rec = {"id": new_id, "base": os.path.basename(basep), "overrides": ov, "cfg": cfg}
    if "native_factors" in base:
        import native_short as N
        c = dict(cfg); c["height_macro"] = 0.5
        b, r = A.build(c); N.set_factors(r, base["native_factors"]); A.bake(b, r); A.ground(b, r)
        rec.update({"route": "native short-adult, base factors reused", "native_factors": base["native_factors"], "height_macro": 0.5})
    else:
        if ov.get("resolve_stature"):
            hm, info = A.solve_height(cfg, cfg["stature"]); rec["height_solve"] = info
        else:
            hm = base["height_macro"]
        c = dict(cfg); c["height_macro"] = hm
        b, r = A.build(c); A.ground(b, r)
        rec.update({"route": "height macro %s" % ("re-solved" if ov.get("resolve_stature") else "held from base"), "height_macro": hm})
    meta = {"id": new_id, "inputs": cfg, "variant_of": base["id"], "state": "rest (generator A-pose)"}
    A.export(b, r, os.path.join(out, new_id + "_rest.npz"), meta)
    pose = A.pose_r6(r); A.ground(b, r); meta.update({"state": "R-6", "pose": pose})
    A.export(b, r, os.path.join(out, new_id + "_r6.npz"), meta)
    rec.update({"pose": pose, "stature_r6": A.stature(b)})
    json.dump(rec, open(os.path.join(out, new_id + "_build.json"), "w"), indent=1)
    print("BUILT", new_id, round(rec["stature_r6"], 2))

if __name__ == "__main__":
    main(*sys.argv[1:5])
