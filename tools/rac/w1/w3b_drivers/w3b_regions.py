# RAC W3B named scale-field regions on the canonical W2 upsampled surface (vertex masks). Membership is read from the canonical W2 region
# fields (FAM: 1 structural / protective, 2 articulation / transition, 3 fine expressive, 4 ventral, 5 contact) and located with the W2
# construction points (tools/rodin/w2/g7geo_w2_points.json) / the head-local skull frame. Roles and boundaries are the canonical ones;
# these masks only NAME representative parts of each field for measurement and testing.
import os, sys, json, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import w3b_common as C, w3b_scale as SC
G = json.load(open('/home/claude/wayfarer-design/tools/rodin/w2/g7geo_w2_points.json'))['points']
def segd(V, a, b):
    a = np.asarray(a, float); b = np.asarray(b, float); v = b - a; t = np.clip(((V - a) @ v) / (v @ v), 0, 1); return np.linalg.norm(V - (a + t[:, None] * v), axis=1), t
_M = None
def masks():
    global _M
    if _M is not None: return _M
    Z = SC.ref(); V = Z['Vu']; FAM = Z['FAM']; N = Z['N']; x, f, u = V.T; ax = np.abs(x); sg = np.where(x >= 0, 1, -1)
    Lh = C.head_local(V); Xa = np.abs(Lh[:, 0]); hd = (u > 170) & (ax < 12) & (f > -14)
    import w3b_head as HD
    eye = np.array([C.head_world(np.array([[s * C.EYE0['x'], C.EYE0['f'], C.EYE0['u']]]))[0] for s in (1, -1)])
    de = np.minimum(np.linalg.norm(V - eye[0], axis=1), np.linalg.norm(V - eye[1], axis=1)); ER = C.EYE0['r'] * C.HS
    seam = np.full(len(V), 99.0); hh = np.where(hd)[0]; seam[hh] = np.abs(Lh[hh, 2] - HD.seam_u(Lh[hh, 1]))
    M = {}
    # ---- face (RM-UF-04)
    M['face_orbital_eyelid'] = hd & (FAM == 3) & (de < 2.1 * ER)
    M['face_mouth_margin'] = hd & (FAM == 3) & (seam < 0.75) & (Lh[:, 1] > 0.5) & (Xa > 0.6)
    M['face_rostrum_cheek'] = hd & (FAM == 3) & (Lh[:, 1] > 3.5) & (Lh[:, 1] < 11.5) & (Lh[:, 2] > 0.4) & (Lh[:, 2] < 3.6) & (Xa > 1.6) & (de > 2.1 * ER) & (seam > 0.75)
    rict = np.array([4.7, -0.6, -0.85])
    M['face_jaw_corner'] = hd & ((FAM == 3) | (FAM == 2)) & (np.linalg.norm(np.c_[Xa, Lh[:, 1], Lh[:, 2]] - rict, axis=1) < 1.8)
    M['face_auricular'] = hd & (Z['TYM'] > 0.05)
    M['face_throat_upper_neck'] = (u > 158) & (u < 176) & (f > 0) & ((FAM == 4) | (FAM == 2)) & (ax < 9)
    M['face_cranial_structural'] = hd & (FAM == 1) & (u > 176)
    # ---- body structural / protective (RM-UB-08)
    dors = N[:, 1] < -0.35
    M['S_upper_posterior_neck'] = (FAM == 1) & (u > 160) & (u < 177) & dors & (ax < 9)
    M['S_dorsal_trunk'] = (FAM == 1) & (u > 115) & (u < 158) & dors & (ax < 16)
    M['S_lateral_trunk'] = (FAM == 1) & (u > 100) & (u < 140) & (np.abs(N[:, 0]) > 0.7) & (ax < 22)
    tail = (f < -26) & (u > 40)
    M['S_dorsal_tail'] = (FAM == 1) & tail & (N[:, 2] > 0.3)
    fo = np.zeros(len(V), bool); sh = np.zeros(len(V), bool); hdors = np.zeros(len(V), bool); fdors = np.zeros(len(V), bool)
    el = np.zeros(len(V), bool); wr = np.zeros(len(V), bool); ax_ = np.zeros(len(V), bool); kn = np.zeros(len(V), bool); an = np.zeros(len(V), bool)
    palm = np.zeros(len(V), bool); sole = np.zeros(len(V), bool)
    for k, s in (('1', 1), ('-1', -1)):
        A = G[k]['ARM']; Lg = G[k]['LEG']; m = sg == s
        d2, t2 = segd(V, A['E'], A['W']); fo |= m & (FAM == 1) & (d2 < 7) & (t2 > 0.2) & (t2 < 0.8)
        dk, tk = segd(V, Lg['K'], Lg['A']); sh |= m & (FAM == 1) & (dk < 9) & (tk > 0.15) & (tk < 0.8) & (N[:, 1] > 0.3)
        Wp = np.array(A['W']); hdors |= m & (FAM == 1) & (np.linalg.norm(V - Wp, axis=1) < 22) & (u < Wp[2] - 2)
        fdors |= m & (FAM == 1) & (u < 10) & (np.linalg.norm(V[:, :2] - np.array(Lg['A'][:2]), axis=1) < 30)
        el |= m & (FAM == 2) & (np.linalg.norm(V - np.array(A['E']), axis=1) < 6)
        wr |= m & (FAM == 2) & (np.linalg.norm(V - Wp, axis=1) < 4.5)
        d1, t1 = segd(V, A['S'], A['E']); ax_ |= m & (FAM == 2) & (d1 < 12) & (t1 < 0.2) & (u < 152) & (u > 132)
        kn |= m & (FAM == 2) & (np.linalg.norm(V - np.array(Lg['K']), axis=1) < 8)
        an |= m & (FAM == 2) & (np.linalg.norm(V - np.array(Lg['A']), axis=1) < 7.5) & (u > 4)
        palm |= m & (FAM == 5) & (u > 60); sole |= m & (FAM == 5) & (u < 12)
    M['S_forearm'] = fo; M['S_shin'] = sh; M['S_dorsal_hand'] = hdors; M['S_dorsal_foot'] = fdors
    # ---- articulation / transition
    M['A_neck_flexion'] = (FAM == 2) & (u > 150) & (u < 170) & ~dors
    M['A_axilla'] = ax_; M['A_elbow'] = el; M['A_wrist'] = wr
    M['A_lower_trunk_flexion'] = (FAM == 2) & (u > 94) & (u < 108) & (ax < 18)
    M['A_hip_crease'] = (FAM == 2) & (u > 70) & (u < 94) & (ax < 16) & (f > -14)
    M['A_knee'] = kn; M['A_ankle'] = an
    M['A_tail_articulation'] = (FAM == 2) & (f < -14) & (f > -40) & (u > 70) & (u < 104)
    # ---- ventral / contact
    M['V_throat_anterior_neck'] = (FAM == 4) & (u > 150) & (u < 172)
    M['V_chest_abdomen'] = (FAM == 4) & (u > 100) & (u < 150)
    M['V_tail_underside'] = (FAM == 4) & tail
    M['C_palmar'] = palm; M['C_plantar'] = sole
    _M = M; return M
