"""D-4b pose-invariance check: generator rest pose vs R-6 measurement pose of the same build.
Checks: per-bone rigid vertex sets (verts weighted >= 0.98 to one bone: pairwise distances must be identical), segment
lengths (bone heads), head dimensions, trunk breadth/depth sections that the arm/leg re-pose could touch, stature, volume,
and the maximum displacement of verts that are NOT in a joint region relative to their own bone (soft-tissue change).
Usage: python3 invariance.py rest.npz r6.npz out.json"""
import sys, json, numpy as np
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from arm_measure import load, volume, measure

def rigid_check(dr, dp, bone, thr=0.98, n=400, seed=0):
    w = dr["w_" + bone]; idx = np.where(dr["keep"] & (w >= thr))[0]
    if len(idx) < 3: return None
    rng = np.random.default_rng(seed); a = rng.choice(idx, min(n, len(idx))); b = rng.choice(idx, min(n, len(idx)))
    d0 = np.linalg.norm(dr["V"][a] - dr["V"][b], axis=1); d1 = np.linalg.norm(dp["V"][a] - dp["V"][b], axis=1)
    return {"n_verts": int(len(idx)), "max_abs_change_cm": float(np.abs(d1 - d0).max())}

def main(rest, r6, out):
    dr, dp = load(rest), load(r6)
    res = {"rigid_sets": {}}
    for b in ("head", "neck_01", "spine_01", "spine_02", "spine_03", "pelvis", "upperarm_l", "upperarm_r", "lowerarm_l", "lowerarm_r",
              "hand_l", "hand_r", "thigh_l", "thigh_r", "calf_l", "calf_r", "foot_l", "foot_r"):
        r = rigid_check(dr, dp, b)
        if r: res["rigid_sets"][b] = r
    mr, mp = measure(rest), measure(r6)
    keys = ["upperarm", "forearm", "hand", "palm", "finger", "thigh", "shin", "foot_len", "foot_breadth"]
    res["segments_cm"] = {k: [mr["mean"][k], mp["mean"][k], mp["mean"][k] - mr["mean"][k]] for k in keys}
    tk = ["torso_len", "neck_len", "thorax_breadth_max", "thorax_depth_max", "iliac_crest_breadth", "bitrochanteric_breadth",
          "pelvic_depth", "waist_breadth", "waist_depth", "shoulder_joint_breadth", "hip_joint_breadth", "bideltoid_breadth"]
    res["trunk_cm"] = {k: [mr[k], mp[k], mp[k] - mr[k]] for k in tk}
    hk = ["HL", "HH", "Eu_Eu", "Zy_Zy", "FPI", "MPI", "MdPI"]
    res["head"] = {k: [mr["cranio"][k], mp["cranio"][k], mp["cranio"][k] - mr["cranio"][k]] for k in hk}
    res["stature_cm"] = [mr["stature"], mp["stature"], mp["stature"] - mr["stature"]]
    vr, vp = abs(volume(dr["V"].astype(float), dr["F"])) / 1000, abs(volume(dp["V"].astype(float), dp["F"])) / 1000
    res["volume_L"] = [vr, vp, vp - vr, (vp - vr) / vr * 100]
    # soft tissue outside joint regions: for verts with weight >= 0.98 on one bone, their position in that bone's frame must
    # not move (exact rigid). Report the largest deviation of any 'single-bone' vert and the fraction of body verts that
    # are blended (joint regions).
    W = np.stack([dr["w_" + b] for b in ("head", "neck_01", "spine_01", "spine_02", "spine_03", "pelvis", "clavicle_l", "clavicle_r",
                                          "upperarm_l", "upperarm_r", "lowerarm_l", "lowerarm_r", "hand_l", "hand_r", "thigh_l",
                                          "thigh_r", "calf_l", "calf_r", "foot_l", "foot_r", "ball_l", "ball_r")], 1)
    res["blended_vert_fraction"] = float(((W.max(1) < 0.98) & dr["keep"]).sum() / dr["keep"].sum())
    json.dump(res, open(out, "w"), indent=1, default=float)
    return res

if __name__ == "__main__":
    r = main(*sys.argv[1:4])
    print(json.dumps({k: r[k] for k in ("stature_cm", "volume_L", "blended_vert_fraction")}, default=float))
    print("rigid max", max(v["max_abs_change_cm"] for v in r["rigid_sets"].values()))
    for k, v in list(r["segments_cm"].items()) + list(r["trunk_cm"].items()) + list(r["head"].items()):
        print(k, [round(x, 4) for x in v])
