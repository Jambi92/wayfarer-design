# hv_make_prod.py BRANCH.npz FAM.npz LANDMARKS.json NAME OUTDIR STATUS TRI_HV1.npz (bpy) : Halvren final whole-character production reference (consolidation order
# 2026-10-30 §9) = fenn_rp3_v001/fn_make_prod.py (production frame, UVMap, 'ear_branch' group, branch-map / landmark / json sidecars; unchanged) + the frozen
# TRI-HV1 production triangulation carried downstream (Halvren ear family freeze, HALVREN-CF-EAR-TRI-LOD-1):
#   face attribute 'TRI_HV1_diagonal' (INT, FACE): 0 = split (v0,v1,v2)+(v0,v2,v3), 1 = split (v0,v1,v3)+(v1,v2,v3) in the polygon's vertex order (= the frozen
#   per-quad choice; every face, ear branch and body); sidecar NAME_TRI-HV1.npz: diagonal choice, the baked triangle list and its sha256 (= frozen hash).
#   Production exports must triangulate with this attribute (or use the sidecar triangles), never with an importer rule.
import sys, os, json, hashlib, shutil, numpy as np
import bpy
a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
BR, FAM, LMJ, NAME, O, STATUS, TRI = a[:7]; os.makedirs(O, exist_ok=True)
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
tz = np.load(TRI); ch = tz['diagonal_choice'].astype(np.int32); assert len(ch) == len(Q)
at = me.attributes.new('TRI_HV1_diagonal', 'INT', 'FACE'); at.data.foreach_set('value', ch)
Tb = np.empty((2 * len(Q), 3), np.int64); A_ = ch == 0; Tb[0::2][A_], Tb[1::2][A_] = Q[A_][:, [0, 1, 2]], Q[A_][:, [0, 2, 3]]; Tb[0::2][~A_], Tb[1::2][~A_] = Q[~A_][:, [0, 1, 3]], Q[~A_][:, [1, 2, 3]]
tri_sha = hashlib.sha256(Tb.tobytes()).hexdigest(); assert tri_sha == str(tz['triangles_sha256']), 'TRI-HV1 triangles differ from the frozen hash'
ob['RAC_triangulation'] = 'TRI-HV1 (frozen, mandatory): triangulate with face attribute TRI_HV1_diagonal or the NAME_TRI-HV1.npz triangles; never an importer rule; LODs with LOD-HV1'
path = os.path.join(O, NAME + '.blend'); bpy.ops.wm.save_as_mainfile(filepath=path, compress=True)
co = np.empty(len(me.vertices) * 3, np.float32); me.vertices.foreach_get('co', co); lv = np.empty(len(me.loops), np.int32); me.loops.foreach_get('vertex_index', lv)
gh = hashlib.sha256(co.tobytes() + lv.tobytes()).hexdigest(); fh = hashlib.sha256(lv.tobytes()).hexdigest()
mp = os.path.join(O, NAME + '_branch_map.npz')
np.savez_compressed(mp, M_data=z['M_data'], M_indices=z['M_indices'], M_indptr=z['M_indptr'], M_shape=z['M_shape'], src_index=z['src_index'], hm08_Q=z['hm08_Q'], Q=z['Q'],
                    v005_to_branch=z['v005_to_branch'], removed_v005=z['removed_v005'], removed_faces_v005=z['removed_faces_v005'], part=z['part'], side=z['side'],
                    note='production vertex i = sum_j M[i, j] * hm08 body vertex j (weight / zone proxy rows; hm08 body vertex order = MPFB source vertex src_index[j]); '
                         'v005_to_branch[v005 vertex] = production vertex (-1 = removed ear-zone vertex); part: v005 / front / back / rim / cuff / transition')
lmo = os.path.join(O, NAME + '_landmarks.json'); shutil.copyfile(LMJ, lmo)
tp = os.path.join(O, NAME + '_TRI-HV1.npz'); np.savez_compressed(tp, diagonal_choice=ch.astype(np.int8), triangles=Tb.astype(np.int32), triangles_sha256=np.array(tri_sha),
                                                                 note=np.array('TRI-HV1 baked production triangulation (Halvren ear family freeze): quad (a,b,c,d) -> 0: (a,b,c)+(a,c,d), 1: (a,b,d)+(b,c,d); face order = the blend polygons'))
rec = dict(name=NAME, file=NAME + '.blend', file_sha256=sha(path), geometry_hash=gh, face_topology_hash=fh, verts=len(me.vertices), quads=len(me.polygons),
           uv_layer='UVMap', uv_family_faces=nuv, uv_placeholder_faces=int(len(Q) - nuv), vertex_groups=['ear_branch'], ear_branch_vertices=int((part != 'v005').sum()),
           branch_map=os.path.basename(mp), branch_map_sha256=sha(mp), landmarks=os.path.basename(lmo), landmarks_sha256=sha(lmo),
           source_branch_npz_sha256=sha(BR), family_realization_sha256=sha(FAM), embedded_status=STATUS,
           face_attributes=['TRI_HV1_diagonal'], tri_hv1=os.path.basename(tp), tri_hv1_sha256=sha(tp), tri_hv1_triangles_sha256=tri_sha)
json.dump(rec, open(os.path.join(O, NAME + '.json'), 'w'), indent=1); print(json.dumps(rec))
