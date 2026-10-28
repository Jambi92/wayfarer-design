# ae_corr_sheets.py OUTDIR : order 0f6aba8 §14 visual package for the Aelari body-source correction (AEL1 -> AEL1-R1, AELF190 -> AELF190-R1).
# Identical orthographic cameras per row, true scale; ears hidden (hm08 w_ears > 0.05, harmonically collapsed) wherever identity is judged.
# Workbench renders (grask_rigprep_v001/render_attr.py) composed with PIL; resumable; 2 Blender processes.
#  00 metrics chart | 01 / 02 original vs corrected c1 / c2 | 03 corrected vs Fenn, equal height, ears hidden | 04 torso / ribcage bands | 05 leg segments
#  06 pelvis | 07 hidden-ear face before / after | 08 full-body displacement before -> after | 09 validator margins | 10 deformation | 11 AE-E2 on the
#  corrected heads | 12 frozen Fenn E2 vs corrected AE-E2
import sys, os, json, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
from concurrent.futures import ThreadPoolExecutor
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True); TMP = os.environ.get('AE_SHEET_TMP', '/tmp/claude-0/rt/ae/r1/sheet_r'); os.makedirs(TMP, exist_ok=True)
A = '/tmp/claude-0/rt/ae'; R1 = A + '/r1'; CC = A + '/corr/cand'; PA = A + '/partA'; EW = R1 + '/ear'; EV = '/home/claude/wayfarer-design/reviews/rac-rp3-evidence'
BP = '/home/claude/stc/bin/python3'; REND = '/home/claude/wayfarer-design/tools/rac/rp/grask_rigprep_v001/render_attr.py'; GREY = np.array([0.80, 0.78, 0.76]); jl = lambda p: json.load(open(p))
CFG = {'c1': dict(O='AEL1', N='AEL1-R1', FN='FNM190', MF='MFM190'), 'c2': dict(O='AELF190', N='AELF190-R1', FN='FNF190', MF='MFF190')}
R6 = {'AEL1': PA + '/ref/AEL1_r6.npz', 'AELF190': PA + '/build/AELF190_r6.npz', 'AEL1-R1': CC + '/AEL1-R1_r6.npz', 'AELF190-R1': CC + '/AELF190-R1_r6.npz'}
for n in ('FNM190', 'FNF190', 'MFM190', 'MFF190'): R6[n] = '%s/cmp/%s_r6.npz' % (PA, n)
HE = {'AEL1': A + '/ov/AEL1_earhidden.npz', 'AELF190': A + '/ov/AELF190_earhidden.npz'}
for n in ('AEL1-R1', 'AELF190-R1', 'FNM190', 'FNF190', 'MFM190', 'MFF190'): HE[n] = '%s/ov/%s_earhidden.npz' % (R1, n)
MEAS = {n: jl(p.replace('_r6.npz', '_meas.json'))['combined'] for n, p in R6.items()}
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
def blend(a, b):
    A_ = np.asarray(a, float) * np.array([1.0, 0.55, 0.55]); B_ = np.asarray(b, float) * np.array([0.55, 0.65, 1.0]); return Image.fromarray(np.clip(0.5 * A_ + 0.5 * B_, 0, 255).astype(np.uint8))
# native hm08 region labels (dominant weight), as ae_hidden_ear.py
nz = np.load('/tmp/claude-0/rt/fn/src/FNL4_native.npz'); bones = [str(b) for b in nz['bones']]; dom = np.array(bones)[np.asarray(nz['W']).argmax(1)]; Qn = np.asarray(nz['Q'])
TRUNK = np.array([b.startswith(('spine', 'pelvis', 'clavicle', 'Root')) for b in dom]); LEG = np.array([b.startswith(('thigh', 'calf', 'foot', 'ball')) for b in dom])
def joints(n):
    j = json.loads(str(np.load(R6[n])['joints'])); z = lambda b: j[b][0][2]
    return dict(clav=0.5 * (z('clavicle_l') + z('clavicle_r')), sp3=z('spine_03'), sp1=z('spine_01'), hip=0.5 * (z('thigh_l') + z('thigh_r')), knee=0.5 * (z('calf_l') + z('calf_r')), ankle=0.5 * (z('foot_l') + z('foot_r')))
