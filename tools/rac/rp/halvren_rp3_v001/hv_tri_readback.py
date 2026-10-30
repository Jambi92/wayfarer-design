# hv_tri_readback.py BLEND TRI_HV1.npz OUT.json (bpy) : read-back of the TRI-HV1 production triangulation carried by a Halvren production .blend (no save):
# the face attribute TRI_HV1_diagonal re-derives the baked triangles; their sha256 must equal the sidecar / frozen hash.
import sys, json, hashlib, numpy as np
import bpy
a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
BL, TRI, OUT = a[:3]; bpy.ops.wm.open_mainfile(filepath=BL); me = [o for o in bpy.data.objects if o.type == 'MESH'][0].data
lt = np.empty(len(me.polygons), np.int32); me.polygons.foreach_get('loop_total', lt); lv = np.empty(len(me.loops), np.int32); me.loops.foreach_get('vertex_index', lv); Q = lv.reshape(-1, 4).astype(np.int64)
ch = np.empty(len(me.polygons), np.int32); me.attributes['TRI_HV1_diagonal'].data.foreach_get('value', ch)
T = np.empty((2 * len(Q), 3), np.int64); A = ch == 0; T[0::2][A], T[1::2][A] = Q[A][:, [0, 1, 2]], Q[A][:, [0, 2, 3]]; T[0::2][~A], T[1::2][~A] = Q[~A][:, [0, 1, 3]], Q[~A][:, [1, 2, 3]]
tz = np.load(TRI); h = hashlib.sha256(T.tobytes()).hexdigest()
r = dict(blend=BL, all_quads=bool((lt == 4).all()), attribute_choice_equals_sidecar=bool(np.array_equal(ch, tz['diagonal_choice'].astype(np.int32))), triangles_sha256=h,
         equals_sidecar_hash=h == str(tz['triangles_sha256']), sidecar_triangles_equal=bool(np.array_equal(T.astype(np.int32), tz['triangles'])))
json.dump(r, open(OUT, 'w'), indent=1); print(json.dumps(r))
