# RAC RM-OT-05G TOOLING VERIFICATION (not a sculpt): runs the Blender support scripts headless through the `bpy` module and records
#   R0  how Blender's own OBJ importer treats the template (vertex count / order / coordinates under default and Z-up/Y-forward axes)
#   R1  unedited round trip: g_setup -> save .blend -> reopen -> Edit / Sculpt mode enter + exit -> g_export -> compare every vertex and face
#       with the template (bit-exact text), no net rotation / translation / scale / stature / ground change; standalone preflight PASS
#   R2  vertex groups / sculpt mask installed from the exact regions.json source indices
#   N*  disposable negative fixtures that the exporter must REFUSE (no file written) and OBJ fixtures the preflight must FAIL
#   P   persistence preview: unedited base -> previews equal their route meshes; T1 tooling fixture -> agrees with the built 05F states
#   V   matched view captures render (8 PNGs, body only)
# Usage: python3 g_tests.py <package root> <out dir>         (out dir: tooling evidence, outside any sculpt-candidate namespace)
import os, sys, json, math, hashlib, importlib.util, shutil, random
import numpy as np, bpy, bmesh
HERE = os.path.dirname(os.path.abspath(__file__))
def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + '.py')); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
ROOT, OUT = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2]); os.makedirs(OUT, exist_ok=True)
SETUP, EXPORT, PRE, PREV, VIEWS = load('g_setup'), load('g_export'), load('g_preflight'), load('g_preview'), load('g_views')
TPL = os.path.join(ROOT, 'template', 'GO_ref_route_r6.obj'); BLEND = os.path.join(OUT, 'tooling_roundtrip.blend')
res = {'blender': bpy.app.version_string, 'package_root': ROOT, 'template_sha256': hashlib.sha256(open(TPL, 'rb').read()).hexdigest()}
Tv, TF, Tfl = PRE.read(TPL)
def reopen(): bpy.ops.wm.open_mainfile(filepath=BLEND)
def lines(p, k): return [l.rstrip('\n') for l in open(p) if l.startswith(k)]
# ---- R0: Blender's own OBJ importer (documentation only; the package never relies on it)
r0 = {}
for nm, kw in (('defaults', {}), ('forward_Y_up_Z', {'forward_axis': 'Y', 'up_axis': 'Z'})):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    try:
        bpy.ops.wm.obj_import(filepath=TPL, **kw); ob = [o for o in bpy.data.objects if o.type == 'MESH'][0]
        co = np.zeros(3 * len(ob.data.vertices)); ob.data.vertices.foreach_get('co', co); co = co.reshape(-1, 3); W = np.array(ob.matrix_world)
        cw = co @ W[:3, :3].T + W[:3, 3]
        same = len(co) == len(Tv) and float(np.abs(cw - Tv).max()) < 1e-4
        r0[nm] = {'vertices': len(co), 'faces': len(ob.data.polygons), 'object_rotation': list(ob.rotation_euler), 'world_coords_equal_template': bool(same),
                  'max_world_dev_cm': float(np.abs(cw - Tv).max()) if len(co) == len(Tv) else None,
                  'mesh_coords_equal_template': bool(len(co) == len(Tv) and float(np.abs(co - Tv).max()) < 1e-4),
                  'faces_equal_template': bool([tuple(p.vertices) for p in ob.data.polygons] == [tuple(f) for f in TF])}
    except Exception as ex: r0[nm] = {'error': str(ex)}
res['R0_native_obj_importer'] = r0
res['R0_operator_options'] = {op: sorted(p.identifier for p in getattr(bpy.ops.wm, op).get_rna_type().properties if p.identifier != 'rna_type') for op in ('obj_import', 'obj_export')}
res['R0_note'] = 'Blender 4.x / 5.x OBJ importer has no "Keep Vert Order" / "Split" option (the legacy Python importer had them); the package never uses it'
# ---- R1: unedited round trip
bpy.ops.wm.read_factory_settings(use_empty=True)
res['R1_setup'] = SETUP.setup(ROOT, BLEND); reopen()
base = bpy.data.objects['GO_SCULPT_BASE']; bpy.context.view_layer.objects.active = base; base.select_set(True)
modes = {}
for m in ('EDIT', 'SCULPT', 'OBJECT'):
    try: bpy.ops.object.mode_set(mode=m); modes[m] = 'ok'
    except Exception as ex: modes[m] = 'n/a in background: %s' % str(ex)[:80]
