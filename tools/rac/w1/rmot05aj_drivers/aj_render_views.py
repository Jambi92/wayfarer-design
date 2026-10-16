# RM-OT-05AJ evidence: identical-camera Workbench renders (matcap-free studio lighting, ortho) of a mesh given as VF.npz.
# Usage: blender-python aj_render_views.py VF.npz LABEL OUTDIR   -> OUTDIR/LABEL_<view>.png
import sys, os, numpy as np, bpy, mathutils
vf, label, od = sys.argv[1:4]; os.makedirs(od, exist_ok=True)
D = np.load(vf); V, F = D['V'], D['F']
bpy.ops.wm.read_factory_settings(use_empty=True)
me = bpy.data.meshes.new('m'); me.from_pydata(V.tolist(), [], F.tolist()); me.update()
o = bpy.data.objects.new('m', me); sc = bpy.context.scene; sc.collection.objects.link(o)
for p in me.polygons: p.use_smooth = True
sc.render.engine = 'BLENDER_WORKBENCH'; sh = sc.display.shading; sh.light = 'STUDIO'; sh.color_type = 'SINGLE'; sh.single_color = (0.7, 0.7, 0.7)
sh.show_cavity = False; sh.background_type = 'VIEWPORT'; sc.render.film_transparent = False
sc.world = bpy.data.worlds.new('w'); sc.render.resolution_percentage = 100
z0 = V[:, 2].min(); cx = float(np.median(V[:, 0])); cy = float(np.median(V[:, 1]))
cam = bpy.data.cameras.new('c'); cam.type = 'ORTHO'; co = bpy.data.objects.new('c', cam); sc.collection.objects.link(co); sc.camera = co
# views: name -> (yaw deg about Z, target z (m above floor), ortho scale m, target x offset, resolution)
VIEWS = {'whole_F': (0, 1.02, 2.2, 0, (900, 1100)), 'whole_P': (90, 1.02, 2.2, 0, (900, 1100)), 'whole_B': (180, 1.02, 2.2, 0, (900, 1100)), 'whole_34': (35, 1.02, 2.2, 0, (900, 1100)),
         'body_F': (0, 0.95, 1.6, 0, (900, 1100)), 'body_P': (90, 0.95, 1.6, 0, (900, 1100)), 'body_B': (180, 0.95, 1.6, 0, (900, 1100)), 'body_34': (35, 0.95, 1.6, 0, (900, 1100)),
         'arms_F': (0, 1.30, 1.0, 0, (1200, 800)), 'arms_34': (35, 1.30, 1.0, 0, (1200, 800)), 'armR_P': (90, 1.30, 0.8, 0, (800, 800)), 'armL_P': (-90, 1.30, 0.8, 0, (800, 800)),
         'thighs_F': (0, 0.62, 0.8, 0, (900, 900)), 'thighs_34': (35, 0.62, 0.8, 0, (900, 900)),
         'calves_P': (90, 0.35, 0.7, 0, (800, 800)), 'calves_B': (180, 0.35, 0.7, 0, (900, 800))}
for name, (yaw, tz, osc, dx, res) in VIEWS.items():
    a = np.radians(yaw); d = mathutils.Vector((np.sin(a), -np.cos(a), 0))       # camera on -Y for front (model faces -Y)
    tgt = mathutils.Vector((cx + dx, cy, z0 + tz)); co.location = tgt + d * 6
    co.rotation_euler = (-d).to_track_quat('-Z', 'Y').to_euler(); cam.ortho_scale = osc; cam.clip_end = 20
    sc.render.resolution_x, sc.render.resolution_y = res; sc.render.filepath = os.path.join(od, f'{label}_{name}.png')
    bpy.ops.render.render(write_still=True)
print('done')
