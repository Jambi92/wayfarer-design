# RM-OT-05U7: build GO-05U7_handoff.blend from an UNCHANGED copy of the accepted U6A cp3 scene (pinned). Geometry, topology, object,
# transform, units, rac_* attributes and the linked references are kept; only support data is added:
#   vertex groups EDIT_upper_crease_U7 (5 target vertices) and FROZEN_ring_U7 (14 ring vertices, incl. held seed 61522);
#   text RAC_U7_README (supported check path). Positions are re-read after saving and must equal cp3 bit-exactly.
# The cp3 .blend must sit next to GO-05T_references.blend in the OUTPUT folder (library path //GO-05T_references.blend).
# Usage (bpy): python3 u7_build_handoff.py --cp3_blend GO-05U6_cp3.blend --sets DIR --out GO-05U7_handoff.blend
import argparse, hashlib, json, os, numpy as np, bpy
ap = argparse.ArgumentParser(); [ap.add_argument(k) for k in ('--cp3_blend', '--sets', '--out')]; a = ap.parse_args()
fH = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
assert fH(a.cp3_blend) == '22345d4d270b84753d3cdf32086d66846644448105aba1db710faaa083746029', 'cp3 scene differs'
assert fH(os.path.join(a.sets, 'u7_sets_v1.json')) == '67aeca8d826cf6a9566d1b2987f26aa4c6565129a1b47f2eeda542f7a50ae1b0'
SE = json.load(open(os.path.join(a.sets, 'u7_sets_v1.json')))
bpy.ops.wm.open_mainfile(filepath=os.path.abspath(a.cp3_blend)); w = bpy.data.objects['GO-05S-S3_working']; me = w.data; nv = len(me.vertices)
vid = np.zeros(nv, np.int32); me.attributes['rac_s3_vid1'].data.foreach_get('value', vid); assert np.array_equal(vid - 1, np.arange(nv))
co0 = np.zeros(nv * 3, np.float32); me.vertices.foreach_get('co', co0)
for nm, idx in (('EDIT_upper_crease_U7', SE['target_vertices']), ('FROZEN_ring_U7', SE['frozen_ring'])):
    g = w.vertex_groups.get(nm) or w.vertex_groups.new(name=nm); g.add([int(i) for i in idx], 1.0, 'REPLACE')
t = bpy.data.texts.get('RAC_U7_README') or bpy.data.texts.new('RAC_U7_README'); t.clear()
t.write('RM-OT-05U7 upper-crease facet extension handoff (from accepted U6A cp3 22345d4d...).\n'
        'Editable: EDIT_upper_crease_U7 (5 vertices: 61183 61586 61771 62027 62063). Frozen: FROZEN_ring_U7 (14, incl. 61522) and everything else.\n'
        'Check ONLY with: bash tools/rac/w1/rmot05u7_drivers/check_return_u7.sh <file>.blend <outdir>\n'
        'Edit Mode vertex moves / small Grab / very light local Smooth only; no topology change, Dyntopo, remesh, script or projection.\n')
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(a.out), compress=True, relative_remap=True)
bpy.ops.wm.open_mainfile(filepath=os.path.abspath(a.out)); w = bpy.data.objects['GO-05S-S3_working']; me = w.data
co1 = np.zeros(nv * 3, np.float32); me.vertices.foreach_get('co', co1)
print(json.dumps(dict(positions_unchanged=bool(np.array_equal(co0, co1)), groups=sorted(g.name for g in w.vertex_groups), libraries=[l.filepath for l in bpy.data.libraries],
                      modifiers=len(w.modifiers), out_sha=fH(a.out))))
