# va_ri_sheets.py RI_WORK EVIDIR OUTDIR : Vael VA-E2 root-integration order §13 visual package (VA_RI_01..19). Identical orthographic cameras per
# configuration (the current VA-E2 head / ear frames), true scale; neutral clay (no annotation) wherever the read is judged. Workbench renders
# (grask_rigprep_v001/render_attr.py) composed with PIL; resumable; 2 Blender processes.
import sys, os, json, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
from concurrent.futures import ThreadPoolExecutor
os.environ.setdefault('EAR_TOPO', 'v002')
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001')
import ear_branch_lib as E
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
W, EV, OUT = sys.argv[1:4]; os.makedirs(OUT, exist_ok=True); TMP = os.environ.get('VA_SHEET_TMP', '/tmp/claude-0/rt/va/ri_sheet_r'); os.makedirs(TMP, exist_ok=True)
BP = '/home/claude/stc/bin/python3'; REND = '/home/claude/wayfarer-design/tools/rac/rp/grask_rigprep_v001/render_attr.py'; CUR = '/tmp/claude-0/rt/va/ear'
GREY = np.array([0.80, 0.78, 0.76]); jl = lambda p: json.load(open(p)); S = jl(EV + '/VAEL_EAR_root_integration_summary.json'); SEL = os.environ.get('VA_RI_SEL', 'RI3')
HEADS = {'c1': 'VAL4-R1-VD2-VF2', 'c2': 'VALF178-R1-VD2-VF2'}; ALTS = ['current', 'RI1', 'RI2', 'RI3']
ALT = {'current': (CUR, 'VA-E2'), 'RI1': (W + '/RI1', 'VA-E2-RI1'), 'RI2': (W + '/RI2', 'VA-E2-RI2'), 'RI3': (W + '/RI3', 'VA-E2-RI3')}
LAB = {'current': 'current VA-E2', 'RI1': 'RI1 reduced stand-off', 'RI2': 'RI2 skin-blended cuff', 'RI3': 'RI3 local Vael cuff'}
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
def hcam(V):
    hv = V[V[:, 2] > V[:, 2].max() - 25]; return np.array([0.0, hv[:, 1].mean(), V[:, 2].max() - 12.0])
Lo = E.canonical_layout(); st = Lo['st']; ns = len(st); J = np.asarray(Lo['J'])
P = {(a, c): '%s/build/%s_%s_branch.npz' % (ALT[a][0], h, ALT[a][1]) for a in ALTS for c, h in HEADS.items()}
CAM = {}
for c, h in HEADS.items():
    z = np.load(P[('current', c)]); r = jl(P[('current', c)].replace('.npz', '.json')); V = z['V']; fr = r['sides']['l']['frame']; O, n, b, u = [np.array(fr[k]) for k in ('O', 'n', 'b', 'u')]
    X = V[np.nonzero(z['side'] == 'l')[0][0]:][:ns]; bu = np.c_[(X - O) @ b, (X - O) @ u]; inJ = (Lo['part'][:ns] == 'front') & (E._inside_dist(bu[J], bu) > 0)
    Cc = X[inJ].mean(0); Tg = X[J[Lo['part'][J] == 'front']].mean(0) - 0.4 * u
    CAM[c] = dict(H=hcam(V), Ce=V[z['side'] == 'l'].mean(0), O=O, Cc=Cc, Tg=Tg, n=n, b=b, u=u)
def views(c, names):
    k = CAM[c]; nb = lambda w: tuple(np.round(w, 4))
    T = dict(front=((0, 1, 0.03), k['H'], 15), prof=((1, 0, 0), k['H'], 15), tqf=((1, 1, 0.1), k['H'], 15), rear=((0, -1, 0), k['H'], 15),
             eface=((1, 0.9, 0.15), k['Ce'], 4.8), elat=((1, 0.15, 0.05), k['Ce'], 5.2), etq=((1, 0.45, 0.25), k['Ce'], 4.8), etqr=((0.6, -1, 0.15), k['Ce'], 4.8),
             root=((1, 0.2, 0.0), k['O'], 3.4), concha=(nb(k['n'] + 0.35 * k['b'] * 0 + 0.25 * np.array([0, 1, 0])), k['Cc'], 2.4),
             tragus=(nb(k['n'] + np.array([0, 0.9, -0.25])), k['Tg'], 2.0))
    return [(n,) + T[n] for n in names]
