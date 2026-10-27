# fn_extra_sheets.py WORK : order 57dc328 §17 sheets 1, 3-9 (identical orthographic cameras; joint close-ups centred on each body's own rig joint).
import sys, os, json, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
W = sys.argv[1]; T = '/home/claude/wayfarer-design/tools/rac/rp/grask_rigprep_v001/render_attr.py'; BP = '/home/claude/stc/bin/python3'
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FN_ = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; FM = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
f = lambda n, b=False: ImageFont.truetype(FB if b else FN_, n); mono = ImageFont.truetype(FM, 12)
OV = W + '/ov'; SH = W + '/sheets'; os.makedirs(OV, exist_ok=True); os.makedirs(SH, exist_ok=True); CLAY = np.array([0.80, 0.77, 0.73]); RA = '/home/claude/wayfarer-design/reviews/reference-assets/r6'; PA = W + '/partA'
def render(V, Q, col, tg, vs, wire='0', px=500):
    o = OV + '/%s.npz' % tg
    if not os.path.exists(OV + '/%s_%s.png' % (tg, vs.split(';')[-1].split(':')[0])):
        np.savez(o, V=V, Q=Q); np.save(o[:-4] + '_c.npy', np.asarray(col, np.float32))
        subprocess.run([BP, T, '--', o, o[:-4] + '_c.npy', OV, tg, vs, wire, str(px)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, env=dict(os.environ, WIRE_T='0.00012'))
        os.remove(o); os.remove(o[:-4] + '_c.npy')
def img(tg, v, w, h=None): return Image.open('%s/%s_%s.png' % (OV, tg, v)).convert('RGB').resize((w, h or w), Image.LANCZOS)
def vs_(views): return ';'.join('%s:%s:%s:%g' % (n, ','.join('%.4f' % x for x in d), ','.join('%.3f' % x for x in c), h) for n, d, c, h in views)
def r6body(p):
    z = np.load(p); k = z['keep']; F = z['F'][k[z['F']].all(1)]; return z['V'].astype(float), F
def joints(p): return {k: np.array(v[0]) for k, v in json.loads(str(np.load(p)['joints'])).items()}
fam = lambda cid: (np.load('%s/cand/%s_fam.npz' % (W, cid))['V'].astype(float), np.load('%s/cand/%s_fam.npz' % (W, cid))['Q'])
PAJ = json.load(open(PA + '/FNF181_reference_validation.json')); HE = json.load(open(W + '/anat/FN_hidden_ear_identity.json'))
# ---------- 1: central references at true scale (c1 bounds FN157-NAT / FN211 for context)
B = [('FN157-NAT', 'FN157-NAT (c1 min, accepted)', r6body(RA + '/FN157-NAT_r6.npz')), ('FNL4', 'FNL4 (c1 central, family v005)', fam('FNL4')), ('FN211', 'FN211 (c1 max, accepted)', r6body(RA + '/FN211_r6.npz')),
     ('FNF181', 'FNF181 (c2 central candidate, family v005)', fam('FNF181'))]
VW = [('front', (0, 1, 0), np.array([0, 0, 107.0]), 110), ('profile', (1, 0, 0), np.array([0, 0, 107.0]), 110)]
for tg, _, (V, Q) in B: render(V, Q, np.tile(CLAY, (len(Q), 1)), 'fc_' + tg, vs_(VW))
cw = 320; rows = PAJ['identity']; S = Image.new('RGB', (8 * cw + 20, 100 + cw + (len(rows) + 4) * 16), 'white'); d = ImageDraw.Draw(S)
d.text((10, 8), 'Fenn central references — identical orthographic camera, true scale (frame 220 cm), clay, R-6; front | profile. Configuration 2 has no accepted bounds yet (FN157-NAT / FN211 are configuration 1)', fill=(0, 0, 0), font=f(14, True))
d.text((10, 30), 'FNF181 = accepted MF-F-R configuration-2 build + exactly the FNL4 targets and bone scales (cfg identical except gender), stature re-solved to 180.99 cm; rebuild-identical (|dV| 0, two re-solves + regen)', fill=(60, 60, 60), font=f(12))
for i, (tg, lab, _) in enumerate(B):
    for j, v in enumerate(('front', 'profile')): S.paste(img('fc_' + tg, v, cw), (10 + (2 * i + j) * cw, 76))
    d.text((14 + 2 * i * cw, 56), '%s — %.2f cm' % (lab, PAJ['stature'][tg]), fill=(150, 20, 20), font=f(12, True))
y = 84 + cw; d.text((10, y), '%-42s %9s %9s  %8s %8s | %8s %8s   canon' % ('Fenn vs matched-stature human (181 cm)', 'FNL4', 'FNF181', 'c1-MF', 'c1-SG', 'c2-MF', 'c2-SG'), fill=(0, 0, 0), font=mono); y += 18
for r in rows:
    ok = (r['c1_canon_ok'], r['c2_canon_ok']); col = (0, 110, 0) if r['canon_direction'] and all(ok) else ((170, 90, 0) if r['canon_direction'] else (60, 60, 60))
    d.text((10, y), '%-42s %9.4f %9.4f  %+7.2f%% %+7.2f%% | %+7.2f%% %+7.2f%%   %s' % (r['measure'], r['FNL4'], r['FNF181'], r['c1_vs_MF_pct'], r['c1_vs_SG_pct'], r['c2_vs_MF_pct'], r['c2_vs_SG_pct'],
           {1: 'Fenn >', -1: 'Fenn <', 0: 'report'}[r['canon_direction']] + ('' if not r['canon_direction'] else ('  ok / ok' if all(ok) else '  c1 %s / c2 %s' % ('ok' if ok[0] else 'NO', 'ok' if ok[1] else 'NO')))), fill=col, font=mono); y += 16
e2 = PAJ['pelvis_skeletal_proxy']['E_A2']['bitroch_over_crest_not_lower_than_MF']
d.text((10, y + 4), 'skin readings are diagnostics (PV-D16). Skeletal-proxy E-A2 bitrochanteric / crest vs MF: c1 %s %%, c2 %s %% (t = 0 / 0.5 / 1): c2 is a tie below method resolution (see gate)' % (e2['c1_pct_by_t'], e2['c2_pct_by_t']), fill=(60, 60, 60), font=f(11))
S.save(SH + '/Fenn_central_references.jpg', quality=85)
# ---------- 3: hidden-ear body, matched stature
CF = {'c1': [('FNL4', 'Fenn FNL4'), ('MFM181', 'Marchfolk MFM181'), ('SGM181', 'Sagekin SGM181')], 'c2': [('FNF181', 'Fenn FNF181'), ('MFF181', 'Marchfolk MFF181'), ('SGF181', 'Sagekin SGF181')]}
VB = [('front', (0, 1, 0), np.array([0, 0, 94.0]), 96), ('profile', (1, 0, 0), np.array([0, 0, 94.0]), 96), ('q3', (0.7, 0.7, 0.1), np.array([0, 0, 94.0]), 96)]
H = {}
for cfg, L in CF.items():
    for n, _ in L:
        z = np.load('%s/%s_earhidden.npz' % (OV, n)); H[n] = (z['V'], z['Q']); render(z['V'], z['Q'], np.tile(CLAY, (len(z['Q']), 1)), 'he_' + n, vs_(VB))
cw = 300; S = Image.new('RGB', (9 * cw + 20, 120 + 2 * (cw + 30) + 150), 'white'); d = ImageDraw.Draw(S)
d.text((10, 8), 'HIDDEN-EAR body comparison at matched stature (~181 cm): Fenn | Marchfolk | Sagekin — ears removed from the read (hm08 auricle collapsed onto the skull), same clay, frame, composition, age, R-6, no hair / clothing', fill=(0, 0, 0), font=f(14, True))
d.text((10, 30), 'front | profile | 3-4 per body; identical camera for all nine bodies per row', fill=(60, 60, 60), font=f(12))
for r, (cfg, L) in enumerate(CF.items()):
    y0 = 56 + r * (cw + 30)
    for i, (n, lab) in enumerate(L):
        for j, v in enumerate(('front', 'profile', 'q3')): S.paste(img('he_' + n, v, cw), (10 + (3 * i + j) * cw, y0 + 20))
        d.text((14 + 3 * i * cw, y0), '%s (%s)' % (lab, cfg), fill=(150, 20, 20), font=f(12, True))
y = 70 + 2 * (cw + 30); d.text((10, y), 'body-region correspondence RMS (ears excluded): Fenn vs Marchfolk | Fenn vs Sagekin | human baseline Sagekin vs Marchfolk', fill=(0, 0, 0), font=f(12, True)); y += 20
for cfg in ('c1', 'c2'):
    b = HE['configs'][cfg]['body']; d.text((10, y), '%s  ' % cfg + '   '.join('%s %.1f | %.1f | %.1f mm' % (k, v['FN_vs_MF_rms_mm'], v['FN_vs_SG_rms_mm'], v['SG_vs_MF_rms_mm_human_baseline']) for k, v in b.items()), fill=(0, 0, 0), font=mono); y += 18
d.text((10, y + 4), 'Body: the Fenn departure is 2-6x the human-human (Sagekin-Marchfolk) difference in every region; canon body directions 16 / 16 (c1) and 15 / 16 (c2: pelvis E-A2 skeletal tie, -0.09 %) — PASS', fill=(0, 110, 0), font=f(12, True))
S.save(SH + '/Fenn_hidden_ear_body.jpg', quality=85)
# ---------- 4: hidden-ear face
cw = 300; S = Image.new('RGB', (9 * cw + 20, 130 + 3 * (cw + 30) + 220), 'white'); d = ImageDraw.Draw(S)
d.text((10, 8), 'HIDDEN-EAR face comparison (ears collapsed): Fenn | Marchfolk | Sagekin heads at matched stature — front | profile | 3-4; bottom row: Fenn face residual vs Marchfolk after removing head size (similarity fit)', fill=(0, 0, 0), font=f(14, True))
def ramp(t):
    t = np.clip(t, 0, 1)[:, None]; return np.where(t < 0.5, (1 - 2 * t) * np.array([0.15, 0.35, 0.85]) + 2 * t * np.array([0.95, 0.9, 0.3]), (2 - 2 * t) * np.array([0.95, 0.9, 0.3]) + (2 * t - 1) * np.array([0.85, 0.1, 0.1]))
for r, (cfg, L) in enumerate(CF.items()):
    y0 = 40 + r * (cw + 30)
    for i, (n, lab) in enumerate(L):
        V, Q = H[n]; jj = joints({'FNL4': RA + '/FNL4_r6.npz', 'FNF181': PA + '/build/FNF181_r6.npz'}.get(n, PA + '/cmp/%s_r6.npz' % n)); hc = jj['head'] + np.array([0, 4.0, 8.5])
        FVv = [('front', (0, 1, 0.05), hc, 13), ('profile', (1, 0.03, 0), hc + [0, -3, 0], 14), ('q3', (0.6, 0.8, 0.05), hc, 13)]
        render(V, Q, np.tile(CLAY, (len(Q), 1)), 'hf_' + n, vs_(FVv))
        for j, v in enumerate(('front', 'profile', 'q3')): S.paste(img('hf_' + n, v, cw), (10 + (3 * i + j) * cw, y0 + 20))
        d.text((14 + 3 * i * cw, y0), '%s (%s)' % (lab, cfg), fill=(150, 20, 20), font=f(12, True))
y0 = 40 + 2 * (cw + 30)
for i, n in enumerate(('FNL4', 'FNF181')):
    V, Q = H[n]; res = np.load('%s/%s_face_resid_vs_MF.npy' % (OV, n)); jj = joints({'FNL4': RA + '/FNL4_r6.npz', 'FNF181': PA + '/build/FNF181_r6.npz'}[n]); hc = jj['head'] + np.array([0, 4.0, 8.5])
    render(V, Q, ramp(res[Q].mean(1) / 2.0), 'hr_' + n, vs_([('front', (0, 1, 0.05), hc, 13), ('profile', (1, 0.03, 0), hc + [0, -3, 0], 14), ('q3', (0.6, 0.8, 0.05), hc, 13)]))
    for j, v in enumerate(('front', 'profile', 'q3')): S.paste(img('hr_' + n, v, cw), (10 + (3 * i + j) * cw, y0 + 20))
    d.text((14 + 3 * i * cw, y0), '%s residual vs Marchfolk (scale removed): blue 0 -> yellow 1 -> red >= 2 mm' % n, fill=(150, 20, 20), font=f(12, True))
y = y0 + cw + 30
for cfg in ('c1', 'c2'):
    fc = HE['configs'][cfg]['face']; d.text((10, y), '%s face RMS vs MF (scale removed): ' % cfg + '  '.join('%s %.2f mm' % (k, v['FN_vs_MF_rms_mm']) for k, v in fc.items()), fill=(0, 0, 0), font=mono); y += 16
    cd = HE['configs'][cfg]['canon_descriptors']; d.text((10, y), '%s canon descriptors FN vs MF: ' % cfg + '  '.join('%s %+.2f%%' % (k.replace('_over_', '/'), v['FN_vs_MF_pct']) for k, v in cd.items()), fill=(0, 0, 0), font=mono); y += 18
d.text((10, y + 4), 'Face: ONLY the orbit / eye region departs (1.17 mm RMS, 0.5 % HH; eye-scale / eye-height targets). Cranium, forehead, cheeks / mid-face, nose, mouth, jaw / chin stay within 0.6 mm of a size-scaled Marchfolk face;', fill=(170, 0, 0), font=f(12, True))
d.text((10, y + 22), 'none of the FENN_V1 §2-7 cranium / mid-face / jaw / forehead tendencies is expressed by the accepted FNL4 head (it is the MPFB human head scaled -1.2 %) — hidden-ear FACIAL identity NOT MET beyond the orbit region', fill=(170, 0, 0), font=f(12, True))
S.save(SH + '/Fenn_hidden_ear_face.jpg', quality=85)
# ---------- 5-8: joint close-ups (each centred on its own joint)
RP = {'FNL4': RA + '/FNL4_r6.npz', 'MFM181': PA + '/cmp/MFM181_r6.npz', 'SGM181': PA + '/cmp/SGM181_r6.npz', 'FNF181': PA + '/build/FNF181_r6.npz', 'MFF181': PA + '/cmp/MFF181_r6.npz', 'SGF181': PA + '/cmp/SGF181_r6.npz'}
JS = {'Fenn_shoulder_joint_scale': [('shoulder', 'upperarm_l', (0.6, 0.75, 0.2), [0, 0, -2], 13), ('elbow', 'lowerarm_l', (0.95, 0.2, 0.1), [0, 0, 0], 9), ('knee', 'calf_l', (0.3, 1, 0.1), [0, 0, 0], 11), ('wrist', 'hand_l', (0.95, 0.2, 0.1), [0, 0, 2], 7)],
      'Fenn_pelvis_leg': [('pelvis front', 'pelvis', (0, 1, 0.05), [0, 0, -12], 26), ('pelvis-leg profile', 'pelvis', (1, 0, 0), [0, 0, -30], 50), ('leg front', 'calf_l', (0, 1, 0.05), [-5, 0, 5], 50)],
      'Fenn_hand': [('hand palm', 'hand_l', (0.95, 0.15, 0.1), [0.5, 0, -8], 11), ('hand dorsal', 'hand_l', (-0.95, -0.15, 0.1), [0.5, 0, -8], 11), ('hand front', 'hand_l', (0.2, 1, 0.05), [0.5, 0, -8], 11)],
      'Fenn_foot': [('foot dorsal', 'foot_l', (0.2, 0.3, 1), [0, 7, -6], 14), ('foot medial', 'foot_l', (-1, 0, 0.1), [0, 7, -6], 14), ('foot lateral', 'foot_l', (1, 0, 0.1), [0, 7, -6], 14)]}
for sheet, views in JS.items():
    cw = 260; S = Image.new('RGB', (6 * cw + 20, 70 + len(views) * (cw + 24)), 'white'); d = ImageDraw.Draw(S)
    d.text((10, 8), '%s — matched stature (~181 cm), identical camera size, each view centred on the body\'s own rig joint; columns: Fenn c1 | Marchfolk c1 | Sagekin c1 | Fenn c2 | Marchfolk c2 | Sagekin c2' % sheet.replace('_', ' '), fill=(0, 0, 0), font=f(13, True))
    for i, (nm, jn, dr, off, h) in enumerate(views):
        for j, n in enumerate(('FNL4', 'MFM181', 'SGM181', 'FNF181', 'MFF181', 'SGF181')):
            V, Q = H[n]; c = joints(RP[n])[jn] + np.array(off, float); tg = 'jc_%s_%s_%d' % (sheet, n, i)
            render(V, Q, np.tile(CLAY, (len(Q), 1)), tg, vs_([('v', dr, c, h)]), '0', 420)
            S.paste(img(tg, 'v', cw), (10 + j * cw, 50 + i * (cw + 24))); d.text((14 + j * cw, 34 + i * (cw + 24)), '%s %s' % (n, nm), fill=(150, 20, 20), font=f(11, True))
    S.save(SH + '/%s.jpg' % sheet, quality=85)
print('fenn extra sheets done')
