# va2_sheets.py OUTDIR : Vael body / face source order (2026-10-28) §20 visual package, 25 sheets. Identical orthographic cameras per row, true scale;
# ears hidden (hm08 w_ears > 0.05 harmonically collapsed) and geometry-only grey shading (complexion / hair / presentation neutral) wherever identity is
# judged. Workbench renders (grask_rigprep_v001/render_attr.py) composed with PIL / matplotlib; resumable; 2 Blender processes.
# Inputs: VB = candidate workspace (/tmp/claude-0/rt/va2/vc2: cand/, r1/, evaluations), W2 = propagation workspace (/tmp/claude-0/rt/va2/prod: src, fam,
# audit, val, def, ov, lm), PA = Vael Part A comparators (/tmp/claude-0/rt/va/partA), EV = evidence folder (OUTDIR/..).
import sys, os, json, gzip, subprocess, numpy as np, scipy.sparse as sp
from PIL import Image, ImageDraw, ImageFont
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001')
import fn_face_metrics as F
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True); EV = os.path.abspath(OUT + '/..'); E_ = os.environ.get
VB = E_('VA2_VB', '/tmp/claude-0/rt/va2/vc2'); W2 = E_('VA2_W2', '/tmp/claude-0/rt/va2/prod'); PA = E_('VA_PA', '/tmp/claude-0/rt/va/partA'); TMP = E_('VA2_SHEET_TMP', W2 + '/sheet_r'); os.makedirs(TMP, exist_ok=True)
BP = '/home/claude/stc/bin/python3'; REND = '/home/claude/wayfarer-design/tools/rac/rp/grask_rigprep_v001/render_attr.py'
GREY = np.array([0.80, 0.78, 0.76]); jl = lambda p: json.load(open(p))
CFG = {'c1': dict(VA='VAL4-R1', O='VAL4', P='VAL4', FN='FNM178', AE='AEM178', MF='MFM178', SG='SGM178'), 'c2': dict(VA='VALF178-R1', O='VALF178', P='VALF178', FN='FNF178', AE='AEF178', MF='MFF178', SG='SGF178')}
R6 = {'VAL4': PA + '/ref/VAL4_r6.npz', 'VALF178': PA + '/build/VALF178_r6.npz', 'VAL4-R1': VB + '/r1/VAL4-R1_r6.npz', 'VALF178-R1': VB + '/r1/VALF178-R1_r6.npz'}
for c in CFG.values():
    for k in ('FN', 'AE', 'MF', 'SG'): R6[c[k]] = '%s/cmp/%s_r6.npz' % (PA, c[k])
BODY_T = ['VB1g', 'VB2g', 'VB3g']; FACE_T = ['VB2gVC1h', 'VB2gVC2h', 'VB2gVC3h']; ALLC = BODY_T + FACE_T + ['VB1gVC2h', 'VB3gVC2h']
for c, K in CFG.items():
    for t in ALLC: R6['%s-%s' % (K['P'], t)] = '%s/cand/%s-%s_r6.npz' % (VB, K['P'], t)
EVL = {c: jl('%s/VA2_candidate_eval_%s.json' % (EV, c)) for c in CFG}; HE = jl(EV + '/VA2_hidden_ear_identity.json'); PV = jl(EV + '/VA2_pelvis_skeletal_proxy.json')
def font(sz, bold=False):
    f = '/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf' % ('-Bold' if bold else ''); return ImageFont.truetype(f, sz) if os.path.exists(f) else ImageFont.load_default()
# native topology, ear collapse, regions
nz = np.load('/tmp/claude-0/rt/fn/src/FNL4_native.npz'); Q = np.asarray(nz['Q']); nV = len(nz['src_index']); bones = [str(b) for b in nz['bones']]; dom = np.array(bones)[np.asarray(nz['W']).argmax(1)]
A = sp.coo_matrix((np.ones(4 * len(Q)), (Q[:, :4].ravel(), np.roll(Q, -1, 1).ravel())), shape=(nV, nV)).tocsr(); A = ((A + A.T) > 0).astype(float); deg = np.asarray(A.sum(1)).ravel()
def collapse(V):
    X = V.copy()
    for _ in range(400): X[F.EAR] = (A @ X)[F.EAR] / deg[F.EAR, None]
    return X
def earhidden(n):
    p = '%s/ov/%s_earhidden.npz' % (W2, n)
    if os.path.exists(p): return p
    p = os.path.join(TMP, 'eh_%s.npz' % n)
    if not os.path.exists(p): np.savez(p, V=collapse(F.load(R6[n])['V']), Q=Q)
    return p
TRUNK = np.array([b.startswith(('spine', 'pelvis', 'clavicle', 'Root')) for b in dom]); LEG = np.array([b.startswith(('thigh', 'calf', 'foot', 'ball')) for b in dom])
def joints(n):
    j = json.loads(str(np.load(R6[n])['joints'])); z = lambda b: j[b][0][2]
    return dict(clav=0.5 * (z('clavicle_l') + z('clavicle_r')), sp3=z('spine_03'), sp1=z('spine_01'), hip=0.5 * (z('thigh_l') + z('thigh_r')), knee=0.5 * (z('calf_l') + z('calf_r')), ankle=0.5 * (z('foot_l') + z('foot_r')))
C_TH, C_WA, C_FE, C_SH = [0.95, 0.60, 0.20], [0.30, 0.70, 0.75], [0.45, 0.55, 0.90], [0.90, 0.45, 0.55]
def band_cols(n, V):
    j = joints(n); C = np.tile(GREY, (len(V), 1)); z = V[:, 2]
    C[TRUNK & (z >= j['sp3']) & (z <= j['clav'])] = C_TH; C[TRUNK & (z >= j['sp1']) & (z < j['sp3'])] = C_WA
    C[LEG & (z <= j['hip']) & (z > j['knee'])] = C_FE; C[LEG & (z <= j['knee']) & (z > j['ankle'])] = C_SH; return C
def heat(x, lo, hi):
    t = np.clip((x - lo) / (hi - lo + 1e-12), 0, 1)[:, None]; return (1 - t) * np.array([0.2, 0.35, 0.85]) + t * np.array([0.95, 0.25, 0.15])
jobs = []
def render(tag, npz, col, views, wire=False, px=520):
    vs = ';'.join('%s:%s:%s:%.2f' % (n, ','.join('%.4f' % x for x in d), ','.join('%.3f' % x for x in c), hs) for n, d, c, hs in views)
    cf = os.path.join(TMP, tag + '_col.npy'); np.save(cf, np.asarray(col, np.float32)); jobs.append([BP, REND, '--', npz, cf, TMP, tag, vs, '1' if wire else '0', str(px)])
