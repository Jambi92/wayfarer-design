# vd_sheets.py OUTDIR : Vael custom body-deformation order (2026-10-28) §16 visual package, 20 sheets (+ the scope diagnostic GX). Identical orthographic
# cameras per row, true scale (one camera per configuration, centred on the Vael R1 source); ears hidden (hm08 w_ears > 0.05 harmonically collapsed),
# geometry-only grey shading. Workbench renders (grask_rigprep_v001/render_attr.py) composed with PIL / matplotlib; resumable; 2 Blender processes.
# Inputs: VD = /tmp/claude-0/rt/vd (cand/, prod/ = family workspace of the winner VD2, evaluations), R1 = /tmp/claude-0/rt/va2/vc2/r1, PA = Part A
# comparators, EV = evidence folder (OUTDIR/..).
import sys, os, json, subprocess, numpy as np, scipy.sparse as sp
from PIL import Image, ImageDraw, ImageFont
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001'); sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1')
import fn_face_metrics as F
import vael_body_field as VF
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True); EV = os.path.abspath(OUT + '/..'); E_ = os.environ.get
VD = E_('VD_DIR', '/tmp/claude-0/rt/vd'); W2 = VD + '/prod'; PA = E_('VA_PA', '/tmp/claude-0/rt/va/partA'); TMP = VD + '/sheet_r'; os.makedirs(TMP, exist_ok=True)
BP = '/home/claude/stc/bin/python3'; REND = '/home/claude/wayfarer-design/tools/rac/rp/grask_rigprep_v001/render_attr.py'
GREY = np.array([0.80, 0.78, 0.76]); jl = lambda p: json.load(open(p))
CFG = {'c1': dict(P='VAL4-R1', FN='FNM178', AE='AEM178', MF='MFM178', SG='SGM178'), 'c2': dict(P='VALF178-R1', FN='FNF178', AE='AEF178', MF='MFF178', SG='SGF178')}
R6 = {}
for c, K in CFG.items():
    R6['%s_R1' % c] = '/tmp/claude-0/rt/va2/vc2/r1/%s_r6.npz' % K['P']
    for t in ('VD1', 'VD2', 'VD3'): R6['%s_%s' % (c, t)] = '%s/cand/%s-%s_r6.npz' % (VD, K['P'], t)
    for k in ('FN', 'AE', 'MF', 'SG'): R6['%s_%s' % (c, k)] = '%s/cmp/%s_r6.npz' % (PA, K[k])
def font(sz, bold=False):
    f = '/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf' % ('-Bold' if bold else ''); return ImageFont.truetype(f, sz) if os.path.exists(f) else ImageFont.load_default()
nz = np.load('/tmp/claude-0/rt/fn/src/FNL4_native.npz'); Q = np.asarray(nz['Q']); si = nz['src_index']; nV = len(si)
A = sp.coo_matrix((np.ones(4 * len(Q)), (Q[:, :4].ravel(), np.roll(Q, -1, 1).ravel())), shape=(nV, nV)).tocsr(); A = ((A + A.T) > 0).astype(float); deg = np.asarray(A.sum(1)).ravel()
def collapse(V):
    X = V.copy()
    for _ in range(400): X[F.EAR] = (A @ X)[F.EAR] / deg[F.EAR, None]
    return X
def eh(n, V=None):
    p = os.path.join(TMP, 'eh_%s.npz' % n)
    if not os.path.exists(p): np.savez(p, V=collapse(F.load(R6[n])['V'] if V is None else V), Q=Q)
    return p
jobs = []
def render(tag, npz, col, views, wire=False, px=520):
    vs = ';'.join('%s:%s:%s:%.2f' % (n, ','.join('%.4f' % x for x in d), ','.join('%.3f' % x for x in c), hs) for n, d, c, hs in views)
    cf = os.path.join(TMP, tag + '_col.npy'); np.save(cf, np.asarray(col, np.float32)); jobs.append([BP, REND, '--', npz, cf, TMP, tag, vs, '1' if wire else '0', str(px)])
def img(tag, name):
    p = os.path.join(TMP, '%s_%s.png' % (tag, name)); return Image.open(p).convert('RGB') if os.path.exists(p) else Image.new('RGB', (600, 600), 'white')
