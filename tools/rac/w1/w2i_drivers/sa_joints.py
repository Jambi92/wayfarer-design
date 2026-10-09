# RAC W2I1 D3 (closure order §4-§5): J-2 MEASUREMENT-ONLY joint landmarks for the rig-less Saurin closure mesh.
#
# SOURCE (order §4A): the accepted Saurin construction skeleton, i.e. the per-side B1 limb axes that the accepted Gate 4 / Gate 5 limb
# reconstructions were built about and kept ("Skeleton kept. Each leg keeps its own B1 hip-knee-ankle axis" - reviews/claude-saurin-gate4-
# hindlimb-foot-reconstruction.md §1; "Each arm keeps its B1 shoulder-elbow-wrist axis" - gate5 §1), carried verbatim in gate1/g7geo.py
# (ARM S/E/W, LEG H/K/A; the Gate 7 "skeleton references") and gate1/g7.py SK. The middle-digit MCP is the hand builder's digit-III metacarpal
# head (gate1/hand.py FING[1], hand frame from W and E, hand.frame) - the analogue of the MPFB middle_01 joint used for palm length.
# No point is placed by eye, fitted, or moved; no humanoid default skeleton is authored.
#
# CHECKS on the frozen SA-M (aff1b52 body, unchanged): every point inside the closed surface (generalized winding number); for the
# mid-limb joints the exact-plane section through the point (normal = limb axis) must enclose it, with the in-plane offset from the
# section centroid reported against the section's equivalent radius.
#
# TRANSPORT to warped bodies (stature route, frames, composition, sex): each joint is an AFFINE-EXACT combination of an anchor ring of
# surface vertices (vertices within 1 cm of the joint plane and 12 cm of the joint; least-norm weights w with sum w = 1 and
# sum w V_i = J on the frozen body). Exact for any affine map, deterministic, reads vertex positions only (MakeHuman-style vertex-defined
# joints). The ring-centroid displacement is computed beside it as a transport-uncertainty control.
#
# READINGS: the arm_measure.py (MPFB) definitions on these joints - upper arm |S-E|, forearm |E-W|, hand = wrist -> farthest hand vertex
# along the wrist -> MCP-III axis (claw keratin included, as MPFB includes the nail; claw-excluded value reported), palm = (MCP - W) . axis,
# thigh |H-K|, shin |K-A|, hip / ankle height; exact-plane joint breadth (w2c1 joint_section.py: elbow axis S->W over the arm set, wrist E->W,
# knee H->A over the leg set, ankle K->A) and depth; femoral S7 exact plane section at 20 % down H->K over the thigh faces (s7_station.py)
# on the body itself and on its composition infimum (muscle -1 / fat -1 = the Saurin composition floor, the analogue of the MPFB CIB
# skeletal envelope) inset 2t for t = 0 / 0.5 / 1.0 cm x H / 173.14; mid-segment sections (REPORT).
# Usage: python3 sa_joints.py OUT.json   (writes the base joint audit + every body's readings)
import sys, os, json, hashlib, numpy as np, igl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_build as B
C = B.C; L = B.L; V0 = C.V; F0 = C.F; H0 = B.H0; Mx = B.Mx
G1 = C.W + '/g1'; sys.path.insert(0, G1)
import g7geo, hand as HB
SIDES = {1: 'L', -1: 'R'}          # mesh side +x / -x (g7geo key +1 = +x)
def base_joints():
    J = {}
    for sg, nm in SIDES.items():
        a = g7geo.ARM[sg]; l = g7geo.LEG[sg]
        J['S' + nm], J['E' + nm], J['W' + nm] = (np.array(a[k], float) for k in ('S', 'E', 'W'))
        J['H' + nm], J['K' + nm], J['A' + nm] = (np.array(l[k], float) for k in ('H', 'K', 'A'))
        fa, fb, fc = HB.frame(a['W'], a['E'], sg); hd = np.array(HB.FING[1][1], float)
        J['M' + nm] = np.array(a['W'], float) + hd[0] * fa + hd[1] * fb + hd[2] * fc
    return J
