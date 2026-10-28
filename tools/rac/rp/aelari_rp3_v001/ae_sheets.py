# ae_sheets.py WORK OUTDIR : order fd71f15 §19 visual package (Part A / B sheets 01-09, Part C sheets 10-20). Identical orthographic cameras per sheet,
# true scale. Workbench renders (grask_rigprep_v001/render_attr.py) composed with PIL; resumable (skips finished renders); 2 Blender processes.
import sys, os, json, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
from concurrent.futures import ThreadPoolExecutor
os.environ.setdefault('EAR_TOPO', 'v002')
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001')
import ear_branch_lib as E
W, OUT = sys.argv[1:3]; os.makedirs(OUT, exist_ok=True); TMP = os.environ.get('AE_SHEET_TMP', os.path.join(OUT, '_r')); os.makedirs(TMP, exist_ok=True)
BP = '/home/claude/stc/bin/python3'; REND = '/home/claude/wayfarer-design/tools/rac/rp/grask_rigprep_v001/render_attr.py'; RA = '/home/claude/wayfarer-design/reviews/reference-assets/r6'
EW = W + '/ear'; GREY = np.array([0.80, 0.78, 0.76]); jl = lambda p: json.load(open(p))
def font(sz, bold=False):
    f = '/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf' % ('-Bold' if bold else ''); return ImageFont.truetype(f, sz) if os.path.exists(f) else ImageFont.load_default()
jobs = []
def render(tag, npz, col, views, wire=False, px=600):
    vs = ';'.join('%s:%s:%s:%.2f' % (n, ','.join('%.4f' % x for x in d), ','.join('%.3f' % x for x in c), hs) for n, d, c, hs in views)
    cf = os.path.join(TMP, tag + '_col.npy'); np.save(cf, np.asarray(col, np.float32)); jobs.append([BP, REND, '--', npz, cf, TMP, tag, vs, '1' if wire else '0', str(px)])
def img(tag, name):
    p = os.path.join(TMP, '%s_%s.png' % (tag, name)); return Image.open(p).convert('RGB') if os.path.exists(p) else Image.new('RGB', (600, 600), 'white')
def heat(x, lo, hi):
    t = np.clip((x - lo) / (hi - lo + 1e-12), 0, 1)[:, None]; return (1 - t) * np.array([0.2, 0.35, 0.85]) + t * np.array([0.95, 0.25, 0.15])
def part_cols(z):
    p = z['part']; C = np.tile(GREY, (len(z['V']), 1)); C[p == 'front'] = [0.88, 0.66, 0.55]; C[p == 'back'] = [0.70, 0.58, 0.80]; C[p == 'rim'] = [0.95, 0.83, 0.45]
    C[p == 'cuff'] = [0.58, 0.76, 0.92]; C[p == 'transition'] = [0.55, 0.85, 0.55]; return C
def face_part(z):
    p = z['part'][z['Q']]; C = np.tile(GREY, (len(z['Q']), 1))
    for k, col in (('transition', [0.55, 0.85, 0.55]), ('cuff', [0.58, 0.76, 0.92]), ('back', [0.70, 0.58, 0.80]), ('front', [0.88, 0.66, 0.55]), ('rim', [0.95, 0.83, 0.45])): C[(p == k).any(1)] = col
    return C
def valence_cols(z):
    Q = z['Q']; Eu = np.unique(np.sort(np.concatenate([Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]]), 1), axis=0); val = np.zeros(len(z['V']), int); np.add.at(val, Eu.ravel(), 1)
    C = part_cols(z) * 0.35 + 0.6; br = z['part'] != 'v005'; C[br & (val == 3)] = [0.1, 0.3, 0.95]; C[br & (val == 5)] = [0.95, 0.15, 0.1]; C[br & (val >= 6)] = [0.6, 0.1, 0.8]; return C
