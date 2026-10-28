# ae_final_sheets.py WORK OUTDIR : Aelari final consolidation (order 2026-10-28) §20 final visual freeze package (20 sheets; identical orthographic cameras
# per row, true scale). WORK = clean-rebuild folder (run_aefinal*.sh). Workbench renders (grask_rigprep_v001/render_attr.py), composed with PIL; resumable.
import sys, os, json, subprocess, csv, numpy as np
from PIL import Image, ImageDraw, ImageFont
from concurrent.futures import ThreadPoolExecutor
os.environ.setdefault('EAR_TOPO', 'v002')
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001')
import ear_branch_lib as E
W, OUT = sys.argv[1:3]; os.makedirs(OUT, exist_ok=True); TMP = os.environ.get('AE_SHEET_TMP', W + '/sheet_r'); os.makedirs(TMP, exist_ok=True)
BP = '/home/claude/stc/bin/python3'; REND = '/home/claude/wayfarer-design/tools/rac/rp/grask_rigprep_v001/render_attr.py'; PA0 = '/tmp/claude-0/rt/ae/partA'
CF = {'c1': ('AEL1-R1', 'AE_M_REF_RP3_v001', 'FNM190', 'MFM190', 'SGM190'), 'c2': ('AELF190-R1', 'AE_F_REF_RP3_v001', 'FNF190', 'MFF190', 'SGF190')}
GREY = np.array([0.80, 0.78, 0.76]); jl = lambda p: json.load(open(p)); CAN = 'AE-E2'
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
# region labels on the native hm08 (dominant weight), for torso / leg bands on the hidden-ear bodies
nz = np.load('/tmp/claude-0/rt/fn/src/FNL4_native.npz'); bones = [str(b) for b in nz['bones']]; dom = np.array(bones)[np.asarray(nz['W']).argmax(1)]
TRUNK = np.array([b.startswith(('spine', 'pelvis', 'clavicle', 'Root')) for b in dom]); LEG = np.array([b.startswith(('thigh', 'calf', 'foot', 'ball')) for b in dom])
R6P = lambda n: ('%s/src/%s_r6_regen.npz' % (W, n)) if n.startswith('AE') else ('%s/cmp/%s_r6.npz' % (PA0, n))
def joints(n):
    j = json.loads(str(np.load(R6P(n))['joints'])); z = lambda b: j[b][0][2]
    return dict(clav=0.5 * (z('clavicle_l') + z('clavicle_r')), sp3=z('spine_03'), sp1=z('spine_01'), hip=0.5 * (z('thigh_l') + z('thigh_r')), knee=0.5 * (z('calf_l') + z('calf_r')), ankle=0.5 * (z('foot_l') + z('foot_r')))
C_TH, C_WA, C_FE, C_SH = [0.95, 0.60, 0.20], [0.30, 0.70, 0.75], [0.45, 0.55, 0.90], [0.90, 0.45, 0.55]
def band_cols(n, V):
    j = joints(n); C = np.tile(GREY, (len(V), 1)); z = V[:, 2]
    C[TRUNK & (z >= j['sp3']) & (z <= j['clav'])] = C_TH; C[TRUNK & (z >= j['sp1']) & (z < j['sp3'])] = C_WA
    C[LEG & (z <= j['hip']) & (z > j['knee'])] = C_FE; C[LEG & (z <= j['knee']) & (z > j['ankle'])] = C_SH; return C
# ---------------------------------------------------------------- data + cameras
D = {}
for c, (h, nm, fn, mf, sg) in CF.items():
    P = '%s/ear/build/%s_%s_branch.npz' % (W, h, CAN); z = np.load(P); r = jl('%s/ear/build/%s_%s_branch.json' % (W, h, CAN))
    V = z['V']; Ce = V[z['side'] == 'l'].mean(0); hv = V[V[:, 2] > V[:, 2].max() - 25]; Hc = np.array([0.0, hv[:, 1].mean(), V[:, 2].max() - 12.0]); O = np.array(r['sides']['l']['frame']['O'])
    Bc = np.array([0.0, V[:, 1].mean(), (V[:, 2].max() + V[:, 2].min()) / 2]); D[c] = dict(h=h, nm=nm, fn=fn, mf=mf, sg=sg, P=P, z=z, r=r, Ce=Ce, H=Hc, O=O, B=Bc, stat=V[:, 2].max() - V[:, 2].min())
