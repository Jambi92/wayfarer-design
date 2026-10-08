# RAC W2C1 elbow / wrist / ankle method check: slab (stature-scaled) vs exact-plane section ratio per body, and the ordering / margin of
# the accepted joint comparisons under both readings. Measurement check only; no body is modified.  Usage: python3 ewa_check.py OUT.json JOINTS.json...
import sys, json
J = {}
for p in sys.argv[2:]: J.update(json.load(open(p)))
PAIRS = [("SKM190", "MFM190", "W2B overlap 190 config 1 (Skarn > Marchfolk)"), ("SKM203", "MFM203", "W2B overlap 203 config 1"), ("SKF190", "MFF190K3", "W2B overlap 190 config 2"),
         ("SKF203", "MFF203", "W2B overlap 203 config 2"), ("SKM183", "MFM203", "W2B canonical pair config 1 (unadjusted for stature)"), ("GO-H208", "GR208", "Gorrund > Grask at 208 cm"),
         ("GO217", "GR218R", "Gorrund > Grask at 217-218 cm"), ("SKM218", "GR218R", "Skarn vs Grask 218 (report: undetermined by canon)"), ("SKM229", "GR229", "Skarn vs Grask 229 (report)"),
         ("MNX", "AEL1", "W2A1 Narrow Marchfolk vs Aelari (unadjusted for stature)"), ("MF-M-R", "AEL1", "Marchfolk central vs Aelari (unadjusted)"), ("MF-M-R", "FNL4", "Marchfolk central vs Fenn (unadjusted)"),
         ("SKMBroad", "GO-H208", "Broad Skarn vs Gorrund 208 (report, AD-4)"), ("SKMNarrow", "MFM203", "Narrow Skarn vs Marchfolk 203 (unadjusted)"), ("GRB2", "SKMB218" if "SKMB218" in J else "SKM218", "Broad Grask vs Skarn (report)")]
out = {"ratio_slab_over_section": {n: {j: J[n]["slab_scaled"][j] / J[n]["section"][j] for j in ("elbow", "wrist", "knee", "ankle")} for n in J}, "pairs": []}
for a, b, lab in PAIRS:
    if a not in J or b not in J: continue
    for j in ("elbow", "wrist", "ankle", "knee"):
        ms = 100 * (J[a]["slab_scaled"][j] / J[b]["slab_scaled"][j] - 1); mp = 100 * (J[a]["section"][j] / J[b]["section"][j] - 1)
        flip = (ms > 0) != (mp > 0) or ((abs(ms) >= 1) != (abs(mp) >= 1))
        out["pairs"].append({"pair": lab, "a": a, "b": b, "joint": j, "slab_margin_pct": ms, "section_margin_pct": mp, "ordering_or_1pct_class_changes": flip})
json.dump(out, open(sys.argv[1], "w"), indent=1)
for j in ("elbow", "wrist", "ankle", "knee"):
    v = [r[j] for r in out["ratio_slab_over_section"].values()]; print("%-6s slab/section %.3f .. %.3f" % (j, min(v), max(v)))
for r in out["pairs"]: print("%-58s %-6s slab %+6.1f%%  section %+6.1f%% %s" % (r["pair"][:58], r["joint"], r["slab_margin_pct"], r["section_margin_pct"], "<-- CLASS CHANGE" if r["ordering_or_1pct_class_changes"] else ""))
