# RM-OT-05Q local repair, method B (after attempts A1/A2 with q_patch.py were rejected by V3-V6: the structured grid +
# zipper folded where the jagged hole boundary wanders more than one grid row). Same plan inputs, same inferred field:
#  1. delete R = G + S; keep every other vertex / face bit-identical (P faces first; kept vertices first, new appended);
#  2. the hole loop is laid out in the arm-local domain (x = theta * 8 cm, y = s). Where the loop crosses the band's
#     overhanging lip at the sector ends the layout folds; there the end-chain layout is made monotone (layout only:
#     3-D boundary positions are never changed);
#  3. constrained quality Delaunay triangulation of that polygon (Shewchuk Triangle: q30, area <= h^2*sqrt3/4, no Steiner
#     points on the boundary -> the 109 source boundary vertices are the only boundary vertices);
#  4. radius field r(theta, s): cubic Hermite between the smoothed lower / upper skin chains with slopes dr/ds of protected
#     skin outside each chain, plus the localized Coons end correction (smoothstep over --ramp cm) toward the remaining
#     band ends, plus a harmonic residual so the field meets every exact boundary vertex. No donor, no projection:
#     INFERRED skin.
# Usage: python3 q_patch_b.py --mesh F1_working.obj --sel plan/ --out DIR --tag B1 [--h 1.0 --ramp 3.0 --smooth 2.0]
import argparse, json, hashlib, os, numpy as np, trimesh, triangle, igl
from scipy.ndimage import gaussian_filter1d
ap = argparse.ArgumentParser(); ap.add_argument('--mesh'); ap.add_argument('--sel'); ap.add_argument('--out'); ap.add_argument('--tag', default='B1')
ap.add_argument('--h', type=float, default=1.0); ap.add_argument('--ramp', type=float, default=3.0); ap.add_argument('--slope_band', type=float, default=2.5)
ap.add_argument('--smooth', type=float, default=2.0); ap.add_argument('--q', type=float, default=30.0); ap.add_argument('--relax', type=int, default=0); ap.add_argument('--relax_zone', type=float, default=3.0); a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
m = trimesh.load(a.mesh, process=False); V = np.asarray(m.vertices, float); F = np.asarray(m.faces, np.int64)
J = json.load(open(os.path.join(a.sel, 'patch_selection.json'))); Z = np.load(os.path.join(a.sel, 'patch_face_sets.npz'))
G, S, P = Z['G'], Z['S'], Z['P']; R = np.union1d(G, S)
O = np.array(J['frame']['origin']); d = np.array(J['frame']['axis']); d /= np.linalg.norm(d); e1 = np.cross([0, 1, 0], d); e1 /= np.linalg.norm(e1); e2 = np.cross(d, e1)
K = np.pi / 180 * 8.0
def tsr(X):
    c = X - O; s = c @ d; return np.degrees(np.arctan2(c @ e2, c @ e1)), s, np.hypot(c @ e1, c @ e2)
def xyz(t, s, r):
    t = np.radians(t); return O + np.outer(s, d) + np.outer(r * np.cos(t), e1) + np.outer(r * np.sin(t), e2)
lt, slo, shi = np.array(J['ledge_theta']), np.array(J['s_lo']), np.array(J['s_hi']); ta, tb = J['sector_theta_deg']
# ---- hole loop, oriented like the removed faces
he = {}
for f in F[R]:
    for i in range(3): he[(f[i], f[(i + 1) % 3])] = True
bnd = [(x, y) for (x, y) in he if (y, x) not in he]; nxt = dict(bnd); assert len(nxt) == len(bnd)
loop = [bnd[0][0]]
while nxt[loop[-1]] != loop[0]: loop.append(nxt[loop[-1]])
assert len(loop) == len(bnd); loop = np.array(loop); n = len(loop)
bt, bs, br = tsr(V[loop]); mid = np.interp(bt, lt, 0.5 * (slo + shi)); low = bs < mid
def corner(t0, lo_):
    near = np.where((np.abs(bt - t0) < 3.0) & (low if lo_ else ~low))[0]; return near[np.argmin(bs[near])] if lo_ else near[np.argmax(bs[near])]