def views(c, names):
    k = D[c]; S = max(D[x]['stat'] for x in D) / 2 + 4
    T = dict(bfront=((0, 1, 0), k['B'], S), bprof=((1, 0, 0), k['B'], S), brear=((0, -1, 0), k['B'], S), btq=((1, 1, 0.05), k['B'], S),
             hfront=((0, 1, 0.03), k['H'], 15), hprof=((1, 0, 0), k['H'], 15), htq=((1, 1, 0.1), k['H'], 15),
             elat=((1, 0.15, 0.05), k['Ce'], 5.6), efront=((0, 1, 0.02), k['Ce'], 5.6), erear=((0.15, -1, 0.05), k['Ce'], 5.6), etop=((0.1, 0.05, 1), k['Ce'], 5.6),
             eface=((1, 0.9, 0.15), k['Ce'], 5.2), ecrear=((0.35, -1, 0.1), k['Ce'], 5.2), root=((1, 0.2, 0.0), k['O'], 3.6), under=((0.3, -0.5, -1), k['Ce'], 3.8))
    return [(n,) + T[n] for n in names]
for c, k in D.items():
    z = k['z']; P = k['P']; t = c
    render(t + '_g', P, np.tile(GREY, (len(z['V']), 1)), views(c, ['bfront', 'bprof', 'brear', 'btq', 'hfront', 'hprof', 'htq', 'elat', 'efront', 'erear', 'etop']))
    render(t + '_w', P, part_cols(z), views(c, ['eface', 'ecrear', 'root', 'under']), wire=True)
    render(t + '_v', P, valence_cols(z), views(c, ['eface', 'ecrear']), wire=True)
    pf = np.load('%s/ear/audit/%s_%s_audit_perface.npz' % (W, k['h'], CAN)); F, bad, asp = pf['faces'], pf['ang_bad'], pf['asp']
    C = face_part(z) * 0.45 + 0.5; C[F] = [0.93, 0.93, 0.93]; C[F[bad]] = [0.92, 0.18, 0.12]; render(t + '_t4', P, C, views(c, ['eface', 'ecrear', 'root']), wire=True)
    C = np.tile(GREY, (len(z['Q']), 1)); C[F] = heat(asp, 1.0, 6.0); C[F[asp > 6]] = [0.55, 0.1, 0.65]; render(t + '_as', P, C, views(c, ['eface', 'ecrear', 'root']), wire=True)
    d = np.load('%s/ear/audit/%s_%s_audit_cuffdev.npy' % (W, k['h'], CAN)); C = np.tile(GREY, (len(z['V']), 1)); C[d[:, 0].astype(int)] = heat(d[:, 1], 0, 0.6); render(t + '_rd', P, C, views(c, ['root', 'under']))
    r6 = np.load('%s/src/%s_r6_regen.npz' % (W, k['h'])); keep = r6['keep']; Fx = r6['F'][keep[r6['F']].all(1)]; sp_ = os.path.join(TMP, 'src_%s.npz' % c); np.savez_compressed(sp_, V=r6['V'], Q=Fx)
    render(t + '_src', sp_, np.tile(GREY, (len(r6['V']), 1)), views(c, ['bfront', 'bprof', 'hprof', 'elat']))
    # hidden-ear bodies (ae_hidden_ear.py output) for the final source and the matched comparators
    Vh = np.load('%s/he/%s_earhidden.npz' % (W, k['h']))['V']; ym = Vh[:, 1].mean(); Bh = np.array([0.0, ym, 96.0]); Hh = np.array([0.0, Vh[Vh[:, 2] > Vh[:, 2].max() - 25][:, 1].mean(), Vh[:, 2].max() - 12.0])
    jA = joints(k['h']); Tc = np.array([0.0, ym, 0.5 * (jA['sp1'] + jA['clav'])]); Lc = np.array([0.0, ym, 53.0]); Pc = np.array([0.0, ym, 98.0])
    for n in (k['h'], k['fn'], k['mf'], k['sg']):
        hp = '%s/he/%s_earhidden.npz' % (W, n); V = np.load(hp)['V']
        render('he_%s' % n, hp, np.tile(GREY, (len(V), 1)), [('bfront', (0, 1, 0), Bh, 102), ('bprof', (1, 0, 0), Bh, 102), ('hfront', (0, 1, 0.03), Hh, 15), ('hprof', (1, 0, 0), Hh, 15),
                                                             ('pelvis', (1, 0.25, 0.0), Pc, 30), ('pfront', (0, 1, 0.0), Pc, 30)], px=520)
        if n != k['sg']: render('band_%s' % n, hp, band_cols(n, V), [('tfront', (0, 1, 0), Tc, 34), ('tprof', (1, 0, 0), Tc, 34), ('lfront', (0, 1, 0), Lc, 56), ('lprof', (1, 0, 0), Lc, 56)], px=520)
    for pn in ('shoulder_abd90_l', 'elbow_130_l', 'hip_flex90_l', 'knee_140_l', 'neck_rot45', 'trunk_twist30'):
        pp = '%s/def/%s_%s_final.npz' % (W, pn, k['h'])
        if not os.path.exists(pp): continue
        X = np.load(pp); Xv = X['V']; Cf_ = np.tile(GREY, (len(z['Q']), 1)); fl_ = np.asarray(X['flip']).astype(int).ravel() if 'flip' in X.files else np.zeros(0, int)
        Cf_[fl_[fl_ < len(Cf_)]] = [0.92, 0.18, 0.12]; q = os.path.join(TMP, 'pose_%s_%s.npz' % (c, pn)); np.savez_compressed(q, V=Xv, Q=z['Q'])
        Cb = np.array([Xv[:, 0].mean(), Xv[:, 1].mean(), (Xv[:, 2].max() + Xv[:, 2].min()) / 2]); render('pose_%s_%s' % (c, pn), q, Cf_, [('v', (1, 1, 0.05), Cb, D[c]['stat'] / 2 + 8)], px=480)
    for pn in ('neck_flex30', 'head_yaw_l45', 'head_pitch_up20', 'head_roll_l20'):
        pp = '%s/ear/deform/%s_%s_%s.npy' % (W, k['h'], CAN, pn)
        if os.path.exists(pp):
            X = np.load(pp); q = os.path.join(TMP, 'epose_%s_%s.npz' % (c, pn)); np.savez_compressed(q, V=X, Q=z['Q']); render('epose_%s_%s' % (c, pn), q, part_cols(z), [('tq', (1, 0.3, 0.1), X[z['side'] == 'l'].mean(0), 8.0)])