def blend(a, b):
    A_ = np.asarray(a, float); B_ = np.asarray(b, float); bg = A_[2, 2]
    ma = np.abs(A_ - bg).sum(2) > 6; mb = np.abs(B_ - bg).sum(2) > 6; O = np.full_like(A_, 255.0)
    both = ma & mb; O[both] = 0.5 * (A_[both] + B_[both]); O[ma & ~mb] = [215, 40, 30]; O[mb & ~ma] = [40, 80, 215]; return Image.fromarray(np.clip(O, 0, 255).astype(np.uint8))
def heat(x, lo, hi):
    t = np.clip((x - lo) / (hi - lo + 1e-12), 0, 1)[:, None]; return (1 - t) * np.array([0.2, 0.35, 0.85]) + t * np.array([0.95, 0.25, 0.15])
# region membership (native vertices) of the field, from the parts on the R1 rest mesh
REGC = {'rib': [0.95, 0.55, 0.20], 'flank': [0.30, 0.70, 0.75], 'asis': [0.55, 0.40, 0.85], 'clav': [0.90, 0.35, 0.55], 'palm': [0.35, 0.65, 0.35], 'heel': [0.85, 0.75, 0.25]}
spec = jl(VD + '/VD_definitions.json')['definition']
REG = {}
for c, K in CFG.items():
    zr = np.load('/tmp/claude-0/rt/va2/vc2/r1/%s_rest.npz' % K['P']); Wd, Jd, kp, Fd = VF.npz_inputs(zr); _, parts, _ = VF.field(zr['V'], Wd, Jd, kp, Fd, spec, 1.0, return_parts=True)
    REG[c] = {k: (np.linalg.norm(v, axis=1) > 0.2 * np.linalg.norm(v, axis=1).max())[si] for k, v in parts.items()}
# GX diagnostic (outside the order's authorised systems; NOT a candidate): VD2 + elf-family frontal gracility probe (upper side wall + limb envelope)
def gx(c):
    z = np.load(R6['%s_VD2' % c]); W, J, keep, Fz = VF.npz_inputs(z); s = json.loads(json.dumps(spec)); s['rib']['k'] = -0.09; s['flank']['k'] = -0.05
    for k in ('asis', 'clav', 'palm', 'heel'): s[k]['k' if k != 'clav' else 'k_cm'] = 0.0
    D, _ = VF.field(z['V'], W, J, keep, Fz, s, 1.0); V = z['V'] + D - 0.0
    D2 = np.zeros_like(V)
    for b in ('upperarm', 'lowerarm', 'thigh', 'calf'):
        for sd in ('l', 'r'):
            h, t = np.array(J['%s_%s' % (b, sd)][0]), np.array(J['%s_%s' % (b, sd)][1]); ax = t - h; L = np.linalg.norm(ax); ax /= L
            w = W['%s_%s' % (b, sd)] * keep; q = z['V'] - h; tt = q @ ax; rad = q - tt[:, None] * ax; win = VF._ss((tt / L + 0.05) / 0.15) * (1 - VF._ss((tt / L - 0.95) / 0.1))
            D2 += -0.05 * rad * (w * win)[:, None]
    D2 = VF._smooth(D2, VF._edges(Fz, len(V)), len(V), keep, 6); return (V + D2)[si]
CAM = {}
for c, K in CFG.items():
    Vv = np.load(eh('%s_R1' % c))['V']; ym = Vv[:, 1].mean(); j = json.loads(str(np.load(R6['%s_R1' % c])['joints'])); z_ = lambda b: j[b][0][2]
    hc = 0.5 * (np.array(j['hand_l'][0]) + np.array(j['middle_01_l'][0])); fc = 0.5 * (np.array(j['foot_l'][0]) + np.array(j['ball_l'][0])); fc[2] = 5.0
    CAM[c] = dict(B=np.array([0.0, ym, 92.0]), T=np.array([0.0, ym, z_('spine_02') + 4]), S=np.array([0.0, ym, z_('clavicle_l') + 2]), P=np.array([0.0, ym, 0.5 * (z_('pelvis') + z_('spine_01'))]), hand=hc, foot=fc)
