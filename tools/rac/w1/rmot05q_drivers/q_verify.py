# RM-OT-05Q verification V1-V6 of a patch result against the committed plan (plan/PLAN.md).
# Usage: python3 q_verify.py --src F1_working.obj --sel plan/ --res GO-05Q-<tag>.obj --out OUTPREFIX [--ramp 3.0]
import argparse, json, hashlib, os, numpy as np, trimesh
from scipy.spatial import cKDTree
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
ap = argparse.ArgumentParser(); ap.add_argument('--src'); ap.add_argument('--sel'); ap.add_argument('--res'); ap.add_argument('--out'); ap.add_argument('--ramp', type=float, default=3.0); a = ap.parse_args()
s0 = trimesh.load(a.src, process=False); V = np.asarray(s0.vertices); F = np.asarray(s0.faces)
r0 = trimesh.load(a.res, process=False); Vr = np.asarray(r0.vertices); Fr = np.asarray(r0.faces)
J = json.load(open(os.path.join(a.sel, 'patch_selection.json'))); Z = np.load(os.path.join(a.sel, 'patch_face_sets.npz')); P = Z['P']; nP = len(P)
vmap = np.load(a.res.replace('.obj', '_vertex_map.npy')); lab = np.load(a.res.replace('.obj', '_face_labels.npy'))
O = np.array(J['frame']['origin']); d = np.array(J['frame']['axis']); d /= np.linalg.norm(d); e1 = np.cross([0, 1, 0], d); e1 /= np.linalg.norm(e1); e2 = np.cross(d, e1)
def tsr(X):
    c = X - O; s = c @ d; return np.degrees(np.arctan2(c @ e2, c @ e1)), s, np.hypot(c @ e1, c @ e2)
out = {}
# V1 protected faces / coordinates
h_plan = '28d2b7aed535275fe9a176b977fc0199f79c5a19af7c5a88f99062c59edfaa34'
h_res = hashlib.sha256(np.ascontiguousarray(Vr[Fr[:nP]]).astype(np.float64).tobytes()).hexdigest()
idx_ok = bool((vmap[Fr[:nP]] == F[P]).all()); coord_ok = bool((Vr[:len(vmap)] == V[vmap]).all())
out['V1'] = dict(pass_=bool(h_res == h_plan and idx_ok and coord_ok), protected_coord_sha256=h_res, plan_sha256=h_plan, index_correspondence=idx_ok, kept_vertices_bit_identical=coord_ok, protected_faces=nP)
# V2 boundary / manifold / orientation / degenerate
def edges_info(FF):
    he = np.r_[FF[:, [0, 1]], FF[:, [1, 2]], FF[:, [2, 0]]]; srt = np.sort(he, 1); u, inv, cnt = np.unique(srt, axis=0, return_inverse=True, return_counts=True)
    return he, srt, u, inv.ravel(), cnt
he, srt, u, inv, cnt = edges_info(Fr); bnd_r = u[cnt == 1]; nonman = int((cnt > 2).sum())
_, _, u0, _, c0 = edges_info(F); bnd_s = u0[c0 == 1]
bnd_r_src = np.sort(np.where(bnd_r < len(vmap), vmap[np.minimum(bnd_r, len(vmap) - 1)], -1), 1)
same_bnd = bool(len(bnd_r) == len(bnd_s) and (bnd_r_src >= 0).all() and set(map(tuple, bnd_r_src.tolist())) == set(map(tuple, np.sort(bnd_s, 1).tolist())))
# orientation: every interior edge must appear once in each direction
two = np.where(cnt == 2)[0]; pair = {}
dirs = {}
for k_, (x, y) in enumerate(he):
    dirs.setdefault(inv[k_], []).append((x, y))
newF = np.arange(nP, len(Fr)); touch = set(inv[np.r_[newF, newF + len(Fr), newF + 2 * len(Fr)]].tolist())
bad_orient = sum(1 for e in touch if len(dirs[e]) == 2 and dirs[e][0] == dirs[e][1])
area = trimesh.triangles.area(Vr[Fr[newF]]); degen = int((area < 1e-6).sum())
out['V2'] = dict(pass_=bool(same_bnd and nonman == 0 and bad_orient == 0 and degen == 0), boundary_edges=int(len(bnd_r)), source_boundary_edges=int(len(bnd_s)),
                 boundary_identical_to_source=same_bnd, nonmanifold_edges=nonman, inconsistent_orientation_edges_at_patch=int(bad_orient), degenerate_new_faces=degen)
