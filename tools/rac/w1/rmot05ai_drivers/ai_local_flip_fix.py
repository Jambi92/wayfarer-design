# RM-OT-05AI s4: bounded local mesh-quality fix on the frozen 05AF baseline.
# Step 1 (crimp relax): vertices of faces folded > 60 deg against ALL neighbours (pre-existing micro-crimps) are moved along the
#   normal of their one-ring best-fit plane onto that plane, capped at 0.5 mm per vertex; repeated for 3 sweeps.
# Step 2 (edge rotations): see below.
# Neighbourhoods: 2-ring vertex sets around the 7 author-listed faces (643992, 686657, 907533, 441095, 448814, 468838, 919029).
# An interior edge (both incident triangles fully inside a neighbourhood) is rotated when it raises the worse of its two triangles'
# quality (4*sqrt(3)*A / sum(e^2)) by > 0.02, the two triangles are near-coplanar (dihedral < 15 deg) and the new triangles keep the
# old orientation (normal dot > 0.95). Repeated until no improving rotation remains (max 20 sweeps). Vertex positions never change.
# Usage: python ai_local_flip_fix.py BASE_05AF.blend EXPECTED_SHA OUTDIR
import sys, os, json, hashlib, numpy as np
import bpy, bmesh
blend, exp, od = sys.argv[1:4]; os.makedirs(od, exist_ok=True)
FACES = [643992, 686657, 907533, 441095, 448814, 468838, 919029]
h = hashlib.sha256(open(blend, 'rb').read()).hexdigest(); assert h == exp, ('05AF hash mismatch', h)
bpy.ops.wm.open_mainfile(filepath=blend)
o = [x for x in bpy.data.objects if x.type == 'MESH'][0]; me = o.data
assert all(len(p.vertices) == 3 for p in me.polygons)
bm = bmesh.new(); bm.from_mesh(me); bm.verts.ensure_lookup_table(); bm.faces.ensure_lookup_table()
V0 = np.array([v.co[:] for v in bm.verts])
def q(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c); n = np.cross(b - a, c - a); A = np.linalg.norm(n) / 2
    s = ((b - a) ** 2).sum() + ((c - b) ** 2).sum() + ((a - c) ** 2).sum(); return 4 * np.sqrt(3) * A / s if s > 0 else 0.0, n
hood = set()
for fi in FACES:
    ring = set(v.index for v in bm.faces[fi].verts)
    for _ in range(2):
        ring |= set(e.other_vert(bm.verts[v]).index for v in list(ring) for e in bm.verts[v].link_edges)
    hood |= ring
before_faces = {tuple(sorted(v.index for v in f.verts)) for f in bm.faces if all(v.index in hood for v in f.verts)}
bm.normal_update()
moved = {}
# crimp faces: folded > 60 deg against all neighbours
crimp = []
for fi in FACES:
    f = bm.faces[fi]
    folds = [np.degrees(np.arccos(np.clip(f.normal.dot([x for x in e.link_faces if x != f][0].normal), -1, 1))) for e in f.edges]
    if min(folds) > 60: crimp.append(fi)
relax_set = set()
for fi in crimp:
    for v in bm.faces[fi].verts: relax_set.add(v.index)
CAP = 5e-4
for it in range(int(os.environ.get('AI_RELAX_SWEEPS', '8'))):
    newpos = {}
    for vi in relax_set:
        v = bm.verts[vi]; nb = np.array([e.other_vert(v).co[:] for e in v.link_edges]); tgt = nb.mean(0)
        p = np.array(v.co[:]) + 0.5 * (tgt - np.array(v.co[:])); p0 = V0[vi]; dd = np.linalg.norm(p - p0)
        if dd > CAP: p = p0 + (p - p0) * (CAP / dd)
        newpos[vi] = p
    for vi, p in newpos.items(): bm.verts[vi].co = p.tolist(); moved[vi] = float(np.linalg.norm(p - V0[vi]))
    bm.normal_update()
