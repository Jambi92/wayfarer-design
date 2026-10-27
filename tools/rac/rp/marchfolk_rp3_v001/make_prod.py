# make_prod.py CAND.npz LANDMARKS.json NAME OUTDIR : RP3 -- write a Marchfolk production candidate .blend (one mesh object, quads, UVMap) in the
# production frame (contract §3: m, Z up, faces -Y, subject left +X; origin = pelvis root projected to the ground), plus its geometry hash
# (sha256 of float32 vertex co + int32 loop vertex_index, as RP2) and the hm08 linear map (common-topology mapping) as NAME_hm08_map.npz.
import sys, os, json, hashlib, numpy as np
import bpy
a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
cz = np.load(a[0]); LM = json.load(open(a[1])); NAME = a[2]; O = a[3]; os.makedirs(O, exist_ok=True)
V = cz['V'].astype(float) + np.array(LM['frame']['origin_translation_cm']); Vb = np.c_[V[:, 0], -V[:, 1], V[:, 2]] / 100.0; Q = cz['Q'].astype(int); UV = cz['UV']
bpy.ops.wm.read_factory_settings(use_empty=True)
me = bpy.data.meshes.new(NAME); me.from_pydata(Vb.tolist(), [], Q.tolist()); me.update()
uv = me.uv_layers.new(name='UVMap'); uv.data.foreach_set('uv', UV.reshape(-1, 2).astype(np.float32).ravel())
ob = bpy.data.objects.new(NAME, me); bpy.context.scene.collection.objects.link(ob)
ob['RAC_status'] = a[4] if len(a) > 4 else 'PRODUCTION CANDIDATE (RP3 Marchfolk) - not accepted'; ob['RAC_frame'] = 'm, Z up, faces -Y, subject left +X, origin pelvis root on ground'
for p in me.polygons: p.use_smooth = True
p = os.path.join(O, NAME + '.blend'); bpy.ops.wm.save_as_mainfile(filepath=p, compress=True)
co = np.empty(len(me.vertices) * 3, np.float32); me.vertices.foreach_get('co', co); li = np.empty(len(me.loops), np.int32); me.loops.foreach_get('vertex_index', li)
gh = hashlib.sha256(co.tobytes() + li.tobytes()).hexdigest(); fh = hashlib.sha256(li.tobytes()).hexdigest()
if 'M_data' in cz.files:
    np.savez_compressed(os.path.join(O, NAME + '_hm08_map.npz'), M_data=cz['M_data'], M_indices=cz['M_indices'], M_indptr=cz['M_indptr'], M_shape=cz['M_shape'], hm08_Q=cz['hm08_Q'], Q=cz['Q'],
                        note='production vertex i = sum_j M[i, j] * hm08 body vertex j (hm08 body vertex order = MPFB source vertex src_index[j])', src_index=cz['src_index'])
print(json.dumps(dict(file=p, sha256=hashlib.sha256(open(p, 'rb').read()).hexdigest(), geometry_hash=gh, face_topology_hash=fh, verts=len(me.vertices), quads=len(me.polygons))))
