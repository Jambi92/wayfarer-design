# sa_tail_module.py SRC_DIR LM_DIR OUT_DIR : RP5 Saurin AUTHORED tail + tail-root topology module (order 53976fb §9 E / F) -- the pilot's deliberately
# constructed, auditable quad module for the primary identity zone (not a remesher output).
# Construction (all on the canonical SA-M188 base surface; every vertex is a barycentric point of a base triangle, so the same module realizes on SA-F188
# exactly through the shared base face list):
#   1. caudal region S = the tip's connected component of the base surface more than 2 cm caudal of the anatomical tail-root plane (sa_landmarks: through the midsagittal dorsal lumbar
#      concavity and the ventral perineal junction); its single boundary is the root loop (the 2 cm band in front of it joins the trunk-pelvis topology).
#   2. tail coordinate: surface geodesic distance from the root loop (Dijkstra on S), normalized at the tip. Root rings are parallel offsets of the
#      root loop (uniform spacing, wrapping the posterior pelvis -- no 'tail stuck on a sacrum'); along the free tail the fronts become axis-normal.
#   3. ring levels: marched along the geodesic coordinate in steps of the ring's own edge length
#      (perimeter / N) -> near-square quads; N = 128 at the root, halved by authored all-quad 2:1 rows when the coarser edge stays <= 0.95 cm
#      (poles on the transition rows only); the last 8-ring reduces to 4 and closes with one quad (tail-tip exemption, no fan pole).
#   4. ring sampling: N equal arc-length points per loop, orientation-consistent; the first ring phase-locked to the dorsal midline (max u), every
#      later ring to the projection of the previous ring's vertex 0 (no twist). (resample_sweep is kept as a tested alternative; not used.)
# Output: module quads + tip fan, base-triangle barycentric placement (tri id, b1, b2), ring table (phi, perimeter, spacing, N), root-ring count.
import sys, os, json, numpy as np, igl, scipy.sparse as sp
from scipy.sparse.linalg import spsolve
SRC, LMD, OUT = sys.argv[1:4]; os.makedirs(OUT, exist_ok=True)
b = np.load(SRC + '/saurin_w2_final_base.npz'); V = b['v'].astype(float); F = b['f'].astype(np.int64)
LM = json.load(open(LMD + '/SA-M188_landmarks.json'))['landmarks']; g = lambda k: np.array(LM[k]['p_cm'])
Dp, Vp, tip = g('tail_root_dorsal'), g('tail_root_ventral'), g('tail_tip')
t_ = Dp - Vp; t_ /= np.linalg.norm(t_); nrm = np.cross([1.0, 0, 0], t_)
if nrm[1] > 0: nrm = -nrm
sd = (V - 0.5 * (Dp + Vp)) @ nrm; inS = sd > 2.0                 # module starts 2 cm caudal of the anatomical root plane: there the caudal surface is ONE closed loop around the tail base (u 89-123, 37 cm wide)
keep = np.all(inS[F], 1); Fs = F[keep]; sub = np.unique(Fs); mp = -np.ones(len(V), int); mp[sub] = np.arange(len(sub)); Fs = mp[Fs]; Vs = V[sub]
bl = igl.boundary_loop(Fs); bl = np.asarray(bl)
# keep the connected component containing the tip
import scipy.sparse.csgraph as cg
nV = len(Vs); A = sp.coo_matrix((np.ones(3 * len(Fs)), (Fs.ravel(), np.roll(Fs, 1, 1).ravel())), shape=(nV, nV)); nc, lab = cg.connected_components(A, directed=False)
ti = int(np.argmin(np.linalg.norm(Vs - tip, axis=1))); comp = lab == lab[ti]
Fs = Fs[comp[Fs[:, 0]]]; sub2 = np.unique(Fs); m2 = -np.ones(nV, int); m2[sub2] = np.arange(len(sub2)); Fs = m2[Fs]; Vs = Vs[sub2]; sub = sub[sub2]; nV = len(Vs)
loops = igl.all_boundary_loop(Fs) if hasattr(igl, 'all_boundary_loop') else [igl.boundary_loop(Fs)]
loops = sorted([np.asarray(l) for l in loops], key=len, reverse=True)
print('S verts', nV, 'boundary loops', [len(l) for l in loops], flush=True)
bnd = loops[0]; tipset = np.nonzero(np.linalg.norm(Vs - tip, axis=1) < 0.6)[0]
# tail coordinate = surface geodesic distance from the root loop (multi-source Dijkstra on the edge graph of S), normalized by its value at the tip.
# Level sets are parallel offsets of the root loop (equally spaced everywhere around the ring by construction: root rings wrap the posterior pelvis at
# uniform spacing -- no crowding) and become axis-normal fronts along the free tail.
from scipy.sparse.csgraph import dijkstra
Eg = np.unique(np.sort(np.r_[Fs[:, [0, 1]], Fs[:, [1, 2]], Fs[:, [2, 0]]], 1), axis=0); wl = np.linalg.norm(Vs[Eg[:, 0]] - Vs[Eg[:, 1]], axis=1)
G = sp.coo_matrix((np.r_[wl, wl], (np.r_[Eg[:, 0], Eg[:, 1]], np.r_[Eg[:, 1], Eg[:, 0]])), shape=(nV, nV)).tocsr()
psi = dijkstra(G, directed=False, indices=bnd, min_only=True); PSI_TIP = float(psi[ti_]) if (ti_ := int(np.argmin(np.linalg.norm(Vs - tip, axis=1)))) is not None else 1.0
phi = psi / PSI_TIP; phi[phi > 1] = 1.0
print('geodesic coordinate: root -> tip', round(PSI_TIP, 2), 'cm', flush=True)
def iso(level):
    """closed iso-contour of phi at level on (Vs, Fs): points with (triangle, barycentric) -- longest loop"""
    f = phi[Fs] - level; s = np.sign(f); cross = ~((s[:, 0] == s[:, 1]) & (s[:, 1] == s[:, 2]))
    segs = []; seginfo = []
    for t in np.nonzero(cross)[0]:
        pts = []
        for a, c in ((0, 1), (1, 2), (2, 0)):
            if (f[t, a] < 0) != (f[t, c] < 0):
                w = f[t, a] / (f[t, a] - f[t, c]); bc = np.zeros(3); bc[a] = 1 - w; bc[c] = w
                key = (min(Fs[t, a], Fs[t, c]), max(Fs[t, a], Fs[t, c])); pts.append((key, bc))
        if len(pts) == 2: segs.append((pts[0][0], pts[1][0])); seginfo.append((t, pts[0][1], pts[1][1]))
    adj = {}
    for i, (a, c) in enumerate(segs): adj.setdefault(a, []).append((c, i)); adj.setdefault(c, []).append((a, i))
    used = set(); best = []
    for start in list(adj):
        if any(i in used for _, i in adj[start]) and len(adj[start]) and all(i in used for _, i in adj[start]): continue
        loop = [start]; cur = start; prev = None
        while True:
            nxt = [(c, i) for c, i in adj[cur] if i not in used]
            if not nxt: break
            c, i = nxt[0]; used.add(i); loop.append(c); cur = c
            if c == start: break
        if len(loop) > len(best): best = loop
    def pos(key):
        a, c = key; t = phi[a] - level; u = phi[c] - level; w = t / (t - u); return (1 - w) * Vs[a] + w * Vs[c], (a, c, w)
    P = []; E = []
    for k in best[:-1]: p, e = pos(k); P.append(p); E.append(e)
    return np.array(P), E
