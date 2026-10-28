# fn_final_sheets.py WORK OUTDIR : order 6d2eadc §15 final visual freeze package (15 sheets; identical orthographic cameras per sheet, true scale).
# WORK = clean-rebuild folder (run_fnfinal.sh / run_fnfinal_eval.sh). Workbench renders (grask_rigprep_v001/render_attr.py), composed with PIL.
import sys, os, json, subprocess, csv, numpy as np
from PIL import Image, ImageDraw, ImageFont
from concurrent.futures import ThreadPoolExecutor
os.environ.setdefault('EAR_TOPO', 'v002')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ear_branch_lib as E
W, OUT = sys.argv[1:3]; os.makedirs(OUT, exist_ok=True); TMP = os.environ.get('FN_SHEET_TMP', os.path.join(OUT, '_r')); os.makedirs(TMP, exist_ok=True)
BP = '/home/claude/stc/bin/python3'; REND = '/home/claude/wayfarer-design/tools/rac/rp/grask_rigprep_v001/render_attr.py'; RA = '/home/claude/wayfarer-design/reviews/reference-assets/r6'
CF = {'c1': ('FNL4-CF2', 'FN_M_REF_RP3_v001'), 'c2': ('FNF181-CF2', 'FN_F_REF_RP3_v001')}
GREY = np.array([0.80, 0.78, 0.76])
def font(sz, bold=False):
    f = '/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf' % ('-Bold' if bold else ''); return ImageFont.truetype(f, sz) if os.path.exists(f) else ImageFont.load_default()
jobs = []
def render(tag, npz, col, views, wire=False, px=640):
    vs = ';'.join('%s:%s:%s:%.2f' % (n, ','.join('%.4f' % x for x in d), ','.join('%.3f' % x for x in c), hs) for n, d, c, hs in views)
    cf = os.path.join(TMP, tag + '_col.npy'); np.save(cf, np.asarray(col, np.float32)); jobs.append([BP, REND, '--', npz, cf, TMP, tag, vs, '1' if wire else '0', str(px)])
def img(tag, name, w=None):
    im = Image.open(os.path.join(TMP, '%s_%s.png' % (tag, name))).convert('RGB'); return im.resize((w, w)) if w else im
def heat(x, lo, hi):
    t = np.clip((x - lo) / (hi - lo + 1e-12), 0, 1)[:, None]; return (1 - t) * np.array([0.2, 0.35, 0.85]) + t * np.array([0.95, 0.25, 0.15])
def part_cols(z):
    p = z['part']; C = np.tile(GREY, (len(z['V']), 1)); C[p == 'front'] = [0.88, 0.66, 0.55]; C[p == 'back'] = [0.70, 0.58, 0.80]; C[p == 'rim'] = [0.95, 0.83, 0.45]
    C[p == 'cuff'] = [0.58, 0.76, 0.92]; C[p == 'transition'] = [0.55, 0.85, 0.55]; return C
def face_part(z):
    p = z['part'][z['Q']]; C = np.tile(GREY, (len(z['Q']), 1))
    for k, col in (('transition', [0.55, 0.85, 0.55]), ('cuff', [0.58, 0.76, 0.92]), ('back', [0.70, 0.58, 0.80]), ('front', [0.88, 0.66, 0.55]), ('rim', [0.95, 0.83, 0.45])): C[(p == k).any(1)] = col
    return C
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
    sheet_ = np.isin(Lo['part'], ['front', 'rim'])
    for sd in ('l', 'r'):
        f = np.nonzero(z['side'] == sd)[0][0]; idx = np.arange(ns)
        C[f + idx[sheet_ & (st[:, 0] < 0.15) & (lab < 0)]] = EXTRA[0][1]; C[f + idx[sheet_ & (st[:, 0] > E.S_UP) & (lab < 0)]] = EXTRA[1][1]
        for k, (key, nm, col) in enumerate(ANAT): C[f + idx[sheet_ & (lab == k)]] = col
    return C, lab
# ---------------------------------------------------------------- data + cameras
D = {}
for c, (h, nm) in CF.items():
    P = '%s/ear/build/%s_E2_branch.npz' % (W, h); z = np.load(P); r = json.load(open('%s/ear/build/%s_E2_branch.json' % (W, h)))
    V = z['V']; Ce = V[z['side'] == 'l'].mean(0); hv = V[V[:, 2] > V[:, 2].max() - 25]; Hc = np.array([0.0, hv[:, 1].mean(), V[:, 2].max() - 11.0]); O = np.array(r['sides']['l']['frame']['O'])
    Bc = np.array([0.0, V[:, 1].mean(), (V[:, 2].max() + V[:, 2].min()) / 2]); D[c] = dict(h=h, nm=nm, P=P, z=z, r=r, Ce=Ce, H=Hc, O=O, B=Bc, stat=V[:, 2].max() - V[:, 2].min())
