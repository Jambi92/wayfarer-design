# va_final_sheets.py WORK OUTDIR : Vael final consolidation / freeze order §21 final visual freeze package (VA_FINAL_01..20; identical orthographic
# cameras per row, true scale, neutral clay wherever the read is judged). WORK = clean-rebuild folder (run_vafinal*.sh + va_final_gates.py).
# Workbench renders (grask_rigprep_v001/render_attr.py), composed with PIL; resumable; 2 Blender processes.
import sys, os, json, subprocess, csv, numpy as np
from PIL import Image, ImageDraw, ImageFont
from concurrent.futures import ThreadPoolExecutor
os.environ.setdefault('EAR_TOPO', 'v002')
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001')
import ear_branch_lib as E
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
W, OUT = sys.argv[1:3]; os.makedirs(OUT, exist_ok=True); TMP = os.environ.get('VA_SHEET_TMP', W + '/sheet_r'); os.makedirs(TMP, exist_ok=True)
BP = '/home/claude/stc/bin/python3'; REND = '/home/claude/wayfarer-design/tools/rac/rp/grask_rigprep_v001/render_attr.py'; PA = '/tmp/claude-0/rt/va/partA'; CUR = '/tmp/claude-0/rt/va/ear'
CF = {'c1': ('VAL4-R1-VD2-VF2', 'VA_M_REF_RP3_v001', 'FNM178', 'AEM178', 'MFM178', 'SGM178'), 'c2': ('VALF178-R1-VD2-VF2', 'VA_F_REF_RP3_v001', 'FNF178', 'AEF178', 'MFF178', 'SGF178')}
GREY = np.array([0.80, 0.78, 0.76]); jl = lambda p: json.load(open(p)); CAN = 'VA-E2-RI3'; EW = W + '/ear/RI3'
def font(sz, bold=False):
    f = '/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf' % ('-Bold' if bold else ''); return ImageFont.truetype(f, sz) if os.path.exists(f) else ImageFont.load_default()
jobs = []
def render(tag, npz, col, views, wire=False, px=640):
    vs = ';'.join('%s:%s:%s:%.2f' % (n, ','.join('%.4f' % x for x in d), ','.join('%.3f' % x for x in c), hs) for n, d, c, hs in views)
    cf = os.path.join(TMP, tag + '_col.npy'); np.save(cf, np.asarray(col, np.float32)); jobs.append([BP, REND, '--', npz, cf, TMP, tag, vs, '1' if wire else '0', str(px)])
def img(tag, name):
    p = os.path.join(TMP, '%s_%s.png' % (tag, name)); return Image.open(p).convert('RGB') if os.path.exists(p) else Image.new('RGB', (600, 600), 'white')
def heat(x, lo, hi):
    t = np.clip((x - lo) / (hi - lo + 1e-12), 0, 1)[:, None]; return (1 - t) * np.array([0.2, 0.35, 0.85]) + t * np.array([0.95, 0.25, 0.15])
def blend(a, b):
    A_ = np.asarray(a, float) * np.array([1.0, 0.55, 0.55]); B_ = np.asarray(b, float) * np.array([0.55, 0.65, 1.0]); return Image.fromarray(np.clip(0.5 * A_ + 0.5 * B_, 0, 255).astype(np.uint8))
def sil(a, b):                                           # silhouette overlay: Vael only red, comparator only blue, both grey (background = corner pixel)
    A_ = np.asarray(a, int); B_ = np.asarray(b, int); ma = (np.abs(A_ - A_[2, 2]).max(2) > 10); mb = (np.abs(B_ - B_[2, 2]).max(2) > 10)
    O_ = np.full(A_.shape, 255, np.uint8); O_[ma & mb] = (150, 150, 150); O_[ma & ~mb] = (215, 40, 40); O_[~ma & mb] = (40, 90, 220); return Image.fromarray(O_)
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
hcam = lambda V: np.array([0.0, V[V[:, 2] > V[:, 2].max() - 25][:, 1].mean(), V[:, 2].max() - 12.0])
Lo = E.canonical_layout(); ns = len(Lo['st']); J = np.asarray(Lo['J'])
# ---------------------------------------------------------------- data + cameras
D = {}
for c, (h, nm, fn, ae, mf, sg) in CF.items():
    P = '%s/build/%s_%s_branch.npz' % (EW, h, CAN); z = np.load(P); r = jl(P.replace('.npz', '.json')); V = z['V']; fr = r['sides']['l']['frame']; O, n, b, u = [np.array(fr[k]) for k in ('O', 'n', 'b', 'u')]
    X = V[np.nonzero(z['side'] == 'l')[0][0]:][:ns]; bu = np.c_[(X - O) @ b, (X - O) @ u]; inJ = (Lo['part'][:ns] == 'front') & (E._inside_dist(bu[J], bu) > 0)
    D[c] = dict(h=h, nm=nm, fn=fn, ae=ae, mf=mf, sg=sg, P=P, z=z, r=r, Ce=V[z['side'] == 'l'].mean(0), H=hcam(V), O=O, n=n, b=b, u=u, Cc=X[inJ].mean(0), Tg=X[J[Lo['part'][J] == 'front']].mean(0) - 0.4 * u,
                B=np.array([0.0, V[:, 1].mean(), (V[:, 2].max() + V[:, 2].min()) / 2]), stat=V[:, 2].max() - V[:, 2].min(), CUR='%s/build/%s_VA-E2_branch.npz' % (CUR, h))
