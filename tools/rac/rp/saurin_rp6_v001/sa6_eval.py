# sa6_eval.py CFG WEIGHTS.npz CORRECTIVES.json OUT.json : RP6 pose suite + 4-step ownership + deformation metrics for one configuration.
#   Pose set = sa6_fit.pose_set (34 anatomical-sign RP5 poses + 14 RP5-literal sagittal variants) + the literal jaw closure (contact check only).
#   Every pose is evaluated at 0.25 / 0.5 / 0.75 / 1.0 of its angles (correctives are driven by the measured joint angle -> mid-angle behaviour is tested).
#   OWNERSHIP (RP5 logic, re-run on the RP6 rig):
#     step 1 SOURCE / POSE : the dense frozen working source (25 % face sample, seed 0) skinned with the RP6 weights interpolated barycentrically from the
#                            cage; source fold rate vs cage fold rate (per mille of area).
#     step 2 RP5 scaffold  : the RP5 diagnostic-scaffold baseline (c1, RP5-literal signs; recorded, not re-run).
#     step 3 RP6 LBS       : production weights alone.
#     step 4 RP6 + correctives (all fractions).
#     TOPOLOGY test        : for every pose with step-3 folds, the RP5 smooth-map test (weights diffused 100 x more, dual-quaternion skinning, cage vs FULL
#                            source within 2.5 cm of each fold; a cage fold > 1 cm from every source fold under the same map = topology-carried); in addition
#                            a fold-free corrected state of the same quad layout (step 4 = 0) is itself proof that the layout is not the owner.  Smooth-map
#                            folds within 1 cm of vertices that interpenetrate under the same smooth map are contact-owned (reported separately).
#   METRICS (corrected, full pose): flips + area; new self-penetration vertices (sa6_fit.penetration: the point 0.2 mm INSIDE the vertex also lies inside another
#     part of the posed body, generalised winding number > 1.5 -> depth >= 0.2 mm; vertices already in that state at rest excluded); local joint volume (cone volume about the posed pivot of the closed-off joint patch: invariant to
#     the rigid motion of either side -> pure deformation); edge stretch (posed / rest edge length in the joint patch: min / p01 / p99 / max);
#     landmark displacement (posed landmark vs the rigid motion of its dominant bone).
import sys, os, json, time, numpy as np, igl, scipy.sparse as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sa6_common as C, sa6_pose as SP, sa6_correctives as CC, sa6_fit as FT
TH = dict(flips=0, volume_ratio=(0.80, 1.15), stretch=(0.5, 1.8), landmark_rigid_cm=0.05)
def main():
    cfg, wf, cf, out = sys.argv[1:5]; d = C.load(); R = SP.Rig(cfg, wf); Cr = CC.Correctives.load(R, cf); PS = FT.pose_set(R); PS['jaw_open_20_rp5lit'] = R.suite('rp5')['jaw_open_20']
    if os.environ.get('POSES'): PS = {k: v for k, v in PS.items() if k in os.environ['POSES'].split(',')}
    Q = R.Q; F = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]].astype(np.int64); w0 = FT.wn_out(R.V, F)
    qa = 0.5 * np.linalg.norm(R.n0, axis=1)
    # dense source sample + interpolated weights
    w = np.load(C.W + '/work/SA_RP5_WORK_v001.npz'); Vd = (w['v_M'] if cfg == 'M' else w['v_F']).astype(float); Fd = w['f'].astype(np.int64)
    rng = np.random.default_rng(0); Fs = Fd[rng.random(len(Fd)) < 0.25]; us = np.unique(Fs); mp = -np.ones(len(Vd), np.int64); mp[us] = np.arange(len(us)); Fs = mp[Fs]; Vs = Vd[us]
    _, ti, cp = igl.point_mesh_squared_distance(Vs, R.V, F); a, b, c = R.V[F[ti, 0]], R.V[F[ti, 1]], R.V[F[ti, 2]]
    v0 = b - a; v1 = c - a; v2 = cp - a; d00 = (v0 * v0).sum(1); d01 = (v0 * v1).sum(1); d11 = (v1 * v1).sum(1); d20 = (v2 * v0).sum(1); d21 = (v2 * v1).sum(1); dn = d00 * d11 - d01 * d01
    bb = (d11 * d20 - d01 * d21) / dn; cc = (d00 * d21 - d01 * d20) / dn; bcs = np.c_[1 - bb - cc, bb, cc]
    Wsp = sp.csr_matrix(R.W); Ws = np.zeros((len(Vs), len(R.DB)))
    for k in range(3): Ws += bcs[:, k:k + 1] * Wsp[F[ti, k]].toarray()
    n0s = np.cross(Vs[Fs[:, 1]] - Vs[Fs[:, 0]], Vs[Fs[:, 2]] - Vs[Fs[:, 0]]); sa_ = 0.5 * np.linalg.norm(n0s, axis=1)
    def relcos_s(P, T):
        dom = Ws[Fs].mean(1).argmax(1); Rq = np.stack([T[R.DB[i]][0] for i in range(len(R.DB))])[dom]; n0r = np.einsum('qij,qj->qi', Rq, n0s)
        n1 = np.cross(P[Fs[:, 1]] - P[Fs[:, 0]], P[Fs[:, 2]] - P[Fs[:, 0]]); return (n0r * n1).sum(1) / (np.linalg.norm(n0r, axis=1) * np.linalg.norm(n1, axis=1) + 1e-12)
    # smooth map (topology test)
    E = np.unique(np.sort(np.r_[Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]], 1), axis=0)
    Ad = sp.coo_matrix((np.ones(2 * len(E)), (np.r_[E[:, 0], E[:, 1]], np.r_[E[:, 1], E[:, 0]])), shape=(R.nv, R.nv)).tocsr(); deg = np.asarray(Ad.sum(1)).ravel()
    W4 = R.W.copy()
    for _ in range(100): W4 = 0.5 * W4 + 0.5 * (Ad @ W4) / deg[:, None]
    W4 /= W4.sum(1, keepdims=True)
    from scipy.spatial import cKDTree; kdd = cKDTree(Vd)
    def dqs(P, Wt, T):
        from scipy.spatial.transform import Rotation as Rt
        q = Rt.from_matrix(np.stack([T[b][0] for b in R.DB])).as_quat(); q0 = np.c_[q[:, 3], q[:, :3]]
        te = np.c_[np.zeros(len(R.DB)), np.stack([T[b][1] for b in R.DB])]
        def qmul(a, b):
            w1, x1, y1, z1 = a.T; w2, x2, y2, z2 = b.T
            return np.stack([w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2, w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2, w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2, w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2], 1)
        qe = 0.5 * qmul(te, q0); sg = np.sign((q0 * q0[R.bi['pelvis']]).sum(1) + 1e-12)[:, None]; q0 = q0 * sg; qe = qe * sg
        b0 = Wt @ q0; be = Wt @ qe; n = np.linalg.norm(b0, axis=1, keepdims=True); b0 /= n; be /= n
        wq, v = b0[:, :1], b0[:, 1:]; t = 2 * (wq * be[:, 1:] - be[:, :1] * v + np.cross(v, be[:, 1:])); return P + 2 * np.cross(v, np.cross(v, P) + wq * P) + t
    def relcos_w(n0, P, el, Wt, T):
        dom = Wt[el].mean(1).argmax(1); Rq = np.stack([T[R.DB[i]][0] for i in range(len(R.DB))])[dom]; n0r = np.einsum('qij,qj->qi', Rq, n0)
        n1 = np.cross(P[el[:, 2]] - P[el[:, 0]], P[el[:, 3]] - P[el[:, 1]]) if el.shape[1] == 4 else np.cross(P[el[:, 1]] - P[el[:, 0]], P[el[:, 2]] - P[el[:, 0]])
        return (n0r * n1).sum(1) / (np.linalg.norm(n0r, axis=1) * np.linalg.norm(n1, axis=1) + 1e-12)
    def topo_test(T):
        P4 = dqs(R.V, W4, T); f4 = np.nonzero(relcos_w(R.n0, P4, Q, W4, T) < 0)[0]
        if not len(f4): return 0, 0, [], 0, 0
        cen = R.V[Q[f4]].mean(1); sv = np.unique(np.concatenate(kdd.query_ball_point(cen, 2.5))); Ff = Fd[np.isin(Fd, sv).all(1)]
        loc = -np.ones(len(Vd), np.int64); loc[sv] = np.arange(len(sv)); Ffl = loc[Ff]; Pv = Vd[sv]
        _, t_, c_ = igl.point_mesh_squared_distance(Pv, R.V, F); A_, B_, C_ = R.V[F[t_, 0]], R.V[F[t_, 1]], R.V[F[t_, 2]]
        u0 = B_ - A_; u1 = C_ - A_; u2 = c_ - A_; e00 = (u0 * u0).sum(1); e01 = (u0 * u1).sum(1); e11 = (u1 * u1).sum(1); e20 = (u2 * u0).sum(1); e21 = (u2 * u1).sum(1); de = e00 * e11 - e01 * e01
        b1 = (e11 * e20 - e01 * e21) / de; b2 = (e00 * e21 - e01 * e20) / de; bc_ = np.c_[1 - b1 - b2, b1, b2]; Wf = np.einsum('sk,skb->sb', bc_, W4[F[t_]])
        n0f = np.cross(Pv[Ffl[:, 1]] - Pv[Ffl[:, 0]], Pv[Ffl[:, 2]] - Pv[Ffl[:, 0]]); Pf = dqs(Pv, Wf, T); ff = np.nonzero(relcos_w(n0f, Pf, Ffl, Wf, T) < 0)[0]
        tq = f4
        flat = 0
        if len(ff):
            qc4 = P4[Q[f4]].mean(1); dd, _ = cKDTree(Pf[Ffl[ff]].mean(1)).query(qc4); foot = np.linalg.norm(P4[Q[f4]] - qc4[:, None], axis=2).max(1)
            flat = int((dd > 1.0).sum()); tq = f4[dd > 1.0 + foot]                 # co-located = within the quad footprint + 1 cm (RP5 PD-2 rule); flat-1cm count kept
        ncont = 0
        if len(tq):                                       # folds inside an interpenetration volume of the same smooth map belong to the contact, not the layout
            pen = FT.penetration(R, P4, F, w0)
            if pen.any():
                dp, _ = cKDTree(P4[pen]).query(P4[Q[tq]].mean(1)); inc = dp <= 1.0; ncont = int(inc.sum())
                if os.environ.get('TOPO_DEBUG'):
                    ddd = cKDTree(Pf[Ffl[ff]].mean(1)).query(P4[Q[tq]].mean(1))[0] if len(ff) else None; print('TOPO_DEBUG tq', len(tq), 'dist to pen', np.round(dp, 2), 'dist to src fold', None if ddd is None else np.round(ddd, 2), 'n src folds', len(ff), 'n pen', int(pen.sum()), flush=True)
                tq = tq[~inc]
        return int(len(tq)), int(len(f4)), [(str(R.ql[q]), np.round(R.V[Q[q]].mean(0), 1).tolist()) for q in tq[:12]], ncont, flat
    old = json.load(open(C.R + '/reviews/rac-rp5-evidence/saurin/full_cage/optionb_final/SA_deformation_4step_final.json'))['poses']
    LMc = {k: (v if cfg == 'M' else __import__('sa6_skeleton').transfer(v, R.V)) for k, v in R.LM.items()}
    lmv = {k: int(np.argmin(np.linalg.norm(R.V - p, axis=1))) for k, p in LMc.items()}
    El = np.unique(np.sort(np.r_[Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]], 1), axis=0); L0 = np.linalg.norm(R.V[El[:, 0]] - R.V[El[:, 1]], axis=1)
    rings = d['tail_rings']; digits = C.digit_components()
    def tipv(s_, pre, k):
        comp = digits[(s_, pre, k)]; b0 = R.V[d['loops']['%s_th_r1' % s_ if pre == 'th' else '%s_%s%d_base' % (s_, pre, k)]].mean(0)
        r2 = R.V[d['loops']['%s_th_r2' % s_ if pre == 'th' else '%s_%s%d_r2' % (s_, pre, k)]].mean(0); u = (r2 - b0) / np.linalg.norm(r2 - b0); return comp[np.argmax((R.V[comp] - b0) @ u)]
    def ring_area(P, rg):
        X = P[rg] - P[rg].mean(0); n = np.linalg.svd(X)[2][-1]; return 0.5 * abs((np.cross(X, np.roll(X, -1, 0)) @ n).sum())
    A0 = np.array([ring_area(R.V, rg) for rg in rings])
    def region_volume(P, labs, piv):
        qm = np.isin(R.ql, labs); a1, b1_, c1, d1 = (P[Q[qm, k]] - piv for k in range(4)); return (np.einsum('ij,ij->i', a1, np.cross(b1_, c1)) + np.einsum('ij,ij->i', a1, np.cross(c1, d1))).sum() / 6
    def gate_metrics(pn, T, P3, P4):
        g = {}
        if 'tail' in pn:
            cen = np.array([P4[rg].mean(0) for rg in rings]); dv = np.diff(cen, axis=0); dv /= np.linalg.norm(dv, axis=1, keepdims=True)
            th = np.degrees(np.arccos(np.clip((dv[1:] * dv[:-1]).sum(1), -1, 1))); win = np.array([th[max(0, k - 5):k + 6].mean() for k in range(len(th))])
            cen0 = np.array([R.V[rg].mean(0) for rg in rings]); dv0 = np.diff(cen0, axis=0); dv0 /= np.linalg.norm(dv0, axis=1, keepdims=True); th0 = np.degrees(np.arccos(np.clip((dv0[1:] * dv0[:-1]).sum(1), -1, 1)))
            ar = np.array([ring_area(P4, rg) for rg in rings[:-3]]) / A0[:-3]; ar3 = np.array([ring_area(P3, rg) for rg in rings[:-3]]) / A0[:-3]
            g['tail'] = dict(segments=16, ring_area_ratio_min=round(float(ar.min()), 4), ring_area_ratio_max=round(float(ar.max()), 4), ring_area_ratio_min_lbs=round(float(ar3.min()), 4),
                             worst_ring=int(ar.argmin()), turning_deg_max=round(float(th.max()), 3), turning_deg_max_neutral=round(float(th0.max()), 3),
                             kink_ratio_max=round(float((th / np.maximum(win, 0.05))[th > 0.2].max()) if (th > 0.2).any() else 1.0, 3), total_turning_deg=round(float(th.sum()), 2))
        for s_ in ('xpos', 'xneg'):
            if 'opposition' in pn and pn.endswith(s_):
                tt = P4[tipv(s_, 'th', 0)]; g['thumb_tip_to_finger_tip_cm'] = {('f%d' % k): round(float(np.linalg.norm(tt - P4[tipv(s_, 'f', k)])), 3) for k in range(1, 5)}
                g['thumb_tip_to_finger_tip_rest_cm'] = {('f%d' % k): round(float(np.linalg.norm(R.V[tipv(s_, 'th', 0)] - R.V[tipv(s_, 'f', k)])), 3) for k in range(1, 5)}
            t = 'l' if s_ == 'xpos' else 'r'; side = (R.V[Q].mean(1)[:, 0] > 0) if t == 'l' else (R.V[Q].mean(1)[:, 0] < 0)
            if pn.endswith(s_) and any(x in pn for x in ('fist', 'grasp', 'opposition', 'hand_', 'thumb')):
                hp = R.H('hand_' + t); hpp = T['hand_' + t][0] @ hp + T['hand_' + t][1]; ql_ = R.ql.copy(); m = np.isin(ql_, ['palm']) & side
                def vol(P, piv): a1, b1_, c1, d1 = (P[Q[m, k]] - piv for k in range(4)); return (np.einsum('ij,ij->i', a1, np.cross(b1_, c1)) + np.einsum('ij,ij->i', a1, np.cross(c1, d1))).sum() / 6
                g['palm_volume_ratio'] = round(float(vol(P4, hpp) / vol(R.V, hp)), 4); g['palm_volume_ratio_lbs'] = round(float(vol(P3, hpp) / vol(R.V, hp)), 4)
            if pn.endswith(s_) and any(x in pn for x in ('toe', 'ankle', 'foot')):
                ap = R.H('foot_' + t); app = T['foot_' + t][0] @ ap + T['foot_' + t][1]; m = np.isin(R.ql, ['foot', 'forefoot']) & side
                def vol(P, piv): a1, b1_, c1, d1 = (P[Q[m, k]] - piv for k in range(4)); return (np.einsum('ij,ij->i', a1, np.cross(b1_, c1)) + np.einsum('ij,ij->i', a1, np.cross(c1, d1))).sum() / 6
                g['foot_volume_ratio'] = round(float(vol(P4, app) / vol(R.V, ap)), 4)
                sole = m & (R.V[Q].mean(1)[:, 2] < R.V[Q[m]].mean((0, 1))[2]); nz = np.cross(P4[Q[sole, 2]] - P4[Q[sole, 0]], P4[Q[sole, 3]] - P4[Q[sole, 1]])
                g['sole_down_facing_fraction'] = round(float((nz[:, 2] < 0).mean()), 4); n0z = R.n0[sole]; g['sole_down_facing_fraction_rest'] = round(float((n0z[:, 2] < 0).mean()), 4)
        if 'jaw' in pn or 'head' in pn or 'neck' in pn:
            hb = 'head'; Rr, tr = T[hb]
            for k in ('rostrum_tip', 'eye_xpos', 'eye_xneg', 'crown'):
                vi = lmv[k]; g['head_rigid_err_%s_cm' % k] = round(float(np.linalg.norm(P4[vi] - (Rr @ R.V[vi] + tr))), 5)
            mc = np.r_[d['loops']['mouth_slit']]; em = np.isin(El, mc).any(1); s4 = np.linalg.norm(P4[El[em, 0]] - P4[El[em, 1]], axis=1) / L0[em]
            g['mouth_slit_edge_stretch_max'] = round(float(s4.max()), 4); g['mouth_slit_edge_stretch_min'] = round(float(s4.min()), 4)
            uj = R.W[:, R.bi['head']] > 0.999; g['upper_head_rigid_vertices_max_err_cm'] = round(float(np.linalg.norm(P4[uj] - (R.V[uj] @ Rr.T + tr), axis=1).max()), 6)
        return g
    res = {}
    for pn, spec in PS.items():
        t0 = time.time(); r = dict(fractions={})
        ent = FT.entries(R, spec, None)
        for fr in (0.25, 0.5, 0.75, 1.0):
            s_ = [(b_, p_, a_, dg * fr) for b_, p_, a_, dg in spec]; T = R.pose(s_); P3 = R.skin(T); f3 = np.nonzero(R.relcos(P3, T) < 0)[0]
            dl, act = Cr.delta(T, True); P4 = R.skin(T, R.V + dl); f4 = np.nonzero(R.relcos(P4, T) < 0)[0]
            pen4 = FT.penetration(R, P4, F, w0)
            r['fractions']['%.2f' % fr] = dict(lbs_flips=int(len(f3)), corrected_flips=int(len(f4)), corrected_flip_quads=[(str(R.ql[q]), np.round(R.V[Q[q]].mean(0), 1).tolist()) for q in f4[:8]],
                                               corrected_new_penetration_vertices=int(pen4.sum()), active_keys=int(sum(len(v[1]) > 0 for v in act.values())))
            if fr == 1.0:
                pen3 = FT.penetration(R, P3, F, w0)
                Pd = R.skin(T, Vs, Ws); fs = relcos_s(Pd, T) < 0
                r.update(step1_source_flips_sampled=int(fs.sum()), step1_source_flip_area_permille=round(float(1000 * sa_[fs].sum() / sa_.sum()), 4),
                         step3_lbs_flips=int(len(f3)), step3_lbs_flip_area_permille=round(float(1000 * qa[f3].sum() / qa.sum()), 4), step3_lbs_new_penetration_vertices=int(pen3.sum()),
                         penetration_centroid=np.round(P4[pen4].mean(0), 1).tolist() if pen4.any() else None)
                tt, n4, wh, nc4, fl1 = topo_test(T) if len(f3) else (0, 0, [], 0, 0); r.update(topology_only_flips=tt, smooth_map_cage_flips=n4, topology_quads=wh, smooth_map_folds_inside_contact_volume=nc4, smooth_map_folds_beyond_flat_1cm_of_source_folds=fl1)
                # metrics on the joint patches
                mets = {}
                for b_, pv, ax in ent:
                    p = R.par[b_]; lim = 0.6 * max(1.0, min(np.linalg.norm(R.Tl(p) - R.H(p)) if p and R.par[p] else 8.0, np.linalg.norm(R.Tl(b_) - R.H(b_))))
                    dv_ = np.linalg.norm(R.V - pv, axis=1); lim = max(lim, 2.0 * dv_.min()); reg = dv_ < lim; qm = reg[Q].all(1); pvp = T[b_][0] @ pv + T[b_][1]
                    if qm.sum() < 8: continue
                    def cone(P, piv): a1, b1_, c1, d1 = (P[Q[qm, k]] - piv for k in range(4)); return (np.einsum('ij,ij->i', a1, np.cross(b1_, c1)) + np.einsum('ij,ij->i', a1, np.cross(c1, d1))).sum() / 6
                    v0_ = cone(R.V, pv); em = reg[El].all(1); s4 = np.linalg.norm(P4[El[em, 0]] - P4[El[em, 1]], axis=1) / L0[em]; s3 = np.linalg.norm(P3[El[em, 0]] - P3[El[em, 1]], axis=1) / L0[em]
                    mets[b_] = dict(patch_radius_cm=round(float(lim), 2), volume_ratio_lbs=round(float(cone(P3, pvp) / v0_), 4), volume_ratio_corrected=round(float(cone(P4, pvp) / v0_), 4),
                                    stretch_corrected=[round(float(x), 3) for x in (s4.min(), np.percentile(s4, 1), np.percentile(s4, 99), s4.max())],
                                    stretch_lbs=[round(float(x), 3) for x in (s3.min(), np.percentile(s3, 1), np.percentile(s3, 99), s3.max())])
                r['joint_metrics'] = mets
                r['gate_metrics'] = gate_metrics(pn, T, P3, P4)
                lmd = {}
                for k, vi in lmv.items():
                    bdom = R.DB[int(R.W[vi].argmax())]; Rr, tr = T[bdom]; lmd[k] = float(np.linalg.norm(P4[vi] - (Rr @ R.V[vi] + tr)))
                rigid = {k: v for k, v in lmd.items() if R.W[lmv[k]].max() > 0.999}
                rv = R.W.max(1) > 0.999; bd = R.W[rv].argmax(1); Rb_ = np.stack([T[b][0] for b in R.DB]); tb_ = np.stack([T[b][1] for b in R.DB])
                drift = np.linalg.norm(P4[rv] - (np.einsum('vij,vj->vi', Rb_[bd], R.V[rv]) + tb_[bd]), axis=1)
                r['rigid_vertex_drift'] = dict(n_rigid_vertices=int(rv.sum()), max_cm=round(float(drift.max()), 4), p99_cm=round(float(np.percentile(drift, 99)), 4), gt_1mm=int((drift > 0.1).sum()))
                r['landmarks'] = dict(max_all_cm=round(max(lmd.values()), 3), max_all_name=max(lmd, key=lmd.get), max_rigid_cm=round(max(rigid.values()), 4) if rigid else 0.0, n_rigid=len(rigid))
        base = pn.replace('_rp5lit', ''); o = old.get(base) if (pn.endswith('_rp5lit') or pn + '_rp5lit' not in PS) else None
        r['step2_rp5_scaffold'] = (dict(step1_cage_flips=o['step1_cage_flips'], step3_improved=o['step3_cage_flips_improved_weights'], classification=o['classification']) if (o and cfg == 'M') else 'n/a (the RP5 scaffold baseline exists for c1 with the RP5-literal signs only; see the _rp5lit variant)')
        fx = r['fractions']; worst4 = max(v['corrected_flips'] for v in fx.values()); worst3 = max(v['lbs_flips'] for v in fx.values()); pen = max(v['corrected_new_penetration_vertices'] for v in fx.values())
        src = r['step1_source_flip_area_permille'] > 0 and r['step1_source_flip_area_permille'] >= r['step3_lbs_flip_area_permille']
        if pn == 'jaw_open_20_rp5lit': cls = 'CONTACT-SETUP (RP5-literal +20 deg closes the closed mouth: lower jaw driven into the upper rostrum; not a deformation pose)'
        elif worst4 and r['topology_only_flips']: cls = 'TOPOLOGY'
        elif worst4: cls = 'RIG-WEIGHTING (UNRESOLVED)'
        elif worst3: cls = 'RIG-WEIGHTING (resolved by correctives)'
        else: cls = 'CLEAN'
        if pen and pn != 'jaw_open_20_rp5lit': cls += ' + CONTACT-SETUP (tissue contact: %d new penetration vertices)' % pen
        if src: cls += ' + SOURCE-POSE (dense source folds at >= the LBS cage rate)'
        r['classification'] = cls; r['rig_owned_folds_after_correctives'] = int(worst4) if pn != 'jaw_open_20_rp5lit' else 0; res[pn] = r
        print('%-30s LBS %4d corr %3d pen %4d src %.3f/%.3f topo %d | %s  %.0fs' % (pn, worst3, worst4, pen, r['step1_source_flip_area_permille'], r['step3_lbs_flip_area_permille'], r['topology_only_flips'], cls[:60], time.time() - t0), flush=True)
    json.dump(dict(status='RP6 RIG PILOT / NOT FROZEN', config=cfg, weights=os.path.basename(wf), correctives=os.path.basename(cf), thresholds=TH, method=open(__file__).read().split('import')[0], poses=res), open(out, 'w'), indent=1)
if __name__ == '__main__': main()
