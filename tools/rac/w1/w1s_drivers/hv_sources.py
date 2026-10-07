# RAC W1s (Halvren W1): source-relationship diagnostics for a Halvren body against the six accepted source populations used directly
# (MF-M-R, SK, SG, FN = FNL4, AE = AEL1, VA = VAL4; no averaged Human or Elf parent is built). Report-level evidence for HV order items
# 3-8: expression recipe by domain (nearest source per reading), source-span coherence, source duplication, and arithmetic-averaging
# tests. Joint readings: joint breadth / stature with the stature-scaled slab (Cogling ruling), from jbw.py output.
# Usage: python3 hv_sources.py HV_meas.json JBW.json JBKEY TAG  -> reviews/rac-w1s-hv-evidence/sources_<TAG>.json
import sys, os, json, itertools
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
EV = os.environ.get('EVDIR', '/home/claude/wayfarer-design/reviews/rac-w1s-hv-evidence'); os.makedirs(EV, exist_ok=True)
HVM, JBF, JBK, TAG = sys.argv[1:5]
SRC = {"MF": S + '/w1g/cand/MF-M-R_meas.json', "SK": S + '/w1g/cand/SK_meas.json', "SG": S + '/w1g/cand/SG_meas.json',
       "FN": S + '/w1p/cand/FNL4_meas.json', "AE": S + '/w1m/legs/AEL1_meas.json', "VA": S + '/w1n/cand/VAL4_meas.json'}
JKEY = {"MF": "MF-M-R", "SK": "SK", "SG": "SG", "FN": "FN", "AE": "AE", "VA": "VA"}
HUMAN, ELF = ("MF", "SK", "SG"), ("FN", "AE", "VA")
L = lambda p: json.load(open(p))["combined"]
M = {k: L(p) for k, p in SRC.items()}; M["HV"] = L(HVM)
JB = json.load(open(JBF)); JSRC = json.load(open(os.environ.get('JBSRC', S + '/w1s/jbw_src.json')))
def jb(i, j): return (JB[JBK] if i == "HV" else JSRC[JKEY[i]])["scaled"][j]
R = lambda k: (lambda i: M[i]["ratio"][k]); C = lambda k: (lambda i: M[i]["cranio"][k])
DOM = {
 "axial skeleton": [("torso / stature", R("torso_share")), ("neck / stature", R("neck_share")), ("thoracic breadth / stature", R("thorax_breadth_share")),
                    ("thoracic depth / stature", R("thorax_depth_share")), ("thoracic depth / breadth", R("thorax_d_over_b")), ("waist interval / torso", R("waist_interval_over_torso")),
                    ("shoulder breadth / stature", R("shoulder_breadth_share"))],
 "appendicular skeleton": [("arm / stature", R("arm_share")), ("leg / stature", R("leg_share")), ("upper arm / arm", R("upperarm_over_arm")), ("forearm / arm", R("forearm_over_arm")),
                    ("femur / leg", R("femur_over_leg")), ("lower leg / leg", R("shin_over_leg")), ("crest / thoracic breadth", R("pelvis_over_thorax_breadth")),
                    ("pelvic depth / thoracic depth", R("pelvic_depth_over_thorax_depth")), ("pelvic vertical / thoracic vertical", R("pelvic_vertical_over_thoracic_vertical")),
                    ("bitrochanteric / crest", R("bitroch_over_crest"))] + [("%s breadth / stature (scaled slab)" % j, (lambda j: lambda i: jb(i, j))(j)) for j in ("elbow", "wrist", "knee", "ankle")],
 "distal anatomy": [("hand / stature", R("hand_share")), ("finger / palm", R("finger_over_palm")), ("palm breadth / hand", R("palm_breadth_over_hand")),
                    ("foot / stature", R("foot_share")), ("foot breadth / foot length", lambda i: M[i]["mean"]["foot_breadth"] / M[i]["mean"]["foot_len"])],
 "craniofacial": [("head height / stature", R("HH_share")), ("face vertical index FVI", C("FVI")), ("face vertical / bizygomatic FVB", C("FVB")), ("facial projection FPI", C("FPI")),
                    ("midface projection MPI", C("MPI")), ("cranial base height CBH", C("CBH")), ("midface vertical MVI", C("MVI")), ("orbit breadth / head length", C("ORB_breadth_over_HL")),
                    ("orbit height / head height", C("ORB_height_over_HH")), ("eye diameter / head height", lambda i: M[i]["cranio"]["eye_diam_cm"] / M[i]["cranio"]["HH"])]}
