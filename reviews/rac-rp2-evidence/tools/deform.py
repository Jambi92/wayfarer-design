# deform.py (bpy) CAND.npz OUT.json [smooth_iters] : diagnostic DQS deformation tests on the production candidate.
# Armature = the source MPFB rig joints (carried unchanged); weights = source MPFB weights interpolated to the production vertices
# (fingers split per finger by nearest finger bone inside the source finger weight). Diagnostic only: not a game rig.
import sys, json, math, numpy as np, bpy, mathutils
from mathutils.bvhtree import BVHTree
a = sys.argv[sys.argv.index('--') + 1:]; R = '/tmp/claude-0/rp2/'
import scipy.sparse as sp
z = np.load(a[0]); V = z['V']; Q = z['Q']; n = len(V)
SS = sp.load_npz(a[0].replace('.npz', '_SS.npz')).tocsr()
src = np.load(R + 'GR5DE3_r6.npz'); J = json.loads(str(src['joints'])); Wb = dict(np.load(R + 'weights_body.npz'))
SMI = int(a[2]) if len(a) > 2 else 0
toB = lambda p: mathutils.Vector((p[0] / 100, -p[1] / 100, p[2] / 100))
W = {k: SS @ v for k, v in Wb.items()}
# per-finger split
fingers = ['thumb', 'index', 'middle', 'ring', 'pinky']
for s in 'lr':
    fw = W.pop('fingers_' + s); segs = []
    for f in fingers:
        for i in (1, 2, 3): h = np.array(J['%s_0%d_%s' % (f, i, s)][0]); t = np.array(J['%s_0%d_%s' % (f, i, s)][1]); segs.append(('%s_0%d_%s' % (f, i, s), h, t))
    D = []
    for nm, h, t in segs:
        ab = t - h; tt = np.clip(((V - h) @ ab) / (ab @ ab), 0, 1); D.append(np.linalg.norm(V - (h + tt[:, None] * ab), axis=1))
    D = np.array(D); near = D.argmin(0)
    for k, (nm, h, t) in enumerate(segs): W[nm] = fw * (near == k)
W.pop('ears', None); W['head'] = W['head'] + SS @ Wb['ears']
if SMI:
    E = np.unique(np.sort(np.vstack([Q[:, [i, (i + 1) % 4]] for i in range(4)]), 1), axis=0)
    A = sp.coo_matrix((np.ones(len(E)), (E[:, 0], E[:, 1])), shape=(n, n)); A = (A + A.T).tocsr(); deg = np.asarray(A.sum(1)).ravel()
    for k in W:
        w = W[k]
        for _ in range(SMI): w = 0.5 * w + 0.5 * (A @ w) / deg
        W[k] = w
tot = sum(W.values()); W = {k: v / np.maximum(tot, 1e-9) for k, v in W.items()}
parent = {'pelvis': None, 'spine_01': 'pelvis', 'spine_02': 'spine_01', 'spine_03': 'spine_02', 'neck_01': 'spine_03', 'head': 'neck_01'}
for s in 'lr':
    parent.update({'clavicle_' + s: 'spine_03', 'upperarm_' + s: 'clavicle_' + s, 'lowerarm_' + s: 'upperarm_' + s, 'hand_' + s: 'lowerarm_' + s,
                   'thigh_' + s: 'pelvis', 'calf_' + s: 'thigh_' + s, 'foot_' + s: 'calf_' + s, 'ball_' + s: 'foot_' + s})
    for f in fingers:
        parent['%s_01_%s' % (f, s)] = 'hand_' + s; parent['%s_02_%s' % (f, s)] = '%s_01_%s' % (f, s); parent['%s_03_%s' % (f, s)] = '%s_02_%s' % (f, s)