cLA, cLB, cUB, cUA = corner(ta, True), corner(tb, True), corner(tb, False), corner(ta, False)
chain = lambda i0, i1: [(i0 + j) % n for j in range(((i1 - i0) % n) + 1)]
c1 = chain(cLA, cLB); low_first = np.mean(low[c1[1:-1]]) > 0.5 and len(c1) < 0.7 * n
if low_first: ch = dict(low=c1, right=chain(cLB, cUB), up=chain(cUB, cUA)[::-1], left=chain(cUA, cLA)[::-1])
else: ch = dict(left=chain(cLA, cUA), up=chain(cUA, cUB), right=chain(cUB, cLB)[::-1], low=chain(cLB, cLA)[::-1])
# ---- 2-D layout (x, y) = (theta*K, s); untangle the end chains (monotone s from low corner to up corner, theta clamped)
X2 = np.c_[bt * K, bs].copy(); fixed = []
for side, tlim, sg_ in (('left', ta, 1), ('right', tb, -1)):
    run = list(chain(cUA, cLA) if low_first else chain(cLA, cUA)) if side == 'left' else list(chain(cLB, cUB) if low_first else chain(cUB, cLB))   # loop order
    # extend the end chain along the loop while the neighbours lie at or beyond the sector edge (+0.5 deg)
    while sg_ * (bt[(run[0] - 1) % n] - tlim) < 0.5 and len(run) < n // 3: run.insert(0, (run[0] - 1) % n)
    while sg_ * (bt[(run[-1] + 1) % n] - tlim) < 0.5 and len(run) < n // 3: run.append((run[-1] + 1) % n)
    ys = bs[run].copy(); dec = ys[0] > ys[-1]
    ys = (np.minimum.accumulate(ys) - np.arange(len(run)) * 1e-3) if dec else (np.maximum.accumulate(ys) + np.arange(len(run)) * 1e-3)
    X2[run, 0] = tlim * K; X2[run, 1] = ys; fixed += [int(i) for i in run]
def simple(P_):
    m_ = len(P_); bad = []
    for i in range(m_):
        for j in range(i + 2, m_):
            if i == 0 and j == m_ - 1: continue
            p1, p2, p3, p4 = P_[i], P_[(i + 1) % m_], P_[j], P_[(j + 1) % m_]
            d1 = np.cross(p2 - p1, p3 - p1); d2 = np.cross(p2 - p1, p4 - p1); d3 = np.cross(p4 - p3, p1 - p3); d4 = np.cross(p4 - p3, p2 - p3)
            if d1 * d2 < 0 and d3 * d4 < 0: bad.append((i, j))
    return bad
bad = simple(X2)
assert not bad, 'layout still folds at %s' % bad
sgn = 0.5 * np.sum(X2[:, 0] * np.roll(X2[:, 1], -1) - np.roll(X2[:, 0], -1) * X2[:, 1])
# ---- constrained quality triangulation
seg = np.c_[np.arange(n), (np.arange(n) + 1) % n]
Tr = triangle.triangulate(dict(vertices=X2, segments=seg), 'pq%gYa%g' % (a.q, a.h * a.h * np.sqrt(3) / 4))
P2 = Tr['vertices']; T2 = Tr['triangles']; assert (np.abs(P2[:n] - X2) < 1e-9).all(), 'boundary vertices moved'
if sgn < 0: T2 = T2[:, ::-1]                                          # keep the removed faces' orientation
nin = len(P2) - n; th_i = P2[n:, 0] / K; s_i = P2[n:, 1]
# ---- field
def guide(cidx):
    Q = np.c_[bt[cidx], bs[cidx], br[cidx]]; Q = Q[np.argsort(Q[:, 0])]
    tg = np.linspace(ta - 3, tb + 3, 400); G_ = np.stack([np.interp(tg, Q[:, 0], Q[:, j]) for j in (1, 2)], -1)
    sg = a.smooth / ((tg[1] - tg[0]) * K); return tg, gaussian_filter1d(G_, sg, axis=0, mode='nearest')
