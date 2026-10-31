# sa_design.py : RP5 Saurin AUTHORED coarse cage (order ad9cb85 §4-§13). Every corner is placed from the working source by a stated anatomical rule; every
# quad carries a semantic label. Modules (build order of the order §4): D axial trunk + E pelvis / sacrum with the accepted F tail module's root ring as a
# 16-edge hole (8 module vertices per coarse edge), I legs (pants split with a perineal crotch path) + J feet, G arms (8-edge shoulder holes) + H hands,
# B neck + A head (harmonic head-neck rings, orbit holes, mouth slit, rostral cap) + C cranial display root.
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sa_geo as GEO
from sa_geo import V, LM, LAB, NV
class Design:
    def __init__(s): s.C = []; s.name = []; s.Q = []; s.qlab = []; s.hint = {}; s.fixed = {}; s.idx = {}; s.pins = {}; s.loops = {}; s.arcs = {}
    def ring_arcs(s, names, P):
        """store the source-loop arcs between consecutive ring corners (ring edges then follow the authored section / level loop exactly)"""
        n = len(P); ii = [int(np.argmin(np.linalg.norm(P - s.C[s.idx[x]], axis=1))) for x in names]
        for dr in (1, -1):
            tot = sum(((ii[(k + 1) % len(ii)] - ii[k]) * dr) % n for k in range(len(ii)))
            if tot == n and len(set(ii)) == len(ii): break
        else: return False
        for k in range(len(names)):
            a, b = ii[k], ii[(k + 1) % len(ii)]; idx = [a]; j = a
            while j != b: j = (j + dr) % n; idx.append(j)
            s.arcs[(names[k], names[(k + 1) % len(names)])] = P[idx]
        return True
    def v(s, name, p):
        if name in s.idx: raise RuntimeError('dup corner ' + name)
        s.idx[name] = len(s.C); s.C.append(np.asarray(p, float)); s.name.append(name); return s.idx[name]
    def q(s, a, b, c, d, lab):
        ids = [s.idx[x] if isinstance(x, str) else x for x in (a, b, c, d)]; s.Q.append(ids); s.qlab.append(lab)
    def h(s, a, b, **kw):
        a, b = s.idx[a], s.idx[b]; s.hint[(min(a, b), max(a, b))] = kw
    def band(s, ra, rb, lab, closed=True, skip=()):
        """quads between two rings of corner names (same length)"""
        n = len(ra); rng = range(n) if closed else range(n - 1)
        for k in rng:
            if k in skip: continue
            s.q(ra[k], ra[(k + 1) % n], rb[(k + 1) % n], rb[k], lab)
D = Design()
def unit(x): x = np.asarray(x, float); return x / np.linalg.norm(x)
TAIL = np.load(GEO.W + '/tail/SA_tail_module.npz'); TR0 = TAIL['V'][TAIL['ring_start'][0]:TAIL['ring_start'][0] + TAIL['ring_N'][0]]     # module root ring (128)
# ------------------------------------------------------------------------------------------------ D / E trunk + pelvis
NT = 16                                                     # trunk columns: 0 ventral midline, 4 subject-left (+x), 8 dorsal, 12 right (-x)
def trunk_pt(u, k, cen=None, nk=NT):
    c = np.array([0.0, 0.0 if u > 125 else -2.0, u]) if cen is None else np.array([cen[0], cen[1], u])      # pelvis: centre slightly dorsal (inside the body above the perineum)
    lp = GEO.loop_around(c, (0, 0, 1), rad=150)
    if lp is None: raise RuntimeError('no trunk loop at u=%.1f' % u)
    P = lp['P']; c2 = P.mean(0); c2[2] = u; a = np.ptp(P[:, 0]) / 2; b = np.ptp(P[:, 1]) / 2; t = 2 * np.pi * k / nk
    if u < 125:                                                                   # pelvis: the section includes the tail -> fixed centre, front extents only
        Pf = P[P[:, 1] > -14]; c2 = np.array([0.0, -2.0, u]); a = np.ptp(Pf[:, 0]) / 2; b = Pf[:, 1].max() + 2.0
    d = unit([a * np.sin(t), b * np.cos(t), 0]); return GEO.ray_loop(c2, (0, 0, 1), lp, [d])[0]
def trunk_ring(name, u, cols=range(NT), ucol=None):
    out = []
    for k in cols:
        uk = u if ucol is None else ucol.get(k, u); out.append(D.v('%s_%d' % (name, k), trunk_pt(uk, k)))
    return ['%s_%d' % (name, k) for k in cols]
TU = dict(T0=164.0, T1=157.0, T2=150.0, T3=139.5, T4=134.0, T5=129.0)
rings = {}
T3U = {k: 143.8 for k in (2, 3, 4, 5, 6)}; T3U.update({k: 140.2 for k in (10, 11, 12, 13, 14)})      # hole bottom row just below each axilla apex (left 144.5, right 140.5)
for nm, u in TU.items(): rings[nm] = trunk_ring(nm, u, ucol=T3U if nm == 'T3' else None)
# pelvis rings P0..P4: dorsal columns 6..10 lie on the tail module root ring (module index 0 = dorsal top, increasing towards -x):
TAILIDX = {('P0', 6): 112, ('P0', 7): 120, ('P0', 8): 0, ('P0', 9): 8, ('P0', 10): 16, ('P1', 10): 24, ('P2', 10): 32, ('P3', 10): 40,
           ('P4', 10): 48, ('P4', 9): 56, ('P4', 8): 64, ('P4', 7): 72, ('P4', 6): 80, ('P3', 6): 88, ('P2', 6): 96, ('P1', 6): 104}
PU_FRONT = dict(P0=124.0, P1=118.5, P2=113.0, P3=107.5)
# perineal midline (midsagittal x = 0 section): front pubic point (f = 7) and the perineum (f = -4); the dorsal end is the tail module's ventral root (index 64)
_mid = GEO.section_loops(np.array([0, -5, 100.0]), (1, 0, 0), rad=60); _mp = np.vstack([lp['P'] for lp in _mid]); _mp = _mp[(_mp[:, 2] < 112) & (_mp[:, 2] > 85) & (np.abs(_mp[:, 1]) < 20)]
def _midbot(f): m = np.abs(_mp[:, 1] - f) < 0.6; return _mp[m][np.argmin(_mp[m, 2])]
for nm in ('P0', 'P1', 'P2', 'P3'):
    names = []
    for k in range(NT):
        cn = '%s_%d' % (nm, k)
        if (nm, k) in TAILIDX: D.v(cn, TR0[TAILIDX[(nm, k)]])
        elif nm == 'P0' and 6 <= k <= 10: continue
        elif nm != 'P0' and 7 <= k <= 9: continue                                  # inside the tail hole
        else:
            uf = PU_FRONT[nm] - (0.6 if k in (2, 3, 4, 12, 13, 14) else 0)
            if k in (5, 11): continue                                              # placed below: midpoint of the surface path lateral column -> tail corner
            D.v(cn, trunk_pt(uf, k))
        names.append(cn)
    import sa_layout as _LY
    for k, kl, kt in ((5, 4, 6), (11, 12, 10)):
        a_, b_ = GEO.snap(D.C[D.idx['%s_%d' % (nm, kl)]]), GEO.snap(D.C[D.idx['%s_%d' % (nm, kt)]]); pth = V[_LY.local_path(a_, b_, np.zeros(NV, bool), factor=1.3, margin=2)]
        sl = np.r_[0, np.cumsum(np.linalg.norm(np.diff(pth, axis=0), axis=1))]; D.v('%s_%d' % (nm, k), pth[np.searchsorted(sl, 0.5 * sl[-1])])
    rings[nm] = names