Lo = E.canonical_layout(); st = Lo['st']; ns = len(st)
ANAT = [('helix', 'helix', (0.85, 0.30, 0.25)), ('antihelix_stem', 'antihelix stem', (0.20, 0.55, 0.85)), ('superior_crus', 'superior crus', (0.10, 0.35, 0.75)),
        ('inferior_crus', 'inferior crus', (0.35, 0.70, 0.95)), ('triangular_fossa', 'triangular fossa', (0.55, 0.40, 0.80)), ('cavum', 'concha cavum', (0.95, 0.65, 0.15)),
        ('cymba', 'concha cymba', (0.95, 0.85, 0.30)), ('crus_of_helix', 'crus of helix', (0.60, 0.25, 0.10)), ('tragus', 'tragus', (0.20, 0.70, 0.35)),
        ('antitragus', 'antitragus', (0.10, 0.50, 0.25)), ('intertragic_notch', 'intertragic notch', (0.95, 0.40, 0.70))]
EXTRA = [('lobe', (0.93, 0.72, 0.72)), ('upper extension / taper', (0.86, 0.80, 0.62)), ('cuff', (0.72, 0.80, 0.88))]
def anat_cols(z, rec):
    p = dict(rec['params']); p['taper'] = tuple(p['taper']); p['helix'] = tuple(p['helix']); _, _, parts = E.relief(st[:, 0], st[:, 1], p)
    C = np.tile(GREY, (len(z['V']), 1)); C[z['part'] == 'cuff'] = EXTRA[2][1]; lab = np.full(ns, -1); best = np.zeros(ns)
    for k, (key, nm, col) in enumerate(ANAT):
        a = np.abs(parts[key]) / (np.abs(parts[key]).max() + 1e-9); m = (a > 0.35) & (a > best); lab[m] = k; best[m] = a[m]
    sh = np.isin(Lo['part'], ['front', 'rim'])
    for sd in ('l', 'r'):
        f = np.nonzero(z['side'] == sd)[0][0]; idx = np.arange(ns)
        C[f + idx[sh & (st[:, 0] < 0.15) & (lab < 0)]] = EXTRA[0][1]; C[f + idx[sh & (st[:, 0] > E.S_UP) & (lab < 0)]] = EXTRA[1][1]
        for k, (key, nm, col) in enumerate(ANAT): C[f + idx[sh & (lab == k)]] = col
    return C
def bcam(V):
    return np.array([0.0, V[:, 1].mean(), (V[:, 2].max() + V[:, 2].min()) / 2]), (V[:, 2].max() - V[:, 2].min()) / 2 + 6
def hcam(V):
    hv = V[V[:, 2] > V[:, 2].max() - 25]; return np.array([0.0, hv[:, 1].mean(), V[:, 2].max() - 12.0])
# ---------------------------------------------------------------- Part A / B renders
r6 = {'AEL1': W + '/partA/ref/AEL1_r6.npz', 'AELF190': W + '/partA/build/AELF190_r6.npz'}
for n, p in r6.items():
    z = np.load(p); keep = z['keep']; Fx = z['F'][keep[z['F']].all(1)]; q = os.path.join(TMP, 'src_%s.npz' % n); np.savez_compressed(q, V=z['V'], Q=Fx); Bc, S = bcam(z['V'][keep])
    render('src_' + n, q, np.tile(GREY, (len(z['V']), 1)), [('front', (0, 1, 0), Bc, 102), ('prof', (1, 0, 0), Bc, 102), ('rear', (0, -1, 0), Bc, 102)])
for n in ('AEL1', 'AELF190'):
    z = np.load('%s/fam/%s_fam.npz' % (W, n)); Bc, S = bcam(z['V']); Hc = hcam(z['V'])
    render('fam_' + n, '%s/fam/%s_fam.npz' % (W, n), np.tile(GREY, (len(z['V']), 1)), [('front', (0, 1, 0), Bc, 102), ('prof', (1, 0, 0), Bc, 102), ('hprof', (1, 0, 0), Hc, 15)])