ids = ["HV"] + list(SRC)
rows = []
for dom, items in DOM.items():
    for name, f in items:
        v = {i: float(f(i)) for i in ids}; hv = v["HV"]
        pct = {s: 100 * (hv / v[s] - 1) for s in SRC}
        near = min(SRC, key=lambda s: abs(pct[s])); lo, hi = min(v[s] for s in SRC), max(v[s] for s in SRC)
        mids = {"%s+%s" % (h, e): (v[h] + v[e]) / 2 for h in HUMAN for e in ELF}
        mid_pct = {k: 100 * (hv / m - 1) for k, m in mids.items()}
        rows.append({"domain": dom, "reading": name, "values": v, "pct_HV_vs": pct, "nearest_source": near, "nearest_family": "human" if near in HUMAN else "elven",
                     "source_span": [lo, hi], "in_span": lo <= hv <= hi, "beyond_span_pct": 0.0 if lo <= hv <= hi else 100 * ((hv - hi) / hi if hv > hi else (hv - lo) / lo),
                     "within_1pct_of": [s for s in SRC if abs(pct[s]) < 1.0], "midpoint_pct": mid_pct, "nearest_midpoint": min(mid_pct, key=lambda k: abs(mid_pct[k]))})
summ = {"by_source": {}, "by_domain": {}, "averaging": {}}
for s in SRC:
    d = [abs(r["pct_HV_vs"][s]) for r in rows]
    summ["by_source"][s] = {"within_1pct": sum(x < 1 for x in d), "n": len(d), "median_abs_pct": sorted(d)[len(d) // 2],
                            "by_domain_within_1pct": {dom: "%d/%d" % (sum(abs(r["pct_HV_vs"][s]) < 1 for r in rows if r["domain"] == dom), sum(r["domain"] == dom for r in rows)) for dom in DOM}}
for dom in DOM:
    rr = [r for r in rows if r["domain"] == dom]
    summ["by_domain"][dom] = {"nearest_counts": {s: sum(r["nearest_source"] == s for r in rr) for s in SRC}, "human_nearest": sum(r["nearest_family"] == "human" for r in rr),
                              "elven_nearest": sum(r["nearest_family"] == "elven" for r in rr), "n": len(rr), "out_of_span": [r["reading"] for r in rr if not r["in_span"]]}
for k in rows[0]["midpoint_pct"]:
    d = [abs(r["midpoint_pct"][k]) for r in rows]
    summ["averaging"][k] = {"within_0p5pct": sum(x < 0.5 for x in d), "within_1pct": sum(x < 1 for x in d), "n": len(d), "median_abs_pct": sorted(d)[len(d) // 2]}
out = {"hv_meas": HVM, "jbw": [JBF, JBK], "rows": rows, "summary": summ,
       "note": "Report-level diagnostics. No duplication or averaging threshold is authored canon; counts are shown for the author's call. Joint rows use the stature-scaled slab."}
json.dump(out, open(EV + '/sources_%s.json' % TAG, 'w'), indent=1)
print(TAG, 'stature %.2f' % M["HV"]["stature"])
for s, v in summ["by_source"].items(): print('  vs %-3s within1%% %2d/%d  median|d| %.1f%%  %s' % (s, v["within_1pct"], v["n"], v["median_abs_pct"], v["by_domain_within_1pct"]))
for dom, v in summ["by_domain"].items(): print('  %-22s human-nearest %d elven-nearest %d  %s  out-of-span %s' % (dom, v["human_nearest"], v["elven_nearest"], {k: c for k, c in v["nearest_counts"].items() if c}, v["out_of_span"]))
best = sorted(summ["averaging"].items(), key=lambda kv: kv[1]["median_abs_pct"])[:3]
print('  closest midpoints:', [(k, v["within_0p5pct"], v["within_1pct"], round(v["median_abs_pct"], 2)) for k, v in best])
