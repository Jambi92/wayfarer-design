# hv_final_sheets.py WORK OUTDIR : Halvren final whole-character consolidation order §10 boards (neutral clay, orthographic, workbench renders):
#   A  final whole-character references c1 / c2: front | front 3/4 | side | rear 3/4 | rear
#   B  matched lineup Marchfolk | Halvren final | frozen Fenn | frozen Aelari | frozen Vael, ears visible (production references, uniformly scaled to
#      178 cm about the ground) and ears hidden (hm08 R-6 sources re-solved at 178 cm, external ear collapsed): full body and head
#   C  regression: accepted R-6 source | accepted HB2 + HF2 + HP-B family realization | final, with |final - family| heat (only the frozen ear + HR2 zone):
#      body, face, pelvis
#   D  ear integration HE2 / HR2 on c1 / c2: front 3/4 | side | true rear 3/4 | lower-rear 3/4
#   E  deformation stress: the worst Standard v1 poses per configuration (flipped faces red)
import sys, os, json, subprocess, numpy as np
from PIL import Image, ImageDraw
from concurrent.futures import ThreadPoolExecutor
os.environ.setdefault('EAR_TOPO', 'v002'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import hv_ear_quick as QK
W, OUT = sys.argv[1:3]; os.makedirs(OUT, exist_ok=True); TMP = W + '/sheets_r'; os.makedirs(TMP, exist_ok=True); font = QK.font; GREY = QK.GREY; jl = lambda p: json.load(open(p))
H = {'c1': 'HVC1-HB2HF2-HPB', 'c2': 'HVF178-HB2HF2-HPB'}; NM = {'c1': 'HV_M_REF_RP3_v001', 'c2': 'HV_F_REF_RP3_v001'}
FINAL = lambda c: '%s/ear/build/%s_HE2_branch.npz' % (W, H[c])
VIS = {'c1': dict(MF='/tmp/claude-0/rt/v5/cand/MF-M-R_v005.npz', FN='/tmp/claude-0/rt/fn/final/ear/build/FNL4-CF2_E2_branch.npz', AE='/tmp/claude-0/rt/ae/final/ear/build/AEL1-R1_AE-E2_branch.npz',
              VA='/tmp/claude-0/rt/va/final/ear/RI3/build/VAL4-R1-VD2-VF2_VA-E2-RI3_branch.npz'),
       'c2': dict(MF='/tmp/claude-0/rt/v5/cand/MF-F-R_v005.npz', FN='/tmp/claude-0/rt/fn/final/ear/build/FNF181-CF2_E2_branch.npz', AE='/tmp/claude-0/rt/ae/final/ear/build/AELF190-R1_AE-E2_branch.npz',
              VA='/tmp/claude-0/rt/va/final/ear/RI3/build/VALF178-R1-VD2-VF2_VA-E2-RI3_branch.npz')}
HID = {'c1': dict(MF='MFM178', FN='FNM178', AE='AEM178', VA='VAM178'), 'c2': dict(MF='MFF178', FN='FNF178', AE='AEF178', VA='VAF178')}
LAB = dict(MF='Marchfolk', HV='Halvren final', FN='frozen Fenn', AE='frozen Aelari', VA='frozen Vael'); ORD = ('MF', 'HV', 'FN', 'AE', 'VA')
jobs = []
def vs(views): return ';'.join('%s:%s:%s:%.2f' % (n, ','.join('%.4f' % x for x in d), ','.join('%.3f' % x for x in c), h) for n, d, c, h in views)
def job(tag, V, Q, col, views, px=700, env=None, wire=False):
    np.savez(TMP + '/%s_m.npz' % tag, V=np.asarray(V, np.float32), Q=np.asarray(Q)); np.save(TMP + '/%s_c.npy' % tag, np.asarray(col if col is not None else np.tile(GREY, (len(V), 1)), np.float32))
    jobs.append(([QK.BP, QK.REND, '--', TMP + '/%s_m.npz' % tag, TMP + '/%s_c.npy' % tag, TMP, tag, vs(views), '1' if wire else '0', str(px)], dict(os.environ, **(env or {}))))
def img(tag, v):
    p = TMP + '/%s_%s.png' % (tag, v); return Image.open(p).convert('RGB') if os.path.exists(p) else Image.new('RGB', (600, 600), (255, 200, 200))
def body_views(V, h=96):
    zc = (V[:, 2].min() + V[:, 2].max()) / 2; c = np.array([np.median(V[:, 0]), np.median(V[:, 1]), zc])
    return [('front', (0, 1, 0.02), c, h), ('tqf', (1, 1, 0.05), c, h), ('side', (1, 0, 0.02), c, h), ('tqr', (1, -1, 0.05), c, h), ('rear', (0, -1, 0.02), c, h)]
def norm178(V):
    V = np.asarray(V, float).copy(); s = 178.0 / (V[:, 2].max() - V[:, 2].min()); z0 = V[:, 2].min(); V[:, 2] = (V[:, 2] - z0) * s; V[:, 0] = (V[:, 0] - np.median(V[:, 0])) * s; V[:, 1] = (V[:, 1] - np.median(V[:, 1])) * s; return V
ENV = dict(RENDER_LIGHTING='STUDIO:studio.sl')
# ---------------- A
for c in H:
    z = np.load(FINAL(c)); job('A_%s' % c, z['V'], z['Q'], None, body_views(z['V'].astype(float)), env=ENV)
# ---------------- B lineups
for c in H:
    for mode in ('vis', 'hid'):
        Vs, Qs, off = [], [], 0; heads = []
        for k in ORD:
            if mode == 'vis': z = np.load(FINAL(c) if k == 'HV' else VIS[c][k]); V = norm178(z['V'])
            else: z = np.load('%s/he/%s_earhidden.npz' % (W, H[c] if k == 'HV' else HID[c][k])); V = norm178(z['V'])
            x = ORD.index(k) * 62.0; V[:, 0] += x; Vs.append(V); Qs.append(np.asarray(z['Q']) + off); off += len(V); heads.append(np.array([x, np.median(V[:, 1]), 178 - 12]))
        V = np.concatenate(Vs); Q = np.concatenate(Qs); cx = 2 * 62.0
        job('B_%s_%s' % (c, mode), V, Q, None, [('front', (0, 1, 0.02), (cx, 0, 89), 160), ('side', (1, 0.0, 0.02), (cx, 0, 89), 160), ('tqf', (1, 1, 0.05), (cx, 0, 89), 160)], px=1400, env=ENV)
        for i, k in enumerate(ORD):
            job('BH_%s_%s_%s' % (c, mode, k), Vs[i], Qs[i] - sum(len(v) for v in Vs[:i]), None, [('hf', (0, 1, 0.03), heads[i], 14), ('hs', (1, 0.15, 0.03), heads[i], 14)], px=420, env=ENV)
# ---------------- C regression
for c in H:
    z = np.load(FINAL(c)); F = np.load('/tmp/claude-0/rt/hv/hpe/fam/%s_fam.npz' % H[c]); r6 = np.load('/home/claude/wayfarer-design/reviews/reference-assets/r6/%s_r6.npz' % H[c])
    v = z['v005_to_branch']; ok = v >= 0; d = np.zeros(len(z['V'])); d[v[ok]] = np.linalg.norm(z['V'][v[ok]].astype(float) - F['V'][ok].astype(float), axis=1)
    d[z['part'] != 'v005'] = np.nan
    col = np.tile(GREY, (len(z['V']), 1)); hot = np.nan_to_num(d) > 1e-4; t = np.clip(np.nan_to_num(d) / 0.8, 0, 1)[:, None]
    col[hot] = (1 - t[hot]) * np.array([0.95, 0.75, 0.2]) + t[hot] * np.array([0.85, 0.1, 0.1]); col[np.isnan(d)] = [0.35, 0.55, 0.9]
    Vz = z['V'].astype(float); hd = np.array([0, np.median(Vz[:, 1]), Vz[:, 2].max() - 12]); pel = np.array([0, np.median(Vz[:, 1]), 0.53 * Vz[:, 2].max()])
    vw = [('front', (0, 1, 0.02), (0, np.median(Vz[:, 1]), 89), 96), ('side', (1, 0, 0.02), (0, np.median(Vz[:, 1]), 89), 96), ('face', (0.35, 1, 0.05), hd, 14), ('pelvis', (0.4, 1, 0.05), pel, 24)]
    job('C_%s_final' % c, Vz, z['Q'], col, vw, env=ENV); job('C_%s_fam' % c, F['V'], F['Q'], None, vw, env=ENV)
    Fr = np.asarray(r6['F']); job('C_%s_r6' % c, r6['V'], Fr, None, vw, env=ENV)
# ---------------- D ear integration
for c in H:
    z = np.load(FINAL(c)); C = QK.cams(H[c]); vw = [(n, C[n][0], C[n][1], C[n][2]) for n in ('etq', 'side', 'rq', 'lr')]
    job('D_%s' % c, z['V'], z['Q'], None, vw, px=560, env=dict(RENDER_LIGHTING='STUDIO:rim.sl', RENDER_SPEC='1'))
# ---------------- E deformation stress
EP = ('shoulder_flex90_l', 'elbow_130_l', 'hip_flex90_l', 'knee_140_l', 'neck_rot45')
for c in H:
    for p in EP:
        X = np.load('%s/def/%s_%s_final.npz' % (W, p, H[c])); Q = np.load(FINAL(c))['Q']; col = np.tile(GREY, (len(Q), 1)); col[X['flip']] = [0.9, 0.1, 0.1]
        V = X['V'].astype(float); cz = np.array([np.median(V[:, 0]), np.median(V[:, 1]), 89])
        job('E_%s_%s' % (c, p), V, Q, col, [('front', (0.3, 1, 0.05), cz, 96), ('side', (1, 0.2, 0.05), cz, 96)], px=560, env=ENV)
if os.environ.get('SKIP_RENDER') != '1':
    with ThreadPoolExecutor(3) as ex: list(ex.map(lambda j: subprocess.run(j[0], env=j[1], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL), jobs))
def sheet(fn, title, rows, heads, colw=300, note=None, lab_w=150, colh=None):
    colh = colh or colw; ncol = max(len(r[1]) for r in rows); nl = note.count('\n') + 1 if note else 0
    S = Image.new('RGB', (lab_w + ncol * colw, 84 + sum(colh + (24 if r[2] else 6) for r in rows) + 20 * nl + 12), 'white'); d = ImageDraw.Draw(S)
    d.text((12, 12), title, fill=(0, 0, 0), font=font(18, True)); y = 54
    for i, h_ in enumerate(heads): d.text((lab_w + i * colw + 4, y), h_, fill=(0, 0, 0), font=font(13, True))
    y += 24
    for lb, ims, cap in rows:
        d.text((8, y + colh // 2 - 20), lb, fill=(0, 0, 0), font=font(14, True))
        for i, im in enumerate(ims): S.paste(im.resize((colw, colh)), (lab_w + i * colw, y))
        y += colh
        if cap: d.text((lab_w + 4, y + 4), cap, fill=(40, 40, 40), font=font(12)); y += 24
        else: y += 6
    if note: d.multiline_text((12, y + 4), note, fill=(60, 60, 60), font=font(13))
    S.save(os.path.join(OUT, fn), quality=90)
G = jl(W + '/gates_out.json') if os.path.exists(W + '/gates_out.json') else None
sheet('HVFINAL_A_whole_character.jpg', 'A. Halvren RP3 final whole-character references (HB2 + HF2 + HP-B + HE2 / HR2), neutral clay, orthographic, 178 cm',
      [('%s\n%s' % (c, NM[c]), [img('A_%s' % c, v) for v in ('front', 'tqf', 'side', 'tqr', 'rear')], None) for c in H], ['front', 'front 3/4', 'side', 'rear 3/4', 'rear'], colw=330, colh=420)
for c in H:
    rows = [('ears visible', [img('B_%s_vis' % c, v) for v in ('front',)], None), ('ears hidden', [img('B_%s_hid' % c, v) for v in ('front',)], None)]
    sheet('HVFINAL_B_lineup_%s.jpg' % c, 'B. Matched lineup %s at 178 cm: %s (ears visible = production references uniformly scaled to 178 cm; hidden = R-6 at 178 cm, ear collapsed)' % (c, ' | '.join(LAB[k] for k in ORD)),
          rows, ['front'], colw=1400, colh=700)
    hr = []
    for mode in ('vis', 'hid'):
        for v in ('hf', 'hs'): hr.append(('%s %s' % ('ears visible' if mode == 'vis' else 'ears hidden', 'front' if v == 'hf' else 'side'), [img('BH_%s_%s_%s' % (c, mode, k), v) for k in ORD], None))
    sheet('HVFINAL_B_heads_%s.jpg' % c, 'B. Matched heads %s: %s' % (c, ' | '.join(LAB[k] for k in ORD)), hr, [LAB[k] for k in ORD], colw=300)
    sheet('HVFINAL_B_lineup_side_%s.jpg' % c, 'B. Matched lineup %s at 178 cm -- side and front 3/4 (ears visible / hidden)' % c,
          [('visible side', [img('B_%s_vis' % c, 'side')], None), ('visible 3/4', [img('B_%s_vis' % c, 'tqf')], None), ('hidden side', [img('B_%s_hid' % c, 'side')], None), ('hidden 3/4', [img('B_%s_hid' % c, 'tqf')], None)], [' '], colw=1400, colh=600)
rows = []
for c in H:
    for v in ('front', 'face', 'pelvis'):
        rows.append(('%s %s' % (c, v), [img('C_%s_r6' % c, v), img('C_%s_fam' % c, v), img('C_%s_final' % c, v)], None))
sheet('HVFINAL_C_regression.jpg', 'C. Regression: accepted R-6 source | accepted HB2 + HF2 + HP-B family realization | final (heat = |final - family|: amber -> red up to 0.8 cm; blue = HE2 ear branch)', rows,
      ['accepted R-6 source (MPFB human ear)', 'accepted family realization', 'final reference'], colw=380,
      note='Outside the frozen HE2 ear branch (blue) and the frozen HR2 root zone (214 / 220 head-skin vertices within 0.45 cm of the branch: root lowering), the final equals the accepted family realization exactly (dV 0).')
sheet('HVFINAL_D_ear_integration.jpg', 'D. Ear integration: HE2 HVEAR3 + HR2 on the final references (grazing light): front 3/4 | side | true rear 3/4 | lower-rear 3/4',
      [('%s' % c, [img('D_%s' % c, v) for v in ('etq', 'side', 'rq', 'lr')], None) for c in H], ['front 3/4', 'side', 'true rear 3/4', 'lower-rear 3/4'], colw=360)
DS = jl(OUT + '/../HALVREN_FINAL_deformation_summary.json') if os.path.exists(OUT + '/../HALVREN_FINAL_deformation_summary.json') else {}
rows = []
for c in H:
    P = DS.get(c, {}).get('poses', {})
    rows.append(('%s front' % c, [img('E_%s_%s' % (c, p), 'front') for p in EP], ' | '.join('%s %d/%d' % (p.split('_')[0], P[p]['final_flipped'], P[p]['marchfolk_v005_flipped']) for p in EP if p in P)))
    rows.append(('%s side' % c, [img('E_%s_%s' % (c, p), 'side') for p in EP], None))
sheet('HVFINAL_E_deformation.jpg', 'E. Deformation stress (Standard v1; flipped faces red; caption: final / Marchfolk v005 flips)', rows, list(EP), colw=300)
print('SHEETS_DONE', sorted(os.listdir(OUT)))