BV = lambda c: [('bf', (0, 1, 0), CAM[c]['B'], 96), ('bq', (1, 1, 0.1), CAM[c]['B'], 96), ('bp', (1, 0, 0), CAM[c]['B'], 96)]
RV = lambda c: [('tf', (0, 1, 0), CAM[c]['T'], 26), ('tq', (1, 1, 0.1), CAM[c]['T'], 26), ('sh', (0.2, 1, 0.35), CAM[c]['S'], 17), ('pf', (0, 1, 0), CAM[c]['P'], 22), ('pq', (1, 0.6, 0.05), CAM[c]['P'], 22),
                ('hand', (1, 0.3, 0), CAM[c]['hand'], 9), ('handb', (-0.3, 1, 0.1), CAM[c]['hand'], 9), ('foot', (0.6, 1, 0.5), CAM[c]['foot'], 11), ('heel', (0, -1, 0.15), CAM[c]['foot'], 11)]
HV = lambda c: [('hfront', (0, 1, 0.03), np.array([0.0, CAM[c]['B'][1], 160.0]), 14.5), ('hprof', (1, 0, 0), np.array([0.0, CAM[c]['B'][1], 160.0]), 14.5)]
for c in CFG:
    for k in ('R1', 'VD1', 'VD2', 'VD3', 'MF', 'SG', 'FN', 'AE'):
        n = '%s_%s' % (c, k); V = np.load(eh(n))['V']; render('he_' + n, eh(n), np.tile(GREY, (len(V), 1)), BV(c) + RV(c) + (HV(c) if k in ('R1', 'VD2') else []))
    n = '%s_GX' % c; p_ = eh(n, gx(c)); render('he_' + n, p_, np.tile(GREY, (nV, 1)), BV(c) + RV(c)[:2])
    Va = np.load(eh('%s_VD2' % c))['V']; Vr = np.load(eh('%s_R1' % c))['V']; d = np.linalg.norm(Va - Vr, axis=1)
    render('disp_%s' % c, eh('%s_VD2' % c), heat(d, 0, 0.8), BV(c) + RV(c)[:2])
    C = np.tile(GREY, (nV, 1))
    for k, col in REGC.items(): C[REG[c][k]] = col
    render('reg_%s' % c, eh('%s_VD2' % c), C, BV(c)[:2] + RV(c))
    body = ~F.HEAD & ~F.EAR
    for k in ('MF', 'SG', 'AE', 'FN'):
        Vk = np.load(eh('%s_%s' % (c, k)))['V']; dd = np.linalg.norm(Vk - Va, axis=1); C = np.tile(GREY, (nV, 1)); C[body] = heat(dd[body], 0, 3.0); render('bres_%s_%s' % (c, k), eh('%s_VD2' % c), C, BV(c)[:2])
    dh = np.linalg.norm(Va - Vr, axis=1) * 10; C = np.tile(GREY, (nV, 1)); C[F.HEAD & ~F.EAR] = heat(dh[F.HEAD & ~F.EAR], 0, 1.0); render('fdiff_%s' % c, eh('%s_VD2' % c), C, HV(c))
    nm = CFG[c]['P'] + '-VD2'; z = np.load('/home/claude/wayfarer-design/reviews/reference-assets/r6/%s_r6.npz' % nm); keep = z['keep']; Fx = z['F'][keep[z['F']].all(1)]
    q = os.path.join(TMP, 'src_%s.npz' % c); np.savez_compressed(q, V=z['V'], Q=Fx); render('src_%s' % c, q, np.tile(GREY, (len(z['V']), 1)), BV(c)[:2])
    fp = '%s/fam/%s_fam.npz' % (W2, nm); fz = np.load(fp); render('fam_%s' % c, fp, np.tile(GREY, (len(fz['V']), 1)), BV(c)[:2])
    for pn in ('shoulder_abd90_l', 'elbow_130_l', 'hip_flex90_l', 'knee_140_l', 'neck_rot45', 'trunk_twist30'):
        pp = '%s/def/%s_%s_fam.npz' % (W2, pn, nm)
        if not os.path.exists(pp): continue
        X = np.load(pp); Xv = X['V']; C = np.tile(GREY, (len(fz['Q']), 1)); fl = np.asarray(X['flip']).astype(int).ravel(); C[fl[fl < len(C)]] = [0.92, 0.18, 0.12]
        q = os.path.join(TMP, 'pose_%s_%s.npz' % (c, pn)); np.savez_compressed(q, V=Xv, Q=fz['Q']); B_ = np.array([0.0, Xv[:, 1].mean(), (Xv[:, 2].max() + Xv[:, 2].min()) / 2])
        render('pose_%s_%s' % (c, pn), q, C, [('v', (1, 1, 0.05), B_, 100)], px=420)