# P4 = the thigh-root ring (inguinal fold -> lateral hip -> tail root base): shortest surface path pubic point -> lateral hip point (u = 97, max |x| at
# |f| < 4) -> tail-root corner (module index 80 / 48); corners at equal arc fractions along it.
D.v('P4_0', _midbot(7.0)); D.v('crotch', _midbot(-4.0))
for k in (6, 7, 8, 9, 10): D.v('P4_%d' % k, TR0[TAILIDX[('P4', k)]])
for sg, ks, kt in ((1, [1, 2, 3, 4, 5], 6), (-1, [15, 14, 13, 12, 11], 10)):
    A = D.C[D.idx['P4_0']]; Cc = D.C[D.idx['P4_%d' % kt]]
    hs = [lp['P'] for lp in GEO.section_loops(np.array([0, 0, 97.0]), (0, 0, 1), rad=60)]; hs = np.vstack(hs); hs = hs[(np.abs(hs[:, 1]) < 4) & (sg * hs[:, 0] > 5) & (sg * hs[:, 0] < 28)]
    Hl = hs[np.argmax(sg * hs[:, 0])]                                              # lateral hip surface point at u = 97
    import sa_layout as LY
    nb = np.zeros(NV, bool); pa = LY.local_path(GEO.snap(A), GEO.snap(Hl), nb, factor=1.3, margin=3); pb = LY.local_path(GEO.snap(Hl), GEO.snap(Cc), nb, factor=1.3, margin=3)
    best = V[np.r_[pa, pb[1:]]]                                                   # surface path pubic point -> lateral hip -> tail-root corner
    sl = np.r_[0, np.cumsum(np.linalg.norm(np.diff(best, axis=0), axis=1))]; sl /= sl[-1]
    for k, t in zip(ks, (0.13, 0.30, 0.50, 0.70, 0.86)): D.v('P4_%d' % k, best[np.searchsorted(sl, t)])
rings['P4'] = ['P4_%d' % k for k in range(NT)]
# trunk bands
order = ['T0', 'T1', 'T2', 'T3', 'T4', 'T5']
ARMHOLE = {1: [3, 4, 5], -1: [13, 12, 11]}                 # +x (left) and -x (right) columns of the 2 x 2 shoulder holes on rows T1..T3
for ra, rb in zip(order[:-1], order[1:]):
    skip = []
    if (ra, rb) in (('T1', 'T2'), ('T2', 'T3')): skip = [3, 4, 11, 12]
    D.band(['%s_%d' % (rb, k) for k in range(NT)], ['%s_%d' % (ra, k) for k in range(NT)], 'trunk', skip=skip)
D.band(['P0_%d' % k for k in range(NT)], ['T5_%d' % k for k in range(NT)], 'trunk')
for ra, rb in (('P0', 'P1'), ('P1', 'P2'), ('P2', 'P3'), ('P3', 'P4')):
    for k in list(range(0, 6)) + list(range(10, 16)):
        D.q('%s_%d' % (rb, k), '%s_%d' % (rb, (k + 1) % NT), '%s_%d' % (ra, (k + 1) % NT), '%s_%d' % (ra, k), 'pelvis')
# tail root edges: fixed (module ring points, 8 segments each)
TAILCORNER = {v: k for k, v in TAILIDX.items()}
seq = sorted(TAILIDX.values())
for i, a in enumerate(seq):
    b = seq[(i + 1) % len(seq)]; ia = D.idx['%s_%d' % TAILCORNER[a]]; ib = D.idx['%s_%d' % TAILCORNER[b]]
    pts = TR0[[(a + j) % 128 for j in range(9)]]
    if ia > ib: pts = pts[::-1]
    D.fixed[(min(ia, ib), max(ia, ib))] = (pts, 8)
D.loops['tail_root_ring'] = ['%s_%d' % TAILCORNER[a] for a in seq]
# ------------------------------------------------------------------------------------------------ limb helpers
def plane_ring(c, n, angles, ref0, ref90, rad=25, vmask=None, field=None, level=None):
    """corners on the section loop (plane c,n) around c at angles (deg) measured from ref0 towards ref90 (both projected into the plane)"""
    n = unit(n); r0 = unit(ref0 - (ref0 @ n) * n); r9 = unit(ref90 - (ref90 @ n) * n - (ref90 @ r0) * r0)
    lp = GEO.loop_around(c, n, rad=rad)
    if lp is None:                                                                 # centre outside a curved section (palm): nearest closed loop, rays from its centroid
        L = [l for l in GEO.section_loops(c, n, rad) if l['closed'] and len(l['P']) > 20]
        if not L: raise RuntimeError('no loop around %s' % np.round(c, 1))
        lp = min(L, key=lambda l: np.linalg.norm(l['P'].mean(0) - c)); c = lp['P'].mean(0)
    return arc_place(lp['P'], c, n, angles, ref0, ref90), lp
def arc_place(P, c, n, angles, r0, r9):
    """corners on the closed loop P: phase = loop point in the direction angles[0] (from c, frame r0 -> r9 in the plane normal n); the others at arc
    fractions (angle_k - angle_0) / 360 in the sense of increasing angle -> always distinct, ordered and spread like the requested angles"""
    n = unit(n); e1 = unit(r0 - (r0 @ n) * n); e2 = unit(r9 - (r9 @ n) * n - (r9 @ e1) * e1)
    xy = np.c_[(P - c) @ e1, (P - c) @ e2]; th = np.arctan2(xy[:, 1], xy[:, 0]); a0 = np.radians(angles[0])
    i0 = int(np.argmin(np.abs(np.angle(np.exp(1j * (th - a0))))))
    area = 0.5 * (xy[:, 0] @ np.roll(xy[:, 1], -1) - xy[:, 1] @ np.roll(xy[:, 0], -1)); dr = 1 if area > 0 else -1
    fr = [((a - angles[0]) % 360) / 360.0 for a in angles]
    return list(GEO.arc_points(P, i0, fr, dr))