# V3 self-intersection (segment-triangle tests), new faces vs all faces within 6 cm; pre-existing source pairs listed separately
def seg_tri(p0, p1, A, B, C):
    e1_, e2_ = B - A, C - A; dd = p1 - p0; h = np.cross(dd, e2_); det = (e1_ * h).sum(-1); ok = np.abs(det) > 1e-12
    inv_ = np.where(ok, 1 / np.where(ok, det, 1), 0); s_ = p0 - A; uu = (s_ * h).sum(-1) * inv_; q = np.cross(s_, e1_); vv = (dd * q).sum(-1) * inv_; t = (e2_ * q).sum(-1) * inv_
    eps = 1e-9; return ok & (uu > eps) & (vv > eps) & (uu + vv < 1 - eps) & (t > eps) & (t < 1 - eps)
def tri_pairs_intersect(VV, FF, ia, ib):
    T1, T2 = VV[FF[ia]], VV[FF[ib]]; hit = np.zeros(len(ia), bool)
    for (i, j) in ((0, 1), (1, 2), (2, 0)):
        hit |= seg_tri(T1[:, i], T1[:, j], T2[:, 0], T2[:, 1], T2[:, 2]); hit |= seg_tri(T2[:, i], T2[:, j], T1[:, 0], T1[:, 1], T1[:, 2])
    return hit
def candidates(VV, FF, set_a, set_b, rad=3.0):
    ca = VV[FF[set_a]].mean(1); cb = VV[FF[set_b]].mean(1); tb = cKDTree(cb); L = tb.query_ball_point(ca, rad)
    ia = np.repeat(set_a, [len(l) for l in L]); ib = set_b[np.concatenate([np.array(l, int) for l in L])] if len(ia) else np.array([], int)
    keep = ia != ib; ia, ib = ia[keep], ib[keep]
    share = (FF[ia][:, :, None] == FF[ib][:, None, :]).any((1, 2)); return ia[~share], ib[~share]
cen = Vr[Fr[newF]].mean(1).mean(0); allc = Vr[Fr].mean(1); nearF = np.where(np.linalg.norm(allc - cen, axis=1) < 30)[0]
box = np.where(np.min(np.linalg.norm(allc[nearF][:, None] - Vr[Fr[newF]].mean(1)[None, ::4], axis=2), 1) < 6)[0]; nearF = nearF[box]
ia, ib = candidates(Vr, Fr, newF, nearF); hit = tri_pairs_intersect(Vr, Fr, ia, ib); new_hits = sorted(set(zip(np.minimum(ia[hit], ib[hit]).tolist(), np.maximum(ia[hit], ib[hit]).tolist())))
srcbox = np.setdiff1d(nearF, newF); ja, jb = candidates(Vr, Fr, srcbox, srcbox); h2 = tri_pairs_intersect(Vr, Fr, ja, jb)
pre = sorted(set(zip(np.minimum(ja[h2], jb[h2]).tolist(), np.maximum(ja[h2], jb[h2]).tolist())))
out['V3'] = dict(pass_=len(new_hits) == 0, new_face_intersections=len(new_hits), new_pairs=new_hits[:20], faces_tested_box=int(len(nearF)), preexisting_source_pairs_in_box=len(pre), preexisting_examples=pre[:10])
# V4 triangle quality
Tn = Vr[Fr[newF]]; L3 = np.linalg.norm(Tn - np.roll(Tn, 1, 1), axis=2)
def angles(T):
    a_ = np.linalg.norm(T[:, 1] - T[:, 2], axis=1); b_ = np.linalg.norm(T[:, 0] - T[:, 2], axis=1); c_ = np.linalg.norm(T[:, 0] - T[:, 1], axis=1)
    A_ = np.degrees(np.arccos(np.clip((b_**2 + c_**2 - a_**2) / (2 * b_ * c_), -1, 1))); B_ = np.degrees(np.arccos(np.clip((a_**2 + c_**2 - b_**2) / (2 * a_ * c_), -1, 1))); return np.c_[A_, B_, 180 - A_ - B_]
