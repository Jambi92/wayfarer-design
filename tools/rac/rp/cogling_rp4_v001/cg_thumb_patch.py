# cg_thumb_patch.py : Cogling copy of pipkin_rp4_v001/pk_thumb_patch.py (frozen Durrim / Pipkin tools left untouched; order 9424c72 §7 / §10). Same two-direction
# engineering architecture; the thumb grid rows are defined on the Cogling central body and every vertex placement is re-solved on the Cogling bodies (cg_thumb_relax.py).
# Pipkin header follows:
# pk_thumb_patch.py : Pipkin copy of durrim_rp4_v002/thumb_patch.py (frozen Durrim tool left untouched). Same two-direction architecture; Pipkin-specific: no unsplit sector.
# thumb_patch.py : MPFB_COMPACT_BRANCH_v002 -- thumb MCP two-direction local densification (order 8080f9f §4).
#
# Topology (per thumb, all indices on the frozen v005 face hash; aligned ring grid from thumb_grid.py):
#   rows P (= Z-1, thenar transition ring), Z (MCP seed ring, t ~ 0), A, B, C, D  (20 columns each).
#   fine region Z..C: every column split circumferentially x2 (40-vertex rings Zf, Af, Bf, T1, T2, Cf); two new rings T1, T2 inside B->C
#   (u = a, b) -> axial x3 there. Strips Zf->Af, Af->Bf, Bf->T1, T1->T2, T2->Cf are regular quad grids (no poles).
#   transitions (2:1 "fan" template, 3 quads per column pair) only in the full-height parent strips P->Z (proximal) and C->D (distal):
#       5-poles on P / D (coarse side), 3-poles on Z / C (fine side). P, Z, C, D are never counted rings; Af, Bf, T1, T2 stay valence-4 loops.
#   fan-centre parity per thumb (PHASE): avoids the existing v005 5-poles on P and keeps both thumb UV seams (SEAM) on kept rung edges.
# Every new vertex is a bilinear point of one parent quad -> one row of S with <= 4 non-zeros: V = S V_v005, M = S M_v005 (map / UV / weight path kept).
# Removed parent quads: P->Z, Z->A, A->B, B->C, C->D (100 per thumb). New quads fill the removed face slots in order, the rest are appended.
import sys, json, hashlib, numpy as np, scipy.sparse as sp
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/durrim_rp4_v002'); sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/pipkin_rp4_v001')
from thumb_grid import grid, edges_of
BR = 'MPFB_COGLING_COMPACT_BRANCH_v001'
DEF_PARAMS = dict(a=1 / 3, b=2 / 3, zr=0.18, cr=0.18, dphase=0, ms=0.5)
PHASE = dict(l=dict(p=0, d=0), r=dict(p=1, d=1))   # fan-centre parity per thumb: avoids the v005 5-poles on P and keeps both UV seams on kept rung edges
def face_hash(Q): return hashlib.sha256(np.ascontiguousarray(Q, np.int64).tobytes()).hexdigest()
def define_side(z, side):
    """aligned rows P, Z, A, B, C, D (v005 vertex ids) for one thumb"""
    g = grid(z, side, 5); G = g['G']; Q = np.asarray(z['Q']); E = edges_of(Q)
    nb = {}
    for q in Q:
        for k in range(4):
            a, b = int(q[k]), int(q[(k + 1) % 4]); nb.setdefault(a, set()).add(b); nb.setdefault(b, set()).add(a)
    Z, A = G[0], G[1]; zs = set(Z.tolist()); P = []
    for i, v in enumerate(Z):
        c = [w for w in nb[int(v)] if w not in zs and w != int(A[i])]; assert len(c) == 1, 'Z vertex not valence 4'; P.append(c[0])
    P = np.array(P); assert all((min(P[i], P[(i + 1) % 20]), max(P[i], P[(i + 1) % 20])) in E for i in range(20)), 'P not a ring'
    rows = np.vstack([P[None], G[:5]]); return dict(rows=rows.tolist(), t=[None] + [round(float(x), 4) for x in g['t'][:5]])
