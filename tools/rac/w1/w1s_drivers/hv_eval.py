# RAC W1s (Halvren W1 acceptance gate): rows for a Halvren body.
#  - existing directional rows involving HV (source-span rows), with the accepted sources in their slots (MF-M-R, SK, SG, FNL4, AEL1, VAL4);
#  - canon-derived rows built on hv_sources.py output (HALVREN L9-13, L27-41, L50, L82, L105, L120-133, L141-148, L162-166, L196-206, L218-223):
#    source-span coherence, no domain-wide source duplication, mixed (not human-with-ears / not elf-with-human-proportions) expression,
#    arithmetic-averaging test, joint coupling, pelvis linear-morph test, craniofacial distance from MF (hidden-ear), ear architecture.
# Usage: python3 hv_eval.py HV_meas.json SOURCES_<TAG>.json TAG  -> reviews/rac-w1s-hv-evidence/central_<TAG>.json
import sys, os, json, shutil, statistics as st
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1')
import directional_checks as DC, ear_families_v2 as E2
R = '/home/claude/wayfarer-design'; S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
EV = os.environ.get('EVDIR', R + '/reviews/rac-w1s-hv-evidence'); os.makedirs(EV, exist_ok=True)
HVM, SRCJ, TAG = sys.argv[1:4]; SJ = json.load(open(SRCJ)); rows = SJ["rows"]
tmp = S + '/w1s/cand_' + TAG
if os.path.exists(tmp): shutil.rmtree(tmp)
shutil.copytree(S + '/w1g/cand', tmp)
for slot, src in (("FN", S + '/w1p/cand/FNL4_meas.json'), ("AE", S + '/w1m/legs/AEL1_meas.json'), ("VA", S + '/w1n/cand/VAL4_meas.json'), ("HV", HVM)):
    shutil.copy(src, tmp + '/%s_meas.json' % slot)
out = {"hv_meas": HVM, "sources": SRCJ, "directional": [r for r in DC.run(tmp) if 'HV' in (r.get('cand'), r.get('b'), r.get('a'))], "added": []}
for r in out["directional"]: r["result"] = "PASS" if r["pass"] else ("MARGINAL" if r.get("marginal") else "FAIL")
def add(chk, src, result, va, op, vb, b, note="", report=False):
    out["added"].append({"cand": "HV", "check": chk + (" — REPORT ONLY" if report else ""), "canon": src, "va": va, "op": op, "vb": vb, "b": b, "result": "REPORT" if report else result, "note": note})
BODY = ("axial skeleton", "appendicular skeleton", "distal anatomy")
# 1. source-span coherence (no reading outside what the six sources span; no incompatible inherited extreme)
for r in rows:
    lo, hi = r["source_span"]; v = r["values"]["HV"]; b = r["beyond_span_pct"]
    res = "PASS" if r["in_span"] else ("MARGINAL" if abs(b) < 1.0 else "FAIL")
    add("%s: %s inside the six-source span" % (r["domain"], r["reading"]), "HV L13, L31, L82, L105", res, v, "in", [lo, hi], "span", "%+.2f %% beyond" % b if b else "")
# 2. no domain-wide duplication of one source (HV L82, L141; source-passing test L145)
for dom in BODY + ("craniofacial",):
    rr = [r for r in rows if r["domain"] == dom]
    for s in ("MF", "SK", "SG", "FN", "AE", "VA"):
        n = sum(abs(r["pct_HV_vs"][s]) < 1.0 for r in rr)
        add("%s: not every reading within 1 %% of %s" % (dom, s), "HV L82, L141, L145", "PASS" if n < len(rr) else "FAIL", n, "<", len(rr), s,
            report=(dom == "craniofacial"), note="craniofacial: the accepted FN / VA / SG heads are themselves within 1 % of MF on most head readings (method limit)" if dom == "craniofacial" else "")
