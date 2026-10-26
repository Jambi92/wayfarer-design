# make_v3cand.py CORE.npz : write the per-configuration v003 candidates cand/MF-{M,F}-R_v003.npz (same layout as v002: V, Q, UV, hm08 map M3, src_index,
# hm08_Q, meta, log) plus the v002 -> v003 map. v003 vertex positions are M3 @ (that configuration's hm08 R-6 vertices), so both configurations come from
# one map and one face list.
import sys, os, json, numpy as np, scipy.sparse as sp
W = '/tmp/claude-0/rt/m3'; z = np.load(sys.argv[1]); M3 = sp.csr_matrix((z['M_data'], z['M_indices'], z['M_indptr']), shape=tuple(z['M_shape']))
v2 = np.load(W + '/cand/MF-M-R_v002.npz'); M2 = sp.csr_matrix((v2['M_data'], v2['M_indices'], v2['M_indptr']), shape=tuple(v2['M_shape'])); n2 = M2.shape[0]
# v002 -> v003: hm08 vertex j == v002 vertex j (first block of v002 is the hm08 vertex set, identity rows), so M3's hm08 columns are v002 columns
assert abs(M2[:13380, :13380] - sp.identity(13380)).max() < 1e-12
M23 = sp.csr_matrix((M3.data, M3.indices, M3.indptr), shape=(M3.shape[0], n2))
for C in 'MF':
    n = np.load('%s/src/MF-%s-R_native.npz' % (W, C)); V = M3 @ n['V'].astype(float)
    np.savez_compressed('%s/cand/MF-%s-R_v003.npz' % (W, C), V=V, Q=z['Q'], UV=z['UV'].astype(np.float32), M_data=M3.data, M_indices=M3.indices, M_indptr=M3.indptr, M_shape=np.array(M3.shape),
                        src_index=n['src_index'], hm08_Q=n['Q'], meta=str(n['meta']), log=str(z['log']))
    # check: v002-routed positions equal direct hm08 positions
    V2 = M2 @ n['V'].astype(float); print(C, 'verts', len(V), 'quads', len(z['Q']), 'v002-route max diff', float(np.abs(M23 @ V2 - V).max()))
np.savez_compressed(W + '/cand/MF_v002_to_v003_map.npz', M_data=M23.data, M_indices=M23.indices, M_indptr=M23.indptr, M_shape=np.array(M23.shape),
                    note='v003 vertex i = sum_k M[i, k] * v002 vertex k (identical for both configurations)')