def define(refp, outp):
    z = np.load(refp); Q = np.asarray(z['Q']); rec = dict(branch=BR, parent='MPFB Family Base v005', parent_face_topology=face_hash(Q), parent_verts=int(len(z['V'])),
                                                         parent_quads=int(len(Q)), ref=refp.split('/')[-1], zones={}, params=DEF_PARAMS)
    for side in ('l', 'r'): rec['zones']['hand:thumb_mcp_' + side] = define_side(z, side)
    json.dump(rec, open(outp, 'w'), indent=1); return rec
# ------------------------------------------------------------------------------------------------ realization
_FIDX = {}
SEAM = dict(l=[5, 13], r=[0, 8])
UNSPLIT = dict(l=[], r=[])   # Cogling: every column split unless a Cogling hand / hip-slab conflict is demonstrated (Durrim c2 sector NOT inherited)
_CH = {}
def uv_charts(Q0, UV0):
    key = (len(Q0), float(UV0[0, 0, 0]))
    if key in _CH: return _CH[key]
    from scipy.sparse.csgraph import connected_components
    E = {}
    for f, q in enumerate(Q0):
        for k in range(4):
            a, b = int(q[k]), int(q[(k + 1) % 4]); E.setdefault((min(a, b), max(a, b)), []).append((f, k))
    r, c = [], []
    for (a, b), L in E.items():
        if len(L) != 2: continue
        (f, k), (g, j) = L; ua = {int(Q0[f][k]): UV0[f][k], int(Q0[f][(k + 1) % 4]): UV0[f][(k + 1) % 4]}; ub = {int(Q0[g][j]): UV0[g][j], int(Q0[g][(j + 1) % 4]): UV0[g][(j + 1) % 4]}
        if all(np.abs(ua[v] - ub[v]).max() < 1e-6 for v in ua): r.append(f); c.append(g)
    n, lab = connected_components(sp.coo_matrix((np.ones(len(r)), (r, c)), shape=(len(Q0), len(Q0))), directed=False); _CH[key] = lab; return lab
_CONT = {}
def uv_continuity(Q0, UV0):
    """face -> faces sharing an edge with identical corner UVs (no seam between them)"""
    key = (len(Q0), float(UV0[0, 0, 0]))
    if key in _CONT: return _CONT[key]
    E = {}
    for f, q in enumerate(Q0):
        for k in range(4):
            a, b = int(q[k]), int(q[(k + 1) % 4]); E.setdefault((min(a, b), max(a, b)), []).append((f, k))
    adj = {}
    for (a, b), L in E.items():
        if len(L) != 2: continue
        (f, k), (g, j) = L; ua = {int(Q0[f][k]): UV0[f][k], int(Q0[f][(k + 1) % 4]): UV0[f][(k + 1) % 4]}; ub = {int(Q0[g][j]): UV0[g][j], int(Q0[g][(j + 1) % 4]): UV0[g][(j + 1) % 4]}
        if all(np.abs(ua[v] - ub[v]).max() < 1e-6 for v in ua): adj.setdefault(f, set()).add(g); adj.setdefault(g, set()).add(f)
    _CONT[key] = adj; return adj
_FOV = {}
def FACES_OF(Q0, verts):
    key = len(Q0)
    if key not in _FOV:
        d = {}
        for f, q in enumerate(Q0):
            for x in q: d.setdefault(int(x), set()).add(f)
        _FOV[key] = d
    s = None
    for v in verts: s = _FOV[key][v] if s is None else s & _FOV[key][v]
    return sorted(s)