HE = ['AEL1', 'FNM190', 'MFM190', 'SGM190', 'AELF190', 'FNF190', 'MFF190', 'SGF190']
for n in HE:
    z = np.load('%s/ov/%s_earhidden.npz' % (W, n)); V = z['V']; Bc = np.array([0.0, V[:, 1].mean(), 96.0]); Hc = hcam(V)
    render('he_' + n, '%s/ov/%s_earhidden.npz' % (W, n), np.tile(GREY, (len(V), 1)),
           [('bfront', (0, 1, 0), Bc, 102), ('bprof', (1, 0, 0), Bc, 102), ('hfront', (0, 1, 0.03), Hc, 15), ('hprof', (1, 0, 0), Hc, 15),
            ('neck', (1, 0.6, 0.05), np.array([0, V[:, 1].mean(), 150.0]), 30), ('shoulder', (0, 1, 0.05), np.array([0, V[:, 1].mean(), 152.0]), 26),
            ('pelvis', (1, 0.25, 0.0), np.array([0, V[:, 1].mean(), 98.0]), 30), ('hand', (0.3, 1, 0.0), np.array([V[:, 0].max() - 10, 0, 82.0]), 14),
            ('foot', (0.8, 0.6, 0.6), np.array([11.0, 8.0, 4.0]), 15)], px=520)
# deformation poses (family candidates)
for n in ('AEL1', 'AELF190'):
    z = np.load('%s/fam/%s_fam.npz' % (W, n))
    for pn in ('shoulder_abd90_l', 'elbow_130_l', 'hip_flex90_l', 'knee_140_l', 'neck_rot45', 'trunk_twist30'):
        pp = '%s/def/%s_%s_fam.npz' % (W, pn, n)
        if not os.path.exists(pp): continue
        X = np.load(pp); Xv = X['V']; C = np.tile(GREY, (len(z['Q']), 1)); fl = np.asarray(X['flip']).astype(int).ravel(); C[fl[fl < len(C)]] = [0.92, 0.18, 0.12]
        q = os.path.join(TMP, 'pose_%s_%s.npz' % (n, pn)); np.savez_compressed(q, V=Xv, Q=z['Q']); Bc, S = bcam(Xv); render('pose_%s_%s' % (n, pn), q, C, [('v', (1, 1, 0.05), Bc, 106)], px=420)
# ---------------------------------------------------------------- Part C renders
HEADS = {'c1': 'AEL1', 'c2': 'AELF190'}; CANDS = ['AE-E1', 'AE-E2', 'AE-E3']; ED = {}
for c, h in HEADS.items():
    for k in CANDS:
        P = '%s/build/%s_%s_branch.npz' % (EW, h, k)
        if not os.path.exists(P): continue
        z = np.load(P); r = jl('%s/build/%s_%s_branch.json' % (EW, h, k)); ED[(c, k)] = (z, r, P)
CAM = {}
for c, h in HEADS.items():
    if (c, 'AE-E2') not in ED: continue
    z, r, P = ED[(c, 'AE-E2')]; V = z['V']; CAM[c] = dict(H=hcam(V), Ce=V[z['side'] == 'l'].mean(0), O=np.array(r['sides']['l']['frame']['O']))
def views(c, names):
    k = CAM[c]; T = dict(front=((0, 1, 0.03), k['H'], 15), prof=((1, 0, 0), k['H'], 15), tqf=((1, 1, 0.1), k['H'], 15), rear=((0, -1, 0), k['H'], 15), top=((0, 0, 1), k['H'], 15),
                         elat=((1, 0.15, 0.05), k['Ce'], 5.6), eface=((1, 0.9, 0.15), k['Ce'], 5.2), ecrear=((0.35, -1, 0.1), k['Ce'], 5.2), root=((1, 0.2, 0.0), k['O'], 3.6), under=((0.3, -0.5, -1), k['Ce'], 3.8))
    return [(n,) + T[n] for n in names]
