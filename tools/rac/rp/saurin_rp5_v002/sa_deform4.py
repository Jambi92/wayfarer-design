# sa_deform4.py CAGE.npz DESIGN.pkl OUT.json : deformation OWNERSHIP, 4 steps per pose (order 236dddc §10). DIAGNOSTIC scaffold only, not a rig.
#   Scaffold: bone segments from the landmark skeleton + digit chains from the cage's own digit rings (finger / thumb / toe ring centroids -> tips);
#   weights w_b ~ exp(-((d_b - d_min) / sigma_b)^2) (sigma 2.5 cm body, 1.2 cm hand / foot, 0.45 cm digits); hierarchical poses.
#   STEP 1 cage + baseline weights.  STEP 2 dense working source (25 % face sample) + the SAME scaffold (rates per 1000 cm^2 for comparability).
#   STEP 3 cage + improved local diagnostic weights (baseline weights heat-diffused 25 x over the cage graph, re-normalised).
#   STEP 4 topology-only fold test: ONE smooth deformation field (the step-3 weights diffused 100 x more, interpolated barycentrically from the cage onto the
#          dense source -> identical field in space; dual-quaternion skinning -> no candy-wrapper) applied to the cage and to the dense source (FULL source
#          resolution, every source face within 2.5 cm of each cage fold). A cage fold is TOPOLOGY-carried only if it lies > 1 cm from every source fold under the
#          same map (the map itself is smooth there, so only the quad layout can fold); folds co-located with source folds belong to the map / scaffold.
#   Weights are region-masked by the authored semantic map (quad labels + side): an arm bone never drives the pelvis / thigh it hangs beside.
#   Flips / folds are measured relative to the rigid motion of each element's dominant bone (a rotated quad is not a flip). fold = normal turned > 90 deg.
#   Classification per pose: CLEAN (step 1 = 0) | WEIGHTING / SCAFFOLD (step 3 or step 4 removes all) | TOPOLOGY (step 4 folds remain) |
#   SOURCE / PD-2 dependence noted when the dense source folds at >= the cage rate in the same pose.
import sys, os, json, pickle, numpy as np, scipy.sparse as sp, scipy.sparse.linalg as spl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_geo as G
CG, DS, OUT = sys.argv[1:4]; z = np.load(CG); Q = z['Q']; Vc = (z['bc'][:, :, None] * G.V[G.F[z['tri']]]).sum(1); L = G.LM; nv = len(Vc)
dsg = pickle.load(open(DS, 'rb')); nm = list(dsg['name'])
def corner(n): return Vc[nm.index(n)]
def cen(prefix): return np.mean([Vc[i] for i, n in enumerate(nm) if n.startswith(prefix + '_') and n[len(prefix) + 1:].isdigit()], 0)
B = {}; PAR = {}; SIG = {}
def bone(n, a, b, par, sig=2.5): B[n] = (np.asarray(a, float), np.asarray(b, float)); PAR[n] = par; SIG[n] = sig
bone('pelvis', L['pelvis_root'], L['spine_lower_axial_107'], None); bone('lumbar', L['spine_lower_axial_107'], L['spine_mid_138'], 'pelvis'); bone('chest', L['spine_mid_138'], L['neck_base'], 'lumbar')
bone('neck', L['neck_base'], L['head_pivot'], 'chest'); bone('head', L['head_pivot'], L['rostrum_tip'], 'neck'); bone('jaw', (L['jaw_hinge_xpos'] + L['jaw_hinge_xneg']) / 2, L['rostrum_tip'] - [0, 0, 1.5], 'head')
bone('tailroot', L['tail_root_centre'], L['tail_chain_04'], 'pelvis'); bone('tailmid', L['tail_chain_04'], L['tail_chain_10'], 'tailroot'); bone('taildist', L['tail_chain_10'], L['tail_tip'], 'tailmid')
DIG = {}
for s in ('xpos', 'xneg'):
    bone('upperarm_' + s, L['glenohumeral_' + s], L['elbow_' + s], 'chest'); bone('forearm_' + s, L['elbow_' + s], L['wrist_' + s], 'upperarm_' + s)
    tips = np.array([L['hand_tip%d_' % k + s] for k in range(1, 6)]); bone('hand_' + s, L['wrist_' + s], tips.mean(0), 'forearm_' + s, 1.2)
    bone('thigh_' + s, L['hip_' + s], L['knee_' + s], 'pelvis'); bone('shin_' + s, L['knee_' + s], L['ankle_' + s], 'thigh_' + s)
    ttips = np.array([L['toe_tip%d_' % k + s] for k in range(1, 6)]); bone('foot_' + s, L['ankle_' + s], L['ball_line_' + s], 'shin_' + s, 1.2)
    pal = np.mean([corner('%s_f%d_P%s' % (s, k, c)) for k in range(1, 5) for c in 'RU'], 0) - np.mean([corner('%s_f%d_D%s' % (s, k, c)) for k in range(1, 5) for c in 'RU'], 0); pal /= np.linalg.norm(pal)
    for k in range(1, 5):
        b0 = np.mean([corner('%s_f%d_%s' % (s, k, c)) for c in ('DR', 'DU', 'PR', 'PU')], 0); r1 = cen('%s_f%d_r1' % (s, k)); r2 = cen('%s_f%d_r2' % (s, k)); tp = tips[np.argmin(np.linalg.norm(tips - r2, axis=1))]
        bone('f%d_1_%s' % (k, s), b0, r1, 'hand_' + s, 0.45); bone('f%d_2_%s' % (k, s), r1, r2, 'f%d_1_%s' % (k, s), 0.45); bone('f%d_3_%s' % (k, s), r2, tp, 'f%d_2_%s' % (k, s), 0.45)
        DIG['f%d_%s' % (k, s)] = pal
    r1 = cen('%s_th_r1' % s); r2 = cen('%s_th_r2' % s); tp = tips[np.argmin(np.linalg.norm(tips - r2, axis=1))]; b0 = r1 - (r2 - r1)
    bone('th_1_' + s, b0, r1, 'hand_' + s, 0.6); bone('th_2_' + s, r1, r2, 'th_1_' + s, 0.45); bone('th_3_' + s, r2, tp, 'th_2_' + s, 0.45); DIG['th_' + s] = pal
    for k in range(1, 6):
        r1 = cen('%s_t%d_r1' % (s, k)); r2 = cen('%s_t%d_r2' % (s, k)); tp = ttips[np.argmin(np.linalg.norm(ttips - r2, axis=1))]; b0 = np.mean([corner('%s_t%d_%s' % (s, k, c)) for c in ('DL', 'DM', 'PL', 'PM')], 0)
        bone('t%d_1_%s' % (k, s), b0, r1, 'foot_' + s, 0.45); bone('t%d_2_%s' % (k, s), r1, tp, 't%d_1_%s' % (k, s), 0.45)
