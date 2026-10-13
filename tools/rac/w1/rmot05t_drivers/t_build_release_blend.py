# RM-OT-05T: build the support-only RELEASE COPY of the 05S handoff scene (the 05S .blend itself is not modified).
#   GO-05T_references.blend : F1_source_reference + B2_reference (copied unchanged from the 05S scene)
#   GO-05T_sculpt_handoff.blend : the S3 working mesh (unchanged geometry) with
#       rac_s3_vid1  (POINT, INT)  S3 vertex index + 1 (0 = vertex created during the edit)   -> identity for export
#       rac_src_vid1 (POINT, INT)  F1_working vertex index + 1 (0 = not a source vertex)        -> provenance only
#       rac_label    (FACE, INT)   unchanged from 05S
#       .sculpt_mask (POINT, FLOAT) 1.0 on every vertex outside EDIT_posterior / EDIT_anterior (protected), 0.0 inside
#       .sculpt_face_set (FACE, INT) 1 protected, 2 posterior interface, 3 anterior interface
#       vertex groups as in 05S; Edit-mode isolation: every face outside the interface (rac_label not 4/5) is hidden
#     references LINKED from GO-05T_references.blend (library data: selectable for inspection, not editable)
#   scene units: metric, scale 0.01, length unit centimetres. A text block RAC_EXPORT_README is embedded.
# Usage: python3 t_build_release_blend.py --src05s GO-05S_interface_handoff.blend --s3maps GO-05S-S3_maps.npz --outdir DIR
import argparse, os, json, numpy as np, bpy
ap = argparse.ArgumentParser(); ap.add_argument('--src05s'); ap.add_argument('--s3maps'); ap.add_argument('--outdir'); a = ap.parse_args(); os.makedirs(a.outdir, exist_ok=True)
refs = os.path.abspath(os.path.join(a.outdir, 'GO-05T_references.blend')); work = os.path.abspath(os.path.join(a.outdir, 'GO-05T_sculpt_handoff.blend'))
# 1. references file
bpy.ops.wm.open_mainfile(filepath=os.path.abspath(a.src05s))
bpy.data.objects.remove(bpy.data.objects['GO-05S-S3_working'], do_unlink=True)
for o in bpy.data.objects: o.hide_set(False); o.hide_select = False; o.hide_viewport = False; o.lock_location = o.lock_rotation = o.lock_scale = (True, True, True)
bpy.ops.outliner.orphans_purge(do_recursive=True) if bpy.context.area else None
bpy.ops.wm.save_as_mainfile(filepath=refs, compress=True)
# 2. working file
bpy.ops.wm.open_mainfile(filepath=os.path.abspath(a.src05s))
for nm in ('F1_source_reference', 'B2_reference'):
    me = bpy.data.objects[nm].data; bpy.data.objects.remove(bpy.data.objects[nm], do_unlink=True); bpy.data.meshes.remove(me)
sc = bpy.context.scene; sc.unit_settings.system = 'METRIC'; sc.unit_settings.scale_length = 0.01; sc.unit_settings.length_unit = 'CENTIMETERS'
w = bpy.data.objects['GO-05S-S3_working']; w.name = 'GO-05S-S3_working'; me = w.data; nv = len(me.vertices); nf = len(me.polygons)
mp = np.load(a.s3maps); src = mp['src_vertex']; assert len(src) == nv
at = me.attributes.new('rac_s3_vid1', 'INT', 'POINT'); at.data.foreach_set('value', (np.arange(nv) + 1).astype(np.int32))
at = me.attributes.new('rac_src_vid1', 'INT', 'POINT'); at.data.foreach_set('value', (src + 1).astype(np.int32))
lab = np.zeros(nf, np.int32); me.attributes['rac_label'].data.foreach_get('value', lab)
E = np.zeros(nv, bool)
for nm in ('EDIT_posterior', 'EDIT_anterior'):
    gi = w.vertex_groups[nm].index
    for v in me.vertices:
        if any(g.group == gi and g.weight > 0.5 for g in v.groups): E[v.index] = True
mask = np.where(E, 0.0, 1.0).astype(np.float32)
am = me.attributes.get('.sculpt_mask') or me.attributes.new('.sculpt_mask', 'FLOAT', 'POINT'); am.data.foreach_set('value', mask)
lv = np.zeros(len(me.loops), np.int32); me.loops.foreach_get('vertex_index', lv); FF = lv.reshape(-1, 3); fc, _, _ = None, None, None
ctr = np.zeros((nv, 3), np.float32); me.vertices.foreach_get('co', ctr.ravel())
fs = np.ones(nf, np.int32); inter = (lab == 4) | (lab == 5); xs = ctr[FF].mean(1)
# posterior / anterior split by the arm-local theta sign (posterior = theta < 0): e2 component of the frame
O = np.array([30.5, -1.3, 160.4]); d = np.array([-0.29408, -0.05401, 0.95425]); d /= np.linalg.norm(d); e1 = np.cross([0, 1, 0], d); e1 /= np.linalg.norm(e1); e2 = np.cross(d, e1)
post = ((xs - O) @ e2) < 0; fs[inter & post] = 2; fs[inter & ~post] = 3
af = me.attributes.get('.sculpt_face_set') or me.attributes.new('.sculpt_face_set', 'INT', 'FACE'); af.data.foreach_set('value', fs)
hp = ~inter; me.polygons.foreach_set('hide', hp)                               # Edit-mode isolation of the interface
hv = np.ones(nv, bool); hv[FF[inter].ravel()] = False; me.vertices.foreach_set('hide', hv)
he_ = np.ones(len(me.edges), bool); ev = np.zeros(len(me.edges) * 2, np.int32); me.edges.foreach_get('vertices', ev); ev = ev.reshape(-1, 2); he_ = hv[ev[:, 0]] | hv[ev[:, 1]]; me.edges.foreach_set('hide', he_)
me.update()
# 3. link references (library data: not editable)
coll = bpy.data.collections.new('REFERENCES_linked_readonly'); sc.collection.children.link(coll)
with bpy.data.libraries.load(refs, link=True, relative=True) as (src_, dst_):
    dst_.objects = ['F1_source_reference', 'B2_reference']
for o in dst_.objects:
    coll.objects.link(o)
for o in coll.objects: o.hide_set(True)
txt = bpy.data.texts.new('RAC_EXPORT_README')
txt.write('Export ONLY with tools/rac/w1/rmot05t_drivers/t_export_blend.py (see START_HERE.md). The built-in OBJ exporter writes 6 decimals and\n'
          'converts axes by default, which destroys exact identity of protected vertices. Do not rename GO-05S-S3_working or the rac_* attributes.\n')
w.select_set(True); bpy.context.view_layer.objects.active = w
bpy.ops.wm.save_as_mainfile(filepath=work, compress=True, relative_remap=True)
print(json.dumps(dict(references=refs, working=work, edit_vertices=int(E.sum()), masked_vertices=int((mask == 1).sum()), face_sets={k: int((fs == k).sum()) for k in (1, 2, 3)},
                      hidden_faces=int(hp.sum()), visible_faces=int((~hp).sum()))))
