# hv_ear_family_boards.py EVIDIR OUTDIR : Halvren ear family closure order §9 boards (identical cameras = left root frame of the common HB2+HF2+HP-B head per
# configuration, matched scale, neutral clay; B with volume-revealing cavity shading):
#   A  HE3 firewall board (c1 common head): Marchfolk | HE1 | HE2 frozen | HE3 before | HE3 corrected | frozen Fenn | Aelari | Vael -- front 3/4, side, true rear 3/4
#   B  HE3 HR2 root gate, corrected HE3 c1 / c2: strict side | true rear 3/4 | direct rear | lower-rear 3/4 (+ Board-E 3/4); frozen HE2 rows for reference
#   C  HE3 body context HB2 + HF2 + HP-B: front | front 3/4 | rear 3/4 (c1 / c2)
#   D  HE1 size-floor board (c1): Marchfolk | HE1 HVEAR3 L 6.3 (old floor) | HE2 frozen | HE1 L 5.3 (edge test) | HE1 L 5.6 (recommended) -- front, side,
#      front 3/4, rear 3/4
#   E  family lineup HE1 | frozen HE2 | corrected HE3: front 3/4 and side, c1 and c2 (+ full-head front)
#   F  HE3 firewall decomposition chart before / after
import sys, os, json, subprocess, numpy as np
from PIL import Image, ImageDraw
from concurrent.futures import ThreadPoolExecutor
os.environ.setdefault('EAR_TOPO', 'v002')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import hv_ear_quick as QK; import hv_ear_domains as D
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
EV, OUT = sys.argv[1:3]; os.makedirs(OUT, exist_ok=True); TMP = '/tmp/claude-0/rt/hv/ear/board_fam'; os.makedirs(TMP, exist_ok=True); QK.TMP = TMP
E = '/tmp/claude-0/rt/hv/ear'; jl = lambda p: json.load(open(p)); H = {'c1': 'HVC1-HB2HF2-HPB', 'c2': 'HVF178-HB2HF2-HPB'}
R = jl(EV + '/HV_ear_family_closure_record.json'); font = QK.font
def extra(h):
    rd = D.frame(h, 'l'); O, n, b, u = rd['O'], rd['n'], rd['b'], rd['u']; z3 = np.array([0, 0, 1.0]); C = O - 2.5 * u + 0.3 * b; nb = lambda w: tuple(np.round(np.asarray(w, float), 4))
    return dict(zf=(nb(0.7 * n - b - 0.3 * z3), C, 2.4), tqr=((1, -1, 0.1), None, 15))
_oc = QK.cams; QK.cams = lambda h: {**_oc(h), **extra(h)}
bp = lambda w, c, k: '%s/%s/build/%s_%s_branch.npz' % (E, w, H[c], k)
IT = {'MF': ('%s/../hpe/fam/%s_fam.npz' % (E, H['c1']), 'c1'), 'MF c2': ('%s/../hpe/fam/%s_fam.npz' % (E, H['c2']), 'c2'),
      'HE1': (bp('fam6', 'c1', 'HE1'), 'c1'), 'HE2': (bp('fam6', 'c1', 'HE2'), 'c1'), 'HE3': (bp('fam6', 'c1', 'HE3'), 'c1'),
      'HE1 c2': (bp('fam6', 'c2', 'HE1'), 'c2'), 'HE2 c2': (bp('fam6', 'c2', 'HE2'), 'c2'), 'HE3 c2': (bp('fam6', 'c2', 'HE3'), 'c2'),
      'HE3 before': (bp('hr2f', 'c1', 'HE3'), 'c1'), 'HE1 L6.3': (bp('hr2f', 'c1', 'HE1'), 'c1'), 'HE1 L5.3': (bp('he1L53', 'c1', 'HE1'), 'c1'), 'HE1 L5.6s': (bp('he1L56', 'c1', 'HE1'), 'c1'),
      'FN': (bp('ref/FN', 'c1', 'E2'), 'c1'), 'AE': (bp('ref/FN', 'c1', 'AE-E2'), 'c1'), 'VA': (bp('ref/RI3', 'c1', 'VA-E2-RI3'), 'c1')}
