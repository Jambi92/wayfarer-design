# sa_identity.py OUT.json : RP5 Saurin identity metrics (order 53976fb §17) on the canonical sources SA-M188 / SA-F188 and their preservation by the
# authored tail module (cage). SA-F188 landmarks = SA-M188 landmarks carried by the shared-vertex displacement field (mean SA-F188 - SA-M188 displacement of
# the 64 nearest base vertices). Metric definitions (all section / landmark readings, same method on source and cage):
#   tail length = centreline arc root centre -> tip; tail / stature; tail cross-section area at 25 / 50 / 75 % arc (plane normal = local chain direction);
#   tail carriage = elevation angle of root centre -> 50 % chain point; lower axial trunk = u(spine 123) - u(spine 91); thorax breadth / depth (u 138 section);
#   pelvic band breadth (u = hip level section); forearm / arm = |E W| / (|S E| + |E W|); femur / leg = |H K| / (|H K| + |K A|);
#   rostral projection = f(rostrum tip) - f(eye centre); orbit spacing = |eye_l - eye_r|; claws = digit-tip counts; plantigrade = ball-line and heel heights.
import sys, json, numpy as np
from scipy.spatial import cKDTree
OUT = sys.argv[1]; W = '/tmp/claude-0/rt/sa'
b = np.load(W + '/src/saurin_w2_final_base.npz'); VM = b['v'].astype(float); F = b['f'].astype(np.int64); VF = np.load(W + '/src/saurin_w2_SA-F188_realization.npz')['v'].astype(float)
LM = json.load(open(W + '/lm/SA-M188_landmarks.json'))['landmarks']; kd = cKDTree(VM); D = VF - VM
def carry(p):
    _, idx = kd.query(p, 64); return np.asarray(p) + D[idx].mean(0)            # mean displacement of the 64 nearest base vertices
def sec_area(Vv, Ff, c, n):
    """area of the closed plane section (edges crossing the plane) of the component nearest c"""
    n = n / np.linalg.norm(n); s = (Vv - c) @ n; E = np.unique(np.sort(np.r_[Ff[:, [0, 1]], Ff[:, [1, 2]], Ff[:, [2, 0]]], 1), axis=0)
    cr = E[(s[E[:, 0]] > 0) != (s[E[:, 1]] > 0)]; w = s[cr[:, 0]] / (s[cr[:, 0]] - s[cr[:, 1]]); P = Vv[cr[:, 0]] + w[:, None] * (Vv[cr[:, 1]] - Vv[cr[:, 0]])
    P = P[np.linalg.norm(P - c, axis=1) < 25]; e1 = np.cross(n, [0, 0, 1.0]); e1 = e1 / np.linalg.norm(e1) if np.linalg.norm(e1) > 1e-6 else np.array([1.0, 0, 0]); e2 = np.cross(n, e1)
    xy = np.c_[(P - c) @ e1, (P - c) @ e2]; cc = xy.mean(0); o = np.argsort(np.arctan2(xy[:, 1] - cc[1], xy[:, 0] - cc[0])); xy = xy[o]
    return float(0.5 * abs(np.dot(xy[:, 0], np.roll(xy[:, 1], -1)) - np.dot(xy[:, 1], np.roll(xy[:, 0], -1))))
def width_depth(Vv, u, band=0.3):
    s = Vv[(np.abs(Vv[:, 2] - u) < band) & (np.abs(Vv[:, 0]) < 22)]; return float(np.ptp(s[:, 0])), float(np.ptp(s[:, 1]))
