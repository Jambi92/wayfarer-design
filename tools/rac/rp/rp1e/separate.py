"""Coarse-cage untangle (design aid): repeatedly find intersecting face pairs (bpy BVH) and push the two faces' movable
vertices apart along the centroid-to-centroid direction (small steps), never moving pinned/fixed vertices.
Usage: blender-python separate.py -- cage.npz movable.npy pins.json step iters OUT.npz"""
import sys, json, numpy as np, bpy
from mathutils.bvhtree import BVHTree
a = sys.argv[sys.argv.index('--') + 1:]
z = np.load(a[0]); V = z['V'].astype(float).copy(); F = z['F']; mov = np.load(a[1]); pins = set(int(k) for k in json.load(open(a[2])))
step = float(a[3]); iters = int(a[4]); out = a[5]
polys = [list(map(int, f[f >= 0])) for f in F]; sv = [set(p) for p in polys]
for it in range(iters):
    t = BVHTree.FromPolygons(V.tolist(), polys, all_triangles=False, epsilon=0.0)
    pairs = [(i, j) for i, j in t.overlap(t) if i < j and not (sv[i] & sv[j])]
    if not pairs: print('ITER', it, 'clean'); break
    D = np.zeros_like(V); n = np.zeros(len(V))
    for i, j in pairs:
        ci = V[polys[i]].mean(0); cj = V[polys[j]].mean(0); d = ci - cj; d /= (np.linalg.norm(d) + 1e-9)
        for vtx in polys[i]: D[vtx] += d; n[vtx] += 1
        for vtx in polys[j]: D[vtx] -= d; n[vtx] += 1
    m = (n > 0) & mov
    for p in pins: m[p] = False
    V[m] += step * D[m] / n[m][:, None]
    print('ITER', it, 'pairs', len(pairs), 'moved', int(m.sum()))
np.savez_compressed(out, V=V, F=F)
