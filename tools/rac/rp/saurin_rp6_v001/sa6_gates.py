# sa6_gates.py : RP6 special-gate pose definitions (order a407015 §13-§16) + gate metrics.  Same spec format as sa6_pose (bone, pivot, axis, deg); sagittal
#   signs anatomical (+y anterior).  No new biological mobility: jaw = single hinge (no lateral / protrusion motion: not supported by the accepted anatomy),
#   cranial display rigid with the head.  Sign check (rot(axis, +deg) right-handed): about +X, +deg turns +z toward -y -> head pitch UP, jaw CLOSE, tail DOWN,
#   ankle (foot pointing +y) toward +z -> DORSI-flexion; toe flex = toward -z.
import numpy as np
import sa6_common as C
X, Y, Z = np.eye(3)
def tail_dist(R, axis_fn, total, joints):
    js = list(joints); return [('tail_%02d' % k, R.H('tail_%02d' % k), axis_fn(k), total / len(js)) for k in js]
def gate_poses(R):
    G = {}; tb = lambda k: R.Tl('tail_%02d' % k) - R.H('tail_%02d' % k)
    # ---- tail (16 joints) ----
    for A in (45, 90, 135): G['tail_lat_%d' % A] = tail_dist(R, lambda k: Z, A, range(1, 17))
    G['tail_up_60'] = tail_dist(R, lambda k: X, -60, range(1, 17)); G['tail_down_60'] = tail_dist(R, lambda k: X, 60, range(1, 17))
    G['tail_S_curve'] = tail_dist(R, lambda k: Z, 40, range(1, 9)) + tail_dist(R, lambda k: Z, -40, range(9, 17))
    G['tail_twist_dist_90'] = tail_dist(R, tb, 90, range(1, 17))
    G['tail_combined'] = tail_dist(R, lambda k: Z, 90, range(1, 17)) + tail_dist(R, lambda k: X, -30, range(1, 17)) + tail_dist(R, tb, 45, range(1, 17))
    G['tail_root_biased_60'] = tail_dist(R, lambda k: Z, 60, range(1, 5)); G['tail_mid_biased_60'] = tail_dist(R, lambda k: Z, 60, range(6, 11))
    G['tail_distal_60'] = tail_dist(R, lambda k: Z, 60, range(12, 17))
    # ---- hands ----
    for s, sg in (('xpos', 1), ('xneg', -1)):
        t = C.side_tag(s); pal = R.palm_normal(s)
        curl = lambda a: sum([R.digit_flex(s, k, a) for k in range(1, 5)], [])
        G['hand_open_' + s] = curl((-15, 0, 0)) + R.digit_flex(s, 0, (-10, 0, 0), True)
        G['hand_relaxed_curl_' + s] = curl((25, 30, 20)) + R.digit_flex(s, 0, (10, 10, 5), True)
        tips = np.array([R.Tl('finger_%d_03_%s' % (k, t)) for k in range(1, 5)] + [R.Tl('thumb_03_' + t)]); hl = tips.mean(0) - R.H('hand_' + t)
        G['hand_broad_grasp_' + s] = curl((20, 30, 15)) + [('thumb_01_' + t, R.H('thumb_01_' + t), hl, -sg * 30)] + R.digit_flex(s, 0, (10, 10, 5), True)   # thumb: partial opposition
        opp = [('thumb_01_' + t, R.H('thumb_01_' + t), hl, -sg * 50)] + R.digit_flex(s, 0, (30, 25, 20), True)
        for k in range(1, 5): G['hand_opposition_f%d_%s' % (k, s)] = opp + R.digit_flex(s, k, (75, 95, 60))      # target finger fully curled toward the thumb
        mid = 0.5 * (R.H('finger_2_01_' + t) + R.H('finger_3_01_' + t))
        spl = []
        for k in range(1, 5):
            dvec = R.H('finger_%d_01_%s' % (k, t)) - mid; ax = pal * np.sign(np.cross(R.Tl('finger_%d_01_%s' % (k, t)) - R.H('finger_%d_01_%s' % (k, t)), dvec) @ pal)
            spl.append(('finger_%d_01_%s' % (k, t), R.H('finger_%d_01_%s' % (k, t)), ax, 10 if k in (1, 4) else 5))
        G['hand_splay_' + s] = spl
        G['hand_opposition_curl_' + s] = opp + curl((25, 30, 20))
        # ---- foot ----
        A = R.H('foot_' + t); toe = lambda k, deg: ('toe_%d_01_%s' % (k, t), R.H('toe_%d_01_%s' % (k, t)), np.cross(R.Tl('toe_%d_01_%s' % (k, t)) - R.H('toe_%d_01_%s' % (k, t)), [0, 0, -1]), deg)
        G['ankle_plantar25_' + s] = [('foot_' + t, A, X, -25)]; G['ankle_dorsi25_' + s] = [('foot_' + t, A, X, 25)]
        G['foot_pushoff_' + s] = [('foot_' + t, A, X, -20)] + [toe(k, -35) for k in range(1, 6)]
        G['foot_curl_' + s] = [('foot_' + t, A, X, -20)] + [toe(k, 30) for k in range(1, 6)]
        G['foot_dorsi_toeflex_' + s] = [('foot_' + t, A, X, 20)] + [toe(k, 25) for k in range(1, 6)]
        mt = R.H('toe_3_01_' + t); tsp = []
        for k in (1, 2, 4, 5):
            dvec = R.H('toe_%d_01_%s' % (k, t)) - mt; ax = Z * np.sign(np.cross(R.Tl('toe_%d_01_%s' % (k, t)) - R.H('toe_%d_01_%s' % (k, t)), dvec) @ Z)
            tsp.append(('toe_%d_01_%s' % (k, t), R.H('toe_%d_01_%s' % (k, t)), ax, 8))
        G['toe_splay_' + s] = tsp
    # ---- jaw / head ----
    J = R.H('jaw'); N2 = R.H('neck_02')
    for a in (8, 20, 32): G['jaw_open_%d' % a] = [('jaw', J, X, -a)]
    G['head_yaw_35'] = [('neck_02', N2, Z, 35)]; G['head_pitch_down_25'] = [('neck_02', N2, X, -25)]; G['head_pitch_up_25'] = [('neck_02', N2, X, 25)]
    G['head_roll_20'] = [('neck_02', N2, Y, 20)]
    G['jaw20_head_yaw_pitch'] = [('neck_02', N2, Z, 30), ('neck_02', N2, X, 15), ('jaw', J, X, -20)]
    G['jaw32_head_pitch_up'] = [('neck_02', N2, X, 20), ('jaw', J, X, -32)]
    return G
