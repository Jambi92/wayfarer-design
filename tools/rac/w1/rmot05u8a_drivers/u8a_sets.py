# RM-OT-05U8A: build the FROZEN U8A sets ONCE from the pinned U8 cp1 return (never from a U8A return).
#   target      = the two crease anchors released for this block only: 61581 (crease A), 61580 (crease B) (order 05U8A section 3)
#   faces       = all faces incident to the target; frozen_ring = every other vertex of those faces
#   layout      = P05U8 prefix minus any U8A prefix faces (P05U8A); prot_sha on the U8 cp1 geometry; exempt = U8 exempt + target sources
#   the crease reference file and thresholds are NOT changed; the anchors' s0 / planes come from the frozen reference, not the mesh
# Usage: python3 u8a_sets.py --s3 GO-05S-S3.obj --cp1 u8cp1_return.npz --outdir DIR
import argparse, hashlib, json, os, numpy as np, trimesh
from collections import defaultdict
ap = argparse.ArgumentParser(); [ap.add_argument(k) for k in ('--s3', '--cp1', '--outdir')]; a = ap.parse_args()
fH = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest(); H = lambda x: hashlib.sha256(np.asarray(x, dtype=np.int64).tobytes()).hexdigest()
CP1 = '89c1def3f59bf677a7b4ad4eab6ea84d32ee6b4c67755209f1476338e031911d'; assert fH(a.cp1) == CP1, 'U8 cp1 return differs'
TARGET = [61580, 61581]
REF = json.load(open('reviews/rac-rmot05u4-readiness/crease_reference_v1.json'))
assert not {v for s in REF['sections'].values() for k in ('entry_edge', 'exit_edge') for v in s[k]} & set(TARGET)
s3 = trimesh.load(a.s3, process=False); Vs = np.asarray(s3.vertices); F = np.asarray(s3.faces)
R = np.load(a.cp1); i = R['s3_vid1'] - 1; V = Vs.copy(); W = np.zeros_like(Vs, dtype=np.float32); W[i] = R['V']; mv = ~np.all(W == Vs.astype(np.float32), 1); V[mv] = W[mv]
vf = defaultdict(list)
for k, f in enumerate(F):
    for x in f: vf[int(x)].append(k)
faces = sorted({f for v in TARGET for f in vf[v]}); ring = sorted({int(v) for f in faces for v in F[f]} - set(TARGET))
U6_EDITED = [61303, 61405, 61559, 61581, 61652, 61750, 62065]; U7_EDITED = [61586, 61771, 62027, 62063]; U8_EDITED = [61562, 61727, 61735, 61940]
P8 = np.load('reviews/rac-rmot05u8-evidence/readiness/P05U8_preview.npz'); keep8 = P8['P05U8_positions_in_P05S']
keepA = np.setdiff1d(keep8, faces); P05S = np.load('reviews/rac-rmot05s-evidence/plan/interface_sets.npz')['P05S_src_ordered']
os.makedirs(a.outdir, exist_ok=True); np.savez(os.path.join(a.outdir, 'P05U8A_preview.npz'), P05U8A_positions_in_P05S=keepA, P05U8A_src_ordered=P05S[keepA])
smap = np.load('reviews/rac-rmot05s-evidence/repair/S3/GO-05S-S3_maps.npz')['src_vertex']
ex8 = np.load('reviews/rac-rmot05u8-evidence/readiness/src_exempt8_f1.npy'); t = np.array(TARGET); exA = np.union1d(ex8, smap[t][smap[t] >= 0]).astype(np.int64)
np.save(os.path.join(a.outdir, 'src_exemptA_f1.npy'), exA)
protA = hashlib.sha256(np.ascontiguousarray(V[F[keepA]]).astype(np.float64).tobytes()).hexdigest()
ed = sorted({tuple(sorted((int(f[x]), int(f[y])))) for f in F[faces] for x, y in ((0, 1), (1, 2), (2, 0))}); L = {e: float(np.linalg.norm(V[e[0]] - V[e[1]])) for e in ed}
def ang(fs):
    P = V[F[fs]]; Lf = np.linalg.norm(P[:, [1, 2, 0]] - P[:, [2, 0, 1]], axis=2)
    cs = np.stack([(Lf[:, (k + 1) % 3]**2 + Lf[:, (k + 2) % 3]**2 - Lf[:, k]**2) / (2 * Lf[:, (k + 1) % 3] * Lf[:, (k + 2) % 3]) for k in range(3)], 1)
    return np.degrees(np.arccos(np.clip(cs, -1, 1))).min(1)
out = dict(version='u8a_sets_v1', target_vertices=TARGET, released=dict(vertices=TARGET, scope='U8A block only; crease reference and thresholds unchanged'),
           u8a_faces=faces, u8a_faces_in_P05U8_prefix=sorted(int(f) for f in faces if f in set(keep8.tolist())),
           u8a_faces_on_crease_run=dict(A=sorted(int(f) for f in faces if f in set(REF['sections']['A']['baseline_run_faces'])), B=sorted(int(f) for f in faces if f in set(REF['sections']['B']['baseline_run_faces']))),
           frozen_ring=ring, u6_edited=U6_EDITED, u7_edited=U7_EDITED, u8_edited=U8_EDITED, released_from_u6_edited=[61581],
           counts=dict(target=len(TARGET), faces=len(faces), ring=len(ring)), min_angle_deg=10.0, edge_band_cm=[0.25, 2.5],
           baseline_out_of_band_edges=[list(e) for e, l in L.items() if l < 0.25 or l > 2.5], baseline_min_angle=round(float(ang(faces).min()), 3),
           step_limits_cm={'61581': 0.06, '61580': 0.04},
           layout=dict(n_prot=int(len(keepA)), prot_sha=protA, prot_faces_file='P05U8A_preview.npz:P05U8A_src_ordered', src_exempt='src_exemptA_f1.npy', src_exempt_count=int(len(exA)), P05U8A_f1_sha=H(P05S[keepA])),
           sources=dict(u8cp1_return_npz=CP1, u8cp1_blend='2341d55445a448e24852f98fd9df3984ab12d706ef0b455cb4a2cdb0782860d6', s3_obj=fH(a.s3),
                        crease_reference=fH('reviews/rac-rmot05u4-readiness/crease_reference_v1.json'), u8_sets=fH('reviews/rac-rmot05u8-evidence/readiness/u8_sets_v1.json')),
           list_hashes=dict(target=H(TARGET), faces=H(faces), ring=H(ring)))
p = os.path.join(a.outdir, 'u8a_sets_v1.json'); json.dump(out, open(p, 'w'), indent=1, sort_keys=True)
print(json.dumps({k: v for k, v in out.items() if k not in ('sources', 'u6_edited', 'u7_edited', 'u8_edited')})); print('sha', fH(p), 'P05U8A', fH(os.path.join(a.outdir, 'P05U8A_preview.npz')), 'exempt', fH(os.path.join(a.outdir, 'src_exemptA_f1.npy')))
