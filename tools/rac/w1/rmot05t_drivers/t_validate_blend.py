# RM-OT-05T: headless validation of a direct-sculpt handoff .blend against its frozen OBJ / label inputs.
# Checks: object set, identity transforms, units, working-mesh coordinates (float32 storage vs float32(OBJ)) and face
# connectivity, rac_label, vertex-group consistency (EDIT vs FROZEN overlap, FOCUS inside EDIT_posterior), reference
# meshes vs F1 / B2, optional release-copy extras (id attributes, sculpt mask, face sets, linked references).
# Usage: python3 t_validate_blend.py --blend X.blend --s3 GO-05S-S3.obj --labels S3_labels.npy --f1 F1_working.obj --b2 B2.obj --out OUT.json
import argparse, json, numpy as np, bpy
ap = argparse.ArgumentParser(); ap.add_argument('--blend'); ap.add_argument('--s3'); ap.add_argument('--labels'); ap.add_argument('--f1'); ap.add_argument('--b2'); ap.add_argument('--out')
ap.add_argument('--working', default='GO-05S-S3_working'); a = ap.parse_args()
def load_obj(p):
    V = []; F = []
    for l in open(p):
        if l.startswith('v '): V.append([float(t) for t in l.split()[1:4]])
        elif l.startswith('f '): F.append([int(t.split('/')[0]) - 1 for t in l.split()[1:4]])
    return np.array(V), np.array(F)
def mesh_arrays(ob):
    me = ob.data; n = len(me.vertices); co = np.zeros(n * 3, np.float32); me.vertices.foreach_get('co', co)
    nl = np.zeros(len(me.polygons), np.int32); me.polygons.foreach_get('loop_total', nl); lv = np.zeros(len(me.loops), np.int32); me.loops.foreach_get('vertex_index', lv)
    return co.reshape(-1, 3), nl, lv
bpy.ops.wm.open_mainfile(filepath=a.blend); sc = bpy.context.scene; R = dict(blend=a.blend, checks={})
def chk(name, ok, **kw): R['checks'][name] = dict(pass_=bool(ok), **kw)
chk('units', abs(sc.unit_settings.scale_length - 0.01) < 1e-6, system=sc.unit_settings.system, scale_length=round(sc.unit_settings.scale_length, 6), length_unit=sc.unit_settings.length_unit, note='1 Blender unit = 1 cm')
obs = {o.name: o for o in bpy.data.objects}; chk('objects_present', a.working in obs, objects=sorted(obs))
for o in obs.values():
    chk('identity_transform_' + o.name, np.allclose(np.array(o.matrix_world), np.eye(4)) and o.parent is None, parent=None if o.parent is None else o.parent.name)
w = obs[a.working]; co, nl, lv = mesh_arrays(w); Vs, Fs = load_obj(a.s3)
chk('working_vertex_count', len(co) == len(Vs), blend=len(co), obj=len(Vs)); chk('working_all_triangles', bool((nl == 3).all()))
same_co = bool(len(co) == len(Vs) and np.array_equal(co, Vs.astype(np.float32)))
chk('working_coords_equal_float32_of_obj', same_co, max_abs_diff_vs_float64=float(np.abs(co.astype(np.float64) - Vs).max()) if len(co) == len(Vs) else None,
    note='Blender stores float32; the float64 OBJ cannot survive a Blender round trip bit-exactly (see export audit)')
Fb = lv.reshape(-1, 3) if (nl == 3).all() else None; chk('working_faces_equal_obj', Fb is not None and np.array_equal(Fb, Fs), faces=len(nl))
lab = np.load(a.labels); at = w.data.attributes.get('rac_label'); bl = np.zeros(len(nl), np.int32)
if at is not None: at.data.foreach_get('value', bl)
chk('rac_label_equal', at is not None and np.array_equal(bl, lab), counts={int(k): int((lab == k).sum()) for k in np.unique(lab)})
g = {}
for vg in w.vertex_groups: g[vg.name] = np.zeros(len(co), bool)
for v in w.data.vertices:
    for e in v.groups: g[w.vertex_groups[e.group].name][v.index] = e.weight > 0.5
newf = np.where((lab == 4) | (lab == 5))[0]; oldf = np.where((lab != 4) & (lab != 5))[0]
vnew = np.zeros(len(co), bool); vnew[Fs[newf].ravel()] = True; vold = np.zeros(len(co), bool); vold[Fs[oldf].ravel()] = True
edit_expected = vnew & ~vold; ring_expected = vnew & vold
E = g.get('EDIT_posterior', 0) | g.get('EDIT_anterior', 0); Fz = g.get('FROZEN_interface_boundary'); Fo = g.get('FOCUS_posterior_crinkle')
chk('edit_groups_equal_interface_interior', np.array_equal(E, edit_expected), edit=int(E.sum()), expected=int(edit_expected.sum()))
chk('frozen_group_equal_interface_boundary_ring', np.array_equal(Fz, ring_expected), frozen=int(Fz.sum()))
chk('edit_frozen_disjoint', not (E & Fz).any(), overlap=int((E & Fz).sum()))
chk('edit_posterior_anterior_disjoint', not (g['EDIT_posterior'] & g['EDIT_anterior']).any())
chk('focus_inside_edit_posterior', bool((Fo <= g['EDIT_posterior']).all()), focus=int(Fo.sum()))
outside = ~(E | Fz); chk('outside_vertices_neither_edit_nor_frozen', True, outside_vertices=int(outside.sum()), note='protected by mask / hide, not by vertex groups (groups are selection aids)')
for nm, p in (('F1_source_reference', a.f1), ('B2_reference', a.b2)):
    if nm in obs:
        c2, n2, l2 = mesh_arrays(obs[nm]); V2, F2 = load_obj(p)
        chk('reference_' + nm + '_equal_float32', len(c2) == len(V2) and np.array_equal(c2, V2.astype(np.float32)) and np.array_equal(l2.reshape(-1, 3), F2),
            library=None if obs[nm].data.library is None else obs[nm].data.library.filepath, data_is_editable=bool(obs[nm].data.is_editable), object_is_editable=bool(obs[nm].is_editable), hide_select=obs[nm].hide_select, lock_location=list(obs[nm].lock_location))
# release-copy extras (only reported if present)
for an in ('rac_s3_vid1', 'rac_src_vid1', '.sculpt_mask', '.sculpt_face_set'):
    at2 = w.data.attributes.get(an)
    if at2 is not None:
        n = len(at2.data); val = np.zeros(n, np.float32 if at2.data_type == 'FLOAT' else np.int32); at2.data.foreach_get('value', val)
        R['checks']['attribute_' + an] = dict(pass_=True, domain=at2.domain, type=at2.data_type, n=n, summary={str(k): int((val == k).sum()) for k in np.unique(val)[:6]} if an.startswith('.') else dict(min=int(val.min()), max=int(val.max()), zeros=int((val == 0).sum())))
R['all_pass'] = all(v['pass_'] for v in R['checks'].values()); json.dump(R, open(a.out, 'w'), indent=1)
print(json.dumps({k: v['pass_'] for k, v in R['checks'].items()}, indent=1), R['all_pass'])
