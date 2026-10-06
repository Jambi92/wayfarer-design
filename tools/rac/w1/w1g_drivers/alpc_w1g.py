# RAC W1g driver AS RUN (scratch paths = this session's working directories; kept for provenance).
"""W1g ALPC stress evaluation on the CIB skeletal readings (AD-W1G-1, -5):
ALPC-5 (GOR-BODY-04 / -12: ALPC-0...4; GOR-BODY-14: depth criteria vs MF), stature stress (GOR-BODY-02 208 cm, GOR-BODY-03 maximum
generator-reachable height: ALPC-0...4), ALPC-7 at every tested Gorrund / Broad Skarn height pair with Skarn height >= Gorrund
height (208 / 215 / 222 / 229 cm), and ALPC-6 (skeletal half = reference GO; skin half = GOR-BODY-16 = the reference GO
skeleton at muscle 0.25 / weight 0.25 through the same AD-G14 route, read against MF and SK at the same composition).
Usage: python3 alpc_w1g.py skp_dir stress_dir go16_meas mf_low_meas sk_low_meas out.json"""
import sys, os, json, shutil, tempfile
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1')
import skeletal_checks as SC, w1e_checks as W, alpc_invariance as AI
from collections import Counter

def sub(skp_dir, repl):
    """copy skp_dir, replace t*/<ID>_meas.json from {ID: (dir_with_t*, src_id)}"""
    tmp = tempfile.mkdtemp(); shutil.copytree(skp_dir, tmp + "/s", symlinks=True, ignore=shutil.ignore_patterns('*_skp.json', '*.json.bak'))
    for t in SC.TS:
        for idn, (d, sid) in repl.items():
            dst = tmp + "/s/t%s/%s_meas.json" % (t, idn)
            if os.path.lexists(dst): os.remove(dst)
            shutil.copy(os.path.join(d, "t%s" % t, sid + "_meas.json"), dst)
    return SC.run(tmp + "/s")

def main(skp, sd, go16, mflow, sklow, out):
    res = {}
    keep = lambda r, depth=False: r["cand"] == "GO" and AI.keep_row(r["check"], depth)
    for n, depth in (("GOR-BODY-04", False), ("GOR-BODY-12", False), ("GOR-BODY-14", True)):
        rows = sub(skp, {"GO": (sd + "/skp_" + n, n)})
        res["ALPC-5 " + n] = [r for r in rows if keep(r, depth) and (not depth or r.get("b") in ("MF", "MF-M-R"))]
    for n in ("GOR-BODY-02", "GOR-BODY-03"):
        rows = sub(skp, {"GO": (sd + "/skp_" + n, n)})
        res["Stature stress %s: ALPC-0...4" % n] = [r for r in rows if keep(r)]
    GOH = {208: (sd + "/skp_GOR-BODY-02", "GOR-BODY-02"), 215: (sd + "/skp_GO-H215", "GO-H215"), 222: (sd + "/skp_GO-H222", "GO-H222"), 229: (skp, "GO")}
    SKBH = {208: (skp, "SKB208"), 215: (sd + "/skp_SKB215", "SKB215"), 222: (sd + "/skp_SKB222", "SKB222"), 229: (skp, "SKB229")}
    for hg, gsrc in GOH.items():
        for hs, ssrc in SKBH.items():
            if hs < hg: continue
            rows = sub(skp, {"GO": gsrc, "SKB": ssrc})
            res["ALPC-7 GO %d cm vs Broad Skarn %d cm" % (hg, hs)] = [r for r in rows if r["cand"] == "GO" and "ALPC-7" in r["check"]]
    res["ALPC-6 skeletal half (reference GO skeleton = GOR-BODY-16 skeleton)"] = [r for r in SC.run(skp) if keep(r)]
    tmp = tempfile.mkdtemp(); os.makedirs(tmp + "/k")
    for idn, p in (("GO", go16), ("MF-M-R", mflow), ("SK", sklow)): shutil.copy(p, tmp + "/k/%s_meas.json" % idn)
    # w1e_checks needs every body it reads; fill the others from the reference skin directory
    ref_skin = os.environ["SKIN_DIR"]
    for f in os.listdir(ref_skin):
        if f.endswith("_meas.json") and not os.path.exists(tmp + "/k/" + f): shutil.copy(os.path.join(ref_skin, f), tmp + "/k/" + f)
    res["ALPC-6 skin half: GOR-BODY-16 skin vs MF and SK at the same low composition"] = [r for r in W.run(tmp + "/k") if keep(r) and "ALPC-3" not in r["check"]]
    summ = {k: dict(Counter(r["result"] for r in v)) for k, v in res.items()}
    json.dump({"summary": summ, "rows": res}, open(out, "w"), indent=1, default=float)
    print(json.dumps(summ, indent=1))
    for k, rows in res.items():
        for r in rows:
            if r["result"] != "PASS": print(k, "|", r["result"], "|", r["check"], "|", r.get("va"), r["op"], r.get("vb"))

if __name__ == "__main__":
    main(*sys.argv[1:7])
