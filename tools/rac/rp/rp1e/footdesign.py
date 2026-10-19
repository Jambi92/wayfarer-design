"""RP1E foot sub-cage DESIGN (prep only; the cage is authored by hand in the Blender UI from these numbers).
Topology: ankle ring A (existing 14-vertex leg ring, kept) -> fan sections F1..Fn (planes through a transverse pivot line C
in front of the ankle, rotating from horizontal to vertical: the leg tube bends forward into the foot; the posterior half of
each ring sweeps round the heel onto the sole) -> optional vertical sections -> cap ring K (7 dorsal + 7 plantar verts at
toe-column boundaries) -> 6 cap quads: hallux 2, toe2 1, toe3 1, toe4 2 -> toe tubes (6-vertex rings for hallux/toe4,
4-vertex rings for toes 2/3) fitted to source sections.
Usage: python3 footdesign.py S params.json   -> fdesign_S.json"""
import numpy as np, sys, json, collections
from scipy.spatial import cKDTree
s = sys.argv[1]; P = json.load(open(sys.argv[2]))
w = np.load('/home/claude/stc/rp1/weld.npz'); V = w['V'].astype(float); F = w['F'].astype(np.int64)
q = np.load('fseg_%s.npz' % s); ax = q['ax']; used = q['used']; labu = q['lab']
lab = np.full(len(V), -1); lab[used] = labu
up = np.array([0, 0, 1.0]); lat = np.cross(ax, up)
cg = np.load('ui_v005.npz'); CV = cg['V']; CF = cg['F']
adj = collections.defaultdict(set)
for f in CF:
    for i in range(4): a, b = int(f[i]), int(f[(i + 1) % 4]); adj[a].add(b); adj[b].add(a)
ringset = set(P['ankle_ring'])
ring = [P['ankle_ring'][0]]
while len(ring) < len(ringset):
    nx = [v for v in adj[ring[-1]] if v in ringset and v not in ring]
    ring.append(nx[0] if len(ring) == 1 else nx[0])
A = CV[ring]
footm = ((w['w_foot_' + s] > 0.5) | (w['w_shin_' + s] > 0.5)) & (V[:, 2] < P['z_cut'])
Fm = F[footm[F].all(1)]
def loop_section(n, p0, keep):
    d = (V - p0) @ n
    T = Fm[(np.sign(d[Fm]).min(1) < 0) & (np.sign(d[Fm]).max(1) > 0)]
    segs = []
    for t in T:
        pts = []
        for i, j in ((0, 1), (1, 2), (2, 0)):
            if d[t[i]] * d[t[j]] < 0: u = d[t[i]] / (d[t[i]] - d[t[j]]); pts.append(V[t[i]] + (V[t[j]] - V[t[i]]) * u)
        if len(pts) == 2 and keep((pts[0] + pts[1]) / 2): segs.append(pts)
    S = np.array(segs)
    # chain
    P0, P1 = S[:, 0], S[:, 1]; T2 = cKDTree(np.vstack([P0, P1])); n_ = len(S); used_ = np.zeros(n_, bool); loops = []
    for st in range(n_):
        if used_[st]: continue
        used_[st] = True; lp = [P0[st], P1[st]]; cur = P1[st]
        for _ in range(n_):
            c = [j % n_ for j in T2.query_ball_point(cur, 1e-5) if not used_[j % n_]]
            if not c: break
            j = c[0]; used_[j] = True; cur = P1[j] if np.linalg.norm(P0[j] - cur) < 1e-5 else P0[j]; lp.append(cur)
        loops.append(np.array(lp))
    L = max(loops, key=lambda l: np.linalg.norm(np.diff(l, axis=0), axis=1).sum())
    return L
