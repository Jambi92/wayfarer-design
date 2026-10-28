# va_sheets.py WORK OUTDIR : Vael order (2026-10-28) §21 visual package, Part A / B (sheets 01-14 + ordering diagnostic). Identical orthographic cameras per
# row, true scale; ears hidden (hm08 w_ears > 0.05 collapsed) and geometry-only grey shading (complexion / hair / presentation neutral) wherever identity is
# judged. Workbench renders (grask_rigprep_v001/render_attr.py) composed with PIL; resumable; 2 Blender processes.
import sys, os, json, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001')
import fn_face_metrics as F
W, OUT = sys.argv[1:3]; os.makedirs(OUT, exist_ok=True); TMP = os.environ.get('VA_SHEET_TMP', W + '/sheet_r'); os.makedirs(TMP, exist_ok=True)
BP = '/home/claude/stc/bin/python3'; REND = '/home/claude/wayfarer-design/tools/rac/rp/grask_rigprep_v001/render_attr.py'; PA = W + '/partA'; EV = OUT + '/..'
GREY = np.array([0.80, 0.78, 0.76]); jl = lambda p: json.load(open(p))
CFG = {'c1': dict(VA='VAL4', FN='FNM178', AE='AEM178', MF='MFM178', SG='SGM178'), 'c2': dict(VA='VALF178', FN='FNF178', AE='AEF178', MF='MFF178', SG='SGF178')}
R6 = {'VAL4': PA + '/ref/VAL4_r6.npz', 'VALF178': PA + '/build/VALF178_r6.npz'}
for c in CFG.values():
    for k in ('FN', 'AE', 'MF', 'SG'): R6[c[k]] = '%s/cmp/%s_r6.npz' % (PA, c[k])
def font(sz, bold=False):
    f = '/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf' % ('-Bold' if bold else ''); return ImageFont.truetype(f, sz) if os.path.exists(f) else ImageFont.load_default()
jobs = []
def render(tag, npz, col, views, wire=False, px=520):
    vs = ';'.join('%s:%s:%s:%.2f' % (n, ','.join('%.4f' % x for x in d), ','.join('%.3f' % x for x in c), hs) for n, d, c, hs in views)
    cf = os.path.join(TMP, tag + '_col.npy'); np.save(cf, np.asarray(col, np.float32)); jobs.append([BP, REND, '--', npz, cf, TMP, tag, vs, '1' if wire else '0', str(px)])
def img(tag, name):
    p = os.path.join(TMP, '%s_%s.png' % (tag, name)); return Image.open(p).convert('RGB') if os.path.exists(p) else Image.new('RGB', (600, 600), 'white')
def heat(x, lo, hi):
    t = np.clip((x - lo) / (hi - lo + 1e-12), 0, 1)[:, None]; return (1 - t) * np.array([0.2, 0.35, 0.85]) + t * np.array([0.95, 0.25, 0.15])
def blend(a, b):
    A_ = np.asarray(a, float) * np.array([1.0, 0.55, 0.55]); B_ = np.asarray(b, float) * np.array([0.55, 0.65, 1.0]); return Image.fromarray(np.clip(0.5 * A_ + 0.5 * B_, 0, 255).astype(np.uint8))
nz = np.load('/tmp/claude-0/rt/fn/src/FNL4_native.npz'); bones = [str(b) for b in nz['bones']]; dom = np.array(bones)[np.asarray(nz['W']).argmax(1)]
TRUNK = np.array([b.startswith(('spine', 'pelvis', 'clavicle', 'Root')) for b in dom]); LEG = np.array([b.startswith(('thigh', 'calf', 'foot', 'ball')) for b in dom])
def joints(n):
    j = json.loads(str(np.load(R6[n])['joints'])); z = lambda b: j[b][0][2]
    return dict(clav=0.5 * (z('clavicle_l') + z('clavicle_r')), sp3=z('spine_03'), sp1=z('spine_01'), hip=0.5 * (z('thigh_l') + z('thigh_r')), knee=0.5 * (z('calf_l') + z('calf_r')), ankle=0.5 * (z('foot_l') + z('foot_r')))
