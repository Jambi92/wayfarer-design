# hv_hidden_ear.py WORK OUT.json : Halvren central-anchor order (2026-10-29) §9-§10 / §14-§17 HIDDEN-EAR / NEUTRAL-PIGMENT gates for the central anchor
# (HVC1 / HVF178), both configurations, at matched stature (178 cm; matched frame / muscle / fat / age, R-6, no clothing / hair; geometry only, so
# pigmentation is neutral by construction) against Marchfolk, Sagekin, Skarn (178 cm diagnostic), frozen Fenn, frozen Aelari and frozen Vael. All bodies
# are MPFB hm08 realizations (shared vertex order); the external ear (hm08 w_ears > 0.05) is EXCLUDED from every metric and harmonically collapsed for renders.
#  Body: per-region correspondence RMS of Halvren vs every source against the human-human baseline (Sagekin vs Marchfolk).
#  Face: per-region RMS after similarity alignment onto the Halvren head (cranium, brow / orbit, cheeks / midface, nose, jaw / chin, lower face ...);
#  craniofacial descriptors on fixed hm08 landmarks; for each descriptor the position of Halvren between the human-family mean (MF, SG) and the elven-family
#  mean (FN, AE, VA), the departure from Marchfolk in units of the human baseline, and the nearest source. No phenotype target is applied (order §14, §16).
import sys, os, json, numpy as np, scipy.sparse as sp
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001')
import fn_face_metrics as F
W, OUT = sys.argv[1:3]; PA = W + '/partA'; OV = os.environ.get('HV_HE_OV', W + '/ov'); os.makedirs(OV, exist_ok=True)
CFG = {'c1': dict(HV=('HVC1', PA + '/ref/HVC1'), MF=('MFM178', PA + '/cmp/MFM178'), SG=('SGM178', PA + '/cmp/SGM178'), SK=('SKM178', PA + '/cmp/SKM178'), FN=('FNM178', PA + '/cmp/FNM178'),
                  AE=('AEM178', PA + '/cmp/AEM178'), VA=('VAM178', PA + '/cmp/VAM178')),
       'c2': dict(HV=('HVF178', PA + '/build/HVF178'), MF=('MFF178', PA + '/cmp/MFF178'), SG=('SGF178', PA + '/cmp/SGF178'), SK=('SKF178', PA + '/cmp/SKF178'), FN=('FNF178', PA + '/cmp/FNF178'),
                  AE=('AEF178', PA + '/cmp/AEF178'), VA=('VAF178', PA + '/cmp/VAF178'))}
for _c in ('c1', 'c2'):                                            # optional override of the Halvren item (final consolidation: HV_HE_C1 / HV_HE_C2 = id:prefix)
    if os.environ.get('HV_HE_' + _c.upper()): CFG[_c]['HV'] = tuple(os.environ['HV_HE_' + _c.upper()].split(':', 1))
SRC = ('MF', 'SG', 'SK', 'FN', 'AE', 'VA'); HUM = ('MF', 'SG'); ELF = ('FN', 'AE', 'VA')
nz = np.load('/tmp/claude-0/rt/fn/src/FNL4_native.npz'); Q = np.asarray(nz['Q']); nV = len(nz['src_index']); bones = [str(b) for b in nz['bones']]
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
DGROUP = {'cranium': ['cranial_height_over_stature', 'skull_breadth_over_HH', 'cranial_height_over_face'], 'forehead / brow': ['brow_projection_over_HH', 'forehead_to_chin_over_bizygomatic'],
          'orbital system': ['orbit_breadth_over_HL', 'orbit_height_over_HH', 'eye_aperture_area_over_HH2'], 'cheeks / midface': ['bizygomatic_over_HH', 'midface_projection_over_HH', 'cheekbone_height_over_HH'],
          'nose': [], 'jaw / chin': ['jaw_width_over_bizygomatic', 'lower_face_width_over_bizygomatic'], 'lower-face mass / height': ['lower_face_height_over_HH', 'face_height_over_bizygomatic']}