for a in ALTS:
    for c in HEADS:
        z = np.load(P[(a, c)]); t = '%s_%s' % (c, a)
        render(t + '_g', P[(a, c)], np.tile(GREY, (len(z['V']), 1)), views(c, ['front', 'prof', 'tqf', 'rear', 'eface', 'elat', 'etq', 'etqr', 'root', 'concha', 'tragus']))
        render(t + '_k', P[(a, c)], np.zeros((len(z['V']), 3)), views(c, ['prof', 'front', 'tqf']))                    # silhouette (flat black)
        render(t + '_w', P[(a, c)], part_cols(z), views(c, ['eface', 'etqr', 'root']), wire=True)
        d, k_ = ALT[a]; pf = '%s/audit/%s_%s_audit_perface.npz' % (d, HEADS[c], k_)
        if os.path.exists(pf):
            q = np.load(pf); F_, bad, asp = q['faces'], q['ang_bad'], q['asp']; C = face_part(z) * 0.45 + 0.5; C[F_] = [0.93, 0.93, 0.93]; C[F_[bad]] = [0.92, 0.18, 0.12]
            render(t + '_t4', P[(a, c)], C, views(c, ['eface', 'root']), wire=True)
            C = np.tile(GREY, (len(z['Q']), 1)); C[F_] = heat(asp, 1.0, 6.0); C[F_[asp > 6]] = [0.55, 0.1, 0.65]; render(t + '_as', P[(a, c)], C, views(c, ['eface']), wire=True)
        rec = jl(P[(a, c)].replace('.npz', '.json')); C = np.tile(GREY, (len(z['V']), 1))                                # lateral stand-off heat (root frame)
        for sd in ('l', 'r'):
            fr = rec['sides'][sd]['frame']; O, n = np.array(fr['O']), np.array(fr['n']); m = (z['side'] == sd) & np.isin(z['part'], ['front', 'back', 'rim']); C[m] = heat((z['V'][m] - O) @ n, 0, 3.2)
        render(t + '_lat', P[(a, c)], C, views(c, ['front', 'etqr']))
FZ = {'FN_c1': '/tmp/claude-0/rt/fn/final/ear/build/FNL4-CF2_E2_branch.npz', 'FN_c2': '/tmp/claude-0/rt/fn/final/ear/build/FNF181-CF2_E2_branch.npz',
      'AE_c1': '/tmp/claude-0/rt/ae/final/ear/build/AEL1-R1_AE-E2_branch.npz', 'AE_c2': '/tmp/claude-0/rt/ae/final/ear/build/AELF190-R1_AE-E2_branch.npz'}
for tag, p in list(FZ.items()) + [('VA_c1', P[(SEL, 'c1')]), ('VA_c2', P[(SEL, 'c2')])]:
    z = np.load(p); V = z['V']; Hc = hcam(V); Ce = V[z['side'] == 'l'].mean(0); rec = jl(p.replace('.npz', '.json')); C = np.tile(GREY, (len(V), 1))
    for sd in ('l', 'r'):
        fr = rec['sides'][sd]['frame']; O, n = np.array(fr['O']), np.array(fr['n']); m = (z['side'] == sd) & np.isin(z['part'], ['front', 'back', 'rim']); C[m] = heat((V[m] - O) @ n, 0, 3.2)
    render('cmp_' + tag, p, np.tile(GREY, (len(V), 1)), [('prof', (1, 0, 0), Hc, 15), ('front', (0, 1, 0.03), Hc, 15), ('rear', (0, -1, 0), Hc, 15), ('elat', (1, 0.15, 0.05), Ce, 5.6), ('etq', (1, 0.45, 0.25), Ce, 5.0)])
    render('cmpl_' + tag, p, C, [('front', (0, 1, 0.03), Hc, 15)])
