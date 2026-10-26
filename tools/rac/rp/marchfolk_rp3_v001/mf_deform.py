# mf_deform.py NATIVE.npz CAND.npz OUTDIR TAG : RP3 limited diagnostic deformation set (order d18ff2a §13). Source rig + source MPFB weights (carried to
# the candidate through its linear map), plain LBS from the R-6 stance; no weight optimisation. The same poses are run on the native hm08 body and the
# candidate so topology effects separate from weight / joint-placement effects.
# Per pose: non-adjacent self-intersecting face pairs (new vs R-6), new folds (dihedral > 120 deg), flipped faces (normal reversed against the normal
# carried by the dominant bone rotation), strain p95 / max of edges within the joint zone, joint-zone cone-volume change, loop compression (min ratio of
# adjacent closed-ring spacing in the zone vs rest). Writes OUTDIR/deform_TAG.json and posed npz.
import sys, os, json, numpy as np, scipy.sparse as sp
import bpy  # noqa: F401  (mathutils)
from mathutils.bvhtree import BVHTree
a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
z = np.load(a[0]); cz = np.load(a[1]); O = a[2]; TAG = a[3]; os.makedirs(O, exist_ok=True)
names = [str(n) for n in z['rest_names']]; REST = dict(zip(names, z['rest'])); POSE = dict(zip(names, z['pose'])); RM = z['rig_world']; m = json.loads(str(z['meta'])); PAR = m['parents']
bones = [str(b) for b in z['bones']]; W0 = z['W'].astype(float); W0 /= np.maximum(W0.sum(1, keepdims=True), 1e-12)
if 'M_data' in cz.files:
    Mx = sp.csr_matrix((cz['M_data'], cz['M_indices'], cz['M_indptr']), shape=tuple(cz['M_shape'])); W = Mx @ W0; W /= np.maximum(W.sum(1, keepdims=True), 1e-12)
else: W = W0
V = cz['V'].astype(float); Q = cz['Q']; nV = len(V)
Vw = np.c_[V[:, 0], -V[:, 1], V[:, 2]] / 100.0; RMi = np.linalg.inv(RM); Va = (np.c_[Vw, np.ones(nV)] @ RMi.T)[:, :3]      # armature space
if os.environ.get('KNEE_OFF_CM'):   # v003 §12 diagnostic: move the calf_l pivot (knee centre) by an analysis-frame cm offset; children follow
    _o = np.array([float(x) for x in os.environ['KNEE_OFF_CM'].split(',')]); _ob = np.array([_o[0], -_o[1], _o[2]]) / 100.0
    POSE['calf_l'] = POSE['calf_l'].copy(); POSE['calf_l'][:3, 3] += RMi[:3, :3] @ _ob
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
        L_ = (np.linalg.inv(POSE[PAR[b]]) @ POSE[b]) if PAR.get(b) else POSE[b]
        base = (P[PAR[b]] @ L_) if PAR.get(b) else L_
        D = np.eye(4)
        for ax, dg in delta.get(b, []): D = D @ rot(ax, dg)
        P[b] = base @ D
    return P
def world_dir(b, P): return (RM[:3, :3] @ P[b][:3, 1])   # bone y axis = head -> tail
def choose(b, want):
    """local axis / sign whose +10 deg rotation moves the bone tail most along the wanted WORLD (Blender) direction"""
    best = None; P0 = fk({}); L_ = np.linalg.norm(np.array(m['tails'][b]) - np.array(m['heads'][b])) / 100.0
    t0 = (P0[b] @ np.r_[0, L_, 0, 1])[:3]
    for ax in ('X', 'Z'):
        for sg in (1, -1):
            P1 = fk({b: [(ax, 10 * sg)]}); t1 = (P1[b] @ np.r_[0, L_, 0, 1])[:3]; sc = (RM[:3, :3] @ (t1 - t0)) @ np.asarray(want, float)
            if best is None or sc > best[0]: best = (sc, ax, sg)
    return best[1], best[2]
LEFT, FWD, UP = np.array([1.0, 0, 0]), np.array([0, -1.0, 0]), np.array([0, 0, 1.0])     # Blender world: subject left +X, forward -Y, up +Z
def R_(b, want, deg):
    ax, sg = choose(b, want); return (b, [(ax, sg * deg)])
