# ear_blend.py BRANCH.npz FAM.npz LANDMARKS.json NAME OUTDIR (bpy) : order bdcd6a6 review file -- the Fenn ear-branch prototype realization
# as one quad mesh in the production frame (contract §3: m, Z up, faces -Y, subject left +X; origin = pelvis root on the ground, as make_prod.py).
# v005 faces keep their UVMap corners; branch faces carry a zero placeholder UV (UV / materials are out of scope, order §21). Vertex group
# 'ear_branch' marks the branch (patch + transition ring). Writes NAME.blend and its geometry hash (sha256 float32 co + int32 loop vertex_index).
import sys, os, json, hashlib, numpy as np
import bpy
a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
z = np.load(a[0]); fz = np.load(a[1]); LM = json.load(open(a[2])); NAME = a[3]; O = a[4]; os.makedirs(O, exist_ok=True)
V = z['V'].astype(float) + np.array(LM['frame']['origin_translation_cm']); Vb = np.c_[V[:, 0], -V[:, 1], V[:, 2]] / 100.0; Q = z['Q'].astype(int); part = z['part']
# UV corners for kept v005 faces: identify by sorted vertex sets
v2b = z['v005_to_branch']; Q0 = np.asarray(fz['Q']); UV0 = fz['UV']; keepf = np.ones(len(Q0), bool); keepf[z['removed_faces_v005']] = False
key0 = {tuple(sorted(v2b[q])): (i, list(v2b[q])) for i, q in zip(np.nonzero(keepf)[0], Q0[keepf])}
UV = np.zeros((len(Q), 4, 2), np.float32)
for fi, q in enumerate(Q):
    k = key0.get(tuple(sorted(q)))
    if k is None: continue
    i, order = k; uv = UV0[i]; m = {v: uv[j] for j, v in enumerate(order)}; UV[fi] = [m[v] for v in q]
bpy.ops.wm.read_factory_settings(use_empty=True)
me = bpy.data.meshes.new(NAME); me.from_pydata(Vb.tolist(), [], Q.tolist()); me.update()
uvl = me.uv_layers.new(name='UVMap'); uvl.data.foreach_set('uv', UV.reshape(-1, 2).ravel())
ob = bpy.data.objects.new(NAME, me); bpy.context.scene.collection.objects.link(ob)
ob['RAC_status'] = os.environ.get('EAR_BLEND_STATUS', 'FENN EAR BRANCH PROTOTYPE (order bdcd6a6) - review only, not accepted, not frozen'); ob['RAC_frame'] = 'm, Z up, faces -Y, subject left +X, origin pelvis root on ground'
vg = ob.vertex_groups.new(name='ear_branch'); vg.add([int(i) for i in np.nonzero(part != 'v005')[0]], 1.0, 'REPLACE')
for p in me.polygons: p.use_smooth = True
path = os.path.join(O, NAME + '.blend'); bpy.ops.wm.save_as_mainfile(filepath=path, compress=True)
co = np.empty(len(me.vertices) * 3, np.float32); me.vertices.foreach_get('co', co); lv = np.empty(len(me.loops), np.int32); me.loops.foreach_get('vertex_index', lv)
gh = hashlib.sha256(co.tobytes() + lv.tobytes()).hexdigest(); fh = hashlib.sha256(open(path, 'rb').read()).hexdigest()
json.dump(dict(name=NAME, verts=len(me.vertices), faces=len(me.polygons), geometry_sha256=gh, file_sha256=fh, branch_vertices=int((part != 'v005').sum())), open(os.path.join(O, NAME + '.json'), 'w'), indent=1)
print(NAME, gh, fh)
