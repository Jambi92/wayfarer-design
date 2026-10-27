# propagate.py FROZEN_BASE.blend FROZEN_HM08_MAP.npz RACE_NATIVE.npz OUT_CAND.npz : MPFB Family Propagation Standard v1, step 2 (hm08 -> frozen family base).
# Fits the FROZEN family topology to an accepted MPFB-family race source without any topology change:
#   production vertex i = sum_j M[i, j] * (race hm08 R-6 vertex j)      (M = frozen hm08 -> family-base map, identical for every family member)
#   faces / vertex order / UVs = the frozen base's (UVs read from the frozen .blend UVMap, per corner)
# Preconditions checked (stop on failure): race hm08 face list == frozen hm08 face list (map.hm08_Q), race src_index == map.src_index,
# frozen .blend face list == map.Q. The frozen .blend is opened read-only and never saved.
import sys, os, json, hashlib, numpy as np, scipy.sparse as sp
import bpy
a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
BL, MAPF, NAT, OUT = a[:4]
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
mz = np.load(MAPF); M = sp.csr_matrix((mz['M_data'], mz['M_indices'], mz['M_indptr']), shape=tuple(mz['M_shape'])); Q = mz['Q'].astype(np.int64)
nz = np.load(NAT); meta = json.loads(str(nz['meta']))
chk = dict(hm08_faces_equal=bool(np.array_equal(nz['Q'], mz['hm08_Q'])), src_index_equal=bool(np.array_equal(nz['src_index'], mz['src_index'])))
bpy.ops.wm.open_mainfile(filepath=BL); ob = [o for o in bpy.data.objects if o.type == 'MESH'][0]; me = ob.data
li = np.empty(len(me.loops), np.int32); me.loops.foreach_get('vertex_index', li); chk['frozen_blend_faces_equal_map'] = bool(np.array_equal(li.reshape(-1, 4), Q.astype(np.int32)))
uv = np.empty(len(me.loops) * 2, np.float32); me.uv_layers['UVMap'].data.foreach_get('uv', uv); UV = uv.reshape(-1, 4, 2)
chk['frozen_face_topology_hash'] = hashlib.sha256(li.tobytes()).hexdigest()
if not all(v for k, v in chk.items() if k.endswith('equal') or k.endswith('_map')): print('PRECONDITION FAIL', chk); sys.exit(1)
V = M @ nz['V'].astype(float)
log = dict(step='MPFB Family Propagation Standard v1 -- hm08 -> frozen family base', frozen_base=os.path.basename(BL), frozen_base_sha256=sha(BL), frozen_map=os.path.basename(MAPF), frozen_map_sha256=sha(MAPF),
           race_native=os.path.basename(NAT), race_native_sha256=sha(NAT), checks=chk, verts=int(len(V)), quads=int(len(Q)))
np.savez_compressed(OUT, V=V, Q=Q, UV=UV, M_data=M.data, M_indices=M.indices, M_indptr=M.indptr, M_shape=np.array(M.shape), src_index=nz['src_index'], hm08_Q=nz['Q'], meta=str(nz['meta']), log=json.dumps(log))
print('PROPAGATE', json.dumps(log))
