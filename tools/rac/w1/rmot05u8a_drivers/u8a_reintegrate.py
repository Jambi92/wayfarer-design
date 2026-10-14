# RM-OT-05U8A: OPT-IN U8A reintegration / protection adapter (additive; the U2 adapter and all defaults are unchanged).
# Frozen baseline = the accepted U8 cp1 return (pinned); additive copy of u8_reintegrate.py. Contract:
#  * inputs pinned: S3 OBJ, F1 OBJ, U8 cp1 return (passed as --cp3), u8a_sets_v1.json, P05U8A preview, U8A exempt list, U8 cp1 U2 labels;
#  * no topology change: unique rac_s3_vid1 one-to-one over all S3 vertices; exported faces == S3 faces with the same orientation;
#  * every vertex outside the two released crease anchors {61580, 61581} equals U8 cp1 bit-exactly at float32 (the 12-vertex U8A ring, the
#    U8 cp1 edits 61562/61727/61735/61940, the U6/U7 edits except released 61581, and everything else); non-finite values rejected;
#  * face labels are the U8 cp1 (U2) labels unchanged; source correspondence kept; the crease reference is NOT touched here;
#  * output layout for s_verify: P05U8A (= P05U8; the 13 U8A faces are all U2 cap faces, already outside the prefix) first.
# ('cp3' variable names = the pinned U8 cp1 baseline.)
# Usage: python3 u8a_reintegrate.py --ret RETURN.npz --s3 GO-05S-S3.obj --f1 F1_working.obj --cp3 cp3_return.npz --sets DIR --out PREFIX
import argparse, hashlib, json, os, numpy as np, trimesh
PIN = dict(s3='1d50383376dc5dd2e249778c7b7d8330f4ec16daa21303656a146c0b4d81ac4c', f1='17591025c24fd080e7fd45e3dc88dccc4707a0bee9efcb3fd70ef5ab6da453b0',
           cp3='89c1def3f59bf677a7b4ad4eab6ea84d32ee6b4c67755209f1476338e031911d', sets='f3ac181c3106dd01c6de7df4b3bdcd2dd00147ec5dab1ee8e157b3f66e33767b',
           p05u7='f1fdedb04abefe0d2df4bb0dc7892f1bf78fe415d596dee12f873596b8f09bff', exempt='36064c64031345e1ff2de50c8fb9d678846423944aa1b3ec68d75bab6b4f6b6b')
