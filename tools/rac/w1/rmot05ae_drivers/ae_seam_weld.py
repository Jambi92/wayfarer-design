# RM-OT-05AE: extend the sculpt-safe seam weld of the frozen 05AD baseline up through the neck base (117.0-172.0 cm from floor).
# Exact / coincident duplicates only (pairwise <= 0.01 mm). Hands / feet / free tail + root stay excluded via the 05AC protection
# mask (carried onto 05AD indices through the 05AD weld map). The protection mask's head rule (z > 168.3 cm) is lifted only up
# to 172.0 cm, as order 05AE s3 allows for neck-base duplicates (0.000 mm displacement). Runs in Blender 5.2.2 (bpy, cloud).
# Usage: python ae_seam_weld.py BASE_05AD.blend EXPECTED_SHA PROTECT_05AC.npy O2N_05AD.npy OUTDIR [--apply]
import sys, os, json, hashlib, numpy as np
import bpy, bmesh
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
blend, exp, pp, mp, od = sys.argv[1:6]; APPLY = '--apply' in sys.argv; ZLO, ZHI, ZHEAD = 117.0, 172.0, 168.3
os.makedirs(od, exist_ok=True)
h = hashlib.sha256(open(blend, 'rb').read()).hexdigest(); assert h == exp, ('05AD hash mismatch', h)
bpy.ops.wm.open_mainfile(filepath=blend)
o = [x for x in bpy.data.objects if x.type == 'MESH'][0]; me = o.data
n = len(me.vertices); V = np.empty(n * 3); me.vertices.foreach_get('co', V); W = np.array(o.matrix_world); V = V.reshape(-1, 3) @ W[:3, :3].T + W[:3, 3]
me.calc_loop_triangles(); T = np.empty(len(me.loop_triangles) * 3, np.int64); me.loop_triangles.foreach_get('vertices', T)
np.savez(os.path.join(od, 'before_VF.npz'), V=V, F=T.reshape(-1, 3))
z = (V[:, 2] - V[:, 2].min()) * 100
P0 = np.load(pp); o2n = np.load(mp); P = np.zeros(n); np.maximum.at(P, o2n, P0); np.save(os.path.join(od, 'protect_05AD_index.npy'), P)
pairs = cKDTree(V).query_pairs(1e-5, output_type='ndarray')
nc, lab = connected_components(coo_matrix((np.ones(len(pairs)), (pairs[:, 0], pairs[:, 1])), shape=(n, n)), directed=False)
groups = {}
for v in np.flatnonzero(np.bincount(lab)[lab] > 1): groups.setdefault(lab[v], []).append(int(v))
ok = lambda v: ZLO <= z[v] <= ZHI and (P[v] == 0 or z[v] > ZHEAD)
sel = [g for g in groups.values() if all(ok(v) for v in g)]
R = dict(base=os.path.basename(blend), base_sha256=h, vertices_before=n, triangles_before=len(T) // 3,
         duplicate_groups_remaining_whole_body=len(groups), newly_merged_groups=len(sel), newly_merged_vertices=int(sum(len(g) - 1 for g in sel)),
         group_sizes={str(k): int(c) for k, c in zip(*np.unique([len(g) for g in sel], return_counts=True))} if sel else {},
         max_intragroup_distance_mm=round(max(float(np.linalg.norm(V[g] - V[g[0]], axis=1).max()) for g in sel) * 1000, 6) if sel else None,
         z_range_cm=[round(float(min(z[g[0]] for g in sel)), 2), round(float(max(z[g[0]] for g in sel)), 2)] if sel else None,
         groups_in_168_3_to_172=int(sum(1 for g in sel if z[g[0]] > ZHEAD)))
json.dump(sel, open(os.path.join(od, 'ae_weld_groups_05AD_indices.json'), 'w'))
if APPLY and sel:
    bm = bmesh.new(); bm.from_mesh(me); bm.verts.ensure_lookup_table()
    bmesh.ops.weld_verts(bm, targetmap={bm.verts[v]: bm.verts[g[0]] for g in sel for v in g[1:]}); bm.to_mesh(me); bm.free(); me.update()
    n2 = len(me.vertices); V2 = np.empty(n2 * 3); me.vertices.foreach_get('co', V2); V2 = V2.reshape(-1, 3) @ W[:3, :3].T + W[:3, 3]
    me.calc_loop_triangles(); T2 = np.empty(len(me.loop_triangles) * 3, np.int64); me.loop_triangles.foreach_get('vertices', T2)
    np.savez(os.path.join(od, 'after_VF.npz'), V=V2, F=T2.reshape(-1, 3))
    rem = np.zeros(n, bool); tgt = np.arange(n)
    for g in sel:
        for v in g[1:]: rem[v] = True; tgt[v] = g[0]
    np.save(os.path.join(od, 'old_to_new_exact.npy'), (np.cumsum(~rem) - 1)[tgt])
    R.update(vertices_after=n2, triangles_after=len(T2) // 3)
    out = os.path.join(od, 'GO-05AE_sculpt_safe_baseline.blend')
    bpy.ops.wm.save_as_mainfile(filepath=out, compress=True)
    bpy.ops.export_scene.gltf(filepath=os.path.join(od, 'GO-05AE_sculpt_safe_baseline.glb'), export_format='GLB')
    R['blend_sha256'] = hashlib.sha256(open(out, 'rb').read()).hexdigest()
    R['glb_sha256'] = hashlib.sha256(open(os.path.join(od, 'GO-05AE_sculpt_safe_baseline.glb'), 'rb').read()).hexdigest()
json.dump(R, open(os.path.join(od, 'ae_weld_report_%s.json' % ('applied' if APPLY else 'candidates')), 'w'), indent=1)
print(json.dumps(R, indent=1))
