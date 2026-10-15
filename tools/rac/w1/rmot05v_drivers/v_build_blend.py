# RM-OT-05V: build GO-ARM-N1.blend (neutral ARM candidate) from an UNCHANGED copy of the selected U8 cp1 scene.
# The U8 cp1 working object is kept untouched and hidden; a new object GO-ARM-N1 carries the neutral geometry with:
#   point attribute rac_s3_vid1 (int; exporter-compatible): S3 identity for inherited source vertices (1..70751), step-coded ids for INFERRED vertices
#   face attribute rac_fgrp (int): 0 inherited source / U8 surface, 1..5 INFERRED by group A..E, 9 INFERRED seam
#   vertex groups INFERRED_A..E, INFERRED_seam (provenance), text RAC_05V_README.
# Positions are re-read after saving and must equal the state npz bit-exactly. The U8 cp1 file itself is never written.
# Usage (bpy): python3 v_build_blend.py --u8 GO-05U8_cp1.blend --state S10_E.npz --out GO-ARM-N1.blend
import argparse, hashlib, json, os, numpy as np, bpy
ap = argparse.ArgumentParser(); [ap.add_argument(k) for k in ('--u8', '--u8npz', '--state', '--out')]; a = ap.parse_args()
fH = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
assert fH(a.u8) == '2341d55445a448e24852f98fd9df3984ab12d706ef0b455cb4a2cdb0782860d6', 'U8 cp1 scene differs'
d = np.load(a.state); V = d['V'].astype(np.float32); F = d['F'].astype(np.int32); vid = d['vid'].astype(np.int64); fg = d['fgrp'].astype(np.int32)
bpy.ops.wm.open_mainfile(filepath=os.path.abspath(a.u8))
src = bpy.data.objects['GO-05S-S3_working']; src.hide_set(True); src.hide_render = True
me = bpy.data.meshes.new('GO-ARM-N1'); me.vertices.add(len(V)); me.vertices.foreach_set('co', V.ravel())
me.loops.add(F.size); me.loops.foreach_set('vertex_index', F.ravel()); me.polygons.add(len(F))
me.polygons.foreach_set('loop_start', (np.arange(len(F)) * 3).astype(np.int32)); me.update(calc_edges=True)
at = me.attributes.new('rac_s3_vid1', 'INT', 'POINT'); at.data.foreach_set('value', vid.astype(np.int32))
af = me.attributes.new('rac_fgrp', 'INT', 'FACE'); af.data.foreach_set('value', fg)
me.polygons.foreach_set('use_smooth', np.ones(len(F), bool))
ob = bpy.data.objects.new('GO-ARM-N1', me); bpy.context.scene.collection.objects.link(ob)
for k, nm in ((1, 'INFERRED_A'), (2, 'INFERRED_B'), (3, 'INFERRED_C'), (4, 'INFERRED_D'), (5, 'INFERRED_E'), (9, 'INFERRED_seam')):
    vs = np.unique(F[fg == k]).tolist()
    if vs: ob.vertex_groups.new(name=nm).add(vs, 1.0, 'REPLACE')
t = bpy.data.texts.get('RAC_05V_README') or bpy.data.texts.new('RAC_05V_README'); t.clear()
t.write('RM-OT-05V neutral ARM candidate GO-ARM-N1 (from U8 cp1 2341d554..., which is kept hidden and unchanged in this file).\n'
        'Object GO-ARM-N1: rac_s3_vid1 (S3 identity / INFERRED ids), rac_fgrp (0 inherited, 1-5 INFERRED groups A-E, 9 seam).\n'
        'All INFERRED surface is reconstruction, never canon (REFERENCE_ANATOMY_V1 §7). Status: candidate; see reviews/claude-rac-rm-ot-05v-*.md.\n'
        'Export: python3 tools/rac/w1/rmot05t_drivers/t_export_blend.py --blend GO-ARM-N1.blend --object GO-ARM-N1 --out PREFIX\n')
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(a.out), compress=True, relative_remap=True)
bpy.ops.wm.open_mainfile(filepath=os.path.abspath(a.out)); ob = bpy.data.objects['GO-ARM-N1']; me = ob.data
co = np.zeros(len(me.vertices) * 3, np.float32); me.vertices.foreach_get('co', co)
s3 = bpy.data.objects['GO-05S-S3_working'].data; c3 = np.zeros(len(s3.vertices) * 3, np.float32); s3.vertices.foreach_get('co', c3)
U8 = np.load(a.u8npz)['V'].astype(np.float32).ravel()
fi = np.zeros(len(me.polygons) * 3, np.int32); me.polygons.foreach_get('vertices', fi) if False else None
print(json.dumps(dict(positions_bit_exact=bool(np.array_equal(co, V.ravel())), vertices=len(me.vertices), faces=len(me.polygons),
                      u8_object_vertices=len(s3.vertices), u8_object_bit_exact_to_u8cp1=bool(np.array_equal(c3, U8)), libraries=[l.filepath for l in bpy.data.libraries], out_sha=fH(a.out))))
