"""RAC W1f AD-G14: SKELETAL-TRUNK PROXY + SCULPTED ENVELOPE body.

The skeleton is constructed on the skeletal-envelope body (minimum generator composition, build_variant "-LEAN") with the race's
skeletal bone scales B (bone-space, inherit-scale off: build_variant overrides "bone_scales"). The reference-composition envelope
is then SCULPTED onto that skeleton by adding the race's own reference-composition soft-tissue field, taken vertex by vertex from
a tissue donor pair (the same race inputs WITHOUT the skeletal bone scales B, at reference and at minimum composition, same
skeleton):     envelope = lean_B + (donor_ref - donor_lean)          (rest and R-6 separately; same topology)
So soft tissue is carried over unscaled: skeletal change does not inflate muscle or fat (the W1e skin-route failure mode), and the
composition firewall (AD-G15) holds by construction. Joints, weights and eyes come from lean_B (the skeleton).
Usage: python3 skeleton_envelope.py lean_B_prefix donor_ref_prefix donor_lean_prefix out_prefix
       (prefix = path without _rest.npz / _r6.npz)"""
import sys, os, json, numpy as np
JK = ["pelvis", "spine_01", "spine_02", "spine_03", "neck_01", "head", "thigh_l", "thigh_r", "calf_l", "calf_r", "foot_l", "foot_r",
      "clavicle_l", "clavicle_r", "upperarm_l", "upperarm_r", "lowerarm_l", "lowerarm_r", "hand_l", "hand_r"]

def simil(src, dst):
    """least-squares uniform scale + translation mapping the src rig joints onto dst (the generator's composition macros move the
    joint set by <= 0.8 % uniformly; this removes that so only soft tissue remains in the tissue field)"""
    js = json.loads(str(src["joints"])); jd = json.loads(str(dst["joints"]))
    P = np.array([jd[k][0] for k in JK]); Q = np.array([js[k][0] for k in JK]); pc, qc = P.mean(0), Q.mean(0)
    s = ((P - pc) * (Q - qc)).sum() / ((Q - qc) ** 2).sum()
    return lambda X: (np.asarray(X, float) - qc) * s + pc, s

def seam_smooth(V, F, mask_w, iters=30, lam=0.5, mu=-0.53):
    """Taubin (non-shrinking) smoothing of the skeleton surface, weighted per vertex by mask_w in [0, 1] (the AD-G14 'sculpt' of the
    bone-space seams between regionally scaled trunk bones). Only vertices with mask_w > 0 move."""
    n = len(V); E = np.r_[F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]]; E = np.r_[E, E[:, ::-1]]
    deg = np.bincount(E[:, 0], minlength=n).astype(float); deg[deg == 0] = 1
    X = V.copy()
    for it in range(iters):
        for f_ in (lam, mu):
            nb = np.zeros_like(X); np.add.at(nb, E[:, 0], X[E[:, 1]]); L = nb / deg[:, None] - X
            X = X + f_ * mask_w[:, None] * L
    return X

def trunk_sculpt(V, L, sc):
    """AD-G14 skeletal-trunk SCULPT on the skeleton surface: per-height depth and breadth factors about each trunk section's own
    centre, piecewise-linear over r = (u - hip-joint height) / (suprasternal proxy - hip-joint height).
    sc = {"r": [...], "kd": [...], "kb": [...]} or with "ka"/"kp" (anterior / posterior depth factors) instead of "kd".
    Arms and the free lower limbs are not moved (weights)."""
    J = json.loads(str(L["joints"])); hip = (J["thigh_l"][0][2] + J["thigh_r"][0][2]) / 2
    sst = (J["clavicle_l"][0][2] + J["clavicle_r"][0][2]) / 2
    armw = np.maximum.reduce([L["w_" + k] for k in ("upperarm_l", "upperarm_r", "lowerarm_l", "lowerarm_r", "hand_l", "hand_r", "fingers_l", "fingers_r")])
    legw = np.maximum.reduce([L["w_" + k] for k in ("thigh_l", "thigh_r", "calf_l", "calf_r", "foot_l", "foot_r")])
    r = (V[:, 2] - hip) / (sst - hip)
    wt = np.clip(1 - armw / 0.3, 0, 1) * np.clip(1 - np.maximum(legw - 0.5, 0) / 0.3, 0, 1) * L["keep"] * (r > -0.25) * (r < 1.15)
    kd = np.interp(r, sc["r"], sc.get("kd", [1.0] * len(sc["r"]))); kb = np.interp(r, sc["r"], sc["kb"])
    kd = 1 + (kd - 1) * wt; kb = 1 + (kb - 1) * wt
    trunk = L["keep"] & (armw < 0.05) & (legw < 0.5)
    zs = np.linspace(V[trunk, 2].min(), V[trunk, 2].max(), 120); cen = []
    for z in zs:
        m = trunk & (np.abs(V[:, 2] - z) < 0.8)
        cen.append(0.5 * (V[m, 1].max() + V[m, 1].min()) if m.sum() > 3 else np.nan)
    cen = np.array(cen); ok = ~np.isnan(cen); c = np.interp(V[:, 2], zs[ok], cen[ok])
    X = V.copy(); X[:, 0] = V[:, 0] * kb
    if "ka" in sc:      # separate anterior / posterior depth factors about the section centre (posterolateral ribcage depth, GO-G2)
        ka = 1 + (np.interp(r, sc["r"], sc["ka"]) - 1) * wt; kp = 1 + (np.interp(r, sc["r"], sc["kp"]) - 1) * wt
        X[:, 1] = c + (V[:, 1] - c) * np.where(V[:, 1] >= c, ka, kp)
    else:
        X[:, 1] = c + (V[:, 1] - c) * kd
    # smooth the displacement field over the mesh so partial arm / leg weights cannot crease the surface (pectoral, axilla)
    Dsp = X - V; F = L["F"]; n = len(V)
    E = np.r_[F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]]; E = np.r_[E, E[:, ::-1]]
    deg = np.bincount(E[:, 0], minlength=n).astype(float); deg[deg == 0] = 1
    for it in range(sc.get("disp_smooth_iters", 40)):
        nb = np.zeros_like(Dsp); np.add.at(nb, E[:, 0], Dsp[E[:, 1]]); Dsp = 0.5 * Dsp + 0.5 * nb / deg[:, None]
    return V + Dsp

