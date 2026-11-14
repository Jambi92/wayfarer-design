# sa6_layer_harness.py : creator-state corrective layer harness (corrective-layer validation order 3e76b509 §1-2).
#   Rebuilds the base corrective sets (c1 / c2) and every creator-state set from the PACKAGE ON DISK only (EV6: SA_RP6_correctives_v002.json +
#   SA_RP6_correctives_{M,F}_v001.npz, SA_RP6_creator_layers_v002.json + SA_RP6_creator_layers_v001.npz), and implements the proposed blend:
#
#     production corrective(body, pose) = (1 - sum_i w_i) * B(T) + sum_i w_i * S_i(T)        [ = B(T) + sum_i w_i * (S_i(T) - B(T)) ]
#
#   B   = base corrective set of the body's base configuration (c1 for SA-M states, c2 for F-N), S_i = full corrective set of contributing state i
#   (base keys it inherits + its changed / new keys), w_i = the convex creator weights that produce the body (the base configuration carries 1 - sum w_i).
#   T   = pose transforms of the ACTUAL pose on the BLENDED body's joint frames; every set is evaluated on that same rig (same driver angles, same pose-key
#   weights), each set exactly as authored (its own samples + hat interpolation, its own pose keys), and the rest-space results are blended, then applied
#   before LBS.  Consequences (documented / tested in sa6_layer_validate.py):
#     * base counted exactly once: the weights of B and of the S_i sum to 1;
#     * inherited keys: identical arrays -> (1-w) b + w b = b, no double count;
#     * different sparse vertex supports: each set is accumulated densely over all vertices before blending (a vertex outside one key's support gets 0);
#     * a state's own new family samples / pose keys exist only in S_i -> they enter with weight w_i times their own driver weight;
#     * a changed sample in S_i also changes the hat weights of its family inside S_i only; B keeps its own interpolation (blend of evaluated sets, not
#       of keys);
#     * endpoint identities: w = 0 -> B(T) exactly; one contributor at w = 1 -> S_i(T) exactly (0 * B + 1 * S); neutral (all drivers 0) -> every family
#       hat and every pose-key tent is 0 -> exactly 0 displacement.
#   Layer v003 (sa6_node_fit.py): a state may carry CREATOR KEYS K_n at creator-weight nodes w_n:  S_i(T, w_i) = S_i(T) + sum_n h_n(w_i) K_n(T), h_n = hat over
#   the knots 0, w_1 .. w_k, 1 (zero at both ends), so  production = (1 - sum w_i) B(T) + sum_i w_i S_i(T, w_i).  Endpoint, zero-influence and neutral
#   identities are unchanged (h = 0 at w = 0 and w = 1; K pose-driven).  Which layer file: RP6_LAYERS (default SA_RP6_creator_layers_v002.json).
import os, sys, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sa6_common as C, sa6_correctives as CC
PKG = os.environ.get('RP6_PKG', C.EV6)
_cache = {}
def _npz(name):
    if name not in _cache: _cache[name] = np.load(os.path.join(PKG, name))
    return _cache[name]
def _js(name):
    if name not in _cache: _cache[name] = json.load(open(os.path.join(PKG, name)))
    return _cache[name]
def _set(rig, fams, pks, arr_of):
    c = CC.Correctives(rig)
    for f in fams:
        key = CC.fam_key(f['bone'], f['axis_parent_frame'])
        c.F[key] = dict(bone=f['bone'], axis=f['axis_parent_frame'], pivot=f['pivot_rest_cm'], samples=[k['sample_deg'] for k in f['keys']], D=[arr_of(k) for k in f['keys']])
    for p in pks:
        idx, d = arr_of(p); c.PK[p['pose']] = dict(drivers=[(x['bone'], x['axis_parent_frame'], x['sample_deg']) for x in p['drivers']], idx=idx, d=d, name=p.get('name', p['pose']))
    return c
def load_base(rig, cfg):
    j = _js('SA_RP6_correctives_v002.json')['configurations'][cfg]; z = _npz(_js('SA_RP6_correctives_v002.json')['arrays'][cfg])
    return _set(rig, j['families'], j['pose_keys'], lambda k: (z[k['name'] + '_idx'].astype(np.int64), z[k['name'] + '_d'].astype(np.float64)))
LAYERS = os.environ.get('RP6_LAYERS', 'SA_RP6_creator_layers_v002.json')
def hats(knots, w):
    """piecewise-linear hats over 0 < knots < 1 (implicit zero knots at 0 and 1): weight of every node at creator weight w"""
    xs = [0.0] + list(knots) + [1.0]; out = [0.0] * len(knots)
    for j in range(len(xs) - 1):
        if xs[j] <= w <= xs[j + 1]:
            t = (w - xs[j]) / (xs[j + 1] - xs[j])
            if 1 <= j <= len(knots): out[j - 1] = 1 - t
            if j + 1 <= len(knots): out[j] = t
            break
    return out
class StateLayer:
    """a creator-state corrective set S (unit influence) + optional creator keys [(w_n, K_n)]"""
    def __init__(self, S, keys=()): self.S = S; self.keys = sorted(keys, key=lambda x: x[0]); self.F = S.F; self.PK = S.PK; self.r = S.r
    def delta(self, T): return self.S.delta(T)
    def delta_w(self, T, w):
        d = self.S.delta(T)
        for (n, K), h in zip(self.keys, hats([k[0] for k in self.keys], w)):
            if h: d = d + h * K.delta(T)
        return d
def load_state(rig, nm):
    L = _js(LAYERS); s = L['states'][nm]; cfg = s['base_config']
    zb = _npz(_js('SA_RP6_correctives_v002.json')['arrays'][cfg]); zl = _npz(L['arrays'])
    def arr(k):
        if k['source'] == 'base': return zb[k['base_key'] + '_idx'].astype(np.int64), zb[k['base_key'] + '_d'].astype(np.float64)
        return zl[k['array'] + '_idx'].astype(np.int64), zl[k['array'] + '_d'].astype(np.float64)
    ck = [(k['node_weight'], _set(rig, k['families'], k['pose_keys'], arr)) for k in s.get('creator_keys', [])]
    return StateLayer(_set(rig, s['families'], s['pose_keys'], arr), ck), cfg
def state_cfg(nm): return _js(LAYERS)['states'][nm]['base_config']
class Blend:
    """production corrective of a creator body: base set B + convex blend of contributing state sets (see module header)"""
    def __init__(self, base, contribs):
        self.B = base; self.S = [(float(w), s) for w, s in contribs if w != 0]; self.wb = 1.0 - sum(w for w, _ in self.S)
        assert self.wb >= -1e-12 and all(w > 0 for w, _ in self.S), 'convex weights only'
    def delta(self, T):
        d = self.B.delta(T) * self.wb if self.wb != 0 else np.zeros_like(self.B.r.V)
        for w, s in self.S: d = d + w * (s.delta_w(T, w) if hasattr(s, 'delta_w') else s.delta(T))
        return d
