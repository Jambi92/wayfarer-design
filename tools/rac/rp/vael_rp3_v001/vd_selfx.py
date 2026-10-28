# vd_selfx.py OUT.json BASE_R6.npz CAND_R6.npz [...] : Vael custom body-deformation order §12 -- source self-intersection audit (bpy BVH overlap of the
# R-6 body triangles, adjacent faces excluded), for the R1 base and each VD candidate on the identical hm08 triangle list; reports the pairs that are NEW
# against the base (attributable to the deformation) and where they are (dominant skin-weight bone of the involved vertices).
import bpy, sys, json, numpy as np, mathutils
from mathutils.bvhtree import BVHTree
a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
OUT, BASE = a[:2]; C = a[2:]
def pairs(p):
    z = np.load(p); keep = z['keep']; F = z['F'][keep[z['F']].all(1)]; V = z['V'].astype(float)
    bvh = BVHTree.FromPolygons([mathutils.Vector(v) for v in V.tolist()], F.tolist(), all_triangles=True); P = set()
    for i, j in bvh.overlap(bvh):
        if i == j or set(F[i]) & set(F[j]): continue
        P.add((min(i, j), max(i, j)))
    return P, F, z
P0, F0, z0 = pairs(BASE); bones = [k[2:] for k in z0.files if k.startswith('w_')]; Wm = np.stack([z0['w_' + b] for b in bones], 1)
res = dict(base=BASE, base_pairs=len(P0), candidates={})
for c in C:
    P, F, z = pairs(c); new = P - P0
    reg = {}
    for i, j in new:
        b = bones[int(Wm[F[i]].sum(0).argmax())]; reg[b] = reg.get(b, 0) + 1
    res['candidates'][c] = dict(pairs=len(P), new_pairs=len(new), removed_pairs=len(P0 - P), new_by_region=reg)
    print(c.split('/')[-1], len(P), 'new', len(new), reg, flush=True)
json.dump(res, open(OUT, 'w'), indent=1)
