# RAC RM-OT-05F shared helpers for the Gorrund hand-sculpt handoff / re-entry layer.
# Conventions of every exported / ingested mesh: centimetres, Z up (ground plane z = 0), +Y anterior, +X = the body's LEFT side,
# R-6 neutral stance, 13 380 body vertices in the template's exact order (MPFB base topology minus helper geometry), faces 1-based in OBJ.
import os, sys, json, hashlib, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); W1 = os.path.dirname(D)
for p in (W1, W1 + '/rmot05c_drivers', W1 + '/rmot05d_drivers'): sys.path.insert(0, p)
import c_guard as CG, c_preview as P, skeleton_envelope as SE, true_envelope as TE, race_base as RB
S = CG.S
REPO = os.path.dirname(os.path.dirname(os.path.dirname(W1)))
HANDOFF = REPO + '/reviews/rac-rmot05f-handoff'
WORK = S + '/rmot05f'; os.makedirs(WORK, exist_ok=True)
SKELETON_BODY = 'GO5DE1'          # any accepted-route Gorrund body: supplies the accepted skeleton route (-LEAN, joints, weights) only
NBODY = 13380                      # body vertices (keep mask = the first 13 380 vertices); helpers are never exported

def route_state(body, st='r6'):
    """unorganized accepted skeleton-route surface of a body's composition state: f(-LEAN) + (donor - donor_lean), grounded.
    Returns (V full array, B npz of the body, L npz of its -LEAN, J body-frame joints of the route)"""
    B = np.load(CG.path(body) + '_%s.npz' % st, allow_pickle=True); m = json.loads(str(B['meta']))
    sk = m['skeleton'].replace('-LEAN', ''); L = np.load(CG.path(sk) + '-LEAN_%s.npz' % st, allow_pickle=True); dr, dl = m['tissue_donor']
    R = np.load(P.find(dr) + '_%s.npz' % st, allow_pickle=True); Dn = np.load(P.find(dl) + '_%s.npz' % st, allow_pickle=True)
    f, sc = SE.simil(Dn, R); V = f(L['V'].astype(float)) + R['V'].astype(float) - f(Dn['V'].astype(float))
    k = L['keep'].astype(bool); z0 = V[k, 2].min(); V[:, 2] -= z0
    JL = json.loads(str(L['joints'])); J = {a: [(f(np.array(h)) - [0, 0, z0]).tolist(), (f(np.array(t)) - [0, 0, z0]).tolist()] for a, (h, t) in JL.items()}
    return V, B, L, J, f, z0

def floor_in_body_frame(L, f, z0):
    """true skeletal floor (05D true_envelope.floor) in the same frame as route_state"""
    Fv = TE.floor(L['V'].astype(float), L, json.loads(str(L['joints'])))[0]
    return f(Fv) - np.array([0, 0, z0])

def write_obj(fn, V, F, header=''):
    with open(fn, 'w') as o:
        for line in header.splitlines(): o.write('# ' + line + '\n')
        o.write('o gorrund_body\n')
        for v in V[:NBODY]: o.write('v %.5f %.5f %.5f\n' % tuple(v))
        Fk = F[(F < NBODY).all(1)]
        for t in Fk: o.write('f %d %d %d\n' % tuple(t + 1))

def read_obj(fn):
    V, F = [], []
    for line in open(fn):
        if line.startswith('v '): V.append([float(x) for x in line.split()[1:4]])
        elif line.startswith('f '): F.append([int(x.split('/')[0]) - 1 for x in line.split()[1:]])
    return np.array(V, float), F

def sha(fn): return hashlib.sha256(open(fn, 'rb').read()).hexdigest()

def regions(B, V, J):
    """vertex masks of the six hard-form families (05F §4 A-F) and the no-touch zones, on the template (weights + joint frames)"""
    w = {k[2:]: B[k].astype(float) for k in B.files if k.startswith('w_')}; keep = B['keep'].astype(bool)
    hip = 0.5 * (J['thigh_l'][0][2] + J['thigh_r'][0][2]); sst = 0.5 * (J['clavicle_l'][0][2] + J['clavicle_r'][0][2])
    rz = (V[:, 2] - hip) / (sst - hip)
    arm = np.maximum.reduce([w[k] for k in ('upperarm_l', 'upperarm_r', 'lowerarm_l', 'lowerarm_r', 'hand_l', 'hand_r', 'fingers_l', 'fingers_r')])
    trunk = np.clip(w['pelvis'] + w['spine_01'] + w['spine_02'] + w['spine_03'] + w['clavicle_l'] + w['clavicle_r'], 0, 1)
    cy = np.median(V[keep & (np.abs(rz - 0.5) < 0.1) & (arm < 0.05), 1])
    post = V[:, 1] < cy
    def tbone(bn, sd):
        h, ax, ln, ea, el = RB._frame(J, bn, sd); return (V - h) @ ax / ln
    thigh_t = np.where(V[:, 0] > 0, tbone('thigh', 'l'), tbone('thigh', 'r')); uarm_t = np.where(V[:, 0] > 0, tbone('upperarm', 'l'), tbone('upperarm', 'r'))
    thighw = np.maximum(w['thigh_l'], w['thigh_r']); calfw = np.maximum(w['calf_l'], w['calf_r']); footw = np.maximum(w['foot_l'], w['foot_r'])
    uaw = np.maximum(w['upperarm_l'], w['upperarm_r']); law = np.maximum(w['lowerarm_l'], w['lowerarm_r']); handw = np.maximum(w['hand_l'], w['hand_r'])
    R = {
     'A_trunk_section_S2_S5': keep & (trunk > 0.5) & (arm < 0.2) & ~post & (rz > 0.05) & (rz < 0.95),
     'B_posterior_axial_load_path': keep & (((trunk > 0.5) & post & (rz > -0.35) & (rz < 0.95) & (arm < 0.2)) | ((thighw > 0.5) & post & (thigh_t < 0.35))),
     'C_pelvis_to_thigh': keep & (((w['pelvis'] > 0.3) & (np.abs(V[:, 0]) > 8)) | ((thighw > 0.5) & (thigh_t < 0.45))) & ~post,
     'D_knee_shank_ankle': keep & (((thighw > 0.5) & (thigh_t > 0.75)) | (calfw > 0.3) | ((footw > 0.3) & (V[:, 2] > 4.0))),
     'E_elbow_forearm_wrist': keep & (((uaw > 0.5) & (uarm_t > 0.75)) | (law > 0.3) | ((handw > 0.3) & (handw < 0.7))),
     'F_shoulder_girdle_neck_root': keep & (((np.maximum(w['clavicle_l'], w['clavicle_r']) > 0.3) | ((uaw > 0.5) & (uarm_t < 0.3)) | ((w['spine_03'] > 0.3) & (rz > 0.85))) & (w['head'] < 0.05)),
     'NO_TOUCH_head_neck': keep & (np.clip(w['head'] + w['ears'] + w['neck_01'], 0, 1) > 0.5),
     'NO_TOUCH_hands_digits': keep & (np.clip(w['hand_l'] + w['hand_r'] + w['fingers_l'] + w['fingers_r'], 0, 1) > 0.7),
     'NO_TOUCH_toes_forefoot': keep & (np.maximum(w['ball_l'], w['ball_r']) > 0.5)}
    return R
