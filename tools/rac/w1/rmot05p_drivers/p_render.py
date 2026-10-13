# RM-OT-05P review renderer: identical camera + material for every body, orthographic, workbench grey.
#   --mode real     : one fixed ortho scale (cm) and ground line for all bodies, 10 cm grid labelled in real cm
#   --mode matched  : each body scaled to its own visible height (matched display stature; labelled as such)
# Views: front (camera +Y, image right = -X), profile (camera +X, anterior to the right), rear, q34 (front-left 3/4),
# rq34 (rear 3/4). Optional --headcut Z removes faces wholly above Z (body-only); optional --marks JSON {label: [[x,y,z],..]}
# draws landmarks / axes. Usage:
#   python3 p_render.py --out OUT.png --mode real --views front,profile,rear,q34 --items "LABEL=mesh.obj[@headcut]" ... [--marks m.json]
import argparse, json, math, os, sys, tempfile, subprocess, numpy as np
from PIL import Image, ImageDraw
ap = argparse.ArgumentParser(); ap.add_argument('--out', required=True); ap.add_argument('--mode', default='real'); ap.add_argument('--views', default='front,profile,rear,q34')
ap.add_argument('--items', nargs='+', required=True); ap.add_argument('--marks', default=None); ap.add_argument('--scale', type=float, default=262.0)
ap.add_argument('--zlo', type=float, default=None); ap.add_argument('--zhi', type=float, default=None); ap.add_argument('--res', type=int, default=900)
ap.add_argument('--title', default=''); ap.add_argument('--aspect', type=float, default=0.62); a = ap.parse_args()
YAW = {'front': 180, 'profile': 90, 'rear': 0, 'q34': 145, 'rq34': 35, 'lprofile': 270}
BLENDER = r'''
import bpy, sys, json, math, numpy as np
from mathutils import Vector
args = json.loads(sys.argv[sys.argv.index('--') + 1])
V = np.array([[float(t) for t in l.split()[1:4]] for l in open(args['mesh']) if l.startswith('v ')])
F = [[int(t.split('/')[0]) - 1 for t in l.split()[1:]] for l in open(args['mesh']) if l.startswith('f ')]
if args.get('cut') is not None:
    F = [f for f in F if min(V[i][2] for i in f) <= args['cut']]
bpy.ops.wm.read_factory_settings(use_empty=True)
me = bpy.data.meshes.new('b'); me.from_pydata(V.tolist(), [], F); me.update(); ob = bpy.data.objects.new('b', me); bpy.context.scene.collection.objects.link(ob)
for p in me.polygons: p.use_smooth = True
sc = bpy.context.scene; sc.render.engine = 'BLENDER_WORKBENCH'; sh = sc.display.shading
sh.light = 'STUDIO'; sh.color_type = 'SINGLE'; sh.single_color = (0.66, 0.66, 0.68); sh.show_cavity = True; sh.cavity_type = 'BOTH'
sc.render.resolution_x = args['w']; sc.render.resolution_y = args['h']; sc.world = bpy.data.worlds.new('w'); sc.render.film_transparent = True
cam = bpy.data.cameras.new('c'); cam.type = 'ORTHO'; cam.clip_start = 1; cam.clip_end = 5000; cam.ortho_scale = args['scale']
co = bpy.data.objects.new('c', cam); sc.collection.objects.link(co); sc.camera = co; c = Vector(args['center'])
for yaw, fn in args['shots']:
    t = math.radians(yaw); p = c + Vector((1000 * math.sin(t), -1000 * math.cos(t), 0))
    co.location = p; co.rotation_euler = (c - p).to_track_quat('-Z', 'Y').to_euler(); sc.render.filepath = fn; bpy.ops.render.render(write_still=True)
'''
tmp = tempfile.mkdtemp(); bs = os.path.join(tmp, 'b.py'); open(bs, 'w').write(BLENDER)
views = a.views.split(','); W, Hh = int(a.res * a.aspect), a.res
marks = json.load(open(a.marks)) if a.marks else {}
cols = []
for it in a.items:
    lab, spec = it.split('=', 1); mesh, cut = (spec.split('@') + [None])[:2]; cut = float(cut) if cut else None
    V = np.array([[float(t) for t in l.split()[1:4]] for l in open(mesh) if l.startswith('v ')]); keep = V if cut is None else V[V[:, 2] <= cut]
    if a.mode == 'real':
        zlo = 0.0 if a.zlo is None else a.zlo; zhi = a.scale if a.zhi is None else a.zhi; scale = zhi - zlo
        center = [0.0, 0.0, (zlo + zhi) / 2]
    else:
        zlo, zhi = keep[:, 2].min(), keep[:, 2].max(); scale = (zhi - zlo) * 1.06; center = [0.0, 0.0, (zlo + zhi) / 2]
    shots = [(YAW[v], os.path.join(tmp, '%s_%s.png' % (len(cols), v))) for v in views]
    subprocess.run([sys.executable, '-c', 'import runpy,sys; sys.argv=["x","--",%r]; runpy.run_path(%r)' % (json.dumps(dict(mesh=mesh, cut=cut, w=W, h=Hh, scale=scale * max(1.0, W / Hh), center=center, shots=shots)), bs)], check=True, capture_output=True)
    ppc = Hh / scale; tiles = []
    for (yaw, fn), v in zip(shots, views):
        im = Image.new('RGB', (W, Hh), (52, 52, 56)); d = ImageDraw.Draw(im)
        t = math.radians(yaw); right = np.array([math.cos(t), math.sin(t), 0.0])
        def proj(p): q = np.array(p) - center; return (W / 2 + q @ right * ppc, Hh / 2 - q[2] * ppc)
        if a.mode == 'real':
            for zc in range(int(zlo // 10 * 10), int(zhi) + 1, 10):
                y = proj([0, 0, zc])[1]; d.line([(0, y), (W, y)], fill=(78, 78, 88) if zc % 50 else (130, 100, 100)); d.text((2, y - 11), str(zc), fill=(200, 200, 120))
        r = Image.open(fn).convert('RGBA'); im.paste(r, (0, 0), r); d = ImageDraw.Draw(im)
        for ml, pts in marks.get(lab, {}).items():
            P = [proj(p) for p in pts]; col = (255, 90, 60) if 'axis' in ml else (90, 220, 120)
            if len(P) > 1: d.line(P, fill=col, width=2)
            for x, y in P: d.ellipse([x - 4, y - 4, x + 4, y + 4], outline=col, width=2)
        d.text((6, Hh - 18), '%s | %s | %s' % (lab, v, 'REAL SCALE (cm grid)' if a.mode == 'real' else 'MATCHED DISPLAY STATURE (each body normalized)'), fill=(235, 235, 235))
        tiles.append(im)
    cols.append(tiles)
N = len(cols); Wt = W * len(views); S = Image.new('RGB', (Wt, Hh * N + (30 if a.title else 0)), (30, 30, 34)); dd = ImageDraw.Draw(S)
if a.title: dd.text((8, 8), a.title, fill=(240, 240, 240))
for i, tiles in enumerate(cols):
    for j, t in enumerate(tiles): S.paste(t, (j * W, i * Hh + (30 if a.title else 0)))
S.save(a.out, quality=90) if a.out.endswith('.jpg') else S.save(a.out); print(a.out, S.size)
