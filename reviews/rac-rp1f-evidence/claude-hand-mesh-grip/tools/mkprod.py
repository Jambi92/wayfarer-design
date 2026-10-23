# mkprod.py (bpy) -- PROD.npz OUT.blend NAME : save the production mesh as a .blend (metres, Blender frame), then reopen and verify
import bpy, sys, numpy as np, os
a = sys.argv[sys.argv.index('--') + 1:]; zf, outb, name = a
z = np.load(zf); V = z['V'] * np.array([1, -1, 1]) / 100.0; Q = z['Q'][:, ::-1]
bpy.ops.wm.read_factory_settings(use_empty=True)
me = bpy.data.meshes.new(name); me.vertices.add(len(V)); me.vertices.foreach_set('co', V.ravel().astype(np.float32))
me.loops.add(Q.size); me.loops.foreach_set('vertex_index', Q.ravel().astype(np.int32)); me.polygons.add(len(Q))
me.polygons.foreach_set('loop_start', np.arange(0, Q.size, 4)); me.polygons.foreach_set('loop_total', np.full(len(Q), 4)); me.update(calc_edges=True)
me.polygons.foreach_set('use_smooth', np.ones(len(Q), bool)); me.validate(verbose=False)
ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
bpy.context.scene['status'] = 'Gorrund production mesh 110: v015 topology refit to rev107 hands + Tyler-directed thumb-tip rebuild (index-fingertip shape). Not frozen.'
bpy.ops.wm.save_as_mainfile(filepath=outb, compress=True)
bpy.ops.wm.open_mainfile(filepath=outb); m = bpy.data.objects[name].data
P = np.zeros(len(m.vertices) * 3); m.vertices.foreach_get('co', P); P = P.reshape(-1, 3)
F = np.zeros(len(m.polygons) * 4, int); m.polygons.foreach_get('vertices', F); F = F.reshape(-1, 4)
print('verts', len(P), 'faces', len(F), 'max dev mm', float(np.abs(P - V.astype(np.float32)).max() * 1000), 'faces identical', bool((F == Q).all()), 'size', os.path.getsize(outb))
