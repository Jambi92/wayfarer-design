# RAC W1r: skeletal (CIB) rows for Cogling bodies on the W1i skeletal base, with the accepted Grask (W1l), Aelari (AEL1), Vael (VAL4) and
# Fenn (FNL4) readings in their slots (accepted Pipkin = the W1i PK-NAT readings already in the base, same geometry). Cogling candidate
# readings copied into both the CG and CG-NAT slots; TAG=BASE keeps the W1i as-built CG-NAT readings (control).
# Usage: python3 cg_skel.py TAG=cg_skp_dir|BASE ...  -> reviews/rac-w1r-cg-evidence/skeletal_<TAG>.json
import sys, os, json, shutil
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1')
import skeletal_checks as SC
R = '/home/claude/wayfarer-design'; S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
SLOTS = {"GR": (S + '/w1l/probe/skp_GRL925_1200', 'GRL925_1200'), "AE": (S + '/w1m/ael1/skp', 'AE'), "VA": (S + '/w1n/val4/skp', 'VA'), "FN": (S + '/w1p/fnl4/skp', 'FN')}
def cls(op, va, vb):
    rel = abs(va - vb) / abs(vb); holds = {">": va > vb, "<": va < vb, ">=": va >= vb, "<=": va <= vb}[op]
    if op in (">", "<"): return ("PASS" if rel >= 0.01 else "NOT DEMONSTRATED") if holds else "FAIL"
    return "PASS" if holds else ("MARGINAL" if rel < 0.01 else "FAIL")
# W1r Cogling skeletal-proxy rows (CIB stations at t = 0 / 0.5 / 1.0 cm tissue allowance; AD-G10)
CGROWS = [("narrow core: skeletal thoracic breadth / stature < MF", "CG L100-102, L649-661", "thorax_breadth_share", "<", "MF-M-R", False),
          ("less pelvis-led than Pipkin: crest / thoracic breadth < PK", "CG L102, L258-262, L685-687; order L32", "pelvis_over_thorax_breadth", "<", "PK-NAT", False),
          ("less pelvis-led than Pipkin: pelvic depth / thoracic depth < PK", "CG L258-262; order L32", "pelvic_depth_over_thorax_depth", "<", "PK-NAT", False),
          ("less pelvis-led than Pipkin: pelvic vertical / thoracic vertical < PK", "CG L258-262, L685-687; order L32", "pelvic_vertical_over_thoracic_vertical", "<", "PK-NAT", False),
          ("fine shafts: S7 subtrochanteric section breadth / stature < height-normalized MF", "CG L116-121", "shaft_b_share", "<", "MF-M-R", False),
          ("fine shafts: S7 subtrochanteric section depth / stature < height-normalized MF", "CG L116-121", "shaft_d_share", "<", "MF-M-R", False),
          ("structural-mass axis: S7 breadth / stature CG < PK", "SRR L41-48; RAC-05 L32", "shaft_b_share", "<", "PK-NAT", False),
          ("structural-mass axis: S7 depth / stature CG < PK", "SRR L41-48; RAC-05 L32", "shaft_d_share", "<", "PK-NAT", False),
          ("structural-mass axis: S7 breadth / stature CG < DU", "SRR L41-48; RAC-05 L32", "shaft_b_share", "<", "DU-NAT", False),
          ("structural-mass axis: S7 depth / stature CG < DU", "SRR L41-48; RAC-05 L32", "shaft_d_share", "<", "DU-NAT", False),
          ("S7 breadth / femur length vs MF (per-segment; femur shortened by design)", "method comparison", "shaft_b_over_femur", "<", "MF-M-R", True),
          ("S7 depth / femur length vs MF (per-segment; femur shortened by design)", "method comparison", "shaft_d_over_femur", "<", "MF-M-R", True),
          ("crest / thoracic breadth vs MF (W1d packet default, not authored canon)", "W1d packet L700", "pelvis_over_thorax_breadth", "<=", "MF-M-R", True),
          ("bitrochanteric / crest vs MF (hip apparatus)", "report", "bitroch_over_crest", ">=", "MF-M-R", True)]
for a in sys.argv[1:]:
    tag, skp = a.split('=', 1); tmp = S + '/w1r/chk_' + tag
    if os.path.exists(tmp): shutil.rmtree(tmp)
    shutil.copytree(R + '/reviews/rac-w1i-evidence/skeletal', tmp, ignore=shutil.ignore_patterns('*.jpg', 'skeletal_checks.json', '*.log'))
    for t in ('0.0', '0.5', '1.0'):
        if skp != 'BASE':
            for slot in ('CG', 'CG-NAT'): shutil.copy(skp + '/t%s/CG-NAT_meas.json' % t, tmp + '/t%s/%s_meas.json' % (t, slot))
        for slot, (d, nm) in SLOTS.items(): shutil.copy(d + '/t%s/%s_meas.json' % (t, nm), tmp + '/t%s/%s_meas.json' % (t, slot))
    rows = [r for r in SC.run(tmp) if 'CG' in (r.get('cand'), r.get('b'))]   # none exist in skeletal_checks for CG; W1r rows below
    def L(t, i):
        c = json.load(open(tmp + '/t%s/%s_meas.json' % (t, i)))["combined"]; b, d = c["alpc_stations"]["S7"]
        return {**c["ratio"], "shaft_b_share": b / c["stature"], "shaft_d_share": d / c["stature"]}
    for chk, src, k, op, b, rep in CGROWS:
        per = {t: (L(t, 'CG-NAT')[k], L(t, b)[k]) for t in ('0.0', '0.5', '1.0')}
        res = {t: ('REPORT' if rep else cls(op, *v)) for t, v in per.items()}; u = set(res.values())
        rows.append({"cand": "CG", "check": chk + (" — REPORT ONLY" if rep else ""), "canon": src, "reading": k, "op": op, "b": b, "by_t": per, "result_by_t": res,
                     "result": (u.pop() if len(u) == 1 else "T-SENSITIVE"), "dependency": b == "DU-NAT"})
    json.dump(rows, open(R + '/reviews/rac-w1r-cg-evidence/skeletal_%s.json' % tag, 'w'), indent=1, default=float)
    print(tag, len(rows), 'non-PASS:', [(r['cand'], r['check'][:60], r['result'], {t: '%.4f/%.4f' % v for t, v in r.get('by_t', {}).items()}) for r in rows if r['result'] not in ('PASS', 'REPORT')])
