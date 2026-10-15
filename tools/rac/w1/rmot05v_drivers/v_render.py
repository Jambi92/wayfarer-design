# RM-OT-05V evidence renders (read-only): front + profile + back workbench renders of a list of states, plus a labelled contact sheet.
# INFERRED faces (rac fgrp != 0) are tinted so the reconstruction is always visible as reconstruction.
# Usage: python3 v_render.py OUT.jpg LABEL=STATE.npz [LABEL=STATE.npz ...]
import sys, os, json, subprocess, tempfile, numpy as np
from PIL import Image, ImageDraw, ImageFont
out = sys.argv[1]; items = [a.split('=', 1) for a in sys.argv[2:]]; tmp = tempfile.mkdtemp()
BL = r'''
import bpy, sys, json, numpy as np
from mathutils import Vector
A = json.loads(sys.argv[sys.argv.index('--') + 1]); d = np.load(A['npz']); V, F = d['V'].astype(np.float32), d['F']
fg = d['fgrp'] if 'fgrp' in d.files else np.zeros(len(F), np.int8)
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
me = bpy.data.meshes.new('b'); me.vertices.add(len(V)); me.vertices.foreach_set('co', V.ravel())
me.loops.add(F.size); me.loops.foreach_set('vertex_index', F.ravel().astype(np.int32)); me.polygons.add(len(F))
me.polygons.foreach_set('loop_start', (np.arange(len(F)) * 3).astype(np.int32)); me.update()
me.polygons.foreach_set('use_smooth', np.ones(len(F), bool))
for nm, col in (('src', (0.62, 0.62, 0.62, 1)), ('inf', (0.80, 0.62, 0.45, 1))):
    m = bpy.data.materials.new(nm); m.diffuse_color = col; me.materials.append(m)
me.polygons.foreach_set('material_index', (fg != 0).astype(np.int32))
ob = bpy.data.objects.new('b', me); sc.collection.objects.link(ob)
sc.render.engine = 'BLENDER_WORKBENCH'; sc.display.shading.light = 'STUDIO'; sc.display.shading.color_type = 'MATERIAL'
sc.render.film_transparent = True; sc.render.resolution_x = 600; sc.render.resolution_y = 900
cam = bpy.data.cameras.new('c'); cam.type = 'ORTHO'; cam.ortho_scale = 260.0; co = bpy.data.objects.new('c', cam); sc.collection.objects.link(co); sc.camera = co
c = Vector((-0.5, -5.0, 120.0))
for name, pos in (('F', (-0.5, 400, 120)), ('P', (400, -5, 120)), ('B', (-0.5, -400, 120))):
    co.location = pos; co.rotation_euler = (c - Vector(pos)).to_track_quat('-Z', 'Y').to_euler()
    sc.render.filepath = A['out'] + '_' + name + '.png'; bpy.ops.render.render(write_still=True)
'''
bp = os.path.join(tmp, 'r.py'); open(bp, 'w').write(BL)
try: font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 20)
except Exception: font = ImageFont.load_default()
cols = []
for lab, st in items:
    o = os.path.join(tmp, lab); subprocess.run([sys.executable, bp, '--', json.dumps(dict(npz=st, out=o))], check=True, capture_output=True)
    cols.append((lab, [Image.open(o + '_' + v + '.png').convert('RGBA') for v in 'FPB']))
w, h = 600, 900; sheet = Image.new('RGB', (w * 3, (h + 40) * len(cols)), 'white'); dr = ImageDraw.Draw(sheet)
for r, (lab, ims) in enumerate(cols):
    for k, im in enumerate(ims): sheet.paste(im, (k * w, r * (h + 40) + 40), im)
    dr.text((10, r * (h + 40) + 8), lab + '   (front / profile / back; tan = INFERRED reconstruction)', font=font, fill='black')
sheet.save(out, quality=88); print(json.dumps(dict(out=out, rows=[l for l, _ in cols])))