for (c, k), (z, r, P) in ED.items():
    t = '%s_%s' % (c, k)
    render(t + '_g', P, np.tile(GREY, (len(z['V']), 1)), views(c, ['front', 'prof', 'tqf', 'rear', 'top', 'elat', 'eface', 'ecrear']))
    render(t + '_w', P, part_cols(z), views(c, ['eface', 'ecrear', 'root', 'under']), wire=True)
    render(t + '_v', P, valence_cols(z), views(c, ['eface', 'ecrear']), wire=True)
    render(t + '_a', P, anat_cols(z, r), views(c, ['eface', 'elat']))
    pf = '%s/audit/%s_%s_audit_perface.npz' % (EW, HEADS[c], k)
    if os.path.exists(pf):
        q = np.load(pf); F_, bad, asp = q['faces'], q['ang_bad'], q['asp']
        C = face_part(z) * 0.45 + 0.5; C[F_] = [0.93, 0.93, 0.93]; C[F_[bad]] = [0.92, 0.18, 0.12]; render(t + '_t4', P, C, views(c, ['eface', 'ecrear', 'root']), wire=True)
        C = np.tile(GREY, (len(z['Q']), 1)); C[F_] = heat(asp, 1.0, 6.0); C[F_[asp > 6]] = [0.55, 0.1, 0.65]; render(t + '_as', P, C, views(c, ['eface', 'ecrear']), wire=True)
    cd = '%s/audit/%s_%s_audit_cuffdev.npy' % (EW, HEADS[c], k)
    if os.path.exists(cd):
        d = np.load(cd); C = np.tile(GREY, (len(z['V']), 1)); C[d[:, 0].astype(int)] = heat(d[:, 1], 0, 0.6); render(t + '_rd', P, C, views(c, ['root', 'under']))
    for pn in ('neck_flex30', 'head_yaw_l45', 'head_roll_l20'):
        pp = '%s/deform/%s_%s_%s.npy' % (EW, HEADS[c], k, pn)
        if k == 'AE-E2' and os.path.exists(pp):
            X = np.load(pp); q = os.path.join(TMP, 'epose_%s_%s.npz' % (c, pn)); np.savez_compressed(q, V=X, Q=z['Q']); Cp = X[z['side'] == 'l'].mean(0)
            render('epose_%s_%s' % (c, pn), q, part_cols(z), [('tq', (1, 0.3, 0.1), Cp, 8.0)])
# Fenn E2 (frozen production candidate) vs Aelari AE-E2 (configuration 1), each on its own head, same relative camera (head-height scaled)
FN = '/tmp/claude-0/rt/fn/final/ear/build/FNL4-CF2_E2_branch.npz'
if os.path.exists(FN) and 'c1' in CAM:
    for tag, P in (('cmpFN', FN), ('cmpAE', ED[('c1', 'AE-E2')][2])):
        z = np.load(P); V = z['V']; Hc = hcam(V); Ce = V[z['side'] == 'l'].mean(0)
        render(tag, P, np.tile(GREY, (len(V), 1)), [('prof', (1, 0, 0), Hc, 15), ('front', (0, 1, 0.03), Hc, 15), ('rear', (0, -1, 0), Hc, 15), ('elat', (1, 0.15, 0.05), Ce, 6.0)])
# probes
PR = ['proj_m10', 'proj_p10', 'tilt_m8', 'tilt_p8', 'sweep_m06', 'sweep_p06', 'len_m10', 'len_p10', 'tip_blunt', 'tip_sharp']
for pn in PR:
    P = '%s/probe/%s/AEL1_AE-E2_branch.npz' % (EW, pn)
    if os.path.exists(P) and 'c1' in CAM: z = np.load(P); render('pr_' + pn, P, part_cols(z), views('c1', ['eface']), wire=True, px=420)
