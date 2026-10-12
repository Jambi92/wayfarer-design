# RAC RM-OT-05F sculpt INGEST (re-entry stage 1). Reads a delivered sculpt OBJ (template vertex order, R-6, cm, Z up, +Y anterior,
# +X body left), checks it against the template BEFORE anything is built, and converts it to the skinned-frame displacement field that
# race_base.sculpt_layer transports to every composition / frame / pose state of the accepted skeleton route.
# Ingest checks (all thresholds fixed here; none may be relaxed for a delivery):
#   I1 topology       exactly 13 380 vertices; faces (if present) identical to the template (no added / removed / reordered geometry)
#   I2 rigid/scale    best similarity fit of the sculpt to the template on the subcutaneous bony anchors (joint zones, hands, feet, head):
#                     |scale - 1| <= 0.002, rotation <= 0.2 deg, translation <= 0.3 cm  (no uniform scaling, no re-posing, no drift)
#   I3 stature/ground stature within 0.05 cm of the template, min z within 0.05 cm of 0 (no stature change)
#   I4 no-touch       head / neck, hands / digits, toes / forefoot within 0.5 cm of the template
#   I5 true floor     raw sculpt (before any guard) has 0 organized vertices more than 0.2 cm inside the 05D true skeletal floor
#   I6 R-6 posture    centroids of the distal anchors (each hand, each foot, head) within 0.3 cm of the template: the limbs and trunk are
#                     not re-posed (the skeleton itself is never read from the sculpt). Segment principal-axis changes are reported as an
#                     advisory only (shape-sensitive). A posture ILLUSION made of soft-tissue form is judged by the author and the blind gate.
#   coverage          per-family displacement statistics for the six hard-form families (advisory: the author judges the forms)
# Usage: python3 f_ingest.py SCULPT.obj SID   ->  WORK/sculpt_SID.npz + WORK/ingest_SID.json ; exit code 0 = ingest PASS
import os, sys, json, numpy as np
from f_common import *
def anchors(B):
    w = {k[2:]: B[k].astype(float) for k in B.files if k.startswith('w_')}
    a = np.zeros(len(B['V']), bool)
    for k in ('hand_l', 'hand_r', 'fingers_l', 'fingers_r', 'ball_l', 'ball_r', 'head'): a |= w[k] > 0.7
    return a[:NBODY]
def simil_fit(A, Bm):
    ca, cb = A.mean(0), Bm.mean(0); A0, B0 = A - ca, Bm - cb
    U, s, Vt = np.linalg.svd(B0.T @ A0); d = np.sign(np.linalg.det(U @ Vt)); Dm = np.diag([1, 1, d]); R = U @ Dm @ Vt
    sc = (s * np.diag(Dm)).sum() / (A0 ** 2).sum(); t = cb - sc * R @ ca
    ang = np.degrees(np.arccos(np.clip((np.trace(R) - 1) / 2, -1, 1)))
    return sc, ang, float(np.linalg.norm(t + sc * R @ ca - ca)), R
