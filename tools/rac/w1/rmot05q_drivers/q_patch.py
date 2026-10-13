# RM-OT-05Q local repair on a DUPLICATE of the F1 working copy (see plan/PLAN.md, committed before this tool existed).
#  1. delete R = G (garment) + S (seam band) faces; drop the orphaned interior vertices; every other vertex / face kept
#     bit-identical (P faces first, original order; kept vertices in original order, new vertices appended);
#  2. hole boundary loop (oriented like the removed faces) -> four chains at the sector corners;
#  3. structured fill grid in the arm-local (theta, s) domain: r by cubic Hermite between the lower / upper skin chains
#     with slopes dr/ds measured on protected skin outside each chain; end chains enter through a localized Coons
#     correction (smoothstep over --ramp cm). No donor, no projection: the fill is INFERRED skin;
#  4. zipper stitch between the grid's outer ring and the hole loop (shorter diagonal first).
# Usage: python3 q_patch.py --mesh F1_working.obj --sel plan/ --out DIR [--h 1.0 --ramp 3.0 --tag A1]
import argparse, json, hashlib, os, numpy as np, trimesh
ap = argparse.ArgumentParser(); ap.add_argument('--mesh'); ap.add_argument('--sel'); ap.add_argument('--out'); ap.add_argument('--tag', default='A1')
ap.add_argument('--h', type=float, default=1.0); ap.add_argument('--ramp', type=float, default=3.0); ap.add_argument('--slope_band', type=float, default=2.5)
ap.add_argument('--hermite', type=int, default=1); ap.add_argument('--smooth', type=float, default=0.0)   # cm: Gaussian smoothing of the guide curves (interior only)
ap.add_argument('--zip', default='loop')   # loop: one global zipper (A1); chain: four corner-matched zippers by arc-length progress
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
m = trimesh.load(a.mesh, process=False); V = np.asarray(m.vertices, float); F = np.asarray(m.faces, np.int64)
J = json.load(open(os.path.join(a.sel, 'patch_selection.json'))); Z = np.load(os.path.join(a.sel, 'patch_face_sets.npz'))
G, S, P = Z['G'], Z['S'], Z['P']; R = np.union1d(G, S)
O = np.array(J['frame']['origin']); d = np.array(J['frame']['axis']); d /= np.linalg.norm(d); e1 = np.cross([0, 1, 0], d); e1 /= np.linalg.norm(e1); e2 = np.cross(d, e1)
def tsr(X):
    c = X - O; s = c @ d; return np.degrees(np.arctan2(c @ e2, c @ e1)), s, np.hypot(c @ e1, c @ e2)
def xyz(t, s, r):
    t = np.radians(t); return O + np.outer(s, d) + np.outer(r * np.cos(t), e1) + np.outer(r * np.sin(t), e2)
lt, slo, shi = np.array(J['ledge_theta']), np.array(J['s_lo']), np.array(J['s_hi']); ta, tb = J['sector_theta_deg']
# ---- 1. hole loop (half-edges of R that are not matched inside R)
he = {}
for f in F[R]:
    for i in range(3): he[(f[i], f[(i + 1) % 3])] = True
bnd = [(x, y) for (x, y) in he if (y, x) not in he]; nxt = dict(bnd); assert len(nxt) == len(bnd), 'non-simple boundary'
loop = [bnd[0][0]]
while True:
    q = nxt[loop[-1]]
    if q == loop[0]: break
    loop.append(q)
assert len(loop) == len(bnd), 'more than one boundary loop'; loop = np.array(loop)
bt, bs, br = tsr(V[loop])
R0 = 8.0; k = np.pi / 180 * R0                                       # theta degrees -> cm on a nominal 8 cm radius
mid = np.interp(bt, lt, 0.5 * (slo + shi))
def corner(t0, low):
    w = (bs < mid) if low else (bs >= mid)
    # extreme vertex: lowest (or highest) s among the vertices within 3 deg of the sector edge
    near = np.where((np.abs(bt - t0) < 3.0) & w)[0]
    return near[np.argmin(bs[near])] if low else near[np.argmax(bs[near])]
cLA, cLB, cUB, cUA = corner(ta, True), corner(tb, True), corner(tb, False), corner(ta, False)
def chain(i0, i1):                                                   # loop indices from i0 to i1 following the loop
    n = len(loop); return [(i0 + j) % n for j in range(((i1 - i0) % n) + 1)]
