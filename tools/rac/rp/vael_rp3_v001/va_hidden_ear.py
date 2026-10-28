# va_hidden_ear.py WORK OUT.json : Vael order (2026-10-28) §10 / §11 HIDDEN-EAR / NEUTRAL-COMPLEXION identity gates for Vael (body + face), both
# configurations, at matched stature (178 cm; matched frame / muscle / fat / age, R-6, no clothing / hair; geometry only, so complexion is neutral by
# construction) against frozen Fenn, frozen Aelari, Marchfolk and Sagekin. All bodies are MPFB hm08 realizations (shared vertex order); the external ear
# (hm08 w_ears > 0.05) is EXCLUDED from every metric and harmonically collapsed for renders.
#  Body: per-region correspondence RMS of Vael vs Fenn / Aelari / Marchfolk / Sagekin, against the human-human baseline (Sagekin vs Marchfolk).
#  Face: per-region RMS after similarity alignment onto the Vael head; descriptors on fixed hm08 landmarks (fn_face_metrics + orbit breadth from the
#  measurement record). Vael face canon (VAEL_V1 §2-12, ECR §13-14; order §11) is read against frozen Aelari (and Fenn for the mandible): direction +
#  material (>= 1 % and > 2x the human baseline); guards against humans (still elven: brow and mandible not heavier than both humans).
#  No low-light physiology is evaluated (pupil, retina, eye shine, glow: OPEN); only authored craniofacial / orbital anatomy.
import sys, os, json, numpy as np, scipy.sparse as sp
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001')
import fn_face_metrics as F
W, OUT = sys.argv[1:3]; PA = W + '/partA'; OV = os.environ.get('VA_HE_OV', W + '/ov'); os.makedirs(OV, exist_ok=True)
_o = lambda k, d: tuple(os.environ[k].split(':')) if k in os.environ else d
CFG = {'c1': dict(VA=_o('VA_HE_C1', ('VAL4', PA + '/ref/VAL4')), FN=('FNM178', PA + '/cmp/FNM178'), AE=('AEM178', PA + '/cmp/AEM178'), MF=('MFM178', PA + '/cmp/MFM178'), SG=('SGM178', PA + '/cmp/SGM178')),
       'c2': dict(VA=_o('VA_HE_C2', ('VALF178', PA + '/build/VALF178')), FN=('FNF178', PA + '/cmp/FNF178'), AE=('AEF178', PA + '/cmp/AEF178'), MF=('MFF178', PA + '/cmp/MFF178'), SG=('SGF178', PA + '/cmp/SGF178'))}
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
    d['cranial_height_over_stature'] = (g('vertex')[2] - g('nasion')[2]) / (V[:, 2].max() - V[:, 2].min())
    d['face_height_over_bizygomatic'] = (g('nasion')[2] - g('menton')[2]) / zy
    d['forehead_to_chin_over_bizygomatic'] = (g('forehead')[2] - g('menton')[2]) / zy
    d['brow_projection_over_HH'] = (g('glabella')[1] - g('nasion')[1]) / HH
    d['orbit_breadth_over_HL'] = mz['cranio']['ORB_breadth_over_HL']; d['orbit_height_over_HH'] = mz['cranio']['ORB_height_over_HH']
    ap = mz['cranio']['aperture']; d['eye_aperture_area_over_HH2'] = 0.5 * (ap['l']['area_cm2'] + ap['r']['area_cm2']) / HH ** 2
    return d
# canon: (direction vs reference, reference) ; guards: Vael not heavier than BOTH humans (still elven)
CANON = {'face_height_over_bizygomatic': (-1, 'AE'), 'forehead_to_chin_over_bizygomatic': (-1, 'AE'), 'cranial_height_over_stature': (-1, 'AE'),
         'bizygomatic_over_HH': (+1, 'AE'), 'midface_projection_over_HH': (+1, 'AE'), 'orbit_breadth_over_HL': (+1, 'AE'), 'brow_projection_over_HH': (+1, 'AE'),
         'jaw_width_over_bizygomatic': (+1, 'AE'), 'jaw_width_over_bizygomatic@FN': (+1, 'FN')}
REPORT = ['cheekbone_height_over_HH', 'skull_breadth_over_HH', 'lower_face_width_over_bizygomatic', 'lower_face_height_over_HH', 'cranial_height_over_face', 'orbit_height_over_HH', 'eye_aperture_area_over_HH2']
GUARD = {'brow_projection_over_HH': 'not heavier than both humans (no permanent scowl / heavy brow)', 'jaw_width_over_bizygomatic': 'not heavier than both humans (gracile vs robust humans)'}
SYS = {'1 less facial verticality than Aelari': ['face_height_over_bizygomatic'], '2 more compact craniofacial vertical distribution': ['forehead_to_chin_over_bizygomatic', 'cranial_height_over_stature'],
       '3 stronger cheek-to-mid-face integration / broader cheeks than Aelari': ['bizygomatic_over_HH'], '4 more mid-face structural depth than Aelari': ['midface_projection_over_HH'],
       '5 somewhat broader orbits than Aelari': ['orbit_breadth_over_HL'], '6 stronger brow-orbit integration than Aelari (no scowl)': ['brow_projection_over_HH'],
       '7 somewhat more mandibular presence than Fenn / Aelari': ['jaw_width_over_bizygomatic', 'jaw_width_over_bizygomatic@FN']}
