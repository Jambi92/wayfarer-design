# hv_sheets.py WORK OUTDIR : Halvren central-anchor order (2026-10-29) §25 visual package, body / face (HV_01..12; the ear sheets 13-23 are not produced:
# ear work is locked, §18). Identical orthographic cameras per row, true scale; ears hidden (hm08 w_ears > 0.05 collapsed) and geometry-only grey shading
# (pigmentation / hair / presentation neutral) wherever identity is judged. Workbench renders (grask_rigprep_v001/render_attr.py) + PIL / matplotlib; resumable.
import sys, os, json, csv, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001')
import fn_face_metrics as F
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
W, OUT = sys.argv[1:3]; os.makedirs(OUT, exist_ok=True); TMP = os.environ.get('HV_SHEET_TMP', W + '/sheet_r'); os.makedirs(TMP, exist_ok=True)
BP = '/home/claude/stc/bin/python3'; REND = '/home/claude/wayfarer-design/tools/rac/rp/grask_rigprep_v001/render_attr.py'; PA = W + '/partA'
GREY = np.array([0.80, 0.78, 0.76]); jl = lambda p: json.load(open(p)); SRC = ('MF', 'SG', 'SK', 'FN', 'AE', 'VA')
NM = dict(HV='Halvren', MF='Marchfolk', SG='Sagekin', SK='Skarn (178 diag.)', FN='frozen Fenn', AE='frozen Aelari', VA='frozen Vael')
CFG = {'c1': dict(HV='HVC1', MF='MFM178', SG='SGM178', SK='SKM178', FN='FNM178', AE='AEM178', VA='VAM178'), 'c2': dict(HV='HVF178', MF='MFF178', SG='SGF178', SK='SKF178', FN='FNF178', AE='AEF178', VA='VAF178')}
R6 = {'HVC1': PA + '/ref/HVC1_r6.npz', 'HVF178': PA + '/build/HVF178_r6.npz'}
for c in CFG.values():
    for k in SRC: R6[c[k]] = '%s/cmp/%s_r6.npz' % (PA, c[k])
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
def sil(a, b):                                           # silhouette overlay: Halvren only red, comparator only blue, both grey (background = corner pixel)
    A_ = np.asarray(a, int); B_ = np.asarray(b, int); ma = (np.abs(A_ - A_[2, 2]).max(2) > 10); mb = (np.abs(B_ - B_[2, 2]).max(2) > 10)
    O_ = np.full(A_.shape, 255, np.uint8); O_[ma & mb] = (150, 150, 150); O_[ma & ~mb] = (215, 40, 40); O_[~ma & mb] = (40, 90, 220); return Image.fromarray(O_)
def joints(n):
    j = json.loads(str(np.load(R6[n])['joints'])); z = lambda b: j[b][0][2]
    return dict(clav=0.5 * (z('clavicle_l') + z('clavicle_r')), sp3=z('spine_03'), sp1=z('spine_01'), hip=0.5 * (z('thigh_l') + z('thigh_r')), knee=0.5 * (z('calf_l') + z('calf_r')), ankle=0.5 * (z('foot_l') + z('foot_r')))
