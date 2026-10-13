# RM-OT-05P stage B: named, local NORMAL-DISPLACEMENT edits of the trunk surface (mesh-based; topology and vertex
# correspondence preserved). Each zone: z tent (z0 -> zp -> z1, smoothstep), a facing filter on the vertex normal
# (lateral: |n_x|, posterior: -n_y, anterior: +n_y; ramped between f0 and f1), an optional |X| window, and an amount in cm
# (+ outward, - inward). Arm vertices are excluded with the arm medial edge from p_trunkprofile (|X| >= arm_cut(z) - 1 cm).
# After displacement, a few local Taubin passes inside the edited band remove steps. Bilateral by construction (the
# filters use |X| and |n_x|). Usage: python3 p_displace.py --in IN.obj --zones ZONES.json --profile PROFILE.json --out OUT.obj
import argparse, json, numpy as np, trimesh
ap = argparse.ArgumentParser(); ap.add_argument('--in', dest='inp'); ap.add_argument('--zones'); ap.add_argument('--profile'); ap.add_argument('--out'); a = ap.parse_args()
m = trimesh.load(a.inp, process=False); V = np.asarray(m.vertices, float).copy(); F = np.asarray(m.faces); V0 = V.copy()
N = trimesh.Trimesh(V, F, process=False).vertex_normals
P = json.load(open(a.profile))['rows']; zz = np.array([r['z'] for r in P]); cutx = np.array([(r['arm_cut_x'] if r['arm_cut_x'] else 99.0) for r in P])
# arm medial edge where separate = the slice's own trunk half-breadth + the gap; use the interpolated cut where contact, else a wide bound
armx = np.interp(V[:, 2], zz, np.where(cutx < 90, cutx, 99.0)); trunk = np.abs(V[:, 0]) < armx - 1.0
# keep away from the arm: arm vertices = |X| beyond the trunk's lateral edge in the arm band; trunk edits fade to 0 within
# 2 cm of any arm vertex (full weight beyond 6 cm), so contact zones are not torn
from scipy.spatial import cKDTree
zr = (V[:, 2] > 100) & (V[:, 2] < 180); arm = zr & ~trunk
dA = cKDTree(V[arm]).query(V)[0] if arm.any() else np.full(len(V), 99.0)
trunk = trunk * (lambda q: q * q * (3 - 2 * q))(np.clip((dA - 2.0) / 4.0, 0, 1))
ss = lambda t: (lambda q: q * q * (3 - 2 * q))(np.clip(t, 0, 1)); log = []; band = np.zeros(len(V), bool); DISP = np.zeros(len(V))
for zn in json.load(open(a.zones)):
    z = V[:, 2]; wz = np.where(z < zn['zp'], ss((z - zn['z0']) / (zn['zp'] - zn['z0'])), ss((zn['z1'] - z) / (zn['z1'] - zn['zp'])))
    fac = {'lateral': np.abs(N[:, 0]), 'posterior': -N[:, 1], 'anterior': N[:, 1]}[zn['facing']]
    wf = ss((fac - zn.get('f0', 0.35)) / (zn.get('f1', 0.8) - zn.get('f0', 0.35)))
    x0, x1 = zn.get('x', [0, 99]); wx = ss((np.abs(V[:, 0]) - x0) / 2.0) * ss((x1 - np.abs(V[:, 0])) / 2.0)
    w = wz * wf * wx * trunk; DISP += zn['amount'] * w; band |= w > 0.01
    log.append(dict(zn, vertices=int((w > 0.01).sum()), max_disp=round(float(np.abs(zn['amount']) * w.max()), 3)))
# the scalar displacement field and the normals are diffused over the mesh (graph averaging, 25 iterations) BEFORE
# applying, so the edit is a broad, smooth change of form and does not crumple the surface where normals are noisy
E = np.vstack([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]]); E = np.unique(np.sort(E, 1), axis=0)
deg0 = np.bincount(E.ravel(), minlength=len(V)).astype(float)
def avg(X):
    acc = np.zeros_like(X); np.add.at(acc, E[:, 0], X[E[:, 1]]); np.add.at(acc, E[:, 1], X[E[:, 0]]); return 0.5 * X + 0.5 * acc / np.maximum(deg0, 1).reshape((-1,) + (1,) * (X.ndim - 1))
Ns = N.copy()
for _ in range(25): DISP = avg(DISP); Ns = avg(Ns)
Ns /= np.maximum(np.linalg.norm(Ns, axis=1), 1e-9)[:, None]; V += DISP[:, None] * Ns; band |= np.abs(DISP) > 0.01
nb = band.copy(); nb[E[band[E[:, 0]] | band[E[:, 1]]].ravel()] = True
deg = np.bincount(E.ravel(), minlength=len(V)).astype(float)
def lap(X):
    acc = np.zeros_like(X); np.add.at(acc, E[:, 0], X[E[:, 1]]); np.add.at(acc, E[:, 1], X[E[:, 0]]); return acc / np.maximum(deg, 1)[:, None] - X
for _ in range(4):
    V[nb] += 0.5 * lap(V)[nb]; V[nb] -= 0.53 * lap(V)[nb]
trimesh.Trimesh(V, F, process=False).export(a.out)
d = np.linalg.norm(V - V0, axis=1)
json.dump(dict(input=a.inp, output=a.out, zones=log, relaxed_vertices=int(nb.sum()), max_disp_cm=round(float(d.max()), 3),
               volume_L=[round(trimesh.Trimesh(V0, F, process=False).volume / 1000, 2), round(trimesh.Trimesh(V, F, process=False).volume / 1000, 2)]),
          open(a.out.replace('.obj', '_record.json'), 'w'), indent=1)
print(json.dumps(log, indent=1)); print('max', d.max().round(2))