AXIS = {'S': ('S', 'E'), 'E': ('S', 'W'), 'W': ('E', 'W'), 'M': ('W', 'M'), 'H': ('H', 'K'), 'K': ('H', 'A'), 'A': ('K', 'A')}
ARMSET = {'S', 'E', 'W', 'M'}
def unit(v): return v / np.linalg.norm(v)
def lset(P, nm, j, thr=0.3):
    sd = 1 if nm == 'L' else -1; w = L.arm if j in ARMSET else L.leg
    return (w > thr) & (L.side == sd)
def plane_pts(P, F, on, c, ax, R=12.0):
    TF = F[on[F].all(1)]; t = (P - c) @ ax; pts = []
    for i, j in ((0, 1), (1, 2), (2, 0)):
        a, b = TF[:, i], TF[:, j]; m = t[a] * t[b] < 0; u = t[a[m]] / (t[a[m]] - t[b[m]]); pts.append(P[a[m]] + (P[b[m]] - P[a[m]]) * u[:, None])
    Q = np.vstack(pts); Q = Q[np.linalg.norm(Q - c, axis=1) < R]; return Q
def inplane(Q, c, ax):
    X = Q - c; X = X - np.outer(X @ ax, ax); e1 = unit(np.cross(ax, [0, 0, 1.0]) if abs(ax[2]) < 0.9 else np.cross(ax, [1.0, 0, 0])); e2 = np.cross(ax, e1)
    return np.stack([X @ e1, X @ e2], 1)
def poly_check(Q2):
    """angle-sorted polygon about the section centroid: centroid, area, equivalent radius, origin (= the joint) inside?"""
    c = Q2.mean(0); ang = np.arctan2(Q2[:, 1] - c[1], Q2[:, 0] - c[0]); o = np.argsort(ang); Pp = Q2[o]
    x, y = Pp[:, 0], Pp[:, 1]; A = 0.5 * (x * np.roll(y, -1) - np.roll(x, -1) * y).sum()
    cx = ((x + np.roll(x, -1)) * (x * np.roll(y, -1) - np.roll(x, -1) * y)).sum() / (6 * A); cy = ((y + np.roll(y, -1)) * (x * np.roll(y, -1) - np.roll(x, -1) * y)).sum() / (6 * A)
    inside = False; n = len(Pp)
    for i in range(n):                                          # ray casting from the origin (joint position)
        x1, y1 = Pp[i]; x2, y2 = Pp[(i + 1) % n]
        if (y1 > 0) != (y2 > 0) and 0 < x1 + (0 - y1) * (x2 - x1) / (y2 - y1): inside = not inside
    return dict(centroid_offset_cm=float(np.hypot(cx, cy)), area_cm2=float(abs(A)), eq_radius_cm=float(np.sqrt(abs(A) / np.pi)), joint_inside_section=bool(inside), n_pts=int(n))
def axis_of(J, j, nm):
    a, b = AXIS[j]; return unit(J[b + nm] - J[a + nm])
def anchors(J):
    """affine-exact least-norm weights over the anchor ring of every joint on the frozen body"""
    W = {}
    for key, p in J.items():
        j, nm = key[0], key[1]; ax = axis_of(J, j, nm)
        m = (np.abs((V0 - p) @ ax) < 1.0) & (np.linalg.norm(V0 - p, axis=1) < 12.0) & (L.tail < 0.2) & (L.head < 0.2) & (L.side == (1 if nm == 'L' else -1))
        idx = np.where(m)[0]; X = V0[idx]; n = len(idx)
        A = np.vstack([X.T, np.ones(n)]); b = np.append(p, 1.0); w0 = np.full(n, 1.0 / n)
        w = w0 + A.T @ np.linalg.solve(A @ A.T, b - A @ w0)
        W[key] = (idx, w, float(np.abs(A @ w - b).max()), p - X.mean(0))
    return W
def transport(P, W):
    J = {}; U = {}
    for key, (idx, w, _, off) in W.items():
        J[key] = w @ P[idx]; U[key] = float(np.linalg.norm(J[key] - (P[idx].mean(0) + off)))   # control: ring-centroid displacement
    return J, U
