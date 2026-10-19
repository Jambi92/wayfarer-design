"""RP1E design aid (cloud, prep only): adjust the positions of selected cage vertices so that the Catmull-Clark smoothed
position of each control vertex lands on its own colour target surface (iterative control-point correction).
Topology is untouched; the result is a list of typed coordinates for manual UI authoring.
Usage: blender-python fit.py -- cage.npz colours.npy TPREFIX movable.npy OUT.npz iters alpha level"""
import sys, numpy as np, bpy
from mathutils.bvhtree import BVHTree
from mathutils import Vector
a = sys.argv[sys.argv.index('--') + 1:]
cg, colp, tp, movp, out = a[:5]; iters = int(a[5]); alpha = float(a[6]); lev = int(a[7]); inset = float(a[8]) if len(a) > 8 else 0.0; beta = float(a[9]) if len(a) > 9 else 0.0
z = np.load(cg); V = z['V'].astype(float).copy(); F = z['F']; col = np.load(colp); mov = np.load(movp)
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
me = bpy.data.meshes.new('c'); me.from_pydata((V / 100).tolist(), [], [list(map(int, f[f >= 0])) for f in F]); me.update()
o = bpy.data.objects.new('c', me); sc.collection.objects.link(o)
m = o.modifiers.new('s', 'SUBSURF'); m.levels = lev; m.render_levels = lev
trees = {}
for c in np.unique(col):
    t = np.load('%s_c%d.npz' % (tp, c)); trees[int(c)] = BVHTree.FromPolygons((t['V'] / 100).tolist(), t['F'].tolist())
idx = np.where(mov)[0]
adj = {}
for f in F:
    f = f[f >= 0]
    for j in range(len(f)): p_, q_ = int(f[j]), int(f[(j + 1) % len(f)]); adj.setdefault(p_, set()).add(q_); adj.setdefault(q_, set()).add(p_)
for it in range(iters):
    for i in idx: me.vertices[i].co = (V[i] / 100).tolist()
    me.update()
    dg = bpy.context.evaluated_depsgraph_get(); oe = o.evaluated_get(dg); em = oe.to_mesh()
    Sm = np.array([em.vertices[i].co[:] for i in idx]) * 100; oe.to_mesh_clear()
    err = []
    for k, i in enumerate(idx):
        loc, nrm, fi, d = trees[int(col[i])].find_nearest(Vector(Sm[k] / 100))
        if loc is None: continue
        tgt = np.array(loc[:]) * 100 - inset * np.array(nrm[:])
        dv = tgt - Sm[k]; V[i] += alpha * dv; err.append(np.linalg.norm(dv))
    if beta > 0:
        Vn = V.copy()
        for i in idx:
            nb = list(adj[i]); Vn[i] = (1 - beta) * V[i] + beta * V[nb].mean(0)
        V[:] = Vn
    print('ITER', it, 'mean err %.3f max %.3f' % (np.mean(err), np.max(err)))
np.savez_compressed(out, V=V, F=F)