ang = angles(Tn).min(1); srcang = angles(V[F[np.union1d(Z['G'], Z['S'])]]).min(1)
out['V4'] = dict(pass_=bool(ang.min() >= 10 and L3.min() >= 0.25 and L3.max() <= 2.5), min_angle_deg=round(float(ang.min()), 2), p5_min_angle=round(float(np.percentile(ang, 5)), 2), faces_below_10deg=int((ang < 10).sum()),
                 edge_cm=[round(float(L3.min()), 3), round(float(L3.max()), 3)], edges_out_of_range=int(((L3 < 0.25) | (L3 > 2.5)).sum()), removed_source_faces_min_angle_p5=round(float(np.percentile(srcang, 5)), 2))
# V5 seam continuity: dihedral across new-face / P-face edges vs P-P edges near the patch
fn = r0.face_normals; adj = r0.face_adjacency; isnew = np.zeros(len(Fr), bool); isnew[newF] = True
dih = np.degrees(np.arccos(np.clip((fn[adj[:, 0]] * fn[adj[:, 1]]).sum(1), -1, 1)))
stitch = isnew[adj[:, 0]] != isnew[adj[:, 1]]; nearP = np.zeros(len(Fr), bool); nearP[nearF] = True
ref = ~isnew[adj[:, 0]] & ~isnew[adj[:, 1]] & nearP[adj[:, 0]] & nearP[adj[:, 1]]; inner = isnew[adj[:, 0]] & isnew[adj[:, 1]]
frac = float((dih[stitch] <= 35).mean())
out['V5'] = dict(pass_=frac >= 0.95, stitch_edges=int(stitch.sum()), stitch_dihedral_p50_p95_max=np.round(np.percentile(dih[stitch], [50, 95, 100]), 2).tolist(), frac_le_35=round(frac, 4),
                 reference_source_skin_dihedral_p50_p95_max=np.round(np.percentile(dih[ref], [50, 95, 100]), 2).tolist(), fill_internal_dihedral_p50_p95_max=np.round(np.percentile(dih[inner], [50, 95, 100]), 2).tolist())
# V6 ridge removed
ta, tb = J['sector_theta_deg']; ramp_deg = np.degrees(a.ramp / 8.0)
t_, s_, rr_ = tsr(Vr[Fr[newF]].mean(1)); core = (t_ > ta + ramp_deg) & (t_ < tb - ramp_deg)
na = np.abs(fn[newF] @ d); ledge = int((na[core] > 0.55).sum())
def profile(VV, FF, th):                                               # half-plane section through the axis at angle th -> (s, r)
    nrm = -np.sin(np.radians(th)) * e1 + np.cos(np.radians(th)) * e2; dirv = np.cos(np.radians(th)) * e1 + np.sin(np.radians(th)) * e2
    sd = (VV - O) @ nrm; T_ = FF[(np.abs(VV[FF] - O).max((1, 2)) < 25)]; sv = sd[T_]; cr = (sv.min(1) < 0) & (sv.max(1) > 0); pts = []
    for f in T_[cr]:
        for i, j in ((0, 1), (1, 2), (2, 0)):
            if (sd[f[i]] < 0) != (sd[f[j]] < 0):
                t0 = sd[f[i]] / (sd[f[i]] - sd[f[j]]); pts.append(VV[f[i]] + t0 * (VV[f[j]] - VV[f[i]]))
    pts = np.array(pts); c = pts - O; ss = c @ d; rr = c @ dirv; k_ = (rr > 0) & (np.abs(ss) < 9) & (rr < 13); return ss[k_], rr[k_]