def resample(L, n_pts, start_pt, normal, orient_ref, fracs):
    # closed polyline L -> n_pts points at arc fractions, starting at the point closest to start_pt, oriented like orient_ref
    if np.linalg.norm(L[0] - L[-1]) > 1e-4: L = np.vstack([L, L[:1]])
    seg = np.linalg.norm(np.diff(L, axis=0), axis=1); cum = np.r_[0, np.cumsum(seg)]; tot = cum[-1]
    i0 = np.argmin(np.linalg.norm(L - start_pt, axis=1)); c0 = cum[i0]
    cen = L[:-1].mean(0)
    # orientation: signed area about normal
    a = np.cross(L[:-1] - cen, L[1:] - cen).sum(0) @ normal
    sgn = 1 if a * orient_ref > 0 else -1
    out = []
    for f in fracs:
        t = (c0 + sgn * f * tot) % tot; k = np.searchsorted(cum, t) - 1; k = min(max(k, 0), len(seg) - 1)
        u = (t - cum[k]) / max(seg[k], 1e-9); out.append(L[k] + u * (L[k + 1] - L[k]))
    return np.array(out), cen
def inset(Q, cen, normal, dd):
    # move each point inward by dd within the section plane (towards the local inside = towards centroid, projected)
    out = []
    for p in Q:
        v = cen - p; v -= (v @ normal) * normal; out.append(p + dd * v / max(np.linalg.norm(v), 1e-9))
    return np.array(out)
# ring A arc fractions starting from its vertex nearest the pivot
uA = A @ ax
C = A[np.argmax(uA)].copy(); C = C + P['pivot_fwd'] * ax; C[2] = A[:, 2].max() + P['pivot_up']

nA = np.cross(A[1] - A[0], A[2] - A[0]); cenA = A.mean(0)
areaA = np.cross(A - cenA, np.roll(A, -1, 0) - cenA).sum(0)
lA = np.linalg.norm(np.roll(A, -1, 0) - A, axis=1); fA = np.r_[0, np.cumsum(lA)[:-1]] / lA.sum()
N = len(ring)
# --- cap ring (radial frame about the ankle centroid on the ground) ---
LM = json.load(open('/home/claude/stc/rp1/landmarks_source.json'))
C0 = np.array(LM['ankle_' + s]['centroid']) * [1, -1, 1]; C0[2] = 0
Dxy = V[:, :2] - C0[:2]; Rr = np.linalg.norm(Dxy, axis=1); Ph = np.degrees(np.arctan2(Dxy[:, 1], Dxy[:, 0]))
rb = {k: float(np.percentile(Rr[lab == k], 3)) for k in range(4)}
phr = {k: (float(Ph[lab == k].min()), float(Ph[lab == k].max())) for k in range(4)}
# medial->lateral order of phi: hallux first
sg = 1 if np.mean(phr[0]) > np.mean(phr[3]) else -1      # +1: phi decreases medial->lateral
def lo(k): return phr[k][0] if sg > 0 else phr[k][1]
def hi(k): return phr[k][1] if sg > 0 else phr[k][0]
bphi = [hi(0) + sg * 0, 0.5 * (hi(0) + lo(0)), 0.5 * (lo(0) + hi(1)), 0.5 * (lo(1) + hi(2)), 0.5 * (lo(2) + hi(3)), 0.5 * (hi(3) + lo(3)), lo(3)]
bphi = np.array(bphi); bphi[0] -= sg * P['edge_in_deg']; bphi[-1] += sg * P['edge_in_deg']
rcol = np.array([rb[0], rb[0], min(rb[0], rb[1]), min(rb[1], rb[2]), min(rb[2], rb[3]), rb[3], rb[3]]) - P['cap_back']
dors, plan = [], []
for rr, ph in zip(rcol, bphi):
    xy = C0[:2] + rr * np.array([np.cos(np.radians(ph)), np.sin(np.radians(ph))])
    m = (np.linalg.norm(V[:, :2] - xy, axis=1) < 0.7) & footm
    zt, zb = V[m, 2].max(), V[m, 2].min()
    dors.append([xy[0], xy[1], zt - P['cap_inset']]); plan.append([xy[0], xy[1], zb + P['cap_inset']])