C_TH, C_WA, C_FE, C_SH = [0.95, 0.60, 0.20], [0.30, 0.70, 0.75], [0.45, 0.55, 0.90], [0.90, 0.45, 0.55]
def band_cols(n, V):
    j = joints(n); C = np.tile(GREY, (len(V), 1)); z = V[:, 2]
    C[TRUNK & (z >= j['sp3']) & (z <= j['clav'])] = C_TH; C[TRUNK & (z >= j['sp1']) & (z < j['sp3'])] = C_WA
    C[LEG & (z <= j['hip']) & (z > j['knee'])] = C_FE; C[LEG & (z <= j['knee']) & (z > j['ankle'])] = C_SH; return C
# ---------------------------------------------------------------- renders
for n in ('VAL4', 'VALF178'):
    z = np.load(R6[n]); keep = z['keep']; Fx = z['F'][keep[z['F']].all(1)]; q = os.path.join(TMP, 'src_%s.npz' % n); np.savez_compressed(q, V=z['V'], Q=Fx); Bc = np.array([0.0, z['V'][keep][:, 1].mean(), 92.0])
    render('src_' + n, q, np.tile(GREY, (len(z['V']), 1)), [('front', (0, 1, 0), Bc, 96), ('prof', (1, 0, 0), Bc, 96), ('rear', (0, -1, 0), Bc, 96)])
    fz = np.load('%s/fam/%s_fam.npz' % (W, n)); render('fam_' + n, '%s/fam/%s_fam.npz' % (W, n), np.tile(GREY, (len(fz['V']), 1)), [('front', (0, 1, 0), Bc, 96), ('prof', (1, 0, 0), Bc, 96)])
for c, K in CFG.items():
    Vv = np.load('%s/ov/%s_earhidden.npz' % (W, K['VA']))['V']; ym = Vv[:, 1].mean(); Bc = np.array([0.0, ym, 92.0]); Hc = np.array([0.0, Vv[Vv[:, 2] > Vv[:, 2].max() - 25][:, 1].mean(), Vv[:, 2].max() - 12.0])
    jv = joints(K['VA']); Tc = np.array([0.0, ym, 0.5 * (jv['sp1'] + jv['clav'])]); Pc = np.array([0.0, ym, jv['hip'] + 4]); Sc = np.array([0.0, ym, jv['clav'] + 6])
    hand = np.array([Vv[:, 0].max() - 9, Vv[:, 1].mean(), jv['hip'] - 22]); foot = np.array([11.0, 6.0, 6.0])
    for n in (K['VA'], K['FN'], K['AE'], K['MF'], K['SG']):
        hp = '%s/ov/%s_earhidden.npz' % (W, n); V = np.load(hp)['V']
        render('he_%s' % n, hp, np.tile(GREY, (len(V), 1)), [('bfront', (0, 1, 0), Bc, 96), ('bprof', (1, 0, 0), Bc, 96), ('hfront', (0, 1, 0.03), Hc, 14.5), ('hprof', (1, 0, 0), Hc, 14.5), ('htq', (1, 1, 0.1), Hc, 14.5),
                                                             ('tprof', (1, 0, 0), Tc, 32), ('tfront', (0, 1, 0), Tc, 32), ('shoulder', (0.25, 1, 0.12), Sc, 24), ('pelvis', (1, 0.25, 0.0), Pc, 28), ('pfront', (0, 1, 0), Pc, 28),
                                                             ('hand', (0.3, 1, 0.0), hand, 14), ('foot', (0.8, 0.6, 0.6), foot, 14), ('ankle', (1, 0.05, 0), foot + np.array([0, -2, 4]), 14)])
        if n != K['SG']: render('band_%s' % n, hp, band_cols(n, V), [('tprof', (1, 0, 0), Tc, 32), ('lprof', (1, 0, 0), np.array([0.0, ym, 50.0]), 52)])
    # face residual heat maps on the Vael head: distance to the similarity-aligned Marchfolk / Aelari / Fenn head (ear excluded)
    D = {k: F.load(R6[K[k]]) for k in ('VA', 'MF', 'AE', 'FN')}; Va = D['VA']['V']; hd = F.HEAD
    for k in ('MF', 'AE', 'FN'):
        f = F.procrustes(D[k]['V'][hd], Va[hd]); d = np.linalg.norm(f(D[k]['V']) - Va, axis=1) * 10; C = np.tile(GREY, (len(Va), 1)); C[hd] = heat(d[hd], 0, 4.0)
        render('fres_%s_%s' % (c, k), '%s/ov/%s_earhidden.npz' % (W, K['VA']), C, [('hfront', (0, 1, 0.03), Hc, 14.5), ('hprof', (1, 0, 0), Hc, 14.5)])
