# RAC W1s: skeletal-proxy (CIB stations, t = 0 / 0.5 / 1.0 cm-equivalent tissue allowance) trunk and pelvis readings for a Halvren body
# against the six accepted sources (MF-M-R, SK, SG from the W1i skeletal base; FNL4, AEL1, VAL4 from their accepted-candidate grids).
# Rows: inside the six-source span at every t (HV L105, L122), and the MF -> elf interpolation fractions per pelvic reading
# (a linear morph gives one fraction for every reading; HV L122). Control: the W1i base HV readings vs this grid's HV readings.
# Usage: python3 hv_skel.py TAG=hv_skp_dir ...  -> reviews/rac-w1s-hv-evidence/skeletal_<TAG>.json
import sys, os, json
R = '/home/claude/wayfarer-design'; S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
B = R + '/reviews/rac-w1i-evidence/skeletal'
SRC = {"MF": (B, 'MF-M-R'), "SK": (B, 'SK'), "SG": (B, 'SG'), "FN": (S + '/w1p/fnl4/skp', 'FN'), "AE": (S + '/w1m/ael1/skp', 'AE'), "VA": (S + '/w1n/val4/skp', 'VA')}
T = ('0.0', '0.5', '1.0')
def load(d, i, t):
    c = json.load(open('%s/t%s/%s_meas.json' % (d, t, i)))["combined"]; s7b, s7d = c["alpc_stations"]["S7"]
    return {**c["ratio"], "shaft_b_share": s7b / c["stature"], "shaft_d_share": s7d / c["stature"]}
K = [("skeletal thoracic breadth / stature", "thorax_breadth_share"), ("skeletal thoracic depth / stature", "thorax_depth_share"), ("crest / thoracic breadth", "pelvis_over_thorax_breadth"),
     ("pelvic depth / thoracic depth", "pelvic_depth_over_thorax_depth"), ("pelvic depth / crest", "pelvic_depth_over_crest"), ("pelvic vertical / crest", "pelvic_vertical_over_crest"),
     ("bitrochanteric / crest", "bitroch_over_crest"), ("hip-joint breadth / stature", "hip_joint_breadth_share"), ("biacromial / thoracic breadth", "biacromial_over_S2_b"),
     ("S7 femoral section breadth / stature", "shaft_b_share"), ("S7 femoral section depth / stature", "shaft_d_share")]
PELV = ("pelvis_over_thorax_breadth", "pelvic_depth_over_thorax_depth", "pelvic_depth_over_crest", "pelvic_vertical_over_crest", "bitroch_over_crest", "hip_joint_breadth_share")
for a in sys.argv[1:]:
    tag, d = a.split('=', 1); rows = []
    V = {t: {**{s: load(*SRC[s], t) for s in SRC}, "HV": load(d, 'HV', t)} for t in T}
    for name, k in K:
        per = {t: {i: V[t][i][k] for i in V[t]} for t in T}; res = {}
        for t in T:
            lo, hi = min(per[t][s] for s in SRC), max(per[t][s] for s in SRC); v = per[t]["HV"]
            b = 0 if lo <= v <= hi else 100 * ((v - hi) / hi if v > hi else (v - lo) / lo)
            res[t] = "PASS" if b == 0 else ("MARGINAL" if abs(b) < 1 else "FAIL")
        u = set(res.values())
        rows.append({"cand": "HV", "check": "%s inside the six-source span (skeletal proxy)" % name, "canon": "HV L105, L122", "reading": k, "by_t": per, "result_by_t": res,
                     "result": u.pop() if len(u) == 1 else "T-SENSITIVE", "nearest_t0": min(SRC, key=lambda s: abs(per['0.0']["HV"] / per['0.0'][s] - 1))})
    for e in ("FN", "AE", "VA"):
        f = {k: (V['0.0']["HV"][k] - V['0.0']["MF"][k]) / (V['0.0'][e][k] - V['0.0']["MF"][k]) for k in PELV if abs(V['0.0'][e][k] - V['0.0']["MF"][k]) > 1e-4}
        rows.append({"cand": "HV", "check": "pelvis (skeletal, t = 0): MF -> %s interpolation fractions per reading — REPORT ONLY" % e, "canon": "HV L122 (not a linear morph)",
                     "fractions": f, "spread": max(f.values()) - min(f.values()), "result": "REPORT"})
    ctl = None
    if os.path.exists(B + '/t0.0/HV_meas.json'):
        ctl = max(abs(load(B, 'HV', t)[k] - V[t]["HV"][k]) for t in T for _, k in K)
    out = {"rows": rows, "control_max_abs_diff_vs_W1i_base_HV": ctl}
    json.dump(out, open(R + '/reviews/rac-w1s-hv-evidence/skeletal_%s.json' % tag, 'w'), indent=1, default=float)
    print(tag, len(rows), 'control', ctl, 'non-PASS:', [(r['check'][:60], r['result']) for r in rows if r['result'] not in ('PASS', 'REPORT')])
    for r in rows:
        if 'fractions' in r: print('  ', r['check'][:60], {k[:14]: round(v, 2) for k, v in r['fractions'].items()})