dors = np.array(dors); plan = np.array(plan); bnd = bphi; ucol = rcol; med_sign = 1
# cap ring in ring order: start = dorsal middle (d3, closest to pivot side = top), orientation like A
K = np.vstack([dors[3:], plan[::-1], dors[:3]])     # d3..d6, p6..p0, d0..d2
cenK = K.mean(0); areaK = np.cross(K - cenK, np.roll(K, -1, 0) - cenK).sum(0)
if (areaK @ -ax) * (areaA @ up) < 0:   # flip direction keeping d3 first
    K = np.vstack([K[:1], K[1:][::-1]]); flipped = True
else: flipped = False
lK = np.linalg.norm(np.roll(K, -1, 0) - K, axis=1); fK = np.r_[0, np.cumsum(lK)[:-1]] / lK.sum()
# --- fan + vertical sections: angular transport of ring A's vertices ---
def ang(Pts, cen, e1, e2): Q = Pts - cen; return np.arctan2(Q @ e2, Q @ e1)
aA = ang(A, A.mean(0), lat, -ax)
i0 = int(np.argmin(np.abs(np.angle(np.exp(1j * (aA - ang(K[:1], K.mean(0), lat, -up)[0])))))); ring = ring[i0:] + ring[:i0]; A = CV[ring]; aA = ang(A, A.mean(0), lat, -ax)
cK = K.mean(0); aK = ang(K, cK, lat, -up)
# orientation: both must run the same way
def runs(a_): d = np.angle(np.exp(1j * (np.roll(a_, -1) - a_))); return np.sign(d.sum())
if runs(aK) != runs(aA):
    K = np.vstack([K[:1], K[1:][::-1]]); flipped = not flipped; aK = ang(K, cK, lat, -up)
dA = np.angle(np.exp(1j * (aK - aA)))
def ray_loop(L, cen, e1, e2, al):
    Q = np.c_[(L - cen) @ e1, (L - cen) @ e2]; out = []
    for a_ in al:
        dv = np.array([np.cos(a_), np.sin(a_)]); best = None
        for k in range(len(Q) - 1):
            p, q_ = Q[k], Q[k + 1]; M = np.array([dv, p - q_]).T
            if abs(np.linalg.det(M)) < 1e-12: continue
            t, u = np.linalg.solve(M, p)
            if t > 0 and 0 <= u <= 1 and (best is None or t > best[0]): best = (t, p + u * (q_ - p))
        out.append(cen + best[1][0] * e1 + best[1][1] * e2)
    return np.array(out)
secs = []; ns = P['n_sec']
# sagittal profile: section of the foot by the plane lat = lat_c through the ankle-ring centre
latc = A.mean(0) @ lat
def pieces(n, p0, mask):
    d = (V - p0) @ n; Fq = F[mask[F].all(1)]
    T = Fq[(np.sign(d[Fq]).min(1) < 0) & (np.sign(d[Fq]).max(1) > 0)]
    segs = []
    for t in T:
        pts = []
        for i, j in ((0, 1), (1, 2), (2, 0)):
            if d[t[i]] * d[t[j]] < 0: u = d[t[i]] / (d[t[i]] - d[t[j]]); pts.append(V[t[i]] + (V[t[j]] - V[t[i]]) * u)
        if len(pts) == 2: segs.append(pts)
    S = np.array(segs); P0, P1 = S[:, 0], S[:, 1]; T2 = cKDTree(np.vstack([P0, P1])); n_ = len(S); us = np.zeros(n_, bool); out = []
    def walk(st):
        lp = [P0[st], P1[st]]; cur = P1[st]
        for _ in range(n_):
            c = [j % n_ for j in T2.query_ball_point(cur, 1e-5) if not us[j % n_]]
            if not c: break
            j = c[0]; us[j] = True; cur = P1[j] if np.linalg.norm(P0[j] - cur) < 1e-5 else P0[j]; lp.append(cur)
        return lp
    for st in range(n_):
        if us[st]: continue
        us[st] = True; a_ = walk(st)
        # extend backwards from start
        P0[st], P1[st] = P1[st].copy(), P0[st].copy(); b_ = walk(st) if False else []
        out.append(np.array(a_))
    return out
