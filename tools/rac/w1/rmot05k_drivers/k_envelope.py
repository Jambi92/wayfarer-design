# RAC RM-OT-05K Branch A: bounded external body-envelope revision over the accepted Gorrund skeleton (order §5-§7).
# Applies ONE smooth, documented skin-level field to the trunk flanks of an S-series sculpt (default: S4, which carries the S4 cue work, §8):
#   lateral (x) inward displacement of the trunk skin, peaking at the lower axial trunk (lumbar, ALPC S4 level), decaying to zero at the
#   hip-joint level below and over the lower costal contour into the deep upper rib cage above. Anterior / posterior midline untouched
#   (depth is not added: no belly, no barrel); hands, arms, legs, head untouched (arm weight < 0.05 only); skeleton untouched.
# Strength A (cm at the flank, at the lumbar peak) is the only parameter varied between candidates (EA1 / EA2 / EA3).
# Usage: python3 k_envelope.py IN.obj OUT.obj A        -> writes OUT.obj and prints skin ALPC stations / rows vs MF and Skarn
#        python3 k_envelope.py IN.obj - 0              -> stations only
import os, sys, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/rmot05f_drivers')
from f_common import *
import bony_envelope as BE
Z_HIP, Z_PEAK0, Z_PEAK1, Z_TOP = 128.0, 139.0, 144.0, 163.0     # cm, reference frame; S5 crest 133.2, S4 lumbar 141.9, S3 150.6, hip joints ~118
FLOOR_MARGIN = 0.35                                                   # cm
LEV = {'S2b': 8, 'S2d': 5, 'S4': 4}                                 # accepted skeleton-anchored station levels (05F stations.json)
REF = REPO + '/reviews/reference-assets/builds'
def g(z):
    up = np.clip((z - Z_HIP) / (Z_PEAK0 - Z_HIP), 0, 1); dn = np.clip((Z_TOP - z) / (Z_TOP - Z_PEAK1), 0, 1)
    return np.where(z < Z_PEAK0, 0.5 - 0.5 * np.cos(np.pi * up), np.where(z > Z_PEAK1, 0.5 - 0.5 * np.cos(np.pi * dn), 1.0))
def field(V, B, A):
    keep = B['keep'].astype(bool)[:NBODY]; w = lambda k: B['w_' + k][:NBODY].astype(float)
    armw = np.maximum.reduce([w(x) for x in ('upperarm_l', 'upperarm_r', 'lowerarm_l', 'lowerarm_r', 'hand_l', 'hand_r', 'fingers_l', 'fingers_r')])
    legw = np.maximum.reduce([w(x) for x in ('thigh_l', 'thigh_r')])
    tr = keep & (armw < 0.05)
    out = V.copy(); z = V[:, 2]; gz = g(z)
    hw = np.zeros(len(V))
    for zc in np.arange(115, 160, 1.0):
        m = tr & (np.abs(z - zc) < 0.6)
        if m.sum() > 5: hw[tr & (np.abs(z - zc) <= 0.5)] = np.abs(V[m, 0]).max()
    lat = np.clip((np.abs(V[:, 0]) / np.maximum(hw, 1e-6) - 0.35) / 0.5, 0, 1); lat = lat * lat * (3 - 2 * lat)
    s = A * gz * lat * (1 - 0.5 * np.clip(legw, 0, 1)) * tr
    # true-floor clamp (05F I5: no vertex inside the true skeletal floor; bony landmarks such as the ASIS stay subcutaneous): the
    # inward step is limited so the signed floor distance stays >= FLOOR_MARGIN, then the limited field is smoothed and re-clamped
    Fl = read_obj(HANDOFF + '/template/GO_true_floor_r6.obj')[0]; Fk = B['F']; Fk = Fk[(Fk < NBODY).all(1)]
    n = np.zeros_like(Fl); fn = np.cross(Fl[Fk[:, 1]] - Fl[Fk[:, 0]], Fl[Fk[:, 2]] - Fl[Fk[:, 0]])
    for k in range(3): np.add.at(n, Fk[:, k], fn)
    n /= np.maximum(np.linalg.norm(n, axis=1), 1e-9)[:, None]
    if np.einsum('ij,ij->i', Fl[Fk[:, 0]], np.cross(Fl[Fk[:, 1]], Fl[Fk[:, 2]])).sum() < 0: n = -n
    sd = np.einsum('ij,ij->i', V - Fl, n); nx = np.maximum(n[:, 0] * np.sign(V[:, 0]), 0.2)
    lim = lambda s_: np.minimum(s_, np.maximum(0, (sd - FLOOR_MARGIN) / nx) * (sd > FLOOR_MARGIN) + np.where(sd <= FLOOR_MARGIN, 0, 0))
    s = lim(s)
    E = np.vstack([Fk[:, [0, 1]], Fk[:, [1, 2]], Fk[:, [2, 0]]]); deg = np.bincount(E.ravel(), minlength=len(V)).astype(float)
    for _ in range(6):
        acc = np.zeros(len(V)); np.add.at(acc, E[:, 0], s[E[:, 1]]); np.add.at(acc, E[:, 1], s[E[:, 0]])
        s = lim(np.where(tr, 0.5 * s + 0.5 * acc / np.maximum(deg, 1), 0))
    out[:, 0] = V[:, 0] - np.sign(V[:, 0]) * s
    return out, s
