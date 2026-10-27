# make_v5cand.py CORE_V5.npz CORE_V4.npz WORK : MPFB Family Base v005 (final toe-2 web correction, order 33a2dfe) -- per-configuration candidates
# WORK/cand/<ID>_v005.npz through ONE map and ONE face list, the frozen-v003 -> v005, v004 -> v005 and hm08 -> v005 maps, and the weight / UV /
# MPFB-target transfer proofs.
import sys, os, json, numpy as np, scipy.sparse as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v004_lib import *
z = np.load(sys.argv[1]); z4 = np.load(sys.argv[2]); WK = sys.argv[3]; os.makedirs(WK + '/cand', exist_ok=True); os.makedirs(WK + '/maps', exist_ok=True)
M5 = csr(z); Q5 = np.asarray(z['Q']); UV5 = z['UV'].astype(float); rc = z['row_class']; n3 = int(z['n_v003']); nb = int(z['n_base']); n5 = M5.shape[0]; log = json.loads(str(z['log']))
M4 = csr(z4); n4 = M4.shape[0]; B = load_base(); M3 = B['M3']; prov = json.loads(str(z['racetrack_provenance']))
# ---- vertex correspondence: v005 = v003 vertices | retained v004 ring vertices (hip, toe-3; same rows) | toe-2 racetrack vertices
rn5, rp5 = z['ring_name'], z['ring_parents']; rn4, rp4 = z4['ring_name'], z4['ring_parents']; to4 = {}
for nm in sorted(set(rn5.tolist())):
    i5 = np.nonzero(rn5 == nm)[0]; i4 = np.nonzero(rn4 == nm)[0]; assert len(i5) == len(i4) and np.array_equal(rp5[i5], rp4[i4]), nm
    for a, b in zip(i5, i4): to4[n3 + int(a)] = n3 + int(b)
# v003 -> v005 (structural; exact for unchanged v003 rows)
r_, c_, w_ = list(range(n3)), list(range(n3)), [1.0] * n3
for i, (p, q) in enumerate(rp5): r_ += [n3 + i, n3 + i]; c_ += [int(p), int(q)]; w_ += [0.5, 0.5]
for e in prov:
    ps = e['parents']; assert all(p < n3 for p in ps), e
    for p in ps: r_.append(e['vertex']); c_.append(p); w_.append(1.0 / len(ps))
P35 = sp.csr_matrix((w_, (r_, c_)), shape=(n5, n3))
# v004 -> v005 (structural; exact for every vertex present in both with an unchanged row)
r_, c_, w_ = list(range(n3)), list(range(n3)), [1.0] * n3
for a, b in to4.items(): r_.append(a); c_.append(b); w_.append(1.0)
for e in prov:
    for p in e['parents']: r_.append(e['vertex']); c_.append(p); w_.append(1.0 / len(e['parents']))
P45 = sp.csr_matrix((w_, (r_, c_)), shape=(n5, n4))
for nm, P, src in (('v003', P35, 'frozen v003'), ('v004', P45, 'v004 candidate')):
    np.savez_compressed('%s/maps/MPFB_FAMILY_%s_to_v005_map.npz' % (WK, nm), M_data=P.data, M_indices=P.indices, M_indptr=P.indptr, M_shape=np.array(P.shape), row_class=rc,
                        note='v005 vertex i = sum_k M[i, k] * %s vertex k. Exact where the v005 row equals the source row; racetrack vertices are their topological parents '
                             '(edge midpoint / quad centre), re-expressed rows are identity. The authoritative geometry is the hm08 -> v005 map; residuals in the transfer proof.' % src)
proof = dict(verts=int(n5), quads=int(len(Q5)), row_class_counts=log['counts'], row_class_legend=log['row_class_legend'], maps={})
for nm, P, Msrc in (('v003_to_v005', P35, M3), ('v004_to_v005', P45, M4)):
    res = {}
    for cid in CFG:
        Vh = B['C'][cid]['Vh']; d = np.linalg.norm(P @ (Msrc @ Vh) - M5 @ Vh, axis=1); res[cid] = {k: round(float(d[rc == int(k)].max() * 10), 4) for k in log['row_class_legend'] if (rc == int(k)).any()}
    exact = int((np.abs((P @ Msrc) - M5).sum(1).A.ravel() < 1e-12).sum()); proof['maps'][nm] = dict(shape=list(P.shape), exact_rows=exact, max_residual_mm_by_row_class=res)