def section_wd(P, F, on, c, ax):
    Q = plane_pts(P, F, on, c, ax, R=15.0)
    if len(Q) < 4: return float('nan'), float('nan')
    X = Q - c; X = X - np.outer(X @ ax, ax); ev, evec = np.linalg.eigh(np.cov(X.T)); wd = evec[:, -1]; dd = np.cross(ax, wd)
    return float((X @ wd).max() - (X @ wd).min()), float((X @ dd).max() - (X @ dd).min())
def s7(P, F, J, nm):
    hp, kn = J['H' + nm], J['K' + nm]; Ln = np.linalg.norm(kn - hp); ax = (kn - hp) / Ln; c = hp + 0.2 * Ln * ax
    on = lset(P, nm, 'K', 0.5); Q = plane_pts(P, F, on, c, ax, R=15.0) - hp; Q = Q - np.outer(Q @ ax, ax)
    return float(np.ptp(Q[:, 0])), float(np.ptp(Q[:, 1]))
CLAW = None
def claw_mask():
    global CLAW
    if CLAW is None:
        g = np.load(C.W + '/c12/g15reg.npz'); CLAW = g['FAM'][:len(V0)] == 6       # g15up keeps the base vertices first (checked: max |dV| = 0)
    return CLAW
def readings(P, J, H):
    out = {}; seg = {}
    for sg, nm in SIDES.items():
        S_, E_, W_, M_, H_, K_, A_ = (J[k + nm] for k in 'SEWMHKA')
        hax = unit(M_ - W_); hv = np.where(B.WHAND * (L.side == sg) > 0.5)[0]; t = (P[hv] - W_) @ hax
        hv_nc = hv[~claw_mask()[hv]]; t_nc = (P[hv_nc] - W_) @ hax
        s = dict(upperarm=np.linalg.norm(E_ - S_), forearm=np.linalg.norm(W_ - E_), hand=float(t.max()), hand_noclaw=float(t_nc.max()), palm=float((M_ - W_) @ hax),
                 thigh=np.linalg.norm(K_ - H_), shin=np.linalg.norm(A_ - K_), hip_height=H_[2], ankle_height=A_[2], shoulder_height=S_[2])
        s['finger'] = s['hand'] - s['palm']; s['arm'] = s['upperarm'] + s['forearm'] + s['hand']; s['leg_joint'] = s['thigh'] + s['shin']
        arm_on = lset(P, nm, 'E'); leg_on = lset(P, nm, 'K')
        s['elbow_breadth'], s['elbow_depth'] = section_wd(P, F0, arm_on, E_, unit(W_ - S_)); s['wrist_breadth'], s['wrist_depth'] = section_wd(P, F0, arm_on, W_, unit(W_ - E_))
        s['knee_breadth'], s['knee_depth'] = section_wd(P, F0, leg_on, K_, unit(A_ - H_)); s['ankle_breadth'], s['ankle_depth'] = section_wd(P, F0, leg_on, A_, unit(A_ - K_))
        for nm2, a_, b_, on in (("mid_humerus", S_, E_, arm_on), ("mid_forearm", E_, W_, arm_on), ("mid_shin", K_, A_, leg_on)):
            s[nm2 + '_breadth'], s[nm2 + '_depth'] = section_wd(P, F0, on, 0.5 * (a_ + b_), unit(b_ - a_))
        s['S7_breadth'], s['S7_depth'] = s7(P, F0, J, nm); seg[nm] = s
    M = {k: float(0.5 * (seg['L'][k] + seg['R'][k])) for k in seg['L']}
    out['L'], out['R'], out['mean'] = seg['L'], seg['R'], M
    out['shoulder_joint_breadth'] = float(np.linalg.norm(J['SL'] - J['SR'])); out['hip_joint_breadth'] = float(np.linalg.norm(J['HL'] - J['HR']))
    R = {"leg_share": M['hip_height'] / H, "arm_share": M['arm'] / H, "span_der": (2 * M['arm'] + out['shoulder_joint_breadth']) / H,
         "upperarm_over_arm": M['upperarm'] / M['arm'], "forearm_over_arm": M['forearm'] / M['arm'], "hand_over_arm": M['hand'] / M['arm'],
         "forearm_over_upperarm": M['forearm'] / M['upperarm'], "finger_over_hand": M['finger'] / M['hand'], "finger_over_palm": M['finger'] / M['palm'],
         "femur_over_leg": M['thigh'] / M['leg_joint'], "shin_over_leg": M['shin'] / M['leg_joint'], "thigh_share": M['thigh'] / H, "shin_share": M['shin'] / H,
         "upperarm_share": M['upperarm'] / H, "forearm_share": M['forearm'] / H, "hand_share": M['hand'] / H, "hand_noclaw_share": M['hand_noclaw'] / H,
         "leg_joint_share": M['leg_joint'] / H, "ankle_height_share": M['ankle_height'] / H,
         "elbow_over_humerus": M['elbow_breadth'] / M['upperarm'], "wrist_over_forearm": M['wrist_breadth'] / M['forearm'],
         "knee_over_femur": M['knee_breadth'] / M['thigh'], "ankle_over_shin": M['ankle_breadth'] / M['shin'],
         "elbow_share": M['elbow_breadth'] / H, "wrist_share": M['wrist_breadth'] / H, "knee_share": M['knee_breadth'] / H, "ankle_share": M['ankle_breadth'] / H,
         "shaft_b_over_femur_self": M['S7_breadth'] / M['thigh'], "shaft_d_over_femur_self": M['S7_depth'] / M['thigh'],
         "shoulder_joint_share": out['shoulder_joint_breadth'] / H, "hip_joint_breadth_share": out['hip_joint_breadth'] / H}
    out['ratio'] = R; return out
