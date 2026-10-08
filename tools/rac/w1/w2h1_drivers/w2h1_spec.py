# RAC W2H1 specification: the full W2H specification (w2h_drivers/w2h_spec.py; Durrim names now resolve to the D1-corrected bodies) plus
# B1 rows: D1 before / after on every Durrim family body (order §4) and the bounded-correction guard (order §2: nothing but pelvic AP may move
# materially; scored at 1 % per reading, skeletal at t = 0). Usage: python3 w2h1_spec.py OUT.json
import sys, json, subprocess
T = '/home/claude/wayfarer-design/tools/rac/w1'; S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
tmp = S + '/w2h1/spec_w2h.json'; subprocess.run(['python3', T + '/w2h_drivers/w2h_spec.py', tmp], check=True, capture_output=True); P = json.load(open(tmp))
T0 = " [t=0.0]"; sk = lambda x: "skeletal %s%s" % (x, T0)
JS = lambda j: "%s breadth / stature (exact-plane section)" % j
TOUCHED = [sk("AP pelvic depth / stature"), sk("pelvic AP / thoracic depth"), "pelvic_depth_share", "pelvic_depth_over_thorax_depth"]
GUARD = [sk("thoracic depth / stature"), sk("thoracic breadth / stature"), sk("crest breadth / stature"), sk("pelvic vertical / stature"), sk("pelvic vertical / crest"),
         sk("hip-joint spacing / stature"), "hip-joint height / stature", sk("crest / thoracic breadth"), "torso_share", "arm_share", "leg_share", "neck_share", "HH_share",
         "hand_share", "foot_share", "palm breadth / stature", "foot breadth / stature", "thorax_depth_share", "thorax_breadth_share", sk("femoral shaft breadth / femur"),
         "femoral S7 breadth / stature" + T0, "femoral S7 depth / stature" + T0] + [JS(j) for j in ("elbow", "wrist", "knee", "ankle")]
for b in ["DU122", "DU137", "DU152", "DUN122", "DUB122", "DUN137", "DUB137", "DUN152", "DUB152"]:
    for k in TOUCHED: P["rows"].append({"code": "B1", "check": "D1 before / after %s: %s" % (b, k.replace(T0, "")), "a": b, "op": "vs", "b": b + "-W2H", "k": k, "note": "D1 pelvis Z x1.04", "report": True})
    P["invariance"].append({"code": "B1", "check": "D1 bounded: %s keeps every non-D1 relation within 1 %% of the uncorrected body" % b, "a": b, "b": b + "-W2H", "keys": GUARD})
for b in ["DU137-" + c for c in ("LOWMUS", "HIMUS", "HIFAT", "HIBOTH", "LOW", "MIN")] + ["DU152-LOW", "DU152-MIN", "DU152-HIBOTH", "DUNLOW"]:
    P["invariance"].append({"code": "B1", "check": "D1 bounded (composition body): %s keeps every non-pelvic skin share within 1 %% of the uncorrected body" % b, "a": b, "b": b + "-W2H",
                            "keys": [k for k in GUARD if not k.startswith(("skeletal", "femoral"))]})
    P["rows"].append({"code": "B1", "check": "D1 before / after %s: skin AP pelvic depth / stature" % b, "a": b, "op": "vs", "b": b + "-W2H", "k": "pelvic_depth_share", "note": "skin diagnostic", "report": True})
# route reproduction: DU137R reproduces the uncorrected accepted DU-NAT (now the BEFORE body)
for r in P["invariance"]:
    if r["code"] == "Z" and r["a"] == "DU137R": r["b"] = "DU137-W2H"; r["check"] = r["check"].replace("accepted DU137", "accepted (uncorrected) DU-NAT")
# DU-P4 before row (uncorrected) for the record
P["rows"].append({"code": "P4", "check": "DU-P4 BEFORE (uncorrected W2H DU152) vs Marchfolk 152 (record)", "a": "DU152-W2H", "op": ">", "b": "MF152", "k": sk("AP pelvic depth / stature"), "note": "W2H gate +0.81 %", "report": True})
# DU-P4 composition independence of the corrected skeleton: LOW / MIN / HIBOTH share the DU152 skeleton (same grid) -> skeletal row identical; skin rows in P4 already
json.dump(P, open(sys.argv[1], 'w'), indent=1)
print(len(P["rows"]), "rows", len(P["invariance"]), "invariance", len(P["moves"]), "moves", len(P["passing"]), "passing")
