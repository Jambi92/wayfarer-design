# fastpose.py : numpy dual-quaternion skinning of the diagnostic hand crops (identical maths to Blender's armature modifier
# with Preserve Volume), plus fast local intersection / depth / fixture checks. Used by the grip solver; the solver's final
# poses are re-evaluated through Blender itself (poses.py) for the saved evidence.
import numpy as np, pickle, os, json
import scipy.sparse as sp

def export_rig(rd):
    """(bpy) dump rest matrices, parents and crop meshes of hand_rig_DIAG.blend to rig_np.npz"""
    import bpy
    bpy.ops.wm.open_mainfile(filepath=os.path.join(rd, 'hand_rig_DIAG.blend'))
    out = {}
    for side in 'LR':
        ob = bpy.data.objects['GO_hand_%s_DIAG' % side]; ao = bpy.data.objects['GO_hand_%s_RIG' % side]; me = ob.data
        P = np.zeros(len(me.vertices) * 3); me.vertices.foreach_get('co', P); P = P.reshape(-1, 3)
        Q = np.zeros(len(me.polygons) * 4, int); me.polygons.foreach_get('vertices', Q); Q = Q.reshape(-1, 4)
        names = [b.name for b in ao.data.bones]; par = [names.index(b.parent.name) if b.parent else -1 for b in ao.data.bones]
        M = np.array([np.array(b.matrix_local) for b in ao.data.bones])
        W = np.zeros((len(P), len(names)), np.float32)
        gi = {g.index: g.name for g in ob.vertex_groups}
        for v in me.vertices:
            for g in v.groups:
                nm = gi[g.group]
                if nm in names: W[v.index, names.index(nm)] = g.weight
        out[side] = dict(P=P, Q=Q, names=names, parent=np.array(par), M=M, W=W)
    pickle.dump(out, open(os.path.join(rd, 'rig_np.pkl'), 'wb'))

def euler_xyz(rx, ry, rz):
    cx, sx = np.cos(rx), np.sin(rx); cy, sy = np.cos(ry), np.sin(ry); cz, sz = np.cos(rz), np.sin(rz)
    Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]]); Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]]); Rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
    return Rz @ Ry @ Rx   # Blender XYZ euler

class Hand:
    def __init__(s, rd, side):
        D = pickle.load(open(os.path.join(rd, 'rig_np.pkl'), 'rb'))[side]
        s.P0 = D['P']; s.Q = D['Q']; s.names = D['names']; s.par = D['parent']; s.M = D['M']; s.W = sp.csr_matrix(D['W'])
        s.nb = len(s.names); s.Minv = np.linalg.inv(s.M)
        s.idx = {n: i for i, n in enumerate(s.names)}
    def skin_mats(s, angles):
        """angles: {bone: (flex, abd, twist) degrees} -> per-bone skinning matrices (armature space)"""
        Pm = np.zeros((s.nb, 4, 4))
        for i in range(s.nb):
            R = np.eye(4)
            a = angles.get(s.names[i])
            if a is not None: R[:3, :3] = euler_xyz(np.radians(a[0]), np.radians(a[2]), np.radians(a[1]))
            if s.par[i] < 0: Pm[i] = s.M[i] @ R
            else: Pm[i] = Pm[s.par[i]] @ (s.Minv[s.par[i]] @ s.M[i]) @ R
        return Pm @ s.Minv
    def pose(s, angles, dqs=True):
        S = s.skin_mats(angles)
        if not dqs:
            P = np.zeros_like(s.P0); Ph = np.c_[s.P0, np.ones(len(s.P0))]
            for b in range(s.nb):
                w = s.W[:, b].toarray().ravel(); m = w > 0
                if m.any(): P[m] += w[m, None] * (Ph[m] @ S[b].T)[:, :3]
            return P
        # dual quaternions
        q0 = np.array([rot2quat(S[b][:3, :3]) for b in range(s.nb)])
        t = S[:, :3, 3]
        qe = np.array([0.5 * qmul(np.r_[0, t[b]], q0[b]) for b in range(s.nb)])
        # sign alignment against the dominant (first non-zero) bone per vertex: align all to q0[0]'s hemisphere
        ref = q0[0]; sg = np.sign(q0 @ ref); sg[sg == 0] = 1; q0 = q0 * sg[:, None]; qe = qe * sg[:, None]
        B0 = s.W @ q0; Be = s.W @ qe
        n = np.linalg.norm(B0, axis=1, keepdims=True); B0 /= n; Be /= n
        w0 = B0[:, 0]; v0 = B0[:, 1:]; we = Be[:, 0]; ve = Be[:, 1:]
        p = s.P0
        # rotate
        tt = 2 * np.cross(v0, p); pr = p + w0[:, None] * tt + np.cross(v0, tt)
        trans = 2 * (w0[:, None] * ve - we[:, None] * v0 + np.cross(v0, ve))
        return pr + trans

def rot2quat(R):
    tr = np.trace(R)
    if tr > 0:
        S = np.sqrt(tr + 1.0) * 2; w = 0.25 * S; x = (R[2, 1] - R[1, 2]) / S; y = (R[0, 2] - R[2, 0]) / S; z = (R[1, 0] - R[0, 1]) / S
    elif R[0, 0] > R[1, 1] and R[0, 0] > R[2, 2]:
        S = np.sqrt(1.0 + R[0, 0] - R[1, 1] - R[2, 2]) * 2; w = (R[2, 1] - R[1, 2]) / S; x = 0.25 * S; y = (R[0, 1] + R[1, 0]) / S; z = (R[0, 2] + R[2, 0]) / S
    elif R[1, 1] > R[2, 2]:
        S = np.sqrt(1.0 + R[1, 1] - R[0, 0] - R[2, 2]) * 2; w = (R[0, 2] - R[2, 0]) / S; x = (R[0, 1] + R[1, 0]) / S; y = 0.25 * S; z = (R[1, 2] + R[2, 1]) / S
    else:
        S = np.sqrt(1.0 + R[2, 2] - R[0, 0] - R[1, 1]) * 2; w = (R[1, 0] - R[0, 1]) / S; x = (R[0, 2] + R[2, 0]) / S; y = (R[1, 2] + R[2, 1]) / S; z = 0.25 * S
    return np.array([w, x, y, z])

def qmul(a, b):
    w1, x1, y1, z1 = a; w2, x2, y2, z2 = b
    return np.array([w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2, w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2, w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2, w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2])
