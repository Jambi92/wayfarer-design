# RAC W1i: ALPC-6 skin half, method attribution. Runs the ALPC-6 skin rows (GOR-BODY-16 vs MF and SK at the same low composition)
# twice: (1) official measurement layer (vertex slabs), (2) stations re-read on plane sections for all three bodies (restation.py).
# Usage: python3 alpc6_attrib.py go16_meas go16_rest mflow_meas mflow_rest sklow_meas sklow_rest skin_dir out.json
import sys, os, json, shutil, tempfile
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1'); sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/w1i_drivers')
import w1e_checks as W, alpc_invariance as AI, restation as RS
from collections import Counter

def run(pairs, skin_dir, sections):
    tmp = tempfile.mkdtemp(); os.makedirs(tmp + "/k")
    for idn, (m, r) in pairs.items():
        if sections: RS.restation(m, r, tmp + "/k/%s_meas.json" % idn)
        else: shutil.copy(m, tmp + "/k/%s_meas.json" % idn)
    for f in os.listdir(skin_dir):
        if f.endswith("_meas.json") and not os.path.exists(tmp + "/k/" + f): shutil.copy(os.path.join(skin_dir, f), tmp + "/k/" + f)
    rows = [r for r in W.run(tmp + "/k") if r["cand"] == "GO" and AI.keep_row(r["check"]) and "ALPC-3" not in r["check"]]
    shutil.rmtree(tmp, ignore_errors=True); return rows

if __name__ == "__main__":
    a = sys.argv[1:]; pairs = {"GO": (a[0], a[1]), "MF-M-R": (a[2], a[3]), "SK": (a[4], a[5])}
    out = {"slab (official measurement layer)": run(pairs, a[6], False), "plane sections (re-read)": run(pairs, a[6], True)}
    json.dump({"summary": {k: dict(Counter(r["result"] for r in v)) for k, v in out.items()}, "rows": out}, open(a[7], "w"), indent=1, default=float)
    for k, v in out.items():
        print(k, dict(Counter(r["result"] for r in v)))
        for r in v:
            if r["result"] != "PASS": print("   ", r["result"], r["check"][:70], round(r["va"], 4), r["op"], round(r["vb"], 4))