class Builder:
    def __init__(s, Q, nV, UV):
        s.Q = Q; s.nV = nV; s.UV = UV; s.rows = []; s.cols = []; s.vals = []; s.key = {}; s.nnew = 0; s.newQ = []; s.newUV = []; s.removed = []
        s.moved = {}; key = (len(Q), int(Q[0, 0]), int(Q[-1, -1]))
        if key not in _FIDX: _FIDX[key] = {frozenset(int(x) for x in q): fi for fi, q in enumerate(Q)}
        s.fidx = _FIDX[key]
    def pquad(s, a, b, c, d):
        """parent face with corners (a,b,c,d) in (s,u) order (0,0),(1,0),(1,1),(0,1); returns (face id, corner position of each in Q[fi])"""
        fi = s.fidx[frozenset((int(a), int(b), int(c), int(d)))]; q = [int(x) for x in s.Q[fi]]; return fi, [q.index(int(x)) for x in (a, b, c, d)]
    def vert(s, corners, su):
        """vertex at bilinear (s, u) of parent quad corners (c00, c10, c11, c01); parent vertex when (s,u) is a corner"""
        (a, b, c, d), (x, y) = corners, su; w = np.array([(1 - x) * (1 - y), x * (1 - y), x * y, (1 - x) * y]); ids = np.array([a, b, c, d], np.int64)
        m = w > 1e-12; ids, w = ids[m], w[m]
        if len(ids) == 1: return int(ids[0])
        k = tuple(sorted((int(i), round(float(v), 9)) for i, v in zip(ids, w)))
        if k not in s.key:
            s.key[k] = s.nV + s.nnew; s.nnew += 1
            for i, v in zip(ids, w): s.rows.append(s.key[k]); s.cols.append(int(i)); s.vals.append(float(v))
        return s.key[k]
    def move(s, pid, corners, su):
        """parent vertex pid re-placed (inside the branch zone) at bilinear (s,u) of a parent quad it belongs to: its own S row, same index"""
        (a, b, c, d), (x, y) = corners, su; w = np.array([(1 - x) * (1 - y), x * (1 - y), x * y, (1 - x) * y]); ids = np.array([a, b, c, d], np.int64)
        m = w > 1e-12; assert int(pid) in set(int(i) for i in ids), 'moved vertex outside its own parent quads'
        s.moved[int(pid)] = (ids[m], w[m]); return int(pid)
    def uv(s, corners, su):
        fi, pos = s.pquad(*corners); U = s.UV[fi]; x, y = su
        return (1 - x) * (1 - y) * U[pos[0]] + x * (1 - y) * U[pos[1]] + x * y * U[pos[2]] + (1 - x) * y * U[pos[3]]
def face_param(B, corners, su):
    """(corners in (s,u) order, (s,u)) -> (parent face id, s', u') in that face's own corner order"""
    fi, pos = B.pquad(*corners); x, y = su; w = np.array([(1 - x) * (1 - y), x * (1 - y), x * y, (1 - x) * y]); W = np.zeros(4); W[pos] = w
    return int(fi), float(W[1] + W[2]), float(W[2] + W[3])
