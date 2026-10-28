# fenn_hidden_ear.py WORK OUT.json : order 57dc328 §8 HIDDEN-EAR identity gate (body + face). All bodies are MPFB hm08 realizations (shared
# vertex order), at matched stature (~181 cm), matched frame / muscle / fat / age, R-6 neutral stance, no clothing / hair; the external ear
# (hm08 w_ears > 0.05) is EXCLUDED from every metric and harmonically collapsed onto the skull for the renders (written as *_earhidden.npz).
#  Body: per body-region correspondence RMS of Fenn vs Marchfolk / Sagekin against the human-human baseline (Sagekin vs Marchfolk).
#  Face: per facial region (cranium vault, forehead, orbit / eye region, nose, cheeks / mid-face, mouth, jaw / chin) after a similarity
#  (scale-removing) alignment of each head onto the Fenn head on all non-ear head vertices; plus canon-direction descriptors (FENN_V1 §2-7).
import sys, os, json, numpy as np, scipy.sparse as sp
W, OUT = sys.argv[1:3]; RA = '/home/claude/wayfarer-design/reviews/reference-assets/r6'; PA = W + '/partA'
_fe = lambda k, d: tuple(os.environ[k].split(':')) if k in os.environ else d    # order 6d2eadc: FN_HE_C1 / FN_HE_C2 = ID:R6 (final consolidation re-run on the CF2 sources)
CFG = {'c1': dict(FN=_fe('FN_HE_C1', ('FNL4', RA + '/FNL4_r6.npz')), MF=('MFM181', PA + '/cmp/MFM181_r6.npz'), SG=('SGM181', PA + '/cmp/SGM181_r6.npz')),
       'c2': dict(FN=_fe('FN_HE_C2', ('FNF181', PA + '/build/FNF181_r6.npz')), MF=('MFF181', PA + '/cmp/MFF181_r6.npz'), SG=('SGF181', PA + '/cmp/SGF181_r6.npz'))}
nz = np.load(W + '/src/FNL4_native.npz'); si = nz['src_index']; Q = np.asarray(nz['Q']); nV = len(si); bones = [str(b) for b in nz['bones']]
A = sp.coo_matrix((np.ones(4 * len(Q)), (np.repeat(Q[:, :4].ravel(), 1), np.roll(Q, -1, 1).ravel())), shape=(nV, nV)).tocsr(); A = ((A + A.T) > 0).astype(float)
def load(p):
    z = np.load(p); return dict(V=z['V'][si].astype(float), we=z['w_ears'][si], wh=z['w_head'][si], eye=(np.array(z['eye_l'], float), np.array(z['eye_r'], float)))
def collapse_ears(V, ear):
    X = V.copy(); deg = np.asarray(A.sum(1)).ravel()
    for _ in range(400): X[ear] = (A @ X)[ear] / deg[ear, None]
    return X
def procrustes(Xs, Xt):                                   # similarity map of Xs onto Xt
    ms, mt = Xs.mean(0), Xt.mean(0); a, b = Xs - ms, Xt - mt; U, S, Vt = np.linalg.svd(a.T @ b); d = np.sign(np.linalg.det(U @ Vt)); D = np.diag([1, 1, d])
    R = U @ D @ Vt; s = (S * np.diag(D)).sum() / (a * a).sum(); return lambda X: s * (X - ms) @ R + mt, s
# body regions from the dominant native skin bone (shared topology)
dom = np.array(bones)[np.asarray(nz['W']).argmax(1)]
def breg(b):
    if b.startswith(('upperarm', 'lowerarm')): return 'arm'
    if b.startswith(('hand', 'index', 'middle', 'ring', 'pinky', 'thumb')): return 'hand'
    if b.startswith(('thigh', 'calf')): return 'leg'
    if b.startswith(('foot', 'ball')): return 'foot'
    if b.startswith(('spine', 'pelvis', 'clavicle', 'Root')): return 'trunk'
    if b.startswith('neck'): return 'neck'
    return 'head'
