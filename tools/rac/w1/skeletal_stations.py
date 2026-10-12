"""RAC RM-OT-05D (§4): SKELETON-ANCHORED ALPC station levels for organized race surfaces.

The W1h fixed-level CIB (bony_envelope.cib) takes the thorax-maximum (S2 b, S2 d) and waist-minimum (S4) slab levels from the REFERENCE
body's skin. Once a race base surface removes the human waist or re-lofts the thorax, those skin searches land at a different height. The
station is then read at another anatomical level: a false regression, while the skeleton has not changed (RM-OT-05C §6).

Here the levels come from the SKELETON surface (-LEAN, minimum composition: the same surface for the old and the organized route), and
every comparison uses the same levels. It is a measurement correction only. The stations themselves are unchanged (bony_envelope.fast_stations,
exact plane sections), and so are the composition-infimum rule and every relation threshold.

Readings returned for one body (its -LEAN, its composition grid, its reference):
  protected  CIB over the UNORGANIZED route (-LEAN + every grid state rebuilt without the race organization) at skeleton levels. These are
             the locked skeletal relations, and they depend on the skeleton only.
  organized  CIB over the organized grid at the same levels: a surface diagnostic.
  floor      the true skeletal floor (true_envelope.floor) sectioned at the same levels: what is actually protected.
  legacy     the own-skin-level readings (skeletal_proxy t = 0.0), for reference."""
import os, sys, json, glob, tempfile, shutil, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bony_envelope as BE, skeleton_envelope as SE

def levels(lean_rest):
    from arm_measure import load
    return BE.fast_stations(load(lean_rest), want_levels=True)[1]

def cib_at(align_ref, comps, lev):
    rows = {}
    for p in comps:
        st, r = BE.stations(align_ref, p, lev); rows[os.path.basename(p).replace("_rest.npz", "")] = st
    out = {"bony": {}, "argmin": {}}
    for S in BE.STATIONS:
        b = min(rows, key=lambda k: rows[k][S][0]); d = min(rows, key=lambda k: rows[k][S][1])
        out["bony"][S] = [rows[b][S][0], rows[d][S][1]]; out["argmin"][S] = [b, d]
    return out

def ratios(b):
    return {"bitroch_over_crest": b["S6"][0] / b["S5"][0], "pelvis_over_thorax_breadth": b["S5"][0] / b["S2"][0],
            "pelvic_depth_over_thorax_depth": b["S6"][1] / b["S2"][1], "S4_over_S2_b": b["S4"][0] / b["S2"][0], "S3_over_S2_d": b["S3"][1] / b["S2"][1]}

def _find_donor(name, dirs):
    for d in dirs:
        if os.path.exists("%s/%s_rest.npz" % (d, name)): return d + "/" + name
    raise FileNotFoundError(name)

def unorganized_state(lean_prefix, comp_rest, out_rest, donor_dirs):
    """the same composition state on the same skeleton WITHOUT the race organization (skeleton_envelope.make arithmetic, rest pose)"""
    C = dict(np.load(comp_rest, allow_pickle=True)); m = json.loads(str(C["meta"])); dr, dl = m["tissue_donor"]
    L = np.load(lean_prefix + "_rest.npz", allow_pickle=True)
    R = np.load(_find_donor(dr, donor_dirs) + "_rest.npz", allow_pickle=True); D = np.load(_find_donor(dl, donor_dirs) + "_rest.npz", allow_pickle=True)
    f, sc = SE.simil(D, R); V = f(L["V"].astype(float)) + R["V"].astype(float) - f(D["V"].astype(float))
    k = L["keep"].astype(bool); z0 = V[k, 2].min(); V[:, 2] -= z0
    J = json.loads(str(L["joints"])); J = {a: [(f(p) - [0, 0, z0]).tolist(), (f(q) - [0, 0, z0]).tolist()] for a, (p, q) in J.items()}
    C["V"] = V.astype(np.float32); C["joints"] = json.dumps(J); np.savez_compressed(out_rest, **C)
    return out_rest

def read_body(body_prefix, donor_dirs):
    """body_prefix = .../NAME/NAME (built by gr_body / go_body with a composition grid in .../NAME/grid_NAME)"""
    d = os.path.dirname(body_prefix); n = os.path.basename(body_prefix); lean = body_prefix + "-LEAN"
    lev = levels(lean + "_rest.npz"); grid = sorted(glob.glob(d + "/grid_%s/*_rest.npz" % n))
    tmp = tempfile.mkdtemp()
    try:
        un = [lean + "_rest.npz"] + [unorganized_state(lean, g, "%s/u%02d_rest.npz" % (tmp, i), donor_dirs) for i, g in enumerate(grid)] + \
             [unorganized_state(lean, body_prefix + "_rest.npz", tmp + "/uref_rest.npz", donor_dirs)]
        prot = cib_at(lean + "_rest.npz", un, lev)
        org = cib_at(lean + "_rest.npz", [lean + "_rest.npz"] + grid + [body_prefix + "_rest.npz"], lev)
        import true_envelope as TE
        Lr = dict(np.load(lean + "_rest.npz", allow_pickle=True)); Fv = TE.floor(Lr["V"].astype(float), Lr)[0]
        Lf = dict(Lr); Lf["V"] = Fv.astype(np.float32); fp = tmp + "/floor_rest.npz"; np.savez_compressed(fp, **Lf)
        flo = cib_at(lean + "_rest.npz", [fp], lev)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    out = {"levels_from": os.path.basename(lean) + " (skeleton surface)", "levels": lev,
           "protected_unorganized_route": {"stations": prot["bony"], "ratios": ratios(prot["bony"])},
           "organized": {"stations": org["bony"], "ratios": ratios(org["bony"]), "argmin": org["argmin"]},
           "true_floor": {"stations": flo["bony"], "ratios": ratios(flo["bony"])}}
    skp = d + "/skp_%s/%s_skp.json" % (n, n)
    if os.path.exists(skp):
        r = json.load(open(skp))["by_t"]["0.0"]["ratio"]; out["legacy_own_skin_levels"] = {k: r.get(k) for k in ("bitroch_over_crest", "pelvis_over_thorax_breadth", "pelvic_depth_over_thorax_depth")}
    return out

if __name__ == "__main__":
    S = "/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad"
    DD = [S + "/w2c/donor", S + "/w2d/h", S + "/w1g/donor", S + "/w2d/donor"]
    print(json.dumps(read_body(sys.argv[1], DD), indent=1, default=float))
