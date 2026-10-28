# va_ear_sheets.py WORK EVIDIR OUTDIR : Vael ear-prototype order §18 visual package (22 sheets, VA_EAR_01..22). Identical orthographic cameras per
# configuration (the VA-E2 head camera of that configuration), true scale. Workbench renders (grask_rigprep_v001/render_attr.py) composed with PIL;
# resumable (skips finished renders); 2 Blender processes. Frozen Fenn E2 / Aelari AE-E2 renders use the same relative (head-height) camera.
import sys, os, json, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
from concurrent.futures import ThreadPoolExecutor
os.environ.setdefault('EAR_TOPO', 'v002')
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001')
import ear_branch_lib as E
W, EV, OUT = sys.argv[1:4]; os.makedirs(OUT, exist_ok=True); TMP = os.environ.get('VA_SHEET_TMP', '/tmp/claude-0/rt/va/sheet_r'); os.makedirs(TMP, exist_ok=True)
BP = '/home/claude/stc/bin/python3'; REND = '/home/claude/wayfarer-design/tools/rac/rp/grask_rigprep_v001/render_attr.py'; CF = '/tmp/claude-0/rt/vf/prod'
GREY = np.array([0.80, 0.78, 0.76]); jl = lambda p: json.load(open(p)); S = jl(EV + '/VAEL_EAR_prototype_summary.json')
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
def valence_cols(z):
    Q = z['Q']; Eu = np.unique(np.sort(np.concatenate([Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]]), 1), axis=0); val = np.zeros(len(z['V']), int); np.add.at(val, Eu.ravel(), 1)
    C = part_cols(z) * 0.35 + 0.6; br = z['part'] != 'v005'; C[br & (val == 3)] = [0.1, 0.3, 0.95]; C[br & (val == 5)] = [0.95, 0.15, 0.1]; C[br & (val >= 6)] = [0.6, 0.1, 0.8]; return C, val
Lo = E.canonical_layout(); st = Lo['st']; ns = len(st)
ANAT = [('helix', 'helix', (0.85, 0.30, 0.25)), ('antihelix_stem', 'antihelix stem', (0.20, 0.55, 0.85)), ('superior_crus', 'superior crus', (0.10, 0.35, 0.75)),
        ('inferior_crus', 'inferior crus', (0.35, 0.70, 0.95)), ('triangular_fossa', 'triangular fossa', (0.55, 0.40, 0.80)), ('cavum', 'concha cavum', (0.95, 0.65, 0.15)),
        ('cymba', 'concha cymba', (0.95, 0.85, 0.30)), ('crus_of_helix', 'crus of helix', (0.60, 0.25, 0.10)), ('tragus', 'tragus', (0.20, 0.70, 0.35)),
        ('antitragus', 'antitragus', (0.10, 0.50, 0.25)), ('intertragic_notch', 'intertragic notch', (0.95, 0.40, 0.70))]
EXTRA = [('lobe', (0.93, 0.72, 0.72)), ('upper extension / taper', (0.86, 0.80, 0.62)), ('cuff', (0.72, 0.80, 0.88))]
def anat_cols(z, rec):
    p = dict(rec['params']); p['taper'] = tuple(p['taper']); p['helix'] = tuple(p['helix']); _, _, parts = E.relief(st[:, 0], st[:, 1], p)
    C = np.tile(GREY, (len(z['V']), 1)); C[z['part'] == 'cuff'] = EXTRA[2][1]; lab = np.full(ns, -1); best = np.zeros(ns)
    for k, (key, nm, col) in enumerate(ANAT):
        a = np.abs(parts[key]) / (np.abs(parts[key]).max() + 1e-9); m = (a > 0.35) & (a > best); lab[m] = k; best[m] = a[m]
    sh = np.isin(Lo['part'], ['front', 'rim'])
    for sd in ('l', 'r'):
        f = np.nonzero(z['side'] == sd)[0][0]; idx = np.arange(ns)
        C[f + idx[sh & (st[:, 0] < 0.15) & (lab < 0)]] = EXTRA[0][1]; C[f + idx[sh & (st[:, 0] > E.S_UP) & (lab < 0)]] = EXTRA[1][1]
        for k, (key, nm, col) in enumerate(ANAT): C[f + idx[sh & (lab == k)]] = col
    return C
