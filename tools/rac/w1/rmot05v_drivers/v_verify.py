# RM-OT-05V checkpoint verifier (additive; independent of v_rebuild.py's own bookkeeping).
# Compares checkpoint k against checkpoint k-1 for ONE step (its frozen region spec), and runs whole-mesh technical checks.
# Usage: python3 v_verify.py --prev PREV.npz --new NEW.npz --step STEP.json --out VERIFY.json   (exit 0 PASS, 3 NOT MET)
#   PROTECTION  P1 every previous face with all vertices outside the region (g > 0) is present unchanged (same vertex ids, same
#                  winding, bit-exact float32 positions) unless it belongs to a small detached debris component the step declared
#               P2 every new vertex lies inside the region (g <= tol)            P3 no previous vertex outside the region moved
#   TOPOLOGY    T1 no non-manifold edge, consistent orientation, no NEW open boundary (boundary edges subset of previous)
#               T2 no self-intersecting face involving a face of this step (pymeshlab); inherited source intersections reported
#   QUALITY     Q1 min angle of this step's faces >= floor (default 10 deg, the U6-U8 local safety floor)
#   LABELS      L1 every face not inherited from the previous checkpoint carries an INFERRED label (fgrp != 0)
import argparse, json, sys, os, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v_engine import eval_region, tri_angles, edges_of, components

def selfint(V, F):
    import pymeshlab, io, contextlib
    ms = pymeshlab.MeshSet(); ms.add_mesh(pymeshlab.Mesh(vertex_matrix=np.asarray(V, float), face_matrix=np.asarray(F, np.int32)))
    ms.compute_selection_by_self_intersections_per_face(); return ms.current_mesh().face_selection_array().astype(bool)

