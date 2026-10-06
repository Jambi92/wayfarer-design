"""RAC W1f: ALPC-5 (frame invariance) and ALPC-6 (composition invariance) for Gorrund (GORRUND ALPC definition; RMQ RM-LR-06).
ALPC-5: ALPC-0...4 must pass on GOR-BODY-04 (Narrow) and GOR-BODY-12 (lower axial-breadth valid extreme) on the SKELETAL PROXY;
        the depth criteria (ALPC-1 depth items, ALPC-2a pelvic AP / thoracic depth) must pass on GOR-BODY-14 (lower thoracic-depth
        valid extreme) at least against MF.
ALPC-6: ALPC-0...4 pass on the skeletal proxy of the reference GO (W1f main run), and the SKIN profile of GOR-BODY-16 (low muscle,
        low fat) shows the same directions vs the MF skin profile (soft-tissue measures are never used as a pass condition).
Each variant is evaluated by substituting its readings for GO in a copy of the check inputs (skeletal: skeletal_checks.run over
the t sweep; skin: w1e_checks.run). Rows kept: ALPC-0, ALPC-1 (incl. 1b), ALPC-2a/2b, ALPC-3 (skeletal only), ALPC-4.
Usage: python3 alpc_invariance.py skp_dir skin_dir variants.json out.json
  variants.json: {"GOR-BODY-04": {"skp": dir_with_t*/ID_meas.json, "id": ID}, ...,
                  "GOR-BODY-16": {"skin_meas": path, "mf_low_meas": path, "sk_low_meas": path}}"""
import sys, os, json, shutil, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import skeletal_checks as SC, w1e_checks as W

def keep_row(chk, depth_only=False):
    c = chk
    alpc = any(k in c for k in ("ALPC-0", "ALPC-1 ", "ALPC-1b", "ALPC-2a", "ALPC-2b", "ALPC-3", "ALPC-4"))
    if not alpc or "ALPC-1c" in c: return False
    if depth_only: return ("depth" in c and "ALPC-1" in c) or "pelvic AP / thoracic depth" in c
    return True

def skeletal_variant(skp_dir, vdir, vid, skb=None):
    tmp = tempfile.mkdtemp(); shutil.copytree(skp_dir, tmp + "/s", symlinks=True)
    for t in SC.TS:
        dst = tmp + "/s/t%s/GO_meas.json" % t
        if os.path.lexists(dst): os.remove(dst)
        shutil.copy(os.path.join(vdir, "t%s" % t, vid + "_meas.json"), dst)
        if skb:     # equal-height Broad Skarn for this body's height
            d2 = tmp + "/s/t%s/SKB_meas.json" % t
            if os.path.lexists(d2): os.remove(d2)
            shutil.copy(os.path.join(skb[0], "t%s" % t, skb[1] + "_meas.json"), d2)
    rows = SC.run(tmp + "/s"); shutil.rmtree(tmp, ignore_errors=True); return rows

def main(skp_dir, skin_dir, vfile, out):
    V = json.load(open(vfile)); res = {}
    base = [r for r in SC.run(skp_dir) if r["cand"] == "GO" and keep_row(r["check"])]
    res["ALPC-6 skeletal proxy (reference GO)"] = base
    for name, depth_only in (("GOR-BODY-04", False), ("GOR-BODY-12", False), ("GOR-BODY-14", True)):
        if name in V:
            rows = skeletal_variant(skp_dir, V[name]["skp"], V[name]["id"])
            res["ALPC-5 " + name] = [r for r in rows if r["cand"] == "GO" and keep_row(r["check"], depth_only) and (not depth_only or r.get("b") in ("MF", "MF-M-R"))]
    if "GOR-BODY-02" in V:      # ALPC-7 must also pass on the 208 cm body (RMQ RM-LR-06), against the equal-height Broad Skarn
        v = V["GOR-BODY-02"]; rows = skeletal_variant(skp_dir, v["skp"], v["id"], (v["skb_skp"], v["skb_id"]))
        res["ALPC-7 GOR-BODY-02 (208 cm) vs Broad Skarn 208"] = [r for r in rows if r["cand"] == "GO" and "ALPC-7" in r["check"]]
        base7 = [r for r in SC.run(skp_dir) if r["cand"] == "GO" and "ALPC-7" in r["check"]]
        res["ALPC-7 reference GO (229 cm) vs Broad Skarn 229"] = base7
    if "GOR-BODY-16" in V:
        tmp = tempfile.mkdtemp(); shutil.copytree(skin_dir, tmp + "/k", symlinks=True)
        dst = tmp + "/k/GO_meas.json"
        if os.path.lexists(dst): os.remove(dst)
        shutil.copy(V["GOR-BODY-16"]["skin_meas"], dst)
        # composition-matched comparators: MF (and SK) at the same low composition, so soft tissue cannot create or hide a direction
        for k, idn in (("mf_low_meas", "MF-M-R"), ("sk_low_meas", "SK")):
            if k in V["GOR-BODY-16"]:
                d2 = tmp + "/k/%s_meas.json" % idn
                if os.path.lexists(d2): os.remove(d2)
                shutil.copy(V["GOR-BODY-16"][k], d2)
        rows = [r for r in W.run(tmp + "/k") if r["cand"] == "GO" and keep_row(r["check"]) and "ALPC-3" not in r["check"]]
        res["ALPC-6 GOR-BODY-16 skin profile (directions vs MF%s)" % (" at matched low composition" if "mf_low_meas" in V["GOR-BODY-16"] else "")] = rows
    summ = {}
    for k, rows in res.items():
        from collections import Counter
        summ[k] = dict(Counter(r["result"] for r in rows))
    json.dump({"summary": summ, "rows": res}, open(out, "w"), indent=1, default=float)
    print(json.dumps(summ, indent=1))
    for k, rows in res.items():
        for r in rows:
            if r["result"] not in ("PASS",): print(k, "|", r["result"], "|", r["check"], "|", r.get("va"), r["op"], r.get("vb"))

if __name__ == "__main__":
    main(*sys.argv[1:5])