res = dict(note='ears excluded (hm08 w_ears > 0.05) from every metric; geometry only (pigmentation / hair / presentation neutral); matched stature 178 cm (Skarn 178 cm diagnostic, below its envelope); no low-light physiology evaluated', configs={})
for cfg, B in CFG.items():
    D = {k: dict(F.load(p + '_r6.npz'), meas=json.load(open(p + '_meas.json'))['combined']) for k, (n, p) in B.items()}; ear = F.EAR; head = F.HEAD
    for k, (n, p) in B.items(): np.savez('%s/%s_earhidden.npz' % (OV, n), V=collapse(D[k]['V'], ear), Q=Q)
    body = {}
    for r in ('trunk', 'arm', 'hand', 'leg', 'foot', 'neck'):
        m = (BREG == r) & ~ear; rms = lambda a, b: float(np.sqrt((np.linalg.norm(D[a]['V'][m] - D[b]['V'][m], axis=1) ** 2).mean()) * 10)
        hb = rms('SG', 'MF'); x = {s: rms('HV', s) for s in SRC}
        body[r] = dict(**{'HV_vs_%s_rms_mm' % s: round(v, 2) for s, v in x.items()}, SG_vs_MF_human_baseline_rms_mm=round(hb, 2), **{'ratio_HV%s_over_human' % s: round(v / hb, 2) for s, v in x.items()},
                       nearest=min(x, key=x.get))
    Vh = D['HV']['V']; HH = F.descriptors(Vh)['head_height_cm']; maps = {k: F.procrustes(D[k]['V'][head], Vh[head]) for k in SRC}; fsm = F.procrustes(D['SG']['V'][head], D['MF']['V'][head])
    face = {}
    for r, m in F.REG.items():
        rm = lambda X, Y: float(np.sqrt((np.linalg.norm(X[m] - Y[m], axis=1) ** 2).mean()) * 10)
        v = {k: rm(Vh, maps[k](D[k]['V'])) for k in SRC}; sm = rm(D['MF']['V'], fsm(D['SG']['V']))
        face[r] = dict(verts=int(m.sum()), **{'HV_vs_%s_rms_mm' % k: round(x, 2) for k, x in v.items()}, SG_vs_MF_rms_mm_human_baseline=round(sm, 2), nearest=min(v, key=v.get),
                       departure_from_MF_over_human_baseline=round(v['MF'] / sm, 2) if sm > 0 else None,
                       departure_from_humans_material=bool(min(v['MF'], v['SG']) > 2 * sm and v['MF'] / 10 / HH * 100 > 0.5))
    dd = {k: desc(D[k]['V'], D[k]['meas']) for k in D}; keys = sorted(set(k for ks in DGROUP.values() for k in ks) | {'cheekbone_height_over_HH', 'skull_breadth_over_HH'})
    keys = [k for k in keys if k in dd['HV']]; descs = {}
    for k in keys:
        h = np.mean([dd[s][k] for s in HUM]); e = np.mean([dd[s][k] for s in ELF]); hb = abs(100 * (dd['SG'][k] / dd['MF'][k] - 1)); gap = e - h
        dMF = 100 * (dd['HV'][k] / dd['MF'][k] - 1)
        descs[k] = dict(values={s: round(dd[s][k], 4) for s in ('HV',) + SRC}, human_mean=round(h, 4), elf_mean=round(e, 4), human_baseline_pct=round(hb, 2), HV_vs_MF_pct=round(dMF, 2),
                        position_human0_elf1=round((dd['HV'][k] - h) / gap, 3) if abs(gap) > 1e-9 else None, family_gap_pct=round(100 * gap / h, 2),
                        departs_from_MF_material=bool(abs(dMF) >= 1.0 and abs(dMF) > 2 * hb), nearest=min(SRC, key=lambda s: abs(dd['HV'][k] - dd[s][k])))
    grp = {g: dict(descriptors=ks, positions=[descs[k]['position_human0_elf1'] for k in ks if k in descs], material_departures_from_MF=sum(descs[k]['departs_from_MF_material'] for k in ks if k in descs)) for g, ks in DGROUP.items()}
    grp['nose']['note'] = 'no nose descriptor on the fixed hm08 landmark set; read from the nose-region RMS and the sheets'
    reg_mat = sum(v['departure_from_humans_material'] for v in face.values())
    res['configs'][cfg] = dict(bodies={k: n for k, (n, p) in B.items()}, HH_cm=round(HH, 2), body=body, face=face, descriptors=descs, descriptor_groups=grp,
                               face_regions_departing_from_humans=reg_mat, face_regions_of=len(face), descriptors_departing_from_MF=sum(v['departs_from_MF_material'] for v in descs.values()), descriptors_of=len(descs),
                               face_nearest_count={s: sum(1 for v in face.values() if v['nearest'] == s) for s in SRC})
    print(cfg, 'BODY', {r: (v['HV_vs_MF_rms_mm'], v['SG_vs_MF_human_baseline_rms_mm'], v['nearest']) for r, v in body.items()})
    print(cfg, 'FACE', {r: (v['HV_vs_MF_rms_mm'], v['SG_vs_MF_rms_mm_human_baseline'], v['nearest']) for r, v in face.items()})
    print(cfg, 'DESC', {k: (v['HV_vs_MF_pct'], v['position_human0_elf1'], v['nearest']) for k, v in descs.items()})
    print(cfg, 'regions departing from humans %d / %d, descriptors departing from MF %d / %d' % (reg_mat, len(face), res['configs'][cfg]['descriptors_departing_from_MF'], len(descs)))
json.dump(res, open(OUT, 'w'), indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