def views(c, names):
    k = D[c]; S = max(D[x]['stat'] for x in D) / 2 + 4; nb = lambda w: tuple(np.round(w, 4))
    T = dict(bfront=((0, 1, 0), k['B'], S), bprof=((1, 0, 0), k['B'], S), brear=((0, -1, 0), k['B'], S), btq=((1, 1, 0.05), k['B'], S),
             hfront=((0, 1, 0.03), k['H'], 15), hprof=((1, 0, 0), k['H'], 15), htq=((1, 1, 0.1), k['H'], 15), hrear=((0, -1, 0), k['H'], 15),
             elat=((1, 0.15, 0.05), k['Ce'], 5.6), efront=((0, 1, 0.02), k['Ce'], 5.6), erear=((0.15, -1, 0.05), k['Ce'], 5.6), etop=((0.1, 0.05, 1), k['Ce'], 5.6),
             eface=((1, 0.9, 0.15), k['Ce'], 4.8), etq=((1, 0.45, 0.25), k['Ce'], 4.8), etqr=((0.6, -1, 0.15), k['Ce'], 4.8), ecrear=((0.35, -1, 0.1), k['Ce'], 5.2),
             root=((1, 0.2, 0.0), k['O'], 3.4), under=((0.3, -0.5, -1), k['Ce'], 3.8), concha=(nb(k['n'] + 0.25 * np.array([0, 1, 0])), k['Cc'], 2.4), tragus=(nb(k['n'] + np.array([0, 0.9, -0.25])), k['Tg'], 2.0))
    return [(n,) + T[n] for n in names]