def views(c, names):
    k = D[c]; S = max(D[x]['stat'] for x in D) / 2 + 4
    T = dict(bfront=((0, 1, 0), k['B'], S), bprof=((1, 0, 0), k['B'], S), brear=((0, -1, 0), k['B'], S), btq=((1, 1, 0.05), k['B'], S),
             hfront=((0, 1, 0.03), k['H'], 14), hprof=((1, 0, 0), k['H'], 14), htq=((1, 1, 0.1), k['H'], 14),
             elat=((1, 0.15, 0.05), k['Ce'], 5.0), efront=((0, 1, 0.02), k['Ce'], 5.0), erear=((0.15, -1, 0.05), k['Ce'], 5.0), etop=((0.1, 0.05, 1), k['Ce'], 5.0),
             eface=((1, 0.9, 0.15), k['Ce'], 4.6), ecrear=((0.35, -1, 0.1), k['Ce'], 4.6), root=((1, 0.2, 0.0), k['O'], 3.4), under=((0.3, -0.5, -1), k['Ce'], 3.6))
    return [(n,) + T[n] for n in names]
for c, k in D.items():
    z = k['z']; P = k['P']; t = c
    render(t + '_g', P, np.tile(GREY, (len(z['V']), 1)), views(c, ['bfront', 'bprof', 'brear', 'btq', 'hfront', 'hprof', 'htq', 'elat', 'efront', 'erear', 'etop']))
    render(t + '_w', P, part_cols(z), views(c, ['eface', 'ecrear', 'root', 'under']), wire=True)
    pf = np.load('%s/ear/audit/%s_E2_audit_perface.npz' % (W, k['h'])); F, bad, asp = pf['faces'], pf['ang_bad'], pf['asp']
    C = face_part(z) * 0.45 + 0.5; C[F] = [0.93, 0.93, 0.93]; C[F[bad]] = [0.92, 0.18, 0.12]; render(t + '_t4', P, C, views(c, ['eface', 'ecrear', 'root']), wire=True)
    C = np.tile(GREY, (len(z['Q']), 1)); C[F] = heat(asp, 1.0, 6.0); C[F[asp > 6]] = [0.55, 0.1, 0.65]; render(t + '_as', P, C, views(c, ['eface', 'ecrear', 'root']), wire=True)
    d = np.load('%s/ear/audit/%s_E2_audit_cuffdev.npy' % (W, k['h'])); C = np.tile(GREY, (len(z['V']), 1)); C[d[:, 0].astype(int)] = heat(d[:, 1], 0, 0.6); render(t + '_rd', P, C, views(c, ['root', 'under']))
    ac, _ = anat_cols(z, k['r']); render(t + '_a', P, ac, views(c, ['eface', 'elat', 'efront']))
    # source -> production overlay: R-6 source (hm08 body, helpers removed) and the production candidate, same cameras
    r6 = np.load('%s/src/%s_r6_regen.npz' % (W, k['h'])); keep = r6['keep']; Fx = r6['F'][keep[r6['F']].all(1)]; sp_ = os.path.join(TMP, 'src_%s.npz' % c); np.savez_compressed(sp_, V=r6['V'], Q=Fx)
    render(t + '_src', sp_, np.tile(GREY, (len(r6['V']), 1)), views(c, ['bfront', 'bprof', 'hprof', 'elat']))
    # hidden-ear (fenn_hidden_ear.py output: v005-free hm08 bodies, ear collapsed) for Fenn CF2 and the matched comparators
    for lab in ([k['h']] + (['MFM181', 'SGM181'] if c == 'c1' else ['MFF181', 'SGF181'])):
        he = np.load('%s/he/%s_earhidden.npz' % (W, lab)); hp = os.path.join(TMP, 'he_%s.npz' % lab); np.savez_compressed(hp, V=he['V'], Q=he['Q'])
        Hh = np.array([0.0, he['V'][he['V'][:, 2] > he['V'][:, 2].max() - 25][:, 1].mean(), he['V'][:, 2].max() - 11.0]); Bh = np.array([0.0, he['V'][:, 1].mean(), (he['V'][:, 2].max() + he['V'][:, 2].min()) / 2])
        render('he_' + lab, hp, np.tile(GREY, (len(he['V']), 1)), [('bfront', (0, 1, 0), Bh, 96), ('bprof', (1, 0, 0), Bh, 96), ('hfront', (0, 1, 0.03), Hh, 14), ('hprof', (1, 0, 0), Hh, 14)])
    # deformation (production candidate, Standard v1 poses): flipped faces red
    for pn in ('shoulder_abd90_l', 'elbow_130_l', 'hip_flex90_l', 'knee_140_l', 'neck_rot45', 'trunk_twist30'):
        pp = '%s/def/%s_%s_final.npz' % (W, pn, k['h'])
        if not os.path.exists(pp): continue
        X = np.load(pp); Xv = X['V']; Cf_ = np.tile(GREY, (len(z['Q']), 1)); fl_ = np.asarray(X['flip']).astype(int).ravel() if 'flip' in X.files else np.zeros(0, int)
        if fl_.dtype == bool or (len(fl_) == len(z['Q'])): fl_ = np.nonzero(fl_)[0]
        Cf_[fl_[fl_ < len(Cf_)]] = [0.92, 0.18, 0.12]; q = os.path.join(TMP, 'pose_%s_%s.npz' % (c, pn)); np.savez_compressed(q, V=Xv, Q=z['Q'])
        Cb = np.array([Xv[:, 0].mean(), Xv[:, 1].mean(), (Xv[:, 2].max() + Xv[:, 2].min()) / 2]); render('pose_%s_%s' % (c, pn), q, Cf_, [('v', (1, 1, 0.05), Cb, D[c]['stat'] / 2 + 8)], px=480)
