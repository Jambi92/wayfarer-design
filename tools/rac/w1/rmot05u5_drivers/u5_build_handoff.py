# RM-OT-05U5: build GO-05U2_sculpt_handoff.blend from an UNCHANGED copy of the verified 05U RETURN (.blend + linked reference).
# Geometry, topology, object, transform, units, rac_s3_vid1 / rac_src_vid1 / rac_label and the linked references are kept.
# Changed support data only (approved 05U2 boundary, pinned lists):
#   .sculpt_mask       1.0 everywhere except 0.0 on the 365 approved editable vertices
#   .sculpt_face_set   1 protected, 2 posterior interface, 3 anterior interface, 4 = the 35 approved added source faces (cap)
#   rac_u2_added       (FACE, INT) 1 on the 35 added faces (provenance helper; return label 6 is assigned by the U2 adapter)
#   vertex groups      EDIT_upper_ext_05U2 (15 added vertices), FROZEN_interface_boundary_05U2 (106);
#                      the old 101-vertex FROZEN_interface_boundary is renamed FROZEN_interface_boundary_05T_historical
#   hide               every face outside the 832 approved editable-region faces hidden (Edit-mode isolation)
#   text               RAC_U2_README (supported export / check path)
# The input RETURN .blend must sit next to GO-05T_references.blend in the OUTPUT folder so the library path stays //GO-05T_references.blend.
# Usage (bpy): python3 u5_build_handoff.py --ret05u_blend RETURN.blend --baseline_npz return.npz --proposal DIR --s3 GO-05S-S3.obj --out OUT.blend
import argparse, hashlib, json, os, numpy as np, bpy, trimesh
ap = argparse.ArgumentParser(); [ap.add_argument(k) for k in ('--ret05u_blend', '--baseline_npz', '--proposal', '--s3', '--out')]; a = ap.parse_args()
H = lambda x: hashlib.sha256(np.asarray(x, dtype=np.int64).tobytes()).hexdigest()
PIN = dict(blend='9593d2016eabdf35e8eea0c7df1a93c5c863ed3ad94676722061aa90f29357a5', npz='0989caf45cba8ddf0f44bdfba962671430c613bb752ac543d99d9b4b16420265',
           added_faces='483ab7feac190c76679eadc3ce677cd8e538349e2dc4842c6db0dfd441797692', added_vertices='5be5a27f133f9e936f6d4164340eb7561de8af0bc9016f17a97aa5fdc6cd0aa1',
           editable='0154b2be773056f049e7a729f15d97e8844fb3862c77b58a760f7c2666e95559', ring='91725db2ca491529305c0a77e14f89db5578628bba7500d9495536f724340426')
fH = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
assert fH(a.ret05u_blend) == PIN['blend'] and fH(a.baseline_npz) == PIN['npz'], 'pinned 05U RETURN inputs differ'
P = np.load(os.path.join(a.proposal, 'proposal_sets.npz')); A = P['added_faces']; E = P['proposed_editable']; R = P['proposed_frozen_ring']
lab_s3 = np.load('reviews/rac-rmot05s-evidence/repair/S3/GO-05S-S3_face_labels.npy'); inter = (lab_s3 == 4) | (lab_s3 == 5)
cur_e = None
assert H(A) == PIN['added_faces'] and H(E) == PIN['editable'] and H(R) == PIN['ring']
s3 = trimesh.load(a.s3, process=False); Fs = np.asarray(s3.faces)
bpy.ops.wm.open_mainfile(filepath=os.path.abspath(a.ret05u_blend))
w = bpy.data.objects['GO-05S-S3_working']; me = w.data; nv = len(me.vertices); nf = len(me.polygons)
chk = {}
vid = np.zeros(nv, np.int32); me.attributes['rac_s3_vid1'].data.foreach_get('value', vid); chk['vertex_order_is_S3'] = bool(np.array_equal(vid - 1, np.arange(nv)))
lv = np.zeros(len(me.loops), np.int32); me.loops.foreach_get('vertex_index', lv); FF = lv.reshape(-1, 3); chk['face_order_is_S3'] = bool(np.array_equal(FF, Fs))
co = np.zeros(nv * 3, np.float32); me.vertices.foreach_get('co', co); co = co.reshape(-1, 3)
B = np.load(a.baseline_npz); Vb = np.zeros_like(B['V']); Vb[B['s3_vid1'] - 1] = B['V']; chk['positions_equal_05U_return_float32'] = bool(np.array_equal(co, Vb))
chk['identity_transform'] = bool(np.allclose(np.array(w.matrix_world), np.eye(4)) and w.parent is None); chk['no_modifiers'] = len(w.modifiers) == 0
chk['added_faces_vertices'] = bool(np.array_equal(np.setdiff1d(np.unique(FF[A]), []), np.unique(Fs[A])))
assert all(chk.values()), chk
# old editable (05T) for face sets
mask = np.ones(nv, np.float32); mask[E] = 0.0
am = me.attributes.get('.sculpt_mask') or me.attributes.new('.sculpt_mask', 'FLOAT', 'POINT'); am.data.foreach_set('value', mask)
fs = np.ones(nf, np.int32); old = np.zeros(nf, np.int32); me.attributes['.sculpt_face_set'].data.foreach_get('value', old)
fs[old == 2] = 2; fs[old == 3] = 3; fs[A] = 4
af = me.attributes['.sculpt_face_set']; af.data.foreach_set('value', fs)
ad = me.attributes.get('rac_u2_added') or me.attributes.new('rac_u2_added', 'INT', 'FACE'); add = np.zeros(nf, np.int32); add[A] = 1; ad.data.foreach_set('value', add)
if 'FROZEN_interface_boundary' in w.vertex_groups: w.vertex_groups['FROZEN_interface_boundary'].name = 'FROZEN_interface_boundary_05T_historical'
for nm, idx in (('EDIT_upper_ext_05U2', np.setdiff1d(E, np.where((np.isin(np.arange(nv), Fs[inter].ravel())) & ~np.isin(np.arange(nv), Fs[~inter].ravel()))[0])), ('FROZEN_interface_boundary_05U2', R)):
    g = w.vertex_groups.get(nm) or w.vertex_groups.new(name=nm); g.add([int(i) for i in idx], 1.0, 'REPLACE'); chk['group_%s' % nm] = int(len(idx))