for c, k in D.items():
    z = k['z']; P = k['P']; t = c
    render(t + '_g', P, np.tile(GREY, (len(z['V']), 1)), views(c, ['bfront', 'bprof', 'brear', 'btq', 'hfront', 'hprof', 'htq', 'hrear', 'elat', 'efront', 'erear', 'etop', 'etq', 'etqr', 'root', 'concha', 'tragus']))
    if os.path.exists(k['CUR']): zc = np.load(k['CUR']); render(t + '_cur', k['CUR'], np.tile(GREY, (len(zc['V']), 1)), views(c, ['etq', 'elat', 'hfront', 'etqr']))
    render(t + '_w', P, part_cols(z), views(c, ['eface', 'ecrear', 'root', 'under']), wire=True)
    render(t + '_v', P, valence_cols(z), views(c, ['eface', 'ecrear']), wire=True)
    pf = np.load('%s/audit/%s_%s_audit_perface.npz' % (EW, k['h'], CAN)); F, bad, asp = pf['faces'], pf['ang_bad'], pf['asp']
    C = face_part(z) * 0.45 + 0.5; C[F] = [0.93, 0.93, 0.93]; C[F[bad]] = [0.92, 0.18, 0.12]; render(t + '_t4', P, C, views(c, ['eface', 'ecrear', 'root']), wire=True)
    C = np.tile(GREY, (len(z['Q']), 1)); C[F] = heat(asp, 1.0, 6.0); C[F[asp > 6]] = [0.55, 0.1, 0.65]; render(t + '_as', P, C, views(c, ['eface', 'ecrear', 'root']), wire=True)
    d = np.load('%s/audit/%s_%s_audit_cuffdev.npy' % (EW, k['h'], CAN)); C = np.tile(GREY, (len(z['V']), 1)); C[d[:, 0].astype(int)] = heat(d[:, 1], 0, 0.6); render(t + '_rd', P, C, views(c, ['root', 'under']))
    r6 = np.load('%s/src/%s_r6_regen.npz' % (W, k['h'])); keep = r6['keep']; Fx = r6['F'][keep[r6['F']].all(1)]; sp_ = os.path.join(TMP, 'src_%s.npz' % c); np.savez_compressed(sp_, V=r6['V'], Q=Fx)
    render(t + '_src', sp_, np.tile(GREY, (len(r6['V']), 1)), views(c, ['bfront', 'bprof', 'hprof', 'elat']))
    # hidden-ear bodies (va_hidden_ear.py output, 178 cm) for the final source and the matched comparators
    Vh = np.load('%s/he/%s_earhidden.npz' % (W, k['h']))['V']; ym = Vh[:, 1].mean(); Bh = np.array([0.0, ym, Vh[:, 2].max() / 2]); Hh = hcam(Vh); Pc = np.array([0.0, ym, 0.53 * Vh[:, 2].max()])
    for nn in (k['h'], k['fn'], k['ae'], k['mf'], k['sg']):
        hp = '%s/he/%s_earhidden.npz' % (W, nn); V = np.load(hp)['V']
        render('he_%s' % nn, hp, np.tile(GREY, (len(V), 1)), [('bfront', (0, 1, 0), Bh, 96), ('bprof', (1, 0, 0), Bh, 96), ('btq', (1, 1, 0.05), Bh, 96), ('hfront', (0, 1, 0.03), Hh, 15), ('hprof', (1, 0, 0), Hh, 15),
                                                              ('htq', (1, 1, 0.1), Hh, 15), ('pelvis', (1, 0.25, 0.0), Pc, 30), ('pfront', (0, 1, 0.0), Pc, 30)], px=520)
    for pn in ('shoulder_flex90_l', 'shoulder_abd90_l', 'elbow_130_l', 'hip_flex90_l', 'knee_140_l', 'neck_rot45'):
        pp = '%s/def/%s_%s_final.npz' % (W, pn, k['h'])
        if not os.path.exists(pp): continue
        X = np.load(pp); Xv = X['V']; Cf_ = np.tile(GREY, (len(z['Q']), 1)); fl_ = np.asarray(X['flip']).astype(int).ravel() if 'flip' in X.files else np.zeros(0, int)
        Cf_[fl_[fl_ < len(Cf_)]] = [0.92, 0.18, 0.12]; q = os.path.join(TMP, 'pose_%s_%s.npz' % (c, pn)); np.savez_compressed(q, V=Xv, Q=z['Q'])
        fo_ = np.asarray(X['fold']).astype(int).ravel() if 'fold' in X.files else np.zeros(0, int); Cf_[fo_[fo_ < len(Cf_)]] = [0.98, 0.55, 0.05]
        Cb = np.array([Xv[:, 0].mean(), Xv[:, 1].mean(), (Xv[:, 2].max() + Xv[:, 2].min()) / 2]); render('pose_%s_%s' % (c, pn), q, Cf_, [('v', (1, 1, 0.05), Cb, D[c]['stat'] / 2 + 8)], px=480)
        if len(fo_):
            Fc = Xv[z['Q'][fo_]].reshape(-1, 3).mean(0); Cz = face_part(z) * 0.5 + 0.45; Cz[fo_] = [0.98, 0.45, 0.05]
            render('fold_%s_%s' % (c, pn), q, Cz, [('near', (1, 0.3, -0.4), Fc, 0.6), ('mid', (1, 0.3, -0.2), Fc, 2.5), ('far', (1, 0.2, 0.0), Fc, 6.0)], wire=True, px=480)
    for pn in ('neck_flex30', 'neck_ext30', 'head_yaw_l45', 'head_yaw_r45', 'head_pitch_down20', 'head_pitch_up20', 'head_roll_l20', 'head_roll_r20'):
        pp = '%s/deform/%s_%s_%s.npy' % (EW, k['h'], CAN, pn)
        if os.path.exists(pp):
            X = np.load(pp); q = os.path.join(TMP, 'epose_%s_%s.npz' % (c, pn)); np.savez_compressed(q, V=X, Q=z['Q']); render('epose_%s_%s' % (c, pn), q, part_cols(z), [('tq', (1, 0.3, 0.1), X[z['side'] == 'l'].mean(0), 7.0)], px=420)
FZ = {'FN_c1': '/tmp/claude-0/rt/fn/final/ear/build/FNL4-CF2_E2_branch.npz', 'FN_c2': '/tmp/claude-0/rt/fn/final/ear/build/FNF181-CF2_E2_branch.npz',
      'AE_c1': '/tmp/claude-0/rt/ae/final/ear/build/AEL1-R1_AE-E2_branch.npz', 'AE_c2': '/tmp/claude-0/rt/ae/final/ear/build/AELF190-R1_AE-E2_branch.npz', 'VA_c1': D['c1']['P'], 'VA_c2': D['c2']['P']}
