"""RAC Stage C C4.1 §3: canonical GR-G1 on the PROTECTED (unorganized) route - frozen methods only, no new definitions.

GR-G1 in the accepted W1/W2 Grask route = skeletal_proxy (W1f/W1g/W1h): glenohumeral breadth (sphere fit on the -LEAN shoulder cap)
and biacromial (-LEAN acromion) over the CIB thoracic breadth S2 b, inset 2t, t in {0, 0.5, 1.0} cm x H/173.14; comparator MF-M-R,
operator <=, PASS / MARGINAL (< 1 %) / FAIL (w1e_checks), direction must hold at all three t.
The Stage C reading ran that method on the ORGANIZED grid (reference skin levels re-searched on the organized skin). Here the SAME
method runs on the protected unorganized route of skeletal_stations.unorganized_state (05D: same skeleton, every composition state rebuilt
WITHOUT the race organization). Readings:
  W1W2_route : skeletal_proxy + CIB(W1h, levels from the unorganized reference skin) over the unorganized states (the accepted W1/W2 method)
  05D_station: the same GH / biacromial landmarks over the 05D protected-station S2 b (skeleton-anchored levels)
  organized  : Stage C control (must reproduce the committed Stage C value)
Usage: python3 c41_gr_g1.py BODY_PREFIX OUT.json"""
import sys, os, json, shutil, tempfile, numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import skeletal_stations as SS, bony_envelope as BE, skeletal_proxy as SP, glob
S = "/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad"
DD = [S + "/w2c/donor", S + "/w2d/h", S + "/w1g/donor", S + "/w2d/donor"]
B, OUT = sys.argv[1], sys.argv[2]; d = os.path.dirname(B); n = os.path.basename(B); lean = B + "-LEAN"
tmp = tempfile.mkdtemp(); res = {"body": n}
try:
    grid = sorted(glob.glob(d + "/grid_%s/*_rest.npz" % n))
    un = [lean + "_rest.npz"] + [SS.unorganized_state(lean, g, "%s/u%02d_rest.npz" % (tmp, i), DD) for i, g in enumerate(grid)]
    uref = SS.unorganized_state(lean, B + "_rest.npz", tmp + "/%sU_rest.npz" % n, DD); un.append(uref)
    shutil.copy(B + "_r6.npz", tmp + "/%sU_r6.npz" % n)                       # same skeleton/pose: stature + leg share
    shutil.copy(lean + "_rest.npz", tmp + "/%sU-LEAN_rest.npz" % n); shutil.copy(lean + "_r6.npz", tmp + "/%sU-LEAN_r6.npz" % n)
    C = BE.cib(uref, un); cj = tmp + "/cib.json"; json.dump(C, open(cj, "w"), default=float)
    SP.main(tmp, tmp, n + "U", tmp + "/skp", cj)
    skp = json.load(open(tmp + "/skp/%sU_skp.json" % n))
    st = SS.read_body(B, DD)
    org = json.load(open(d + "/skp_%s/%s_skp.json" % (n, n)))
    for lab, src in (("W1W2_route", skp), ("organized", org)):
        res[lab] = {t: {"gh": v["extra"]["gh_breadth"], "biac": v["extra"]["biacromial"], "S2b": v["alpc_stations"]["S2"][0],
                        "S1_over_S2_b": v["ratio"]["S1_over_S2_b"], "biacromial_over_S2_b": v["ratio"]["biacromial_over_S2_b"]} for t, v in src["by_t"].items()}
    k = skp["stature_r6"] / 173.14; P = st["protected_unorganized_route"]["stations"]["S2"][0]
    res["05D_station"] = {}
    for t, v in skp["by_t"].items():
        tb = P - 2 * float(t) * k
        res["05D_station"][t] = {"gh": v["extra"]["gh_breadth"], "biac": v["extra"]["biacromial"], "S2b": tb,
                                 "S1_over_S2_b": v["extra"]["gh_breadth"] / tb, "biacromial_over_S2_b": v["extra"]["biacromial"] / tb}
    res["cib_argmin_S2"] = C["argmin"]["S2"]; res["cib_levels"] = C["station_levels_from_reference"]
    res["protected_station_S2"] = st["protected_unorganized_route"]["stations"]["S2"]; res["station_levels"] = st["levels"]
finally:
    shutil.rmtree(tmp, ignore_errors=True)
json.dump(res, open(OUT, "w"), indent=1, default=float); print(json.dumps(res, default=float)[:3000])
