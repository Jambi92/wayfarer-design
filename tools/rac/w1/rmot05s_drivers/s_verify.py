# RM-OT-05S verification (derived from the 05R r_verify.py): V1-V5 + historical V6 unchanged, plus the pre-registered
# anatomy-aware V6c-1..3 and the verdict rules of reviews/rac-rmot05s-evidence/plan/PLAN.md. Can score B2 / R3 too.
# Usage: python3 r_verify.py --src F1_working.obj --q05 <05Q evidence> --plan <05R plan dir> --res RESULT.obj --maps RESULT_maps.npz --labels RESULT_face_labels.npy --nprot N --out PREFIX
import argparse, json, hashlib, os, sys, numpy as np, trimesh
from scipy.spatial import cKDTree
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
ap = argparse.ArgumentParser(); ap.add_argument('--src'); ap.add_argument('--q05'); ap.add_argument('--plan'); ap.add_argument('--res'); ap.add_argument('--maps'); ap.add_argument('--labels')
ap.add_argument('--nprot', type=int, default=139807); ap.add_argument('--prot_sha', default='4468dd862307b8393dfcc8dab58d5cab6033558a87ba523b220e379b7df57c55'); ap.add_argument('--prot_faces', default='P05S')
ap.add_argument('--r05plan', default='reviews/rac-rmot05r-evidence/plan')
ap.add_argument('--out'); a = ap.parse_args()
s0 = trimesh.load(a.src, process=False); V = np.asarray(s0.vertices); F = np.asarray(s0.faces)
r0 = trimesh.load(a.res, process=False); Vr = np.asarray(r0.vertices); Fr = np.asarray(r0.faces)
Q = json.load(open(os.path.join(a.q05, 'plan/patch_selection.json'))); P = (np.load(os.path.join(a.plan, 'interface_sets.npz'))['P05S_src_ordered'] if a.prot_faces == 'P05S' else np.load(os.path.join(a.r05plan, 'junction_sets.npz'))['P05R_src_ordered'] if a.prot_faces == 'P05R' else np.load(os.path.join(a.q05, 'plan/patch_face_sets.npz'))['P'])
nP = a.nprot; assert len(P) == nP
mp = np.load(a.maps); smap = mp['src_vertex'] if 'src_vertex' in mp.files else mp['arr_0']; lab = np.load(a.labels)
O = np.array(Q['frame']['origin']); d = np.array(Q['frame']['axis']); d /= np.linalg.norm(d); e1 = np.cross([0, 1, 0], d); e1 /= np.linalg.norm(e1); e2 = np.cross(d, e1)
lt, slo, shi = np.array(Q['ledge_theta']), np.array(Q['s_lo']), np.array(Q['s_hi']); ta, tb = Q['sector_theta_deg']
def tsr(X):
    c = X - O; return np.degrees(np.arctan2(c @ e2, c @ e1)), c @ d, np.hypot(c @ e1, c @ e2)
out = {}
# V1 outside anatomy
h = hashlib.sha256(np.ascontiguousarray(Vr[Fr[:nP]]).astype(np.float64).tobytes()).hexdigest()
idx_ok = bool((smap[Fr[:nP]] == F[P]).all()); ks = smap >= 0; coord_ok = bool((Vr[ks] == V[smap[ks]]).all())
newF = np.arange(nP, len(Fr)); newsrc = np.unique(Fr[newF]); moved_src = int(((smap[newsrc] >= 0) & ~(np.abs(Vr[newsrc] - V[np.maximum(smap[newsrc], 0)]).max(1) == 0)).sum())
out['V1_outside_anatomy'] = dict(pass_=bool(h == a.prot_sha and idx_ok and coord_ok), protected_coord_sha256=h, plan_sha256=a.prot_sha, protected_faces=nP, index_correspondence=idx_ok,
                                 kept_source_vertices_bit_identical=coord_ok, source_vertices_on_patch_boundary_moved=moved_src)