tg, Bg = guide(ch['low']); _, Tg = guide(ch['up'])
Pc = V[F[P]].mean(1); pt, ps, pr = tsr(Pc); nr_ = (pt > ta - 8) & (pt < tb + 8) & (np.abs(ps) < 14) & (pr < 13); pt, ps, pr = pt[nr_], ps[nr_], pr[nr_]
def slope(t0, s0, r0, side):
    k_ = (np.abs(pt - t0) < 4) & (((ps < s0) & (ps > s0 - a.slope_band)) if side < 0 else ((ps > s0) & (ps < s0 + a.slope_band))) & (np.abs(pr - r0) < 2.5)
    if k_.sum() < 3: return np.nan
    return np.linalg.lstsq(np.c_[ps[k_] - s0, np.ones(k_.sum())], pr[k_], rcond=None)[0][0]
def fill(g):
    ok = ~np.isnan(g); g = np.interp(np.arange(len(g)), np.where(ok)[0], g[ok]); return np.clip(gaussian_filter1d(g, 8, mode='nearest'), -1.5, 1.5)
gB = fill(np.array([slope(tg[i], *Bg[i], -1) for i in range(len(tg))])); gT = fill(np.array([slope(tg[i], *Tg[i], +1) for i in range(len(tg))]))
def field_v(th, s):
    sB = np.interp(th, tg, Bg[:, 0]); rB = np.interp(th, tg, Bg[:, 1]); sT = np.interp(th, tg, Tg[:, 0]); rT = np.interp(th, tg, Tg[:, 1])
    gb = np.interp(th, tg, gB); gt = np.interp(th, tg, gT); ds = sT - sB; v = np.clip((s - sB) / ds, 0, 1)
    return (2 * v**3 - 3 * v**2 + 1) * rB + (-2 * v**3 + 3 * v**2) * rT + (v**3 - 2 * v**2 + v) * ds * gb + (v**3 - v**2) * ds * gt
def end_curve(cidx):
    Q = np.c_[bs[cidx], br[cidx], bt[cidx]]; Q = Q[np.argsort(Q[:, 0])]; return Q
EL, ER = end_curve(ch['left']), end_curve(ch['right'])
def field(th, s):
    r = field_v(th, s)
    for E_, sgn_ in ((EL, 1), (ER, -1)):
        te = np.interp(s, E_[:, 0], E_[:, 2]); re = np.interp(s, E_[:, 0], E_[:, 1])
        x = np.clip(sgn_ * (th - te) * K / a.ramp, 0, 1); w = 1 - x * x * (3 - 2 * x)
        r = r + w * (re - field_v(te, s))
    return r
r0_i = field(th_i, s_i); delta_b = br - field(bt, bs)
# harmonic residual (Dirichlet on the exact boundary radii), solved on the 2-D layout
V2 = np.c_[P2, np.zeros(len(P2))]; bidx = np.arange(n)
dl = igl.harmonic(V2, T2.astype(np.int64), bidx.astype(np.int64), delta_b[:, None].astype(float), 1)[:, 0]
r_i = r0_i + dl[n:]
# ---- assemble
keepv = np.unique(F[P]); vmap = -np.ones(len(V), np.int64); vmap[keepv] = np.arange(len(keepv)); nb = len(keepv)
Vn = np.vstack([V[keepv], xyz(th_i, s_i, r_i)])
idmap = np.r_[vmap[loop], nb + np.arange(nin)]; assert (idmap[:n] >= 0).all()
newF = idmap[T2]
relaxed = 0
if a.relax > 0:   # local umbrella relaxation of NEW vertices near the two band ends only (boundary fixed); untangles the end corners
    xe = np.minimum(np.abs(P2[:, 0] - ta * K), np.abs(P2[:, 0] - tb * K)); w = np.clip(1 - xe / a.relax_zone, 0, 1); w[:n] = 0
    nbr = [[] for _ in range(len(P2))]
    for t3 in T2:
        for i in range(3): nbr[t3[i]] += [t3[(i + 1) % 3], t3[(i + 2) % 3]]
    nbr = [np.unique(x) for x in nbr]; X3 = np.vstack([V[loop], Vn[nb:]])
    for _ in range(a.relax):
        avg = np.array([X3[nb_].mean(0) for nb_ in nbr]); X3 = X3 + 0.5 * w[:, None] * (avg - X3)
    Vn[nb:] = X3[n:]; relaxed = int((w > 0).sum())
