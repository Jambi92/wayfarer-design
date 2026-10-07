# joint breadths (combined convention: anatomy from rest, normalized to R-6 stature) with the +/-1 cm slab held absolute (as measured)
# and scaled with stature (slab = 1 cm x stature / MF-M-R stature 173.14). Usage: jbw.py MODDIR OUT.json PREFIX...  (PREFIX_rest.npz, PREFIX_r6.npz)
# MODDIR holds am_win.py built by make_am_win.sh.
import sys, json; sys.path.insert(0, sys.argv[1]); import am_win as A
MF = 173.1428; out = {}
J = ("elbow", "wrist", "knee", "ankle")
for p in sys.argv[3:]:
    A.JBWIN[0] = 1.0; st = A.measure(p + "_r6.npz")["stature"]; r = {"stature": st}
    for mode, win in (("abs", 1.0), ("scaled", st / MF)):
        A.JBWIN[0] = win; m = A.measure(p + "_rest.npz")["mean"]
        r[mode] = {k: m[k + "_breadth"] / st for k in J}; r[mode + "_window_cm"] = win
    out[p.split('/')[-1]] = r
    print("%-14s %6.2f abs %s | scaled %s" % (p.split('/')[-1][:14], st, " ".join("%.4f" % r["abs"][k] for k in J), " ".join("%.4f" % r["scaled"][k] for k in J)), flush=True)
json.dump(out, open(sys.argv[2], "w"), indent=1)
