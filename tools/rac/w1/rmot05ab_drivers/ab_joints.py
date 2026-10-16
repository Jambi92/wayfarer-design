# RM-OT-05AB: estimate donor-C joint centres from read-only section loops (review frame: X right, Y back, Z up, raw cm, uncentred),
# and derive the macro targets from the accepted W1 ARM (GO_r6 joint record). Nothing is written to any mesh.
# Limb joints: elbow = arm-perimeter minimum between upper-arm and forearm maxima; wrist = arm-perimeter minimum above the hand flare;
# knee = leg-perimeter minimum between thigh and calf; ankle = shin loop centre above the malleoli projected to ankle height;
# hip = thigh-axis line (knee -> mid-thigh) extended to crotch + 4.0 % H (the W1 hip-above-crotch share); shoulder = deltoid-cap top
# = 0.04 H medial to the most lateral deltoid point (0.76-0.86 H), at that height.
# Usage: python3 ab_joints.py FIG0.npz GO_r6.npz MACRO_AA0.json OUT.json
import sys, json, numpy as np, trimesh
fig, gor6, macro, out = sys.argv[1:5]
d = np.load(fig); P = d['V'].astype(float); V = np.stack([P[:, 0], -P[:, 2], P[:, 1]], 1) * 100; F = d['F']
m = trimesh.Trimesh(V, F, process=False); H = float(V[:, 2].max())
def loops(z):
    s = m.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1]); R = []
    for e in (s.discrete if s is not None else []):
        R.append(dict(c=e.mean(0), per=float(np.linalg.norm(np.diff(e, axis=0), axis=1).sum()), xmin=e[:, 0].min(), xmax=e[:, 0].max()))
    return R
# trunk midline x (0.55 H trunk loop) and body-relative side test
tr = max(loops(0.55 * H), key=lambda l: l['per']); cx = float(tr['c'][0]); cy = float(tr['c'][1])
M = json.load(open(macro)); crotch = M['C_513bc9e2']['crotch_pct'] / 100 * H; tip = M['C_513bc9e2']['fingertip_pct'] / 100 * H
J = dict(H=round(H, 2), midline_x=round(cx, 2), midline_y=round(cy, 2), crotch_z=round(crotch, 2), fingertip_z=round(tip, 2))
def track(side, z0, z1, pick):
    zs = np.arange(z0, z1, 0.25); rows = []
    for z in zs:
        L = [l for l in loops(z) if pick(l, side)]
        if L: l = max(L, key=lambda l: l['per']); rows.append((z, l['per'], l['c']))
    return rows
arm = lambda l, s: s * (l['c'][0] - cx) > 0.14 * H and abs(l['c'][1] - cy) < 0.10 * H and not (l['xmin'] < cx < l['xmax'])
leg = lambda l, s: 0.02 * H < s * (l['c'][0] - cx) < 0.14 * H and abs(l['c'][1] - cy) < 0.08 * H and not (l['xmin'] < cx - 0.5 < l['xmax'] and l['xmin'] < cx + 0.5 < l['xmax'])
for s, nm in ((1, 'L'), (-1, 'R')):                      # L = +X side of the review frame
    A = track(s, 0.46 * H, 0.655 * H, arm); z = np.array([r[0] for r in A]); p = np.array([r[1] for r in A]); C = np.array([r[2] for r in A])
    # wrist: min perimeter in 0.46-0.54 H; forearm max in 0.53-0.60 H; elbow: min in [forearm max, 0.655 H]
    w = (z < 0.54 * H); iw = np.where(w)[0][np.argmin(p[w])]
    fm = (z > 0.53 * H) & (z < 0.60 * H); ifm = np.where(fm)[0][np.argmax(p[fm])]
    el = (z > z[ifm]) & (z < 0.655 * H); ie = np.where(el)[0][np.argmin(p[el])]
    J['wrist_' + nm] = np.round(C[iw], 2).tolist(); J['elbow_' + nm] = np.round(C[ie], 2).tolist(); J['forearm_max_z_' + nm] = round(float(z[ifm]), 2)
    # shoulder joint: deltoid-cap top minus W1 cap->joint drop (4.7 cm at 230.9) scaled; x/y from the cap, 2 cm medial
    # deltoid: most lateral shoulder point between 0.76 and 0.86 H; glenohumeral centre taken 0.04 H medial to it at that height
    sel = V[(V[:, 2] > 0.76 * H) & (V[:, 2] < 0.86 * H) & (s * (V[:, 0] - cx) > 0)]; lat = sel[np.argmax(s * (sel[:, 0] - cx))]
    J['deltoid_lateral_' + nm] = np.round(lat, 2).tolist()
    J['shoulder_' + nm] = np.round([lat[0] - s * 0.04 * H, lat[1], lat[2]], 2).tolist()
    Lg = track(s, 0.03 * H, 0.42 * H, leg); z = np.array([r[0] for r in Lg]); p = np.array([r[1] for r in Lg]); C = np.array([r[2] for r in Lg])
    kn = (z > 0.22 * H) & (z < 0.33 * H); ik = np.where(kn)[0][np.argmin(p[kn])]
    an = (z > 0.06 * H) & (z < 0.14 * H); ia = np.where(an)[0][np.argmin(p[an])]
    knee = C[ik]; J['knee_' + nm] = np.round(knee, 2).tolist()
    ankle_z = 0.048 * H; J['ankle_' + nm] = np.round([C[ia][0], C[ia][1], ankle_z], 2).tolist()
    it = np.argmin(abs(z - 0.38 * H)); thigh = C[it]; hip_z = crotch + 0.040 * H; t = (hip_z - knee[2]) / (thigh[2] - knee[2])
    J['hip_' + nm] = np.round(knee + t * (thigh - knee), 2).tolist()
    toe = V[(s * (V[:, 0] - cx) > 0) & (V[:, 2] < 0.04 * H)]; J['toe_' + nm] = np.round([knee[0], toe[:, 1].min(), 2.0], 2).tolist()
    hand = V[(s * (V[:, 0] - cx) > 0.15 * H) & (V[:, 2] < J['wrist_' + nm][2]) & (V[:, 2] > 0.30 * H)]; J['fingertip_' + nm] = np.round(hand[np.argmin(hand[:, 2])], 2).tolist()
# W1 ARM joint shares (GO_r6 joint record, % of surface height 230.9)
g = np.load(gor6, allow_pickle=True); j = json.loads(str(g['joints'])); HG = 230.89719
W = dict(shoulder=j['upperarm_l'][0][2], elbow=j['lowerarm_l'][0][2], wrist=j['hand_l'][0][2], hip=j['thigh_l'][0][2], knee=j['calf_l'][0][2], ankle=j['foot_l'][0][2])
J['W1_joint_share_pct'] = {k: round(100 * v / HG, 2) for k, v in W.items()}
json.dump(J, open(out, 'w'), indent=1); print(json.dumps(J, indent=1))