bm.normal_update()
rot = []
for sweep in range(int(os.environ.get('AI_ROT_SWEEPS', '20'))):
    changed = 0
    for e in list(bm.edges):
        if not e.is_valid or not e.is_manifold or len(e.link_faces) != 2: continue
        f1, f2 = e.link_faces
        if not all(v.index in hood for f in (f1, f2) for v in f.verts): continue
        a, b = e.verts; c = [v for v in f1.verts if v not in (a, b)][0]; d = [v for v in f2.verts if v not in (a, b)][0]
        if bm.edges.get([c, d]) is not None: continue                              # new diagonal must not already exist
        if f1.normal.dot(f2.normal) < np.cos(np.radians(15)): continue               # only near-coplanar pairs
        q1, _ = q(a.co, b.co, c.co); q2, _ = q(a.co, b.co, d.co); old = min(q1, q2)
        q3, _ = q(c.co, d.co, a.co); q4, _ = q(c.co, d.co, b.co); new = min(q3, q4)
        if new <= old + 0.02: continue
        nav = np.array(f1.normal) + np.array(f2.normal); nav /= np.linalg.norm(nav) + 1e-30
        # convex, near-planar quad a-c-b-d: a and b on opposite sides of cd, c and d on opposite sides of ab (in the nav plane)
        A_, B_, C_, D_ = (np.array(x.co[:]) for x in (a, b, c, d))
        side = lambda p, x, y: np.dot(np.cross(y - x, p - x), nav)
        if not (side(A_, C_, D_) * side(B_, C_, D_) < 0 and side(C_, A_, B_) * side(D_, A_, B_) < 0): continue
        m1 = np.cross(D_ - C_, A_ - C_); m2 = np.cross(D_ - C_, B_ - C_)
        m1 /= np.linalg.norm(m1) + 1e-30; m2 /= np.linalg.norm(m2) + 1e-30
        if abs(np.dot(m1, nav)) < 0.97 or abs(np.dot(m2, nav)) < 0.97: continue        # new triangles stay near the local plane
        ne = bmesh.utils.edge_rotate(e, True)
        if ne is None: continue
        bm.normal_update()
        nf = list(ne.link_faces)
        ok = len(nf) == 2 and all(np.dot(np.array(f.normal), nav) > 0.95 for f in nf) and nf[0].normal.dot(nf[1].normal) > np.cos(np.radians(15))
        if not ok:
            back = bmesh.utils.edge_rotate(ne, False); bm.normal_update()
            if back is None: raise RuntimeError('could not revert rotation')
            continue
        rot.append(dict(sweep=sweep, edge_was=[a.index, b.index], edge_now=[c.index, d.index], q_old=round(float(old), 4), q_new=round(float(new), 4)))
        changed += 1
    if not changed: break
bm.faces.ensure_lookup_table(); bm.normal_update()
after_faces = {tuple(sorted(v.index for v in f.verts)) for f in bm.faces if all(v.index in hood for v in f.verts)}
V1 = np.array([v.co[:] for v in bm.verts]); dv = np.linalg.norm(V1 - V0, axis=1); assert set(np.flatnonzero(dv > 0)) <= hood
bm.to_mesh(me); bm.free(); me.update()
W = np.array(o.matrix_world); Vw = V1 @ W[:3, :3].T + W[:3, 3]
me.calc_loop_triangles(); T = np.empty(len(me.loop_triangles) * 3, np.int64); me.loop_triangles.foreach_get('vertices', T)
np.savez(os.path.join(od, 'after_VF.npz'), V=Vw, F=T.reshape(-1, 3)); np.save(os.path.join(od, 'hood_vertices.npy'), np.array(sorted(hood)))
out = os.path.join(od, 'GO-05AI_local_quality_baseline.blend'); bpy.ops.wm.save_as_mainfile(filepath=out, compress=True)
bpy.ops.export_scene.gltf(filepath=os.path.join(od, 'GO-05AI_local_quality_baseline.glb'), export_format='GLB')
R = dict(base_sha256=h, neighbourhood_vertices=len(hood), edge_rotations=len(rot), rotations=rot,
         faces_removed=sorted([list(f) for f in before_faces - after_faces]), faces_added=sorted([list(f) for f in after_faces - before_faces]),
         vertices_moved={str(k): round(v * 1000, 4) for k, v in sorted(moved.items())}, max_vertex_move_mm=round(float(dv.max()) * 1000, 4), blend_sha256=hashlib.sha256(open(out, 'rb').read()).hexdigest(),
         glb_sha256=hashlib.sha256(open(os.path.join(od, 'GO-05AI_local_quality_baseline.glb'), 'rb').read()).hexdigest())
json.dump(R, open(os.path.join(od, 'ai_prep_report.json'), 'w'), indent=1)
print(json.dumps({k: v for k, v in R.items() if k not in ('rotations', 'faces_removed', 'faces_added')}, indent=1))
for fi in FACES: pass
