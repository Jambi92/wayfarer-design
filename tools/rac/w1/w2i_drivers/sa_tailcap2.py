# RAC W2I1 (closure order §3 D2): reachable tail cap under the AUTHOR-CLARIFIED same-state balance reference.
#   D2(a): cap read on the most permissive ADMISSIBLE coupled base inside the RSI band (base solved for size-normalized RSI 1.19, the band edge
#          0.75-1.20 less a 0.01 solver margin); constant sufficiency (RSI 1.00) is kept as a report column.
#   D2(c): the interim +3 deg relative-lean guard is judged PRIMARILY against the same-stature, same-frame / composition (and same carriage)
#          reference body = the same state carrying the reference tail (64.613 % H, base 1.0). The frozen SA-M188 comparison is SECONDARY (W1
#          continuity) and no longer gates.
#   Other guards unchanged (§256): RSI 0.75-1.20 | taper <= 1.25 x ref | A50 0.27-0.48 | A25 >= 0.065 | thoracic d/w <= 1.00 (§258).
# Same power-law base solve as sa_tailcap.py (W2I). Diagnostic only; no production cap function is authored.
# Env: CURV (tail_curv, deg; - = lift) applies a neutral-carriage offset to every body incl. the references (D4 regression);
#      STATES (comma list) restricts the state set; TGT (rsi119,rsi100) restricts the base convention. Usage: python3 sa_tailcap2.py OUT.json
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_build as B
C = B.C; Mx = B.Mx; NAR, BRD = B.NAR, B.BRD; H0 = B.H0
CURV = float(os.environ.get('CURV', '0'))
RPITCH = float(os.environ.get('RPITCH', '0')); RLEN = float(os.environ.get('RLEN', '20'))      # W2I2 root pitch (needs the sa_cand in-memory warp extension; run via w2i2_drivers/run_tailcap_root.py)
def car(p):
    p = Mx(p, {'tail_curv': CURV}) if CURV else dict(p)
    return Mx(p, {'tail_root_pitch': RPITCH, 'tail_root_len': RLEN}) if RPITCH else p
REF = B.measure(*C.build({})[:2])                      # frozen SA-M188 (0 deg carriage): normalization and the secondary lean reference
def ev(state, pct, base, h):
    p = car(Mx(state, {'tail_len': pct / 64.613, 'tail_base': base})); P, q = C.build(p); P2, q2, k = B.at_stature(P, q, h); M = B.measure(P2, q2, k)
    sH = M['height'] / H0
    return M, dict(RSI=M['tail_RSI_raw'] / REF['tail_RSI_raw'] / sH, taper=M['tail_taper_raw'] / REF['tail_taper_raw'], A50=M['tail_A50'], A25=M['tail_A25'])
def solve_base(state, pct, h, target):
    base = (pct / 64.613) ** 1.18 * (1.0 / target) ** (1 / 1.7)
    for _ in range(6):
        M, n = ev(state, pct, base, h)
        if abs(n['RSI'] - target) < 0.006: break
        base *= (n['RSI'] / target) ** (1 / 1.7)
    return base, M, n
def guards(M, n, lean0):
    return {"RSI": 0.75 <= n['RSI'] <= 1.20, "taper": n['taper'] <= 1.25, "A50": 0.27 <= n['A50'] <= 0.48, "A25": n['A25'] >= 0.065,
            "lean_same_state": M['lean_scaled_deg'] - lean0 <= 3.0, "d/w": M['thorax_d_over_w'] <= 1.00}
STATES = {"Balanced-188": ({}, H0), "Broad-188": (BRD, H0), "Narrow-188": (NAR, H0), "Narrow+fat-hi-188": (Mx(NAR, {'fat': 1.0}), H0),
          "Balanced+fat-hi-188": ({'fat': 1.0}, H0), "female-centre-188": (B.CEN, H0),
          "Balanced-168": ({}, 168.0), "Balanced-208": ({}, 208.0), "Broad-208": (BRD, 208.0)}
