# RM-OT-05P stage C: named ELLIPSOID-region normal displacements (bilateral mirror), for joint-adjacent soft-tissue
# transitions. Each zone: centre (left side, X>0), radii, amount cm (+ out / - in), optional facing filter on the normal
# relative to the zone centre ('radial' = all directions). The per-vertex displacement and the normals are diffused over the
# mesh (8 graph-averaging passes) before applying, so edits change form smoothly without crumpling. Topology preserved.
# Usage: python3 p_regiondisp.py --in IN.obj --zones ZONES.json --out OUT.obj
import argparse, json, numpy as np, trimesh
ap = argparse.ArgumentParser(); ap.add_argument('--in', dest='inp'); ap.add_argument('--zones'); ap.add_argument('--out'); a = ap.parse_args()
m = trimesh.load(a.inp, process=False); V = np.asarray(m.vertices, float).copy(); F = np.asarray(m.faces); V0 = V.copy()
N = trimesh.Trimesh(V, F, process=False).vertex_normals
E = np.vstack([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]]); E = np.unique(np.sort(E, 1), axis=0); deg = np.bincount(E.ravel(), minlength=len(V)).astype(float)
def avg(X):
    acc = np.zeros_like(X); np.add.at(acc, E[:, 0], X[E[:, 1]]); np.add.at(acc, E[:, 1], X[E[:, 0]]); return 0.5 * X + 0.5 * acc / np.maximum(deg, 1).reshape((-1,) + (1,) * (X.ndim - 1))
ss = lambda t: (lambda q: q * q * (3 - 2 * q))(np.clip(t, 0, 1)); D = np.zeros(len(V)); log = []
for zn in json.load(open(a.zones)):
    c = np.array(zn['c'], float); r = np.array(zn['r'], float); W = np.zeros(len(V))
    for sx in (1, -1):
        cc = c * [sx, 1, 1]; q = np.sqrt((((V - cc) / r) ** 2).sum(1)); w = ss(1 - q)
        if zn.get('facing') and zn['facing'] != 'radial':
            dirv = {'medial': [-sx, 0, 0], 'lateral': [sx, 0, 0], 'anterior': [0, 1, 0], 'posterior': [0, -1, 0]}[zn['facing']]
            w *= ss((N @ np.array(dirv, float) - 0.2) / 0.5)
        W = np.maximum(W, w * (np.sign(V[:, 0]) == sx))
    D += zn['amount'] * W; log.append(dict(zn, vertices=int((W > 0.01).sum())))
Ns = N.copy()
for _ in range(8): D = avg(D); Ns = avg(Ns)
Ns /= np.maximum(np.linalg.norm(Ns, axis=1), 1e-9)[:, None]; V += D[:, None] * Ns
trimesh.Trimesh(V, F, process=False).export(a.out); d = np.linalg.norm(V - V0, axis=1)
json.dump(dict(input=a.inp, output=a.out, zones=log, max_disp_cm=round(float(d.max()), 3), moved=int((d > 0.01).sum()),
               volume_L=[round(trimesh.Trimesh(V0, F, process=False).volume / 1000, 2), round(trimesh.Trimesh(V, F, process=False).volume / 1000, 2)]),
          open(a.out.replace('.obj', '_record.json'), 'w'), indent=1); print('moved', int((d > 0.01).sum()), 'max', round(float(d.max()), 2))
