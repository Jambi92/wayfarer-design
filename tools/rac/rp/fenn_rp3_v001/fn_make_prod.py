# fn_make_prod.py BRANCH.npz FAM.npz LANDMARKS.json NAME OUTDIR STATUS (bpy) : order 6d2eadc §3 / §4 -- the final Fenn RP3 production body:
# CF2 family realization (MPFB Family Base v005 topology) outside the ear branch + the accepted Fenn ear branch topology v002 (E2), one quad mesh in the
# production frame (contract §3: m, Z up, faces -Y, subject left +X; origin = pelvis root projected to the ground, as make_prod.py / ear_blend.py).
#   UVMap   : v005 faces keep their family UV corners; ear-branch faces carry a zero placeholder (UV / materials out of scope; same plan on c1 and c2).
#   groups  : vertex group 'ear_branch' (patch + transition ring).
#   sidecars: NAME_branch_map.npz -- production vertex i = sum_j M[i, j] * hm08 body vertex j for weight / zone proxy rows (v005 rows for kept vertices; branch
#             vertices take the row of the nearest removed v005 ear vertex, same side), plus v005 -> production index map, removed v005 vertices / faces,
#             per-vertex part / side and the production face list; NAME.json (hashes, counts, provenance); NAME_landmarks.json (pelvis-root frame landmarks).
# Hashes as RP2 / make_prod.py: geometry = sha256(float32 co + int32 loop vertex_index), face topology = sha256(int32 loop vertex_index).
import sys, os, json, hashlib, shutil, numpy as np
import bpy
a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
BR, FAM, LMJ, NAME, O, STATUS = a[:6]; os.makedirs(O, exist_ok=True)
z = np.load(BR); fz = np.load(FAM); LM = json.load(open(LMJ)); sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
V = z['V'].astype(float) + np.array(LM['frame']['origin_translation_cm']); Vb = np.c_[V[:, 0], -V[:, 1], V[:, 2]] / 100.0; Q = z['Q'].astype(int); part = z['part']
v2b = z['v005_to_branch']; Q0 = np.asarray(fz['Q']); UV0 = fz['UV']; keepf = np.ones(len(Q0), bool); keepf[z['removed_faces_v005']] = False
key0 = {tuple(sorted(v2b[q])): (i, list(v2b[q])) for i, q in zip(np.nonzero(keepf)[0], Q0[keepf])}
UV = np.zeros((len(Q), 4, 2), np.float32); nuv = 0
for fi, q in enumerate(Q):
    k = key0.get(tuple(sorted(q)))
    if k is None: continue
    i, order = k; m = {v: UV0[i][j] for j, v in enumerate(order)}; UV[fi] = [m[v] for v in q]; nuv += 1
bpy.ops.wm.read_factory_settings(use_empty=True)
me = bpy.data.meshes.new(NAME); me.from_pydata(Vb.tolist(), [], Q.tolist()); me.update()
uvl = me.uv_layers.new(name='UVMap'); uvl.data.foreach_set('uv', UV.reshape(-1, 2).ravel())
ob = bpy.data.objects.new(NAME, me); bpy.context.scene.collection.objects.link(ob)
ob['RAC_status'] = STATUS; ob['RAC_frame'] = 'm, Z up, faces -Y, subject left +X, origin pelvis root on ground'
ob['RAC_composition'] = os.environ.get('RAC_COMPOSITION', 'Fenn RP3: CF2 family realization on MPFB Family Base v005 outside the ear branch + Fenn ear branch topology v002 (E2)')   # order 0f6aba8+: Aelari passes its own
vg = ob.vertex_groups.new(name='ear_branch'); vg.add([int(i) for i in np.nonzero(part != 'v005')[0]], 1.0, 'REPLACE')
for p in me.polygons: p.use_smooth = True
path = os.path.join(O, NAME + '.blend'); bpy.ops.wm.save_as_mainfile(filepath=path, compress=True)
co = np.empty(len(me.vertices) * 3, np.float32); me.vertices.foreach_get('co', co); lv = np.empty(len(me.loops), np.int32); me.loops.foreach_get('vertex_index', lv)
gh = hashlib.sha256(co.tobytes() + lv.tobytes()).hexdigest(); fh = hashlib.sha256(lv.tobytes()).hexdigest()
mp = os.path.join(O, NAME + '_branch_map.npz')
np.savez_compressed(mp, M_data=z['M_data'], M_indices=z['M_indices'], M_indptr=z['M_indptr'], M_shape=z['M_shape'], src_index=z['src_index'], hm08_Q=z['hm08_Q'], Q=z['Q'],
                    v005_to_branch=z['v005_to_branch'], removed_v005=z['removed_v005'], removed_faces_v005=z['removed_faces_v005'], part=z['part'], side=z['side'],
                    note='production vertex i = sum_j M[i, j] * hm08 body vertex j (weight / zone proxy rows; hm08 body vertex order = MPFB source vertex src_index[j]); '
                         'v005_to_branch[v005 vertex] = production vertex (-1 = removed ear-zone vertex); part: v005 / front / back / rim / cuff / transition')
lmo = os.path.join(O, NAME + '_landmarks.json'); shutil.copyfile(LMJ, lmo)
rec = dict(name=NAME, file=NAME + '.blend', file_sha256=sha(path), geometry_hash=gh, face_topology_hash=fh, verts=len(me.vertices), quads=len(me.polygons),
           uv_layer='UVMap', uv_family_faces=nuv, uv_placeholder_faces=int(len(Q) - nuv), vertex_groups=['ear_branch'], ear_branch_vertices=int((part != 'v005').sum()),
           branch_map=os.path.basename(mp), branch_map_sha256=sha(mp), landmarks=os.path.basename(lmo), landmarks_sha256=sha(lmo),
           source_branch_npz_sha256=sha(BR), family_realization_sha256=sha(FAM), embedded_status=STATUS)
json.dump(rec, open(os.path.join(O, NAME + '.json'), 'w'), indent=1); print(json.dumps(rec))