def make(lean_b, donor_ref, donor_lean, out, tag=None, smooth=None, sculpt=None, tissue_scale=None):
    """tissue_scale=None: the donor pair is the same race (its lean is aligned to the skeleton like the donor lean);
    tissue_scale=k: the donor pair is ANOTHER body (W1f: the accepted human reference MF-M-R) and its tissue field is carried
    vertex-wise onto this skeleton, multiplied by k (stature ratio), with no alignment of the skeleton."""
    rec = {}
    for st in ("rest", "r6"):
        L = dict(np.load("%s_%s.npz" % (lean_b, st), allow_pickle=True))
        R = np.load("%s_%s.npz" % (donor_ref, st), allow_pickle=True); D = np.load("%s_%s.npz" % (donor_lean, st), allow_pickle=True)
        f, sc = simil(D, R)
        tissue = R["V"].astype(float) - f(D["V"])
        if tissue_scale is not None:
            tissue = tissue * tissue_scale; f = (lambda X: np.asarray(X, float)); sc = 1.0
        Vs = L["V"].astype(float)
        if sculpt:
            Vs = trunk_sculpt(Vs, L, sculpt)
            if not smooth:
                L2 = dict(L); L2["V"] = Vs.astype(np.float32); m2 = json.loads(str(L["meta"])); m2["trunk_sculpt"] = sculpt
                L2["meta"] = json.dumps(m2); np.savez_compressed("%s_%s.npz" % (lean_b, st), **L2)
        if smooth:      # {"lo_joint": "spine_01", "hi_joint": "neck_01", "iters": n}: trunk band between two rig joints, arms excluded
            Jl = json.loads(str(L["joints"])); lo = Jl[smooth["lo_joint"]][0][2]; hi = Jl[smooth["hi_joint"]][0][2]
            armw = np.maximum.reduce([L["w_" + k] for k in ("upperarm_l", "upperarm_r", "lowerarm_l", "lowerarm_r", "hand_l", "hand_r", "fingers_l", "fingers_r")])
            z = Vs[:, 2]; band = np.clip(np.minimum(z - lo, hi - z) / 4.0, 0, 1) * (armw < 0.05) * L["keep"]
            Vs = seam_smooth(Vs, L["F"], band.astype(float), iters=smooth.get("iters", 30))
            # the smoothed surface IS the skeleton: write it back as the skeletal-envelope body that skeletal_proxy.py measures
            L2 = dict(L); L2["V"] = Vs.astype(np.float32); m2 = json.loads(str(L["meta"])); m2["skeleton_seam_smoothing"] = smooth
            L2["meta"] = json.dumps(m2); np.savez_compressed("%s_%s.npz" % (lean_b, st), **L2)
        V = f(Vs) + tissue
        # re-ground (feet on u = 0) after adding plantar tissue
        keep = L["keep"]; z0 = V[keep, 2].min(); V[:, 2] -= z0
        J = json.loads(str(L["joints"])); J = {k: [(f(a) - [0, 0, z0]).tolist(), (f(b) - [0, 0, z0]).tolist()] for k, (a, b) in J.items()}
        L["V"] = V.astype(np.float32); L["joints"] = json.dumps(J)
        L["eye_l"] = f(L["eye_l"]) - np.array([0, 0, z0]); L["eye_r"] = f(L["eye_r"]) - np.array([0, 0, z0])
        meta = json.loads(str(L["meta"])); meta.update({"id": tag or os.path.basename(out), "construction": "AD-G14 skeletal proxy + sculpted envelope",
                                                       "skeleton": os.path.basename(lean_b), "tissue_donor": [os.path.basename(donor_ref), os.path.basename(donor_lean)], "skeleton_seam_smoothing": smooth, "trunk_sculpt": sculpt, "tissue_scale": tissue_scale})
        L["meta"] = json.dumps(meta)
        np.savez_compressed("%s_%s.npz" % (out, st), **L)
        rec[st] = {"stature": float(V[keep, 2].max()), "tissue_max_cm": float(np.linalg.norm(tissue, axis=1).max()), "lean_to_ref_scale": sc}
    return rec

if __name__ == "__main__":
    print(json.dumps(make(*sys.argv[1:5])))
