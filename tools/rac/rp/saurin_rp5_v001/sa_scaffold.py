# sa_scaffold.py IN.npz(V,F) TARGET_FACES OUT.npz (bpy) : DIAGNOSTIC SCAFFOLD ONLY (order 53976fb §8: automatic remesh may be used only as a diagnostic
# scaffold, never as the accepted production topology). Blender QuadriFlow remesh of the (decimated) canonical base at a uniform target face count,
# preserving sharp features off, mesh symmetry off (source asymmetry kept). Output quads in the analysis frame (cm).
import sys, numpy as np, bpy, bmesh
a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
z = np.load(a[0]); V = z['V'].astype(float); F = z['F'].astype(int); T = int(a[1])
bpy.ops.wm.read_factory_settings(use_empty=True)
me = bpy.data.meshes.new('src'); me.from_pydata((V / 100.0).tolist(), [], F.tolist()); me.update()
ob = bpy.data.objects.new('src', me); bpy.context.scene.collection.objects.link(ob); bpy.context.view_layer.objects.active = ob; ob.select_set(True)
r = bpy.ops.object.quadriflow_remesh(use_mesh_symmetry=False, use_preserve_sharp=False, use_preserve_boundary=False, preserve_attributes=False, smooth_normals=False,
                                     mode='FACES', target_faces=T, seed=0)
me = ob.data; Vo = np.array([v.co[:] for v in me.vertices]) * 100.0; Fo = [list(p.vertices) for p in me.polygons]
q = np.array([f for f in Fo if len(f) == 4]); t = [f for f in Fo if len(f) != 4]
np.savez_compressed(a[2], V=Vo, Q=q, other=np.array([len(f) for f in t]))
print('SCAFFOLD', r, len(Vo), 'verts', len(q), 'quads', len(t), 'non-quads')
