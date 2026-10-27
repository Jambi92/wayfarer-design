# repair.py CORE_IN.npz CORE_OUT.npz : v003 anatomy / contact repair pass (order 103c832 §5 "no geometry may leave the accepted source envelope
# beyond T-1 / T-2"; §11 no new deformation-class / contact defect). Run with the bpy python (mathutils BVH).
#  1. source-envelope: every SOURCE (hm08) vertex must lie within 0.8 mm of the v003 surface in BOTH configurations (T-2 identity-zone max is 1.5 mm;
#     0.8 mm keeps margin). Offending source vertices that were relocated are restored to their own v002 row; offending source vertices that were
#     not relocated get their relocated 1-ring restored.
#  2. contact: v003 self-intersecting face pairs in hands / feet (v002 has none in configuration 1 and only source toe contact in 2) -> the relocated
#     vertices of those faces (and their 1-ring) are restored.
#  Iterates until clean; then re-audits the §7 stations and reports what changed.
import sys, os, json, numpy as np, scipy.sparse as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy  # noqa: F401
from mathutils.bvhtree import BVHTree
from core3lib import *
IN, OUT = sys.argv[1], sys.argv[2]
B = load(); z = np.load(IN); Q = z['Q']; M3 = sp.csr_matrix((z['M_data'], z['M_indices'], z['M_indptr']), shape=tuple(z['M_shape'])); nV = M3.shape[0]; n2 = int(z['n_v002'])
bs = np.load(W + '/v3_base.npz'); surf = Surface(B['A'], B['Qh'], bs['chart'])
# rebuild the ring-stage base rows (deterministic, same as v003_build R stage)
Qb = B['Q2'].copy(); UVb = B['UV2'].copy(); Mb = B['M2'].copy(); loops0 = closed_loops(Qb, Mb.shape[0]); mir0 = mirror_map(Mb @ B['A'], 0.3)
log = json.loads(str(z['log']))
RINGS = [('pinky_mcp_hypothenar_root', 412, 1006), ('toe1_mtp_root', 491, 1113), ('toe2_mtp_root', 497, 1120), ('toe3_mtp_root', 508, 1132), ('toe4_toe5_mtp_root', 520, 1147)]
for nm, la, lb in RINGS:
    for A_, B_ in ((loops0[la], loops0[lb]), (mir0[loops0[la]], mir0[loops0[lb]])):
        Qb, UVb, Mb, _ = insert_ring(Qb, UVb, Mb, A_.tolist(), B_.tolist())
assert np.array_equal(Qb, Q), 'ring rebuild mismatch'
moved = {int(v): (int(t), b) for v, t, b in zip(z['moved'], z['tri'], z['bary'])}
Adj = adjacency(Q, nV); TRI = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]; qid = np.r_[np.arange(len(Q)), np.arange(len(Q))]
def rows():
    Ml = Mb.tolil(copy=True)
    for v, (t, bc) in moved.items():
        row = {}
        for j, w in zip(surf.T[t], bc):
            if w > 1e-12: row[int(j)] = row.get(int(j), 0.0) + float(w)
        Ml.rows[v] = sorted(row); Ml.data[v] = [row[j] for j in sorted(row)]
    return Ml.tocsr()
def s2p(V, Vh):
    """distance of every hm08 source vertex to the production triangle surface"""
    cen = V[TRI].mean(1); kd = cKDTree(cen); _, idx = kd.query(Vh, k=16); d = np.zeros(len(Vh))
    for i in range(len(Vh)):
        T = TRI[idx[i]]; q, _ = closest_on_tris(np.repeat(Vh[i:i + 1], len(T), 0), V[T[:, 0]], V[T[:, 1]], V[T[:, 2]]); d[i] = np.linalg.norm(q - Vh[i], axis=1).min()
    return d
def selfx(V):
    bvh = BVHTree.FromPolygons(V.tolist(), TRI.tolist(), all_triangles=True, epsilon=0.0); bad = set()
    for i, j in bvh.overlap(bvh):
        fi, fj = qid[i], qid[j]
        if fi == fj or set(Q[fi]) & set(Q[fj]): continue
        bad.add((min(fi, fj), max(fi, fj)))
    return bad
