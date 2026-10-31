# sa_fc_deform.py CAGE.npz OUT.json : RP5 full-cage DIAGNOSTIC deformation pilot (order ad9cb85 §21) -- temporary scaffold only, not a rig.
# Bones from the landmark skeleton (segments); weights w_b ~ exp(-(d_b / 2.5 cm)^2) of the distance to each bone segment, normalized (cage and dense
# source get the SAME scaffold); poses rotate the distal chain about the joint. Per pose: flipped quads (normal reversal vs rest), folded quads (normal
# turned > 120 deg vs rest), edge strain p95 -- cage vs the dense working source (ownership: issue on the source too = source-deformation dependency).
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_geo as G
CG, OUT = sys.argv[1:3]; z = np.load(CG); Q = z['Q']; fi, bc = z['tri'], z['bc']; Vc = (bc[:, :, None] * G.V[G.F[fi]]).sum(1); L = G.LM
def seg(a, b): return (np.asarray(a, float), np.asarray(b, float))
B = {}
for s in ('xpos', 'xneg'):
    B['upperarm_' + s] = seg(L['glenohumeral_' + s], L['elbow_' + s]); B['forearm_' + s] = seg(L['elbow_' + s], L['wrist_' + s])
    B['hand_' + s] = seg(L['wrist_' + s], np.mean([L['hand_tip%d_' % k + s] for k in range(1, 6)], 0))
    B['thigh_' + s] = seg(L['hip_' + s], L['knee_' + s]); B['shin_' + s] = seg(L['knee_' + s], L['ankle_' + s]); B['foot_' + s] = seg(L['ankle_' + s], L['ball_line_' + s])
B['pelvis'] = seg(L['pelvis_root'], L['spine_lower_axial_107']); B['lumbar'] = seg(L['spine_lower_axial_107'], L['spine_mid_138']); B['chest'] = seg(L['spine_mid_138'], L['neck_base'])
B['neck'] = seg(L['neck_base'], L['head_pivot']); B['head'] = seg(L['head_pivot'], L['rostrum_tip']); B['jaw'] = seg((L['jaw_hinge_xpos'] + L['jaw_hinge_xneg']) / 2, L['rostrum_tip'] - [0, 0, 1.5])
B['tailroot'] = seg(L['tail_root_centre'], L['tail_chain_04']); B['tailmid'] = seg(L['tail_chain_04'], L['tail_chain_10']); B['taildist'] = seg(L['tail_chain_10'], L['tail_tip'])
names = list(B)
def weights(P):
    D = []
    for b in names:
        a, c = B[b]; t = np.clip(((P - a) @ (c - a)) / ((c - a) @ (c - a)), 0, 1); D.append(np.linalg.norm(P - (a + t[:, None] * (c - a)), axis=1))
    D = np.stack(D, 1); w = np.exp(-((D - D.min(1, keepdims=True)) / 2.5) ** 2); w[D.argmin(1)[:, None] == np.arange(len(names))] += 1e-9
    return w / w.sum(1, keepdims=True)
CHILD = {'upperarm': ['forearm', 'hand'], 'forearm': ['hand'], 'thigh': ['shin', 'foot'], 'shin': ['foot'], 'lumbar': ['chest', 'neck', 'head', 'jaw'] + ['upperarm_xpos', 'forearm_xpos', 'hand_xpos', 'upperarm_xneg', 'forearm_xneg', 'hand_xneg'],
         'neck': ['head', 'jaw'], 'tailroot': ['tailmid', 'taildist'], 'tailmid': ['taildist']}
def rot(axis, deg):
    a = np.asarray(axis, float); a /= np.linalg.norm(a); t = np.radians(deg); K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]]); return np.eye(3) + np.sin(t) * K + (1 - np.cos(t)) * K @ K
def pose(spec):
    """spec: list of (bone, pivot, axis, deg); returns per-bone rigid (R, t) composed along the chain"""
    T = {b: (np.eye(3), np.zeros(3)) for b in names}
    for bone, piv, ax, deg in spec:
        Rm = rot(ax, deg); piv = np.asarray(piv, float); s = bone.split('_')[-1] if '_' in bone else ''
        kids = [bone] + [c + ('_' + s if s and c in ('forearm', 'hand', 'shin', 'foot') else '') for c in CHILD.get(bone.split('_')[0] if s else bone, [])]
        for k in kids:
            if k not in T: continue
            R0, t0 = T[k]; T[k] = (Rm @ R0, Rm @ (t0 - piv) + piv)
    return T
def skin(P, W, T):
    out = np.zeros_like(P)
    for i, b in enumerate(names):
        R0, t0 = T[b]; out += W[:, i:i + 1] * (P @ R0.T + t0)
    return out
