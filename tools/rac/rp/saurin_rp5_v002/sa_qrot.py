# sa_qrot.py IN.npz OUT.npz : local quad PHASE changes for the T-4 production pass (order 236dddc §9 "local phase changes"). For each residual quad
#   (aspect > 4 outside tip exceptions) and each neighbour across an edge, the hexagon of the pair is re-split along one of its two other main diagonals
#   (quad edge rotation; vertex count and positions unchanged, 100 % quads, orientation kept). The best split is taken only if the pair's worst
#   aspect / angle improves and no vertex leaves valence 3..5 (no new valence-2 / >= 6 poles). Quads touching pins / the tail ring, the tail module and tip caps are not touched.
import sys, os, numpy as np, collections, igl
from scipy.spatial import cKDTree
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_geo as G
IN, OUT = sys.argv[1:3]
z = dict(np.load(IN)); Q = z['Q'].copy(); V = (z['bc'][:, :, None] * G.V[G.F[z['tri']]]).sum(1); nv = len(V); nb = int(z['n_body']); ql = z['qlab'].astype(str)
NO = {'finger_cap', 'thumb_cap', 'toe_cap', 'tail'}; CRIT = {'shoulder', 'elbow', 'wrist', 'hip', 'knee', 'ankle', 'neck', 'finger', 'thumb', 'toe'}
def score(P4):
    sd = np.linalg.norm(np.roll(P4, -1, 0) - P4, axis=1); a = sd.max() / max(sd.min(), 1e-9)
    u1 = np.roll(P4, 1, 0) - P4; u2 = np.roll(P4, -1, 0) - P4; g = np.degrees(np.arccos(np.clip((u1 * u2).sum(1) / (np.linalg.norm(u1, axis=1) * np.linalg.norm(u2, axis=1) + 1e-12), -1, 1)))
    convex = np.all(np.cross(u2, u1) @ np.cross(P4[2] - P4[0], P4[3] - P4[1]) > 0)
    return max(a - 4, (45 - g.min()) / 10, (g.max() - 135) / 10) + (0 if convex else 10)
val = np.bincount(Q.ravel(), minlength=nv); rot = 0
zone = np.isin(G.LAB, ['head', 'hand_xneg', 'hand_xpos', 'foot_xneg', 'foot_xpos', 'tail']); thr = np.where(zone, 0.13, 0.27); KS = cKDTree(G.V)
def cov_ok(old, new):
    P_ = V[np.unique(np.r_[old].ravel())]; c = P_.mean(0); r = np.linalg.norm(P_ - c, axis=1).max(); sv = np.array(KS.query_ball_point(c, r), int)
    if not len(sv): return True
    To = np.array([[q[0], q[1], q[2]] for q in old] + [[q[0], q[2], q[3]] for q in old]); Tn = np.array([[q[0], q[1], q[2]] for q in new] + [[q[0], q[2], q[3]] for q in new])
    db = np.sqrt(igl.point_mesh_squared_distance(G.V[sv], V, To)[0]); da = np.sqrt(igl.point_mesh_squared_distance(G.V[sv], V, Tn)[0])
    return not np.any((da > thr[sv]) & (da > db + 1e-5))
pin = np.zeros(nv, bool); pin[nb:] = True; pin[z['tail_ring']] = True; pin[z['pinned']] = True
for rnd in range(3):
    EQ = collections.defaultdict(list)
    for i, q in enumerate(Q):
        for k in range(4): EQ[(min(q[k], q[(k + 1) % 4]), max(q[k], q[(k + 1) % 4]))].append(i)
    sd = np.linalg.norm(np.roll(V[Q], -1, 1) - V[Q], axis=2); asp = sd.max(1) / sd.min(1)
    bad = [i for i in np.argsort(-asp) if asp[i] > 4 and ql[i] not in NO]; used = set(); n0 = rot
    if os.environ.get('CRITANG'):
        P4_ = V[Q]; u1_ = np.roll(P4_, 1, 1) - P4_; u2_ = np.roll(P4_, -1, 1) - P4_; an_ = np.degrees(np.arccos(np.clip((u1_ * u2_).sum(2) / (np.linalg.norm(u1_, axis=2) * np.linalg.norm(u2_, axis=2) + 1e-12), -1, 1)))
        bad = [i for i in np.nonzero(((an_.min(1) < 45) | (an_.max(1) > 135)) & np.isin(ql, list(CRIT)))[0]]
    for qi in bad:
        if qi in used: continue
        best = None
        for k in range(4):
            q = list(Q[qi]); u, v = q[k], q[(k + 1) % 4]; nbr = [j for j in EQ[(min(u, v), max(u, v))] if j != qi]
            if not nbr: continue
            r = nbr[0]
            if r in used or ql[r] in NO or pin[q + list(Q[r])].any(): continue
            qq = q[k:] + q[:k]; w, y = qq[2], qq[3]; rr = list(Q[r]); kr = rr.index(v); rr = rr[kr:] + rr[:kr]; assert rr[1] == u; s_, t_ = rr[2], rr[3]
            H = [v, w, y, u, s_, t_]; cur = max(score(V[qq]), score(V[rr]))
            for (A1, A2), (e1, e2) in (((H[1:5], [H[4], H[5], H[0], H[1]]), (w, s_)), (([H[2], H[3], H[4], H[5]], [H[5], H[0], H[1], H[2]]), (y, t_))):
                vv = val.copy(); vv[[u, v]] -= 1; vv[[e1, e2]] += 1
                if vv[[u, v, e1, e2]].min() < 3 or vv[[u, v, e1, e2]].max() > (int(os.environ.get('VMAX', 5)) if ql[qi] not in CRIT else 5): continue
                sc = max(score(V[A1]), score(V[A2]))
                if sc < cur - 0.05 and (best is None or sc < best[0]) and cov_ok([qq, rr], [A1, A2]): best = (sc, r, A1, A2, u, v, e1, e2)
        if best:
            sc, r, A1, A2, u, v, e1, e2 = best; Q[qi] = A1; Q[r] = A2; val[[u, v]] -= 1; val[[e1, e2]] += 1; used |= {qi, r}; rot += 1
    print('round', rnd, 'rotations', rot - n0, flush=True)
    if rot == n0: break
ec = collections.Counter((min(q[k], q[(k + 1) % 4]), max(q[k], q[(k + 1) % 4])) for q in Q for k in range(4)); assert min(ec.values()) == 2 and max(ec.values()) == 2
dirE = collections.Counter((q[k], q[(k + 1) % 4]) for q in Q for k in range(4)); assert max(dirE.values()) == 1
sd = np.linalg.norm(np.roll(V[Q], -1, 1) - V[Q], axis=2); asp = sd.max(1) / sd.min(1); print('rotations', rot, 'aspect>4 non-tip', int(((asp > 4) & ~np.isin(ql, list(NO))).sum()))
z['Q'] = Q; np.savez_compressed(OUT, **z)
