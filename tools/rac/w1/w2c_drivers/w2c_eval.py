# RAC W2C (Grask boundary foundation) evaluation. NON-CANON diagnostics throughout.
# Values: skin layer (run_candidate 'combined' ratios), skeletal proxy (CIB, exact-plane S7, t = 0 / 0.5 / 1.0), joints (stature-scaled slab).
# Canonical Grask rows per body: w1k_drivers/gr_eval.evaluate (directional + skin + skeletal rows, accepted comparators; S7-normalized
# skeletal base). Checks: C continuity, U head allometry, K joints vs allometry, G canonical rows, D / L frames, A arm clearance,
# M composition, X named extremes, S matched-height Grask vs Skarn, B Broad span, AD2 / AD3 boundaries, H Marchfolk overlap.
# Usage: python3 w2c_eval.py REGISTRY.json JBW.json OUT.json
import sys, os, json
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; R = '/home/claude/wayfarer-design'
os.environ.setdefault('SKPBASE', S + '/s7n/w1i_base'); os.environ.setdefault('EVDIR', S + '/w2c/ev')
sys.path.insert(0, R + '/tools/rac/w1'); sys.path.insert(0, R + '/tools/rac/w1/w1k_drivers'); sys.path.insert(0, R + '/tools/rac/w1/w1g_drivers')
REG = json.load(open(sys.argv[1])); JB = json.load(open(sys.argv[2])); OUT = sys.argv[3]
AL = json.load(open(R + '/tools/rac/w1/native_short_allometry.json'))["slopes"]
SKIN = ["torso_share", "leg_share", "arm_share", "span_der", "upperarm_over_arm", "forearm_over_arm", "femur_over_leg", "shin_over_leg", "neck_share", "HH_share",
        "hand_share", "foot_share", "finger_over_palm", "thorax_breadth_share", "thorax_depth_share", "shoulder_joint_share", "elbow_over_humerus", "knee_over_femur"]
SKEL = [("thoracic breadth / stature", "thorax_breadth_share"), ("thoracic depth / stature", "thorax_depth_share"), ("shoulder-joint breadth / stature", "shoulder_joint_share"),
        ("biacromial / stature", "biacromial_share"), ("crest breadth / stature", "crest_share"), ("AP pelvic depth / stature", "pelvic_depth_share"),
        ("pelvic vertical / stature", "pelvic_vertical_share"), ("hip-joint spacing / stature", "hip_joint_breadth_share"), ("bitrochanteric / crest", "bitroch_over_crest"),
        ("crest / thoracic breadth", "pelvis_over_thorax_breadth"), ("shoulder-joint / thoracic breadth", "S1_over_S2_b"), ("thoracic depth / breadth", "thorax_d_over_b")]
def cls(op, va, vb):
    rel = abs(va - vb) / abs(vb) if vb else 1.0; holds = {">": va > vb, "<": va < vb, ">=": va >= vb, "<=": va <= vb}[op]
    if op in (">", "<"): return ("PASS" if rel >= 0.01 else "NOT DEMONSTRATED") if holds else "FAIL"
    return "PASS" if holds else ("MARGINAL" if rel < 0.01 else "FAIL")
V = {}
for b, e in REG.items():
    m = json.load(open(e["meas"] + '_meas.json'))["combined"]; r = m["ratio"]; H = m["stature"]
    v = {"stature (cm)": H}
    for k in SKIN: v[k] = r.get(k)
    if e.get("skp"):
        for t in ("0.0", "0.5", "1.0"):
            q = json.load(open('%s/t%s/%s_meas.json' % (e["skp"], t, e["skp_id"])))["combined"]; qr = q["ratio"]; st = q["stature"]; b7, d7 = q["alpc_stations"]["S7"]
            for nm, k in SKEL: v["skeletal %s [t=%s]" % (nm, t)] = qr[k]
            v["femoral S7 breadth / stature [t=%s]" % t] = b7 / st; v["femoral S7 depth / stature [t=%s]" % t] = d7 / st
    jk = e.get("jbw")
    if jk and jk in JB:
        for j in ("elbow", "wrist", "knee", "ankle"): v["%s breadth / stature (scaled slab)" % j] = JB[jk]["scaled"][j]
    V[b] = v
