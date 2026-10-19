"""RP1E hand sub-cage DESIGN (prep only; the cage is authored by hand in the Blender UI from these numbers).
Palm: wrist ring W0 (existing 10-vertex cage loop, kept), palm rings P1,P2,P3 (10 verts each: dorsal row d0..d4 radial->ulnar,
palmar row p0..p4), P3 capped by 4 quads (index, middle, ring, pinky bases); thumb extruded from the palmar radial quad between
P1 and P2. Digit tubes: 4-vertex rings at selected stations (inset fraction k of the measured half extents).
Writes design_S.json (Blender frame, cm)."""
import numpy as np, sys, json
s = sys.argv[1]; P = json.loads(sys.argv[2])
dg = json.load(open('/home/claude/stc/rp1e/digits_%s.json' % s))
w = np.load('/home/claude/stc/rp1/weld.npz'); V = w['V'].astype(float); F = w['F'].astype(np.int64)
seg = np.load('/home/claude/stc/rp1e/segH_%s.npz' % s); used = seg['used']; lab = seg['lab']
lab_full = -np.ones(len(V), int); lab_full[used] = lab
hand = lab_full >= 0
dors = np.array(P['dorsal'], float)
def section(z0, keep_palm=True):
    Fm = F[hand[F].all(1)]; d = V[:, 2] - z0
    T = Fm[(np.sign(d[Fm]).min(1) < 0) & (np.sign(d[Fm]).max(1) > 0)]
    segs = []; labs = []
    for t in T:
        pts = []
        for i, j in ((0, 1), (1, 2), (2, 0)):
            if d[t[i]] * d[t[j]] < 0: u = d[t[i]] / (d[t[i]] - d[t[j]]); pts.append(V[t[i]] + (V[t[j]] - V[t[i]]) * u)
        if len(pts) == 2: segs.append(pts); labs.append(lab_full[t].max())
    return np.array(segs), np.array(labs)
def loops_of(S):
    # chain section segments into loops by endpoint proximity
    from scipy.spatial import cKDTree
    n = len(S); P0 = S[:, 0]; P1 = S[:, 1]; T = cKDTree(np.vstack([P0, P1]))
    used = np.zeros(n, bool); loops = []
    for st in range(n):
        if used[st]: continue
        used[st] = True; lp = [st]; cur = P1[st]; guard = 0
        while guard < n:
            guard += 1
            cand = [j % n for j in T.query_ball_point(cur, 1e-4) if not used[j % n]]
            if not cand: break
            j = cand[0]; used[j] = True; lp.append(j); cur = P1[j] if np.linalg.norm(P0[j] - cur) < 1e-4 else P0[j]
        loops.append(lp)
    return loops
def palm_points(z0, uu, ew, et, inset, exclude, O, frac):
    S, Ls = section(z0)
    loops = loops_of(S); per = [np.linalg.norm(S[l, 1] - S[l, 0], axis=1).sum() for l in loops]
    big = loops[int(np.argmax(per))]; M = S[big].mean(1)
    c = O.copy(); c[2] = z0; U = (M - c) @ ew; T = (M - c) @ et
    lo_, hi_ = np.percentile(U, 0.5), np.percentile(U, 99.5)
    if frac is not None: uu = lo_ + frac * (hi_ - lo_)
    uu = np.clip(uu, lo_ + 0.9, hi_ - 0.9)
    out_d, out_p = [], []
    for u in uu:
        sel = np.abs(U - u) < 0.5
        if sel.sum() < 2: sel = np.argsort(np.abs(U - u))[:4]
        tmax, tmin = T[sel].max(), T[sel].min(); mid = 0.5 * (tmax + tmin); hw = 0.5 * (tmax - tmin)
        base = c + u * ew; base[2] = z0
        out_d.append(base + (mid + inset * hw) * et); out_p.append(base + (mid - inset * hw) * et)
    return np.array(out_d), np.array(out_p), c
