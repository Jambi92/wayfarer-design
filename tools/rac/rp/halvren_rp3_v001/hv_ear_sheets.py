# hv_ear_sheets.py EVIDIR OUTDIR : Halvren central-accept + mixed-ear order §24 visual package HVE_01..25. Identical orthographic cameras per configuration
# (left root frame of the common HB2+HF2+HP-B head; true scale), neutral clay wherever the read is judged. Workbench renders (grask render_attr.py)
# composed with PIL / matplotlib; resumable; 2 Blender processes.
import sys, os, json, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
from concurrent.futures import ThreadPoolExecutor
os.environ.setdefault('EAR_TOPO', 'v002')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import hv_ear_domains as D; import hv_ear_quick as QK
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001'); import ear_branch_lib as E
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
EV, OUT = sys.argv[1:3]; os.makedirs(OUT, exist_ok=True); TMP = os.environ.get('HV_SHEET_TMP', '/tmp/claude-0/rt/hv/ear/sheet_r'); os.makedirs(TMP, exist_ok=True); QK.TMP = TMP
EW = '/tmp/claude-0/rt/hv/ear'; HP = '/tmp/claude-0/rt/hv/hpe'; jl = lambda p: json.load(open(p)); GREY = np.array([0.80, 0.78, 0.76])
HEADS = {'c1': 'HVC1-HB2HF2-HPB', 'c2': 'HVF178-HB2HF2-HPB'}; HE = ['HE1', 'HE2', 'HE3']
S = jl(EV + '/HV_ear_summary.json'); A = jl(EV + '/HV_ear_audit.json'); PRB = jl(EV + '/HV_ear_probes_HE2.json'); V6 = jl(EV + '/HV_HPB_validation.json')
def he(c, k): return '%s/he/build/%s_%s_branch.npz' % (EW, HEADS[c], k)
def mf(c): return '%s/fam/%s_fam.npz' % (HP, HEADS[c])
REF = {'FN': '%s/ref/FN/build/%s_E2_branch.npz' % (EW, HEADS['c1']), 'AE': '%s/ref/FN/build/%s_AE-E2_branch.npz' % (EW, HEADS['c1']), 'VA': '%s/ref/RI3/build/%s_VA-E2-RI3_branch.npz' % (EW, HEADS['c1'])}
LAB = dict(MF='Marchfolk (family human auricle)', HE1='HE1 human-forward', HE2='HE2 balanced central', HE3='HE3 elf-forward', FN='frozen Fenn E2', AE='frozen Aelari AE-E2', VA='frozen Vael VA-E2-RI3')
def font(sz, bold=False):
    f = '/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf' % ('-Bold' if bold else ''); return ImageFont.truetype(f, sz) if os.path.exists(f) else ImageFont.load_default()
jobs = []
def R_(tag, npz, head, views, col=None, wire=False, px=560): jobs.append(QK.run(tag, npz, head, views, px, col, wire))
def img(tag, v):
    p = os.path.join(TMP, '%s_%s.png' % (tag, v)); return Image.open(p).convert('RGB') if os.path.exists(p) else Image.new('RGB', (560, 560), (255, 200, 200))
def heat(x, lo, hi):
    t = np.clip((x - lo) / (hi - lo + 1e-12), 0, 1)[:, None]; return (1 - t) * np.array([0.2, 0.35, 0.85]) + t * np.array([0.95, 0.25, 0.15])
def part_cols(z):
    p = z['part']; C = np.tile(GREY, (len(z['V']), 1)); C[p == 'front'] = [0.88, 0.66, 0.55]; C[p == 'back'] = [0.70, 0.58, 0.80]; C[p == 'rim'] = [0.95, 0.83, 0.45]
    C[p == 'cuff'] = [0.58, 0.76, 0.92]; C[p == 'transition'] = [0.55, 0.85, 0.55]; return C