bpy.ops.wm.read_factory_settings(use_empty=True)
P = np.c_[V[:, 0], -V[:, 1], V[:, 2]] / 100
me = bpy.data.meshes.new('GR'); me.from_pydata(P.tolist(), [], Q.tolist()); me.update(); ob = bpy.data.objects.new('GR', me); bpy.context.scene.collection.objects.link(ob)
arm = bpy.data.armatures.new('RIG'); ao = bpy.data.objects.new('RIG', arm); bpy.context.scene.collection.objects.link(ao)
bpy.context.view_layer.objects.active = ao; bpy.ops.object.mode_set(mode='EDIT')
for k in parent:
    b = arm.edit_bones.new(k); b.head = toB(J[k][0]); b.tail = toB(J[k][1])
for k, p in parent.items():
    if p: arm.edit_bones[k].parent = arm.edit_bones[p]
bpy.ops.object.mode_set(mode='OBJECT')
HEAT = len(a) > 3 and a[3] == 'heat'
if HEAT:
    bpy.ops.object.select_all(action='DESELECT'); ob.select_set(True); ao.select_set(True); bpy.context.view_layer.objects.active = ao
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')
    mod = [m for m in ob.modifiers if m.type == 'ARMATURE'][0]; mod.use_deform_preserve_volume = True
    ng = sum(1 for g in ob.vertex_groups); print('heat weights groups', ng, flush=True)
    # vertices without any weight -> fall back to the interpolated source weights
else:
    for k, w in W.items():
        g = ob.vertex_groups.new(name=k); idx = np.where(w > 1e-4)[0]
        for i in idx: g.add([int(i)], float(w[i]), 'REPLACE')
    mod = ob.modifiers.new('arm', 'ARMATURE'); mod.object = ao; mod.use_deform_preserve_volume = True
T = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]
def evalP():
    dg = bpy.context.evaluated_depsgraph_get(); e = ob.evaluated_get(dg); m = e.to_mesh(); X = np.zeros(len(m.vertices) * 3); m.vertices.foreach_get('co', X); e.to_mesh_clear()
    X = X.reshape(-1, 3) * 100; return np.c_[X[:, 0], -X[:, 1], X[:, 2]]
def sx(X):
    t = BVHTree.FromPolygons(X.tolist(), Q.tolist(), all_triangles=False, epsilon=0.0); pr = np.array(t.overlap(t), int).reshape(-1, 2); pr = pr[pr[:, 0] < pr[:, 1]]
    if len(pr): A_ = Q[pr[:, 0]]; B_ = Q[pr[:, 1]]; pr = pr[~(A_[:, :, None] == B_[:, None, :]).any((1, 2))]
    return pr
def qarea(X): return 0.5 * (np.linalg.norm(np.cross(X[Q[:, 1]] - X[Q[:, 0]], X[Q[:, 2]] - X[Q[:, 0]]), axis=1) + np.linalg.norm(np.cross(X[Q[:, 2]] - X[Q[:, 0]], X[Q[:, 3]] - X[Q[:, 0]]), axis=1))
def qn(X): nn = np.cross(X[Q[:, 2]] - X[Q[:, 0]], X[Q[:, 3]] - X[Q[:, 1]]); return nn / (np.linalg.norm(nn, axis=1)[:, None] + 1e-30)
X0 = evalP(); rest = set(map(tuple, sx(X0).tolist())); A0 = qarea(X0); N0 = qn(X0)
_E = np.vstack([np.c_[np.sort(Q[:, [i, (i + 1) % 4]], 1), np.arange(len(Q))] for i in range(4)]); _o = np.lexsort((_E[:, 1], _E[:, 0])); _E = _E[_o]
_same = (_E[1:, :2] == _E[:-1, :2]).all(1); FA = _E[:-1, 2][_same]; FB = _E[1:, 2][_same]
def crumple(N): return (N[FA] * N[FB]).sum(1)
C0 = crumple(N0)
dom = np.array(list(W.keys()))[np.argmax(np.stack([W[k] for k in W]), 0)]
# poses: (name, [(bone, world_axis_analysis, deg)])  analysis frame axes: x left, f forward, u up
X_, F_, U_ = (1, 0, 0), (0, 1, 0), (0, 0, 1)
def rotv(v, ax, deg):
    ax = np.array(ax, float); th = math.radians(deg); v = np.asarray(v, float)
    return v * math.cos(th) + np.cross(ax, v) * math.sin(th) + ax * (ax @ v) * (1 - math.cos(th))
