# RM-OT-05V: apply ONE neutralization step (a bounded region rebuild) to a checkpoint state.
# State npz: V float32 (n,3) cm, F int64 (m,3), vid int32 (S3 rac_s3_vid1, 0 = new INFERRED vertex), fgrp int8 per face
#            (0 = source surface, 1..5 = INFERRED by group A..E, 9 = bridge seam, also INFERRED).
# Usage: python3 v_rebuild.py --state IN.npz --step STEP.json --out OUT.npz [--log LOG.json]
import argparse, json, time, numpy as np, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v_engine import *
import v_fields

def load_state(p):
    d = np.load(p); return dict(V=d['V'].astype(np.float32), F=d['F'].astype(np.int64), vid=d['vid'].astype(np.int64), fgrp=d['fgrp'].astype(np.int8))

def save_state(p, S, **meta):
    np.savez_compressed(p, V=S['V'].astype(np.float32), F=S['F'].astype(np.int64), vid=S['vid'].astype(np.int64), fgrp=S['fgrp'].astype(np.int8),
                        meta=json.dumps(meta))

def rebuild(S, step, log):
    t0 = time.time()
    def tick(msg): print('[%6.1fs] %s' % (time.time() - t0, msg), file=sys.stderr, flush=True)
    V32 = S['V']; V = V32.astype(np.float64); F = S['F']; nv = len(V)
    reg = step['region']; t = step.get('t', 3.0); h = step.get('h', 1.0); res = step.get('res', 0.45)
    gV = eval_region(reg, V)
    rmF = (gV[F] <= 0).any(1)
    # optional: also drop small detached kept components touched by the region (garment debris), never the main body
    keepF = ~rmF
    lab = components(F[keepF], nv); used = np.unique(F[keepF]); sizes = np.bincount(lab[used], minlength=lab.max() + 1)
    main = np.argmax(sizes); comp_of_face = lab[F[keepF][:, 0]]
    debris_max = step.get('debris_max_faces', 0)
    if debris_max:
        cf = np.bincount(comp_of_face, minlength=lab.max() + 1)
        near = np.zeros(lab.max() + 1, bool)
        touch = np.unique(lab[np.unique(F[rmF])])
        near[touch] = True
        drop_c = np.where((cf > 0) & (cf <= debris_max) & near & (np.arange(len(cf)) != main))[0]
        if step.get('debris_keep_points'):   # anatomy anchors (e.g. a hand below a rebuilt forearm) are never debris
            kp = np.asarray(step['debris_keep_points'], float); vk = cKDTree(V).query(kp)[1]
            drop_c = np.setdiff1d(drop_c, lab[vk])
        dropF = np.isin(comp_of_face, drop_c); kf = np.where(keepF)[0]; keepF[kf[dropF]] = False
        log['debris_components_dropped'] = int(len(drop_c)); log['debris_faces_dropped'] = int(dropF.sum())
    # boundary cleanup: no bow-tie boundary vertices, no kept face hanging by >= 2 boundary edges (makes simple, bridgeable loops)
    ncl = 0
    for _ in range(12):
        KFt = F[keepF]; E = edges_of(KFt); key = np.sort(E, 1); u, inv, c = np.unique(key, axis=0, return_inverse=True, return_counts=True)
        be = c[inv.ravel()] == 1; bcount = np.bincount(E[be].ravel(), minlength=nv)
        fb = be.reshape(3, -1).sum(0)                      # boundary edges per kept face
        bad_v = bcount > 2
        badf = (fb >= 2) | bad_v[KFt].any(1)
        # only touch faces next to the removed area
        rmv0 = np.zeros(nv, bool); rmv0[np.unique(F[~keepF])] = True; badf &= rmv0[KFt].any(1)
        if not badf.any(): break
        kf = np.where(keepF)[0]; keepF[kf[badf]] = False; ncl += int(badf.sum())
    log['boundary_cleanup_faces'] = ncl
    removed_faces = np.where(~keepF)[0]
    # grid
    transplant = step.get('mode') == 'transplant'
    if not transplant:
        box = step['box']; G = Grid(box[0], box[1], res)
        tick('sdf')
        phi_src = sdf_on_grid(V, F, G)
        P = G.points(); gG = eval_region(reg, P).reshape(G.n)
        phi_inf = v_fields.build(step.get('field', {}), phi_src, G, P, S, log)
        phi = blend(phi_src, phi_inf, gG, t)
        # never extract outside the region influence: outside the region phi_src is kept implicitly by the kept faces
        tick('nets')
        Vn, T = surface_nets(phi, G)
        # orientation check against the field gradient
        n, _ = face_normals(Vn, T); gr = G.grad(phi, Vn[T].mean(1)); sgn = np.sign((n * gr).sum(1))
        if (sgn < 0).mean() > 0.5: T = T[:, ::-1]
        log['orientation_flipped'] = bool((sgn < 0).mean() > 0.5)
        gN = eval_region(reg, Vn); pf = (gN[T] < -h).all(1); T = T[pf]
        # keep patch components that reach the region boundary band (have a boundary loop); drop closed floating blobs
        ui = np.unique(T); mp = -np.ones(len(Vn), np.int64); mp[ui] = np.arange(len(ui)); Vn = Vn[ui]; T = mp[T]
        labn = components(T, len(Vn)); loopsP = boundary_loops(T)
        has_loop = np.zeros(labn.max() + 1, bool)
        for lp in loopsP: has_loop[labn[lp[0]]] = True
        minf = step.get('min_patch_component_faces', 200)
        cfaces = np.bincount(labn[T[:, 0]], minlength=labn.max() + 1)
        keepc = has_loop & (cfaces >= minf); kT = keepc[labn[T[:, 0]]]
        log['patch_components'] = int((cfaces > 0).sum()); log['patch_components_kept'] = int(keepc.sum()); log['patch_faces_dropped'] = int((~kT).sum())
        T = T[kT]; ui = np.unique(T); mp = -np.ones(len(Vn), np.int64); mp[ui] = np.arange(len(ui)); Vn = Vn[ui]; T = mp[T]
        gN2 = eval_region(reg, Vn); Vn, T = repair_patch(Vn, T, gN2 < -(h + 1.0), log)
    else:
        # bilateral counterpart transplant: mirror the selected faces of the current mesh across x = mirror_x (no field, no remesh)
        tp = step['transplant']; gS = eval_region(tp['select'], V); fs = (gS[F] < 0).all(1) & keepF
        Fs = F[fs]; u = np.unique(Fs); mp = -np.ones(nv, np.int64); mp[u] = np.arange(len(u)); Vn = V[u].copy(); T = mp[Fs][:, ::-1].copy()
        Vn[:, 0] = 2 * tp['mirror_x'] - Vn[:, 0]
        # keep the largest component (the limb), drop selection crumbs
        labn = components(T, len(Vn)); cf = np.bincount(labn[T[:, 0]]); T = T[labn[T[:, 0]] == np.argmax(cf)]
        ui = np.unique(T); mp2 = -np.ones(len(Vn), np.int64); mp2[ui] = np.arange(len(ui)); Vn = Vn[ui]; T = mp2[T]
        log['transplant_faces'] = int(len(T)); log['transplant_source_vids'] = int(len(ui))
        phi = None; G = None
    loopsP = boundary_loops(T); log['nm_patch'] = nm_count(T)
    # kept boundary loops created by the removal (pre-existing open boundaries are reported separately)
    KF = F[keepF]; loopsK = boundary_loops(KF)
    pre = set(np.unique(np.concatenate(boundary_loops(F)) if len(boundary_loops(F)) else np.zeros(0, int)).tolist())
    rmv = np.zeros(nv, bool); rmv[np.unique(F[~keepF])] = True
    newK = [lp for lp in loopsK if any(rmv[v] for v in lp)]
    oldK = [lp for lp in loopsK if not any(rmv[v] for v in lp)]
    log['kept_new_loops'] = [len(l) for l in newK]; log['patch_loops'] = [len(l) for l in loopsP]; log['kept_preexisting_open_loops'] = [len(l) for l in oldK]
    # assemble
    off = nv; Vall = np.concatenate([V, Vn]); PL = [[v + off for v in lp] for lp in loopsP]
    cK = np.array([V[lp].mean(0) for lp in newK]) if newK else np.zeros((0, 3)); cP = np.array([Vall[lp].mean(0) for lp in PL]) if PL else np.zeros((0, 3))
    if step.get('debug'):
        np.savez(step['debug'], Vn=Vn, T=T, K=np.concatenate([V[l] for l in newK]) if newK else np.zeros((0, 3)),
                 Kid=np.concatenate([np.full(len(l), i) for i, l in enumerate(newK)]) if newK else np.zeros(0),
                 P=np.concatenate([Vall[l] for l in PL]) if PL else np.zeros((0, 3)), Pid=np.concatenate([np.full(len(l), i) for i, l in enumerate(PL)]) if PL else np.zeros(0))
    tick('pairing')
    from scipy.optimize import linear_sum_assignment
    C = np.full((len(newK), len(PL)), 1e6)
    for i, lp in enumerate(newK):
        tree = cKDTree(Vall[lp])
        for j, pl in enumerate(PL):
            if np.linalg.norm(Vall[lp].mean(0) - Vall[pl].mean(0)) > 60: continue
            d1 = tree.query(Vall[pl])[0].mean(); d2 = cKDTree(Vall[pl]).query(Vall[lp])[0].mean(); C[i, j] = max(d1, d2)
    r_, c_ = linear_sum_assignment(C) if C.size else (np.zeros(0, int), np.zeros(0, int))
    maxgap = step.get('max_loop_gap_cm', 4.0)
    pairs = [(i, j, float(C[i, j])) for i, j in zip(r_, c_) if C[i, j] <= maxgap]
    pk = {i for i, j, d in pairs}; pp = {j for i, j, d in pairs}
    log['loop_pairs'] = [dict(kept_len=len(newK[i]), patch_len=len(PL[j]), mean_gap_cm=round(d, 3)) for i, j, d in pairs]
    capK = [newK[i] for i in range(len(newK)) if i not in pk]; capP = [PL[j] for j in range(len(PL)) if j not in pp]
    maxcap = step.get('max_cap_loop', 400)
    if any(len(l) > maxcap for l in capK + capP) or len(capK + capP) > 40:
        raise RuntimeError('unpaired loop too large to cap: kept %s patch %s' % ([len(l) for l in capK], [len(l) for l in capP]))
    log['capped_kept_loops'] = [len(l) for l in capK]; log['capped_patch_loops'] = [len(l) for l in capP]
    CAPT = []; ncapf = 0
    for lp in capK + capP:
        if len(lp) < 3:
            log.setdefault('degenerate_loops_skipped', []).append(len(lp)); continue
        r = cap_fill(Vall, lp)
        if r is None:   # fallback: centroid fan
            ci = len(Vall); Vall = np.concatenate([Vall, Vall[lp].mean(0)[None]])
            for q in range(len(lp)): CAPT.append((lp[(q + 1) % len(lp)], lp[q], ci))
            ncapf += 1
        else:
            nvx, tri = r; Vall = np.concatenate([Vall, nvx]); CAPT.extend(tri.tolist())
    log['cap_fill_fallback_fans'] = ncapf
    BT = []
    for i, j, d in pairs:
        bt, rev = bridge(Vall, newK[i], PL[j]); BT.append(bt)
    tick('bridged')
    BT = np.concatenate(BT + ([np.array(CAPT, np.int64)] if CAPT else [])) if (BT or CAPT) else np.zeros((0, 3), np.int64)
    Fall = np.concatenate([KF, T + off, BT])
    gr_new = step['group_code']
    fg_keep = S['fgrp'][keepF].copy()
    log['nm_assembled'] = nm_count(Fall)
    gmax = step.get('seam_g_max', 1.0)
    def clampP(Pp):
        Pp = Pp.copy()
        for _ in range(4):
            gg = eval_region(reg, Pp); o = gg > gmax
            if not o.any(): break
            e = 1e-3; q = Pp[o]; grad = np.stack([(eval_region(reg, q + e * np.eye(3)[k]) - gg[o]) / e for k in range(3)], 1)
            Pp[o] = q - ((gg[o] - gmax) / np.maximum((grad * grad).sum(1), 1e-6))[:, None] * grad
        return Pp
    def clamp(Vx, mv):
        Vx = Vx.copy(); Vx[mv] = clampP(Vx[mv]); return Vx
    movable = np.zeros(len(Vall), bool); movable[off:] = True
    fixed = np.zeros(len(Fall), bool); fixed[:len(KF)] = True
    # seam fairing: pure Laplacian on new vertices within seam_cm of the kept boundary (no projection), then projected quality passes
    seam_cm = step.get('seam_cm', 2.5); bverts = np.unique(np.concatenate(newK)) if newK else np.zeros(0, int)
    if len(bverts):
        dseam = cKDTree(V[bverts]).query(Vall[off:])[0]; near = np.zeros(len(Vall), bool); near[off:] = dseam < seam_cm
        Vall = relax(Vall, Fall, near, clampP, n=step.get('seam_iters', 6), lam=0.5)
    def project(Pp):
        if transplant: return Pp
        for _ in range(2):
            f = G.sample(phi, Pp); g = G.grad(phi, Pp); gg = np.maximum((g * g).sum(1), 1e-6); Pp = Pp - (f / gg)[:, None] * g
        return Pp
    # projection only away from the seam (seam band keeps its faired shape)
    far = movable.copy()
    if len(bverts): far[off:] &= dseam >= seam_cm
    if transplant:   # only the seam band may move; the transplanted limb keeps its (mirrored) source positions
        mv2 = near.copy() if len(bverts) else np.zeros(len(Vall), bool)
        mv2[off + len(Vn):] = True          # cap-fill vertices may always move
        movable = mv2
    else:
        tick('improve')
    Vall, Fall = improve(Vall, Fall, far, project, fixed, iters=step.get('quality_iters', 5), movable_all=movable)
    Fall = flip_pass(Vall, Fall, fixed, movable); log['nm_improved'] = nm_count(Fall)
    Vall = clamp(Vall, movable)
    tick('fix_slivers')
    for _pass in range(3):
        Vall, Fall, fixed, movable = fix_slivers(Vall, Fall, movable, fixed, floor=step.get('angle_floor', 12.0), log=log, project=clampP)
        Vall = clamp(Vall, movable)
        if not ((tri_angles(Vall, Fall).min(1) < step.get('angle_floor', 12.0)) & ~fixed).any(): break
    tick('selfint')
    # local self-intersection repair on this step's faces (relax the involved new vertices + 2 rings, then re-fix quality)
    try:
        from v_verify import selfint
        for rr in range(5):
            si = selfint(Vall, Fall) & ~fixed
            if not si.any(): break
            mv = np.zeros(len(Vall), bool); mv[np.unique(Fall[si])] = True
            for _ in range(2): mv[np.unique(Fall[mv[Fall].any(1)])] = True
            mv &= movable
            Vall = relax(Vall, Fall, mv, clampP, n=4, lam=0.6); Fall = flip_pass(Vall, Fall, fixed, movable)
            log.setdefault('selfint_repair_rounds', []).append(int(si.sum()))
        if log.get('selfint_repair_rounds'):
            Vall, Fall, fixed, movable = fix_slivers(Vall, Fall, movable, fixed, floor=step.get('angle_floor', 12.0), log=log, project=clampP)
        # persistent folds: excise the intersecting new faces (+3 rings of new faces) and refill each hole with a relaxed disk
        for rr in range(3):
            si = selfint(Vall, Fall) & ~fixed
            if not si.any(): break
            cut = si.copy()
            for _ in range(3):
                vv = np.zeros(len(Vall), bool); vv[np.unique(Fall[cut])] = True; cut = vv[Fall].any(1) & ~fixed
            Fk = Fall[~cut]; fx = fixed[~cut]; loops_cut = [lp for lp in boundary_loops(Fk) if any(v in set(np.unique(Fall[cut]).tolist()) for v in lp)]
            addF = []
            for lp in loops_cut:
                r = cap_fill(Vall, lp)
                if r is None: continue
                nvx, tri = r; Vall = np.concatenate([Vall, nvx]); movable = np.r_[movable, np.ones(len(nvx), bool)]; addF.append(tri)
            Fall = np.vstack([Fk] + addF); fixed = np.r_[fx, np.zeros(sum(len(x) for x in addF), bool)]
            Vall = relax(Vall, Fall, movable & np.isin(np.arange(len(Vall)), np.unique(np.vstack(addF)) if addF else []), clampP, n=6, lam=0.5)
            Vall, Fall, fixed, movable = fix_slivers(Vall, Fall, movable, fixed, floor=step.get('angle_floor', 12.0), log=log, project=clampP)
            log.setdefault('fold_excise_rounds', []).append(dict(si=int(si.sum()), cut=int(cut.sum()), holes=len(loops_cut)))
    except ImportError:
        pass
    # close tiny holes made only of new vertices (bow-tie leftovers of the extracted patch)
    pre_b = set(map(tuple, np.sort(np.array([e for l in boundary_loops(F) for e in zip(l, l[1:] + l[:1])]), 1).tolist())) if len(boundary_loops(F)) else set()
    nclose = 0
    for lp in boundary_loops(Fall):
        if len(lp) < 3 or len(lp) > 12 or any(v < off for v in lp): continue
        if len(lp) == 3: Fall = np.vstack([Fall, [[lp[2], lp[1], lp[0]]]]); fixed = np.r_[fixed, False]; nclose += 1; continue
        r = cap_fill(Vall, lp)
        if r is None: continue
        nvx, tri = r; Vall = np.concatenate([Vall, nvx]); movable = np.r_[movable, np.ones(len(nvx), bool)]; Fall = np.vstack([Fall, tri]); fixed = np.r_[fixed, np.zeros(len(tri), bool)]; nclose += 1
    log['tiny_holes_closed'] = nclose
    log['nm_fixed'] = nm_count(Fall)
    fg = np.concatenate([fg_keep, np.full(len(Fall) - len(fg_keep), 0, np.int8)])
    # face group labels after flips/collapses: kept faces are untouched (fixed), all others are this step's INFERRED faces;
    # bridge faces = new faces that use at least one kept vertex
    usesk = (Fall[len(fg_keep):] < off).any(1); fg[len(fg_keep):] = np.where(usesk, 9, gr_new)
    # post-step crumbs: detached components smaller than debris_max (never the main body) are dropped and logged
    stepm = np.r_[np.zeros(len(fg_keep), bool), np.ones(len(Fall) - len(fg_keep), bool)]
    lab_ = components(Fall, len(Vall)); fl_ = lab_[Fall[:, 0]]; cnt_ = np.bincount(fl_); main_ = np.argmax(cnt_)
    crumbs = (fl_ != main_) & (cnt_[fl_] <= step.get('debris_max_faces', 0))
    if crumbs.any():
        log['post_crumbs_dropped_faces'] = int(crumbs.sum()); Fall = Fall[~crumbs]; fixed = fixed[~crumbs]; fg = fg[~crumbs]; stepm = stepm[~crumbs]
    tick('compact')
    # compact
    ui = np.unique(Fall); mp = -np.ones(len(Vall), np.int64); mp[ui] = np.arange(len(ui))
    Vout = Vall[ui]; Fout = mp[Fall]; vid = np.concatenate([S['vid'].astype(np.int64), step['vid_base'] + np.arange(len(Vall) - nv, dtype=np.int64)])[ui]
    # kept vertices must be bit-exact copies
    keptmask = ui < nv; assert np.array_equal(Vout[keptmask].astype(np.float32), V32[ui[keptmask]]), 'kept vertex moved'
    Vout32 = Vout.astype(np.float32); Vout32[keptmask] = V32[ui[keptmask]]
    newF = fg != 0
    ang = tri_angles(Vout, Fout)
    log.update(dict(removed_faces=int(len(removed_faces)), removed_vertices=int((~np.isin(np.arange(nv), ui)).sum()),
                    removed_vids=sorted(set(S['vid'][np.setdiff1d(np.arange(nv), ui)].tolist()) - {0})[:0],
                    new_vertices=int((~keptmask).sum()), new_faces_this_step=int(stepm.sum()),
                    min_angle_this_step=round(float(ang[stepm].min()), 2), faces_below_10deg_this_step=int((ang[stepm].min(1) < 10).sum()),
                    faces_below_floor_this_step=int((ang[stepm].min(1) < step.get('angle_floor', 12.0)).sum()),
                    seconds=round(time.time() - t0, 1)))
    out = dict(V=Vout32, F=Fout, vid=vid, fgrp=fg)
    removed_v = np.setdiff1d(np.arange(nv), ui)
    return out, removed_faces, removed_v

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--state'); ap.add_argument('--step'); ap.add_argument('--out'); ap.add_argument('--log'); a = ap.parse_args()
    S = load_state(a.state); step = json.load(open(a.step)); log = dict(step=step.get('name'))
    out, rf, rv = rebuild(S, step, log)
    save_state(a.out, out, step=step.get('name'))
    np.savez_compressed(a.out.replace('.npz', '_removed.npz'), removed_faces=rf, removed_vertex_vids=S['vid'][rv], removed_vertices_prev_index=rv)
    if a.log: json.dump(log, open(a.log, 'w'), indent=1)
    print(json.dumps(log))