tag = lambda k: k.replace(' ', '_').replace('.', '')
VG = ['etq', 'elat', 'rq', 'front', 'tqf', 'tqr', 'aq']
jobs = [(QK.run(tag(k) + '_g', p, H[c], VG, 600), os.environ) for k, (p, c) in IT.items()]
REV = dict(os.environ, RENDER_REVEAL='1')
for k in ('HE3', 'HE3 c2', 'HE3 before', 'HE2', 'HE2 c2'): p, c = IT[k]; jobs.append((QK.run(tag(k) + '_rv', p, H[c], ['side', 'aq', 'rq', 'rr', 'lr', 'zf'], 600), REV))
with ThreadPoolExecutor(2) as ex: list(ex.map(lambda j: subprocess.run(j[0], env=j[1], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL), jobs))
def img(t, v):
    p = os.path.join(TMP, '%s_%s.png' % (t, v)); return Image.open(p).convert('RGB') if os.path.exists(p) else Image.new('RGB', (600, 600), (255, 200, 200))
def sheet(fn, title, rows, colw=360, note=None, lab_w=150, heads=None):
    ncol = max(len(r[1]) for r in rows); nl = note.count('\n') + 1 if note else 0; hh = 26 if heads else 0
    Sh = Image.new('RGB', (lab_w + ncol * colw, 60 + hh + sum(colw + (28 if r[2] else 8) for r in rows) + 21 * nl + 14), 'white'); d = ImageDraw.Draw(Sh)
    d.text((14, 14), title, fill=(0, 0, 0), font=font(19, True)); y = 56
    if heads:
        for i, t in enumerate(heads): d.text((lab_w + 6 + i * colw, y), t, fill=(0, 0, 0), font=font(14, True))
        y += hh
    for lab, ims, caps in rows:
        d.multiline_text((8, y + colw // 2 - 18), lab, fill=(0, 0, 0), font=font(15, True), spacing=4)
        for i, im in enumerate(ims):
            Sh.paste(im.resize((colw, colw)), (lab_w + i * colw, y))
            if caps and caps[i]: d.text((lab_w + 6 + i * colw, y + colw + 4), caps[i], fill=(30, 30, 30), font=font(12))
        y += colw + (28 if caps else 8)
    if note: d.multiline_text((14, y + 4), note, fill=(50, 50, 50), font=font(14), spacing=6)
    Sh.save(os.path.join(OUT, fn), quality=90)
FW = R['firewall']; CO = R['family']['composite_elfward']
fwc = lambda k: 'best R2 %.2f (%s)' % (FW[k]['best_r2'], FW[k]['best_pair']) if k in FW else ''
L8 = [('MF', 'Marchfolk', None), ('HE1', 'HE1', 'HE1'), ('HE2', 'HE2 frozen', 'HE2'), ('HE3 before', 'HE3 before', 'HE3-before'), ('HE3', 'HE3 corrected', 'HE3'),
      ('FN', 'frozen Fenn', None), ('AE', 'frozen Aelari', None), ('VA', 'frozen Vael', None)]
sheet('HVF_A_HE3_firewall.jpg', 'A. HE3 firewall board -- common Halvren head (c1), identical camera, matched scale',
      [(v, [img(tag(k) + '_g', vv) for k, _, _ in L8], ['%s | %s' % (lb, fwc(fk)) if fk else lb for k, lb, fk in L8] if v == 'side' else None) for v, vv in (('front 3/4', 'etq'), ('side', 'elat'), ('true rear 3/4', 'rq'))],
      colw=300, heads=[lb for _, lb, _ in L8], note='HE3 before = HVEAR3 HE3 on HR2 (R2 0.88 MF<->Fenn); HE3 corrected = HVEAR4 (R2 %.2f / %.2f / %.2f MF<->Fenn / Aelari / Vael); composite elfward HE1 %.2f < HE2 %.2f < HE3 %.2f.'
      % (FW['HE3']['pairs']['MF-FN']['r2'], FW['HE3']['pairs']['MF-AE']['r2'], FW['HE3']['pairs']['MF-VA']['r2'], CO['HE1'], CO['HE2'], CO['HE3']))
SI = R['silhouette']; sc = lambda k: 'pedestal p90 post %.2f / inf %.2f cm | loop crease %.0f / %.0f deg' % tuple([SI[k]['pedestal_vs_true_head'][s]['p90_cm'] for s in ('posterior', 'inferior')] + [SI[k]['loop_crease_deg'][s]['mean'] for s in ('posterior', 'inferior')])
TE = R['technical']; tc = lambda k: 'min %.1f deg | aspect %.2f | selfx %d | 8 poses %s | guard %d' % (TE[k]['min_angle'], TE[k]['aspect_max'], TE[k]['branch_selfx'], 'clean' if TE[k]['poses_clean'] else 'FAIL', TE[k]['guard_iterations'])
sheet('HVF_B_HE3_HR2_root_gate.jpg', 'B. HE3 corrected -- HR2 root gate, c1 / c2 (+ frozen HE2 under the same shading for reference), revealing cavity shading: strict side | true rear 3/4 | direct rear | lower-rear 3/4 | Board-E 3/4 | lower root ant.',
      [('HE3\nc1', [img('HE3_rv', v) for v in ('side', 'rq', 'rr', 'lr', 'aq', 'zf')], [sc('HE3 c1'), None, tc('HE3 c1'), None, None, None]),
       ('HE3\nc2', [img('HE3_c2_rv', v) for v in ('side', 'rq', 'rr', 'lr', 'aq', 'zf')], [sc('HE3 c2'), None, tc('HE3 c2'), None, None, None]),
       ('HE2\nfrozen\nc1 (ref)', [img('HE2_rv', v) for v in ('side', 'rq', 'rr', 'lr', 'aq', 'zf')], [sc('HE2 c1') if 'HE2 c1' in SI else None, None, tc('HE2 c1'), None, None, None]),
       ('HE2\nfrozen\nc2 (ref)', [img('HE2_c2_rv', v) for v in ('side', 'rq', 'rr', 'lr', 'aq', 'zf')], [sc('HE2 c2') if 'HE2 c2' in SI else None, None, tc('HE2 c2'), None, None, None])], colw=360,
      heads=['strict side', 'true rear 3/4', 'direct rear', 'lower-rear 3/4', 'Board-E 3/4 (etqr)', 'lower root, anterior'])
sheet('HVF_C_HE3_body_context.jpg', 'C. HE3 corrected in body / face context -- HB2 + HF2 + HP-B: front | front 3/4 | rear 3/4',
      [('c1', [img('HE3_g', v) for v in ('front', 'tqf', 'tqr')], None), ('c2', [img('HE3_c2_g', v) for v in ('front', 'tqf', 'tqr')], None)], colw=480, heads=['front', 'front 3/4', 'rear 3/4'])
LP = R['family']['HE1_length_vs_MF_pct']; TD = lambda k: TE[k + ' c1']
L5 = [('MF', 'Marchfolk (0 %)'), ('HE1 L6.3', 'HE1 L 6.3 old floor (+%.0f %%)' % LP['HE1-HVEAR3']), ('HE2', 'HE2 frozen (+%.0f %%)' % LP['HE2']),
      ('HE1 L5.3', 'L 5.3 size test (+%.0f %%)' % LP['HE1-L5.3']), ('HE1 L5.6s', 'L 5.6 size-only (+%.0f %%)' % LP['HE1-L5.6size']), ('HE1', 'HE1 RECOMMENDED (+%.0f %%)' % LP['HE1'])]
cap5 = {'MF': '', 'HE1 L6.3': 'aspect %.2f | clean c1+c2' % TD('HE1-HVEAR3')['aspect_max'], 'HE2': '', 'HE1 L5.3': 'aspect %.3f / c2 %.3f: at the gate' % (TD('HE1-L5.3')['aspect_max'], TE['HE1-L5.3 c2']['aspect_max']),
        'HE1 L5.6s': 'aspect %.2f | clean c1+c2' % TD('HE1-L5.6size')['aspect_max'], 'HE1': 'aspect %.2f / %.2f | clean | 8 poses' % (TD('HE1')['aspect_max'], TE['HE1 c2']['aspect_max'])}
sheet('HVF_D_HE1_size_floor.jpg', 'D. HE1 size floor -- matched scale, common head (c1); measured length vs the Marchfolk auricle in the column heads',
      [(v, [img(tag(k) + '_g', vv) for k, _ in L5], [cap5[k] for k, _ in L5] if v == 'side' else None) for v, vv in (('front', 'front'), ('side', 'elat'), ('front 3/4', 'etq'), ('rear 3/4', 'rq'))],
      colw=310, heads=[lb for _, lb in L5], note='Shared engineering sheet + HR2 + stage-3 sheet stretch repair (same connectivity, same family controls). L 6.3 (old floor) read as a scaled HE2.\nL 5.3 sits at the aspect gate. Recommended HE1 = L 5.6 with a human-family outline (upright, rounded upper ear with a soft Halvren apex) and a fully rolled\nhuman helix; the L 5.6 size-only column keeps the HVEAR3 body for comparison.')
sheet('HVF_E_family_lineup.jpg', 'E. Final Halvren ear family -- HE1 (HVEAR4) | HE2 (frozen) | HE3 (HVEAR4); matched head / scale / camera',
      [('%s %s' % (c, v), [img(tag(k + ('' if c == 'c1' else ' c2')) + '_g', vv) for k in ('HE1', 'HE2', 'HE3')], ['HE1 composite %.2f' % CO['HE1'], 'HE2 %.2f' % CO['HE2'], 'HE3 %.2f' % CO['HE3']] if (c, v) == ('c1', 'side') else None)
       for c in ('c1', 'c2') for v, vv in (('front 3/4', 'etq'), ('side', 'elat'))] + [('c1 head', [img(tag(k) + '_g', 'front') for k in ('HE1', 'HE2', 'HE3')], None)], colw=420, heads=['HE1', 'HE2 (frozen)', 'HE3'])
DC = R['decomposition']; DOM = R['domain_list']; fig, axs = plt.subplots(1, 3, figsize=(21, 6.5), sharey=True)
for ai, p in enumerate(('MF-FN', 'MF-AE', 'MF-VA')):
    ax = axs[ai]
    for k, col, off in (('HE3-before', '#999999', -0.18), ('HE3', '#c0392b', 0.18)):
        dd = DC[k][p]['domains']; qs = [q for q in DOM if q in dd]
        ax.barh(np.array([DOM.index(q) for q in qs]) + off, [dd[q]['residual'] for q in qs], height=0.34, color=col, label='%s R2 %.2f (alpha %.2f, n %d)' % (k, DC[k][p]['r2'], DC[k][p]['alpha'], DC[k][p]['n']))
    ax.axvline(0, c='k', lw=0.8); ax.set_yticks(range(len(DOM))); ax.set_yticklabels(DOM, fontsize=9); ax.set_title(p + ': residual from the one-alpha line (source-SD units)', fontsize=11); ax.legend(fontsize=9, loc='lower right'); ax.grid(alpha=0.3)
fig.suptitle('F. HE3 firewall decomposition before (HVEAR3 on HR2) / after (HVEAR4): larger residuals = less like a Marchfolk -> elf interpolation'); fig.tight_layout(rect=(0, 0, 1, 0.93)); fig.savefig(os.path.join(OUT, 'HVF_F_HE3_decomposition.jpg'), dpi=72); plt.close(fig)
print('BOARDS_DONE', sorted(os.listdir(OUT)))
