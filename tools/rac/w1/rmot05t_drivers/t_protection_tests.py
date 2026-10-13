# RM-OT-05T disposable protection tests of the release scene + recommended export + reintegration + s_verify.
# Every test edits a DISPOSABLE copy of GO-05T_sculpt_handoff.blend (headless bpy, scripted displacement / topology ops:
# tooling fixtures only, never sculpt candidates) and runs the real return path:
#   t_export_blend.py -> t_reintegrate.py -> (if accepted) s_verify.py
# T0 unchanged fixture | T1 small displacement of EDIT (focus) vertices | T2 protected source vertex moved 0.001 cm |
# T3 frozen-boundary vertex moved 0.001 cm (B2-retained, non-source) | T3b frozen-boundary source vertex moved |
# T4 local topology change inside the interface (edge subdivision) | T5 built-in OBJ exporter + exact rematch (diagnosis) |
# M  sculpt mask / face-set / hide numeric check
# Usage: python3 t_protection_tests.py --blend GO-05T_sculpt_handoff.blend --s3 S3.obj --s3maps .. --s3labels .. --f1 F1.obj --q05 DIR --plan05s DIR --s3verify S3_verify.json --out DIR
import argparse, json, os, shutil, subprocess, sys, hashlib, numpy as np, bpy, bmesh
ap = argparse.ArgumentParser()
for k in ('blend', 's3', 's3maps', 's3labels', 'f1', 'q05', 'plan05s', 's3verify', 'out'): ap.add_argument('--' + k)
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True); here = os.path.dirname(os.path.abspath(__file__)); py = sys.executable
S5 = os.path.join(here, '..', 'rmot05s_drivers'); res = {}
lab = np.load(a.s3labels)
def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True); return r.returncode, r.stdout[-3000:], r.stderr[-1500:]
def pipeline(tag, blendfile):
    pre = os.path.join(a.out, tag); rc, o, e = run([py, os.path.join(here, 't_export_blend.py'), '--blend', blendfile, '--out', pre + '_return'])
    out = dict(export_rc=rc, export=o.strip().splitlines()[-1] if o.strip() else e[-400:])
    rc, o, e = run([py, os.path.join(here, 't_reintegrate.py'), '--ret', pre + '_return.npz', '--s3', a.s3, '--s3maps', a.s3maps, '--s3labels', a.s3labels, '--out', pre + '_reint'])
    rj = json.load(open(pre + '_reint_reintegrate.json')); out['reintegrate'] = rj
    if rj['verdict'] == 'ACCEPTED_FOR_VERIFICATION':
        rc, o, e = run([py, os.path.join(S5, 's_verify.py'), '--src', a.f1, '--q05', a.q05, '--plan', a.plan05s, '--res', pre + '_reint.obj', '--maps', pre + '_reint_maps.npz', '--labels', pre + '_reint_face_labels.npy', '--out', pre + '_verify'])
        vj = json.load(open(pre + '_verify_verify.json')); out['s_verify'] = {k: (v['pass_'] if isinstance(v, dict) else v) for k, v in vj.items()}
        out['V1_protected_coord_sha256'] = vj['V1_outside_anatomy']['protected_coord_sha256']
    for f in (pre + '_return.obj',):
        if os.path.exists(f): os.remove(f)                                              # keep npz + json evidence, drop bulky OBJ
    return out
def copy_and_edit(tag, fn):
    dst = os.path.join(a.out, tag + '_fixture.blend'); shutil.copy2(a.blend, dst)
    refs = os.path.join(os.path.dirname(a.blend), 'GO-05T_references.blend'); shutil.copy2(refs, os.path.join(a.out, 'GO-05T_references.blend'))
    bpy.ops.wm.open_mainfile(filepath=os.path.abspath(dst)); bpy.context.preferences.filepaths.save_version = 0; ob = bpy.data.objects['GO-05S-S3_working']; info = fn(ob)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(dst), compress=True); return dst, info
def groups(ob):
    g = {vg.name: set() for vg in ob.vertex_groups}
    for v in ob.data.vertices:
        for e in v.groups:
            if e.weight > 0.5: g[ob.vertex_groups[e.group].name].add(v.index)
    return g