Lo = E.canonical_layout(); st = Lo['st']; ns = len(st)
ANAT = [('helix', (0.95, 0.75, 0.2)), ('antihelix_stem', (0.3, 0.7, 0.3)), ('superior_crus', (0.1, 0.55, 0.45)), ('inferior_crus', (0.55, 0.8, 0.3)), ('triangular_fossa', (0.6, 0.4, 0.8)),
        ('cymba', (0.3, 0.45, 0.85)), ('cavum', (0.15, 0.25, 0.6)), ('crus_of_helix', (0.9, 0.45, 0.2)), ('tragus', (0.85, 0.2, 0.25)), ('antitragus', (0.95, 0.45, 0.6)),
        ('intertragic_notch', (0.45, 0.15, 0.15)), ('lobe_thickening', (0.95, 0.9, 0.6))]
def anat_cols(npz, cand):
    z = np.load(npz); r = jl(npz.replace('.npz', '.json')); p = dict(r['params']); p['taper'] = tuple(p['taper']); p['helix'] = tuple(p['helix'])
    _, _, parts = E.relief(st[:, 0], st[:, 1], p); C = np.tile(GREY, (len(z['V']), 1)); fr = Lo['part'][:ns] == 'front'
    M = np.array([np.abs(parts[k]) for k, _ in ANAT]); w = M.argmax(0); amp = M.max(0); up = st[:, 0] > p['taper'][1]
    for sd in ('l', 'r'):
        f0 = np.nonzero(z['side'] == sd)[0][0]; idx = np.arange(ns)
        cc = np.tile([0.86, 0.84, 0.80], (ns, 1)); cc[up & fr] = [0.80, 0.86, 0.95]                                       # upper extension (above taper start)
        for i, (k, col) in enumerate(ANAT): m = fr & (w == i) & (amp > 0.03); cc[m] = col
        C[f0 + idx[fr]] = cc[fr]
    return C
# ------------------------------------------------------------------ render jobs
BODYV = lambda V: {'bfront': ((0, 1, 0.03), np.array([0, V[:, 1].mean(), (V[:, 2].max() + V[:, 2].min()) / 2]), 96), 'bprof': ((1, 0, 0.0), np.array([0, V[:, 1].mean(), (V[:, 2].max() + V[:, 2].min()) / 2]), 96),
                    'btq': ((1, 1, 0.08), np.array([0, V[:, 1].mean(), (V[:, 2].max() + V[:, 2].min()) / 2]), 96), 'brear': ((0, -1, 0.03), np.array([0, V[:, 1].mean(), (V[:, 2].max() + V[:, 2].min()) / 2]), 96)}
for c in HEADS:
    V = np.load(mf(c))['V']; BV = BODYV(V); vs = ';'.join('%s:%s:%s:%.2f' % (k, ','.join('%.4f' % x for x in d), ','.join('%.3f' % x for x in ce), hs) for k, (d, ce, hs) in BV.items())
    cf = os.path.join(TMP, 'body_%s_col.npy' % c); np.save(cf, np.tile(GREY, (len(V), 1)).astype(np.float32)); jobs.append([QK.BP, QK.REND, '--', mf(c), cf, TMP, 'body_' + c, vs, '0', '700'])