fig, axs = plt.subplots(1, 4, figsize=(20, 5)); steps = {}
for k_, th in enumerate((-60, -20, 20, 60)):
    for VV, FF, col, nm in ((V, F, '0.6', 'source'), (Vr, Fr, 'b', 'result')):
        ss, rr = profile(VV, FF, th); o = np.argsort(ss); ss, rr = ss[o], rr[o]
        # outermost surface per 0.25 cm bin -> step = max |dr| between neighbouring bins in the band zone (s -2..9)
        bins = np.arange(-9, 9.01, 0.25); idx = np.digitize(ss, bins); prof = np.array([rr[idx == b].max() if (idx == b).any() else np.nan for b in range(1, len(bins))]); bc = 0.5 * (bins[1:] + bins[:-1])
        zone = (bc > -2) & (bc < 9); dp = np.abs(np.diff(prof)); dz = zone[1:] & zone[:-1] & ~np.isnan(dp)
        steps.setdefault(nm, {})[th] = round(float(np.nanmax(dp[dz])), 3) if dz.any() else None
        axs[k_].plot(rr, ss, '.', ms=2, color=col, label=nm)
    axs[k_].set_title('theta %d: section through the arm axis (r vs s)' % th, fontsize=9); axs[k_].set_aspect('equal'); axs[k_].grid(alpha=.3); axs[k_].legend(fontsize=7); axs[k_].set_xlabel('r cm'); axs[k_].set_ylabel('s cm')
plt.tight_layout(); plt.savefig(a.out + '_V6_sections.png', dpi=80)
out['V6'] = dict(pass_=bool(ledge == 0 and all(v_ is not None and v_ < 0.3 for v_ in steps['result'].values())), core_reconstructed_faces=int(core.sum()), ledge_faces_in_core=ledge,
                 max_radial_step_per_0p25cm_bin=steps, note='step = largest change of the outermost radius between neighbouring 0.25 cm bins for s in (-2, 9); source shows the band edges')
# ---- SUPPLEMENTARY (post hoc, NOT part of the pre-registered verdict): split by zone
ev = r0.face_adjacency_edges; Xe = Vr[ev].mean(1); te, se, _ = tsr(Xe); endz = (te < ta + 3) | (te > tb - 3)
sk = stitch & ~endz; en = stitch & endz
tq, sq, _ = tsr(Vr[Fr[newF]].mean(1)); endf = (tq < ta + 3) | (tq > tb - 3)
Pm = np.zeros(len(F), bool); Pm[P] = True; c_s = V[F].mean(1); ts_, ss_, rs_ = tsr(c_s); hi_ = np.interp(ts_, J['ledge_theta'], J['s_hi'])
above = Pm & (ts_ > ta + ramp_deg) & (ts_ < tb - ramp_deg) & (ss_ > hi_ + 1.8) & (ss_ < hi_ + 4) & (rs_ < 13)
na_src = np.abs(s0.face_normals[above] @ d); tr_, sr_, _ = tsr(Vr[Fr[newF]].mean(1)); hi_r = np.interp(tr_, J['ledge_theta'], J['s_hi'])
topfill = core & (sr_ > hi_r - 1.0)
out['supplementary_posthoc'] = dict(
    note='post-hoc breakdown to locate failures; does not change the pre-registered verdict',
    V5_skin_seams=dict(edges=int(sk.sum()), frac_le_35=round(float((dih[sk] <= 35).mean()), 4), max=round(float(dih[sk].max()), 1)),
    V5_band_end_junctions_within_3deg=dict(edges=int(en.sum()), frac_le_35=round(float((dih[en] <= 35).mean()), 4), max=round(float(dih[en].max()), 1)),
    V4_faces_below_10deg=dict(at_band_ends=int(((ang < 10) & endf).sum()), elsewhere=int(((ang < 10) & ~endf).sum())),
    V6_context=dict(source_skin_above_band_frac_abs_n_d_gt_0p55=round(float((na_src > 0.55).mean()), 3), source_faces=int(above.sum()),
                    fill_top_zone_frac_abs_n_d_gt_0p55=round(float((na[topfill] > 0.55).mean()), 3) if topfill.any() else None,
                    fill_core_below_top_zone_ledge_faces=int(((na > 0.55) & core & ~topfill).sum())))
vals = [out[k]['pass_'] for k in ('V1', 'V2', 'V3', 'V4', 'V5', 'V6')]
out['verdict_automated'] = 'PASS' if all(vals) else ('FAIL' if not (out['V1']['pass_'] and out['V2']['pass_']) or out['V3']['new_face_intersections'] > 0 else 'INCONCLUSIVE')
json.dump(out, open(a.out + '_verify.json', 'w'), indent=1); print(json.dumps(out, indent=1))