def signed(bone, ax, deg, crit):
    h = np.array(J[bone][0]); t = np.array(J[bone][1])
    d1 = rotv(t - h, ax, deg) + h - t
    return (bone, ax, deg if crit(d1, h) else -deg)
away = lambda d, h: d[0] * np.sign(h[0]) > 0          # tip moves laterally (abduction)
toward = lambda d, h: d[0] * np.sign(h[0]) < 0
fwd = lambda d, h: d[1] > 0; back = lambda d, h: d[1] < 0
POSES = []
for s in 'lr':
    abd = lambda ss: [signed('upperarm_' + ss, F_, 45, away)]
    arms = abd('l') + abd('r')
    POSES += [('shoulder_abd45_' + s, [signed('upperarm_' + s, F_, 45, away)]), ('shoulder_abd90_' + s, [signed('upperarm_' + s, F_, 90, away)]),
              ('shoulder_flex60_' + s, [signed('upperarm_' + s, X_, 60, fwd)]), ('shoulder_ext30_' + s, [signed('upperarm_' + s, X_, 30, back)]),
              ('elbow_flex90_' + s, [signed('lowerarm_' + s, X_, 90, fwd)]), ('elbow_flex120_' + s, [signed('lowerarm_' + s, X_, 120, fwd)]),
              ('wrist_flex45_' + s, abd(s) + [signed('hand_' + s, F_, 45, toward)]), ('wrist_ext45_' + s, abd(s) + [signed('hand_' + s, F_, 45, away)]),
              ('fingers_curl_half_' + s, abd(s) + [signed('%s_0%d_%s' % (f, i, s), F_, (40, 45, 30)[i - 1], toward) for f in fingers[1:] for i in (1, 2, 3)]),
              ('fingers_curl_full_' + s, abd(s) + [signed('%s_0%d_%s' % (f, i, s), F_, (70, 90, 60)[i - 1], toward) for f in fingers[1:] for i in (1, 2, 3)]),
              ('hip_flex45_' + s, arms + [signed('thigh_' + s, X_, 45, fwd)]), ('hip_flex90_' + s, arms + [signed('thigh_' + s, X_, 90, fwd)]),
              ('hip_abd30_' + s, arms + [signed('thigh_' + s, F_, 30, away)]), ('hip_ext15_' + s, arms + [signed('thigh_' + s, X_, 15, back)]),
              ('knee_flex90_' + s, [signed('calf_' + s, X_, 90, back)]), ('knee_flex120_' + s, [signed('calf_' + s, X_, 120, back)]),
              ('ankle_dorsi20_' + s, [signed('foot_' + s, X_, 20, lambda d, h: d[2] > 0)]), ('ankle_plantar30_' + s, [signed('foot_' + s, X_, 30, lambda d, h: d[2] < 0)]),
              ('toes_ext20_' + s, [signed('ball_' + s, X_, 20, lambda d, h: d[2] > 0)]), ('toes_ext30_' + s, [signed('ball_' + s, X_, 30, lambda d, h: d[2] > 0)])]
arms = [signed('upperarm_l', F_, 45, away), signed('upperarm_r', F_, 45, away)]
POSES += [('neck_flex30', [signed('neck_01', X_, 30, fwd)]), ('neck_ext20', [signed('neck_01', X_, 20, back)]), ('neck_turn45', [('neck_01', U_, 45)]),
          ('spine_flex20', arms + [signed('spine_02', X_, 20, fwd)]), ('spine_ext15', arms + [signed('spine_02', X_, 15, back)]),
          ('spine_twist25', arms + [('spine_02', U_, 25)]), ('spine_lat20', arms + [signed('spine_02', F_, 20, lambda d, h: d[0] > 0)]),
          ('rigprep_A_pose45', arms + [signed('lowerarm_l', X_, 10, fwd), signed('lowerarm_r', X_, 10, fwd)])]
