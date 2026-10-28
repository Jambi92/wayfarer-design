# ae_hidden_ear.py WORK OUT.json : order fd71f15 §9 / §10 HIDDEN-EAR identity gates for Aelari (body + face), both configurations, at matched stature
# (~190 cm; matched frame / muscle / fat / age, R-6, no clothing / hair) against frozen Fenn CF2, Sagekin and Marchfolk. All bodies are MPFB hm08
# realizations (shared vertex order); the external ear (hm08 w_ears > 0.05) is EXCLUDED from every metric and harmonically collapsed for renders.
#  Body: per region correspondence RMS of Aelari vs Fenn / Marchfolk / Sagekin and Fenn vs Marchfolk, against the human-human baseline (Sagekin vs Marchfolk).
#  Face: per region RMS after a similarity (scale-removing) alignment onto the Aelari head; canon descriptors on fixed hm08 landmarks (fn_face_metrics), with
#  the Aelari face canon (AELARI_V1 v1.2 §2-8; order §10) checked against BOTH humans (direction + material: >= 1 % and > 2x the human baseline) and the
#  Fenn-relation checks (Aelari vs frozen Fenn CF2 at the same height: more vertical, narrower lower face, longer / narrower eye presentation).
import sys, os, json, numpy as np, scipy.sparse as sp
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001')
import fn_face_metrics as F
W, OUT = sys.argv[1:3]; PA = W + '/partA'; OV = W + '/ov'; os.makedirs(OV, exist_ok=True)
CFG = {'c1': dict(AE=('AEL1', PA + '/ref/AEL1'), FN=('FNM190', PA + '/cmp/FNM190'), MF=('MFM190', PA + '/cmp/MFM190'), SG=('SGM190', PA + '/cmp/SGM190')),
       'c2': dict(AE=('AELF190', PA + '/build/AELF190'), FN=('FNF190', PA + '/cmp/FNF190'), MF=('MFF190', PA + '/cmp/MFF190'), SG=('SGF190', PA + '/cmp/SGF190'))}
nz = np.load('/tmp/claude-0/rt/fn/src/FNL4_native.npz'); si = nz['src_index']; Q = np.asarray(nz['Q']); nV = len(si); bones = [str(b) for b in nz['bones']]
A = sp.coo_matrix((np.ones(4 * len(Q)), (Q[:, :4].ravel(), np.roll(Q, -1, 1).ravel())), shape=(nV, nV)).tocsr(); A = ((A + A.T) > 0).astype(float); deg = np.asarray(A.sum(1)).ravel()
def collapse(V, ear):
    X = V.copy()
    for _ in range(400): X[ear] = (A @ X)[ear] / deg[ear, None]
    return X
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
def desc(V, mz):
    d = F.descriptors(V); g = lambda k: V[F.LM[k]]; zy = abs(g('zygion_l')[0] - g('zygion_r')[0]); HH = d['head_height_cm']
    d['cranial_height_over_stature'] = (g('vertex')[2] - g('nasion')[2]) / (V[:, 2].max() - V[:, 2].min())   # cranial-height contribution at matched stature
    d['face_height_over_bizygomatic'] = (g('nasion')[2] - g('menton')[2]) / zy                        # facial verticality
    d['forehead_to_chin_over_bizygomatic'] = (g('forehead')[2] - g('menton')[2]) / zy                 # longer forehead-to-chin relationship
    d['brow_projection_over_HH'] = (g('glabella')[1] - g('nasion')[1]) / HH                             # lighter brow tendency
    ap = mz['cranio']['aperture']; d['eye_aperture_elongation'] = 0.5 * (ap['l']['width'] / ap['l']['height'] + ap['r']['width'] / ap['r']['height'])
    return d
# cranial_height_over_face is report-only: with a longer face (canon) the face-relative ratio falls even when the cranium is higher; the canon
# 'slightly greater cranial-height contribution' is read at matched stature (cranial_height_over_stature).
# Aelari face canon: +1 Aelari > both humans, -1 <, 0 report only; FN: Aelari vs Fenn relation (+1 >, -1 <, None not required)
CANON = {'cranial_height_over_stature': (+1, +1), 'cranial_height_over_face': (0, None), 'face_height_over_bizygomatic': (+1, +1), 'forehead_to_chin_over_bizygomatic': (+1, +1), 'lower_face_width_over_bizygomatic': (-1, None),
         'jaw_width_over_bizygomatic': (-1, None), 'cheekbone_height_over_HH': (+1, None), 'brow_projection_over_HH': (-1, None), 'eye_aperture_elongation': (0, +1),
         'skull_breadth_over_HH': (0, None), 'midface_projection_over_HH': (0, None), 'lower_face_height_over_HH': (0, None)}
SYS = {'1 facial verticality': ['face_height_over_bizygomatic'], '2 cranial-height contribution': ['cranial_height_over_stature'], '3 forehead-to-chin length': ['forehead_to_chin_over_bizygomatic'],
       '4 narrower lower face': ['lower_face_width_over_bizygomatic'], '5 lighter mandible': ['jaw_width_over_bizygomatic'], '6 vertical cheek / mid-face': ['cheekbone_height_over_HH'],
       '7 lighter brow': ['brow_projection_over_HH']}
