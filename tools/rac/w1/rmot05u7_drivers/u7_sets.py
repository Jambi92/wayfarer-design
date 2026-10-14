# RM-OT-05U7: build the FROZEN U7 sets ONCE from the pinned U6A cp3 return (never from a U7 return).
#   seeds         = 61522, 61771, 62027, 61586, 61183, 62063 (order 05U7 section 2)
#   target        = seeds that can move without breaking a frozen reference: 61522 is an endpoint of the FROZEN crease-B entry
#                   edge 61355-61522 (crease_reference_v1.json) and therefore stays frozen -> 5 editable vertices
#   faces         = all faces incident to the target (U7 authorized / local faces)
#   frozen_ring   = every other vertex of those faces (one topological ring), incl. 61522
#   layout        = P05U2 protected prefix minus the U7 faces (P05U7), so s_verify V2/V3/V5/V6c evaluate the U7 faces as "new"
#   prot_sha7     = coordinate hash of the P05U7 prefix on the cp3 geometry; src_exempt7 = cp3 exempt + target source vertices
# Usage: python3 u7_sets.py --s3 GO-05S-S3.obj --cp3 cp3_return.npz --outdir DIR
import argparse, hashlib, json, os, numpy as np, trimesh
from collections import defaultdict
ap = argparse.ArgumentParser(); [ap.add_argument(k) for k in ('--s3', '--cp3', '--outdir')]; a = ap.parse_args()
fH = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest(); H = lambda x: hashlib.sha256(np.asarray(x, dtype=np.int64).tobytes()).hexdigest()
CP3 = 'cbb786053ed4830e2f5b9ec2ebbcb2e1bb40d6b9df0e59b1b29f13364412affe'; assert fH(a.cp3) == CP3, 'cp3 return differs'
SEEDS = [61522, 61771, 62027, 61586, 61183, 62063]
REF = json.load(open('reviews/rac-rmot05u4-readiness/crease_reference_v1.json'))
s3 = trimesh.load(a.s3, process=False); Vs = np.asarray(s3.vertices); F = np.asarray(s3.faces)
R = np.load(a.cp3); i = R['s3_vid1'] - 1; V = Vs.copy(); mv = ~np.all(R['V'] == Vs[i].astype(np.float32), 1); V[i[mv]] = R['V'][mv]
crease_frozen = sorted({int(v) for s in REF['sections'].values() for k in ('entry_edge', 'exit_edge') for v in s[k]})
target = sorted(v for v in SEEDS if v not in crease_frozen); held = sorted(v for v in SEEDS if v in crease_frozen)
vf = defaultdict(list)
for k, f in enumerate(F):
    for x in f: vf[int(x)].append(k)
