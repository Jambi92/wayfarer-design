"""RAC W1g (AD-W1G-1, M-1(a)): COMPOSITION-INFIMUM BONY ENVELOPE (CIB) - the explicit bony-station model that stays physically
inside every tested composition.

Problem (W1f M-3): the W1f skeletal proxy read the skeleton off the generator's minimum-composition body (muscle 0, weight 0).
At the iliac crest (S5) that body is WIDER than the same skeleton at other compositions (the generator's min/min corner adds
lateral pelvic volume), so some skins lay inside the "skeleton" (GOR-BODY-16: about 3 cm per side) - physically impossible.

Model (BUILDER-CHOSEN, R-14; measurer method, not canon):
  The same skeleton is built across the generator composition grid  G = {muscle, weight} in {0, 0.25, 0.5}^2  (9 bodies; this
  contains the reference composition 0.5/0.5 and the ALPC-6 low composition 0.25/0.25). Each body is aligned to the reference
  body's rig joints (least-squares similarity, as skeletal_proxy.align) and its ALPC stations S2...S7 are read (arm_measure).
  The bony station value is the INFIMUM over G, separately for breadth and depth:
        bony(S) = min over g in G of skin_g(S)                               (then inset 2t by skeletal_proxy, t sweep)
  Bone cannot be wider than the thinnest skin of the same skeleton, so this is the tightest generator-supported UPPER BOUND on the
  bony value; by construction every tested composition's skin lies on or outside it (physical validity). It is not a measurement
  of bone: true bony values may be smaller; the residual is covered only by the t sweep. Grid resolution is a disclosed limit.
  Proximal-femur scale (hip centre -> greater trochanter) is the lateral extremum at the S6 level, so it is reduced by half the
  S6-breadth correction:  pf_bony = pf_lean - (S6_lean - S6_bony) / 2.
For AD-G14 bodies (GO, GR and their variants) every grid body is assembled with the same route as the reference:
  body_g = skeleton (sculpted lean_B) + (donor_g - donor_lean)   (skeleton_envelope.make, no further sculpt).
Usage: python3 bony_envelope.py ref_rest.npz out.json comp_rest.npz [comp_rest.npz ...]"""
import sys, os, json, tempfile, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import skeletal_proxy as SP
from arm_measure import measure

GRID = [(m, w) for m in (0.0, 0.25, 0.5) for w in (0.0, 0.25, 0.5)]
STATIONS = ("S2", "S3", "S4", "S5", "S6", "S7")

def tag(m, w):
    return "C%03d%03d" % (round(m * 100), round(w * 100))

def fast_stations(d):
    """S2...S7 exactly as arm_measure.measure computes alpc_stations (same slabs, masks and levels), without the rest of measure"""
    V = d["V"].astype(float); keep = d["keep"]; J = d["joints"]; w = lambda k: d["w_" + k]; head = lambda n: np.asarray(J[n][0], float)
    armw = np.maximum.reduce([w(k) for k in ("upperarm_l", "upperarm_r", "lowerarm_l", "lowerarm_r", "hand_l", "hand_r", "fingers_l", "fingers_r")])
    trunk = keep & (armw < 0.2)
    def slab(level, mask, half=1.0):
        m = mask & (np.abs(V[:, 2] - level) < half); P = V[m]
        return (float(P[:, 0].max() - P[:, 0].min()), float(P[:, 1].max() - P[:, 1].min())) if len(P) > 5 else (np.nan, np.nan)
    sh_u = (head("upperarm_l")[2] + head("upperarm_r")[2]) / 2; hipc = (head("thigh_l") + head("thigh_r")) / 2
    lv = np.linspace(head("spine_02")[2], sh_u - 2, 12); vals = [slab(z, trunk) for z in lv]
    st = {"S2": (float(np.nanmax([v[0] for v in vals])), float(np.nanmax([v[1] for v in vals])))}
    s02 = head("spine_03")[2]; s01 = head("spine_01")[2]
    st["S3"] = slab(s02, trunk)
    zs = np.linspace(s01, s02, 9); vv = [slab(z, trunk) for z in zs]; k = int(np.nanargmin([v[0] for v in vv])); st["S4"] = vv[k]
    st["S5"] = (slab(s01, trunk)[0], slab(s01, trunk)[1])
    bt = trunk & (np.abs(V[:, 2] - hipc[2]) < 3)
    st["S6"] = (float(V[bt, 0].max() - V[bt, 0].min()), slab(hipc[2], trunk)[1])
    th = []
    for sd in ("l", "r"):
        hp_, kn_ = head("thigh_" + sd), head("calf_" + sd); ax = (kn_ - hp_) / np.linalg.norm(kn_ - hp_)
        tv = np.where(keep & (w("thigh_" + sd) > 0.5))[0]; P = V[tv] - hp_; t = P @ ax
        m_ = np.abs(t - 0.2 * np.linalg.norm(kn_ - hp_)) < 0.8; Q = P[m_] - np.outer(t[m_], ax)
        th.append((float(Q[:, 0].max() - Q[:, 0].min()), float(Q[:, 1].max() - Q[:, 1].min())))
    st["S7"] = tuple(np.mean(th, axis=0))
    return {k: [float(a), float(b)] for k, (a, b) in st.items()}