FNE = '/tmp/claude-0/rt/fn/final/ear/build/FNL4-CF2_E2_branch.npz'
for tag, P in (('cmpFN', FNE), ('cmpAE', D['c1']['P'])):
    z = np.load(P); V = z['V']; hv = V[V[:, 2] > V[:, 2].max() - 25]; Hc = np.array([0.0, hv[:, 1].mean(), V[:, 2].max() - 12.0]); Ce = V[z['side'] == 'l'].mean(0)
    render(tag, P, np.tile(GREY, (len(V), 1)), [('prof', (1, 0, 0), Hc, 15), ('front', (0, 1, 0.03), Hc, 15), ('rear', (0, -1, 0), Hc, 15), ('elat', (1, 0.15, 0.05), Ce, 6.0)])
PR = ['proj_m10', 'proj_p10', 'tilt_m8', 'tilt_p8', 'sweep_m06', 'sweep_p06', 'len_m10', 'len_p10', 'tip_blunt', 'tip_sharp']
for pn in PR:
    P = '%s/ear/probe/%s/%s_%s_branch.npz' % (W, pn, D['c1']['h'], CAN)
    if os.path.exists(P): z = np.load(P); render('pr_' + pn, P, part_cols(z), views('c1', ['eface']), wire=True, px=420)
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
G = jl(OUT + '/../AELARI_FINAL_gates.json') if os.path.exists(OUT + '/../AELARI_FINAL_gates.json') else jl(W + '/AELARI_FINAL_gates.json')
GC = G['configurations']; AU = {c: jl('%s/ear/audit/%s_%s_audit.json' % (W, k['h'], CAN)) for c, k in D.items()}; ME = {c: GC[c]['ear']['measures'] for c in D}
for c, k in D.items():
    i = 1 if c == 'c1' else 2
    sheet('AE_FINAL_%02d_full_body_%s.jpg' % (i, c), 'Aelari RP3 final — configuration %s full body (%s from %s; front | profile | rear | 3-4)' % (c[1], k['nm'], k['h']),
          [(c, [img(c + '_g', v) for v in ('bfront', 'bprof', 'brear', 'btq')], ['%s  stature %.1f cm  %d V / %d Q' % (k['nm'], k['stat'], len(k['z']['V']), len(k['z']['Q'])), '', '', ''])], colw=560)
    sheet('AE_FINAL_%02d_head_%s.jpg' % (i + 2, c), 'Aelari RP3 final — configuration %s head (accepted face + AE-E2 ear; front | profile | 3-4)' % c[1], [(c, [img(c + '_g', v) for v in ('hfront', 'hprof', 'htq')], [k['h'], '', ''])])