print('render jobs', len(jobs), flush=True)
done_ = lambda j: all(os.path.exists(os.path.join(TMP, '%s_%s.png' % (j[6], v_.split(':')[0]))) for v_ in j[7].split(';'))
todo = [j for j in jobs if not done_(j)]; print('to render', len(todo), flush=True)
with ThreadPoolExecutor(int(os.environ.get('FN_SHEET_THREADS', '2'))) as ex: list(ex.map(lambda j: subprocess.run(j, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL), todo))
# ---------------------------------------------------------------- compose
def sheet(fname, title, rows, colw=640, note=None, lab_w=170, legend=None):
    ncol = max(len(r_[1]) for r_ in rows); Wd = lab_w + ncol * colw; Hh = 70 + sum(colw + 34 for _ in rows) + (44 if note else 0) + (44 if legend else 0)
    S = Image.new('RGB', (Wd, Hh), 'white'); d = ImageDraw.Draw(S); d.text((14, 14), title, fill=(0, 0, 0), font=font(22, True)); y = 70
    for lab, ims, caps in rows:
        d.text((10, y + colw // 2), lab, fill=(0, 0, 0), font=font(18, True))
        for k_, im in enumerate(ims):
            S.paste(im.resize((colw, colw)), (lab_w + k_ * colw, y))
            if caps and k_ < len(caps) and caps[k_]: d.text((lab_w + 6 + k_ * colw, y + colw + 4), caps[k_], fill=(30, 30, 30), font=font(15))
        y += colw + 34
    if legend:
        x = 14
        for nm, col in legend:
            d.rectangle((x, y + 10, x + 24, y + 30), fill=tuple(int(255 * v) for v in col)); d.text((x + 30, y + 10), nm, fill=(0, 0, 0), font=font(15)); x += 40 + 9 * len(nm)
        y += 44
    if note: d.text((14, y + 4), note, fill=(60, 60, 60), font=font(16))
    S.save(os.path.join(OUT, fname), quality=90)
AU = {c: json.load(open('%s/ear/audit/%s_E2_audit.json' % (W, k['h']))) for c, k in D.items()}; ME = {c: json.load(open('%s/ear/meas/%s_E2_measure.json' % (W, k['h'])))['sides']['l'] for c, k in D.items()}
VA = {c: json.load(open('%s/val/%s_final_validator_v2_D1-D6.json' % (W, k['h']))) for c, k in D.items()}
for c, k in D.items():
    cap = '%s  %s  stature %.1f cm' % (k['nm'], k['h'], k['stat'])
    sheet('FENN_FINAL_%02d_full_body_%s.jpg' % (1 if c == 'c1' else 2, c), 'Fenn RP3 final — configuration %s full body (%s; front | profile | rear | 3-4; same camera both configurations)' % (c[1], k['nm']),
          [(c, [img(c + '_g', v) for v in ('bfront', 'bprof', 'brear', 'btq')], [cap, '', '', ''])], colw=560)
    sheet('FENN_FINAL_%02d_head_%s.jpg' % (3 if c == 'c1' else 4, c), 'Fenn RP3 final — configuration %s head (CF2 + E2 ear v002; front | profile | 3-4)' % c[1],
          [(c, [img(c + '_g', v) for v in ('hfront', 'hprof', 'htq')], [k['h'], '', ''])])
m = lambda c: 'chord %.2f cm  width %.2f  angle %.1f°  extent %.2f  upper axis %.1f°' % (ME[c]['length_lobe_to_tip_cm'], ME[c]['max_width_cm'], ME[c]['auricle_body_angle_deg'], ME[c]['total_lateral_extent_from_root_plane_cm'], ME[c]['side_view_upper_extension_deg'])
sheet('FENN_FINAL_05_ear_E2.jpg', 'Fenn RP3 final — E2 ear (topology v002): lateral | front | rear | top (left ear; identical cameras per row)',
      [(c, [img(c + '_g', v) for v in ('elat', 'efront', 'erear', 'etop')], [m(c), '', '', '']) for c in D])
sheet('FENN_FINAL_06_ear_wire.jpg', 'Fenn RP3 final — ear wire (front orange, back violet, rim yellow, cuff blue, transition green)',
      [(c, [img(c + '_w', v) for v in ('eface', 'ecrear', 'root', 'under')], ['%d V / %d Q mesh' % (AU[c]['verts'], AU[c]['faces']), '', '', '']) for c in D])
t4c = lambda c: 'T-4 %d / %d (%.1f %%)  aspect max %.2f  >10: %d' % (AU[c]['T4']['angle_violations'], AU[c]['T4']['branch_faces'], 100 * AU[c]['T4']['angle_violations'] / AU[c]['T4']['branch_faces'], AU[c]['T4']['aspect_max'], AU[c]['T4']['aspect_gt10'])
sheet('FENN_FINAL_07_T4_aspect.jpg', 'Fenn RP3 final — T-4 (red = a corner outside 45-135°) and quad aspect (blue 1 .. red 6, violet > 6); accepted v002 residuals',
      [(c + ' T-4', [img(c + '_t4', v) for v in ('eface', 'ecrear', 'root')], [t4c(c), '', '']) for c in D] + [(c + ' aspect', [img(c + '_as', v) for v in ('eface', 'ecrear', 'root')], None) for c in D])
rc = lambda c: 'root crease max %.1f / %.1f°  transition max %.3f cm  valence 4: %s' % (AU[c]['root_dihedral']['l']['max_deg'], AU[c]['root_dihedral']['r']['max_deg'], AU[c]['transition_ring']['displacement_max_cm'], AU[c]['root_valence'])
sheet('FENN_FINAL_08_root_integration.jpg', 'Fenn RP3 final — root integration (cuff skin vs hidden-ear CF2 skull, 0 .. 0.6 cm) and wire root close-up',
      [(c, [img(c + '_rd', 'root'), img(c + '_rd', 'under'), img(c + '_w', 'root')], [rc(c), '', '']) for c in D])
sheet('FENN_FINAL_09_ear_anatomy.jpg', 'Fenn RP3 final — external-ear anatomy annotation (dominant W1e relief system per vertex; E2)',
      [(c, [img(c + '_a', v) for v in ('eface', 'elat', 'efront')], None) for c in D], legend=[(nm, col) for _, nm, col in ANAT] + EXTRA)
sheet('FENN_FINAL_10_c1_vs_c2_E2.jpg', 'Fenn RP3 final — configuration 1 | configuration 2, E2 ear (shared topology; each on its CF2 head)',
      [('3-4 head', [img(c + '_g', 'htq') for c in D], [D[c]['nm'] for c in D]), ('ear', [img(c + '_g', 'elat') for c in D], None), ('wire', [img(c + '_w', 'eface') for c in D], None)])
HE = json.load(open('%s/he/FN_hidden_ear_identity_CF2.json' % W))
for c, k in D.items():
    labs = [k['h']] + (['MFM181', 'SGM181'] if c == 'c1' else ['MFF181', 'SGF181'])
    sheet('FENN_FINAL_11_hidden_ear_body_%s.jpg' % c, 'Fenn RP3 final — hidden-ear BODY comparison, configuration %s (ear collapsed; matched stature ~181 cm): Fenn | Marchfolk | Sagekin' % c[1],
          [('front', [img('he_' + l, 'bfront') for l in labs], labs), ('profile', [img('he_' + l, 'bprof') for l in labs], None)], colw=520)
    sheet('FENN_FINAL_12_hidden_ear_face_%s.jpg' % c, 'Fenn RP3 final — hidden-ear FACE comparison, configuration %s (ear collapsed): Fenn CF2 | Marchfolk | Sagekin' % c[1],
          [('front', [img('he_' + l, 'hfront') for l in labs], labs), ('profile', [img('he_' + l, 'hprof') for l in labs], None)])
# 13 validator / margin table
rows_ = sorted(VA['c1']['stations'].keys())
def stv(c, s):
    x = VA[c]['stations'][s]; return x
cw = [260, 170, 170, 170, 170, 170, 170]; Wd = sum(cw) + 40; Hh = 140 + 26 * (len(rows_) + 2)
S = Image.new('RGB', (Wd, Hh), 'white'); d = ImageDraw.Draw(S)
d.text((14, 14), 'Fenn RP3 final — validator D1+D3+D4+D5+D6, production bodies', fill=(0, 0, 0), font=font(20, True))
d.text((14, 44), 'margin = loops - contract minimum (red = 0).   c1 %s: %d / %d firm PASS    c2 %s: %d / %d firm PASS' % (D['c1']['nm'], VA['c1']['summary']['firm_pass_count'], VA['c1']['summary']['stations'], D['c2']['nm'], VA['c2']['summary']['firm_pass_count'], VA['c2']['summary']['stations']), fill=(0, 0, 0), font=font(17))
hdr = ['station', 'c1 loops', 'c1 min', 'c1 margin', 'c2 loops', 'c2 min', 'c2 margin']; x = 20; y = 90
for i, t in enumerate(hdr): d.text((x + sum(cw[:i]), y), t, fill=(0, 0, 0), font=font(16, True))
y += 28
def g(x_, *ks):
    for k_ in ks:
        if k_ in x_: return x_[k_]
    return None
with open(os.path.join(OUT, 'FENN_FINAL_validator_margin_table.csv'), 'w', newline='') as fh:
    wr = csv.writer(fh); wr.writerow(hdr + ['c1 status', 'c2 status'])
    for s in rows_:
        a, b = stv('c1', s), stv('c2', s); la, lb = g(a, 'loops_v2'), g(b, 'loops_v2'); ma, mb = g(a, 'required'), g(b, 'required')
        mga, mgb = g(a, 'margin'), g(b, 'margin'); vals = [s, la, ma, mga, lb, mb, mgb]
        wr.writerow(vals + [g(a, 'status_D1_D3'), g(b, 'status_D1_D3')])
        for i, t in enumerate(vals):
            col = (200, 30, 30) if (i in (3, 6) and t == 0) else (0, 0, 0); d.text((20 + sum(cw[:i]), y), str(t), fill=col, font=font(15))
        y += 26
S.save(os.path.join(OUT, 'FENN_FINAL_13_validator_margin.jpg'), quality=90)
# 14 deformation summary
DS = json.load(open('%s/FENN_FINAL_deformation_summary.json' % W)) if os.path.exists('%s/FENN_FINAL_deformation_summary.json' % W) else None
PN = ('shoulder_abd90_l', 'elbow_130_l', 'hip_flex90_l', 'knee_140_l', 'neck_rot45', 'trunk_twist30')
rows = []
for c in D:
    ims = [img('pose_%s_%s' % (c, pn), 'v') for pn in PN if os.path.exists(os.path.join(TMP, 'pose_%s_%s_v.png' % (c, pn)))]
    caps = ['%s  flips %s (family %s, MF v005 %s)' % (pn, DS[c]['poses'][pn]['final_flipped'], DS[c]['poses'][pn]['family_flipped'], DS[c]['poses'][pn]['marchfolk_v005_flipped']) if DS else pn for pn in PN]
    rows.append((c, ims, caps))
sheet('FENN_FINAL_14_deformation_summary.jpg', 'Fenn RP3 final — Standard v1 deformation (production body, source rig + carried MPFB weights, plain LBS); ear head / neck readiness clean (0 / 0 / 0)', rows, colw=420)
# 15 source -> production overlay (source red, production blue; 50 % blend)
def blend(a, b):
    A = np.asarray(a, float); B_ = np.asarray(b, float); A = A * np.array([1.0, 0.55, 0.55]); B_ = B_ * np.array([0.55, 0.65, 1.0]); return Image.fromarray(np.clip(0.5 * A + 0.5 * B_, 0, 255).astype(np.uint8))
sheet('FENN_FINAL_15_source_production_overlay.jpg', 'Fenn RP3 final — accepted R-6 source (red) over production body (blue), same camera; only the ear branch departs from the source (human auricle -> E2)',
      [(c, [blend(img(c + '_src', v), img(c + '_g', v)) for v in ('bfront', 'bprof', 'hprof', 'elat')], [D[c]['nm'], '', '', '']) for c in D])
print('sheets done', flush=True)