src_ids = np.load(a.s3maps)['src_vertex']
# M: mask / face sets / hide
bpy.ops.wm.open_mainfile(filepath=os.path.abspath(a.blend)); ob = bpy.data.objects['GO-05S-S3_working']; me = ob.data; g = groups(ob)
E = np.zeros(len(me.vertices), bool); E[list(g['EDIT_posterior'] | g['EDIT_anterior'])] = True
mask = np.zeros(len(me.vertices), np.float32); me.attributes['.sculpt_mask'].data.foreach_get('value', mask)
fs = np.zeros(len(me.polygons), np.int32); me.attributes['.sculpt_face_set'].data.foreach_get('value', fs)
hp = np.zeros(len(me.polygons), bool); me.polygons.foreach_get('hide', hp); inter = (lab == 4) | (lab == 5)
res['M_mask_and_isolation'] = dict(pass_=bool(np.array_equal(mask == 0.0, E) and np.all((mask == 0) | (mask == 1)) and np.array_equal(fs > 1, inter) and np.array_equal(hp, ~inter)),
    mask_zero_exactly_on_EDIT=bool(np.array_equal(mask == 0.0, E)), mask_one_on_all_other_vertices=int((mask == 1).sum()), face_sets_match_interface=bool(np.array_equal(fs > 1, inter)),
    editmode_hidden_faces_equal_non_interface=bool(np.array_equal(hp, ~inter)), note='numeric attribute check only; brush / UI behaviour NOT tested (no interactive Blender)')
res['T0_unchanged_fixture'] = pipeline('T0', copy_and_edit('T0', lambda ob: dict(edit='none'))[0])
s3sha = hashlib.sha256(open(a.s3, 'rb').read()).hexdigest(); t0 = res['T0_unchanged_fixture']
t0['result_bit_identical_to_S3_obj'] = t0['reintegrate'].get('result_obj_sha256') == s3sha
t0['s_verify_identical_to_S3'] = t0.get('s_verify') == {k: (v['pass_'] if isinstance(v, dict) else v) for k, v in json.load(open(a.s3verify)).items()}
def t1(ob):
    gg = groups(ob); ids = sorted(gg['FOCUS_posterior_crinkle'])[:20]; me = ob.data
    for i in ids: me.vertices[i].co = me.vertices[i].co + me.vertices[i].normal * 0.05
    me.update(); return dict(moved=ids, by_cm=0.05)
dst, info = copy_and_edit('T1', t1); res['T1_allowed_interface_displacement'] = dict(edit=info, **pipeline('T1', dst))
def pick_far_source(ob):
    co = np.zeros(len(ob.data.vertices) * 3, np.float32); ob.data.vertices.foreach_get('co', co); co = co.reshape(-1, 3)
    cand = np.where(src_ids >= 0)[0]; return int(cand[np.argmin(co[cand, 2])])        # lowest source vertex (foot), far from the arm
def t2(ob):
    i = pick_far_source(ob); ob.data.vertices[i].co.x += 0.001; ob.data.update(); return dict(moved_vertex=i, source_vertex=int(src_ids[i]), by_cm=0.001)
dst, info = copy_and_edit('T2', t2); res['T2_protected_source_vertex_moved'] = dict(edit=info, **pipeline('T2', dst))
def t3(ob, want_source):
    gg = groups(ob); ring = sorted(gg['FROZEN_interface_boundary']); i = [k for k in ring if (src_ids[k] >= 0) == want_source][0]
    ob.data.vertices[i].co.z += 0.001; ob.data.update(); return dict(moved_vertex=i, is_source_vertex=bool(src_ids[i] >= 0), by_cm=0.001)