# decide whether the loop runs LA -> LB along the lower chain (mid-sector vertices low) or LA -> UA first
c1 = chain(cLA, cLB); low_first = np.mean(bs[c1[1:-1]] < mid[c1[1:-1]]) > 0.5 and len(c1) < len(loop) * 0.7
if low_first:
    ch = dict(low=c1, right=chain(cLB, cUB), up=chain(cUB, cUA)[::-1], left=chain(cUA, cLA)[::-1])
else:
    ch = dict(left=chain(cLA, cUA), up=chain(cUA, cUB), right=chain(cUB, cLB)[::-1], low=chain(cLB, cLA)[::-1])
for kk, c_ in ch.items(): assert len(c_) >= 2, kk
def param(cidx):                                                     # chain -> cumulative 3-D arc length (0..1) and (t, s, r)
    X = V[loop[cidx]]; L = np.r_[0, np.cumsum(np.linalg.norm(np.diff(X, axis=0), axis=1))]; return L / L[-1], L[-1], np.c_[bt[cidx], bs[cidx], br[cidx]]
def samp(cidx, u):
    t_, Ltot, Q = param(cidx); return np.stack([np.interp(u, t_, Q[:, j]) for j in range(3)], -1), Ltot
# ---- 2. grid resolution
_, Llow = samp(ch['low'], [0]); _, Lup = samp(ch['up'], [0]); _, Lleft = samp(ch['left'], [0]); _, Lright = samp(ch['right'], [0])
def smooth_len(cidx):
    Q_ = xyz(*samp(cidx, np.linspace(0, 1, 400))[0].T)
    if a.smooth > 0:
        from scipy.ndimage import gaussian_filter1d
        L_ = np.r_[0, np.cumsum(np.linalg.norm(np.diff(Q_, axis=0), axis=1))]; sg = a.smooth / (L_[-1] / 400)
        Q_ = gaussian_filter1d(Q_, sg, axis=0, mode='nearest')
    return np.linalg.norm(np.diff(Q_, axis=0), axis=1).sum()
if a.smooth > 0: Llow, Lup = smooth_len(ch['low']), smooth_len(ch['up'])
Nu = max(4, int(round(0.5 * (Llow + Lup) / a.h))); Nv = max(4, int(round(0.5 * (Lleft + Lright) / a.h)))
u = np.linspace(0, 1, Nu + 1); v = np.linspace(0, 1, Nv + 1)
B, _ = samp(ch['low'], u); T, _ = samp(ch['up'], u); Lc, _ = samp(ch['left'], v); Rc, _ = samp(ch['right'], v)
if a.smooth > 0:                                                     # guide curves only; boundary vertices stay exact
    from scipy.ndimage import gaussian_filter1d
    for C_, Lt in ((B, Llow), (T, Lup)):
        sg = a.smooth / (Lt / Nu); ends = C_[[0, -1]].copy(); C_[:] = gaussian_filter1d(C_, sg, axis=0, mode='nearest'); C_[[0, -1]] = ends
# slopes dr/ds of protected skin just outside the lower / upper chains (per column, from P faces within +-4 deg)
Pc = V[F[P]].mean(1); pt, ps, pr = tsr(Pc); near = (pt > ta - 8) & (pt < tb + 8) & (np.abs(ps) < 14) & (pr < 13)
pt, ps, pr = pt[near], ps[near], pr[near]
def slope(t0, s0, r0, side):
    k_ = (np.abs(pt - t0) < 4) & ((ps < s0) & (ps > s0 - a.slope_band) if side < 0 else (ps > s0) & (ps < s0 + a.slope_band)) & (np.abs(pr - r0) < 2.5)
    if k_.sum() < 3: return np.nan
    A_ = np.c_[ps[k_] - s0, np.ones(k_.sum())]; return np.linalg.lstsq(A_, pr[k_], rcond=None)[0][0]
gB = np.array([slope(*B[j], -1) for j in range(Nu + 1)]); gT = np.array([slope(*T[j], +1) for j in range(Nu + 1)])
for g in (gB, gT):
    ok = ~np.isnan(g); g[:] = np.interp(np.arange(len(g)), np.where(ok)[0], g[ok]); g[:] = np.convolve(np.r_[g[0], g[0], g, g[-1], g[-1]], np.ones(5) / 5, 'valid')