print('render jobs', len(jobs), flush=True)
done_ = lambda j: all(os.path.exists(os.path.join(TMP, '%s_%s.png' % (j[6], v_.split(':')[0]))) for v_ in j[7].split(';'))
todo = [j for j in jobs if not done_(j)]; print('to render', len(todo), flush=True)
with ThreadPoolExecutor(int(E_('VA_SHEET_THREADS', '2'))) as ex: list(ex.map(lambda j: subprocess.run(j, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL), todo))
def sheet(fname, title, rows, colw=420, note=None, lab_w=150, legend=None):
    ncol = max(len(r_[1]) for r_ in rows); Wd = lab_w + ncol * colw; tl = title.split(' — ', 1) if font(21, True).getlength(title) > Wd - 28 else [title]; th = 70 + 30 * (len(tl) - 1)
    nl = len(note.split('\n')) if note else 0; Hh = th + sum(colw + 34 for _ in rows) + (24 * nl + 20 if note else 0) + (44 if legend else 0)
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
        for nm_, col in legend:
            d.rectangle((x, y + 10, x + 24, y + 30), fill=tuple(int(255 * v) for v in col)); d.text((x + 30, y + 10), nm_, fill=(0, 0, 0), font=font(14)); x += 40 + 9 * len(nm_)
        y += 44
    if note:
        for i_, ln in enumerate(note.split('\n')): d.text((14, y + 4 + 24 * i_), ln, fill=(60, 60, 60), font=font(15))
    S.save(os.path.join(OUT, fname), quality=88)
EVC = {c: jl('%s/VD_eval_%s.json' % (EV, c)) for c in CFG}
def sysnote(c, keys=None):
    out = []
    for name, row in EVC[c]['systems'].items():
        if keys and not any(name.startswith(k) for k in keys): continue
        x = row['items']; s = '%s: region RMS vs MF R1 %.1f / VD2 %.1f mm (SG-MF %.1f)' % (name, x['R1']['vs_MF_rms_mm'], x['VD2']['vs_MF_rms_mm'], row['SG_vs_MF_rms_mm'])
        if row['descriptor']: s += ';  %s vs MF R1 %+.1f / VD2 %+.1f %% (human var %.1f)' % (row['descriptor'], x['R1']['vs_MF_pct'], x['VD2']['vs_MF_pct'], row['human_var_pct'])
        out.append('%s %s' % (c, s))
    return '\n'.join(out)
T4 = ['R1', 'VD1', 'VD2', 'VD3']; C4 = ['R1 (accepted)', 'VD1 (0.6)', 'VD2 (1.0)', 'VD3 (1.4)']
for i, (v, lab) in enumerate((('bf', 'front'), ('bq', 'three-quarter'), ('bp', 'profile'))):
    sheet('VD_%02d_R1_vs_VD_%s.jpg' % (i + 1, lab.replace('-', '')), 'Vael R1 vs VD1 / VD2 / VD3 — full body %s, ears hidden, 178 cm, same camera' % lab,
          [(c, [img('he_%s_%s' % (c, t), v) for t in T4], C4) for c in CFG], colw=430)
for i, (v, lab) in enumerate((('bf', 'front'), ('bq', 'three-quarter'))):
    sheet('VD_%02d_VD2_vs_humans_%s.jpg' % (i + 4, lab.replace('-', '')), 'Vael VD2 vs Marchfolk / Sagekin — %s, ears hidden, equal height; overlay VD2 red / Marchfolk blue' % lab,
          [(c, [img('he_%s_%s' % (c, t), v) for t in ('VD2', 'MF', 'SG')] + [blend(img('he_%s_VD2' % c, v), img('he_%s_MF' % c, v))], ['Vael VD2', 'Marchfolk', 'Sagekin', 'overlay']) for c in CFG], colw=430)
sheet('VD_06_VD2_vs_Fenn_Aelari.jpg', 'Vael VD2 vs frozen Fenn / frozen Aelari — front, three-quarter, profile (ears hidden, equal height)',
      [('%s %s' % (c, v[1:]), [img('he_%s_%s' % (c, t), v) for t in ('VD2', 'FN', 'AE')], ['Vael VD2', 'frozen Fenn', 'frozen Aelari'] if v == 'bf' else None) for c in CFG for v in ('bf', 'bq', 'bp')], colw=400)