def img(tag, name):
    p = os.path.join(TMP, '%s_%s.png' % (tag, name)); return Image.open(p).convert('RGB') if os.path.exists(p) else Image.new('RGB', (600, 600), 'white')
def blend(a, b):   # silhouette overlay: both = grey shading, only first = red, only second = blue (background = the render's flat grey)
    A_ = np.asarray(a, float); B_ = np.asarray(b, float); bg = A_[2, 2]
    ma = np.abs(A_ - bg).sum(2) > 6; mb = np.abs(B_ - bg).sum(2) > 6; O = np.full_like(A_, 255.0)
    both = ma & mb; O[both] = 0.5 * (A_[both] + B_[both]); O[ma & ~mb] = [215, 40, 30]; O[mb & ~ma] = [40, 80, 215]; return Image.fromarray(np.clip(O, 0, 255).astype(np.uint8))
# ---------------------------------------------------------------- cameras (per configuration, centred on the Vael R1 source)
CAM = {}
for c, K in CFG.items():
    Vv = np.load(earhidden(K['VA']))['V']; ym = Vv[:, 1].mean(); top = Vv[:, 2].max(); jv = joints(K['VA'])
    Hc = np.array([0.0, Vv[Vv[:, 2] > top - 25][:, 1].mean(), top - 12.0]); g = lambda k: Vv[F.LM[k]]
    CAM[c] = dict(B=np.array([0.0, ym, 92.0]), H=Hc, T=np.array([0.0, ym, 0.5 * (jv['sp1'] + jv['clav'])]), P=np.array([0.0, ym, jv['hip'] + 4]), S=np.array([0.0, ym, jv['clav'] + 6]),
                  hand=np.array([Vv[:, 0].max() - 9, ym, jv['hip'] - 22]), foot=np.array([11.0, 6.0, 6.0]), L=np.array([0.0, ym, 50.0]),
                  cran=np.array([0.0, Hc[1], top - 6.0]), orb=np.array([0.0, g('nasion')[1], g('nasion')[2] - 1.0]), mid=np.array([0.0, g('nasion')[1], 0.5 * (g('nasion')[2] + g('menton')[2])]),
                  jaw=np.array([0.0, g('menton')[1] - 3, g('menton')[2] + 3.5]))
BV = lambda c: [('bfront', (0, 1, 0), CAM[c]['B'], 96), ('bprof', (1, 0, 0), CAM[c]['B'], 96)]
HV = lambda c: [('hfront', (0, 1, 0.03), CAM[c]['H'], 14.5), ('hprof', (1, 0, 0), CAM[c]['H'], 14.5), ('htq', (1, 1, 0.1), CAM[c]['H'], 14.5)]
RV = lambda c: [('tprof', (1, 0, 0), CAM[c]['T'], 32), ('tfront', (0, 1, 0), CAM[c]['T'], 32), ('shoulder', (0.25, 1, 0.12), CAM[c]['S'], 24), ('pelvis', (1, 0.25, 0.0), CAM[c]['P'], 28), ('pfront', (0, 1, 0), CAM[c]['P'], 28),
                ('hand', (0.3, 1, 0.0), CAM[c]['hand'], 14), ('foot', (0.8, 0.6, 0.6), CAM[c]['foot'], 14), ('ankle', (1, 0.05, 0), CAM[c]['foot'] + np.array([0, -2, 4]), 14)]
FV = lambda c: [('cran', (1, 0.15, 0.25), CAM[c]['cran'], 10), ('ctop', (0, 1, 1.2), CAM[c]['cran'], 11), ('orbp', (1, 0.1, 0.05), CAM[c]['orb'], 6.5), ('orbq', (0.7, 1, 0.1), CAM[c]['orb'], 6.5),
                ('midq', (1, 1, -0.15), CAM[c]['mid'], 8.5), ('midu', (0, 1, -0.6), CAM[c]['mid'], 8.5), ('jawl', (0.8, 1, -0.45), CAM[c]['jaw'], 8.0), ('jawp', (1, 0, 0), CAM[c]['jaw'], 8.0)]
REGC = {'cranium_vault': [0.85, 0.55, 0.30], 'forehead': [0.80, 0.70, 0.35], 'orbit_eye_region': [0.40, 0.60, 0.85], 'cheeks_midface': [0.90, 0.45, 0.50], 'jaw_chin': [0.45, 0.70, 0.45], 'nose': [0.70, 0.55, 0.80], 'mouth': [0.85, 0.65, 0.65]}
def regcols(V):
    C = np.tile(GREY, (len(V), 1))
    for r, col in REGC.items(): C[F.REG[r]] = col
    return C
for c, K in CFG.items():
    for n in (K['VA'], K['FN'], K['AE'], K['MF'], K['SG']):
        hp = earhidden(n); V = np.load(hp)['V']
        render('he_' + n, hp, np.tile(GREY, (len(V), 1)), BV(c) + HV(c) + RV(c) + FV(c))
        if n != K['SG']: render('band_' + n, hp, band_cols(n, V), [('tprof', (1, 0, 0), CAM[c]['T'], 32), ('lprof', (1, 0, 0), CAM[c]['L'], 52)])
        if n == K['VA']: render('reg_' + n, hp, regcols(V), HV(c) + FV(c))
    for n in [K['O']] + ['%s-%s' % (K['P'], t) for t in BODY_T]:
        hp = earhidden(n); V = np.load(hp)['V']; render('hb_' + n, hp, np.tile(GREY, (len(V), 1)), BV(c) + [('tprof', (1, 0, 0), CAM[c]['T'], 32)])
    for n in [K['O']] + ['%s-%s' % (K['P'], t) for t in FACE_T]:
        hp = earhidden(n); V = np.load(hp)['V']; render('hc_' + n, hp, np.tile(GREY, (len(V), 1)), HV(c))
    # body residual heat (equal stature, common frame) and face residual heat (similarity aligned onto the Vael head)
    Va = np.load(earhidden(K['VA']))['V']; body = ~F.HEAD & ~F.EAR
    for k in ('MF', 'SG', 'AE', 'FN'):
        Vk = np.load(earhidden(K[k]))['V']; d = np.linalg.norm(Vk - Va, axis=1); C = np.tile(GREY, (len(Va), 1)); C[body] = heat(d[body], 0, 3.0)
        render('bres_%s_%s' % (c, k), earhidden(K['VA']), C, BV(c))
        f = F.procrustes(Vk[F.HEAD], Va[F.HEAD]); d = np.linalg.norm(f(Vk) - Va, axis=1) * 10; C = np.tile(GREY, (len(Va), 1)); C[F.HEAD & ~F.EAR] = heat(d[F.HEAD & ~F.EAR], 0, 4.0)
        render('fres_%s_%s' % (c, k), earhidden(K['VA']), C, HV(c)[:2])
    # family propagation overlay
    z = np.load(R6[K['VA']]); keep = z['keep']; Fx = z['F'][keep[z['F']].all(1)]; q = os.path.join(TMP, 'src_%s.npz' % K['VA']); np.savez_compressed(q, V=z['V'], Q=Fx)
    render('src_' + K['VA'], q, np.tile(GREY, (len(z['V']), 1)), BV(c) + [('hq', (1, 1, 0.1), CAM[c]['H'], 14.5)])
    fz = np.load('%s/fam/%s_fam.npz' % (W2, K['VA'])); render('fam_' + K['VA'], '%s/fam/%s_fam.npz' % (W2, K['VA']), np.tile(GREY, (len(fz['V']), 1)), BV(c) + [('hq', (1, 1, 0.1), CAM[c]['H'], 14.5)])
    fz2 = np.load('%s/fam/%s_fam.npz' % (W2, K['VA'])); render('famw_' + K['VA'], '%s/fam/%s_fam.npz' % (W2, K['VA']), np.tile(GREY, (len(fz2['V']), 1)), [('hq', (1, 1, 0.1), CAM[c]['H'], 14.5)], wire=True)
