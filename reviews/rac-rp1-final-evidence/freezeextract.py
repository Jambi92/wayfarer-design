# freezeextract.py (bpy) -- BLEND OUT.npz REF.npz OUT.json : extract the mesh from the frozen file, write it in the
# analysis frame (cm, y flipped) with REF's auxiliary arrays, hash the geometry, compare with REF (accepted rev110).
import bpy, sys, numpy as np, json, hashlib
a = sys.argv[sys.argv.index('--') + 1:]
bpy.ops.wm.open_mainfile(filepath=a[0]); obs = [o for o in bpy.data.objects if o.type == 'MESH']; o = obs[0]; m = o.data
V = np.zeros(len(m.vertices) * 3, np.float32); m.vertices.foreach_get('co', V); V = V.reshape(-1, 3)
nf = len(m.polygons); ls = np.zeros(nf, np.int32); m.polygons.foreach_get('loop_total', ls)
F = np.zeros(int(ls.sum()), np.int32); m.polygons.foreach_get('vertices', F)
gh = hashlib.sha256(V.tobytes() + F.tobytes()).hexdigest()
z = np.load(a[2]); P = (z['V'] * np.array([1, -1, 1]) / 100).astype(np.float64); Q = z['Q']
same_order = len(V) == len(P) and (ls == 4).all() and np.array_equal(F.reshape(-1, 4), Q)
dev = float(np.abs(V.astype(np.float64) - P).max() * 1000) if len(V) == len(P) else None
Va = V.astype(np.float64) * 100 * np.array([1, -1, 1])
np.savez(a[1], V=Va, Q=F.reshape(-1, 4), **{k: z[k] for k in z.files if k not in ('V', 'Q')})
r = dict(objects=[x.name for x in obs], object=o.name, vertices=len(V), faces=nf, all_quads=bool((ls == 4).all()), geometry_sha256_f32_verts_int32_faces=gh,
         faces_and_order_identical_to_rev110=bool(same_order), max_vertex_diff_vs_rev110_mm=dev, matrix_identity=bool(np.allclose(np.array(o.matrix_world), np.eye(4))),
         bbox_m=dict(min=V.min(0).tolist(), max=V.max(0).tolist()))
print(json.dumps(r)); json.dump(r, open(a[3], 'w'), indent=1)
