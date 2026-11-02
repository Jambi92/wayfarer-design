# sa6_pose.py : Saurin RP6 rig pilot -- forward kinematics, LBS, the EXACT RP5 34-pose suite (sa_deform4.py definitions, re-targeted to the RP6 bone names;
#   same pivots / axes / angles), flip metric (RP5 relcos: posed quad normal vs the rest normal rotated by the quad's dominant bone).
import os, json, numpy as np, scipy.sparse as sp
import sa6_common as C
X, Y, Z = np.eye(3)
def rot(axis, deg):
    a = np.asarray(axis, float); a = a / np.linalg.norm(a); t = np.radians(deg); K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + np.sin(t) * K + (1 - np.cos(t)) * K @ K
class Rig:
    def __init__(self, cfg, wfile=None):
        d = C.load(); self.cfg = cfg; self.Q = d['Q']; self.V = (d['V1'] if cfg == 'M' else d['V2']).copy(); self.nv = len(self.V); self.ql = d['qlab']
        self.P = json.load(open(C.EV6 + '/SA_RP6_joint_placement_%s_v001.json' % cfg))['bones']; self.LM = d['LM']
        self.DB = [b for b, v in self.P.items() if v['deform']]; self.bi = {b: i for i, b in enumerate(self.DB)}
        self.par = {b: v['parent'] for b, v in self.P.items()}
        self.kids_ = {b: [c for c in self.P if self.par[c] == b] for b in self.P}
        if wfile:
            z = np.load(wfile); S = sp.csr_matrix((z['data'], z['indices'], z['indptr']), shape=tuple(z['shape'])); assert list(z['bones']) == self.DB; self.W = S.toarray().astype(np.float64)
        self.n0 = self.qn(self.V)
    def H(self, b): return np.array(self.P[b]['head'])
    def Tl(self, b): return np.array(self.P[b]['tail'])
    def sub(self, b):
        out = [b]
        for c in self.kids_[b]: out += self.sub(c)
        return out
    def qn(self, P): Q = self.Q; return np.cross(P[Q[:, 2]] - P[Q[:, 0]], P[Q[:, 3]] - P[Q[:, 1]])
    def pose(self, spec):
        T = {b: (np.eye(3), np.zeros(3)) for b in self.P}
        for bn, piv, ax, deg in spec:
            R0p, t0p = T[bn]; piv = R0p @ np.asarray(piv, float) + t0p; ax = R0p @ np.asarray(ax, float); Rm = rot(ax, deg)
            for k in self.sub(bn): R0, t0 = T[k]; T[k] = (Rm @ R0, Rm @ (t0 - piv) + piv)
        return T
    def skin(self, T, P=None, W=None):
        P = self.V if P is None else P; W = self.W if W is None else W; out = np.zeros_like(P)
        for i, b in enumerate(self.DB):
            m = W[:, i] > 0
            if not m.any(): continue
            R0, t0 = T[b]; out[m] += W[m, i:i + 1] * (P[m] @ R0.T + t0)
        return out
    def blendR(self, T, W=None):
        W = self.W if W is None else W; Rb = np.stack([T[b][0] for b in self.DB]); return np.einsum('vb,bij->vij', W, Rb)
    def relcos(self, Pp, T, W=None):
        if W is None:
            if not hasattr(self, '_dom'): self._dom = sum(self.W[self.Q[:, k]] for k in range(4)).argmax(1)       # dominant bone per quad (cached)
            W = self.W; dom = self._dom
        else: dom = W[self.Q].mean(1).argmax(1)
        Rq = np.stack([T[self.DB[b]][0] for b in range(len(self.DB))])[dom]
        n0r = np.einsum('qij,qj->qi', Rq, self.n0); n1 = self.qn(Pp); return (n0r * n1).sum(1) / (np.linalg.norm(n0r, axis=1) * np.linalg.norm(n1, axis=1) + 1e-12)
    # ---- the RP5 34-pose suite, re-targeted (sa_deform4.py) ----
    def palm_normal(self, s):
        d = C.load(); nm = d['names']; V = self.V
        pal = np.mean([V[nm['%s_f%d_P%s' % (s, k, c)]] for k in range(1, 5) for c in 'RU'], 0) - np.mean([V[nm['%s_f%d_D%s' % (s, k, c)]] for k in range(1, 5) for c in 'RU'], 0)
        return pal / np.linalg.norm(pal)
    def digit_flex(self, s, k, degs, thumb=False):
        t = C.side_tag(s); pal = self.palm_normal(s); out = []
        for j, dg in enumerate(degs, 1):
            bn = ('thumb_%02d_%s' % (j, t)) if thumb else ('finger_%d_%02d_%s' % (k, j, t)); a, c = self.H(bn), self.Tl(bn); out.append((bn, a, np.cross(c - a, pal), dg))
        return out
    def suite(self, kind='rp5'):
        """kind='rp5': the EXACT RP5 sa_deform4 definitions (signs as written).  kind='anat': the same poses with the sagittal signs set to the anatomical
        direction (+y = anterior): the RP5 literal sagittal signs move the jaw closed, the neck / lower axial into extension, the shoulder / hip into extension,
        the elbow / knee into hyper-extension and the ankle into plantar-flexion (RP5 assumed +y posterior).  Non-sagittal poses are identical in both."""
        P = self.suite_rp5()
        if kind == 'rp5': return P
        flip = ('jaw_open_20', 'neck_flex_30', 'lower_axial_flex_25', 'shoulder_flex60', 'elbow_90', 'elbow_130', 'hip_flex70', 'knee_90', 'ankle_dorsi20')
        return {k: ([(b, p, a, -d) for b, p, a, d in v] if k.startswith(flip) else v) for k, v in P.items()}
    def suite_rp5(self):
        POSES = {'jaw_open_20': [('jaw', self.H('jaw'), X, 20)], 'neck_flex_30': [('neck_01', self.H('neck_01'), X, 30)], 'neck_rot_40': [('neck_01', self.H('neck_01'), Z, 40)]}
        for s, sg in (('xpos', 1), ('xneg', -1)):
            t = C.side_tag(s); S, E_, Hh, K, A = self.H('upperarm_' + t), self.H('forearm_' + t), self.H('thigh_' + t), self.H('shin_' + t), self.H('foot_' + t)
            POSES.update({'shoulder_abd45_' + s: [('upperarm_' + t, S, Y, -sg * 45)], 'shoulder_abd90_' + s: [('upperarm_' + t, S, Y, -sg * 90)], 'shoulder_flex60_' + s: [('upperarm_' + t, S, X, -60)],
                          'elbow_90_' + s: [('forearm_' + t, E_, X, -90)], 'elbow_130_' + s: [('forearm_' + t, E_, X, -130)], 'hip_flex70_' + s: [('thigh_' + t, Hh, X, -70)],
                          'knee_90_' + s: [('shin_' + t, K, X, 90)], 'ankle_dorsi20_' + s: [('foot_' + t, A, X, -20)]})
            fist = sum([self.digit_flex(s, k, (75, 95, 60)) for k in range(1, 5)], []) + self.digit_flex(s, 0, (35, 30, 25), True)
            grasp = sum([self.digit_flex(s, k, (40, 50, 30)) for k in range(1, 5)], []) + self.digit_flex(s, 0, (25, 20, 15), True)
            tips = np.array([self.Tl('finger_%d_03_%s' % (k, t)) for k in range(1, 5)] + [self.Tl('thumb_03_' + t)]); hl = tips.mean(0) - self.H('hand_' + t)
            opp = [('thumb_01_' + t, self.H('thumb_01_' + t), hl, -sg * 50)] + self.digit_flex(s, 0, (30, 25, 20), True)
            toe = lambda k, deg: ('toe_%d_01_%s' % (k, t), self.H('toe_%d_01_%s' % (k, t)), np.cross(self.Tl('toe_%d_01_%s' % (k, t)) - self.H('toe_%d_01_%s' % (k, t)), [0, 0, -1]), deg)
            POSES.update({'fist_' + s: fist, 'grasp_' + s: grasp, 'thumb_opposition_' + s: opp, 'toe_flex30_' + s: [toe(k, 30) for k in range(1, 6)], 'toe_ext30_' + s: [toe(k, -30) for k in range(1, 6)]})
        import sa6_skeleton as SK
        tr = (lambda p: p) if self.cfg == 'M' else (lambda p: SK.transfer(p, self.V))
        trc = tr(self.LM['tail_root_centre']); tc4 = tr(self.LM['tail_chain_04'])          # RP5 pivot / axis landmarks (c2: same landmark transferred)
        POSES.update({'trunk_twist_30': [('spine_01', self.H('spine_01'), Z, 30)], 'lower_axial_flex_25': [('spine_01', self.H('spine_01'), X, 25)],
                      'tail_root_lateral_30': [('tail_01', trc, Z, 30)], 'tail_root_vertical_25': [('tail_01', trc, X, 25)], 'tail_twist_30': [('tail_01', trc, tc4 - trc, 30)]})
        return POSES