COLS5 = ['R1', 'VD2', 'MF', 'FN', 'AE']; CAP5 = ['Vael R1', 'Vael VD2', 'Marchfolk', 'frozen Fenn', 'frozen Aelari']
def region_sheet(fname, title, views, note, legend=None):
    rows = [('%s %s' % (c, v), [img('reg_%s' % c, v)] + [img('he_%s_%s' % (c, t), v) for t in COLS5], ['VD2 field regions'] + CAP5 if v == views[0] else None) for c in CFG for v in views]
    sheet(fname, title, rows, colw=330, note=note, legend=legend)
LEG = [(k, v) for k, v in REGC.items()]
region_sheet('VD_07_torso_ribcage.jpg', 'Torso / ribcage — front and oblique (field regions | R1 | VD2 | MF | Fenn | Aelari)', ('tf', 'tq'), sysnote('c1', ['1', '2']) + '\n' + sysnote('c2', ['1', '2']), LEG)
region_sheet('VD_08_shoulder_clavicle.jpg', 'Shoulder / clavicle integration (field regions | R1 | VD2 | MF | Fenn | Aelari)', ('sh',), sysnote('c1', ['3']) + '\n' + sysnote('c2', ['3']), LEG)
region_sheet('VD_09_pelvis_hip.jpg', 'Pelvis / hip silhouette — front and oblique (field regions | R1 | VD2 | MF | Fenn | Aelari)', ('pf', 'pq'), sysnote('c1', ['4']) + '\n' + sysnote('c2', ['4']), LEG)
region_sheet('VD_10_wrist_hand_base.jpg', 'Wrist / hand base — side and back of hand (field regions | R1 | VD2 | MF | Fenn | Aelari)', ('hand', 'handb'), sysnote('c1', ['5']) + '\n' + sysnote('c2', ['5']), LEG)
region_sheet('VD_11_ankle_foot_base.jpg', 'Ankle / foot base — three-quarter and heel (field regions | R1 | VD2 | MF | Fenn | Aelari)', ('foot', 'heel'), sysnote('c1', ['6']) + '\n' + sysnote('c2', ['6']), LEG)
sheet('VD_12_silhouette_overlays_vs_MF.jpg', 'Silhouette overlays vs Marchfolk (candidate red / Marchfolk blue) — R1 | VD2 | VD3 | GX scope diagnostic (not a candidate)',
      [('%s %s' % (c, v[1:]), [blend(img('he_%s_%s' % (c, t), v), img('he_%s_MF' % c, v)) for t in ('R1', 'VD2', 'VD3', 'GX')], ['R1', 'VD2', 'VD3', 'GX (outside scope)'] if v == 'bf' else None) for c in CFG for v in ('bf', 'bq', 'tf')], colw=400,
      note='GX = VD2 + a stronger lateral trunk side wall (rib -0.09, flank -0.05) + 5 % radial limb-envelope slimming: an elf-family frontal-gracility probe outside the order §4 systems, shown only to locate the remaining gap')
sheet('VD_13_regional_displacement.jpg', 'VD2 field — displacement |VD2 - R1| (blue 0 .. red >= 8 mm) and region map', [(c, [img('disp_%s' % c, v) for v in ('bf', 'bq', 'tf', 'tq')] + [img('reg_%s' % c, 'tq')], ['front', '3/4', 'torso', 'torso 3/4', 'regions']) for c in CFG], colw=340,
      legend=LEG, note='\n'.join('%s: VD2 affected %d verts, max %.2f cm, RMS %.2f cm; per region max cm %s' % (c, EVC[c]['audit']['VD2']['affected_vertices_rest'], EVC[c]['audit']['VD2']['max_cm_rest'], EVC[c]['audit']['VD2']['rms_cm_rest_affected'],
                                                                                                           {k: round(v['max_cm'], 2) for k, v in EVC[c]['audit']['VD2']['per_region'].items()}) for c in CFG))