def secring(labk, c, t, ew, et, R=3.2):
    t = t / np.linalg.norm(t); m = lab_full == labk
    Fk = F[m[F].all(1)]; d = (V - c) @ t
    Fk = Fk[(np.sign(d[Fk]).min(1) < 0) & (np.sign(d[Fk]).max(1) > 0)]
    pts = []; wts = []
    for f in Fk:
        q = []
        for i_, j_ in ((0, 1), (1, 2), (2, 0)):
            if d[f[i_]] * d[f[j_]] < 0: u = d[f[i_]] / (d[f[i_]] - d[f[j_]]); q.append(V[f[i_]] + (V[f[j_]] - V[f[i_]]) * u)
        if len(q) == 2 and np.linalg.norm((q[0] + q[1]) / 2 - c) < R: pts.append((q[0] + q[1]) / 2); wts.append(np.linalg.norm(q[0] - q[1]))
    if len(pts) < 10: return None
    Pp = np.array(pts); w_ = np.array(wts)
    e1 = ew - (ew @ t) * t; e1 /= np.linalg.norm(e1); e2 = np.cross(t, e1)
    X2 = np.c_[(Pp - c) @ e1, (Pp - c) @ e2]; mu = (X2 * w_[:, None]).sum(0) / w_.sum()
    Cv = np.cov((X2 - mu).T, aweights=w_); ev, evec = np.linalg.eigh(Cv)
    ax = evec[:, np.argmax(np.abs(evec[0]))]          # principal axis closest to e1
    if ax[0] < 0: ax = -ax
    ang = np.degrees(np.arctan2(ax[1], ax[0])); aniso = ev.max() / max(ev.min(), 1e-9)
    if aniso < 1.3: ang = 0.0
    ang = float(np.clip(ang, -20, 20)); ax = np.array([np.cos(np.radians(ang)), np.sin(np.radians(ang))])
    ew_ = ax[0] * e1 + ax[1] * e2; ew_ /= np.linalg.norm(ew_); et_ = np.cross(t, ew_)
    if et_ @ et < 0: et_ = -et_
    U = (Pp - c) @ ew_; W = (Pp - c) @ et_
    cc = c + 0.5 * (U.max() + U.min()) * ew_ + 0.5 * (W.max() + W.min()) * et_
    return cc, ew_, et_, 0.5 * (U.max() - U.min()), 0.5 * (W.max() - W.min())
order = P['finger_order']          # radial -> ulnar
# finger tubes
tubes = {}
for role in order + ['thumb']:
    d = dg[role]; C = np.array(d['c']); EW = np.array(d['ew']); ET = np.array(d['et']); A = np.array(d['a']); B = np.array(d['b']); S_ = np.array(d['s'])
    picks = P['stations'][role]
    rings = []
    for pr in P.get('pre_rings', {}).get(role, []):
        t_ = np.array(pr['t'], float); t_ /= np.linalg.norm(t_); et_ = ET[0] - (ET[0] @ t_) * t_; et_ /= np.linalg.norm(et_); ew_ = np.cross(t_, et_); ew_ *= np.sign(ew_ @ EW[0])
        cc = np.array(pr['c']); a = pr['a'] * P['k']; b = pr['b'] * P['k']
        rings.append([cc - a * ew_ + b * et_, cc + a * ew_ + b * et_, cc + a * ew_ - b * et_, cc - a * ew_ - b * et_])
    if role == 'thumb' and P.get('thumb_extend'):
        T0 = np.array(d['t'][0]); cx = C[0] - P['thumb_extend'] * T0; a = A[0] * P['k'] * 1.05; b = B[0] * P['k'] * 1.05
        rings.append([cx - a * EW[0] + b * ET[0], cx + a * EW[0] + b * ET[0], cx + a * EW[0] - b * ET[0], cx - a * EW[0] - b * ET[0]])
    for i in picks:
        if isinstance(i, dict):
            j = i['frame']; cc = np.array(i['c']); a = i['a'] * P['k']; b = i['b'] * P['k']
            et_ = ET[j]; t_ = np.array(i['t']) if 't' in i else np.array(d['t'][j]); t_ = t_ / np.linalg.norm(t_)
            et_ = et_ - (et_ @ t_) * t_; et_ /= np.linalg.norm(et_); ew_ = np.cross(t_, et_); ew_ *= np.sign(ew_ @ EW[j])
            rings.append([cc - a * ew_ + b * et_, cc + a * ew_ + b * et_, cc + a * ew_ - b * et_, cc - a * ew_ - b * et_]); continue
        a = max(A[i] * P['k'], 0.35); b = max(B[i] * P['k'], 0.35)
        kk = P.get('k_' + role, P['k'])
        if P.get('secfit', 1):
            fit_ = secring(d['label'], C[i], np.array(d['t'][i]), EW[i], ET[i])
            if fit_ is not None:
                cc, ew_, et_, a0, b0 = fit_; a = max(a0 * P.get('ka_' + role, P.get('ka', kk)), 0.35); b = max(b0 * kk, 0.35)
                rings.append([cc - a * ew_ + b * et_, cc + a * ew_ + b * et_, cc + a * ew_ - b * et_, cc - a * ew_ - b * et_]); continue
        # ring order: dorsal-radial, dorsal-ulnar, palmar-ulnar, palmar-radial ; ew points radial->ulnar (sign fixed below)
        rings.append([C[i] - a * EW[i] + b * ET[i], C[i] + a * EW[i] + b * ET[i], C[i] + a * EW[i] - b * ET[i], C[i] - a * EW[i] - b * ET[i]])
    if P.get('tip_ring', 1):
        lab_k = d['label']; Xd = V[used[lab == lab_k]]
        R4 = np.array(rings[-1]); cl = R4.mean(0); tl = cl - np.array(rings[-2]).mean(0); tl /= np.linalg.norm(tl)
        proj = (Xd - cl) @ tl; tipp = Xd[np.argmax(proj)]; tc = cl + (proj.max() - P.get('tip_inset', 0.45)) * tl
        if (tc - cl) @ tl > 0.5:
            sc_ = P.get('tip_scale', 0.55); rings.append(list(tc + sc_ * (R4 - cl)))
    tubes[role] = np.array(rings)
