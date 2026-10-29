# hv_he2_rootvis_boards.py EVIDIR OUTDIR : Halvren root visual-integration order §7 boards (identical cameras = left root frame of the common HB2+HF2+HP-B head
# per configuration, matched scale, neutral clay; A / B / G with volume-revealing cavity shading):
#   A  critical root-silhouette board, corrected HE2 (HR2) c1 / c2: strict side | Board-E rear 3/4 (the 29f2c16 'etqr' view) | rear 3/4 | stronger rear 3/4 |
#      direct rear | lower-rear 3/4 (inferior root)
#   B  before (29f2c16 HR1) / after (HR2), c1 and c2: Board-E rear 3/4 | rear 3/4 | direct rear | lower-root closeups (lower anterior / lower posterior)
#   C  wireframe / root topology: HR1 | HR2 (c1), altered vertices marked (red = root loop lowered, orange = head skin in the fall-off band / extra faired ring,
#      magenta = auricle-sheet vertices moved by the postauricular sulcus / lobe-edge lift; cuff blue, transition green)
#   D  standard ear views (front | side | front 3/4, c1 / c2) + ear-only lineup on the common head (MF | HE1 | HE2 | HE3 | frozen Fenn | Aelari | Vael)
#   E  body / face / ear context HB2 + HF2 + HP-B + corrected HE2: front | front 3/4 | rear 3/4 (c1 / c2)
#   F  measured-domain firewall chart HR1 / HR2
import sys, os, json, subprocess, numpy as np
from PIL import Image, ImageDraw
from concurrent.futures import ThreadPoolExecutor
os.environ.setdefault('EAR_TOPO', 'v002')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import hv_ear_quick as QK; import hv_ear_domains as D
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
EV, OUT = sys.argv[1:3]; os.makedirs(OUT, exist_ok=True); TMP = '/tmp/claude-0/rt/hv/ear/board_rv'; os.makedirs(TMP, exist_ok=True); QK.TMP = TMP
E = '/tmp/claude-0/rt/hv/ear'; jl = lambda p: json.load(open(p)); GREY = np.array([0.80, 0.78, 0.76]); H = {'c1': 'HVC1-HB2HF2-HPB', 'c2': 'HVF178-HB2HF2-HPB'}
R = jl(EV + '/HE2_root_visual_record.json'); font = QK.font
def extra(h):
    rd = D.frame(h, 'l'); O, n, b, u = rd['O'], rd['n'], rd['b'], rd['u']; z3 = np.array([0, 0, 1.0]); C = O - 2.5 * u + 0.3 * b; nb = lambda w: tuple(np.round(np.asarray(w, float), 4))
    return dict(zf=(nb(0.7 * n - b - 0.3 * z3), C, 2.4), zr=(nb(0.7 * n + b - 0.3 * z3), C, 2.4), zl=(nb(n), C, 2.4), tqr=((1, -1, 0.1), None, 15))
_oc = QK.cams; QK.cams = lambda h: {**_oc(h), **extra(h)}
bp = lambda w, c, k: '%s/%s/build/%s_%s_branch.npz' % (E, w, H[c], k)
IT = {'HR1 c1': (bp('he3', 'c1', 'HE2'), 'c1'), 'HR2 c1': (bp('hr2f', 'c1', 'HE2'), 'c1'), 'HR1 c2': (bp('he3', 'c2', 'HE2'), 'c2'), 'HR2 c2': (bp('hr2f', 'c2', 'HE2'), 'c2'),
      'MF': ('%s/../hpe/fam/%s_fam.npz' % (E, H['c1']), 'c1'), 'HE1': (bp('hr2f', 'c1', 'HE1'), 'c1'), 'HE3': (bp('hr2f', 'c1', 'HE3'), 'c1'), 'HE1 c2': (bp('hr2f', 'c2', 'HE1'), 'c2'), 'HE3 c2': (bp('hr2f', 'c2', 'HE3'), 'c2'),
      'FN': (bp('ref/FN', 'c1', 'E2'), 'c1'), 'AE': (bp('ref/FN', 'c1', 'AE-E2'), 'c1'), 'VA': (bp('ref/RI3', 'c1', 'VA-E2-RI3'), 'c1')}
