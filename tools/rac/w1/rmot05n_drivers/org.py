# RM-OT-05N full organism: final reference field + the source leonine mane over the nape (as generated) + the source tail study
# (Rodin part p4) placed at the sacral root. Head is the source head throughout. Usage: org.py REF_FIELD.npz OUTPREFIX params.json
import sys, json, numpy as np, trimesh, igl
sys.path.insert(0, D := '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/rd'); from field import *
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/rmot05l_drivers'); from l_clay import smin
d = np.load(sys.argv[1]); S = d['S'].astype(float); lo = d['lo']; h = float(d['h']); P = json.load(open(sys.argv[3])); xs, ys, zs = coords(S.shape, lo, h)
s0 = np.load(D + '/S0.npz'); S0 = s0['S']; assert np.allclose(s0['lo'], lo) and S0.shape == S.shape
pad = int(round(P['pad_y'] / h))                       # room behind the body for the tail
S = np.pad(S, ((0, 0), (pad, 0), (0, 0)), constant_values=60.0); S0 = np.pad(S0, ((0, 0), (pad, 0), (0, 0)), constant_values=60.0)
lo = lo.copy(); lo[1] -= pad * h; xs, ys, zs = coords(S.shape, lo, h)
X3, Y3, Z3 = np.meshgrid(xs, ys, zs, indexing='ij')
m = P['mane']; yc = m['y'] + (Z3 - m['z0']) * m['slope']
manemask = (Z3 > m['z0']) & (Z3 < m['z1']) & (Y3 < yc + m['dy']) & (np.abs(X3) < m['x'])
S = np.where(manemask, np.minimum(S, S0), S)
# tail
t = P['tail']; tm = trimesh.load(D + '/../n/p4.obj', process=False); V = np.asarray(tm.vertices, float); s = t['scale']; r = np.array(t['root_raw'])
W = np.c_[-(V[:, 1] - r[1]) * s, (V[:, 0] - r[0]) * s, (V[:, 2] - r[2]) * s]
th = np.radians(-t['tilt_deg']); c_, s_ = np.cos(th), np.sin(th); W = np.c_[W[:, 0], W[:, 1] * c_ - W[:, 2] * s_, W[:, 1] * s_ + W[:, 2] * c_] 
ps = np.radians(t['yaw_deg']); W = np.c_[W[:, 0] * np.cos(ps) - W[:, 1] * np.sin(ps), W[:, 0] * np.sin(ps) + W[:, 1] * np.cos(ps), W[:, 2]] + t['attach']
lo_t, hi_t = W.min(0) - 2, W.max(0) + 2; i0 = np.floor((lo_t - lo) / h).astype(int); i1 = np.ceil((hi_t - lo) / h).astype(int)
Q = np.stack(np.meshgrid(xs[i0[0]:i1[0]], ys[i0[1]:i1[1]], zs[i0[2]:i1[2]], indexing='ij'), -1)
wn = igl.fast_winding_number(np.ascontiguousarray(W), np.ascontiguousarray(tm.faces, np.int64), Q.reshape(-1, 3)).reshape(Q.shape[:3])
OT = np.zeros(S.shape, bool); OT[i0[0]:i1[0], i0[1]:i1[1], i0[2]:i1[2]] = np.abs(wn) > 0.4
from scipy import ndimage as ndi
L, n = ndi.label(OT); a = ndi.sum(OT, L, range(1, n + 1)); OT = L == (1 + np.argmax(a))       # main tail body (fur flecks dropped)
ST = ndi.gaussian_filter(sdf(OT, h), 0.6 / h)
S = smin(S, ST, t['blend'])
np.savez_compressed(sys.argv[2] + '.npz', S=S.astype(np.float32), lo=lo, h=h)
mm = mesh(S, lo, h, sys.argv[2] + '_raw.obj'); print(mm.bounds.round(1), mm.is_watertight)
json.dump(dict(params=P, tail_bounds=[W.min(0).round(1).tolist(), W.max(0).round(1).tolist()]), open(sys.argv[2] + '_log.json', 'w'), indent=1)
