# cg_branch_v001.py : MPFB_COGLING_COMPACT_BRANCH_v001 (order 9424c72 §10) = thumb MCP two-direction local densification only (cg_thumb_patch.py, Cogling
# placement re-solved on the Cogling bodies), on MPFB Family Base v005. No neck reroute (Cogling neck passes on v005), no unsplit hip sector (no Cogling
# hand / hip conflict), no toe / face topology. Copy of pipkin_rp4_v001/pk_branch_v001.py.
#   build THUMB_DEF.json THUMB_RELAX.json OUT_DEF.json      apply V005_FAM.npz DEF.json OUT.npz
# Map: V = S V_v005, M = S M_v005 (S rows <= 4 non-zeros); v005 order preserved, new thumb vertices appended; seam-aware UVs (pk_thumb_patch).
import sys, json, hashlib, numpy as np, scipy.sparse as sp
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/durrim_rp4_v002'); sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/cogling_rp4_v001')
import cg_thumb_patch as TP
BR = 'MPFB_COGLING_COMPACT_BRANCH_v001'
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
def build(tdef, trel, out):
    T = json.load(open(tdef)); R = json.load(open(trel))
    rec = dict(branch=BR, parent='MPFB Family Base v005', parent_face_topology=T['parent_face_topology'], parent_verts=T['parent_verts'], parent_quads=T['parent_quads'],
               defined_on=T['ref'], components=['thumb MCP two-direction local densification (both thumbs)'], not_included=['jaw-neck reroute (not needed: Cogling neck passes on v005)',
               'unsplit hip sector (Durrim c2-specific; no Cogling hand / hip conflict)', 'toe MTP support (Cogling c1 toe3 / toe4 j1 failures diagnosed as validator geometry; author decision)',
               'face topology (no compact-scale face deficiency demonstrated)'],
               thumb=dict(zones=T['zones'], params=R.get('params') or TP.DEF_PARAMS, override=R['override'], unsplit=TP.UNSPLIT, phase=TP.PHASE, seam=TP.SEAM),
               provenance=dict(thumb_def=sha(tdef), thumb_relax=sha(trel), engineering_concept='MPFB_COMPACT_BRANCH_v002 (Durrim) / MPFB_PIPKIN_COMPACT_BRANCH_v001 thumb architecture (identical v005 thumb grid rows); placement re-solved on Cogling bodies'))
    json.dump(rec, open(out, 'w'), indent=1); return rec
def realize(z, rec):
    tb = dict(parent_face_topology=rec['parent_face_topology'], zones=rec['thumb']['zones'], params=rec['thumb']['params'])
    r = TP.realize(dict(z), tb, rec['thumb']['params'], override={int(k): tuple(v) for k, v in rec['thumb']['override'].items()})
    r['thumb_faces'] = np.r_[r['removed'], np.arange(len(z['Q']), len(r['Q']))]; return r
def apply(famp, recp, outp):
    z = dict(np.load(famp, allow_pickle=True)); rec = json.load(open(recp)); r = realize(z, rec); S = r['S']; out = dict(z)
    out['V'] = r['V'].astype(z['V'].dtype); out['Q'] = r['Q']
    if r['UV'] is not None: out['UV'] = r['UV'].astype(z['UV'].dtype)
    M = sp.csr_matrix((z['M_data'], z['M_indices'], z['M_indptr']), shape=tuple(z['M_shape'])); Mb = (S @ M).tocsr()
    out.update(M_data=Mb.data, M_indices=Mb.indices, M_indptr=Mb.indptr, M_shape=np.array(Mb.shape))
    nV0 = len(z['V']); part = np.array(['v005'] * S.shape[0], dtype='<U12'); part[nV0:] = 'thumb_new'
    for side in ('l', 'r'): part[np.array(rec['thumb']['zones']['hand:thumb_mcp_' + side]['rows'])[1:5].ravel()] = 'thumb_moved'
    out.update(branch_S_data=S.data, branch_S_indices=S.indices, branch_S_indptr=S.indptr, branch_S_shape=np.array(S.shape), branch=np.array(BR), parent_verts=np.array(nV0),
               branch_thumb_faces=r['thumb_faces'], branch_neck_faces=np.array([], np.int64), branch_part=part, branch_def_sha256=np.array(sha(recp)))
    np.savez_compressed(outp, **out); return r
if __name__ == '__main__':
    if sys.argv[1] == 'build': build(*sys.argv[2:5]); print('BUILT', sys.argv[4])
    else: r = apply(*sys.argv[2:5]); print('CGB', sys.argv[4], 'V', r['S'].shape[1], '->', r['S'].shape[0], 'Q', len(r['Q']))