X, Y, Zz = np.eye(3)
POSES = {'jaw_open_20': [('jaw', (L['jaw_hinge_xpos'] + L['jaw_hinge_xneg']) / 2, X, 20)], 'neck_flex_30': [('neck', L['neck_base'], X, 30)], 'neck_rot_40': [('neck', L['neck_base'], Zz, 40)]}
for s, sg in (('xpos', 1), ('xneg', -1)):
    S, E_, Wr, H, K, A = L['glenohumeral_' + s], L['elbow_' + s], L['wrist_' + s], L['hip_' + s], L['knee_' + s], L['ankle_' + s]
    POSES.update({'shoulder_abd45_' + s: [('upperarm_' + s, S, Y, -sg * 45)], 'shoulder_abd90_' + s: [('upperarm_' + s, S, Y, -sg * 90)], 'shoulder_flex60_' + s: [('upperarm_' + s, S, X, -60)],
                  'elbow_90_' + s: [('forearm_' + s, E_, X, -90)], 'elbow_130_' + s: [('forearm_' + s, E_, X, -130)], 'wrist_flex50_' + s: [('hand_' + s, Wr, Y, sg * 50)], 'wrist_ext40_' + s: [('hand_' + s, Wr, Y, -sg * 40)],
                  'hip_flex70_' + s: [('thigh_' + s, H, X, -70)], 'knee_90_' + s: [('shin_' + s, K, X, 90)], 'knee_deep130_' + s: [('shin_' + s, K, X, 130)], 'ankle_dorsi20_' + s: [('foot_' + s, A, X, -20)]})
POSES.update({'trunk_twist_30': [('lumbar', L['spine_lower_axial_107'], Zz, 30)], 'lower_axial_flex_25': [('lumbar', L['spine_lower_axial_107'], X, 25)],
              'tail_root_lateral_30': [('tailroot', L['tail_root_centre'], Zz, 30)], 'tail_root_vertical_25': [('tailroot', L['tail_root_centre'], X, 25)],
              'tail_mid_bend_40': [('tailmid', L['tail_chain_04'], Zz, 40)], 'tail_twist_30': [('tailroot', L['tail_root_centre'], G.LM['tail_chain_04'] - G.LM['tail_root_centre'], 30)]})
def quad_normals(P, Qq): return np.cross(P[Qq[:, 2]] - P[Qq[:, 0]], P[Qq[:, 3]] - P[Qq[:, 1]])
def tri_normals(P, Ff): return np.cross(P[Ff[:, 1]] - P[Ff[:, 0]], P[Ff[:, 2]] - P[Ff[:, 0]])
Wc = weights(Vc); rng = np.random.default_rng(0)
Fs = G.F[rng.random(len(G.F)) < 0.25]; us = np.unique(Fs); mp = -np.ones(G.NV, int); mp[us] = np.arange(len(us)); Fs = mp[Fs]; Vs = G.V[us]; Ws = weights(Vs)
n0c = quad_normals(Vc, Q); n0s = tri_normals(Vs, Fs); E = np.unique(np.sort(np.r_[Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]], 1), axis=0); l0 = np.linalg.norm(Vc[E[:, 0]] - Vc[E[:, 1]], axis=1)
res = {}
for nm, spec in POSES.items():
    T = pose(spec); Pc = skin(Vc, Wc, T); Ps = skin(Vs, Ws, T); n1c = quad_normals(Pc, Q); n1s = tri_normals(Vs * 0 + Ps, Fs)
    cc = (n0c * n1c).sum(1) / (np.linalg.norm(n0c, axis=1) * np.linalg.norm(n1c, axis=1) + 1e-12); cs = (n0s * n1s).sum(1) / (np.linalg.norm(n0s, axis=1) * np.linalg.norm(n1s, axis=1) + 1e-12)
    # flips / folds measured relative to the rigid motion of the quad's dominant bone (a rotated quad is not a flip)
    dom = Wc[Q].mean(1).argmax(1); Rq = np.stack([T[names[b]][0] for b in dom]); n0r = np.einsum('qij,qj->qi', Rq, n0c); cr = (n0r * n1c).sum(1) / (np.linalg.norm(n0r, axis=1) * np.linalg.norm(n1c, axis=1) + 1e-12)
    doms = Ws[Fs].mean(1).argmax(1); Rs = np.stack([T[names[b]][0] for b in doms]); n0sr = np.einsum('qij,qj->qi', Rs, n0s); csr = (n0sr * n1s).sum(1) / (np.linalg.norm(n0sr, axis=1) * np.linalg.norm(n1s, axis=1) + 1e-12)
    l1 = np.linalg.norm(Pc[E[:, 0]] - Pc[E[:, 1]], axis=1); strain = np.abs(l1 / np.maximum(l0, 1e-9) - 1)
    bad = np.nonzero(cr < -0.5)[0]; where = sorted({str(z['qlab'][q]) for q in bad})[:8]
    res[nm] = dict(cage_flips=int((cr < 0).sum()), cage_folds_gt120=int((cr < -0.5).sum()), cage_strain_p95_pct=round(float(np.percentile(strain, 95) * 100), 2),
                   source_flips_sampled=int((csr < 0).sum()), source_folds_gt120_sampled=int((csr < -0.5).sum()), fold_regions=where)
    print(nm, res[nm], flush=True)
json.dump(dict(scaffold='temporary LBS diagnostic (landmark segments, gaussian distance weights 2.5 cm); NOT a rig', poses=res), open(OUT, 'w'), indent=1)
