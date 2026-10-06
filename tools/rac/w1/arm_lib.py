"""RAC W1 continuation: MPFB ARM candidate builder (runs inside bpy with the MPFB extension enabled).

Build a MakeHuman/MPFB human at its NATIVE stature (height macro solved, no uniform scaling), at the ARM
measurement-state age (35 y apparent, D-4a), add landmark eyeballs (D-4c), pose it to the R-6 measurement stance
by rotating rig bones only (D-4b), check pose invariance, and export arrays for numpy measurement.

Conventions of the exported npz: cm; x = subject's left (+), f = forward, u = up; feet on u = 0.
Every input that is not canon is a BUILDER-CHOSEN value and is written into the npz 'meta' record.
"""
import bpy, json, math, os, sys
import numpy as np
from mathutils import Vector, Matrix, Quaternion
import addon_utils
addon_utils.enable("bl_ext.user_default.mpfb", default_set=True)
from bl_ext.user_default.mpfb.services.humanservice import HumanService
from bl_ext.user_default.mpfb.services.targetservice import TargetService

# MakeHuman 1.x age slider mapping (human.py setAgeYears): 0.5 -> 25 y, 1.0 -> 90 y, linear in between.
def age_value(years):
    return 0.5 + (years - 25.0) / (90.0 - 25.0) * 0.5 if years >= 25 else 0.1875 + (years - 11.0) / (25.0 - 11.0) * 0.3125

EYE_DIAM_CM = 2.4   # adult human globe ~24 mm (documented anatomical reference; see provenance note in the W1c report)
ARM_ABD_DEG = 8.0   # R-6 'small fixed abduction' - canon gives no angle -> BUILDER-CHOSEN

def side_targets(name, value):
    sided = name.startswith("LR:")
    n = name[3:] if sided else name
    return [{"target": p + n, "value": value} for p in (("l-", "r-") if sided else ("",))]

def build(cfg):
    bpy.ops.wm.read_homefile(use_empty=True)
    pheno = TargetService.get_default_macro_info_dict()
    pheno.update({"gender": cfg.get("gender", 1.0), "age": cfg.get("age", age_value(35.0)),
                  "muscle": cfg.get("muscle", 0.5), "weight": cfg.get("weight", 0.5),
                  "proportions": cfg.get("proportions", 0.5), "height": cfg.get("height_macro", 0.5),
                  "cupsize": cfg.get("cupsize", 0.5), "firmness": cfg.get("firmness", 0.5),
                  "race": cfg.get("race", {"asian": 0.333, "caucasian": 0.334, "african": 0.333})})
    tl = []
    for k, v in cfg.get("targets", {}).items():
        if abs(v) > 1e-4: tl += side_targets(k, v)
    info = {"phenotype": pheno, "targets": tl, "rig": "game_engine", "name": cfg.get("name", "arm"),
            "skin_mhmat": "", "skin_material_type": "NONE", "skin_material_settings": {}, "eyes_material_type": "",
            "eyes_material_settings": {}, "eyes": "", "eyebrows": "", "eyelashes": "", "hair": "", "teeth": "", "tongue": "",
            "clothes": [], "clothes_material_type": "MAKESKIN", "color_adjustments": {}, "alternative_materials": {}, "makeup": []}
    st = HumanService.get_default_deserialization_settings()
    st.update({"subdiv_levels": 0, "load_clothes": False, "override_skin_model": "PRESET"})
    body = HumanService.deserialize_from_dict(info, st)
    return body, body.parent

def groups(body):
    names = {g.index: g.name for g in body.vertex_groups}
    out = {}
    for v in body.data.vertices:
        for w in v.groups:
            out.setdefault(names[w.group], {})[v.index] = w.weight
    return out

def coords(body):
    """Evaluated (posed) coordinates of every base vertex, helpers included, in cm (x, f, u)."""
    for md in body.modifiers:
        if md.type == "MASK": md.show_viewport = False
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get(); ev = body.evaluated_get(dg); me = ev.to_mesh()
    n = len(me.vertices); a = np.empty(n * 3); me.vertices.foreach_get("co", a); ev.to_mesh_clear()
    for md in body.modifiers:
        if md.type == "MASK": md.show_viewport = True
    bpy.context.view_layer.update()
    a = a.reshape(-1, 3) * 100.0
    M = np.array(body.matrix_world); a = a @ M[:3, :3].T + M[:3, 3] * 100.0
    return np.c_[a[:, 0], -a[:, 1], a[:, 2]]

def bone_pts(rig):
    """Posed bone heads/tails in cm (x, f, u)."""
    bpy.context.view_layer.update()
    M = rig.matrix_world; d = {}
    for pb in rig.pose.bones:
        h = M @ pb.head; t = M @ pb.tail
        d[pb.name] = (np.array([h.x, -h.y, h.z]) * 100, np.array([t.x, -t.y, t.z]) * 100)
    return d