sheet('VD_14_body_residual_heatmaps.jpg', 'VD2 body residuals at equal stature (blue 0 .. red >= 3 cm): vs Marchfolk | Sagekin | Aelari | Fenn',
      [('%s %s' % (c, v[1:]), [img('bres_%s_%s' % (c, k), v) for k in ('MF', 'SG', 'AE', 'FN')], ['vs Marchfolk', 'vs Sagekin', 'vs Aelari', 'vs Fenn'] if v == 'bf' else None) for c in CFG for v in ('bf', 'bq')], colw=380)
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
PV = {t: jl('%s/VD_pelvis_%s.json' % (EV, t)) for t in ('VD1', 'VD2', 'VD3')}; PR1 = jl(EV + '/../vael_rp3_source/VA2_pelvis_skeletal_proxy.json')
fig, axs = plt.subplots(1, 2, figsize=(15, 4.8))
for ax, key, ttl in zip(axs, ('leg_share', 'waist_interval_over_torso'), ('hip-joint height / stature (skeletal proxy, t = 0.5): MF < Vael < Aelari < Fenn', 'VA-P6 waist interval / torso < Aelari')):
    x = 0; xt = []; xl = []
    for c in ('c1', 'c2'):
        r1 = [r for r in PR1['rules'][c] if r['key'] == key]; ref = {r['rel'][-2:]: r['by_t']['0.5']['ref'] for r in r1}
        vals = [('MF', ref.get('MF')), ('R1', r1[0]['by_t']['0.5']['VA'])] + [(t, [r for r in PV[t]['rules'][c] if r['key'] == key][0]['by_t']['0.5']['VA']) for t in ('VD1', 'VD2', 'VD3')] + [('AE', ref.get('AE')), ('FN', ref.get('FN'))]
        for lab, v in vals:
            if v is None: continue
            ax.bar(x, v, color={'MF': '#6aa36a', 'AE': '#7a4fb0', 'FN': '#4a78c2'}.get(lab, '#e07a2e')); xt.append(x); xl.append('%s %s' % (c, lab)); x += 1
        x += 1
    vv = [p.get_height() for p in ax.patches]; lo, hi = min(vv), max(vv); ax.set_ylim(lo - 0.3 * (hi - lo), hi + 0.3 * (hi - lo)); ax.set_xticks(xt); ax.set_xticklabels(xl, rotation=60, fontsize=7); ax.set_title(ttl, fontsize=10)
fig.tight_layout(); fig.savefig(os.path.join(OUT, 'VD_15_pelvis_ordering.jpg'), dpi=100); plt.close(fig)
names = {c: CFG[c]['P'] + '-VD2' for c in CFG}; VA_ = {c: jl('%s/val/%s_fam_validator_v2_D1-D6.json' % (W2, names[c])) for c in CFG}; st_ = sorted(VA_['c1']['stations'])
S = Image.new('RGB', (1200, 140 + 26 * (len(st_) + 2)), 'white'); d = ImageDraw.Draw(S)
d.text((14, 14), 'Vael VD2 family candidates on frozen v005 — validator D1+D3+D4+D5+D6', fill=(0, 0, 0), font=font(20, True))
d.text((14, 44), 'margin = loops - contract minimum (red = 0).   c1: %d / 69   c2: %d / 69' % (VA_['c1']['summary']['firm_pass_count'], VA_['c2']['summary']['firm_pass_count']), fill=(0, 0, 0), font=font(16))
cw = [260, 150, 150, 150, 150, 150, 150]; y = 90
for i, t in enumerate(['station', 'c1 loops', 'c1 min', 'c1 margin', 'c2 loops', 'c2 min', 'c2 margin']): d.text((20 + sum(cw[:i]), y), t, fill=(0, 0, 0), font=font(15, True))
y += 28
for s_ in st_:
    a, b = VA_['c1']['stations'][s_], VA_['c2']['stations'][s_]; vals = [s_, a['loops_v2'], a['required'], a['margin'], b['loops_v2'], b['required'], b['margin']]
    for i, t in enumerate(vals): d.text((20 + sum(cw[:i]), y), str(t), fill=(200, 30, 30) if (i in (3, 6) and t == 0) else (0, 0, 0), font=font(14))
    y += 26
S.save(os.path.join(OUT, 'VD_16_validator_margins.jpg'), quality=88)
fig, ax = plt.subplots(figsize=(11, 4.5)); zs = ['face', 'ears', 'hand', 'foot', 'trunk', 'arm', 'leg', 'neck', 'head']; x = np.arange(len(zs)); okall = True
for i, c in enumerate(CFG):
    au = jl('%s/audit/%s_fam_audit.json' % (W2, names[c]))['density_pct_of_stature']; ax.bar(x + (i - 0.5) * 0.35, [au[z]['mean'] for z in zs], 0.35, label=names[c]); okall &= all(au[z]['pass_mean'] for z in zs)
    ax.scatter(x, [au[z]['limit'] for z in zs], marker='_', s=600, color='k')