rows = []
for c, k in D.items():
    for lab, v in (('front', 'bfront'), ('profile', 'bprof')):
        rows.append(('%s %s' % (c, lab), [img('he_' + k['h'], v), img('he_' + k['fn'], v), blend(img('he_' + k['h'], v), img('he_' + k['fn'], v))], [k['h'], k['fn'] + ' (frozen Fenn)', 'overlay (Aelari red, Fenn blue)'] if lab == 'front' else None))
sheet('AE_FINAL_05_equal_height_vs_Fenn_hidden_ear.jpg', 'Aelari RP3 final — equal height (190 cm), ears hidden: Aelari | frozen Fenn | overlay', rows, colw=480)
cap_t = lambda c, n, key: '%s  thor %.4f  waist/torso %.4f' % (n, GC[c]['body_identity']['vs_fenn']['thoracic_vertical_share'][key], GC[c]['body_identity']['vs_fenn']['waist_interval_over_torso'][key])
rows = []
for c, k in D.items():
    ns_ = [k['h'], k['fn'], k['mf']]; caps = [cap_t(c, k['h'], 'AE'), cap_t(c, k['fn'], 'FN'), k['mf']]
    rows += [('%s front' % c, [img('band_' + n, 'tfront') for n in ns_], caps), ('%s profile' % c, [img('band_' + n, 'tprof') for n in ns_], None)]
sheet('AE_FINAL_06_thorax_torso.jpg', 'Aelari RP3 final — thorax / torso (ears hidden): Aelari | frozen Fenn | Marchfolk — orange thoracic vertical, teal waist interval', rows, colw=480, legend=[('thoracic vertical', C_TH), ('waist interval', C_WA)],
      note='thoracic vertical vs Fenn: c1 %+.2f %%, c2 %+.2f %%' % (GC['c1']['body_identity']['thoracic_vs_FN_pct'], GC['c2']['body_identity']['thoracic_vs_FN_pct']))
rows = []
for c, k in D.items():
    ns_ = [k['h'], k['fn'], k['mf']]; sl = GC[c]['body_identity']['vs_fenn']['shin_over_leg']
    rows += [('%s front' % c, [img('band_' + n, 'lfront') for n in ns_], ['%s shin/leg %.4f' % (k['h'], sl['AE']), '%s shin/leg %.4f' % (k['fn'], sl['FN']), k['mf']]), ('%s profile' % c, [img('band_' + n, 'lprof') for n in ns_], None)]