names = list(B); IDX = {n: i for i, n in enumerate(names)}
QL = z['qlab'].astype(str); QLU = sorted(set(QL)); qli = {q: i for i, q in enumerate(QLU)}
VL = np.zeros((nv, len(QLU)), bool); VL[Q.ravel(), np.repeat([qli[q] for q in QL], 4)] = True          # vertex -> qlabs of its incident quads (authored semantic map)
def allowed(b):
    sd = b.split('_')[-1] if b.split('_')[-1] in ('xpos', 'xneg') else None
    if b.startswith('upperarm'): S = {'shoulder', 'upper_arm', 'elbow'}
    elif b.startswith('forearm'): S = {'elbow', 'forearm', 'wrist'}
    elif b.startswith('hand'): S = {'wrist', 'palm', 'thumb', 'finger_web', 'finger'}
    elif (b[0] == 'f' and b[1].isdigit()) or b.startswith('th_'): S = {'palm', 'finger', 'finger_cap', 'finger_web', 'thumb', 'thumb_cap'}
    elif b.startswith('thigh'): S = {'hip', 'thigh', 'knee', 'pelvis'}
    elif b.startswith('shin'): S = {'knee', 'shin', 'ankle'}
    elif b.startswith('foot'): S = {'ankle', 'foot', 'forefoot', 'toe_web', 'toe'}
    elif b[0] == 't' and b[1].isdigit(): S = {'forefoot', 'toe', 'toe_cap', 'toe_web'}
    elif b in ('pelvis', 'lumbar'): S = {'trunk', 'pelvis', 'hip', 'shoulder', 'neck', 'tail'}
    elif b == 'chest': S = {'trunk', 'neck', 'shoulder'}
    elif b in ('neck', 'head', 'jaw'): S = {'neck', 'head', 'rostrum_cap', 'orbit', 'eye', 'display_root', 'trunk'}
    elif b.startswith('tail'): S = {'tail', 'pelvis'}
    return [qli[q] for q in S if q in qli], sd
