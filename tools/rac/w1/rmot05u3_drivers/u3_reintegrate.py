# RM-OT-05U3: OPT-IN U2 reintegration / protection adapter (NON-PRODUCTION until Tyler approves the 05U2 boundary).
# It never changes the default 05T/05U path (t_reintegrate.py / s_verify.py defaults are untouched).
#
# Usage: python3 u3_reintegrate.py --ret EDITED_return.npz --proposal reviews/rac-rmot05u2-proposal --s3 GO-05S-S3.obj
#                                  --baseline reviews/rac-rmot05u-evidence/checks/return/return.npz --f1 F1_working.obj --out PREFIX
#
# Contract (05U2 proposal, corrected by 05U3):
#  * inputs are pinned: S3 OBJ, 05U baseline return, the three proposal files and every list hash must match the committed
#    values; the 365 editable vertices / 106 frozen vertices / 832 editable faces are DERIVED from S3 + the added-face list
#    and must equal the committed preview (supplied counts are never trusted);
#  * method is no-topology-change: every exported vertex carries a unique rac_s3_vid1 covering all 70,751 S3 vertices once,
#    and the exported faces mapped through the ids must equal the S3 faces with the same orientation (no missing, reversed,
#    extra or duplicated faces);
#  * every vertex outside the 365 must equal the frozen 05U baseline bit-exactly at float32 (then its exact float64 baseline
#    coordinate is restored); a moved vertex is accepted only if its id is in the 365 - an id alone never authorizes a
#    moved protected vertex (spoofs fail the position check of the claimed id or the face check);
#  * source provenance is kept for all vertices (moved source vertices keep their F1 correspondence);
#  * output layout for s_verify: the 139,772 P05U2 faces first (P05S order), then all other faces in S3 order; the 35 added
#    faces are therefore inside the "new" set that V2-V6c evaluate; added faces carry label 6 (edited source surface, INFERRED);
#  * the legacy V1 is reported faithfully plus a correspondence-aware diagnostic: actual changed source vertices / affected
#    P05S faces must be a subset of the authorized 15 / 35 (a maximum region, not a quota).
import argparse, hashlib, json, os, numpy as np, trimesh
PIN = dict(s3_sha='1d50383376dc5dd2e249778c7b7d8330f4ec16daa21303656a146c0b4d81ac4c',
           baseline_sha='0989caf45cba8ddf0f44bdfba962671430c613bb752ac543d99d9b4b16420265',
           f1_sha='17591025c24fd080e7fd45e3dc88dccc4707a0bee9efcb3fd70ef5ab6da453b0',
           added_vertices='5be5a27f133f9e936f6d4164340eb7561de8af0bc9016f17a97aa5fdc6cd0aa1', added_faces='483ab7feac190c76679eadc3ce677cd8e538349e2dc4842c6db0dfd441797692',
           editable='0154b2be773056f049e7a729f15d97e8844fb3862c77b58a760f7c2666e95559', ring='91725db2ca491529305c0a77e14f89db5578628bba7500d9495536f724340426',
           cur_editable='ff059bb07151f4ea6b522b271faaddb65f0f9db0a3c855d26c7dc4a201af8243', cur_ring='ff07157bb2bf7d2a3b98809057940958c7e6d55bd0c2ffdf6b6bc84f1eecb3f0',
           p05u2_coord='25ffe5ac83d60e81b1026baf91bf3dbc07d7dc7136a8495f77f5581920328ffd', p05u2_f1idx='02b608bc55df4148df0b5ec1e86ab2c3767ff24e42b0287b7272dac92ae29184',
           p05s_coord='4468dd862307b8393dfcc8dab58d5cab6033558a87ba523b220e379b7df57c55', n_p05s=139807, n_p05u2=139772, n_edit=365, n_ring=106, n_faces=832, n_added_v=15, n_added_f=35)
