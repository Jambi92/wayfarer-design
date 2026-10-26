# joint_centring.py NATIVE.npz OUT.json : RP3 joint-placement plausibility (order d18ff2a §12 / §13 'joint placement' class).
# For each hinge / ball joint: offset of the source-rig joint centre from the centroid of the limb cross-section through it (vertices weighted
# >= 0.25 to the parent or child bone, within +-0.6 cm of the plane normal to the parent bone), as a fraction of the section radius.
import sys, json, numpy as np
z = np.load(sys.argv[1]); V = z['V']; W = z['W']; bn = list(z['bones']); m = json.loads(str(z['meta'])); H = {k: np.array(v) for k, v in m['heads'].items()}; T = {k: np.array(v) for k, v in m['tails'].items()}
R = {}
for s in ('l', 'r'):
    for j, b, pb in (('elbow', 'lowerarm', 'upperarm'), ('knee', 'calf', 'thigh'), ('wrist', 'hand', 'lowerarm'), ('ankle', 'foot', 'calf')):
        b, pb = b + '_' + s, pb + '_' + s; p = H[b]; d = T[pb] - H[pb]; d /= np.linalg.norm(d); P = V - p; t = P @ d
        w = W[:, bn.index(b)] + W[:, bn.index(pb)]; sel = (np.abs(t) < 0.6) & (w >= 0.25)
        rad = P[sel] - np.outer(t[sel], d); cen = rad.mean(0); r = np.linalg.norm(rad - cen, axis=1).mean()
        R['%s_%s' % (j, s)] = dict(offset_cm=round(float(np.linalg.norm(cen)), 3), section_radius_cm=round(float(r), 3), offset_frac=round(float(np.linalg.norm(cen) / r), 3), n=int(sel.sum()),
                                   offset_vec_cm=np.round(cen, 3).tolist(), flag=bool(np.linalg.norm(cen) / r > 0.35))
json.dump(R, open(sys.argv[2], 'w'), indent=1); print({k: (v['offset_cm'], v['offset_frac'], v['n']) for k, v in R.items()})
