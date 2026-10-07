# RAC W2A: Marchfolk central-stature frames (breadth-only Narrow / Broad, ±8 % clavicle Y, spine_01-03 X, pelvis X) and composition variants
# (order W2A items 4-5). Frame must stay skeletal only (lengths, depth and joints unchanged); composition must not redefine anatomy (segment and head
# shares stay within 1 % of the central body; skin breadth / depth changes are composition diagnostics). Broad must not become Skarn-like.
# Usage: python3 w2a_fc.py JBW.json  -> reviews/rac-w2a-mf-evidence/frames_comp.json
import sys, os, json
R = '/home/claude/wayfarer-design'; S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; W = S + '/w2a'
EV = R + '/reviews/rac-w2a-mf-evidence'; BS = R + '/reviews/rac-w1i-evidence/skeletal'; JB = json.load(open(sys.argv[1]))
B = {"M173": (S + '/w1f/final/MF-M-R', BS, 'MF-M-R'), "M Narrow": (W + '/g/MFM-NARROWB/final/MF-M-R', W + '/g/MFM-NARROWB/skp', 'MF-M-R'),
     "M Broad": (W + '/g/MFM-BROADB/final/MF-M-R', W + '/g/MFM-BROADB/skp', 'MF-M-R'), "M minimum composition": (S + '/w1r/lean/MF-M-R-LEAN', None, None),
     "M low 0.25 / 0.25": (S + '/w1f/low/MF-M-R-LOW', None, None), "M low muscle 0 / 0.5": (W + '/comp/MFM-LOWMUS', None, None), "M high muscle 1 / 0.5": (W + '/comp/MFM-HIMUS', None, None),
     "M higher fat 0.5 / 1": (W + '/comp/MFM-HIFAT', None, None), "M high muscle + fat 1 / 1": (W + '/comp/MFM-HIBOTH', None, None),
     "F173": (S + '/w1f/final/MF-F-R', BS, 'MF-F-R'), "F Narrow": (W + '/fr/MFF-NARROWB', None, None), "F Broad": (W + '/fr/MFF-BROADB', None, None),
     "F low 0.25 / 0.25": (W + '/comp/MFF-LOW', None, None), "F high muscle + fat 1 / 1": (W + '/comp/MFF-HIBOTH', None, None), "SK": (S + '/w1f/final/SK', BS, 'SK')}
JK = {"M173": "MF-M-R", "M Narrow": "MFM-NARROWB", "M Broad": "MFM-BROADB", "F173": "MF-F-R", "SK": "SK"}
RD = ["torso / stature", "leg / stature", "arm / stature", "head height / stature", "thoracic breadth / stature (skin)", "thoracic depth / stature (skin)", "shoulder-joint breadth / stature",
      "crest / thoracic breadth (skin)", "hip-joint spacing / stature (skin)", "skeletal thoracic breadth / stature", "skeletal thoracic depth / stature", "skeletal crest / stature",
      "skeletal hip-joint spacing / stature", "skeletal bitrochanteric / crest", "elbow breadth / stature (scaled slab)", "wrist breadth / stature (scaled slab)", "knee breadth / stature (scaled slab)"]
V = {}
for b, (p, skd, sid) in B.items():
    if not os.path.exists(p + '_meas.json'): print('missing', b); continue
    c = json.load(open(p + '_meas.json'))["combined"]; r = c["ratio"]
    v = {"torso / stature": r["torso_share"], "leg / stature": r["leg_share"], "arm / stature": r["arm_share"], "head height / stature": r["HH_share"],
         "thoracic breadth / stature (skin)": r["thorax_breadth_share"], "thoracic depth / stature (skin)": r["thorax_depth_share"], "shoulder-joint breadth / stature": r["shoulder_joint_share"],
         "crest / thoracic breadth (skin)": r["pelvis_over_thorax_breadth"], "hip-joint spacing / stature (skin)": r["hip_joint_breadth_share"]}
    if skd and os.path.exists(skd + '/t0.0/%s_meas.json' % sid):
        q = json.load(open(skd + '/t0.0/%s_meas.json' % sid))["combined"]["ratio"]
        v.update({"skeletal thoracic breadth / stature": q["thorax_breadth_share"], "skeletal thoracic depth / stature": q["thorax_depth_share"], "skeletal crest / stature": q["crest_share"],
                  "skeletal hip-joint spacing / stature": q["hip_joint_breadth_share"], "skeletal bitrochanteric / crest": q["bitroch_over_crest"]})
    if JK.get(b) in JB:
        for j in ("elbow", "wrist", "knee"): v["%s breadth / stature (scaled slab)" % j] = JB[JK[b]]["scaled"][j]
    V[b] = v
C = []
def add(name, ok, note="", result=None): C.append({"check": name, "result": result or ("PASS" if ok else "FAIL"), "note": note})
for cfg in ("M", "F"):
    ce = cfg + "173"
    for fr in ("Narrow", "Broad"):
        b = "%s %s" % (cfg, fr)
        if b not in V: continue
        same = [k for k in ("torso / stature", "leg / stature", "arm / stature", "head height / stature", "skeletal thoracic depth / stature", "elbow breadth / stature (scaled slab)",
                            "wrist breadth / stature (scaled slab)", "knee breadth / stature (scaled slab)") if k in V[b] and k in V[ce]]
        moved = [k for k in same if abs(V[b][k] / V[ce][k] - 1) >= 0.005]
        add("%s frame is skeletal breadth only: lengths, head, skeletal depth and joints within 0.5 %% of central" % b, not moved, "checked: %d; moved: %s" % (len(same), ", ".join(moved) or "none"))
        k = "skeletal thoracic breadth / stature" if "skeletal thoracic breadth / stature" in V[b] else "thoracic breadth / stature (skin)"
        d = 100 * (V[b][k] / V[ce][k] - 1)
        add("%s frame changes breadth in its own direction (%s %+.1f %%)" % (b, k, d), d < 0 if fr == "Narrow" else d > 0)
    if "M Broad" in V and cfg == "M":
        for k in ("skeletal thoracic depth / stature", "wrist breadth / stature (scaled slab)", "knee breadth / stature (scaled slab)"):
            if k in V["M Broad"] and k in V["SK"]:
                add("M Broad not Skarn-like: %s < SK" % k, V["M Broad"][k] < V["SK"][k] * 0.99, "%.4f vs %.4f" % (V["M Broad"][k], V["SK"][k]))
    for b in [x for x in V if x.startswith(cfg + " ") and ("muscle" in x or "fat" in x or "low" in x or "minimum" in x)]:
        moved = [k for k in ("torso / stature", "leg / stature", "arm / stature", "head height / stature") if abs(V[b][k] / V[ce][k] - 1) >= 0.01]
        add("%s: composition does not redefine anatomy (torso, leg, arm, head shares within 1 %% of central)" % b, not moved, "moved: %s" % (", ".join("%s %+.1f %%" % (k, 100 * (V[b][k] / V[ce][k] - 1)) for k in moved) or "none"))
json.dump({"readings": RD, "values": V, "checks": C}, open(EV + '/frames_comp.json', 'w'), indent=1)
for c in C: print(c["result"], c["check"][:100], c["note"][:120])