MASKL = [allowed(b) for b in names]
from scipy.spatial import cKDTree
_kdc = cKDTree(Vc)
def labels_of(P): return _kdc.query(P)[1]                    # nearest cage vertex (its authored label set and side)
def kids(n): out = [n]; [out.extend(kids(c)) for c in names if PAR[c] == n]; return out
def weights(P, sigmul=1.0, lab=None):
    lab = labels_of(P) if lab is None else lab
    D = []
    for b in names:
        a, c = B[b]; t = np.clip(((P - a) @ (c - a)) / max((c - a) @ (c - a), 1e-9), 0, 1); D.append(np.linalg.norm(P - (a + t[:, None] * (c - a)), axis=1))
    D = np.stack(D, 1); xs = Vc[lab, 0]
    ok = np.stack([VL[lab][:, li].any(1) & (True if sd is None else ((xs > 0) if sd == 'xpos' else (xs < 0))) for li, sd in MASKL], 1); ok[~ok.any(1)] = True
    D = np.where(ok, D, 1e6); sg = sigmul * np.array([SIG[b] for b in names]); w = np.exp(-((D - D.min(1, keepdims=True)) / sg) ** 2) * ok
    return w / w.sum(1, keepdims=True)
def rot(axis, deg):
    a = np.asarray(axis, float); a /= np.linalg.norm(a); t = np.radians(deg); K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]]); return np.eye(3) + np.sin(t) * K + (1 - np.cos(t)) * K @ K
def pose(spec):
    T = {b: (np.eye(3), np.zeros(3)) for b in names}
    for bn, piv, ax, deg in spec:                      # applied in order; pivots / axes are in the CURRENT (already posed) frame of the parent
        R0p, t0p = T[bn]; piv = R0p @ np.asarray(piv, float) + t0p; ax = R0p @ np.asarray(ax, float); Rm = rot(ax, deg)
        for k in kids(bn): R0, t0 = T[k]; T[k] = (Rm @ R0, Rm @ (t0 - piv) + piv)
    return T
def skin(P, W, T):
    out = np.zeros_like(P)
    for i, b in enumerate(names):
        if W[:, i].max() < 1e-6: continue
        R0, t0 = T[b]; out += W[:, i:i + 1] * (P @ R0.T + t0)
    return out
X, Y, Zz = np.eye(3)
def digit_flex(s, k, degs, which='f'):
    pal = DIG['%s%s_%s' % (which, k, s)] if which == 'f' else DIG['th_' + s]; out = []
    for j, dg in enumerate(degs, 1):
        bn = '%s%s_%d_%s' % (which, k, j, s) if which == 'f' else 'th_%d_%s' % (j, s); a, c = B[bn]; ax = np.cross(c - a, pal); out.append((bn, a, ax, dg))
    return out
POSES = {'jaw_open_20': [('jaw', (L['jaw_hinge_xpos'] + L['jaw_hinge_xneg']) / 2, X, 20)], 'neck_flex_30': [('neck', L['neck_base'], X, 30)], 'neck_rot_40': [('neck', L['neck_base'], Zz, 40)]}
for s, sg in (('xpos', 1), ('xneg', -1)):
    S, E_, Wr, H, K, A = L['glenohumeral_' + s], L['elbow_' + s], L['wrist_' + s], L['hip_' + s], L['knee_' + s], L['ankle_' + s]
    POSES.update({'shoulder_abd45_' + s: [('upperarm_' + s, S, Y, -sg * 45)], 'shoulder_abd90_' + s: [('upperarm_' + s, S, Y, -sg * 90)], 'shoulder_flex60_' + s: [('upperarm_' + s, S, X, -60)],
                  'elbow_90_' + s: [('forearm_' + s, E_, X, -90)], 'elbow_130_' + s: [('forearm_' + s, E_, X, -130)], 'hip_flex70_' + s: [('thigh_' + s, H, X, -70)],
                  'knee_90_' + s: [('shin_' + s, K, X, 90)], 'ankle_dorsi20_' + s: [('foot_' + s, A, X, -20)]})
    fist = sum([digit_flex(s, k, (75, 95, 60)) for k in range(1, 5)], []) + digit_flex(s, '', (35, 30, 25), 'th')
    grasp = sum([digit_flex(s, k, (40, 50, 30)) for k in range(1, 5)], []) + digit_flex(s, '', (25, 20, 15), 'th')
    hl = B['hand_' + s][1] - B['hand_' + s][0]
    opp = [('th_1_' + s, B['th_1_' + s][0], hl, -sg * 50)] + digit_flex(s, '', (30, 25, 20), 'th')
    POSES.update({'fist_' + s: fist, 'grasp_' + s: grasp, 'thumb_opposition_' + s: opp,
                  'toe_flex30_' + s: [('t%d_1_%s' % (k, s), B['t%d_1_%s' % (k, s)][0], np.cross(B['t%d_1_%s' % (k, s)][1] - B['t%d_1_%s' % (k, s)][0], [0, 0, -1]), 30) for k in range(1, 6)],
                  'toe_ext30_' + s: [('t%d_1_%s' % (k, s), B['t%d_1_%s' % (k, s)][0], np.cross(B['t%d_1_%s' % (k, s)][1] - B['t%d_1_%s' % (k, s)][0], [0, 0, -1]), -30) for k in range(1, 6)]})