# expression sanity renders (family realization; MPFB expression units added to the R-6 source and carried by the hm08 map, as cf_expr.py)
UD = '/home/claude/mpfb2_2017/src/mpfb/data/targets/expression/units/caucasian'
def unit(n):
    D = {}
    for l in gzip.open('%s/%s.target.gz' % (UD, n), 'rt'):
        p = l.split()
        if len(p) == 4: D[int(p[0])] = np.array([float(p[1]), float(p[3]), float(p[2])]) * 10.0
    return D
EX = {'neutral': {}, 'blink': {'eye-left-closure': 1, 'eye-right-closure': 1}, 'look_up': {'eye-left-opened-up': 1, 'eye-right-opened-up': 1}, 'look_down': {'eye-left-slit': 1, 'eye-right-slit': 1},
      'smile': {'mouth-corner-puller': 1, 'mouth-upward-retraction': 0.5}, 'anger': {'eyebrows-left-down': 1, 'eyebrows-right-down': 1, 'nose-compression': 0.6, 'mouth-compression': 0.6},
      'surprise': {'eyebrows-left-up': 1, 'eyebrows-right-up': 1, 'eye-left-opened-up': 1, 'eye-right-opened-up': 1, 'mouth-open': 0.7}, 'sadness': {'eyebrows-left-inner-up': 1, 'eyebrows-right-inner-up': 1, 'mouth-depression': 1}}
UC = {n: unit(n) for e in EX.values() for n in e}
for c, K in CFG.items():
    z = np.load(R6[K['VA']]); fz = np.load('%s/fam/%s_fam.npz' % (W2, K['VA'])); si = fz['src_index']; M = sp.csr_matrix((fz['M_data'], fz['M_indices'], fz['M_indptr']), shape=tuple(fz['M_shape']))
    Hf = M @ z['V'][si].astype(float); top = Hf[:, 2].max(); hc = np.array([0.0, Hf[Hf[:, 2] > top - 25][:, 1].mean(), top - 12.0])
    for e, comp in EX.items():
        q = os.path.join(TMP, 'ex_%s_%s.npz' % (c, e))
        if not os.path.exists(q):
            Vx = z['V'].astype(float).copy()
            for un, w in comp.items():
                for i, dv in UC[un].items(): Vx[i] += w * dv
            np.savez_compressed(q, V=M @ Vx[si], Q=fz['Q'])
        render('ex_%s_%s' % (c, e), q, np.tile(GREY, (len(fz['V']), 1)), [('f', (0.35, 1, 0.05), hc, 13.0)], px=420)
# deformation poses
for c, K in CFG.items():
    n = K['VA']; fz = np.load('%s/fam/%s_fam.npz' % (W2, n))
    for pn in ('shoulder_abd90_l', 'elbow_130_l', 'hip_flex90_l', 'knee_140_l', 'neck_rot45', 'trunk_twist30'):
        pp = '%s/def/%s_%s_fam.npz' % (W2, pn, n)
        if not os.path.exists(pp): continue
        X = np.load(pp); Xv = X['V']; C = np.tile(GREY, (len(fz['Q']), 1)); fl = np.asarray(X['flip']).astype(int).ravel(); C[fl[fl < len(C)]] = [0.92, 0.18, 0.12]
        q = os.path.join(TMP, 'pose_%s_%s.npz' % (n, pn)); np.savez_compressed(q, V=Xv, Q=fz['Q']); Bc_ = np.array([0.0, Xv[:, 1].mean(), (Xv[:, 2].max() + Xv[:, 2].min()) / 2])
        render('pose_%s_%s' % (n, pn), q, C, [('v', (1, 1, 0.05), Bc_, 100)], px=420)
