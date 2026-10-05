"""RAC W1: Part 7 rostral-index convention (corneal-surface proxy points) on the same corners, for convention mapping."""
import sys, json, pickle, numpy as np
sys.path.insert(0, '/tmp/claude-0/rodin/v1'); sys.path.insert(0, '/tmp/claude-0/rb')
import vary, metrics, wf_saurin_head63 as H
z = np.load(vary.REF_BASE); V = z['V'].astype(float); F = z['F'].astype(np.int64)
L = pickle.load(open('/tmp/claude-0/rodin/v1/Lbase.pkl', 'rb')); L._u0 = V[:, 2]; L._f0 = V[:, 1]
lm = pickle.load(open('/tmp/claude-0/rodin/v1/lm.pkl', 'rb')); ref = json.load(open('/tmp/claude-0/rodin/v1/ref_metrics.json'))
eye = (H.eye_centers()[0], H.eye_centers()[1]); out = {}
for jid, q in (('ref', {}), ('rostrum_min_-15', {'ros_len': 0.85}), ('cranium_long_+8', {'cran_len': 1.08}),
               ('corner_rostrum_min_x_cranium_long', {'ros_len': 0.85, 'cran_len': 1.08}), ('rostrum_max_+20', {'ros_len': 1.20})):
    qq = dict(q); P = vary.warp(V, L, qq, eye=eye); M = metrics.measure(P, F, L, qq, lm, ref)
    out[jid] = dict(rostral_index_part7=float(M['rostral_index']), head_len=float(M['head_len']), rostral_proj=float(M['rostral_proj']))
    print(jid, {k: round(v, 4) for k, v in out[jid].items()})
json.dump(out, open(sys.argv[1], 'w'), indent=1)
