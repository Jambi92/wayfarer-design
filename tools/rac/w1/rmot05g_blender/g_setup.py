# RAC RM-OT-05G — Gorrund hand-sculpt Blender SCENE SETUP (run inside Blender; tested with the bpy module 4.2.0 LTS and 5.0.1).
#
#   GUI:  Blender > Scripting > Open this file > Run Script      (package root found automatically; else set PACKAGE_ROOT below)
#   CLI:  blender --background --python g_setup.py -- --package <handoff dir> --out <working .blend>
#
# What it builds (nothing is written into the frozen package; the scene is saved where you choose):
#   GO_SOURCE_REFERENCE   immutable source (hidden, unselectable, transforms locked)          collection REF_LOCKED_NO_EXPORT
#   GO_SCULPT_BASE        the ONLY editable / exported object (transforms locked at identity)  collection SCULPT_EXPORT
#   GO_true_floor, GO_old_lean, GO_low_route            guide meshes, unselectable          collection GUIDES_NO_EXPORT
#   JOINT_* empties, GROUND plane, STATURE_230.90 marker                                     collection OVERLAYS_NO_EXPORT
#   GO_VIEW_ANATOMICAL    linked display duplicate mirrored to the 05D/05E sheet convention   collection VIEW_NO_EXPORT
#   CAM_F / CAM_Q / CAM_P / CAM_RQ  orthographic sheet cameras (g_views.py renders them)
# The source OBJ is parsed by this script in file order (no importer, no split / merge / sort), so vertex i of GO_SCULPT_BASE is template
# vertex i and every face keeps its order and winding. Each vertex carries:
#   rac_src_index (INT)       its template index  -> the exporter refuses any mesh where this is not exactly 0..13379 in order
#   rac_src_co   (FLOAT_VECTOR) its template position -> preflight displacement checks inside Blender
# Vertex groups: NO_TOUCH_head_neck, NO_TOUCH_hands_digits, NO_TOUCH_toes_forefoot, NO_TOUCH_all, FAM_A ... FAM_F (editing jurisdiction only).
# Sculpt mask: NO_TOUCH_all is written as the sculpt mask (masked = protected). Masks are editing AIDS; the numeric checks enforce the contract.
# Colour attribute rac_regions shows the families / no-touch zones (Solid shading > Attribute).  No coordinate is changed by any of this.
import bpy, os, sys, json, hashlib, math
REMASK_ONLY = False          # True: only re-install the sculpt mask from NO_TOUCH_all on the existing GO_SCULPT_BASE (no other change)
PACKAGE_ROOT = None          # set to the handoff folder (".../rac-rmot05f-handoff") if auto-detection fails
NV = 13380
FAM_COL = {'FAM_A': (0.12, 0.47, 0.71), 'FAM_B': (0.84, 0.15, 0.16), 'FAM_C': (0.58, 0.40, 0.74), 'FAM_D': (0.17, 0.63, 0.17),
           'FAM_E': (1.0, 0.50, 0.05), 'FAM_F': (0.09, 0.75, 0.81)}
REGION_MAP = {'A_trunk_section_S2_S5': 'FAM_A', 'B_posterior_axial_load_path': 'FAM_B', 'C_pelvis_to_thigh': 'FAM_C', 'D_knee_shank_ankle': 'FAM_D',
              'E_elbow_forearm_wrist': 'FAM_E', 'F_shoulder_girdle_neck_root': 'FAM_F', 'NO_TOUCH_head_neck': 'NO_TOUCH_head_neck',
              'NO_TOUCH_hands_digits': 'NO_TOUCH_hands_digits', 'NO_TOUCH_toes_forefoot': 'NO_TOUCH_toes_forefoot'}
# 05D / 05E sheet cameras (ot05r_package.VIEWS, rclose.py): name, yaw, elevation; ortho scale 250, ground 120 cm below the target
VIEWS = (('F', 0, 0), ('Q', 35, 6), ('P', 90, 0), ('RQ', 145, 6))

def args():
    a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
    d = {}
    for i, k in enumerate(a):
        if k.startswith('--'): d[k[2:]] = a[i + 1] if i + 1 < len(a) and not a[i + 1].startswith('--') else True
    return d

def package_root(d):
    if d.get('package'): return os.path.abspath(d['package'])
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
    raise RuntimeError('package root not found: set PACKAGE_ROOT at the top of g_setup.py to the rac-rmot05f-handoff folder')