S = 'reviews/rac-rmot05s-evidence/'
H = lambda x: hashlib.sha256(np.asarray(x, dtype=np.int64).tobytes()).hexdigest()
fH = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
def main():
    ap = argparse.ArgumentParser(); [ap.add_argument(k) for k in ('--ret', '--proposal', '--s3', '--baseline', '--f1', '--out')]; ap.add_argument('--pins', default=None)
    a = ap.parse_args(); rep = dict(mode='U2 opt-in adapter (NON-PRODUCTION until boundary approval)', ret=a.ret); errs = []
    pins = dict(PIN); pins.update(json.load(open(a.pins)) if a.pins else {})
    # ---- 1. pinned inputs
    for nm, p, k in (('S3 OBJ', a.s3, 's3_sha'), ('05U baseline return', a.baseline, 'baseline_sha'), ('F1 working OBJ', a.f1, 'f1_sha')):
        if fH(p) != pins[k]: errs.append('%s hash mismatch' % nm)
    PS = np.load(os.path.join(a.proposal, 'proposal_sets.npz')); J = json.load(open(os.path.join(a.proposal, 'proposal_region.json')))
    PV = np.load(os.path.join(a.proposal, 'P05U2_preview.npz')); PJ = json.load(open(os.path.join(a.proposal, 'P05U2_preview.json')))
    s3 = trimesh.load(a.s3, process=False); Vs = np.asarray(s3.vertices); Fs = np.asarray(s3.faces); nV = len(Vs)
    f1 = trimesh.load(a.f1, process=False); V1 = np.asarray(f1.vertices); F1 = np.asarray(f1.faces)
    lab = np.load(S + 'repair/S3/GO-05S-S3_face_labels.npy'); smap = np.load(S + 'repair/S3/GO-05S-S3_maps.npz')['src_vertex']
    P05S = np.load(S + 'plan/interface_sets.npz')['P05S_src_ordered']
    A = np.asarray(PS['added_faces'], np.int64)
    checks = dict(added_faces_list=H(A) == pins['added_faces'] == J['proposed_added']['faces_sha256'], added_faces_count=len(A) == pins['n_added_f'],
                  added_faces_are_label0_P05S_positions=bool((lab[A] == 0).all() and (A < pins['n_p05s']).all()))
    inter = (lab == 4) | (lab == 5)
    vn = np.zeros(nV, bool); vn[Fs[inter].ravel()] = True; vo = np.zeros(nV, bool); vo[Fs[~inter].ravel()] = True
    checks['current_editable'] = H(np.where(vn & ~vo)[0]) == pins['cur_editable']; checks['current_ring'] = H(np.where(vn & vo)[0]) == pins['cur_ring']
    region = inter.copy(); region[A] = True
    vin = np.zeros(nV, bool); vin[Fs[region].ravel()] = True; vout = np.zeros(nV, bool); vout[Fs[~region].ravel()] = True
    EDIT = vin & ~vout; RING = vin & vout; added_v = np.where(EDIT & ~(vn & ~vo))[0]
    checks.update(derived_editable=bool(H(np.where(EDIT)[0]) == pins['editable'] and EDIT.sum() == pins['n_edit'] and np.array_equal(np.where(EDIT)[0], PS['proposed_editable'])),
                  derived_ring=bool(H(np.where(RING)[0]) == pins['ring'] and RING.sum() == pins['n_ring'] and np.array_equal(np.where(RING)[0], PS['proposed_frozen_ring'])),
                  derived_editable_faces=int(region.sum()) == pins['n_faces'],
                  derived_added_vertices=bool(H(added_v) == pins['added_vertices'] == J['proposed_added']['vertices_sha256'] and len(added_v) == pins['n_added_v']))
    keep = np.setdiff1d(np.arange(pins['n_p05s']), A)
    checks['P05U2_list'] = bool(np.array_equal(PV['P05U2_positions_in_P05S'], keep) and H(P05S[keep]) == pins['p05u2_f1idx'] == PJ['P05U2_f1_face_index_sha256'] and len(keep) == pins['n_p05u2'])
    checks['P05U2_coord_on_S3'] = hashlib.sha256(np.ascontiguousarray(Vs[Fs[keep]]).astype(np.float64).tobytes()).hexdigest() == pins['p05u2_coord'] == PJ['P05U2_coord_sha256_on_S3']
    checks['P05S_prefix_is_S3_prefix'] = bool((smap[Fs[:pins['n_p05s']]] == F1[P05S]).all())
    errs += ['proposal/precondition check failed: %s' % k for k, v in checks.items() if not v]; rep['pinned_input_checks'] = checks
    # ---- 2. frozen 05U baseline in S3 order (exact float64 for protected / 05U-unmoved vertices)
    B = np.load(a.baseline); bid = B['s3_vid1'].astype(np.int64) - 1; Vb = Vs.copy(); bv = B['V']
    assert len(bid) == nV and np.array_equal(np.sort(bid), np.arange(nV))
    moved05u = ~np.all(bv == Vs[bid].astype(np.float32), axis=1); Vb[bid[moved05u]] = bv[moved05u].astype(np.float64)
    rep['baseline'] = dict(vertices_moved_in_05U=int(moved05u.sum()), moved_05U_subset_of_05U_editable=bool(np.all((vn & ~vo)[bid[moved05u]])))
    if errs:
        rep['verdict'] = 'REJECTED'; rep['errors'] = errs; json.dump(rep, open(a.out + '_u2_reintegrate.json', 'w'), indent=1); print(json.dumps(rep, indent=1)); return
    # ---- 3. returned mesh: identity and topology (no-topology-change method)
    R = np.load(a.ret); Vr = R['V'].astype(np.float32); Fr = np.asarray(R['F'], np.int64); ids = R['s3_vid1'].astype(np.int64) - 1
    rep['export'] = dict(vertices=int(len(Vr)), faces=int(len(Fr)), identity_transform=bool(R['identity_transform']), triangulated_ngons=int(R['triangulated_ngons']))
    if not bool(R['identity_transform']): errs.append('object transform is not identity')
    if not np.isfinite(Vr).all(): errs.append('non-finite vertex coordinates in the return (%d vertices)' % int((~np.isfinite(Vr).all(1)).sum()))   # RM-OT-05U4 addition
    valid = (ids >= 0) & (ids < nV); u, c = np.unique(ids[valid], return_counts=True)
    idrep = dict(invalid_or_zero_ids=int((~valid).sum()), duplicate_ids=int((c > 1).sum()), missing_ids=int(nV - len(u)), vertex_count_matches=len(Vr) == nV)
    rep['identity'] = idrep
    if idrep['invalid_or_zero_ids'] or idrep['duplicate_ids'] or idrep['missing_ids'] or not idrep['vertex_count_matches']: errs.append('identity attribute is not a one-to-one cover of the S3 vertices (topology change or spoof)')
    if not errs:
        e2s = ids; Fm = e2s[Fr]
        def canon(F_):
            r = np.argmin(F_, 1); return np.stack([F_[np.arange(len(F_)), (r + k) % 3] for k in range(3)], 1)
        want = {tuple(x): i for i, x in enumerate(canon(Fs).tolist())}; got = {}
        for i, x in enumerate(canon(Fm).tolist()): got.setdefault(tuple(x), []).append(i)
        missing = [j for k_, j in want.items() if k_ not in got]; extra = [k_ for k_ in got if k_ not in want]; dupf = [k_ for k_, v in got.items() if len(v) > 1]
        rev = sum(1 for k_ in extra if (k_[0], k_[2], k_[1]) in want)
        rep['topology'] = dict(missing_faces=len(missing), missing_examples=[int(x) for x in missing[:10]], missing_protected=int(sum(1 for j in missing if not region[j])),
                               extra_faces=len(extra), of_which_reversed=int(rev), duplicate_faces=len(dupf), face_count_matches=len(Fr) == len(Fs))
        if missing or extra or dupf or len(Fr) != len(Fs): errs.append('face set differs from S3 (missing / reversed / extra / duplicate faces)')
        # positions vs frozen baseline (claimed id)
        Vin = np.zeros((nV, 3), np.float32); Vin[e2s] = Vr
        changed = ~np.all(Vin == Vb.astype(np.float32), axis=1)
        out_mv = np.where(changed & ~EDIT)[0]
        cat = lambda v: 'new_frozen_ring' if RING[v] and not (vn[v] and vo[v]) else ('retained_frozen_ring' if RING[v] else ('05U_frozen_ring_now_editable' if (vn[v] and vo[v]) else 'protected'))
        rep['P1_U2_vertices_outside_365'] = dict(expected=int(nV - EDIT.sum()), unchanged_bit_exact=int(nV - EDIT.sum() - len(out_mv)), moved=int(len(out_mv)),
                                                  moved_examples=[dict(s3_index0=int(v), category=cat(v)) for v in out_mv[:10]],
                                                  frozen_ring_expected=int(RING.sum()), frozen_ring_moved=int(RING[out_mv].sum()))
        if len(out_mv): errs.append('vertex outside the approved 365 changed')
        rep['P2_U2_faces_outside_832'] = dict(expected=int((~region).sum()), present_same_orientation=int((~region).sum()) - rep['topology']['missing_protected'])
        ed_mv = np.where(changed & EDIT)[0]
        rep['editable_changes'] = dict(moved=int(len(ed_mv)), of_which_05U2_added_source=int(np.isin(ed_mv, added_v).sum()), of_which_05U_interface=int((ed_mv.size) - np.isin(ed_mv, added_v).sum()))
    if errs:
        rep['verdict'] = 'REJECTED'; rep['errors'] = errs; json.dump(rep, open(a.out + '_u2_reintegrate.json', 'w'), indent=1); print(json.dumps(rep, indent=1)); return
    # ---- 4. accepted: result in S3 order + s_verify layout
    Vo = Vb.copy(); Vo[ed_mv] = Vin[ed_mv].astype(np.float64)
    lab_u2 = lab.astype(np.int8).copy(); lab_u2[A] = 6
    srcmoved = np.where((smap >= 0) & np.any(Vo != V1[np.maximum(smap, 0)], axis=1))[0]
    aff = np.where(np.isin(Fs[:pins['n_p05s']], srcmoved).any(1))[0]
    leg_hash = hashlib.sha256(np.ascontiguousarray(Vo[Fs[:pins['n_p05s']]]).astype(np.float64).tobytes()).hexdigest()
    rep['legacy_V1_diagnostic'] = dict(note='Original V1 (P05S, 139,807 faces) evaluated on the U2 result in S3 order with full correspondence; the lists are a maximum region, not a quota.',
                                       P05S_coord_sha256=leg_hash, original_V1_hash_matches=leg_hash == pins['p05s_coord'],
                                       source_vertices_changed=[int(v) for v in srcmoved], source_vertices_changed_f1=[int(smap[v]) for v in srcmoved],
                                       P05S_faces_affected=[int(f) for f in aff], all_changed_source_within_authorized_15=bool(np.isin(srcmoved, added_v).all()),
                                       all_affected_faces_within_authorized_35=bool(np.isin(aff, A).all()))
    if not (rep['legacy_V1_diagnostic']['all_changed_source_within_authorized_15'] and rep['legacy_V1_diagnostic']['all_affected_faces_within_authorized_35']):
        errs.append('source change outside the authorized region')
    order = np.r_[keep, np.setdiff1d(np.arange(len(Fs)), keep)]
    with open(a.out + '.obj', 'w') as fh:
        np.savetxt(fh, Vo, fmt='v %.17g %.17g %.17g'); np.savetxt(fh, Fs[order] + 1, fmt='f %d %d %d')
    np.savez(a.out + '_maps.npz', src_vertex=smap.astype(np.int64), s3_vertex=np.arange(nV), face_order_s3=order)
    np.save(a.out + '_face_labels.npy', lab_u2[order]); np.save(a.out + '_s3order_face_labels.npy', lab_u2)
    np.save(a.out + '_src_exempt_f1.npy', smap[added_v].astype(np.int64))
    rep['layout'] = dict(first_faces=pins['n_p05u2'], first_faces_are='P05U2 in P05S order', remaining='all other S3 faces in S3 order (includes the 35 added faces and all 797 interface faces)',
                         face_order_in_maps='face_order_s3', label_6_faces=int((lab_u2 == 6).sum()), labels_s3order=np.bincount(lab_u2, minlength=7).tolist(),
                         src_exempt_f1_vertices=[int(x) for x in smap[added_v]])
    rep['result_obj_sha256'] = fH(a.out + '.obj'); rep['verdict'] = 'REJECTED' if errs else 'ACCEPTED_FOR_VERIFICATION_U2'
    if errs: rep['errors'] = errs
    json.dump(rep, open(a.out + '_u2_reintegrate.json', 'w'), indent=1); print(json.dumps({k: rep[k] for k in ('verdict',) + (('errors',) if errs else ())}))
if __name__ == '__main__': main()
