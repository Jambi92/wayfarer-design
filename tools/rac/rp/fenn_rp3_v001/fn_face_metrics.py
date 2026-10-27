# fn_face_metrics.py : order 2de0e28 -- craniofacial metrics on MPFB hm08 bodies (shared vertex order). Landmarks are FIXED hm08 vertex indices chosen
# once on the accepted FNL4 template (so every body / candidate is read at the same anatomical vertices); regions as the parent hidden-ear gate.
# External ear (w_ears > 0.05) excluded everywhere.
import json, numpy as np
TEMPLATE_NATIVE = '/tmp/claude-0/rt/fn/src/FNL4_native.npz'; TEMPLATE_R6 = '/home/claude/wayfarer-design/reviews/reference-assets/r6/FNL4_r6.npz'
_nz = np.load(TEMPLATE_NATIVE); SI = _nz['src_index']; Q = np.asarray(_nz['Q'])
def load(p):
    z = np.load(p); return dict(V=z['V'][SI].astype(float), we=z['w_ears'][SI], wh=z['w_head'][SI], eye=(np.array(z['eye_l'], float), np.array(z['eye_r'], float)))
_t = load(TEMPLATE_R6); EAR = _t['we'] > 0.05; HEAD = (_t['wh'] > 0.5) & ~EAR; HV = np.nonzero(HEAD)[0]
def _template():
    V = _t['V']; E = 0.5 * (_t['eye'][0] + _t['eye'][1]); P = V - E; h = HV
    def am(mask, key): idx = h[mask[h]]; return int(idx[np.argmax(key(P[idx]))])
    L = {}
    L['vertex'] = am(np.ones(len(V), bool), lambda p: p[:, 2])
    L['menton'] = am((np.abs(P[:, 0]) < 0.8) & (P[:, 1] > 0), lambda p: -p[:, 2])
    L['nasion'] = am((np.abs(P[:, 0]) < 0.35) & (P[:, 2] > -0.5) & (P[:, 2] < 1.5) & (P[:, 1] > 0), lambda p: -p[:, 1])
    L['glabella'] = am((np.abs(P[:, 0]) < 0.35) & (P[:, 2] > 1.0) & (P[:, 2] < 2.6) & (P[:, 1] > 0), lambda p: p[:, 1])
    L['forehead'] = am((np.abs(P[:, 0]) < 0.35) & (P[:, 2] > 4.0) & (P[:, 2] < 5.0) & (P[:, 1] > 0), lambda p: p[:, 1])
    L['cranium_front'] = am((np.abs(P[:, 0]) < 0.35) & (P[:, 2] > 7.5) & (P[:, 2] < 8.5) & (P[:, 1] > -2), lambda p: p[:, 1])
    L['stomion'] = am((np.abs(P[:, 0]) < 0.35) & (P[:, 2] > -7.0) & (P[:, 2] < -5.0) & (P[:, 1] > 0), lambda p: -np.abs(p[:, 2] + 6.0) + 0.3 * p[:, 1])
    for s, sg in (('l', 1), ('r', -1)):
        L['euryon_' + s] = am((sg * P[:, 0] > 0) & (P[:, 2] > 1.0) & (P[:, 2] < 7.0), lambda p: sg * p[:, 0])
        L['zygion_' + s] = am((sg * P[:, 0] > 0) & (P[:, 2] > -3.0) & (P[:, 2] < -0.5) & (P[:, 1] > -3.0), lambda p: sg * p[:, 0])
        L['cheek_apex_' + s] = am((sg * P[:, 0] > 2.5) & (sg * P[:, 0] < 5.5) & (P[:, 2] > -4.0) & (P[:, 2] < -1.0), lambda p: p[:, 1])
        L['gonion_' + s] = am((sg * P[:, 0] > 0) & (P[:, 1] < -3.5) & (P[:, 1] > -7.5) & (P[:, 2] < P[L['menton'], 2] + 4.5) & (P[:, 2] > P[L['menton'], 2] + 1.5), lambda p: sg * p[:, 0] - 0.5 * p[:, 2])
        L['lowerface_' + s] = am((sg * P[:, 0] > 0) & (P[:, 2] > -7.0) & (P[:, 2] < -5.0) & (P[:, 1] > -3.0), lambda p: sg * p[:, 0])
        L['crown_' + s] = am((sg * P[:, 0] > 0) & (P[:, 2] > 8.5) & (P[:, 2] < 9.5), lambda p: sg * p[:, 0])                      # guard: upper-vault breadth (crown roundness)
    orbit = HEAD & ((np.linalg.norm(V - _t['eye'][0], axis=1) < 2.3) | (np.linalg.norm(V - _t['eye'][1], axis=1) < 2.3)) & (P[:, 1] > -1.5)
    fore = HEAD & ~orbit & (P[:, 2] > 1.2) & (P[:, 2] < 6.0) & (P[:, 1] > -2.5) & (np.abs(P[:, 0]) < 5.5)
    nose = HEAD & ~orbit & (np.abs(P[:, 0]) < 1.7) & (P[:, 2] > -5.0) & (P[:, 2] < 0.5) & (P[:, 1] > 0.3)
    cheek = HEAD & ~orbit & ~nose & (np.abs(P[:, 0]) > 1.7) & (np.abs(P[:, 0]) < 6.5) & (P[:, 2] > -5.0) & (P[:, 2] < -1.0) & (P[:, 1] > -3.0)
    mouth = HEAD & (np.abs(P[:, 0]) < 3.0) & (P[:, 2] > -7.5) & (P[:, 2] <= -5.0) & (P[:, 1] > -1.5)
    jaw = HEAD & ~mouth & (P[:, 2] <= -5.0) & (P[:, 1] > -7.0)
    vault = HEAD & ~fore & ~orbit & (P[:, 2] > 1.2)
    R = dict(cranium_vault=vault, forehead=fore, orbit_eye_region=orbit, nose=nose, cheeks_midface=cheek, mouth=mouth, jaw_chin=jaw)
    return L, R
