# ear_deform.py NATIVE.npz BRANCH.npz OUT.json (bpy python) : order bdcd6a6 §13 static head / neck deformation readiness of the ear branch.
# Source MPFB rig and weights carried to the branch through its weight-proxy map (branch vertices take the row of the nearest removed v005
# ear-zone vertex, i.e. head-bone weighting as the v005 ear), plain LBS from the R-6 stance -- no ear rig, no weight optimisation.
# Per pose, branch-local: new self-intersection pairs touching the branch (vs rest), flipped branch faces (normal against the normal carried
# by its corners' mean bone rotation), root-band face area ratio, minimum ear-sheet clearance to non-head skin (neck / shoulder / trunk),
# root-loop edge strain.
import sys, json, numpy as np, scipy.sparse as sp
import bpy  # noqa: F401
from mathutils.bvhtree import BVHTree
from scipy.spatial import cKDTree
a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
z = np.load(a[0]); cz = np.load(a[1]); OUT = a[2]; SAVE = a[3] if len(a) > 3 and a[3] != '-' else None; FAM = a[4] if len(a) > 4 else None
names = [str(n) for n in z['rest_names']]; POSE = dict(zip(names, z['pose'])); RM = z['rig_world']; m = json.loads(str(z['meta'])); PAR = m['parents']
bones = [str(b) for b in z['bones']]; W0 = z['W'].astype(float); W0 /= np.maximum(W0.sum(1, keepdims=True), 1e-12)
Mx = sp.csr_matrix((cz['M_data'], cz['M_indices'], cz['M_indptr']), shape=tuple(cz['M_shape'])); W = Mx @ W0; W /= np.maximum(W.sum(1, keepdims=True), 1e-12)
V = cz['V'].astype(float); Q = np.asarray(cz['Q']); part = cz['part']; nV = len(V); rec = json.load(open(a[1].replace('.npz', '.json')))
Vw = np.c_[V[:, 0], -V[:, 1], V[:, 2]] / 100.0; RMi = np.linalg.inv(RM); Va = (np.c_[Vw, np.ones(nV)] @ RMi.T)[:, :3]
order = []
def visit(b):
    if b in order: return
    if PAR.get(b): visit(PAR[b])
    order.append(b)
for b in names: visit(b)
def rot(ax, deg):
    t = np.radians(deg); c, s = np.cos(t), np.sin(t); R = {'X': [[1, 0, 0], [0, c, -s], [0, s, c]], 'Y': [[c, 0, s], [0, 1, 0], [-s, 0, c]], 'Z': [[c, -s, 0], [s, c, 0], [0, 0, 1]]}[ax]
    M4 = np.eye(4); M4[:3, :3] = R; return M4
def fk(delta):
    P = {}
    for b in order:
        L_ = (np.linalg.inv(POSE[PAR[b]]) @ POSE[b]) if PAR.get(b) else POSE[b]; base = (P[PAR[b]] @ L_) if PAR.get(b) else L_; D = np.eye(4)
        for ax, dg in delta.get(b, []): D = D @ rot(ax, dg)
        P[b] = base @ D
    return P
def choose(b, want):
    best = None; P0 = fk({}); L_ = np.linalg.norm(np.array(m['tails'][b]) - np.array(m['heads'][b])) / 100.0; t0 = (P0[b] @ np.r_[0, L_, 0, 1])[:3]
    for ax in ('X', 'Z'):
        for sg in (1, -1):
            P1 = fk({b: [(ax, 10 * sg)]}); t1 = (P1[b] @ np.r_[0, L_, 0, 1])[:3]; sc = (RM[:3, :3] @ (t1 - t0)) @ np.asarray(want, float)
            if best is None or sc > best[0]: best = (sc, ax, sg)
    return best[1], best[2]