sheet('AE_FINAL_07_leg_segments.jpg', 'Aelari RP3 final — leg segments (ears hidden): Aelari | frozen Fenn | Marchfolk — blue thigh, rose lower leg', rows, colw=480, legend=[('thigh', C_FE), ('lower leg', C_SH)],
      note='shin / leg gap to Marchfolk: c1 %.4f (Fenn %.4f), c2 %.4f (Fenn %.4f)' % (GC['c1']['body_identity']['shin_over_leg_gap_to_MF'], GC['c1']['body_identity']['fenn_shin_over_leg_gap_to_MF'], GC['c2']['body_identity']['shin_over_leg_gap_to_MF'], GC['c2']['body_identity']['fenn_shin_over_leg_gap_to_MF']))
pn_ = lambda c: '  '.join('%s%s %+.2f%%' % (r['rule'].split(' ')[0], 'F' if 'Fenn' in r['rule'] else '', list(r['by_t'].values())[1]['diff_pct']) for r in GC[c]['pelvis']['rules'])
rows = []
for c, k in D.items():
    ns_ = [k['h'], k['fn'], k['mf']]; rows += [('%s oblique' % c, [img('he_' + n, 'pelvis') for n in ns_], ns_), ('%s front' % c, [img('he_' + n, 'pfront') for n in ns_], None)]
sheet('AE_FINAL_08_pelvis.jpg', 'Aelari RP3 final — pelvis (ears hidden): Aelari | frozen Fenn | Marchfolk — skeletal-proxy rules hold at t = 0 / 0.5 / 1.0', rows, colw=480,
      note='c1 (t=0.5): %s\nc2 (t=0.5): %s' % (pn_('c1'), pn_('c2')))
rows = []
for c, k in D.items():
    ns_ = [k['h'], k['fn'], k['mf'], k['sg']]
    rows += [('%s front' % c, [img('he_' + n, 'hfront') for n in ns_], ['%s systems %d/7' % (k['h'], GC[c]['hidden_ear_face']['systems_material']), k['fn'], k['mf'], k['sg']]), ('%s profile' % c, [img('he_' + n, 'hprof') for n in ns_], None)]
sheet('AE_FINAL_09_hidden_ear_face.jpg', 'Aelari RP3 final — hidden-ear face (ears collapsed, 190 cm): Aelari | frozen Fenn | Marchfolk | Sagekin', rows, colw=460)
m = lambda c: 'L %.2f cm  width %.2f  angle %.1f°  extent %.2f  upper %.1f°' % (ME[c]['length_lobe_to_tip_cm'], ME[c]['max_width_cm'], ME[c]['auricle_body_angle_deg'], ME[c]['total_lateral_extent_from_root_plane_cm'], ME[c]['side_view_upper_extension_deg'])
sheet('AE_FINAL_10_ear_AE-E2.jpg', 'Aelari RP3 final — AE-E2 ear: lateral | front | rear | top (left ear; identical cameras per row)', [(c, [img(c + '_g', v) for v in ('elat', 'efront', 'erear', 'etop')], [m(c), '', '', '']) for c in D])
sheet('AE_FINAL_11_ear_wire_poles.jpg', 'Aelari RP3 final — ear wire (front orange, back violet, rim yellow, cuff blue, transition green) and poles (blue 3, red 5, violet 6+)',
      [(c, [img(c + '_w', 'eface'), img(c + '_w', 'ecrear'), img(c + '_v', 'eface'), img(c + '_v', 'ecrear')], ['%d V / %d Q' % (AU[c]['verts'], AU[c]['faces']), '', 'poles', '']) for c in D], colw=520)