faces = sorted({f for v in target for f in vf[v]}); ring = sorted({int(v) for f in faces for v in F[f]} - set(target))
U6 = json.load(open('reviews/rac-rmot05u6-evidence/readiness/u6_sets_v1.json')); U6T = U6['target_vertices']
PS = np.load('reviews/rac-rmot05u2-proposal/proposal_sets.npz'); E = PS['proposed_editable']
assert len(target) <= 24 and len(faces) <= 70 and not set(target) & set(U6T) and not set(target) & set(E.tolist())
keep = np.load('reviews/rac-rmot05u2-proposal/P05U2_preview.npz')['P05U2_positions_in_P05S']; A35 = PS['added_faces']
assert np.isin(faces, np.union1d(keep, A35)).all()   # U7 faces are P05U2 prefix faces or approved U2 cap faces (already outside the prefix)
faces_in_cap = sorted(int(f) for f in faces if f in set(A35.tolist())); faces_in_prefix = sorted(int(f) for f in faces if f in set(keep.tolist()))
keep7 = np.setdiff1d(keep, faces); P05S = np.load('reviews/rac-rmot05s-evidence/plan/interface_sets.npz')['P05S_src_ordered']
os.makedirs(a.outdir, exist_ok=True); np.savez(os.path.join(a.outdir, 'P05U7_preview.npz'), P05U7_positions_in_P05S=keep7, P05U7_src_ordered=P05S[keep7])
smap = np.load('reviews/rac-rmot05s-evidence/repair/S3/GO-05S-S3_maps.npz')['src_vertex']
ex6 = np.load('reviews/rac-rmot05u6-evidence/return_u6a/checks/result_src_exempt_f1.npy'); ex7 = np.union1d(ex6, smap[target][smap[target] >= 0]).astype(np.int64)
np.save(os.path.join(a.outdir, 'src_exempt7_f1.npy'), ex7)
prot7 = hashlib.sha256(np.ascontiguousarray(V[F[keep7]]).astype(np.float64).tobytes()).hexdigest()
ed = sorted({tuple(sorted((int(f[x]), int(f[y])))) for f in F[faces] for x, y in ((0, 1), (1, 2), (2, 0))}); L = {e: float(np.linalg.norm(V[e[0]] - V[e[1]])) for e in ed}
def ang(fs):
    P = V[F[fs]]; Lf = np.linalg.norm(P[:, [1, 2, 0]] - P[:, [2, 0, 1]], axis=2)
    cs = np.stack([(Lf[:, (k + 1) % 3]**2 + Lf[:, (k + 2) % 3]**2 - Lf[:, k]**2) / (2 * Lf[:, (k + 1) % 3] * Lf[:, (k + 2) % 3]) for k in range(3)], 1)
    return np.degrees(np.arccos(np.clip(cs, -1, 1))).min(1)
out = dict(version='u7_sets_v1', seeds=SEEDS, target_vertices=target, seeds_held_frozen=dict(vertices=held, reason='endpoint of a FROZEN crease reference entry/exit edge (crease_reference_v1.json); moving it would invalidate the frozen crease measurement'),
           u7_faces=faces, u7_faces_in_P05U2_prefix=faces_in_prefix, u7_faces_that_are_U2_cap_faces=faces_in_cap, frozen_ring=ring, u6_target_in_ring=[v for v in ring if v in U6T], u6_target_overlap=[], counts=dict(target=len(target), faces=len(faces), ring=len(ring)),
           bounds=dict(max_target=24, max_faces=70), min_angle_deg=10.0, edge_band_cm=[0.25, 2.5], baseline_out_of_band_u7_edges=[list(e) for e, l in L.items() if l < 0.25 or l > 2.5],
           baseline_u7_min_angle=round(float(ang(faces).min()), 3), corridor_z_cm=[169.4, 172.3], target_z_cm=[round(float(V[target][:, 2].min()), 3), round(float(V[target][:, 2].max()), 3)],
           layout=dict(n_prot=int(len(keep7)), prot_sha=prot7, prot_faces_file='P05U7_preview.npz:P05U7_src_ordered', src_exempt='src_exempt7_f1.npy', src_exempt_count=int(len(ex7)),
                       P05U7_f1_sha=H(P05S[keep7])),
           sources=dict(cp3_return_npz=CP3, cp3_blend='22345d4d270b84753d3cdf32086d66846644448105aba1db710faaa083746029', s3_obj=fH(a.s3), crease_reference=fH('reviews/rac-rmot05u4-readiness/crease_reference_v1.json'),
                        u6_sets=fH('reviews/rac-rmot05u6-evidence/readiness/u6_sets_v1.json')),
           list_hashes=dict(target=H(target), faces=H(faces), ring=H(ring)))
p = os.path.join(a.outdir, 'u7_sets_v1.json'); json.dump(out, open(p, 'w'), indent=1, sort_keys=True)
print(json.dumps({k: v for k, v in out.items() if k not in ('u7_faces', 'frozen_ring', 'sources')})); print('sha', fH(p), 'P05U7_preview', fH(os.path.join(a.outdir, 'P05U7_preview.npz')), 'exempt', fH(os.path.join(a.outdir, 'src_exempt7_f1.npy')))