def metrics(Vv, L, tailP=None, tailF=None):
    g = lambda k: np.asarray(L[k]); H = float(np.ptp(Vv[:, 2]))
    ch = np.array([g('tail_root_centre')] + [g('tail_chain_%02d' % k) for k in range(1, 17)] + [g('tail_tip')]); arc = np.r_[0, np.cumsum(np.linalg.norm(np.diff(ch, axis=0), axis=1))]
    out = dict(stature_cm=round(H, 3), tail_length_cm=round(float(arc[-1]), 3), tail_over_stature=round(float(arc[-1] / H), 4))
    mid = ch[8]; out['tail_carriage_elevation_deg'] = round(float(np.degrees(np.arctan2(mid[2] - ch[0][2], np.hypot(mid[0] - ch[0][0], mid[1] - ch[0][1])))), 3)
    TP, TF = (Vv, F) if tailP is None else (tailP, tailF)
    for frac in (0.25, 0.5, 0.75):
        s = frac * arc[-1]; k = int(np.searchsorted(arc, s)) - 1; t = (s - arc[k]) / (arc[k + 1] - arc[k]); c = ch[k] + t * (ch[k + 1] - ch[k]); n = ch[k + 1] - ch[k]
        out['tail_area_%d_cm2' % int(frac * 100)] = round(sec_area(TP, TF, c, n), 3)
    if tailP is None:
        out['lower_axial_trunk_cm'] = round(float(g('spine_lower_axial_123')[2] - g('spine_lower_axial_91')[2]), 3)
        tb, td = width_depth(Vv, 138.0); out['thorax_breadth_cm'] = round(tb, 3); out['thorax_depth_cm'] = round(td, 3); out['thorax_depth_over_breadth'] = round(td / tb, 4)
        pb, _ = width_depth(Vv, float(g('pelvis_root')[2]), 0.3); out['pelvic_band_breadth_cm'] = round(pb, 3)
        for s_ in ('xneg', 'xpos'):
            S, E, Wr = g('glenohumeral_' + s_), g('elbow_' + s_), g('wrist_' + s_); Hh, K, A = g('hip_' + s_), g('knee_' + s_), g('ankle_' + s_)
            out['forearm_over_arm_' + s_] = round(float(np.linalg.norm(Wr - E) / (np.linalg.norm(E - S) + np.linalg.norm(Wr - E))), 4)
            out['femur_over_leg_' + s_] = round(float(np.linalg.norm(K - Hh) / (np.linalg.norm(K - Hh) + np.linalg.norm(A - K))), 4)
            out['ball_line_height_cm_' + s_] = round(float(g('ball_line_' + s_)[2]), 3)
        out['rostral_projection_cm'] = round(float(g('rostrum_tip')[1] - 0.5 * (g('eye_xneg')[1] + g('eye_xpos')[1])), 3); out['orbit_spacing_cm'] = round(float(np.linalg.norm(g('eye_xneg') - g('eye_xpos'))), 3)
        out['hand_claw_tips'] = sum(1 for k in L if k.startswith('hand_tip')); out['toe_claw_tips'] = sum(1 for k in L if k.startswith('toe_tip'))
        out['heel_min_u_cm'] = round(float(Vv[(Vv[:, 2] < 6) & (Vv[:, 1] < 2)][:, 2].min()), 3)
    return out
LMm = {k: v['p_cm'] for k, v in LM.items()}; LMf = {k: carry(v).tolist() for k, v in LMm.items()}
res = dict(source={'SA-M188': metrics(VM, LMm), 'SA-F188': metrics(VF, LMf)})
z = np.load(W + '/tail/SA_tail_module.npz'); Qc = z['Q']; Tc = np.r_[Qc[:, [0, 1, 2]], Qc[:, [0, 2, 3]]]; fi = z['tri']; BC = z['bc']
cage = {}
for bid, VS, L in (('SA-M188', VM, LMm), ('SA-F188', VF, LMf)):
    Vc = (BC[:, :, None] * VS[F[fi]]).sum(1); src = res['source'][bid]; cm = metrics(VS, L, Vc, Tc)
    cage[bid] = {k: dict(source=src[k], cage=cm[k], diff_pct=round(100 * (cm[k] / src[k] - 1), 3)) for k in cm if k.startswith('tail_area')}
res['tail_module_preservation'] = cage
json.dump(res, open(OUT, 'w'), indent=1); print(json.dumps(res['source'], indent=0)[:1800]); print(cage)