C = []
def add(code, chk, a, op, b, k, note="", report=False, va=None, vb=None):
    va = V[a][k] if va is None else va; vb = V[b][k] if vb is None and b in V else vb
    if va is None or vb is None: return
    C.append({"code": code, "check": chk + (" — REPORT ONLY" if report else ""), "a": a, "b": b, "reading": k, "va": va, "op": op, "vb": vb,
              "margin_pct": 100 * (va / vb - 1), "result": "REPORT" if report else cls(op, va, vb), "note": note})
def adj(val, frm, to, j): return val * (to / frm) ** (AL[j] - 1)
X = json.load(open(os.environ["W2C_SPEC"])) if os.environ.get("W2C_SPEC") else {}
# A. stature foundation: continuity, head allometry, joints vs allometry
lo, ce, hi = "GR198", "GR218", "GR239"
if all(x in V for x in (lo, ce, hi)):
    add("U", "head share allometric: 198 > 218", lo, ">", ce, "HH_share"); add("U", "head share allometric: 239 < 218", hi, "<", ce, "HH_share")
    for k in V[ce]:
        if k.startswith("stature") or V[lo].get(k) is None or V[hi].get(k) is None or V[ce].get(k) is None: continue
        a, b_, d = V[lo][k], V[ce][k], V[hi][k]
        ok = (a <= b_ <= d) or (a >= b_ >= d) or min(abs(a / b_ - 1), abs(d / b_ - 1)) < 0.01
        C.append({"code": "C", "check": "continuity 198 -> 218 -> 239: %s" % k, "a": lo, "b": hi, "reading": k, "va": [a, b_, d], "op": "trend", "vb": None,
                  "result": "PASS" if ok else "NON-MONOTONIC (>= 1 % reversal)", "note": "%+.1f %% / %+.1f %% vs 218" % (100 * (a / b_ - 1), 100 * (d / b_ - 1))})
    for x in (lo, "GR208", "GR229", hi):
        for j in ("elbow", "wrist", "knee", "ankle"):
            k = "%s breadth / stature (scaled slab)" % j
            if x in V and k in V[x] and k in V[ce]:
                e = adj(V[ce][k], V[ce]["stature (cm)"], V[x]["stature (cm)"], j); d = V[x][k] / e - 1
                C.append({"code": "K", "check": "%s %s vs the generator allometric expectation from the 218 cm anchor" % (x, k), "a": x, "b": "expected", "reading": k, "va": V[x][k], "op": "~", "vb": e,
                          "result": "PASS" if abs(d) < 0.03 else "REPORT (>= 3 % off slope)", "note": "%+.1f %%" % (100 * d)})
# G. canonical Grask rows (W1 row set) on every Grask body that has its own skeleton
CANON = {}
if os.environ.get("W2C_CANON", "1") == "1":
    import gr_eval as GE
    for b, e in REG.items():
        if not e.get("grask"): continue
        d, nm = os.path.dirname(e["meas"]), os.path.basename(e["meas"])
        res = GE.evaluate(nm, d, bool(e.get("skp")))
        rows = []
        for kind in ("skeletal", "skin", "directional"):
            for r in res.get(kind, []):
                rs = r.get("result_ADG10") if kind == "directional" else r.get("result")
                if kind == "directional" and r.get("op") not in (">", "<"): rs = "PASS" if r.get("pass") else "FAIL"
                rows.append({"kind": kind, "check": r["check"], "cand": r.get("cand"), "result": rs, "va": r.get("va"), "vb": r.get("vb"), "by_t": r.get("by_t")})
        CANON[b] = rows
        bad = [x for x in rows if x["result"] not in ("PASS", "REPORT", None)]
        C.append({"code": "G", "check": "%s: canonical Grask rows (W1 row set; skeletal CIB, skin, directional)" % b, "a": b, "b": "accepted comparators", "reading": "rows",
                  "va": len(rows) - len(bad), "op": "of", "vb": len(rows), "result": "PASS" if not bad else "NOT ALL PASS", "note": "; ".join("%s %s" % (x["result"], x["check"][:80]) for x in bad)})