def thick_cols(z):                                            # front-to-back cartilage + skin thickness per sheet vertex (front vertex and its back twin)
    C = np.tile(GREY, (len(z['V']), 1)); pf = Lo['part'][:ns] == 'front'; pb = Lo['part'][:ns] == 'back'
    key = {(round(float(st[v, 0]), 9), round(float(st[v, 1]), 9)): v for v in np.nonzero(pb)[0]}
    for sd in ('l', 'r'):
        f = np.nonzero(z['side'] == sd)[0][0]; X = z['V'][f:f + ns]
        for v in np.nonzero(pf)[0]:
            w = key.get((round(float(st[v, 0]), 9), round(float(st[v, 1]), 9)))
            if w is None: continue
            t = np.linalg.norm(X[v] - X[w]); C[f + v] = heat(np.array([t]), 0.10, 0.50)[0]; C[f + w] = C[f + v]
    return C
def hcam(V):
    hv = V[V[:, 2] > V[:, 2].max() - 25]; return np.array([0.0, hv[:, 1].mean(), V[:, 2].max() - 12.0])
def bcam(V):
    return np.array([0.0, V[:, 1].mean(), (V[:, 2].max() + V[:, 2].min()) / 2]), (V[:, 2].max() - V[:, 2].min()) / 2 + 6
HEADS = {'c1': 'VAL4-R1-VD2-VF2', 'c2': 'VALF178-R1-VD2-VF2'}; CANDS = ['VA-E1', 'VA-E2', 'VA-E3']; ED = {}
for c, h in HEADS.items():
    for k in CANDS:
        P = '%s/build/%s_%s_branch.npz' % (W, h, k); ED[(c, k)] = (np.load(P), jl(P.replace('.npz', '.json')), P)
CAM = {}
for c in HEADS:
    z, r, P = ED[(c, 'VA-E2')]; V = z['V']; CAM[c] = dict(H=hcam(V), Ce=V[z['side'] == 'l'].mean(0), O=np.array(r['sides']['l']['frame']['O']))
VIEW = dict(front=((0, 1, 0.03), 'H', 15), prof=((1, 0, 0), 'H', 15), tqf=((1, 1, 0.1), 'H', 15), rear=((0, -1, 0), 'H', 15), tqr=((1, -1, 0.1), 'H', 15), top=((0, 0, 1), 'H', 15),
            elat=((1, 0.15, 0.05), 'Ce', 5.6), eface=((1, 0.9, 0.15), 'Ce', 5.2), ecrear=((0.35, -1, 0.1), 'Ce', 5.2), root=((1, 0.2, 0.0), 'O', 3.6), under=((0.3, -0.5, -1), 'Ce', 3.8))
def views(c, names): return [(n, VIEW[n][0], CAM[c][VIEW[n][1]], VIEW[n][2]) for n in names]
for (c, k), (z, r, P) in ED.items():
    t = '%s_%s' % (c, k)
    render(t + '_g', P, np.tile(GREY, (len(z['V']), 1)), views(c, ['front', 'prof', 'tqf', 'rear', 'tqr', 'top', 'elat', 'eface', 'ecrear', 'root']))
    render(t + '_w', P, part_cols(z), views(c, ['eface', 'ecrear', 'root', 'under']), wire=True)
    render(t + '_v', P, valence_cols(z)[0], views(c, ['eface', 'ecrear']), wire=True)
    render(t + '_a', P, anat_cols(z, r), views(c, ['eface', 'elat']))
    render(t + '_th', P, thick_cols(z), views(c, ['eface', 'ecrear']))
    q = np.load('%s/audit/%s_%s_audit_perface.npz' % (W, HEADS[c], k)); F_, bad, asp = q['faces'], q['ang_bad'], q['asp']
    C = face_part(z) * 0.45 + 0.5; C[F_] = [0.93, 0.93, 0.93]; C[F_[bad]] = [0.92, 0.18, 0.12]; render(t + '_t4', P, C, views(c, ['eface', 'ecrear', 'root']), wire=True)
    C = np.tile(GREY, (len(z['Q']), 1)); C[F_] = heat(asp, 1.0, 6.0); C[F_[asp > 6]] = [0.55, 0.1, 0.65]; render(t + '_as', P, C, views(c, ['eface', 'ecrear']), wire=True)
    d = np.load('%s/audit/%s_%s_audit_cuffdev.npy' % (W, HEADS[c], k)); C = np.tile(GREY, (len(z['V']), 1)); C[d[:, 0].astype(int)] = heat(d[:, 1], 0, 0.6); render(t + '_rd', P, C, views(c, ['root', 'under']))