for n in ('VAL4', 'VALF178'):
    fz = np.load('%s/fam/%s_fam.npz' % (W, n))
    for pn in ('shoulder_abd90_l', 'elbow_130_l', 'hip_flex90_l', 'knee_140_l', 'neck_rot45', 'trunk_twist30'):
        pp = '%s/def/%s_%s_fam.npz' % (W, pn, n)
        if not os.path.exists(pp): continue
        X = np.load(pp); Xv = X['V']; C = np.tile(GREY, (len(fz['Q']), 1)); fl = np.asarray(X['flip']).astype(int).ravel(); C[fl[fl < len(C)]] = [0.92, 0.18, 0.12]
        q = os.path.join(TMP, 'pose_%s_%s.npz' % (n, pn)); np.savez_compressed(q, V=Xv, Q=fz['Q']); Bc_ = np.array([0.0, Xv[:, 1].mean(), (Xv[:, 2].max() + Xv[:, 2].min()) / 2])
        render('pose_%s_%s' % (n, pn), q, C, [('v', (1, 1, 0.05), Bc_, 100)], px=420)
print('render jobs', len(jobs), flush=True)
done_ = lambda j: all(os.path.exists(os.path.join(TMP, '%s_%s.png' % (j[6], v_.split(':')[0]))) for v_ in j[7].split(';'))
todo = [j for j in jobs if not done_(j)]; print('to render', len(todo), flush=True)
with ThreadPoolExecutor(int(os.environ.get('VA_SHEET_THREADS', '2'))) as ex: list(ex.map(lambda j: subprocess.run(j, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL), todo))
# ---------------------------------------------------------------- compose
def sheet(fname, title, rows, colw=480, note=None, lab_w=170, legend=None):
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
PV = jl(PA + '/VALF178_reference_validation.json'); HE = jl(W + '/VA_hidden_ear_identity.json')
sheet('VA_01_VAL4_vs_VALF178.jpg', 'Vael — accepted configuration-1 VAL4 | configuration-2 central reference VALF178 (R-6, ~178 cm, same camera)',
      [(v, [img('src_VAL4', v), img('src_VALF178', v)], ['VAL4 %.2f cm' % PV['envelope']['VAL4'], 'VALF178 %.2f cm' % PV['envelope']['VALF178']] if v == 'front' else None) for v in ('front', 'prof', 'rear')], colw=560)
sheet('VA_02_source_vs_family.jpg', 'Vael body-family candidates — R-6 source (red) over family realization on v005 (blue), same camera (V = M @ hm08)',
      [(n, [blend(img('src_' + n, 'front'), img('fam_' + n, 'front')), blend(img('src_' + n, 'prof'), img('fam_' + n, 'prof'))], None) for n in ('VAL4', 'VALF178')], colw=560)
row3 = []
for c, K in CFG.items():
    for lab, v in (('front', 'bfront'), ('profile', 'bprof')):
        row3.append(('%s %s' % (c, lab), [img('he_' + K[k], v) for k in ('VA', 'FN', 'AE')], ['%s (Vael)' % K['VA'], '%s (frozen Fenn)' % K['FN'], '%s (frozen Aelari)' % K['AE']] if lab == 'front' else None))
sheet('VA_03_three_elf_equal_height_ears_hidden.jpg', 'Equal height 178 cm, ears hidden, neutral shading: Vael | frozen Fenn | frozen Aelari', row3, colw=440)
row4 = []
for c, K in CFG.items():
    for lab, v in (('front', 'bfront'), ('profile', 'bprof')):
        row4.append(('%s %s' % (c, lab), [img('he_' + K[k], v) for k in ('VA', 'MF', 'SG')] + [blend(img('he_' + K['VA'], v), img('he_' + K['MF'], v))], [K['VA'], K['MF'], K['SG'], 'Vael red / Marchfolk blue'] if lab == 'front' else None))