print('render jobs', len(jobs), flush=True)
done_ = lambda j: all(os.path.exists(os.path.join(TMP, '%s_%s.png' % (j[6], v_.split(':')[0]))) for v_ in j[7].split(';'))
todo = [j for j in jobs if not done_(j)]; print('to render', len(todo), flush=True)
with ThreadPoolExecutor(int(E_('VA_SHEET_THREADS', '2'))) as ex: list(ex.map(lambda j: subprocess.run(j, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL), todo))
# ---------------------------------------------------------------- compose
def sheet(fname, title, rows, colw=480, note=None, lab_w=170, legend=None):
    ncol = max(len(r_[1]) for r_ in rows); Wd = lab_w + ncol * colw; tl = title.split(' — ', 1) if font(21, True).getlength(title) > Wd - 28 else [title]; th = 70 + 30 * (len(tl) - 1)
    nl = len(note.split('\n')) if note else 0; Hh = th + sum(colw + 34 for _ in rows) + (24 * nl + 20 if note else 0) + (44 if legend else 0)
    S = Image.new('RGB', (Wd, Hh), 'white'); d = ImageDraw.Draw(S)
    for i_, t_ in enumerate(tl): d.text((14, 14 + 30 * i_), t_ if i_ == 0 else '— ' + t_, fill=(0, 0, 0), font=font(21, True))
    y = th
    for lab, ims, caps in rows:
        d.text((10, y + colw // 2), lab, fill=(0, 0, 0), font=font(17, True))
        for k_, im in enumerate(ims):
            S.paste(im.resize((colw, colw)), (lab_w + k_ * colw, y))
            if caps and k_ < len(caps) and caps[k_]: d.text((lab_w + 6 + k_ * colw, y + colw + 4), caps[k_], fill=(30, 30, 30), font=font(14))
        y += colw + 34
    if legend:
        x = 14
        for nm, col in legend:
            d.rectangle((x, y + 10, x + 24, y + 30), fill=tuple(int(255 * v) for v in col)); d.text((x + 30, y + 10), nm, fill=(0, 0, 0), font=font(14)); x += 40 + 9 * len(nm)
        y += 44
    if note:
        for i_, ln in enumerate(note.split('\n')): d.text((14, y + 4 + 24 * i_), ln, fill=(60, 60, 60), font=font(15))
    S.save(os.path.join(OUT, fname), quality=88)
def cv(c, k, tag='R1'):
    return next(r for r in EVL[c]['items'][tag]['canon'] if r['key'] == k)
pct = lambda c, k, ref, tag='R1': cv(c, k, tag)['vs_pct'][ref]
NM = lambda c, k: CFG[c][k]
# 01 body candidates
rows = []
for c, K in CFG.items():
    for v in ('bfront', 'bprof', 'tprof'):
        rows.append(('%s %s' % (c, v[1:] if v != 'tprof' else 'torso'), [img('hb_' + K['O'], v)] + [img('hb_%s-%s' % (K['P'], t), v) for t in BODY_T], ['%s (original)' % K['O'], 'VB1 (VB1g)', 'VB2 (VB2g)', 'VB3 (VB3g)'] if v == 'bfront' else None))
sheet('VA2_01_body_candidates_VB1_VB2_VB3.jpg', 'Vael body-source candidates (body only, no VC; ears hidden, 178 cm, same camera) — original | VB1 | VB2 | VB3 (one architecture, bounded magnitude)', rows, colw=360,
      note='VB architecture: pelvis bone scale [1.02, 1.045, 1.03] + thigh / calf Y x 0.9975 (hip-joint window) + torso-scale-depth-incr / neck-scale-horiz-incr / foot-scale-depth-incr at\n'
           'VB1 0.18 / 0.08 / 0.04, VB2 0.25 / 0.20 / 0.06, VB3 0.33 / 0.32 / 0.08 (identical on c1 / c2; stature re-solved).  Body systems material vs humans (with VC2): ' +
           '  '.join('%s c1 %d c2 %d' % (t, EVL['c1']['items'][t]['body_systems_material'], EVL['c2']['items'][t]['body_systems_material']) for t in ('VB1gVC2h', 'R1', 'VB3gVC2h')))
def four(prefix, view, keys=('VA', 'MF', 'SG')):
    return [img(prefix + CFG[c][k], view) for k in keys]
rows = []
for c, K in CFG.items():
    for lab, v in (('front', 'bfront'), ('profile', 'bprof')):
        rows.append(('%s %s' % (c, lab), [img('he_' + K[k], v) for k in ('VA', 'MF', 'SG')] + [blend(img('he_' + K['VA'], v), img('he_' + K['MF'], v))], ['%s (Vael)' % K['VA'], K['MF'], K['SG'], 'Vael red / Marchfolk blue'] if lab == 'front' else None))
sheet('VA2_02_equal_height_vs_humans.jpg', 'Equal height 178 cm, ears hidden, neutral shading: Vael R1 | Marchfolk | Sagekin | overlay Vael-Marchfolk', rows, colw=400)
rows = []
for c, K in CFG.items():
    for lab, v in (('front', 'bfront'), ('profile', 'bprof')):
        rows.append(('%s %s' % (c, lab), [img('he_' + K[k], v) for k in ('VA', 'FN', 'AE')], ['%s (Vael)' % K['VA'], '%s (frozen Fenn)' % K['FN'], '%s (frozen Aelari)' % K['AE']] if lab == 'front' else None))
sheet('VA2_03_equal_height_three_elf.jpg', 'Equal height 178 cm, ears hidden, neutral shading: Vael R1 | frozen Fenn | frozen Aelari', rows, colw=420)
reg = lambda vname, title, fname, legend=None, note=None, colw=400: sheet(fname, title, [('%s' % c, [img(('band_' if vname.startswith('band') else 'he_') + K[k], vname.replace('band:', '')) for k in ('VA', 'FN', 'AE', 'MF')], [K[k] for k in ('VA', 'FN', 'AE', 'MF')]) for c, K in CFG.items()], colw=colw, legend=legend, note=note)
reg('band:tprof', 'Vael — torso / ribcage depth (ears hidden): Vael R1 | Fenn | Aelari | Marchfolk — orange thoracic vertical, teal waist interval', 'VA2_04_torso_ribcage.jpg', legend=[('thoracic vertical', C_TH), ('waist interval', C_WA)],
    note='thorax depth / stature vs Fenn / Aelari / MF: c1 %+.1f / %+.1f / %+.1f %%, c2 %+.1f / %+.1f / %+.1f %%;  waist interval / torso vs Aelari (VA-P6): c1 %+.2f %%, c2 %+.2f %%' % (
        pct('c1', 'thorax_depth_share', 'FN'), pct('c1', 'thorax_depth_share', 'AE'), pct('c1', 'thorax_depth_share', 'MF'), pct('c2', 'thorax_depth_share', 'FN'), pct('c2', 'thorax_depth_share', 'AE'), pct('c2', 'thorax_depth_share', 'MF'),
        pct('c1', 'waist_interval_over_torso', 'AE'), pct('c2', 'waist_interval_over_torso', 'AE')))
nk = lambda c: next(d for d in EVL[c]['items']['R1']['body_systems']['8 shoulder / neck integration']['descriptors'] if d['key'] == 'neck_breadth_over_shoulder_joint')
reg('shoulder', 'Vael — shoulder / neck integration (ears hidden): Vael R1 | Fenn | Aelari | Marchfolk', 'VA2_05_shoulder_neck.jpg',
    note='neck breadth / shoulder-joint breadth vs MF: c1 %+.1f %%, c2 %+.1f %% (human variation %.1f / %.1f %%); shoulder breadth unchanged (no new mandatory breadth)' % (nk('c1')['VA_vs_MF_pct'], nk('c2')['VA_vs_MF_pct'], nk('c1')['human_var_pct'], nk('c2')['human_var_pct']))
pvl = lambda rs: '  '.join('%s%s %s %+.2f%%' % (r['rule'].split(' ')[0], '' if r['gating'] else '(rep)', 'OK' if r['holds_all_t'] else 'NO', r['by_t']['0.5']['diff_pct']) for r in rs)
pv = lambda c: pvl(PV['rules'][c][:8]) + '\n      ' + pvl(PV['rules'][c][8:])
sheet('VA2_06_pelvis_waist.jpg', 'Vael — pelvis / waist (ears hidden): Vael R1 | Fenn | Aelari | Marchfolk (oblique and front)', [('%s %s' % (c, v), [img('he_' + K[k], v) for k in ('VA', 'FN', 'AE', 'MF')], [K[k] for k in ('VA', 'FN', 'AE', 'MF')] if v == 'pelvis' else None) for c, K in CFG.items() for v in ('pelvis', 'pfront')], colw=380,
      note='skeletal proxy, t = 0.5 cm (rule, holds at all t, Vael vs reference; (rep) = construction proxy, report-only, visual check here):\nc1: %s\nc2: %s' % (pv('c1'), pv('c2')))
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
# 07 hip-joint ordering diagnostic + vertical partition
fig, axs = plt.subplots(1, 3, figsize=(19, 5.6))
TAGS = [('VAL4', 'original'), ('VB1g', 'VB1'), ('VB2g', 'VB2'), ('VB3g', 'VB3'), ('VB1gVC2h', 'VB1+VC2'), ('R1', 'VB2+VC2 (R1)'), ('VB3gVC2h', 'VB3+VC2'), ('VB2gVC1h', 'VB2+VC1'), ('VB2gVC3h', 'VB2+VC3')]
for ax, key, t in zip(axs[:2], ('leg_share', 'waist_interval_over_torso'), ('hip-joint height / stature (VA-P2a: MF < Vael < Aelari < Fenn)', 'waist interval / torso (VA-P6: Vael < Aelari)')):
    for i, c in enumerate(('c1', 'c2')):
        it = EVL[c]['items']; r0 = cv(c, key, 'R1'); labs = ['MF', 'AE'] + [l for _, l in TAGS]; vals = [r0['MF'], r0['AE']] + [cv(c, key, tg)['VA'] for tg, _ in TAGS]
        xs = np.arange(len(labs)) + i * (len(labs) + 1); cols = ['#6aa36a', '#7a4fb0'] + ['#bbbbbb' if l == 'original' else '#e07a2e' if 'R1' in l else '#f0b27a' for l in labs[2:]]
        ax.bar(xs, vals, color=cols); [ax.text(xx, v, ' %s %s' % (c, l), rotation=90, fontsize=7, ha='center', va='bottom') for xx, v, l in zip(xs, vals, labs)]
        ax.axhline(r0['MF'], xmin=i * 0.5, xmax=i * 0.5 + 0.5, color='#6aa36a', lw=0.8, ls='--'); ax.axhline(r0['AE'], xmin=i * 0.5, xmax=i * 0.5 + 0.5, color='#7a4fb0', lw=0.8, ls='--')
    lo = min(min(cv(c, key, 'R1')['MF'], cv(c, key, 'R1')['AE'], min(cv(c, key, tg)['VA'] for tg, _ in TAGS)) for c in ('c1', 'c2')); hi = max(max(cv(c, key, 'R1')['MF'], cv(c, key, 'R1')['AE'], max(cv(c, key, tg)['VA'] for tg, _ in TAGS)) for c in ('c1', 'c2'))
    ax.set_ylim(lo - 0.3 * (hi - lo), hi + 0.9 * (hi - lo)); ax.set_title(t, fontsize=10); ax.set_xticks([])
PT = jl(EV + '/VA2_vertical_partition.json'); ax = axs[2]; parts = ['leg', 'torso', 'neck', 'cran', 'rest']; pc = ['#4a78c2', '#e07a2e', '#9c6', '#c66', '#999']; x = 0; xt = []
for c in ('c1', 'c2'):
    for k in ('MF', 'VA', 'AE'):
        b = 0
        for p_, col in zip(parts, pc): v = PT[c][k][p_]; ax.bar(x, v, bottom=b, color=col, label=p_ if x == 0 else None); ax.text(x, b + v / 2, '%.4f' % v, ha='center', va='center', fontsize=6.5); b += v
        xt.append('%s %s' % (c, k)); x += 1
    x += 0.6
ax.set_xticks([0, 1, 2, 3.6, 4.6, 5.6]); ax.set_xticklabels(xt, fontsize=8); ax.set_ylim(0, 1.0); ax.legend(fontsize=7, loc='lower right')
ax.set_title('vertical partition of stature: leg + torso + neck + cranial + rest (face below the canthus) = 1\nVael leg < Aelari and rest < Aelari  =>  central (torso + neck + cranial) > Aelari', fontsize=9)
fig.suptitle('Vael ordering diagnostic at matched stature (178 cm) — left block c1, right block c2 (dashed: MF green, Aelari purple)'); fig.tight_layout(); fig.savefig(os.path.join(OUT, 'VA2_07_hip_ordering_diagnostic.jpg'), dpi=100); plt.close(fig)
reg('hand', 'Vael — arm / hand base (ears hidden): Vael R1 | Fenn | Aelari | Marchfolk', 'VA2_08_arms_hands.jpg', note='palm breadth / hand vs Fenn / Aelari / MF: c1 %+.1f / %+.1f / %+.1f %%; c2 %+.1f / %+.1f / %+.1f %%;  wrist / forearm vs Fenn / Aelari: c1 %+.1f / %+.1f %%, c2 %+.1f / %+.1f %%' % (
    pct('c1', 'palm_breadth_over_hand', 'FN'), pct('c1', 'palm_breadth_over_hand', 'AE'), pct('c1', 'palm_breadth_over_hand', 'MF'), pct('c2', 'palm_breadth_over_hand', 'FN'), pct('c2', 'palm_breadth_over_hand', 'AE'), pct('c2', 'palm_breadth_over_hand', 'MF'),
    pct('c1', 'wrist_over_forearm', 'FN'), pct('c1', 'wrist_over_forearm', 'AE'), pct('c2', 'wrist_over_forearm', 'FN'), pct('c2', 'wrist_over_forearm', 'AE')))
sheet('VA2_09_legs_ankles_feet.jpg', 'Vael — leg segments, ankle and foot base (ears hidden): Vael R1 | Fenn | Aelari | Marchfolk', [('%s %s' % (c, v), [img(('band_' if v == 'lprof' else 'he_') + K[k], v) for k in ('VA', 'FN', 'AE', 'MF')], [K[k] for k in ('VA', 'FN', 'AE', 'MF')] if v == 'lprof' else None) for c, K in CFG.items() for v in ('lprof', 'foot', 'ankle')], colw=360,
      legend=[('thigh', C_FE), ('lower leg', C_SH)], note='foot breadth / length vs Fenn / Aelari / MF: c1 %+.1f / %+.1f / %+.1f %%, c2 %+.1f / %+.1f / %+.1f %%;  foot share vs MF c1 %+.2f %%, c2 %+.2f %%;  ankle / shin vs Fenn / Aelari c1 %+.1f / %+.1f %%' % (
          pct('c1', 'foot_breadth_over_length', 'FN'), pct('c1', 'foot_breadth_over_length', 'AE'), pct('c1', 'foot_breadth_over_length', 'MF'), pct('c2', 'foot_breadth_over_length', 'FN'), pct('c2', 'foot_breadth_over_length', 'AE'), pct('c2', 'foot_breadth_over_length', 'MF'),
          pct('c1', 'foot_share', 'MF'), pct('c2', 'foot_share', 'MF'), pct('c1', 'ankle_over_shin', 'FN'), pct('c1', 'ankle_over_shin', 'AE')))
rows = []
for c in CFG:
    for v in ('bfront', 'bprof'): rows.append(('%s %s' % (c, v[1:]), [img('bres_%s_%s' % (c, k), v) for k in ('MF', 'SG', 'AE', 'FN')], ['vs Marchfolk', 'vs Sagekin', 'vs Aelari', 'vs Fenn'] if v == 'bfront' else None))
br = lambda c: '  '.join('%s %.1f/%.1f/%.1f/%.1f (SG-MF %.1f)' % (r, v['VA_vs_MF_rms_mm'], v['VA_vs_SG_rms_mm'], v['VA_vs_AE_rms_mm'], v['VA_vs_FN_rms_mm'], v['SG_vs_MF_human_baseline_rms_mm']) for r, v in HE['configs'][c]['body'].items())
sheet('VA2_10_body_residual_heatmaps.jpg', 'Vael R1 body residuals at equal stature (blue 0 .. red >= 3 cm, ears / head grey): vs Marchfolk | Sagekin | Aelari | Fenn', rows, colw=380,
      note='region RMS mm  VA vs MF / SG / AE / FN (human baseline SG vs MF):\nc1: %s\nc2: %s' % (br('c1'), br('c2')))
# face
rows = []
for c, K in CFG.items():
    for v in ('hfront', 'hprof', 'htq'): rows.append(('%s %s' % (c, v[1:]), [img('hc_' + K['O'], v)] + [img('hc_%s-%s' % (K['P'], t), v) for t in FACE_T], ['%s source face' % K['O'], 'VC1 (restrained)', 'VC2 (balanced)', 'VC3 (stronger)'] if v == 'hfront' else None))
fs = lambda t: '  '.join('%s c1 %d/6 c2 %d/6' % (t_, EVL['c1']['items'][t_]['face_systems_material'], EVL['c2']['items'][t_]['face_systems_material']) for t_ in t)
sheet('VA2_11_face_source_vs_VC1_VC2_VC3.jpg', 'Vael craniofacial candidates on body VB2 (ears hidden, same camera) — source | VC1 | VC2 | VC3 (one architecture, magnitude 0.6 / 1.0 / 1.4)', rows, colw=360,
      note='VC2 = head-oval 0.15, forehead-scale-vert-incr 0.03, head-scale-horiz-incr 0.06, chin-height-decr 0.20, cheek-inner-incr 0.35, cheek-trans-up 0.80, eyebrows-trans-backward 0.015, chin-bones-incr 0.30, head-diamond 0.12\n'
           'face systems material vs MF: ' + fs(['VB2gVC1h', 'VB2gVC2h', 'VB2gVC3h']))
rows = []
for c, K in CFG.items():
    for v in ('hfront', 'hprof'):
        rows.append(('%s %s' % (c, v[1:]), [blend(img('hc_%s-%s' % (K['P'], t), v), img('he_' + K['MF'], v)) for t in FACE_T] + [blend(img('he_' + K['VA'], v), img('he_' + K['AE'], v))], ['VC1 red / MF blue', 'VC2 red / MF blue', 'VC3 red / MF blue', 'R1 red / Aelari blue'] if v == 'hfront' else None))
sheet('VA2_12_ears_hidden_candidate_comparison.jpg', 'Ears-hidden candidate comparison — VC1 / VC2 / VC3 over Marchfolk, and the selected R1 over frozen Aelari (equal stature, same camera)', rows, colw=380)
rows = []
for c, K in CFG.items():
    for v in ('hfront', 'hprof', 'htq'): rows.append(('%s %s' % (c, v[1:]), [img('he_' + K[k], v) for k in ('VA', 'MF', 'SG', 'FN', 'AE')], ['Vael R1', 'Marchfolk', 'Sagekin', 'frozen Fenn', 'frozen Aelari'] if v == 'hfront' else None))
sheet('VA2_13_face_vs_MF_SG_FN_AE.jpg', 'Hidden-ear / neutral-complexion face, 178 cm: Vael R1 | Marchfolk | Sagekin | frozen Fenn | frozen Aelari', rows, colw=340)
fd = lambda c, k: EVL[c]['items']['R1']['face_desc_vs_MF_pct'].get(k)
fe = lambda c, k: EVL[c]['items']['R1']['face_canon_vs_elves'][k]['VA_vs_ref_pct']
def fsheet(fname, title, views, note):
    rows = [('%s %s' % (c, v), [img('reg_' + K['VA'], v)] + [img('he_' + K[k], v) for k in ('VA', 'MF', 'FN', 'AE')], ['Vael R1 (regions)', 'Vael R1', 'Marchfolk', 'frozen Fenn', 'frozen Aelari'] if v == views[0] else None) for c, K in CFG.items() for v in views]
    sheet(fname, title, rows, colw=330, note=note, legend=[(r, col) for r, col in REGC.items()])
fsheet('VA2_14_cranial_region.jpg', 'Vael cranial region (ears hidden): oblique profile and front-top', ('cran', 'ctop'),
       'cranial height / face vs MF: c1 %+.1f %%, c2 %+.1f %%;  cranial height / stature vs MF c1 %+.1f %%, vs Aelari c1 %+.2f %% / c2 %+.2f %% (compact vs Aelari; elven vs human)' % (fd('c1', 'cranial_height_over_face'), fd('c2', 'cranial_height_over_face'), fd('c1', 'cranial_height_over_stature'), fe('c1', 'cranial_height_over_stature'), fe('c2', 'cranial_height_over_stature')))
fsheet('VA2_15_cheek_midface.jpg', 'Vael cheek / mid-face (ears hidden): three-quarter and from below', ('midq', 'midu'),
       'bizygomatic / HH vs MF c1 %+.1f / c2 %+.1f %%, vs Aelari c1 %+.1f / c2 %+.1f %%;  mid-face projection / HH vs MF c1 %+.1f / c2 %+.1f %%, vs Aelari c1 %+.1f / c2 %+.1f %%;  cheekbone height vs MF c1 %+.1f %%' % (
           fd('c1', 'bizygomatic_over_HH'), fd('c2', 'bizygomatic_over_HH'), fe('c1', 'bizygomatic_over_HH'), fe('c2', 'bizygomatic_over_HH'), fd('c1', 'midface_projection_over_HH'), fd('c2', 'midface_projection_over_HH'), fe('c1', 'midface_projection_over_HH'), fe('c2', 'midface_projection_over_HH'), fd('c1', 'cheekbone_height_over_HH')))
fsheet('VA2_16_orbit_brow.jpg', 'Vael orbit / brow (ears hidden): profile close-up and three-quarter', ('orbp', 'orbq'),
       'brow projection / HH vs MF c1 %+.1f / c2 %+.1f %% (lighter than humans), vs Aelari c1 %+.1f / c2 %+.1f %% (stronger than Aelari);  no scowl term, eye scale = VAL4 (unchanged); no low-light physiology' % (
           fd('c1', 'brow_projection_over_HH'), fd('c2', 'brow_projection_over_HH'), fe('c1', 'brow_projection_over_HH'), fe('c2', 'brow_projection_over_HH')))
fsheet('VA2_17_jaw_chin.jpg', 'Vael jaw / chin (ears hidden): low three-quarter and profile', ('jawl', 'jawp'),
       'jaw width / bizygomatic vs Aelari c1 %+.1f / c2 %+.1f %%, vs Fenn c1 %+.1f / c2 %+.1f %%, vs MF c1 %+.2f / c2 %+.2f %% (not material);  lower-face width / bizygomatic vs MF c1 %+.1f / c2 %+.1f %% (gracile)' % (
           fe('c1', 'jaw_width_over_bizygomatic'), fe('c2', 'jaw_width_over_bizygomatic'), fe('c1', 'jaw_width_over_bizygomatic@FN'), fe('c2', 'jaw_width_over_bizygomatic@FN'), fd('c1', 'jaw_width_over_bizygomatic'), fd('c2', 'jaw_width_over_bizygomatic'), fd('c1', 'lower_face_width_over_bizygomatic'), fd('c2', 'lower_face_width_over_bizygomatic')))
rows = []
for c in CFG:
    for v in ('hfront', 'hprof'): rows.append(('%s %s' % (c, v[1:]), [img('fres_%s_%s' % (c, k), v) for k in ('MF', 'SG', 'AE', 'FN')], ['vs Marchfolk', 'vs Sagekin', 'vs Aelari', 'vs Fenn'] if v == 'hfront' else None))
fr = lambda c: '  '.join('%s %.2f/%.2f/%.2f (%.2f)' % (r[:10], v['VA_vs_MF_rms_mm'], v['VA_vs_AE_rms_mm'], v['VA_vs_FN_rms_mm'], v['SG_vs_MF_rms_mm_human_baseline']) for r, v in HE['configs'][c]['face'].items())
sheet('VA2_18_face_regional_residuals.jpg', 'Vael R1 face residuals after similarity alignment (blue 0 .. red >= 4 mm on the Vael head): vs Marchfolk | Sagekin | Aelari | Fenn', rows, colw=380,
      note='region RMS mm  VA vs MF / AE / FN (human baseline SG vs MF)\nc1: %s\nc2: %s' % (fr('c1'), fr('c2')))
# 19 descriptor table visual
DK = ['cranial_height_over_stature', 'cranial_height_over_face', 'face_height_over_bizygomatic', 'lower_face_height_over_HH', 'bizygomatic_over_HH', 'cheekbone_height_over_HH', 'midface_projection_over_HH', 'brow_projection_over_HH', 'jaw_width_over_bizygomatic', 'lower_face_width_over_bizygomatic']
fig, axs = plt.subplots(2, 1, figsize=(17, 9.5))
for ax, c in zip(axs, ('c1', 'c2')):
    cd = HE['configs'][c]; allr = {**cd['canon_descriptors'], **{k: dict(**v) for k, v in cd['report'].items()}}
    def val(k, who):
        if k in cd['canon_descriptors']: return cd['canon_descriptors'][k][who] if who != 'VA' else cd['canon_descriptors'][k]['VA']
        return cd['report'][k][who]
    x = np.arange(len(DK)); w = 0.2
    for j, (who, col) in enumerate((('VA', '#e07a2e'), ('SG', '#6aa36a'), ('FN', '#4a78c2'), ('AE', '#7a4fb0'))):
        vals = [100 * (val(k, who) / val(k, 'MF') - 1) for k in DK]; ax.bar(x + (j - 1.5) * w, vals, w, color=col, label={'VA': 'Vael R1', 'SG': 'Sagekin', 'FN': 'frozen Fenn', 'AE': 'frozen Aelari'}[who])
        for xx, v in zip(x + (j - 1.5) * w, vals): ax.text(xx, v, '%+.1f' % v, fontsize=6, ha='center', va='bottom' if v >= 0 else 'top')
    ax.axhline(0, color='k', lw=0.7); ax.set_xticks(x); ax.set_xticklabels([k.replace('_over_', ' / ') for k in DK], fontsize=8, rotation=12); ax.set_ylabel('% vs Marchfolk'); ax.set_title('%s: face descriptors relative to Marchfolk (ears excluded, head-size removed)' % c, fontsize=10); ax.legend(fontsize=8)
fig.tight_layout(); fig.savefig(os.path.join(OUT, 'VA2_19_face_descriptor_table.jpg'), dpi=100); plt.close(fig)
EXJ = jl(EV + '/VA2_expression_sanity.json')
def exc(tag, e):
    k = [x for x in EXJ['expressions'] if x.split(' ')[0] == e][0]; v = EXJ['bodies'][tag][k]; return '%s  new selfx %d (orbit %d) flips %d' % (e, v['new_selfx_pairs'], v['new_selfx_in_orbit'], v['flipped_faces'])
sheet('VA2_20_expression_sanity.jpg', 'Expression sanity, provisional winner R1 on the family realization (MPFB 2.0.17 expression units, diagnostic; no facial weights / correctives authored)',
      [(c, [img('ex_%s_%s' % (c, e), 'f') for e in EX], [exc(CFG[c]['VA'], e) for e in EX]) for c in CFG], colw=300,
      note='baseline: original VAL4 / VALF178 (human-family face) with the same units — %s' % '  '.join('%s: %s' % (t, ' '.join('%s %d/%d' % (e.split(' ')[0], v['new_selfx_pairs'], v['flipped_faces']) for e, v in EXJ['bodies'][t].items())) for t in EXJ['bodies'] if not t.endswith('R1')))
# technical
rows = []
for c, K in CFG.items(): rows.append((c, [blend(img('src_' + K['VA'], v), img('fam_' + K['VA'], v)) for v in ('bfront', 'bprof', 'hq')] + [img('famw_' + K['VA'], 'hq')], ['source red / family blue', 'profile', 'head', 'family wire (v005 topology)']))
MAN = jl(EV + '/VAEL_RP3_bodyfam_propagation_manifest.json')
sheet('VA2_21_family_propagation_overlay.jpg', 'Vael R1 sources propagated to frozen MPFB Family Base v005 — R-6 source (red) over family realization (blue), same camera; topology unchanged', rows, colw=420,
      note='topology identity: ' + '  '.join('%s faces=%s uv=%s map=%s face-hash=%s |V - M hm08| %.1e' % (k, v['faces_equal'], v['uv_equal'], v['map_equal'], v['face_hash_equal'], v['V_eq_M_hm08']) for k, v in MAN['topology_identity_proof'].items()))
VA_ = {CFG[c]['VA']: jl('%s/val/%s_fam_validator_v2_D1-D6.json' % (W2, CFG[c]['VA'])) for c in CFG}; n1, n2 = CFG['c1']['VA'], CFG['c2']['VA']; st_ = sorted(VA_[n1]['stations'])
S = Image.new('RGB', (1200, 140 + 26 * (len(st_) + 2)), 'white'); d = ImageDraw.Draw(S)
d.text((14, 14), 'Vael R1 family candidates on frozen v005 — validator D1+D3+D4+D5+D6', fill=(0, 0, 0), font=font(20, True))
d.text((14, 44), 'margin = loops - contract minimum (red = 0).   %s: %d / 69   %s: %d / 69' % (n1, VA_[n1]['summary']['firm_pass_count'], n2, VA_[n2]['summary']['firm_pass_count']), fill=(0, 0, 0), font=font(16))
cw = [260, 150, 150, 150, 150, 150, 150]; y = 90
for i, t in enumerate(['station', 'c1 loops', 'c1 min', 'c1 margin', 'c2 loops', 'c2 min', 'c2 margin']): d.text((20 + sum(cw[:i]), y), t, fill=(0, 0, 0), font=font(15, True))
y += 28
for s in st_:
    a, b = VA_[n1]['stations'][s], VA_[n2]['stations'][s]; vals = [s, a['loops_v2'], a['required'], a['margin'], b['loops_v2'], b['required'], b['margin']]
    for i, t in enumerate(vals): d.text((20 + sum(cw[:i]), y), str(t), fill=(200, 30, 30) if (i in (3, 6) and t == 0) else (0, 0, 0), font=font(14))
    y += 26
S.save(os.path.join(OUT, 'VA2_22_validator_margins.jpg'), quality=88)
fig, ax = plt.subplots(figsize=(11, 4.5)); zs = ['face', 'ears', 'hand', 'foot', 'trunk', 'arm', 'leg', 'neck', 'head']; x = np.arange(len(zs)); okall = True
for i, n in enumerate((n1, n2)):
    au = jl('%s/audit/%s_fam_audit.json' % (W2, n))['density_pct_of_stature']; ax.bar(x + (i - 0.5) * 0.35, [au[z]['mean'] for z in zs], 0.35, label=n); okall &= all(au[z]['pass_mean'] for z in zs)
    ax.scatter(x, [au[z]['limit'] for z in zs], marker='_', s=600, color='k')
ax.set_xticks(x); ax.set_xticklabels(zs); ax.set_ylabel('mean edge / stature (%)'); ax.set_title('Vael R1 family density, 9 zones (black bar = limit): %s' % ('all pass' if okall else 'FAIL present')); ax.legend(); fig.tight_layout(); fig.savefig(os.path.join(OUT, 'VA2_23_density.jpg'), dpi=105); plt.close(fig)
dc = jl(EV + '/VAEL_deformation_comparison.json'); PN = ('shoulder_abd90_l', 'elbow_130_l', 'hip_flex90_l', 'knee_140_l', 'neck_rot45', 'trunk_twist30')
sheet('VA2_24_deformation.jpg', 'Vael R1 family candidates — Standard v1 deformation (source rig + carried MPFB weights, plain LBS; red = flipped faces)',
      [(n, [img('pose_%s_%s' % (n, p), 'v') for p in PN], ['%s %d (MF v005 %d)' % (p, dc[n]['poses'][p]['aelari_family'], dc[n]['poses'][p]['marchfolk_v005']) for p in PN]) for n in (n1, n2)], colw=360,
      note='flipped faces per pose, Vael family vs the frozen Marchfolk v005 realization of the same configuration class: worst excess %s; poses worse by > 5: %s' % ({n: dc[n]['worst_flip_excess'] for n in dc}, {n: dc[n]['poses_worse_by_more_than_5'] for n in dc}))
rows = []
for c, K in CFG.items():
    for lab, v in (('front', 'bfront'), ('profile', 'bprof')): rows.append(('%s %s' % (c, lab), [img('he_' + K[k], v) for k in ('VA', 'FN', 'AE', 'MF', 'SG')], ['Vael R1', 'frozen Fenn', 'frozen Aelari', 'Marchfolk', 'Sagekin'] if lab == 'front' else None))
sheet('VA2_25_final_three_elf_human_comparison.jpg', 'FINAL equal-height (178 cm) hidden-ear neutral comparison — Vael R1 | frozen Fenn | frozen Aelari | Marchfolk | Sagekin', rows, colw=340)
print('sheets done', len([f for f in os.listdir(OUT) if f.startswith('VA2_')]), flush=True)
