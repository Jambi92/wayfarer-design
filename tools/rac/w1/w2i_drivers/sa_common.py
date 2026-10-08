# RAC W2I Saurin common loader: the frozen SA-M closure mesh (PC-staged saurin_final_base.npz, aff1b52) + the creator-biology tool chain
# (tools/rodin/creator-biology vary / metrics / meas, female/closure tissue / fsets3, gate1 wf_saurin_head63) rebuilt in the scratchpad
# (w2i setup_wc.py; the original /tmp working copies no longer exist). Read-only on the frozen anatomy.
import sys, os, pickle, json, numpy as np
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; W = S + '/w2i/rodin'
for d in ('v1', 'v5', 'rb'): sys.path.insert(0, W + '/' + d)
import vary, metrics, tissue, fsets3
import wf_saurin_head63 as H
z = np.load(vary.REF_BASE); V = z['V'].astype(float); F = z['F'].astype(np.int64)
L = pickle.load(open(W + '/v1/Lbase.pkl', 'rb')); L._u0 = V[:, 2]; L._f0 = V[:, 1]
EYE = (H.eye_centers()[0], H.eye_centers()[1])
def landmarks():
    p = W + '/v1/lm.pkl'
    if not os.path.exists(p): pickle.dump(metrics.landmarks(V, L), open(p, 'wb'))
    return pickle.load(open(p, 'rb'))
LM = landmarks(); REFM = json.load(open(W + '/v1/ref_metrics.json'))
TOR = L.torso > 0.6
I91 = int(np.argmin(np.abs(V[:, 2] - 91) + 100 * (~TOR))); I123 = int(np.argmin(np.abs(V[:, 2] - 123) + 100 * (~TOR)))   # hip-joint level / costal margin (authored stations; female closure sweeps)
def build(q):
    """female-closure tissue warp (= vary.warp + E / B soft tissue when present); q is copied"""
    q = dict(q); P = tissue.fwarp(V, L, q, eye=EYE); return P, q
def measure(P, q):
    M = metrics.measure(P, F, L, q, LM, REFM); M.pop('_A', None); M = {k: float(v) for k, v in M.items() if np.isscalar(v)}
    M['lower_trunk'] = float(P[I123, 2] - P[I91, 2]); M['lower_trunk_over_H'] = M['lower_trunk'] / M['height']
    return M
