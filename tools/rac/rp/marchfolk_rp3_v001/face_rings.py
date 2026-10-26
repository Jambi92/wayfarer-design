# face_rings.py CAND.npz LOOPS.npz LANDMARKS.json OUT.json : RP3 face readiness (order d18ff2a §9) -- concentric closed edge loops around the mouth,
# centred on the lip-slit centre (midpoint of the surface-fit mouth corners, x = 0), axis = forward. The audit's first pass centred the mouth test on
# the MPFB 'mouth' joint cube, which sits at nose height (~4 cm above the slit) and therefore found 0 rings; this replaces that number.
# Also: orbit rings (eye helper centre), poles inside the perioral / orbital regions, and the lip-slit / eye-socket openings (inner pocket present).
import sys, json, numpy as np
a = sys.argv[1:]; cz = np.load(a[0]); lz = np.load(a[1], allow_pickle=True); LM = json.load(open(a[2]))['landmarks']; OUT = a[3]
V = cz['V'].astype(float); loops = lz['loops']; poles = lz['poles']
def encircling(c, d, rmax, win):
    d = d / np.linalg.norm(d); out = []
    u = np.cross(d, [0, 0, 1.0]); u /= np.linalg.norm(u); vv = np.cross(d, u)
    for li, L in enumerate(loops):
        P = V[L] - c; t = P @ d; rad = P - np.outer(t, d); rr = np.linalg.norm(rad, axis=1)
        if rr.max() > rmax or abs(t.mean()) > win or rr.min() < 1e-6: continue
        th = np.arctan2(rad @ vv, rad @ u); dth = np.diff(np.r_[th, th[0]]); dth = (dth + np.pi) % (2 * np.pi) - np.pi
        if abs(abs(dth.sum()) - 2 * np.pi) < 0.5: out.append(dict(loop=int(li), n=int(len(L)), mean_radius_cm=round(float(rr.mean()), 2), min_radius_cm=round(float(rr.min()), 2), depth_cm=round(float(t.mean()), 2)))
    return sorted(out, key=lambda x: x['mean_radius_cm'])
ml, mr = np.array(LM['mouth_corner_l']['p_cm']), np.array(LM['mouth_corner_r']['p_cm']); mc = 0.5 * (ml + mr); mc[0] = 0.0
R = dict(mouth_centre_cm=np.round(mc, 3).tolist(), mouth_width_cm=round(float(np.linalg.norm(ml - mr)), 3))
mo = encircling(mc, np.array([0, 1.0, 0]), 5.5, 3.5)
R['mouth_rings'] = dict(count=len(mo), rings=mo, note='closed loops encircling the lip-slit centre about the forward axis, within 5.5 cm radius')
R['mouth_rings_concentric_count'] = len({round(x['mean_radius_cm'], 1) for x in mo})
for s in ('l', 'r'):
    ec = np.array(LM['eye_' + s]['p_cm']); eo = encircling(ec, np.array([0, 1.0, 0]), 3.2, 3.0); R['orbit_rings_' + s] = dict(count=len(eo), radii_cm=[x['mean_radius_cm'] for x in eo], loops=[x['loop'] for x in eo])
    pp = V[poles]; R['poles_within_2cm_of_eye_' + s] = int((np.linalg.norm(pp - ec, axis=1) < 2.0).sum())
pp = V[poles]; dm = np.linalg.norm((pp - mc) * [1, 0.6, 1], axis=1); R['poles_within_2cm_of_mouth'] = int((dm < 2.0).sum())
R['poles_at_mouth_corners'] = int(min(np.linalg.norm(pp - ml, axis=1).min(), np.linalg.norm(pp - mr, axis=1).min()) < 0.3)
R['criterion'] = 'contract §9 asks for ring loops around mouth and orbit (no count); >= 3 concentric closed rings used here'
R['mouth_pass'] = bool(R['mouth_rings']['count'] >= 3); R['orbit_pass'] = bool(min(R['orbit_rings_l']['count'], R['orbit_rings_r']['count']) >= 3)
json.dump(R, open(OUT, 'w'), indent=1); print(json.dumps({k: v for k, v in R.items() if k != 'mouth_rings'}), 'mouth rings', R['mouth_rings']['count'], [x['mean_radius_cm'] for x in mo])