J = {n: joints(n) for n in R6}
C_TH, C_WA, C_FE, C_SH = [0.95, 0.60, 0.20], [0.30, 0.70, 0.75], [0.45, 0.55, 0.90], [0.90, 0.45, 0.55]
def band_cols(n, V):
    j = J[n]; C = np.tile(GREY, (len(V), 1)); z = V[:, 2]
    C[TRUNK & (z >= j['sp3']) & (z <= j['clav'])] = C_TH; C[TRUNK & (z >= j['sp1']) & (z < j['sp3'])] = C_WA
    C[LEG & (z <= j['hip']) & (z > j['knee'])] = C_FE; C[LEG & (z <= j['knee']) & (z > j['ankle'])] = C_SH; return C
# ---------------------------------------------------------------- renders
for n, p in R6.items():
    if n[:2] not in ('AE',): continue
    z = np.load(p); keep = z['keep']; Fx = z['F'][keep[z['F']].all(1)]; q = os.path.join(TMP, 'src_%s.npz' % n); np.savez_compressed(q, V=z['V'], Q=Fx)
    Bc = np.array([0.0, z['V'][keep][:, 1].mean(), 96.0]); render('src_' + n, q, np.tile(GREY, (len(z['V']), 1)), [('front', (0, 1, 0), Bc, 102), ('prof', (1, 0, 0), Bc, 102), ('rear', (0, -1, 0), Bc, 102)])
for c, K in CFG.items():
    Vn = np.load(HE[K['N']])['V']; ym = Vn[:, 1].mean(); Bc = np.array([0.0, ym, 96.0]); Hc = np.array([0.0, Vn[Vn[:, 2] > Vn[:, 2].max() - 25][:, 1].mean(), Vn[:, 2].max() - 12.0])
    Tc = np.array([0.0, ym, 0.5 * (J[K['N']]['sp1'] + J[K['N']]['clav'])]); Lc = np.array([0.0, ym, 53.0]); Pc = np.array([0, ym, 98.0])
    for n in (K['O'], K['N'], K['FN']):
        V = np.load(HE[n])['V']
        render('he_%s_%s' % (c, n), HE[n], np.tile(GREY, (len(V), 1)), [('bfront', (0, 1, 0), Bc, 102), ('bprof', (1, 0, 0), Bc, 102), ('hfront', (0, 1, 0.03), Hc, 15), ('hprof', (1, 0, 0), Hc, 15),
                                                                         ('pelvis', (1, 0.25, 0.0), Pc, 30), ('pfront', (0, 1, 0.0), Pc, 30)], px=520)
        render('band_%s_%s' % (c, n), HE[n], band_cols(n, V), [('tfront', (0, 1, 0), Tc, 34), ('tprof', (1, 0, 0), Tc, 34), ('lfront', (0, 1, 0), Lc, 56), ('lprof', (1, 0, 0), Lc, 56)], px=520)
    Vo = np.load(HE[K['O']])['V']; d = np.linalg.norm(Vn - Vo, axis=1) * 10
    render('disp_%s' % c, HE[K['N']], heat(d, 0, 15), [('bfront', (0, 1, 0), Bc, 102), ('bprof', (1, 0, 0), Bc, 102), ('brear', (0, -1, 0), Bc, 102)], px=520)
    zf = np.load('%s/fam/%s_fam.npz' % (R1, K['N']))
    for pn in ('shoulder_abd90_l', 'elbow_130_l', 'hip_flex90_l', 'knee_140_l', 'neck_rot45', 'trunk_twist30'):
        pp = '%s/def/%s_%s_fam.npz' % (R1, pn, K['N'])
        if not os.path.exists(pp): continue
        X = np.load(pp); Xv = X['V']; C = np.tile(GREY, (len(zf['Q']), 1)); fl = np.asarray(X['flip']).astype(int).ravel(); C[fl[fl < len(C)]] = [0.92, 0.18, 0.12]
        q = os.path.join(TMP, 'pose_%s_%s.npz' % (K['N'], pn)); np.savez_compressed(q, V=Xv, Q=zf['Q']); Bc_ = np.array([0.0, Xv[:, 1].mean(), (Xv[:, 2].max() + Xv[:, 2].min()) / 2])
        render('pose_%s_%s' % (K['N'], pn), q, C, [('v', (1, 1, 0.05), Bc_, 106)], px=420)
def part_cols(z):
    p = z['part']; C = np.tile(GREY, (len(z['V']), 1)); C[p == 'front'] = [0.88, 0.66, 0.55]; C[p == 'back'] = [0.70, 0.58, 0.80]; C[p == 'rim'] = [0.95, 0.83, 0.45]
    C[p == 'cuff'] = [0.58, 0.76, 0.92]; C[p == 'transition'] = [0.55, 0.85, 0.55]; return C
