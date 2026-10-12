# RAC RM-OT-05G — MATCHED VIEW CAPTURES in Blender (run inside a scene made by g_setup.py).
#
#   GUI:  Scripting > Open g_views.py > Run Script          -> PNGs in <blend folder>/views/
#   CLI:  blender --background <working.blend> --python g_views.py -- [--outdir <dir>] [--previews]
#
# Renders front (F), front 3/4 (Q), profile (P) and rear 3/4 (RQ) with the 05D / 05E sheet geometry (rclose.py: orthographic, scale 250 cm,
# ground 120 cm below frame centre, yaw 0 / 35 / 90 / 145, elevation 0 / 6 / 0 / 6, Workbench studio light, neutral grey 0.66 / 0.66 / 0.68
# with cavity, transparent background, 750 px), in neutral grey and black silhouette, body only: head and neck are hidden by a MASK modifier
# on the display object, no vertex is deleted. The display object GO_VIEW_ANATOMICAL shares GO_SCULPT_BASE's mesh, mirrored y -> -y as the
# sheets are (the package data is +Y anterior / +X body left; the sheets show the anatomically correct, non-mirrored body).
# --previews also renders PREVIEW_low / narrow / broad (from g_preview.py) the same way.
# These captures are for the delivery record and for side-by-side comparison with the evidence sheets; they are not an acceptance test.
import bpy, os, sys
def outdir():
    if '--outdir' in sys.argv: return os.path.abspath(sys.argv[sys.argv.index('--outdir') + 1])
    return os.path.join(os.path.dirname(bpy.data.filepath) if bpy.data.filepath else os.getcwd(), 'views')
def render_object(ob, tag, od):
    sc = bpy.context.scene; sh = sc.display.shading
    keep = {o.name: o.hide_render for o in bpy.data.objects}
    for o in bpy.data.objects: o.hide_render = True
    loc, scl = tuple(ob.location), tuple(ob.scale); lk = (tuple(ob.lock_location), tuple(ob.lock_scale))
    ob.lock_location = ob.lock_scale = (False, False, False); ob.location = (0, 0, 0); ob.scale = (1, -1, 1); ob.hide_render = False
    tmp = None
    if not any(m.type == 'MASK' for m in ob.modifiers):
        tmp = ob.modifiers.new('TMP_hide_head_neck', 'MASK'); tmp.vertex_group = 'NO_TOUCH_head_neck'; tmp.invert_vertex_group = True
    files = []
    try:
        for mode in ('grey', 'sil'):
            sc.render.engine = 'BLENDER_WORKBENCH'; sc.render.film_transparent = True; sc.render.resolution_x = sc.render.resolution_y = 750
            sh.color_type = 'SINGLE'
            if mode == 'grey': sh.light = 'STUDIO'; sh.single_color = (0.66, 0.66, 0.68); sh.show_cavity = True; sh.cavity_type = 'BOTH'
            else: sh.light = 'FLAT'; sh.single_color = (0.0, 0.0, 0.0); sh.show_cavity = False
            for v in ('F', 'Q', 'P', 'RQ'):
                sc.camera = bpy.data.objects['CAM_' + v]; fn = os.path.join(od, '%s_%s_%s.png' % (tag, v, mode)); sc.render.filepath = fn
                bpy.ops.render.render(write_still=True); files.append(fn)
    finally:
        if tmp: ob.modifiers.remove(tmp)
        ob.location, ob.scale = loc, scl; ob.lock_location, ob.lock_scale = lk
        for o in bpy.data.objects: o.hide_render = keep.get(o.name, True)
    return files
if __name__ == '__main__':
    od = outdir(); os.makedirs(od, exist_ok=True); out = []
    vw = bpy.data.objects['GO_VIEW_ANATOMICAL']
    vw.hide_render = False; out += render_object(vw, 'GO_SCULPT_BASE', od); vw.hide_render = True
    if '--previews' in sys.argv:
        for st in ('low', 'narrow', 'broad'):
            ob = bpy.data.objects.get('PREVIEW_' + st)
            if ob: out += render_object(ob, 'PREVIEW_' + st, od)
    print('RAC_VIEWS', len(out), od)
