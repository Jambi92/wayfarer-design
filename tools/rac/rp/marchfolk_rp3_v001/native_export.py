# native_export.py REGEN_SOURCE.blend OUT.npz : RP3 -- read the regenerated MPFB source (never saved back) and export the native hm08 BODY (helpers
# removed: only vertices with body-group weight > 0.5 and faces entirely on them) in the R-6 stance:
#   V (cm, analysis frame x left / f forward / u up, evaluated = posed R-6), Q (quads, body-local indices), src_index (index in the source mesh),
#   UV (per face corner, quads), helper inventory (names + vertex counts of every helper group / extra object), deform weights (dense, body verts x bones),
#   bone names, rig rest + R-6 pose matrices (Blender frame, armature object space), bone heads / tails posed (cm).
import sys, json, numpy as np
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1')
import bpy
a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
bpy.ops.wm.open_mainfile(filepath=a[0])
objs = list(bpy.data.objects); body = [o for o in objs if o.type == 'MESH' and any(m.type == 'ARMATURE' for m in o.modifiers)][0]; rig = body.parent
names = {g.index: g.name for g in body.vertex_groups}; nV = len(body.data.vertices)
G = {}
for v in body.data.vertices:
    for w in v.groups: G.setdefault(names[w.group], {})[v.index] = w.weight
keep = np.array([G['body'].get(i, 0) > 0.5 for i in range(nV)])
# posed coordinates (all modifiers except MASK, as arm_lib.coords)
for md in body.modifiers:
    if md.type == 'MASK': md.show_viewport = False
bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get(); ev = body.evaluated_get(dg); me = ev.to_mesh()
P = np.empty(len(me.vertices) * 3); me.vertices.foreach_get('co', P); ev.to_mesh_clear(); P = P.reshape(-1, 3)
M = np.array(body.matrix_world); P = P @ M[:3, :3].T + M[:3, 3]; Vsrc = np.c_[P[:, 0], -P[:, 1], P[:, 2]] * 100.0
idx = np.nonzero(keep)[0]; remap = -np.ones(nV, int); remap[idx] = np.arange(len(idx))
uvl = body.data.uv_layers.active; Qb = []; UV = []; sizes = {}
for p in body.data.polygons:
    vs = list(p.vertices)
    if all(keep[i] for i in vs):
        sizes[len(vs)] = sizes.get(len(vs), 0) + 1
        if len(vs) == 4: Qb.append([remap[i] for i in vs]); UV.append([tuple(uvl.data[li].uv) for li in p.loop_indices])
deform = [b.name for b in rig.data.bones if b.use_deform]
W = np.zeros((len(idx), len(deform)), np.float32)
for j, n in enumerate(deform):
    for i, w in G.get(n, {}).items():
        if keep[i]: W[remap[i], j] = w
helpers = {n: len(d) for n, d in G.items() if n.startswith('helper') or n.startswith('joint') or n in ('tights', 'skirt', 'hair')}
rest = {b.name: np.array(b.matrix_local) for b in rig.data.bones}; pose = {pb.name: np.array(pb.matrix) for pb in rig.pose.bones}
RM = np.array(rig.matrix_world)
heads = {pb.name: ((RM @ np.r_[np.array(pb.head), 1])[:3] * [100, -100, 100]).tolist() for pb in rig.pose.bones}
tails = {pb.name: ((RM @ np.r_[np.array(pb.tail), 1])[:3] * [100, -100, 100]).tolist() for pb in rig.pose.bones}
parents = {b.name: (b.parent.name if b.parent else None) for b in rig.data.bones}
jc = {n_[6:]: Vsrc[list(d.keys())].mean(0).tolist() for n_, d in G.items() if n_.startswith('joint-')}       # MPFB joint-helper cube centres (posed R-6, cm)
hc = {n_: Vsrc[[i for i, w in d.items() if w > 0.5]].mean(0).tolist() for n_, d in G.items() if n_ in ('helper-l-eye', 'helper-r-eye')}
np.savez_compressed(a[1], V=Vsrc[idx].astype(np.float64), Q=np.array(Qb, np.int32), src_index=idx.astype(np.int32), UV=np.array(UV, np.float32), W=W, bones=np.array(deform),
                    rest=np.array([rest[n] for n in rest]), rest_names=np.array(list(rest)), pose=np.array([pose[n] for n in rest]), rig_world=RM,
                    meta=json.dumps(dict(source_verts=nV, body_verts=int(len(idx)), body_poly_sizes=sizes, helper_groups=helpers, objects=[o.name + ':' + o.type for o in objs],
                                         uv_layers=[u.name for u in body.data.uv_layers], shape_keys=(len(body.data.shape_keys.key_blocks) if body.data.shape_keys else 0),
                                         vertex_groups=len(body.vertex_groups), joint_cubes=jc, eye_helpers=hc, heads=heads, tails=tails, parents=parents, modifiers=[m.type for m in body.modifiers])))
print('NATIVE', a[1], len(idx), sizes, helpers)
