# RAC W1k: Grask vs Gorrund (accepted W1i/W1j point at its 215 / 222 donors: 217.0 / 224.1 cm) and Broad Skarn (215 / 222 cm)
# at overlapping stature: the canon directions that separate Grask without stature (GR L148, L279, L727; R2 L53-L61; RA L131).
# Same measurement layer as directional_checks.py (arm_measure 'combined' ratios). AD-G10 classes on strict directions.
import json, os
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; M = S + '/w1k/matched'
EV = os.environ.get('EVDIR', '/home/claude/wayfarer-design/reviews/rac-w1k-gr-evidence')
L = lambda p: json.load(open(p))["combined"]
B = {"GR 218": L(os.environ.get('GRMEAS', S + '/w1g/final/GR_meas.json')), "GO 217": L(M + '/GO217_meas.json'), "GO 224": L(M + '/GO224_meas.json'),
     "Broad SK 215": L(M + '/SKB215_meas.json'), "Broad SK 222": L(M + '/SKB222_meas.json')}
H = {k: v["stature"] for k, v in B.items()}
ROWS = [("torso_share", "<", ("GO 217", "GO 224", "Broad SK 215", "Broad SK 222"), "GR L198; R2 L53 (GO > GR)"),
        ("leg_share", ">", ("GO 217", "GO 224", "Broad SK 215", "Broad SK 222"), "GR L233; RAC-04 L29"),
        ("arm_share", ">", ("GO 217", "GO 224", "Broad SK 215", "Broad SK 222"), "GR L241; GO L221"),
        ("span_der", ">", ("GO 217", "GO 224", "Broad SK 215", "Broad SK 222"), "GR L243; RA L131"),
        ("forearm_over_arm", ">", ("Broad SK 215", "Broad SK 222"), "GR L247"),
        ("finger_over_palm", ">", ("Broad SK 215", "Broad SK 222"), "GR L255"),
        ("thorax_breadth_share", "<", ("GO 217", "GO 224", "Broad SK 215", "Broad SK 222"), "GR L203; RMQ RM-LR-02 (a)"),
        ("thorax_depth_share", "<", ("GO 217", "GO 224"), "RMQ RM-LR-02 (b)"),
        ("elbow_over_humerus", "<", ("GO 217", "GO 224"), "R2 L61 (GO > GR joints)"),
        ("knee_over_femur", "<", ("GO 217", "GO 224"), "R2 L61 (GO > GR joints)")]
out = {"stature": H, "rows": []}
for k, op, comps, src in ROWS:
    a = B["GR 218"]["ratio"][k]
    for c in comps:
        b = B[c]["ratio"][k]; holds = a > b if op == ">" else a < b; rel = abs(a - b) / abs(b)
        res = ("PASS" if rel >= 0.01 else "NOT DEMONSTRATED") if holds else "FAIL"
        out["rows"].append({"reading": k, "op": op, "GR": a, "comparator": c, "value": b, "margin_pct": 100 * rel * (1 if holds else -1), "result": res, "canon": src})
        print("%-22s GR %.4f %s %-13s %.4f  %+.2f %%  %s" % (k, a, op, c, b, 100 * rel * (1 if holds else -1), res))
json.dump(out, open(EV + '/matched_height.json', 'w'), indent=1, default=float); print(H)