for tag, p in FZ.items():
    z = np.load(p); V = z['V']; Hc = hcam(V); Ce = V[z['side'] == 'l'].mean(0); rec = jl(p.replace('.npz', '.json')); C = np.tile(GREY, (len(V), 1))
    for sd in ('l', 'r'):
        fr = rec['sides'][sd]['frame']; O, n = np.array(fr['O']), np.array(fr['n']); m = (z['side'] == sd) & np.isin(z['part'], ['front', 'back', 'rim']); C[m] = heat((V[m] - O) @ n, 0, 3.2)
    render('cmp_' + tag, p, np.tile(GREY, (len(V), 1)), [('prof', (1, 0, 0), Hc, 15), ('front', (0, 1, 0.03), Hc, 15), ('rear', (0, -1, 0), Hc, 15), ('etq', (1, 0.45, 0.25), Ce, 5.0)])
    render('cmpl_' + tag, p, C, [('front', (0, 1, 0.03), Hc, 15)])
PR = ['proj_m10', 'proj_p10', 'tilt_m8', 'tilt_p8', 'sweep_m06', 'sweep_p06', 'len_m10', 'len_p10', 'tip_blunt', 'tip_sharp', 'wb_m8', 'wb_p8']
for pn in PR:
    P = '%s/probe/%s/%s_%s_branch.npz' % (EW, pn, D['c1']['h'], CAN)
    if os.path.exists(P): z = np.load(P); render('pr_' + pn, P, np.tile(GREY, (len(z['V']), 1)), views('c1', ['etq']), px=400); render('prw_' + pn, P, part_cols(z), views('c1', ['eface']), wire=True, px=400)
print('render jobs', len(jobs), flush=True)
done_ = lambda j: all(os.path.exists(os.path.join(TMP, '%s_%s.png' % (j[6], v_.split(':')[0]))) for v_ in j[7].split(';'))
todo = [j for j in jobs if not done_(j)]; print('to render', len(todo), flush=True)
with ThreadPoolExecutor(int(os.environ.get('VA_SHEET_THREADS', '2'))) as ex: list(ex.map(lambda j: subprocess.run(j, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL), todo))
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
G = jl(W + '/VAEL_FINAL_gates.json'); GC = G['configurations']; AU = {c: jl('%s/audit/%s_%s_audit.json' % (EW, k['h'], CAN)) for c, k in D.items()}
for c, k in D.items():
    i = 1 if c == 'c1' else 2
    sheet('VA_FINAL_%02d_full_body_%s.jpg' % (i, c), 'Vael RP3 final — configuration %s full body (%s from %s; front | profile | rear | 3-4)' % (c[1], k['nm'], k['h']),
          [(c, [img(c + '_g', v) for v in ('bfront', 'bprof', 'brear', 'btq')], ['%s  stature %.1f cm  %d V / %d Q' % (k['nm'], k['stat'], len(k['z']['V']), len(k['z']['Q'])), '', '', ''])], colw=560)
rows = []
for c, k in D.items():
    for lab, v in (('front', 'bfront'), ('profile', 'bprof'), ('3-4', 'btq')):
        rows.append(('%s %s' % (c, lab), [img('he_' + n, v) for n in (k['h'], k['fn'], k['ae'])] + [sil(img('he_' + k['h'], v), img('he_' + k['ae'], v)), sil(img('he_' + k['h'], v), img('he_' + k['fn'], v))],
                     ['Vael ' + k['h'], 'frozen Fenn ' + k['fn'], 'frozen Aelari ' + k['ae'], 'Vael only red / Aelari only blue', 'Vael only red / Fenn only blue'] if lab == 'front' else None))
cv = lambda c: GC[c]['vael_canon_firewalls']
sheet('VA_FINAL_03_three_elf_hidden_ear_bodies.jpg', 'Vael RP3 final — three-elf body firewall at equal height (178 cm), ears hidden, geometry only: Vael | frozen Fenn | frozen Aelari | silhouette overlays (grey = shared)', rows, colw=400,
      note='canon (incl. all vs-Fenn / vs-Aelari rows): c1 %s, c2 %s; equal to the accepted VF2 result: c1 %s, c2 %s' % (cv('c1')['canon'], cv('c2')['canon'], cv('c1')['equals_accepted_VF2'], cv('c2')['equals_accepted_VF2']))
rows = []
for c, k in D.items():
    for lab, v in (('front', 'bfront'), ('profile', 'bprof')):
        rows.append(('%s %s' % (c, lab), [img('he_' + n, v) for n in (k['h'], k['mf'], k['sg'])] + [sil(img('he_' + k['h'], v), img('he_' + k['mf'], v))],
                     ['Vael', 'Marchfolk ' + k['mf'], 'Sagekin ' + k['sg'], 'Vael only red / Marchfolk only blue'] if lab == 'front' else None))