def loop_ring(lp, c, n, angles, ref0, ref90):
    return arc_place(lp['P'], c, n, angles, ref0, ref90)
def _loop_ring_rays(lp, c, n, angles, ref0, ref90):
    n = unit(n); r0 = unit(ref0 - (ref0 @ n) * n); r9 = unit(ref90 - (ref90 @ n) * n - (ref90 @ r0) * r0)
    # rays in the loop's best-fit plane from its centroid
    dirs = [np.cos(np.radians(a)) * r0 + np.sin(np.radians(a)) * r9 for a in angles]
    P = lp['P']; e1, e2 = r0, r9; xy = np.c_[(P - c) @ e1, (P - c) @ e2]; out = []
    for d in dirs:
        d2 = np.array([d @ e1, d @ e2]); d2 /= np.linalg.norm(d2); ang = np.arctan2(xy[:, 1], xy[:, 0]); a0 = np.arctan2(d2[1], d2[0])
        dd = np.abs(np.angle(np.exp(1j * (ang - a0)))); out.append(P[np.argmin(dd)])
    return out
def loop_frame(P):
    c = P.mean(0); u, s, vt = np.linalg.svd(P - c); return c, vt[2]
# ------------------------------------------------------------------------------------------------ I legs + J feet
NL = 10
def leg(sg):
    s = 'xpos' if sg > 0 else 'xneg'; H, K, A = LM['hip_' + s], LM['knee_' + s], LM['ankle_' + s]
    if sg > 0: r0 = ['P4_%d' % k for k in range(0, 9)] + ['crotch']
    else: r0 = ['P4_%d' % k for k in (0, 15, 14, 13, 12, 11, 10, 9, 8)] + ['crotch']        # same anatomical order: ant-med ... lateral ... post-med, medial
    lat = np.array([sg, 0, 0.0]); ant = np.array([0, 1.0, 0])
    tA = unit(K - H); tB = unit(A - K)
    stations = [('L%d' % (i + 1), H + t * (K - H), tA) for i, t in enumerate((0.16, 0.32, 0.48, 0.63, 0.77))] + \
               [('Kn1', H + 0.90 * (K - H), unit(tA + 0.3 * tB)), ('Kn2', K, unit(tA + tB)), ('Kn3', K + 0.07 * (A - K), unit(0.3 * tA + tB))] + \
               [('S%d' % (i + 1), K + t * (A - K), tB) for i, t in enumerate(np.linspace(0.15, 0.86, 11))]          # ring spacing ~ column width (square coarse quads)
    # ring-0 corner angles around the thigh axis (anterior = 0, towards lateral = +90)
    c1, n1 = stations[0][1], stations[0][2]
    a0 = unit(ant - (ant @ n1) * n1); a9 = unit(lat - (lat @ n1) * n1 - (lat @ a0) * a0)
    P0 = np.array([D.C[D.idx[x]] for x in r0]); ang0 = np.degrees(np.unwrap(np.arctan2((P0 - c1) @ a9, (P0 - c1) @ a0)))
    uni = ang0[0] + np.arange(NL) * 36.0 * np.sign(ang0[3] - ang0[0])
    prev = r0; names = {}
    for i, (nm, c, n) in enumerate(stations):
        blend = min(1.0, 0.35 + 0.12 * i); ang = (1 - blend) * ang0 + blend * uni
        pts, lp = plane_ring(c, n, ang, ant, lat, rad=30)
        cur = []
        for k, p in enumerate(pts): cur.append(D.v('%s_%s_%d' % (nm, s, k), p))
        cur = ['%s_%s_%d' % (nm, s, k) for k in range(NL)]; D.ring_arcs(cur, lp['P'])
        D.band(prev, cur, 'hip' if i == 0 else ('knee' if nm.startswith('Kn') else ('thigh' if nm.startswith('L') else 'shin'))); prev = cur; names[nm] = cur
    D.loops['hip_ring0_' + s] = r0
    return prev, uni, (a0, a9)
LEGEND = {}
for sg in (1, -1): LEGEND[sg] = leg(sg)
# ------------------------------------------------------------------------------------------------ G arms (8-edge shoulder holes on rows T1..T3)
NA = 8
ARM_ANG = [-45, 0, 45, 90, 135, 180, 225, 270]            # from lateral towards posterior: ant-lat, lat, post-lat, post, post-med, med, ant-med, ant
def arm(sg):
    s = 'xpos' if sg > 0 else 'xneg'; c3, c4, c5 = (3, 4, 5) if sg > 0 else (13, 12, 11)
    r0 = ['T1_%d' % c3, 'T1_%d' % c4, 'T1_%d' % c5, 'T2_%d' % c5, 'T3_%d' % c5, 'T3_%d' % c4, 'T3_%d' % c3, 'T2_%d' % c3]
    S, E, Wr = LM['glenohumeral_' + s], LM['elbow_' + s], LM['wrist_' + s]
    lat = np.array([sg, 0, 0.0]); post = np.array([0, -1.0, 0]); tA = unit(E - S); tB = unit(Wr - E)
    st = [('A%d' % i, S + t * (E - S), tA) for i, t in enumerate((0.22, 0.36, 0.50, 0.63, 0.75))] + \
         [('El1', S + 0.87 * (E - S), unit(tA + 0.4 * tB)), ('El2', E, unit(tA + tB)), ('El3', E + 0.12 * (Wr - E), unit(0.4 * tA + tB))] + \
         [('Fa%d' % (i + 1), E + t * (Wr - E), tB) for i, t in enumerate(np.linspace(0.25, 0.86, 6))] + [('Wr', Wr, tB)]
    prev = r0
    c1_, n1_ = st[0][1], st[0][2]; e1 = unit(lat - (lat @ n1_) * n1_); e2 = unit(post - (post @ n1_) * n1_ - (post @ e1) * e1)
    H = np.array([D.C[D.idx[x]] for x in r0]); ha = np.degrees(np.unwrap(np.arctan2((H - c1_) @ e2, (H - c1_) @ e1)))
    if ha[-1] < ha[0]: ha = -ha
    ha = ha[0] + np.cumsum(np.r_[0, np.clip(np.diff(ha), 20, 70)]); ha = ha[0] + (ha - ha[0]) * 315.0 / max(ha[-1] - ha[0], 1e-6)   # monotone, 8 spread fans
    if np.degrees(np.arctan2((H[1] - c1_) @ e2, (H[1] - c1_) @ e1)) * 0 == 0 and (np.unwrap(np.arctan2((H - c1_) @ e2, (H - c1_) @ e1))[-1] - np.unwrap(np.arctan2((H - c1_) @ e2, (H - c1_) @ e1))[0]) < 0: e2 = -e2
    for i, (nm, c, n) in enumerate(st):
        bl = min(1.0, i / 4.0); ang = list((1 - bl) * ha + bl * (ha[0] + np.arange(8) * 45.0))
        pts, lp = plane_ring(c, n, ang, e1, e2 if (e2 @ post) > 0 else e2, rad=20)
        cur = []
        for k, p in enumerate(pts): D.v('%s_%s_%d' % (nm, s, k), p); cur.append('%s_%s_%d' % (nm, s, k))
        D.ring_arcs(cur, lp['P'])
        D.band(prev, cur, 'shoulder' if i == 0 else ('elbow' if nm.startswith('El') else ('upper_arm' if nm.startswith('A') else ('wrist' if nm == 'Wr' else 'forearm')))); prev = cur
    D.loops['shoulder_ring0_' + s] = r0
    return prev