tag = lambda k: k.replace(' ', '_')
def marks(k):
    z = np.load(IT[k][0]); p = z['part']; C = np.tile(GREY, (len(z['V']), 1)); C[p == 'cuff'] = [0.58, 0.76, 0.92]; C[p == 'transition'] = [0.55, 0.85, 0.55]
    rec = jl(IT[k][0].replace('.npz', '.json')); lp = z['v005_to_branch'][np.r_[[np.array(rec['sides'][s]['root_loop_v005']) for s in ('l', 'r')]].ravel()]
    if k.startswith('HR2'):
        fz = np.load('%s/../hpe/fam/%s_fam.npz' % (E, H[IT[k][1]])); vb = z['v005_to_branch']; keep = np.nonzero(vb >= 0)[0]; mv = np.linalg.norm(z['V'][vb[keep]] - fz['V'][keep], axis=1) > 1e-4
        C[vb[keep[mv]]] = np.where((p[vb[keep[mv]]] == 'transition')[:, None], C[vb[keep[mv]]], [0.98, 0.62, 0.25])
        a = np.load(IT['HR1 ' + IT[k][1]][0]); sh = np.isin(p, ('front', 'back', 'rim'))
        for sd in ('l', 'r'):
            m = sh & (z['side'] == sd); d = z['V'][m] - a['V'][m]; d -= d.mean(0); idx = np.nonzero(m)[0]; C[idx[np.linalg.norm(d, axis=1) > 0.06]] = [0.85, 0.35, 0.85]
    C[lp] = [0.92, 0.12, 0.12]; return C
REV = dict(os.environ, RENDER_REVEAL='1'); jobs = []
for k in ('HR1 c1', 'HR2 c1', 'HR1 c2', 'HR2 c2'):
    p, c = IT[k]; jobs.append((QK.run(tag(k) + '_rv', p, H[c], ['side', 'aq', 'rq', 'rq2', 'rr', 'lr', 'zf', 'zr'], 620), REV))
    jobs.append((QK.run(tag(k) + '_g', p, H[c], ['front', 'elat', 'etq', 'tqf', 'tqr', 'aq', 'rq'], 620), os.environ))
for k in ('HR1 c1', 'HR2 c1'): p, c = IT[k]; jobs.append((QK.run(tag(k) + '_w', p, H[c], ['rq', 'lr', 'zl', 'zf'], 620, marks(k), True), os.environ))
for k in ('MF', 'HE1', 'HE3', 'HE1 c2', 'HE3 c2', 'FN', 'AE', 'VA'): p, c = IT[k]; jobs.append((QK.run(tag(k) + '_g', p, H[c], ['elat', 'etq', 'aq', 'rq'], 620), os.environ))
for k in ('HE1', 'HE3', 'HE1 c2', 'HE3 c2'): p, c = IT[k]; jobs.append((QK.run(tag(k) + '_rv', p, H[c], ['aq', 'rq', 'lr', 'zf'], 620), REV))
with ThreadPoolExecutor(3) as ex: list(ex.map(lambda j: subprocess.run(j[0], env=j[1], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL), jobs))
def img(t, v):
    p = os.path.join(TMP, '%s_%s.png' % (t, v)); return Image.open(p).convert('RGB') if os.path.exists(p) else Image.new('RGB', (620, 620), (255, 200, 200))
