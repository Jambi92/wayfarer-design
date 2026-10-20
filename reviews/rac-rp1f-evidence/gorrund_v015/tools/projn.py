# blender-python projn.py -- IN.npz TARGET.npz OUT.npz cx,cy,cz(blender) R [NREL]
# bounded transfer of the production patch onto an author-target surface (RP1F claws): each vertex in the ball moves along its own
# normal onto the target (nearest of the two ray hits, max 0.5 cm), weight -> 0 over the outer 30 %; then NREL rounds of tangential
# relaxation + closest-point reprojection onto the target redistribute vertices over the claw. Topology unchanged.
import sys, numpy as np, bpy, mathutils
from mathutils.bvhtree import BVHTree
a = sys.argv[sys.argv.index('--') + 1:]
z = np.load(a[0]); t = np.load(a[1]); out = a[2]; c = np.array([float(x) for x in a[3].split(',')]) * np.array([1, -1, 1]); R = float(a[4]); NREL = int(a[5]) if len(a) > 5 else 6
V = z['V'].astype(float).copy(); Q = z['Q'].astype(np.int64); F = z['F'].astype(np.int64)
TV = t['V'].astype(float); TF = t['F'].astype(np.int64)
bvh = BVHTree.FromPolygons(TV.tolist(), TF.tolist())
d0 = np.linalg.norm(V - c, axis=1); reg = np.where(d0 < R)[0]; w = np.clip((R - d0[reg]) / (0.3 * R), 0, 1)
Fl = F[(np.isin(F, reg)).any(1)]
def normals(P):
    fn = np.cross(P[Fl[:, 1]] - P[Fl[:, 0]], P[Fl[:, 2]] - P[Fl[:, 0]]); vn = np.zeros_like(P)
    for k in range(3): np.add.at(vn, Fl[:, k], fn)
    return vn / (np.linalg.norm(vn, axis=1, keepdims=True) + 1e-15)
nb = {}
for q in Q[(np.isin(Q, reg)).any(1)]:
    for i in range(4): nb.setdefault(q[i], set()).update((q[i - 1], q[(i + 1) % 4]))
rn = [np.array(sorted(nb[v])) for v in reg]
vn = normals(V)[reg]; P0 = V[reg].copy(); newp = P0.copy()
for i, (p, nn) in enumerate(zip(P0, vn)):
    best = None
    for sgn in (1, -1):
        h = bvh.ray_cast(mathutils.Vector((p - sgn * 1e-4 * nn).tolist()), mathutils.Vector((sgn * nn).tolist()), 0.5)
        if h[0] is not None and (best is None or h[3] < best[1]): best = (np.array(h[0]), h[3])
    if best is None:
        h = bvh.find_nearest(mathutils.Vector(p.tolist()), 0.5)
        if h[0] is not None: best = (np.array(h[0]), h[3])
    if best is not None: newp[i] = best[0]
V[reg] = P0 + w[:, None] * (newp - P0)
for it in range(NREL):
    vn = normals(V)[reg]; L = np.array([V[n].mean(0) for n in rn]) - V[reg]; Lt = L - (L * vn).sum(1, keepdims=True) * vn
    Pn = V[reg] + 0.5 * Lt
    for i, p in enumerate(Pn):
        h = bvh.find_nearest(mathutils.Vector(p.tolist()), 0.5)
        if h[0] is not None: Pn[i] = np.array(h[0])
    V[reg] = V[reg] + w[:, None] * (Pn - V[reg])
mv = np.linalg.norm(V[reg] - P0, axis=1) * 10
print('region', len(reg), 'moved', int((mv > 1e-3).sum()), 'max mm %.2f' % mv.max())
np.savez_compressed(out, V=V, F=F, Q=Q)