# V2 boundary / manifold / orientation
def einfo(FF):
    he = np.r_[FF[:, [0, 1]], FF[:, [1, 2]], FF[:, [2, 0]]]; u, inv, cnt = np.unique(np.sort(he, 1), axis=0, return_inverse=True, return_counts=True); return he, u, inv.ravel(), cnt
he, u, inv, cnt = einfo(Fr); bnd = u[cnt == 1]; _, u0, _, c0 = einfo(F); bs = {tuple(x) for x in np.sort(u0[c0 == 1], 1).tolist()}
bm = smap[bnd]; mapped_ok = bool((bm >= 0).all()); br = {tuple(x) for x in np.sort(bm, 1).tolist()} if mapped_ok else set()
same = bool(mapped_ok and br == bs and len(bnd) == len(bs))
dirs = {}
for k_, (x, y) in enumerate(he): dirs.setdefault(inv[k_], []).append((x, y))
touch = set(inv[np.r_[newF, newF + len(Fr), newF + 2 * len(Fr)]].tolist()); bad_or = sum(1 for e in touch if len(dirs[e]) == 2 and dirs[e][0] == dirs[e][1])
area = trimesh.triangles.area(Vr[Fr[newF]]); degen = int((area < 1e-6).sum())
out['V2_boundary_manifold'] = dict(pass_=bool(same and (cnt > 2).sum() == 0 and bad_or == 0 and degen == 0), boundary_edges=int(len(bnd)), source_boundary_edges=len(bs),
                                   boundary_identical_to_source_by_correspondence=same, nonmanifold_edges=int((cnt > 2).sum()), inconsistent_orientation_at_patch=int(bad_or), degenerate_new_faces=degen)
# V3 intersections
def seg_tri(p0, p1, A, B, C):
    e1_, e2_ = B - A, C - A; dd = p1 - p0; hh = np.cross(dd, e2_); det = (e1_ * hh).sum(-1); ok = np.abs(det) > 1e-12
    iv = np.where(ok, 1 / np.where(ok, det, 1), 0); s_ = p0 - A; uu = (s_ * hh).sum(-1) * iv; q = np.cross(s_, e1_); vv = (dd * q).sum(-1) * iv; t = (e2_ * q).sum(-1) * iv
    eps = 1e-9; return ok & (uu > eps) & (vv > eps) & (uu + vv < 1 - eps) & (t > eps) & (t < 1 - eps)
def pairs_hit(ia, ib):
    T1, T2 = Vr[Fr[ia]], Vr[Fr[ib]]; hit = np.zeros(len(ia), bool)
    for (i, j) in ((0, 1), (1, 2), (2, 0)):
        hit |= seg_tri(T1[:, i], T1[:, j], T2[:, 0], T2[:, 1], T2[:, 2]); hit |= seg_tri(T2[:, i], T2[:, j], T1[:, 0], T1[:, 1], T1[:, 2])
    return hit
def cand(sa, sb, rad=3.0):
    ca = Vr[Fr[sa]].mean(1); cb = Vr[Fr[sb]].mean(1); L = cKDTree(cb).query_ball_point(ca, rad)
    ia = np.repeat(sa, [len(l) for l in L]); ib = sb[np.concatenate([np.array(l, int) for l in L])] if len(ia) else np.array([], int)
    k = ia != ib; ia, ib = ia[k], ib[k]; shr = (Fr[ia][:, :, None] == Fr[ib][:, None, :]).any((1, 2)); return ia[~shr], ib[~shr]