def stations(ref_rest, comp_rest):
    from arm_measure import load
    tmp = tempfile.mkdtemp(); a = os.path.join(tmp, "a.npz"); s, r = SP.align(comp_rest, ref_rest, a)
    return fast_stations(load(a)), r

def cib(ref_rest, comps):
    rows = {}
    for p in comps:
        st, r = stations(ref_rest, p); rows[os.path.basename(p).replace("_rest.npz", "")] = {"stations": st, "align_resid_cm": r}
    out = {"ref": os.path.basename(ref_rest), "n": len(rows), "per_body": rows, "bony": {}, "argmin": {}}
    for S in STATIONS:
        b = min(rows, key=lambda k: rows[k]["stations"][S][0]); d = min(rows, key=lambda k: rows[k]["stations"][S][1])
        out["bony"][S] = [rows[b]["stations"][S][0], rows[d]["stations"][S][1]]; out["argmin"][S] = [b, d]
    from arm_measure import load as _ld
    ref_st = fast_stations(_ld(ref_rest))
    out["ref_skin"] = {S: ref_st[S] for S in STATIONS}
    out["tissue_per_side_min_cm"] = {k: {S: [(v["stations"][S][0] - out["bony"][S][0]) / 2, (v["stations"][S][1] - out["bony"][S][1]) / 2]
                                         for S in STATIONS} for k, v in rows.items()}
    return out

def assemble_grid(lean_b, donor_dir, donor_id, donor_lean, out_dir, out_id):
    """AD-G14 grid bodies: skeleton lean_b (already sculpted) + (donor_g - donor_lean). Returns list of rest paths (incl. lean_b)."""
    import skeleton_envelope as SE
    paths = [lean_b + "_rest.npz"]
    for m, w in GRID:
        if (m, w) == (0.0, 0.0): continue
        dp = os.path.join(donor_dir, "%s-%s" % (donor_id, tag(m, w)))
        if not os.path.exists(dp + "_rest.npz"): raise FileNotFoundError(dp)
        op = os.path.join(out_dir, "%s-%s" % (out_id, tag(m, w)))
        if not os.path.exists(op + "_rest.npz"): SE.make(lean_b, dp, donor_lean, op, tag=out_id + "-" + tag(m, w))
        paths.append(op + "_rest.npz")
    return paths

if __name__ == "__main__":
    ref, out = sys.argv[1], sys.argv[2]
    R = cib(ref, sys.argv[3:]); json.dump(R, open(out, "w"), indent=1, default=float)
    print(json.dumps({S: [round(R["bony"][S][0], 2), round(R["bony"][S][1], 2), R["argmin"][S]] for S in STATIONS}))
