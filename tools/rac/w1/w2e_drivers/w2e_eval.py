# RAC W2E (Sagekin W2) evaluation. NON-CANON diagnostics throughout.
# Values: skin layer (run_candidate 'combined' ratios), skeletal proxy (CIB grid, exact-plane S7, t = 0 / 0.5 / 1.0), joints (EXACT-PLANE SECTION,
# w2c1_drivers/joint_section.py; per stature and per adjacent segment, RAC-05 L32).
# G rows: the accepted Sagekin W1 directional rows (directional_checks.py, the body in the SG slot, Marchfolk 173 fixed reference). At statures
# other than the reference these are fixed-reference rows (boundary-stature rule: stature-matched rows in code O govern).
# Comparison rows come from the spec (w2e_spec.py). Classes: AD-G10.   Usage: python3 w2e_eval.py REGISTRY.json SPEC.json OUT.json JOINTS.json ...
import sys, os, json, shutil
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; R = '/home/claude/wayfarer-design'
sys.path.insert(0, R + '/tools/rac/w1')
REG = json.load(open(sys.argv[1])); SPEC = json.load(open(sys.argv[2])); OUT = sys.argv[3]
JS = {}
for f in sys.argv[4:]: JS.update(json.load(open(f)))
SKIN = ["torso_share", "leg_share", "arm_share", "span_der", "upperarm_over_arm", "forearm_over_arm", "femur_over_leg", "shin_over_leg", "neck_share", "HH_share",
        "hand_share", "finger_over_hand", "palm_breadth_over_hand", "foot_share", "thorax_breadth_share", "thorax_depth_share", "shoulder_joint_share"]     # joints: exact-plane sections only (slab ratios are historical)
SKEL = [("thoracic breadth / stature", "thorax_breadth_share"), ("thoracic depth / stature", "thorax_depth_share"), ("thoracic depth / breadth", "thorax_d_over_b"),
        ("shoulder-joint breadth / stature", "shoulder_joint_share"), ("biacromial / stature", "biacromial_share"), ("crest breadth / stature", "crest_share"),
        ("AP pelvic depth / stature", "pelvic_depth_share"), ("pelvic vertical / stature", "pelvic_vertical_share"), ("hip-joint spacing / stature", "hip_joint_breadth_share"),
        ("bitrochanteric / crest", "bitroch_over_crest"), ("crest / thoracic breadth", "pelvis_over_thorax_breadth"), ("pelvic AP / thoracic depth", "pelvic_depth_over_thorax_depth"),
        ("waist interval / torso", "waist_interval_over_torso"), ("pelvic vertical / thoracic vertical", "pelvic_vertical_over_thoracic_vertical"), ("ribcage vertical / breadth", "ribcage_vertical_over_S2_b"),
        ("femoral shaft breadth / femur", "shaft_b_over_femur")]
J = ("elbow", "wrist", "knee", "ankle")
def cls(op, va, vb):
    if op == "~": return "PASS" if abs(va - vb) <= 0.010 else "FAIL"
    rel = abs(va - vb) / abs(vb) if vb else 1.0; holds = {">": va > vb, "<": va < vb, ">=": va >= vb, "<=": va <= vb}[op]
    if op in (">", "<"): return ("PASS" if rel >= 0.01 else "NOT DEMONSTRATED") if holds else "FAIL"
    return "PASS" if holds else ("MARGINAL" if rel < 0.01 else "FAIL")
