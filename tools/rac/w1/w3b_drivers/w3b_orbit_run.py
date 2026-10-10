# RAC W3B RM-UF-03 spacing sweep: integrated orbital-platform lateral shift dx (head-local cm per side; world = dx * 1.08) on the canonical
# W2 base (copies), optionally on top of a head-corner warp (creator-biology vary.warp step 3: cran_w, orbit, ros_len (+ accepted depth /
# jaw coupling), combined). Order of operations: spacing on the canonical skull (level-set transfer), then the head-corner warp.
# Outputs per case: base-resolution vertex array (npy), metrics (IOD family + quality + regional strain), head npz for rendering.
# Usage: python3 w3b_orbit_run.py SET   (sweep | fine | corners | render)
import os, sys, json, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import w3b_common as C, w3b_orbit as O
W = C.W + '/orbit'; os.makedirs(W, exist_ok=True)
sys.path.insert(0, C.S + '/w2i/rodin/v1'); sys.path.insert(0, C.S + '/w2i/rodin/v5'); sys.path.insert(0, C.S + '/w2i/rodin/rb')
def corner_params(c):
    return {"ref": {}, "cw-8": {"cran_w": 0.92}, "cw+8": {"cran_w": 1.08}, "or-8": {"orbit": 0.92}, "or+8": {"orbit": 1.08},
            "ros-15": {"ros_len": 0.85}, "ros+20": {"ros_len": 1.20, "ros_d": 1.08, "jaw_d": 1.08},
            "comb-in": {"cran_w": 0.92, "orbit": 1.08, "ros_len": 0.85}, "comb-out": {"cran_w": 0.92, "orbit": 1.08, "ros_len": 1.20, "ros_d": 1.08, "jaw_d": 1.08}}[c]
_L = None
def labels():
    global _L
    if _L is None:
        import pickle; _L = pickle.load(open(C.S + '/w2i/rodin/v1/Lbase.pkl', 'rb'))
        _L.N = __import__('igl').per_vertex_normals(C.V0, C.F0); _L._u0 = C.V0[:, 2]; _L._f0 = C.V0[:, 1]
    return _L
def head_warp(P, p, dx=0.0):
    if not p: return P
    import vary
    eye = ([(s * (C.EYE0['x'] + dx), C.EYE0['f'], C.EYE0['u']) for s in (1, -1)], C.EYE0['r'], C.EYE0['yaw'])     # head-local (vary convention), carried with the spacing shift
    L = labels(); L.N = __import__('igl').per_vertex_normals(P, C.F0)
    return vary.warp(P, L, dict(p), eye=eye)
def build(dx, corner='ref'):
    tag = 'dx%+.2f_%s' % (dx, corner); f = W + '/%s.npy' % tag
    if os.path.exists(f): return tag, np.load(f).astype(float)
    P = C.V0.copy() if dx == 0 else C.level_set_transfer(lambda Q: C.sdf(Q, eye_dx=dx), pre=lambda Q: C.orbit_shift_points(Q, dx))
    P = head_warp(P, corner_params(corner), dx); np.save(f, P.astype(np.float32)); return tag, P
def regional_strain(P, Pref):
    """edge-length ratio percentiles in named head regions (canonical vertex sets): interorbital / canthal, brow / supraorbital,
    postorbital / temporal support, rostral base"""
    Lh = C.L0; Xa = np.abs(Lh[:, 0]); f = Lh[:, 1]; u = Lh[:, 2]
    reg = {"interorbital_canthal": (Xa < 2.2) & (f > 4) & (f < 10) & (u > 3) & C.HEADM,
           "brow_supraorbital": (Xa > 1.5) & (Xa < 5.5) & (f > 1) & (f < 9) & (u > 5) & C.HEADM,
           "postorbital_temporal": (Xa > 4.0) & (f > -3) & (f < 5) & (u > 1.5) & (u < 7) & C.HEADM,
           "rostral_base": (f > 8) & (f < 12) & (u > -1) & C.HEADM}
    E = np.vstack([C.F0[:, [0, 1]], C.F0[:, [1, 2]], C.F0[:, [2, 0]]]); out = {}
    la = np.linalg.norm(P[E[:, 0]] - P[E[:, 1]], axis=1); lr = np.linalg.norm(Pref[E[:, 0]] - Pref[E[:, 1]], axis=1); r = la / np.maximum(lr, 1e-12)
    for k, m in reg.items():
        e = m[E[:, 0]] & m[E[:, 1]]; out[k] = np.percentile(r[e], [0.5, 50, 99.5]).round(3).tolist()
    return out
def run(cases):
    res = json.load(open(W + '/results.json')) if os.path.exists(W + '/results.json') else {}
    for dx, corner in cases:
        tag, P = build(dx, corner)
        if tag in res: continue
        _, Pc = build(0.0, corner)
        M, rings = O.measure(P); q = C.quality(P, C.F0, Pc)
        M.update(dx_local=dx, dx_world=dx * C.HS, corner=corner, quality=q, strain=regional_strain(P, Pc))
        res[tag] = M; json.dump(res, open(W + '/results.json', 'w'), indent=1)
        print(tag, 'IOD %.3f IOD/cran %.3f med %.2f latsup %.3f flips %d strain %s' % (M['IOD'], M['IOD_over_cranial'], M['medial_margin_sep'], M['lateral_support_min'], q['flipped'], q['strain_pct']), flush=True)
if __name__ == '__main__':
    st = sys.argv[1]
    if st == 'sweep': run([(dx, 'ref') for dx in (0.0, -0.2, -0.4, -0.6, -0.8, -1.0, -1.2, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2)])
    if st == 'corners':
        dxs = [float(x) for x in sys.argv[2].split(',')]
        run([(dx, c) for c in ('cw-8', 'cw+8', 'or-8', 'or+8', 'ros-15', 'ros+20', 'comb-in', 'comb-out') for dx in [0.0] + dxs])
    if st == 'cases': run([(float(a.split('@')[0]), a.split('@')[1]) for a in sys.argv[2].split(',')])
