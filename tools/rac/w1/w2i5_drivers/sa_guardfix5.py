# RAC W2I5 fold-guard closure: the 12-round guard left 2 residual faces (SA-M188-N-FAHI-T72 / -T78, same face); this pass zeroes the W2I5
# delta smoothly (diffused hard mask) around any remaining bad face and re-checks the affected bodies until 0, then re-checks all 62 bodies.
import sys, os, json, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import sa_sculpt as SC
FN = SC.FN; F0 = FN.F0; V0 = FN.V0
import sa_w2i2_build as WB
fn = SC.OUTD + '/sculpt_delta.npz'; z = np.load(fn); D5 = z['D']; info = json.loads(str(z['info']))
A, deg = FN.adjacency(); nr = lambda Q: np.cross(Q[F0[:, 1]] - Q[F0[:, 0]], Q[F0[:, 2]] - Q[F0[:, 0]]).astype(np.float32)
def check(bodies):
    SC._D5 = D5; bad_all = np.zeros(len(F0), bool); per = {}
    for bid, p, h, note in WB.ALL:
        if bodies is not None and bid not in bodies: continue
        P4 = FN.build_f(p, h)[0]; n4 = nr(P4); ns = SC.smooth_face_normals(P4, A, deg); fold4 = np.einsum('ij,ij->i', n4, ns) < 0
        nP = nr(SC.build_s(p, h)[0]); flip4 = np.einsum('ij,ij->i', n4, nP) < 0; foldP = np.einsum('ij,ij->i', ns, nP) < 0
        cos = lambda a, b: np.einsum('ij,ij->i', a, b) / (np.linalg.norm(a, axis=1) * np.linalg.norm(b, axis=1) + 1e-20)
        bad = (flip4 & ~(~foldP & (cos(nP, ns) > cos(n4, ns)))) | (foldP & ~fold4)
        if bad.any(): per[bid] = int(bad.sum()); bad_all |= bad
    SC._D5 = None; return bad_all, per
fixlog = []
bodies = set(info['fold_guard'][-1]['bodies'])
for rnd in range(6):
    bad, per = check(bodies); fixlog.append(per); print('fix round', rnd, per, flush=True)
    if not bad.any(): break
    m = np.zeros(len(V0)); m[np.unique(F0[bad])] = 1
    for _ in range(4): m = np.minimum(1, m + A @ m)
    w = m.copy()
    for _ in range(8): w = np.maximum(w, 0.5 * w + 0.5 * (A @ w) / deg)
    D5 = D5 * (1 - np.clip(w, 0, 1))[:, None]
bad, per = check(None); print('all 62 bodies residual', per, flush=True)
info['fold_guard_closure'] = dict(rounds=fixlog, all_bodies_residual=per); info['max_delta_cm'] = float(np.linalg.norm(D5, axis=1).max())
np.savez_compressed(fn, D=D5.astype(np.float64), info=json.dumps(info)); print('saved', info['max_delta_cm'])