def _aim(rig, name, target_dir_world, twist_ref=None):
    """Rotate pose bone so its head->tail points along target_dir (Blender world axes). Rotation only, head fixed."""
    bpy.context.view_layer.update()
    pb = rig.pose.bones[name]
    cur = (pb.tail - pb.head).normalized()
    q = cur.rotation_difference(Vector(target_dir_world).normalized())
    M = pb.matrix.copy(); loc = M.to_translation()
    R = q.to_matrix().to_4x4()
    pb.matrix = Matrix.Translation(loc) @ R @ Matrix.Translation(-loc) @ M
    bpy.context.view_layer.update()

def _twist(rig, name, angle_rad):
    bpy.context.view_layer.update()
    pb = rig.pose.bones[name]; ax = (pb.tail - pb.head).normalized()
    M = pb.matrix.copy(); loc = M.to_translation()
    R = Quaternion(ax, angle_rad).to_matrix().to_4x4()
    pb.matrix = Matrix.Translation(loc) @ R @ Matrix.Translation(-loc) @ M
    bpy.context.view_layer.update()

def pose_r6(rig, abd_deg=ARM_ABD_DEG):
    """R-6: arms hanging with small fixed abduction, elbows extended, palms toward thighs; legs: hip joint above ankle
    (feet at hip width), knees/hips extended keeping the rest sagittal knee/ankle relation; feet parallel and flat.
    Spine, neck and head are left at the generator's upright rest (neutral carriage)."""
    rec = {"arm_abduction_deg": abd_deg}
    a = math.radians(abd_deg)
    for s, sx in (("l", 1), ("r", -1)):
        down = Vector((sx * math.sin(a), 0.0, -math.cos(a)))
        _aim(rig, "upperarm_" + s, down); _aim(rig, "lowerarm_" + s, down); _aim(rig, "hand_" + s, down)
        # palms toward thighs: pinky->index knuckle vector points forward (Blender -y)
        P = lambda n: rig.pose.bones[n].head.copy()
        def across():
            bpy.context.view_layer.update()
            v = rig.matrix_world @ P("index_01_" + s) - rig.matrix_world @ P("pinky_01_" + s)
            ax = (rig.pose.bones["lowerarm_" + s].tail - rig.pose.bones["lowerarm_" + s].head).normalized()
            v = v - ax * v.dot(ax); return v.normalized(), ax
        v, ax = across()
        tgt = Vector((0, -1, 0)); tgt = (tgt - ax * tgt.dot(ax)).normalized()
        ang = math.atan2(v.cross(tgt).dot(ax), v.dot(tgt))
        # split forearm rotation between humerus (1/3) and forearm (2/3) to limit candy-wrap; record both
        _twist(rig, "upperarm_" + s, ang / 3.0); v2, _ = across()
        ang2 = math.atan2(v2.cross(tgt).dot(ax), v2.dot(tgt)); _twist(rig, "lowerarm_" + s, ang2)
        v3, _ = across(); rec["palm_twist_deg_" + s] = round(math.degrees(ang), 2)
        rec["palm_residual_deg_" + s] = round(math.degrees(math.atan2(v3.cross(tgt).dot(ax), v3.dot(tgt))), 3)
        # legs
        th = rig.pose.bones["thigh_" + s]; ca = rig.pose.bones["calf_" + s]
        dt = (th.tail - th.head); _aim(rig, "thigh_" + s, Vector((0.0, dt.y, dt.z)))
        dc = (ca.tail - ca.head); _aim(rig, "calf_" + s, Vector((0.0, dc.y, dc.z)))
        ft = rig.pose.bones["foot_" + s]; df = Vector(rig.data.bones["foot_" + s].tail_local - rig.data.bones["foot_" + s].head_local)
        _aim(rig, "foot_" + s, Vector((0.0, df.y, df.z)))
        db = Vector(rig.data.bones["ball_" + s].tail_local - rig.data.bones["ball_" + s].head_local)
        _aim(rig, "ball_" + s, Vector((0.0, db.y, db.z)))
    return rec

def ground(body, rig):
    c = coords(body); g = groups(body); bm = np.array([g["body"].get(i, 0) > 0.5 for i in range(len(c))])
    z0 = c[bm, 2].min()
    rig.location.z -= z0 / 100.0; bpy.context.view_layer.update()

def stature(body, g=None):
    c = coords(body); g = g or groups(body)
    bm = np.array([g["body"].get(i, 0) > 0.5 for i in range(len(c))])
    return c[bm, 2].max() - c[bm, 2].min()

def tri_faces(body, keep):
    F = []
    for p in body.data.polygons:
        vs = list(p.vertices)
        if all(keep[i] for i in vs):
            for k in range(1, len(vs) - 1): F.append((vs[0], vs[k], vs[k + 1]))
    return np.array(F, dtype=np.int32)