sheet('VA_FINAL_04_Vael_vs_humans.jpg', 'Vael RP3 final — human firewall (178 cm, ears / pigmentation neutralised): Vael | Marchfolk | Sagekin | overlay', rows, colw=440,
      note='body systems material vs humans: c1 %s, c2 %s (accepted VF2: 5 / 8 both)\n%s' % (cv('c1')['body_systems_material_vs_humans'], cv('c2')['body_systems_material_vs_humans'],
            '; '.join('%s %s' % (s.split(' ', 1)[1], 'M' if v['material'] else '-') for s, v in cv('c1')['body_systems'].items())))
pn_ = lambda c: '  '.join('%s %s' % (r['rule'].split(' ')[0], 'ok' if r['holds_all_t'] else 'NO') for r in GC[c]['pelvis']['rules'] if r.get('gating'))
rows = []
for c, k in D.items():
    ns_ = [k['h'], k['fn'], k['ae'], k['mf']]; rows += [('%s oblique' % c, [img('he_' + n, 'pelvis') for n in ns_], ['Vael', 'Fenn', 'Aelari', 'Marchfolk']), ('%s front' % c, [img('he_' + n, 'pfront') for n in ns_], None)]
sheet('VA_FINAL_05_pelvis.jpg', 'Vael RP3 final — pelvis (ears hidden, 178 cm): Vael | frozen Fenn | frozen Aelari | Marchfolk — skeletal-proxy rules at t = 0 / 0.5 / 1.0', rows, colw=440,
      note='c1 %s gating: %s\nc2 %s gating: %s' % (GC['c1']['pelvis']['gating'], pn_('c1'), GC['c2']['pelvis']['gating'], pn_('c2')))
rows = []
for c, k in D.items():
    ns_ = [k['h'], k['fn'], k['ae'], k['mf'], k['sg']]
    rows += [('%s front' % c, [img('he_' + n, 'hfront') for n in ns_], ['Vael  face systems %s  elf rows %s' % (cv(c)['face_systems_material'], cv(c)['elf_face_rows']), 'Fenn', 'Aelari', 'Marchfolk', 'Sagekin']),
             ('%s profile' % c, [img('he_' + n, 'hprof') for n in ns_], None), ('%s 3-4' % c, [img('he_' + n, 'htq') for n in ns_], None)]
sheet('VA_FINAL_06_hidden_ear_face.jpg', 'Vael RP3 final — hidden-ear neutral-complexion face (ears collapsed, 178 cm): Vael | frozen Fenn | frozen Aelari | Marchfolk | Sagekin', rows, colw=420)
for c, k in D.items():
    i = 7 if c == 'c1' else 8
    sheet('VA_FINAL_%02d_head_%s.jpg' % (i, c), 'Vael RP3 final — configuration %s head (VC2 face + VA-E2-RI3 ear; front | profile | 3-4 | rear)' % c[1], [(c, [img(c + '_g', v) for v in ('hfront', 'hprof', 'htq', 'hrear')], [k['nm'], '', '', ''])], colw=540)
sheet('VA_FINAL_09_ear_neutral_clay.jpg', 'Vael RP3 final — VA-E2-RI3 neutral clay, no annotation (head 3-4 | close 3-4 front | close profile | close 3-4 rear)',
      [(c, [img(c + '_g', v) for v in ('htq', 'etq', 'elat', 'etqr')], None) for c in D], colw=560)
ME = {c: jl('%s/meas/%s_%s_measure.json' % (EW, k['h'], CAN))['sides'] for c, k in D.items()}; av = lambda c, x: float(np.mean([ME[c][q][x] for q in ('l', 'r')]))
m = lambda c: 'L %.2f cm  width %.2f  body angle %.1f°  chord %.1f°  upper %.1f°' % (av(c, 'length_lobe_to_tip_cm'), av(c, 'max_width_cm'), av(c, 'auricle_body_angle_deg'), av(c, 'side_view_chord_lobe_to_tip_deg'), av(c, 'side_view_upper_extension_deg'))
sheet('VA_FINAL_10_ear_views.jpg', 'Vael RP3 final — VA-E2-RI3 ear: lateral | front | rear | top (left ear; identical cameras per row)', [(c, [img(c + '_g', v) for v in ('elat', 'efront', 'erear', 'etop')], [m(c), '', '', '']) for c in D])
sheet('VA_FINAL_11_root_concha_closeups.jpg', 'Vael RP3 final — root / concha closeups, neutral clay: root (lateral, low) | concha (looking in) | tragus / antitragus | close 3-4 rear',
      [(c, [img(c + '_g', v) for v in ('root', 'concha', 'tragus', 'etqr')], None) for c in D], colw=540)