BREG = np.array([breg(b) for b in dom])
res = dict(note='ears excluded (hm08 w_ears > 0.05) from every metric', configs={})
for cfg, B in CFG.items():
    D = {k: load(p) for k, (n, p) in B.items()}; ear = D['FN']['we'] > 0.05; head = (D['FN']['wh'] > 0.5) & ~ear
    for k, (n, p) in B.items():
        np.savez('%s/%s_earhidden.npz' % (os.environ.get('FN_HE_OV', W + '/ov'), n), V=collapse_ears(D[k]['V'], ear), Q=Q)
    # ---- body
    body = {}
    for r in ('trunk', 'arm', 'hand', 'leg', 'foot', 'neck'):
        m = (BREG == r) & ~ear
        rms = lambda a, b: float(np.sqrt((np.linalg.norm(D[a]['V'][m] - D[b]['V'][m], axis=1) ** 2).mean()) * 10)
        fm, fs, sm = rms('FN', 'MF'), rms('FN', 'SG'), rms('SG', 'MF')
        body[r] = dict(FN_vs_MF_rms_mm=round(fm, 2), FN_vs_SG_rms_mm=round(fs, 2), SG_vs_MF_rms_mm_human_baseline=round(sm, 2), ratio_FNMF_over_human=round(fm / sm, 2), ratio_FNSG_over_human=round(fs / sm, 2))
    # ---- face: regions on the Fenn template geometry
    Vf = D['FN']['V']; el, er = D['FN']['eye']; E = 0.5 * (el + er); hv = np.nonzero(head)[0]; P = Vf - E
    me_z = Vf[hv][(np.abs(P[hv, 0]) < 2) & (P[hv, 1] > 0)][:, 2].min(); top_z = Vf[hv][:, 2].max(); HH = top_z - me_z
    orbit = head & ((np.linalg.norm(Vf - el, axis=1) < 2.3) | (np.linalg.norm(Vf - er, axis=1) < 2.3)) & (P[:, 1] > -1.5)
    fore = head & ~orbit & (P[:, 2] > 1.2) & (P[:, 2] < 6.0) & (P[:, 1] > -2.5) & (np.abs(P[:, 0]) < 5.5)
    nose = head & ~orbit & (np.abs(P[:, 0]) < 1.7) & (P[:, 2] > -5.0) & (P[:, 2] < 0.5) & (P[:, 1] > 0.3)
    cheek = head & ~orbit & ~nose & (np.abs(P[:, 0]) > 1.7) & (np.abs(P[:, 0]) < 6.5) & (P[:, 2] > -5.0) & (P[:, 2] < -1.0) & (P[:, 1] > -3.0)
    mouth = head & (np.abs(P[:, 0]) < 3.0) & (P[:, 2] > -7.5) & (P[:, 2] <= -5.0) & (P[:, 1] > -1.5)
    jaw = head & ~mouth & (P[:, 2] <= -5.0) & (P[:, 1] > -7.0)
    vault = head & ~fore & ~orbit & (P[:, 2] > 1.2)
    REG = dict(cranium_vault=vault, forehead=fore, orbit_eye_region=orbit, nose=nose, cheeks_midface=cheek, mouth=mouth, jaw_chin=jaw)
    face = {}; maps = {}
    for k in ('MF', 'SG'):
        f, s = procrustes(D[k]['V'][head], Vf[head]); maps[k] = (f, s)
    fsm, _ = procrustes(D['SG']['V'][head], D['MF']['V'][head])
    for r, m in REG.items():
        rm = lambda X, Y: float(np.sqrt((np.linalg.norm(X[m] - Y[m], axis=1) ** 2).mean()) * 10)
        fm = rm(Vf, maps['MF'][0](D['MF']['V'])); fs = rm(Vf, maps['SG'][0](D['SG']['V'])); sm = rm(D['MF']['V'], fsm(D['SG']['V']))
        face[r] = dict(verts=int(m.sum()), FN_vs_MF_rms_mm=round(fm, 2), FN_vs_SG_rms_mm=round(fs, 2), SG_vs_MF_rms_mm_human_baseline=round(sm, 2), ratio_FNMF_over_human=round(fm / max(sm, 1e-3), 2),
                       FN_vs_MF_pct_HH=round(fm / 10 / HH * 100, 2), departure_material=bool(fm > 2 * sm and fm / 10 / HH * 100 > 0.5))
    # per-vertex FN-vs-MF residual for the heat sheet
    np.save('%s/ov/%s_face_resid_vs_MF.npy' % (W, B['FN'][0]), np.linalg.norm(Vf - maps['MF'][0](D['MF']['V']), axis=1) * 10)
    # ---- canon descriptors (each body in its own geometry; ears excluded)
    def desc(X, eyes):
        e = 0.5 * (eyes[0] + eyes[1]); Px = X - e; h = hv
        mez = X[h][(np.abs(Px[h, 0]) < 2) & (Px[h, 1] > 0)][:, 2].min(); tz = X[h][:, 2].max(); hh = tz - mez
        def width(z0, z1, fmin=-3):
            sel = h[(Px[h, 2] > z0) & (Px[h, 2] < z1) & (Px[h, 1] > fmin)]; return float(2 * np.abs(Px[sel, 0]).max()) if len(sel) else np.nan
        zy = width(-2.5, -0.5); jaw_w = width(mez - e[2] + 1.5, mez - e[2] + 3.0, -6); low = width(-7.0, -5.0, -4); skull = width(1.0, 6.0, -12)
        mid = h[(Px[h, 2] > -5) & (Px[h, 2] < 0) & (np.abs(Px[h, 0]) > 3) & (Px[h, 1] > -3)]; cz = float(Px[mid[np.argmax(np.abs(Px[mid, 0]))], 2]) if len(mid) else np.nan
        ml = h[(np.abs(Px[h, 0]) < 0.3) & (Px[h, 2] > 0.5) & (Px[h, 1] > -9)]; o = ml[np.argsort(Px[ml, 2])]; prof = Px[o][:, [1, 2]]
        curv = float(np.abs(np.diff(np.arctan2(np.diff(prof[:, 0]), np.diff(prof[:, 1])))).mean()) if len(o) > 5 else np.nan
        return dict(cranial_height_over_face=(tz - e[2]) / (e[2] - mez), skull_breadth_over_HH=skull / hh, lower_face_width_over_bizygomatic=low / zy, jaw_width_over_bizygomatic=jaw_w / zy,
                    cheekbone_height_over_HH=cz / hh, forehead_profile_mean_turn_rad=curv, head_height_over_stature=hh / 181.0)
    dd = {k: desc(D[k]['V'], D[k]['eye']) for k in D}
    CAN = dict(cranial_height_over_face=+1, skull_breadth_over_HH=-1, lower_face_width_over_bizygomatic=-1, jaw_width_over_bizygomatic=-1, cheekbone_height_over_HH=+1, forehead_profile_mean_turn_rad=-1, head_height_over_stature=0)
    canon = {}
    for k, sg in CAN.items():
        a, b, c = dd['FN'][k], dd['MF'][k], dd['SG'][k]
        dm = 100 * (a / b - 1); ds = 100 * (a / c - 1); hb = abs(100 * (c / b - 1))
        canon[k] = dict(FN=round(a, 4), MF=round(b, 4), SG=round(c, 4), FN_vs_MF_pct=round(dm, 2), FN_vs_SG_pct=round(ds, 2), human_baseline_SG_vs_MF_pct=round(hb, 2), canon_direction=sg,
                        direction_holds=None if sg == 0 else bool(np.sign(dm) == sg and np.sign(ds) == sg), exceeds_human_baseline=bool(abs(dm) > max(2 * hb, 1.0)))
    res['configs'][cfg] = dict(bodies={k: n for k, (n, p) in B.items()}, HH_cm=round(HH, 2), body=body, face=face, canon_descriptors=canon)
    print(cfg, 'BODY', {r: (v['FN_vs_MF_rms_mm'], v['SG_vs_MF_rms_mm_human_baseline']) for r, v in body.items()})
    print(cfg, 'FACE', {r: (v['FN_vs_MF_rms_mm'], v['SG_vs_MF_rms_mm_human_baseline'], v['departure_material']) for r, v in face.items()})
    print(cfg, 'CANON', {k: (v['FN_vs_MF_pct'], v['human_baseline_SG_vs_MF_pct'], v['direction_holds']) for k, v in canon.items()})
json.dump(res, open(OUT, 'w'), indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
