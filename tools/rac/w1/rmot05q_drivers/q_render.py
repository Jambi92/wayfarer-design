# RM-OT-05Q close-up renderer (Blender workbench, orthographic, fixed cameras so before/after are pixel-registered).
#   --mesh M.obj [--labels L.npy]  per-face integer labels -> colours (0 untouched grey, 1 removed/garment red,
#                                   2 reconstructed blue, 3 seam band amber, 4 body-under-garment green, 5 ambiguous purple)
#   --box x0 x1 y0 y1 z0 z1         keep only faces with a vertex inside the box (crop)
#   --center x y z --scale S        ortho window (cm) centred on the point
#   --views yaw:pitch,...           yaw 0 = camera on -Y looking +Y (rear), 180 = front, 90 = camera on +X; pitch deg up
#   (labels 6-10: further inventory zone colours)
#   --wire 1                        overlay the triangle wireframe (dark)
#   --cut nx ny nz d                drop faces whose centroid is on the + side of plane n.x > d (cut-away / underside views)
import argparse, json, os, subprocess, tempfile, numpy as np, trimesh
from PIL import Image, ImageDraw
ap = argparse.ArgumentParser(); ap.add_argument('--mesh'); ap.add_argument('--labels'); ap.add_argument('--box', type=float, nargs=6)
ap.add_argument('--center', type=float, nargs=3); ap.add_argument('--scale', type=float, default=40); ap.add_argument('--views', default='180:0')
ap.add_argument('--wire', type=int, default=0); ap.add_argument('--cut', type=float, nargs=4); ap.add_argument('--res', type=int, default=700)
ap.add_argument('--out'); ap.add_argument('--title', default=''); a = ap.parse_args()
m = trimesh.load(a.mesh, process=False); V = np.asarray(m.vertices); F = np.asarray(m.faces)
lab = np.load(a.labels) if a.labels else np.zeros(len(F), int)
keep = np.ones(len(F), bool)
if a.box:
    b = a.box; inb = (V[:, 0] >= b[0]) & (V[:, 0] <= b[1]) & (V[:, 1] >= b[2]) & (V[:, 1] <= b[3]) & (V[:, 2] >= b[4]) & (V[:, 2] <= b[5]); keep &= inb[F].any(1)
if a.cut:
    n = np.array(a.cut[:3]); keep &= (V[F].mean(1) @ n) <= a.cut[3]
F = F[keep]; lab = lab[keep]; vi = np.unique(F); mp = -np.ones(len(V), int); mp[vi] = np.arange(len(vi)); F = mp[F]; V = V[vi]
PAL = np.array([[.66, .66, .68], [.85, .2, .15], [.2, .45, .9], [.95, .7, .1], [.25, .7, .3], [.6, .3, .75],
                [.1, .75, .75], [.9, .45, .6], [.55, .55, .2], [.95, .55, .25], [.45, .3, .2]])   # 6-10: extra inventory zones
tmp = tempfile.mkdtemp(); np.savez(os.path.join(tmp, 'm.npz'), V=V, F=F, C=PAL[lab])
BL = r'''
import bpy, sys, json, math, numpy as np
from mathutils import Vector
A = json.loads(sys.argv[sys.argv.index('--') + 1]); d = np.load(A['npz']); V, F, C = d['V'], d['F'], d['C']
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
def mk(name, wire):
    me = bpy.data.meshes.new(name); me.vertices.add(len(V)); me.vertices.foreach_set('co', V.ravel().astype(np.float32))
    me.loops.add(F.size); me.loops.foreach_set('vertex_index', F.ravel().astype(np.int32)); me.polygons.add(len(F))
    me.polygons.foreach_set('loop_start', (np.arange(len(F)) * 3).astype(np.int32)); me.update()
    at = me.color_attributes.new('c', 'FLOAT_COLOR', 'CORNER'); cc = np.ones((len(F), 3, 4), np.float32)
    cc[..., :3] = 0.08 if wire else np.repeat(C[:, None, :], 3, 1); at.data.foreach_set('color', cc.ravel()); me.color_attributes.active_color = at
    if not wire:
        me.polygons.foreach_set('use_smooth', np.ones(len(F), bool))
    ob = bpy.data.objects.new(name, me); sc.collection.objects.link(ob); return ob
mk('b', False)
if A['wire']:
    w = mk('w', True); md = w.modifiers.new('wf', 'WIREFRAME'); md.thickness = A['wt']; md.use_relative_offset = False; md.offset = 1.0
sc.render.engine = 'BLENDER_WORKBENCH'; sh = sc.display.shading; sh.light = 'STUDIO'; sh.color_type = 'VERTEX'; sh.show_cavity = True; sh.cavity_type = 'BOTH'
sc.render.resolution_x = sc.render.resolution_y = A['res']; sc.world = bpy.data.worlds.new('w'); sc.render.film_transparent = True
cam = bpy.data.cameras.new('c'); cam.type = 'ORTHO'; cam.ortho_scale = A['scale']; cam.clip_start = 0.1; cam.clip_end = 5000
co = bpy.data.objects.new('c', cam); sc.collection.objects.link(co); sc.camera = co; c = Vector(A['center'])
for i, (yaw, pit) in enumerate(A['views']):
    y, p = math.radians(yaw), math.radians(pit); dv = Vector((math.sin(y) * math.cos(p), -math.cos(y) * math.cos(p), math.sin(p)))
    co.location = c + dv * 1000; co.rotation_euler = (-dv).to_track_quat('-Z', 'Y').to_euler()
    sc.render.filepath = A['out'] + '_%d.png' % i; bpy.ops.render.render(write_still=True)
'''
open(os.path.join(tmp, 'b.py'), 'w').write(BL)
views = [tuple(float(t) for t in v.split(':')) for v in a.views.split(',')]
cen = a.center if a.center else list(V.mean(0))
arg = dict(npz=os.path.join(tmp, 'm.npz'), wire=a.wire, wt=a.scale / 1500.0, res=a.res, scale=a.scale, center=cen, views=views, out=os.path.join(tmp, 'r'))
import sys
subprocess.run([sys.executable, '-c', 'import runpy,sys; sys.argv=["x","--",%r]; runpy.run_path(%r)' % (json.dumps(arg), os.path.join(tmp, 'b.py'))], check=True, capture_output=True)
ims = [Image.open(os.path.join(tmp, 'r_%d.png' % i)).convert('RGBA') for i in range(len(views))]
W = Image.new('RGB', (a.res * len(ims), a.res + 30), (34, 35, 42)); dr = ImageDraw.Draw(W)
for i, im in enumerate(ims):
    bg = Image.new('RGBA', im.size, (34, 35, 42, 255)); bg.alpha_composite(im); W.paste(bg.convert('RGB'), (i * a.res, 30))
    dr.text((i * a.res + 6, 32), 'yaw %g pitch %g | window %g cm' % (views[i][0], views[i][1], a.scale), fill=(230, 230, 230))
dr.text((6, 8), a.title + ' | centre %s' % np.round(cen, 1).tolist(), fill=(240, 240, 240)); W.save(a.out); print(a.out, W.size)