allc = Vr[Fr].mean(1); nc = Vr[Fr[newF]].mean(1); tr_ = cKDTree(nc); dmin, _ = tr_.query(allc); near = np.where(dmin < 6)[0]
ia, ib = cand(newF, near); hit = pairs_hit(ia, ib); newhits = sorted(set(zip(np.minimum(ia[hit], ib[hit]).tolist(), np.maximum(ia[hit], ib[hit]).tolist())))
srcbox = np.setdiff1d(near, newF); ja, jb = cand(srcbox, srcbox); h2 = pairs_hit(ja, jb); pre = sorted(set(zip(np.minimum(ja[h2], jb[h2]).tolist(), np.maximum(ja[h2], jb[h2]).tolist())))
out['V3_intersections'] = dict(pass_=len(newhits) == 0, new_face_intersections=len(newhits), pairs=newhits[:20], faces_tested=int(len(near)), preexisting_source_pairs_in_box=len(pre))
# V4 triangle quality (all new faces)
T = Vr[Fr[newF]]; Ls = np.linalg.norm(T[:, [1, 2, 0]] - T[:, [2, 0, 1]], axis=2)
cs = np.stack([(Ls[:, (i + 1) % 3]**2 + Ls[:, (i + 2) % 3]**2 - Ls[:, i]**2) / (2 * Ls[:, (i + 1) % 3] * Ls[:, (i + 2) % 3]) for i in range(3)], 1)
ang = np.degrees(np.arccos(np.clip(cs.max(1), -1, 1))); badE = (Ls < 0.25) | (Ls > 2.5)
ft, fs, fr = tsr(nc)
outl = [dict(face=int(newF[i]), label=int(lab[newF[i]]), theta=round(float(ft[i]), 1), s=round(float(fs[i]), 2), min_angle=round(float(ang[i]), 2), edges=np.round(Ls[i], 3).tolist())
        for i in np.where((ang < 10) | badE.any(1))[0]]
out['V4_triangle_quality'] = dict(pass_=bool(ang.min() >= 10 and not badE.any()), new_faces=int(len(newF)), min_angle=round(float(ang.min()), 2), angle_percentiles_p1_p5_p50=np.round(np.percentile(ang, [1, 5, 50]), 2).tolist(),
                                  faces_below_10deg=int((ang < 10).sum()), faces_below_5deg=int((ang < 5).sum()), edge_cm_min_max=[round(float(Ls.min()), 3), round(float(Ls.max()), 3)], edges_out_of_range=int(badE.sum()), outliers=outl)
# V5 seam continuity
fn = r0.face_normals; adj = r0.face_adjacency; ev = r0.face_adjacency_edges; isn = np.zeros(len(Fr), bool); isn[newF] = True
dih = np.degrees(np.arccos(np.clip((fn[adj[:, 0]] * fn[adj[:, 1]]).sum(1), -1, 1))); st = isn[adj[:, 0]] != isn[adj[:, 1]]; nn = isn[adj[:, 0]] & isn[adj[:, 1]]
et, es, _ = tsr(Vr[ev].mean(1)); frac = float((dih[st] <= 35).mean())
nearP = np.zeros(len(Fr), bool); nearP[near] = True; ref = ~isn[adj[:, 0]] & ~isn[adj[:, 1]] & nearP[adj[:, 0]] & nearP[adj[:, 1]]
v5out = [dict(theta=round(float(et[k]), 1), s=round(float(es[k]), 2), dihedral=round(float(dih[k]), 1)) for k in np.where(st & (dih > 35))[0]]
out['V5_seam_continuity'] = dict(pass_=frac >= 0.95, stitch_edges=int(st.sum()), frac_le_35=round(frac, 4), dihedral_percentiles_p50_p90_p95_p99_max=np.round(np.percentile(dih[st], [50, 90, 95, 99, 100]), 2).tolist(),
                                 histogram_deg=dict(edges=[0, 10, 20, 35, 45, 60, 90, 180], counts=np.histogram(dih[st], [0, 10, 20, 35, 45, 60, 90, 180])[0].tolist()),
                                 reference_source_skin_p50_p95_max=np.round(np.percentile(dih[ref], [50, 95, 100]), 2).tolist(), outliers=v5out)