res = dict(note='ears excluded (hm08 w_ears > 0.05) from every metric; matched stature ~190 cm', configs={})
for cfg, B in CFG.items():
    D = {k: dict(F.load(p + '_r6.npz'), meas=json.load(open(p + '_meas.json'))['combined']) for k, (n, p) in B.items()}; ear = F.EAR; head = F.HEAD
    for k, (n, p) in B.items():
        np.savez('%s/%s_earhidden.npz' % (OV, n), V=collapse(D[k]['V'], ear), Q=Q)
    body = {}
    for r in ('trunk', 'arm', 'hand', 'leg', 'foot', 'neck'):
        m = (BREG == r) & ~ear; rms = lambda a, b: float(np.sqrt((np.linalg.norm(D[a]['V'][m] - D[b]['V'][m], axis=1) ** 2).mean()) * 10)
        af, am, as_, fm, sm = rms('AE', 'FN'), rms('AE', 'MF'), rms('AE', 'SG'), rms('FN', 'MF'), rms('SG', 'MF')
        body[r] = dict(AE_vs_FN_rms_mm=round(af, 2), AE_vs_MF_rms_mm=round(am, 2), AE_vs_SG_rms_mm=round(as_, 2), FN_vs_MF_rms_mm=round(fm, 2), SG_vs_MF_rms_mm_human_baseline=round(sm, 2),
                       ratio_AEFN_over_human=round(af / sm, 2), ratio_AEMF_over_human=round(am / sm, 2), ratio_AESG_over_human=round(as_ / sm, 2))
    Va = D['AE']['V']; face = {}
    maps = {k: F.procrustes(D[k]['V'][head], Va[head]) for k in ('MF', 'SG', 'FN')}; fsm = F.procrustes(D['SG']['V'][head], D['MF']['V'][head])
    HH = F.descriptors(Va)['head_height_cm']
    for r, m in F.REG.items():
        rm = lambda X, Y: float(np.sqrt((np.linalg.norm(X[m] - Y[m], axis=1) ** 2).mean()) * 10)
        am = rm(Va, maps['MF'](D['MF']['V'])); as_ = rm(Va, maps['SG'](D['SG']['V'])); af = rm(Va, maps['FN'](D['FN']['V'])); sm = rm(D['MF']['V'], fsm(D['SG']['V']))
        face[r] = dict(verts=int(m.sum()), AE_vs_MF_rms_mm=round(am, 2), AE_vs_SG_rms_mm=round(as_, 2), AE_vs_FN_rms_mm=round(af, 2), SG_vs_MF_rms_mm_human_baseline=round(sm, 2),
                       AE_vs_MF_pct_HH=round(am / 10 / HH * 100, 2), departure_from_humans_material=bool(min(am, as_) > 2 * sm and am / 10 / HH * 100 > 0.5),
                       departure_from_fenn_material=bool(af > 2 * sm and af / 10 / HH * 100 > 0.5))
    dd = {k: desc(D[k]['V'], D[k]['meas']) for k in D}; canon = {}
    for k, (sg, sf) in CANON.items():
        a, b, c, f = dd['AE'][k], dd['MF'][k], dd['SG'][k], dd['FN'][k]; dm = 100 * (a / b - 1); ds = 100 * (a / c - 1); hb = abs(100 * (c / b - 1)); dfn = 100 * (a / f - 1)
        canon[k] = dict(AE=round(a, 4), MF=round(b, 4), SG=round(c, 4), FN=round(f, 4), AE_vs_MF_pct=round(dm, 2), AE_vs_SG_pct=round(ds, 2), AE_vs_FN_pct=round(dfn, 2), human_baseline_pct=round(hb, 2),
                        canon_direction=sg, direction_holds=None if sg == 0 else bool(np.sign(dm) == sg and np.sign(ds) == sg),
                        material=None if sg == 0 else bool(np.sign(dm) == sg and np.sign(ds) == sg and min(abs(dm), abs(ds)) >= 1.0 and min(abs(dm), abs(ds)) > 2 * hb),
                        fenn_relation=sf, fenn_relation_holds=None if sf is None else bool(np.sign(dfn) == sf))
    systems = {s: dict(descriptors=ks, direction_ok=all(canon[k]['direction_holds'] for k in ks), material=all(canon[k]['material'] for k in ks)) for s, ks in SYS.items()}
    res['configs'][cfg] = dict(bodies={k: n for k, (n, p) in B.items()}, HH_cm=round(HH, 2), body=body, face=face, canon_descriptors=canon, systems=systems,
                               systems_direction_ok=sum(v['direction_ok'] for v in systems.values()), systems_material=sum(v['material'] for v in systems.values()), of=len(systems),
                               fenn_relations={k: v['fenn_relation_holds'] for k, v in canon.items() if v['fenn_relation'] is not None})
    print(cfg, 'BODY', {r: (v['AE_vs_FN_rms_mm'], v['AE_vs_MF_rms_mm'], v['SG_vs_MF_rms_mm_human_baseline']) for r, v in body.items()})
    print(cfg, 'FACE', {r: (v['AE_vs_MF_rms_mm'], v['AE_vs_FN_rms_mm'], v['SG_vs_MF_rms_mm_human_baseline'], v['departure_from_humans_material']) for r, v in face.items()})
    print(cfg, 'CANON', {k: (v['AE_vs_MF_pct'], v['AE_vs_SG_pct'], v['AE_vs_FN_pct'], v['human_baseline_pct'], v['direction_holds'], v['material']) for k, v in canon.items()})
    print(cfg, 'systems dir %d material %d / %d' % (res['configs'][cfg]['systems_direction_ok'], res['configs'][cfg]['systems_material'], len(systems)), res['configs'][cfg]['fenn_relations'])
json.dump(res, open(OUT, 'w'), indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