POSES.update({'trunk_twist_30': [('lumbar', L['spine_lower_axial_107'], Zz, 30)], 'lower_axial_flex_25': [('lumbar', L['spine_lower_axial_107'], X, 25)],
              'tail_root_lateral_30': [('tailroot', L['tail_root_centre'], Zz, 30)], 'tail_root_vertical_25': [('tailroot', L['tail_root_centre'], X, 25)],
              'tail_twist_30': [('tailroot', L['tail_root_centre'], L['tail_chain_04'] - L['tail_root_centre'], 30)]})
if os.environ.get('POSES'): POSES = {k: v for k, v in POSES.items() if any(p in k for p in os.environ['POSES'].split(','))}
E = np.unique(np.sort(np.r_[Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]], 1), axis=0)
Ad = sp.coo_matrix((np.ones(2 * len(E)), (np.r_[E[:, 0], E[:, 1]], np.r_[E[:, 1], E[:, 0]])), shape=(nv, nv)).tocsr(); deg = np.asarray(Ad.sum(1)).ravel()
Wc = weights(Vc); W3 = Wc.copy()
for _ in range(25): W3 = 0.5 * W3 + 0.5 * (Ad @ W3) / deg[:, None]
W3 /= W3.sum(1, keepdims=True)
Wc4 = W3.copy()
for _ in range(100): Wc4 = 0.5 * Wc4 + 0.5 * (Ad @ Wc4) / deg[:, None]
Wc4 /= Wc4.sum(1, keepdims=True)
rng = np.random.default_rng(0); Fs = G.F[rng.random(len(G.F)) < 0.25]; us = np.unique(Fs); mp = -np.ones(G.NV, int); mp[us] = np.arange(len(us)); Fs = mp[Fs]; Vs = G.V[us]; lab_s = labels_of(Vs); Ws = weights(Vs, 1.0, lab_s); _kdsrc = cKDTree(G.V)
import igl as _igl
_Tc = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]; _, _ti, _cp = _igl.point_mesh_squared_distance(Vs, Vc, _Tc)
_a, _b, _c = Vc[_Tc[_ti, 0]], Vc[_Tc[_ti, 1]], Vc[_Tc[_ti, 2]]; _bc = _igl.barycentric_coordinates(_cp, _a, _b, _c) if hasattr(_igl, 'barycentric_coordinates') else None
if _bc is None or np.ndim(_bc) != 2:
    v0 = _b - _a; v1 = _c - _a; v2 = _cp - _a; d00 = (v0 * v0).sum(1); d01 = (v0 * v1).sum(1); d11 = (v1 * v1).sum(1); d20 = (v2 * v0).sum(1); d21 = (v2 * v1).sum(1); dn = d00 * d11 - d01 * d01
    bb = (d11 * d20 - d01 * d21) / dn; cc_ = (d00 * d21 - d01 * d20) / dn; _bc = np.c_[1 - bb - cc_, bb, cc_]
