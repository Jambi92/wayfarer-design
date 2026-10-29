# hv_he2_boards.py EVIDIR OUTDIR : Halvren HE2 closure order §9 comparison boards HE2C_A..F (matched scale, identical cameras = left root frame of the common
# HB2+HF2+HP-B head per configuration, neutral clay): A HE2 before / after; B ear-only firewall lineup; C root / concha hard gate c1 / c2 with junction / mound
# metrics; D body / face / ear mosaic; E updated topology audit (corrected HE2 on rigid cuff / Vael RI3 root / Halvren HR1 path + wireframe connectivity);
# F measured-domain firewall chart before / after.
import sys, os, json, subprocess, numpy as np
from PIL import Image, ImageDraw
from concurrent.futures import ThreadPoolExecutor
os.environ.setdefault('EAR_TOPO', 'v002')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import hv_ear_quick as QK
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
EV, OUT = sys.argv[1:3]; os.makedirs(OUT, exist_ok=True); TMP = '/tmp/claude-0/rt/hv/ear/board_r'; os.makedirs(TMP, exist_ok=True); QK.TMP = TMP
E = '/tmp/claude-0/rt/hv/ear'; jl = lambda p: json.load(open(p)); GREY = np.array([0.80, 0.78, 0.76]); H = {'c1': 'HVC1-HB2HF2-HPB', 'c2': 'HVF178-HB2HF2-HPB'}
R = jl(EV + '/HE2_closure_record.json'); font = QK.font
b = lambda w, c, k: '%s/%s/build/%s_%s_branch.npz' % (E, w, H[c], k)
IT = {'MF': ('%s/../hpe/fam/%s_fam.npz' % (E, H['c1']), 'c1'), 'HE2-before': (b('he', 'c1', 'HE2'), 'c1'), 'HE2': (b('he3', 'c1', 'HE2'), 'c1'), 'HE2 c2': (b('he3', 'c2', 'HE2'), 'c2'),
      'MF c2': ('%s/../hpe/fam/%s_fam.npz' % (E, H['c2']), 'c2'), 'HE1': (b('he3', 'c1', 'HE1'), 'c1'), 'HE3': (b('he3', 'c1', 'HE3'), 'c1'),
      'FN': (b('ref/FN', 'c1', 'E2'), 'c1'), 'AE': (b('ref/FN', 'c1', 'AE-E2'), 'c1'), 'VA': (b('ref/RI3', 'c1', 'VA-E2-RI3'), 'c1'),
      'HE2 rigid': (b('topo3/FN', 'c1', 'HE2-R'), 'c1'), 'HE2 RI3': (b('topo3/RI3', 'c1', 'HE2-V'), 'c1')}
def tag(k): return k.replace(' ', '_')
def pc(z):
    p = z['part']; C = np.tile(GREY, (len(z['V']), 1)); C[p == 'front'] = [0.88, 0.66, 0.55]; C[p == 'back'] = [0.70, 0.58, 0.80]; C[p == 'rim'] = [0.95, 0.83, 0.45]; C[p == 'cuff'] = [0.58, 0.76, 0.92]; C[p == 'transition'] = [0.55, 0.85, 0.55]; return C
jobs = []
for k, (p, c) in IT.items():
    if os.path.exists(p): jobs.append(QK.run(tag(k) + '_g', p, H[c], ['etq', 'front', 'elat', 'root', 'etqr', 'tqf'], 520))
for k in ('HE2', 'HE2 rigid', 'HE2 RI3', 'HE2 c2'):
    p, c = IT[k]
    if os.path.exists(p): jobs.append(QK.run(tag(k) + '_w', p, H[c], ['elat', 'root'], 520, pc(np.load(p)), True))
todo = [j for j in jobs if not all(os.path.exists(os.path.join(TMP, '%s_%s.png' % (j[6], v.split(':')[0]))) for v in j[7].split(';'))]
with ThreadPoolExecutor(2) as ex: list(ex.map(lambda j: subprocess.run(j, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL), todo))
def img(t, v):
    p = os.path.join(TMP, '%s_%s.png' % (t, v)); return Image.open(p).convert('RGB') if os.path.exists(p) else Image.new('RGB', (520, 520), (255, 200, 200))
