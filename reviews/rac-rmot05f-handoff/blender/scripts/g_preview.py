# RAC RM-OT-05G — PERSISTENCE PREVIEW in Blender (run inside a scene made by g_setup.py, after / while sculpting).
#
#   GUI:  Scripting > Open g_preview.py > Run Script              (re-run any time to refresh from the current GO_SCULPT_BASE)
#   CLI:  blender --background <working.blend> --python g_preview.py -- [--save]
#
# Builds PREVIEW_low / PREVIEW_narrow / PREVIEW_broad (collection PREVIEW_NO_EXPORT, unselectable, placed beside the base at x = +110 / +220
# / +330 cm) using the 05F transport exactly as the pipeline does before its guard:
#       preview = route_state + s * T @ (GO_SCULPT_BASE - template)            (data: blender/transport/*.npz, made by g_make_transport.py)
# low = muscle 0 / weight 0.5 composition; narrow / broad = the Frame extremes of the accepted route. It never scales the whole body and never
# invents shape: with an unedited base every preview equals its route mesh exactly. It does NOT apply the true-floor clamp or the
# volume-restoring layer (f_reentry does); it REPORTS how many preview vertices fall more than 0.2 cm inside that state's true floor, which
# is where the pipeline would clamp (= where a form would be lost at that state); 'new_inside_caused_by_sculpt' excludes the few
# places where the unedited route itself already touches its floor. Verified against the 05F pipeline: p90 difference <= 0.02 cm.
import bpy, os, sys, json
import numpy as np
PACKAGE_ROOT = None
NV = 13380
STATES = (('low', 110.0), ('narrow', 220.0), ('broad', 330.0))

def package_root():
    if '--' in sys.argv and '--package' in sys.argv: return os.path.abspath(sys.argv[sys.argv.index('--package') + 1])
    if PACKAGE_ROOT: return PACKAGE_ROOT
    cands = []
    try: cands.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    except NameError: pass
    if bpy.data.filepath: cands += [os.path.dirname(bpy.data.filepath), os.path.dirname(os.path.dirname(bpy.data.filepath))]
    for t in bpy.data.texts:
        if t.filepath: cands.append(os.path.dirname(os.path.dirname(bpy.path.abspath(t.filepath))))
    for c in cands:
        for r in (c, os.path.join(c, '..')):
            if os.path.exists(os.path.join(r, 'template', 'GO_ref_route_r6.obj')): return os.path.abspath(r)
    raise RuntimeError('package root not found: set PACKAGE_ROOT')

def parse_v(p):
    return np.array([[float(x) for x in ln.split()[1:4]] for ln in open(p) if ln.startswith('v ')], float)

def normals_out(V, F):
    n = np.zeros_like(V); fn = np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]])
    for k in range(3): np.add.at(n, F[:, k], fn)
    n /= np.maximum(np.linalg.norm(n, axis=1), 1e-9)[:, None]
    vol = np.einsum('ij,ij->i', V[F[:, 0]], np.cross(V[F[:, 1]], V[F[:, 2]])).sum() / 6.0
    return n if vol > 0 else -n

def preview(root):
    base = bpy.data.objects['GO_SCULPT_BASE']; me = base.data
    if bpy.context.object and bpy.context.object.mode != 'OBJECT': bpy.ops.object.mode_set(mode='OBJECT')
    co = np.zeros(3 * NV, np.float32); me.vertices.foreach_get('co', co); src = np.zeros(3 * NV, np.float32); me.attributes['rac_src_co'].data.foreach_get('vector', src)
    Dw = (co - src).reshape(-1, 3).astype(float)
    F = np.array([tuple(p.vertices) for p in me.polygons], int)
    regions = json.load(open(os.path.join(root, 'data', 'regions.json')))['regions']
    ext = np.zeros(NV, bool); ext[regions['NO_TOUCH_head_neck']] = True; ext[regions['NO_TOUCH_hands_digits']] = True
    c = bpy.data.collections.get('PREVIEW_NO_EXPORT') or bpy.data.collections.new('PREVIEW_NO_EXPORT')
    if c.name not in bpy.context.scene.collection.children: bpy.context.scene.collection.children.link(c)
    rep = {}
    for st, dx in STATES:
        tdir = os.path.join(root, 'blender', 'transport')
        Vr = parse_v(os.path.join(tdir, 'GO_%s_route_r6.obj' % st)); Fl = parse_v(os.path.join(tdir, 'GO_%s_true_floor_r6.obj' % st))
        tr = np.load(os.path.join(tdir, 'GO_%s_transport.npz' % st)); T, s = tr['T'].astype(float), tr['s'].astype(float)
        P = Vr + s[:, None] * np.einsum('nij,nj->ni', T, Dw)
        nF = normals_out(Fl, F); sd = np.einsum('ij,ij->i', P - Fl, nF); inside = (sd < -0.2) & ~ext
        route_inside = (np.einsum('ij,ij->i', Vr - Fl, nF) < -0.2) & ~ext          # where the unedited route already touches the floor
        nm = 'PREVIEW_' + st; ob = bpy.data.objects.get(nm)
        if ob is None:
            pm = bpy.data.meshes.new(nm); pm.from_pydata(P.tolist(), [], F.tolist()); pm.polygons.foreach_set('use_smooth', [True] * len(F))
            ob = bpy.data.objects.new(nm, pm); c.objects.link(ob)
            g = ob.vertex_groups.new(name='NO_TOUCH_head_neck'); g.add(regions['NO_TOUCH_head_neck'], 1.0, 'REPLACE')
            ob.lock_location = ob.lock_rotation = ob.lock_scale = (True, True, True)
        else:
            ob.data.vertices.foreach_set('co', P.astype(np.float32).ravel()); ob.data.update()
        ob.location = (dx, 0, 0); ob.hide_select = True; ob['rac_preview'] = 'transport preview (pre-guard, pre-volume) of GO_SCULPT_BASE at %s; not a body, never exported' % st
        rep[st] = {'vertices_inside_true_floor_by_0p2cm': int(inside.sum()), 'new_inside_caused_by_sculpt': int((inside & ~route_inside).sum()), 'max_displacement_cm': round(float(np.linalg.norm(P - Vr, axis=1).max()), 3)}
    bpy.context.view_layer.objects.active = base
    return rep

if __name__ == '__main__':
    r = preview(package_root()); print('RAC_PREVIEW', json.dumps(r))
    if '--save' in sys.argv: bpy.ops.wm.save_mainfile()