def stations(Vb, B, J):
    Vf = np.load(CG.path(SKELETON_BODY) + '_r6.npz', allow_pickle=True)['V'].astype(float).copy(); Vf[:NBODY] = Vb
    d = {'V': Vf, 'keep': B['keep'], 'joints': J, 'F': B['F']}
    for k in B.files:
        if k.startswith('w_'): d[k] = B[k]
    return BE.fast_stations(d, levels=LEV)
def rows(st):
    MF = json.load(open(REF + '/MF-M-R_meas.json'))['combined']['ratio']; SK = json.load(open(REF + '/SK_meas.json'))['combined']['ratio']
    b = lambda s: st[s][0]; dd = lambda s: st[s][1]
    r = {'S3_over_S2_b': b('S3') / b('S2'), 'S4_over_S2_b': b('S4') / b('S2'), 'S4_over_S2_d': dd('S4') / dd('S2'), 'S5_over_S2_b': b('S5') / b('S2'),
         'S6_over_S2_b': b('S6') / b('S2'), 'S5_over_S4_b': b('S5') / b('S4'), 'S6_over_S4_b': b('S6') / b('S4'), 'pelvic_depth_over_thorax_depth': dd('S6') / dd('S2')}
    out = {}
    def add(k, op, ref, lab):
        va, vb = r[k], ref[k]; rel = abs(va - vb) / vb
        hold = {'>': va > vb, '>=': va >= vb, '<=': va <= vb}[op]
        res = (('PASS' if rel >= 0.01 else 'NOT DEMONSTRATED') if hold else 'FAIL') if op == '>' else ('PASS' if hold else ('MARGINAL' if rel < 0.01 else 'FAIL'))
        out['%s %s %s %s' % (lab, k, op, 'MF' if ref is MF else 'SK')] = [round(va, 3), round(vb, 3), res]
    for k in ('S3_over_S2_b', 'S4_over_S2_b', 'S4_over_S2_d'): add(k, '>', MF, 'ALPC-1')
    for k in ('S5_over_S2_b', 'S6_over_S2_b', 'pelvic_depth_over_thorax_depth'): add(k, '>=', MF, 'ALPC-2a')
    for k in ('S5_over_S4_b', 'S6_over_S4_b'): add(k, '<=', MF, 'ALPC-2b')
    for k in ('S3_over_S2_b', 'S4_over_S2_b', 'S4_over_S2_d', 'S5_over_S2_b', 'S6_over_S2_b', 'pelvic_depth_over_thorax_depth'): add(k, '>', SK, 'ALPC-7')
    bb = [b('S%d' % k) for k in range(2, 7)]
    out['ALPC-0 shape (S2>=S3>=S4<S5<=S6, S4<S2)'] = [bb, None, 'PASS' if (bb[0] >= bb[1] >= bb[2] and bb[2] < bb[3] <= bb[4] and bb[2] < bb[0]) else 'FAIL']
    return out
if __name__ == '__main__':
    src, dst, A = sys.argv[1], sys.argv[2], float(sys.argv[3])
    V0, B, L, J, f, z0 = route_state(SKELETON_BODY); Vs, Fs = read_obj(src)
    Vn, s = field(Vs, B, A)
    if dst != '-':
        write_obj(dst, Vn, B['F'], 'RAC RM-OT-05K Branch A envelope candidate: k_envelope.py %s A=%.2f cm (lumbar-peak flank inward field)' % (os.path.basename(src), A))
    st = stations(Vn, B, J); R = rows(st)
    print(json.dumps({'A_cm': A, 'moved_vertices': int((s > 0.01).sum()), 'max_cm': round(float(s.max()), 3),
                      'skin_stations': {k: [round(x, 2) for x in v] for k, v in st.items()}, 'rows': R}, indent=1))