Ws4 = np.einsum('sk,skb->sb', _bc, Wc4[_Tc[_ti]])                     # the SAME smooth field, interpolated from the cage onto the dense source
def qn(P): return np.cross(P[Q[:, 2]] - P[Q[:, 0]], P[Q[:, 3]] - P[Q[:, 1]])
def tn(P): return np.cross(P[Fs[:, 1]] - P[Fs[:, 0]], P[Fs[:, 2]] - P[Fs[:, 0]])
n0c = qn(Vc); n0s = tn(Vs); qa = 0.5 * np.linalg.norm(n0c, axis=1); sa = 0.5 * np.linalg.norm(n0s, axis=1) / 0.25
def relcos(n0, n1, W, el, T):
    dom = W[el].mean(1).argmax(1); Rq = np.stack([T[names[b]][0] for b in range(len(names))])[dom]; n0r = np.einsum('qij,qj->qi', Rq, n0)
    return (n0r * n1).sum(1) / (np.linalg.norm(n0r, axis=1) * np.linalg.norm(n1, axis=1) + 1e-12)
def qmul(a, b):
    w1, x1, y1, z1 = a[..., 0], a[..., 1], a[..., 2], a[..., 3]; w2, x2, y2, z2 = b[..., 0], b[..., 1], b[..., 2], b[..., 3]
    return np.stack([w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2, w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2, w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2, w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2], -1)
def r2q(R):
    w = np.sqrt(max(1e-12, 1 + R[0, 0] + R[1, 1] + R[2, 2])) / 2
    if w > 1e-3: return np.array([w, (R[2, 1] - R[1, 2]) / (4 * w), (R[0, 2] - R[2, 0]) / (4 * w), (R[1, 0] - R[0, 1]) / (4 * w)])
    import scipy.spatial.transform as st; x, y, zq, ww = st.Rotation.from_matrix(R).as_quat(); return np.array([ww, x, y, zq])
def dqs(P, W, T):
    q0 = np.stack([r2q(T[b][0]) for b in names]); te = np.stack([np.r_[0, T[b][1]] for b in names]); qe = 0.5 * qmul(te, q0)
    sgn = np.sign((q0 * q0[IDX['pelvis']]).sum(1) + 1e-12)[:, None]; q0 = q0 * sgn; qe = qe * sgn
    b0 = W @ q0; be = W @ qe; n = np.linalg.norm(b0, axis=1, keepdims=True); b0 /= n; be /= n
    w, v = b0[:, :1], b0[:, 1:]; t = 2 * (w * be[:, 1:] - be[:, :1] * v + np.cross(v, be[:, 1:]))
    Pr = P + 2 * np.cross(v, np.cross(v, P) + w * P); return Pr + t
lap0 = Vc - (Ad @ Vc) / deg[:, None]
def topo_test(Pc, bad, T, W):
    m = np.zeros(nv, bool); m[Q[bad].ravel()] = True
    for _ in range(3): m |= (Ad @ m.astype(float)) > 0
    inner = m.copy(); bnd = m & ((Ad @ (~m).astype(float)) > 0); inner &= ~bnd; ii = np.nonzero(inner)[0]
    if not len(ii): return 0
    Rb = np.stack([T[b][0] for b in names]); Rv = np.einsum('vb,bij->vij', W[ii], Rb); U, _, Vt = np.linalg.svd(Rv); Rv = U @ Vt
    tgt = np.einsum('vij,vj->vi', Rv, lap0[ii]); loc = -np.ones(nv, int); loc[ii] = np.arange(len(ii))
    Lm = (sp.eye(nv) - sp.diags(1 / deg) @ Ad).tocsr(); Lii = Lm[ii][:, ii]; Lib = Lm[ii][:, ~inner]
    rhs = tgt - Lib @ Pc[~inner]; X_ = np.stack([spl.spsolve(Lii.tocsc(), rhs[:, k]) for k in range(3)], 1); P2 = Pc.copy(); P2[ii] = X_
    qm = m[Q].all(1); c = relcos(n0c[qm], qn(P2)[qm], W, Q[qm], T); return int((c < 0).sum())
