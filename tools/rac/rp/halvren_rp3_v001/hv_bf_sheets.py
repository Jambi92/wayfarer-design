# hv_bf_sheets.py OUTDIR : Halvren body / face source order (2026-10-29) §21 visual package (HVBF_01..20). Identical orthographic cameras per row, true
# scale; ears hidden (hm08 w_ears > 0.05 harmonically collapsed) and geometry-only grey shading (pigment / hair / presentation neutral) wherever identity
# is judged. Workbench renders (grask_rigprep_v001/render_attr.py) + PIL / matplotlib; resumable; 2 Blender processes.
import sys, os, json, subprocess, numpy as np, scipy.sparse as sp
from PIL import Image, ImageDraw, ImageFont
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001')
import fn_face_metrics as F
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True); W = '/tmp/claude-0/rt/hv'; TMP = os.environ.get('HV_SHEET_TMP', W + '/bf_sheet_r'); OV = W + '/bf_ov'; os.makedirs(TMP, exist_ok=True); os.makedirs(OV, exist_ok=True)
BP = '/home/claude/stc/bin/python3'; REND = '/home/claude/wayfarer-design/tools/rac/rp/grask_rigprep_v001/render_attr.py'; PA = W + '/partA'; HB = W + '/hb/cand'; HE = W + '/hbe'; HPD = W + '/hp'
GREY = np.array([0.80, 0.78, 0.76]); jl = lambda p: json.load(open(p))
CF = {'c1': dict(pre='HVC1', HV0=PA + '/ref/HVC1', MF='MFM178', SG='SGM178', SK='SKM178', FN='FNM178', AE='AEM178', VA='VAM178'), 'c2': dict(pre='HVF178', HV0=PA + '/build/HVF178', MF='MFF178', SG='SGF178', SK='SKF178', FN='FNF178', AE='AEF178', VA='VAF178')}
NM = dict(HV0='current HVC1/HVF178', MF='Marchfolk', SG='Sagekin', SK='Skarn (178 diag.)', FN='frozen Fenn', AE='frozen Aelari', VA='frozen Vael')
TAGS = ['HB1', 'HB2', 'HB3', 'HB1HF1', 'HB2HF2', 'HB3HF3', 'HB2HF1', 'HB2HF3']
def path(c, k):
    C = CF[c]
    if k == 'HV0': return C['HV0'] + '_r6.npz'
    if k in ('MF', 'SG', 'SK', 'FN', 'AE', 'VA'): return '%s/cmp/%s_r6.npz' % (PA, C[k])
    if k.startswith('HP'): return '%s/cand/%s-HB2HF2-%s_r6.npz' % (HPD, C['pre'], k.replace('-', ''))
    return '%s/%s-%s_r6.npz' % (HB, C['pre'], k)
nz = np.load('/tmp/claude-0/rt/fn/src/FNL4_native.npz'); Q = np.asarray(nz['Q']); nV = len(nz['src_index'])
A = sp.coo_matrix((np.ones(4 * len(Q)), (Q[:, :4].ravel(), np.roll(Q, -1, 1).ravel())), shape=(nV, nV)).tocsr(); A = ((A + A.T) > 0).astype(float); deg = np.asarray(A.sum(1)).ravel()
def hidden(c, k):
    o = '%s/%s_%s.npz' % (OV, c, k)
    if not os.path.exists(o):
        V = F.load(path(c, k))['V'].copy(); ear = F.EAR
        for _ in range(400): V[ear] = (A @ V)[ear] / deg[ear, None]
        np.savez(o, V=V, Q=Q)
    return o
def font(sz, bold=False):
    f = '/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf' % ('-Bold' if bold else ''); return ImageFont.truetype(f, sz) if os.path.exists(f) else ImageFont.load_default()
jobs = []
def render(tag, npz, col, views, wire=False, px=480):
    vs = ';'.join('%s:%s:%s:%.2f' % (n, ','.join('%.4f' % x for x in d), ','.join('%.3f' % x for x in c_), hs) for n, d, c_, hs in views)
    cf = os.path.join(TMP, tag + '_col.npy'); np.save(cf, np.asarray(col, np.float32)); jobs.append([BP, REND, '--', npz, cf, TMP, tag, vs, '1' if wire else '0', str(px)])
def img(tag, name):
    p = os.path.join(TMP, '%s_%s.png' % (tag, name)); return Image.open(p).convert('RGB') if os.path.exists(p) else Image.new('RGB', (600, 600), 'white')