dst, info = copy_and_edit('T3', lambda ob: t3(ob, False)); res['T3_frozen_boundary_nonsource_vertex_moved'] = dict(edit=info, **pipeline('T3', dst))
dst, info = copy_and_edit('T3b', lambda ob: t3(ob, True)); res['T3b_frozen_boundary_source_vertex_moved'] = dict(edit=info, **pipeline('T3b', dst))
# independent-check demonstration: what s_verify alone says when the frozen non-source vertex moved (bypassing the rejection)
def t4(ob):
    gg = groups(ob); Ein = gg['EDIT_posterior'] | gg['EDIT_anterior']; bm = bmesh.new(); bm.from_mesh(ob.data)
    edges = [e for e in bm.edges if e.verts[0].index in Ein and e.verts[1].index in Ein][:30]
    r = bmesh.ops.subdivide_edges(bm, edges=edges, cuts=1, use_grid_fill=False); bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) != 3])
    lay = bm.verts.layers.int.get('rac_s3_vid1'); newv = [v for v in r['geom_inner'] if isinstance(v, bmesh.types.BMVert)]
    vals = [v[lay] for v in newv]
    bm.to_mesh(ob.data); bm.free(); ob.data.update(); return dict(subdivided_edges=len(edges), new_vertices=len(newv), id_values_on_new_vertices=dict(zero=int(sum(1 for x in vals if x == 0)), nonzero=int(sum(1 for x in vals if x != 0))))
dst, info = copy_and_edit('T4', t4); res['T4_local_topology_change_inside_interface'] = dict(edit=info, **pipeline('T4', dst))
# T5: the built-in exporter (identity axes) + the 05S exact-coordinate rematch
bpy.ops.wm.open_mainfile(filepath=os.path.abspath(a.blend)); ob = bpy.data.objects['GO-05S-S3_working']
bpy.ops.object.select_all(action='DESELECT'); ob.select_set(True); bpy.context.view_layer.objects.active = ob
p5 = os.path.join(a.out, 'T5_builtin_export.obj')
bpy.ops.wm.obj_export(filepath=p5, export_selected_objects=True, forward_axis='Y', up_axis='Z', export_uv=False, export_normals=False, export_materials=False, export_triangulated_mesh=True, apply_modifiers=False)
rc, o, e = run([py, os.path.join(S5, 's_rematch.py'), '--edited', p5, '--src', a.f1, '--plan', a.plan05s, '--out', os.path.join(a.out, 'T5_rematch')])
res['T5_builtin_exporter_exact_rematch'] = dict(rematch=json.load(open(os.path.join(a.out, 'T5_rematch_rematch.json'))), note='Blender OBJ exporter prints 6 decimals (and converts axes by default): exact identity is lost -> the 05S HANDOFF.md export instruction would reject every return. Superseded by t_export_blend.py.')
for f in ('T5_builtin_export.obj', 'T5_rematch.obj', 'T5_rematch_maps.npz', 'T5_rematch_face_labels.npy'):
    if os.path.exists(os.path.join(a.out, f)): os.remove(os.path.join(a.out, f))
for f in os.listdir(a.out):
    if f.endswith('_fixture.blend') or f == 'GO-05T_references.blend' or (f.endswith('_reint.obj')): os.remove(os.path.join(a.out, f))
# expectations
exp = dict(T0_unchanged_fixture='ACCEPTED_FOR_VERIFICATION', T1_allowed_interface_displacement='ACCEPTED_FOR_VERIFICATION', T2_protected_source_vertex_moved='REJECTED',
           T3_frozen_boundary_nonsource_vertex_moved='REJECTED', T3b_frozen_boundary_source_vertex_moved='REJECTED', T4_local_topology_change_inside_interface='ACCEPTED_FOR_VERIFICATION')
for k, v in exp.items(): res[k]['expected'] = v; res[k]['as_expected'] = res[k]['reintegrate']['verdict'] == v
res['all_as_expected'] = bool(all(res[k]['as_expected'] for k in exp) and res['M_mask_and_isolation']['pass_'] and t0['result_bit_identical_to_S3_obj'] and t0['s_verify_identical_to_S3'])
json.dump(res, open(os.path.join(a.out, 'protection_tests.json'), 'w'), indent=1)
print(json.dumps({k: (v.get('reintegrate', {}).get('verdict'), v.get('as_expected')) if isinstance(v, dict) else v for k, v in res.items()}, indent=1))