V = {}
for b, e in REG.items():
    if not os.path.exists(e["meas"] + '_meas.json'): print("missing", b); continue
    m = json.load(open(e["meas"] + '_meas.json'))["combined"]; r = m["ratio"]; v = {"stature (cm)": m["stature"]}
    for k in SKIN: v[k] = r.get(k)
    if e.get("skp") and os.path.exists('%s/t0.0/%s_meas.json' % (e["skp"], e["skp_id"])):
        for t in ("0.0", "0.5", "1.0"):
            q = json.load(open('%s/t%s/%s_meas.json' % (e["skp"], t, e["skp_id"])))["combined"]; qr = q["ratio"]; st = q["stature"]; b7, d7 = q["alpc_stations"]["S7"]
            for nm, k in SKEL: v["skeletal %s [t=%s]" % (nm, t)] = qr.get(k)
            v["femoral S7 breadth / stature [t=%s]" % t] = b7 / st; v["femoral S7 depth / stature [t=%s]" % t] = d7 / st
    jk = e.get("joint")
    if jk and jk in JS:
        for j in J: v["%s breadth / stature (exact-plane section)" % j] = JS[jk]["section"][j]
        seg = {"elbow": (r.get("upperarm_over_arm"), r.get("arm_share")), "wrist": (r.get("forearm_over_arm"), r.get("arm_share")),
               "knee": (r.get("femur_over_leg"), r.get("leg_share")), "ankle": (r.get("shin_over_leg"), r.get("leg_share"))}
        for j, (a_, b_) in seg.items():
            if a_ and b_: v["%s breadth / adjacent segment (exact-plane section)" % j] = JS[jk]["section"][j] / (a_ * b_)
    V[b] = v
C = []
def add(code, chk, a, op, b, k, note="", report=False, va=None, vb=None):
    va = V.get(a, {}).get(k) if va is None else va; vb = V.get(b, {}).get(k) if vb is None else vb
    if va is None or vb is None: C.append({"code": code, "check": chk, "a": a, "b": b, "reading": k, "va": None, "op": op, "vb": None, "result": "NOT RUN", "note": "reading unavailable"}); return
    C.append({"code": code, "check": chk + (" — REPORT ONLY" if report else ""), "a": a, "b": b, "reading": k, "va": va, "op": op, "vb": vb,
              "margin_pct": 100 * (va / vb - 1), "result": "REPORT" if report else cls(op, va, vb), "note": note})
def tsweep(code, chk, a, op, b, k, note="", report=False):
    ks = [k.replace("[t=0.0]", "[t=%s]" % t) for t in ("0.0", "0.5", "1.0")]
    if not all(V.get(a, {}).get(x) is not None and V.get(b, {}).get(x) is not None for x in ks): add(code, chk, a, op, b, k, note, report); return
    res = [cls(op, V[a][x], V[b][x]) for x in ks]; out = res[0] if len(set(res)) == 1 else "T-SENSITIVE"
    C.append({"code": code, "check": chk + (" — REPORT ONLY" if report else ""), "a": a, "b": b, "reading": k.replace(" [t=0.0]", " [t=0 / 0.5 / 1]"), "va": [V[a][x] for x in ks], "op": op,
              "vb": [V[b][x] for x in ks], "margin_pct": 100 * (V[a][ks[1]] / V[b][ks[1]] - 1), "result": "REPORT" if report else out, "note": note + ("; by t: " + "/".join(res) if len(set(res)) > 1 else "")})
# continuity over the stature family (route seam: 152 native / >= 163 macro)
SER = SPEC.get("series", [])
if all(x in V for x in SER):
    for k in V[SER[2]]:
        if k.startswith("stature") or "[t=0.5]" in k or "[t=1.0]" in k: continue
        vals = [V[x].get(k) for x in SER]
        if any(v is None for v in vals): continue
        rev = [100 * (vals[i + 1] / vals[i] - 1) for i in range(len(vals) - 1)]; up = sum(r > 0 for r in rev); dn = sum(r < 0 for r in rev)
        bad = [i for i, r in enumerate(rev) if up and dn and ((r > 0) != (up >= dn)) and abs(r) >= 1.0]
        C.append({"code": "C", "check": "continuity %s: %s" % (" -> ".join(x.replace("SG", "").replace("-NAT", "") for x in SER), k), "a": SER[0], "b": SER[-1], "reading": k, "va": vals, "op": "trend", "vb": None,
                  "result": "PASS" if not bad else "NON-MONOTONIC (>= 1 % reversal)", "note": " / ".join("%+.1f" % r for r in rev) + " % per step" + ("; reversal at step(s) %s" % ", ".join("%s->%s" % (SER[i], SER[i + 1]) for i in bad) if bad else "")})
