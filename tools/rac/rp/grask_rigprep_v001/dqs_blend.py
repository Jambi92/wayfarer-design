# dqs_blend.py : shared LBS / DQS preserve-volume blend (same maths as sw_dqs.py, order 28dd8d3 §16) as a function, so a rest-space shape key D can be
# evaluated through the SW3 skinning:  X(D) = (1 - b) * LBS(V0 + D) + b * DQS(V0 + D)   (source cm in / out).
import numpy as np
from diag_lib import src_to_bl, bl_to_src
def _quat(R):
    w = np.sqrt(max(0.0, 1 + R[0, 0] + R[1, 1] + R[2, 2])) / 2; x = np.sqrt(max(0.0, 1 + R[0, 0] - R[1, 1] - R[2, 2])) / 2
    y = np.sqrt(max(0.0, 1 - R[0, 0] + R[1, 1] - R[2, 2])) / 2; z = np.sqrt(max(0.0, 1 - R[0, 0] - R[1, 1] + R[2, 2])) / 2
    x = np.copysign(x, R[2, 1] - R[1, 2]); y = np.copysign(y, R[0, 2] - R[2, 0]); z = np.copysign(z, R[1, 0] - R[0, 1]); q = np.array([w, x, y, z]); return q / np.linalg.norm(q)
def _qmul(a, b_):
    w1, x1, y1, z1 = a.T; w2, x2, y2, z2 = b_.T
    return np.stack([w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2, w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2, w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2, w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2], -1)
def blend_pose(rig, Vsrc, pose, b):
    """returns (X source cm, Lin (n,3,3) LBS linear part in the Blender frame)"""
    Vb = src_to_bl(Vsrc); Xb, L, M = rig.skin(Vb, pose); _, S = rig.pose_mats(pose); act = np.nonzero(b > 0)[0]
    if len(act):
        nb = len(rig.names); Qr = np.zeros((nb, 4)); Qd = np.zeros((nb, 4))
        for i, n in enumerate(rig.names):
            q = _quat(S[n][:3, :3]); Qr[i] = q; Qd[i] = 0.5 * _qmul(np.r_[0, S[n][:3, 3]][None], q[None])[0]
        Wa = (rig.W / rig.tot[:, None])[act]; dom = Wa.argmax(1); sg = np.sign((Qr[None, :, :] * Qr[dom][:, None, :]).sum(-1)); sg[sg == 0] = 1
        qr = np.einsum('vb,vb,bk->vk', Wa, sg, Qr); qd = np.einsum('vb,vb,bk->vk', Wa, sg, Qd); nr = np.linalg.norm(qr, axis=1)[:, None]; qr /= nr; qd /= nr
        w, x, y, z = qr.T; p = Vb[act]
        Rm = np.stack([np.stack([1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y)], -1), np.stack([2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x)], -1),
                       np.stack([2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)], -1)], -2)
        Xd = np.einsum('vij,vj->vi', Rm, p) + 2 * _qmul(qd, qr * np.array([1, -1, -1, -1]))[:, 1:]
        Xb = Xb.copy(); Xb[act] = (1 - b[act, None]) * Xb[act] + b[act, None] * Xd
        L = L.copy(); L[act] = (1 - b[act, None, None]) * L[act] + b[act, None, None] * Rm
    return bl_to_src(Xb), L
