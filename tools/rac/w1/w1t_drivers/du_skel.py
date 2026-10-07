# RAC W1t: Durrim skeletal-proxy rows (CIB stations at t = 0 / 0.5 / 1.0 tissue allowance; AD-G10) on the W1i skeletal base: DU-P2b..P6
# (PV-D16: canon is validated on skeletal geometry), thorax, femoral S7 section, and the short-race structural-mass axis CG < PK < DU against
# the accepted Pipkin (PK-NAT, W1i base) and Cogling (CGJ7 grid).  Usage: python3 du_skel.py TAG=du_skp_dir|BASE ...
import sys, os, json
R = '/home/claude/wayfarer-design'; S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
B = R + '/reviews/rac-w1i-evidence/skeletal'; T = ('0.0', '0.5', '1.0')
# MFSKP: matched-stature MF grid (152 cm boundary)
SRC = {"MF-M-R": (os.environ.get('MFSKP', B), 'MF-M-R'), "SK": (B, 'SK'), "PK": (B, 'PK-NAT'), "CG": (S + '/w1r/cgj7/skp', 'CG-NAT')}
def cls(op, va, vb):
    rel = abs(va - vb) / abs(vb); holds = {">": va > vb, "<": va < vb, ">=": va >= vb, "<=": va <= vb}[op]
    if op in (">", "<"): return ("PASS" if rel >= 0.01 else "NOT DEMONSTRATED") if holds else "FAIL"
    return "PASS" if holds else ("MARGINAL" if rel < 0.01 else "FAIL")
def load(d, i, t):
    c = json.load(open('%s/t%s/%s_meas.json' % (d, t, i)))["combined"]; b7, d7 = c["alpc_stations"]["S7"]
    return {**c["ratio"], "shaft_b_share": b7 / c["stature"], "shaft_d_share": d7 / c["stature"]}
ROWS = [("DU-P2b hip-joint spacing / stature > MF", "DU L114", "hip_joint_breadth_share", ">", "MF-M-R"),
        ("DU-P3 pelvic vertical / crest breadth < MF (broad and compact, not tall)", "DU L116", "pelvic_vertical_over_crest", "<", "MF-M-R"),
        ("DU-P4 AP pelvic depth / stature > MF", "DU L117", "pelvic_depth_share", ">", "MF-M-R"),
        ("DU-P5 iliac-crest breadth / stature > MF", "DU L118", "crest_share", ">", "MF-M-R"),
        ("DU-P6 thorax-led: crest / thoracic breadth <= MF", "DU L119", "pelvis_over_thorax_breadth", "<=", "MF-M-R"),
        ("DU-P4 continuity: pelvic depth / thoracic depth (no abrupt shallow step) vs MF — report", "DU L117", "pelvic_depth_over_thorax_depth", ">=", "MF-M-R"),
        ("broad skeletal thorax: thoracic breadth / stature > MF", "DU L30, L101", "thorax_breadth_share", ">", "MF-M-R"),
        ("deep skeletal thorax: thoracic depth / stature > MF", "DU L29, L101", "thorax_depth_share", ">", "MF-M-R"),
        ("substantial femoral structure: S7 breadth / stature > MF", "DU L40, L130", "shaft_b_share", ">", "MF-M-R"),
        ("substantial femoral structure: S7 depth / stature > MF", "DU L40, L130", "shaft_d_share", ">", "MF-M-R"),
        ("structural-mass axis PK < DU: S7 breadth / stature", "SRR L41-48; order item 5", "shaft_b_share", ">", "PK"),
        ("structural-mass axis PK < DU: S7 depth / stature", "SRR L41-48; order item 5", "shaft_d_share", ">", "PK"),
        ("structural-mass axis CG < DU: S7 breadth / stature", "SRR L41-48; order item 5", "shaft_b_share", ">", "CG"),
        ("structural-mass axis CG < DU: S7 depth / stature", "SRR L41-48; order item 5", "shaft_d_share", ">", "CG"),
        ("thorax vs Pipkin: skeletal thoracic depth / stature > PK", "SR-COMP-03", "thorax_depth_share", ">", "PK"),
        ("thorax-led vs Pipkin pelvis-led: crest / thoracic breadth < PK", "DU-P6; PIPKIN L150", "pelvis_over_thorax_breadth", "<", "PK"),
        ("thorax vs Cogling: skeletal thoracic breadth / stature > CG", "COG-BODY-10", "thorax_breadth_share", ">", "CG"),
        ("thorax vs Skarn: skeletal thoracic depth / stature vs SK — report", "DU L29", "thorax_depth_share", ">", "SK")]
for a in sys.argv[1:]:
    tag, d = a.split('=', 1); d = B if d == 'BASE' else d; nm = 'DU-NAT' if d == B else 'DU-NAT'
    V = {t: {**{s: load(*SRC[s], t) for s in SRC}, "DU": load(d, nm, t)} for t in T}
    rows = []
    for chk, src, k, op, b in ROWS:
        rep = "report" in chk
        per = {t: (V[t]["DU"][k], V[t][b][k]) for t in T}; res = {t: ("REPORT" if rep else cls(op, *v)) for t, v in per.items()}; u = set(res.values())
        rows.append({"cand": "DU", "check": chk, "canon": src, "reading": k, "op": op, "b": b, "by_t": per, "result_by_t": res, "result": u.pop() if len(u) == 1 else "T-SENSITIVE"})
    json.dump(rows, open(R + '/reviews/rac-w1t-du-evidence/skeletal_%s.json' % tag, 'w'), indent=1, default=float)
    print(tag, len(rows), 'non-PASS:', [(r['check'][:60], r['result'], {t: '%.4f/%.4f' % v for t, v in r['by_t'].items()}) for r in rows if r['result'] not in ('PASS', 'REPORT')])