ARMEND = {sg: arm(sg) for sg in (1, -1)}
# ------------------------------------------------------------------------------------------------ digit helpers (H hands, J feet)
def find_tips(region, seed, ntip, minsep=1.5, max_perim2=None):
    d = GEO.geodesic_from(seed, region); sub = np.nonzero(region)[0]; Gs = GEO.G[sub][:, sub].tocoo(); m = d[sub].copy()
    for _ in range(12):
        mm = m.copy(); np.maximum.at(mm, Gs.row, m[Gs.col]); m = mm
    pk = sub[np.nonzero((d[sub] >= m - 1e-9) & np.isfinite(d[sub]))[0]]; pk = pk[np.argsort(-d[pk])]; tips = []
    for p in pk:
        if not all(np.linalg.norm(V[p] - V[q]) > minsep for q in tips): continue
        if max_perim2 is not None:                                                # reject pads / bumps: the 2-cm loop must be finger-sized
            dt = GEO.geodesic_from(np.arange(NV) == p, region); L = [l for l in GEO.iso_loops(dt, 2.0, region & np.isfinite(dt)) if l['closed']]
            if not L or min(GEO.loop_len(l['P']) for l in L) > max_perim2: continue
        tips.append(p)
        if len(tips) == ntip: break
    return tips
def digit_loops(tip, region, step=0.2, dmax=10.0, grow=1.35):
    """iso-loops of the geodesic distance from the tip; base = last level (>= 3.4 cm) before the loop perimeter exceeds grow x the median shaft perimeter (web reached)"""
    dt = GEO.geodesic_from(np.arange(NV) == tip, region); mask = region & np.isfinite(dt); rows = []
    for lev in np.arange(0.4, dmax, step):
        L = [l for l in GEO.iso_loops(dt, lev, mask) if l['closed']]
        if len(L) != 1:
            if lev < 1.5: continue
            break
        per = GEO.loop_len(L[0]['P'])
        ref = [r[1] for r in rows if r[0] >= 2.4]                                  # shaft perimeter (claw / tip loops excluded)
        if lev >= 3.4 and len(ref) >= 4 and per > grow * np.median(ref): break
        rows.append((lev, per, L[0]))
    return dt, mask, rows
def digit_tube(tag, tipv, rows, base_names, d_dir, r_dir, lab, fracs=(0.64, 0.33), angles=(45, 135, 225, 315)):
    """digit rings at fractions of the base distance (geodesic iso-loops), 4 corners [DR, DU, PU, PR] = angles from the radial-dorsal frame;
    the tube starts at base_names (4 corners) and ends with a cap quad (claw tip pinned at its centre)"""
    dbase = rows[-1][0]; prev = base_names; used = {len(rows) - 1}
    print('digit', tag, 'base %.2f cm' % dbase, 'rows', len(rows), flush=True)
    for i, fr in enumerate(fracs):
        lev = fr * dbase; js = np.argsort([abs(r[0] - lev) for r in rows]); j = int([x for x in js if x not in used][0]); used.add(j); P = rows[j][2]['P']; c, n = loop_frame(P)
        if (V[tipv] - c) @ n < 0: n = -n
        pts = loop_ring(rows[j][2], c, n, [0, 90, 180, 270], d_dir, -r_dir)          # 0 dorsal, 90 ulnar, 180 palmar, 270 radial (base frame)
        # 4 corners at 45 / 135 / 225 / 315 = DR? -> use mid-angles
        pts = loop_ring(rows[j][2], c, n, [-45, 45, 135, 225], d_dir, -r_dir)          # DR (dorsal-radial), DU, PU, PR
        cur = []
        for k, p in enumerate(pts): D.v('%s_r%d_%d' % (tag, i + 1, k), p); cur.append('%s_r%d_%d' % (tag, i + 1, k))
        D.ring_arcs(cur, rows[j][2]['P'])
        D.band(prev, cur, lab); prev = cur
    D.q(prev[0], prev[1], prev[2], prev[3], lab + '_cap'); D.pins[tag + '_tip'] = V[tipv]
    for k in range(4): D.h(prev[k], prev[(k + 1) % 4], even=True)
    return prev
def field_base(phi, region, tips, t, lv_top):
    """digit base loop = level loop of the hand / foot field just distal of the saddle where this digit separates (level sets of one field never cross:
    neighbouring base loops and the palm / forefoot ring are disjoint by construction)"""
    from scipy.sparse.csgraph import connected_components
    sub = np.nonzero(region & np.isfinite(phi))[0]; mp = -np.ones(NV, int); mp[sub] = np.arange(len(sub)); Gs = GEO.G[sub][:, sub].tocsr()
    for lv in np.linspace(lv_top, 0.02, 120):
        m = phi[sub] < lv; nc, lab = connected_components(Gs[m][:, m], directed=False); ids = -np.ones(len(sub), int); ids[m] = lab
        mine = ids[mp[t]]
        if mine >= 0 and all(ids[mp[o]] != mine for o in tips if o != t):
            lv = 0.85 * lv; L = [l for l in GEO.iso_loops(phi, lv, region & np.isfinite(phi)) if l['closed']]
            lp = min(L, key=lambda l: np.linalg.norm(l['P'].mean(0) - V[t]) + 0.3 * GEO.loop_len(l['P'])); return lv, lp
    raise RuntimeError('no separate base level')
def base_corners(rows, tipv, d_dir, r_dir):
    P = rows[-1][2]['P']; c, n = loop_frame(P)
    if (V[tipv] - c) @ n < 0: n = -n
    return loop_ring(rows[-1][2], c, n, [-45, 45, 135, 225], d_dir, -r_dir), c, n