LEFT, FWD = np.array([1.0, 0, 0]), np.array([0, -1.0, 0])
def R_(b, want, deg): ax, sg = choose(b, want); return (b, [(ax, sg * deg)])
POSES = {'neck_flex30': dict([R_('neck_01', FWD, 15), R_('head', FWD, 15)]), 'neck_ext30': dict([R_('neck_01', -FWD, 15), R_('head', -FWD, 15)]),
         'head_yaw_l45': {'neck_01': [('Y', 22.5)], 'head': [('Y', 22.5)]}, 'head_yaw_r45': {'neck_01': [('Y', -22.5)], 'head': [('Y', -22.5)]},
         'head_pitch_down20': dict([R_('head', FWD, 20)]), 'head_pitch_up20': dict([R_('head', -FWD, 20)]),
         'head_roll_l20': dict([R_('neck_01', LEFT, 10), R_('head', LEFT, 10)]), 'head_roll_r20': dict([R_('neck_01', -LEFT, 10), R_('head', -LEFT, 10)])}
bi = {b: i for i, b in enumerate(bones)}
def skin(P):
    out = np.zeros_like(Va); Rr = np.zeros((nV, 3, 3))
    for b in bones:
        w = W[:, bi[b]]; k = w > 0
        if not k.any(): continue
        S = P[b] @ np.linalg.inv(POSE[b]); out[k] += w[k, None] * (Va[k] @ S[:3, :3].T + S[:3, 3]); Rr[k] += w[k, None, None] * S[:3, :3]
    Xw = np.c_[out, np.ones(nV)] @ RM.T; return np.c_[Xw[:, 0], -Xw[:, 1], Xw[:, 2]] * 100.0, Rr
X0, _ = skin(fk({})); rest_err = float(np.abs(X0 - V).max())
br_v = part != 'v005'; br_f = br_v[Q].any(1); near = np.zeros(nV, bool)
for s_ in ('l', 'r'): near |= np.linalg.norm(V - V[cz['side'] == s_].mean(0), axis=1) < 14
Fsel = np.nonzero(near[Q].all(1))[0]; tri = np.r_[Q[Fsel][:, [0, 1, 2]], Q[Fsel][:, [0, 2, 3]]]; qid = np.r_[Fsel, Fsel]
def selfx(X):
    bvh = BVHTree.FromPolygons(X.tolist(), tri.tolist(), all_triangles=True, epsilon=0.0); bad = set()
    for i, j in bvh.overlap(bvh):
        fi, fj = qid[i], qid[j]
        if fi != fj and not (set(Q[fi]) & set(Q[fj])) and (br_f[fi] or br_f[fj]): bad.add((min(fi, fj), max(fi, fj)))
    return bad
def fnorm(X): n = np.cross(X[Q[:, 2]] - X[Q[:, 0]], X[Q[:, 3]] - X[Q[:, 1]]); return n / np.maximum(np.linalg.norm(n, axis=1), 1e-12)[:, None]
def area(X, q): return 0.5 * np.linalg.norm(np.cross(X[q[:, 2]] - X[q[:, 0]], X[q[:, 3]] - X[q[:, 1]]), axis=1)
SX0 = selfx(V); N0 = fnorm(V)
v2b = cz['v005_to_branch']; loops = {s_: v2b[np.array(rec['sides'][s_]['root_loop_v005'])] for s_ in ('l', 'r')}
Ls = set(np.r_[loops['l'], loops['r']].tolist()); band = np.array([fi for fi in range(len(Q)) if (part[Q[fi]] == 'cuff').any() and (set(Q[fi].tolist()) & Ls)])
ear = np.nonzero(np.isin(part, ['front', 'back', 'rim']))[0]; hw = W[:, bi['head']]; nonhead = np.nonzero((hw < 0.5) & (part == 'v005') & (V[:, 2] > V[:, 2].max() - 45))[0]
def clearance(X):
    d, _ = cKDTree(X[nonhead]).query(X[ear]); return float(d.min())