def ingest(obj, sid):
    V0, B, L, J, f, z0 = route_state(SKELETON_BODY); F = B['F']; keep = B['keep'].astype(bool)
    Vs, Fs = read_obj(obj); rep = {'sculpt_obj': os.path.basename(obj), 'sha256': sha(obj), 'sid': sid, 'checks': {}}; C = rep['checks']
    Ft = F[(F < NBODY).all(1)]
    C['I1_topology'] = {'n_vertices': int(len(Vs)), 'expected': NBODY, 'faces_present': bool(len(Fs)),
                        'faces_identical': bool(len(Fs) == 0 or (len(Fs) == len(Ft) and np.array_equal(np.array(Fs), Ft)))}
    C['I1_topology']['pass'] = bool(len(Vs) == NBODY and C['I1_topology']['faces_identical'])
    if not C['I1_topology']['pass']: rep['pass'] = False; return rep, None
    Vt = V0[:NBODY]; an = anchors(B)
    sc, ang, tr, _ = simil_fit(Vt[an], Vs[an])
    C['I2_rigid_scale'] = {'scale': float(sc), 'rotation_deg': float(ang), 'translation_cm': float(tr), 'pass': bool(abs(sc - 1) <= 0.002 and ang <= 0.2 and tr <= 0.3)}
    st, st0 = Vs[:, 2].max(), Vt[:, 2].max()
    C['I3_stature_ground'] = {'stature_cm': float(st), 'template_cm': float(st0), 'min_z_cm': float(Vs[:, 2].min()), 'pass': bool(abs(st - st0) <= 0.05 and abs(Vs[:, 2].min()) <= 0.05)}
    Dw = Vs - Vt; dn = np.linalg.norm(Dw, axis=1); R = regions(B, V0, J)
    nt = {k: float(dn[m[:NBODY]].max()) for k, m in R.items() if k.startswith('NO_TOUCH')}
    C['I4_no_touch'] = {'max_change_cm': nt, 'limit_cm': 0.5, 'pass': bool(max(nt.values()) <= 0.5)}
    Fl = floor_in_body_frame(L, f, z0); nF = TE.outward_normals(Fl, F, keep)
    sd = np.einsum('ij,ij->i', Vs - Fl[:NBODY], nF[:NBODY])
    ext = (np.clip(B['w_head'] + B['w_neck_01'] + B['w_hand_l'] + B['w_hand_r'] + B['w_fingers_l'] + B['w_fingers_r'], 0, 1) >= 0.3)[:NBODY]
    C['I5_true_floor_raw'] = {'n_inside_0p2cm': int((sd[~ext] < -0.2).sum()), 'min_signed_cm': float(sd[~ext].min()), 'pass': bool((sd[~ext] < -0.2).sum() == 0)}
    ax = {}
    for seg in ('thigh_l', 'thigh_r', 'calf_l', 'calf_r', 'upperarm_l', 'upperarm_r', 'lowerarm_l', 'lowerarm_r'):
        m = (B['w_' + seg] > 0.8)[:NBODY]
        a0 = np.linalg.svd(Vt[m] - Vt[m].mean(0))[2][0]; a1 = np.linalg.svd(Vs[m] - Vs[m].mean(0))[2][0]
        ax[seg] = round(float(np.degrees(np.arccos(min(1.0, abs(a0 @ a1))))), 3)
    cen = {}
    for nm, ks in (('hand_l', ('hand_l', 'fingers_l')), ('hand_r', ('hand_r', 'fingers_r')), ('foot_l', ('foot_l', 'ball_l')), ('foot_r', ('foot_r', 'ball_r')), ('head', ('head',))):
        m = (np.clip(sum(B['w_' + k] for k in ks), 0, 1) > 0.7)[:NBODY]; cen[nm] = round(float(np.linalg.norm(Vs[m].mean(0) - Vt[m].mean(0))), 4)
    C['I6_posture_anchors'] = {'anchor_centroid_shift_cm': cen, 'limit_cm': 0.3, 'segment_axis_change_deg_advisory': ax, 'pass': bool(max(cen.values()) <= 0.3)}
    rep['coverage_advisory'] = {k: {'n': int(m[:NBODY].sum()), 'p50_cm': round(float(np.percentile(dn[m[:NBODY]], 50)), 2), 'p90_cm': round(float(np.percentile(dn[m[:NBODY]], 90)), 2),
                                    'max_cm': round(float(dn[m[:NBODY]].max()), 2), 'mean_normal_cm': None} for k, m in R.items() if not k.startswith('NO_TOUCH')}
    nT = TE.outward_normals(V0, F, keep)[:NBODY]; dnorm = np.einsum('ij,ij->i', Dw, nT)
    for k, m in R.items():
        if not k.startswith('NO_TOUCH'): rep['coverage_advisory'][k]['mean_normal_cm'] = round(float(dnorm[m[:NBODY]].mean()), 2)
    v_t = TE.signed_volume(V0, F, keep); Vfull = V0.copy(); Vfull[:NBODY] = Vs; v_s = TE.signed_volume(Vfull, F, keep)
    rep['raw_volume_ratio_vs_template'] = float(abs(v_s) / abs(v_t))
    rep['pass'] = bool(all(c['pass'] for c in C.values()))
    # skinned-frame field (full vertex array; helpers 0)
    Lj = dict(L); Rf, ln = RB.skin_frames(Lj, J)
    Dfull = np.zeros_like(V0); Dfull[:NBODY] = Dw
    Dloc = np.einsum('nji,nj->ni', Rf, Dfull)
    out = WORK + '/sculpt_%s.npz' % sid
    np.savez_compressed(out, D_local=Dloc, len_ref=ln, template=SKELETON_BODY, sha256=rep['sha256'])
    return rep, out
if __name__ == '__main__':
    rep, out = ingest(sys.argv[1], sys.argv[2])
    json.dump(rep, open(WORK + '/ingest_%s.json' % sys.argv[2], 'w'), indent=1, default=float)
    print(json.dumps({k: v.get('pass') for k, v in rep['checks'].items()}), 'INGEST', 'PASS' if rep['pass'] else 'FAIL', out)
    sys.exit(0 if rep['pass'] else 1)