# ---------------------------------------------------------------- renders
for c, K in CFG.items():
    n = K['HV']; z = np.load(R6[n]); keep = z['keep']; Fx = z['F'][keep[z['F']].all(1)]; q = os.path.join(TMP, 'src_%s.npz' % n); np.savez_compressed(q, V=z['V'], Q=Fx); Bc = np.array([0.0, z['V'][keep][:, 1].mean(), 90.0])
    render('src_' + n, q, np.tile(GREY, (len(z['V']), 1)), [('front', (0, 1, 0), Bc, 95), ('prof', (1, 0, 0), Bc, 95), ('tq', (1, 1, 0.05), Bc, 95), ('rear', (0, -1, 0), Bc, 95)])
    fz = np.load('%s/fam/%s_fam.npz' % (W, n)); render('fam_' + n, '%s/fam/%s_fam.npz' % (W, n), np.tile(GREY, (len(fz['V']), 1)), [('front', (0, 1, 0), Bc, 95), ('prof', (1, 0, 0), Bc, 95)])
    render('famw_' + n, '%s/fam/%s_fam.npz' % (W, n), np.tile(GREY, (len(fz['V']), 1)), [('head', (1, 1, 0.1), np.array([0.0, Bc[1], fz['V'][:, 2].max() - 12]), 14)], wire=True)
    Vh = np.load('%s/ov/%s_earhidden.npz' % (W, n))['V']; ym = Vh[:, 1].mean(); Bc = np.array([0.0, ym, 90.0]); Hc = np.array([0.0, Vh[Vh[:, 2] > Vh[:, 2].max() - 25][:, 1].mean(), Vh[:, 2].max() - 12.0])
    jv = joints(n); Tc = np.array([0.0, ym, 0.5 * (jv['sp1'] + jv['clav'])]); Pc = np.array([0.0, ym, jv['hip'] + 4]); Sc = np.array([0.0, ym, jv['clav'] + 6])
    hand = np.array([Vh[:, 0].max() - 9, Vh[:, 1].mean(), jv['hip'] - 22]); foot = np.array([11.0, 6.0, 6.0]); Ac = np.array([0.0, ym, 0.5 * (jv['clav'] + jv['hip']) - 8]); Lc = np.array([0.0, ym, jv['knee']])
    for k in ('HV',) + SRC:
        hp = '%s/ov/%s_earhidden.npz' % (W, K[k]); V = np.load(hp)['V']
        render('he_%s' % K[k], hp, np.tile(GREY, (len(V), 1)), [('bfront', (0, 1, 0), Bc, 95), ('bprof', (1, 0, 0), Bc, 95), ('hfront', (0, 1, 0.03), Hc, 14.5), ('hprof', (1, 0, 0), Hc, 14.5), ('htq', (1, 1, 0.1), Hc, 14.5),
                                                               ('tfront', (0, 1, 0), Tc, 32), ('tprof', (1, 0, 0), Tc, 32), ('shoulder', (0.25, 1, 0.12), Sc, 24), ('pelvis', (1, 0.25, 0.0), Pc, 28), ('pfront', (0, 1, 0), Pc, 28),
                                                               ('arm', (0, 1, 0), Ac, 44), ('leg', (1, 0, 0), Lc, 50), ('hand', (0.3, 1, 0.0), hand, 14), ('foot', (0.8, 0.6, 0.6), foot, 14)], px=480)
    D = {k: F.load(R6[K[k]]) for k in ('HV', 'MF', 'FN', 'AE', 'VA')}; Vv = D['HV']['V']; hd = F.HEAD
    for k in ('MF', 'FN', 'AE', 'VA'):
        f = F.procrustes(D[k]['V'][hd], Vv[hd]); d = np.linalg.norm(f(D[k]['V']) - Vv, axis=1) * 10; C = np.tile(GREY, (len(Vv), 1)); C[hd] = heat(d[hd], 0, 4.0)
        render('fres_%s_%s' % (c, k), '%s/ov/%s_earhidden.npz' % (W, n), C, [('hfront', (0, 1, 0.03), Hc, 14.5), ('hprof', (1, 0, 0), Hc, 14.5)])
    for pn in ('shoulder_abd90_l', 'shoulder_flex90_l', 'elbow_130_l', 'thumb_opposition_l', 'hip_flex90_l', 'knee_90_l', 'knee_140_l', 'trunk_twist30'):
        pp = '%s/def/%s_%s_fam.npz' % (W, pn, n)
        if not os.path.exists(pp): continue
        X = np.load(pp); Xv = X['V']; Cf_ = np.tile(GREY, (len(fz['Q']), 1)); fl_ = np.asarray(X['flip']).astype(int).ravel() if 'flip' in X.files else np.zeros(0, int); Cf_[fl_[fl_ < len(Cf_)]] = [0.92, 0.18, 0.12]
        sx = np.asarray(X['selfx']).astype(int).ravel() if 'selfx' in X.files else np.zeros(0, int); Cf_[sx[sx < len(Cf_)]] = [0.98, 0.65, 0.1]
        q = os.path.join(TMP, 'pose_%s_%s.npz' % (c, pn)); np.savez_compressed(q, V=Xv, Q=fz['Q']); Cb = np.array([Xv[:, 0].mean(), Xv[:, 1].mean(), (Xv[:, 2].max() + Xv[:, 2].min()) / 2])
        render('pose_%s_%s' % (c, pn), q, Cf_, [('v', (1, 1, 0.05), Cb, 98)], px=440)