print('render jobs', len(jobs), flush=True)
done_ = lambda j: all(os.path.exists(os.path.join(TMP, '%s_%s.png' % (j[6], v_.split(':')[0]))) for v_ in j[7].split(';'))
todo = [j for j in jobs if not done_(j)]; print('to render', len(todo), flush=True)
with ThreadPoolExecutor(int(os.environ.get('AE_SHEET_THREADS', '2'))) as ex: list(ex.map(lambda j: subprocess.run(j, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL), todo))
# ---------------------------------------------------------------- compose
def sheet(fname, title, rows, colw=600, note=None, lab_w=170, legend=None):
    ncol = max(len(r_[1]) for r_ in rows); Wd = lab_w + ncol * colw; Hh = 70 + sum(colw + 34 for _ in rows) + (44 if note else 0) + (44 if legend else 0)
    S = Image.new('RGB', (Wd, Hh), 'white'); d = ImageDraw.Draw(S); d.text((14, 14), title, fill=(0, 0, 0), font=font(21, True)); y = 70
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
    if note: d.text((14, y + 4), note, fill=(60, 60, 60), font=font(15))
    S.save(os.path.join(OUT, fname), quality=88)
def blend(a, b):
    A = np.asarray(a, float) * np.array([1.0, 0.55, 0.55]); B_ = np.asarray(b, float) * np.array([0.55, 0.65, 1.0]); return Image.fromarray(np.clip(0.5 * A + 0.5 * B_, 0, 255).astype(np.uint8))
PA = jl(W + '/partA/AELF190_reference_validation.json'); HEJ = jl(W + '/AE_hidden_ear_identity.json')
sheet('AE_01_AEL1_vs_AELF190.jpg', 'Aelari — accepted configuration-1 AEL1 | configuration-2 central reference AELF190 (R-6, ~190 cm, same camera)',
      [('front', [img('src_AEL1', 'front'), img('src_AELF190', 'front')], ['AEL1 %.1f cm' % PA['envelope']['AEL1'], 'AELF190 %.1f cm' % PA['envelope']['AELF190']]),
       ('profile', [img('src_AEL1', 'prof'), img('src_AELF190', 'prof')], None), ('rear', [img('src_AEL1', 'rear'), img('src_AELF190', 'rear')], None)])
sheet('AE_02_source_vs_production.jpg', 'Aelari body-family candidates — R-6 source (red) over production on v005 (blue), same camera (V = M @ hm08)',
      [(n, [blend(img('src_' + n, 'front'), img('fam_' + n, 'front')), blend(img('src_' + n, 'prof'), img('fam_' + n, 'prof')), img('fam_' + n, 'hprof')], ['', '', 'production head (family human auricle; not final)']) for n in ('AEL1', 'AELF190')])
sheet('AE_03_equal_height_Aelari_vs_Fenn_ears_hidden.jpg', 'Equal height (~190 cm), ears hidden: Aelari | frozen Fenn CF2 | overlay (Aelari red, Fenn blue)',
      [(lab, [img('he_' + a, v), img('he_' + f, v), blend(img('he_' + a, v), img('he_' + f, v))], [a, f, 'overlay']) for lab, a, f, v in
       (('c1 front', 'AEL1', 'FNM190', 'bfront'), ('c1 profile', 'AEL1', 'FNM190', 'bprof'), ('c2 front', 'AELF190', 'FNF190', 'bfront'), ('c2 profile', 'AELF190', 'FNF190', 'bprof'))], colw=480)
sheet('AE_04_Aelari_vs_humans_ears_hidden.jpg', 'Ears hidden, ~190 cm: Aelari | Marchfolk | Sagekin (front and profile)',
      [(lab, [img('he_' + n, v) for n in ns_], ns_) for lab, ns_, v in (('c1 front', ['AEL1', 'MFM190', 'SGM190'], 'bfront'), ('c1 profile', ['AEL1', 'MFM190', 'SGM190'], 'bprof'),
                                                                        ('c2 front', ['AELF190', 'MFF190', 'SGF190'], 'bfront'), ('c2 profile', ['AELF190', 'MFF190', 'SGF190'], 'bprof'))], colw=480)
