# sw_dqs.py CONFIG.json WEIGHTS.npz OUTDIR POSE1,POSE2,... : Track S2 (order 28dd8d3 §16) local volume-preserving field for the shoulder = a bounded
# blend of linear-blend and dual-quaternion skinning (the production mechanism behind Blender's armature "Preserve Volume" with a vertex-group mix):
#   X = (1 - b) * LBS + b * DQS,   b = C2 bump of the rest distance to the GH centre (1 inside R_core, 0 at R_out) on arm_s / axial vertices,
# optionally restricted to the shoulder bones' influence (b *= share of the girdle columns). Same weights, same pose matrices; vertices with b = 0 are
# the LBS result bit-for-bit. Writes OUTDIR/<pose>.npz (V in source cm), consumed by diag_run.py through VSRC=OUTDIR, plus OUTDIR/blend_mask.npy.
# POSE_JSON (diag_lib) applies as usual (S1 mechanics).
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '/tmp/claude-0/rt')
from common import PARTS
from diag_lib import Rig, build_poses, src_to_bl, bl_to_src
CF, WF, O, PL = sys.argv[1:5]; CFG = json.load(open(CF)); os.makedirs(O, exist_ok=True)
RD = '/tmp/claude-0/rt/rd'; rig = Rig(RD + '/rig/rig_v001.json', WF); P = build_poses(rig)
Z = np.load('/tmp/claude-0/rt/frz/v003_frz.npz'); V0 = Z['V'].astype(float); Q = np.asarray(Z['Q']); FP = Z['FP']; nV = len(V0)
vpart = np.empty(nV, object); vpart[Q.ravel()] = np.repeat(np.array(PARTS, object)[FP], 4)
LM = json.load(open(RD + '/out/GR_U_REF_RP2_rigprep_landmarks_v002.json'))['joints']
c2 = lambda t: (lambda u: u * u * u * (u * (6 * u - 15) + 10))(np.clip(t, 0, 1))
b = np.zeros(nV)
for s in CFG['sides']:
    gh = np.array(LM['glenohumeral_' + s]['position_source_frame_cm']); d = np.linalg.norm(V0 - gh, axis=1)
    b = np.maximum(b, CFG.get('strength', 1.0) * c2((CFG['R_out'] - d) / (CFG['R_out'] - CFG['R_core'])) * np.isin(vpart, ['arm_' + s, 'axial']))
if CFG.get('girdle_share'):
    gcols = [i for i, n in enumerate(rig.names) if n.split('_')[0] in ('clavicle', 'scapula', 'upperarm')]
    b *= np.clip(rig.W[:, gcols].sum(1) / np.maximum(rig.W.sum(1), 1e-12) / CFG.get('share_full', 0.5), 0, 1)
np.save(O + '/blend_mask.npy', b.astype(np.float32)); act = np.nonzero(b > 0)[0]
def quat(R):
    w = np.sqrt(max(0.0, 1 + R[0, 0] + R[1, 1] + R[2, 2])) / 2; x = np.sqrt(max(0.0, 1 + R[0, 0] - R[1, 1] - R[2, 2])) / 2
    y = np.sqrt(max(0.0, 1 - R[0, 0] + R[1, 1] - R[2, 2])) / 2; z = np.sqrt(max(0.0, 1 - R[0, 0] - R[1, 1] + R[2, 2])) / 2
    x = np.copysign(x, R[2, 1] - R[1, 2]); y = np.copysign(y, R[0, 2] - R[2, 0]); z = np.copysign(z, R[1, 0] - R[0, 1]); q = np.array([w, x, y, z]); return q / np.linalg.norm(q)
def qmul(a, b_):
    w1, x1, y1, z1 = a.T; w2, x2, y2, z2 = b_.T
    return np.stack([w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2, w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2, w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2, w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2], -1)
Wn = rig.W / rig.tot[:, None]; Vb0 = src_to_bl(V0)
for pn in PL.split(','):
    Xb, L, M = rig.skin(Vb0, P[pn]); _, S = rig.pose_mats(P[pn])
    nb = len(rig.names); Qr = np.zeros((nb, 4)); Qd = np.zeros((nb, 4))
    for i, n in enumerate(rig.names):
        R = S[n][:3, :3]; t = S[n][:3, 3]; q = quat(R); Qr[i] = q; Qd[i] = 0.5 * qmul(np.r_[0, t][None], q[None])[0]
    Wa = Wn[act]; dom = Wa.argmax(1); sg = np.sign((Qr[None, :, :] * Qr[dom][:, None, :]).sum(-1)); sg[sg == 0] = 1
    qr = np.einsum('vb,vb,bk->vk', Wa, sg, Qr); qd = np.einsum('vb,vb,bk->vk', Wa, sg, Qd); nr = np.linalg.norm(qr, axis=1)[:, None]; qr /= nr; qd /= nr
    w, x, y, z = qr.T; p = Vb0[act]
    Rm = np.stack([np.stack([1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y)], -1), np.stack([2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x)], -1),
                   np.stack([2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)], -1)], -2)
    tq = 2 * qmul(qd, qr * np.array([1, -1, -1, -1]))[:, 1:]
    Xd = np.einsum('vij,vj->vi', Rm, p) + tq
    Xo = Xb.copy(); Xo[act] = (1 - b[act, None]) * Xb[act] + b[act, None] * Xd
    np.savez_compressed('%s/%s.npz' % (O, pn), V=bl_to_src(Xo).astype(np.float32))
print(json.dumps(dict(blend_vertices=int(len(act)), max_b=float(b.max()))))
