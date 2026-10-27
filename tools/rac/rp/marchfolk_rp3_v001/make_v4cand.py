# make_v4cand.py CORE_V4.npz WORK : MPFB Family Base v004 -- per-configuration candidates WORK/cand/<ID>_v004.npz (all four accepted family
# configurations through ONE map and ONE face list), the frozen-v003 -> v004 map, and the weight / UV / MPFB-target transfer proofs (order a18371c §8).
import sys, os, json, numpy as np, scipy.sparse as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v004_lib import *
z = np.load(sys.argv[1]); WK = sys.argv[2]; os.makedirs(WK + '/cand', exist_ok=True); os.makedirs(WK + '/maps', exist_ok=True)
M4 = csr(z); Q4 = np.asarray(z['Q']); UV4 = z['UV'].astype(float); rc = z['row_class']; n3 = int(z['n_v003']); n4 = M4.shape[0]; log = json.loads(str(z['log'])); B = load_base(); M3 = B['M3']
proof = dict(verts=int(n4), quads=int(len(Q4)), row_class_counts={k: int((rc == int(k)).sum()) for k in log['row_class_legend']}, row_class_legend=log['row_class_legend'])
# ---- frozen v003 -> v004 structural map (v004 vertex i ~ sum_k P[i, k] * v003 vertex k)
par = z['ring_parents']; assert (par < n3).all(), 'ring parent outside v003'
r_ = list(range(n3)); c_ = list(range(n3)); w_ = [1.0] * n3
for i, (p, q) in enumerate(par): r_ += [n3 + i, n3 + i]; c_ += [int(p), int(q)]; w_ += [0.5, 0.5]
P = sp.csr_matrix((w_, (r_, c_)), shape=(n4, n3))
np.savez_compressed(WK + '/maps/MPFB_FAMILY_v003_to_v004_map.npz', M_data=P.data, M_indices=P.indices, M_indptr=P.indptr, M_shape=np.array(P.shape), row_class=rc,
                    note='v004 vertex i = sum_k M[i, k] * frozen v003 vertex k. EXACT for row_class 0 (unchanged v003 rows); for new ring vertices (class 1 / 3) the row is the '
                         'topological parent edge midpoint and for re-expressed rows (class 2 / 4) the identity; the authoritative geometry of classes 1-4 is the hm08 -> v004 map. '
                         'Residuals per class are recorded in the transfer proof.')
proof['v003_to_v004'] = dict(shape=list(P.shape), exact_rows=int((rc == 0).sum()))
res = {}
for cid in CFG:
    Vh = B['C'][cid]['Vh']; V3 = M3 @ Vh; V4 = M4 @ Vh; d = np.linalg.norm(P @ V3 - V4, axis=1)
    res[cid] = {k: round(float(d[rc == int(k)].max() * 10), 4) if (rc == int(k)).any() else None for k in log['row_class_legend']}
proof['v003_to_v004']['max_residual_mm_by_row_class'] = res
# ---- hm08 -> v004 map properties
rs = np.asarray(M4.sum(1)).ravel(); proof['hm08_map'] = dict(row_sum_min=float(rs.min()), row_sum_max=float(rs.max()), negative_weights=int((M4.data < -1e-12).sum()),
                                                          max_row_support=int(np.diff(M4.indptr).max()), unchanged_rows_identical_to_frozen=bool(abs(M4[:n3][rc[:n3] == 0] - M3[rc[:n3] == 0]).max() == 0))
# ---- weight transfer proof (source rig weights through the map)
n = np.load(NAT['MF-M-R']); Wh = n['W'].astype(float); W4 = M4 @ Wh; W3 = M3 @ Wh
proof['weights'] = dict(bones=int(Wh.shape[1]), sum_min=float(W4.sum(1).min()), sum_max=float(W4.sum(1).max()), min_weight=float(W4.min()),
                        unchanged_rows_max_abs_diff_vs_v003=float(np.abs(W4[:n3][rc[:n3] == 0] - W3[rc[:n3] == 0]).max()),
                        rule='v004 weights = M4 @ hm08 weights (partition of unity and non-negativity inherited because every map row is a convex combination)')
for cid in CFG:
    nn = np.load(NAT[cid]); assert np.array_equal(nn['W'].shape, n['W'].shape)
# ---- UV transfer proof
CU = corner_uvs(Q4, UV4, n4); seams = np.array([len(x) > 1 for x in CU]); CU3 = corner_uvs(B['Q3'], B['UV3'], n3); seams3 = np.array([len(x) > 1 for x in CU3])
fz3 = {tuple(q): f for f, q in enumerate(B['Q3'].tolist())}; same = [(f, fz3[tuple(q)]) for f, q in enumerate(Q4.tolist()) if tuple(q) in fz3]
chg = set(np.nonzero(rc != 0)[0].tolist()); same_un = [(a, b) for a, b in same if not (set(Q4[a].tolist()) & chg)]
proof['uv'] = dict(faces_unchanged=len(same), faces_unchanged_uv_max_diff=float(max(np.abs(UV4[a] - B['UV3'][b]).max() for a, b in same_un)) if same_un else None,
                   seam_vertices_v003=int(seams3.sum()), seam_vertices_v004=int(seams.sum()), new_seam_vertices=int(seams[n3:].sum()), uv_in_unit_square=bool((UV4 >= -1e-6).all() and (UV4 <= 1 + 1e-6).all()),
                   rule='one per-corner UV layout for the family base (identical for every race); split faces interpolate their parent corner UVs; re-expressed '
                        'non-seam vertices take the hm08 UV at their barycentric point')
# ---- MPFB target / morph transfer proof (linearity): race delta = composite MPFB macro target
mt = {}
for a_, b_ in (('MF-M-R', 'MF-F-R'), ('MF-F-R', 'SKF208'), ('MF-M-R', 'SK208-C1R')):
    D = B['C'][b_]['Vh'] - B['C'][a_]['Vh']; lhs = M4 @ (B['C'][a_]['Vh'] + D); rhs = M4 @ B['C'][a_]['Vh'] + M4 @ D
    mt['%s -> %s' % (a_, b_)] = dict(max_abs_diff_cm=float(np.abs(lhs - rhs).max()), equals_target_realization=float(np.abs(lhs - M4 @ B['C'][b_]['Vh']).max()), delta_max_cm=float(np.abs(D).max()))
proof['mpfb_target_transfer'] = dict(cases=mt, rule='a family-base morph target = M4 @ (hm08 target delta); exact by linearity (the map has no per-race term)')
# ---- per-configuration candidates
for cid in CFG:
    nn = np.load(NAT[cid]); V = M4 @ nn['V'].astype(float)
    np.savez_compressed('%s/cand/%s_v004.npz' % (WK, cid), V=V, Q=Q4, UV=UV4.astype(np.float32), M_data=M4.data, M_indices=M4.indices, M_indptr=M4.indptr, M_shape=np.array(M4.shape),
                        src_index=nn['src_index'], hm08_Q=nn['Q'], meta=str(nn['meta']), log=json.dumps(dict(log, configuration=cid)))
json.dump(proof, open(WK + '/maps/MPFB_FAMILY_v004_transfer_proof.json', 'w'), indent=1); print(json.dumps(proof, indent=1)[:3000])
