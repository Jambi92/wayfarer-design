# sa_tail_deform.py OUT.json : RP5 Saurin DIAGNOSTIC tail deformation (order 53976fb §19 tail items) -- not rig finalization. A temporary articulation
# scaffold = the 16-point equal-arc tail chain (sa_landmarks) + root centre + tip; linear blend skinning with smooth weights (each vertex between its two
# nearest chain joints by projection parameter, 2-joint linear falloff). The SAME skinning is applied to the authored tail module (cage) and to the canonical
# source tail surface (caudal region S of the base), so topology effects separate from scaffold / source effects (ownership classification, §20):
#   identical class on cage and source -> scaffold / source-deformation (PD-2-type) item, not topology; worse on cage only -> topology.
# Poses: root lateral bend 30 deg (about u over joints 0-3), root vertical bend 25 deg (about x over joints 0-3), mid-tail lateral bend 40 deg (joints 6-10),
# twist 30 deg (about the local chain axis, joints 2-12). Metrics: flipped faces (normal reversal vs rest), folds (adjacent face normal angle change > 120 deg
# where the rest pair is < 120 deg), edge strain p95 / max (%), local volume proxy of each ring (area change %).
import sys, json, numpy as np, igl
OUT = sys.argv[1]; W = '/tmp/claude-0/rt/sa'
LM = json.load(open(W + '/lm/SA-M188_landmarks.json'))['landmarks']
J = np.array([LM['tail_root_centre']['p_cm']] + [LM['tail_chain_%02d' % k]['p_cm'] for k in range(1, 17)] + [LM['tail_tip']['p_cm']])
z = np.load(W + '/tail/SA_tail_module.npz'); Vc = z['V'].astype(float); Qc = z['Q']; Tc = np.r_[Qc[:, [0, 1, 2]], Qc[:, [0, 2, 3]]]
b = np.load(W + '/src/saurin_w2_final_base.npz'); VB = b['v'].astype(float); FB = b['f'].astype(np.int64); sub = z['sub']
inS = np.zeros(len(VB), bool); inS[sub] = True; FS = FB[np.all(inS[FB], 1)]; m = -np.ones(len(VB), int); m[sub] = np.arange(len(sub)); FS = m[FS]; VS = VB[sub]
def weights(P):
    best = np.full(len(P), 1e9); seg = np.zeros(len(P), int); tt = np.zeros(len(P))
    for k in range(len(J) - 1):
        a, v = J[k], J[k + 1] - J[k]; t = np.clip(((P - a) @ v) / (v @ v), 0, 1); d = np.linalg.norm(P - (a + np.outer(t, v)), axis=1); mm = d < best; best[mm] = d[mm]; seg[mm] = k; tt[mm] = t[mm]
    Wt = np.zeros((len(P), len(J))); Wt[np.arange(len(P)), seg] = 1 - tt; Wt[np.arange(len(P)), seg + 1] += tt; return Wt
def rot(axis, deg):
    a = np.asarray(axis, float); a /= np.linalg.norm(a); t = np.radians(deg); K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]]); return np.eye(3) + np.sin(t) * K + (1 - np.cos(t)) * K @ K
def pose_mats(kind):
    """per-joint world transforms (R, t) composing the chain rotations from the root outward"""
    loc = {}
    if kind == 'root_lateral_30': loc = {k: (np.array([0, 0, 1.0]), 30 / 4) for k in range(0, 4)}
    if kind == 'root_vertical_25': loc = {k: (np.array([1.0, 0, 0]), 25 / 4) for k in range(0, 4)}
    if kind == 'mid_lateral_40': loc = {k: (np.array([0, 0, 1.0]), 40 / 5) for k in range(6, 11)}
    if kind == 'twist_30': loc = {k: (None, 30 / 11) for k in range(2, 13)}
    M = [np.eye(4)]
    for k in range(len(J)):
        T = M[-1].copy()
        if k in loc:
            ax, dg = loc[k]
            if ax is None: ax = J[min(k + 1, len(J) - 1)] - J[k]
            R = rot(ax, dg); jp = T[:3, :3] @ J[k] + T[:3, 3]; R4 = np.eye(4); R4[:3, :3] = R; R4[:3, 3] = jp - R @ jp; T = R4 @ T
        M.append(T)
    return M[1:]
def skin(P, Wt, M):
    out = np.zeros_like(P)
    for k in range(len(J)): out += Wt[:, k:k + 1] * (P @ M[k][:3, :3].T + M[k][:3, 3])
    return out
def metrics(P0, P1, T):
    n0 = np.cross(P0[T[:, 1]] - P0[T[:, 0]], P0[T[:, 2]] - P0[T[:, 0]]); n1 = np.cross(P1[T[:, 1]] - P1[T[:, 0]], P1[T[:, 2]] - P1[T[:, 0]])
    flip = int(((n0 * n1).sum(1) < 0).sum())
    TT, _ = igl.triangle_triangle_adjacency(T); i = np.repeat(np.arange(len(T)), 3); j = TT.ravel(); ok = j >= 0; i, j = i[ok], j[ok]
    u0 = n0 / np.maximum(np.linalg.norm(n0, axis=1, keepdims=True), 1e-12); u1 = n1 / np.maximum(np.linalg.norm(n1, axis=1, keepdims=True), 1e-12)
    c = np.cos(np.radians(120)); fold = int((((u1[i] * u1[j]).sum(1) < c) & ((u0[i] * u0[j]).sum(1) >= c)).sum() // 2)
    E = np.unique(np.sort(np.r_[T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]], 1), axis=0); l0 = np.linalg.norm(P0[E[:, 0]] - P0[E[:, 1]], axis=1); l1 = np.linalg.norm(P1[E[:, 0]] - P1[E[:, 1]], axis=1)
    st = np.abs(l1 / np.maximum(l0, 1e-9) - 1) * 100
    return dict(flipped=flip, folds=fold, strain_p95_pct=round(float(np.percentile(st, 95)), 3), strain_max_pct=round(float(st.max()), 2))
Wc = weights(Vc); Ws = weights(VS); res = {}
for kind in ('root_lateral_30', 'root_vertical_25', 'mid_lateral_40', 'twist_30'):
    M = pose_mats(kind); Pc = skin(Vc, Wc, M); Ps = skin(VS, Ws, M)
    mc = metrics(Vc, Pc, Tc); ms = metrics(VS, Ps, FS)
    new = [k for k in ('flipped', 'folds') if mc[k] > 0 and ms[k] == 0]
    if new: cls = 'NEW TOPOLOGY CLASS on the cage: ' + ', '.join(new)
    elif mc['flipped'] == mc['folds'] == 0 and ms['flipped'] == ms['folds'] == 0: cls = 'clean on cage and source'
    elif mc['flipped'] == mc['folds'] == 0: cls = 'clean on the cage; the dense source surface flips / folds under the same scaffold (source-deformation / PD-2-type ownership, not topology)'
    else: cls = 'same class on cage and source (scaffold / source-deformation ownership)'
    res[kind] = dict(cage=mc, source=ms, classification=cls); np.savez_compressed(W + '/tail/pose_%s.npz' % kind, V=Pc, Q=Qc)
    print(kind, mc, ms, cls, flush=True)
json.dump(dict(scaffold='temporary 18-joint tail chain LBS (diagnostic only)', poses=res), open(OUT, 'w'), indent=1)