def heat(x, lo, hi):
    t = np.clip((x - lo) / (hi - lo + 1e-12), 0, 1)[:, None]; return (1 - t) * np.array([0.2, 0.35, 0.85]) + t * np.array([0.95, 0.25, 0.15])
def sil(a, b):
    A_ = np.asarray(a, int); B_ = np.asarray(b, int); ma = (np.abs(A_ - A_[2, 2]).max(2) > 10); mb = (np.abs(B_ - B_[2, 2]).max(2) > 10)
    O_ = np.full(A_.shape, 255, np.uint8); O_[ma & mb] = (150, 150, 150); O_[ma & ~mb] = (215, 40, 40); O_[~ma & mb] = (40, 90, 220); return Image.fromarray(O_)
def joints(c):
    j = json.loads(str(np.load(path(c, 'HB2HF2'))['joints'])); z = lambda b: j[b][0][2]
    return dict(clav=0.5 * (z('clavicle_l') + z('clavicle_r')), sp1=z('spine_01'), hip=0.5 * (z('thigh_l') + z('thigh_r')), knee=0.5 * (z('calf_l') + z('calf_r')))
BODYK = ['HV0', 'HB1', 'HB2', 'HB3', 'MF', 'SG', 'SK', 'FN', 'AE', 'VA', 'HB1HF1', 'HB2HF2', 'HB3HF3', 'HB2HF1', 'HB2HF3', 'HP-B', 'HP-C']
CAM = {}
for c in CF:
    Vh = np.load(hidden(c, 'HB2HF2'))['V']; ym = Vh[:, 1].mean(); jv = joints(c); B = np.array([0.0, ym, 90.0]); H = np.array([0.0, Vh[Vh[:, 2] > Vh[:, 2].max() - 25][:, 1].mean(), Vh[:, 2].max() - 12.0])
    CAM[c] = dict(bfront=((0, 1, 0), B, 95), bprof=((1, 0, 0), B, 95), btq=((1, 1, 0.05), B, 95), hfront=((0, 1, 0.03), H, 14.5), hprof=((1, 0, 0), H, 14.5), htq=((1, 1, 0.1), H, 14.5),
                  htop=((0.05, 0.4, 1), H + np.array([0, 0, 4]), 13), brow=((0.15, 1, 0.12), H + np.array([0, -2, 3]), 7.5), cheek=((0.75, 1, -0.15), H + np.array([3.5, -4, -1.5]), 7.5),
                  jaw=((0.6, 1, -0.45), H + np.array([0, -3, -6]), 8.5), tfront=((0, 1, 0), np.array([0, ym, 0.5 * (jv['sp1'] + jv['clav'])]), 32), tprof=((1, 0, 0), np.array([0, ym, 0.5 * (jv['sp1'] + jv['clav'])]), 32),
                  shoulder=((0.25, 1, 0.12), np.array([0, ym, jv['clav'] + 6]), 24), arm=((0, 1, 0), np.array([0, ym, 0.5 * (jv['clav'] + jv['hip']) - 8]), 44), leg=((1, 0, 0), np.array([0, ym, jv['knee']]), 50),
                  hand=((0.3, 1, 0.0), np.array([Vh[:, 0].max() - 9, ym, jv['hip'] - 22]), 14), foot=((0.8, 0.6, 0.6), np.array([11.0, 6.0, 6.0]), 14), pelvis=((1, 0.25, 0.0), np.array([0, ym, jv['hip'] + 4]), 28),
                  pfront=((0, 1, 0), np.array([0, ym, jv['hip'] + 4]), 28))