CLASS = {'face': [k for k in ['face_orbital_eyelid', 'face_mouth_margin', 'face_rostrum_cheek', 'face_jaw_corner', 'face_auricular', 'face_throat_upper_neck', 'face_cranial_structural']],
         'structural': ['S_upper_posterior_neck', 'S_dorsal_trunk', 'S_lateral_trunk', 'S_dorsal_tail', 'S_forearm', 'S_shin', 'S_dorsal_hand', 'S_dorsal_foot'],
         'articulation': ['A_neck_flexion', 'A_axilla', 'A_elbow', 'A_wrist', 'A_lower_trunk_flexion', 'A_hip_crease', 'A_knee', 'A_ankle', 'A_tail_articulation'],
         'ventral': ['V_throat_anterior_neck', 'V_chest_abdomen', 'V_tail_underside'], 'contact': ['C_palmar', 'C_plantar']}
# adjacent structural reference for the hierarchy guard (fine / articulation must stay finer than the structural field they border)
ADJ = {'face_orbital_eyelid': 'face_cranial_structural', 'face_mouth_margin': 'face_cranial_structural', 'face_rostrum_cheek': 'face_cranial_structural',
       'face_jaw_corner': 'face_cranial_structural', 'face_auricular': 'face_cranial_structural', 'face_throat_upper_neck': 'S_upper_posterior_neck',
       'A_neck_flexion': 'S_upper_posterior_neck', 'A_axilla': 'S_lateral_trunk', 'A_elbow': 'S_forearm', 'A_wrist': 'S_forearm', 'A_lower_trunk_flexion': 'S_lateral_trunk',
       'A_hip_crease': 'S_lateral_trunk', 'A_knee': 'S_shin', 'A_ankle': 'S_shin', 'A_tail_articulation': 'S_dorsal_tail',
       'C_palmar': 'S_dorsal_hand', 'C_plantar': 'S_dorsal_foot'}
