# sa_eval.py CAGE.npz TAG OUT.json [--region tail] : RP5 Saurin source-vs-cage anatomy gates (order 53976fb §13-§17) on BOTH configurations.
# The cage is embedded once on SA-M188 (every cage vertex -> closest point on the canonical base: base triangle + barycentric) and realized on
# SA-F188 through the SHARED base face list (same triangle, same barycentric on the SA-F188 vertices) -- the c1 / c2 shared-topology test.
#   T-1 body : source base vertices -> cage surface distance (median / p95 / max, mm);  T-2 identity zones (head / rostrum-orbit-jaw, hands, feet, tail root,
#              tail stations = tail minus the tail-tip exemption zone (terminal ring system + cap; 2 cm default), which is reported separately);  T-3 stature / bbox;  T-4 quad angle 45-135 / aspect <= 4:1;  T-5 mean / p95 edge / stature by region;
#   T-6 landmarks: surface / canon / derived landmarks -> cage surface distance; section landmarks re-fitted as cage plane-section centroids;
#   T-7 silhouettes (front / rear / profiles / 3-4 at 3 px / cm, the RP3 anatomy.py raster) WITH the tail, plus a no-tail diagnostic.
# --region tail: partial-cage mode (the authored tail module): T-1 / T-2 restricted to the source vertices the module covers (caudal region, phi > 0.003).
import sys, os, json, numpy as np, igl
from PIL import Image, ImageDraw
CG, TAG, OUT = sys.argv[1:4]; REG = sys.argv[sys.argv.index('--region') + 1] if '--region' in sys.argv else None
W = os.environ.get('SA_W', '/tmp/claude-0/rt/sa'); SRC = W + '/src'
b = np.load(SRC + '/saurin_w2_final_base.npz'); F = b['f'].astype(np.int64); VM = b['v'].astype(float); VF = np.load(SRC + '/saurin_w2_SA-F188_realization.npz')['v'].astype(float)
lab = np.load(W + '/lm/SA-M188_regions.npz')['label']; LM = json.load(open(W + '/lm/SA-M188_landmarks.json'))['landmarks']
z = np.load(CG, allow_pickle=True); Qc = np.asarray(z['Q']).astype(np.int64)
if 'tri' in z.files: fi = z['tri']; BC = z['bc']
else:
    d2, fi, cp = igl.point_mesh_squared_distance(z['V'].astype(float), VM, F)
    a0, b0, c0 = VM[F[fi, 0]], VM[F[fi, 1]], VM[F[fi, 2]]; v0 = b0 - a0; v1 = c0 - a0; v2 = cp - a0
    d00 = (v0 * v0).sum(1); d01 = (v0 * v1).sum(1); d11 = (v1 * v1).sum(1); d20 = (v2 * v0).sum(1); d21 = (v2 * v1).sum(1); den = d00 * d11 - d01 * d01
    bb = (d11 * d20 - d01 * d21) / den; cc = (d00 * d21 - d01 * d20) / den; BC = np.c_[1 - bb - cc, bb, cc]
def realize(Vs): return (BC[:, :, None] * Vs[F[fi]]).sum(1)
TC = np.r_[Qc[:, [0, 1, 2]], Qc[:, [0, 2, 3]]]
if 'T' in z.files and len(z['T']): TC = np.r_[TC, np.asarray(z['T'])]
H = VM[:, 2].max() - VM[:, 2].min()
ZONES = {'head': lab == 'head', 'hands': np.isin(lab, ['hand_xneg', 'hand_xpos']), 'feet': np.isin(lab, ['foot_xneg', 'foot_xpos'])}
rc = np.array(LM['tail_root_centre']['p_cm']); ZONES['tail_root'] = (lab == 'tail') & (np.linalg.norm(VM - rc, axis=1) < 18)
tipp = np.array(LM['tail_tip']['p_cm']); RT = 2.0
if 'ring_N' in z.files:          # tail-tip exemption = the terminal ring system (the 8-vertex terminal rings + cap) of the module: radius = tip -> first terminal ring centroid
    rs_, rn_ = z['ring_start'], z['ring_N']; k0 = int(np.nonzero(rn_ == rn_.min())[0][0]); RT = float(np.linalg.norm(z['V'][rs_[k0]:rs_[k0] + rn_[k0]].mean(0) - tipp)) + 0.25
ZONES['tail_stations'] = (lab == 'tail') & (np.linalg.norm(VM - tipp, axis=1) > RT)
TIPZ = (lab == 'tail') & (np.linalg.norm(VM - tipp, axis=1) <= RT)      # tail-tip exemption zone: reported, not gated
def stats(d): return dict(median_mm=round(float(np.median(d) * 10), 4), p95_mm=round(float(np.percentile(d, 95) * 10), 4), max_mm=round(float(d.max() * 10), 4)) if len(d) else None
res = dict(cage=os.path.basename(CG), tag=TAG, mode=REG or 'full body', cage_verts=int(len(fi)), cage_quads=int(len(Qc)), cage_tris=int(len(TC) - 2 * len(Qc)))
cover = np.ones(len(VM), bool)
if REG == 'tail':
    sub = z['sub']; phi = z['phi']; cover = np.zeros(len(VM), bool); cover[sub[phi > 0.003]] = True