# full body with VA-E2 (context) and hidden-ear head
for c, h in HEADS.items():
    z, r, P = ED[(c, 'VA-E2')]; Bc, hs = bcam(z['V']); render('%s_body' % c, P, np.tile(GREY, (len(z['V']), 1)), [('front', (0, 1, 0), Bc, hs), ('tqf', (1, 1, 0.05), Bc, hs)], px=700)
    he = '%s/ov/%s_earhidden.npz' % (CF, h); zh = np.load(he); Vh = zh['V']; render('%s_hidden' % c, he, np.tile(GREY, (len(Vh), 1)), [('prof', (1, 0, 0), hcam(Vh), 15), ('front', (0, 1, 0.03), hcam(Vh), 15)])
    # outside-branch displacement heat vs the VF2 family body (0 everywhere outside the branch; transition ring shown)
    fz = np.load('%s/fam/%s_fam.npz' % (CF, h)); m5 = np.asarray(z['v005_to_branch']); kept = np.nonzero(m5 >= 0)[0]; dd = np.zeros(len(z['V'])); dd[m5[kept]] = np.linalg.norm(z['V'][m5[kept]] - fz['V'][kept], axis=1)
    C = heat(dd, 0, 0.1); C[(z['part'] != 'v005') & (z['part'] != 'transition')] = [0.85, 0.85, 0.85]; render('%s_disp' % c, P, C, views(c, ['prof', 'front']))
    for pn in ('neck_flex30', 'neck_ext30', 'head_yaw_l45', 'head_yaw_r45', 'head_pitch_down20', 'head_pitch_up20', 'head_roll_l20', 'head_roll_r20'):
        pp = '%s/deform/%s_VA-E2_%s.npy' % (W, h, pn); X = np.load(pp); q = os.path.join(TMP, 'epose_%s_%s.npz' % (c, pn)); np.savez_compressed(q, V=X, Q=z['Q'])
        render('epose_%s_%s' % (c, pn), q, part_cols(z), [('tq', (1, 0.3, 0.1), X[z['side'] == 'l'].mean(0), 8.0)], px=420)
# frozen Fenn E2 / Aelari AE-E2 on their own heads, same relative camera
FZ = {'FN_c1': '/tmp/claude-0/rt/fn/final/ear/build/FNL4-CF2_E2_branch.npz', 'FN_c2': '/tmp/claude-0/rt/fn/final/ear/build/FNF181-CF2_E2_branch.npz',
      'AE_c1': '/tmp/claude-0/rt/ae/final/ear/build/AEL1-R1_AE-E2_branch.npz', 'AE_c2': '/tmp/claude-0/rt/ae/final/ear/build/AELF190-R1_AE-E2_branch.npz'}
for tag, P in list(FZ.items()) + [('VA_c1', ED[('c1', 'VA-E2')][2]), ('VA_c2', ED[('c2', 'VA-E2')][2])]:
    z = np.load(P); V = z['V']; Hc = hcam(V); Ce = V[z['side'] == 'l'].mean(0)
    render('cmp_' + tag, P, np.tile(GREY, (len(V), 1)), [('prof', (1, 0, 0), Hc, 15), ('front', (0, 1, 0.03), Hc, 15), ('rear', (0, -1, 0), Hc, 15), ('top', (0, 0, 1), Hc, 15), ('elat', (1, 0.15, 0.05), Ce, 6.0)])