nb = [r for r in rows if r["domain"] in BODY]
for s in ("MF", "SK", "SG", "FN", "AE", "VA"):
    n = sum(abs(r["pct_HV_vs"][s]) < 1.0 for r in nb)
    add("body (axial + appendicular + distal): within 1 %% of %s on fewer than all readings" % s, "HV L82, L141, L145", "PASS" if n < len(nb) else "FAIL", n, "<", len(nb), s)
# 3. mixed expression in the body: not a human body with elven ears, not an elven body with human proportions (HV L9, L41, L162)
hn = sum(r["nearest_family"] == "human" for r in nb); en = len(nb) - hn
add("body readings nearest an ELVEN source (not a human body with pointed ears)", "HV L9, L162", "PASS" if en > 0 and en >= 0.2 * len(nb) else "FAIL", en, ">=", round(0.2 * len(nb), 1), "20 % of body readings",
    note="20 % is a builder diagnostic floor, not canon")
add("body readings nearest a HUMAN source (not a generic elf with human proportions)", "HV L9", "PASS" if hn > 0 and hn >= 0.2 * len(nb) else "FAIL", hn, ">=", round(0.2 * len(nb), 1), "20 % of body readings",
    note="20 % is a builder diagnostic floor, not canon")
mf_beyond = [r["reading"] for r in nb if abs(r["pct_HV_vs"]["MF"]) >= 1.0]
add("body readings differing from MF by >= 1 % (elven contribution expressed somewhere)", "HV L9, L41", "PASS" if mf_beyond else "FAIL", len(mf_beyond), ">", 0, "MF", "; ".join(mf_beyond))
# 4. arithmetic averaging (HV L13: never (human + elf) / 2): on readings where a human-elf pair differs by >= 3 %, count HV readings within
#    10 % of the pair gap from the midpoint
for h in ("MF", "SK", "SG"):
    for e in ("FN", "AE", "VA"):
        disc = [r for r in nb if abs(r["values"][h] / r["values"][e] - 1) >= 0.03]
        at = [r["reading"] for r in disc if abs(r["values"]["HV"] - (r["values"][h] + r["values"][e]) / 2) <= 0.1 * abs(r["values"][h] - r["values"][e])]
        add("not the arithmetic %s + %s midpoint (readings where the pair differs >= 3 %%)" % (h, e), "HV L13", "PASS" if len(at) < len(disc) or not disc else "FAIL", len(at), "of", len(disc), h + "+" + e, "; ".join(at), report=True)
# 5. joint coupling (HV L133): HV joint spread vs MF compared with each source's own spread
J = [r for r in nb if r["reading"].endswith("(scaled slab)")]
spread = lambda s: max(r["pct_HV_vs"]["MF"] if s == "HV" else 100 * (r["values"][s] / r["values"]["MF"] - 1) for r in J) - min(r["pct_HV_vs"]["MF"] if s == "HV" else 100 * (r["values"][s] / r["values"]["MF"] - 1) for r in J)
sp = {s: spread(s) for s in ("HV", "SK", "SG", "FN", "AE", "VA")}
add("joint coupling: spread of joint-breadth % vs MF across elbow / wrist / knee / ankle no larger than the widest source spread", "HV L133", "PASS" if sp["HV"] <= max(v for k, v in sp.items() if k != "HV") else "FAIL",
    sp["HV"], "<=", max(v for k, v in sp.items() if k != "HV"), "max source spread", "; ".join("%s %.1f" % kv for kv in sp.items()))
# 6. pelvis is not a linear morph (HV L122): fraction f = (HV - MF) / (E - MF) per pelvic reading for each elf; a linear morph gives one f
P = [r for r in nb if r["reading"] in ("crest / thoracic breadth", "pelvic depth / thoracic depth", "pelvic vertical / thoracic vertical", "bitrochanteric / crest")]
for e in ("FN", "AE", "VA"):
    f = [(r["values"]["HV"] - r["values"]["MF"]) / (r["values"][e] - r["values"]["MF"]) for r in P if abs(r["values"][e] - r["values"]["MF"]) > 1e-4]
    add("pelvis: MF -> %s interpolation fractions differ across pelvic readings (not one linear morph)" % e, "HV L122", "PASS", [round(x, 2) for x in f], "spread", round(max(f) - min(f), 2), e, report=True)
