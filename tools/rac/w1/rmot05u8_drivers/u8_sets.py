# RM-OT-05U8: build the FROZEN U8 sets ONCE from the pinned U7 cp2 return (never from a U8 return).
#   seeds   = 61562, 61735, 61940 (order 05U8 section 3)
#   support = 61727: the one-ring neighbour of 61562 that shares the two sharpest lower-corridor edges (61562-61727 40.6 deg,
#             61727-62061 32.0 deg at cp2); minimum support for a continuous correction of the 61562 cut
#   held    = 61580 (crease-B anchor; frozen by order) and any crease-reference entry/exit endpoint
#   faces   = all faces incident to the target; frozen_ring = every other vertex of those faces
#   layout  = P05U7 prefix minus the U8 prefix faces (P05U8); prot_sha8 on the cp2 geometry; exempt = U7 exempt + target sources
# Usage: python3 u8_sets.py --s3 GO-05S-S3.obj --cp2 u7cp2_return.npz --outdir DIR
import argparse, hashlib, json, os, numpy as np, trimesh
from collections import defaultdict
ap = argparse.ArgumentParser(); [ap.add_argument(k) for k in ('--s3', '--cp2', '--outdir')]; a = ap.parse_args()
fH = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest(); H = lambda x: hashlib.sha256(np.asarray(x, dtype=np.int64).tobytes()).hexdigest()
CP2 = 'cb2f10524ce5f159312bbd932e6c149f827ef4b37a248c2a41550a969119b7bb'; assert fH(a.cp2) == CP2, 'U7 cp2 return differs'
SEEDS = [61562, 61735, 61940]; SUPPORT = [61727]; HELD = [61580]
REF = json.load(open('reviews/rac-rmot05u4-readiness/crease_reference_v1.json'))
crease_frozen = sorted({int(v) for s in REF['sections'].values() for k in ('entry_edge', 'exit_edge') for v in s[k]})
target = sorted(set(SEEDS + SUPPORT) - set(HELD) - set(crease_frozen)); assert target == sorted(SEEDS + SUPPORT)
s3 = trimesh.load(a.s3, process=False); Vs = np.asarray(s3.vertices); F = np.asarray(s3.faces)
R = np.load(a.cp2); i = R['s3_vid1'] - 1; V = Vs.copy(); W = np.zeros_like(Vs, dtype=np.float32); W[i] = R['V']; mv = ~np.all(W == Vs.astype(np.float32), 1); V[mv] = W[mv]
vf = defaultdict(list)
for k, f in enumerate(F):
    for x in f: vf[int(x)].append(k)
faces = sorted({f for v in target for f in vf[v]}); ring = sorted({int(v) for f in faces for v in F[f]} - set(target))
U6T = json.load(open('reviews/rac-rmot05u6-evidence/readiness/u6_sets_v1.json'))['target_vertices']; U7 = json.load(open('reviews/rac-rmot05u7-evidence/readiness/u7_sets_v1.json'))
U6_EDITED = [61303, 61405, 61559, 61581, 61652, 61750, 62065]; U7_EDITED = [61586, 61771, 62027, 62063]
assert len(target) <= 8 and len(faces) <= 28 and 61580 in ring and not set(target) & set(U7_EDITED) and not set(target) & set(U6_EDITED)
P7 = np.load('reviews/rac-rmot05u7-evidence/readiness/P05U7_preview.npz'); keep7 = P7['P05U7_positions_in_P05S']
A35 = np.load('reviews/rac-rmot05u2-proposal/proposal_sets.npz')['added_faces']; U7F = U7['u7_faces']
assert np.isin(faces, np.union1d(np.union1d(keep7, A35), U7F)).all()
keep8 = np.setdiff1d(keep7, faces); P05S = np.load('reviews/rac-rmot05s-evidence/plan/interface_sets.npz')['P05S_src_ordered']
os.makedirs(a.outdir, exist_ok=True); np.savez(os.path.join(a.outdir, 'P05U8_preview.npz'), P05U8_positions_in_P05S=keep8, P05U8_src_ordered=P05S[keep8])
smap = np.load('reviews/rac-rmot05s-evidence/repair/S3/GO-05S-S3_maps.npz')['src_vertex']
ex7 = np.load('reviews/rac-rmot05u7-evidence/readiness/src_exempt7_f1.npy'); t = np.array(target); ex8 = np.union1d(ex7, smap[t][smap[t] >= 0]).astype(np.int64)
np.save(os.path.join(a.outdir, 'src_exempt8_f1.npy'), ex8)
prot8 = hashlib.sha256(np.ascontiguousarray(V[F[keep8]]).astype(np.float64).tobytes()).hexdigest()
ed = sorted({tuple(sorted((int(f[x]), int(f[y])))) for f in F[faces] for x, y in ((0, 1), (1, 2), (2, 0))}); L = {e: float(np.linalg.norm(V[e[0]] - V[e[1]])) for e in ed}
def ang(fs):
    P = V[F[fs]]; Lf = np.linalg.norm(P[:, [1, 2, 0]] - P[:, [2, 0, 1]], axis=2)
    cs = np.stack([(Lf[:, (k + 1) % 3]**2 + Lf[:, (k + 2) % 3]**2 - Lf[:, k]**2) / (2 * Lf[:, (k + 1) % 3] * Lf[:, (k + 2) % 3]) for k in range(3)], 1)
    return np.degrees(np.arccos(np.clip(cs, -1, 1))).min(1)
