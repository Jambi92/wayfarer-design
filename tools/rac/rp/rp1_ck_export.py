"""RAC RP1 checkpoint DIAGNOSTIC (read-only on the checkpoint file): evaluate the manual cage object as it would be finished
(Subdivision Surface Catmull-Clark level N inserted before the existing Shrinkwrap -> weldsrc) and export cage + evaluated mesh
in the analysis frame (cm; x = subject left, f = forward = -y Blender, u = up). The checkpoint .blend is never saved.
Usage: blender-python rp1_ck_export.py -- CHECKPOINT.blend CAGE_OBJECT LEVELS OUT.npz"""
import sys, numpy as np, bpy, bmesh
a = sys.argv[sys.argv.index('--') + 1:]; path, name, lev, out = a[0], a[1], int(a[2]), a[3]
bpy.ops.wm.open_mainfile(filepath=path)
o = bpy.data.objects[name]
def arr(me):
    V = np.array([v.co[:] for v in me.vertices], np.float64)
    V = (np.asarray(o.matrix_world) @ np.c_[V, np.ones(len(V))].T).T[:, :3]
    return np.c_[V[:, 0], -V[:, 1], V[:, 2]] * 100.0
# cage stats
bm = bmesh.new(); bm.from_mesh(o.data)
cage = dict(verts=len(bm.verts), faces=len(bm.faces), quads=sum(len(f.verts) == 4 for f in bm.faces),
            tris=sum(len(f.verts) == 3 for f in bm.faces), ngons=sum(len(f.verts) > 4 for f in bm.faces),
            boundary_edges=sum(e.is_boundary for e in bm.edges), nonmanifold_edges=sum(not e.is_manifold and not e.is_boundary for e in bm.edges),
            wire_edges=sum(e.is_wire for e in bm.edges), loose_verts=sum(len(v.link_edges) == 0 for v in bm.verts))
Vc = arr(o.data); Fc = [[v.index for v in f.verts] for f in bm.faces]
# evaluated with subdivision inserted before shrinkwrap
m = o.modifiers.new('ck_subsurf', 'SUBSURF'); m.levels = lev; m.render_levels = lev; m.subdivision_type = 'CATMULL_CLARK'
bpy.context.view_layer.objects.active = o
while o.modifiers.find('ck_subsurf') > 0: bpy.ops.object.modifier_move_up(modifier='ck_subsurf')
dg = bpy.context.evaluated_depsgraph_get(); oe = o.evaluated_get(dg); me = oe.to_mesh()
me.calc_loop_triangles()
Ve = arr(me); Fe = np.array([t.vertices[:] for t in me.loop_triangles], np.int64)
Q = [list(p.vertices) for p in me.polygons]
np.savez_compressed(out, Vc=Vc, Fc=np.array([f + [-1] * (max(map(len, Fc)) - len(f)) for f in Fc]), Ve=Ve, Fe=Fe,
                    npoly=len(Q), nquad=sum(len(q) == 4 for q in Q), cage=str(cage), mods=str([(mm.name, mm.type) for mm in o.modifiers]))
print('CAGE', cage); print('EVAL', len(Ve), len(Q), 'mods', [(mm.name, mm.type) for mm in o.modifiers])
