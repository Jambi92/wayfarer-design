# RM-OT-05U8: build GO-05U8_handoff.blend from an UNCHANGED copy of the accepted U7 cp2 scene (pinned); additive copy of u7_build_handoff.py. Geometry, topology, object,
# transform, units, rac_* attributes and the linked references are kept; only support data is added:
#   vertex groups EDIT_lower_cut_U8 (4 target vertices) and FROZEN_ring_U8 (15 ring vertices, incl. crease-B anchor 61580);
#   text RAC_U8_README (supported check path). Positions are re-read after saving and must equal U7 cp2 bit-exactly.
# The U7 cp2 .blend must sit next to GO-05T_references.blend in the OUTPUT folder (library path //GO-05T_references.blend).
# Usage (bpy): python3 u8_build_handoff.py --cp3_blend GO-05U7_cp2.blend (the pinned U7 cp2 scene; argument name kept from u7) --sets DIR --out GO-05U8_handoff.blend
import argparse, hashlib, json, os, numpy as np, bpy
ap = argparse.ArgumentParser(); [ap.add_argument(k) for k in ('--cp3_blend', '--sets', '--out')]; a = ap.parse_args()
fH = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
assert fH(a.cp3_blend) == '1de9d0ac88f0011062a37f75eed6b6811a5288ae1ef80cc632bfc18c38bfb667', 'U7 cp2 scene differs'
assert fH(os.path.join(a.sets, 'u8_sets_v1.json')) == '54414665bbe25cc9b9039649ae3692cb7a274bf95fb98c40fa0f167cb34f787a'
SE = json.load(open(os.path.join(a.sets, 'u8_sets_v1.json')))
bpy.ops.wm.open_mainfile(filepath=os.path.abspath(a.cp3_blend)); w = bpy.data.objects['GO-05S-S3_working']; me = w.data; nv = len(me.vertices)
vid = np.zeros(nv, np.int32); me.attributes['rac_s3_vid1'].data.foreach_get('value', vid); assert np.array_equal(vid - 1, np.arange(nv))
co0 = np.zeros(nv * 3, np.float32); me.vertices.foreach_get('co', co0)
for nm, idx in (('EDIT_lower_cut_U8', SE['target_vertices']), ('FROZEN_ring_U8', SE['frozen_ring'])):
    g = w.vertex_groups.get(nm) or w.vertex_groups.new(name=nm); g.add([int(i) for i in idx], 1.0, 'REPLACE')
t = bpy.data.texts.get('RAC_U8_README') or bpy.data.texts.new('RAC_U8_README'); t.clear()
t.write('RM-OT-05U8 lower-cut facet cleanup handoff (from accepted U7 cp2 1de9d0ac...).\n'
        'Editable: EDIT_lower_cut_U8 (4 vertices: 61562 61727 61735 61940). Frozen: FROZEN_ring_U8 (15, incl. 61580) and everything else.\n'
        'Check ONLY with: bash tools/rac/w1/rmot05u8_drivers/check_return_u8.sh <file>.blend <outdir>\n'
        'Edit Mode vertex moves / small Grab / very light local Smooth only; no topology change, Dyntopo, remesh, script or projection.\n')
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(a.out), compress=True, relative_remap=True)
bpy.ops.wm.open_mainfile(filepath=os.path.abspath(a.out)); w = bpy.data.objects['GO-05S-S3_working']; me = w.data
co1 = np.zeros(nv * 3, np.float32); me.vertices.foreach_get('co', co1)
print(json.dumps(dict(positions_unchanged=bool(np.array_equal(co0, co1)), groups=sorted(g.name for g in w.vertex_groups), libraries=[l.filepath for l in bpy.data.libraries],
                      modifiers=len(w.modifiers), out_sha=fH(a.out))))
