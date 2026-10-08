# RAC W2C: stature-matched human reference for the W1 rows whose reference is a fixed-stature human body (MF-M-R 173 cm / SK 208 cm).
# The generator's own height allometry moves the human references in the same direction as Grask; this reports where each Grask stature
# body sits against the Marchfolk reference carried to the same stature (linear in stature between the accepted MF 173 and MF 203 bodies;
# beyond 203 cm an EXTRAPOLATION, diagnostic) and against matched-height Skarn where one exists. Report only; no row is re-scored.
# Usage: python3 w2c_drift.py W2C.json OUT.json
import sys, json
d = json.load(open(sys.argv[1])); V = d["values"]
K = [("GR-G1 shoulder-joint / thoracic breadth (skeletal, t=0) <= MF", "skeletal shoulder-joint / thoracic breadth [t=0.0]"), ("GR-P6 crest / thoracic breadth (skeletal, t=0) ~ MF", "skeletal crest / thoracic breadth [t=0.0]"),
     ("GR-P2b bitrochanteric / crest (skeletal, t=0) >= MF", "skeletal bitrochanteric / crest [t=0.0]"), ("lower leg / leg > MF, SK", "shin_over_leg"), ("forearm / arm > MF, SK", "forearm_over_arm"),
     ("pelvic vertical / stature (skeletal, t=0)", "skeletal pelvic vertical / stature [t=0.0]")]
mf0, mf1 = V["MF173"], V["MF203"]; h0, h1 = mf0["stature (cm)"], mf1["stature (cm)"]
out = []
for name, k in K:
    for g, sk in (("GR198", "SK198"), ("GR208", "SK208"), ("GR218", "SK218"), ("GR229", "SK229"), ("GR239", None)):
        h = V[g]["stature (cm)"]; mfh = mf0[k] + (mf1[k] - mf0[k]) * (h - h0) / (h1 - h0)
        row = {"row": name, "body": g, "stature": h, "grask": V[g][k], "MF173": mf0[k], "MF_at_stature": mfh, "extrapolated": h > h1 + 0.5,
               "vs_MF173_pct": 100 * (V[g][k] / mf0[k] - 1), "vs_MF_at_stature_pct": 100 * (V[g][k] / mfh - 1)}
        if sk and sk in V: row.update({"SK_matched": V[sk][k], "vs_SK_matched_pct": 100 * (V[g][k] / V[sk][k] - 1)})
        out.append(row)
json.dump(out, open(sys.argv[2], "w"), indent=1)
for r in out: print("%-40s %-6s %.4f | MF173 %.4f (%+.1f%%) | MF@H %.4f (%+.1f%%)%s%s" % (r["row"][:40], r["body"], r["grask"], r["MF173"], r["vs_MF173_pct"], r["MF_at_stature"], r["vs_MF_at_stature_pct"], " extrap" if r["extrapolated"] else "", (" | SK %.4f (%+.1f%%)" % (r["SK_matched"], r["vs_SK_matched_pct"])) if "SK_matched" in r else ""))