def resample_sweep(P, prevR, N):
    """sweep sampling: the previous ring's vertices (every other one at a 2:1 row) are projected to this loop (arc parameters), then the parameters
    are relaxed along the loop (5 Laplacian passes in arc length) -- keeps vertex-to-vertex correspondence between rings (no shear bands where the
    cross-section changes shape) while evening out the spacing."""
    c = P.mean(0); d = tip - c; d /= np.linalg.norm(d)
    if np.dot(np.cross(P[1] - c, P[2] - c), d) < 0: P = P[::-1]
    Qs = np.vstack([P, P[:1]]); seg = Qs[1:] - Qs[:-1]; sl = np.r_[0, np.cumsum(np.linalg.norm(seg, axis=1))]; L = sl[-1]
    src = prevR if len(prevR) == N else prevR[::len(prevR) // N]
    tp = []
    for q in src:
        tt = np.clip(((q - Qs[:-1]) * seg).sum(1) / np.maximum((seg * seg).sum(1), 1e-12), 0, 1); dd = np.linalg.norm(Qs[:-1] + tt[:, None] * seg - q, axis=1); j = int(np.argmin(dd))
        tp.append(sl[j] + tt[j] * np.linalg.norm(seg[j]))
    t = np.unwrap(np.array(tp) / L * 2 * np.pi) / (2 * np.pi) * L
    if t[-1] < t[0]: t = t[0] - (t - t[0])          # keep increasing orientation
    for _ in range(5):
        tn = t.copy(); ext = np.r_[t[-1] - L, t, t[0] + L]; tn = 0.5 * t + 0.25 * (ext[:-2] + ext[2:]); tn[0] = t[0]; t = tn
    t = np.mod(t, L); out = []
    for s_ in t:
        j = min(np.searchsorted(sl, s_, side='right') - 1, len(P) - 1); w = (s_ - sl[j]) / max(sl[j + 1] - sl[j], 1e-12); out.append((1 - w) * Qs[j] + w * Qs[j + 1])
    return np.array(out), L
def resample(P, E, N, prev0=None):
    """N points at equal arc length; phase-locked to the dorsal-most (max u) point; orientation fixed (counter-clockwise seen from the tip)"""
    c = P.mean(0); d = tip - c; d /= np.linalg.norm(d)
    if np.dot(np.cross(P[1] - c, P[2] - c), d) < 0: P = P[::-1]; E = E[::-1]
    if prev0 is None: i0 = int(np.argmax(P[:, 2]))                 # first ring: phase at the dorsal midline
    else:                                                          # later rings: phase = projection of the previous ring's vertex 0 (no twist / phase jumps)
        Qs = np.vstack([P, P[:1]]); seg = Qs[1:] - Qs[:-1]; tt = np.clip(((prev0 - Qs[:-1]) * seg).sum(1) / np.maximum((seg * seg).sum(1), 1e-12), 0, 1)
        dd = np.linalg.norm(Qs[:-1] + tt[:, None] * seg - prev0, axis=1); j0 = int(np.argmin(dd)); P = np.vstack([Qs[:-1][j0] + tt[j0] * seg[j0], P[j0 + 1:], P[:j0 + 1]]); E = [E[j0]] + E[j0 + 1:] + E[:j0 + 1]; i0 = 0
    P = np.roll(P, -i0, 0); E = E[i0:] + E[:i0]
    Q = np.vstack([P, P[:1]]); from scipy.ndimage import gaussian_filter1d
    Ps = np.c_[[gaussian_filter1d(P[:, j], 6, mode='wrap') for j in range(3)]].T; Qsm = np.vstack([Ps, Ps[:1]])        # arc length on the 6-sample-smoothed loop: small relief ripples do not shift samples
    sl = np.r_[0, np.cumsum(np.linalg.norm(np.diff(Qsm, axis=0), axis=1))]; L = np.r_[0, np.cumsum(np.linalg.norm(np.diff(Q, axis=0), axis=1))][-1]; Ls = sl[-1]
    out = []; emb = []
    for k in range(N):
        s = k * Ls / N; j = np.searchsorted(sl, s, side='right') - 1; j = min(j, len(P) - 1); w = (s - sl[j]) / max(sl[j + 1] - sl[j], 1e-12)
        a1, c1, w1 = E[j]; a2, c2, w2 = E[(j + 1) % len(E)]
        out.append((1 - w) * Q[j] + w * Q[j + 1]); emb.append((j, w))
    return np.array(out), L
# ring levels: march phi so that loop spacing ~= edge length (perimeter / N)
rings = []; level = 0.3 / PSI_TIP; Ncur = 128; EMAX = 0.95                 # N halves (authored 2:1 row) as soon as the coarser ring edge (perimeter / (N / 2)) would be <= EMAX cm
Nsched = 'N = 128 at the root ring; 2:1 halving whenever perimeter / (N / 2) <= %.2f cm (N stays a multiple of 4 down to 8); tip: 8 -> 4 -> one cap quad' % EMAX
P0, E0 = iso(level); prevP = P0
while level < 0.9985:
    P, E = iso(level)
    if len(P) < 4: break
    per0 = np.linalg.norm(np.diff(np.vstack([P, P[:1]]), axis=0), axis=1).sum()
    if Ncur > 8 and per0 / (Ncur / 2) <= (EMAX if Ncur // 2 >= 16 else 0.45): Ncur //= 2      # the terminal 16 -> 8 halving waits for a <= 0.45 cm edge (tip curvature)
    N = Ncur; R, per = resample(P, E, N, rings[-1]['P'][0] if rings else None); rings.append(dict(level=level, N=N, P=R, perimeter=per))
    e = per / N; level = level + e / PSI_TIP                         # next ring one edge length further along the geodesic coordinate (square quads)
print('rings', len(rings), [r['N'] for r in rings][:5], '...', flush=True)
# faces: regular quads between rings of equal N. Authored all-quad 2:1 transitions (fine 4p -> coarse 2p): per 4 fine segments (f0..f4) and 2 coarse
# segments (c0..c2) one interior vertex x, 4 quads [f0 f1 x c0] [f1 f2 f3 x] [f3 f4 c2 x] [x c2 c1 c0] (x valence 4; the poles sit on the transition row).
# Tip: the 12-ring reduces once more to a 6-ring (same template) which closes with two quads [0 1 2 3] [3 4 5 0] (tail-tip exemption: no fan pole).
Vout = []; Q = []; Tri = []; ringidx = []
for r in rings:
    ringidx.append(np.arange(len(Vout), len(Vout) + r['N'])); Vout.extend(r['P'].tolist())
Vout = np.array(Vout)
def two_to_one(a, c):
    global Vout
    Na, Nc = len(a), len(c); assert Na == 2 * Nc and Nc % 2 == 0
    for p in range(Nc // 2):
        f = [a[(4 * p + j) % Na] for j in range(5)]; cc = [c[(2 * p + j) % Nc] for j in range(3)]
        x = 0.25 * (Vout[f[1]] + Vout[f[3]] + Vout[cc[0]] + Vout[cc[2]]); xi = len(Vout); Vout = np.vstack([Vout, x])
        Q.extend([[f[0], f[1], xi, cc[0]], [f[1], f[2], f[3], xi], [f[3], f[4], cc[2], xi], [xi, cc[2], cc[1], cc[0]]])
for i in range(len(rings) - 1):
    a, c = ringidx[i], ringidx[i + 1]; Na, Nc = len(a), len(c)
    if Na == Nc:
        for k in range(Na): Q.append([a[k], a[(k + 1) % Na], c[(k + 1) % Na], c[k]])
    else: two_to_one(a, c)
last = ringidx[-1]; cap = []; Nl = len(last)
for k in range(Nl // 2):
    p = Vout[last[2 * k]] + 0.45 * (tip - Vout[last[2 * k]]); cap.append(len(Vout)); Vout = np.vstack([Vout, p])
two_to_one(last, np.array(cap))
tipi = len(Vout); Vout = np.vstack([Vout, tip])                                  # the tip vertex closes the cap (2 quads around it; tail-tip exemption)
if len(cap) == 4: Q.extend([[cap[0], cap[1], tipi, cap[3]], [cap[1], cap[2], cap[3], tipi]])
else: Q.extend([[cap[0], cap[1], cap[2], tipi], [cap[2], cap[3], cap[4], tipi], [cap[4], cap[5], cap[0], tipi]])
Q = np.array(Q); Tri = np.array(Tri)
# authored relax pass (the 'relax brush' step of manual retopology): 25 iterations of quad-graph umbrella smoothing, each followed by projection back to
# the base surface (S sub-mesh); the root ring (boundary) and the tip vertex are pinned. Topology is unchanged; this only removes shear left by the
# level-set sampling where the tail cross-section changes shape.
Eq = np.unique(np.sort(np.r_[Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]], 1), axis=0); nVo = len(Vout)
Aq = sp.coo_matrix((np.ones(2 * len(Eq)), (np.r_[Eq[:, 0], Eq[:, 1]], np.r_[Eq[:, 1], Eq[:, 0]])), shape=(nVo, nVo)).tocsr(); deg = np.asarray(Aq.sum(1)).ravel()
pin = np.zeros(nVo, bool); pin[ringidx[0]] = True; pin[ringidx[-1][0]:] = True; pin[np.r_[ringidx[-2], ringidx[-3]]] = True   # root ring, last 3 rings + cap + tip pinned
for it in range(25):
    avg = (Aq @ Vout) / deg[:, None]; new = Vout.copy(); new[~pin] = 0.5 * Vout[~pin] + 0.5 * avg[~pin]
    _, _, cp_ = igl.point_mesh_squared_distance(new, Vs, Fs); Vout[~pin] = cp_[~pin]
# project every module vertex to the base surface (closest point) and record (base triangle, barycentric) for exact c1 / c2 realization
d2, fi, cp = igl.point_mesh_squared_distance(Vout, V, F); BC = igl.barycentric_coordinates(cp, V[F[fi, 0]], V[F[fi, 1]], V[F[fi, 2]]) if hasattr(igl, 'barycentric_coordinates') else None
if BC is None:
    a0, b0, c0 = V[F[fi, 0]], V[F[fi, 1]], V[F[fi, 2]]; v0 = b0 - a0; v1 = c0 - a0; v2 = cp - a0
    d00 = (v0 * v0).sum(1); d01 = (v0 * v1).sum(1); d11 = (v1 * v1).sum(1); d20 = (v2 * v0).sum(1); d21 = (v2 * v1).sum(1); den = d00 * d11 - d01 * d01
    bb = (d11 * d20 - d01 * d21) / den; cc = (d00 * d21 - d01 * d20) / den; BC = np.c_[1 - bb - cc, bb, cc]
Vp_ = (BC[:, :, None] * V[F[fi]]).sum(1)
spacing = [float(np.mean(np.linalg.norm(rings[i + 1]['P'][:, None] - rings[i]['P'][None], axis=2).min(1))) for i in range(len(rings) - 1)]
root_rings = sum(1 for r in rings if r['level'] < 0.08)
np.savez_compressed(OUT + '/SA_tail_module.npz', V=Vp_, Q=Q, T=Tri, tri=fi, bc=BC, ring_start=np.array([r[0] for r in ringidx]), ring_N=np.array([len(r) for r in ringidx]),
                    ring_level=np.array([r['level'] for r in rings]), phi=phi, sub=sub)
info = dict(rings=len(rings), N_schedule=Nsched, root_rings_phi_lt_0p08=root_rings, verts=int(len(Vp_)), quads=int(len(Q)), tris=int(len(Tri)),
            quad_fraction=round(len(Q) / (len(Q) + len(Tri)), 4), ring_table=[dict(level=round(r['level'], 5), N=r['N'], perimeter_cm=round(r['perimeter'], 2), edge_cm=round(r['perimeter'] / r['N'], 3),
                                                                                   spacing_to_next_cm=round(spacing[i], 3) if i < len(spacing) else None) for i, r in enumerate(rings)],
            projection_max_mm=round(float(np.sqrt(d2.max()) * 10), 4))
json.dump(info, open(OUT + '/SA_tail_module.json', 'w'), indent=1)
print('MODULE', info['verts'], 'V', info['quads'], 'Q', info['tris'], 'T', 'rings', info['rings'], 'root rings', root_rings, 'quad frac', info['quad_fraction'])
