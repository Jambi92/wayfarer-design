# RM-OT-05AF: weld only SAFE_SCULPT_SEAM groups inside the AC1-AC3 sculpt zones (from af_groups.json) on the frozen 05AE baseline.
# Exact duplicates collapse onto an existing member position (bmesh weld_verts); nothing else changes. Display-only data is left as
# in 05AE (UVs / custom normals were already removed in 05AD). Runs in Blender 5.2.2 (bpy, cloud workspace).
# Usage: python af_weld.py BASE_05AE.blend EXPECTED_SHA AF_GROUPS.json OUTDIR
import sys, os, json, hashlib, numpy as np
import bpy, bmesh
blend, exp, gp, od = sys.argv[1:5]
h = hashlib.sha256(open(blend, 'rb').read()).hexdigest(); assert h == exp, ('05AE hash mismatch', h)
rows = json.load(open(gp)); sel = [r['members'] for r in rows if r['in_sculpt_zone'] and r['cls'] == 'SAFE_SCULPT_SEAM']
bpy.ops.wm.open_mainfile(filepath=blend)
o = [x for x in bpy.data.objects if x.type == 'MESH'][0]; me = o.data; n = len(me.vertices)
bm = bmesh.new(); bm.from_mesh(me); bm.verts.ensure_lookup_table()
bmesh.ops.weld_verts(bm, targetmap={bm.verts[v]: bm.verts[g[0]] for g in sel for v in g[1:]}); bm.to_mesh(me); bm.free(); me.update()
W = np.array(o.matrix_world); n2 = len(me.vertices); V2 = np.empty(n2 * 3); me.vertices.foreach_get('co', V2); V2 = V2.reshape(-1, 3) @ W[:3, :3].T + W[:3, 3]
me.calc_loop_triangles(); T2 = np.empty(len(me.loop_triangles) * 3, np.int64); me.loop_triangles.foreach_get('vertices', T2)
np.savez(os.path.join(od, 'after_VF.npz'), V=V2, F=T2.reshape(-1, 3))
rem = np.zeros(n, bool); tgt = np.arange(n)
for g in sel:
    for v in g[1:]: rem[v] = True; tgt[v] = g[0]
o2n = (np.cumsum(~rem) - 1)[tgt]; np.save(os.path.join(od, 'old_to_new_05AE_to_05AF.npy'), o2n)
out = os.path.join(od, 'GO-05AF_full_sculpt_safe_baseline.blend')
bpy.ops.wm.save_as_mainfile(filepath=out, compress=True)
bpy.ops.export_scene.gltf(filepath=os.path.join(od, 'GO-05AF_full_sculpt_safe_baseline.glb'), export_format='GLB')
R = dict(base_sha256=h, groups_welded=len(sel), vertices_removed=int(rem.sum()), vertices_before=n, vertices_after=n2, triangles_after=len(T2) // 3,
         blend_sha256=hashlib.sha256(open(out, 'rb').read()).hexdigest(),
         glb_sha256=hashlib.sha256(open(os.path.join(od, 'GO-05AF_full_sculpt_safe_baseline.glb'), 'rb').read()).hexdigest())
json.dump(R, open(os.path.join(od, 'af_weld_report.json'), 'w'), indent=1); print(json.dumps(R, indent=1))
