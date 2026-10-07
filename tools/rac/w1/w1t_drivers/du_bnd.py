# RAC W1t: Durrim boundary and short-race comparison cases (order items 6-9). All bodies built without uniform scaling: native short-adult
# regional route (native_short.py: per-region length / girth / hand / foot / head factors at the target stature) for DU, PK, CG and, at 152 cm,
# MF and SG (the generator height macro below ~159 cm has an implausible femur and is excluded, native_short_allometry.json). Joint rows use the
# stature-scaled slab. Cases:
#   B152  DURRIM L19, L72, L156: DU152 vs MF152 vs SG152 (permanent equal-height boundary)
#   B122  SR-COMP-03: DU122 vs PK122 (maximum-height Pipkin, minimum-height Durrim)
#   C10A  COG-BODY-10A: CG107 (maximum-height Cogling) beside DU122 (minimum-height Durrim), actual height
#   C10   COG-BODY-10 / SR-COMP-10: Broad high-muscle Cogling (CGJ7 Broad, muscle 1) vs Narrow Durrim (normalized readings)
#   PKB   order item 6: Broad Pipkin (PK-NAT Broad, pelvis x1.12) vs Narrow Durrim
# Usage: python3 du_bnd.py JBW.json  -> reviews/rac-w1t-du-evidence/boundary.json
import sys, os, json
R = '/home/claude/wayfarer-design'; S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; T = S + '/w1t'
JB = json.load(open(sys.argv[1]))
P = {"DU152": T + '/bnd/DU152-NAT', "MF152": T + '/bnd/MF152-NAT', "SG152": T + '/bnd/SG152-NAT', "DU122": T + '/bnd/DU122-NAT', "PK122": T + '/bnd/PK122-NAT',
     "CG107": T + '/bnd/CG107-NAT', "CGBHM": T + '/cgb/CGBHM', "DU-NARROW": T + '/frame_NARROWB/final/DU-NAT', "PK-BROAD": S + '/w1q/frame_BROADB_P112/final/PK-NAT',
     "MF-M-R": S + '/w1f/final/MF-M-R', "SG": S + '/w1f/final/SG', "DU": S + '/w1f/final/DU-NAT', "CHILD9": T + '/child/CHILD9'}
def cls(op, va, vb):
    rel = abs(va - vb) / abs(vb); holds = {">": va > vb, "<": va < vb, ">=": va >= vb, "<=": va <= vb}[op]
    if op in (">", "<"): return ("PASS" if rel >= 0.01 else "NOT DEMONSTRATED") if holds else "FAIL"
    return "PASS" if holds else ("MARGINAL" if rel < 0.01 else "FAIL")
M = {k: json.load(open(p + '_meas.json'))["combined"] for k, p in P.items() if os.path.exists(p + '_meas.json')}
def g(i, k):
    c = M[i]; r = c["ratio"]; m = c["mean"]; s = c["stature"]
    if k.startswith("jb:"): return JB[i]["scaled"][k[3:]]
    return {"palm breadth / stature": m["palm_breadth"] / s, "palm depth / stature": m["palm_depth"] / s, "foot breadth / stature": m["foot_breadth"] / s,
            "hip-joint height / stature": m["hip_height"] / s, "femur / tibia (segment plausibility)": m["thigh"] / m["shin"], "FVB": c["cranio"]["FVB"]}.get(k, r.get(k))
NAME = {"HH_share": "head height / stature", "neck_share": "neck / stature", "torso_share": "torso / stature", "leg_share": "leg / stature", "arm_share": "arm / stature",
        "thorax_breadth_share": "thoracic breadth / stature", "thorax_depth_share": "thoracic depth / stature", "shoulder_joint_share": "shoulder-joint breadth / stature",
        "crest_share": "crest breadth / stature", "hip_joint_breadth_share": "hip-joint spacing / stature", "pelvis_over_thorax_breadth": "crest / thoracic breadth",
        "pelvic_depth_share": "AP pelvic depth / stature", "hand_share": "hand / stature", "upperarm_over_arm": "upper arm / arm", "forearm_over_arm": "forearm / arm",
        "finger_over_palm": "finger / palm", "palm_breadth_over_hand": "palm breadth / hand", "foot_share": "foot / stature", "jb:elbow": "elbow breadth / stature (scaled slab)",
        "jb:wrist": "wrist breadth / stature (scaled slab)", "jb:knee": "knee breadth / stature (scaled slab)", "jb:ankle": "ankle breadth / stature (scaled slab)"}
nm = lambda k: NAME.get(k, k)
out = {"cases": {}, "statures": {k: M[k]["stature"] for k in M}, "plausibility": {k: g(k, "femur / tibia (segment plausibility)") for k in M}}
def case(cid, title, canon, rows, a, b):
    rr = []
    for k, op, rep in rows:
        if a not in M or b not in M: continue
        va, vb = g(a, k), g(b, k)
        rr.append({"check": "%s %s %s" % (a, op, b), "reading": nm(k), "va": va, "op": op, "vb": vb, "a": a, "b": b, "result": "REPORT" if rep else cls(op, va, vb), "pct": 100 * (va / vb - 1)})
    out["cases"].setdefault(cid, {"title": title, "canon": canon, "rows": []})["rows"] += rr