region = inter.copy(); region[A] = True
me.polygons.foreach_set('hide', ~region)
hv = np.ones(nv, bool); hv[FF[region].ravel()] = False; me.vertices.foreach_set('hide', hv)
ev = np.zeros(len(me.edges) * 2, np.int32); me.edges.foreach_get('vertices', ev); ev = ev.reshape(-1, 2); me.edges.foreach_set('hide', hv[ev[:, 0]] | hv[ev[:, 1]]); me.update()
t = bpy.data.texts.get('RAC_U2_README') or bpy.data.texts.new('RAC_U2_README'); t.clear()
t.write('RM-OT-05U5 bounded revision handoff (approved 05U2 boundary: 365 editable vertices, 106 frozen ring, 832 faces).\n'
        'Export and check ONLY with: bash tools/rac/w1/rmot05u4_drivers/check_return_u2.sh <file>.blend <outdir>\n'
        'Do not use the built-in OBJ exporter. Do not rename GO-05S-S3_working or the rac_* attributes. Smooth brush only; no topology change.\n')
for lib in list(bpy.data.libraries):                                             # drop stale brush-asset library links carried from the
    if 'essentials_brushes' in lib.filepath: bpy.data.libraries.remove(lib)      # 05U desktop session (desktop Blender supplies its own)
w.select_set(True); bpy.context.view_layer.objects.active = w
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(a.out), compress=True, relative_remap=True)
# reopen and validate what was saved
bpy.ops.wm.open_mainfile(filepath=os.path.abspath(a.out)); w = bpy.data.objects['GO-05S-S3_working']; me = w.data
m2 = np.zeros(nv, np.float32); me.attributes['.sculpt_mask'].data.foreach_get('value', m2); f2 = np.zeros(nf, np.int32); me.attributes['.sculpt_face_set'].data.foreach_get('value', f2)
co2 = np.zeros(nv * 3, np.float32); me.vertices.foreach_get('co', co2); hp = np.zeros(nf, bool); me.polygons.foreach_get('hide', hp)
v = dict(checks_before_save=chk, mask_zero=int((m2 == 0).sum()), mask_zero_equals_365_list=bool(np.array_equal(np.where(m2 == 0)[0], E)),
         face_sets={k: int((f2 == k).sum()) for k in (1, 2, 3, 4)}, positions_unchanged=bool(np.array_equal(co2.reshape(-1, 3), Vb)), visible_faces=int((~hp).sum()),
         groups=sorted(g.name for g in w.vertex_groups), libraries=[l.filepath for l in bpy.data.libraries], linked_refs=[o.name for o in bpy.data.objects if o.library],
         units=[bpy.context.scene.unit_settings.system, round(bpy.context.scene.unit_settings.scale_length, 6), bpy.context.scene.unit_settings.length_unit], modifiers=len(w.modifiers),
         object_name=w.name, attributes=sorted(x.name for x in me.attributes if not x.name.startswith('.')))
print(json.dumps(v))
