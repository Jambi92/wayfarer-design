# du_branch.py : RP4 compact-branch candidate MPFB_COMPACT_BRANCH_v001 (order 609c557 §9) -- local midpoint ring insertion on the frozen MPFB Family Base v005.
#   define REF_FAM.npz BRANCH.json [RINGS_PER_SIDE]   : topology-only branch definition from one v005 realization (the accepted central DU137C-NAT):
#       thumb MCP station (validator thumb_ip1 ring station = thumb_02 head, thumb_02 axis, ring test exactly as val2lib / core3lib.encircling):
#       the closed edge rings encircling the thumb axis are ordered along the axis; the ring nearest the MCP is the seed and the quad strips to its
#       two quad strips distal of it (2nd and 3rd ring from the seed: the MCP joint zone where the rings are full digit rings, clear of the thenar web) are
#       each trisected (RINGS = 2 new rings per strip: rung points at 1/3, 2/3). Stored as v005 vertex-index rings (no geometry).
#   apply V005_FAM.npz BRANCH.json OUT.npz            : realize the branch on any v005 realization (any race / configuration):
#       every strip quad (two rung edges between ring A and ring B) is split at n equally spaced rung points -> new vertex = (1 - u) a + u b (a linear map
#       row), the quad becomes n + 1 quads with the original winding; per-corner UVs averaged on the split rungs. V_branch = S V_v005, M_branch = S M_v005 (the family map
#       carried through S, so V_branch = M_branch @ hm08 V exactly and the source weight / morph transfer path is kept). v005 vertex order is unchanged
#       (new vertices appended); split faces keep their index (first half), second halves are appended.
# A bilinear quad split on its 0.5 iso-line keeps the piecewise-bilinear surface: the branch adds support, not shape.
import sys, json, hashlib, numpy as np, scipy.sparse as sp
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001')
from core3lib import closed_loops, ring_stations, encircling
REF_STATURE = 173.143
def strip_quads(Q, A, B):
    a, b = set(A.tolist()), set(B.tolist()); out = []
    for fi, q in enumerate(Q):
        ina = [v in a for v in q]; inb = [v in b for v in q]
        if sum(ina) == 2 and sum(inb) == 2: out.append(fi)
    return out
def define(refp, outp, per_side=2):
    z = np.load(refp); V = z['V'].astype(float); Q = np.asarray(z['Q']); meta = json.loads(str(z['meta'])); loops = closed_loops(Q, len(V))
    H = V[:, 2].max() - V[:, 2].min(); s = H / REF_STATURE; JR = {j[0]: j for j in ring_stations(meta)}; rec = dict(branch='MPFB_COMPACT_BRANCH_v001', parent_face_topology=hashlib.sha256(np.ascontiguousarray(Q, np.int64).tobytes()).hexdigest(), parent_verts=len(V), parent_quads=len(Q), ref=refp, zones={})
    for side in ('l', 'r'):
        nm, c, d, rr, win = JR['thumb_ip1_' + side]; d = d / np.linalg.norm(d)
        ids = encircling(V, loops, c, d, 3.0 * s * 1.6, 1.6 * s * 3)                     # generous search; the validator itself decides the count
        ring = sorted(ids, key=lambda li: float(((V[loops[li]] - c) @ d).mean()))
        tt = [float(((V[loops[li]] - c) @ d).mean()) for li in ring]
        k0 = int(np.argmin(np.abs(tt))); pairs = []
        cand = [(k0 + 1, k0 + 2), (k0 + 2, k0 + 3)]              # the two quad strips across the MCP joint zone distal of the seed ring (thenar-free full rings)
        for i, j in cand:
            if min(i, j) < 0 or max(i, j) >= len(ring): continue
            A, B = loops[ring[i]], loops[ring[j]]; fq = strip_quads(Q, A, B)
            if len(fq) == len(A) == len(B): pairs.append(dict(new_rings=per_side, ring_a=[int(x) for x in A], ring_b=[int(x) for x in B], t_a_cm=round(tt[i], 3), t_b_cm=round(tt[j], 3), strip_quads=len(fq)))
        rec['zones']['hand:thumb_mcp_' + side] = dict(station='thumb_mcp_%s (validator ring station thumb_ip1_%s)' % (side, side), rings_found=len(ring), ring_t_cm=[round(x, 3) for x in tt], seed_ring_t_cm=round(tt[k0], 3), inserted=pairs,
                                                   why='Durrim thumb MCP fails the authoritative D1 closed-ring fallback (2 anatomical rings < 3) on every unbranched v005 Durrim realization (122 / 137 / 152 c1, 137 c2); the relatively large compact-race hand puts the v005 thumb rings at a wider spacing than the stature-normalised station (D4) window')
    json.dump(rec, open(outp, 'w'), indent=1); print(json.dumps({k: (v['rings_found'], v['ring_t_cm'][:8], [(p['t_a_cm'], p['t_b_cm']) for p in v['inserted']]) for k, v in rec['zones'].items()}))
