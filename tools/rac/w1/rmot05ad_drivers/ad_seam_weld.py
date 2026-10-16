# RM-OT-05AD: sculpt-safe seam weld of the frozen 05AB1 clean baseline (working derivative only; baseline untouched).
# Runs in Blender 5.2.2 (bpy module, cloud workspace). Steps:
#  1. verify the baseline .blend SHA-256, open it, read the single mesh object;
#  2. find coincident duplicate vertex groups (pairwise distance <= 0.01 mm);
#  3. keep only groups wholly inside the AC1 torso / shoulder band: 117 <= z <= 168.3 cm from the floor and protection mask == 0
#     (GO-05AC_protect_mask.npy: head, hands, feet, free tail + fused root). The AC1 region mask was too tight: 48 of the 1,480
#     seams opened by the rejected AC1 lay just outside it (shoulder-cap / upper-back edge), so the band rule is used instead;
#  4. write a candidate report, then (only with --apply) collapse each group onto its first member with bmesh weld_verts;
#  5. save GO-05AD_sculpt_safe_baseline.blend and export the review GLB, dump before/after V/F npz for the gates.
# Usage: python ad_seam_weld.py BASE.blend EXPECTED_SHA MASK_AC1.npy PROTECT.npy OUTDIR [--apply]
import sys, os, json, hashlib, numpy as np
import bpy, bmesh
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

blend, exp, mp, pp, od = sys.argv[1:6]; APPLY = '--apply' in sys.argv
os.makedirs(od, exist_ok=True)
h = hashlib.sha256(open(blend, 'rb').read()).hexdigest(); assert h == exp, ('baseline hash mismatch', h)
bpy.ops.wm.open_mainfile(filepath=blend)
meshes = [o for o in bpy.data.objects if o.type == 'MESH']; assert len(meshes) == 1, [o.name for o in meshes]
o = meshes[0]; me = o.data
n = len(me.vertices); V = np.empty(n * 3); me.vertices.foreach_get('co', V); V = V.reshape(-1, 3)
W = np.array(o.matrix_world); Vw = V @ W[:3, :3].T + W[:3, 3]
me.calc_loop_triangles(); T = np.empty(len(me.loop_triangles) * 3, np.int64); me.loop_triangles.foreach_get('vertices', T); T = T.reshape(-1, 3)
np.savez(os.path.join(od, 'before_VF.npz'), V=Vw.astype(np.float64), F=T)
zcm = (Vw[:, 2] - Vw[:, 2].min()) * 100
M = np.load(mp).astype(float); P = np.load(pp).astype(float)
R = dict(baseline=os.path.basename(blend), baseline_sha256=h, object=o.name, blender=bpy.app.version_string,
         vertices_before=n, polygons_before=len(me.polygons), triangles_before=len(T), mask_lengths=[len(M), len(P)],
         world_matrix_identity=bool(np.allclose(W, np.eye(4))), height_cm=round(float(np.ptp(Vw[:, 2])) * 100, 4))
assert len(M) == n and len(P) == n, ('mask length mismatch', len(M), len(P), n)

TOL = 1e-5  # metres = 0.01 mm
pairs = cKDTree(Vw).query_pairs(TOL, output_type='ndarray')
nc, lab = connected_components(coo_matrix((np.ones(len(pairs)), (pairs[:, 0], pairs[:, 1])), shape=(n, n)), directed=False)
sizes = np.bincount(lab); dupgrp = sizes[lab] > 1
gids = np.unique(lab[dupgrp])
allg = {}
for v in np.flatnonzero(dupgrp): allg.setdefault(lab[v], []).append(v)
inband = lambda vs: all(117.0 <= zcm[v] <= 168.3 and P[v] == 0.0 for v in vs)   # torso/shoulder band, never protected regions
sel = [vs for vs in allg.values() if inband(vs)]
spread = lambda vs: float(np.linalg.norm(Vw[vs] - Vw[vs[0]], axis=1).max()) * 1000
R['duplicate_groups_whole_body'] = len(allg); R['duplicate_vertices_whole_body'] = int(dupgrp.sum())
R['candidate_groups_ac1_band'] = len(sel); R['candidate_vertices_ac1_band'] = int(sum(len(v) for v in sel))
R['candidate_group_sizes'] = {str(k): int(c) for k, c in zip(*np.unique([len(v) for v in sel], return_counts=True))} if sel else {}
R['candidate_max_intragroup_distance_mm'] = round(max(spread(v) for v in sel), 6) if sel else None
R['groups_excluded_outside_band'] = len(allg) - len(sel)
if sel:
    C = np.array([Vw[v[0]] for v in sel]) * 100
    R['candidate_bbox_cm'] = dict(min=np.round(C.min(0), 2).tolist(), max=np.round(C.max(0), 2).tolist())
    R['candidate_z_from_floor_cm'] = [round(float(zcm[[v[0] for v in sel]].min()), 2), round(float(zcm[[v[0] for v in sel]].max()), 2)]
    np.save(os.path.join(od, 'candidate_positions_m.npy'), np.array([Vw[v[0]] for v in sel]))
    json.dump([[int(x) for x in v] for v in sel], open(os.path.join(od, 'candidate_groups.json'), 'w'))
if APPLY and sel:
    bm = bmesh.new(); bm.from_mesh(me); bm.verts.ensure_lookup_table()
    tm = {bm.verts[v]: bm.verts[g[0]] for g in sel for v in g[1:]}
    bmesh.ops.weld_verts(bm, targetmap=tm)
    bm.to_mesh(me); bm.free(); me.update()
    n2 = len(me.vertices); V2 = np.empty(n2 * 3); me.vertices.foreach_get('co', V2); V2 = V2.reshape(-1, 3) @ W[:3, :3].T + W[:3, 3]
    me.calc_loop_triangles(); T2 = np.empty(len(me.loop_triangles) * 3, np.int64); me.loop_triangles.foreach_get('vertices', T2)
    np.savez(os.path.join(od, 'after_VF.npz'), V=V2, F=T2.reshape(-1, 3))
    R.update(vertices_after=n2, polygons_after=len(me.polygons), triangles_after=len(T2) // 3, vertices_removed=n - n2)
    # keep a vertex map old->new by nearest position for mask transfer
    d, idx = cKDTree(V2).query(Vw); R['max_old_vertex_to_new_vertex_mm'] = round(float(d.max()) * 1000, 6)
    np.save(os.path.join(od, 'old_to_new_vertex.npy'), idx.astype(np.int64))
    out = os.path.join(od, 'GO-05AD_sculpt_safe_baseline.blend')
    bpy.ops.wm.save_as_mainfile(filepath=out, compress=False)
    bpy.ops.export_scene.gltf(filepath=os.path.join(od, 'GO-05AD_sculpt_safe_baseline.glb'), export_format='GLB')
    R['blend_sha256'] = hashlib.sha256(open(out, 'rb').read()).hexdigest()
    R['glb_sha256'] = hashlib.sha256(open(os.path.join(od, 'GO-05AD_sculpt_safe_baseline.glb'), 'rb').read()).hexdigest()
json.dump(R, open(os.path.join(od, 'weld_report_%s.json' % ('applied' if APPLY else 'candidates')), 'w'), indent=1)
print(json.dumps(R, indent=1))
