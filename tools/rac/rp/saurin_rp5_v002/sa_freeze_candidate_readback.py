# sa_freeze_candidate_readback.py BLEND CANDIDATE.npz FACE_SEM.npy CONFIG(v_M|v_F) OUT.json : clean read-back of one freeze-candidate .blend in a FRESH Blender
#   process (order cd87d9c §7): objects / names / types / visibility, vertex + quad counts, face-list and vertex-order identity, semantic attribute identity,
#   topology hash, provenance properties, max vertex read-back error vs the candidate realised on the clean working source, transforms, units / scale,
#   modifiers, shape keys, constraints, parenting, geometry-node / node groups, materials, images, libraries, external file references.
import sys, os, json, hashlib, numpy as np, bpy
BL, CG, FSEM, KEY, OUT = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:6]; W = os.environ.get('SA_W', '/tmp/claude-0/rp5clean')
bpy.ops.wm.open_mainfile(filepath=BL)
z = np.load(CG); Q = z['Q'].astype(np.int64); w = np.load(W + '/work/SA_RP5_WORK_v001.npz'); F = w['f'].astype(np.int64)
V = (z['bc'][:, :, None] * w[KEY].astype(float)[F[z['tri']]]).sum(1); fsem = np.load(FSEM, allow_pickle=True); labs = sorted(set(map(str, fsem))); fsi = np.array([labs.index(str(x)) for x in fsem], np.int32)
tag = os.path.splitext(os.path.basename(BL))[0]; r = dict(file=os.path.basename(BL), sha256=hashlib.sha256(open(BL, 'rb').read()).hexdigest(), blender=bpy.app.version_string)
r['objects'] = [dict(name=o.name, type=o.type, hidden_viewport=o.hide_viewport, hidden_render=o.hide_render, hidden_get=o.hide_get(), parent=o.parent.name if o.parent else None) for o in bpy.data.objects]
r['collections'] = [c.name for c in bpy.data.collections]; r['scene_objects'] = [o.name for o in bpy.context.scene.objects]
ob = bpy.data.objects.get(tag); r['expected_object_present'] = ob is not None and ob.type == 'MESH'
me = ob.data
co = np.zeros(len(me.vertices) * 3); me.vertices.foreach_get('co', co); co = co.reshape(-1, 3)
sizes = np.zeros(len(me.polygons), np.int64); me.polygons.foreach_get('loop_total', sizes)
lt = np.zeros(len(me.loops), np.int64); me.loops.foreach_get('vertex_index', lt); st = np.zeros(len(me.polygons), np.int64); me.polygons.foreach_get('loop_start', st)
all_quads = bool((sizes == 4).all()); Qr = lt[(st[:, None] + np.arange(4))] if all_quads else None
sv = np.zeros(len(me.polygons), np.int32); me.attributes['semantic'].data.foreach_get('value', sv)
r.update(verts=len(me.vertices), quads=int(len(me.polygons)), all_quads=all_quads, face_list_identical=bool(all_quads and np.array_equal(Qr, Q)),
         vertex_order_identical=bool(len(co) == len(V)), max_vertex_readback_error_cm=float(np.abs(co - V).max()),
         semantic_identical=bool(np.array_equal(sv, fsi)), semantic_table_identical=json.loads(ob['semantic_table']) == labs,
         topology_sha256=hashlib.sha256(np.ascontiguousarray(Qr).tobytes()).hexdigest() if all_quads else None,
         properties={k: ob[k] for k in ob.keys() if isinstance(ob[k], (str, int, float))}, scene_status=bpy.context.scene.get('status'),
         transform=dict(location=list(ob.location), rotation_euler=list(ob.rotation_euler), rotation_mode=ob.rotation_mode, scale=list(ob.scale), delta_location=list(ob.delta_location),
                        delta_scale=list(ob.delta_scale), matrix_world_diag=[ob.matrix_world[i][i] for i in range(4)]),
         unit_settings=dict(system=bpy.context.scene.unit_settings.system, scale_length=bpy.context.scene.unit_settings.scale_length),
         modifiers=[m.type for m in ob.modifiers], constraints=[c.type for c in ob.constraints], shape_keys=(None if me.shape_keys is None else [k.name for k in me.shape_keys.key_blocks]),
         materials=[m.name for m in bpy.data.materials], images=[i.name for i in bpy.data.images], libraries=[l.filepath for l in bpy.data.libraries], node_groups=[n.name for n in bpy.data.node_groups],
         meshes=[m.name for m in bpy.data.meshes], external_paths=sorted(set(bpy.utils.blend_paths(absolute=True))), mesh_attributes=[a.name for a in me.attributes if not a.name.startswith('.')])
clean = (r['expected_object_present'] and len(r['objects']) == 1 and r['face_list_identical'] and r['semantic_identical'] and r['max_vertex_readback_error_cm'] < 1e-4
         and not r['modifiers'] and not r['constraints'] and r['shape_keys'] is None and not r['libraries'] and not r['external_paths'] and not r['node_groups']
         and not r['images'] and r['properties'].get('status') == 'FREEZE CANDIDATE / NOT FROZEN' and 'FROZEN' not in r['properties'].get('status').replace('NOT FROZEN', '')
         and r['transform']['location'] == [0, 0, 0] and r['transform']['rotation_euler'] == [0, 0, 0] and all(abs(s - 0.01) < 1e-9 for s in r['transform']['scale']))
r['readback_verdict'] = 'PASS' if clean else 'FAIL'
json.dump(r, open(OUT, 'w'), indent=1); print(tag, r['readback_verdict'], r['max_vertex_readback_error_cm'])