nontoe = footm & ~np.isin(lab, [0, 1, 2, 3])
pcs = pieces(lat, latc * lat, nontoe)
pcs = [p for p in pcs if len(p) > 20]
zA = A[:, 2].mean()
fA_ = A[np.argmax(A @ ax)]; bA_ = A[np.argmin(A @ ax)]
def best_piece(pt):
    return min(pcs, key=lambda p: np.min(np.linalg.norm(p - pt, axis=1)))
def nearest_on(p, pt): return int(np.argmin(np.linalg.norm(p - pt, axis=1)))
def subpath(p, a_, b_):
    i, j = nearest_on(p, a_), nearest_on(p, b_)
    return p[i:j + 1] if j >= i else p[j:i + 1][::-1]
dK = K[0]; pK = K[7]
fstart = A[np.argmax(A @ ax)].copy(); bstart = A[np.argmin(A @ ax)].copy()
Pf = best_piece(np.array([*(latc * lat)[:2], 0]) * 0 + fstart); pf = subpath(Pf, fstart, dK)
Pb = best_piece(bstart); pb = subpath(Pb, bstart, pK)
print('front path', pf[0].round(1), '->', pf[-1].round(1), len(pf), ' back path', pb[0].round(1), '->', pb[-1].round(1), len(pb))
def at(pth, f):
    sl = np.r_[0, np.cumsum(np.linalg.norm(np.diff(pth, axis=0), axis=1))]; t = f * sl[-1]; k = min(np.searchsorted(sl, t) - 1, len(pth) - 2); k = max(k, 0)
    return pth[k] + (t - sl[k]) / max(sl[k + 1] - sl[k], 1e-9) * (pth[k + 1] - pth[k])
for k in range(ns):
    fr = (k + 1) / (ns + 1)
    fp = at(pf, fr); bp = at(pb, fr)
    e2 = bp - fp; e2 -= (e2 @ lat) * lat; e2 /= np.linalg.norm(e2); n = np.cross(lat, e2)
    p0 = 0.5 * (fp + bp); print('sec', k, 'f', fp.round(1), 'b', bp.round(1))
    L = loop_section(n, p0, lambda p, n=n, p0=p0: True)
    if np.linalg.norm(L[0] - L[-1]) > 1e-4: L = np.vstack([L, L[:1]])
    cen = L[:-1].mean(0)
    # in-plane frame consistent with ring A (lat, -ax) and cap (lat, -up): e1 = lat, e2 = direction front -> back/down
    Q = ray_loop(L, cen, lat, e2, aA + fr * dA)
    secs.append(dict(name='S%d' % (k + 1), pts=inset(Q, cen, n, P['inset']), normal=n))
secs.append(dict(name='K', pts=K, normal=ax))
# --- toe tubes ---
dg = json.load(open('digits_F%s.json' % s))
def secring(labk, c, t, ew, et, R=3.5):
    t = t / np.linalg.norm(t); m = lab == labk
    Fk = F[m[F].all(1)]; d = (V - c) @ t
    Fk = Fk[(np.sign(d[Fk]).min(1) < 0) & (np.sign(d[Fk]).max(1) > 0)]
    pts = []
    for f in Fk:
        qq = []
        for i_, j_ in ((0, 1), (1, 2), (2, 0)):
            if d[f[i_]] * d[f[j_]] < 0: u = d[f[i_]] / (d[f[i_]] - d[f[j_]]); qq.append(V[f[i_]] + (V[f[j_]] - V[f[i_]]) * u)
        if len(qq) == 2 and np.linalg.norm((qq[0] + qq[1]) / 2 - c) < R: pts.append((qq[0] + qq[1]) / 2)
    if len(pts) < 10: return None
    Pp = np.array(pts); e1 = ew - (ew @ t) * t; e1 /= np.linalg.norm(e1); e2 = np.cross(t, e1)
    if e2 @ et < 0: e2 = -e2
    U = (Pp - c) @ e1; W = (Pp - c) @ e2
    return c + 0.5 * (U.max() + U.min()) * e1 + 0.5 * (W.max() + W.min()) * e2, e1, e2, 0.5 * np.ptp(U), 0.5 * np.ptp(W)
