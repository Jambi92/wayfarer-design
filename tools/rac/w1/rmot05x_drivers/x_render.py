# RM-OT-05X: read-only review renders of the new Gorrund GLB (or a disposable diagnostic copy). Never writes the source.
# Workbench, studio light, single neutral grey, orthographic, matched framing (fixed ortho scale per view set), common ground line.
# Input: an npz with V (metres, glTF axes: X right, Y up, Z toward the viewer of a glTF front view) and F; or the GLB itself.
# Views: F front (+Z), B back (-Z), L left profile (camera on the figure's left = +X), R right profile, Q front 3/4 (front-left),
#        RQ rear 3/4; close-ups are any view with a centre + ortho scale.
# Usage: python3 x_render.py SPEC.json      SPEC = {"mesh": path, "out": prefix, "views": [{"name","dir","center","scale","res"}], "ground": true}
import sys, json, subprocess, tempfile, os, numpy as np
spec = json.load(open(sys.argv[1]))
BL = r'''
import bpy, sys, json, numpy as np, math
from mathutils import Vector
S = json.loads(open(sys.argv[sys.argv.index('--') + 1]).read())
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
if S['mesh'].endswith('.glb'):
    bpy.ops.import_scene.gltf(filepath=S['mesh']); ob = [o for o in sc.objects if o.type == 'MESH'][0]
    # glTF importer converts Y-up to Blender Z-up: Blender (x, y, z) = glTF (x, -z, y)
else:
    d = np.load(S['mesh']); V = d['V'].astype(np.float32); F = d['F'].astype(np.int32)
    V = np.stack([V[:, 0], -V[:, 2], V[:, 1]], 1)            # same mapping as the glTF importer
    me = bpy.data.meshes.new('m'); me.vertices.add(len(V)); me.vertices.foreach_set('co', V.ravel())
    me.loops.add(F.size); me.loops.foreach_set('vertex_index', F.ravel()); me.polygons.add(len(F))
    me.polygons.foreach_set('loop_start', (np.arange(len(F)) * 3).astype(np.int32)); me.update()
    me.polygons.foreach_set('use_smooth', np.ones(len(F), bool)); ob = bpy.data.objects.new('m', me); sc.collection.objects.link(ob)
sc.render.engine = 'BLENDER_WORKBENCH'; sc.display.shading.light = 'STUDIO'; sc.display.shading.color_type = 'SINGLE'
sc.display.shading.color_type = 'MATERIAL' if S.get('ground', False) else 'SINGLE'
sc.display.shading.single_color = (0.62, 0.62, 0.62); sc.render.film_transparent = True
sc.view_settings.view_transform = 'Standard'
if S.get('ground', False):
    bpy.ops.mesh.primitive_plane_add(size=6, location=(0, 0, -0.0005)); g = bpy.context.active_object
    m = bpy.data.materials.new('g'); m.diffuse_color = (0.85, 0.85, 0.85, 1); g.data.materials.append(m)
cam = bpy.data.cameras.new('c'); cam.type = 'ORTHO'; co = bpy.data.objects.new('c', cam); sc.collection.objects.link(co); sc.camera = co
cam.clip_end = 100
DIRS = {'F': (0, -1, 0), 'B': (0, 1, 0), 'L': (1, 0, 0), 'R': (-1, 0, 0), 'Q': (0.5, -0.866, 0), 'RQ': (-0.5, 0.866, 0),
        'QR': (-0.5, -0.866, 0), 'RQL': (0.5, 0.866, 0), 'TOP': (0, -0.01, 1), 'BOT': (0, -0.01, -1)}
for v in S['views']:
    c = Vector(v['center']); dv = Vector(DIRS[v['dir']]).normalized(); pos = c + dv * 10
    co.location = pos; co.rotation_euler = (c - pos).to_track_quat('-Z', 'Y').to_euler(); cam.ortho_scale = v['scale']
    sc.render.resolution_x = v.get('rx', 800); sc.render.resolution_y = v.get('ry', 1000)
    sc.render.filepath = S['out'] + '_' + v['name'] + '.png'; bpy.ops.render.render(write_still=True)
'''
tmp = tempfile.mkdtemp(); bp = os.path.join(tmp, 'r.py'); open(bp, 'w').write(BL); sp = os.path.join(tmp, 's.json'); json.dump(spec, open(sp, 'w'))
r = subprocess.run([sys.executable, bp, '--', sp], capture_output=True, text=True)
if r.returncode: print(r.stdout[-2000:], r.stderr[-2000:]); sys.exit(1)
print(json.dumps([spec['out'] + '_' + v['name'] + '.png' for v in spec['views']]))
