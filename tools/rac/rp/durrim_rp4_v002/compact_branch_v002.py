# compact_branch_v002.py : MPFB_COMPACT_BRANCH_v002 = thumb MCP two-direction local densification (thumb_patch.py) + jaw-neck pole reroute
# (neck_reroute.py edge rotations + on-surface vertex re-placement). Order 8080f9f §3-§6.
#   build THUMB_DEF.json THUMB_RELAX.json NECK_OPS.json NECK_SLIDE.json OUT_DEF.json   : assemble the one branch definition record
#   apply V005_FAM.npz BRANCH_DEF.json OUT.npz                                      : realize on any v005 realization (c1 / c2 / any stature)
# Map: V_branch = S V_v005 exactly; M_branch = S M_v005 (hm08 -> production rows, so weights / morph transfer go through the same path); v005 vertex
# order preserved (new thumb vertices appended; thumb Z / A / C row and neck vertices re-placed in place as bilinear points of their own v005 quads);
# v005 face slots kept (thumb replacement quads fill the removed thumb slots first, the rest appended; the neck rotations rewrite their own slots).
# UV: per-corner bilinear interpolation of the parent v005 face UVs at each vertex's (face, s, u) (the branch zones carry no UV seam -- checked).
import sys, json, hashlib, numpy as np, scipy.sparse as sp
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/durrim_rp4_v002')
import thumb_patch as TP, neck_reroute as NR
BR = 'MPFB_COMPACT_BRANCH_v002'
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def build(tdef, trel, nops, nsl, out):
    T = json.load(open(tdef)); R = json.load(open(trel)); N = json.load(open(nops)); L = json.load(open(nsl))
    rec = dict(branch=BR, parent='MPFB Family Base v005', parent_face_topology=T['parent_face_topology'], parent_verts=T['parent_verts'], parent_quads=T['parent_quads'],
               defined_on=T['ref'], thumb=dict(zones=T['zones'], params=R.get('params') or TP.DEF_PARAMS, override=R['override']),
               neck=dict(ops=N, slide={str(k): v for k, v in L.items()}, note='pole moved + one 3/5 pair added (4 quad edge rotations per side; no vertex added)'),
               provenance=dict(thumb_def=sha(tdef), thumb_relax=sha(trel), neck_ops=sha(nops), neck_slide=sha(nsl)))
    json.dump(rec, open(out, 'w'), indent=1); return rec
def uv_seam_free(Q0, UV0, verts):
    """True if every listed vertex has one UV over all its v005 faces"""
    vs = set(int(v) for v in verts); seen = {}
    for f, q in enumerate(Q0):
        for k, v in enumerate(q):
            v = int(v)
            if v in vs:
                u = tuple(np.round(UV0[f][k], 6)); seen.setdefault(v, set()).add(u)
    return all(len(s) == 1 for s in seen.values()), {v: s for v, s in seen.items() if len(s) > 1}
def realize(z, rec):
    Q0 = np.asarray(z['Q']).astype(np.int64); V0 = z['V'].astype(float); UV0 = np.asarray(z['UV']) if 'UV' in z else None
    tb = dict(parent_face_topology=rec['parent_face_topology'], zones=rec['thumb']['zones'], params=rec['thumb']['params'])
    r = TP.realize(dict(z), tb, rec['thumb']['params'], override={int(k): tuple(v) for k, v in rec['thumb']['override'].items()})
    S = r['S'].tolil(); Q = r['Q'].copy(); UV = r['UV'].copy() if r['UV'] is not None else None
    Qn, touched = NR.apply_def(Q, rec['neck']['ops'])                                  # neck rotations rewrite their own (v005) face slots
    sl = {int(k): v for k, v in rec['neck']['slide'].items()}
    for v, (f, a, b) in sl.items():
        S.rows[v] = []; S.data[v] = []
        for c, w in zip(Q0[int(f)], [(1 - a) * (1 - b), a * (1 - b), a * b, (1 - a) * b]):
            if w > 1e-12: S[v, int(c)] = w
    S = S.tocsr()
    if UV is not None:                                                                # neck faces: vertex UVs (seam-free zone) at the re-placed points
        vuv = {}
        for v, (f, a, b) in sl.items(): U = UV0[int(f)]; vuv[v] = (1 - a) * (1 - b) * U[0] + a * (1 - b) * U[1] + a * b * U[2] + (1 - a) * b * U[3]
        aff = sorted(set(touched) | {i for i, q in enumerate(Qn[:len(Q0)]) if any(int(x) in sl for x in q)})
        for f in aff:
            for k, v in enumerate(Qn[f]):
                v = int(v)
                if v in vuv: UV[f][k] = vuv[v]
                else:                                                                 # unmoved vertex of a rotated face: its (unique) v005 UV
                    g = next(i for i, q in enumerate(Q0) if v in q); UV[f][k] = UV0[g][list(Q0[g]).index(v)]
    neck_faces = sorted(set(touched) | {i for i, q in enumerate(Qn) if any(int(x) in sl for x in q)})
    thumb_faces = np.r_[r['removed'], np.arange(len(Q0), len(Qn))]
    return dict(V=S @ V0, Q=Qn, UV=UV, S=S, thumb_faces=thumb_faces, neck_faces=np.array(neck_faces), thumb_info=r['info'], neck_moved=np.array(sorted(sl)),
                thumb_param=r['param'])
def apply(famp, recp, outp):
    z = dict(np.load(famp, allow_pickle=True)); rec = json.load(open(recp)); r = realize(z, rec); S = r['S']; out = dict(z)
    assert hashlib.sha256(np.ascontiguousarray(z['Q'], np.int64).tobytes()).hexdigest() == rec['parent_face_topology']
    out['V'] = r['V'].astype(z['V'].dtype); out['Q'] = r['Q']
    if r['UV'] is not None: out['UV'] = r['UV'].astype(z['UV'].dtype)
    if 'M_data' in z:
        M = sp.csr_matrix((z['M_data'], z['M_indices'], z['M_indptr']), shape=tuple(z['M_shape'])); Mb = (S @ M).tocsr()
        out.update(M_data=Mb.data, M_indices=Mb.indices, M_indptr=Mb.indptr, M_shape=np.array(Mb.shape))
    nV0 = len(z['V']); part = np.array(['v005'] * S.shape[0], dtype='<U12'); part[nV0:] = 'thumb_new'
    for side in ('l', 'r'):
        rows = np.array(rec['thumb']['zones']['hand:thumb_mcp_' + side]['rows']); part[rows[1:5].ravel()] = 'thumb_moved'
    part[r['neck_moved']] = 'neck_moved'
    out.update(branch_S_data=S.data, branch_S_indices=S.indices, branch_S_indptr=S.indptr, branch_S_shape=np.array(S.shape), branch=np.array(BR), parent_verts=np.array(nV0),
               branch_thumb_faces=r['thumb_faces'], branch_neck_faces=r['neck_faces'], branch_part=part, branch_def_sha256=np.array(sha(recp)))
    np.savez_compressed(outp, **out); return r
if __name__ == '__main__':
    if sys.argv[1] == 'build': build(*sys.argv[2:7]); print('BUILT', sys.argv[6])
    else:
        r = apply(sys.argv[2], sys.argv[3], sys.argv[4]); print('V2', sys.argv[4], 'V', r['S'].shape[1], '->', r['S'].shape[0], 'Q', len(r['Q']))