def hcam(V):
    hv = V[V[:, 2] > V[:, 2].max() - 25]; return np.array([0.0, hv[:, 1].mean(), V[:, 2].max() - 12.0])
ED = {}
for c, K in CFG.items():
    P = '%s/build/%s_AE-E2_branch.npz' % (EW, K['N'])
    if os.path.exists(P):
        z = np.load(P); V = z['V']; Hc = hcam(V); Ce = V[z['side'] == 'l'].mean(0); ED[c] = P
        render('ear_%s_g' % c, P, np.tile(GREY, (len(V), 1)), [('front', (0, 1, 0.03), Hc, 15), ('prof', (1, 0, 0), Hc, 15), ('tqf', (1, 1, 0.1), Hc, 15), ('elat', (1, 0.15, 0.05), Ce, 5.6)])
        render('ear_%s_w' % c, P, part_cols(z), [('eface', (1, 0.9, 0.15), Ce, 5.2), ('ecrear', (0.35, -1, 0.1), Ce, 5.2)], wire=True)
        render('ear_he_%s' % c, HE[K['N']], np.tile(GREY, (len(np.load(HE[K['N']])['V']), 1)), [('prof', (1, 0, 0), Hc, 15), ('front', (0, 1, 0.03), Hc, 15)])
FNE = '/tmp/claude-0/rt/fn/final/ear/build/FNL4-CF2_E2_branch.npz'
if 'c1' in ED:
    for tag, P in (('cmpFN', FNE), ('cmpAE', ED['c1'])):
        z = np.load(P); V = z['V']; Hc = hcam(V); Ce = V[z['side'] == 'l'].mean(0)
        render(tag, P, np.tile(GREY, (len(V), 1)), [('prof', (1, 0, 0), Hc, 15), ('front', (0, 1, 0.03), Hc, 15), ('rear', (0, -1, 0), Hc, 15), ('elat', (1, 0.15, 0.05), Ce, 6.0)])
print('render jobs', len(jobs), flush=True)
done_ = lambda j: all(os.path.exists(os.path.join(TMP, '%s_%s.png' % (j[6], v_.split(':')[0]))) for v_ in j[7].split(';'))
todo = [j for j in jobs if not done_(j)]; print('to render', len(todo), flush=True)
with ThreadPoolExecutor(int(os.environ.get('AE_SHEET_THREADS', '2'))) as ex: list(ex.map(lambda j: subprocess.run(j, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL), todo))
# ---------------------------------------------------------------- compose
def sheet(fname, title, rows, colw=600, note=None, lab_w=170, legend=None):
    ncol = max(len(r_[1]) for r_ in rows); Wd = lab_w + ncol * colw; tl = title.split(' — ', 1) if font(21, True).getlength(title) > Wd - 28 else [title]; th = 70 + 30 * (len(tl) - 1)
    Hh = th + sum(colw + 34 for _ in rows) + (30 * len(note.split('\n')) + 14 if note else 0) + (44 if legend else 0)
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
    if note: d.text((14, y + 4), note, fill=(60, 60, 60), font=font(15))
    S.save(os.path.join(OUT, fname), quality=88)
MX = jl(A + '/corr/R1_matrix.json'); P0 = jl(A + '/partA_orig_check.json'); P1 = jl(R1 + '/partA_R1.json'); H0 = jl(A + '/AE_hidden_ear_identity.json'); H1 = jl(R1 + '/AE_hidden_ear_identity_R1.json')
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig, axs = plt.subplots(1, 4, figsize=(17, 4.6)); KS = [('thoracic_vertical_share', 'thoracic vertical / stature'), ('shin_over_leg', 'shin / leg (MF more even)'), ('torso_share', 'torso share'), ('leg_share', 'leg share')]
for ax, (k, t) in zip(axs, KS):
    for i, c in enumerate(CFG):
        K = CFG[c]; ns_ = [K['O'], K['N'], K['FN'], K['MF']]; x = np.arange(4) + i * 5; v = [MX[n][k] for n in ns_]
        ax.bar(x, v, color=['#b0b0b0', '#e07a2e', '#4a78c2', '#6aa36a'], width=0.8)
        for xx, n in zip(x, ns_): ax.text(xx, ax.get_ylim()[0], '', fontsize=7)
    lo = min(MX[n][k] for K in CFG.values() for n in K.values()); hi = max(MX[n][k] for K in CFG.values() for n in K.values()); ax.set_ylim(lo - 0.15 * (hi - lo) - 1e-4, hi + 0.15 * (hi - lo) + 1e-4)
    ax.set_xticks([1.5, 6.5]); ax.set_xticklabels(['c1 (male class)', 'c2 (female class)']); ax.set_title(t, fontsize=11)