CP3_LABELS = 'reviews/rac-rmot05u8-evidence/return/checks/result_s3order_face_labels.npy'
fH = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
def main():
    ap = argparse.ArgumentParser(); [ap.add_argument(k) for k in ('--ret', '--s3', '--f1', '--cp3', '--sets', '--out')]; a = ap.parse_args()
    rep = dict(mode='U8A opt-in adapter (frozen baseline = U8 cp1)', ret=a.ret); errs = []
    sp = os.path.join(a.sets, 'u8a_sets_v1.json'); pv = os.path.join(a.sets, 'P05U8A_preview.npz'); xp = os.path.join(a.sets, 'src_exemptA_f1.npy')
    for nm, p, k in (('S3 OBJ', a.s3, 's3'), ('F1 OBJ', a.f1, 'f1'), ('U8 cp1 return', a.cp3, 'cp3'), ('u8a sets', sp, 'sets'), ('P05U8A preview', pv, 'p05u7'), ('U8A exempt list', xp, 'exempt')):
        if not os.path.exists(p) or fH(p) != PIN[k]: errs.append('%s missing or hash mismatch' % nm)
    if errs:
        rep.update(verdict='REJECTED', errors=errs); json.dump(rep, open(a.out + '_u8a_reintegrate.json', 'w'), indent=1); print(json.dumps(rep)); return
    SE = json.load(open(sp)); T = np.array(SE['target_vertices']); RING = np.array(SE['frozen_ring']); U7F = np.array(SE['u8a_faces'])
    U6T = np.array(json.load(open('reviews/rac-rmot05u6-evidence/readiness/u6_sets_v1.json'))['target_vertices'])
    s3 = trimesh.load(a.s3, process=False); Vs = np.asarray(s3.vertices); Fs = np.asarray(s3.faces); nV = len(Vs)
    V1 = np.asarray(trimesh.load(a.f1, process=False).vertices)
    smap = np.load('reviews/rac-rmot05s-evidence/repair/S3/GO-05S-S3_maps.npz')['src_vertex']; lab = np.load(CP3_LABELS)
    C = np.load(a.cp3); cid = C['s3_vid1'].astype(np.int64) - 1; Wc = np.zeros((nV, 3), np.float32); Wc[cid] = C['V']
    Vc = Vs.copy(); mvc = ~np.all(Wc == Vs.astype(np.float32), 1); Vc[mvc] = Wc[mvc].astype(np.float64)          # cp3 exact geometry
    R = np.load(a.ret); Vr = R['V'].astype(np.float32); Fr = np.asarray(R['F'], np.int64); ids = R['s3_vid1'].astype(np.int64) - 1
    rep['export'] = dict(vertices=int(len(Vr)), faces=int(len(Fr)), identity_transform=bool(R['identity_transform']), triangulated_ngons=int(R['triangulated_ngons']))
    if not bool(R['identity_transform']): errs.append('object transform is not identity')
    if not np.isfinite(Vr).all(): errs.append('non-finite vertex coordinates in the return')
    valid = (ids >= 0) & (ids < nV); u, c = np.unique(ids[valid], return_counts=True)
    rep['identity'] = dict(invalid_or_zero_ids=int((~valid).sum()), duplicate_ids=int((c > 1).sum()), missing_ids=int(nV - len(u)), vertex_count_matches=len(Vr) == nV)
    if (~valid).any() or (c > 1).any() or len(u) != nV or len(Vr) != nV: errs.append('identity attribute is not a one-to-one cover of the S3 vertices')
    if not errs:
        Fm = ids[Fr]
        def canon(F_):
            r = np.argmin(F_, 1); return np.stack([F_[np.arange(len(F_)), (r + k) % 3] for k in range(3)], 1)
        want = {tuple(x) for x in canon(Fs).tolist()}; got = {}
        for i, x in enumerate(canon(Fm).tolist()): got.setdefault(tuple(x), []).append(i)
        missing = len(want - set(got)); extra = [k for k in got if k not in want]; dup = sum(1 for v in got.values() if len(v) > 1)
        rep['topology'] = dict(missing_faces=missing, extra_faces=len(extra), of_which_reversed=sum(1 for k in extra if (k[0], k[2], k[1]) in want), duplicate_faces=dup, face_count_matches=len(Fr) == len(Fs))
        if missing or extra or dup or len(Fr) != len(Fs): errs.append('face set differs from S3 (topology change)')
        Win = np.zeros((nV, 3), np.float32); Win[ids] = Vr
        changed = ~np.all(Win == Wc, 1); out = np.setdiff1d(np.where(changed)[0], T)
        rep['protection_vs_u8cp1'] = dict(vertices_outside_U8A_target=int(nV - len(T)), moved_outside_target=int(len(out)), moved_examples=[int(v) for v in out[:10]],
                                        u8a_frozen_ring_moved=[int(v) for v in RING if changed[v]], u6_target_moved=[int(v) for v in U6T if changed[v] and v not in set(T.tolist())], anchors_moved=[int(v) for v in T if changed[v]],
                                        u6_edited_moved=[int(v) for v in SE['u6_edited'] if changed[v] and v not in set(SE['released_from_u6_edited'])], u7_edited_moved=[int(v) for v in SE['u7_edited'] if changed[v]],
                                        u8_edited_moved=[int(v) for v in SE['u8_edited'] if changed[v]],
                                        target_moved=[int(v) for v in T if changed[v]])
        if len(out): errs.append('vertex outside the U8A target changed relative to U8 cp1')
    if errs:
        rep.update(verdict='REJECTED', errors=errs); json.dump(rep, open(a.out + '_u8a_reintegrate.json', 'w'), indent=1); print(json.dumps({k: rep[k] for k in ('verdict', 'errors')})); return
    Vo = Vc.copy(); tm = np.array(rep['protection_vs_u8cp1']['target_moved'], np.int64); Vo[tm] = Win[tm].astype(np.float64)
    keep7 = np.load(pv)['P05U8A_positions_in_P05S']; order = np.r_[keep7, np.setdiff1d(np.arange(len(Fs)), keep7)]
    with open(a.out + '.obj', 'w') as fh:
        np.savetxt(fh, Vo, fmt='v %.17g %.17g %.17g'); np.savetxt(fh, Fs[order] + 1, fmt='f %d %d %d')
    np.savez(a.out + '_maps.npz', src_vertex=smap.astype(np.int64), s3_vertex=np.arange(nV), face_order_s3=order)
    np.save(a.out + '_face_labels.npy', lab[order]); np.save(a.out + '_s3order_face_labels.npy', lab)
    np.save(a.out + '_src_exempt_f1.npy', np.load(xp))
    srcm = np.where((smap >= 0) & np.any(Vo != Vc, 1))[0]
    rep['correspondence'] = dict(labels='U8 cp1 (U2) labels unchanged (no new label)', label_counts=np.bincount(lab, minlength=7).tolist(), source_vertices_changed_vs_cp3=[int(v) for v in srcm],
                                 all_within_target=bool(np.isin(srcm, T).all()), all_mapped_to_source=bool((smap[T] >= 0).all()))
    rep['layout'] = dict(first_faces=int(len(keep7)), first_faces_are='P05U8A = P05U8 (no U8A face is a prefix face; P05S order)', u8a_faces_in_new_set=int(np.isin(U7F, order[len(keep7):]).sum()))
    rep['result_obj_sha256'] = fH(a.out + '.obj'); rep['verdict'] = 'ACCEPTED_FOR_VERIFICATION_U8A'
    json.dump(rep, open(a.out + '_u8a_reintegrate.json', 'w'), indent=1); print(json.dumps({'verdict': rep['verdict'], 'target_moved': rep['protection_vs_u8cp1']['target_moved']}))
if __name__ == '__main__': main()
