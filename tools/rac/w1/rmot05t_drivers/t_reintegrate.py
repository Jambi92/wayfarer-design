# RM-OT-05T return reintegration + independent protection check (additive; s_verify.py and its scores are unchanged).
# Identity comes from the rac_s3_vid1 attribute exported by t_export_blend.py. A vertex is accepted as UNCHANGED only if
# its exported float32 position equals float32(S3 position) bit-for-bit; unchanged vertices get their exact float64 S3
# coordinates back (no rounding, no guessing). Protection rule (exact, no tolerance):
#   P1 every S3 vertex outside EDIT_posterior / EDIT_anterior (all source, B2-retained and frozen-boundary vertices) must be
#      present exactly once among identity-verified vertices
#   P2 every S3 face outside the interface (rac_label not 4/5) must be present with the same vertices and orientation
#   any violation -> REJECTED (result not written). Otherwise the result OBJ is written in the s_verify layout
#   (P05S faces first in order, retained B2 faces, then interface faces) with maps / labels, ready for s_verify.py.
# Usage: python3 t_reintegrate.py --ret RETURN.npz --s3 GO-05S-S3.obj --s3maps S3_maps.npz --s3labels S3_labels.npy --out PREFIX
import argparse, json, hashlib, numpy as np, trimesh
ap = argparse.ArgumentParser(); ap.add_argument('--ret'); ap.add_argument('--s3'); ap.add_argument('--s3maps'); ap.add_argument('--s3labels'); ap.add_argument('--out'); ap.add_argument('--nprot', type=int, default=139807); a = ap.parse_args()
R = np.load(a.ret, allow_pickle=True); Vr = R['V']; Fr = R['F']; ids = R['s3_vid1'] - 1
s3 = trimesh.load(a.s3, process=False); Vs = np.asarray(s3.vertices); Fs = np.asarray(s3.faces); lab = np.load(a.s3labels); smap = np.load(a.s3maps)['src_vertex']
inter = (lab == 4) | (lab == 5); vnew = np.zeros(len(Vs), bool); vnew[Fs[inter].ravel()] = True; vold = np.zeros(len(Vs), bool); vold[Fs[~inter].ravel()] = True
EDIT = vnew & ~vold; PROT = ~EDIT                                                    # protected = everything not in an EDIT group
rep = dict(return_npz=a.ret, identity_transform=bool(R['identity_transform']), triangulated_ngons=int(R['triangulated_ngons']), exported_vertices=int(len(Vr)), exported_faces=int(len(Fr)))
# identity verification
valid = (ids >= 0) & (ids < len(Vs)); exact = np.zeros(len(Vr), bool)
exact[valid] = np.all(Vr[valid] == Vs[ids[valid]].astype(np.float32), axis=1)
claim = {}
for i in np.where(valid & exact)[0]: claim.setdefault(int(ids[i]), []).append(int(i))
dup = {k: v for k, v in claim.items() if len(v) > 1}
ver = {k: v[0] for k, v in claim.items()}                                             # verified S3 vertex -> export index
prot_missing = [int(k) for k in np.where(PROT)[0] if k not in ver]
moved_prot = [int(k) for k in prot_missing if np.any(ids == k)]
rep['P1_protected_vertices'] = dict(expected=int(PROT.sum()), verified_unchanged=int(PROT.sum()) - len(prot_missing), missing_or_moved=len(prot_missing), of_which_moved=len(moved_prot),
                                    examples=prot_missing[:10], duplicates_of_exact_identity=len(dup), frozen_boundary_expected=int((vnew & vold).sum()),
                                    frozen_boundary_missing_or_moved=int(sum(1 for k in prot_missing if vnew[k] and vold[k])), b2_or_new_nonsource_missing=int(sum(1 for k in prot_missing if smap[k] < 0)))
# faces
e2s = -np.ones(len(Vr), np.int64)
for k, i in ver.items(): e2s[i] = k
def key(f):
    r = int(np.argmin(f)); return tuple(np.roll(f, -r))
fset = {}
for i, f in enumerate(Fr):
    m = e2s[f]
    if (m >= 0).all(): fset[key(m)] = i
need = np.where(~inter)[0]; found = [fset.get(key(Fs[j])) for j in need]; miss = [int(need[k]) for k, v in enumerate(found) if v is None]
rep['P2_protected_faces'] = dict(expected=int(len(need)), present=int(len(need) - len(miss)), missing=len(miss), examples=miss[:10])
rep['edit_vertices'] = dict(expected=int(EDIT.sum()), unchanged=int(sum(1 for k in np.where(EDIT)[0] if k in ver)), moved_or_replaced=int(sum(1 for k in np.where(EDIT)[0] if k not in ver)),
                            new_vertices=int((ids < 0).sum()))
verified_idx = set(ver.values()); unver = [i for i in range(len(Vr)) if i not in verified_idx]
rep['export_vertices_identity'] = dict(verified_unchanged=len(verified_idx), unverified_new_or_moved=len(unver), with_attribute_zero=int(sum(1 for i in unver if ids[i] < 0)),
                                       with_nonzero_but_unverified_id=int(sum(1 for i in unver if ids[i] >= 0)),
                                       note='Blender may interpolate rac_s3_vid1 onto vertices created by topology operations; such ids are never trusted without bit-exact float32 position agreement')
ok = not prot_missing and not miss; rep['verdict'] = 'ACCEPTED_FOR_VERIFICATION' if ok else 'REJECTED'
if ok:
    used = set(v for v in found if v is not None); rest = [i for i in range(len(Fr)) if i not in used]
    order = [fset[key(Fs[j])] for j in need]                                          # S3 order: P05S first, then retained B2 faces
    ikey = {key(Fs[j]): j for j in np.where(inter)[0]}                                 # interface faces kept verbatim keep 05S order / label
    kept = sorted([(ikey[key(e2s[Fr[i]])], i) for i in rest if (e2s[Fr[i]] >= 0).all() and key(e2s[Fr[i]]) in ikey])
    keptset = set(i for _, i in kept); edited = [i for i in rest if i not in keptset]
    Fo_e = np.vstack([Fr[order], Fr[[i for _, i in kept]].reshape(-1, 3), Fr[edited].reshape(-1, 3)])
    Vout = Vr.astype(np.float64)
    for k, i in ver.items(): Vout[i] = Vs[k]                                          # exact float64 for identity-verified vertices
    newsrc = np.full(len(Vr), -1, np.int64)
    for k, i in ver.items(): newsrc[i] = smap[k]
    labo = np.r_[lab[need], np.array([lab[j] for j, _ in kept], np.int8), np.full(len(edited), 5, np.int8)]
    rep['interface_faces'] = dict(kept_verbatim=len(kept), edited_or_new=len(edited))
    with open(a.out + '.obj', 'w') as fh:
        np.savetxt(fh, Vout, fmt='v %.17g %.17g %.17g'); np.savetxt(fh, Fo_e + 1, fmt='f %d %d %d')
    np.savez(a.out + '_maps.npz', src_vertex=newsrc, s3_vertex=e2s); np.save(a.out + '_face_labels.npy', labo.astype(np.int8))
    rep['result_obj_sha256'] = hashlib.sha256(open(a.out + '.obj', 'rb').read()).hexdigest(); rep['result_faces'] = int(len(Fo_e)); rep['first_faces_are_P05S'] = int(a.nprot)
json.dump(rep, open(a.out + '_reintegrate.json', 'w'), indent=1); print(json.dumps(rep, indent=1))