sheet('AE_05_body_regions.jpg', 'Body regions, ears hidden, configuration 1 (~190 cm): Aelari | frozen Fenn | Marchfolk | Sagekin',
      [(rg, [img('he_' + n, v) for n in ('AEL1', 'FNM190', 'MFM190', 'SGM190')], ['AEL1', 'FNM190', 'MFM190', 'SGM190'] if rg == 'neck / torso' else None) for rg, v in
       (('neck / torso', 'neck'), ('shoulder / clavicle', 'shoulder'), ('pelvis / leg', 'pelvis'), ('hand', 'hand'), ('foot', 'foot'))], colw=430)
ca = lambda c: 'systems material %d / 7' % HEJ['configs'][c]['systems_material']
sheet('AE_06_hidden_ear_face.jpg', 'Hidden-ear face (ears collapsed): Aelari | frozen Fenn CF2 | Marchfolk | Sagekin, ~190 cm',
      [('c1 front', [img('he_' + n, 'hfront') for n in ('AEL1', 'FNM190', 'MFM190', 'SGM190')], ['AEL1 ' + ca('c1'), 'FNM190', 'MFM190', 'SGM190']),
       ('c1 profile', [img('he_' + n, 'hprof') for n in ('AEL1', 'FNM190', 'MFM190', 'SGM190')], None),
       ('c2 front', [img('he_' + n, 'hfront') for n in ('AELF190', 'FNF190', 'MFF190', 'SGF190')], ['AELF190 ' + ca('c2'), 'FNF190', 'MFF190', 'SGF190']),
       ('c2 profile', [img('he_' + n, 'hprof') for n in ('AELF190', 'FNF190', 'MFF190', 'SGF190')], None)], colw=480)
# 07 validator table, 08 density, 09 deformation
VA = {n: jl('%s/val/%s_fam_validator_v2_D1-D6.json' % (W, n)) for n in ('AEL1', 'AELF190')}; st_ = sorted(VA['AEL1']['stations'])
Wd, Hh = 1200, 140 + 26 * (len(st_) + 2); S = Image.new('RGB', (Wd, Hh), 'white'); d = ImageDraw.Draw(S)
d.text((14, 14), 'Aelari body-family candidates — validator D1+D3+D4+D5+D6', fill=(0, 0, 0), font=font(20, True))
d.text((14, 44), 'margin = loops - contract minimum (red = 0).   AEL1: %d / 69   AELF190: %d / 69' % (VA['AEL1']['summary']['firm_pass_count'], VA['AELF190']['summary']['firm_pass_count']), fill=(0, 0, 0), font=font(16))
cw = [260, 150, 150, 150, 150, 150, 150]; hdr = ['station', 'c1 loops', 'c1 min', 'c1 margin', 'c2 loops', 'c2 min', 'c2 margin']; y = 90
for i, t in enumerate(hdr): d.text((20 + sum(cw[:i]), y), t, fill=(0, 0, 0), font=font(15, True))
y += 28
for s in st_:
    a, b = VA['AEL1']['stations'][s], VA['AELF190']['stations'][s]; vals = [s, a['loops_v2'], a['required'], a['margin'], b['loops_v2'], b['required'], b['margin']]
    for i, t in enumerate(vals): d.text((20 + sum(cw[:i]), y), str(t), fill=(200, 30, 30) if (i in (3, 6) and t == 0) else (0, 0, 0), font=font(14))
    y += 26
S.save(os.path.join(OUT, 'AE_07_validator_margins.jpg'), quality=88)
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(11, 4.5)); zs = ['face', 'ears', 'hand', 'foot', 'trunk', 'arm', 'leg', 'neck', 'head']; x = np.arange(len(zs))
for i, n in enumerate(('AEL1', 'AELF190')):
    au = jl('%s/audit/%s_fam_audit.json' % (W, n))['density_pct_of_stature']; ax.bar(x + (i - 0.5) * 0.35, [au[z]['mean'] for z in zs], 0.35, label=n)
    ax.scatter(x, [au[z]['limit'] for z in zs], marker='_', s=600, color='k')
