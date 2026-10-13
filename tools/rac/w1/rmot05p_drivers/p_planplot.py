# Plan illustration on the declared baseline (x-ray vertex projection): proxy hip-knee-ankle axes (red), stage-A leg region
# (green), stage-B trunk zones (blue), stage-C joint zones (purple), LOW protected regions (red outlines as filled dots).
import sys, json, numpy as np, trimesh, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
base, axes, bz, cz, low, out = sys.argv[1:7]
V = trimesh.load(base, process=False).vertices; A = json.load(open(axes)); B = json.load(open(bz)); C = json.load(open(cz)); L = json.load(open(low))
ss = lambda t: np.clip(t, 0, 1)
def tent(z, z0, zp, z1): return np.where(z < zp, ss((z - z0) / (zp - z0)), ss((z1 - z) / (z1 - zp)))
col = np.full((len(V), 3), 0.85)
legA = (V[:, 2] < 120) & (np.abs(V[:, 0]) > 2) & (np.abs(V[:, 0]) < 34); col[legA] = (0.65, 0.88, 0.65)
for zn in B:
    w = tent(V[:, 2], zn['z0'], zn['zp'], zn['z1']) * (np.abs(V[:, 0]) > zn['x'][0]) * (np.abs(V[:, 0]) < zn['x'][1]) > 0.3; col[w] = (0.45, 0.6, 1.0)
for zn in C:
    for sx in (1, -1):
        q = np.sqrt((((V - np.array(zn['c']) * [sx, 1, 1]) / np.array(zn['r'])) ** 2).sum(1)); col[q < 1] = (0.7, 0.45, 0.9)
for name, c, r in L['protect']:
    for sx in ((1,) if c[0] == 0 else (1, -1)):
        q = np.sqrt((((V - np.array(c) * [sx, 1, 1]) / np.array(r)) ** 2).sum(1)); col[q < 1] = (0.9, 0.15, 0.15)
fig, axs = plt.subplots(1, 2, figsize=(12, 10))
for ax, (t, u, s) in zip(axs, (('front (x-ray; image right = -X)', 0, -1), ('profile (x-ray; anterior right)', 1, 1))):
    ax.scatter(s * V[:, u], V[:, 2], c=col, s=0.5, linewidths=0)
    for sx in (1, -1):
        P = np.array([A['hip'], A['knee'], A['ankle']]) * [sx, 1, 1]; ax.plot(s * P[:, u], P[:, 2], 'r-o', ms=4, lw=1.5)
    ax.set_aspect('equal'); ax.grid(alpha=.25); ax.set_title(t)
fig.suptitle('RD4 plan on baseline GO-RD3b: green = stage A leg chain (coronal); blue = stage B trunk zones; purple = stage C joint zones;\nred = LOW protected skeletal regions; red lines = proxy hip-knee-ankle axes (section mid-point fits, ~+/-3 cm hip uncertainty)', fontsize=9)
fig.savefig(out, dpi=95, bbox_inches='tight'); print(out)
