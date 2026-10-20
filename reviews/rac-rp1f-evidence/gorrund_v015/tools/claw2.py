# claw2.py IN.npz OUT.npz NAILS.json : RP1F feline claw/sheath (v2). Per nail, in the local frame (n dorsal, e1 distal, e2 lateral):
#  1. erase: the human nail-plate border is relaxed away (bounded Laplacian smoothing over the plate area)
#  2. claw: a narrow arched keratin ridge along the distal-phalanx midline, tapering toward the tip
#  3. tip: the distal end of the ridge extends with a mild downward curl (modest pointed tip)
#  4. sheath: a soft fold around the claw root
import sys, json, numpy as np
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
inp, out, nj = sys.argv[1:4]
z = np.load(inp); Q = z['Q'].astype(np.int64); F = z['F'].astype(np.int64)
fl = np.array([1, -1, 1]); V = z['V'].astype(float) * fl
nails = json.load(open(nj)); rep = {}
def smooth01(x): x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)
def vnormals(P):
    fn = np.cross(P[F[:, 1]] - P[F[:, 0]], P[F[:, 2]] - P[F[:, 0]]); vn = np.zeros_like(P)
    for k in range(3): np.add.at(vn, F[:, k], fn)
    return vn / (np.linalg.norm(vn, axis=1, keepdims=True) + 1e-15)
V0 = V.copy(); vn0 = vnormals(V)
for nm, P in nails.items():
    C = np.array(P['C']); T = np.array(P['T']); W = P['W']
    near = np.where(np.linalg.norm(V0 - C, axis=1) < 0.25)[0]; n = vn0[near].mean(0); n /= np.linalg.norm(n)
    if 'n' in P: n = np.array(P['n']) / np.linalg.norm(P['n'])
    d = T - C; e1 = d - (d @ n) * n; L = np.linalg.norm(e1); e1 /= L; e2 = np.cross(n, e1)
    sr = -P.get('root', L); Rr = max(1.6 * W, L - sr + 0.4) + 0.3
    reg = np.where((np.linalg.norm(V0 - C, axis=1) < Rr) & ((vn0 @ n) > P.get('ncut', -0.2)))[0]
    lm = -np.ones(len(V), int); lm[reg] = np.arange(len(reg)); qq = Q[(lm[Q] >= 0).all(1)]
    ee = np.vstack([qq[:, [i, (i + 1) % 4]] for i in range(4)]); A = sp.coo_matrix((np.ones(len(ee)), (lm[ee[:, 0]], lm[ee[:, 1]])), shape=(len(reg), len(reg))).tocsr()
    _, lab = connected_components(A, directed=False); keep = lab == lab[np.argmin(np.linalg.norm(V0[reg] - C, axis=1))]
    reg = reg[keep]; lm[:] = -1; lm[reg] = np.arange(len(reg)); A = A[keep][:, keep]
    X = V0[reg] - C; s = X @ e1; u = X @ e2; au = np.abs(u)
    # 1 erase weight: plate area (+ margin) and smooth falloff
    we = smooth01((1.35 * W - au) / (0.35 * W)) * smooth01((s - (sr - 0.25)) / 0.25) * smooth01((L + 0.2 - s) / 0.2)
    deg = np.asarray(A.sum(1)).ravel(); Pm = V[reg].copy()
    for it in range(P.get('erase_it', 30)):
        Lp = (A @ Pm) / np.maximum(deg, 1)[:, None] - Pm; Pm += 0.5 * we[:, None] * Lp
    # restore the smoothed shrink along the normal (volume keep): push back by the mean normal offset in the plate core
    nv = vn0[reg]; off = ((V0[reg] - Pm) * nv).sum(1); core = we > 0.8
    Pm += (np.median(off[core]) if core.any() else 0.0) * we[:, None] * nv
    # 2 claw ridge (tapering), 3 tip extension, 4 sheath fold
    t = np.clip((s - sr) / (L - sr), 0, 1)
    sig = P['sig'] * (1 - 0.55 * t)
    rise = smooth01((s - sr) / 0.3) * smooth01((L + 0.05 - s) / 0.12 + 0.4)
    ridge = P['H'] * np.exp(-(u / sig) ** 2) * rise
    th = np.radians(P.get('curl_deg', 40))
    tipw = np.exp(-(u / (0.8 * sig)) ** 2) * smooth01((s - (L - P['tl'])) / P['tl']) * np.clip(nv @ n + 0.2, 0, 1)
    tipd = P['tip'] * tipw[:, None] * (np.cos(th) * e1 - np.sin(th) * n)[None, :]
    sheath = P['sheath'] * np.exp(-((s - (sr + 0.12)) / 0.14) ** 2) * smooth01((1.1 * W - au) / (0.4 * W)) * (1 - np.exp(-(u / (0.9 * P['sig'])) ** 2) * 0.6)
    V[reg] = Pm + (ridge + sheath)[:, None] * nv + tipd
    mv = np.linalg.norm(V[reg] - V0[reg], axis=1)
    rep[nm] = dict(C=C.round(3).tolist(), T=T.round(3).tolist(), n=n.round(3).tolist(), e1=e1.round(3).tolist(), C_to_T_cm=round(float(L), 3),
                   region_vertices=int(len(reg)), moved_vertices=int((mv > 1e-5).sum()), max_move_mm=round(float(mv.max() * 10), 3), params=P)
    print(nm, 'region', len(reg), 'moved', int((mv > 1e-5).sum()), 'max mm %.2f' % (mv.max() * 10))
np.savez_compressed(out, V=V * fl, F=F, Q=Q); json.dump(rep, open(out.replace('.npz', '_claws.json'), 'w'), indent=1)