print('render jobs', len(jobs), flush=True)
done_ = lambda j: all(os.path.exists(os.path.join(TMP, '%s_%s.png' % (j[6], v_.split(':')[0]))) for v_ in j[7].split(';'))
todo = [j for j in jobs if not done_(j)]; print('to render', len(todo), flush=True)
with ThreadPoolExecutor(int(os.environ.get('HV_SHEET_THREADS', '2'))) as ex: list(ex.map(lambda j: subprocess.run(j, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL), todo))
# ---------------------------------------------------------------- compose
def sheet(fname, title, rows, colw=480, note=None, lab_w=150):
    ncol = max(len(r_[1]) for r_ in rows); Wd = lab_w + ncol * colw; tl = title.split(' — ', 1) if font(21, True).getlength(title) > Wd - 28 else [title]; th = 70 + 30 * (len(tl) - 1)
    nl = note.split('\n') if note else []; Hh = th + sum(colw + 34 for _ in rows) + (24 * len(nl) + 16 if note else 0)
    S = Image.new('RGB', (Wd, Hh), 'white'); d = ImageDraw.Draw(S)
    for i_, t_ in enumerate(tl): d.text((14, 14 + 30 * i_), t_ if i_ == 0 else '— ' + t_, fill=(0, 0, 0), font=font(21, True))
    y = th
    for lab, ims, caps in rows:
        d.text((10, y + colw // 2), lab, fill=(0, 0, 0), font=font(16, True))
        for k_, im in enumerate(ims):
            S.paste(im.resize((colw, colw)), (lab_w + k_ * colw, y))
            if caps and k_ < len(caps) and caps[k_]: d.text((lab_w + 6 + k_ * colw, y + colw + 4), caps[k_], fill=(30, 30, 30), font=font(14))
        y += colw + 34
    for i_, l_ in enumerate(nl): d.text((14, y + 4 + 24 * i_), l_, fill=(60, 60, 60), font=font(15))
    S.save(os.path.join(OUT, fname), quality=88)
PAj = jl(PA + '/HV_partA.json'); HE = jl(W + '/HV_hidden_ear_identity.json')
sheet('HV_01_HVC1_vs_HVF178_central_anchor.jpg', 'Halvren central anchor — HVC1 (c1, accepted W1s diagnostic) | HVF178 (c2, new): front | profile | 3-4 | rear (R-6 source, family human auricle = non-final ear)',
      [(c, [img('src_' + CFG[c]['HV'], v) for v in ('front', 'prof', 'tq', 'rear')], ['%s  %.1f cm' % (CFG[c]['HV'], PAj['envelope']['HVC1' if c == 'c1' else 'HVF178']), '', '', '']) for c in CFG],
      note='HVF178 = MF-F-R route + exactly the HVC1 body targets, stature re-solved (178.01 cm); second resolve max |dV| 0; configuration consistency %d / %d metrics follow the human-family c1 -> c2 pattern' % (PAj['configuration_consistency']['within_human_pattern'], PAj['configuration_consistency']['of']))
sheet('HV_02_source_vs_family.jpg', 'Halvren central anchor — R-6 source vs v005 family realization (silhouette: source only red, family only blue, shared grey) and family wire',
      [(c, [img('src_' + CFG[c]['HV'], 'front'), img('fam_' + CFG[c]['HV'], 'front'), sil(img('src_' + CFG[c]['HV'], 'front'), img('fam_' + CFG[c]['HV'], 'front')), sil(img('src_' + CFG[c]['HV'], 'prof'), img('fam_' + CFG[c]['HV'], 'prof')), img('famw_' + CFG[c]['HV'], 'head')],
        ['source', 'family v005', 'front overlay', 'profile overlay', 'family wire (head)']) for c in CFG], colw=420)
for fn_, ttl, grp in (('HV_03_vs_humans.jpg', 'human family: Marchfolk | Sagekin | Skarn (178 cm diagnostic)', ('MF', 'SG', 'SK')), ('HV_04_vs_frozen_elves.jpg', 'elven family: frozen Fenn | frozen Aelari | frozen Vael', ('FN', 'AE', 'VA'))):
    rows = []
    for c, K in CFG.items():
        for lab, v in (('front', 'bfront'), ('profile', 'bprof')):
            rows.append(('%s %s' % (c, lab), [img('he_' + K['HV'], v)] + [img('he_' + K[s], v) for s in grp] + [sil(img('he_' + K['HV'], v), img('he_' + K[grp[0]], v))],
                         ['Halvren ' + K['HV']] + [NM[s] for s in grp] + ['Halvren only red / %s only blue' % NM[grp[0]]] if lab == 'front' else None))
    pr = PAj['configs']
    sheet(fn_, 'Halvren central anchor vs %s — 178 cm, ears hidden, geometry only' % ttl, rows, colw=380,
          note='\n'.join('%s material metric differences (of %d; >= 1 %% and > 2x human baseline): %s' % (c, pr[c]['source_protection']['MF']['of'], ', '.join('%s %d' % (s, pr[c]['source_protection'][s]['material_metrics']) for s in SRC)) for c in CFG))
for fn_, ttl, views in (('HV_05a_regions_torso_shoulder_pelvis.jpg', 'torso front / profile, shoulders, pelvis oblique', ('tfront', 'tprof', 'shoulder', 'pelvis')),
                        ('HV_05b_regions_limbs_hands_feet.jpg', 'arm, leg, hand, foot', ('arm', 'leg', 'hand', 'foot'))):
    rows = []
    for c, K in CFG.items():
        for v in views:
            rows.append(('%s %s' % (c, v), [img('he_' + K[k], v) for k in ('HV',) + SRC], [NM[k] for k in ('HV',) + SRC] if v == views[0] else None))
    sheet(fn_, 'Halvren central anchor — body regions (%s): Halvren | Marchfolk | Sagekin | Skarn | Fenn | Aelari | Vael, same camera' % ttl, rows, colw=300)
# arithmetic-midpoint diagnostic
fig, axs = plt.subplots(2, 5, figsize=(26, 10), squeeze=False); GR = PAj['groups']; gcol = plt.cm.tab10(np.linspace(0, 1, len(GR)))
for ci, c in enumerate(CFG):
    for pi, (p, a) in enumerate(PAj['configs'][c]['arithmetic_average_audit'].items()):
        ax = axs[ci, pi]; ax.axvspan(0.35, 0.65, color='#eee'); ax.axvline(0, color='k', lw=0.8); ax.axvline(1, color='k', lw=0.8); ax.axvline(0.5, color='k', ls=':', lw=0.8); y = 0; lab = []
        for gi, (g, ks) in enumerate(GR.items()):
            for k in ks:
                if a['t'] and k in a['t']: ax.scatter(np.clip(a['t'][k], -1.5, 2.5), y, color=gcol[gi], s=30); lab.append(k); y += 1
        ax.set_yticks(range(len(lab))); ax.set_yticklabels(lab, fontsize=7); ax.set_xlim(-1.6, 2.6)
        ax.set_title('%s %s: t median %s, blend a %.2f (R2 %.2f)' % (c, p, a['t_median'], a['scalar_blend_fit']['alpha'], a['scalar_blend_fit']['r2']), fontsize=10); ax.set_xlabel('t = (HV - human) / (elf - human); 0 human, 1 elf')
fig.suptitle('Halvren central anchor — arithmetic-average audit: position of each metric (material pair gap only) between the human and elven source of each pair; grey band = 0.35-0.65 midpoint zone'); fig.tight_layout(rect=(0, 0, 1, 0.95))
fig.savefig(os.path.join(OUT, 'HV_06_arithmetic_midpoint_audit.jpg'), dpi=72); plt.close(fig)
# pelvis report
fig, axs = plt.subplots(1, 2, figsize=(20, 6.5))
for ci, c in enumerate(CFG):
    ax = axs[ci]; rows = PAj['pelvis_report'][c]; x = np.arange(len(rows)); wd = 0.13
    for si, s in enumerate(SRC): ax.bar(x + (si - 2.5) * wd, [np.clip(r_['by_t']['0.5']['HV_vs_pct'][s], -12, 12) for r_ in rows], wd, label='HV vs ' + NM[s])
    ax.axhline(0, color='k', lw=0.8); ax.set_xticks(x); ax.set_xticklabels([r_['measure'].split(' (')[0] for r_ in rows], rotation=25, ha='right', fontsize=8); ax.set_ylabel('Halvren vs source (%), skeletal proxy t = 0.5 (clipped +/-12)')
    ax.set_title('%s pelvis — REPORT ONLY (Halvren pelvic inheritance is OPEN)' % c); ax.legend(fontsize=7, ncol=3)
fig.tight_layout(); fig.savefig(os.path.join(TMP, 'pelvis_chart.png'), dpi=80); plt.close(fig)
rows = [(c + ' oblique', [img('he_' + CFG[c][k], 'pelvis') for k in ('HV', 'MF', 'SG', 'FN', 'AE', 'VA')], [NM[k] for k in ('HV', 'MF', 'SG', 'FN', 'AE', 'VA')]) for c in CFG] + [(c + ' front', [img('he_' + CFG[c][k], 'pfront') for k in ('HV', 'MF', 'SG', 'FN', 'AE', 'VA')], None) for c in CFG]
sheet('HV_07_pelvis_report_renders.jpg', 'Halvren central anchor — pelvis (ears hidden, 178 cm): Halvren | Marchfolk | Sagekin | Fenn | Aelari | Vael', rows, colw=320)
ch = Image.open(os.path.join(TMP, 'pelvis_chart.png')).convert('RGB'); ch.save(os.path.join(OUT, 'HV_07b_pelvis_report_chart.jpg'), quality=88)
rows = []
for c, K in CFG.items():
    for lab, v in (('front', 'hfront'), ('profile', 'hprof'), ('3-4', 'htq')): rows.append(('%s %s' % (c, lab), [img('he_' + K[k], v) for k in ('HV',) + SRC], [NM[k] for k in ('HV',) + SRC] if lab == 'front' else None))
sheet('HV_08_hidden_ear_face.jpg', 'Halvren central anchor — hidden-ear neutral-pigment face (ears collapsed, hair removed, neutral expression, 178 cm): Halvren | Marchfolk | Sagekin | Skarn | Fenn | Aelari | Vael', rows, colw=300,
      note='\n'.join('%s: face regions departing materially from humans %d / %d; descriptors departing from Marchfolk %d / %d; nearest source per region %s' % (c, HE['configs'][c]['face_regions_departing_from_humans'], HE['configs'][c]['face_regions_of'], HE['configs'][c]['descriptors_departing_from_MF'], HE['configs'][c]['descriptors_of'], HE['configs'][c]['face_nearest_count']) for c in CFG))
rows = [(c, [img('fres_%s_%s' % (c, k), v) for k in ('MF', 'FN', 'AE', 'VA') for v in ('hfront',)], ['residual vs Marchfolk', 'vs frozen Fenn', 'vs frozen Aelari', 'vs frozen Vael']) for c in CFG]
sheet('HV_09a_face_residual_maps.jpg', 'Halvren central anchor — face residual after similarity alignment onto the Halvren head (blue 0 .. red 4 mm; ear excluded)', rows, colw=420)
fig, axs = plt.subplots(2, 2, figsize=(22, 11))
for ci, c in enumerate(CFG):
    fr = HE['configs'][c]['face']; regs = list(fr); x = np.arange(len(regs)); ax = axs[ci, 0]; wd = 0.12
    for si, s in enumerate(SRC): ax.bar(x + (si - 2.5) * wd, [fr[r]['HV_vs_%s_rms_mm' % s] for r in regs], wd, label=NM[s])
    ax.scatter(x, [fr[r]['SG_vs_MF_rms_mm_human_baseline'] for r in regs], marker='_', s=500, color='k', label='human baseline (SG vs MF)')
    ax.set_xticks(x); ax.set_xticklabels(regs, rotation=20, fontsize=9); ax.set_ylabel('Halvren vs source RMS (mm, aligned)'); ax.set_title('%s face regional residual (Halvren vs source)' % c); ax.legend(fontsize=7, ncol=4)
    ds = HE['configs'][c]['descriptors']; ks = list(ds); ax = axs[ci, 1]
    ax.barh(range(len(ks)), [np.clip(ds[k]['HV_vs_MF_pct'], -12, 12) for k in ks], color='#a32'); ax.barh(np.arange(len(ks)) + 0.4, [np.clip(ds[k]['family_gap_pct'], -12, 12) for k in ks], 0.35, color='#79b')
    ax.set_yticks(range(len(ks))); ax.set_yticklabels(ks, fontsize=8); ax.axvline(0, color='k'); ax.set_xlabel('%: red = Halvren vs Marchfolk; blue = elven-family mean vs human-family mean (the room a mixed face could use)')
    ax.set_title('%s craniofacial descriptors' % c)
fig.suptitle('Halvren central anchor — face regional residual and descriptor sheet (ears excluded)'); fig.tight_layout(rect=(0, 0, 1, 0.96)); fig.savefig(os.path.join(OUT, 'HV_09b_face_descriptors.jpg'), dpi=72); plt.close(fig)
VA_ = {c: jl('%s/val/%s_fam_validator_v2_D1-D6.json' % (W, K['HV'])) for c, K in CFG.items()}; st_ = sorted(VA_['c1']['stations'])
cw = [260, 150, 150, 150, 150, 150, 150]; S = Image.new('RGB', (sum(cw) + 40, 140 + 26 * (len(st_) + 2)), 'white'); d = ImageDraw.Draw(S)
d.text((14, 14), 'Halvren central anchor — validator D1+D3+D4+D5+D6, v005 body-family candidates', fill=(0, 0, 0), font=font(20, True))
d.text((14, 44), 'margin = loops - contract minimum (red = 0).   c1 HV_M_REF_RP3_bodyfam_v001: %d / 69    c2 HV_F_REF_RP3_bodyfam_v001: %d / 69' % (VA_['c1']['summary']['firm_pass_count'], VA_['c2']['summary']['firm_pass_count']), fill=(0, 0, 0), font=font(16))
hdr = ['station', 'c1 loops', 'c1 min', 'c1 margin', 'c2 loops', 'c2 min', 'c2 margin']; y = 90
for i, t in enumerate(hdr): d.text((20 + sum(cw[:i]), y), t, fill=(0, 0, 0), font=font(15, True))
y += 28
with open(os.path.join(OUT, 'HV_validator_margin_table.csv'), 'w', newline='') as fh:
    wr = csv.writer(fh); wr.writerow(hdr + ['c1 status', 'c2 status'])
    for s in st_:
        a, b = VA_['c1']['stations'][s], VA_['c2']['stations'][s]; vals = [s, a['loops_v2'], a['required'], a['margin'], b['loops_v2'], b['required'], b['margin']]; wr.writerow(vals + [a['status_D1_D3'], b['status_D1_D3']])
        for i, t in enumerate(vals): d.text((20 + sum(cw[:i]), y), str(t), fill=(200, 30, 30) if (i in (3, 6) and t == 0) else (0, 0, 0), font=font(14))
        y += 26
S.save(os.path.join(OUT, 'HV_10_validator_margins.jpg'), quality=88)
fig, ax = plt.subplots(figsize=(12, 4.6)); zs = ['face', 'ears', 'hand', 'foot', 'trunk', 'arm', 'leg', 'neck', 'head']; x = np.arange(len(zs))
AU = {c: jl('%s/audit/%s_fam_audit.json' % (W, K['HV']))['density_pct_of_stature'] for c, K in CFG.items()}
for i, c in enumerate(CFG): ax.bar(x + (i - 0.5) * 0.35, [AU[c][z]['mean'] for z in zs], 0.35, label='%s (%s)' % (CFG[c]['HV'], c))
ax.scatter(x, [AU['c1'][z]['limit'] for z in zs], marker='_', s=600, color='k'); ax.set_xticks(x); ax.set_xticklabels(zs); ax.set_ylabel('mean edge / stature (%)')
ax.set_title('Halvren body-family density — 9 standard zones (black bar = limit): %s' % ('all pass' if all(v['pass_mean'] for a in AU.values() for v in a.values()) else 'FAIL')); ax.legend(); fig.tight_layout()
fig.savefig(os.path.join(OUT, 'HV_11_density.jpg'), dpi=105); plt.close(fig)
DF = jl(OUT + '/../HALVREN_deformation_comparison.json'); PN = ('shoulder_abd90_l', 'shoulder_flex90_l', 'elbow_130_l', 'thumb_opposition_l', 'hip_flex90_l', 'knee_90_l', 'knee_140_l', 'trunk_twist30')
sheet('HV_12_deformation.jpg', 'Halvren central anchor — Standard v1 deformation (v005 family; source rig + carried MPFB weights, plain LBS; red = flipped, orange = new contact faces)',
      [(c, [img('pose_%s_%s' % (c, p), 'v') for p in PN], ['%s %d/%d (MF %d/%d)' % (p.replace('_l', ''), DF[CFG[c]['HV']]['poses'][p]['halvren_family'], DF[CFG[c]['HV']]['poses'][p]['selfx_family'], DF[CFG[c]['HV']]['poses'][p]['marchfolk_v005'], DF[CFG[c]['HV']]['poses'][p]['selfx_mf']) for p in PN]) for c in CFG],
      colw=330, note='caption: flips / new contacts (Marchfolk v005 flips / contacts). Contact excess (c1 thumb opposition, c2 knee 90) is already on the native source (19 vs Marchfolk native 12; 28 vs 22): source anatomy (finger / lower-leg length), not topology')
print('sheets done', flush=True)