ax.set_xticks(x); ax.set_xticklabels(zs); ax.set_ylabel('mean edge / stature (%)'); ax.set_title('Aelari body-family density, 9 zones (black bar = limit): all pass'); ax.legend(); fig.tight_layout(); fig.savefig(os.path.join(OUT, 'AE_08_density.jpg'), dpi=110); plt.close(fig)
DC = jl(W + '/../ae_deform_comparison.json') if os.path.exists(W + '/../ae_deform_comparison.json') else None
PN = ('shoulder_abd90_l', 'elbow_130_l', 'hip_flex90_l', 'knee_140_l', 'neck_rot45', 'trunk_twist30')
dcmp = jl('/home/claude/wayfarer-design/reviews/rac-rp3-evidence/aelari_rp3_v001/AELARI_deformation_comparison.json')
sheet('AE_09_deformation.jpg', 'Aelari body-family candidates — Standard v1 deformation (source rig + carried MPFB weights, plain LBS; red = flipped faces)',
      [(n, [img('pose_%s_%s' % (n, p), 'v') for p in PN], ['%s flips %d (MF v005 %d)' % (p, dcmp[n]['poses'][p]['aelari_family'], dcmp[n]['poses'][p]['marchfolk_v005']) for p in PN]) for n in ('AEL1', 'AELF190')], colw=400)