tubes = {}
names = ['t1', 't2', 't3', 't4']
for k, nm in enumerate(names):
    d = dg[nm]; Cc = np.array(d['c']); T = np.array(d['t']); EW = np.array(d['ew']); ET = np.array(d['et'])
    rings = []
    rc = np.linalg.norm(Cc[:, :2] - C0[:2], axis=1); colsof = {'t1': [0, 1, 2], 't2': [2, 3], 't3': [3, 4], 't4': [4, 5, 6]}[nm]; capr = rcol[colsof].max() + P['st_gap']
    cand = [i for i in range(len(Cc) - 1) if rc[i] > capr]
    st_ = [cand[0]]
    for i in cand[1:]:
        if np.linalg.norm(Cc[i] - Cc[st_[-1]]) >= P['st_step']: st_.append(i)
    print(nm, "stations", st_, "of", len(Cc))
    for i in st_:
        Ta = Cc[-1] - Cc[0]; Ta /= np.linalg.norm(Ta)
        r = secring(k, Cc[i], Ta if P.get('parallel', 1) else T[i], EW[i], ET[i])
        if r is None: continue
        cc, e1, e2, a, b = r; a *= P['ka']; b *= P['kb']; a = max(a, 0.35); b = max(b, 0.35)
        hmed = V[lab == 0].mean(0) - V[lab == 3].mean(0); hmed -= (hmed @ Ta) * Ta
        if e1 @ hmed < 0: e1 = -e1          # e1 points medial
        if nm in ('t1', 't4'):   # 6 verts: dorsal medial, dorsal mid, dorsal lateral, plantar lateral, plantar mid, plantar medial
            rings.append([cc + a * e1 + b * e2, cc + b * e2 * 1.08, cc - a * e1 + b * e2, cc - a * e1 - b * e2, cc - b * e2 * 1.08, cc + a * e1 - b * e2])
        else:
            rings.append([cc + a * e1 + b * e2, cc - a * e1 + b * e2, cc - a * e1 - b * e2, cc + a * e1 - b * e2])
    # tip ring
    R4 = np.array(rings[-1]); cl = R4.mean(0); tl = cl - np.array(rings[-2]).mean(0); tl /= np.linalg.norm(tl)
    Xd = V[lab == k]; pr = (Xd - cl) @ tl; tc = cl + (pr.max() - P['tip_inset']) * tl
    if (tc - cl) @ tl > 0.4: rings.append(list(tc + P['tip_scale'] * (R4 - cl)))
    tubes[nm] = np.array(rings)
out = dict(side=s, ankle_ring=ring, pivot=C.tolist(), flipped=flipped,
           sections=[dict(name=x['name'], pts=np.round(x['pts'], 3).tolist()) for x in secs],
           dors=dors.round(3).tolist(), plan=plan.round(3).tolist(), bnd=bnd.round(2).tolist(), ucol=ucol.round(2).tolist(),
           tubes={k: v.round(3).tolist() for k, v in tubes.items()}, ax=ax.tolist(), lat=lat.tolist(), med_sign=med_sign)
json.dump(out, open('fdesign_%s.json' % s, 'w'))
print(s, 'pivot', C.round(1), 'ring0', A[0].round(1), 'sections', [x['name'] for x in secs], 'tubes', {k: len(v) for k, v in tubes.items()})
print(' bnd', bnd.round(1), 'ucol', ucol.round(1))
