# render_attr.py (bpy module) -- MESH.npz COLORS.npy OUTDIR TAG VIEWSPEC [WIRE 0|1] [PX]
# Orthographic render (v005 analysis source frame, cm) with per-vertex (n_v x 3) or per-face (n_f x 3) RGB colours in 0..1.
# Derived inspection scene only (never saved). VIEWSPEC as render.py: name:dx,df,du:cx,cf,cu:halfsize ; ...
import bpy, sys, os, json, numpy as np, mathutils
a = sys.argv[sys.argv.index('--') + 1:]
src, cf, O, TAG, VS = a[:5]; WIRE = len(a) > 5 and a[5] == '1'; PX = int(a[6]) if len(a) > 6 else 800
z = np.load(src); V = z['V'].astype(float); F = np.asarray(z['Q']); Cc = np.load(cf).astype(np.float32)
bpy.ops.wm.read_factory_settings(use_empty=True)
P = np.c_[V[:, 0], -V[:, 1], V[:, 2]] / 100
me = bpy.data.meshes.new('m'); me.from_pydata(P.tolist(), [], F.tolist()); me.update()
ob = bpy.data.objects.new('m', me); bpy.context.scene.collection.objects.link(ob); me.polygons.foreach_set('use_smooth', [True] * len(me.polygons))
lv = np.empty(len(me.loops), np.int32); me.loops.foreach_get('vertex_index', lv)
if len(Cc) == len(V): rgba = np.c_[Cc[lv], np.ones(len(lv))]
else:
    lp = np.repeat(np.arange(len(me.polygons)), [p.loop_total for p in me.polygons]); rgba = np.c_[Cc[lp], np.ones(len(lv))]
ca = me.color_attributes.new('c', 'FLOAT_COLOR', 'CORNER'); ca.data.foreach_set('color', rgba.astype(np.float32).ravel())
sc = bpy.context.scene; sc.render.engine = 'BLENDER_WORKBENCH'; sh = sc.display.shading; sh.light = 'STUDIO'; sh.show_specular_highlight = False; sh.color_type = 'VERTEX'
if os.environ.get('RENDER_REVEAL', '0') == '1':      # optional volume-revealing shading (inert by default): cavity (ridge / valley + curvature) on the studio light,
    sh.show_cavity = True; sh.cavity_type = 'BOTH'; sh.cavity_ridge_factor = 1.3; sh.cavity_valley_factor = 1.6; sh.curvature_ridge_factor = 1.2; sh.curvature_valley_factor = 1.4
    if os.environ.get('RENDER_SHADOWS', '0') == '1':   # + optional cast shadows (fixed light direction)
        sh.show_shadows = True; sh.shadow_intensity = 0.5; sc.display.light_direction = (0.45, -0.35, 0.82); sc.display.shadow_shift = 0.25
if os.environ.get('RENDER_LIGHTING'):              # optional inspection lighting (inert by default): STUDIO:<name>[:rotz_deg] grazing studio light, MATCAP:<name> reflection matcap;
    lt = os.environ['RENDER_LIGHTING'].split(':')    # RENDER_SPEC=1 adds the specular highlight
    if lt[0] == 'MATCAP': sh.light = 'MATCAP'; sh.studio_light = lt[1]
    else:
        sh.light = 'STUDIO'; sh.studio_light = lt[1]; sh.use_world_space_lighting = len(lt) > 2; sh.studiolight_rotate_z = float(lt[2]) * np.pi / 180 if len(lt) > 2 else 0.0
    sh.show_specular_highlight = os.environ.get('RENDER_SPEC', '0') == '1'
if WIRE:
    w = ob.copy(); w.data = ob.data.copy(); sc.collection.objects.link(w); md = w.modifiers.new('wf', 'WIREFRAME'); md.thickness = float(os.environ.get('WIRE_T', '0.0005')); md.use_replace = True
    wc = w.data.color_attributes['c']; wc.data.foreach_set('color', np.tile([0.1, 0.1, 0.14, 1.0], len(wc.data)).astype(np.float32))
sc.world = bpy.data.worlds.new('w'); sc.world.color = (1, 1, 1)
cam = bpy.data.cameras.new('c'); cam.type = 'ORTHO'; co_ = bpy.data.objects.new('c', cam); sc.collection.objects.link(co_); sc.camera = co_
sc.render.resolution_x = sc.render.resolution_y = PX
B = lambda v: np.array([v[0], -v[1], v[2]])
for spec in VS.split(';'):
    nm, d, c, h = spec.split(':'); d = np.array([float(v) for v in d.split(',')]); d /= np.linalg.norm(d); c = np.array([float(v) for v in c.split(',')]); h = float(h)
    up = np.array([0, 0, 1.0]) if abs(d[2]) < 0.9 else np.array([0, 1.0, 0]); y = up - (up @ d) * d; y /= np.linalg.norm(y)
    xb = np.cross(B(y), B(d)); M = mathutils.Matrix([list(xb), list(B(y)), list(B(d))]).transposed()
    co_.matrix_world = mathutils.Matrix.Translation(mathutils.Vector(B(c + d * 150) / 100)) @ M.to_4x4(); cam.ortho_scale = 2 * h / 100; cam.clip_end = 10
    sc.render.filepath = '%s/%s_%s.png' % (O, TAG, nm); bpy.ops.render.render(write_still=True)
    json.dump(dict(c=c.tolist(), x=[xb[0], -xb[1], xb[2]], y=y.tolist(), d=d.tolist(), h=h, px=PX), open('%s/%s_%s.json' % (O, TAG, nm), 'w'))