DUDIR = [("HH_share", ">", True), ("neck_share", "<", False), ("torso_share", ">", False), ("leg_share", "<", False), ("arm_share", "<", False), ("thorax_breadth_share", ">", False),
         ("thorax_depth_share", ">", False), ("shoulder_joint_share", ">", False), ("crest_share", ">", False), ("hip_joint_breadth_share", ">", False),
         ("pelvis_over_thorax_breadth", "<=", False), ("pelvic_depth_share", ">", False), ("hand_share", ">", False), ("palm breadth / stature", ">", False),
         ("foot breadth / stature", ">", False), ("jb:elbow", ">", False), ("jb:wrist", ">", False), ("jb:knee", ">", False), ("jb:ankle", ">", False)]
case("B152", "152 cm equal-height boundary: Durrim vs Marchfolk", "DURRIM L19, L72, L156 (permanent)", DUDIR, "DU152", "MF152")
case("B152", "", "", DUDIR, "DU152", "SG152")
SGDIR = [("leg_share", ">", False), ("arm_share", ">", True), ("thorax_breadth_share", "<", False), ("thorax_depth_share", "<", True), ("torso_share", "<", True), ("hand_share", ">", True)]
case("B152SG", "152 cm: Sagekin keeps Sagekin anatomy vs Marchfolk (never Durrim-like)", "DURRIM L156; SAGEKIN linear tendencies (HALVREN L116 / L459-460 normalization)", SGDIR, "SG152", "MF152")
case("B152SG", "", "", [(k, op, True) for k, op, _ in SGDIR], "SG", "MF-M-R")
PKDIR = [("thorax_depth_share", ">", False), ("thorax_breadth_share", ">", False), ("leg_share", "<", False), ("arm_share", "<", False), ("pelvis_over_thorax_breadth", "<", False),
         ("hand_share", ">", False), ("palm breadth / stature", ">", False), ("foot breadth / stature", ">", False), ("neck_share", "<", False),
         ("jb:elbow", ">", False), ("jb:wrist", ">", False), ("jb:knee", ">", False), ("jb:ankle", ">", False)]
case("B122", "~122 cm Pipkin / Durrim boundary", "SR-COMP-03; DURRIM L156", PKDIR, "DU122", "PK122")
CGDIR = [("thorax_depth_share", ">", False), ("thorax_breadth_share", ">", False), ("leg_share", "<", False), ("arm_share", "<", False), ("upperarm_over_arm", ">", False),
         ("forearm_over_arm", "<", False), ("finger_over_palm", "<", False), ("palm_breadth_over_hand", ">", False), ("foot breadth / stature", ">", False), ("neck_share", "<", False),
         ("jb:elbow", ">", False), ("jb:wrist", ">", False), ("jb:knee", ">", False), ("jb:ankle", ">", False)]
case("C10A", "Actual height: maximum-height Cogling (107 cm) beside minimum-height Durrim (122 cm)", "COG-BODY-10A; DURRIM L156", CGDIR, "DU122", "CG107")
case("C10", "Normalized: Broad high-muscle Cogling vs Narrow Durrim", "COG-BODY-10; SR-COMP-10", CGDIR, "DU-NARROW", "CGBHM")
case("PKB", "Broad Pipkin vs Narrow Durrim", "order item 6; SR-COMP-10", PKDIR, "DU-NARROW", "PK-BROAD")
CH = [("HH_share", "<", True), ("FVB", ">", True), ("leg_share", "vs", True), ("pelvis_over_thorax_breadth", "<", True), ("thorax_depth_share", ">", True), ("hand_share", ">", True),
      ("waist_interval_over_torso", "vs", True)]
for k, op, rep in CH:
    if "DU" in M and "CHILD9" in M:
        va, vb = g("DU", k), g("CHILD9", k)
        out["cases"].setdefault("ADULT", {"title": "Adult read: DU (137 cm) vs generator human-child proxy (137 cm, age ~9 y; diagnostic)", "canon": "DURRIM L21, L76", "rows": []})["rows"].append(
            {"check": "DU vs CHILD9", "reading": nm(k), "va": va, "op": op, "vb": vb, "a": "DU", "b": "CHILD9", "result": "REPORT", "pct": 100 * (va / vb - 1)})
json.dump(out, open(R + '/reviews/rac-w1t-du-evidence/boundary.json', 'w'), indent=1, default=float)
print('statures', {k: round(v, 1) for k, v in out["statures"].items()}); print('femur / tibia', {k: round(v, 3) for k, v in out["plausibility"].items()})
for cid, c in out["cases"].items():
    bad = [(r["check"], r["reading"], round(r["pct"], 1), r["result"]) for r in c["rows"] if r["result"] not in ("PASS", "REPORT")]
    print(cid, '%d rows' % sum(r["result"] != "REPORT" for r in c["rows"]), 'non-PASS:', bad)