PR = ['proj_m10', 'proj_p10', 'tilt_m8', 'tilt_p8', 'sweep_m06', 'sweep_p06', 'len_m10', 'len_p10', 'tip_blunt', 'tip_sharp', 'wb_m8', 'wb_p8']
for pn in PR:
    P = '%s/probe/%s/%s_VA-E2_branch.npz' % (W, pn, HEADS['c1']); z = np.load(P); render('pr_' + pn, P, part_cols(z), views('c1', ['eface']), wire=True, px=420); render('prg_' + pn, P, np.tile(GREY, (len(z['V']), 1)), views('c1', ['front']), px=420)
print('render jobs', len(jobs), flush=True)
done_ = lambda j: all(os.path.exists(os.path.join(TMP, '%s_%s.png' % (j[6], v_.split(':')[0]))) for v_ in j[7].split(';'))
todo = [j for j in jobs if not done_(j)]; print('to render', len(todo), flush=True)
with ThreadPoolExecutor(int(os.environ.get('VA_SHEET_THREADS', '2'))) as ex: list(ex.map(lambda j: subprocess.run(j, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL), todo))
# ---------------------------------------------------------------- compose
def sheet(fname, title, rows, colw=600, note=None, lab_w=170, legend=None):
    ncol = max(len(r_[1]) for r_ in rows); Wd = lab_w + ncol * colw; Hh = 70 + sum(colw + 34 for _ in rows) + (44 if note else 0) + (44 if legend else 0)
    Sh = Image.new('RGB', (Wd, Hh), 'white'); d = ImageDraw.Draw(Sh); d.text((14, 14), title, fill=(0, 0, 0), font=font(21, True)); y = 70
    for lab, ims, caps in rows:
        d.text((10, y + colw // 2), lab, fill=(0, 0, 0), font=font(17, True))
        for k_, im in enumerate(ims):
            Sh.paste(im.resize((colw, colw)), (lab_w + k_ * colw, y))
            if caps and k_ < len(caps) and caps[k_]: d.text((lab_w + 6 + k_ * colw, y + colw + 4), caps[k_], fill=(30, 30, 30), font=font(14))
        y += colw + 34
    if legend:
        x = 14
        for nm, col in legend:
            d.rectangle((x, y + 10, x + 24, y + 30), fill=tuple(int(255 * v) for v in col)); d.text((x + 30, y + 10), nm, fill=(0, 0, 0), font=font(14)); x += 40 + 9 * len(nm)
        y += 44
    if note: d.text((14, y + 4), note, fill=(60, 60, 60), font=font(15))
    Sh.save(os.path.join(OUT, fname), quality=88)
RZ = S['realizations']; K = lambda c, k: '%s_%s' % (HEADS[c], k)
def cap(c, k):
    m = RZ[K(c, k)]['measure']; return '%s %s  L/HH %.3f  angle %.0f°  w/L %.2f  T-4 %d' % (c, k, m['length_over_HH'], m['body_angle_deg'], m['max_width_over_length'], RZ[K(c, k)]['T4'])
def multi(fname, title, tagsuf, view, **kw):
    rows = []
    for c in HEADS: rows.append((c, [img('%s_%s_%s' % (c, k, tagsuf), view) for k in CANDS], [cap(c, k) for k in CANDS]))
    sheet(fname, title, rows, **kw)
CN = 'VA-E1 restrained | VA-E2 balanced central | VA-E3 stronger'
multi('VA_EAR_01_front.jpg', 'Vael ears — front (%s); c1 / c2, same camera per configuration' % CN, 'g', 'front')
multi('VA_EAR_02_rear.jpg', 'Vael ears — rear (%s)' % CN, 'g', 'rear')
multi('VA_EAR_03_profile.jpg', 'Vael ears — profile (%s)' % CN, 'g', 'prof')
multi('VA_EAR_04_three_quarter_front.jpg', 'Vael ears — 3/4 front (%s)' % CN, 'g', 'tqf')
multi('VA_EAR_05_three_quarter_rear.jpg', 'Vael ears — 3/4 rear (%s)' % CN, 'g', 'tqr')
multi('VA_EAR_06_top.jpg', 'Vael ears — top (%s)' % CN, 'g', 'top')
multi('VA_EAR_07_close_profile.jpg', 'Vael ears — close profile, left ear (%s)' % CN, 'g', 'elat')
multi('VA_EAR_08_close_rear.jpg', 'Vael ears — close rear / posterior surface, left ear (%s)' % CN, 'g', 'ecrear')
sheet('VA_EAR_09_root_closeup.jpg', 'Vael ears — root closeup (grey | wire, part colours: cuff blue, transition ring green)',
      [('%s %s' % (c, v), [img('%s_%s_%s' % (c, k, 'g' if v == 'grey' else 'w'), 'root') for k in CANDS], [k for k in CANDS]) for c in HEADS for v in ('grey', 'wire')])
sheet('VA_EAR_10_wireframe.jpg', 'Vael ears — wireframe (front sheet orange, back violet, rim yellow, cuff blue, transition green)',
      [('%s %s' % (c, v), [img('%s_%s_w' % (c, k), v) for k in CANDS], CANDS) for c in HEADS for v in ('eface', 'ecrear')])
def pole_cap(c, k):
    z = ED[(c, k)][0]; _, val = valence_cols(z); br = z['part'] != 'v005'; return '%s  poles v3 %d  v5 %d  v6+ %d  root valence-4 %s' % (k, (br & (val == 3)).sum(), (br & (val == 5)).sum(), (br & (val >= 6)).sum(), all(v.get('4', 0) == 52 for v in RZ[K(c, k)]['root_valence'].values()))
sheet('VA_EAR_11_poles_valence.jpg', 'Vael ears — pole / valence map (blue valence 3, red 5, violet 6+); identical counts on every realization (one topology)',
      [('%s %s' % (c, v), [img('%s_%s_v' % (c, k), v) for k in CANDS], [pole_cap(c, k) for k in CANDS] if v == 'eface' else None) for c in HEADS for v in ('eface', 'ecrear')])
sheet('VA_EAR_12_annotated_anatomy.jpg', 'Vael ears — annotated anatomy (dominant W1e relief system per vertex): helix, antihelix + crura, fossa, cymba / cavum, crus, tragus, antitragus, notch, lobe, upper extension',
      [('%s %s' % (c, v), [img('%s_%s_a' % (c, k), v) for k in CANDS], CANDS) for c in HEADS for v in ('eface', 'elat')], legend=[(nm, col) for _, nm, col in ANAT] + EXTRA)
# 13 thickness + sections
subprocess.run(['python3', '/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001/ear_sections.py', W, TMP], env=dict(os.environ, EAR_HEADS='c1:%s,c2:%s' % (HEADS['c1'], HEADS['c2']), EAR_CANDS=','.join(CANDS), EAR_RACE='Vael', EAR_TOPO='v002'), stdout=subprocess.DEVNULL)
def thcap(c, k):
    m = RZ[K(c, k)]['measure']; return '%s  median %.2f  p05 %.2f  upper ext. %.2f cm' % (k, m['thickness_median_cm'], m['thickness_p05_cm'], m['upper_thickness_median_cm'])
sheet('VA_EAR_13a_thickness.jpg', 'Vael ears — cartilage + skin thickness (front vertex to back twin; blue 0.10 .. red 0.50 cm): no paper-thin tip, no knob',
      [('%s %s' % (c, v), [img('%s_%s_th' % (c, k), v) for k in CANDS], [thcap(c, k) for k in CANDS] if v == 'eface' else None) for c in HEADS for v in ('eface', 'ecrear')])
for c in HEADS:
    s_ = os.path.join(TMP, 'FENN_EAR_13b_sections_%s.jpg' % c)
    if os.path.exists(s_): Image.open(s_).convert('RGB').save(os.path.join(OUT, 'VA_EAR_13b_sections_%s.jpg' % c), quality=88)
def t4cap(c, k):
    r = RZ[K(c, k)]; return '%s T-4 %d / %d  asp max %.2f  min ang %.1f°' % (k, r['T4'], r['branch_faces'], r['aspect_max'], r['min_angle'])
sheet('VA_EAR_14_T4_aspect.jpg', 'Vael ears — T-4 (red = corner outside 45-135°) and aspect (blue 1 .. red 6; violet > 6)',
      [('%s %s' % (c, lab), [img('%s_%s_%s' % (c, k, tg), v) for k in CANDS], [t4cap(c, k) for k in CANDS] if lab == 'T-4' else None) for c in HEADS for lab, tg, v in (('T-4', 't4', 'eface'), ('T-4 root', 't4', 'root'), ('aspect', 'as', 'eface'))])
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig, axs = plt.subplots(1, 2, figsize=(14, 4.8)); x = np.arange(3)
for i, c in enumerate(HEADS):
    axs[0].bar(x + (i - 0.5) * 0.35, [RZ[K(c, k)]['density']['branch_mean_edge_pct_stature'] for k in CANDS], 0.35, label=c + ' mean'); axs[0].scatter(x + (i - 0.5) * 0.35, [RZ[K(c, k)]['density']['p95_pct'] for k in CANDS], marker='^', color='k')
axs[0].axhline(0.25, color='r', ls='--', label='limit 0.25 %'); axs[0].set_xticks(x); axs[0].set_xticklabels(CANDS); axs[0].set_ylabel('branch edge / stature (%)  (triangle = p95)'); axs[0].legend(); axs[0].set_title('branch density: mean edge / stature')
fr = jl('/tmp/claude-0/rt/fn/final/ear/audit/FNL4-CF2_E2_audit.json')['density']; ar = jl('/tmp/claude-0/rt/ae/final/ear/audit/AEL1-R1_AE-E2_audit.json')['density']
vals = [RZ[K('c1', k)]['density']['branch_mean_edge_cm'] for k in CANDS] + [fr['branch_mean_edge_cm'], ar['branch_mean_edge_cm']]
axs[1].bar(range(5), vals, color=['#c98', '#c76', '#c54', '#79b', '#9b7']); axs[1].set_xticks(range(5)); axs[1].set_xticklabels(CANDS + ['Fenn E2 (frozen)', 'Aelari AE-E2 (frozen)']); axs[1].set_ylabel('branch mean edge (cm), c1'); axs[1].set_title('same topology; edge scale follows ear size')
fig.suptitle('Vael ears — density (all pass; branch faces per side %d vs v005 ear zone %d)' % (RZ[K('c1', 'VA-E2')]['density']['branch_faces_per_side'], RZ[K('c1', 'VA-E2')]['density']['v005_ear_zone_faces_per_side'])); fig.tight_layout(); fig.savefig(os.path.join(OUT, 'VA_EAR_15_density.jpg'), dpi=110); plt.close(fig)
def rdcap(c, k):
    r = RZ[K(c, k)]; return '%s crease max %.0f°  transition %.3f cm  clearance %.2f cm' % (k, max(v['max_deg'] for v in r['root_dihedral'].values()), r['transition']['displacement_max_cm'], r['clearance']['min_cm'])
sheet('VA_EAR_16_root_deviation.jpg', 'Vael ears — root deviation (cuff skin vs hidden-ear skull, blue 0 .. red 0.6 cm) and underside',
      [('%s %s' % (c, v), [img('%s_%s_rd' % (c, k), v) for k in CANDS], [rdcap(c, k) for k in CANDS] if v == 'root' else None) for c in HEADS for v in ('root', 'under')])
sheet('VA_EAR_17_VF2_VC2_head_with_ears.jpg', 'Accepted Vael VF2 body + VC2 head with VA-E2 (full character) and VA-E1 / VA-E2 / VA-E3 on the head (3/4 front)',
      [(c, [img('%s_body' % c, 'front'), img('%s_body' % c, 'tqf')] + [img('%s_%s_g' % (c, k), 'tqf') for k in CANDS], ['VF2 + VC2 + VA-E2', '3/4'] + CANDS) for c in HEADS], colw=520)
sheet('VA_EAR_18_c1_vs_c2_VA-E2.jpg', 'Vael VA-E2 — configuration 1 | configuration 2 (one topology, one parameter set; head scale / root frame only)',
      [(v, [img('c1_VA-E2_g', v), img('c2_VA-E2_g', v)], ['c1 %s' % HEADS['c1'], 'c2 %s' % HEADS['c2']] if v == 'tqf' else None) for v in ('tqf', 'prof', 'elat')] + [('wire', [img('c1_VA-E2_w', 'eface'), img('c2_VA-E2_w', 'eface')], None)])
FW = S['firewall']
def fwcap(nm, c):
    m = FW[c]['frozen'][nm] if nm != 'Vael VA-E2' else FW[c]['vael']['VA-E2']['vael']
    return '%s  angle %.0f°  w/L %.2f  tip-up/HH %.3f  chord %.0f°' % (nm, m['body_angle_deg'], m['max_width_over_length'], m['tip_above_root_over_HH'], m['side_view_chord_deg'])
rows = []
for c in HEADS:
    for v in ('prof', 'front', 'rear', 'elat'):
        rows.append(('%s %s' % (c, v), [img('cmp_FN_' + c, v), img('cmp_VA_' + c, v), img('cmp_AE_' + c, v)], [fwcap(n, c) for n in ('Fenn E2', 'Vael VA-E2', 'Aelari AE-E2')] if v == 'prof' else None))
sheet('VA_EAR_19_three_elf_ears.jpg', 'Three-elf ears — frozen Fenn E2 | Vael VA-E2 | frozen Aelari AE-E2, each on its own head, same relative camera (head-height scaled)', rows, colw=480)
HR = S['hidden_ear_regression']
sheet('VA_EAR_20_hidden_ear_regression.jpg', 'Hidden-ear VF2 / VC2 regression — hidden-ear head | VA-E2 head | displacement outside the branch vs the VF2 family body (blue 0 .. red 0.1 cm; grey = branch)',
      [(c, [img('%s_hidden' % c, 'prof'), img('%s_VA-E2_g' % c, 'prof'), img('%s_disp' % c, 'prof'), img('%s_disp' % c, 'front')],
        ['hidden ear (VF2 + VC2)', 'VA-E2', 'outside branch max %.1e cm' % HR[K(c, 'VA-E2')]['max_displacement_outside_branch_cm'], 'transition ring max %.3f cm' % HR[K(c, 'VA-E2')]['transition_ring_max_cm']]) for c in HEADS], colw=480)
PN = ('neck_flex30', 'neck_ext30', 'head_yaw_l45', 'head_yaw_r45', 'head_pitch_down20', 'head_pitch_up20', 'head_roll_l20', 'head_roll_r20')
dcap = lambda c, p: '%s  %s' % (p, '/'.join(str(x) for x in RZ[K(c, 'VA-E2')]['deform'][p]))
sheet('VA_EAR_21_deformation_readiness.jpg', 'Vael VA-E2 — static head / neck readiness (new branch contacts / flips / root inversions per pose; all 0 / 0 / 0 is a pass)',
      [('%s %d' % (c, i), [img('epose_%s_%s' % (c, p), 'tq') for p in PN[4 * i:4 * i + 4]], [dcap(c, p) for p in PN[4 * i:4 * i + 4]]) for c in HEADS for i in (0, 1)], colw=420)
PB = S['probes']; pcap = lambda p: '%s  T-4 %d  SI %d  %s' % (p, PB[p]['T4'], PB[p]['self_intersection_branch'], 'ok' if PB[p]['moves_intended'] else 'WRONG DIR')
sheet('VA_EAR_22_shape_probes.jpg', 'Vael VA-E2 — geometry-only readiness probes (configuration 1; same topology): wire close + head front',
      [('probes %d-%d' % (i + 1, i + 4), [img('pr_' + p, 'eface') for p in PR[i:i + 4]], [pcap(p) for p in PR[i:i + 4]]) for i in (0, 4, 8)] +
      [('front %d-%d' % (i + 1, i + 6), [img('prg_' + p, 'front') for p in PR[i:i + 6]], PR[i:i + 6]) for i in (0, 6)], colw=420)
print('sheets done', flush=True)