COL = {'front': '#d9774a', 'back': '#8f6fb8', 'rim': '#d8b23a', 'cuff': '#4f8fd0', 'transition': '#4caf50', 'v005': '#9a9a9a'}
fig, axs = plt.subplots(len(D), 4, figsize=(19, 4.6 * len(D)), squeeze=False)
for ci, (c, k) in enumerate(D.items()):
    O, n, b, u = k['O'], k['n'], k['b'], k['u']; cc = k['Cc'] - O; z = k['z']; V = z['V']; Q = z['Q']; part = z['part']; dd = V - O; B = dd @ b; U = dd @ u; N = dd @ n
    near = (np.abs(B) < 6) & (np.abs(U) < 6) & (N > -4) & (V[:, 0] > 0); Qs = Q[near[Q].all(1)]; Es = np.unique(np.sort(np.concatenate([Qs[:, [0, 1]], Qs[:, [1, 2]], Qs[:, [2, 3]], Qs[:, [3, 0]]]), 1), axis=0); A_, B_ = Es[:, 0], Es[:, 1]
    for li, (mode, L_) in enumerate((('h', cc @ u), ('h', cc @ u + 1.2), ('v', cc @ b), ('v', cc @ b + 1.0))):
        X = U if mode == 'h' else B; Y = B if mode == 'h' else U; s = (X[A_] - L_) * (X[B_] - L_) < 0; t = (L_ - X[A_[s]]) / (X[B_[s]] - X[A_[s]])
        py = Y[A_[s]] + t * (Y[B_[s]] - Y[A_[s]]); pn = N[A_[s]] + t * (N[B_[s]] - N[A_[s]]); pp = np.where(part[A_[s]] != 'v005', part[A_[s]], part[B_[s]]); ax = axs[ci, li]
        for k2, col in COL.items(): mm = pp == k2; ax.scatter(py[mm], pn[mm], s=3, c=col)
        ax.set_aspect('equal'); ax.set_xlim(-3.5, 4.0); ax.set_ylim(-1.5, 3.5); ax.grid(alpha=0.3)
        ax.set_title('%s %s section %s %+.1f cm' % (c, 'horizontal' if mode == 'h' else 'vertical', 'up' if mode == 'h' else 'posterior', L_), fontsize=10); ax.set_xlabel('posterior (cm)' if mode == 'h' else 'up (cm)')
        if li == 0: ax.set_ylabel('lateral from root plane (cm)')
fig.suptitle('Vael RP3 final — root / concha sections (root frame, true scale; orange front, violet back, yellow rim, blue cuff, green transition, grey skin)'); fig.tight_layout(rect=(0, 0, 1, 0.96))
fig.savefig(os.path.join(OUT, 'VA_FINAL_12_root_concha_sections.jpg'), dpi=80); plt.close(fig)
sheet('VA_FINAL_13_ear_wire_poles.jpg', 'Vael RP3 final — ear wire (front orange, back violet, rim yellow, cuff blue, transition green) and poles (blue 3, red 5, violet 6+)',
      [(c, [img(c + '_w', 'eface'), img(c + '_w', 'ecrear'), img(c + '_v', 'eface'), img(c + '_v', 'ecrear')], ['%d V / %d Q' % (AU[c]['verts'], AU[c]['faces']), '', 'poles', '']) for c in D], colw=520)
t4c = lambda c: 'T-4 %d / %d (%.1f %%)  aspect max %.2f  >10: %d  min corner %.1f°' % (AU[c]['T4']['angle_violations'], AU[c]['T4']['branch_faces'], 100 * AU[c]['T4']['angle_violations'] / AU[c]['T4']['branch_faces'], AU[c]['T4']['aspect_max'], AU[c]['T4']['aspect_gt10'], AU[c]['T4']['min_angle'])
sheet('VA_FINAL_14_T4_aspect.jpg', 'Vael RP3 final — T-4 (red = a corner outside 45-135°) and quad aspect (blue 1 .. red 6, violet > 6)',
      [(c + ' T-4', [img(c + '_t4', v) for v in ('eface', 'ecrear', 'root')], [t4c(c), '', '']) for c in D] + [(c + ' aspect', [img(c + '_as', v) for v in ('eface', 'ecrear', 'root')], None) for c in D])
RS = jl('/home/claude/wayfarer-design/reviews/rac-rp3-evidence/vael_rp3_ear_root_integration/VAEL_EAR_root_integration_summary.json')['alternatives']
rc = lambda c: 'crease %.0f / %.0f°  cuff dev mean %.3f p95 %.3f cm  anterior mound p90 %.2f cm  clearance %.2f cm' % (AU[c]['root_dihedral']['l']['max_deg'], AU[c]['root_dihedral']['r']['max_deg'], AU[c]['root_deviation']['cuff_mean_cm'],
                                                                                                          AU[c]['root_deviation']['cuff_p95_cm'], RS['RI3 %s' % c]['root_concha']['anterior_cuff_mound_p90_cm'], AU[c]['ear_to_head_clearance']['min_cm'])