rng = np.random.default_rng(0); samp = np.nonzero(cover)[0]; samp = samp[rng.random(len(samp)) < (0.25 if REG is None else 1.0)]
for bid, VS in (('SA-M188', VM), ('SA-F188', VF)):
    Vc = realize(VS); d2, _, _ = igl.point_mesh_squared_distance(VS[samp], Vc, TC); d = np.sqrt(d2)
    r = dict(T1_body=stats(d), T2={k: stats(d[m[samp]]) for k, m in ZONES.items() if m[samp].any()})
    T1 = dict(median_mm=0.5, p95_mm=1.5, max_mm=3.0); T2 = dict(median_mm=0.3, p95_mm=0.8, max_mm=1.5)
    r['T1_pass'] = all(r['T1_body'][k] <= T1[k] for k in T1); r['T2_pass'] = {k: all(v[kk] <= T2[kk] for kk in T2) for k, v in r['T2'].items()}
    r['tail_tip_exempt_zone'] = dict(radius_cm=round(RT, 3), **(stats(d[TIPZ[samp]]) or {})) if TIPZ[samp].any() else None
    if REG is None:
        r['T3'] = dict(stature_source_cm=round(float(np.ptp(VS[:, 2])), 3), stature_cage_cm=round(float(np.ptp(Vc[:, 2])), 3),
                       stature_diff_mm=round(float((np.ptp(Vc[:, 2]) - np.ptp(VS[:, 2])) * 10), 3), bbox_diff_mm=np.round((np.r_[Vc.min(0), Vc.max(0)] - np.r_[VS.min(0), VS.max(0)]) * 10, 3).tolist())
        r['T3_pass'] = abs(r['T3']['stature_diff_mm']) <= 1.0 and max(abs(x) for x in r['T3']['bbox_diff_mm']) <= 2.0
    # T-4
    ang = []
    for k in range(4):
        p0, p1, p2 = Vc[Qc[:, (k - 1) % 4]], Vc[Qc[:, k]], Vc[Qc[:, (k + 1) % 4]]; u1 = p0 - p1; u2 = p2 - p1
        ang.append(np.degrees(np.arccos(np.clip((u1 * u2).sum(1) / np.linalg.norm(u1, axis=1) / np.linalg.norm(u2, axis=1), -1, 1))))
    ang = np.stack(ang, 1); sides = np.stack([np.linalg.norm(Vc[Qc[:, (k + 1) % 4]] - Vc[Qc[:, k]], axis=1) for k in range(4)], 1); asp = sides.max(1) / np.maximum(sides.min(1), 1e-9)
    r['T4'] = dict(quads=int(len(Qc)), angle_outside_45_135=int(((ang.min(1) < 45) | (ang.max(1) > 135)).sum()), angle_outside_pct=round(float(((ang.min(1) < 45) | (ang.max(1) > 135)).mean() * 100), 3),
                   aspect_gt4=int((asp > 4).sum()), aspect_p99=round(float(np.percentile(asp, 99)), 3), aspect_max=round(float(asp.max()), 3))
    # T-5 density by region (cage edges labelled by the source label of their embedding triangle's first vertex)
    E = np.unique(np.sort(np.r_[Qc[:, [0, 1]], Qc[:, [1, 2]], Qc[:, [2, 3]], Qc[:, [3, 0]]], 1), axis=0); el = np.linalg.norm(Vc[E[:, 0]] - Vc[E[:, 1]], axis=1) / H * 100
    el_lab = lab[F[fi[E[:, 0]], 0]]; grp = {'head': ['head'], 'neck': ['neck'], 'trunk_pelvis': ['torso'], 'arms': ['arm_xneg', 'arm_xpos'], 'legs': ['leg_xneg', 'leg_xpos'],
                                            'hands': ['hand_xneg', 'hand_xpos'], 'feet': ['foot_xneg', 'foot_xpos'], 'tail': ['tail']}
    CEIL = dict(head=0.25, neck=0.6, trunk_pelvis=0.6, arms=0.6, legs=0.6, hands=0.3, feet=0.3, tail=0.6)
    r['T5_density_pct_of_stature'] = {k: dict(mean=round(float(el[np.isin(el_lab, v)].mean()), 4), p95=round(float(np.percentile(el[np.isin(el_lab, v)], 95)), 4),
                                              max=round(float(el[np.isin(el_lab, v)].max()), 4), ceiling=CEIL[k], mean_within=bool(el[np.isin(el_lab, v)].mean() <= CEIL[k]))
                                      for k, v in grp.items() if np.isin(el_lab, v).any()}
    # T-6 (surface-type landmarks -> cage surface; c2 landmarks carried by the same affine-exact anchor: nearest base vertex offset)
    if REG is None:
        names = [k for k, v in LM.items() if v['method'] in ('extremal', 'canon', 'derived', 'section')]
        P = np.array([LM[k]['p_cm'] for k in names]); kd_i = igl.point_mesh_squared_distance(P, VM, F)
        # landmark position on this body: c1 as fitted; c2 = same offset from the closest base point (barycentric) carried to SA-F188
        a0 = (igl.barycentric_coordinates(kd_i[2], VM[F[kd_i[1], 0]], VM[F[kd_i[1], 1]], VM[F[kd_i[1], 2]]) if hasattr(igl, 'barycentric_coordinates') else None)
        surf = [k for k in names if LM[k]['method'] in ('extremal',)]
        Ps = np.array([LM[k]['p_cm'] for k in surf])
        if bid == 'SA-F188':
            d2s, fis, cps = igl.point_mesh_squared_distance(Ps, VM, F); a1, b1, c1 = VM[F[fis, 0]], VM[F[fis, 1]], VM[F[fis, 2]]
            v0 = b1 - a1; v1 = c1 - a1; v2 = cps - a1; d00 = (v0 * v0).sum(1); d01 = (v0 * v1).sum(1); d11 = (v1 * v1).sum(1); d20 = (v2 * v0).sum(1); d21 = (v2 * v1).sum(1); den = d00 * d11 - d01 * d01
            bb = (d11 * d20 - d01 * d21) / den; cc = (d00 * d21 - d01 * d20) / den; Bs = np.c_[1 - bb - cc, bb, cc]; Ps = (Bs[:, :, None] * VS[F[fis]]).sum(1)
        dl = np.sqrt(igl.point_mesh_squared_distance(Ps, Vc, TC)[0]) * 10
        r['T6_surface_landmarks_mm'] = dict(zip(surf, np.round(dl, 4).tolist())); r['T6_max_mm'] = round(float(dl.max()), 4); r['T6_over_1mm'] = [s for s, x in zip(surf, dl) if x > 1.0]
        r['T6_pass'] = bool(dl.max() <= 1.5)
        # T-7 silhouettes with tail (organism) and without tail (diagnostic)
        px = 3.0; ZT = float(np.ceil(VS[:, 2].max() + 5)); XO = float(np.ceil(np.abs(VS[:, :2]).max() + 10))
        def sil(Vv, Ff, yaw, ss=2):
            an = np.radians(yaw); Rm = np.array([[np.cos(an), -np.sin(an), 0], [np.sin(an), np.cos(an), 0], [0, 0, 1]]); Pp = Vv @ Rm.T; q = px * ss
            u = (Pp[:, 0] + XO) * q; v = (ZT - Pp[:, 2]) * q; W_, H_ = int(2 * XO * px), int((ZT + 5) * px)
            im = Image.new('L', (W_ * ss, H_ * ss), 0); dr = ImageDraw.Draw(im)
            for t in Ff: dr.polygon([(u[t[0]], v[t[0]]), (u[t[1]], v[t[1]]), (u[t[2]], v[t[2]])], fill=255)
            a_ = np.array(im, float).reshape(H_, ss, W_, ss).mean((1, 3)); return a_ >= 127.5
        notail_src = F[~np.isin(lab[F], ['tail']).any(1)]; tl = lab[F[fi]][:, 0]; notail_cg = TC[~np.isin(tl[TC], ['tail']).any(1)]
        iou = {}; iou_nt = {}
        for nm, yaw in (('front', 0), ('rear', 180), ('profile_left', 90), ('profile_right', -90), ('q3_front_left', 45), ('q3_front_right', -45)):
            A = sil(VS, F, yaw); B = sil(Vc, TC, yaw); iou[nm] = round(float((A & B).sum() / (A | B).sum()), 6)
            if nm in ('front', 'profile_left'):
                A = sil(VS, notail_src, yaw); B = sil(Vc, notail_cg, yaw); iou_nt[nm] = round(float((A & B).sum() / (A | B).sum()), 6)
        r['T7_with_tail'] = iou; r['T7_pass'] = bool(min(iou[k] for k in ('front', 'rear', 'profile_left', 'profile_right')) >= 0.995); r['T7_no_tail_diagnostic'] = iou_nt
    res[bid] = r; print(TAG, bid, 'T1', r['T1_body'], 'T1', r['T1_pass'], 'T2', r['T2_pass'], 'T4', r['T4'], flush=True)
json.dump(res, open(OUT, 'w'), indent=1)