sheet('VA_04_Vael_vs_humans_ears_hidden.jpg', 'Equal height 178 cm, ears hidden: Vael | Marchfolk | Sagekin | overlay Vael-Marchfolk', row4, colw=420)
reg = lambda key, vname, title, fname, extra=None, legend=None, note=None: sheet(fname, title, [('%s' % c, [img(('band_' if vname.startswith('band') else 'he_') + K[k], vname.replace('band:', '')) for k in ('VA', 'FN', 'AE', 'MF')], [K[k] for k in ('VA', 'FN', 'AE', 'MF')]) for c, K in CFG.items()], colw=420, legend=legend, note=note)
cv = lambda c, k: next(r for r in PV['configs'][c]['canon'] if r['key'] == k)
reg('', 'band:tprof', 'Vael — torso depth / profile (ears hidden): Vael | Fenn | Aelari | Marchfolk — orange thoracic vertical, teal waist interval', 'VA_05_torso_depth_profile.jpg',
    legend=[('thoracic vertical', C_TH), ('waist interval', C_WA)], note='thorax depth / stature vs Fenn / Aelari: c1 %+.1f / %+.1f %%, c2 %+.1f / %+.1f %%;  waist interval / torso vs Aelari: c1 %+.2f %%, c2 %+.2f %% (c2 FAILS < Aelari)' % (
        cv('c1', 'thorax_depth_share')['VA_vs_FN_pct'], cv('c1', 'thorax_depth_share')['VA_vs_AE_pct'], cv('c2', 'thorax_depth_share')['VA_vs_FN_pct'], cv('c2', 'thorax_depth_share')['VA_vs_AE_pct'], cv('c1', 'waist_interval_over_torso')['VA_vs_AE_pct'], cv('c2', 'waist_interval_over_torso')['VA_vs_AE_pct']))
reg('', 'shoulder', 'Vael — shoulder / neck integration (ears hidden): Vael | Fenn | Aelari | Marchfolk', 'VA_06_shoulder_neck.jpg')
pvl = lambda c, rs: '  '.join('%s%s %s%+.2f%%' % (r['rule'].split(' ')[0], '' if r['gating'] else '(report)', 'OK' if r['holds_all_t'] else 'NO', r['by_t']['0.5']['diff_pct']) for r in rs)
pv = lambda c: pvl(c, PV['pelvis_skeletal_proxy'][c][:8]) + '\n     ' + pvl(c, PV['pelvis_skeletal_proxy'][c][8:])
sheet('VA_07_pelvis_waist.jpg', 'Vael — pelvis / waist (ears hidden): Vael | Fenn | Aelari | Marchfolk (oblique and front)', [('%s %s' % (c, v), [img('he_' + K[k], v) for k in ('VA', 'FN', 'AE', 'MF')], [K[k] for k in ('VA', 'FN', 'AE', 'MF')] if v == 'pelvis' else None) for c, K in CFG.items() for v in ('pelvis', 'pfront')], colw=400,
      note='skeletal proxy, t = 0.5 (rule, holds at all t, Vael vs reference):\nc1: %s\nc2: %s' % (pv('c1'), pv('c2')))
reg('', 'hand', 'Vael — arm / hand base (ears hidden): Vael | Fenn | Aelari | Marchfolk', 'VA_08_arm_hand_base.jpg', note='palm breadth / hand vs Fenn / Aelari: c1 %+.1f / %+.1f %%; c2 %+.1f / %+.1f %%' % (
    cv('c1', 'palm_breadth_over_hand')['VA_vs_FN_pct'], cv('c1', 'palm_breadth_over_hand')['VA_vs_AE_pct'], cv('c2', 'palm_breadth_over_hand')['VA_vs_FN_pct'], cv('c2', 'palm_breadth_over_hand')['VA_vs_AE_pct']))