GV = ['front', 'prof', 'tqf', 'rear', 'elat', 'etq', 'etqr', 'root']
for c, h in HEADS.items():
    R_('%s_MF_g' % c, mf(c), h, GV)
    for k in HE:
        p = he(c, k); z = np.load(p); R_('%s_%s_g' % (c, k), p, h, GV); R_('%s_%s_w' % (c, k), p, h, ['elat', 'etqr', 'root'], part_cols(z), True)
        R_('%s_%s_an' % (c, k), p, h, ['elat'], anat_cols(p, k))
        a = '%s/he/audit/%s_%s_audit_perface.npz' % (EW, h, k)
        if os.path.exists(a):
            q = np.load(a); F_, bad, asp = q['faces'], q['ang_bad'], q['asp']; C = np.tile(GREY, (len(z['Q']), 1)) * 0.6 + 0.35; C[F_] = [0.93, 0.93, 0.93]; C[F_[bad]] = [0.92, 0.18, 0.12]
            R_('%s_%s_t4' % (c, k), p, h, ['elat', 'root'], C, True)
            C = np.tile(GREY, (len(z['Q']), 1)); C[F_] = heat(asp, 1.0, 6.0); C[F_[asp > 6]] = [0.55, 0.1, 0.65]; R_('%s_%s_as' % (c, k), p, h, ['elat'], C, True)
        Q = z['Q']; X = z['V'][Q]; el = np.mean([np.linalg.norm(X[:, i] - X[:, (i + 1) % 4], axis=1) for i in range(4)], 0); stt = z['V'][:, 2].max() - z['V'][:, 2].min()
        br = (z['part'][Q] != 'v005').any(1); C = np.tile(GREY, (len(Q), 1)); C[br] = heat(100 * el[br] / stt, 0.03, 0.25); R_('%s_%s_dn' % (c, k), p, h, ['elat'], C, True)
        rec = jl(p.replace('.npz', '.json')); C = np.tile(GREY, (len(z['V']), 1))
        for sd in ('l', 'r'):
            fr = rec['sides'][sd]['frame']; O, n, b, u = [np.array(fr[q]) for q in ('O', 'n', 'b', 'u')]; sk = D.frame(h, sd)['skull']; m = (z['side'] == sd) & (z['part'] == 'cuff')
            X_ = z['V'][m] - O; C[m] = heat(X_ @ n - sk(np.c_[X_ @ b, X_ @ u]), 0.0, 0.6)
        R_('%s_%s_rd' % (c, k), p, h, ['elat', 'root'], C)
for k, p in REF.items(): R_('c1_%s_g' % k, p, HEADS['c1'], ['elat', 'etq', 'etqr', 'front'])
DG = {'HV-DFN': 'FN', 'HV-DAE': 'AE', 'HV-DVA': 'VA', 'HV-DHU': 'MF'}
for k in DG: R_('c1_%s_g' % k, '%s/he/build/%s_%s_branch.npz' % (EW, HEADS['c1'], k), HEADS['c1'], ['elat', 'etq', 'etqr', 'front'])
MOS = [('HB2+HF2 + HE1', he('c1', 'HE1'), HEADS['c1']), ('HB2+HF2 + HE2', he('c1', 'HE2'), HEADS['c1']), ('HB2+HF2 + HE3', he('c1', 'HE3'), HEADS['c1']),
       ('HB2+HF1 + HE3', '%s/mos/build/HVC1-HB2HF1-HPB_HE3_branch.npz' % EW, 'HVC1-HB2HF1-HPB'), ('HB2+HF3 + HE1', '%s/mos/build/HVC1-HB2HF3-HPB_HE1_branch.npz' % EW, 'HVC1-HB2HF3-HPB')]
for i, (l, p, h) in enumerate(MOS): R_('mos%d' % i, p, h, ['tqf', 'front', 'etq'])
PN = ('neck_flex30', 'neck_ext30', 'head_yaw_l45', 'head_yaw_r45', 'head_pitch_down20', 'head_pitch_up20', 'head_roll_l20', 'head_roll_r20')
for c, h in HEADS.items():
    z = np.load(he(c, 'HE2'))
    for pn in PN:
        f = '%s/he/deform/%s_HE2_%s.npy' % (EW, h, pn)
        if not os.path.exists(f): continue
        X = np.load(f); q = os.path.join(TMP, 'epose_%s_%s.npz' % (c, pn)); np.savez_compressed(q, V=X, Q=z['Q']); Ce = X[z['side'] == 'l'].mean(0)
        cf = os.path.join(TMP, 'epose_%s_%s_col.npy' % (c, pn)); np.save(cf, part_cols(z).astype(np.float32))
        jobs.append([QK.BP, QK.REND, '--', q, cf, TMP, 'epose_%s_%s' % (c, pn), 'tq:1.0000,0.3000,0.1000:%s:7.00' % ','.join('%.3f' % x for x in Ce), '0', '420'])
for pn in sorted(PRB['probes']):
    p = '%s/he/probe/%s/%s_HE2_branch.npz' % (EW, pn, HEADS['c1'])
    if os.path.exists(p): R_('pr_' + pn, p, HEADS['c1'], ['etq'], px=420)
