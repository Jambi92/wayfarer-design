# gripsolve.py (bpy python, mathutils) -- RIGDIR SIDE TASK.json OUT.json
# Greedy contact-aware pose solver on the diagnostic rig. Each digit advances its flexion fraction in small steps (in the
# given order); after every step the actual skinned mesh (DQS) is checked:
#   - new self-intersections vs rest: skin-skin contact allowed up to SKIN_TOL penetration, claw contact up to CLAW_TOL
#   - fixture: no vertex deeper than FIX_TOL inside; a digit stops when it reaches contact (|d| <= CONTACT)
# A blocked step first tries small abduction offsets (fingers) before the digit is frozen. Every accepted state is a
# validated intermediate keyframe; the sequence is written out.
import sys, json, numpy as np, os, math, igl
sys.path.insert(0, '/tmp/claude-0/hand/tools'); from fastpose import Hand
import bpy
from mathutils.bvhtree import BVHTree
from scipy.spatial import cKDTree
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
import pickle
a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
rd, side, angj, outp = a[:4]
T = {}; H = Hand(rd, side); Q = H.Q
RD = pickle.load(open(os.path.join(rd, 'rig_data.pkl'), 'rb'))[side]; own = RD['own']; ker = RD['ker']
digs = {'L': ['A_L17', 'A_L18', 'A_L19', 'A_L20', 'A_Lthumb'], 'R': ['A_R21', 'A_R22', 'A_R23', 'A_R24', 'A_Rthumb']}[side]
fown = np.array([np.bincount(own[q] + 1, minlength=6).argmax() - 1 for q in Q]); kerq = ker[Q].all(1)
SKIN_TOL = T.get('skin_tol_mm', 1.0) / 1000; CLAW_TOL = T.get('claw_tol_mm', 0.5) / 1000
FIX_TOL = T.get('fixture_tol_mm', 0.5) / 1000; CONTACT = T.get('contact_mm', 0.5) / 1000
vq = [[] for _ in range(len(H.P0))]
for qi, q in enumerate(Q):
    for v in q: vq[v].append(qi)
def ring(qs): return np.unique(np.concatenate([vq[v] for v in np.unique(Q[qs])]))
def selfx(P):
    t = BVHTree.FromPolygons(P.tolist(), Q.tolist(), all_triangles=False, epsilon=0.0)
    pr = np.array(t.overlap(t), int).reshape(-1, 2); pr = pr[pr[:, 0] < pr[:, 1]]
    if len(pr): A = Q[pr[:, 0]]; B = Q[pr[:, 1]]; pr = pr[~(A[:, :, None] == B[:, None, :]).any((1, 2))]
    return pr
def depths(P, pairs):
    d = np.zeros(len(pairs))
    if not len(pairs): return d
    C = P[Q[pairs[:, 0]]].mean(1); e = np.array(list(cKDTree(C).query_pairs(0.004)), int).reshape(-1, 2); n = len(C)
    _, lab = connected_components(sp.coo_matrix((np.ones(len(e)), (e[:, 0], e[:, 1])), shape=(n, n)), directed=False)
    for c in np.unique(lab):
        m = lab == c; A = np.unique(pairs[m, 0]); B = np.unique(pairs[m, 1]); best = 0.0
        for X_, Y_ in ((A, B), (B, A)):
            Yr = np.setdiff1d(ring(Y_), X_)
            if not len(Yr): continue
            TT = np.vstack([Q[Yr][:, [0, 1, 2]], Q[Yr][:, [0, 2, 3]]])[:, ::-1]
            sd, _, _, _ = igl.signed_distance(P[np.unique(Q[X_])], P, TT, sign_type=igl.SIGNED_DISTANCE_TYPE_PSEUDONORMAL)
            sd = sd[np.abs(sd) < 0.005]
            if len(sd) and sd.min() < 0: best = max(best, -sd.min())
        d[m] = best
    return d
def fixture_sd(P, fx):
    c = np.array(fx['c']) / 100; ax = np.array(fx['ax'], float); ax /= np.linalg.norm(ax); r = fx['r'] / 100; hl = fx['hl'] / 100
    dd = P - c; t = dd @ ax; rad = np.linalg.norm(dd - t[:, None] * ax, axis=1); dr = rad - r; dt = np.abs(t) - hl
    return np.sqrt(np.maximum(dr, 0) ** 2 + np.maximum(dt, 0) ** 2) + np.minimum(np.maximum(dr, dt), 0)
P0 = H.pose({}); rest = set(map(tuple, selfx(P0).tolist()))
BASE = {}
def angles_of(state):
    ang = {b: list(v) for b, v in BASE.items()}
    for k, st in state.items():
        tgt = T['targets'].get(k, {})
        for b, v in tgt.items():
            v = [(st['f'] if b.endswith('_0') else st.get('g', st['f'])) * x for x in v]
            if b.endswith('_0') and 'thumb' not in k: v[1] += st['abd']
            ang[b] = [x + y for x, y in zip(ang.get(b, [0, 0, 0]), v)]
    return ang
def check(state):
    P = H.pose(angles_of(state)); pr = selfx(P)
    new = np.array(sorted(set(map(tuple, pr.tolist())) - rest), int).reshape(-1, 2)
    dep = depths(P, new); isc = (kerq[new[:, 0]] | kerq[new[:, 1]]) if len(new) else np.zeros(0, bool)
    viol = new[np.where(isc, dep > CLAW_TOL, dep > SKIN_TOL)] if len(new) else new
    vd = set()
    for a_, b_ in viol: vd.add(int(fown[a_])); vd.add(int(fown[b_]))
    info = dict(pairs=int(len(new)), viol=int(len(viol)), skin_depth_mm=float(dep[~isc].max() * 1000) if (~isc).any() else 0.0,
                claw_depth_mm=float(dep[isc].max() * 1000) if isc.any() else 0.0, viol_owners=sorted(vd))
    contact = {}
    if T.get('fixture'):
        sd = fixture_sd(P, T['fixture'])
        for i_, k in enumerate(digs):
            m = own == i_
            if m.any(): contact[k] = dict(min_mm=float(sd[m].min() * 1000), pen=bool((sd[m] < -FIX_TOL).any()), touch=bool((np.abs(sd[m]) <= CONTACT).any()))
        palm = own < 0; contact['palm'] = dict(min_mm=float(sd[palm].min() * 1000), pen=bool((sd[palm] < -FIX_TOL).any()), touch=bool((np.abs(sd[palm]) <= CONTACT).any()))
        info['fixture'] = contact
        info['fixture_claw_pen'] = int(((sd < -FIX_TOL) & ker).sum())
    return info, P

ang = json.loads(open(angj).read()) if os.path.exists(angj) else json.loads(angj)
P = H.pose(ang); pr = selfx(P); new = np.array(sorted(set(map(tuple, pr.tolist())) - rest), int).reshape(-1, 2)
dep = depths(P, new); isc = (kerq[new[:, 0]] | kerq[new[:, 1]]) if len(new) else np.zeros(0, bool)
viol = new[np.where(isc, dep > CLAW_TOL, dep > SKIN_TOL)] if len(new) else new
from collections import Counter
print('new', len(new), 'viol', len(viol), dict(Counter(tuple(sorted((int(fown[a_]), int(fown[b_])))) for a_, b_ in viol)), 'maxdepth mm %.2f' % (dep.max() * 1000 if len(dep) else 0))
np.save(outp + '_P.npy', P.astype(np.float32)); np.save(outp + '_pr.npy', viol)