def setpose(spec):
    for pb in ao.pose.bones: pb.rotation_mode = 'QUATERNION'; pb.rotation_quaternion = (1, 0, 0, 0)
    bpy.context.view_layer.update()
    for bn, ax, deg in spec:
        pb = ao.pose.bones[bn]; axb = mathutils.Vector((ax[0], -ax[1], ax[2]))
        Rw = mathutils.Matrix.Rotation(-math.radians(deg), 4, axb)          # analysis frame is mirrored (y) w.r.t. Blender: angle flips
        M = pb.bone.matrix_local; loc = (M.inverted().to_3x3() @ Rw.to_3x3() @ M.to_3x3()).to_quaternion()
        pb.rotation_quaternion = loc
    bpy.context.view_layer.update()
import os
DUMP = os.environ.get('DUMP', '').split(',')
res = {}
for name, spec in POSES:
    setpose(spec); X = evalP()
    pr = np.array(sorted(set(map(tuple, sx(X).tolist())) - rest), int).reshape(-1, 2)
    ar = qarea(X) / np.maximum(A0, 1e-12)
    # folded faces: normal reversal relative to the rest normal rotated with the face's dominant bone
    bones = {}
    nf = qn(X)
    Rb = {}
    for pb in ao.pose.bones: Rb[pb.name] = np.array((ao.matrix_world @ pb.matrix @ pb.bone.matrix_local.inverted()).to_3x3())
    fdom = dom[Q[:, 0]]
    Rf = np.stack([Rb[b] for b in fdom]); Mflip = np.diag([1, -1, 1]); Rf = Mflip @ Rf @ Mflip
    cc = crumple(nf); flips = int(((cc < 0) & (C0 > 0.3)).sum())          # adjacent faces folded over each other (dihedral > 90 deg) that were smooth at rest
    depth = 0.0
    if len(pr):
        Cb = X[Q[pr[:, 1]]].mean(1); Nb = qn(X)[pr[:, 1]]; Ca = X[Q[pr[:, 0]]].mean(1); Na = qn(X)[pr[:, 0]]
        da = np.einsum('nkj,nj->nk', X[Q[pr[:, 0]]] - Cb[:, None], Nb); db = np.einsum('nkj,nj->nk', X[Q[pr[:, 1]]] - Ca[:, None], Na)
        dep = np.minimum(np.minimum(-da.min(1), da.max(1)).clip(0), np.minimum(-db.min(1), db.max(1)).clip(0)); depth = float(dep.max() * 10)
    pairs_info = {}
    if len(pr):
        ca = dom[Q[pr[:, 0], 0]]; cb = dom[Q[pr[:, 1], 0]]
        for x, y in zip(ca, cb):
            k = '%s|%s' % tuple(sorted((x, y))); pairs_info[k] = pairs_info.get(k, 0) + 1
    def ph(bn, tail=False):
        pb = ao.pose.bones[bn]; p = ao.matrix_world @ (pb.tail if tail else pb.head); return np.array([p[0], -p[1], p[2]]) * 100
    jt = ph(spec[-1][0]) if spec else np.zeros(3)
    if name.startswith('fingers'): jt = ph('hand_' + name[-1], True)
    far = float(np.linalg.norm(X[Q[pr.ravel()]].mean(1) - jt, axis=1).max()) if len(pr) else 0.0
    lim = 25.0 if any(k in name for k in ('hip', 'knee', 'wrist')) else 15.0
    cls = 'clean' if len(pr) == 0 else ('local flexion-crease contact' if far <= lim else 'NON-LOCAL CONTACT')
    res[name] = dict(new_selfx_pairs=int(len(pr)), max_depth_mm=depth, max_contact_distance_from_joint_cm=far, classification=cls, pairs_by_bone=pairs_info, min_area_ratio=float(ar.min()), faces_area_ratio_lt_0p2=int((ar < 0.2).sum()), folded_faces=flips)
    print(name, json.dumps(res[name]), flush=True)
    if name in DUMP: np.savez(R + 'pose_%s.npz' % name, V=X, Q=Q)
# return to rest
setpose([]); Xr = evalP(); res['return_to_rest_max_mm'] = float(np.abs(Xr - X0).max() * 10)
json.dump(res, open(a[1], 'w'), indent=1)