runB = set(REF['sections']['B']['baseline_run_faces']); runA = set(REF['sections']['A']['baseline_run_faces'])
out = dict(version='u8_sets_v1', seeds=SEEDS, support=dict(vertices=SUPPORT, reason='shares the two sharpest lower-corridor edges with/next to 61562 (61562-61727 40.6, 61727-62061 32.0 deg at U7 cp2)'),
           held_frozen=dict(vertices=HELD, reason='crease-B anchor (order 05U8 section 3)'), target_vertices=target, u8_faces=faces,
           u8_faces_in_P05U7_prefix=sorted(int(f) for f in faces if f in set(keep7.tolist())), u8_faces_U2_cap=sorted(int(f) for f in faces if f in set(A35.tolist())),
           u8_faces_on_crease_run=dict(A=sorted(int(f) for f in faces if f in runA), B=sorted(int(f) for f in faces if f in runB)),
           frozen_ring=ring, u6_edited_in_ring=[v for v in ring if v in U6_EDITED], u7_edited_in_ring=[v for v in ring if v in U7_EDITED], u6_target_in_target=[v for v in target if v in U6T],
           u6_edited=U6_EDITED, u7_edited=U7_EDITED, counts=dict(target=len(target), faces=len(faces), ring=len(ring)), bounds=dict(max_target=8, max_faces=28),
           min_angle_deg=10.0, edge_band_cm=[0.25, 2.5], baseline_out_of_band_u8_edges=[list(e) for e, l in L.items() if l < 0.25 or l > 2.5], baseline_u8_min_angle=round(float(ang(faces).min()), 3),
           layout=dict(n_prot=int(len(keep8)), prot_sha=prot8, prot_faces_file='P05U8_preview.npz:P05U8_src_ordered', src_exempt='src_exempt8_f1.npy', src_exempt_count=int(len(ex8)), P05U8_f1_sha=H(P05S[keep8])),
           sources=dict(u7cp2_return_npz=CP2, u7cp2_blend='1de9d0ac88f0011062a37f75eed6b6811a5288ae1ef80cc632bfc18c38bfb667', s3_obj=fH(a.s3), crease_reference=fH('reviews/rac-rmot05u4-readiness/crease_reference_v1.json'),
                        u7_sets=fH('reviews/rac-rmot05u7-evidence/readiness/u7_sets_v1.json')),
           list_hashes=dict(target=H(target), faces=H(faces), ring=H(ring)))
p = os.path.join(a.outdir, 'u8_sets_v1.json'); json.dump(out, open(p, 'w'), indent=1, sort_keys=True)
print(json.dumps({k: v for k, v in out.items() if k not in ('u8_faces', 'sources', 'u6_edited', 'u7_edited')})); print('sha', fH(p), 'P05U8', fH(os.path.join(a.outdir, 'P05U8_preview.npz')), 'exempt', fH(os.path.join(a.outdir, 'src_exempt8_f1.npy')))