# V6 historical (05Q definition) + V6b supplemental
ramp_deg = np.degrees(3.0 / 8.0); core = (ft > ta + ramp_deg) & (ft < tb - ramp_deg); na = np.abs(fn[newF] @ d)
def profile(VV, FF, th):
    nrm = -np.sin(np.radians(th)) * e1 + np.cos(np.radians(th)) * e2; dv = np.cos(np.radians(th)) * e1 + np.sin(np.radians(th)) * e2
    sd = (VV - O) @ nrm; T_ = FF[(np.abs(VV[FF] - O).max((1, 2)) < 25)]; sv = sd[T_]; cr = (sv.min(1) < 0) & (sv.max(1) > 0); pts = []
    for f in T_[cr]:
        for i, j in ((0, 1), (1, 2), (2, 0)):
            if (sd[f[i]] < 0) != (sd[f[j]] < 0): t0 = sd[f[i]] / (sd[f[i]] - sd[f[j]]); pts.append(VV[f[i]] + t0 * (VV[f[j]] - VV[f[i]]))
    pts = np.array(pts); c = pts - O; ss = c @ d; rr = c @ dv; k = (rr > 0) & (np.abs(ss) < 10) & (rr < 13); return ss[k], rr[k]
def step(VV, FF, th):
    ss, rr = profile(VV, FF, th); lo_ = np.interp(th, lt, slo) - 2; hi_ = np.interp(th, lt, shi) + 2
    bins = np.arange(-10, 10.01, 0.25); ix = np.digitize(ss, bins); pr = np.array([rr[ix == b].max() if (ix == b).any() else np.nan for b in range(1, len(bins))]); bc = 0.5 * (bins[1:] + bins[:-1])
    z = (bc > lo_) & (bc < hi_); dp = np.abs(np.diff(pr)); dz = z[1:] & z[:-1] & ~np.isnan(dp); return round(float(np.nanmax(dp[dz])), 3) if dz.any() else None
ths = (-120, -104, -90, -80, -60, -40, -20, 0, 20, 40, 60, 74, 90, 104, 118); stp = {th: step(Vr, Fr, th) for th in ths}; stp_src = {th: step(V, F, th) for th in ths}
hi_r = np.interp(ft, lt, shi); top = core & (fs > hi_r - 1.0)
Pm = np.zeros(len(F), bool); Pm[P] = True; c_s = V[F].mean(1); ts_, ss_, rs_ = tsr(c_s); hs_ = np.interp(ts_, lt, shi)
above = Pm & (ts_ > ta + ramp_deg) & (ts_ < tb - ramp_deg) & (ss_ > hs_ + 1.8) & (ss_ < hs_ + 4) & (rs_ < 13); src_frac = float((np.abs(s0.face_normals[above] @ d) > 0.55).mean())
out['V6_historical_05Q'] = dict(pass_=bool((na[core] > 0.55).sum() == 0 and all(v is not None and v < 0.3 for v in [stp[-60], stp[-20], stp[20], stp[60]])), ledge_faces_in_core=int((na[core] > 0.55).sum()),
                                steps_at_05Q_angles={k: stp[k] for k in (-60, -20, 20, 60)}, note='retained as a historical diagnostic (author ruling); can flag legitimate deltoid slope')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'rmot05s_drivers')); import s_lib, s_design
frS = s_lib.Frame(os.path.join(a.q05, 'plan/patch_selection.json'))
def section(VV, FF, th):
    P_, _ = s_lib.profile(frS, VV, FF, th, (8.0, -4.0)); return P_
DZ = {nm: dict(np.load(os.path.join(a.plan, 'design_%s.npz' % nm))) for nm in ('posterior', 'anterior')}
def AB(th):
    nm = 'posterior' if th < 0 else 'anterior'; Dd = DZ[nm]; k = int(np.argmin(np.abs(Dd['theta'] - th))); return Dd['S'][k][0], Dd['S'][k][-1], Dd['s_led'][k]
def seg_between(P_, pa, pb):
    L = s_lib.arclen(P_); la, _ = s_lib.project(P_, L, pa); lb, _ = s_lib.project(P_, L, pb); ll = np.arange(min(la, lb), max(la, lb), 0.05); return s_lib.at_len(P_, L, ll)
def max_turn(Q, win=0.5):
    if len(Q) < 3: return None
    d_ = np.diff(Q, axis=0); ang = np.degrees(np.unwrap(np.arctan2(d_[:, 1], d_[:, 0]))); n = max(1, int(round(win / 0.05)))
    return float(np.max(np.abs(ang[n:] - ang[:-n]))) if len(ang) > n else 0.0