VIEWS = list(CAM['c1'])
for c in CF:
    for k in BODYK:
        p = hidden(c, k); V = np.load(p)['V']; render('%s_%s' % (c, k), p, np.tile(GREY, (len(V), 1)), [(v,) + CAM[c][v] for v in VIEWS])
    # before / after displacement (HB2 vs current) and face residual heat maps
    a = F.load(path(c, 'HB2'))['V']; b = F.load(path(c, 'HV0'))['V']; d = np.linalg.norm(a - b, axis=1) * 10; C = heat(d, 0, 15); C[F.EAR] = GREY
    render('%s_dispHB2' % c, hidden(c, 'HB2'), C, [(v,) + CAM[c][v] for v in ('bfront', 'bprof')])
    hd = F.HEAD
    for k in ('HB2HF1', 'HB2HF2', 'HB2HF3'):
        Vv = F.load(path(c, k))['V']
        for s in ('MF', 'FN', 'AE', 'VA'):
            if s != 'MF' and k != 'HB2HF2': continue
            f = F.procrustes(F.load(path(c, s))['V'][hd], Vv[hd]); dd = np.linalg.norm(f(F.load(path(c, s))['V']) - Vv, axis=1) * 10; C = np.tile(GREY, (len(Vv), 1)); C[hd] = heat(dd[hd], 0, 4.0); C[F.EAR] = GREY
            render('%s_fres_%s_%s' % (c, k, s), hidden(c, k), C, [(v,) + CAM[c][v] for v in ('hfront', 'hprof')])
    for pn in ('shoulder_abd90_l', 'shoulder_flex90_l', 'elbow_130_l', 'thumb_opposition_l', 'hip_flex90_l', 'knee_90_l', 'knee_140_l', 'neck_rot45'):
        pp = '%s/def/%s_%s-HB2HF2_fam.npz' % (HE, pn, CF[c]['pre']); fz = '%s/fam/%s-HB2HF2_fam.npz' % (HE, CF[c]['pre'])
        if not (os.path.exists(pp) and os.path.exists(fz)): continue
        X = np.load(pp); Qf = np.load(fz)['Q']; Cf = np.tile(GREY, (len(Qf), 1)); fl = np.asarray(X['flip']).astype(int).ravel(); Cf[fl[fl < len(Cf)]] = [0.92, 0.18, 0.12]
        q = os.path.join(TMP, 'pose_%s_%s.npz' % (c, pn)); np.savez_compressed(q, V=X['V'], Q=Qf); Xv = X['V']
        render('pose_%s_%s' % (c, pn), q, Cf, [('v', (1, 1, 0.05), np.array([Xv[:, 0].mean(), Xv[:, 1].mean(), (Xv[:, 2].max() + Xv[:, 2].min()) / 2]), 98)], px=420)
print('render jobs', len(jobs), flush=True)
done_ = lambda j: all(os.path.exists(os.path.join(TMP, '%s_%s.png' % (j[6], v_.split(':')[0]))) for v_ in j[7].split(';'))
todo = [j for j in jobs if not done_(j)]; print('to render', len(todo), flush=True)
with ThreadPoolExecutor(int(os.environ.get('HV_SHEET_THREADS', '2'))) as ex: list(ex.map(lambda j: subprocess.run(j, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL), todo))
# ---------------------------------------------------------------- compose
def sheet(fname, title, rows, colw=420, note=None, lab_w=150):
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
EV = {c: jl('%s/hb/HB_eval_%s.json' % (W, c))['items'] for c in CF}
mcap = lambda c, k: '%s  vs MF %d mat, %d groups' % (k, EV[c][k]['body']['source_protection']['MF']['material'], EV[c][k]['body']['groups_with_signal_vs_MF']) if k in EV[c] else k
L = lambda k: NM.get(k, k)
sheet('HVBF_01_current_vs_HB.jpg', 'Halvren body candidates — current HVC1 | HB1 | HB2 | HB3 (c1; 178 cm, ears hidden; body only, current face)',
      [(v, [img('c1_' + k, v) for k in ('HV0', 'HB1', 'HB2', 'HB3')], [mcap('c1', k) for k in ('HV0', 'HB1', 'HB2', 'HB3')] if v == 'bfront' else None) for v in ('bfront', 'bprof', 'btq')], colw=460)
sheet('HVBF_02_c1_c2_HB.jpg', 'Halvren body candidates — c1 | c2 of each HB candidate (one shared design on both configurations), front | profile',
      [('%s %s' % (k, v), [img('c1_' + k, v), img('c2_' + k, v)], ['c1 ' + mcap('c1', k), 'c2 ' + mcap('c2', k)] if v == 'bfront' else None) for k in ('HB1', 'HB2', 'HB3') for v in ('bfront', 'bprof')], colw=420)
