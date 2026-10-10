# RAC W3A1 source-passing closure (AD-W3A-4 hidden complete-body validity rule; RM-OT-03 closure). NON-CANON diagnostics.
# RULE (author ruling AD-W3A-4): a generated Halvren is INVALID if, after neutralization and legitimate matched-source comparison, the complete-body
# source-passing protocol classifies it as a near-duplicate of a valid source population. The criterion is the resulting anatomy, never a hidden coordinate.
# Protocol: the 24 body-only readings (W2G BODY: 13 skin + 4 exact-plane joints + 7 skeletal-proxy t = 0); separated = |a / b - 1| >= 1 %;
# NEAR-DUPLICATE < 2 separated; AMBIGUOUS 2-3; DISTINCT >= 4 (W3A classes). Matched source = linear interpolation inside the source family's valid range
# over real accepted / W3A / W3A1 source bodies (skeletal readings interpolated over the bodies that carry a grid); outside it the nearest valid adult
# (ENDPOINT, labelled, never a rejection basis). Where a body or source has no skeletal grid, the 17 non-skeletal readings are used and labelled (CONSERVATIVE:
# fewer readings can only separate less).
# Parts: (C) W3A lower-tail samples re-evaluated; (D) focused central native-range confirmation; (U) coupled upper-tail samples vs their W3A uncoupled twins.
# Usage: python3 w3a1_rs.py W3A1_VALUES.json W3A_RS.json OUT.json
import sys, json, numpy as np
V = json.load(open(sys.argv[1]))["values"]; RS0 = json.load(open(sys.argv[2])); OUT = sys.argv[3]
JP = lambda j: "%s breadth / adjacent segment (exact-plane section)" % j
K17 = ["torso_share", "leg_share", "arm_share", "span_der", "forearm_over_arm", "shin_over_leg", "neck_share", "hand_share", "finger_over_hand", "palm_breadth_over_hand",
       "foot_share", "thorax_breadth_share", "thorax_depth_share", JP("elbow"), JP("wrist"), JP("knee"), JP("ankle")]
SK7 = ["skeletal %s [t=0.0]" % x for x in ("thoracic breadth / stature", "thoracic depth / stature", "shoulder-joint breadth / stature", "crest breadth / stature",
       "AP pelvic depth / stature", "pelvic vertical / stature", "waist interval / torso")]
FAM = {"MF": (147.0, 203.0, ["MF147", "MF147p2", "MF147p5", "MF148", "MF149", "MF150", "MF152", "MF157", "MF163", "MF173", "MF178", "MF181", "MF190", "MF203"]),
       "SK": (183.0, 229.0, ["SK183", "SK190", "SK203", "SK208", "SK215", "SK217", "SK219", "SK220p8", "SK221", "SK223", "SK225", "SK227", "SK228p8", "SK229"]),
       "AE": (168.0, 221.0, ["AE168", "AE173", "AE178", "AE181", "AE190", "AE203", "AE211", "AE215", "AE217", "AE219", "AE220p8", "AE221"]),
       "FN": (157.0, 211.0, ["FN157", "FN163", "FN173", "FN178", "FN181", "FN190", "FN203", "FN211"]),
       "VA": (157.0, 203.0, ["VA157", "VA163", "VA173", "VA178", "VA181", "VA190", "VA203"]),
       "SG": (152.0, 208.0, ["SG152", "SG163", "SG173", "SG178", "SG181", "SG190", "SG203", "SG208"])}
def st(b): return V[b]["stature (cm)"]
def has_sk(b): return all(V[b].get(k) is not None for k in SK7)
def interp(s, h, keys):
    lo, hi, names = FAM[s]; hc = min(max(h, lo), hi); out = {}
    for k in keys:
        P = sorted((st(b), V[b][k]) for b in names if b in V and V[b].get(k) is not None)
        if len(P) < 2 or not (P[0][0] - 0.05 <= hc <= P[-1][0] + 0.05): return None, None
        out[k] = float(np.interp(hc, [p[0] for p in P], [p[1] for p in P]))
    return out, lo - 1e-6 <= h <= hi + 1e-6
