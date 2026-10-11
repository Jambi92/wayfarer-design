# RAC W3D: Saurin r3 FPI on the CANONICAL W2 reference (W1 used aff1b52) - reference, rostrum -15 %, and the Part 7 coupled minimum corner
# (ros_len 0.8847473 at cran_len 1.08, the W1 D-1 corner), with head-pitch +-3 deg about the eye midpoint. Same r3 definition as
# saurin_w1.fpi(): FAL = anterior-most midline head vertex (|x| < 1, head weight > 0.95); Op = posterior-most head vertex above u 176;
# OC = eye centres carried by the mean displacement of the 200 nearest reference vertices. Writes w3d/saurin_fpi.json and corner npy.
import os, sys, json, numpy as np
from scipy.spatial import cKDTree
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import w3b_common as C, w3b_orbit_run as OR
S = C.S; os.makedirs(S + '/w3d', exist_ok=True)
L = OR.labels(); V = C.V0
E = np.array([C.head_world(np.array([s * C.EYE0['x'], C.EYE0['f'], C.EYE0['u']])) for s in (1, -1)])
def fpi(P, pitch=0.0):
    hd = L.head > 0.95; x_, f_, u_ = P.T; tr = cKDTree(V); OC = []
    for c in E: _, k = tr.query(c, k=200); OC.append(c + (P[k] - V[k]).mean(0))
    oc = np.mean(OC, 0); a = np.radians(pitch); ca, sa = np.cos(a), np.sin(a); rel = P - oc
    f2 = oc[1] + ca * rel[:, 1] - sa * rel[:, 2]
    mid = hd & (np.abs(x_) < 1.0); i_fal = np.where(mid)[0][np.argmax(f2[mid])]; post = hd & (u_ > 176); i_op = np.where(post)[0][np.argmin(f2[post])]
    top = np.sort(f2[mid])[-20:]; HL = f2[i_fal] - f2[i_op]; proj = f2[i_fal] - oc[1]
    return dict(HL_cm=float(HL), proj_cm=float(proj), FPI=float(proj / HL), FAL_top20_spread_cm=float(top.max() - top.min()), part7_from_conversion=float(proj / HL - 1.194 / HL))
CASES = {'W2_reference': {}, 'W2_rostrum-15': {'ros_len': 0.85}, 'W2_coupled_min_corner': {'ros_len': 0.8847473, 'cran_len': 1.08}}
out = {}
for nm, p in CASES.items():
    P = OR.head_warp(V.copy(), p) if p else V.copy(); np.save(S + '/w3d/%s.npy' % nm, P.astype(np.float32))
    r = {('pitch%+d' % a): fpi(P, a) for a in (0, -3, 3)}; r['params'] = p; out[nm] = r
    print(nm, 'FPI %.5f (pitch -3 %.5f / +3 %.5f) HL %.3f spread %.3f part7(conv) %.5f' % (r['pitch+0']['FPI'], r['pitch-3']['FPI'], r['pitch+3']['FPI'], r['pitch+0']['HL_cm'], r['pitch+0']['FAL_top20_spread_cm'], r['pitch+0']['part7_from_conversion']), flush=True)
json.dump(out, open(S + '/w3d/saurin_fpi.json', 'w'), indent=1)