# width axis across the knuckles: from index base to pinky base
c0 = np.array([np.array(dg[r]['c'][0]) for r in order])
ew = c0[-1] - c0[0]; ew[2] = 0; ew /= np.linalg.norm(ew)
et = dors - (dors @ ew) * ew; et[2] = 0; et /= np.linalg.norm(et)
# make tube ew consistent (radial->ulnar = +ew): flip rings if needed
for role in tubes:
    R = tubes[role]
    if (R[0, 1] - R[0, 0]) @ ew < 0 and role != 'thumb': tubes[role] = R[:, [1, 0, 3, 2]]
# P3 vertex u positions = finger boundaries
pc = np.array([(c0[i] - c0.mean(0)) @ ew for i in range(4)])
bnd = [pc[0] - (pc[1] - pc[0]) * 0.55, (pc[0] + pc[1]) / 2, (pc[1] + pc[2]) / 2, (pc[2] + pc[3]) / 2, pc[3] + (pc[3] - pc[2]) * 0.55]
rings = {}
for nm, z0, scale in P['palm_rings']:
    O = c0.mean(0)
    if nm == P['palm_rings'][-1][0]: uu, frac = np.array(bnd), None
    else:
        frac = np.array(scale)
        uu = None
    dd, pp, c = palm_points(z0, uu, ew, et, P['palm_inset'], P['exclude'][nm], O, frac)
    if nm == P['palm_rings'][-1][0] and P.get('p3_web_z'):
        for k_, zz in zip((1, 2, 3), P['p3_web_z']):
            dd[k_][2] = zz; pp[k_][2] = zz
    for key, val in P.get('palm_override', {}).get(nm, {}).items():
        (dd if key[0] == 'd' else pp)[int(key[1])] = np.array(val)
    rings[nm] = dict(d=dd.round(3).tolist(), p=pp.round(3).tolist())
json.dump(dict(ring_names=[r[0] for r in P['palm_rings']], crotch=P.get('crotch', {}), thumb_between=P.get('thumb_between', ['P1', 'P2']), rings=rings, tubes={k: v.round(3).tolist() for k, v in tubes.items()}, ew=ew.tolist(), et=et.tolist()),
          open('/home/claude/stc/rp1e/design_%s.json' % s, 'w'), indent=0)
print('bnd', np.round(bnd, 2))
for nm in rings: print(nm, 'd', np.round(rings[nm]['d'], 1).tolist())