# G. accepted Sagekin W1 directional rows (fixed Marchfolk 173 reference) on every Sagekin body
CANON = {}
import directional_checks as DC
CAND = S + '/w1g/cand'     # accepted W1 comparator measurement set (as w2d_drivers/go_search.py)
for b, e in REG.items():
    if not e.get("sagekin") or b not in V or not CAND: continue
    tmp = S + '/w2e/cand_' + b
    if os.path.exists(tmp): shutil.rmtree(tmp)
    shutil.copytree(CAND, tmp); shutil.copy(e["meas"] + '_meas.json', tmp + '/SG_meas.json')
    rows = []
    for x in DC.run(tmp):
        if x.get("cand") != "SG": continue
        va, vb, op = x.get("va"), x.get("vb"), x.get("op")
        res = cls({"≥": ">=", "≤": "<="}.get(op, op), va, vb) if op in (">", "<") and va is not None and vb else ("PASS" if x.get("pass") else "FAIL")
        rows.append({"check": x["check"], "op": op, "va": va, "vb": vb, "result": res})
    CANON[b] = rows; bad = [x for x in rows if x["result"] != "PASS"]
    C.append({"code": "G", "check": "%s: accepted Sagekin W1 directional rows vs Marchfolk 173 (fixed reference)" % b, "a": b, "b": "MF-M-R", "reading": "rows", "va": len(rows) - len(bad), "op": "of", "vb": len(rows),
              "result": "PASS" if not bad else "NOT ALL PASS", "note": "; ".join("%s %s (%.4f vs %.4f)" % (x["result"], x["check"], x["va"], x["vb"]) for x in bad)})
for row in SPEC.get("rows", []):
    if row.get("gate"):     # provisional anti-elf rows: scored only where the W1 elf is beyond matched-height Marchfolk by >= 1 % on that reading
        elf, mf = row["gate"]; ve, vm = V.get(elf, {}).get(row["k"]), V.get(mf, {}).get(row["k"])
        beyond = ve is not None and vm is not None and ((ve > vm * 1.01) if row["op"] == "<" else (ve < vm * 0.99))
        if not beyond: row = dict(row, report=True, note=row.get("note", "") + "; W1 elf not beyond matched Marchfolk (%s) by 1 %% on this reading" % mf)
    (tsweep if "[t=0.0]" in row["k"] else add)(row["code"], row["check"], row["a"], row["op"], row["b"], row["k"], row.get("note", ""), row.get("report", False))
for row in SPEC.get("invariance", []):
    a, b = row["a"], row["b"]
    if a not in V or b not in V: continue
    moved = [k for k in row["keys"] if V[a].get(k) and V[b].get(k) and abs(V[a][k] / V[b][k] - 1) >= row.get("tol", 0.01)]
    C.append({"code": row["code"], "check": row["check"], "a": a, "b": b, "reading": "shares", "va": len(moved), "op": "=", "vb": 0,
              "result": "PASS" if not moved else ("REPORT" if row.get("report") else "FAIL"), "note": "; ".join("%s %+.2f %%" % (k, 100 * (V[a][k] / V[b][k] - 1)) for k in moved) or "none"})
for row in SPEC.get("moves", []):
    a, b, k = row["a"], row["b"], row["k"]
    if V.get(a, {}).get(k) is None or V.get(b, {}).get(k) is None: continue
    d = V[a][k] / V[b][k] - 1
    if row["kind"] == "D": res = "PASS" if row["sign"] * d >= 0.01 else "NOT DEMONSTRATED"
    else: res = "PASS" if abs(d) < row["tol"] else ("REPORT" if row.get("report") else "FAIL")
    C.append({"code": row["code"], "check": row["check"], "a": a, "b": b, "reading": k, "va": V[a][k], "op": row["kind"], "vb": V[b][k], "margin_pct": 100 * d, "result": res, "note": "%+.2f %%" % (100 * d)})
json.dump({"values": V, "checks": C, "canonical_rows": CANON}, open(OUT, 'w'), indent=1, default=float)
import collections
print(len(C), "checks", collections.Counter((c["code"], c["result"] if c["result"] in ("PASS", "REPORT") else c["result"][:16]) for c in C))
for c in C:
    if c["result"] not in ("PASS", "REPORT"): print(" ", c["code"], c["check"][:120], "|", str(c.get("note", ""))[:220], c["result"])