# zones (hands / feet) via R-6 weights carried through the map
r6 = np.load('/home/claude/wayfarer-design/reviews/reference-assets/r6/MF-M-R_r6.npz'); si = np.load(W + '/src/MF-M-R_native.npz')['src_index']
w = {k[2:]: r6[k][si] for k in r6.files if k.startswith('w_')}; hf_h = sum(w[k] for k in ('hand_l', 'hand_r', 'fingers_l', 'fingers_r', 'foot_l', 'foot_r', 'ball_l', 'ball_r'))
hf = (Mb @ hf_h) > 0.5; hff = hf[Q].any(1)
# v002 contact baseline (configuration 2 has source toe contact): count per configuration in hands / feet
base_si = {}
for C in 'MF':
    V2 = B['M2'] @ B[C]['Vh']; Q2 = B['Q2']; T2 = np.r_[Q2[:, [0, 1, 2]], Q2[:, [0, 2, 3]]]; q2 = np.r_[np.arange(len(Q2)), np.arange(len(Q2))]
    bvh = BVHTree.FromPolygons(V2.tolist(), T2.tolist(), all_triangles=True, epsilon=0.0); hf2 = ((B['M2'] @ hf_h) > 0.5)[Q2].any(1); n_ = 0; seen = set()
    for i, j in bvh.overlap(bvh):
        fi, fj = q2[i], q2[j]
        if fi == fj or set(Q2[fi]) & set(Q2[fj]): continue
        k = (min(fi, fj), max(fi, fj))
        if k not in seen: seen.add(k); n_ += hf2[fi] or hf2[fj]
    base_si[C] = n_
print('v002 hand/foot self-x pairs', base_si, 'relocated', len(moved), flush=True)
REP = dict(restored_envelope=[], restored_contact=[], rounds=[])
for rnd in range(12):
    M = rows(); restore = set(); info = {}
    for C in 'MF':
        Vh = B[C]['Vh']; V = M @ Vh; d = s2p(V, Vh); off = np.nonzero(d > 0.08)[0]                          # 0.8 mm
        for j in off:
            if j in moved: restore.add(int(j))
            else:
                for u in Adj.indices[Adj.indptr[j]:Adj.indptr[j + 1]]:
                    if int(u) in moved: restore.add(int(u))
        bad = selfx(V); badhf = [p for p in bad if hff[p[0]] or hff[p[1]]]; info[C] = dict(envelope_off=int(len(off)), max_s2p_mm=round(float(d.max() * 10), 3), selfx_hand_foot=len(badhf), selfx_total=len(bad))
        if len(badhf) > base_si[C]:
            for p in badhf:
                for f_ in p:
                    for v in Q[f_]:
                        if int(v) in moved: restore.add(int(v))
                        for u in Adj.indices[Adj.indptr[v]:Adj.indptr[v + 1]]:
                            if int(u) in moved: restore.add(int(u))
    print('round', rnd, info, 'restore', len(restore), flush=True); REP['rounds'].append(dict(round=rnd, **{C: info[C] for C in 'MF'}, restore=len(restore)))
    if not restore: break
    for v in restore: moved.pop(v, None)
M = rows(); loops = closed_loops(Q, nV); RS = {}
for C in 'MF':
    R = full_s7(M @ B[C]['Vh'], Q, B[C]['meta'], loops); RS[C] = dict(firm_fail=sorted(k for k, r in R.items() if not r['firm']), strict_fail=sorted(k for k, r in R.items() if not r['strict']))
    a = quality(M @ B[C]['Vh'], Q); RS[C]['t4_union'] = int((a[2] | a[3]).sum())
print(json.dumps(RS), flush=True)
UV3 = UVb.copy(); Tq = surf.tq; Tk = surf.tk
for f, q in enumerate(Q):
    for k, v in enumerate(q):
        if int(v) in moved:
            t, bc = moved[int(v)]; corners = [0, 1, 2] if Tk[t] == 0 else [0, 2, 3]; UV3[f, k] = (B['UVh'][Tq[t]][corners] * bc[:, None]).sum(0)
log['repair'] = dict(REP, result=RS); mv = np.array(sorted(moved), int)
np.savez_compressed(OUT, Q=Q, UV=UV3, M_data=M.data, M_indices=M.indices, M_indptr=M.indptr, M_shape=np.array(M.shape), moved=mv, tri=np.array([moved[v][0] for v in mv], int),
                    bary=np.array([moved[v][1] for v in mv]).reshape(-1, 3), pin=z['pin'], n_v002=n2, log=json.dumps(log))
