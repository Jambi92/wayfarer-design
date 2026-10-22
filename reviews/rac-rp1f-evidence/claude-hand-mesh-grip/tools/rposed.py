# rposed.py (bpy) -- RIGDIR SIDE POSED.npy OUTPREFIX [pairs.npy] [fixture.json] : render a posed hand crop (red = intersecting quads)
import bpy, numpy as np, sys, json, os, mathutils
a = sys.argv[sys.argv.index('--') + 1:]; rd, side, pp, outp = a[:4]
bpy.ops.wm.open_mainfile(filepath=os.path.join(rd, 'hand_rig_DIAG.blend')); sc = bpy.context.scene
src = bpy.data.objects['GO_hand_%s_DIAG' % side]; me0 = src.data
Q = np.zeros(len(me0.polygons) * 4, int); me0.polygons.foreach_get('vertices', Q); Q = Q.reshape(-1, 4)
P = np.load(pp).astype(np.float64)
for o in list(sc.objects): bpy.data.objects.remove(o, do_unlink=True)
me = bpy.data.meshes.new('p'); me.vertices.add(len(P)); me.vertices.foreach_set('co', P.ravel().astype(np.float32))
me.loops.add(Q.size); me.loops.foreach_set('vertex_index', Q.ravel()); me.polygons.add(len(Q)); me.polygons.foreach_set('loop_start', np.arange(0, Q.size, 4)); me.polygons.foreach_set('loop_total', np.full(len(Q), 4)); me.update()
me.polygons.foreach_set('use_smooth', np.ones(len(Q), bool))
m1 = bpy.data.materials.new('g'); m1.diffuse_color = (0.8, 0.78, 0.74, 1); m2 = bpy.data.materials.new('r'); m2.diffuse_color = (0.95, 0.1, 0.1, 1); me.materials.append(m1); me.materials.append(m2)
lab = np.zeros(len(Q), np.int32)
if len(a) > 4 and a[4] != '-' and os.path.exists(a[4]): pr = np.load(a[4]); lab[pr.ravel()] = 1
me.polygons.foreach_set('material_index', lab); me.update()
ob = bpy.data.objects.new('p', me); sc.collection.objects.link(ob)
if len(a) > 5:
    fx = json.load(open(a[5])); c = np.array(fx['c']) / 100; ax = np.array(fx['ax']); ax /= np.linalg.norm(ax)
    bpy.ops.mesh.primitive_cylinder_add(radius=fx['r'] / 100, depth=2 * fx['hl'] / 100, location=c, vertices=64)
    f = bpy.context.object; f.rotation_mode = 'QUATERNION'; f.rotation_quaternion = mathutils.Vector((0, 0, 1)).rotation_difference(mathutils.Vector(ax))
    m3 = bpy.data.materials.new('f'); m3.diffuse_color = (0.25, 0.45, 0.85, 1); f.data.materials.append(m3)
sh = sc.display.shading; sc.render.engine = 'BLENDER_WORKBENCH'; sh.light = 'STUDIO'; sh.color_type = 'MATERIAL'; sh.show_cavity = True
sh.background_type = 'VIEWPORT'; sh.background_color = (0.16, 0.17, 0.19); sc.render.resolution_x = 800; sc.render.resolution_y = 800
cam = bpy.data.cameras.new('c'); cam.type = 'ORTHO'; co = bpy.data.objects.new('c', cam); sc.collection.objects.link(co); sc.camera = co
cx = P[P[:, 2] < P[:, 2].min() + 0.2].mean(0)
sg = 1 if side == 'L' else -1
for nm, d in (('1palm', (-sg, -0.25, -0.1)), ('2side', (0, -1, -0.1)), ('3back', (sg, -0.3, 0.1)), ('4below', (0.15 * sg, -0.3, -1))):
    dv = mathutils.Vector(d).normalized(); co.location = mathutils.Vector(cx) + dv * 2; co.rotation_euler = (-dv).to_track_quat('-Z', 'Y').to_euler(); cam.ortho_scale = 0.27
    sc.render.filepath = '%s_%s.png' % (outp, nm); bpy.ops.render.render(write_still=True)
