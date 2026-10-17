# RM-OT-05AU renders (read-only geometry). Usage: blender-python au_render.py VF.npz LABEL OUTDIR VIEWSET
import sys, os, numpy as np, bpy, mathutils
vf, label, od, vset = sys.argv[1:5]; os.makedirs(od, exist_ok=True)
D = np.load(vf); V, F = D['V'], D['F']
bpy.ops.wm.read_factory_settings(use_empty=True)
me = bpy.data.meshes.new('m'); me.from_pydata(V.tolist(), [], F.tolist()); me.update()
o = bpy.data.objects.new('m', me); sc = bpy.context.scene; sc.collection.objects.link(o)
for p in me.polygons: p.use_smooth = True
sc.render.engine = 'BLENDER_WORKBENCH'; sh = sc.display.shading; sh.light = 'STUDIO'; sh.color_type = 'SINGLE'; sh.single_color = (0.7, 0.7, 0.7)
sh.show_cavity = False; sh.background_type = 'VIEWPORT'; sc.world = bpy.data.worlds.new('w'); sc.render.resolution_percentage = 100
z0 = V[:, 2].min(); cx = float(np.median(V[:, 0])); cy = float(np.median(V[:, 1]))
cam = bpy.data.cameras.new('c'); cam.type = 'ORTHO'; co = bpy.data.objects.new('c', cam); sc.collection.objects.link(co); sc.camera = co
SETS = {
 'whole': {'whole_F': (0, 1.02, 2.2, 0, 0, (900, 1100)), 'whole_P': (90, 1.02, 2.2, 0, 0, (900, 1100)), 'whole_34': (35, 1.02, 2.2, 0, 0, (900, 1100)), 'whole_B': (180, 1.02, 2.2, 0, 0, (900, 1100))},
 'head': {'head_F': (0, 1.70, 0.75, 0, 0, (1000, 1000)), 'head_P': (90, 1.70, 0.75, 0, -0.25, (1000, 1000)), 'head_34': (35, 1.70, 0.75, 0, -0.1, (1000, 1000))},
 'feet': {'feet_F': (0, 0.12, 0.75, 0, 0, (1200, 600)), 'feet_B': (180, 0.12, 0.75, 0, 0, (1200, 600)), 'footL_P': (-90, 0.12, 0.6, 0.19, -0.3, (1000, 500)), 'footR_P': (90, 0.12, 0.6, -0.19, -0.3, (1000, 500)), 'feet_34': (35, 0.15, 0.8, 0, -0.1, (1200, 700))},
 'tail': {'tail_B': (180, 1.05, 0.55, 0, 0, (900, 900)), 'tail_P': (90, 1.05, 0.55, 0, 0.12, (900, 900)), 'tail_34B': (145, 1.05, 0.6, 0, 0.05, (900, 900))},
}
import json
VS = json.load(open(vset)) if vset.endswith('.json') else SETS[vset]
ABS = vset.endswith('.json')
for name, (yaw, tz, osc, dx, dy, res) in VS.items():
    a = np.radians(yaw); d = mathutils.Vector((np.sin(a), -np.cos(a), 0))
    tgt = mathutils.Vector((dx, dy, z0 + tz)) if ABS else mathutils.Vector((cx + dx, cy + dy, z0 + tz)); co.location = tgt + d * 6
    co.rotation_euler = (-d).to_track_quat('-Z', 'Y').to_euler(); cam.ortho_scale = osc; cam.clip_end = 20
    sc.render.resolution_x, sc.render.resolution_y = res; sc.render.filepath = os.path.join(od, f'{label}_{name}.png'); bpy.ops.render.render(write_still=True)
print('done')
