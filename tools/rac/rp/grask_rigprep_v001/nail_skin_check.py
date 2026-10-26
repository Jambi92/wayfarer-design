# nail_skin_check.py WORKDIR POSE TAG... : surrounding-skin check for the nail candidates (order b303b9e §3).
# For each left digit: (a) where the documented-cap residual lives — per-vertex deviation from the best rigid fit of the cap, split into
# plate / groove ring / beyond-groove fold skin; (b) skin around the cap — edges within 1.0 cm of the cap boundary that are NOT in the cap:
# max / p95 |strain| and max dihedral change vs rest, per tag. Writes diag/nailskin_POSE.json.
import sys, json, numpy as np
W, P = sys.argv[1:3]; TAGS = sys.argv[3:]
Z = np.load('/tmp/claude-0/rt/frz/v003_frz.npz'); V0 = Z['V'].astype(float); Q = np.asarray(Z['Q'])
CAP = json.load(open(W + '/w/weights_WNcap_log.json'))['digits']; PL = json.load(open(W + '/w/weights_WN_log.json'))['digits']
E = np.unique(np.sort(np.concatenate([Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]]), 1), axis=0)
Es = np.sort(np.concatenate([Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]]), 1); ue, inv = np.unique(Es, axis=0, return_inverse=True)
o = np.argsort(inv.ravel(), kind='stable'); EF = np.tile(np.arange(len(Q)), 4)[o].reshape(-1, 2)
fn = lambda V: (lambda n: n / np.maximum(np.linalg.norm(n, axis=1), 1e-12)[:, None])(np.cross(V[Q[:, 2]] - V[Q[:, 0]], V[Q[:, 3]] - V[Q[:, 1]]))
def rig(P_, X):
    pc, xc = P_.mean(0), X.mean(0); U, S, Vt = np.linalg.svd((P_ - pc).T @ (X - xc)); d = np.sign(np.linalg.det(Vt.T @ U.T)); R = Vt.T @ np.diag([1, 1, d]) @ U.T
    return np.linalg.norm((P_ - pc) @ R.T + xc - X, axis=1)
N0 = fn(V0); d0 = np.degrees(np.arccos(np.clip((N0[EF[:, 0]] * N0[EF[:, 1]]).sum(1), -1, 1))); L0 = np.linalg.norm(V0[ue[:, 0]] - V0[ue[:, 1]], axis=1)
out = {}
for t in TAGS:
    V = np.load('%s/diag/posed/%s_full_%s.npz' % (W, P, t))['V'].astype(float); N = fn(V); dd = np.degrees(np.arccos(np.clip((N[EF[:, 0]] * N[EF[:, 1]]).sum(1), -1, 1))) - d0
    st = np.linalg.norm(V[ue[:, 0]] - V[ue[:, 1]], axis=1) / L0 - 1; out[t] = {}
    for fg in ('index', 'middle', 'ring', 'pinky', 'thumb'):
        k = fg + '_l'; cap = np.array(CAP[k]['vertex_ids']); pl = np.array(PL[k]['vertex_ids']); gr = np.array(PL[k]['groove_ring_ids']); fo = np.setdiff1d(np.setdiff1d(cap, pl), gr)
        dev = dict(zip(cap.tolist(), rig(V0[cap], V[cap]) * 10))
        g = lambda ids: dict(n=len(ids), max_mm=round(max([dev[i] for i in ids], default=0), 4), mean_mm=round(float(np.mean([dev[i] for i in ids])) if len(ids) else 0, 4))
        incap = np.zeros(len(V0), bool); incap[cap] = True
        bnd = np.unique(ue[incap[ue[:, 0]] ^ incap[ue[:, 1]]].ravel()); dist = np.min(np.linalg.norm(V0[:, None] - V0[bnd][None], axis=2), 1) if len(bnd) < 400 else None
        near = (dist < 1.0) & ~incap; em = near[ue[:, 0]] | near[ue[:, 1]]
        out[t][k] = dict(cap_deviation_from_rigid=dict(plate=g(pl.tolist()), groove_ring=g(gr.tolist()), beyond_groove_fold=g(fo.tolist())),
                         ring_skin_outside_cap=dict(edges=int(em.sum()), max_abs_strain_pct=round(float(np.abs(st[em]).max() * 100), 2), p95_abs_strain_pct=round(float(np.percentile(np.abs(st[em]), 95) * 100), 2),
                                                    max_dihedral_change_deg=round(float(dd[em].max()), 2)))
json.dump(out, open('%s/diag/nailskin_%s.json' % (W, P), 'w'), indent=1)
for t in TAGS:
    for k, v in out[t].items(): print(P, t, k, 'dev plate %.3f groove %.3f fold %.3f' % (v['cap_deviation_from_rigid']['plate']['max_mm'], v['cap_deviation_from_rigid']['groove_ring']['max_mm'], v['cap_deviation_from_rigid']['beyond_groove_fold']['max_mm']), 'ring', v['ring_skin_outside_cap'])