sheet('VA_FINAL_15_root_integration.jpg', 'Vael RP3 final — root integration: cuff skin vs hidden-ear skull (0 .. 0.6 cm), wire root, and prototype VA-E2 (red) over final RI3 (blue), same camera',
      [(c, [img(c + '_rd', 'root'), img(c + '_w', 'root'), img(c + '_g', 'concha')], [rc(c), '', '']) for c in D] +
      [(c + ' overlay', [blend(img(c + '_cur', v), img(c + '_g', v)) for v in ('etq', 'elat', 'etqr')], ['3-4 close', 'profile close', '3-4 rear close']) for c in D], colw=560)
FW = G['ear_firewall']['configs']; fcap = lambda c, nm: '%s  angle %.1f°  w/L %.3f  chord %.1f°' % (nm, FW[c]['measures'][nm]['body_angle_deg'], FW[c]['measures'][nm]['max_width_over_length'], FW[c]['measures'][nm]['side_view_chord_deg'])
rows = []
for c in D:
    for v in ('prof', 'front', 'rear', 'etq'):
        rows.append(('%s %s' % (c, v), [img('cmp_FN_' + c, v), img('cmp_VA_' + c, v), img('cmp_AE_' + c, v)], [fcap(c, nm) for nm in ('Fenn E2', 'Vael VA-E2-RI3', 'Aelari AE-E2')] if v == 'prof' else None))
sheet('VA_FINAL_16_three_elf_ears.jpg', 'Vael RP3 final — frozen Fenn E2 | Vael VA-E2-RI3 | frozen Aelari AE-E2, each on its own head, same relative camera', rows, colw=470,
      note='; '.join('%s: %s' % (c, ', '.join('%s %s' % (k_, 'ok' if v_ else 'NO') for k_, v_ in FW[c]['checks'].items())) for c in FW))
fig, axs = plt.subplots(2, 5, figsize=(22, 8.5)); order = ['Fenn E2', 'Vael VA-E2-RI3', 'Aelari AE-E2']; colr = ['#79b', '#a32', '#9b7']
for ci, c in enumerate(D):
    for mi, (key, ttl) in enumerate((('body_angle_deg', 'auricle-body angle (deg)'), ('max_width_over_length', 'max width / length'), ('side_view_chord_deg', 'side-view chord (deg, backward)'),
                                      ('free_standoff_mean_over_HH', 'mean free-ear stand-off / HH'), ('tip_standoff_over_HH', 'tip stand-off / HH'))):
        ax = axs[ci, mi]; vals = [FW[c]['measures'][o][key] for o in order]; ax.bar(range(3), vals, color=colr); ax.set_xticks(range(3)); ax.set_xticklabels(['Fenn', 'Vael', 'Aelari'])
        ax.set_title('%s %s' % (c, ttl), fontsize=10); ax.set_ylim(min(vals) * 0.85 if 'standoff' in key or 'width' in key else 0, max(vals) * 1.08)
        for xi, vv in enumerate(vals): ax.text(xi, vv, '%.3f' % vv if vv < 5 else '%.1f' % vv, ha='center', va='bottom', fontsize=9)
rs = {c: FW[c]['standoff_residual'] for c in FW}
fig.suptitle('Vael RP3 final — projection / stand-off vs frozen Fenn / Aelari. Accepted c1 residual (order §2): mean %+.4f, tip %+.4f HH over Fenn; c2 order Fenn > Vael > Aelari: %s' %
             (rs['c1']['mean_over_fenn_HH'], rs['c1']['tip_over_fenn_HH'], rs['c2']['stand_off_order_fenn_gt_vael_gt_aelari'])); fig.tight_layout(rect=(0, 0, 1, 0.94))
fig.savefig(os.path.join(TMP, 'proj_chart.png'), dpi=90); plt.close(fig)
ch = Image.open(os.path.join(TMP, 'proj_chart.png')).convert('RGB'); lat = Image.new('RGB', (6 * 330, 330), 'white')
for i, t in enumerate(('cmpl_FN_c1', 'cmpl_VA_c1', 'cmpl_AE_c1', 'cmpl_FN_c2', 'cmpl_VA_c2', 'cmpl_AE_c2')): lat.paste(img(t, 'front').resize((330, 330)), (330 * i, 0))
Sh = Image.new('RGB', (max(ch.width, lat.width), ch.height + lat.height + 40), 'white'); Sh.paste(ch, (0, 0)); Sh.paste(lat, (0, ch.height + 40))
ImageDraw.Draw(Sh).text((14, ch.height + 8), 'Lateral stand-off from the root plane (blue 0 .. red 3.2 cm), head front: c1 Fenn | Vael | Aelari, c2 Fenn | Vael | Aelari', fill=(0, 0, 0), font=font(16, True))
Sh.save(os.path.join(OUT, 'VA_FINAL_17_projection_standoff.jpg'), quality=88)
DSm = jl(W + '/VAEL_FINAL_deformation_summary.json'); PN = ('shoulder_flex90_l', 'shoulder_abd90_l', 'elbow_130_l', 'hip_flex90_l', 'knee_140_l', 'trunk_twist30')
sheet('VA_FINAL_18_body_deformation.jpg', 'Vael RP3 final — Standard v1 deformation (production body; source rig + carried MPFB weights, plain LBS; red = flipped). c1 shoulder_flex90 = registered VAEL-CF-SHOULDER-1',
      [(c, [img('pose_%s_%s' % (c, p), 'v') for p in PN], ['%s %d (fam %d, MF %d)' % (p.replace('_l', ''), DSm[c]['poses'][p]['final_flipped'], DSm[c]['poses'][p]['family_flipped'], DSm[c]['poses'][p]['marchfolk_v005_flipped']) for p in PN]) for c in D], colw=400)
