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
# ---------------- B lineups (each figure rotated in place so the row camera sees its front / front 3/4 / side; spacing 62 cm)
ROT = dict(front=0.0, tqf=45.0, side=90.0)
def rot(V, deg):
    t = np.radians(deg); c0 = np.array([np.median(V[:, 0]), np.median(V[:, 1])]); X = V[:, :2] - c0; R = np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])
    V = V.copy(); V[:, :2] = X @ R.T + c0; return V
for c in H:
    for mode in ('vis', 'hid'):
        Vs, Qs, off = [], [], 0; heads = []
        for k in ORD:
            if mode == 'vis': z = np.load(FINAL(c) if k == 'HV' else VIS[c][k]); V = norm178(z['V'])
            else: z = np.load('%s/he/%s_earhidden.npz' % (W, H[c] if k == 'HV' else HID[c][k])); V = norm178(z['V'])
            Vs.append(V); Qs.append(np.asarray(z['Q'])); heads.append(np.array([0, np.median(V[:, 1]), 178 - 12]))
        cx = 2 * 62.0
        for vn, deg in ROT.items():
            VV, QQ, off = [], [], 0
            for i, V in enumerate(Vs):
                X = rot(V, deg); X[:, 0] += i * 62.0; VV.append(X); QQ.append(Qs[i] + off); off += len(X)
            job('B2_%s_%s_%s' % (c, mode, vn), np.concatenate(VV), np.concatenate(QQ), None, [('row', (0, 1, 0.02), (cx, 0, 89), 160)], px=1400, env=ENV)
        for i, k in enumerate(ORD):
            job('BH_%s_%s_%s' % (c, mode, k), Vs[i], Qs[i], None, [('hf', (0, 1, 0.03), heads[i], 14), ('hs', (1, 0.15, 0.03), heads[i], 14)], px=420, env=ENV)
# ---------------- C regression
for c in H:
    z = np.load(FINAL(c)); F = np.load('/tmp/claude-0/rt/hv/hpe/fam/%s_fam.npz' % H[c]); r6 = np.load('/home/claude/wayfarer-design/reviews/reference-assets/r6/%s_r6.npz' % H[c])
    v = z['v005_to_branch']; ok = v >= 0; d = np.zeros(len(z['V'])); d[v[ok]] = np.linalg.norm(z['V'][v[ok]].astype(float) - F['V'][ok].astype(float), axis=1)
    d[z['part'] != 'v005'] = np.nan
    col = np.tile(GREY, (len(z['V']), 1)); hot = np.nan_to_num(d) > 1e-4; t = np.clip(np.nan_to_num(d) / 0.8, 0, 1)[:, None]
    col[hot] = (1 - t[hot]) * np.array([0.95, 0.75, 0.2]) + t[hot] * np.array([0.85, 0.1, 0.1]); col[np.isnan(d)] = [0.35, 0.55, 0.9]
    Vz = z['V'].astype(float); hd = np.array([0, np.median(Vz[:, 1]), Vz[:, 2].max() - 12]); pel = np.array([0, np.median(Vz[:, 1]), 0.52 * Vz[:, 2].max()]); bv = Vz[z['part'] != 'v005']; er = bv[bv[:, 0] > 0].mean(0); Cq = QK.cams(H[c])
    vw = [('front', (0, 1, 0.02), (0, np.median(Vz[:, 1]), 89), 96), ('side', (1, 0, 0.02), (0, np.median(Vz[:, 1]), 89), 96), ('face', (0.35, 1, 0.05), hd, 14), ('pelvis', (0.4, 1, 0.05), pel, 34), ('root', (1, 0.1, 0.05), er, 6), ('rootr', Cq['rq'][0], Cq['rq'][1], Cq['rq'][2])]
    job('C3_%s_final' % c, Vz, z['Q'], col, vw, env=ENV); job('C3_%s_fam' % c, F['V'], F['Q'], None, vw, env=ENV)
    Fr = np.asarray(r6['F']); job('C3_%s_r6' % c, r6['V'], Fr, None, vw, env=ENV)
# ---------------- D ear integration
for c in H:
    z = np.load(FINAL(c)); C = QK.cams(H[c]); vw = [(n, C[n][0], C[n][1], C[n][2]) for n in ('etq', 'side', 'rq', 'lr')]
    job('D_%s' % c, z['V'], z['Q'], None, vw, px=560, env=dict(RENDER_LIGHTING='STUDIO:rim.sl', RENDER_SPEC='1'))