def compare(b, s):
    keys = K17 + (SK7 if has_sk(b) else []); m, matched = interp(s, st(b), keys)
    if m is None and keys != K17: keys = K17; m, matched = interp(s, st(b), keys)
    if m is None: return {"n_readings": 0, "nsep": None, "class": "NOT RUN", "comparison": "source family unavailable", "separating": []}
    sep = [k for k in keys if abs(V[b][k] / m[k] - 1) >= 0.01]; n = len(sep)
    return {"n_readings": len(keys), "nsep": n, "class": "NEAR-DUPLICATE" if n < 2 else "AMBIGUOUS" if n < 4 else "DISTINCT", "comparison": "matched height" if matched else "ENDPOINT (nearest valid adult)",
            "separating": [k.replace(" [t=0.0]", "") for k in sep]}
def assess(b, sup):
    per = {s: compare(b, s) for s in FAM}; dup = [s for s, p in per.items() if p["class"] == "NEAR-DUPLICATE" and p["comparison"] == "matched height"]
    amb = [s for s, p in per.items() if p["class"] == "AMBIGUOUS" and p["comparison"] == "matched height"]
    return {"id": b, "h": st(b), "per_source": per, "invalid_duplicate": dup, "ambiguous_with": amb, "valid": not dup, "readings_24": has_sk(b)}
R = {"rule": "AD-W3A-4 complete-body validity rule (anatomy result; no coordinate threshold)", "lower": [], "central": [], "upper": []}
# (C) lower tail: every W3A L-MF sample (68). The gridded ones (W3A near-duplicates + ambiguous) get the 24-reading protocol.
for x in RS0["samples"]:
    if x["stratum"] != "L-MF" or x["id"] not in V: continue
    a = assess(x["id"], "MF"); a.update(e_MF=x["e"].get("MF", 0.0), w3a_class=("NEAR-DUPLICATE" if x["dup_matched"] else "AMBIGUOUS" if x["ambiguous"] else "DISTINCT"),
                                   w3a_nsep_MF=x["per_source"]["MF"]["nsep"]); R["lower"].append(a)
# (D) central native-range confirmation
for h in ("152", "157", "163"):
    for xx in (60, 80, 90, 100):
        b = "HC%sM%02d" % (h, xx)
        if b in V: a = assess(b, "MF"); a.update(e_MF=xx / 100); R["central"].append(a)
# (U) coupled upper samples vs their uncoupled W3A twins (17 readings: no grids for these samples)
for b in sorted(V):
    if b.startswith("RU") and b.endswith("c"):
        a = assess(b, None); tw = next(x for x in RS0["samples"] if x["id"] == b[:-1]); a.update(twin=b[:-1], stratum=tw["stratum"], e=tw["e"],
            twin_nsep={s: tw["per_source"][s]["nsep"] for s in tw["per_source"]}); R["upper"].append(a)
def summ(L):
    return {"n": len(L), "invalid_duplicate": sum(1 for a in L if a["invalid_duplicate"]), "valid": sum(1 for a in L if a["valid"]),
            "valid_ambiguous": sum(1 for a in L if a["valid"] and a["ambiguous_with"]), "valid_distinct": sum(1 for a in L if a["valid"] and not a["ambiguous_with"]),
            "with_24_readings": sum(1 for a in L if a["readings_24"])}
R["summary"] = {k: summ(R[k]) for k in ("lower", "central", "upper")}
L = R["lower"]; R["summary"]["lower_transition"] = {"w3a_dup_now_invalid": sum(1 for a in L if a["w3a_class"] == "NEAR-DUPLICATE" and a["invalid_duplicate"]),
    "w3a_dup_now_valid": [a["id"] for a in L if a["w3a_class"] == "NEAR-DUPLICATE" and a["valid"]],
    "w3a_amb_now_invalid": [a["id"] for a in L if a["w3a_class"] == "AMBIGUOUS" and a["invalid_duplicate"]],
    "w3a_distinct_now_invalid": [a["id"] for a in L if a["w3a_class"] == "DISTINCT" and a["invalid_duplicate"]]}
json.dump(R, open(OUT, "w"), indent=1)
for k, v in R["summary"].items(): print(k, v)