def sheet(fn, title, rows, colw=400, note=None, lab_w=150, heads=None):
    ncol = max(len(r[1]) for r in rows); nl = note.count('\n') + 1 if note else 0; hh = 26 if heads else 0
    Sh = Image.new('RGB', (lab_w + ncol * colw, 60 + hh + sum(colw + (28 if r[2] else 8) for r in rows) + 21 * nl + 14), 'white'); d = ImageDraw.Draw(Sh)
    d.text((14, 14), title, fill=(0, 0, 0), font=font(19, True)); y = 56
    if heads:
        for i, t in enumerate(heads): d.text((lab_w + 6 + i * colw, y), t, fill=(0, 0, 0), font=font(15, True))
        y += hh
    for lab, ims, caps in rows:
        d.multiline_text((8, y + colw // 2 - 18), lab, fill=(0, 0, 0), font=font(15, True), spacing=4)
        for i, im in enumerate(ims):
            Sh.paste(im.resize((colw, colw)), (lab_w + i * colw, y))
            if caps and caps[i]: d.text((lab_w + 6 + i * colw, y + colw + 4), caps[i], fill=(30, 30, 30), font=font(13))
        y += colw + (28 if caps else 8)
    if note: d.multiline_text((14, y + 4), note, fill=(50, 50, 50), font=font(14), spacing=6)
    Sh.save(os.path.join(OUT, fn), quality=90)
TE = R['technical']; SI = R['silhouette']
cap = lambda c: 'pedestal p90 post %.2f / inf %.2f cm | loop crease post %.0f / inf %.0f deg' % tuple([SI['HE2 %s HR2' % c]['pedestal_vs_true_head'][s]['p90_cm'] for s in ('posterior', 'inferior')] + [SI['HE2 %s HR2' % c]['loop_crease_deg'][s]['mean'] for s in ('posterior', 'inferior')])
V6 = ['side', 'aq', 'rq', 'rq2', 'rr', 'lr']; HD6 = ['strict side', 'Board-E rear 3/4 (etqr)', 'rear 3/4', 'stronger rear 3/4', 'direct rear', 'lower-rear 3/4']
sheet('HE2RV_A_critical_root_silhouette.jpg', 'A. Critical root silhouette -- corrected HE2 (HR2 root), c1 / c2, revealing shading (cavity ridge / valley); one auricle, no flange, no lower fork?',
      [('HE2 HR2\nc1', [img('HR2_c1_rv', v) for v in V6], [cap('c1'), None, None, None, None, None]), ('HE2 HR2\nc2', [img('HR2_c2_rv', v) for v in V6], [cap('c2'), None, None, None, None, None])],
      colw=380, heads=HD6, note='Camera = left root frame of each configuration head (b posterior). Board-E rear 3/4 = the 29f2c16 HE2C_E / HE2C_C "3/4 rear" camera (it looks backward from anterior-lateral);\nrear 3/4 / stronger / direct rear / lower-rear 3/4 = true posterior cameras (n + b mixes). Captions: HR2 secondary-silhouette measures (pedestal above the extrapolated head; root-loop crease).')
V4 = ['aq', 'rq', 'rr', 'zf', 'zr']; HD4 = ['Board-E rear 3/4', 'rear 3/4', 'direct rear', 'lower root, anterior', 'lower root, posterior']
bc = lambda k: 'pedestal post %.2f inf %.2f | crease %.0f / %.0f deg' % tuple([SI[k]['pedestal_vs_true_head'][s]['p90_cm'] for s in ('posterior', 'inferior')] + [SI[k]['loop_crease_deg'][s]['mean'] for s in ('posterior', 'inferior')])
sheet('HE2RV_B_before_after.jpg', 'B. Before (29f2c16 HR1) / after (HR2) -- HE2 c1 and c2, identical cameras, revealing shading (cavity)',
      [('BEFORE\nHR1 c1', [img('HR1_c1_rv', v) for v in V4], [bc('HE2 c1 HR1')] + [None] * 4), ('AFTER\nHR2 c1', [img('HR2_c1_rv', v) for v in V4], [bc('HE2 c1 HR2')] + [None] * 4),
       ('BEFORE\nHR1 c2', [img('HR1_c2_rv', v) for v in V4], [bc('HE2 c2 HR1')] + [None] * 4), ('AFTER\nHR2 c2', [img('HR2_c2_rv', v) for v in V4], [bc('HE2 c2 HR2')] + [None] * 4)],
      colw=400, heads=HD4, note='BEFORE: raised root pedestal behind / below the pinna (second contour), raised cuff tab beside the free lobe with a notch between (lower fork).\nAFTER: root loop seated on the head, wide-faired postauricular sulcus, lobe edge close to the head -- the lowest form is the lobe itself.')
sheet('HE2RV_C_wireframe_root_topology.jpg', 'C. Wireframe / root topology, c1: HR1 (29f2c16) | HR2 -- identical connectivity (face sha256 equal); altered vertices marked',
      [('HR1', [img('HR1_c1_w', v) for v in ('rq', 'lr', 'zl', 'zf')], None), ('HR2', [img('HR2_c1_w', v) for v in ('rq', 'lr', 'zl', 'zf')], None)], colw=430, heads=['rear 3/4', 'lower-rear 3/4', 'lower root, side', 'lower root, anterior'],
      note='red = 52-vertex root loop (HR2: lowered onto the extrapolated head, cap 0.30 / inferior 0.60 x head scale; now a biharmonic unknown) | orange = v005 head skin moved by HR2 (1.0 cm fall-off band +\nthe extra faired ring) | magenta = auricle-sheet vertices moved non-rigidly > 0.06 cm (postauricular sulcus on the back / rim sheet near the junction; lobe-edge lift 0.70 -> 0.30) | blue = cuff | green = transition ring.\nFaces / topology unchanged: same quad connectivity, root valence 4 x 52 both sides.')
sheet('HE2RV_D_standard_views.jpg', 'D. Standard ear views -- corrected HE2 (HR2) c1 / c2: front | side | front 3/4',
      [('HE2 HR2\nc1', [img('HR2_c1_g', v) for v in ('front', 'elat', 'etq')], None), ('HE2 HR2\nc2', [img('HR2_c2_g', v) for v in ('front', 'elat', 'etq')], None)], colw=460, heads=['front', 'side', 'front 3/4'])
FW = R['firewall']; L7 = ['MF', 'HE1', 'HR2 c1', 'HE3', 'FN', 'AE', 'VA']; LB = {'MF': 'Marchfolk', 'HE1': 'HE1 (HR2)', 'HR2 c1': 'HE2 corrected', 'HE3': 'HE3 (HR2)', 'FN': 'frozen Fenn', 'AE': 'frozen Aelari', 'VA': 'frozen Vael'}
fk = {'HE1': 'HE1', 'HR2 c1': 'HE2', 'HE3': 'HE3'}
sheet('HE2RV_D2_ear_only_lineup.jpg', 'D2. Ear-only lineup -- one common Halvren head (c1), identical camera, matched scale',
      [(v, [img(tag(k) + '_g', v) for k in L7], ['%s R2 %.2f' % (LB[k], FW[fk[k]]['best_r2']) if k in fk else LB[k] for k in L7] if v == 'elat' else None) for v in ('elat', 'etq', 'aq', 'rq')], colw=330)
sheet('HE2RV_E_body_face_ear.jpg', 'E. Body / face / ear context -- HB2 + HF2 + HP-B + corrected HE2 (HR2): front | front 3/4 | rear 3/4',
      [('c1', [img('HR2_c1_g', v) for v in ('front', 'tqf', 'tqr')], None), ('c2', [img('HR2_c2_g', v) for v in ('front', 'tqf', 'tqr')], None)], colw=500, heads=['front', 'front 3/4', 'rear 3/4'])
sheet('HE2RV_G_HE1_HE3_consistency.jpg', 'G. HE1 / HE3 with the shared HR2 root (consistency only; not frozen): Board-E rear 3/4 | rear 3/4 | lower-rear 3/4 | lower root, anterior',
      [(k.replace(' ', '\n'), [img(tag(k) + '_rv', v) for v in ('aq', 'rq', 'lr', 'zf')], None) for k in ('HE1', 'HE1 c2', 'HE3', 'HE3 c2')], colw=380)
DM = R['domains']; DOM = R['domain_list']; fig, axs = plt.subplots(1, 2, figsize=(18, 6.5))
for ai, k in enumerate(('HE2-HR1', 'HE2')):
    ax = axs[ai]; ax.scatter(np.clip([DM[k]['t'][q] for q in DOM], -1.45, 2.45), np.arange(len(DOM)), c='k', s=50, zorder=3)
    ax.set_yticks(range(len(DOM))); ax.set_yticklabels(DOM, fontsize=9); ax.axvspan(0.35, 0.65, color='#eeeeee'); ax.axvline(0, c='k', lw=0.8); ax.axvline(1, c='k', lw=0.8); ax.set_xlim(-1.5, 2.5)
    ax.set_title('%s: R2 %s' % ('HR1 (29f2c16)' if k == 'HE2-HR1' else 'HR2 (corrected root)', ' / '.join('%s %.2f' % (p, FW[k]['pairs'][p]['r2']) for p in ('MF-FN', 'MF-AE', 'MF-VA'))), fontsize=11)
    ax.set_xlabel('t (0 Marchfolk, 1 elf mean; grey = midpoint band; clipped at -1.45 / 2.45)'); ax.grid(alpha=0.3)
fig.suptitle('F. HE2 measured-domain arithmetic firewall, HR1 / HR2 (fail: R2 >= 0.8 with n >= 6)'); fig.tight_layout(rect=(0, 0, 1, 0.93)); fig.savefig(os.path.join(OUT, 'HE2RV_F_firewall.jpg'), dpi=72); plt.close(fig)
print('BOARDS_DONE', sorted(os.listdir(OUT)))