# ---------------- E deformation stress: per configuration the five worst Standard v1 poses by final flipped faces + the HR2-relevant head poses
DSJ = jl(OUT + '/../HALVREN_FINAL_deformation_summary.json'); EPS = {}
for c in H:
    P = DSJ[c]['poses']; EPS[c] = sorted(P, key=lambda p: -P[p]['final_flipped'])[:5] + ['neck_rot45', 'neck_flex30']
    Q = np.load(FINAL(c))['Q']; z0 = np.load(FINAL(c)); earv = np.where(z0['part'] != 'v005')[0]
    for p in EPS[c]:
        X = np.load('%s/def/%s_%s_final.npz' % (W, p, H[c])); col = np.tile(GREY, (len(X['V']), 1)); fl = np.asarray(X['flip']); V = X['V'].astype(float)
        fv = np.unique(np.asarray(Q)[fl].ravel()) if fl.dtype != bool else np.unique(np.asarray(Q)[fl].ravel())
        if len(fv): col[fv] = [0.9, 0.1, 0.1]
        cz = np.array([np.median(V[:, 0]), np.median(V[:, 1]), 89])
        if p.startswith('neck'): j = V[earv].mean(0); jd = (1, 0.3, 0.1); jh = 9
        else:
            qf = np.asarray(Q)[fl]; a, b_, d_ = V[qf[:, 0]], V[qf[:, 1]], V[qf[:, 2]]; nrm = np.cross(b_ - a, d_ - a); nrm /= np.linalg.norm(nrm, axis=1)[:, None] + 1e-12
            j = V[fv].mean(0); jd = -nrm.mean(0); jd = jd / (np.linalg.norm(jd) + 1e-9) if np.linalg.norm(jd) > 0.2 else np.array([0.5, 1, 0.15])
            ext = np.percentile(np.linalg.norm(V[fv] - j, axis=1), 90); jh = float(np.clip(1.4 * ext + 2, 5, 14))
        job('E3_%s_%s' % (c, p), V, Q, col, [('front', (0.3, 1, 0.05), cz, 96), ('close', jd, j, jh)], px=560, env=ENV)
if os.environ.get('SKIP_RENDER') != '1':
    jobs = [j for j in jobs if os.environ.get('FORCE') == '1' or not all(os.path.exists('%s/%s_%s.png' % (TMP, j[0][6], v.split(':')[0])) for v in j[0][7].split(';'))]
    print('render jobs', len(jobs))
    with ThreadPoolExecutor(3) as ex: list(ex.map(lambda j: subprocess.run(j[0], env=j[1], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL), jobs))