PN = ('neck_flex30', 'neck_ext30', 'head_yaw_l45', 'head_yaw_r45', 'head_pitch_down20', 'head_pitch_up20', 'head_roll_l20', 'head_roll_r20')
for c, h in HEADS.items():
    d, k_ = ALT[SEL]; z = np.load(P[(SEL, c)])
    for pn in PN:
        X = np.load('%s/deform/%s_%s_%s.npy' % (d, h, k_, pn)); q = os.path.join(TMP, 'epose_%s_%s.npz' % (c, pn)); np.savez_compressed(q, V=X, Q=z['Q'])
        render('epose_%s_%s' % (c, pn), q, part_cols(z), [('tq', (1, 0.3, 0.1), X[z['side'] == 'l'].mean(0), 7.0)], px=420)
PR = ['proj_m10', 'proj_p10', 'tilt_m8', 'tilt_p8', 'sweep_m06', 'sweep_p06', 'len_m10', 'len_p10', 'tip_blunt', 'tip_sharp', 'wb_m8', 'wb_p8']
for pn in PR:
    d, k_ = ALT[SEL]; p = '%s/probe/%s/%s_%s_branch.npz' % (d, pn, HEADS['c1'], k_)
    if os.path.exists(p): z = np.load(p); render('pr_' + pn, p, np.tile(GREY, (len(z['V']), 1)), views('c1', ['etq']), px=420); render('prw_' + pn, p, part_cols(z), views('c1', ['eface']), wire=True, px=420)
