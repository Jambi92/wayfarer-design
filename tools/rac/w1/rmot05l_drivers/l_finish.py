# RAC RM-OT-05L: finish a clay voxel remesh into the concept asset (bpy): surface relax (Laplacian smooth, volume-preserving),
# decimate to a working density, save the source .blend and the concept OBJ.   Usage: python3 l_finish.py RAW.obj OUT_PREFIX [ratio]
import sys, bpy, numpy as np
raw, out = sys.argv[1], sys.argv[2]; ratio = float(sys.argv[3]) if len(sys.argv) > 3 else 0.35
V = [[float(t) for t in l.split()[1:4]] for l in open(raw) if l.startswith('v ')]
F = [[int(t) - 1 for t in l.split()[1:4]] for l in open(raw) if l.startswith('f ')]
bpy.ops.wm.read_factory_settings(use_empty=True)
me = bpy.data.meshes.new('GO_RS'); me.from_pydata(V, [], F); me.update()
ob = bpy.data.objects.new('GO_RS', me); bpy.context.scene.collection.objects.link(ob); bpy.context.view_layer.objects.active = ob; ob.select_set(True)
m = ob.modifiers.new('relax', 'LAPLACIANSMOOTH'); m.iterations = 6; m.lambda_factor = 0.6; m.use_volume_preserve = True
d = ob.modifiers.new('dec', 'DECIMATE'); d.ratio = ratio
bpy.ops.object.modifier_apply(modifier='relax'); bpy.ops.object.modifier_apply(modifier='dec')
for p in me.polygons: p.use_smooth = True
bpy.ops.wm.save_as_mainfile(filepath=out + '.blend')
me = ob.data; me.calc_loop_triangles()
Vo = np.array([v.co[:] for v in me.vertices]); Fo = np.array([t.vertices[:] for t in me.loop_triangles])
with open(out + '.obj', 'w') as o:
    o.write('# RAC RM-OT-05L %s concept asset (clay -> voxel remesh -> relax -> decimate); cm, Z up, +Y anterior, +X body left\n' % out.split('/')[-1])
    for v in Vo: o.write('v %.4f %.4f %.4f\n' % tuple(v))
    for t in Fo: o.write('f %d %d %d\n' % tuple(t + 1))
print(len(Vo), len(Fo), Vo.min(0), Vo.max(0))