res = dict(note='ears excluded (hm08 w_ears > 0.05) from every metric; geometry only (complexion / hair / presentation neutral); matched stature 178 cm; no low-light physiology evaluated', configs={})
for cfg, B in CFG.items():
    D = {k: dict(F.load(p + '_r6.npz'), meas=json.load(open(p + '_meas.json'))['combined']) for k, (n, p) in B.items()}; ear = F.EAR; head = F.HEAD
    for k, (n, p) in B.items(): np.savez('%s/%s_earhidden.npz' % (OV, n), V=collapse(D[k]['V'], ear), Q=Q)
    body = {}
    for r in ('trunk', 'arm', 'hand', 'leg', 'foot', 'neck'):
        m = (BREG == r) & ~ear; rms = lambda a, b: float(np.sqrt((np.linalg.norm(D[a]['V'][m] - D[b]['V'][m], axis=1) ** 2).mean()) * 10)
        x = {'VA_vs_FN': rms('VA', 'FN'), 'VA_vs_AE': rms('VA', 'AE'), 'VA_vs_MF': rms('VA', 'MF'), 'VA_vs_SG': rms('VA', 'SG'), 'FN_vs_AE': rms('FN', 'AE'), 'SG_vs_MF_human_baseline': rms('SG', 'MF')}
        body[r] = {k + '_rms_mm': round(v, 2) for k, v in x.items()}; hb = x['SG_vs_MF_human_baseline']
        body[r].update(ratio_VAFN_over_human=round(x['VA_vs_FN'] / hb, 2), ratio_VAAE_over_human=round(x['VA_vs_AE'] / hb, 2), ratio_VAMF_over_human=round(x['VA_vs_MF'] / hb, 2), ratio_VASG_over_human=round(x['VA_vs_SG'] / hb, 2))
    Va = D['VA']['V']; face = {}
    maps = {k: F.procrustes(D[k]['V'][head], Va[head]) for k in ('MF', 'SG', 'FN', 'AE')}; fsm = F.procrustes(D['SG']['V'][head], D['MF']['V'][head])
    HH = F.descriptors(Va)['head_height_cm']
    for r, m in F.REG.items():
        rm = lambda X, Y: float(np.sqrt((np.linalg.norm(X[m] - Y[m], axis=1) ** 2).mean()) * 10)
        v = {k: rm(Va, maps[k](D[k]['V'])) for k in ('MF', 'SG', 'FN', 'AE')}; sm = rm(D['MF']['V'], fsm(D['SG']['V']))
        face[r] = dict(verts=int(m.sum()), **{'VA_vs_%s_rms_mm' % k: round(x, 2) for k, x in v.items()}, SG_vs_MF_rms_mm_human_baseline=round(sm, 2),
                       departure_from_humans_material=bool(min(v['MF'], v['SG']) > 2 * sm and v['MF'] / 10 / HH * 100 > 0.5),
                       departure_from_aelari_material=bool(v['AE'] > 2 * sm and v['AE'] / 10 / HH * 100 > 0.5), departure_from_fenn_material=bool(v['FN'] > 2 * sm and v['FN'] / 10 / HH * 100 > 0.5))
    dd = {k: desc(D[k]['V'], D[k]['meas']) for k in D}; canon = {}
    hbase = lambda key: abs(100 * (dd['SG'][key] / dd['MF'][key] - 1))
    for key, (sg, ref) in CANON.items():
        k = key.split('@')[0]; a = dd['VA'][k]; b = dd[ref][k]; dr = 100 * (a / b - 1); hb = hbase(k)
        canon[key] = dict(VA=round(a, 4), ref=ref, ref_value=round(b, 4), MF=round(dd['MF'][k], 4), SG=round(dd['SG'][k], 4), FN=round(dd['FN'][k], 4), AE=round(dd['AE'][k], 4),
                          VA_vs_ref_pct=round(dr, 2), VA_vs_MF_pct=round(100 * (a / dd['MF'][k] - 1), 2), human_baseline_pct=round(hb, 2), direction=sg,
                          direction_holds=bool(np.sign(dr) == sg), material=bool(np.sign(dr) == sg and abs(dr) >= 1.0 and abs(dr) > 2 * hb))
    guards = {k: dict(VA=round(dd['VA'][k], 4), MF=round(dd['MF'][k], 4), SG=round(dd['SG'][k], 4), rule=t, holds=bool(dd['VA'][k] <= max(dd['MF'][k], dd['SG'][k]))) for k, t in GUARD.items()}
    rep = {k: {x: round(dd[x][k], 4) for x in dd} for k in REPORT}
    systems = {s: dict(descriptors=ks, direction_ok=all(canon[k]['direction_holds'] for k in ks), material=all(canon[k]['material'] for k in ks)) for s, ks in SYS.items()}
    res['configs'][cfg] = dict(bodies={k: n for k, (n, p) in B.items()}, HH_cm=round(HH, 2), body=body, face=face, canon_descriptors=canon, guards=guards, report=rep, systems=systems,
                               systems_direction_ok=sum(v['direction_ok'] for v in systems.values()), systems_material=sum(v['material'] for v in systems.values()), of=len(systems))
    print(cfg, 'BODY', {r: (v['VA_vs_FN_rms_mm'], v['VA_vs_AE_rms_mm'], v['VA_vs_MF_rms_mm'], v['SG_vs_MF_human_baseline_rms_mm']) for r, v in body.items()})
    print(cfg, 'FACE', {r: (v['VA_vs_AE_rms_mm'], v['VA_vs_FN_rms_mm'], v['VA_vs_MF_rms_mm'], v['SG_vs_MF_rms_mm_human_baseline']) for r, v in face.items()})
    print(cfg, 'CANON', {k: (v['VA_vs_ref_pct'], v['human_baseline_pct'], v['direction_holds'], v['material']) for k, v in canon.items()}, 'GUARDS', {k: v['holds'] for k, v in guards.items()})
    print(cfg, 'systems dir %d material %d / %d' % (res['configs'][cfg]['systems_direction_ok'], res['configs'][cfg]['systems_material'], len(systems)))
json.dump(res, open(OUT, 'w'), indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
