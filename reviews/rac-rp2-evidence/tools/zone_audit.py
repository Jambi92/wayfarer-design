# zone_audit.py CAND.npz OUT.json : deformation-zone topology audit (loops across each joint, quads only, poles near crease planes)
# + creator-density audit (mean edge length / stature per zone, contract s8)
import sys, json, numpy as np, scipy.sparse as sp
R = '/tmp/claude-0/rp2/'
z = np.load(sys.argv[1]); V = z['V']; Q = z['Q']; n = len(V)
SS = sp.load_npz(sys.argv[1].replace('.npz', '_SS.npz')).tocsr()
J = json.loads(str(np.load(R + 'GR5DE3_r6.npz')['joints'])); Wb = dict(np.load(R + 'weights_body.npz')); W = {k: SS @ v for k, v in Wb.items()}
E = np.unique(np.sort(np.vstack([Q[:, [i, (i + 1) % 4]] for i in range(4)]), 1), axis=0)
val = np.bincount(E.ravel(), minlength=n)
stature = V[:, 2].max() - V[:, 2].min()
def loops_across(center, axis, radius, half):
    """number of edge loops crossed along the surface, on a line parallel to the axis through the joint (front side),
    within +-half cm of the joint: count mesh edges crossed by the section plane (axis, side) at axial offsets in the window"""
    axis = axis / np.linalg.norm(axis); side = np.cross(axis, [0, 1, 0]);
    if np.linalg.norm(side) < 1e-3: side = np.cross(axis, [1, 0, 0])
    side /= np.linalg.norm(side); fwd = np.cross(side, axis)
    s = (V - center) @ side; t = (V - center) @ axis; r = (V - center) @ fwd
    a, b = E[:, 0], E[:, 1]; cross = (np.sign(s[a]) != np.sign(s[b]))
    u = s[a] / (s[a] - s[b] + 1e-12); tt = t[a] + u * (t[b] - t[a]); rr = r[a] + u * (r[b] - r[a])
    near = cross & (np.abs(tt) <= half) & (rr > 0) & (np.abs(rr) < radius)
    return int(near.sum())
zones = {}
def bone(bn): h = np.array(J[bn][0]); t = np.array(J[bn][1]); return h, t
spec = [('shoulder', 'upperarm', 'head', 5, 3.0), ('elbow', 'lowerarm', 'head', 3, 2.0), ('wrist', 'hand', 'head', 3, 1.5),
        ('hip', 'thigh', 'head', 5, 3.0), ('knee', 'calf', 'head', 3, 2.0), ('ankle', 'foot', 'head', 3, 1.5), ('toes_ball', 'ball', 'head', 2, 1.0),
        ('knuckle_index', 'index_01', 'head', 3, 0.8), ('ip_index_pip', 'index_02', 'head', 2, 0.6), ('ip_index_dip', 'index_03', 'head', 2, 0.5)]
out = {}
for nm, bn, end, need, half in spec:
    for s_ in 'lr':
        h, t = bone(bn + '_' + s_); ax = t - h
        if nm in ('shoulder', 'hip'):
            ph, pt = bone(('upperarm' if nm == 'shoulder' else 'thigh') + '_' + s_); ax = pt - ph
        c = loops_across(h, ax, 25.0, half)
        out['%s_%s' % (nm, s_)] = dict(loops_in_window=c, window_cm=2 * half, required=need, pass_=c >= need)
h, t = bone('neck_01'); out['neck'] = dict(loops_in_window=loops_across((h + t) / 2, t - h, 15, 3.0), window_cm=6, required=4)
out['neck']['pass_'] = out['neck']['loops_in_window'] >= 4
h, t = bone('spine_02'); out['spine_abdomen'] = dict(loops_in_window=loops_across(h, t - h, 30, 4.0), window_cm=8, required='horizontal loops present')
out['spine_abdomen']['pass_'] = out['spine_abdomen']['loops_in_window'] >= 4
# poles near the crease planes (within 1.5 cm of the joint plane, inside the limb)
pol = {}
for nm, bn in (('elbow', 'lowerarm'), ('knee', 'calf'), ('wrist', 'hand'), ('ankle', 'foot')):
    for s_ in 'lr':
        h, t = bone(bn + '_' + s_); ax = (t - h) / np.linalg.norm(t - h); d = (V - h) @ ax; rad = np.linalg.norm((V - h) - d[:, None] * ax, axis=1)
        m = (np.abs(d) < 1.5) & (rad < 12); pol['%s_%s' % (nm, s_)] = int(((val != 4) & m).sum())
# quads in deformation zones: the mesh is all quads
dens = {}
g = lambda *k: sum(W[x] for x in k)
zm = {'face_ears': g('head', 'ears') > 0.5, 'hands_digits': g('hand_l', 'hand_r', 'fingers_l', 'fingers_r') > 0.5, 'feet_toes': g('foot_l', 'foot_r', 'ball_l', 'ball_r') > 0.5,
      'trunk_pelvis': g('pelvis', 'spine_01', 'spine_02', 'spine_03', 'clavicle_l', 'clavicle_r', 'neck_01') > 0.5,
      'limbs': g('upperarm_l', 'upperarm_r', 'lowerarm_l', 'lowerarm_r', 'thigh_l', 'thigh_r', 'calf_l', 'calf_r') > 0.5}
ceil = {'face_ears': 0.25, 'hands_digits': 0.3, 'feet_toes': 0.3, 'trunk_pelvis': 0.6, 'limbs': 0.6}
L = np.linalg.norm(V[E[:, 0]] - V[E[:, 1]], axis=1)
for k, m in zm.items():
    me = m[E].all(1); r = float(L[me].mean() / stature * 100)
    dens[k] = dict(mean_edge_mm=float(L[me].mean() * 10), mean_edge_pct_stature=r, ceiling_pct=ceil[k], pass_=r <= ceil[k])
res = dict(loops=out, poles_within_1p5cm_of_crease_planes=pol, quads_in_deformation_zones_pct=100.0, density=dens,
           all_loops_pass=all(v['pass_'] for v in out.values()), all_density_pass=all(v['pass_'] for v in dens.values()))
json.dump(res, open(sys.argv[2], 'w'), indent=1)
for k, v in out.items(): print('%-18s loops %3d (need %s)' % (k, v['loops_in_window'], v['required']))
print('poles', pol); print(json.dumps(dens, indent=0)); print('loops pass', res['all_loops_pass'], 'density pass', res['all_density_pass'])