for fn_, ttl, grp in (('HVBF_03_HB2_vs_humans.jpg', 'Marchfolk | Sagekin | Skarn (178 diag.)', ('MF', 'SG', 'SK')), ('HVBF_04_HB2_vs_frozen_elves.jpg', 'frozen Fenn | frozen Aelari | frozen Vael', ('FN', 'AE', 'VA'))):
    rows = []
    for c in CF:
        for v in ('bfront', 'bprof'):
            rows.append(('%s %s' % (c, v), [img('%s_HB2' % c, v)] + [img('%s_%s' % (c, s), v) for s in grp] + [sil(img('%s_HB2' % c, v), img('%s_%s' % (c, grp[0]), v))],
                         ['HB2'] + [L(s) for s in grp] + ['HB2 only red / %s only blue' % L(grp[0])] if v == 'bfront' else None))
    sheet(fn_, 'Halvren HB2 vs %s — 178 cm, ears hidden, geometry only' % ttl, rows, colw=360,
          note='\n'.join('%s HB2 material metric differences (of 31): %s' % (c, ', '.join('%s %d' % (s, EV[c]['HB2']['body']['source_protection'][s]['material']) for s in ('MF', 'SG', 'SK', 'FN', 'AE', 'VA'))) for c in CF))
for fn_, views in (('HVBF_05a_regions_torso_shoulder_arm.jpg', ('tfront', 'tprof', 'shoulder', 'arm')), ('HVBF_05b_regions_leg_hand_foot.jpg', ('leg', 'hand', 'foot'))):
    ks = ('HV0', 'HB1', 'HB2', 'HB3', 'MF', 'FN', 'AE', 'VA')
    sheet(fn_, 'Halvren body candidates — close regions (%s): current | HB1 | HB2 | HB3 | Marchfolk | Fenn | Aelari | Vael, same camera' % ', '.join(views),
          [('%s %s' % (c, v), [img('%s_%s' % (c, k), v) for k in ks], [L(k) for k in ks] if v == views[0] else None) for c in CF for v in views], colw=270)
fig, axs = plt.subplots(2, 3, figsize=(24, 13), squeeze=False); GR = jl(PA + '/HV_partA.json')['groups']; gcol = plt.cm.tab10(np.linspace(0, 1, len(GR)))
for ci, c in enumerate(CF):
    for pi, p in enumerate(('MF-FN', 'MF-AE', 'MF-VA')):
        ax = axs[ci, pi]; ax.axvspan(0.35, 0.65, color='#eee'); [ax.axvline(x, color='k', lw=0.8, ls=ls) for x, ls in ((0, '-'), (1, '-'), (0.5, ':'))]; lab = []; y = 0
        for gi, (g, ks) in enumerate(GR.items()):
            for k in ks:
                hit = False
                for ti, (t, mk) in enumerate((('HB1', 'o'), ('HB2', 's'), ('HB3', '^'))):
                    tv = EV[c][t]['body']['arithmetic_average_audit'][p]['t'].get(k)
                    if tv is not None: ax.scatter(np.clip(tv, -1.5, 2.5), y + (ti - 1) * 0.22, color=gcol[gi], marker=mk, s=26); hit = True
                if hit: lab.append(k); y += 1
        ax.set_yticks(range(len(lab))); ax.set_yticklabels(lab, fontsize=7); ax.set_xlim(-1.6, 2.6)
        a2 = EV[c]['HB2']['body']['arithmetic_average_audit'][p]
        ax.set_title('%s %s (o HB1, s HB2, ^ HB2/3): HB2 blend a %.2f, R2 %.2f, t IQR %s' % (c, p, a2['alpha'], a2['r2'], a2['t_iqr']), fontsize=10); ax.set_xlabel('t = (HV - human) / (elf - human)')
fig.suptitle('Halvren body candidates — arithmetic-average audit (material pair gap metrics only; grey = midpoint zone). Domain-specific spread, not one alpha'); fig.tight_layout(rect=(0, 0, 1, 0.95))
fig.savefig(os.path.join(OUT, 'HVBF_06_arithmetic_midpoint.jpg'), dpi=68); plt.close(fig)
sheet('HVBF_07_before_after_displacement.jpg', 'Halvren HB2 vs current HVC1 / HVF178 — vertex displacement (blue 0 .. red 15 mm; same stature 178 cm, ears excluded)',
      [(c, [img('%s_dispHB2' % c, 'bfront'), img('%s_dispHB2' % c, 'bprof'), img('%s_HV0' % c, 'bfront'), img('%s_HB2' % c, 'bfront')], ['displacement front', 'profile', 'current', 'HB2']) for c in CF], colw=420)