print('render jobs', len(jobs), flush=True)
done_ = lambda j: all(os.path.exists(os.path.join(TMP, '%s_%s.png' % (j[6], v_.split(':')[0]))) for v_ in j[7].split(';'))
todo = [j for j in jobs if not done_(j)]; print('to render', len(todo), flush=True)
with ThreadPoolExecutor(int(os.environ.get('VA_SHEET_THREADS', '2'))) as ex: list(ex.map(lambda j: subprocess.run(j, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL), todo))
# ---------------------------------------------------------------- compose
def sheet(fname, title, rows, colw=600, note=None, lab_w=150, caps_font=14):
    ncol = max(len(r_[1]) for r_ in rows); Wd = lab_w + ncol * colw; Hh = 64 + sum(colw + (30 if r_[2] else 8) for r_ in rows) + (40 if note else 0)
    Sh = Image.new('RGB', (Wd, Hh), 'white'); d = ImageDraw.Draw(Sh); d.text((14, 14), title, fill=(0, 0, 0), font=font(20, True)); y = 64
    for lab, ims, caps in rows:
        d.text((10, y + colw // 2), lab, fill=(0, 0, 0), font=font(16, True))
        for k_, im in enumerate(ims):
            Sh.paste(im.resize((colw, colw)), (lab_w + k_ * colw, y))
            if caps and k_ < len(caps) and caps[k_]: d.text((lab_w + 6 + k_ * colw, y + colw + 4), caps[k_], fill=(30, 30, 30), font=font(caps_font))
        y += colw + (30 if caps else 8)
    if note: d.text((14, y + 4), note, fill=(60, 60, 60), font=font(15))
    Sh.save(os.path.join(OUT, fname), quality=88)
AL = S['alternatives']; cap4 = [LAB[a] for a in ALTS]
def four(fname, title, suf, view, caps=True, colw=560):
    sheet(fname, title, [(c, [img('%s_%s_%s' % (c, a, suf), view) for a in ALTS], cap4 if caps else None) for c in HEADS], colw=colw)
four('VA_RI_01_three_quarter_front.jpg', 'VA-E2 root integration — close 3/4 front, neutral clay: current | RI1 | RI2 | RI3 (same camera per configuration)', 'g', 'etq')
four('VA_RI_02_close_profile.jpg', 'VA-E2 root integration — close profile, neutral clay', 'g', 'elat')
four('VA_RI_03_close_three_quarter_rear.jpg', 'VA-E2 root integration — close 3/4 rear, neutral clay', 'g', 'etqr')
four('VA_RI_04_front.jpg', 'VA-E2 root integration — head front, neutral clay', 'g', 'front')
four('VA_RI_05_rear.jpg', 'VA-E2 root integration — head rear, neutral clay', 'g', 'rear')
four('VA_RI_06_root_closeup.jpg', 'VA-E2 root integration — root closeup (lateral, low), neutral clay', 'g', 'root')
four('VA_RI_07_concha_closeup.jpg', 'VA-E2 root integration — concha closeup (looking into the concha), neutral clay', 'g', 'concha')
four('VA_RI_08_tragus_antitragus_closeup.jpg', 'VA-E2 root integration — tragus / antitragus closeup (front-lateral, from below), neutral clay', 'g', 'tragus')
sheet('VA_RI_09_wireframe.jpg', 'VA-E2 root integration — wireframe (front orange, back violet, rim yellow, cuff blue, transition green)',
      [('%s %s' % (c, v), [img('%s_%s_w' % (c, a), v) for a in ALTS], ['%s  V %d  cuff T-4 %d' % (LAB[a], AL['%s %s' % (a, c)]['verts'], AL['%s %s' % (a, c)]['T4_by_part']['cuff']) for a in ALTS] if v == 'eface' else None)
       for c in HEADS for v in ('eface', 'root')], colw=520)
COL = {'front': '#d9774a', 'back': '#8f6fb8', 'rim': '#d8b23a', 'cuff': '#4f8fd0', 'transition': '#4caf50', 'v005': '#9a9a9a'}
def sections(fname, title, mode):
    fig, axs = plt.subplots(len(HEADS) * 2, 4, figsize=(19, 4.4 * len(HEADS) * 2), squeeze=False)
    for ci, (c, h) in enumerate(HEADS.items()):
        k = CAM[c]; O, n, b, u = k['O'], k['n'], k['b'], k['u']; cc = k['Cc'] - O; lv = [cc @ u, cc @ u + 1.2] if mode == 'h' else [cc @ b, cc @ b + 1.0]
        for li, L_ in enumerate(lv):
            for ai, a in enumerate(ALTS):
                z = np.load(P[(a, c)]); V = z['V']; Q = z['Q']; part = z['part']; dd = V - O; B = dd @ b; U = dd @ u; N = dd @ n
                near = (np.abs(B) < 6) & (np.abs(U) < 6) & (N > -4) & (V[:, 0] > 0); Qs = Q[near[Q].all(1)]
                Es = np.unique(np.sort(np.concatenate([Qs[:, [0, 1]], Qs[:, [1, 2]], Qs[:, [2, 3]], Qs[:, [3, 0]]]), 1), axis=0); A_, B_ = Es[:, 0], Es[:, 1]
                X = U if mode == 'h' else B; Y = B if mode == 'h' else U; s = (X[A_] - L_) * (X[B_] - L_) < 0; t = (L_ - X[A_[s]]) / (X[B_[s]] - X[A_[s]])
                py = Y[A_[s]] + t * (Y[B_[s]] - Y[A_[s]]); pn = N[A_[s]] + t * (N[B_[s]] - N[A_[s]]); pp = np.where(part[A_[s]] != 'v005', part[A_[s]], part[B_[s]])
                ax = axs[ci * 2 + li, ai]
                for k2, col in COL.items(): m = pp == k2; ax.scatter(py[m], pn[m], s=3, c=col)
                ax.set_aspect('equal'); ax.set_xlim(-3.5, 4.0); ax.set_ylim(-1.5, 3.5); ax.grid(alpha=0.3)
                ax.set_title('%s %s  %s %+.1f cm' % (c, LAB[a], 'up' if mode == 'h' else 'posterior', L_), fontsize=10)
                if ai == 0: ax.set_ylabel('lateral from root plane (cm)')
                ax.set_xlabel('posterior (cm)' if mode == 'h' else 'up (cm)')
    fig.suptitle(title); fig.tight_layout(rect=(0, 0, 1, 0.97)); fig.savefig(os.path.join(OUT, fname), dpi=80); plt.close(fig)
sections('VA_RI_10_section_root_concha.jpg', 'Horizontal sections through root / concha (root frame, true scale; orange front, violet back, yellow rim, blue cuff, green transition, grey skin)', 'h')
sections('VA_RI_11_section_helix_concha.jpg', 'Vertical sections through helix / concha (constant posterior offset; root frame, true scale)', 'v')
sheet('VA_RI_12_silhouette.jpg', 'VA-E2 root integration — silhouette only (profile / front / 3-4): the outer silhouette is unchanged',
      [('%s %s' % (c, v), [img('%s_%s_k' % (c, a), v) for a in ALTS], cap4 if v == 'prof' else None) for c in HEADS for v in ('prof', 'front')], colw=480)
sheet('VA_RI_13_neutral_clay.jpg', 'Neutral clay — selected %s, no annotation' % SEL,
      [(c, [img('%s_%s_g' % (c, SEL), v) for v in ('tqf', 'etq', 'elat', 'etqr')], None) for c in HEADS], colw=560)
def blend(a, b):
    A = np.asarray(a, float) * np.array([1.0, 0.55, 0.55]); B_ = np.asarray(b, float) * np.array([0.55, 0.65, 1.0]); return Image.fromarray(np.clip(0.5 * A + 0.5 * B_, 0, 255).astype(np.uint8))
sheet('VA_RI_14_current_vs_revised_overlay.jpg', 'Current VA-E2 (red) over revised %s (blue), same camera: the cuff mound and the raised root perimeter disappear; the outer leaf coincides' % SEL,
      [(c, [blend(img('%s_current_g' % c, v), img('%s_%s_g' % (c, SEL), v)) for v in ('etq', 'elat', 'front', 'etqr')], ['3/4 close', 'profile close', 'head front', '3/4 rear close']) for c in HEADS], colw=520)
PJ = S['projection']
def fwcap(nm, c):
    m = PJ[c][nm]; return '%s  angle %.0f°  mean %.3f  tip %.3f HH' % (nm.replace('Vael ', 'Vael '), m['body_angle_deg'], m['free_standoff_mean_over_HH'], m['tip_standoff_over_HH'])
rows = []
for c in HEADS:
    for v in ('prof', 'front', 'rear', 'etq'):
        rows.append(('%s %s' % (c, v), [img('cmp_FN_' + c, v), img('cmp_VA_' + c, v), img('cmp_AE_' + c, v)], [fwcap(nm, c) for nm in ('Fenn E2', 'Vael %s' % SEL, 'Aelari AE-E2')] if v == 'prof' else None))
sheet('VA_RI_15_three_elf_ears.jpg', 'Frozen Fenn E2 | revised Vael VA-E2 %s | frozen Aelari AE-E2 — each on its own head, same relative camera' % SEL, rows, colw=470)
dcap = lambda c, p: '%s %s' % (p, '/'.join(str(x) for x in AL['%s %s' % (SEL, c)]['deform'][p]))
sheet('VA_RI_16_deformation_readiness.jpg', 'Revised VA-E2 %s — static head / neck readiness (new branch contacts / flips / root inversions; 0/0/0 = pass)' % SEL,
      [('%s %d' % (c, i), [img('epose_%s_%s' % (c, p), 'tq') for p in PN[4 * i:4 * i + 4]], [dcap(c, p) for p in PN[4 * i:4 * i + 4]]) for c in HEADS for i in (0, 1)], colw=420)
t4cap = lambda a, c: '%s T-4 %d asp %.2f min %.1f°' % (LAB[a], AL['%s %s' % (a, c)]['T4'], AL['%s %s' % (a, c)]['aspect_max'], AL['%s %s' % (a, c)]['min_angle'])
sheet('VA_RI_17_T4_aspect.jpg', 'T-4 (red = corner outside 45-135°) and aspect (blue 1 .. red 6; violet > 6)',
      [('%s %s' % (c, lab), [img('%s_%s_%s' % (c, a, tg), v) for a in ALTS], [t4cap(a, c) for a in ALTS] if lab == 'T-4' else None) for c in HEADS for lab, tg, v in (('T-4', 't4', 'eface'), ('T-4 root', 't4', 'root'), ('aspect', 'as', 'eface'))], colw=500)
fig, axs = plt.subplots(2, 4, figsize=(20, 8.5))
order = ['Fenn E2', 'Vael current', 'Vael RI1', 'Vael RI2', 'Vael RI3', 'Aelari AE-E2']; colr = ['#79b', '#c98', '#c76', '#c54', '#a32', '#9b7']
for ci, c in enumerate(HEADS):
    for mi, (key, ttl) in enumerate((('body_angle_deg', 'auricle-body angle (deg)'), ('free_standoff_mean_over_HH', 'mean free-ear stand-off / HH'), ('free_standoff_median_over_HH', 'median free-ear stand-off / HH'), ('tip_standoff_over_HH', 'tip stand-off / HH'))):
        ax = axs[ci, mi]; vals = [PJ[c][o][key] for o in order]; ax.bar(range(6), vals, color=colr); ax.set_xticks(range(6)); ax.set_xticklabels([o.replace('Vael ', 'V ').replace(' E2', '').replace(' AE-E2', '') for o in order], fontsize=9)
        ax.set_title('%s %s' % (c, ttl), fontsize=10); ax.set_ylim(min(vals) * 0.85 if key != 'body_angle_deg' else 0, max(vals) * 1.08)
fig.suptitle('Projection / stand-off: frozen Fenn E2, Vael VA-E2 current / RI1 / RI2 / RI3, frozen Aelari AE-E2 (free ear = sheet outside the junction ring, root frame)'); fig.tight_layout(rect=(0, 0, 1, 0.95))
fig.savefig(os.path.join(TMP, 'proj_chart.png'), dpi=90); plt.close(fig)
ch = Image.open(os.path.join(TMP, 'proj_chart.png')).convert('RGB')
lat = Image.new('RGB', (3 * 520 * 2, 520), 'white')
for i, t in enumerate(('cmpl_FN_c1', 'cmpl_VA_c1', 'cmpl_AE_c1', 'cmpl_FN_c2', 'cmpl_VA_c2', 'cmpl_AE_c2')): lat.paste(img(t, 'front').resize((520, 520)), (520 * i, 0))
Sh = Image.new('RGB', (max(ch.width, lat.width), ch.height + lat.height + 40), 'white'); Sh.paste(ch, (0, 0)); Sh.paste(lat, (0, ch.height + 40))
ImageDraw.Draw(Sh).text((14, ch.height + 8), 'Lateral stand-off of the auricle from the root plane (blue 0 .. red 3.2 cm), head front: c1 Fenn | Vael %s | Aelari, c2 Fenn | Vael %s | Aelari' % (SEL, SEL), fill=(0, 0, 0), font=font(16, True))
Sh.save(os.path.join(OUT, 'VA_RI_18_projection_standoff.jpg'), quality=88)
PB = S['probes']; pcap = lambda p: '%s T-4 %d SI %d %s' % (p, PB[p]['T4'], PB[p]['self_intersection_branch'], 'ok' if PB[p]['moves_intended'] else 'WRONG')
prs = [p for p in PR if p in PB]
sheet('VA_RI_19_shape_probe_regression.jpg', 'Revised VA-E2 %s — shape probes (c1): neutral clay 3/4 close (root / concha stay one structure) and wire' % SEL,
      [('clay %d-%d' % (i + 1, i + 6), [img('pr_' + p, 'etq') for p in prs[i:i + 6]], [pcap(p) for p in prs[i:i + 6]]) for i in (0, 6)] +
      [('wire %d-%d' % (i + 1, i + 6), [img('prw_' + p, 'eface') for p in prs[i:i + 6]], None) for i in (0, 6)], colw=400)
print('sheets done', flush=True)