if os.environ.get('STATES'): STATES = {k: v for k, v in STATES.items() if k in os.environ['STATES'].split(',')}
PCTS = [55, 64.613, 70, 72, 74, 76, 78, 80, 82, 84]
TARGETS = {"rsi119": 1.19, "rsi100": 1.0}
if os.environ.get('TGT'): TARGETS = {k: v for k, v in TARGETS.items() if k in os.environ['TGT'].split(',')}
# named D2 / non-pass cases at their recorded (Part 7 / W2I) bases: id -> (state key, pct, base)
NAMED = {"Balanced 78 % (anchor, base 1.15)": ("Balanced-188", 78, 1.15), "Balanced 80 % (rule base 1.22)": ("Balanced-188", 80, 1.22),
         "Broad 80 % (anchor, base 1.16)": ("Broad-188", 80, 1.16), "Narrow + high fat 72 % (anchor, base 1.10)": ("Narrow+fat-hi-188", 72, 1.10),
         "Narrow + high fat 78 % (base 1.15)": ("Narrow+fat-hi-188", 78, 1.15), "208 cm Broad 80 % (base 1.16)": ("Broad-208", 80, 1.16),
         "55 % coupled base 0.85": ("Balanced-188", 55, 0.85), "55 % coupled base 0.83": ("Balanced-188", 55, 0.83), "168 cm + 55 % (base 0.85)": ("Balanced-168", 55, 0.85)}
if __name__ == '__main__':
    out = {"carriage_tail_curv_deg": CURV, "reference_SA-M188": {k: REF[k] for k in ('tail_len_pct', 'tail_RSI_raw', 'tail_taper_raw', 'tail_A50', 'tail_A25', 'lean_scaled_deg')},
           "state_reference": {}, "named": {}}
    for sn, (st, h) in STATES.items():
        Ms, ns = ev(st, 64.613, 1.0, h); out["state_reference"][sn] = dict(lean=Ms['lean_scaled_deg'], height=Ms['height'], dw=Ms['thorax_d_over_w'], **ns)
        print('REF', sn, round(Ms['height'], 2), 'lean %.3f' % Ms['lean_scaled_deg'], flush=True)
    for nm, (sn, pct, base) in NAMED.items():
        if sn not in STATES: continue
        st, h = STATES[sn]; M, n = ev(st, pct, base, h); lean0 = out["state_reference"][sn]['lean']; g = guards(M, n, lean0)
        out["named"][nm] = dict(state=sn, pct=pct, base=base, tail_len_pct=M['tail_len_pct'], **n, lean=M['lean_scaled_deg'], dlean_same_state=M['lean_scaled_deg'] - lean0,
                                dlean_SA_M188=M['lean_scaled_deg'] - REF['lean_scaled_deg'], dw=M['thorax_d_over_w'], guards=g, ok=all(g.values()))
        print('NAMED', nm, 'dlean %.2f / %.2f' % (M['lean_scaled_deg'] - lean0, M['lean_scaled_deg'] - REF['lean_scaled_deg']), 'OK' if all(g.values()) else [k for k, v in g.items() if not v], flush=True)
    for tk, tv in TARGETS.items():
        out[tk] = {}
        for sn, (st, h) in STATES.items():
            lean0 = out["state_reference"][sn]['lean']; rows = []
            for pct in PCTS:
                base, M, n = solve_base(st, pct, h, tv); g = guards(M, n, lean0)
                rows.append(dict(pct=pct, base=base, tail_len_pct=M['tail_len_pct'], **n, lean=M['lean_scaled_deg'], dlean_same_state=M['lean_scaled_deg'] - lean0,
                                 dlean_SA_M188=M['lean_scaled_deg'] - REF['lean_scaled_deg'], dw=M['thorax_d_over_w'], guards=g, ok=all(g.values())))
                print(tk, sn, pct, 'base %.3f' % base, {k: round(v, 3) for k, v in n.items()}, 'dlean %.2f / %.2f' % (rows[-1]['dlean_same_state'], rows[-1]['dlean_SA_M188']),
                      'OK' if rows[-1]['ok'] else [k for k, v in g.items() if not v], flush=True)
                if not rows[-1]['ok'] and pct > 64.613: break                 # every guard is monotone in length past the reference
            okp = [r['pct'] for r in rows if r['ok']]; cap = max(okp) if okp else None; binding = []
            if cap is not None and cap < PCTS[-1] and len(rows) > PCTS.index(cap) + 1:
                lo = cap; hi = PCTS[PCTS.index(cap) + 1]; binding = [k for k, v in rows[PCTS.index(cap) + 1]['guards'].items() if not v]
                for _ in range(4):
                    mid = 0.5 * (lo + hi); base, M, n = solve_base(st, mid, h, tv); okm = all(guards(M, n, lean0).values())
                    lo, hi = (mid, hi) if okm else (lo, mid)
                cap = lo
            lowfail = [k for k, v in rows[0]['guards'].items() if not v]
            out[tk][sn] = dict(params={k: v for k, v in st.items()}, stature=h, lean_ref=lean0, rows=rows, reachable_cap_pct=cap, binding=binding, low_end_55_fail=lowfail)
            print('CAP', tk, sn, cap, binding, 'low55', lowfail, flush=True)
    json.dump(out, open(sys.argv[1], 'w'), indent=1, default=float)