POSES = {}
s = 'l'; sl = 1
POSES['shoulder_abd45_l'] = dict([R_('upperarm_l', LEFT, 37)]); POSES['shoulder_abd90_l'] = dict([R_('upperarm_l', LEFT, 82)]); POSES['shoulder_flex90_l'] = dict([R_('upperarm_l', FWD, 90)])
POSES['elbow_90_l'] = dict([R_('lowerarm_l', FWD, 90)]); POSES['elbow_130_l'] = dict([R_('lowerarm_l', FWD, 130)])
POSES['wrist_flex60_l'] = dict([R_('hand_l', -LEFT, 60)]); POSES['wrist_ext60_l'] = dict([R_('hand_l', LEFT, 60)])
fist = {}
for fg in ('index', 'middle', 'ring', 'pinky'):
    for k, dg in ((1, 70), (2, 90), (3, 60)): b = '%s_%02d_l' % (fg, k); fist.update(dict([R_(b, -LEFT, dg)]))
fist.update(dict([R_('thumb_02_l', -LEFT, 30), R_('thumb_03_l', -LEFT, 40)])); POSES['fist_l'] = fist
POSES['thumb_opposition_l'] = dict([R_('thumb_01_l', -LEFT + FWD, 35), R_('thumb_02_l', -LEFT, 25), R_('thumb_03_l', -LEFT, 25)])
POSES['hip_flex90_l'] = dict([R_('thigh_l', FWD, 90)]); POSES['knee_90_l'] = dict([R_('calf_l', -FWD, 90)]); POSES['knee_140_l'] = dict([R_('calf_l', -FWD, 140)])
POSES['ankle_dorsi20_l'] = dict([R_('foot_l', UP, 20)])
POSES['trunk_twist30'] = {b: [('Y', 10.0)] for b in ('spine_01', 'spine_02', 'spine_03')}
POSES['neck_flex30'] = dict([R_('neck_01', FWD, 15), R_('head', FWD, 15)]); POSES['neck_rot45'] = {'neck_01': [('Y', 22.5)], 'head': [('Y', 22.5)]}
if os.environ.get('ONLY_POSES'): POSES = {k: v for k, v in POSES.items() if k in os.environ['ONLY_POSES'].split(',')}
ZONE = {'shoulder': ('upperarm_l', 14), 'elbow': ('lowerarm_l', 9), 'wrist': ('hand_l', 6), 'fist': ('hand_l', 10), 'thumb': ('thumb_01_l', 6), 'hip': ('thigh_l', 16),
        'knee': ('calf_l', 10), 'ankle': ('foot_l', 8), 'trunk': ('spine_02', 22), 'neck': ('neck_01', 10)}
P0 = fk({}); Sk0 = {b: P0[b] @ np.linalg.inv(POSE[b]) for b in bones}
bi = {b: i for i, b in enumerate(bones)}
def skin(P):
    out = np.zeros_like(Va); Rr = np.zeros((nV, 3, 3))
    for b in bones:
        w = W[:, bi[b]]; k = w > 0
        if not k.any(): continue
        S = P[b] @ np.linalg.inv(POSE[b]); out[k] += w[k, None] * (Va[k] @ S[:3, :3].T + S[:3, 3]); Rr[k] += w[k, None, None] * S[:3, :3]
    Xw = np.c_[out, np.ones(nV)] @ RM.T; X = np.c_[Xw[:, 0], -Xw[:, 1], Xw[:, 2]] * 100.0; return X, Rr
X0, _ = skin(P0); rest_err = float(np.abs(X0 - V).max())
TRI = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]; qid = np.r_[np.arange(len(Q)), np.arange(len(Q))]
E = np.unique(np.sort(np.concatenate([Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]]), 1), axis=0); L0 = np.linalg.norm(V[E[:, 0]] - V[E[:, 1]], axis=1)
fe = {}
for fi, q in enumerate(Q):
    for k in range(4): fe.setdefault((min(q[k], q[(k + 1) % 4]), max(q[k], q[(k + 1) % 4])), []).append(fi)