res['R1_mode_round_trip'] = modes
r = EXPORT.check_and_export(ROOT, 'ZZ', 'TOOLING-ROUNDTRIP (no sculpt)', OUT)
res['R1_export'] = {k: r[k] for k in ('pass', 'checks', 'n_moved_vertices') if k in r}
ex = os.path.join(OUT, 'GO_sculpt_ZZ_r6.obj')
if os.path.exists(ex): os.rename(ex, os.path.join(OUT, 'TOOLING_roundtrip_unedited_r6.obj')); os.rename(ex[:-4] + '_export_report.json', os.path.join(OUT, 'TOOLING_roundtrip_unedited_export_report.json'))
rt = os.path.join(OUT, 'TOOLING_roundtrip_unedited_r6.obj')
Ev, EF, Efl = PRE.read(rt)
res['R1_compare'] = {'v_records_bit_identical': lines(rt, 'v ') == lines(TPL, 'v '), 'f_records_identical': lines(rt, 'f ') == lines(TPL, 'f '),
                     'max_abs_coord_diff_cm': float(np.abs(Ev - Tv).max()), 'stature_diff_cm': float(Ev[:, 2].max() - Tv[:, 2].max()),
                     'ground_min_z_cm': float(Ev[:, 2].min()), 'anchor_fit': PRE.preflight(rt, ROOT)['checks']['P5_anchor_fit']}
pf = PRE.preflight(rt, ROOT); res['R1_preflight'] = {'pass': pf['pass'], 'checks': {k: v['pass'] for k, v in pf['checks'].items()}}
# ---- R2: groups / mask from exact source indices
reopen(); base = bpy.data.objects['GO_SCULPT_BASE']; me = base.data
regs = json.load(open(os.path.join(ROOT, 'data', 'regions.json')))['regions']
gi = {g.index: g.name for g in base.vertex_groups}; mem = {n: set() for n in gi.values()}
for v in me.vertices:
    for g in v.groups:
        if g.weight > 0.5: mem[gi[g.group]].add(v.index)
mapping = SETUP.REGION_MAP; ok = {k: mem[mapping[k]] == set(ix) for k, ix in regs.items()}
mk = me.attributes.get('.sculpt_mask'); mv = np.zeros(len(me.vertices)); mk.data.foreach_get('value', mv) if mk else None
allnt = set(i for k, ix in regs.items() if k.startswith('NO_TOUCH') for i in ix)
res['R2_groups'] = {'groups_equal_source_indices': ok, 'NO_TOUCH_all_equal': mem['NO_TOUCH_all'] == allnt,
                    'sculpt_mask_attribute': bool(mk), 'sculpt_mask_equals_no_touch': bool(mk) and set(np.where(mv > 0.5)[0].tolist()) == allnt,
                    'sculpt_mask_kind': json.loads(bpy.context.scene['rac_setup'])['sculpt_mask']}
# ---- R2b: re-mask helper restores the mask from NO_TOUCH_all without changing coordinates
reopen(); b = bpy.data.objects['GO_SCULPT_BASE']; ma = b.data.attributes['.sculpt_mask']; ma.data.foreach_set('value', [0.0] * len(b.data.vertices))
c0 = np.zeros(3 * len(b.data.vertices)); b.data.vertices.foreach_get('co', c0); rm = SETUP.remask(); c1 = np.zeros_like(c0); b.data.vertices.foreach_get('co', c1)
mv2 = np.zeros(len(b.data.vertices)); b.data.attributes['.sculpt_mask'].data.foreach_get('value', mv2)
res['R2b_remask'] = {'restored_equals_no_touch': set(np.where(mv2 > 0.5)[0].tolist()) == allnt, 'coordinates_unchanged': bool(np.array_equal(c0, c1)), **rm}
# ---- N: exporter negative fixtures (each on a fresh reopen; must REFUSE and write nothing)
def neg(name, fn, expect):
    reopen(); b = bpy.data.objects['GO_SCULPT_BASE']; bpy.context.view_layer.objects.active = b
    for o in bpy.data.objects: o.select_set(False)
    b.select_set(True)
    try: fn(b)
    except Exception as e: return {'fixture_error': str(e)[:200]}
    out = os.path.join(OUT, 'neg'); os.makedirs(out, exist_ok=True)
    r = EXPORT.check_and_export(ROOT, 'ZZ', 'TOOLING-NEGATIVE', out)
    failed = [k for k, v in r['checks'].items() if not v['pass']]
    wrote = os.path.exists(os.path.join(out, 'GO_sculpt_ZZ_r6.obj'))
    if wrote: os.remove(os.path.join(out, 'GO_sculpt_ZZ_r6.obj'))
    return {'refused': not r['pass'], 'failed_checks': failed, 'file_written': wrote, 'expected': expect, 'as_expected': (not r['pass']) and (not wrote) and expect in failed}