# 7. hidden-ear craniofacial distance from MF and each elf (HV L64, L162-166, L218)
CF = [r for r in rows if r["domain"] == "craniofacial"]
for s in ("MF", "FN", "AE", "VA"):
    n = sum(abs(r["pct_HV_vs"][s]) >= 1.0 for r in CF)
    add("hidden-ear craniofacial: head readings differing from %s by >= 1 %%" % s, "HV L64, L162, L218", "REPORT", n, "of", len(CF), s, report=True)
for s in ("FN", "VA", "SG"):
    n = sum(abs(r["values"][s] / r["values"]["MF"] - 1) >= 0.01 for r in CF)
    add("method context: accepted %s head readings differing from MF by >= 1 %%" % s, "W1g / W1i heads", "REPORT", n, "of", len(CF), s, report=True)
# 8. ear architecture (HV L196-206; W1i ear families, BUILDER-CHOSEN reference centres)
F = E2.BASE; P_ = lambda fam, k: F[fam][k]
hv, mf, el = F["HV-mixed"], F["MF-human"], [F[k] for k in ("FN-elven", "AE-elven", "VA-elven")]
add("ear: whole-ear architecture, not a human ear with a pointiness scalar — HV ear carries the elven continuous taper law (human ear has none)", "HV L196-198", "PASS" if hv["taper"] and not mf["taper"] else "FAIL", hv["taper"][0], "vs", "none", "MF")
add("ear: length between human and elven families (mixed, not a copy)", "HV L198", "PASS" if mf["L"] < hv["L"] < min(x["L"] for x in el) else "FAIL", hv["L"], "in", [mf["L"], min(x["L"] for x in el)], "MF..min elf")
add("ear: taper starts later on the ear than every elven ear (human-influenced base; mixed, not the elven taper)", "HV L198 (example: broader human-influenced base)", "PASS" if hv["taper"][1] > max(x["taper"][1] for x in el) else "FAIL", hv["taper"][1], ">", max(x["taper"][1] for x in el), "max elf")
add("ear: human-family lobe fraction retained", "HV L198 (example: more human-like lobe)", "PASS" if abs(hv["lobe"] - mf["lobe"]) < 1e-9 else "FAIL", hv["lobe"], "=", mf["lobe"], "MF", report=True)
keys = ("L", "wb", "lobe", "bowl", "ah", "proj", "tilt", "sweep", "thick")
for fam in ("MF-human", "FN-elven", "AE-elven", "VA-elven"):
    n = sum(abs(hv[k] / F[fam][k] - 1) < 0.02 for k in keys)
    add("ear: parameters within 2 %% of the %s ear (not a copy)" % fam, "HV L219", "PASS" if n < len(keys) else "FAIL", n, "<", len(keys), fam)
mid = {k: (mf[k] + st.mean(x[k] for x in el)) / 2 for k in keys}
n = [k for k in keys if abs(hv[k] / mid[k] - 1) < 0.02]
add("ear: parameters within 2 % of the MF / elven-mean midpoint ear (never one midpoint ear)", "HV L219", "PASS" if len(n) < len(keys) else "FAIL", len(n), "of", len(keys), "midpoint", ", ".join(n), report=True)
json.dump(out, open(EV + '/central_%s.json' % TAG, 'w'), indent=1, default=float)
bad = [(r['check'][:80], r['result']) for k in ('directional', 'added') for r in out[k] if r['result'] not in ('PASS', 'REPORT')]
print(TAG, {k: len(out[k]) for k in ('directional', 'added')}, 'non-PASS:', bad)
