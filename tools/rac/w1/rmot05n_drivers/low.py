# RM-OT-05N GO-RD-LOW: manual low-composition companion of the final reference. Soft-tissue masses are reduced region by region
# (named, hand-placed, mirrored); bony landmarks / joint scale (knee, ankle, elbow, wrist, girdle points, pelvis frame) are left
# untouched. No uniform shrink, no Marchfolk deltas.  Usage: low.py REF_FIELD.npz OUTPREFIX low.json
import sys, json, numpy as np
sys.path.insert(0, D := '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/rd'); from field import *
d = np.load(sys.argv[1]); S = d['S'].astype(float); lo = d['lo']; h = float(d['h']); P = json.load(open(sys.argv[3])); xs, ys, zs = coords(S.shape, lo, h)
X3, Y3, Z3 = np.meshgrid(xs, ys, zs, indexing='ij'); log = []
for name, c, r, amt, mirror in P['tissue']:
    for sx in ((1, -1) if mirror else (1,)):
        q = np.sqrt(((X3 - c[0] * sx) / r[0]) ** 2 + ((Y3 - c[1]) / r[1]) ** 2 + ((Z3 - c[2]) / r[2]) ** 2)
        w = np.clip(1 - q, 0, 1); S += amt * w * w * (3 - 2 * w)
    log.append('%s -%.1f cm' % (name, amt))
for name, c, r in P['protect']:   # report only: confirm joints untouched (weights computed for the record)
    log.append('protected %s' % name)
np.savez_compressed(sys.argv[2] + '.npz', S=S.astype(np.float32), lo=lo, h=h)
m = mesh(S, lo, h, sys.argv[2] + '_raw.obj'); print(m.bounds.round(1), m.is_watertight)
json.dump(dict(params=P, log=log), open(sys.argv[2] + '_log.json', 'w'), indent=1)
