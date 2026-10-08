# RAC W2I §23.1: reproduce SA-M (frozen closure reference) and SA-F (§263 female centre) on the rebuilt tool chain against the frozen Part 7
# reference metrics (ref_metrics.json) and the accepted W1 ARM values. Usage: python3 sa_repro.py OUT.json
import sys, json, hashlib, numpy as np
sys.path.insert(0, __import__('os').path.dirname(__file__)); import sa_common as C
R = {"pc_sha256": hashlib.sha256(open('/mnt/attach/outputs/racebodies_v35/saurin_final_base.npz', 'rb').read()).hexdigest()}
P, q = C.build({}); M = C.measure(P, q); R['SA-M'] = M
R['SA-M_vs_ref_metrics'] = {k: [M[k], C.REFM[k], 100 * (M[k] / C.REFM[k] - 1) if C.REFM[k] else None] for k in C.REFM if k in M}
Pf, qf = C.build(C.fsets3.CEN); R['SA-F'] = C.measure(Pf, qf)
Pr, qr = C.build(C.fsets3.REF); R['SA-F-REF10'] = C.measure(Pr, qr)
R['W1_ARM'] = {"SA-M": {"height": 187.880, "lower_trunk": 32.0, "pelvis_w": 41.7, "thorax_d_over_w": 0.880, "tail_len_pct": 64.61},
               "SA-F": {"height": 187.881, "lower_trunk": 33.640, "pelvis_w": 43.055, "thorax_d_over_w": 0.9217, "head_len_ratio": 0.1698, "tail_len_pct": 64.66}}
json.dump(R, open(sys.argv[1], 'w'), indent=1)
for k, v in R['SA-M_vs_ref_metrics'].items(): print('%-22s %10.4f %10.4f %+.3f%%' % (k, v[0], v[1], v[2] if v[2] is not None else 0))
for b in ('SA-M', 'SA-F', 'SA-F-REF10'): print(b, {k: round(R[b][k], 4) for k in ('height', 'lower_trunk', 'pelvis_w', 'thorax_d_over_w', 'head_len_ratio', 'tail_len_pct')})
