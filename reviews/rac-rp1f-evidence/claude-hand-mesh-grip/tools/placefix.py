# placefix.py (bpy python) -- RIGDIR SIDE OUT.json : place the 32 mm x 180 mm handle fixture across the palm of the rest pose
import sys, json, numpy as np, os, pickle
sys.path.insert(0, '/tmp/claude-0/hand/tools'); import bpy; from fastpose import Hand
from mathutils.bvhtree import BVHTree; import mathutils
a = sys.argv[sys.argv.index('--') + 1:]; rd, side, outf = a[:3]
H = Hand(rd, side); Q = H.Q
BA = json.load(open(a[3])) if len(a) > 3 else {}
P = H.pose(BA)
RD = pickle.load(open(os.path.join(rd, 'rig_data.pkl'), 'rb'))[side]; J = RD['joints']
digs = {'L': ['A_L17', 'A_L18', 'A_L19', 'A_L20'], 'R': ['A_R21', 'A_R22', 'A_R23', 'A_R24']}[side]
Sk = H.skin_mats(BA)
def tp(b, p_): return (Sk[H.idx[b]] @ np.r_[p_, 1])[:3]
mcp = {k: tp(k + '_0', np.array(J[k]['base']) / 100) for k in digs}; pip = {k: tp(k + '_1', np.array(J[k]['j1']) / 100) for k in digs}
idx, lit = (digs[3], digs[0]) if side == 'L' else (digs[0], digs[3])
ax = mcp[lit] - mcp[idx]; ax /= np.linalg.norm(ax)
ventral = np.array([-1.0, 0, 0]) if side == 'L' else np.array([1.0, 0, 0])
ventral = ventral - (ventral @ ax) * ax; ventral /= np.linalg.norm(ventral)
mid = np.mean([mcp[k] for k in digs], 0); fdir = np.mean([pip[k] - mcp[k] for k in digs], 0); fdir -= (fdir @ ax) * ax; fdir -= (fdir @ ventral) * ventral; fdir /= np.linalg.norm(fdir)
t = BVHTree.FromPolygons(P.tolist(), Q.tolist(), all_triangles=False)
r = 0.016; hl = 0.09
def sd_all(c):
    d = P - c; tt = d @ ax; rad = np.linalg.norm(d - tt[:, None] * ax, axis=1); dr = rad - r; dt = np.abs(tt) - hl
    return np.sqrt(np.maximum(dr, 0) ** 2 + np.maximum(dt, 0) ** 2) + np.minimum(np.maximum(dr, dt), 0)
best = None
ax0 = ax.copy()
for tilt in np.radians(np.arange(-56, 57, 7)):
  ax = np.cos(tilt) * ax0 + np.sin(tilt) * fdir; ax /= np.linalg.norm(ax)
  for along in np.arange(-0.03, 0.06, 0.005):
    o = mid + along * fdir
    h = t.ray_cast(mathutils.Vector(o), mathutils.Vector(ventral), 0.2)
    if h[0] is None: continue
    surf = np.array(h[0])
    for off in np.arange(0.0, 0.06, 0.001):
        c = surf + ventral * (r + off); m = sd_all(c).min()
        if m >= 0.0015: break
    cand = dict(c=(c * 100).tolist(), ax=ax.tolist(), r=r * 100, hl=hl * 100, along_cm=float(along * 100), tilt_deg=float(np.degrees(tilt)), gap_mm=float(m * 1000), palm_offset_mm=float(off * 1000))
    if m >= 0.0015 and (best is None or off < best['palm_offset_mm'] / 1000): best = cand
own = RD['own']; c_ = np.array(best['c']) / 100; ax = np.array(best['ax']); sdv = sd_all(c_); i_ = int(np.argmin(sdv)); best['closest_owner'] = int(own[i_]); best['closest_pt'] = (P[i_] * 100).tolist()
print(json.dumps(best)); json.dump(best, open(outf, 'w'), indent=1)