fk = ('HV0', 'HB2HF1', 'HB2HF2', 'HB2HF3'); fcap = lambda c, k: '%s  regions off MF %d/7' % (k, EV[c][k]['face']['regions_departing_from_MF']) if k in EV[c] else 'current face'
sheet('HVBF_08_current_face_vs_HF.jpg', 'Halvren face candidates — current face | HF1 | HF2 | HF3 (on the HB2 body), ears hidden, neutral', [('%s %s' % (c, v), [img('%s_%s' % (c, k), v) for k in fk], [fcap(c, k) for k in fk] if v == 'hfront' else None) for c in CF for v in ('hfront', 'hprof', 'htq')], colw=380)
for fn_, ttl, grp in (('HVBF_09_HF2_vs_humans.jpg', 'human family', ('MF', 'SG', 'SK')), ('HVBF_10_HF2_vs_frozen_elves.jpg', 'frozen elves', ('FN', 'AE', 'VA'))):
    sheet(fn_, 'Halvren HF2 hidden-ear neutral face vs %s (ears collapsed, hair removed)' % ttl, [('%s %s' % (c, v), [img('%s_HB2HF2' % c, v)] + [img('%s_%s' % (c, s), v) for s in grp], ['HF2'] + [L(s) for s in grp] if v == 'hfront' else None) for c in CF for v in ('hfront', 'hprof', 'htq')], colw=380)
for n_, (fn_, v, ttl) in enumerate((('HVBF_11_cranium.jpg', 'htop', 'cranium (top-front)'), ('HVBF_12_brow_orbit.jpg', 'brow', 'brow / orbit'), ('HVBF_13_cheeks_midface.jpg', 'cheek', 'cheeks / midface (3-4 low)'), ('HVBF_14_jaw_chin.jpg', 'jaw', 'jaw / chin (3-4 below)'))):
    ks = ('HV0', 'HB2HF1', 'HB2HF2', 'HB2HF3', 'MF', 'FN', 'AE', 'VA')
    sheet(fn_, 'Halvren face candidates — %s: current | HF1 | HF2 | HF3 | Marchfolk | Fenn | Aelari | Vael' % ttl, [(c, [img('%s_%s' % (c, k), v) for k in ks], [L(k) for k in ks]) for c in CF], colw=280)
rows = [(c, [img('%s_fres_%s_MF' % (c, k), 'hfront') for k in ('HB2HF1', 'HB2HF2', 'HB2HF3')] + [img('%s_fres_HB2HF2_%s' % (c, s), 'hfront') for s in ('FN', 'AE', 'VA')], ['HF1 vs MF', 'HF2 vs MF', 'HF3 vs MF', 'HF2 vs Fenn', 'HF2 vs Aelari', 'HF2 vs Vael']) for c in CF]
sheet('HVBF_15_face_residuals.jpg', 'Halvren face candidates — residual after similarity alignment (blue 0 .. red 4 mm; ears excluded)', rows, colw=340)
XP = jl(W + '/hbe/HV_expression_sanity.json') if os.path.exists(W + '/hbe/HV_expression_sanity.json') else None
if XP:
    bods = list(XP['bodies']); us = list(XP['bodies'][bods[0]])
    fig, ax = plt.subplots(figsize=(20, 0.45 * len(bods) + 2.2)); ax.axis('off')
    cell = [[b] + ['%d / %d' % (XP['bodies'][b][u]['new_selfx_pairs'], XP['bodies'][b][u]['flipped_faces']) for u in us] for b in bods]
    t = ax.table(cellText=cell, colLabels=['body'] + [u.split(' (')[0] for u in us], loc='center'); t.auto_set_font_size(False); t.set_fontsize(8); t.scale(1, 1.4)
    ax.set_title('Halvren face candidates — expression sanity (MPFB expression units on the source, carried to the v005 family): new head contact pairs / flipped faces; rows HV0 = current face (generic MPFB baseline)')
    fig.tight_layout(); fig.savefig(os.path.join(OUT, 'HVBF_16_expression_sanity.jpg'), dpi=90); plt.close(fig)