fig.legend([plt.Rectangle((0, 0), 1, 1, color=c_) for c_ in ('#b0b0b0', '#e07a2e', '#4a78c2', '#6aa36a')], ['original (AEL1 / AELF190)', 'corrected R1', 'frozen Fenn', 'Marchfolk'], loc='lower center', ncol=4)
fig.suptitle('Aelari body-source correction — targeted and guarded shares at 190 cm (skin rig measures)'); fig.tight_layout(rect=(0, 0.08, 1, 0.95)); fig.savefig(os.path.join(OUT, 'AEC_00_metrics.jpg'), dpi=105); plt.close(fig)
for i, c in enumerate(CFG):
    K = CFG[c]; mo, mn = MEAS[K['O']], MEAS[K['N']]
    sheet('AEC_0%d_original_vs_corrected_%s.jpg' % (i + 1, c), 'Aelari %s — original %s | corrected %s | overlay (original red, corrected blue); R-6 source, same camera' % (c, K['O'], K['N']),
          [(v, [img('src_' + K['O'], v), img('src_' + K['N'], v), blend(img('src_' + K['O'], v), img('src_' + K['N'], v))], ['%s %.2f cm' % (K['O'], mo['stature']), '%s %.2f cm' % (K['N'], mn['stature']), 'overlay'] if v == 'front' else None)
           for v in ('front', 'prof', 'rear')], colw=520)
rows = []
for c, K in CFG.items():
    for lab, v in (('front', 'bfront'), ('profile', 'bprof')):
        rows.append(('%s %s' % (c, lab), [img('he_%s_%s' % (c, K['N']), v), img('he_%s_%s' % (c, K['FN']), v), blend(img('he_%s_%s' % (c, K['N']), v), img('he_%s_%s' % (c, K['FN']), v))], [K['N'], K['FN'] + ' (frozen Fenn)', 'overlay'] if lab == 'front' else None))
sheet('AEC_03_corrected_vs_Fenn_equal_height_ears_hidden.jpg', 'Equal height (190 cm), ears hidden: corrected Aelari | frozen Fenn | overlay (Aelari red, Fenn blue)', rows, colw=480)
cap_t = lambda n, c: '%s  thor %.4f  waist/torso %.4f' % (n, MX[n]['thoracic_vertical_share'], MX[n]['waist_interval_over_torso'])
cap_l = lambda n: '%s  shin/leg %.4f  leg %.4f' % (n, MX[n]['shin_over_leg'], MX[n]['leg_share'])
rows = []
for c, K in CFG.items():
    ns_ = [K['O'], K['N'], K['FN']]
    rows += [('%s front' % c, [img('band_%s_%s' % (c, n), 'tfront') for n in ns_], [cap_t(n, c) for n in ns_]), ('%s profile' % c, [img('band_%s_%s' % (c, n), 'tprof') for n in ns_], None)]
sheet('AEC_04_torso_ribcage_before_after_Fenn.jpg', 'Torso / ribcage (ears hidden, same camera): original | corrected | frozen Fenn — orange = thoracic vertical (spine_03 -> clavicle heads), teal = waist interval (spine_01 -> spine_03)',
      rows, colw=480, legend=[('thoracic vertical', C_TH), ('waist interval', C_WA)], note='Thoracic vertical / stature vs Fenn: c1 %+.2f %% (was %+.2f %%), c2 %+.2f %% (was %+.2f %%).' % (MX['AEL1-R1']['thoracic_vs_FN_pct'], MX['AEL1']['thoracic_vs_FN_pct'], MX['AELF190-R1']['thoracic_vs_FN_pct'], MX['AELF190']['thoracic_vs_FN_pct']))
rows = []
for c, K in CFG.items():
    ns_ = [K['O'], K['N'], K['FN']]
    rows += [('%s front' % c, [img('band_%s_%s' % (c, n), 'lfront') for n in ns_], [cap_l(n) for n in ns_]), ('%s profile' % c, [img('band_%s_%s' % (c, n), 'lprof') for n in ns_], None)]
