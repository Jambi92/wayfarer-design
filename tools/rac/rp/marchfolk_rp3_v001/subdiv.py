# subdiv.py NATIVE.npz OUT.npz [RINGS.json] : RP3 v002 bounded topology candidate generator (order d18ff2a §10).
# Step 1 -- one level of LINEAR (simple) quad subdivision of the native hm08 body: every hm08 vertex is kept (same index, first block), every edge gets
#   its midpoint, every quad its corner average, and each quad becomes 4 quads. No smoothing: the new surface is the source surface (edge midpoints lie on
#   it exactly; face points within the quad's non-planarity). The operation is a fixed sparse linear map M (new = M @ hm08), so UVs, MPFB targets and
#   source weights carry over exactly, and both Marchfolk configurations (identical hm08 topology) get identical v002 topology.
# Step 2 (optional RINGS.json) -- targeted closed-ring insertions: for each listed pair of adjacent closed loops (found on the subdivided mesh by the audit),
#   every quad of the strip between them is split by a new loop through the midpoints of the connecting edges (quad-only; no T-junction because the strip
#   is closed). Also linear (part of M).
# Output: V (cm), Q, UV (per corner), M (CSR: data / indices / indptr / shape), src_index, plus provenance.
import sys, json, numpy as np, scipy.sparse as sp
a = sys.argv[1:]; z = np.load(a[0]); V0 = z['V'].astype(float); Q0 = np.asarray(z['Q']); UV0 = z['UV'].astype(float); n0 = len(V0)
# ---- level-1 linear subdivision
E = np.sort(np.concatenate([Q0[:, [0, 1]], Q0[:, [1, 2]], Q0[:, [2, 3]], Q0[:, [3, 0]]]), 1); uE, einv = np.unique(E, axis=0, return_inverse=True); nE = len(uE); nF = len(Q0)
eid = einv.reshape(4, nF).T                      # edge id of side k (k -> k+1) of every quad
rows = list(range(n0)); cols = list(range(n0)); vals = [1.0] * n0
for i, (p, q) in enumerate(uE): rows += [n0 + i] * 2; cols += [p, q]; vals += [0.5, 0.5]
for f in range(nF): rows += [n0 + nE + f] * 4; cols += list(Q0[f]); vals += [0.25] * 4
M = sp.csr_matrix((vals, (rows, cols)), shape=(n0 + nE + nF, n0))
Q = []; UV = []
for f in range(nF):
    c = n0 + nE + f; e = n0 + eid[f]; v = Q0[f]; uv = UV0[f]; uvc = uv.mean(0); uve = [(uv[k] + uv[(k + 1) % 4]) / 2 for k in range(4)]
    for k in range(4):   # quad at corner k: v_k, e_k, c, e_{k-1}  (keeps the original winding)
        Q.append([v[k], e[k], c, e[(k - 1) % 4]]); UV.append([uv[k], uve[k], uvc, uve[(k - 1) % 4]])
Q = np.array(Q, np.int32); UV = np.array(UV, np.float32); log = dict(step1='linear level-1 subdivision', hm08_verts=n0, verts_after_step1=int(M.shape[0]), quads_after_step1=int(len(Q)))
# ---- optional ring insertions
if len(a) > 2:
    RG = json.load(open(a[2])); V = M @ V0; nV = len(V); extra_rows = []; ins = []
    for ring in RG['rings']:                      # ring = {name, A: loop vertex list, B: adjacent closed loop} on the subdivided mesh
        A_ = set(ring['A']); B_ = set(ring['B']); Qn = []; UVn = []; mid = {}
        for qi, q in enumerate(Q):
            ina = [k for k in range(4) if q[k] in A_]; inb = [k for k in range(4) if q[k] in B_]
            if len(ina) == 2 and len(inb) == 2:
                # sides connecting A to B
                conn = [k for k in range(4) if (q[k] in A_) != (q[(k + 1) % 4] in A_)]
                k1, k2 = conn; pts = []
                for k in (k1, k2):
                    key = (min(q[k], q[(k + 1) % 4]), max(q[k], q[(k + 1) % 4]))
                    if key not in mid: mid[key] = nV + len(extra_rows); extra_rows.append(key)
                    pts.append(mid[key])
                uv = UV[qi]; m1 = (uv[k1] + uv[(k1 + 1) % 4]) / 2; m2 = (uv[k2] + uv[(k2 + 1) % 4]) / 2
                # split: [q[k1], pts0, pts1, q[k2+1]] and [pts0, q[k1+1], q[k2], pts1]
                Qn.append([q[k1], pts[0], pts[1], q[(k2 + 1) % 4]]); UVn.append([uv[k1], m1, m2, uv[(k2 + 1) % 4]])
                Qn.append([pts[0], q[(k1 + 1) % 4], q[k2], pts[1]]); UVn.append([m1, uv[(k1 + 1) % 4], uv[k2], m2])
            else: Qn.append(list(q)); UVn.append(UV[qi])
        Q = np.array(Qn, np.int32); UV = np.array(UVn, np.float32); ins.append(ring.get('name'))
    if extra_rows:
        r_ = []; c_ = []; v_ = []
        for i, (p, q) in enumerate(extra_rows): r_ += [i, i]; c_ += [p, q]; v_ += [0.5, 0.5]
        Mx = sp.csr_matrix((v_, (r_, c_)), shape=(len(extra_rows), nV)) @ M; M = sp.vstack([M, Mx]).tocsr()
    log.update(step2_rings=len(RG['rings']), verts_added_step2=len(extra_rows))
V = M @ V0
log.update(verts=int(len(V)), quads=int(len(Q)))
np.savez_compressed(a[1], V=V, Q=Q, UV=UV, M_data=M.data, M_indices=M.indices, M_indptr=M.indptr, M_shape=np.array(M.shape), src_index=z['src_index'], hm08_Q=Q0,
                    meta=str(z['meta']), log=json.dumps(log))
print(json.dumps(log))