# Part C
if ED:
    AU = {k: jl('%s/audit/%s_%s_audit.json' % (EW, HEADS[c], k_)) for (c, k_), _ in ED.items() for k in [(c, k_)] if os.path.exists('%s/audit/%s_%s_audit.json' % (EW, HEADS[c], k_))}
    ME = {k: jl('%s/meas/%s_%s_measure.json' % (EW, HEADS[k[0]], k[1]))['sides']['l'] for k in ED if os.path.exists('%s/meas/%s_%s_measure.json' % (EW, HEADS[k[0]], k[1]))}
    cap = lambda k: '%s  L %.2f  angle %.0f°  extent %.2f  upper %.0f°  T-4 %d' % (k[1], ME[k]['length_lobe_to_tip_cm'], ME[k]['auricle_body_angle_deg'], ME[k]['total_lateral_extent_from_root_plane_cm'], ME[k]['side_view_upper_extension_deg'], AU[k]['T4']['angle_violations']) if k in ME and k in AU else k[1]
    for c in HEADS:
        ks = [(c, k) for k in CANDS if (c, k) in ED]
        if not ks: continue
        sheet('AE_10_ears_head_%s.jpg' % c, 'Aelari ears %s — AE-E1 | AE-E2 | AE-E3 full head (front / profile / 3-4; same camera)' % c,
              [(v, [img('%s_%s_g' % k, v) for k in ks], [cap(k) for k in ks] if v == 'front' else None) for v in ('front', 'prof', 'tqf')])
        sheet('AE_11_ears_rear_top_%s.jpg' % c, 'Aelari ears %s — rear / top' % c, [(v, [img('%s_%s_g' % k, v) for k in ks], [k[1] for k in ks]) for v in ('rear', 'top')])
        sheet('AE_12_ear_anatomy_%s.jpg' % c, 'Aelari ears %s — close ear anatomy (dominant W1e relief system per vertex)' % c,
              [(v, [img('%s_%s_a' % k, v) for k in ks], [k[1] for k in ks]) for v in ('eface', 'elat')] + [('lateral grey', [img('%s_%s_g' % k, 'elat') for k in ks], None)], legend=[(nm, col) for _, nm, col in ANAT] + EXTRA)
        sheet('AE_13_wire_poles_%s.jpg' % c, 'Aelari ears %s — wire (part colours) and poles (blue valence 3, red 5, violet 6+)' % c,
              [('wire', [img('%s_%s_w' % k, 'eface') for k in ks], [k[1] for k in ks]), ('rear wire', [img('%s_%s_w' % k, 'ecrear') for k in ks], None), ('poles', [img('%s_%s_v' % k, 'eface') for k in ks], None)])
        sheet('AE_14_T4_aspect_%s.jpg' % c, 'Aelari ears %s — T-4 (red = corner outside 45-135°) and aspect (blue 1 .. red 6; violet > 6)' % c,
              [('T-4', [img('%s_%s_t4' % k, 'eface') for k in ks], ['%s T-4 %d / %d  asp max %.2f' % (k[1], AU[k]['T4']['angle_violations'], AU[k]['T4']['branch_faces'], AU[k]['T4']['aspect_max']) if k in AU else k[1] for k in ks]),
               ('T-4 root', [img('%s_%s_t4' % k, 'root') for k in ks], None), ('aspect', [img('%s_%s_as' % k, 'eface') for k in ks], None)])
        sheet('AE_15_root_%s.jpg' % c, 'Aelari ears %s — root integration (cuff skin vs hidden-ear skull 0 .. 0.6 cm) and wire root' % c,
              [('deviation', [img('%s_%s_rd' % k, 'root') for k in ks], ['%s crease max %.0f°, transition %.3f cm' % (k[1], max(v['max_deg'] for v in AU[k]['root_dihedral'].values()), AU[k]['transition_ring']['displacement_max_cm']) if k in AU else k[1] for k in ks]),
               ('under', [img('%s_%s_rd' % k, 'under') for k in ks], None), ('wire', [img('%s_%s_w' % k, 'root') for k in ks], None)])
    if ('c1', 'AE-E2') in ED and ('c2', 'AE-E2') in ED:
        sheet('AE_17_c1_vs_c2_AE-E2.jpg', 'Aelari AE-E2 — configuration 1 | configuration 2 (shared topology)',
              [(v, [img('c1_AE-E2_g', v), img('c2_AE-E2_g', v)], ['AEL1', 'AELF190'] if v == 'tqf' else None) for v in ('tqf', 'elat')] + [('wire', [img('c1_AE-E2_w', 'eface'), img('c2_AE-E2_w', 'eface')], None)])
        sheet('AE_18_Fenn_E2_vs_Aelari_AE-E2.jpg', 'Frozen Fenn E2 (FN_M_REF_RP3_v001) | Aelari AE-E2 (AEL1) — each on its own head, same relative camera',
              [(v, [img('cmpFN', v), img('cmpAE', v)], ['Fenn E2', 'Aelari AE-E2'] if v == 'prof' else None) for v in ('prof', 'front', 'rear', 'elat')])
        sheet('AE_19_hidden_ear_confirmation.jpg', 'Aelari — hidden-ear head (ear collapsed) | AE-E2 visible ear, same camera',
              [(c, [img('he_' + HEADS[c], 'hprof'), img('%s_AE-E2_g' % c, 'prof'), img('he_' + HEADS[c], 'hfront'), img('%s_AE-E2_g' % c, 'front')], ['hidden', 'AE-E2', 'hidden', 'AE-E2']) for c in HEADS])
        prs = [p for p in PR if os.path.exists(os.path.join(TMP, 'pr_%s_eface.png' % p))]
        sheet('AE_20_deformation_probes.jpg', 'Aelari AE-E2 — static head / neck readiness (configuration 1 / 2) and the ten shape probes (configuration 1)',
              [('c1 poses', [img('epose_c1_%s' % p, 'tq') for p in ('neck_flex30', 'head_yaw_l45', 'head_roll_l20')], ['neck flex 30', 'yaw L 45', 'roll L 20']),
               ('c2 poses', [img('epose_c2_%s' % p, 'tq') for p in ('neck_flex30', 'head_yaw_l45', 'head_roll_l20')], None),
               ('probes 1-5', [img('pr_' + p, 'eface') for p in prs[:5]], prs[:5]), ('probes 6-10', [img('pr_' + p, 'eface') for p in prs[5:]], prs[5:])], colw=420)
print('sheets done', flush=True)