sheet('VA_09_leg_ankle_foot_base.jpg', 'Vael — leg segments, ankle and foot base (ears hidden): Vael | Fenn | Aelari | Marchfolk', [('%s %s' % (c, v), [img(('band_' if v == 'lprof' else 'he_') + K[k], v) for k in ('VA', 'FN', 'AE', 'MF')], [K[k] for k in ('VA', 'FN', 'AE', 'MF')] if v == 'lprof' else None) for c, K in CFG.items() for v in ('lprof', 'foot')], colw=400,
      legend=[('thigh', C_FE), ('lower leg', C_SH)], note='leg share vs MF / Fenn / Aelari: c1 %+.2f / %+.2f / %+.2f %% (Aelari FAILS: Vael > Aelari); c2 %+.2f / %+.2f / %+.2f %%;  foot breadth / length vs Fenn / Aelari: c1 %+.1f / %+.1f %%' % (
          cv('c1', 'leg_share')['VA_vs_MF_pct'], cv('c1', 'leg_share')['VA_vs_FN_pct'], cv('c1', 'leg_share')['VA_vs_AE_pct'], cv('c2', 'leg_share')['VA_vs_MF_pct'], cv('c2', 'leg_share')['VA_vs_FN_pct'], cv('c2', 'leg_share')['VA_vs_AE_pct'],
          cv('c1', 'foot_breadth_over_length')['VA_vs_FN_pct'], cv('c1', 'foot_breadth_over_length')['VA_vs_AE_pct']))
row10 = []
for c, K in CFG.items():
    for lab, v in (('front', 'hfront'), ('profile', 'hprof')):
        row10.append(('%s %s' % (c, lab), [img('he_' + K[k], v) for k in ('VA', 'FN', 'AE', 'MF', 'SG')], [K[k] for k in ('VA', 'FN', 'AE', 'MF', 'SG')] if lab == 'front' else None))
sheet('VA_10_hidden_ear_neutral_face.jpg', 'Hidden-ear / neutral-complexion face, 178 cm: Vael | frozen Fenn | frozen Aelari | Marchfolk | Sagekin', row10, colw=400)
row11 = []
for c, K in CFG.items():
    row11.append(('%s front' % c, [img('fres_%s_%s' % (c, k), 'hfront') for k in ('MF', 'AE', 'FN')], ['Vael vs Marchfolk', 'Vael vs Aelari', 'Vael vs Fenn']))
    row11.append(('%s profile' % c, [img('fres_%s_%s' % (c, k), 'hprof') for k in ('MF', 'AE', 'FN')], None))
fr = lambda c: ' '.join('%s %.2f/%.2f/%.2f' % (r[:8], v['VA_vs_MF_rms_mm'], v['VA_vs_AE_rms_mm'], v['VA_vs_FN_rms_mm']) for r, v in HE['configs'][c]['face'].items())
sheet('VA_11_face_regional_residuals.jpg', 'Vael face regional residuals after similarity alignment (blue 0 .. red >= 4 mm on the Vael head): vs Marchfolk | vs Aelari | vs Fenn', row11, colw=440,
      note='region RMS mm (vs MF / AE / FN)\nc1: %s\nc2: %s\nVael vs Marchfolk: no region departs materially (all < 0.6 mm) -- the Vael head is the Marchfolk head plus eye-scale / cheek-bone targets' % (fr('c1'), fr('c2')))
VA_ = {n: jl('%s/val/%s_fam_validator_v2_D1-D6.json' % (W, n)) for n in ('VAL4', 'VALF178')}; st_ = sorted(VA_['VAL4']['stations'])
S = Image.new('RGB', (1200, 140 + 26 * (len(st_) + 2)), 'white'); d = ImageDraw.Draw(S)
d.text((14, 14), 'Vael body-family candidates on frozen v005 — validator D1+D3+D4+D5+D6', fill=(0, 0, 0), font=font(20, True))
d.text((14, 44), 'margin = loops - contract minimum (red = 0).   VAL4: %d / 69   VALF178: %d / 69' % (VA_['VAL4']['summary']['firm_pass_count'], VA_['VALF178']['summary']['firm_pass_count']), fill=(0, 0, 0), font=font(16))
cw = [260, 150, 150, 150, 150, 150, 150]; y = 90
for i, t in enumerate(['station', 'c1 loops', 'c1 min', 'c1 margin', 'c2 loops', 'c2 min', 'c2 margin']): d.text((20 + sum(cw[:i]), y), t, fill=(0, 0, 0), font=font(15, True))
y += 28
for s in st_:
    a, b = VA_['VAL4']['stations'][s], VA_['VALF178']['stations'][s]; vals = [s, a['loops_v2'], a['required'], a['margin'], b['loops_v2'], b['required'], b['margin']]
    for i, t in enumerate(vals): d.text((20 + sum(cw[:i]), y), str(t), fill=(200, 30, 30) if (i in (3, 6) and t == 0) else (0, 0, 0), font=font(14))
    y += 26
