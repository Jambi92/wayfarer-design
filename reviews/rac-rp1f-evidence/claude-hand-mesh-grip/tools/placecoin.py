# placecoin.py (bpy python) -- RIGDIR SIDE ANGLES.json OUT.json : coin fixture (22 mm x 2 mm) against the index pad, facing the thumb pad
import sys, json, numpy as np, os, pickle
sys.path.insert(0, '/tmp/claude-0/hand/tools'); import bpy; from fastpose import Hand
a = sys.argv[sys.argv.index('--') + 1:]; rd, side, aj, outf = a
H = Hand(rd, side); RD = pickle.load(open(os.path.join(rd, 'rig_data.pkl'), 'rb'))[side]; own = RD['own']; ker = RD['ker']
ang = json.load(open(aj)); P = H.pose(ang)
ix = 3 if side == 'L' else 0; th = 4
W = H.W.toarray(); nm = H.names
idist = W[:, nm.index(('A_L20' if side == 'L' else 'A_R21') + '_2')]; tdist = W[:, nm.index('A_%sthumb_2' % side)]
iv = np.where((own == ix) & ~ker & (idist > 0.95))[0]; tv = np.where((own == th) & ~ker & (tdist > 0.95))[0]
from scipy.spatial import cKDTree
d, j = cKDTree(P[tv]).query(P[iv]); k = int(np.argmin(d)); pi = P[iv[k]]; pt = P[tv[j[k]]]
axv = (pt - pi) / np.linalg.norm(pt - pi)
mode = os.environ.get('COINMODE', 'mid')
c = (pi + pt) / 2 if mode == 'mid' else (pt - axv * 0.0013 if mode == 'thumb' else pi + axv * (0.001 + 0.0003))
fx = dict(c=(c * 100).tolist(), ax=axv.tolist(), r=1.1, hl=0.1, pad_gap_mm=float(d[k] * 1000))
dd = P - c; tt = dd @ axv; rad = np.linalg.norm(dd - tt[:, None] * axv, axis=1); dr = rad - 0.011; dt = np.abs(tt) - 0.001
sdv = np.sqrt(np.maximum(dr, 0) ** 2 + np.maximum(dt, 0) ** 2) + np.minimum(np.maximum(dr, dt), 0); fx['min_clear_mm'] = float(sdv.min() * 1000); fx['closest_owner'] = int(own[np.argmin(sdv)])
print(json.dumps(fx)); json.dump(fx, open(outf, 'w'), indent=1)