def two_to_one(fine, coarse, lab, tag):
    """authored all-quad 2:1 transition (fine ring 2N -> coarse ring N): per 4 fine edges / 2 coarse edges one interior corner x (valence 4)"""
    nf, nc = len(fine), len(coarse); assert nf == 2 * nc and nc % 2 == 0
    for p in range(nc // 2):
        f = [fine[(4 * p + j) % nf] for j in range(5)]; cc = [coarse[(2 * p + j) % nc] for j in range(3)]
        import sa_layout as _LY
        a_, b_ = GEO.snap(D.C[D.idx[f[2]]]), GEO.snap(D.C[D.idx[cc[1]]]); pth = V[_LY.local_path(a_, b_, np.zeros(NV, bool), factor=1.3, margin=1)]
        sl = np.r_[0, np.cumsum(np.linalg.norm(np.diff(pth, axis=0), axis=1))]; x = '%s_x%d' % (tag, p)
        D.v(x, pth[np.searchsorted(sl, 0.5 * sl[-1])])                           # x = midpoint of the surface path (middle fine corner -> middle coarse corner)
        D.q(f[0], f[1], x, cc[0], lab); D.q(f[1], f[2], f[3], x, lab); D.q(f[3], f[4], cc[2], x, lab); D.q(x, cc[2], cc[1], cc[0], lab)
# ------------------------------------------------------------------------------------------------ H hands
def hand(sg):
    s = 'xpos' if sg > 0 else 'xneg'; Wr = LM['wrist_' + s]
    region = np.isin(LAB, ['hand_' + s]) | ((LAB == 'arm_' + s) & (V[:, 2] < 100))
    seed = (V[:, 2] > 99) & (V[:, 2] < 99.6) & region
    tips = find_tips(region, seed, 5); tips = sorted(tips, key=lambda t: -np.linalg.norm(V[t] - Wr))
    fingers = sorted(tips[:4], key=lambda t: -V[t, 1]); thumb = tips[4]                   # finger 1 = most radial (anterior, max f) ... 4 = little
    ax = unit(np.mean(V[fingers], 0) - Wr); dor = unit(np.array([sg, 0, 0.0]) - (np.array([sg, 0, 0.0]) @ ax) * ax); rad = unit(np.cross(ax, dor)); rad = rad if rad[1] > 0 else -rad
    # palm rings: H0 = wrist ring (arm end), H1 = mid palm (plane normal = hand axis), knuckle ring K from the finger base loops
    H0 = ARMEND[sg]; drows = []
    zero = np.zeros(NV, bool)
    for t in list(fingers) + [thumb]: zero |= np.linalg.norm(V - V[t], axis=1) < 0.3
    phh = GEO.harmonic(region, zero, region & ((V - Wr) @ ax < -0.3))
    for i, t in enumerate(fingers):
        dt, mask, rows = digit_loops(t, region); lvb, lpb = field_base(phh, region, list(fingers) + [thumb], t, 0.9)
        db = float(np.mean(dt[GEO.snap(lpb['P'])]))
        if db <= rows[-1][0] + 1.0: rows = [r for r in rows if r[0] < 0.92 * db] + [(db, GEO.loop_len(lpb['P']), lpb)]
        drows.append(rows)                                                         # field base far beyond the geodesic web (digits in contact): geodesic base kept
    bases = [base_corners(rows, t, dor, rad) for rows, t in zip(drows, fingers)]
    K = []
    for i, (pts, c, n) in enumerate(bases):
        for k, nm in enumerate(('DR', 'DU', 'PU', 'PR')): D.v('%s_f%d_%s' % (s, i + 1, nm), pts[k])
        D.ring_arcs(['%s_f%d_%s' % (s, i + 1, nm) for nm in ('DR', 'DU', 'PU', 'PR')], drows[i][-1][2]['P'])
    Kn = []
    for i in range(4): Kn += ['%s_f%d_DR' % (s, i + 1), '%s_f%d_DU' % (s, i + 1)]
    for i in (3, 2, 1, 0): Kn += ['%s_f%d_PU' % (s, i + 1), '%s_f%d_PR' % (s, i + 1)]
    for i in range(3): D.q('%s_f%d_DU' % (s, i + 1), '%s_f%d_DR' % (s, i + 2), '%s_f%d_PR' % (s, i + 2), '%s_f%d_PU' % (s, i + 1), 'finger_web')
    kc = np.mean([b[1] for b in bases], 0); hl = (kc - Wr) @ ax
    # mid-palm ring H1 = level loop of the harmonic hand field (1 proximal of the wrist ring, 0 on the 5 digit-tip disks) whose centroid lies ~55 % wrist -> knuckles
    def palm_ring(name, target):
        best = None
        for lv in np.linspace(0.95, 0.05, 91):
            L = [l for l in GEO.iso_loops(phh, lv, region & np.isfinite(phh)) if l['closed']]
            if not L: continue
            lp = max(L, key=lambda l: GEO.loop_len(l['P'])); fr = (lp['P'].mean(0) - Wr) @ ax / hl
            if best is None or abs(fr - target) < best[0]: best = (abs(fr - target), lp)
        lp = best[1]; c, n = loop_frame(lp['P'])
        if n @ ax < 0: n = -n
        pts = loop_ring(lp, c, n, ARM_ANG, np.array([sg, 0, 0.0]), np.array([0, -1.0, 0])); R_ = []
        for k, p in enumerate(pts): D.v('%s_%s_%d' % (name, s, k), p); R_.append('%s_%s_%d' % (name, s, k))
        D.ring_arcs(R_, lp['P']); return R_
    H0b = palm_ring('H0b', 0.25); H1 = palm_ring('H1', 0.62)
    # thumb hole: the H0-H1 quad nearest the thumb's proximal axis point
    dtt, mtt, trows = digit_loops(thumb, region, dmax=7.0)
    tb = trows[-1][2]['P'].mean(0); cen = [np.mean([D.C[D.idx[H0[k]]], D.C[D.idx[H0[(k + 1) % 8]]], D.C[D.idx[H0b[k]]], D.C[D.idx[H0b[(k + 1) % 8]]]], 0) for k in range(8)]
    kt = int(np.argmin([np.linalg.norm(c - tb) for c in cen]))
    D.band(H0, H0b, 'palm', skip=[kt]); D.band(H0b, H1, 'palm')                    # thumb hole in the proximal palm band (H1 keeps valence <= 6 for the 2:1 row)
    thumb_r0 = [H0[kt], H0[(kt + 1) % 8], H0b[(kt + 1) % 8], H0b[kt]]
    # thumb tube: ring corners matched to the hole order by angle around the thumb axis
    c, n = loop_frame(trows[-1][2]['P'])
    if (V[thumb] - c) @ n < 0: n = -n
    hole = np.array([D.C[D.idx[x]] for x in thumb_r0]); e1 = unit(hole[0] - c - ((hole[0] - c) @ n) * n); e2 = np.cross(n, e1)
    hang = np.degrees(np.unwrap(np.arctan2((hole - c) @ e2, (hole - c) @ e1)))
    sgn = np.sign(np.sum(np.angle(np.exp(1j * np.radians(np.diff(np.r_[hang, hang[0]])))))) or 1.0
    hang = hang[0] + sgn * 90.0 * np.arange(4)                                     # thumb rings: 4 corners at 90 deg, phase / sense of the hole corners
    prev = thumb_r0; dbase = trows[-1][0]
    for i, fr in enumerate((0.64, 0.33)):
        lev = fr * dbase; j = int(np.argmin([abs(r[0] - lev) for r in trows])); lp = trows[j][2]; cj, nj = loop_frame(lp['P'])
        if (V[thumb] - cj) @ nj < 0: nj = -nj
        pts = loop_ring(lp, cj, nj, list(hang), e1, e2); cur = []
        for k, p in enumerate(pts): D.v('%s_th_r%d_%d' % (s, i + 1, k), p); cur.append('%s_th_r%d_%d' % (s, i + 1, k))
        D.ring_arcs(cur, lp['P'])
        D.band(prev, cur, 'thumb'); prev = cur
    D.q(prev[0], prev[1], prev[2], prev[3], 'thumb_cap'); D.pins[s + '_thumb_tip'] = V[thumb]
    for k in range(4): D.h(prev[k], prev[(k + 1) % 4], even=True)
    # fingers
    for i, (t, rows) in enumerate(zip(fingers, drows)):
        digit_tube('%s_f%d' % (s, i + 1), t, rows, ['%s_f%d_%s' % (s, i + 1, x) for x in ('DR', 'DU', 'PU', 'PR')], dor, rad, 'finger')
    # palm -> knuckle ring: 2:1 transition (H1 8 -> K 16), K rotated so that K[0] (f1 DR) sits over H1[0] (dorsal-radial)
    two_to_one(Kn, H1, 'palm', '%s_pt' % s)
    D.loops['knuckle_' + s] = Kn
    return dict(fingers=fingers, thumb=thumb, thumb_quad=kt)
HANDS = {sg: hand(sg) for sg in (1, -1)}
# ------------------------------------------------------------------------------------------------ J feet (harmonic ankle -> forefoot rings, 2:1 to the toe ring)
FOOT_ANG3 = np.array([-60, -30, 0, 30, 60, 100, 140, 180, 220, 260.0])          # forefoot ring: dorsal-medial ... dorsal-lateral, lateral, plantar ..., medial
def foot(sg):
    s = 'xpos' if sg > 0 else 'xneg'; S3, uni, (a0, a9) = LEGEND[sg]
    uS3 = np.mean([D.C[D.idx[x]][2] for x in S3]); region = (np.sign(V[:, 0]) == sg) & (V[:, 2] < uS3 + 1.5) & (np.abs(V[:, 0]) > 8)
    tips = find_tips(region, region & (V[:, 2] > uS3 + 1.0), 5, minsep=2.0, max_perim2=12.0)
    tips = sorted(tips, key=lambda t: sg * V[t, 0])                                      # toe 1 = medial (big toe) ... 5 = lateral
    zero = np.zeros(NV, bool)
    for t in tips: zero |= np.linalg.norm(V - V[t], axis=1) < 0.4
    phi = GEO.harmonic(region, zero, region & (V[:, 2] > uS3 + 0.5))
    lat = np.array([sg, 0, 0.0]); asup = unit(np.array([0, 1.0, 1.0])); prev = S3
    levels = (0.84, 0.72, 0.60, 0.42, 0.25)
    for i, lev in enumerate(levels):
        L = [l for l in GEO.iso_loops(phi, lev, region & np.isfinite(phi)) if l['closed']]; lp = max(L, key=lambda l: GEO.loop_len(l['P']))
        c, n = loop_frame(lp['P'])
        if n[1] + n[2] * 0 < 0 and i > 0: n = -n
        bl = (i + 1) / len(levels); ang = (1 - bl) * uni + bl * FOOT_ANG3
        pts = loop_ring(lp, c, n, list(ang), asup, lat); cur = []
        for k, p in enumerate(pts): D.v('Fd%d_%s_%d' % (i, s, k), p); cur.append('Fd%d_%s_%d' % (i, s, k))
        D.ring_arcs(cur, lp['P'])
        D.band(prev, cur, 'ankle' if i < 3 else 'foot'); prev = cur
    # toes
    up = np.array([0, 0, 1.0]); med = -lat; trows = []; Kn = []
    for i, t in enumerate(tips):
        dt, _, rows = digit_loops(t, region, dmax=11.0); lvb, lpb = field_base(phi, region, tips, t, levels[-1] - 0.02)
        db = float(np.mean(dt[GEO.snap(lpb['P'])])); rows = [r for r in rows if r[0] < 0.92 * db] + [(db, GEO.loop_len(lpb['P']), lpb)]; trows.append(rows)
        pts, c, n = base_corners(rows, t, up, med)
        for k, nm in enumerate(('DM', 'DL', 'PL', 'PM')): D.v('%s_t%d_%s' % (s, i + 1, nm), pts[k])
        D.ring_arcs(['%s_t%d_%s' % (s, i + 1, nm) for nm in ('DM', 'DL', 'PL', 'PM')], rows[-1][2]['P'])
    for i in range(5): Kn += ['%s_t%d_DM' % (s, i + 1), '%s_t%d_DL' % (s, i + 1)]
    for i in (4, 3, 2, 1, 0): Kn += ['%s_t%d_PL' % (s, i + 1), '%s_t%d_PM' % (s, i + 1)]
    for i in range(4): D.q('%s_t%d_DL' % (s, i + 1), '%s_t%d_DM' % (s, i + 2), '%s_t%d_PM' % (s, i + 2), '%s_t%d_PL' % (s, i + 1), 'toe_web')
    for i, (t, rows) in enumerate(zip(tips, trows)):
        digit_tube('%s_t%d' % (s, i + 1), t, rows, ['%s_t%d_%s' % (s, i + 1, x) for x in ('DM', 'DL', 'PL', 'PM')], up, med, 'toe')
    two_to_one(Kn, prev, 'forefoot', '%s_ft' % s)
    D.loops['toe_ring_' + s] = Kn
    return tips
FEET = {sg: foot(sg) for sg in (1, -1)}
# ------------------------------------------------------------------------------------------------ B neck + A head + C display root
GULAR = np.array([0, 8.0, 171.0])                                                 # air point in the throat / jaw angle: picks the ventral midline crossing
def midline_cross(P):
    x = P[:, 0]; i = np.nonzero(np.sign(x) != np.sign(np.roll(x, -1)))[0]; return i
def concavity(P, c, n, k):
    out = np.zeros(len(P))
    for i in range(len(P)):
        m = 0.5 * (P[i - k] + P[(i + k) % len(P)]); o = P[i] - c; o = o - (o @ n) * n; o /= np.linalg.norm(o) + 1e-12; out[i] = (P[i] - m) @ o
    return out
def head():
    region = (V[:, 2] >= 163.0) & (np.abs(V[:, 0]) < 18)
    tip = LM['rostrum_tip']; zero = region & (np.linalg.norm(V - tip, axis=1) < 0.5); one = region & (V[:, 2] < 164.3)
    phi = GEO.harmonic(region, zero, one); mask = region & np.isfinite(phi)
    def ring_loop(lev):
        L = [l for l in GEO.iso_loops(phi, lev, mask) if l['closed']]; return max(L, key=lambda l: GEO.loop_len(l['P']))
    # midline arcs vs phi
    levs = np.linspace(0.97, 0.03, 95); dors = []; vent = []; per = []
    for lv in levs:
        P = ring_loop(lv)['P']; ix = midline_cross(P); pts = P[ix]; dv = np.linalg.norm(pts - GULAR, axis=1)
        vent.append(pts[np.argmin(dv)]); dors.append(pts[np.argmax(dv)]); per.append(GEO.loop_len(P))
    dors = np.array(dors); vent = np.array(vent); s = np.r_[0, np.cumsum(0.5 * (np.linalg.norm(np.diff(dors, axis=0), axis=1) + np.linalg.norm(np.diff(vent, axis=0), axis=1)))]
    per = np.array(per)
    pm = 0.5 * (phi[GEO.snap(LM['mouth_corner_xpos'])] + phi[GEO.snap(LM['mouth_corner_xneg'])])
    eye_bot = {sg: GEO.snap(GEO.V[GEO.KD.query(LM['eye_' + ('xpos' if sg > 0 else 'xneg')])[1]]) for sg in (1, -1)}
    pe = 0.5 * (phi[eye_bot[1]] + phi[eye_bot[-1]])
    pc = float(levs[np.argmin(np.abs(per - 15.0) + 100 * (levs > pm))])          # front cap ring: perimeter ~15 cm, ahead of the mouth corner
    # ring levels: arc spacing 3.2 cm on the neck (mean midline arc), 2.3 cm on the head; mouth-corner and eye levels exact
    sm = np.interp(pm, levs[::-1], s[::-1]); se = np.interp(pe, levs[::-1], s[::-1]); sc = np.interp(pc, levs[::-1], s[::-1])
    tg = [1.6]
    while tg[-1] < sc - 1.0: tg.append(tg[-1] + (3.2 if tg[-1] < 12 else 2.3))
    tg = np.array(tg[:-1])
    for fixed in (sm, se): tg[np.argmin(np.abs(tg - fixed))] = fixed
    tg = np.r_[np.sort(tg), sc]; lv_ring = np.interp(tg, s, levs)
    ie = int(np.argmin(np.abs(tg - se))); im = int(np.argmin(np.abs(tg - sm))); nr = len(tg)
    print('head rings', nr, 'eye ring', ie, 'mouth ring', im, 'levels', np.round(lv_ring, 3), flush=True)
    prev = rings['T0']; names = []
    for r, lv in enumerate(lv_ring):
        lp = ring_loop(lv); P = lp['P']; c, n = loop_frame(P); ix = midline_cross(P); dv = np.linalg.norm(P[ix] - GULAR, axis=1)
        iv, idr = ix[np.argmin(dv)], ix[np.argmax(dv)]
        # direction: from the ventral crossing towards +x first
        step = 1 if P[(iv + 3) % len(P), 0] > 0 else -1
        Q = np.roll(P, -iv, 0)
        if step < 0: Q = np.vstack([Q[:1], Q[1:][::-1]])
        jd = int(np.argmin(np.linalg.norm(Q - P[idr], axis=1))); left = Q[:jd + 1]; right = np.vstack([Q[jd:], Q[:1]])
        def arcpts(A, fr):
            sl = np.r_[0, np.cumsum(np.linalg.norm(np.diff(A, axis=0), axis=1))]; sl /= sl[-1]; return [A[min(np.searchsorted(sl, t), len(A) - 1)] for t in fr]
        def side_cols(A, mouth):
            if not mouth: return arcpts(A, np.arange(9) / 8.0)
            k = max(2, int(0.4 / max(GEO.loop_len(P) / len(P), 1e-3)))
            cv = concavity(A, c, n, k); win = (A[:, 2] > 174.5) & (A[:, 2] < 179.8); win[:3] = False; win[-3:] = False
            j = int(np.argmin(np.where(win, cv, 9))); sl = np.r_[0, np.cumsum(np.linalg.norm(np.diff(A, axis=0), axis=1))]; t = sl[j] / sl[-1]
            return arcpts(A, list(np.linspace(0, t, 5)) + list(np.linspace(t, 1, 5))[1:])
        mouth = r >= im
        L9 = side_cols(left, mouth); R9 = side_cols(right[::-1], mouth)[::-1]       # right half measured from the ventral crossing too
        pts = L9[:8] + R9[::-1][:8][::-1] if False else L9[:8] + [R9[::-1][k] for k in range(8, 0, -1)]
        cur = []
        for k in range(16): D.v('Hd%d_%d' % (r, k), pts[k]); cur.append('Hd%d_%d' % (r, k))
        D.ring_arcs(cur, P)
        names.append(cur)
    # eyes: hole corners = 8 points of the orbit rim loop; orbit rings = geodesic iso-loops from the eye-pit floor
    holes = {}
    for sg in (1, -1):
        s_ = 'xpos' if sg > 0 else 'xneg'; bot = eye_bot[sg]
        cand = range(5, 8) if sg > 0 else range(9, 12); cc_ = min(cand, key=lambda k: np.linalg.norm(D.C[D.idx[names[ie][k]]] - V[bot]))
        cols = [cc_ - 1, cc_, cc_ + 1] if sg > 0 else [cc_ + 1, cc_, cc_ - 1]
        sub = region & (np.linalg.norm(V - V[bot], axis=1) < 4.0); dg = GEO.geodesic_from(np.arange(NV) == bot, sub)
        hole_names = [names[ie - 1][cols[0]], names[ie - 1][cols[1]], names[ie - 1][cols[2]], names[ie][cols[2]], names[ie + 1][cols[2]], names[ie + 1][cols[1]], names[ie + 1][cols[0]], names[ie][cols[0]]]
        ax = unit(GEO.VN[bot] * 0 + np.mean(GEO.VN[GEO.KD.query_ball_point(V[bot], 2.5)], 0))
        e1 = unit(np.cross(ax, [0, 0, 1.0])); e2 = np.cross(ax, e1)
        dflt = np.array([D.C[D.idx[h]] for h in hole_names]); ang = np.degrees(np.unwrap(np.arctan2((dflt - V[bot]) @ e2, (dflt - V[bot]) @ e1)))
        if not (np.all(np.diff(ang) > 0) or np.all(np.diff(ang) < 0)): print('WARNING eye hole default order not monotonic', s_, np.round(ang), flush=True)
        def rim(d):
            L = [l for l in GEO.iso_loops(dg, d, sub & np.isfinite(dg)) if l['closed']]; return max(L, key=lambda l: GEO.loop_len(l['P']))
        if ang[-1] < ang[0]: ang = -ang; e2 = -e2
        ang = ang[0] + np.arange(8) * 45.0; esg = e2                               # orbit rings: 45 deg fans phased on the hole corner 0 (hole = the head-ring corners)
        D.v('%s_eye_c' % s_, V[bot]); D.pins['eye_floor_' + s_] = V[bot]
        prev = hole_names
        for i, d in enumerate((1.8, 0.9)):
            lp = rim(d); P = lp['P']; cur = []; pts = arc_place(P, V[bot], ax, list(ang), e1, esg)
            for k in range(8): nm = '%s_orb%d_%d' % (s_, i, k); D.v(nm, pts[k]); cur.append(nm)
            D.ring_arcs(cur, P)
            D.band(prev, cur, 'orbit'); prev = cur
        cn = '%s_eye_c' % s_
        D.q(prev[0], prev[1], prev[2], cn, 'eye'); D.q(prev[2], prev[3], prev[4], cn, 'eye'); D.q(prev[4], prev[5], prev[6], cn, 'eye'); D.q(prev[6], prev[7], prev[0], cn, 'eye')
        holes[sg] = (ie, cols); D.loops['orbit_rim_' + s_] = hole_names
    # bands: T0 -> ring 0 -> ... (skipping the eye-hole quads)
    allr = [rings['T0']] + names
    for r in range(len(allr) - 1):
        skip = []
        for sg, (ie_, cols) in holes.items():
            if r in (ie_, ie_ + 1):                                                 # bands Hd(ie-1)-Hd(ie) and Hd(ie)-Hd(ie+1) are allr index ie, ie+1
                skip += [min(cols), min(cols) + 1]
        lab = 'neck' if np.mean([D.C[D.idx[x]][2] for x in allr[r + 1]]) < 172.5 and r < len(allr) - 6 else 'head'
        D.band(allr[r], allr[r + 1], lab, skip=skip)
    # front cap (6 x 2): top row cols 5..11, bottom row cols 13..3, middle row = the lip crease across the snout front (mouth slit)
    last = names[-1]; Lp = D.C[D.idx[last[4]]]; Rp = D.C[D.idx[last[12]]]; capmask = mask & (phi < lv_ring[-1])
    import sa_layout as _LY
    pth = V[_LY.local_path(GEO.snap(Lp), GEO.snap(Rp), np.zeros(NV, bool), factor=1.3, margin=1)]          # lip line across the snout front (col 4 -> col 12)
    sl = np.r_[0, np.cumsum(np.linalg.norm(np.diff(pth, axis=0), axis=1))]
    for j in range(1, 6): D.v('mouth_m%d' % j, pth[np.searchsorted(sl, sl[-1] * j / 6.0)])
    top = [last[k] for k in range(5, 12)]; mid = [last[4]] + ['mouth_m%d' % j for j in range(1, 6)] + [last[12]]; bot = [last[k % 16] for k in (3, 2, 1, 0, 15, 14, 13)]
    for j in range(6): D.q(mid[j], mid[j + 1], top[j + 1], top[j], 'rostrum_cap'); D.q(bot[j], bot[j + 1], mid[j + 1], mid[j], 'rostrum_cap')
    D.pins['rostrum_tip'] = LM['rostrum_tip']
    D.loops['mouth_slit'] = [names[r][4] for r in range(im, len(names))] + mid[1:-1] + [names[r][12] for r in range(len(names) - 1, im - 1, -1)]
    D.head = dict(nr=nr, ie=ie, im=im, levels=lv_ring.tolist())
head()
# ------------------------------------------------------------------------------------------------ semantic relabel: display root (posterior skull top)
for qi, q in enumerate(D.Q):
    cc = np.mean([D.C[i] for i in q], 0)
    if D.qlab[qi] == 'head' and cc[1] < -1.0 and cc[2] > 180.5: D.qlab[qi] = 'display_root'
# ------------------------------------------------------------------------------------------------ compaction (corners used by no quad: hole interiors) + orientation
used = sorted({i for q in D.Q for i in q}); remap = {o: n for n, o in enumerate(used)}
D.C = [D.C[i] for i in used]; D.name = [D.name[i] for i in used]; D.idx = {nm: i for i, nm in enumerate(D.name)}; D.Q = [[remap[i] for i in q] for q in D.Q]
D.hint = {(min(remap[a], remap[b]), max(remap[a], remap[b])): v for (a, b), v in D.hint.items() if a in remap and b in remap}
D.fixed = {(min(remap[a], remap[b]), max(remap[a], remap[b])): v for (a, b), v in D.fixed.items()}
ARCS = {}
for (a, b), P in D.arcs.items():
    if a in D.idx and b in D.idx and np.linalg.norm(P[0] - D.C[D.idx[a]]) < 0.3 and np.linalg.norm(P[-1] - D.C[D.idx[b]]) < 0.3:
        ia, ib = D.idx[a], D.idx[b]; ARCS[(min(ia, ib), max(ia, ib))] = P if ia < ib else P[::-1]
D.arcs = ARCS
def orient():
    Q = [list(q) for q in D.Q]; nq = len(Q); emap = {}
    for qi, q in enumerate(Q):
        for k in range(4): emap.setdefault((min(q[k], q[(k + 1) % 4]), max(q[k], q[(k + 1) % 4])), []).append(qi)
    seen = np.zeros(nq, bool); flips = 0
    def dirs(q): return {(q[k], q[(k + 1) % 4]) for k in range(4)}
    for s0 in range(nq):
        if seen[s0]: continue
        seen[s0] = True; st = [s0]
        while st:
            a = st.pop(); da = dirs(Q[a])
            for k in range(4):
                e = (min(Q[a][k], Q[a][(k + 1) % 4]), max(Q[a][k], Q[a][(k + 1) % 4]))
                for b in emap[e]:
                    if b == a or seen[b]: continue
                    if dirs(Q[b]) & da: Q[b] = Q[b][::-1]; flips += 1
                    seen[b] = True; st.append(b)
    # outward: compare with the source normals at the corners
    C = np.array(D.C); sgn = 0
    for q in Q:
        p = C[q]; nrm = np.cross(p[2] - p[0], p[3] - p[1]); vn = GEO.VN[GEO.snap(p.mean(0))]; sgn += np.sign(nrm @ vn)
    if sgn < 0: Q = [q[::-1] for q in Q]
    D.Q = Q; print('orientation: flips', flips, 'outward score', sgn, '/', len(Q), flush=True)
orient()