gB = np.clip(gB, -1.5, 1.5); gT = np.clip(gT, -1.5, 1.5)
# ---- 3. field
VV, UU = np.meshgrid(v, u, indexing='ij')                            # [Nv+1, Nu+1]
h00 = 2 * VV**3 - 3 * VV**2 + 1; h01 = -2 * VV**3 + 3 * VV**2; h10 = VV**3 - 2 * VV**2 + VV; h11 = VV**3 - VV**2
th_v = (1 - VV) * B[None, :, 0] + VV * T[None, :, 0]; s_v = (1 - VV) * B[None, :, 1] + VV * T[None, :, 1]
ds = (T[:, 1] - B[:, 1])[None, :]
r_v = h00 * B[None, :, 2] + h01 * T[None, :, 2] + a.hermite * (h10 * ds * gB[None, :] + h11 * ds * gT[None, :])
if not a.hermite: r_v = (1 - VV) * B[None, :, 2] + VV * T[None, :, 2]
def end_w(Ltot):
    x = np.clip(UU * Ltot / a.ramp, 0, 1); return 1 - x * x * (3 - 2 * x)
Lmean = 0.5 * (Llow + Lup); wl = end_w(Lmean); wr = (lambda x: 1 - x * x * (3 - 2 * x))(np.clip((1 - UU) * Lmean / a.ramp, 0, 1))
Q = []
for qv, j in ((th_v, 0), (s_v, 1), (r_v, 2)):
    Q.append(qv + wl * (Lc[:, None, j] - qv[:, :1]) + wr * (Rc[:, None, j] - qv[:, -1:]))
TH, SS, RR = Q
# ---- 4. assemble
keepv = np.unique(F[P]); vmap = -np.ones(len(V), np.int64); vmap[keepv] = np.arange(len(keepv))
Vn = [V[keepv]]; nb = len(keepv)
gid = -np.ones((Nv + 1, Nu + 1), np.int64); ii, jj = np.meshgrid(np.arange(1, Nv), np.arange(1, Nu), indexing='ij')
gid[1:Nv, 1:Nu] = nb + np.arange(ii.size).reshape(ii.shape)
Vn.append(xyz(TH[1:Nv, 1:Nu].ravel(), SS[1:Nv, 1:Nu].ravel(), RR[1:Nv, 1:Nu].ravel())); Vn = np.vstack(Vn)
newF = []
for i in range(1, Nv - 1):
    for j in range(1, Nu - 1):
        q00, q01, q11, q10 = gid[i, j], gid[i, j + 1], gid[i + 1, j + 1], gid[i + 1, j]
        if np.linalg.norm(Vn[q00] - Vn[q11]) < np.linalg.norm(Vn[q01] - Vn[q10]): newF += [[q00, q01, q11], [q00, q11, q10]]
        else: newF += [[q00, q01, q10], [q01, q11, q10]]
gridF = len(newF)
# inner ring (grid outer ring) ordered like the hole loop: low -> right -> up(rev) -> left(rev) when low_first
ring = [gid[1, j] for j in range(1, Nu)] + [gid[i, Nu - 1] for i in range(2, Nv)] + [gid[Nv - 1, j] for j in range(Nu - 2, 0, -1)] + [gid[i, 1] for i in range(Nv - 2, 1, -1)]
if not low_first: ring = [ring[0]] + ring[1:][::-1]
outer = list(vmap[loop[np.r_[cLA:len(loop), 0:cLA]]])
inner = ring
def zip_open(outer, inner, progress):                             # open chains, both from corner to corner
    no, ni = len(outer) - 1, len(inner) - 1; io = jn = 0
    if progress:
        po = np.r_[0, np.cumsum(np.linalg.norm(np.diff(Vn[outer], axis=0), axis=1))]; po /= po[-1]
        pi = np.r_[0, np.cumsum(np.linalg.norm(np.diff(Vn[inner], axis=0), axis=1))]; pi /= pi[-1]
    while io < no or jn < ni:
        o0, n0 = outer[io], inner[jn]
        if jn >= ni: adv_o = True
        elif io >= no: adv_o = False
        elif progress: adv_o = po[io + 1] <= pi[jn + 1]
        else: adv_o = np.linalg.norm(Vn[outer[io + 1]] - Vn[n0]) <= np.linalg.norm(Vn[inner[jn + 1]] - Vn[o0])
        if adv_o: newF.append([o0, outer[io + 1], n0]); io += 1
        else: newF.append([o0, inner[jn + 1], n0]); jn += 1
if a.zip == 'loop':
    zip_open(outer + [outer[0]], inner + [inner[0]], False)
