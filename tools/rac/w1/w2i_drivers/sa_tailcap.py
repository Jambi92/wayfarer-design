# RAC W2I §11-12 (RM-UB-04 body-measurement portion): reachable tail cap per frame / composition state under the accepted SAURIN §256 coupling.
# For each state and tail length (% standing height) the dependent tail base is SOLVED for constant root sufficiency (size-normalized RSI = 1.00
# of the W2I-reproduced reference; §256.1 "length drives the base"), then every §256 guard is evaluated:
#   RSI 0.75-1.20 (by construction 1.00) | abrupt taper <= 1.25 x ref | A50 0.27-0.48 | A25 >= 0.065 | counterbalance: lean - lean(state, reference tail) <= +3 deg
#   (§256.4 is relative to the frozen reference; reported both relative to the state's own reference-tail lean and to SA-M) | thoracic d/w <= 1.00 (§258)
# The reachable cap is the longest length passing every guard. Tail ratios are normalized to the W2I-reproduced SA-M (axis re-derived on the
# frozen base: taper_raw +2.3 % vs Part 7, RSI_raw -0.3 %). Diagnostic only; no interpolation function is asserted. Usage: python3 sa_tailcap.py OUT.json
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_build as B
C = B.C; Mx = B.Mx; NAR, BRD = B.NAR, B.BRD; H0 = B.H0
REF = B.measure(*C.build({})[:2])
def norm(M, sH=1.0):
    return dict(RSI=M['tail_RSI_raw'] / REF['tail_RSI_raw'] / sH, taper=M['tail_taper_raw'] / REF['tail_taper_raw'], A50=M['tail_A50'], A25=M['tail_A25'])
def ev(state, pct, base, h=H0):
    p = Mx(state, {'tail_len': pct / 64.613, 'tail_base': base}); P, q = C.build(p); P2, q2, k = B.at_stature(P, q, h); M = B.measure(P2, q2, k)
    return M, norm(M, M['height'] / H0)
def solve_base(state, pct, h=H0, target=1.0):
    """fixed-point on the §256.1 power law RSI ~ length^2 / base^1.7: base <- base * (RSI / target)^(1 / 1.7)"""
    base = (pct / 64.613) ** 1.18 * (1.0 / target) ** (1 / 1.7)
    for _ in range(6):
        M, n = ev(state, pct, base, h)
        if abs(n['RSI'] - target) < 0.006: break
        base *= (n['RSI'] / target) ** (1 / 1.7)
    return base, M, n
STATES = {"Balanced-ref": {}, "Broad": BRD, "Narrow": NAR, "Narrow+fat-hi": Mx(NAR, {'fat': 1.0}), "Balanced+fat-hi": {'fat': 1.0}, "female-centre": B.CEN}
PCTS = [55, 64.613, 70, 72, 74, 76, 78, 80, 82]
TARGETS = {'constant sufficiency (RSI 1.00)': 1.0, 'most permissive admissible base (RSI 1.20 band edge)': 1.19}
if __name__ == '__main__':
    out = {"reference": {k: REF[k] for k in ('tail_len_pct', 'tail_RSI_raw', 'tail_taper_raw', 'tail_A50', 'tail_A25', 'lean_scaled_deg', 'tail_mass_share')}, "states": {}}
    for tn, tv in TARGETS.items():
      key = "states_" + ("rsi100" if tv == 1.0 else "rsi120"); out[key] = {}
      for sn, st in STATES.items():
        Ms, _ = ev(st, 64.613, 1.0); lean0 = Ms['lean_scaled_deg']; rows = []
        for pct in PCTS:
            base, M, n = solve_base(st, pct, target=tv)
            g = {"RSI": 0.75 <= n['RSI'] <= 1.20, "taper": n['taper'] <= 1.25, "A50": 0.27 <= n['A50'] <= 0.48, "A25": n['A25'] >= 0.065,
                 "lean_rel_state": M['lean_scaled_deg'] - lean0 <= 3.0, "lean_rel_SA-M": M['lean_scaled_deg'] - REF['lean_scaled_deg'] <= 3.0, "d/w": M['thorax_d_over_w'] <= 1.00}
            rows.append(dict(pct=pct, base=base, tail_len_pct=M['tail_len_pct'], **n, lean=M['lean_scaled_deg'], dlean_state=M['lean_scaled_deg'] - lean0,
                             dlean_ref=M['lean_scaled_deg'] - REF['lean_scaled_deg'], tail_mass_share=M['tail_mass_share'], dw=M['thorax_d_over_w'], guards=g, ok=all(g.values())))
            print(key, sn, pct, 'base %.3f' % base, {k: round(v, 3) for k, v in n.items()}, 'dlean %.2f / %.2f' % (rows[-1]['dlean_state'], rows[-1]['dlean_ref']), 'OK' if rows[-1]['ok'] else [k for k, v in g.items() if not v], flush=True)
        okp = [r['pct'] for r in rows if r['ok']]; cap = max(okp) if okp else None
        if cap is not None and cap < PCTS[-1]:
            lo = cap; hi = PCTS[PCTS.index(cap) + 1]
            for _ in range(4):
                mid = 0.5 * (lo + hi); base, M, n = solve_base(st, mid, target=tv)
                okm = 0.75 <= n['RSI'] <= 1.20 and n['taper'] <= 1.25 and 0.27 <= n['A50'] <= 0.48 and n['A25'] >= 0.065 and M['lean_scaled_deg'] - lean0 <= 3.0 and M['lean_scaled_deg'] - REF['lean_scaled_deg'] <= 3.0 and M['thorax_d_over_w'] <= 1.0
                lo, hi = (mid, hi) if okm else (lo, mid)
            cap = lo
        binding = [k for k, v in next((r['guards'] for r in rows if not r['ok'] and r['pct'] > (cap or 0)), {}).items() if not v]
        out[key][sn] = dict(params={k: v for k, v in st.items()}, lean_ref_tail=lean0, rows=rows, reachable_cap_pct=cap, binding=binding)
        print('CAP', key, sn, cap, binding, flush=True)
    json.dump(out, open(sys.argv[1], 'w'), indent=1, default=float)