def realize(z, br, params=None, sides=('l', 'r'), override=None):
    """returns dict(V, Q, UV, S, removed faces, new quads per side, poles, param {vid: (face, s, u)}) for one v005 realization;
    override {vid: (face, s, u)} replaces the bilinear placement of branch vertices (the per-vertex relaxed v002 definition)"""
    p = dict(DEF_PARAMS, **(params or br.get('params', {}))); V0 = z['V'].astype(float); Q0 = np.asarray(z['Q']).astype(np.int64); nV = len(V0)
    assert face_hash(Q0) == br['parent_face_topology'], 'not a v005 realization'
    UV0 = np.asarray(z['UV']) if 'UV' in z else None; B = Builder(Q0, nV, UV0); repl = []; info = {}; param = {}; keys = {}
    for side in sides:
        R = np.array(br['zones']['hand:thumb_mcp_' + side]['rows']); n = R.shape[1]; Pr, Zr, Ar, Br_, Cr, Dr = R
        # winding of parent strip quads relative to (s,u) CCW
        fi, pos = B.pquad(Zr[0], Zr[1], Ar[1], Ar[0]); sgn = 1 if (pos[1] - pos[0]) % 4 == 1 else -1
        cq = lambda r0, r1, k: (r0[k], r0[(k + 1) % n], r1[(k + 1) % n], r1[k])           # parent quad corners in (s,u) order
        pts = {}                                                                          # (row name, j) -> (corners, (s,u)); j in 0..2n-1
        ms = p['ms']
        def at(lo, hi, k, s_, u):                                                          # u measured from row 'lo' (u < 0 -> into the strip below via 'below')
            return (cq(lo, hi, k), (s_, u))
        U = set(UNSPLIT.get(side, [])); run = [(max(U) + 1 + t) % n for t in range(n - len(U))] if U else [(PHASE[side]['p'] + 1 + t) % n for t in range(n)]
        pairs = [(run[t], run[t + 1]) for t in range(0, len(run), 2)]; centres = sorted((b_ for a_, b_ in pairs))   # fan centre line = the line inside each column pair
        assert all((c - PHASE[side]['p']) % 2 == 0 for c in centres), 'fan-centre parity broken'
        for k in range(n):
            ce = k in centres; de = ce                                                     # proximal and distal fans share the column pairs
            uz = p.get('uz_e', 0.0) if ce else p.get('uz_o', 0.0); um = p.get('uz_m', -p['zr'])
            pts[('Z', 2 * k)] = at(Zr, Ar, k, 0, uz) if uz >= 0 else at(Pr, Zr, k, 0, 1 + uz)
            ua = p.get('ua', 0.0); uc = p.get('uc_e', 0.0) if de else p.get('uc_o', 0.0); ucm = p.get('uc_m', p['cr'])
            pts[('A', 2 * k)] = at(Ar, Br_, k, 0, ua); pts[('B', 2 * k)] = at(Br_, Cr, k, 0, 0)
            pts[('T1', 2 * k)] = at(Br_, Cr, k, 0, p['a']); pts[('T2', 2 * k)] = at(Br_, Cr, k, 0, p['b'])
            pts[('C', 2 * k)] = at(Cr, Dr, k, 0, uc) if uc >= 0 else at(Br_, Cr, k, 0, 1 + uc)
            if k not in U:                                                                 # split column: mid vertices on every fine row
                pts[('Z', 2 * k + 1)] = at(Zr, Ar, k, ms, um) if um >= 0 else at(Pr, Zr, k, ms, 1 + um)
                pts[('A', 2 * k + 1)] = at(Ar, Br_, k, ms, p.get('ua_m', ua)); pts[('B', 2 * k + 1)] = at(Br_, Cr, k, ms, 0)
                pts[('T1', 2 * k + 1)] = at(Br_, Cr, k, ms, p['a']); pts[('T2', 2 * k + 1)] = at(Br_, Cr, k, ms, p['b'])
                pts[('C', 2 * k + 1)] = at(Cr, Dr, k, ms, ucm) if ucm >= 0 else at(Br_, Cr, k, ms, 1 + ucm)
            pts[('P', k)] = (cq(Pr, Zr, k), (0, 0)); pts[('D', k)] = (cq(Cr, Dr, k), (0, 1))
        own = {}                                                                          # row line vertices that are v005 parent vertices
        for k in range(n):
            own[('Z', 2 * k)] = Zr[k]; own[('A', 2 * k)] = Ar[k]; own[('B', 2 * k)] = Br_[k]; own[('C', 2 * k)] = Cr[k]
        vid = {}
        for key, v in pts.items():
            if key in own and not (v[1][0] == 0 and v[1][1] == 0 and v[0][0] == own[key]): vid[key] = B.move(own[key], *v)
            else: vid[key] = B.vert(*v)
            if key[0] not in ('P', 'D'): param[vid[key]] = face_param(B, *v); keys[vid[key]] = (side,) + key
        quads = []; home = []                                                             # (key tuple) CCW in (s,u); home parent face (UV chart) per quad
        J = [j for j in range(2 * n) if not (j % 2 and (j // 2) in U)]
        for r0, r1, lo, hi in (('Z', 'A', Zr, Ar), ('A', 'B', Ar, Br_), ('B', 'T1', Br_, Cr), ('T1', 'T2', Br_, Cr), ('T2', 'C', Br_, Cr)):
            for t in range(len(J)):
                j0, j1 = J[t], J[(t + 1) % len(J)]; quads.append(((r0, j0), (r0, j1), (r1, j1), (r1, j0))); home.append(B.pquad(*cq(lo, hi, j0 // 2))[0])
        Pk = lambda k: ('P', k % n); Dk = lambda k: ('D', k % n); F = lambda r, j: (r, j % (2 * n))
        for c in centres:                                                                 # proximal fans, centre P_c
            quads += [(Pk(c - 1), Pk(c), F('Z', 2 * c - 1), F('Z', 2 * c - 2)), (Pk(c), F('Z', 2 * c + 1), F('Z', 2 * c), F('Z', 2 * c - 1)),
                      (Pk(c), Pk(c + 1), F('Z', 2 * c + 2), F('Z', 2 * c + 1))]
            home += [B.pquad(*cq(Pr, Zr, (c - 1) % n))[0], B.pquad(*cq(Pr, Zr, c % n))[0], B.pquad(*cq(Pr, Zr, c % n))[0]]
        for k in sorted(U):                                                               # unsplit columns: plain quads in the two transition strips
            quads += [(Pk(k), Pk(k + 1), F('Z', 2 * k + 2), F('Z', 2 * k)), (F('C', 2 * k), F('C', 2 * k + 2), Dk(k + 1), Dk(k))]
            home += [B.pquad(*cq(Pr, Zr, k))[0], B.pquad(*cq(Cr, Dr, k))[0]]
        for d in centres:                                                                 # distal fans, centre D_d
            quads += [(F('C', 2 * d - 2), F('C', 2 * d - 1), Dk(d), Dk(d - 1)), (F('C', 2 * d - 1), F('C', 2 * d), F('C', 2 * d + 1), Dk(d)),
                      (F('C', 2 * d + 1), F('C', 2 * d + 2), Dk(d + 1), Dk(d))]
            home += [B.pquad(*cq(Cr, Dr, (d - 1) % n))[0], B.pquad(*cq(Cr, Dr, d % n))[0], B.pquad(*cq(Cr, Dr, d % n))[0]]
        # removed parent faces
        rem = []
        for r0, r1 in ((Pr, Zr), (Zr, Ar), (Ar, Br_), (Br_, Cr), (Cr, Dr)):
            for k in range(n): rem.append(B.pquad(*cq(r0, r1, k))[0])
        for qk, hf in zip(quads, home):
            q = [vid[x] for x in qk]; uvk = [face_param(B, *pts[x]) for x in qk]
            if sgn < 0: q = q[::-1]; uvk = uvk[::-1]
            repl.append((q, uvk, hf))
        B.removed += rem; info[side] = dict(new_quads=len(quads), removed=len(rem), sign=sgn, centres_P=[int(Pr[c % n]) for c in centres],
                                            centres_D=[int(Dr[d % n]) for d in centres], centre_lines=centres, unsplit_columns=sorted(U), seam_lines=SEAM.get(side, []),
                                            fine_rings={r: [int(vid[(r, j)]) for j in J] for r in ('Z', 'A', 'B', 'T1', 'T2', 'C')},
                                            fine_ring_lines={r: [int(vid[(r, 2 * k)]) for k in range(n)] for r in ('Z', 'A', 'B', 'T1', 'T2', 'C')})
    keep = np.array([i for i in range(nV) if i not in B.moved], np.int64); mr, mc, mv = [], [], []
    for pid, (ids, w) in B.moved.items(): mr += [pid] * len(ids); mc += list(ids); mv += list(w)
    S = sp.csr_matrix((np.r_[np.ones(len(keep)), mv, B.vals], (np.r_[keep, mr, B.rows], np.r_[keep, mc, B.cols])), shape=(nV + B.nnew, nV))
    if override:
        S = S.tolil()
        for v, (f, a, b) in override.items():
            v = int(v); assert v in param, 'override of a non-branch vertex'; S.rows[v] = []; S.data[v] = []
            for c, w in zip(Q0[int(f)], [(1 - a) * (1 - b), a * (1 - b), a * b, (1 - a) * b]):
                if w > 1e-12: S[v, int(c)] = w
            param[v] = (int(f), float(a), float(b))
        S = S.tocsr()
    if UV0 is not None:
        cont = uv_continuity(Q0, UV0)
        def uvat(fp, h):
            """UV of the point (face f, s, u) in the local UV chart of home face h: the nearest face containing the point's support that is reachable
            from h through UV-continuous edges (BFS depth <= 7), so corners on a seam take the UV of the home quad's side"""
            f, a, b = fp; w = np.array([(1 - a) * (1 - b), a * (1 - b), a * b, (1 - a) * b]); C = {int(Q0[f][k]): w[k] for k in range(4) if w[k] > 1e-9}
            cand = set(FACES_OF(Q0, list(C))); seen = {h}; fr = [h]; g = h if h in cand else None
            for _ in range(7):
                if g is not None: break
                nx = []
                for x in fr:
                    for y in cont.get(x, ()):
                        if y not in seen: seen.add(y); nx.append(y)
                g = next((y for y in nx if y in cand), None); fr = nx
            assert g is not None, 'no UV-continuous face for a branch corner'
            qg = [int(x) for x in Q0[g]]; ww = np.array([C.get(x, 0.0) for x in qg]); assert abs(ww.sum() - 1) < 1e-6
            return (ww[:, None] * UV0[g]).sum(0)
        repl = [(q, [uvat(param.get(vv, fp), hf) for vv, fp in zip(q, uvk)]) for q, uvk, hf in repl]   # home = the quad's own parent face (column / strip)
    else: repl = [(q, None) for q, uvk, hf in repl]
    rem = sorted(B.removed); assert len(set(rem)) == len(rem), 'overlapping branch zones'
    Q = Q0.copy(); UV = UV0.copy() if UV0 is not None else None; extra = []; extraUV = []
    for i, (q, u) in enumerate(repl):
        if i < len(rem):
            Q[rem[i]] = q
            if UV is not None: UV[rem[i]] = u
        else:
            extra.append(q); extraUV.append(u)
    if extra:
        Q = np.vstack([Q, np.array(extra, Q.dtype)])
        if UV is not None: UV = np.concatenate([UV, np.array(extraUV, UV.dtype)])
    return dict(V=S @ V0, Q=Q, UV=UV, S=S, removed=np.array(rem), info=info, params=p, param=param, keys=keys)
def apply(famp, brp, outp, params=None):
    z = dict(np.load(famp, allow_pickle=True)); br = json.load(open(brp)); ov = {int(k): v for k, v in br.get('override', {}).items()}
    r = realize(z, br, params, override=ov or None); out = dict(z); S = r['S']
    out['V'] = r['V'].astype(z['V'].dtype); out['Q'] = r['Q']
    if r['UV'] is not None: out['UV'] = r['UV'].astype(z['UV'].dtype)
    if 'M_data' in z:
        M = sp.csr_matrix((z['M_data'], z['M_indices'], z['M_indptr']), shape=tuple(z['M_shape'])); Mb = (S @ M).tocsr()
        out.update(M_data=Mb.data, M_indices=Mb.indices, M_indptr=Mb.indptr, M_shape=np.array(Mb.shape))
    out.update(branch_S_data=S.data, branch_S_indices=S.indices, branch_S_indptr=S.indptr, branch_S_shape=np.array(S.shape), branch_removed_faces=r['removed'],
               branch=np.array(br['branch']), parent_verts=np.array(len(z['V'])), branch_params=json.dumps(r['params']))
    np.savez_compressed(outp, **out); return r
if __name__ == '__main__':
    if sys.argv[1] == 'define': print(json.dumps(define(sys.argv[2], sys.argv[3])['zones'], default=str)[:400])
    else:
        r = apply(sys.argv[2], sys.argv[3], sys.argv[4]); print('BRANCH', sys.argv[4], 'V', r['S'].shape[1], '->', r['S'].shape[0], 'Q ->', len(r['Q']))