else:
    gl = lambda cidx: list(vmap[loop[cidx]])
    rows = dict(low=[gid[1, j] for j in range(1, Nu)], right=[gid[i, Nu - 1] for i in range(1, Nv)],
                up=[gid[Nv - 1, j] for j in range(1, Nu)], left=[gid[i, 1] for i in range(1, Nv)])
    if low_first:   # loop order: low (LA->LB), right (LB->UB), up reversed (UB->UA), left reversed (UA->LA)
        segs = [(gl(ch['low']), rows['low']), (gl(ch['right']), rows['right']), (gl(ch['up'])[::-1], rows['up'][::-1]), (gl(ch['left'])[::-1], rows['left'][::-1])]
    else:
        segs = [(gl(ch['left']), rows['left']), (gl(ch['up']), rows['up']), (gl(ch['right'])[::-1], rows['right'][::-1]), (gl(ch['low'])[::-1], rows['low'][::-1])]
    for o_, n_ in segs: zip_open(o_, n_, True)
newF = np.array(newF, np.int64)
# grid orientation must agree with the stitch (stitch uses inner half-edge n1 -> n0); flip grid faces if needed
gh = set(map(tuple, np.r_[newF[:gridF, [0, 1]], newF[:gridF, [1, 2]], newF[:gridF, [2, 0]]].tolist()))
st = newF[gridF:]; sh = [(f[1], f[2]) for f in st if f[1] in set(inner) and f[2] in set(inner) and f[1] != f[0]]
agree = np.mean([(y, x) in gh for (x, y) in sh]) if sh else 1.0
if agree < 0.5: newF[:gridF] = newF[:gridF, ::-1]
Fn = np.vstack([vmap[F[P]], newF])
lab = np.zeros(len(Fn), np.int8); cn = Vn[newF].mean(1); t_, s_, r_ = tsr(cn)
inG = (s_ >= np.interp(t_, lt, slo) - J['dg']) & (s_ <= np.interp(t_, lt, shi) + J['dg']); lab[len(P):] = np.where(inG, 2, 3)
out = os.path.join(a.out, 'GO-05Q-%s.obj' % a.tag)
with open(out, 'w') as fh:
    fh.write('# RM-OT-05Q %s: F1 working copy with +X armband exposed arc removed; faces %d.. are INFERRED reconstruction\n' % (a.tag, len(P)))
    np.savetxt(fh, Vn, fmt='v %.17g %.17g %.17g'); np.savetxt(fh, Fn + 1, fmt='f %d %d %d')
np.save(os.path.join(a.out, 'GO-05Q-%s_face_labels.npy' % a.tag), lab); np.save(os.path.join(a.out, 'GO-05Q-%s_vertex_map.npy' % a.tag), keepv)
rec = dict(tag=a.tag, input=a.mesh, input_sha256=hashlib.sha256(open(a.mesh, 'rb').read()).hexdigest(), output=out, output_sha256=hashlib.sha256(open(out, 'rb').read()).hexdigest(),
           params=dict(h=a.h, ramp_cm=a.ramp, slope_band_cm=a.slope_band, hermite=a.hermite, smooth_cm=a.smooth, zip=a.zip), loop_vertices=int(len(loop)), low_first=bool(low_first),
           chains={k_: len(c_) for k_, c_ in ch.items()}, grid=dict(Nu=Nu, Nv=Nv, lengths_cm=dict(low=round(Llow, 2), up=round(Lup, 2), left=round(Lleft, 2), right=round(Lright, 2))),
           slopes_dr_ds=dict(lower=np.round(gB, 3).tolist(), upper=np.round(gT, 3).tolist()), grid_orientation_flipped=bool(agree < 0.5),
           faces=dict(protected=int(len(P)), removed=int(len(R)), new=int(len(newF)), new_grid=int(gridF), new_stitch=int(len(newF) - gridF), reconstructed_label2=int((lab == 2).sum()), seam_label3=int((lab == 3).sum())),
           vertices=dict(kept=int(nb), new=int(len(Vn) - nb), deleted=int(len(np.setdiff1d(np.unique(F[R]), keepv)))),
           output_layout='vertices: kept source vertices in original order (vertex_map.npy gives their F1_working index), then new; faces: P in original order, then new')
json.dump(rec, open(os.path.join(a.out, 'GO-05Q-%s_record.json' % a.tag), 'w'), indent=1)
print(json.dumps({k_: v_ for k_, v_ in rec.items() if k_ != 'slopes_dr_ds'}, indent=1))