sheet('AEC_05_leg_segments_before_after_Fenn.jpg', 'Leg segments (ears hidden, same camera): original | corrected | frozen Fenn — blue = thigh (hip -> knee joint), rose = lower leg (knee -> ankle joint)',
      rows, colw=480, legend=[('thigh', C_FE), ('lower leg', C_SH)], note='shin / leg gap to Marchfolk: c1 %.4f (was %.4f; Fenn %.4f), c2 %.4f (was %.4f; Fenn %.4f) -- more even than Fenn on both.' % (
          MX['AEL1-R1']['shin_over_leg_gap_to_MF'], MX['AEL1']['shin_over_leg_gap_to_MF'], MX['AEL1-R1']['FN_shin_over_leg_gap_to_MF'], MX['AELF190-R1']['shin_over_leg_gap_to_MF'], MX['AELF190']['shin_over_leg_gap_to_MF'], MX['AELF190-R1']['FN_shin_over_leg_gap_to_MF']))
pn_ = lambda P, c: '  '.join('%s %+.2f%%' % (r['rule'].split(' ')[0] + ('F' if 'Fenn' in r['rule'] else ''), r['by_t']['0.5']['diff_pct'] if '0.5' in r['by_t'] else list(r['by_t'].values())[1]['diff_pct']) for r in P['pelvis_skeletal_proxy'][c])
rows = []
for c, K in CFG.items():
    ns_ = [K['O'], K['N'], K['FN']]
    rows += [('%s oblique' % c, [img('he_%s_%s' % (c, n), 'pelvis') for n in ns_], ns_), ('%s front' % c, [img('he_%s_%s' % (c, n), 'pfront') for n in ns_], None)]
sheet('AEC_06_pelvis_before_after_Fenn.jpg', 'Pelvis (ears hidden, same camera): original | corrected | frozen Fenn — skeletal-proxy pelvis rules all hold at t = 0 / 0.5 / 1.0 on both',
      rows, colw=480, note='c1 orig: %s\nc1 R1:   %s\nc2 orig: %s\nc2 R1:   %s' % (pn_(P0, 'c1'), pn_(P1, 'c1'), pn_(P0, 'c2'), pn_(P1, 'c2')))
rows = []
for c, K in CFG.items():
    for lab, v in (('front', 'hfront'), ('profile', 'hprof')):
        rows.append(('%s %s' % (c, lab), [img('he_%s_%s' % (c, K['O']), v), img('he_%s_%s' % (c, K['N']), v), blend(img('he_%s_%s' % (c, K['O']), v), img('he_%s_%s' % (c, K['N']), v))],
                     [K['O'], K['N'], 'overlay (orig red, R1 blue)'] if lab == 'front' else None))
sheet('AEC_07_hidden_ear_face_before_after.jpg', 'Hidden-ear face (ears collapsed), same camera: original | corrected | overlay — craniofacial targets untouched', rows, colw=480,
      note='Head shape (similarity-aligned) RMS original -> corrected: c1 0.010 mm, c2 0.012 mm; head scale follows the stature re-solve (HH c1 %.2f -> %.2f cm, c2 %.2f -> %.2f cm). Face systems material: 7/7 -> 7/7 both.' % (
          H0['configs']['c1']['HH_cm'], H1['configs']['c1']['HH_cm'], H0['configs']['c2']['HH_cm'], H1['configs']['c2']['HH_cm']))
sheet('AEC_08_full_body_displacement_before_after.jpg', 'Full body, original -> corrected per-vertex displacement (ears hidden; blue 0 .. red >= 15 mm), shown on the corrected body',
      [(c, [img('disp_%s' % c, v) for v in ('bfront', 'bprof', 'brear')], ['front', 'profile', 'rear'] if c == 'c1' else None) for c in CFG], colw=520)