S.save(os.path.join(OUT, 'VA_12_validator_margins.jpg'), quality=88)
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(11, 4.5)); zs = ['face', 'ears', 'hand', 'foot', 'trunk', 'arm', 'leg', 'neck', 'head']; x = np.arange(len(zs))
for i, n in enumerate(('VAL4', 'VALF178')):
    au = jl('%s/audit/%s_fam_audit.json' % (W, n))['density_pct_of_stature']; ax.bar(x + (i - 0.5) * 0.35, [au[z]['mean'] for z in zs], 0.35, label=n)
    ax.scatter(x, [au[z]['limit'] for z in zs], marker='_', s=600, color='k')
ax.set_xticks(x); ax.set_xticklabels(zs); ax.set_ylabel('mean edge / stature (%)'); ax.set_title('Vael body-family density, 9 zones (black bar = limit): all pass'); ax.legend(); fig.tight_layout(); fig.savefig(os.path.join(OUT, 'VA_13_density.jpg'), dpi=105); plt.close(fig)
dc = jl(EV + '/VAEL_deformation_comparison.json'); PN = ('shoulder_abd90_l', 'elbow_130_l', 'hip_flex90_l', 'knee_140_l', 'neck_rot45', 'trunk_twist30')
sheet('VA_14_deformation.jpg', 'Vael body-family candidates — Standard v1 deformation (source rig + carried MPFB weights, plain LBS; red = flipped). Expression sanity not run: face gate not passed',
      [(n, [img('pose_%s_%s' % (n, p), 'v') for p in PN], ['%s %d (MF v005 %d)' % (p, dc[n]['poses'][p]['aelari_family'], dc[n]['poses'][p]['marchfolk_v005']) for p in PN]) for n in ('VAL4', 'VALF178')], colw=400)
# ordering diagnostic: the matched-stature window MF < Vael < Aelari for hip-joint height and (c2) waist interval
DG = jl(EV + '/partA/VAEL_ordering_diagnostic.json') if os.path.exists(EV + '/partA/VAEL_ordering_diagnostic.json') else None
if DG:
    fig, axs = plt.subplots(1, 2, figsize=(14, 4.8))
    for ax, key, t in zip(axs, ('leg_share', 'waist_interval_over_torso'), ('hip-joint height / stature (VA-P2a: MF < Vael < Fenn, Aelari)', 'waist interval / torso (VA-P6: Vael < Aelari)')):
        for i, c in enumerate(('c1', 'c2')):
            rows = DG[c][key]; labs = list(rows.keys()); vals = [rows[l] for l in labs]; xs = np.arange(len(labs)) + i * (len(labs) + 1)
            cols = ['#e07a2e' if l.startswith('Vael') else '#7a4fb0' if 'Aelari' in l else '#4a78c2' if 'Fenn' in l else '#6aa36a' for l in labs]
            ax.bar(xs, vals, color=cols); [ax.text(xx, v, l, rotation=90, fontsize=7, ha='center', va='bottom') for xx, v, l in zip(xs, vals, labs)]
        lo = min(min(DG[c][key].values()) for c in ('c1', 'c2')); hi = max(max(DG[c][key].values()) for c in ('c1', 'c2')); ax.set_ylim(lo - 0.25 * (hi - lo), hi + 0.6 * (hi - lo)); ax.set_title(t, fontsize=10); ax.set_xticks([])
    fig.suptitle('Vael ordering diagnostic — matched-stature comparisons (left block c1, right block c2)'); fig.tight_layout(); fig.savefig(os.path.join(OUT, 'VA_15_ordering_diagnostic.jpg'), dpi=105); plt.close(fig)
print('sheets done', flush=True)
