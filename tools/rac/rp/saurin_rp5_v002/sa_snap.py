# sa_snap.py IN.npz OUT.npz : greedy crease-apex vertex sliding (order 236dddc §3-§8, "local sliding"). Topology unchanged; vertices stay embedded on the source.
#   Each round: source points over target (zones 1.2 mm, body 2.6 mm), worst first; nearest unlocked cage vertex is slid onto the apex point with a ring falloff
#   (1, .55, .25, .08) so the local quads translate together; conflict-free (>= 4 rings apart); moved vertices re-embedded onto the local source patch with a jump limit;
#   then shape relaxation (tangential umbrella + parallelogram rule) of unlocked vertices. Tail module / tail ring / pins untouched.
import sys, os, numpy as np, igl, scipy.sparse as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_geo as G
from scipy.spatial import cKDTree
IN, OUT = sys.argv[1:3]; R = int(os.environ.get('ROUNDS', 25)); TZ = float(os.environ.get('TZONE', 1.2)); TB = float(os.environ.get('TB', 2.6)); NS = int(os.environ.get('NSHAPE', 6))
z = dict(np.load(IN)); Q = z['Q']; nb = int(z['n_body']); V = (z['bc'][:, :, None] * G.V[G.F[z['tri']]]).sum(1); nv = len(V); T = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]
pin = np.zeros(nv, bool); pin[nb:] = True; pin[z['tail_ring']] = True; pin[z['pinned']] = True
E = np.unique(np.sort(np.r_[Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]], 1), axis=0)
A = sp.coo_matrix((np.ones(2 * len(E)), (np.r_[E[:, 0], E[:, 1]], np.r_[E[:, 1], E[:, 0]])), shape=(nv, nv)).tocsr(); A.data[:] = 1; deg = np.asarray(A.sum(1)).ravel()
lab = G.LAB; zone = np.isin(lab, ['head', 'hand_xneg', 'hand_xpos', 'foot_xneg', 'foot_xpos', 'tail'])
thr = np.where(zone, TZ, TB) / 10
kd_s = cKDTree(G.V)
def rings(v, k):
    out = [np.array([v])]; seen = {v}
    for _ in range(k):
        nx = np.setdiff1d(A[out[-1]].indices, list(seen)); seen.update(nx.tolist()); out.append(nx)
    return out
def qual(P):
    sd = np.stack([np.linalg.norm(P[Q[:, (k + 1) % 4]] - P[Q[:, k]], axis=1) for k in range(4)], 1); asp = sd.max(1) / np.maximum(sd.min(1), 1e-9); ang = []
    for k in range(4):
        u1 = P[Q[:, (k - 1) % 4]] - P[Q[:, k]]; u2 = P[Q[:, (k + 1) % 4]] - P[Q[:, k]]; ang.append(np.degrees(np.arccos(np.clip((u1 * u2).sum(1) / (np.linalg.norm(u1, axis=1) * np.linalg.norm(u2, axis=1) + 1e-12), -1, 1))))
    ang = np.stack(ang, 1); return (asp > 4) | (ang.min(1) < 45) | (ang.max(1) > 135), asp
def reproject(idx, P, prev):
    d2, fi, cp = igl.point_mesh_squared_distance(P[idx], G.V, G.F)
    bad = np.linalg.norm(cp - prev[idx], axis=1) > np.maximum(0.45, 1.5 * np.linalg.norm(P[idx] - prev[idx], axis=1)); cp[bad] = prev[idx][bad]; return cp