PR = ('HB1HF1', 'HB2HF2', 'HB3HF3', 'HB2HF1', 'HB2HF3')
sheet('HVBF_17_pair_matrix.jpg', 'Halvren body x face pair matrix (c1 / c2; ears hidden): HB1+HF1 | HB2+HF2 | HB3+HF3 | HB2+HF1 | HB2+HF3', [('%s %s' % (c, v), [img('%s_%s' % (c, k), v) for k in PR], list(PR) if v == 'bfront' else None) for c in CF for v in ('bfront', 'htq')], colw=360)
sheet('HVBF_18_recommended_pair.jpg', 'Halvren recommended central pair HB2 + HF2 — c1 / c2 full body and head (ears hidden; family human auricle is non-final)',
      [(c, [img('%s_HB2HF2' % c, v) for v in ('bfront', 'bprof', 'btq', 'hfront', 'hprof')], None) for c in CF], colw=400)
HPJ = jl(W + '/hp/HV_pelvis_package.json') if os.path.exists(W + '/hp/HV_pelvis_package.json') else None
rows = [('%s %s' % (c, v), [img('%s_%s' % (c, k), v) for k in ('HB2HF2', 'HP-B', 'HP-C', 'MF', 'FN', 'AE', 'VA')], ['HP-A (HB2HF2)', 'HP-B mild', 'HP-C stronger', 'Marchfolk', 'Fenn', 'Aelari', 'Vael'] if v == 'pelvis' else None) for c in CF for v in ('pelvis', 'pfront')]
note = None
if HPJ:
    note = '\n'.join('%s %s: hip ht %s | pelvic vert / crest vs MF %+.2f %% | AP depth vs MF %+.2f %% | crest vs MF %+.2f %%' % (hp, c, HPJ['hp']['%s %s' % (hp, c)]['skeletal_proxy']['leg_share']['0.5']['value'],
                     HPJ['hp']['%s %s' % (hp, c)]['skeletal_proxy']['pelvic_vertical_over_crest']['0.5']['vs_MF_pct'], HPJ['hp']['%s %s' % (hp, c)]['skeletal_proxy']['pelvic_depth_share']['0.5']['vs_MF_pct'],
                     HPJ['hp']['%s %s' % (hp, c)]['skeletal_proxy']['crest_share']['0.5']['vs_MF_pct']) for c in CF for hp in ('HP-A', 'HP-B', 'HP-C'))
sheet('HVBF_19_pelvis_decision.jpg', 'Halvren pelvis AUTHOR-DECISION package (diagnostic, not canon): HP-A human-family-dominant | HP-B mild mixed | HP-C stronger mixed, on HB2+HF2', rows, colw=300, note=note)
TS = jl(W + '/hbe/HV_bf_technical.json') if os.path.exists(W + '/hbe/HV_bf_technical.json') else None
if TS:
    ids = list(TS); fig, axs = plt.subplots(1, 3, figsize=(24, 6))
    axs[0].bar(range(len(ids)), [TS[i]['validator'] for i in ids], color='#5a8'); axs[0].axhline(69, color='k'); axs[0].set_ylim(60, 70); axs[0].set_title('validator D1-D6 firm / 69')
    axs[1].bar(range(len(ids)), [TS[i]['density_max_over_limit'] for i in ids], color='#58a'); axs[1].axhline(1.0, color='k'); axs[1].set_title('density: worst zone mean / limit (< 1 = pass)')
    axs[2].bar(np.arange(len(ids)) - 0.2, [TS[i]['worst_flip_excess'] for i in ids], 0.4, label='worst flip excess vs MF v005'); axs[2].bar(np.arange(len(ids)) + 0.2, [TS[i]['new_contact_class'] for i in ids], 0.4, label='new rest-contact class')
    axs[2].legend(); axs[2].set_title('Standard v1 deformation / contact')
    for ax in axs: ax.set_xticks(range(len(ids))); ax.set_xticklabels(ids, rotation=60, ha='right', fontsize=8)
    fig.suptitle('Halvren body x face candidates on frozen MPFB v005 — technical summary'); fig.tight_layout(rect=(0, 0, 1, 0.93)); fig.savefig(os.path.join(OUT, 'HVBF_20_technical_summary.jpg'), dpi=80); plt.close(fig)
PN = ('shoulder_abd90_l', 'shoulder_flex90_l', 'elbow_130_l', 'thumb_opposition_l', 'hip_flex90_l', 'knee_90_l', 'knee_140_l', 'neck_rot45')
sheet('HVBF_20b_deformation_HB2HF2.jpg', 'Halvren HB2 + HF2 — Standard v1 deformation (v005 family, plain LBS; red = flipped)', [(c, [img('pose_%s_%s' % (c, p), 'v') for p in PN], list(PN)) for c in CF], colw=300)
print('sheets done', flush=True)
