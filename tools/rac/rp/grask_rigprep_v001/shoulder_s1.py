# shoulder_s1.py CONFIG.json OUTDIR : Track S (order 69f2660 §14) S1 diagnostic shoulder-girdle mechanics. Writes OUTDIR/pose_S1.json (diag_lib POSE_JSON)
# and OUTDIR/kinematics_S1.json (+ the same kinematics for W0). Uses ONLY the existing v002 landmark architecture of the diagnostic rig:
#   SC = clavicle head, GH = clavicle tail = upperarm head (unchanged; GH stays tied to the accepted centre), scapula bone = medial proxy -> acromion (child of the clavicle).
# Rule (simple, reproducible, diagnostic only -- not production anatomy). For each D1 pose the humeral elevation from the stance, e, is read from the W0 pose:
#   scapulothoracic share  ST(e) = st_ratio * max(0, e - st_onset_deg)                       (classic ~2:1 GH:ST rhythm after ~30 deg -> ratio 1/3)
#   clavicle elevation     = clav_elev_frac * ST about the clavicle axis that raises its tail (the GH)
#   clavicle protraction   = clav_prot_frac * ST for flexion poses (tail forward), 0 for abduction
#   scapula upward rotation= scap_uprot_frac * ST about the scapula axis that drops the medial border root, pivoting at the ACROMION (tail fixed: pose
#                            location t = (I - R)(0, L, 0)), so the inferior angle swings laterally / up and the acromion-GH link is not broken
#   upperarm               = local rotation re-solved (two local axes, least squares) so the WORLD humeral direction equals the W0 pose exactly
# Extension (ext30) has e <= 0 -> ST = 0 -> the pose is bit-identical to W0 (rest / low-angle sanity). Girdle variants use the same rule with their own W0
# humeral direction (the W0 girdle clavicle rotation is replaced by the rule).
import sys, os, json, numpy as np
from scipy.optimize import least_squares
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from diag_lib import Rig, build_poses, rotm, bl_to_src, src_to_bl, bl_dir, UP, FWD, LEFT
CF, O = sys.argv[1:3]; CFG = json.load(open(CF)); os.makedirs(O, exist_ok=True)
RD = '/tmp/claude-0/rt/rd'; rig = Rig(RD + '/rig/rig_v001.json', RD + '/rig/weights_v001c.npz'); P = build_poses(rig)
LM = json.load(open(RD + '/out/GR_U_REF_RP2_rigprep_landmarks_v002.json'))['joints']
src = lambda v: bl_to_src(np.asarray(v, float)[None])[0]
def world(pose):
    M, S = rig.pose_mats(pose); return M, S
def hum_dir(M, s):
    h = M['upperarm_' + s][:3, 3]; t = M['upperarm_' + s] @ np.r_[0, np.linalg.norm(np.array(rig.B['upperarm_' + s]['tail']) - np.array(rig.B['upperarm_' + s]['head'])), 0, 1]
    d = t[:3] - h; return d / np.linalg.norm(d)
def scap_pose(s, ang):
    """scapula local rotation about the TAIL (acromion): choose the local axis/sign that moves the head (medial root) most downward"""
    L = np.linalg.norm(np.array(rig.B['scapula_' + s]['tail']) - np.array(rig.B['scapula_' + s]['head'])); best = None
    for ax in ('X', 'Z'):
        for sg in (1, -1):
            R = rotm(ax, 10 * sg); t = (np.eye(3) - R) @ np.array([0, L, 0]); M, _ = world({'scapula_' + s: [(ax, 10 * sg), ('T', t.tolist())]})
            dz = (M['scapula_' + s][:3, 3] - rig.rest['scapula_' + s][:3, 3])[2]
            if best is None or dz < best[0]: best = (dz, ax, sg)
    _, ax, sg = best; R = rotm(ax, sg * ang); t = (np.eye(3) - R) @ np.array([0, L, 0])
    return [(ax, sg * ang), ('T', t.tolist())], (ax, sg)
