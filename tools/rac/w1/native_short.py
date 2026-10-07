"""RAC W1d: native short-adult test bodies (PK 107 cm, CG 91 cm) WITHOUT whole-body uniform scaling.

Workflow (strategy option 2, "modelling workflow directly authored at target stature"):
1. Start from the accepted human reference construction (MF-M-R settings: MPFB adult, age 35, macro 0.5) plus the race's
   generator targets (proportion directions; same targets as the W1c proxies). The generator's own minimum-height model is
   NOT used: its short-stature macro is anatomically implausible (femur joint-to-joint 23.8 cm < tibia 39.2 cm at 137.6 cm).
2. Re-proportion region by region at the target stature with explicit absolute factors per region (pose-bone scale in bone
   space, inherit-scale off, baked into the rest mesh):
     - segment LENGTHS (bone Y): one length factor k_len, solved so the R-6 stature equals the target exactly;
     - trunk/limb BREADTH and DEPTH (bone X/Z) and joint size: k_len ** beta_girth;
     - HEAD (uniform): PK -> k_len ** beta_head; CG -> factor that puts HH at the canon centre value 12 cm (CG L1589: 11-13 cm);
     - HANDS / FEET (uniform): k_len ** beta_hand, k_len ** beta_foot.
   The betas are BUILDER-CHOSEN: log-log slopes of the generator's own adult size allometry measured on MPFB configuration-1
   builds at 137.6-243.5 cm (tools/rac/w1/native_short_allometry.json). They replace the single global factor of a uniform
   scale; no single factor is applied to the whole body.
3. Landmark globes: DER from the (head-scaled) generator socket.
Usage (inside bpy env): python3 native_short.py cfg.json outdir"""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import arm_lib as A
import numpy as np
bpy = A.bpy

HEADS = {"head", "neck_01"}
HANDS = ("hand_", "thumb_", "index_", "middle_", "ring_", "pinky_")
FEET = ("foot_", "ball_")

def set_factors(rig, f):
    for pb in rig.pose.bones:
        pb.bone.inherit_scale = "NONE"
        n = pb.name
        if n == "head": s = (f["head"],) * 3
        elif any(n.startswith(h) for h in HANDS): s = (f["hand"],) * 3
        elif any(n.startswith(h) for h in FEET): s = (f["foot"],) * 3
        elif n == "Root": s = (1.0, 1.0, 1.0)
        else: s = (f["girth"], f["len"], f["girth"])
        pb.scale = s
    bpy.context.view_layer.update()

bake = A.bake

def head_HH(body):
    """Head height (vertex to lowest chin point) on the current rest mesh, cm - quick check used for CG."""
    c = A.coords(body); g = A.groups(body); hw = np.array([g["head"].get(i, 0) for i in range(len(c))])
    keep = np.array([g["body"].get(i, 0) > 0.5 for i in range(len(c))])
    eyes = [c[[i for i, w in g["helper-%s-eye" % s].items() if w > 0.5]].mean(0) for s in ("l", "r")]
    oc = (eyes[0] + eyes[1]) / 2
    top = c[keep & (hw > 0.5), 2].max()
    chin = keep & (hw > 0.5) & (np.abs(c[:, 0]) < 0.6) & (c[:, 1] > oc[1] - 4) & (c[:, 2] < oc[2] - 4)
    return top - c[chin, 2].min()

def build_native(cfg, betas, k_len, head_override=None):
    c = dict(cfg); c["height_macro"] = cfg.get("base_height_macro", 0.5);   # W2A: optional base macro (default 0.5 = W1 behaviour)
    c.pop("proxy_scale", None)
    body, rig = A.build(c)
    gb = cfg.get("girth_beta", betas["girth"])     # per-race override: canon may require a narrower core than generator allometry
    f = {"len": k_len, "girth": k_len ** gb, "hand": k_len ** betas["hand"], "foot": k_len ** betas["foot"],
         "head": head_override if head_override else k_len ** betas["head"]}
    set_factors(rig, f); bake(body, rig); A.ground(body, rig)
    return body, rig, f

def main(cfgp, out):
    cfg = json.load(open(cfgp)); tag = cfg["id"] + "-NAT"
    betas = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "native_short_allometry.json")))["betas"]
    target = cfg["stature"]
    # solve k_len (and the CG head factor) by secant on the R-6 stature
    def stat(k, hov=None):
        b, r, f = build_native(cfg, betas, k, hov); A.pose_r6(r); A.ground(b, r); return A.stature(b), b, f
    k0, k1 = target / 173.0, target / 173.0 * 1.02
    h0, _, _ = stat(k0); h1, _, _ = stat(k1); hov = None
    for it in range(12):
        k2 = k1 + (target - h1) * (k1 - k0) / (h1 - h0)
        if cfg.get("head_HH_cm"):
            b, r, f = build_native(cfg, betas, k2, hov); hh = head_HH(b); base = f["head"]
            hov = base * cfg["head_HH_cm"] / hh
        h2, b, f = stat(k2, hov)
        k0, h0, k1, h1 = k1, h1, k2, h2
        if abs(h2 - target) < 0.02: break
    b, r, f = build_native(cfg, betas, k1, hov)
    meta = {"id": tag, "inputs": cfg, "native_factors": f, "betas": betas, "state": "rest (re-proportioned, baked)",
            "method": "regional re-proportioning at target stature (no global uniform scale)"}
    A.export(b, r, os.path.join(out, tag + "_rest.npz"), meta)
    pose = A.pose_r6(r); A.ground(b, r); meta.update({"state": "R-6", "pose": pose})
    A.export(b, r, os.path.join(out, tag + "_r6.npz"), meta)
    rec = {"id": tag, "cfg": cfg, "height_macro": cfg.get("base_height_macro", 0.5), "native_factors": f, "betas": betas, "stature_r6": A.stature(b), "iters": it + 1, "pose": pose}
    json.dump(rec, open(os.path.join(out, tag + "_build.json"), "w"), indent=1)
    print("BUILT", tag, rec["stature_r6"], f)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