import textwrap
CROP_ROW = (0, 262, 1400, 1118)        # z = 187 .. -8 cm of the 320 cm lineup frame
def imgc(tag, v, box=CROP_ROW): return img(tag, v).crop(box)
def sheet(fn, title, rows, heads, colw=300, note=None, lab_w=170, colh=None, tw=None):
    colh = colh or colw; ncol = max(len(r[1]) for r in rows); Wd = lab_w + ncol * colw; tw = tw or max(60, int(Wd / 11.2))
    tl = textwrap.wrap(title, tw); nt = [l for para in (note or '').split('\n') for l in (textwrap.wrap(para, int(Wd / 7.3)) or [''])] if note else []
    top = 20 + 24 * len(tl) + 10
    S = Image.new('RGB', (Wd, top + 30 + sum(colh + (24 if r[2] else 6) for r in rows) + 19 * len(nt) + 16), 'white'); d = ImageDraw.Draw(S)
    for k, l in enumerate(tl): d.text((12, 12 + 24 * k), l, fill=(0, 0, 0), font=font(18, True))
    y = top
    for i, h_ in enumerate(heads): d.text((lab_w + i * colw + 4, y), h_, fill=(0, 0, 0), font=font(13, True))
    y += 26
    for lb, ims, cap in rows:
        d.multiline_text((8, y + colh // 2 - 20), '\n'.join(textwrap.wrap(lb, 18)) if '\n' not in lb else lb, fill=(0, 0, 0), font=font(14, True))
        for i, im in enumerate(ims): S.paste(im.resize((colw, int(round(colw * im.size[1] / im.size[0]))) if colh is None else (colw, colh)), (lab_w + i * colw, y))
        y += colh
        if cap:
            for i, cc in enumerate(cap if isinstance(cap, list) else [cap]): d.text((lab_w + i * colw + 4, y + 4), cc, fill=(40, 40, 40), font=font(12))
            y += 24
        else: y += 6
    for k, l in enumerate(nt): d.text((12, y + 4 + 19 * k), l, fill=(60, 60, 60), font=font(13))
    S.save(os.path.join(OUT, fn), quality=90)
sheet('HVFINAL_A_whole_character.jpg', 'A. Halvren RP3 final whole-character references (HB2 + HF2 + HP-B + HE2 HVEAR3 / HR2, TRI-HV1), neutral clay, orthographic, 178 cm',
      [('%s\n%s' % (c, NM[c]), [img('A_%s' % c, v) for v in ('front', 'tqf', 'side', 'tqr', 'rear')], None) for c in H], ['front', 'front 3/4', 'side', 'rear 3/4', 'rear'], colw=330, colh=420, lab_w=190)
LH = 1400 * 856 // 1400
for c in H:
    for mode, ml in (('vis', 'ears visible: production references (Marchfolk v005, Halvren final, frozen Fenn / Aelari / Vael), uniformly scaled to 178 cm about the ground'),
                     ('hid', 'ears hidden: hm08 R-6 sources re-solved at 178 cm with the external ear collapsed (accepted hidden-ear method)')):
        sheet('HVFINAL_B_lineup_%s_%s.jpg' % (c, mode), 'B. Matched lineup %s, %s -- left to right: %s; same camera, orthographic' % (c, ml, ' | '.join(LAB[k] for k in ORD)),
              [(vl, [imgc('B2_%s_%s_%s' % (c, mode, v), 'row')], None) for v, vl in (('front', 'front'), ('tqf', 'front 3/4'), ('side', 'side'))], [' '], colw=1400, colh=856)
    hr = []
    for mode in ('vis', 'hid'):
        for v in ('hf', 'hs'): hr.append(('%s %s' % ('ears visible' if mode == 'vis' else 'ears hidden', 'front' if v == 'hf' else 'side'), [img('BH_%s_%s_%s' % (c, mode, k), v) for k in ORD], None))
    sheet('HVFINAL_B_heads_%s.jpg' % c, 'B. Matched heads %s at 178 cm (same camera): %s -- rows 1-2 ears visible, rows 3-4 ears hidden' % (c, ' | '.join(LAB[k] for k in ORD)), hr, [LAB[k] for k in ORD], colw=300)
for c in H:
    rows = [('%s %s' % (c, vl), [img('C3_%s_r6' % c, v), img('C3_%s_fam' % c, v), img('C3_%s_final' % c, v)], None)
            for v, vl in (('front', 'body'), ('face', 'face'), ('pelvis', 'pelvis'), ('root', 'ear root side'), ('rootr', 'ear root rear'))]
    sheet('HVFINAL_C_regression_%s.jpg' % c, 'C. Regression %s: accepted R-6 source | accepted HB2 + HF2 + HP-B family realization | final reference. Heat on the final = |final - family|: amber -> red up to 0.8 cm; blue = frozen HE2 ear branch' % c, rows,
          ['accepted R-6 source (MPFB human ear)', 'accepted family realization', 'final reference'], colw=380,
          note='Outside the frozen HE2 ear branch (blue) and the frozen HR2 root zone (%s head-skin vertices, all within 0.45 cm of the branch: HR2 root lowering, part of the frozen HE2 V hash), the final equals the accepted family realization exactly (dV = 0 on every other vertex).' % ('214' if c == 'c1' else '220'))
sheet('HVFINAL_D_ear_integration.jpg', 'D. Ear integration: frozen HE2 HVEAR3 + HR2 on the final references (grazing light): front 3/4 | side | true rear 3/4 | lower-rear 3/4',
      [('%s' % c, [img('D_%s' % c, v) for v in ('etq', 'side', 'rq', 'lr')], None) for c in H], ['front 3/4', 'side', 'true rear 3/4', 'lower-rear 3/4'], colw=360)
for c in H:
    P = DSJ[c]['poses']; cap = lambda p: '%d / %d / %d' % (P[p]['final_flipped'], P[p]['family_flipped'], P[p]['marchfolk_v005_flipped'])
    rows = [('%s full body' % c, [img('E3_%s_%s' % (c, p), 'front') for p in EPS[c]], [cap(p) for p in EPS[c]]), ('%s joint / ear close-up' % c, [img('E3_%s_%s' % (c, p), 'close') for p in EPS[c]], None)]
    sheet('HVFINAL_E_deformation_%s.jpg' % c, 'E. Deformation stress %s (Standard v1 18-pose suite): the five worst poses by flipped faces + the HR2-relevant head poses; flipped faces red; caption = flipped faces final / accepted family / Marchfolk v005. Final - family new flips and new self-intersections = 0 on every pose.' % c,
          rows, EPS[c], colw=250)
print('SHEETS_DONE', sorted(os.listdir(OUT)))