OUT = {}; KIN = {}
for s, sg in (('l', 1), ('r', -1)):
    ax_c, s_c = rig.choose('clavicle_' + s, bl_dir(UP), ('X', 'Z')); ax_p, s_p = rig.choose('clavicle_' + s, bl_dir(FWD), ('X', 'Z'))
    d_rest = hum_dir(rig.rest, s)
    for nm in ('abd45', 'abd90', 'flex90', 'ext30', 'abd90_girdle', 'flex90_girdle'):
        pn = 'D1_%s_%s' % (s, nm); M0, _ = world(P[pn]); target = hum_dir(M0, s)
        e = np.degrees(np.arccos(np.clip(-target[2], -1, 1)))                                 # humeral elevation from straight down (Blender z up)
        flex = 'flex' in nm; ext = 'ext' in nm
        ST = 0.0 if ext else CFG['st_ratio'] * max(0.0, e - CFG['st_onset_deg'])
        pose = {}
        if ST > 0:
            pose['clavicle_' + s] = [(ax_c, s_c * CFG['clav_elev_frac'] * ST)] + ([(ax_p, s_p * CFG['clav_prot_frac'] * ST)] if flex and CFG['clav_prot_frac'] else [])
            sc_ent, scax = scap_pose(s, CFG['scap_uprot_frac'] * ST); pose['scapula_' + s] = sc_ent
            ua = P[pn]['upperarm_' + s]; ax1 = ua[0][0]; ax2 = 'Z' if ax1 == 'X' else 'X'
            def f(x): M, _ = world(dict(pose, **{'upperarm_' + s: [(ax1, x[0]), (ax2, x[1])]})); return hum_dir(M, s) - target
            r = least_squares(f, [ua[0][1], 0.0]); pose['upperarm_' + s] = [(ax1, float(r.x[0])), (ax2, float(r.x[1]))]
            OUT[pn] = {b: [[a, d] for a, d in L] for b, L in pose.items()}
            MS, _ = world(pose)
        else:
            MS = M0                                                                            # no girdle motion: the W0 pose definition is kept (bit-identical)
        for tg, M in (('W0', M0), ('S1', MS)):
            gh = src(M['upperarm_' + s][:3, 3]); ac = src(M['scapula_' + s][:3, 3] + M['scapula_' + s][:3, :3] @ np.array([0, np.linalg.norm(np.array(rig.B['scapula_' + s]['tail']) - np.array(rig.B['scapula_' + s]['head'])), 0]))
            sc_ = src(M['clavicle_' + s][:3, 3]); med = src(M['scapula_' + s][:3, 3])
            pinf = np.array(LM['scapular_inferior_proxy_' + s]['position_source_frame_cm']); pinf_bl = src_to_bl(pinf[None])[0]
            inf = src((M['scapula_' + s] @ np.linalg.inv(rig.rest['scapula_' + s]) @ np.r_[pinf_bl, 1])[:3])
            hd = hum_dir(M, s); scap_x = M['scapula_' + s][:3, :3]; clv = M['clavicle_' + s][:3, 1]
            rest_clv = rig.rest['clavicle_' + s][:3, 1]; rest_sc = rig.rest['scapula_' + s][:3, :3]
            KIN.setdefault(pn, {})[tg] = dict(
                humeral_elevation_deg=round(float(np.degrees(np.arccos(np.clip(-hd[2], -1, 1)))), 2),
                glenohumeral_motion_deg=round(float(np.degrees(np.arccos(np.clip((scap_x.T @ hd) @ (rest_sc.T @ d_rest), -1, 1)))), 2),   # humerus relative to the scapula frame
                humeral_dir_err_deg=round(float(np.degrees(np.arccos(np.clip(hd @ target, -1, 1)))), 4),
                scapulothoracic_share_deg=round(ST if tg == 'S1' else 0.0, 2),
                clavicle_rotation_deg=round(float(np.degrees(np.arccos(np.clip(clv @ rest_clv, -1, 1)))), 2),
                scapula_rotation_deg=round(float(np.degrees(np.arccos(np.clip((np.trace(rest_sc.T @ scap_x) - 1) / 2, -1, 1)))), 2),
                GH_cm=np.round(gh, 2).tolist(), GH_disp_cm=round(float(np.linalg.norm(gh - src(rig.rest['upperarm_' + s][:3, 3]))), 2),
                acromion_cm=np.round(ac, 2).tolist(), GH_acromion_dist_cm=round(float(np.linalg.norm(ac - gh)), 3),
                humerus_vs_acromion_deg=round(float(np.degrees(np.arccos(np.clip(hd @ ((ac - gh) / np.linalg.norm(ac - gh) * np.array([1, -1, 1])), -1, 1)))), 2),
                SC_cm=np.round(sc_, 2).tolist(), scapula_medial_cm=np.round(med, 2).tolist(), scapula_inferior_cm=np.round(inf, 2).tolist(),
                scapula_inferior_disp_cm=np.round(inf - pinf, 2).tolist(), scapula_medial_disp_cm=np.round(med - np.array(LM['scapula_medial_proxy_' + s]['position_source_frame_cm']), 2).tolist())
json.dump(OUT, open(O + '/pose_S1.json', 'w'), indent=1); json.dump(dict(config=CFG, kinematics=KIN), open(O + '/kinematics_S1.json', 'w'), indent=1)
for k, v in KIN.items(): print(k, 'W0', {a: v['W0'][a] for a in ('humeral_elevation_deg', 'glenohumeral_motion_deg', 'GH_disp_cm')}, 'S1', {a: v['S1'][a] for a in ('humeral_elevation_deg', 'humeral_dir_err_deg', 'scapulothoracic_share_deg', 'clavicle_rotation_deg', 'scapula_rotation_deg', 'glenohumeral_motion_deg', 'GH_disp_cm', 'scapula_inferior_disp_cm')})