def sha(*arrs):
    h = hashlib.sha256()
    for a in arrs: h.update(np.ascontiguousarray(a).tobytes())
    return h.hexdigest()
MIN = {'muscle': -1.0, 'fat': -1.0}
BODIES = []
for h in (168, 173, 178, 181, 188, 190, 203, 208):
    hh = H0 if h == 188 else float(h); BODIES += [("SA-M%d" % h, {}, hh), ("SA-F%d" % h, B.CEN, hh)]
for h in (188, 208):
    hh = H0 if h == 188 else float(h); BODIES += [("SA-M%d-N" % h, B.NAR, hh), ("SA-M%d-B" % h, B.BRD, hh)]
BODIES += [("SA-M188-MIN", MIN, H0), ("SA-M188-MUHI", {'muscle': 1.0}, H0), ("SA-M188-MUFAHI", {'muscle': 1.0, 'fat': 1.0}, H0), ("SA-M208-B-MUHI", Mx(B.BRD, {'muscle': 1.0}), 208.0),
           ("SA-M168-LT90", {'trunk_len': 0.90}, 168.0), ("SA-M203-LT90", {'trunk_len': 0.90}, 203.0)]
if __name__ == '__main__':
    out = {"source": "gate1/g7geo.py ARM / LEG (Gate 4 / Gate 5 B1 construction axes) + gate1/hand.py FING[1] MCP-III", "audit": {}, "base": {}, "bodies": {}}
    hV0, hF0 = sha(V0), sha(F0); f_sha = hashlib.sha256(open(C.vary.REF_BASE, 'rb').read()).hexdigest()
    M_before = B.measure(*C.build({})[:2])
    J0 = base_joints(); J0b = base_joints()
    wn = igl.fast_winding_number(V0, F0, np.array([J0[k] for k in sorted(J0)]))
    for i, key in enumerate(sorted(J0)):
        j, nm = key[0], key[1]; ax = axis_of(J0, j, nm); rec = dict(point=J0[key].tolist(), winding_number=float(wn[i]), inside_mesh=bool(wn[i] > 0.5), axis=ax.tolist())
        if j in 'EWKA':
            Q = plane_pts(V0, F0, lset(V0, nm, j), J0[key], ax); rec['section'] = poly_check(inplane(Q, J0[key], ax))
        out["base"][key] = rec; print(key, J0[key], 'wn %.3f' % wn[i], rec.get('section', ''), flush=True)
    W = anchors(J0); Jt, U = transport(V0, W)
    out["audit"]["anchor_ring_sizes"] = {k: int(len(v[0])) for k, v in W.items()}
    out["audit"]["affine_constraint_residual_cm"] = max(v[2] for v in W.values())
    out["audit"]["base_reconstruction_max_cm"] = float(max(np.linalg.norm(Jt[k] - J0[k]) for k in J0))
    Aff = np.array([[1.07, 0.02, -0.01], [0.015, 0.93, 0.03], [-0.02, 0.01, 1.11]]); tv = np.array([3.0, -2.0, 5.0]); Ja, _ = transport(V0 @ Aff.T + tv, W)
    out["audit"]["affine_exactness_max_cm"] = float(max(np.linalg.norm(Ja[k] - (Aff @ J0[k] + tv)) for k in J0))
    out["audit"]["deterministic_points"] = all(np.array_equal(J0[k], J0b[k]) for k in J0)
    W2 = anchors(base_joints()); out["audit"]["deterministic_weights"] = all(np.array_equal(W[k][1], W2[k][1]) for k in W)
    for bid, p, h in BODIES:
        P, q = C.build(p); P2, q2, k = B.at_stature(P, q, h); hP = sha(P2); M = B.measure(P2, q2, k); Hh = M['height']
        J, U = transport(P2, W); r = readings(P2, J, Hh)
        Pm, qm = C.build(Mx(p, MIN)); Pm2, qm2, km = B.at_stature(Pm, qm, h); Jm, _ = transport(Pm2, W); rm = readings(Pm2, Jm, Hh)
        S7b, S7d, fl = rm['mean']['S7_breadth'], rm['mean']['S7_depth'], r['mean']['thigh']
        r['S7_CIB'] = {"%.1f" % tt: dict(t_cm=tt * Hh / 173.14, S7_breadth=S7b - 2 * tt * Hh / 173.14, S7_depth=S7d - 2 * tt * Hh / 173.14,
                                          shaft_b_over_femur=(S7b - 2 * tt * Hh / 173.14) / fl, shaft_d_over_femur=(S7d - 2 * tt * Hh / 173.14) / fl) for tt in (0.0, 0.5, 1.0)}
        r['transport_control_max_cm'] = max(U.values()); r['stature'] = Hh; r['params'] = dict(p); r['joints'] = {kk: v.tolist() for kk, v in J.items()}
        r['body_unchanged_by_landmarking'] = (sha(P2) == hP)
        r['axial'] = {kk: M[kk] for kk in ('u_hip', 'lower_trunk_costal_hip', 'u_costal', 'u_platform', 'head_len', 'foot_len_over_H')}
        out["bodies"][bid] = r
        print(bid, round(Hh, 2), {kk: round(v, 4) for kk, v in r['ratio'].items() if kk in ('leg_share', 'arm_share', 'forearm_over_arm', 'femur_over_leg', 'knee_over_femur', 'elbow_over_humerus')},
              'S7cib', round(r['S7_CIB']['0.5']['shaft_b_over_femur'], 4), 'ctl %.3f' % r['transport_control_max_cm'], flush=True)
    M_after = B.measure(*C.build({})[:2])
    out["audit"]["mesh_sha_V_before_after"] = [hV0, sha(V0)]; out["audit"]["mesh_sha_F_before_after"] = [hF0, sha(F0)]
    out["audit"]["base_npz_sha256_before_after"] = [f_sha, hashlib.sha256(open(C.vary.REF_BASE, 'rb').read()).hexdigest()]
    diff = {kk: abs(M_before[kk] - M_after[kk]) for kk in M_before if isinstance(M_before[kk], float)}
    out["audit"]["measure_readings_compared"] = len(diff); out["audit"]["measure_max_abs_diff"] = max(diff.values())
    out["audit"]["readings_checked"] = {kk: [M_before[kk], M_after[kk]] for kk in ('height', 'lower_trunk', 'lower_trunk_costal_hip', 'thorax_d_over_w', 'thorax_d', 'thorax_w', 'pelvis_w',
                                                                                 'tail_len_pct', 'tail_RSI_raw', 'tail_A50', 'head_len', 'head_depth', 'foot_len_over_H', 'u_hip') if kk in M_before}
    json.dump(out, open(sys.argv[1], 'w'), indent=1, default=float)
    print('AUDIT', {k: v for k, v in out['audit'].items() if k != 'readings_checked'})