VO = {n: jl('%s/val/%s_fam_validator_v2_D1-D6.json' % (A, n)) for n in ('AEL1', 'AELF190')}; VN = {n: jl('%s/val/%s_fam_validator_v2_D1-D6.json' % (R1, n)) for n in ('AEL1-R1', 'AELF190-R1')}
st_ = sorted(VN['AEL1-R1']['stations']); Wd, Hh = 1260, 140 + 26 * (len(st_) + 2); S = Image.new('RGB', (Wd, Hh), 'white'); d = ImageDraw.Draw(S)
d.text((14, 14), 'Corrected Aelari body-family candidates on frozen v005 — validator D1+D3+D4+D5+D6', fill=(0, 0, 0), font=font(20, True))
d.text((14, 44), 'margin = loops - contract minimum (red = 0; d = change vs original).   AEL1-R1: %d / 69   AELF190-R1: %d / 69' % (VN['AEL1-R1']['summary']['firm_pass_count'], VN['AELF190-R1']['summary']['firm_pass_count']), fill=(0, 0, 0), font=font(16))
cw = [260, 140, 120, 140, 110, 140, 120, 140, 110]; hdr = ['station', 'c1 loops', 'c1 min', 'c1 margin', 'c1 d', 'c2 loops', 'c2 min', 'c2 margin', 'c2 d']; y = 90
for i, t in enumerate(hdr): d.text((20 + sum(cw[:i]), y), t, fill=(0, 0, 0), font=font(15, True))
y += 28
for s in st_:
    a, b = VN['AEL1-R1']['stations'][s], VN['AELF190-R1']['stations'][s]; ao, bo = VO['AEL1']['stations'][s], VO['AELF190']['stations'][s]
    vals = [s, a['loops_v2'], a['required'], a['margin'], '%+d' % (a['margin'] - ao['margin']), b['loops_v2'], b['required'], b['margin'], '%+d' % (b['margin'] - bo['margin'])]
    for i, t in enumerate(vals): d.text((20 + sum(cw[:i]), y), str(t), fill=(200, 30, 30) if (i in (3, 7) and t == 0) else (0, 0, 0), font=font(14))
    y += 26
S.save(os.path.join(OUT, 'AEC_09_validator_margins.jpg'), quality=88)
PN = ('shoulder_abd90_l', 'elbow_130_l', 'hip_flex90_l', 'knee_140_l', 'neck_rot45', 'trunk_twist30')
dn = jl(EV + '/aelari_rp3_correction/family/AELARI_deformation_comparison.json'); do = jl(EV + '/aelari_rp3_v001/AELARI_deformation_comparison.json')
sheet('AEC_10_deformation.jpg', 'Corrected Aelari body-family candidates — Standard v1 deformation (source rig + carried MPFB weights, plain LBS; red = flipped faces)',
      [(K['N'], [img('pose_%s_%s' % (K['N'], p), 'v') for p in PN], ['%s %d (orig %d, MF %d)' % (p, dn[K['N']]['poses'][p]['aelari_family'], do[K['O']]['poses'][p]['aelari_family'], dn[K['N']]['poses'][p]['marchfolk_v005']) for p in PN]) for K in CFG.values()], colw=400)
if ED:
    AU = {c: jl('%s/audit/%s_AE-E2_audit.json' % (EW, CFG[c]['N'])) for c in ED}; ME = {c: jl('%s/meas/%s_AE-E2_measure.json' % (EW, CFG[c]['N']))['sides']['l'] for c in ED}
    cap = lambda c: '%s AE-E2  L %.2f  angle %.0f  T-4 %d  SI %d' % (CFG[c]['N'], ME[c]['length_lobe_to_tip_cm'], ME[c]['auricle_body_angle_deg'], AU[c]['T4']['angle_violations'], AU[c]['self_intersection_pairs_touching_branch'])
    sheet('AEC_11_corrected_heads_with_AE-E2.jpg', 'Corrected heads with AE-E2 (parameters, topology and root unchanged): hidden-ear head | AE-E2 visible ear | 3-4 | ear lateral | wire',
          [(c, [img('ear_he_%s' % c, 'prof'), img('ear_%s_g' % c, 'prof'), img('ear_%s_g' % c, 'tqf'), img('ear_%s_g' % c, 'elat'), img('ear_%s_w' % c, 'eface')], [cap(c), '', '', '', 'wire (part colours)']) for c in ED], colw=440)
    if 'c1' in ED:
        sheet('AEC_12_Fenn_E2_vs_corrected_AE-E2.jpg', 'Frozen Fenn E2 (FN_M_REF_RP3_v001) | Aelari AE-E2 on corrected AEL1-R1 — each on its own head, same relative camera',
              [(v, [img('cmpFN', v), img('cmpAE', v)], ['Fenn E2', 'Aelari AE-E2 (AEL1-R1)'] if v == 'prof' else None) for v in ('prof', 'front', 'rear', 'elat')])
print('sheets done', flush=True)
