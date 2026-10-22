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
c = pi + axv * (0.001 + 0.0003)
fx = dict(c=(c * 100).tolist(), ax=axv.tolist(), r=1.1, hl=0.1, pad_gap_mm=float(d[k] * 1000))
print(json.dumps(fx)); json.dump(fx, open(outf, 'w'), indent=1)
