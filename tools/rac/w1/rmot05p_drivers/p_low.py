# RM-OT-05P §5: LOW rebuilt from the repaired REF with REAL protection (mesh-based, identical vertex correspondence).
# Tissue regions: ellipsoids, mirrored; inward normal displacement amount * smoothstep(1 - q).
# Protection: P = 1 inside each protected ellipsoid, smooth falloff to 0 over falloff_cm outside (distance approximated as
# (q - 1) * min radius); the displacement is multiplied by (1 - P), so protected interiors move EXACTLY zero.
# Normals are smoothed (graph averaging, 6 passes) for direction only; no post-smoothing / remeshing of positions.
# Writes the LOW mesh, the per-vertex masks (npz: protected interior, falloff band, tissue weight) and a record.
# Usage: python3 p_low.py --ref REF.obj --regions low_regions.json --out LOW.obj
import argparse, json, numpy as np, trimesh
ap = argparse.ArgumentParser(); ap.add_argument('--ref'); ap.add_argument('--regions'); ap.add_argument('--out'); a = ap.parse_args()
m = trimesh.load(a.ref, process=False); V = np.asarray(m.vertices, float); F = np.asarray(m.faces); R = json.load(open(a.regions))
ss = lambda t: (lambda q: q * q * (3 - 2 * q))(np.clip(t, 0, 1))
def q_of(c, r, sx):
    return np.sqrt((((V - np.array(c) * [sx, 1, 1]) / np.array(r)) ** 2).sum(1))
P = np.zeros(len(V)); inside = np.zeros(len(V), bool); per = {}
for name, c, r in R['protect']:
    pm = np.zeros(len(V)); im = np.zeros(len(V), bool)
    for sx in ((1,) if c[0] == 0 else (1, -1)):
        q = q_of(c, r, sx); im |= q <= 1; pm = np.maximum(pm, np.where(q <= 1, 1.0, ss(1 - (q - 1) * min(r) / R['falloff_cm'])))
    P = np.maximum(P, pm); inside |= im; per[name] = im
T = np.zeros(len(V))
for name, c, r, amt in R['tissue']:
    for sx in ((1,) if c[0] == 0 else (1, -1)):
        T += amt * ss(1 - q_of(c, r, sx))
N = trimesh.Trimesh(V, F, process=False).vertex_normals.copy()
E = np.vstack([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]]); E = np.unique(np.sort(E, 1), axis=0); deg = np.bincount(E.ravel(), minlength=len(V)).astype(float)
for _ in range(6):
    acc = np.zeros_like(N); np.add.at(acc, E[:, 0], N[E[:, 1]]); np.add.at(acc, E[:, 1], N[E[:, 0]]); N = 0.5 * N + 0.5 * acc / np.maximum(deg, 1)[:, None]
N /= np.linalg.norm(N, axis=1)[:, None]
disp = T * (1 - P); L = V - disp[:, None] * N
trimesh.Trimesh(L, F, process=False).export(a.out)
np.savez_compressed(a.out.replace('.obj', '_masks.npz'), protected_interior=inside, protection=P.astype(np.float32), tissue=T.astype(np.float32), displacement=disp.astype(np.float32))
d = np.linalg.norm(L - V, axis=1); band = (P > 0) & ~inside
st = lambda x: dict(n=int(len(x)), max=round(float(x.max()), 4) if len(x) else None, p99=round(float(np.percentile(x, 99)), 4) if len(x) else None, p95=round(float(np.percentile(x, 95)), 4) if len(x) else None)
rec = dict(ref=a.ref, low=a.out, method='vertex-identical normal displacement; correspondence = vertex index', volume_L=[round(m.volume / 1000, 2), round(trimesh.Trimesh(L, F, process=False).volume / 1000, 2)],
           protected_interior_displacement_cm={k: st(d[v]) for k, v in per.items()}, all_protected_interior=st(d[inside]), falloff_band=st(d[band]), tissue_max_cm=round(float(d.max()), 3))
json.dump(rec, open(a.out.replace('.obj', '_record.json'), 'w'), indent=1); print(json.dumps(rec, indent=1))