rs = np.asarray(M5.sum(1)).ravel(); proof['maps']['hm08_to_v005'] = dict(row_sum_min=float(rs.min()), row_sum_max=float(rs.max()), negative_weights=int((M5.data < -1e-12).sum()), max_row_support=int(np.diff(M5.indptr).max()),
                                                                     rows_identical_to_v004=int(sum(1 for i in range(n5) if abs(M5[i] - (M4[to4.get(i, i)] if (i < n3 or i in to4) else M5[i] * 0)).sum() < 1e-12 and (i < n3 or i in to4))))
n = np.load(NAT['MF-M-R']); Wh = n['W'].astype(float); W5 = M5 @ Wh; W4 = M4 @ Wh
same = [i for i in range(n5) if (i < n3 or i in to4) and abs(M5[i] - M4[to4.get(i, i)]).sum() < 1e-12]; src4 = [to4.get(i, i) for i in same]
proof['weights'] = dict(bones=int(Wh.shape[1]), sum_min=float(W5.sum(1).min()), sum_max=float(W5.sum(1).max()), min_weight=float(W5.min()), rows_identical_to_v004=len(same),
                        identical_rows_max_abs_diff_vs_v004=float(np.abs(W5[same] - W4[src4]).max()), rule='v005 weights = M5 @ hm08 weights (convex rows -> partition of unity, non-negative)')
CU = corner_uvs(Q5, UV5, n5); seams = np.array([len(x) > 1 for x in CU]); Q4 = np.asarray(z4['Q']); UV4 = z4['UV'].astype(float)
inv4 = {v: k for k, v in to4.items()}; map4 = lambda v: v if v < n3 else inv4.get(v, -1)
k4 = {tuple(map4(v) for v in q): f for f, q in enumerate(Q4.tolist())}; chg = set(np.nonzero(rc >= 5)[0].tolist())
same_f = [(f, k4[tuple(q)]) for f, q in enumerate(Q5.tolist()) if tuple(q) in k4 and not (set(q) & chg)]
proof['uv'] = dict(faces_identical_to_v004=len(same_f), uv_max_diff_on_those=float(max(np.abs(UV5[a] - UV4[b]).max() for a, b in same_f)), seam_vertices=int(seams.sum()), new_seam_vertices=int(seams[nb:].sum()),
                   uv_in_unit_square=bool((UV5 >= -1e-6).all() and (UV5 <= 1 + 1e-6).all()))
mt = {}
for a_, b_ in (('MF-M-R', 'MF-F-R'), ('MF-F-R', 'SKF208'), ('MF-M-R', 'SK208-C1R')):
    D = B['C'][b_]['Vh'] - B['C'][a_]['Vh']; lhs = M5 @ (B['C'][a_]['Vh'] + D); rhs = M5 @ B['C'][a_]['Vh'] + M5 @ D
    mt['%s -> %s' % (a_, b_)] = dict(max_abs_diff_cm=float(np.abs(lhs - rhs).max()), equals_target_realization=float(np.abs(lhs - M5 @ B['C'][b_]['Vh']).max()))
proof['mpfb_target_transfer'] = dict(cases=mt, rule='family-base morph target = M5 @ (hm08 target delta); exact by linearity')
for cid in CFG:
    nn = np.load(NAT[cid]); V = M5 @ nn['V'].astype(float)
    np.savez_compressed('%s/cand/%s_v005.npz' % (WK, cid), V=V, Q=Q5, UV=UV5.astype(np.float32), M_data=M5.data, M_indices=M5.indices, M_indptr=M5.indptr, M_shape=np.array(M5.shape),
                        src_index=nn['src_index'], hm08_Q=nn['Q'], meta=str(nn['meta']), log=json.dumps(dict(log, configuration=cid)))
json.dump(proof, open(WK + '/maps/MPFB_FAMILY_v005_transfer_proof.json', 'w'), indent=1); print(json.dumps(proof, indent=1)[:2500])
