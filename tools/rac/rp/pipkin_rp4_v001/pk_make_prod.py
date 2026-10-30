# pk_make_prod.py CB.npz LANDMARKS.json NAME OUTDIR STATUS (bpy) : RP4 Pipkin order 68ba8e5 §5 -- Pipkin production reference candidate on MPFB_PIPKIN_COMPACT_BRANCH_v001
# (thumb MCP two-direction densification only) over MPFB Family Base v005. One quad mesh in the production frame
# (contract §3: m, Z up, faces -Y, subject left +X; origin = pelvis root projected to the ground, as make_prod.py / fn_make_prod.py).
#   UVMap   : every face carries its UV corners (v005 faces: family UVs; branch faces: bilinear interpolation of the parent v005 face UVs, seam-aware).
#   groups  : 'compact_branch_thumb' (new + re-placed thumb vertices). Adapted from durrim_rp4_v002/du_make_prod.py (frozen Durrim tool untouched).
#   sidecars: NAME_branch_map.npz -- production vertex i = sum_j M[i, j] * hm08 body vertex j EXACTLY (M = S M_v005; S = branch rows over v005, also stored),
#             v005 -> production index map (identity: v005 order preserved; branch vertices appended), branch face lists, per-vertex part;
#             NAME.json (hashes, counts, provenance); NAME_landmarks.json (pelvis-root frame landmarks).
# Hashes as RP2 / make_prod.py: geometry = sha256(float32 co + int32 loop vertex_index), face topology = sha256(int32 loop vertex_index).
import sys, os, json, hashlib, shutil, numpy as np
import bpy
a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
CB, LMJ, NAME, O, STATUS = a[:5]; os.makedirs(O, exist_ok=True)
z = np.load(CB); LM = json.load(open(LMJ)); sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
V = z['V'].astype(float) + np.array(LM['frame']['origin_translation_cm']); Vb = np.c_[V[:, 0], -V[:, 1], V[:, 2]] / 100.0; Q = z['Q'].astype(int); part = z['branch_part']
UV = np.asarray(z['UV'], np.float32)
bpy.ops.wm.read_factory_settings(use_empty=True)
me = bpy.data.meshes.new(NAME); me.from_pydata(Vb.tolist(), [], Q.tolist()); me.update()
assert len(me.polygons) == len(Q) and all(len(p.vertices) == 4 for p in me.polygons)
uvl = me.uv_layers.new(name='UVMap'); uvl.data.foreach_set('uv', UV.reshape(-1, 2).ravel())
ob = bpy.data.objects.new(NAME, me); bpy.context.scene.collection.objects.link(ob)
ob['RAC_status'] = STATUS; ob['RAC_frame'] = 'm, Z up, faces -Y, subject left +X, origin pelvis root on ground'
ob['RAC_composition'] = 'Pipkin RP4: accepted Pipkin source on MPFB Family Base v005 + MPFB_PIPKIN_COMPACT_BRANCH_v001 (thumb MCP two-direction densification only)'
g1 = ob.vertex_groups.new(name='compact_branch_thumb'); g1.add([int(i) for i in np.nonzero(np.isin(part, ['thumb_new', 'thumb_moved']))[0]], 1.0, 'REPLACE')
for p in me.polygons: p.use_smooth = True
path = os.path.join(O, NAME + '.blend'); bpy.ops.wm.save_as_mainfile(filepath=path, compress=True)
co = np.empty(len(me.vertices) * 3, np.float32); me.vertices.foreach_get('co', co); lv = np.empty(len(me.loops), np.int32); me.loops.foreach_get('vertex_index', lv)
gh = hashlib.sha256(co.tobytes() + lv.tobytes()).hexdigest(); fh = hashlib.sha256(lv.tobytes()).hexdigest()
nV0 = int(z['parent_verts']); v2p = np.arange(nV0)
mp = os.path.join(O, NAME + '_branch_map.npz')
np.savez_compressed(mp, M_data=z['M_data'], M_indices=z['M_indices'], M_indptr=z['M_indptr'], M_shape=z['M_shape'], src_index=z['src_index'], hm08_Q=z['hm08_Q'], Q=z['Q'],
                    S_data=z['branch_S_data'], S_indices=z['branch_S_indices'], S_indptr=z['branch_S_indptr'], S_shape=z['branch_S_shape'], v005_to_production=v2p,
                    thumb_faces=z['branch_thumb_faces'], neck_faces=z['branch_neck_faces'], part=part, branch=z['branch'], branch_def_sha256=z['branch_def_sha256'],
                    note='production vertex i = sum_j M[i, j] * hm08 body vertex j (exact; hm08 body vertex order = MPFB source vertex src_index[j]); M = S M_v005 with S the '
                         'MPFB_PIPKIN_COMPACT_BRANCH_v001 rows over v005 vertices; v005 vertex order preserved (v005_to_production = identity), branch vertices appended; '
                         'part: v005 / thumb_new / thumb_moved')
lmo = os.path.join(O, NAME + '_landmarks.json'); shutil.copyfile(LMJ, lmo)
rec = dict(name=NAME, file=NAME + '.blend', file_sha256=sha(path), geometry_hash=gh, face_topology_hash=fh, verts=len(me.vertices), quads=len(me.polygons),
           uv_layer='UVMap', vertex_groups=['compact_branch_thumb'], thumb_branch_vertices=int(len(g1_ := np.nonzero(np.isin(part, ['thumb_new', 'thumb_moved']))[0])),
           branch=str(z['branch']), branch_def_sha256=str(z['branch_def_sha256']),
           branch_map=os.path.basename(mp), branch_map_sha256=sha(mp), landmarks=os.path.basename(lmo), landmarks_sha256=sha(lmo), source_cb2_npz_sha256=sha(CB), embedded_status=STATUS)
json.dump(rec, open(os.path.join(O, NAME + '.json'), 'w'), indent=1); print(json.dumps(rec))