locked = np.zeros(nv, bool); FALL = [1.0, 0.55, 0.25, 0.08]
for r in range(R):
    d = np.sqrt(igl.point_mesh_squared_distance(G.V, V, T)[0]); over = np.nonzero(d > thr)[0]
    bq, asp = qual(V)
    print(r, 'over', len(over), 'max body %.2f zone %.2f mm' % (d[~zone].max() * 10, d[zone].max() * 10), 'bad quads', int(bq.sum()), 'aspect>4', int((asp > 4).sum()), flush=True)
    if not len(over): break
    order = over[np.argsort(-d[over] / thr[over])]; blocked = np.zeros(nv, bool); disp = np.zeros_like(V); wsum = np.zeros(nv); moved = []; cl = -np.ones(nv, int)
    kdc = cKDTree(V)
    for s in order[:4000]:
        cand = kdc.query(G.V[s], k=6)[1]
        cand = [c for c in cand if not pin[c] and not blocked[c] and not locked[c]]
        if not cand: continue
        v = cand[0]; dv = G.V[s] - V[v]; Lr = rings(v, 5)
        el = np.linalg.norm(V[Lr[1]] - V[v], axis=1).mean()
        if np.linalg.norm(dv) > 0.7 * el: dv *= 0.7 * el / np.linalg.norm(dv)
        for k, ring in enumerate(Lr[:4]):
            ring = ring[~pin[ring]]; disp[ring] += FALL[k] * dv; wsum[ring] += 1
        allr = np.concatenate(Lr); cl[allr[cl[allr] < 0]] = len(moved); blocked[np.concatenate(rings(v, 9))] = True; moved.append(v)
    V0 = V.copy(); m = wsum > 0; Vn = V.copy(); Vn[m] += disp[m] / wsum[m][:, None]; idx = np.nonzero(m)[0]
    Vn[idx] = reproject(idx, Vn, V); V = Vn
    mv = np.zeros(nv, bool); mv[moved] = True
    fr = np.nonzero((cl >= 0) & ~pin & ~mv)[0]
    for _ in range(NS):
        N = np.nan_to_num(igl.per_vertex_normals(V, T)); L = (A @ V) / deg[:, None] - V; L -= (L * N).sum(1)[:, None] * N
        bq, _ = qual(V); S = np.zeros_like(V); sc = np.zeros(nv)
        for k in range(4):
            q = Q[bq]; v_ = q[:, k]; a = q[:, (k + 1) % 4]; b = q[:, (k + 2) % 4]; c = q[:, (k + 3) % 4]; np.add.at(S, v_, V[a] + V[c] - V[b] - V[v_]); np.add.at(sc, v_, 1)
        Sd = np.where(sc[:, None] > 0, S / np.maximum(sc, 1)[:, None], 0); Sd -= (Sd * N).sum(1)[:, None] * N
        Vt = V.copy(); Vt[fr] += 0.2 * L[fr] + 0.2 * Sd[fr]; Vt[fr] = reproject(fr, Vt, V); V = Vt
    # per-cluster accept / reject: local worst normalised error must drop and local bad-quad count must not grow
    ch = np.nonzero(np.linalg.norm(V - V0, axis=1) > 1e-7)[0]
    if len(ch):
        sloc = np.unique(np.concatenate(kd_s.query_ball_point(V0[ch], 2.5)))
        dn = np.sqrt(igl.point_mesh_squared_distance(G.V[sloc], V, T)[0])
        own = cl[ch][cKDTree(V0[ch]).query(G.V[sloc])[1]]
        bq0, _ = qual(V0); bq1, _ = qual(V); qcl = cl[Q].max(1)
        acc = 0
        for c in range(len(moved)):
            mm = own == c
            ok = mm.any() and (dn[mm] / thr[sloc[mm]]).max() < (d[sloc[mm]] / thr[sloc[mm]]).max() - 1e-3 and bq1[qcl == c].sum() <= bq0[qcl == c].sum() + 1
            if not ok: V[cl == c] = V0[cl == c]
            else: acc += 1; locked[moved[c]] = True
        print('   moves', len(moved), 'accepted', acc, flush=True)
fi2, bc2, dist = G.embed(V); z['V'] = V; z['tri'] = fi2; z['bc'] = bc2
np.savez_compressed(OUT, **z); print('saved', OUT, 'off-surface max %.4f mm' % (dist.max() * 10))