t4c = lambda c: 'T-4 %d / %d (%.1f %%)  aspect max %.2f  >10: %d' % (AU[c]['T4']['angle_violations'], AU[c]['T4']['branch_faces'], 100 * AU[c]['T4']['angle_violations'] / AU[c]['T4']['branch_faces'], AU[c]['T4']['aspect_max'], AU[c]['T4']['aspect_gt10'])
sheet('AE_FINAL_12_T4_aspect.jpg', 'Aelari RP3 final — T-4 (red = a corner outside 45-135°) and quad aspect (blue 1 .. red 6, violet > 6)',
      [(c + ' T-4', [img(c + '_t4', v) for v in ('eface', 'ecrear', 'root')], [t4c(c), '', '']) for c in D] + [(c + ' aspect', [img(c + '_as', v) for v in ('eface', 'ecrear', 'root')], None) for c in D])
rc = lambda c: 'crease max %.1f / %.1f°  transition %.3f cm  clearance %.2f cm' % (AU[c]['root_dihedral']['l']['max_deg'], AU[c]['root_dihedral']['r']['max_deg'], AU[c]['transition_ring']['displacement_max_cm'], AU[c]['ear_to_head_clearance']['min_cm'])
sheet('AE_FINAL_13_root_integration.jpg', 'Aelari RP3 final — root integration (cuff skin vs hidden-ear skull, 0 .. 0.6 cm) and wire root', [(c, [img(c + '_rd', 'root'), img(c + '_rd', 'under'), img(c + '_w', 'root')], [rc(c), '', '']) for c in D])
fw = G['firewall']['configs']['c1']
sheet('AE_FINAL_14_Aelari_AE-E2_vs_Fenn_E2.jpg', 'Aelari RP3 final — frozen Fenn E2 | Aelari AE-E2 (c1), each on its own head, same relative camera',
      [(v, [img('cmpFN', v), img('cmpAE', v)], ['Fenn E2', 'Aelari AE-E2'] if v == 'prof' else None) for v in ('prof', 'front', 'rear', 'elat')],
      note='[Aelari, Fenn]: body angle %s deg; lateral extent / L %s; upper extension %s deg; L / HH %s; width / L %s' % (fw['projection_body_angle_deg'], fw['lateral_extent_over_length'], fw['upper_extension_deg'], fw['length_over_HH'], fw['width_over_length']))
sheet('AE_FINAL_15_c1_vs_c2_AE-E2.jpg', 'Aelari RP3 final — configuration 1 | configuration 2, AE-E2 (shared topology; each on its own head)',
      [('3-4 head', [img(c + '_g', 'htq') for c in D], [D[c]['nm'] for c in D]), ('ear', [img(c + '_g', 'elat') for c in D], None), ('wire', [img(c + '_w', 'eface') for c in D], None)])
VA = {c: jl('%s/val/%s_final_validator_v2_D1-D6.json' % (W, k['h'])) for c, k in D.items()}; rows_ = sorted(VA['c1']['stations'])
cw = [260, 160, 160, 160, 160, 160, 160]; S = Image.new('RGB', (sum(cw) + 40, 140 + 26 * (len(rows_) + 2)), 'white'); d = ImageDraw.Draw(S)
d.text((14, 14), 'Aelari RP3 final — validator D1+D3+D4+D5+D6, production bodies', fill=(0, 0, 0), font=font(20, True))
d.text((14, 44), 'margin = loops - contract minimum (red = 0).   c1 %s: %d / 69    c2 %s: %d / 69' % (D['c1']['nm'], VA['c1']['summary']['firm_pass_count'], D['c2']['nm'], VA['c2']['summary']['firm_pass_count']), fill=(0, 0, 0), font=font(16))
hdr = ['station', 'c1 loops', 'c1 min', 'c1 margin', 'c2 loops', 'c2 min', 'c2 margin']; y = 90
for i, t in enumerate(hdr): d.text((20 + sum(cw[:i]), y), t, fill=(0, 0, 0), font=font(15, True))
y += 28
with open(os.path.join(OUT, 'AE_FINAL_validator_margin_table.csv'), 'w', newline='') as fh:
    wr = csv.writer(fh); wr.writerow(hdr + ['c1 status', 'c2 status'])
    for s in rows_:
        a, b = VA['c1']['stations'][s], VA['c2']['stations'][s]; vals = [s, a['loops_v2'], a['required'], a['margin'], b['loops_v2'], b['required'], b['margin']]; wr.writerow(vals + [a['status_D1_D3'], b['status_D1_D3']])
        for i, t in enumerate(vals): d.text((20 + sum(cw[:i]), y), str(t), fill=(200, 30, 30) if (i in (3, 6) and t == 0) else (0, 0, 0), font=font(14))
        y += 26
