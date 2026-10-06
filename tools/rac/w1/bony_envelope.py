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

def fast_stations(d, levels=None, want_levels=False, section=None):
    """S2...S7 exactly as arm_measure.measure computes alpc_stations (same slabs, masks and levels), without the rest of measure.
    W1h (AD-W1H-1/-3 station-level refinement): levels = {"S2b", "S2d", "S4"} slab indices taken from the REFERENCE body; when given,
    the thorax-maximum and waist stations are read at those fixed levels instead of being re-searched in every composition body
    (a re-search can jump to a different anatomical level in one grid body and set the infimum alone - a station artifact).
    section=False reproduces the measurement layer (arm_measure.measure: vertex slabs) on the same body."""
    V = d["V"].astype(float); keep = d["keep"]; J = d["joints"]; w = lambda k: d["w_" + k]; head = lambda n: np.asarray(J[n][0], float)
    armw = np.maximum.reduce([w(k) for k in ("upperarm_l", "upperarm_r", "lowerarm_l", "lowerarm_r", "hand_l", "hand_r", "fingers_l", "fingers_r")])
    trunk = keep & (armw < 0.2)
    Fm = d["F"]; TF = Fm[trunk[Fm].all(1)]
    def slab(level, mask, half=1.0):
        if (SECTION if section is None else section):   # W1h: exact plane section of the trunk faces (vertex slabs miss whole vertex rings where the mesh is stretched)
            A, B, Cc = V[TF[:, 0]], V[TF[:, 1]], V[TF[:, 2]]; pts = []
            for a, b in ((A, B), (B, Cc), (Cc, A)):
                m = (a[:, 2] - level) * (b[:, 2] - level) < 0; t = (level - a[m, 2]) / (b[m, 2] - a[m, 2]); pts.append(a[m, :2] + (b[m, :2] - a[m, :2]) * t[:, None])
            P = np.vstack(pts)
            return (float(np.ptp(P[:, 0])), float(np.ptp(P[:, 1]))) if len(P) > 5 else (np.nan, np.nan)
        m = mask & (np.abs(V[:, 2] - level) < half); P = V[m]
        return (float(P[:, 0].max() - P[:, 0].min()), float(P[:, 1].max() - P[:, 1].min())) if len(P) > 5 else (np.nan, np.nan)
    sh_u = (head("upperarm_l")[2] + head("upperarm_r")[2]) / 2; hipc = (head("thigh_l") + head("thigh_r")) / 2
    lv = np.linspace(head("spine_02")[2], sh_u - 2, 12); vals = [slab(z, trunk) for z in lv]
    i2b = int(np.nanargmax([v[0] for v in vals])) if levels is None else levels["S2b"]; i2d = int(np.nanargmax([v[1] for v in vals])) if levels is None else levels["S2d"]
    st = {"S2": (float(vals[i2b][0]), float(vals[i2d][1]))}
    s02 = head("spine_03")[2]; s01 = head("spine_01")[2]
    st["S3"] = slab(s02, trunk)
    zs = np.linspace(s01, s02, 9); vv = [slab(z, trunk) for z in zs]; k = int(np.nanargmin([v[0] for v in vv])) if levels is None else levels["S4"]; st["S4"] = vv[k]
    st["S5"] = (slab(s01, trunk)[0], slab(s01, trunk)[1])
    bt = trunk & (np.abs(V[:, 2] - hipc[2]) < 3)
    st["S6"] = (float(V[bt, 0].max() - V[bt, 0].min()), slab(hipc[2], trunk)[1])
    for key, frac in (("S7", 0.2),):
        th = []
        for sd in ("l", "r"):
            hp_, kn_ = head("thigh_" + sd), head("calf_" + sd); ax = (kn_ - hp_) / np.linalg.norm(kn_ - hp_)
            tv = np.where(keep & (w("thigh_" + sd) > 0.5))[0]; P = V[tv] - hp_; t = P @ ax
            m_ = np.abs(t - frac * np.linalg.norm(kn_ - hp_)) < 0.8; Q = P[m_] - np.outer(t[m_], ax)
            th.append((float(Q[:, 0].max() - Q[:, 0].min()), float(Q[:, 1].max() - Q[:, 1].min())))
        st[key] = tuple(np.mean(th, axis=0))
    out = {k: [float(a), float(b)] for k, (a, b) in st.items()}
    return (out, {"S2b": i2b, "S2d": i2d, "S4": k}) if want_levels else out

SECTION = True        # W1h: trunk stations read on exact plane sections (set False with FIXED_LEVELS False to reproduce W1g)
FIXED_LEVELS = True   # W1h: read S2 / S4 at the reference body's levels (set False to reproduce W1g)

def stations(ref_rest, comp_rest, levels=None):
    from arm_measure import load
    import shutil
    tmp = tempfile.mkdtemp(); a = os.path.join(tmp, "a.npz"); s, r = SP.align(comp_rest, ref_rest, a)
    st = fast_stations(load(a), levels=levels); shutil.rmtree(tmp, ignore_errors=True)    # W1h: no temp build-up
    return st, r

def cib(ref_rest, comps):
    from arm_measure import load as _l0
    lev = fast_stations(_l0(ref_rest), want_levels=True)[1] if FIXED_LEVELS else None
    rows = {}
    for p in comps:
        st, r = stations(ref_rest, p, lev); rows[os.path.basename(p).replace("_rest.npz", "")] = {"stations": st, "align_resid_cm": r}
    out = {"ref": os.path.basename(ref_rest), "n": len(rows), "per_body": rows, "bony": {}, "argmin": {}, "station_levels_from_reference": lev,
           "no_lean_clamp": bool(lev)}   # with fixed levels the minimum-composition body is in the grid at the same levels
    for S in STATIONS:
        b = min(rows, key=lambda k: rows[k]["stations"][S][0]); d = min(rows, key=lambda k: rows[k]["stations"][S][1])
        out["bony"][S] = [rows[b]["stations"][S][0], rows[d]["stations"][S][1]]; out["argmin"][S] = [b, d]
    from arm_measure import load as _ld
    ref_st = fast_stations(_ld(ref_rest))
    out["ref_skin"] = {S: ref_st[S] for S in STATIONS}
    out["tissue_per_side_min_cm"] = {k: {S: [(v["stations"][S][0] - out["bony"][S][0]) / 2, (v["stations"][S][1] - out["bony"][S][1]) / 2]
                                         for S in STATIONS} for k, v in rows.items()}
    return out

def cib8(C):
    """W1h SENSITIVITY variant (AD-W1H-1 / -3): the same infimum with the generator's (muscle 0, weight 0) corner body EXCLUDED.
    That corner shows features no neighbouring composition has (MF: wasp waist and crest flare; MF: knee; GOR-BODY-03: lower-thorax
    depth collapse at the maximum height macro). Used only to isolate generator-corner artifacts; the accepted reading stays CIB."""
    rows = {k: v for k, v in C["per_body"].items() if not k.endswith("-LEAN")}
    out = dict(C); out = {k: v for k, v in C.items() if k not in ("bony", "argmin", "tissue_per_side_min_cm")}
    out["variant"] = "CIB-8 (generator minimum corner excluded; sensitivity only)"; out["no_lean_clamp"] = True; out["bony"] = {}; out["argmin"] = {}
    for S in STATIONS:
        b = min(rows, key=lambda k: rows[k]["stations"][S][0]); d = min(rows, key=lambda k: rows[k]["stations"][S][1])
        out["bony"][S] = [rows[b]["stations"][S][0], rows[d]["stations"][S][1]]; out["argmin"][S] = [b, d]
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