def sha256(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()

def parse_obj(p):
    """strict source-order parser: 'v x y z' and 'f a b c' (1-based, optional /vt/vn ignored); no reordering, merging or splitting"""
    V, F = [], []
    with open(p) as fh:
        for ln in fh:
            if ln.startswith('v '):
                x = ln.split(); V.append((float(x[1]), float(x[2]), float(x[3])))
            elif ln.startswith('f '):
                F.append(tuple(int(t.split('/')[0]) - 1 for t in ln.split()[1:]))
    return V, F

def make_mesh(name, V, F):
    me = bpy.data.meshes.new(name)
    me.from_pydata(V, [], F)                     # vertices and polygons are created in the given order; loops keep the given winding
    me.validate(verbose=False, clean_customdata=False)
    if len(me.vertices) != len(V) or len(me.polygons) != len(F): raise RuntimeError('mesh construction changed the element count of ' + name)
    return me

def coll(name, parent=None):
    c = bpy.data.collections.get(name) or bpy.data.collections.new(name)
    if c.name not in (parent or bpy.context.scene.collection).children: (parent or bpy.context.scene.collection).children.link(c)
    return c

def lock(ob, selectable=True):
    ob.lock_location = ob.lock_rotation = ob.lock_scale = (True, True, True)
    ob.lock_rotation_w = True
    ob.hide_select = not selectable

def mat(name, rgba):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name); m.diffuse_color = rgba; return m