c1 = {}
for th in (-112, -104, -96, -90, 84, 90, 96, 102):
    pa, pb, _ = AB(th); Pr = section(Vr, Fr, th); Ps = section(V, F, th)
    c1[th] = dict(result=round(max_turn(seg_between(Pr, pa, pb)), 1), source=round(max_turn(seg_between(Ps, pa, pb)), 1))
out['V6c_1_garment_ledge_removed'] = dict(pass_=all(v['result'] <= 35 for v in c1.values()), max_direction_change_deg_per_0p5cm=c1)
c2 = {}
for nm, rng in (('posterior', np.arange(-136, -115.9, 2.0)), ('anterior', np.arange(122, 103.9, -2.0))):
    steps = []; under = []
    for th in rng:
        pa, pb, sl = AB(th); Q = seg_between(section(Vr, Fr, th), pa, pb); k = (Q[:, 1] > sl - 1.5) & (Q[:, 1] < sl + 1.5)
        steps.append(round(float(np.ptp(Q[k, 0])) if k.sum() > 1 else 0.0, 3))
        i_top = int(np.argmax(Q[:, 0] * k)) if k.any() else 0; under.append(bool(np.any(np.diff(Q[:i_top + 1, 1]) < -0.05)))
    mono = all(steps[i + 1] <= steps[i] + 0.1 for i in range(len(steps) - 1)); c2[nm] = dict(theta_from_untouched_end=rng.tolist(), ledge_step_cm=steps, undercut=under, monotone=mono)
out['V6c_2_taper_termination'] = dict(pass_=all(v['monotone'] and not any(v['undercut']) for v in c2.values()), zones=c2)
f120 = int(((dih > 120) & (st | nn)).sum()); f90 = int(((dih > 90) & (st | nn)).sum())
out['V6c_3_no_folds'] = dict(pass_=f120 == 0, dihedral_gt_120=f120, dihedral_gt_90=f90, locations_gt_90=[dict(theta=round(float(et[k]), 1), s=round(float(es[k]), 2), dihedral=round(float(dih[k]), 1)) for k in np.where((dih > 90) & (st | nn))[0]])
core_ok = [out[k]['pass_'] for k in ('V1_outside_anatomy', 'V2_boundary_manifold', 'V3_intersections', 'V4_triangle_quality', 'V5_seam_continuity', 'V6c_1_garment_ledge_removed', 'V6c_2_taper_termination', 'V6c_3_no_folds')]
fail = not (out['V1_outside_anatomy']['pass_'] and out['V2_boundary_manifold']['pass_'] and out['V3_intersections']['pass_']) or out['V4_triangle_quality']['faces_below_5deg'] > 0 or f120 > 0
out['verdict_automated'] = 'PASS' if all(core_ok) else ('FAIL' if fail else 'UNRESOLVED')
fig, axs = plt.subplots(1, len(ths), figsize=(3.0 * len(ths), 5))
for k, th in enumerate(ths):
    for VV, FF, col, nm in ((V, F, '0.6', 'source'), (Vr, Fr, 'b', 'result')):
        ss, rr = profile(VV, FF, th); axs[k].plot(rr, ss, '.', ms=2, color=col, label=nm)
    axs[k].set_title('theta %d' % th, fontsize=9); axs[k].set_aspect('equal'); axs[k].grid(alpha=.3); axs[k].set_xlabel('r cm'); axs[k].legend(fontsize=6)
axs[0].set_ylabel('s cm'); plt.tight_layout(); plt.savefig(a.out + '_profiles.png', dpi=75)
json.dump(out, open(a.out + '_verify.json', 'w'), indent=1)
print(json.dumps({k: ({kk: vv for kk, vv in v.items() if kk not in ('outliers', 'pairs', 'fold_locations', 'locations_gt_90')} if isinstance(v, dict) else v) for k, v in out.items()}, indent=1))
