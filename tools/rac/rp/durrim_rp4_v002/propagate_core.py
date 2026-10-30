# propagate_core.py CORE.npz HM08_MAP.npz RACE_NATIVE.npz OUT_CAND.npz : MPFB Family Propagation Standard v1 step 2, cloud form.
# Identical maths/output to tools/rac/rp/mpfb_family/propagate.py, but the frozen face list and per-corner UVs are read from the committed
# MPFB_FAMILY_BASE_v005_core.npz (repo) instead of the frozen production .blend on the PC. Preconditions: core Q == map Q, race hm08 faces ==
# map hm08_Q, race src_index == map src_index. The frozen-blend hash is recorded from the committed production hash list (not re-read).
import sys, os, json, hashlib, numpy as np, scipy.sparse as sp
CORE, MAPF, NAT, OUT = sys.argv[1:5]
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
FROZEN_BLEND_SHA = 'e560386cf041368568a79a3395343e95bedcbde5386bcd22ecc3288286a19a92'  # MF_M_REF_RP3_retopo_v005.blend (production_files_sha256.txt)
mz = np.load(MAPF); M = sp.csr_matrix((mz['M_data'], mz['M_indices'], mz['M_indptr']), shape=tuple(mz['M_shape'])); Q = mz['Q'].astype(np.int64)
cz = np.load(CORE); nz = np.load(NAT)
chk = dict(hm08_faces_equal=bool(np.array_equal(nz['Q'], mz['hm08_Q'])), src_index_equal=bool(np.array_equal(nz['src_index'], mz['src_index'])),
           core_faces_equal_map=bool(np.array_equal(cz['Q'].astype(np.int64), Q)),
           frozen_face_topology_hash=hashlib.sha256(Q.astype(np.int32).tobytes()).hexdigest())
if not all(v for k, v in chk.items() if k != 'frozen_face_topology_hash'): print('PRECONDITION FAIL', chk); sys.exit(1)
UV = cz['UV'].astype(np.float32)
V = M @ nz['V'].astype(float)
log = dict(step='MPFB Family Propagation Standard v1 -- hm08 -> frozen family base (cloud: faces/UV from committed v005 core)',
           frozen_base='MF_M_REF_RP3_retopo_v005.blend', frozen_base_sha256=FROZEN_BLEND_SHA, frozen_core=os.path.basename(CORE), frozen_core_sha256=sha(CORE),
           frozen_map=os.path.basename(MAPF), frozen_map_sha256=sha(MAPF), race_native=os.path.basename(NAT), race_native_sha256=sha(NAT),
           checks=chk, verts=int(len(V)), quads=int(len(Q)))
np.savez_compressed(OUT, V=V, Q=Q, UV=UV, M_data=M.data, M_indices=M.indices, M_indptr=M.indptr, M_shape=np.array(M.shape), src_index=nz['src_index'],
                    hm08_Q=nz['Q'], meta=str(nz['meta']), log=json.dumps(log))
print('PROPAGATE', json.dumps(log))