Fn = np.vstack([vmap[F[P]], newF])
lab = np.zeros(len(Fn), np.int8); t_, s_, _ = tsr(Vn[newF].mean(1))
inG = (s_ >= np.interp(t_, lt, slo) - J['dg']) & (s_ <= np.interp(t_, lt, shi) + J['dg']); lab[len(P):] = np.where(inG, 2, 3)
out = os.path.join(a.out, 'GO-05Q-%s.obj' % a.tag)
with open(out, 'w') as fh:
    fh.write('# RM-OT-05Q %s: F1 working copy with +X armband exposed arc removed; faces %d.. are INFERRED reconstruction\n' % (a.tag, len(P)))
    np.savetxt(fh, Vn, fmt='v %.17g %.17g %.17g'); np.savetxt(fh, Fn + 1, fmt='f %d %d %d')
np.save(os.path.join(a.out, 'GO-05Q-%s_face_labels.npy' % a.tag), lab); np.save(os.path.join(a.out, 'GO-05Q-%s_vertex_map.npy' % a.tag), keepv)
rec = dict(tag=a.tag, method='B: constrained Delaunay in the (theta,s) layout + Hermite/Coons inferred field + harmonic residual', input=a.mesh,
           input_sha256=hashlib.sha256(open(a.mesh, 'rb').read()).hexdigest(), output=out, output_sha256=hashlib.sha256(open(out, 'rb').read()).hexdigest(),
           params=dict(h=a.h, ramp_cm=a.ramp, slope_band_cm=a.slope_band, smooth_cm=a.smooth, triangle_min_angle=a.q, relax_iters=a.relax, relax_zone_cm=a.relax_zone), relaxed_vertices=relaxed, loop_vertices=int(n), low_first=bool(low_first),
           chains={k_: len(c_) for k_, c_ in ch.items()}, layout_end_runs_straightened=fixed,
           harmonic_residual_cm=dict(boundary_abs_max=round(float(np.abs(delta_b).max()), 3), boundary_abs_mean=round(float(np.abs(delta_b).mean()), 3), interior_abs_max=round(float(np.abs(dl[n:]).max()), 3)),
           slopes_dr_ds=dict(lower=[round(float(np.percentile(gB, q)), 3) for q in (5, 50, 95)], upper=[round(float(np.percentile(gT, q)), 3) for q in (5, 50, 95)]),
           faces=dict(protected=int(len(P)), removed=int(len(R)), new=int(len(newF)), reconstructed_label2=int((lab == 2).sum()), seam_label3=int((lab == 3).sum())),
           vertices=dict(kept=int(nb), new=int(nin), deleted=int(len(np.setdiff1d(np.unique(F[R]), keepv)))),
           output_layout='vertices: kept source vertices in original order (vertex_map.npy -> F1_working index), then new; faces: P in original order, then new')
json.dump(rec, open(os.path.join(a.out, 'GO-05Q-%s_record.json' % a.tag), 'w'), indent=1)
print(json.dumps({k_: v_ for k_, v_ in rec.items() if k_ not in ('slopes_dr_ds',)}, indent=1))
