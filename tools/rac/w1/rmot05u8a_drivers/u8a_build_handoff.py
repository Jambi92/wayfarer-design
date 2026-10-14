# RM-OT-05U8A: build GO-05U8A_handoff.blend from an UNCHANGED copy of the accepted U8 cp1 scene (pinned); additive copy of u8_build_handoff.py. Geometry, topology, object,
# transform, units, rac_* attributes and the linked references are kept; only support data is added:
#   vertex groups EDIT_crease_anchors_U8A (61580, 61581) and FROZEN_ring_U8A (12 ring vertices);
#   text RAC_U8A_README (supported check path). Positions are re-read after saving and must equal U8 cp1 bit-exactly.
# The U8 cp1 .blend must sit next to GO-05T_references.blend in the OUTPUT folder (library path //GO-05T_references.blend).
# Usage (bpy): python3 u8a_build_handoff.py --cp3_blend GO-05U8_cp1.blend (the pinned U8 cp1 scene) --sets DIR --out GO-05U8A_handoff.blend
import argparse, hashlib, json, os, numpy as np, bpy
ap = argparse.ArgumentParser(); [ap.add_argument(k) for k in ('--cp3_blend', '--sets', '--out')]; a = ap.parse_args()
fH = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
assert fH(a.cp3_blend) == '2341d55445a448e24852f98fd9df3984ab12d706ef0b455cb4a2cdb0782860d6', 'U8 cp1 scene differs'
assert fH(os.path.join(a.sets, 'u8a_sets_v1.json')) == 'f3ac181c3106dd01c6de7df4b3bdcd2dd00147ec5dab1ee8e157b3f66e33767b'
SE = json.load(open(os.path.join(a.sets, 'u8a_sets_v1.json')))
bpy.ops.wm.open_mainfile(filepath=os.path.abspath(a.cp3_blend)); w = bpy.data.objects['GO-05S-S3_working']; me = w.data; nv = len(me.vertices)
vid = np.zeros(nv, np.int32); me.attributes['rac_s3_vid1'].data.foreach_get('value', vid); assert np.array_equal(vid - 1, np.arange(nv))
co0 = np.zeros(nv * 3, np.float32); me.vertices.foreach_get('co', co0)
for nm, idx in (('EDIT_crease_anchors_U8A', SE['target_vertices']), ('FROZEN_ring_U8A', SE['frozen_ring'])):
    g = w.vertex_groups.get(nm) or w.vertex_groups.new(name=nm); g.add([int(i) for i in idx], 1.0, 'REPLACE')
t = bpy.data.texts.get('RAC_U8A_README') or bpy.data.texts.new('RAC_U8A_README'); t.clear()
t.write('RM-OT-05U8A controlled crease-anchor release handoff (from accepted U8 cp1 2341d554...).\n'
        'Editable: EDIT_crease_anchors_U8A (61581 first, max 0.06 cm; then 61580 only if needed, max 0.04 cm). Frozen: FROZEN_ring_U8A (12) and everything else.\n'
        'Check ONLY with: bash tools/rac/w1/rmot05u8a_drivers/check_return_u8a.sh <file>.blend <outdir>\n'
        'Edit Mode vertex moves / small Grab / very light local Smooth only; no topology change, Dyntopo, remesh, script or projection.\n')
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(a.out), compress=True, relative_remap=True)
bpy.ops.wm.open_mainfile(filepath=os.path.abspath(a.out)); w = bpy.data.objects['GO-05S-S3_working']; me = w.data
co1 = np.zeros(nv * 3, np.float32); me.vertices.foreach_get('co', co1)
print(json.dumps(dict(positions_unchanged=bool(np.array_equal(co0, co1)), groups=sorted(g.name for g in w.vertex_groups), libraries=[l.filepath for l in bpy.data.libraries],
                      modifiers=len(w.modifiers), out_sha=fH(a.out))))