def apply(famp, brp, outp):
    z = dict(np.load(famp, allow_pickle=True)); br = json.load(open(brp)); V = z['V'].astype(np.float64); Q = np.asarray(z['Q']).copy(); nV = len(V)
    assert hashlib.sha256(np.ascontiguousarray(Q, np.int64).tobytes()).hexdigest() == br['parent_face_topology'], 'not a v005 realization'
    UV = np.asarray(z['UV']).copy() if 'UV' in z else None
    rows, cols, vals = list(range(nV)), list(range(nV)), [1.0] * nV; mid = {}; newQ = []; newUV = []; split_faces = []
    def m(a, b, u):
        k = (a, b, round(u, 6))
        if (b, a, round(1 - u, 6)) in mid: return mid[(b, a, round(1 - u, 6))]
        if k not in mid: mid[k] = nV + len(mid); rows.extend([mid[k]] * 2); cols.extend([a, b]); vals.extend([1 - u, u])
        return mid[k]
    for zn, zd in br['zones'].items():
        for p in zd['inserted']:
            A = set(p['ring_a']); n = int(p.get('new_rings', 1)); us = [(t + 1) / (n + 1) for t in range(n)]
            for fi in strip_quads(Q, np.array(p['ring_a']), np.array(p['ring_b'])):
                q = list(Q[fi]); rung = [k for k in range(4) if (q[k] in A) != (q[(k + 1) % 4] in A)]
                assert len(rung) == 2 and rung[1] == rung[0] + 2, 'not a strip quad'
                k = rung[0]; i0, i1, i2, i3 = [(k + t) % 4 for t in range(4)]                # rung edges (i0 -> i1) and (i3 -> i2), i0 / i3 on one ring
                P1 = [q[i0]] + [m(q[i0], q[i1], u) for u in us] + [q[i1]]; P2 = [q[i3]] + [m(q[i3], q[i2], u) for u in us] + [q[i2]]
                uv = UV[fi].copy() if (UV is not None and UV.ndim == 3) else None
                U1 = [uv[i0] * (1 - u) + uv[i1] * u for u in [0] + us + [1]] if uv is not None else None; U2 = [uv[i3] * (1 - u) + uv[i2] * u for u in [0] + us + [1]] if uv is not None else None
                for t in range(n + 1):
                    f = [None] * 4; f[i0], f[i1], f[i2], f[i3] = P1[t], P1[t + 1], P2[t + 1], P2[t]
                    if t == 0: Q[fi] = f
                    else: newQ.append(f)
                    if uv is not None:
                        g = uv.copy(); g[i0], g[i1], g[i2], g[i3] = U1[t], U1[t + 1], U2[t + 1], U2[t]
                        if t == 0: UV[fi] = g
                        else: newUV.append(g)
                split_faces.append(int(fi))
    S = sp.csr_matrix((vals, (rows, cols)), shape=(nV + len(mid), nV)); Vb = S @ V
    Qb = np.vstack([Q, np.array(newQ, Q.dtype)]) if newQ else Q
    out = dict(z); out['V'] = Vb.astype(z['V'].dtype); out['Q'] = Qb
    if UV is not None and UV.ndim == 3 and newUV: out['UV'] = np.concatenate([UV, np.array(newUV, UV.dtype)])
    if 'M_data' in z:
        M = sp.csr_matrix((z['M_data'], z['M_indices'], z['M_indptr']), shape=tuple(z['M_shape'])); Mb = (S @ M).tocsr()
        out.update(M_data=Mb.data, M_indices=Mb.indices, M_indptr=Mb.indptr, M_shape=np.array(Mb.shape))
    out['branch_S_data'] = S.data; out['branch_S_indices'] = S.indices; out['branch_S_indptr'] = S.indptr; out['branch_S_shape'] = np.array(S.shape)
    out['branch_split_faces'] = np.array(split_faces, np.int64); out['branch'] = np.array(br['branch']); out['parent_verts'] = np.array(nV)
    np.savez_compressed(outp, **out)
    print('BRANCH', outp, 'V', nV, '->', len(Vb), 'Q', len(z['Q']), '->', len(Qb), 'new rings verts', len(mid))
if __name__ == '__main__':
    if sys.argv[1] == 'define': define(sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 2)
    else: apply(sys.argv[2], sys.argv[3], sys.argv[4])