def export(body, rig, path, meta, eye_diam=EYE_DIAM_CM):
    g = groups(body); c = coords(body); n = len(c)
    keep = np.array([g["body"].get(i, 0) > 0.5 for i in range(n)])
    F = tri_faces(body, keep)
    eyes = {}; ext = []
    for s in ("l", "r"):
        idx = [i for i, w in g["helper-%s-eye" % s].items() if w > 0.5]
        eyes[s] = c[idx].mean(0); ext.append((c[idx].max(0) - c[idx].min(0)).mean())
    jp = bone_pts(rig)
    wnames = ["head", "ears", "neck_01", "pelvis", "spine_01", "spine_02", "spine_03", "clavicle_l", "clavicle_r",
              "upperarm_l", "upperarm_r", "lowerarm_l", "lowerarm_r", "hand_l", "hand_r", "thigh_l", "thigh_r",
              "calf_l", "calf_r", "foot_l", "foot_r", "ball_l", "ball_r"]
    W = {k: np.array([g.get(k, {}).get(i, 0.0) for i in range(n)], dtype=np.float32) for k in wnames}
    hand_groups = [k for k in g if any(k.startswith(p) for p in ("index", "middle", "ring", "pinky", "thumb"))]
    for s in ("l", "r"):
        W["fingers_" + s] = np.array([max([g[k].get(i, 0.0) for k in hand_groups if k.endswith("_" + s)] + [0.0]) for i in range(n)], dtype=np.float32)
    np.savez_compressed(path, V=c.astype(np.float32), F=F, keep=keep, eye_l=eyes["l"], eye_r=eyes["r"], eye_diam=eye_diam, helper_eye_ext=float(np.mean(ext)),
                        joints=json.dumps({k: [v[0].tolist(), v[1].tolist()] for k, v in jp.items()}),
                        meta=json.dumps(meta), **{"w_" + k: v for k, v in W.items()})
    return c, keep, F

def scale_proxy(body, rig, target):
    """NON-COMPLIANT (R-2) units device for statures below the generator's adult range: uniform rig scale."""
    h = stature(body); k = target / h
    rig.scale = (rig.scale[0] * k, rig.scale[1] * k, rig.scale[2] * k); bpy.context.view_layer.update(); ground(body, rig)
    return k

def solve_height(cfg, target, pose=True, tol=0.02, it=12):
    """Secant/bisection on the MPFB height macro so the R-6-posed stature equals target natively (no scaling)."""
    lo, hi = 0.0, 1.0
    def H(hm):
        c = dict(cfg); c["height_macro"] = hm; b, r = build(c)
        if pose: pose_r6(r)
        ground(b, r); return stature(b), b, r
    h_lo, _, _ = H(lo); h_hi, _, _ = H(hi)
    if not (h_lo <= target <= h_hi):
        return None, {"reachable": False, "range_cm": [h_lo, h_hi]}
    hist = []; best = None
    for k in range(24):
        x = (lo + hi) / 2; h, b, r = H(x); hist.append((x, h))
        if best is None or abs(h - target) < abs(best[1] - target): best = (x, h)
        if abs(h - target) < tol: return x, {"reachable": True, "stature": h, "iters": k + 1}
        if h < target: lo = x
        else: hi = x
    # MPFB's height macro has a step near its default (0.4845 -> 0.485 jumps ~0.37 cm); take the closest reachable value
    return best[0], {"reachable": True, "stature": best[1], "iters": 24, "deviation_cm": best[1] - target,
                     "note": "closest reachable native stature (macro step); no scaling applied"}

def face_forward(body, D_cm):
    """MF-FACE-PROJ-MAX: bimaxillary forward displacement of the lower face (maxilla + mandible region with the soft tissue
    over them), as a shape key on the rest mesh. D_cm is BUILDER-CHOSEN. Full displacement from 5 cm below the eye centres
    down to the chin; fades to zero at 2 cm below the eye centres (infraorbital) and under the chin (submental, 12.5-14.5 cm
    below the eye centres); fades out posteriorly (in front of the ear) and laterally (Gaussian, sigma 5 cm).
    Blender axes: forward = -y."""
    g = groups(body)
    if body.data.shape_keys is None: body.shape_key_add(name="Basis")
    kb = body.shape_key_add(name="WF_FaceProjMax", from_mix=True)
    for i, k in enumerate(body.data.shape_keys.key_blocks):
        if i > 0 and k.name != kb.name: k.value = 0.0
    kb.value = 1.0
    eyes = [np.mean([tuple(kb.data[i].co) for i, w in g["helper-%s-eye" % s].items() if w > 0.5], axis=0) for s in ("l", "r")]
    oc = (eyes[0] + eyes[1]) / 2; m = 0.01  # metres per cm
    hw = g.get("head", {})
    def smooth(t): t = min(max(t, 0.0), 1.0); return t * t * (3 - 2 * t)
    for i, w in hw.items():
        if w < 0.05: continue
        p = kb.data[i].co; dz = (oc[2] - p.z) / m; fwd = (oc[1] - p.y) / m
        gz = smooth((dz - 2.0) / 3.0) * (1.0 - smooth((dz - 12.5) / 2.0))
        gf = smooth((fwd + 4.0) / 6.0)
        gx = math.exp(-0.5 * (p.x / m / 5.0) ** 2)
        a = D_cm * m * w * gz * gf * gx
        p.y -= a
    body.data.update()