def bm_edit(b, f):
    bm = bmesh.new(); bm.from_mesh(b.data); f(bm); bm.to_mesh(b.data); bm.free(); b.data.update()
def del_vertex(b): bm_edit(b, lambda bm: (bm.verts.ensure_lookup_table(), bmesh.ops.delete(bm, geom=[bm.verts[5000]], context='VERTS')))
def sort_random(b):
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT'); bpy.ops.mesh.sort_elements(type='RANDOMIZE', elements={'VERT'}, seed=7); bpy.ops.object.mode_set(mode='OBJECT')
def flip_face(b): bm_edit(b, lambda bm: (bm.faces.ensure_lookup_table(), bmesh.ops.reverse_faces(bm, faces=[bm.faces[100]])))
def drop_index(b): b.data.attributes.remove(b.data.attributes['rac_src_index'])
def rot(b): b.lock_rotation = (False, False, False); b.rotation_euler = (0, 0, math.radians(5))
def scl(b): b.lock_scale = (False, False, False); b.scale = (1.01, 1.01, 1.01)
def mov(b): b.lock_location = (False, False, False); b.location = (0, 0.5, 0)
def delta(b): b.delta_rotation_euler = (math.radians(3), 0, 0)
def quat(b): b.rotation_mode = 'QUATERNION'; b.lock_rotation_w = False; b.lock_rotation = (False, False, False); b.rotation_quaternion = (0.999, 0.0447, 0, 0)
def hand(b):
    ix = regs['NO_TOUCH_hands_digits'][:50]
    for i in ix: b.data.vertices[i].co.y += 1.0
def shapekey(b): b.shape_key_add(name='Basis'); b.shape_key_add(name='K1')
def multires(b): b.modifiers.new('MR', 'MULTIRES')
def lift(b):
    for v in b.data.vertices: v.co.z += 2.0
def single(b): bpy.ops.object.make_single_user(object=True, obdata=True)     # the base mesh is shared with the view duplicate; a user would have to do this first
def remesh(b):
    single(b); m = b.modifiers.new('RM', 'REMESH'); m.mode = 'VOXEL'; m.voxel_size = 3.0; bpy.ops.object.modifier_apply(modifier='RM')
def subdiv(b):
    single(b); m = b.modifiers.new('SS', 'SUBSURF'); m.levels = 1; bpy.ops.object.modifier_apply(modifier='SS')
def nan(b): b.data.vertices[200].co.x = float('nan')
def weld(b):
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT'); bpy.ops.mesh.remove_doubles(threshold=0.5); bpy.ops.object.mode_set(mode='OBJECT')
N = {'N1_delete_vertex': (del_vertex, 'X2_counts'), 'N2_reorder_vertices_same_count': (sort_random, 'X3_identity'), 'N3_face_winding': (flip_face, 'X4_faces'),
     'N4_missing_original_index': (drop_index, 'X3_identity'), 'N5_object_rotation_5deg': (rot, 'X1_object'), 'N6_object_scale_1p01': (scl, 'X1_object'),
     'N7_object_translation': (mov, 'X1_object'), 'N7b_delta_rotation': (delta, 'X1_object'), 'N7c_quaternion_rotation': (quat, 'X1_object'), 'N8_hand_moved_1cm': (hand, 'X9_no_touch'), 'N9_shape_keys': (shapekey, 'X5_state'),
     'N10_multires': (multires, 'X5_state'), 'N11_mesh_lifted_2cm': (lift, 'X8_stature_ground'), 'N12_voxel_remesh': (remesh, 'X2_counts'),
     'N13_applied_subdivision': (subdiv, 'X2_counts'), 'N14_nan_coordinate': (nan, 'X6_values'), 'N15_weld_merge_0p5cm': (weld, 'X2_counts')}