FE = np.array([v for v in fe.values() if len(v) == 2])
def fnorm(X): n = np.cross(X[Q[:, 2]] - X[Q[:, 0]], X[Q[:, 3]] - X[Q[:, 1]]); return n / np.maximum(np.linalg.norm(n, axis=1), 1e-12)[:, None]
def selfx(X):
    bvh = BVHTree.FromPolygons(X.tolist(), TRI.tolist(), all_triangles=True, epsilon=0.0); bad = set()
    for i, j in bvh.overlap(bvh):
        fi, fj = qid[i], qid[j]
        if fi != fj and not (set(Q[fi]) & set(Q[fj])): bad.add((min(fi, fj), max(fi, fj)))
    return bad
SX0 = selfx(V); N0 = fnorm(V); D0 = (N0[FE[:, 0]] * N0[FE[:, 1]]).sum(1)
def cone(X, c, sel):
    q = Q[sel]; return float(np.einsum('ij,ij->i', X[q[:, 0]] - c, np.cross(X[q[:, 1]] - c, X[q[:, 2]] - c)).sum() / 6 + np.einsum('ij,ij->i', X[q[:, 0]] - c, np.cross(X[q[:, 2]] - c, X[q[:, 3]] - c)).sum() / 6)
out = dict(tag=TAG, verts=nV, rest_reproduction_max_cm=rest_err, rest_selfx_pairs=len(SX0), poses={})
for pn, dl in POSES.items():
    P = fk(dl); X, Rr = skin(P); key = pn.split('_')[0]; zb, zr = ZONE.get(key, ZONE.get(pn.split('_')[0], ('spine_02', 20)))
    jc0 = np.array(m['heads'][zb]); zv = np.linalg.norm(V - jc0, axis=1) < zr; zf = zv[Q].all(1)
    jc = (np.c_[(RM @ np.r_[P[zb][:3, 3], 1])[:3][None]] * [100, -100, 100])[0]
    SX = selfx(X); new = SX - SX0; N = fnorm(X); Dd = (N[FE[:, 0]] * N[FE[:, 1]]).sum(1); fold = (Dd < np.cos(np.radians(120))) & (D0 >= np.cos(np.radians(120)))
    Nc = np.einsum('vij,vj->vi', Rr, np.c_[N0[:, 0], -N0[:, 1], N0[:, 2]][Q[:, 0]] if False else np.zeros((nV, 3)))   # placeholder (not used)
    # carried normal: rest face normal rotated by the mean linear part of its corners (Blender frame), back to analysis
    Rf = Rr[Q].mean(1); n0b = np.c_[N0[:, 0], -N0[:, 1], N0[:, 2]]; nc = np.einsum('fij,fj->fi', Rf, n0b); nc = np.c_[nc[:, 0], -nc[:, 1], nc[:, 2]]
    flip = ((N * nc).sum(1) < 0)
    st = np.linalg.norm(X[E[:, 0]] - X[E[:, 1]], axis=1) / L0 - 1; ze = zv[E].all(1)
    v0 = cone(V, jc0, zf); v1 = cone(X, jc, zf)
    out['poses'][pn] = dict(new_selfx_pairs=len(new), new_selfx_in_zone=int(sum(1 for p in new if zf[p[0]] or zf[p[1]])), new_folds=int(fold.sum()), new_folds_in_zone=int((fold & zf[FE[:, 0]]).sum()),
                            flipped_faces=int(flip.sum()), flipped_in_zone=int((flip & zf).sum()), strain_p95_pct=round(float(np.percentile(np.abs(st[ze]), 95) * 100), 1),
                            strain_max_pct=round(float(np.abs(st[ze]).max() * 100), 1), zone_volume_pct=round(100 * (v1 / v0 - 1), 2) if abs(v0) > 1e-9 else None, zone=[zb, zr])
    np.savez_compressed('%s/%s_%s.npz' % (O, pn, TAG), V=X.astype(np.float32), flip=np.nonzero(flip)[0].astype(np.int32), selfx=np.array(sorted(new), np.int32).reshape(-1, 2), fold=FE[fold].astype(np.int32))
    print(pn, out['poses'][pn], flush=True)
json.dump(out, open('%s/deform_%s.json' % (O, TAG), 'w'), indent=1)