fd = DSm['c1']['worse_than_family_detail']
if fd:
    sheet('VA_FINAL_18b_c1_neck_rot45_fold.jpg', 'Vael RP3 final — OPEN ITEM: c1 neck_rot45, one new fold (> 120° dihedral, orange) on two sub-millimetre left cuff quads at the lobe junction',
          [('c1 neck_rot45', [img('fold_c1_neck_rot45', v) for v in ('near', 'mid', 'far')], ['edges (mm) %s' % fd['neck_rot45']['edge_lengths_mm'][0], 'cuff wire', 'head'])], colw=560,
          note='no flip, no contact, no root inversion; family realization 0 folds in this pose; with the ear branch bound 100 % to the head bone (diagnostic, not production) every pose equals the family')
pr = GC['c1']['probes']['rebuilt']; EP = ('neck_flex30', 'neck_ext30', 'head_yaw_l45', 'head_yaw_r45', 'head_pitch_down20', 'head_pitch_up20', 'head_roll_l20', 'head_roll_r20')
dc = lambda c, p: '%s %s' % (p, '/'.join(str(x) for x in GC[c]['ear']['deform'][p]))
pcap = lambda p: '%s T4 %d SI %d %s' % (p, pr[p]['T4'], pr[p]['self_intersection_branch'], 'ok' if pr[p]['moves_intended'] else 'WRONG') if p in pr else p
sheet('VA_FINAL_19_ear_readiness_probes.jpg', 'Vael RP3 final — head / neck readiness (branch contacts / flips / root inversions; 0/0/0 = pass) and the twelve RI3 shape probes (c1; diagnostics, not morphs)',
      [('%s %d' % (c, i + 1), [img('epose_%s_%s' % (c, p), 'tq') for p in EP[4 * i:4 * i + 4]], [dc(c, p) for p in EP[4 * i:4 * i + 4]]) for c in D for i in (0, 1)] +
      [('probes %d-%d' % (i + 1, i + 6), [img('pr_' + p, 'etq') for p in PR[i:i + 6]], [pcap(p) for p in PR[i:i + 6]]) for i in (0, 6)] +
      [('wire %d-%d' % (i + 1, i + 6), [img('prw_' + p, 'eface') for p in PR[i:i + 6]], None) for i in (0, 6)], colw=380)
sheet('VA_FINAL_20_source_production_overlay.jpg', 'Vael RP3 final — accepted R-6 VF2 source vs production body, same camera — only the ear branch departs from the source (human auricle -> VA-E2-RI3)',
      [(c, [sil(img(c + '_src', v), img(c + '_g', v)) for v in ('bfront', 'bprof', 'hprof')] + [blend(img(c + '_src', 'elat'), img(c + '_g', 'elat'))], [D[c]['nm'] + '  silhouette: source only red, production only blue', '', '', 'ear close: source red / production blue tint']) for c in D])
VA = {c: jl('%s/val/%s_final_validator_v2_D1-D6.json' % (W, k['h'])) for c, k in D.items()}; rows_ = sorted(VA['c1']['stations'])
with open(os.path.join(OUT, 'VA_FINAL_validator_margin_table.csv'), 'w', newline='') as fh:
    wr = csv.writer(fh); wr.writerow(['station', 'c1 loops', 'c1 min', 'c1 margin', 'c2 loops', 'c2 min', 'c2 margin', 'c1 status', 'c2 status'])
    for s in rows_:
        a, b = VA['c1']['stations'][s], VA['c2']['stations'][s]; wr.writerow([s, a['loops_v2'], a['required'], a['margin'], b['loops_v2'], b['required'], b['margin'], a['status_D1_D3'], b['status_D1_D3']])
print('sheets done', flush=True)