res['N_exporter'] = {k: neg(k, f, e) for k, (f, e) in N.items()}
# ---- N: standalone preflight negative OBJ fixtures
def write_obj(p, vl, fl): open(p, 'w').write('o gorrund_body\n' + '\n'.join(vl) + '\n' + '\n'.join(fl) + '\n')
tv, tf = lines(TPL, 'v '), lines(TPL, 'f '); d = os.path.join(OUT, 'neg_obj'); os.makedirs(d, exist_ok=True); rnd = random.Random(3)
perm = list(range(len(tv))); rnd.shuffle(perm); inv = {o: n for n, o in enumerate(perm)}
fx = {'P_missing_vertex': (tv[:-1], tf), 'P_reordered_with_remapped_faces': ([tv[o] for o in perm], ['f ' + ' '.join(str(inv[int(x) - 1] + 1) for x in l.split()[1:]) for l in tf]),
      'P_reordered_faces_unchanged': ([tv[o] for o in perm], tf), 'P_face_winding': (tv, [tf[0].split()[0] + ' ' + ' '.join(tf[0].split()[1:][::-1])] + tf[1:]),
      'P_uniform_scale_1p02': (['v %.5f %.5f %.5f' % tuple(1.02 * float(x) for x in l.split()[1:]) for l in tv], tf)}
pres = {}
for k, (vl, fl) in fx.items():
    p = os.path.join(d, k + '.obj'); write_obj(p, vl, fl); r = PRE.preflight(p, ROOT)
    pres[k] = {'fail': not r['pass'], 'failed_checks': [c for c, v in r['checks'].items() if not v['pass']]}; os.remove(p)
res['N_preflight'] = pres
# ---- P: persistence preview
reopen(); res['P_unedited'] = PREV.preview(ROOT)
pv = {}
for st in ('low', 'narrow', 'broad'):
    ob = bpy.data.objects['PREVIEW_' + st]; co = np.zeros(3 * len(ob.data.vertices)); ob.data.vertices.foreach_get('co', co)
    rv = PREV.parse_v(os.path.join(ROOT, 'blender', 'transport', 'GO_%s_route_r6.obj' % st)); pv[st] = float(np.abs(co.reshape(-1, 3) - rv).max())
res['P_unedited_max_dev_from_route_cm'] = pv
T1 = os.environ.get('RAC_T1_FIXTURE')
if T1 and os.path.exists(T1):
    reopen(); b = bpy.data.objects['GO_SCULPT_BASE']; V1 = PRE.read(T1)[0]; b.data.vertices.foreach_set('co', V1.astype(np.float32).ravel()); b.data.update()
    res['P_T1_fixture'] = PREV.preview(ROOT)
    built = json.loads(os.environ.get('RAC_T1_BUILT', '{}'))
    cmp_ = {}
    for st, path in built.items():
        ob = bpy.data.objects['PREVIEW_' + st]; co = np.zeros(3 * len(ob.data.vertices)); ob.data.vertices.foreach_get('co', co)
        Bv = np.load(path)['V'][:len(co) // 3]; e = np.linalg.norm(co.reshape(-1, 3) - Bv, axis=1)
        cmp_[st] = {'p50': round(float(np.median(e)), 4), 'p90': round(float(np.percentile(e, 90)), 4), 'max': round(float(e.max()), 4)}
    res['P_T1_preview_vs_built_05F_states_cm'] = cmp_
# ---- V: matched view captures (tooling: unedited base)
reopen(); vd = os.path.join(OUT, 'views'); os.makedirs(vd, exist_ok=True)
vw = bpy.data.objects['GO_VIEW_ANATOMICAL']; fs = VIEWS.render_object(vw, 'TOOLING_unedited', vd)
res['V_views'] = {'files': [os.path.basename(f) for f in fs], 'all_written': all(os.path.exists(f) and os.path.getsize(f) > 1000 for f in fs)}
res['ALL_EXPECTED'] = bool(res['R1_export'].get('pass') and res['R1_compare']['v_records_bit_identical'] and res['R1_compare']['f_records_identical']
                           and res['R1_preflight']['pass'] and all(res['R2_groups']['groups_equal_source_indices'].values()) and res['R2_groups']['NO_TOUCH_all_equal'] and res['R2b_remask']['restored_equals_no_touch'] and res['R2b_remask']['coordinates_unchanged']
                           and all(v.get('as_expected') for v in res['N_exporter'].values()) and all(v['fail'] for v in res['N_preflight'].values())
                           and max(pv.values()) < 1e-4 and res['V_views']['all_written'])
json.dump(res, open(os.path.join(OUT, 'tooling_results.json'), 'w'), indent=1, default=str)
print('RAC_TOOLING', 'ALL AS EXPECTED' if res['ALL_EXPECTED'] else 'SEE RESULTS', os.path.join(OUT, 'tooling_results.json'))