ax.set_xticks(x); ax.set_xticklabels(zs); ax.set_ylabel('mean edge / stature (%)'); ax.set_title('Vael VD2 family density, 9 zones (black bar = limit): %s' % ('all pass' if okall else 'FAIL present')); ax.legend(); fig.tight_layout(); fig.savefig(os.path.join(OUT, 'VD_17_density.jpg'), dpi=105); plt.close(fig)
dc = jl(EV + '/VAEL_deformation_comparison.json'); PN = ('shoulder_abd90_l', 'elbow_130_l', 'hip_flex90_l', 'knee_140_l', 'neck_rot45', 'trunk_twist30')
sheet('VD_18_deformation.jpg', 'Vael VD2 family candidates — Standard v1 deformation (source rig + carried MPFB weights, plain LBS; red = flipped faces)',
      [(c, [img('pose_%s_%s' % (c, p), 'v') for p in PN], ['%s %d (MF v005 %d)' % (p, dc[names[c]]['poses'][p]['aelari_family'], dc[names[c]]['poses'][p]['marchfolk_v005']) for p in PN]) for c in CFG], colw=360,
      note='worst flip excess vs the frozen Marchfolk v005 realisation: %s; poses worse by > 5: %s' % ({n: dc[n]['worst_flip_excess'] for n in dc}, {n: dc[n]['poses_worse_by_more_than_5'] for n in dc}))
FR = jl(EV + '/VD_face_regression.json')
sheet('VD_19_hidden_ear_face_regression.jpg', 'VC2 face regression — R1 | VD2 (ears hidden) and |VD2 - R1| on the head (blue 0 .. red >= 1 mm)',
      [('%s %s' % (c, v[1:]), [img('he_%s_R1' % c, v), img('he_%s_VD2' % c, v), img('fdiff_%s' % c, v)], ['R1', 'VD2', 'difference'] if v == 'hfront' else None) for c in CFG for v in ('hfront', 'hprof')], colw=400,
      note='\n'.join('%s: head max |dV| %.4f cm; face systems %d / 6 (R1 %d); elf rows %d / 9; whole-face vs MF %.2f mm (R1 %.2f); brow vs MF %+.2f %% (R1 %+.2f); jaw vs MF %+.2f %% (R1 %+.2f)' % (
          c, FR[c]['head_max_dV_cm'], FR[c]['VD2']['face_systems'], FR[c]['R1']['face_systems'], FR[c]['VD2']['elf_rows'], FR[c]['VD2']['whole_face_mm'], FR[c]['R1']['whole_face_mm'],
          FR[c]['VD2']['brow_pct'], FR[c]['R1']['brow_pct'], FR[c]['VD2']['jaw_pct'], FR[c]['R1']['jaw_pct']) for c in CFG))
sheet('VD_20_final_five_population.jpg', 'FINAL equal-height (178 cm) hidden-ear neutral comparison — Vael VD2 | frozen Fenn | frozen Aelari | Marchfolk | Sagekin',
      [('%s %s' % (c, v[1:]), [img('he_%s_%s' % (c, t), v) for t in ('VD2', 'FN', 'AE', 'MF', 'SG')], ['Vael VD2', 'frozen Fenn', 'frozen Aelari', 'Marchfolk', 'Sagekin'] if v == 'bf' else None) for c in CFG for v in ('bf', 'bq', 'bp')], colw=340)
sheet('VD_21_scope_diagnostic_GX.jpg', 'Scope diagnostic GX (NOT a candidate; outside the order §4 systems) — R1 | VD2 | GX | Marchfolk | frozen Fenn | frozen Aelari',
      [('%s %s' % (c, v[1:]), [img('he_%s_%s' % (c, t), v) for t in ('R1', 'VD2', 'GX', 'MF', 'FN', 'AE')], ['R1', 'VD2', 'GX', 'Marchfolk', 'Fenn', 'Aelari'] if v == 'bf' else None) for c in CFG for v in ('bf', 'bq', 'tf')], colw=300,
      note='GX = VD2 with a stronger trunk side wall (rib -0.09, flank -0.05 x waist half-breadth) and 5 % radial slimming of the upper arm / forearm / thigh / calf envelope (frontal elf-family gracility)')
print('sheets done', len([f for f in os.listdir(OUT) if f.startswith('VD_')]), flush=True)