res = {}
for pn, spec in POSES.items():
    T = pose(spec)
    P1 = skin(Vc, Wc, T); c1 = relcos(n0c, qn(P1), Wc, Q, T); f1 = np.nonzero(c1 < 0)[0]
    Ps = skin(Vs, Ws, T); cs = relcos(n0s, tn(Ps), Ws, Fs, T); fs = cs < 0
    P3 = skin(Vc, W3, T); c3 = relcos(n0c, qn(P3), W3, Q, T); f3 = np.nonzero(c3 < 0)[0]
    if len(f3):
        P4 = dqs(Vc, Wc4, T); c4 = relcos(n0c, qn(P4), Wc4, Q, T); f4 = np.nonzero(c4 < 0)[0]
        Ps4 = dqs(Vs, Ws4, T); cs4 = relcos(n0s, tn(Ps4), Ws4, Fs, T); fs4 = np.nonzero(cs4 < 0)[0]
        tq4 = f4
        if len(f4):
            # FULL-resolution source check around each cage fold (all source faces within 2.5 cm; same field interpolated from the cage)
            cen4 = Vc[Q[f4]].mean(1); sv = np.unique(np.concatenate(_kdsrc.query_ball_point(cen4, 2.5))); fm = np.isin(G.F, sv).all(1); Ff = G.F[fm]
            loc = -np.ones(G.NV, int); loc[sv] = np.arange(len(sv)); Ffl = loc[Ff]; Pv = G.V[sv]
            _, ti_, cp_ = _igl.point_mesh_squared_distance(Pv, Vc, _Tc); a_, b_, c_ = Vc[_Tc[ti_, 0]], Vc[_Tc[ti_, 1]], Vc[_Tc[ti_, 2]]
            v0 = b_ - a_; v1 = c_ - a_; v2 = cp_ - a_; d00 = (v0 * v0).sum(1); d01 = (v0 * v1).sum(1); d11 = (v1 * v1).sum(1); d20 = (v2 * v0).sum(1); d21 = (v2 * v1).sum(1); dn = d00 * d11 - d01 * d01
            bb = (d11 * d20 - d01 * d21) / dn; cc_ = (d00 * d21 - d01 * d20) / dn; bcs = np.c_[1 - bb - cc_, bb, cc_]; Wf = np.einsum('sk,skb->sb', bcs, Wc4[_Tc[ti_]])
            n0f = np.cross(Pv[Ffl[:, 1]] - Pv[Ffl[:, 0]], Pv[Ffl[:, 2]] - Pv[Ffl[:, 0]]); Pf = dqs(Pv, Wf, T); n1f = np.cross(Pf[Ffl[:, 1]] - Pf[Ffl[:, 0]], Pf[Ffl[:, 2]] - Pf[Ffl[:, 0]])
            cf = relcos(n0f, n1f, Wf, Ffl, T); ff = np.nonzero(cf < 0)[0]
            if len(ff):
                kd4 = cKDTree(Pf[Ffl[ff]].mean(1)); dd4, _ = kd4.query(P4[Q[f4]].mean(1)); tq4 = f4[dd4 > 1.0]
        t4 = int(len(tq4)); n4c, n4s = int(len(f4)), int(len(fs4))
        sd4 = np.linalg.norm(np.roll(Vc[Q[tq4]], -1, 1) - Vc[Q[tq4]], axis=2); t4where = [(str(z['qlab'][q]), np.round(Vc[Q[q]].mean(0), 1).tolist(), round(float(a), 2)) for q, a in zip(tq4, sd4.max(1) / sd4.min(1))][:12]
    else: t4 = 0; n4c = n4s = 0; t4where = []
    rate_c = 1000 * qa[f1].sum() / qa.sum() * 100; rate_s = 1000 * sa[fs].sum() / sa.sum() * 100           # per mille of surface area (x100 -> per 1000 cm2 proxy)
    regs = sorted({str(z['qlab'][q]) for q in f1})[:8]
    cls = 'CLEAN' if not len(f1) else ('WEIGHTING / SCAFFOLD' if (not len(f3) or t4 == 0) else 'TOPOLOGY')
    src = bool(fs.sum() and rate_s >= rate_c)
    res[pn] = dict(step1_cage_flips=int(len(f1)), step1_flip_area_permille=round(float(1000 * qa[f1].sum() / qa.sum()), 4), step2_source_flips_sampled=int(fs.sum()),
                   step2_source_flip_area_permille=round(float(1000 * sa[fs].sum() / sa.sum()), 4), step3_cage_flips_improved_weights=int(len(f3)), step4_topology_only_flips=int(t4), step4_smooth_map_cage_flips=n4c, step4_smooth_map_source_flips=n4s, step4_topology_quads=t4where,
                   regions=regs, classification=cls + (' (+ SOURCE / PD-2 dependence: dense source folds at >= cage rate)' if src else ''))
    print(pn, res[pn], flush=True)
json.dump(dict(scaffold='temporary LBS diagnostic; landmark segments + cage digit-ring chains; NOT a rig', bones=len(names), poses=res), open(OUT, 'w'), indent=1)