lE = [np.c_[L, np.roll(L, -1)] for L in loops.values()]; lE = np.concatenate(lE); l0 = np.linalg.norm(V[lE[:, 0]] - V[lE[:, 1]], axis=1)
res = dict(rest_reproduction_max_cm=rest_err, rest_selfx_pairs_touching_branch=len(SX0), rest_ear_to_nonhead_clearance_cm=clearance(V),
           ear_head_weight_min=float(hw[ear].min()), cuff_head_weight_range=[float(hw[part == 'cuff'].min()), float(hw[part == 'cuff'].max())], poses={})
for pn, dl in POSES.items():
    X, Rr = skin(fk(dl)); SX = selfx(X); new = SX - SX0; N = fnorm(X)
    Rf = Rr[Q].mean(1); n0b = np.c_[N0[:, 0], -N0[:, 1], N0[:, 2]]; nc = np.einsum('fij,fj->fi', Rf, n0b); nc = np.c_[nc[:, 0], -nc[:, 1], nc[:, 2]]
    flip = ((N * nc).sum(1) < 0) & br_f
    ar = area(X, Q[band]) / np.maximum(area(V, Q[band]), 1e-12); st_ = np.linalg.norm(X[lE[:, 0]] - X[lE[:, 1]], axis=1) / l0 - 1
    res['poses'][pn] = dict(new_selfx_pairs_touching_branch=len(new), flipped_branch_faces=int(flip.sum()), root_band_area_ratio_min=float(ar.min()), root_band_area_ratio_max=float(ar.max()),
                            root_band_inverted=int((((N * nc).sum(1) < 0)[band]).sum()), root_loop_edge_strain_pct=[float(100 * st_.min()), float(100 * st_.max())],
                            ear_to_nonhead_clearance_cm=clearance(X),
                            new_pairs=[[int(f), int(g), '/'.join(sorted(set(part[Q[f]].tolist()))), '/'.join(sorted(set(part[Q[g]].tolist())))] for f, g in sorted(new)[:20]],
                            flipped_faces=[int(f) for f in np.nonzero(flip)[0][:50]], root_inverted_faces=[int(f) for f in band[((N * nc).sum(1) < 0)[band]][:50]])
    if SAVE: np.save('%s_%s.npy' % (SAVE, pn), X.astype(np.float32))
    print(pn, res['poses'][pn], flush=True)
if FAM:                                                    # v005 baseline: the same root-loop edges on the CF2 family realization
    fz = np.load(FAM); Mf = sp.csr_matrix((fz['M_data'], fz['M_indices'], fz['M_indptr']), shape=tuple(fz['M_shape'])); Wf = Mf @ W0; Wf /= np.maximum(Wf.sum(1, keepdims=True), 1e-12)
    Vf = fz['V'].astype(float); Vfa = (np.c_[np.c_[Vf[:, 0], -Vf[:, 1], Vf[:, 2]] / 100.0, np.ones(len(Vf))] @ RMi.T)[:, :3]
    lE0 = np.concatenate([np.c_[np.array(rec['sides'][s_]['root_loop_v005']), np.roll(np.array(rec['sides'][s_]['root_loop_v005']), -1)] for s_ in ('l', 'r')]); l00 = np.linalg.norm(Vf[lE0[:, 0]] - Vf[lE0[:, 1]], axis=1)
    for pn, dl in POSES.items():
        P = fk(dl); out = np.zeros_like(Vfa)
        for b in bones:
            w = Wf[:, bi[b]]; k = w > 0
            if k.any(): S = P[b] @ np.linalg.inv(POSE[b]); out[k] += w[k, None] * (Vfa[k] @ S[:3, :3].T + S[:3, 3])
        Xw = np.c_[out, np.ones(len(Vf))] @ RM.T; Xf = np.c_[Xw[:, 0], -Xw[:, 1], Xw[:, 2]] * 100.0
        st0 = np.linalg.norm(Xf[lE0[:, 0]] - Xf[lE0[:, 1]], axis=1) / l00 - 1; res['poses'][pn]['v005_root_loop_edge_strain_pct'] = [float(100 * st0.min()), float(100 * st0.max())]
json.dump(res, open(OUT, 'w'), indent=1)