LM, REG = _template()
def descriptors(V):
    g = lambda k: V[LM[k]]; HHt = g('vertex')[2] - g('menton')[2]; w = lambda a: abs(g(a + '_l')[0] - g(a + '_r')[0])
    zy = w('zygion'); eu = w('euryon')
    def turn(a, b, c):
        u = g(b) - g(a); v = g(c) - g(b); u = u[[1, 2]]; v = v[[1, 2]]; return float(np.degrees(np.arccos(np.clip(u @ v / np.linalg.norm(u) / np.linalg.norm(v), -1, 1))))
    cz = 0.5 * (g('cheek_apex_l')[2] + g('cheek_apex_r')[2])
    return dict(cranial_height_over_face=(g('vertex')[2] - g('nasion')[2]) / (g('nasion')[2] - g('menton')[2]), skull_breadth_over_HH=eu / HHt, bizygomatic_over_HH=zy / HHt,
                lower_face_width_over_bizygomatic=w('lowerface') / zy, lower_face_height_over_HH=(g('stomion')[2] - g('menton')[2]) / HHt, jaw_width_over_bizygomatic=w('gonion') / zy,
                cheekbone_height_over_HH=(cz - g('menton')[2]) / HHt, midface_projection_over_HH=(0.5 * (g('cheek_apex_l')[1] + g('cheek_apex_r')[1]) - g('zygion_l')[1]) / HHt,
                forehead_cranium_turn_deg=turn('glabella', 'forehead', 'cranium_front') + turn('nasion', 'glabella', 'forehead'), head_height_cm=HHt,
                crown_breadth_over_euryon=w('crown') / eu)
# canon directions (FENN_V1 §2-7; order 2de0e28 §4): +1 Fenn > Marchfolk, -1 Fenn <, 0 report
CANON = dict(cranial_height_over_face=+1, skull_breadth_over_HH=-1, bizygomatic_over_HH=0, lower_face_width_over_bizygomatic=-1, lower_face_height_over_HH=-1, jaw_width_over_bizygomatic=-1,
             cheekbone_height_over_HH=+1, midface_projection_over_HH=-1, forehead_cranium_turn_deg=-1, head_height_cm=0, crown_breadth_over_euryon=0)
SYSTEMS = {'1 cranium height / shape': ['cranial_height_over_face'], '2 skull breadth / cranial proportion': ['skull_breadth_over_HH'], '3 forehead-to-cranium transition': ['forehead_cranium_turn_deg'],
           '4 cheekbone / mid-face': ['cheekbone_height_over_HH', 'midface_projection_over_HH'], '5 lower-face mass': ['lower_face_width_over_bizygomatic', 'lower_face_height_over_HH'], '6 jaw / chin': ['jaw_width_over_bizygomatic']}
def procrustes(Xs, Xt):
    ms, mt = Xs.mean(0), Xt.mean(0); a, b = Xs - ms, Xt - mt; U, S, Vt = np.linalg.svd(a.T @ b); d = np.sign(np.linalg.det(U @ Vt)); D = np.diag([1, 1, d])
    R = U @ D @ Vt; s = (S * np.diag(D)).sum() / (a * a).sum(); return lambda X: s * (X - ms) @ R + mt
def region_rms(Vfn, Vref):
    f = procrustes(Vref[HEAD], Vfn[HEAD]); X = f(Vref); d = np.linalg.norm(Vfn - X, axis=1) * 10
    return {r: round(float(np.sqrt((d[m] ** 2).mean())), 3) for r, m in REG.items()}, d