print('render jobs', len(jobs), flush=True)
done_ = lambda j: all(os.path.exists(os.path.join(TMP, '%s_%s.png' % (j[6], v_.split(':')[0]))) for v_ in j[7].split(';'))
todo = [j for j in jobs if not done_(j)]; print('to render', len(todo), flush=True)
with ThreadPoolExecutor(2) as ex: list(ex.map(lambda j: subprocess.run(j, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL), todo))
# ------------------------------------------------------------------ compose
def sheet(fname, title, rows, colw=420, note=None, lab_w=170, hl=None):
    ncol = max(len(r_[1]) for r_ in rows); Wd = lab_w + ncol * colw; nl = (note.count('\n') + 1) if note else 0; Hh = 64 + sum(colw + (30 if r_[2] else 8) for r_ in rows) + 20 * nl + 16
    Sh = Image.new('RGB', (Wd, Hh), 'white'); d = ImageDraw.Draw(Sh); d.text((14, 14), title, fill=(0, 0, 0), font=font(20, True)); y = 64
    for ri, (lab, ims, caps) in enumerate(rows):
        d.text((8, y + colw // 2 - 10), lab, fill=(0, 0, 0), font=font(15, True))
        for k_, im in enumerate(ims):
            Sh.paste(im.resize((colw, colw)), (lab_w + k_ * colw, y))
            if hl is not None and k_ == hl: d.rectangle([lab_w + k_ * colw + 2, y + 2, lab_w + (k_ + 1) * colw - 3, y + colw - 3], outline=(220, 30, 30), width=5)
            if caps and k_ < len(caps) and caps[k_]: d.text((lab_w + 6 + k_ * colw, y + colw + 4), caps[k_], fill=(30, 30, 30), font=font(13))
        y += colw + (30 if caps else 8)
    if note: d.multiline_text((14, y + 4), note, fill=(50, 50, 50), font=font(14), spacing=6)
    Sh.save(os.path.join(OUT, fname), quality=88)
SM = S['items']; cap = lambda c, k: '%s  T4 %d  min %.0f°  asp %.1f' % (LAB[k], SM['%s %s' % (k, c)]['T4'], SM['%s %s' % (k, c)]['min_angle'], SM['%s %s' % (k, c)]['aspect_max'])
sheet('HVE_01_central_source_full_body.jpg', 'Central accepted source HB2 + HF2 + HP-B (versioned HVC1-HB2HF2-HPB / HVF178-HB2HF2-HPB) — neutral clay, true scale; family human auricle (pre-ear)',
      [(c, [img('body_' + c, v) for v in ('bfront', 'bprof', 'btq', 'brear')], ['front', 'profile', '3/4', 'rear']) for c in HEADS], colw=460,
      note='\n'.join('%s: 69/69 D1-D6 | technical PASS | body material vs MF %d/31 | one-alpha blend best R2 %.2f (%s) | deterministic dV 0' % (i, V6['sources'][i]['technical']['validator'], V6['sources'][i]['body']['material_vs']['MF'][1],
                     V6['sources'][i]['body']['scalar_blend'][1]['best_r2'], V6['sources'][i]['body']['scalar_blend'][1]['best_pair']) for i in V6['sources']))
BF = '/tmp/claude-0/rt/hv/bf_sheet_r'; bimg = lambda t, v: Image.open('%s/%s_%s.png' % (BF, t, v)).convert('RGB') if os.path.exists('%s/%s_%s.png' % (BF, t, v)) else Image.new('RGB', (480, 480), (255, 200, 200))
sheet('HVE_02_pelvis_HPA_HPB_HPC.jpg', 'Pelvis HP-A | HP-B (SELECTED, red) | HP-C on HB2+HF2 — neutral clay, identical camera; HP-A / HP-C diagnostic variation references only',
      [('%s %s' % (c, v), [bimg('%s_%s' % (c, k), v) for k in ('HB2HF2', 'HP-B', 'HP-C')], ['HP-A human-family-dominant', 'HP-B mild mixed — SELECTED', 'HP-C stronger mixed'] if v == 'pelvis' else None) for c in HEADS for v in ('pelvis', 'pfront')],
      colw=420, hl=1, note='\n'.join('HP-B %s: pelvic vertical / crest vs MF %+.1f %% (vs FN %+.1f, AE %+.1f, VA %+.1f) | crest share vs MF %+.1f %% | AP depth vs MF %+.1f %% | leg share vs MF %+.2f %%' % (
          c, *[V6['sources'][i]['skeletal_proxy_t05']['pelvic_vertical_over_crest'][q] for q in ('vs_MF_pct', 'vs_FN_pct', 'vs_AE_pct', 'vs_VA_pct')], V6['sources'][i]['skeletal_proxy_t05']['crest_share']['vs_MF_pct'],
          V6['sources'][i]['skeletal_proxy_t05']['pelvic_depth_share']['vs_MF_pct'], V6['sources'][i]['skeletal_proxy_t05']['leg_share']['vs_MF_pct']) for c, i in zip(HEADS, V6['sources'])))
four = lambda c: ['MF'] + HE
def cmp4(fname, title, v, colw=440):
    sheet(fname, title, [(c, [img('%s_%s_g' % (c, k), v) for k in four(c)], [LAB[k] for k in four(c)]) for c in HEADS], colw=colw)
cmp4('HVE_03_front.jpg', 'Marchfolk vs HE1 / HE2 / HE3 — head front, neutral clay, identical camera per configuration', 'front')
cmp4('HVE_04_profile.jpg', 'Marchfolk vs HE1 / HE2 / HE3 — head profile, neutral clay', 'prof')
cmp4('HVE_05_three_quarter_front.jpg', 'Marchfolk vs HE1 / HE2 / HE3 — close 3/4 front, neutral clay', 'etq')
cmp4('HVE_06_three_quarter_rear.jpg', 'Marchfolk vs HE1 / HE2 / HE3 — close 3/4 rear, neutral clay', 'etqr')
cmp4('HVE_07_rear.jpg', 'Marchfolk vs HE1 / HE2 / HE3 — head rear, neutral clay', 'rear')
cmp4('HVE_08_close_neutral_ear.jpg', 'Close neutral ear (lateral), neutral clay, true scale — Marchfolk | HE1 | HE2 | HE3', 'elat', colw=480)
sheet('HVE_09_root_concha_closeup.jpg', 'ROOT / CONCHA one-auricle hard gate — root closeup, neutral clay (anterior attachment, concha floor, tragus): does each read as ONE auricle?',
      [(c, [img('%s_%s_g' % (c, k), 'root') for k in four(c)], [LAB['MF']] + ['%s  mound p90 %.2f / junction %.2f cm' % (LAB[k], SM['%s %s' % (k, c)]['root_concha']['anterior_cuff_mound_p90_cm'], SM['%s %s' % (k, c)]['root_concha']['junction_anterior_height_mean_cm']) for k in HE]) for c in HEADS], colw=480)
sheet('HVE_10_wireframe.jpg', 'Wireframe (front orange, back violet, rim yellow, cuff blue, transition green) — engineering topology v002 sheet + RI3 six-ring cuff connectivity (read-only)',
      [('%s %s' % (c, v), [img('%s_%s_w' % (c, k), v) for k in HE], [cap(c, k) for k in HE] if v == 'elat' else None) for c in HEADS for v in ('elat', 'etqr', 'root')], colw=440)
leg = '  '.join('%s' % k.replace('_', ' ') for k, _ in ANAT)
def legend_img(w=440):
    im = Image.new('RGB', (w, w), 'white'); d = ImageDraw.Draw(im)
    for i, (k, col) in enumerate(ANAT + [('upper extension (above taper start)', (0.80, 0.86, 0.95)), ('cuff / skin', tuple(GREY))]):
        y = 14 + i * 30; d.rectangle([14, y, 40, y + 20], fill=tuple(int(255 * x) for x in col)); d.text((50, y + 2), k.replace('_', ' '), fill=(0, 0, 0), font=font(15))
    return im
sheet('HVE_11_annotated_anatomy.jpg', 'Annotated whole-ear anatomy (dominant relief system per front vertex): helix, antihelix stem, superior / inferior crura, triangular fossa, cymba, cavum, crus of helix, tragus, antitragus, intertragic notch, lobe, upper extension',
      [(c, [img('%s_%s_an' % (c, k), 'elat') for k in HE] + [legend_img()], [LAB[k] for k in HE] + ['legend']) for c in HEADS], colw=440)
COL = {'front': '#d9774a', 'back': '#8f6fb8', 'rim': '#d8b23a', 'cuff': '#4f8fd0', 'transition': '#4caf50', 'v005': '#9a9a9a'}
def sections(fname, title):
    fig, axs = plt.subplots(4, 4, figsize=(19, 17), squeeze=False)
    for ci, (c, h) in enumerate(HEADS.items()):
        rd = D.frame(h, 'l'); O, n, b, u = rd['O'], rd['n'], rd['b'], rd['u']
        for li, (mode, L_) in enumerate((('h', 0.0), ('v', 1.2))):
            for ai, k in enumerate(four(c)):
                z = np.load(mf(c) if k == 'MF' else he(c, k)); V = z['V']; Q = z['Q']; part = z['part'] if 'part' in z.files else np.array(['v005'] * len(V)); dd = V - O; B = dd @ b; U = dd @ u; N = dd @ n
                near = (np.abs(B - 1) < 7) & (np.abs(U) < 7) & (N > -4) & (V[:, 0] > 0); Qs = Q[near[Q].all(1)]
                Es = np.unique(np.sort(np.concatenate([Qs[:, [0, 1]], Qs[:, [1, 2]], Qs[:, [2, 3]], Qs[:, [3, 0]]]), 1), axis=0); a_, b_ = Es[:, 0], Es[:, 1]
                X = U if mode == 'h' else B; Y = B if mode == 'h' else U; s = (X[a_] - L_) * (X[b_] - L_) < 0; t = (L_ - X[a_[s]]) / (X[b_[s]] - X[a_[s]])
                py = Y[a_[s]] + t * (Y[b_[s]] - Y[a_[s]]); pn = N[a_[s]] + t * (N[b_[s]] - N[a_[s]]); pp = np.where(part[a_[s]] != 'v005', part[a_[s]], part[b_[s]])
                ax = axs[ci * 2 + li, ai]
                for k2, col in COL.items(): m = pp == k2; ax.scatter(py[m], pn[m], s=3, c=col)
                ax.set_aspect('equal'); ax.set_xlim(-3.5, 5.5); ax.set_ylim(-2.0, 4.0); ax.grid(alpha=0.3); th = SM.get('%s %s' % (k, c), {}).get('measure', {}).get('thickness_median_cm')
                ax.set_title('%s %s  %s %+.1f cm%s' % (c, LAB[k], 'up' if mode == 'h' else 'posterior', L_, '  thick med %.2f' % th if th else ''), fontsize=9)
                ax.set_xlabel('posterior (cm)' if mode == 'h' else 'up (cm)'); ax.set_ylabel('lateral from root plane (cm)') if ai == 0 else None
    fig.suptitle(title); fig.tight_layout(rect=(0, 0, 1, 0.97)); fig.savefig(os.path.join(OUT, fname), dpi=72); plt.close(fig)
sections('HVE_12_sections_thickness.jpg', 'Sections through root / concha (horizontal at root centroid height; vertical 1.2 cm behind it), root frame, true scale — grey skin, blue cuff, orange front, violet back, yellow rim')
sheet('HVE_13_T4_aspect.jpg', 'T-4 (red: corner outside 45-135 deg) and aspect (blue 1 -> red 6, violet > 6) of the branch faces',
      [('%s %s' % (c, t), [img('%s_%s_%s' % (c, k, t), 'elat') for k in HE], [cap(c, k) for k in HE] if t == 't4' else None) for c in HEADS for t in ('t4', 'as')], colw=440)
sheet('HVE_14_density.jpg', 'Branch density: mean face edge / stature (blue 0.03 % -> red 0.25 % limit)',
      [(c, [img('%s_%s_dn' % (c, k), 'elat') for k in HE], ['%s  mean %.3f %%' % (LAB[k], SM['%s %s' % (k, c)]['density_pct']) for k in HE]) for c in HEADS], colw=440)
sheet('HVE_15_root_deviation.jpg', 'Root deviation: cuff height above the hidden-ear skull (blue 0 -> red 0.6 cm); HR1 skin-hugging root, no raised cuff perimeter',
      [('%s %s' % (c, v), [img('%s_%s_rd' % (c, k), v) for k in HE], ['%s  cuff mean %.2f / p95 %.2f cm' % (LAB[k], SM['%s %s' % (k, c)]['root_concha']['cuff_height_above_skin_mean_cm'], SM['%s %s' % (k, c)]['root_concha']['cuff_height_above_skin_p95_cm']) for k in HE] if v == 'elat' else None) for c in HEADS for v in ('elat', 'root')], colw=440)
MA = A['measured']['items']; FW = ['MF'] + HE + ['FN', 'AE', 'VA']
fcap = lambda k: LAB[k] if k not in MA else '%s | nearest %s | R2 %.2f' % (k, MA[k]['nearest_source'], MA[k]['scalar_fit']['best_r2'])
sheet('HVE_16_ear_only_firewall.jpg', 'EAR-ONLY FIREWALL — one common Halvren head (face / pigment neutral, no hair), identical camera, matched head scale: Marchfolk | HE1 | HE2 | HE3 | frozen Fenn | Aelari | Vael',
      [(v, [img('c1_%s_g' % k, v) for k in FW], [fcap(k) for k in FW] if v == 'elat' else None) for v in ('elat', 'etq', 'etqr')], colw=360,
      note='frozen elf ears are their frozen parameter sets realized on the common head (frozen meshes untouched); Marchfolk = the v005 family human auricle of the same head')
fig, axs = plt.subplots(1, 4, figsize=(22, 6.5))
for ai, k in enumerate(HE + ['design HE2']):
    ax = axs[ai]; src = A['design_parameters']['items']['HE2'] if k == 'design HE2' else MA[k]
    for j, (pr, col) in enumerate((('MF-FN', '#d9774a'), ('MF-AE', '#4f8fd0'), ('MF-VA', '#4caf50'))):
        t = src['midpoint'][pr]['t']; ax.scatter(list(t.values()), [list(t.keys()).index(q) + 0.18 * (j - 1) if False else (sorted(set(sum([list(src['midpoint'][x]['t'].keys()) for x in src['midpoint']], []))).index(q) + 0.2 * (j - 1)) for q in t], c=col, s=40, label='%s  n %d  R2 %.2f  alpha %.2f' % (pr, src['midpoint'][pr]['n'], src['midpoint'][pr]['r2'], src['midpoint'][pr]['alpha']))
    keys = sorted(set(sum([list(src['midpoint'][x]['t'].keys()) for x in src['midpoint']], []))); ax.set_yticks(range(len(keys))); ax.set_yticklabels(keys, fontsize=9)
    ax.axvspan(0.35, 0.65, color='#eeeeee'); ax.axvline(0, c='k', lw=0.8); ax.axvline(1, c='k', lw=0.8); ax.set_xlim(-1.5, 2.5); ax.set_xlabel('t = (HV - MF) / (elf - MF)   (0 Marchfolk, 1 elf; grey = midpoint band)')
    ax.set_title('%s  (%s)' % (k, 'measured ear domains' if k != 'design HE2' else 'authored parameters'), fontsize=11); ax.legend(fontsize=8, loc='lower right'); ax.grid(alpha=0.3)
fig.suptitle('ARITHMETIC-AVERAGE EAR FIREWALL — per-domain inheritance position vs each human / elf pair; fail if one alpha explains HE2 (R2 >= 0.8, n >= 6)'); fig.tight_layout(rect=(0, 0, 1, 0.94)); fig.savefig(os.path.join(OUT, 'HVE_17_arithmetic_average_ear_audit.jpg'), dpi=72); plt.close(fig)
for i, (k, s) in enumerate(DG.items()):
    nm = {'HV-DFN': 'Fenn-influenced', 'HV-DAE': 'Aelari-influenced', 'HV-DVA': 'Vael-influenced', 'HV-DHU': 'human-forward'}[k]; srcl = 'c1_%s_g' % s
    m = MA.get(k, {}); cc = ['HE2 (central)', '%s diagnostic  nearest %s  differs from %s in %s domains' % (nm, m.get('nearest_source'), s, m.get('distance', {}).get(s, {}).get('domains_gt_half_sd')), LAB[s]]
    sheet('HVE_%02d_%s_diagnostic.jpg' % (18 + i, nm.replace('-', '_').lower()), '%s DIAGNOSTIC (internal validation only, not a subrace): HE2 | %s | %s — neutral clay, identical camera' % (nm.upper(), k, LAB[s]),
          [(v, [img('c1_HE2_g', v), img('c1_%s_g' % k, v), img(srcl if s != 'MF' else 'c1_MF_g', v)], cc if v == 'elat' else None) for v in ('elat', 'etq', 'etqr')], colw=460)
sheet('HVE_22_body_face_ear_mosaic.jpg', 'BODY / FACE / EAR MOSAIC — HB2+HF2+HP-B with HE1 / HE2 / HE3; HB2+HF1 with HE3 (stronger ear, subtler face); HB2+HF3 with HE1 (subtler ear, stronger face)',
      [(v, [img('mos%d' % i, v) for i in range(len(MOS))], [l for l, _, _ in MOS] if v == 'tqf' else None) for v in ('tqf', 'front', 'etq')], colw=400)
sheet('HVE_23_deformation_readiness.jpg', 'Head / neck readiness, HE2 (flex / ext 30, yaw +/-45, pitch +/-20, roll +/-20): branch contacts / flips / root inversions per pose in captions',
      [(c, [img('epose_%s_%s' % (c, pn), 'tq') for pn in PN], ['%s %d/%d/%d' % (pn.replace('head_', ''), *[SM['HE2 %s' % c]['poses'][pn][q] for q in ('contacts', 'flips', 'root_inv')]) for pn in PN]) for c in HEADS], colw=300)
pr = sorted(PRB['probes']); half = (len(pr) + 1) // 2
sheet('HVE_24_shape_probes.jpg', 'HE2 geometry probes (same topology; c1): length, projection, sweep, vertical angle, base width, tip sharpness, lobe — own-domain response in SD units; technical state',
      [(('probes %d' % r_), [img('pr_' + pn, 'etq') for pn in pr[r_ * half:(r_ + 1) * half]], ['%s  own %+.1f SD  %s' % (pn, PRB['probes'][pn]['own_response_sd'], 'OK' if PRB['probes'][pn]['technical']['pass'] else 'TECH FAIL') for pn in pr[r_ * half:(r_ + 1) * half]]) for r_ in range(2)], colw=300)
reg = S.get('regression', {})
sheet('HVE_25_hidden_ear_body_face_regression.jpg', 'Body / face / pelvis regression after ear insertion: outside the ear branch every vertex is byte-identical to the HB2+HF2+HP-B family realization (HE1 / HE2 / HE3, c1 / c2)',
      [(c, [img('%s_MF_g' % c, 'front'), img('%s_HE2_g' % c, 'front'), img('%s_HE2_g' % c, 'prof')], ['family source (hidden-ear eval basis)', 'HE2 inserted', 'HE2 profile']) for c in HEADS], colw=420,
      note='\n'.join('%s: outside-branch identical %s | hidden-ear eval (ears excluded) = HP-B source eval: body material vs MF %d/31, face departing %d/7, one-alpha best R2 %.2f, 69/69' % (
          k, reg.get(k), V6['sources'][HEADS[k.split()[-1]]]['body']['material_vs']['MF'][1], V6['sources'][HEADS[k.split()[-1]]]['face']['regions_departing_MF'][1], V6['sources'][HEADS[k.split()[-1]]]['body']['scalar_blend'][1]['best_r2']) for k in sorted(reg)))
print('SHEETS_DONE', len(os.listdir(OUT)))