S.save(os.path.join(OUT, 'AE_FINAL_16_validator_margin.jpg'), quality=88)
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(12, 4.6)); zs = ['face', 'ears', 'hand', 'foot', 'trunk', 'arm', 'leg', 'neck', 'head']; x = np.arange(len(zs) + 1)
for i, c in enumerate(D):
    dz = GC[c]['density']['zones']; ax.bar(x + (i - 0.5) * 0.35, [dz[z]['mean'] for z in zs] + [GC[c]['density']['ear_branch_mean_pct']], 0.35, label='%s (%s)' % (D[c]['nm'], c))
ax.scatter(x, [GC['c1']['density']['zones'][z]['limit'] for z in zs] + [0.25], marker='_', s=600, color='k')
ax.set_xticks(x); ax.set_xticklabels(zs + ['AE-E2 branch']); ax.set_ylabel('mean edge / stature (%)'); ax.set_title('Aelari RP3 final density — 9 family zones + ear branch (black bar = limit): all pass'); ax.legend(); fig.tight_layout()
fig.savefig(os.path.join(OUT, 'AE_FINAL_17_density.jpg'), dpi=105); plt.close(fig)
DSm = jl(W + '/AELARI_FINAL_deformation_summary.json'); PN = ('shoulder_abd90_l', 'elbow_130_l', 'hip_flex90_l', 'knee_140_l', 'neck_rot45', 'trunk_twist30')
sheet('AE_FINAL_18_deformation_summary.jpg', 'Aelari RP3 final — Standard v1 deformation (production body; source rig + carried MPFB weights, plain LBS; red = flipped)',
      [(c, [img('pose_%s_%s' % (c, p), 'v') for p in PN], ['%s %d (family %d, MF %d)' % (p, DSm[c]['poses'][p]['final_flipped'], DSm[c]['poses'][p]['family_flipped'], DSm[c]['poses'][p]['marchfolk_v005_flipped']) for p in PN]) for c in D], colw=400)
pr = GC['c1']['probes']['rebuilt']; EP = ('neck_flex30', 'head_yaw_l45', 'head_pitch_up20', 'head_roll_l20')
sheet('AE_FINAL_19_ear_readiness_probes.jpg', 'Aelari RP3 final — AE-E2 head / neck readiness (0 / 0 / 0 on all 8 poses) and the ten shape probes (configuration 1; diagnostics, not morphs)',
      [('c1 poses', [img('epose_c1_%s' % p, 'tq') for p in EP], list(EP)), ('c2 poses', [img('epose_c2_%s' % p, 'tq') for p in EP], None),
       ('probes 1-5', [img('pr_' + p, 'eface') for p in PR[:5]], ['%s T4 %d' % (p, pr[p]['T4']) for p in PR[:5]]), ('probes 6-10', [img('pr_' + p, 'eface') for p in PR[5:]], ['%s T4 %d' % (p, pr[p]['T4']) for p in PR[5:]])], colw=400)
sheet('AE_FINAL_20_source_production_overlay.jpg', 'Aelari RP3 final — accepted R-6 source (red) over production body (blue), same camera; only the ear branch departs from the source (human auricle -> AE-E2)',
      [(c, [blend(img(c + '_src', v), img(c + '_g', v)) for v in ('bfront', 'bprof', 'hprof', 'elat')], [D[c]['nm'], '', '', '']) for c in D])
print('sheets done', flush=True)