# D / L. frames (central GR218 vs GRN / GRB)
DOM = ["skeletal thoracic breadth / stature [t=0.0]", "skeletal shoulder-joint breadth / stature [t=0.0]", "skeletal biacromial / stature [t=0.0]",
       "skeletal crest breadth / stature [t=0.0]", "skeletal hip-joint spacing / stature [t=0.0]", "femoral S7 breadth / stature [t=0.0]", "femoral S7 depth / stature [t=0.0]",
       "knee breadth / stature (scaled slab)", "wrist breadth / stature (scaled slab)", "ankle breadth / stature (scaled slab)", "elbow breadth / stature (scaled slab)"]
for n, br in (tuple(os.environ.get("W2C_FRAMES", "GRN,GRB").split(",")),):
    if not all(x in V for x in (n, br, ce)): continue
    for k in DOM:
        for x, sg in ((br, 1), (n, -1)):
            if k in V[x]:
                d = V[x][k] / V[ce][k] - 1
                C.append({"code": "D", "check": "%s moves %s central by >= 1 %%: %s" % (x, "above" if sg > 0 else "below", k), "a": x, "b": ce, "reading": k, "va": V[x][k], "op": ">" if sg > 0 else "<",
                          "vb": V[ce][k], "margin_pct": 100 * d, "result": "PASS" if sg * d >= 0.01 else "NOT DEMONSTRATED", "note": "%+.1f %%" % (100 * d)})
    for k in ("stature (cm)", "torso_share", "leg_share", "arm_share", "forearm_over_arm", "shin_over_leg", "HH_share", "hand_share", "skeletal thoracic depth / stature [t=0.0]"):
        for x in (n, br):
            d = V[x][k] / V[ce][k] - 1; lim = 0.005 if "depth" not in k else 0.01
            C.append({"code": "L", "check": "%s unchanged vs central (%.1f %%): %s" % (x, 100 * lim, k), "a": x, "b": ce, "reading": k, "va": V[x][k], "op": "~", "vb": V[ce][k],
                      "result": "PASS" if abs(d) < lim else "FAIL", "note": "%+.2f %%" % (100 * d)})
# spec-driven comparison rows (matched height, frames vs Skarn / Gorrund, composition, extremes, AD-2 / AD-3, Marchfolk overlap)
for row in X.get("rows", []):
    a, b = row["a"], row["b"]
    if a not in V or b not in V or row["k"] not in V[a] or row["k"] not in V[b]: continue
    va, vb = V[a][row["k"]], V[b][row["k"]]
    if row.get("adj_joint"): vb = adj(vb, V[b]["stature (cm)"], V[a]["stature (cm)"], row["adj_joint"])
    add(row["code"], row["check"], a, row["op"], b, row["k"], row.get("note", ""), row.get("report", False), va, vb)
for row in X.get("invariance", []):
    a, b = row["a"], row["b"]
    if a not in V or b not in V: continue
    moved = [k for k in row["keys"] if V[a].get(k) and V[b].get(k) and abs(V[a][k] / V[b][k] - 1) >= row.get("tol", 0.01)]
    C.append({"code": row["code"], "check": row["check"], "a": a, "b": b, "reading": "shares", "va": len(moved), "op": "=", "vb": 0,
              "result": "PASS" if not moved else "FAIL", "note": "; ".join("%s %+.1f %%" % (k, 100 * (V[a][k] / V[b][k] - 1)) for k in moved) or "none"})
out = {"values": V, "checks": C, "canonical_rows": CANON, "envelope_candidates": {}}
six = [x for x in ("GR198", "GR208", "GR218", "GR229", "GR239") if x in V]
for k in V.get("GR218", {}):
    vals = [(V[x][k], x) for x in six if V[x].get(k) is not None]
    if len(vals) == len(six): out["envelope_candidates"][k] = {"min": min(vals)[0], "min_body": min(vals)[1], "max": max(vals)[0], "max_body": max(vals)[1], "status": "NON-CANON diagnostic candidate"}
json.dump(out, open(OUT, 'w'), indent=1, default=float)
import collections
print(len(C), "checks", collections.Counter(c["result"] if c["result"] in ("PASS", "REPORT") else c["result"][:16] for c in C))
for c in C:
    if c["result"] not in ("PASS", "REPORT"): print(" ", c["code"], c["check"][:110], c.get("note", "")[:160], c["result"])