def sheet(fn, title, rows, colw=420, note=None, lab_w=160):
    ncol = max(len(r[1]) for r in rows); nl = note.count('\n') + 1 if note else 0; Sh = Image.new('RGB', (lab_w + ncol * colw, 64 + sum(colw + (30 if r[2] else 8) for r in rows) + 22 * nl + 14), 'white'); d = ImageDraw.Draw(Sh)
    d.text((14, 14), title, fill=(0, 0, 0), font=font(19, True)); y = 64
    for lab, ims, caps in rows:
        d.text((8, y + colw // 2 - 10), lab, fill=(0, 0, 0), font=font(15, True))
        for i, im in enumerate(ims):
            Sh.paste(im.resize((colw, colw)), (lab_w + i * colw, y))
            if caps and caps[i]: d.text((lab_w + 6 + i * colw, y + colw + 4), caps[i], fill=(30, 30, 30), font=font(13))
        y += colw + (30 if caps else 8)
    if note: d.multiline_text((14, y + 4), note, fill=(50, 50, 50), font=font(14), spacing=6)
    Sh.save(os.path.join(OUT, fn), quality=88)
FW = R['firewall']; T = R['technical']
fcap = lambda k: '%s | best R2 %.2f (%s)' % (k, FW[k]['best_r2'], FW[k]['best_pair']) if k in FW else k
sheet('HE2C_A_before_after.jpg', 'A. HE2 before (HVEAR2 on the shared path) | after (HVEAR3 realization-calibrated, HR1 + cuff repair) — c1, neutral clay, identical cameras',
      [(v, [img('HE2-before_g', v), img('HE2_g', v)], [fcap('HE2-before'), fcap('HE2')] if v == 'etq' else None) for v in ('etq', 'front', 'elat', 'root')], colw=460)
L7 = ['MF', 'HE1', 'HE2', 'HE3', 'FN', 'AE', 'VA']; LB = dict(MF='Marchfolk', HE1='HE1', HE2='HE2 corrected', HE3='HE3', FN='frozen Fenn', AE='frozen Aelari', VA='frozen Vael')
sheet('HE2C_B_ear_only_firewall.jpg', 'B. Ear-only firewall — one common Halvren head (face / pigment neutral, no hair), identical camera, matched head scale',
      [(v, [img(tag(k) + '_g', v) for k in L7], [LB[k] if k not in FW else '%s R2 %.2f' % (LB[k], FW[k]['best_r2']) for k in L7] if v == 'elat' else None) for v in ('elat', 'etq', 'etqr')], colw=330)
rc = lambda c: T['HE2 %s' % c]
sheet('HE2C_C_root_concha_gate.jpg', 'C. Root / concha hard gate — corrected HE2 on c1 and c2 (HR1 root): one auricle? junction / mound metrics in captions',
      [('%s' % c, [img(('MF' if c == 'c1' else 'MF_c2') + '_g', 'root'), img(('HE2' if c == 'c1' else 'HE2_c2') + '_g', 'root'), img(('HE2' if c == 'c1' else 'HE2_c2') + '_g', 'etqr'), img(('HE2' if c == 'c1' else 'HE2_c2') + '_g', 'elat')],
        ['Marchfolk', 'HE2 root | mound p90 %.2f | junction %.2f cm' % (rc(c)['mound_p90_cm'], rc(c)['junction_cm']), 'HE2 3/4 rear | min corner %.1f deg' % rc(c)['min_angle'], 'HE2 side | %s' % ('CLEAN' if rc(c)['technical_pass'] else 'FAIL')]) for c in ('c1', 'c2')], colw=440)
sheet('HE2C_D_mosaic.jpg', 'D. Body / face / ear mosaic on HB2 + HF2 + HP-B: HE1 | corrected HE2 | HE3',
      [(v, [img(tag(k) + '_g', v) for k in ('HE1', 'HE2', 'HE3')], [k for k in ('HE1', 'HE2 corrected', 'HE3')] if v == 'tqf' else None) for v in ('tqf', 'front', 'etq')], colw=480)
TA = R['topology_audit']
sheet('HE2C_E_topology_audit.jpg', 'E. Corrected HE2 realization path — same HVEAR3 geometry on: rigid Fenn v002 cuff | exact Vael RI3 root | Halvren HR1 path (seat rule + cuff repair); wireframe: front orange, back violet, rim yellow, cuff blue',
      [(v, [img(tag(k) + s, v) for k in ('HE2 rigid', 'HE2 RI3', 'HE2')], ['%s | %s | %.0f deg | mound %.2f' % (k, 'clean' if TA[k]['technical_pass'] else 'FAIL', TA[k]['min_angle'], TA[k]['mound_p90_cm']) for k in ('HE2 rigid', 'HE2 RI3', 'HE2')] if v == 'etqr' else None)
       for v, s in (('etqr', '_g'), ('root', '_g'), ('elat', '_w'))], colw=440)
D = R['domains']; DOM = R['domain_list']; fig, axs = plt.subplots(1, 2, figsize=(18, 6.5))
for ai, k in enumerate(('HE2-before', 'HE2')):
    ax = axs[ai]
    for j, (pr, col) in enumerate((('MF-FN', '#d9774a'), ('MF-AE', '#4f8fd0'), ('MF-VA', '#4caf50'))):
        f = FW[k]['pairs'][pr]; ax.scatter([D[k]['t'][q] for q in DOM], np.arange(len(DOM)) + 0.2 * (j - 1), c=col, s=40, label='%s  n %d  R2 %.2f  alpha %.2f' % (pr, f['n'], f['r2'], f['alpha'])) if j == 0 else None
    ax.scatter([D[k]['t'][q] for q in DOM], np.arange(len(DOM)), c='k', s=45, label='t vs Marchfolk -> elf mean')
    ax.set_yticks(range(len(DOM))); ax.set_yticklabels(DOM, fontsize=9); ax.axvspan(0.35, 0.65, color='#eeeeee'); ax.axvline(0, c='k', lw=0.8); ax.axvline(1, c='k', lw=0.8); ax.set_xlim(-1.5, 2.5)
    ax.set_title('%s: R2 %s' % ('before (HVEAR2)' if k == 'HE2-before' else 'after (HVEAR3)', ' / '.join('%s %.2f' % (p, FW[k]['pairs'][p]['r2']) for p in ('MF-FN', 'MF-AE', 'MF-VA'))), fontsize=11)
    ax.set_xlabel('t (0 Marchfolk, 1 elf mean; grey = midpoint band)'); ax.grid(alpha=0.3)
fig.suptitle('F. HE2 measured-domain arithmetic firewall, before / after (fail: R2 >= 0.8 with n >= 6)'); fig.tight_layout(rect=(0, 0, 1, 0.93)); fig.savefig(os.path.join(OUT, 'HE2C_F_firewall_before_after.jpg'), dpi=72); plt.close(fig)
print('BOARDS_DONE', sorted(os.listdir(OUT)))