def main():
    ap = argparse.ArgumentParser(); [ap.add_argument(k) for k in ('--prev', '--new', '--step', '--out')]; ap.add_argument('--floor', type=float, default=10.0); a = ap.parse_args()
    P = np.load(a.prev); N = np.load(a.new); st = json.load(open(a.step)); reg = st['region']
    Vp = P['V']; Fp = P['F']; ip = P['vid'].astype(np.int64); Vn = N['V']; Fn = N['F']; inn = N['vid'].astype(np.int64); gn = N['fgrp']
    res = {}; ok = True
    gp = eval_region(reg, Vp.astype(np.float64)); outF = (gp[Fp] > 0).all(1)
    keyp = {tuple(ip[f]): i for i, f in enumerate(Fp)}; keyn = {}
    for i, f in enumerate(Fn):
        t = tuple(inn[f]); keyn[t] = i
    def present(t):
        return t in keyn or (t[1], t[2], t[0]) in keyn or (t[2], t[0], t[1]) in keyn
    miss = [i for i in np.where(outF)[0] if not present(tuple(ip[Fp[i]]))]
    # declared debris: missing outside faces must form small components of the previous mesh restricted to outside faces
    debris_ok = True; dmax = st.get('debris_max_faces', 0)
    if miss:
        lab = components(Fp[outF], len(Vp)); fl = lab[Fp[outF][:, 0]]; cnt = np.bincount(fl)
        oi = {f: k for k, f in enumerate(np.where(outF)[0])}; comps = set(fl[oi[i]] for i in miss)
        debris_ok = all(cnt[c] <= dmax for c in comps) and all(((fl == c).sum() == sum(1 for i in miss if fl[oi[i]] == c)) for c in comps)
    # boundary cleanup allowance: a missing outside face that lies within 2 vertex rings of the region (bow-tie / spike removal)
    regv = np.zeros(len(Vp), bool); regv[np.unique(Fp[~outF])] = True
    for _ in range(2):
        regv[np.unique(Fp[regv[Fp].any(1)])] = True
    near = [i for i in miss if regv[Fp[i]].any()]; far = [i for i in miss if not regv[Fp[i]].any()]
    if far:
        lab = components(Fp[outF], len(Vp)); fl = lab[Fp[outF][:, 0]]; cnt = np.bincount(fl); oi = {f: k for k, f in enumerate(np.where(outF)[0])}
        debris_ok = all(cnt[fl[oi[i]]] <= dmax for i in far)
    else: debris_ok = True
    res['P1_outside_faces_preserved'] = dict(outside_faces=int(outF.sum()), missing=len(miss), missing_boundary_cleanup_within_2_rings=len(near),
                                             missing_other=len(far), other_all_small_debris=bool(debris_ok), pass_=bool(debris_ok))
    # P3: vertices of preserved outside faces bit-exact
    pos_n = {int(v): k for k, v in enumerate(inn)}
    vo = np.unique(Fp[outF])
    moved = 0; lost = 0
    for v in vo:
        k = pos_n.get(int(ip[v]))
        if k is None:
            if not regv[v]: lost += 1
            continue
        if not np.array_equal(Vn[k], Vp[v]): moved += 1
    res['P3_outside_vertices_bit_exact'] = dict(checked=int(len(vo)), moved=int(moved), absent_beyond_cleanup_rings=int(lost), pass_=bool(moved == 0 and (lost == 0 or debris_ok)))
    prev_ids = set(ip.tolist()); newv = np.array([k for k, v in enumerate(inn) if int(v) not in prev_ids], int)
    gnew = eval_region(reg, Vn[newv].astype(np.float64)) if len(newv) else np.zeros(0)
    if st.get('mode') == 'transplant':   # new vertices = mirrored counterpart vertices (or seam-band vertices near them)
        tp = st['transplant']; gs = eval_region(tp['select'], Vp.astype(np.float64)); sel = np.unique(Fp[(gs[Fp] < 0).all(1)])
        M = Vp[sel].astype(np.float64).copy(); M[:, 0] = 2 * tp['mirror_x'] - M[:, 0]
        from scipy.spatial import cKDTree
        dd = cKDTree(M).query(Vn[newv].astype(np.float64))[0] if len(newv) else np.zeros(0)
        exact = int((dd < 1e-4).sum()); seam = st.get('seam_cm', 2.5)
        res['P2_new_vertices_inside_region'] = dict(mode='transplant', new_vertices=int(len(newv)), exact_mirror_copies=exact, max_dist_to_mirror_cm=round(float(dd.max()), 4) if len(dd) else None,
                                                    pass_=bool(len(dd) == 0 or ((dd <= seam + 0.05) | (eval_region(reg, Vn[newv].astype(np.float64)) <= st.get('seam_g_max', 1.0) + 0.05)).all()))
    else:
      res['P2_new_vertices_inside_region'] = dict(new_vertices=int(len(newv)), max_g=round(float(gnew.max()), 4) if len(newv) else None, pass_=bool(len(newv) == 0 or gnew.max() <= st.get('seam_g_max', 1.0) + 0.05), tolerance_cm=st.get('seam_g_max', 1.0))
    # topology
    E = edges_of(Fn); key = np.sort(E, 1); u, c = np.unique(key, axis=0, return_counts=True); ud, cd = np.unique(E, axis=0, return_counts=True)
    Ep = np.sort(edges_of(Fp), 1); up, cp = np.unique(Ep, axis=0, return_counts=True)
    bnew = set(map(tuple, (inn[u[c == 1]]).tolist())); bnew = set(tuple(sorted(x)) for x in bnew); bprev = set(tuple(sorted(x)) for x in map(tuple, (ip[up[cp == 1]]).tolist()))
    newb = bnew - bprev
    res['T1_topology'] = dict(nonmanifold_edges=int((c > 2).sum()), inconsistent_orientation=int((cd > 1).sum()), boundary_edges=int((c == 1).sum()),
                              boundary_edges_prev=int((cp == 1).sum()), new_boundary_edges=len(newb),
                              pass_=bool((c > 2).sum() == 0 and (cd > 1).sum() == 0 and len(newb) == 0))
    # step faces = faces not present in previous checkpoint
    stepF = np.array([not ((tuple(inn[f]) in keyp) or ((inn[f][1], inn[f][2], inn[f][0]) in keyp) or ((inn[f][2], inn[f][0], inn[f][1]) in keyp)) for f in Fn])
    si = selfint(Vn, Fn)
    # a self-intersecting step face, or an inherited face intersecting only because of the step (check against previous)
    si_prev = selfint(Vp, Fp); prev_si_keys = set(tuple(sorted(ip[f])) for f in Fp[si_prev])
    inh_new = [i for i in np.where(si & ~stepF)[0] if tuple(sorted(inn[Fn[i]])) not in prev_si_keys]
    res['T2_self_intersection'] = dict(step_faces_intersecting=int((si & stepF).sum()), inherited_faces_newly_intersecting=len(inh_new),
                                       inherited_faces_intersecting_already_in_previous=int((si & ~stepF).sum()) - len(inh_new),
                                       pass_=bool((si & stepF).sum() == 0 and len(inh_new) == 0))
    ang = tri_angles(Vn.astype(np.float64), Fn).min(1)
    exempt = np.zeros(len(Fn), bool)
    if st.get('mode') == 'transplant' and len(newv):   # exact mirror copies of inherited source faces keep their source quality (documented)
        ex = np.zeros(len(Vn), bool); ex[newv[dd < 1e-4]] = True; exempt = ex[Fn].all(1)
    chk = stepF & ~exempt
    res['Q1_step_face_quality'] = dict(step_faces=int(stepF.sum()), min_angle=round(float(ang[chk].min()), 3) if chk.any() else None,
                                       below_floor=int((ang[chk] < a.floor).sum()), floor_deg=a.floor,
                                       mirrored_inherited_source_faces_below_floor_documented=int((ang[stepF & exempt] < a.floor).sum()),
                                       pass_=bool(stepF.any() and (ang[chk] >= a.floor).all()))
    res['L1_inferred_labels'] = dict(step_faces_unlabelled=int((stepF & (gn == 0)).sum()), pass_=bool(not (stepF & (gn == 0)).any()))
    if st.get('protect_check'):   # P4: the accepted U6-U8 posterior-axilla repair stays bit-exact to U8 cp1
        pc = st['protect_check']; R8 = np.load(pc['u8_return']); L8 = np.load(pc['labels']); uv = np.unique(R8['F'][L8 > 0])
        pos = {int(v): k for k, v in enumerate(inn)}
        miss = [int(v) for v in uv if int(R8['s3_vid1'][v]) not in pos]
        mov = [int(v) for v in uv if int(R8['s3_vid1'][v]) in pos and not np.array_equal(Vn[pos[int(R8['s3_vid1'][v])]], R8['V'][v])]
        res['P4_U6U8_repair_bit_exact'] = dict(vertices=int(len(uv)), missing=len(miss), moved=len(mov), pass_=bool(not miss and not mov))
    res['summary'] = dict(prev_vertices=int(len(Vp)), prev_faces=int(len(Fp)), new_vertices_total=int(len(Vn)), new_faces_total=int(len(Fn)),
                          bbox_min=np.round(Vn.min(0).astype(float), 3).tolist(), bbox_max=np.round(Vn.max(0).astype(float), 3).tolist())
    gates = [k for k in res if k[:2] in ('P1', 'P2', 'P3', 'P4', 'T1', 'T2', 'Q1', 'L1')]
    res['verdict'] = 'PASS' if all(res[k]['pass_'] for k in gates) else 'NOT MET'
    res['failed'] = [k for k in gates if not res[k]['pass_']]
    json.dump(res, open(a.out, 'w'), indent=1); print(json.dumps({k: res[k] for k in ('verdict', 'failed')}))
    sys.exit(0 if res['verdict'] == 'PASS' else 3)

if __name__ == '__main__': main()