def setup(root, out=None):
    tpl = os.path.join(root, 'template', 'GO_ref_route_r6.obj')
    V, F = parse_obj(tpl)
    if len(V) != NV: raise RuntimeError('template has %d vertices, expected %d' % (len(V), NV))
    regions = json.load(open(os.path.join(root, 'data', 'regions.json')))['regions']
    joints = json.load(open(os.path.join(root, 'data', 'joints_r6.json')))['joints']
    for ob in list(bpy.data.objects): bpy.data.objects.remove(ob, do_unlink=True)
    sc = bpy.context.scene
    sc.unit_settings.system = 'NONE'; sc.unit_settings.scale_length = 1.0          # 1 Blender unit = 1 cm; no unit conversion anywhere
    # immutable reference + editable base, both built from the same parse
    cr = coll('REF_LOCKED_NO_EXPORT'); cs = coll('SCULPT_EXPORT'); cg = coll('GUIDES_NO_EXPORT'); co = coll('OVERLAYS_NO_EXPORT'); cv = coll('VIEW_NO_EXPORT')
    ref = bpy.data.objects.new('GO_SOURCE_REFERENCE', make_mesh('GO_SOURCE_REFERENCE', V, F)); cr.objects.link(ref); lock(ref, False)
    ref.hide_set(True); ref.hide_render = True; cr.hide_render = True
    me = make_mesh('GO_SCULPT_BASE', V, F); base = bpy.data.objects.new('GO_SCULPT_BASE', me); cs.objects.link(base); lock(base, True)
    for m_ in (me, ref.data):
        a = m_.attributes.new('rac_src_index', 'INT', 'POINT'); a.data.foreach_set('value', list(range(NV)))
        b = m_.attributes.new('rac_src_co', 'FLOAT_VECTOR', 'POINT'); b.data.foreach_set('vector', [c for v in V for c in v])
    me['rac_template_sha256'] = sha256(tpl); me['rac_template_path'] = 'template/GO_ref_route_r6.obj'; me['rac_n_vertices'] = NV; me['rac_n_faces'] = len(F)
    me['rac_contract'] = 'RM-OT-05G: move existing vertices only; export with g_export.py; units cm, Z up, +Y anterior, +X body left'
    # vertex groups + sculpt mask + region colours
    allnt = set()
    for k, ix in regions.items():
        g = base.vertex_groups.new(name=REGION_MAP[k]); g.add(ix, 1.0, 'REPLACE')
        if k.startswith('NO_TOUCH'): allnt.update(ix)
    g = base.vertex_groups.new(name='NO_TOUCH_all'); g.add(sorted(allnt), 1.0, 'REPLACE')
    mask = [0.0] * NV
    for i in allnt: mask[i] = 1.0
    try:
        ma = me.attributes.get('.sculpt_mask') or me.attributes.new('.sculpt_mask', 'FLOAT', 'POINT'); ma.data.foreach_set('value', mask); mask_kind = '.sculpt_mask attribute'
    except Exception as ex:
        mask_kind = 'not installed (%s): use Sculpt > Mask > from vertex group NO_TOUCH_all' % ex
    col = [0.78, 0.78, 0.80, 1.0] * NV
    for k, ix in regions.items():
        c = (0.18, 0.18, 0.18) if k.startswith('NO_TOUCH') else FAM_COL[REGION_MAP[k]]
        for i in ix: col[4 * i:4 * i + 3] = c
    ca = me.color_attributes.new('rac_regions', 'FLOAT_COLOR', 'POINT'); ca.data.foreach_set('color', col)
    me.polygons.foreach_set('use_smooth', [True] * len(F))
    base.data.materials.append(mat('RAC_neutral_grey', (0.66, 0.66, 0.68, 1.0)))
    # guides (unselectable, never exported)
    for fn, nm, rgba in (('GO_true_floor_r6.obj', 'GO_true_floor', (0.1, 0.35, 0.9, 0.35)), ('GO_old_lean_r6.obj', 'GO_old_lean', (0.85, 0.15, 0.15, 0.25)),
                         ('GO_low_route_r6.obj', 'GO_low_route', (0.2, 0.7, 0.3, 0.25))):
        Vg, Fg = parse_obj(os.path.join(root, 'template', fn))
        o = bpy.data.objects.new(nm, make_mesh(nm, Vg, Fg)); cg.objects.link(o); lock(o, False); o.display_type = 'WIRE'; o.hide_set(True); o.hide_render = True
        o.data.materials.append(mat('RAC_' + nm, rgba))
    # overlays: joint heads, ground, stature marker (never exported)
    for jn, (h, t) in joints.items():
        if jn in ('Root',) or jn.startswith(('index', 'middle', 'pinky', 'ring', 'thumb')): continue
        e = bpy.data.objects.new('JOINT_' + jn, None); e.empty_display_type = 'SPHERE'; e.empty_display_size = 1.5; e.location = h; co.objects.link(e); lock(e, False)
    gp = bpy.data.objects.new('GROUND_z0', None); gp.empty_display_type = 'CIRCLE'; gp.empty_display_size = 60; co.objects.link(gp); lock(gp, False)
    st = bpy.data.objects.new('STATURE_230.90', None); st.empty_display_type = 'SINGLE_ARROW'; st.empty_display_size = 10
    st.location = (0, 0, max(v[2] for v in V)); co.objects.link(st); lock(st, False)
    # anatomical (sheet-convention) display duplicate: SAME mesh data, object scale y = -1 (05D/05E rclose.py renders y = -f).
    vw = bpy.data.objects.new('GO_VIEW_ANATOMICAL', me); cv.objects.link(vw); vw.scale = (1, -1, 1); lock(vw, False); vw.hide_set(True)
    mk = vw.modifiers.new('VIEW_hide_head_neck', 'MASK'); mk.vertex_group = 'NO_TOUCH_head_neck'; mk.invert_vertex_group = True
    cv.hide_render = False; vw.hide_render = True
    # sheet cameras (target the anatomical duplicate, rclose.py geometry)
    ys = [-v[1] for i, v in enumerate(V)]; cf = 0.5 * (min(ys) + max(ys)); tgt = (0.0, cf, 250.0 / 2 - 5)
    from mathutils import Vector
    for nm, yaw, el in VIEWS:
        cd = bpy.data.cameras.get('CAM_' + nm) or bpy.data.cameras.new('CAM_' + nm); cd.type = 'ORTHO'; cd.ortho_scale = 250.0; cd.clip_end = 5000
        cam = bpy.data.objects.new('CAM_' + nm, cd); cv.objects.link(cam)
        a, e = math.radians(yaw), math.radians(el); d = Vector((math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), math.sin(e)))
        cam.location = Vector(tgt) + d * 1500; cam.rotation_euler = (-d).to_track_quat('-Z', 'Y').to_euler(); lock(cam, False)
    sc.camera = bpy.data.objects['CAM_F']
    sc.render.engine = 'BLENDER_WORKBENCH'; sc.display.shading.light = 'STUDIO'; sc.display.shading.color_type = 'SINGLE'
    sc.display.shading.single_color = (0.66, 0.66, 0.68); sc.render.resolution_x = sc.render.resolution_y = 750; sc.render.film_transparent = True
    # select only the base
    for o in bpy.data.objects: o.select_set(False)
    base.select_set(True); bpy.context.view_layer.objects.active = base
    sc['rac_setup'] = json.dumps({'blender': bpy.app.version_string, 'template_sha256': sha256(tpl), 'regions_sha256': sha256(os.path.join(root, 'data', 'regions.json')),
                                  'joints_sha256': sha256(os.path.join(root, 'data', 'joints_r6.json')), 'sculpt_mask': mask_kind, 'script': 'g_setup.py RM-OT-05G'})
    if out: bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(out))
    return {'blender': bpy.app.version_string, 'vertices': len(me.vertices), 'faces': len(me.polygons), 'sculpt_mask': mask_kind, 'saved': out}

def remask():
    """re-install the sculpt mask (1 = protected) from vertex group NO_TOUCH_all; coordinates are not touched"""
    base = bpy.data.objects['GO_SCULPT_BASE']; me = base.data; gi = base.vertex_groups['NO_TOUCH_all'].index
    if base.mode != 'OBJECT': bpy.ops.object.mode_set(mode='OBJECT')
    mask = [1.0 if any(g.group == gi and g.weight > 0.5 for g in v.groups) else 0.0 for v in me.vertices]
    ma = me.attributes.get('.sculpt_mask') or me.attributes.new('.sculpt_mask', 'FLOAT', 'POINT'); ma.data.foreach_set('value', mask); me.update()
    return {'masked_vertices': int(sum(mask))}

if __name__ == '__main__':
    d = args()
    if REMASK_ONLY or d.get('remask'): print('RAC_REMASK', json.dumps(remask()))
    else: print('RAC_SETUP', json.dumps(setup(package_root(d), d.get('out'))))
