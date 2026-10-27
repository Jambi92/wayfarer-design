# cf_sheets.py WORK : order 2de0e28 §13 author sheets 1-12 (identical cameras, true scale; production family realizations unless stated).
import sys, os, json, subprocess, numpy as np, scipy.sparse as sp
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import fn_face_metrics as FM
W = sys.argv[1]; C = W + '/cf'; T = '/home/claude/wayfarer-design/tools/rac/rp/grask_rigprep_v001/render_attr.py'; BP = '/home/claude/stc/bin/python3'
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FN_ = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; mono = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 12)
f = lambda n, b=False: ImageFont.truetype(FB if b else FN_, n); OV = C + '/ov'; SH = C + '/sheets'; os.makedirs(OV, exist_ok=True); os.makedirs(SH, exist_ok=True); CLAY = np.array([0.80, 0.77, 0.73])
RA = '/home/claude/wayfarer-design/reviews/reference-assets/r6'; PA = W + '/partA'
EV = json.load(open(C + '/CF_hidden_ear_eval.json')); EX = json.load(open(C + '/CF_expression_sanity.json'))
def render(V, Q, col, tg, vs, wire='0', px=500):
    o = OV + '/%s.npz' % tg
    if not os.path.exists(OV + '/%s_%s.png' % (tg, vs.split(';')[-1].split(':')[0])):
        np.savez(o, V=V, Q=Q); np.save(o[:-4] + '_c.npy', np.asarray(col, np.float32))
        subprocess.run([BP, T, '--', o, o[:-4] + '_c.npy', OV, tg, vs, wire, str(px)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, env=dict(os.environ, WIRE_T='0.00010'))
        os.remove(o); os.remove(o[:-4] + '_c.npy')
def img(tg, v, w, h=None): return Image.open('%s/%s_%s.png' % (OV, tg, v)).convert('RGB').resize((w, h or w), Image.LANCZOS)
def vs_(views): return ';'.join('%s:%s:%s:%g' % (n, ','.join('%.4f' % x for x in d), ','.join('%.3f' % x for x in c), h) for n, d, c, h in views)
# bodies: family realizations (ID -> (fam npz, r6))
CF = {'c1': [('source', W + '/cand/FNL4_fam.npz', RA + '/FNL4_r6.npz')] + [('CF%d' % i, '%s/fam/FNL4-CF%d_fam.npz' % (C, i), '%s/cand/FNL4-CF%d/FNL4-CF%d_r6.npz' % (C, i, i)) for i in (1, 2, 3)],
      'c2': [('source', W + '/cand/FNF181_fam.npz', RA + '/FNF181_r6.npz')] + [('CF%d' % i, '%s/fam/FNF181-CF%d_fam.npz' % (C, i), '%s/cand/FNF181-CF%d/FNF181-CF%d_r6.npz' % (C, i, i)) for i in (1, 2, 3)]}
HUM = {'c1': [('MFM181', PA + '/cmp/MFM181_r6.npz'), ('SGM181', PA + '/cmp/SGM181_r6.npz')], 'c2': [('MFF181', PA + '/cmp/MFF181_r6.npz'), ('SGF181', PA + '/cmp/SGF181_r6.npz')]}
fz0 = np.load(W + '/cand/FNL4_fam.npz'); Qf = np.asarray(fz0['Q']); M = sp.csr_matrix((fz0['M_data'], fz0['M_indices'], fz0['M_indptr']), shape=tuple(fz0['M_shape'])); si = fz0['src_index']
z0 = np.load(RA + '/FNL4_r6.npz'); EARf = (M @ z0['w_ears'][si].astype(float)) > 0.05; nV = len(EARf)
A = sp.coo_matrix((np.ones(4 * len(Qf)), (Qf.ravel(), np.roll(Qf, -1, 1).ravel())), shape=(nV, nV)).tocsr(); A = ((A + A.T) > 0).astype(float); deg = np.asarray(A.sum(1)).ravel()
def hide(V):
    X = V.copy()
    for _ in range(500): X[EARf] = (A @ X)[EARf] / deg[EARf, None]
    return X
def head_c(r6): return np.array(json.loads(str(np.load(r6)['joints']))['head'][0]) + np.array([0, 4.0, 8.5])
FV = lambda hc: [('front', (0, 1, 0.05), hc, 13), ('profile', (1, 0.03, 0), hc + [0, -3, 0], 14), ('q3', (0.6, 0.8, 0.05), hc, 13)]
famV = {}
for cfg in CF:
    for tag, fp, r6 in CF[cfg]: famV[(cfg, tag)] = (np.load(fp)['V'].astype(float), r6)
    for n, r6 in HUM[cfg]: famV[(cfg, n)] = (M @ np.load(r6)['V'][si].astype(float), r6)     # matched humans realized through the same family map
# ---- sheets 1 / 2
for hid, sname in ((False, 'CF_1_source_vs_candidates'), (True, 'CF_2_source_vs_candidates_ears_hidden')):
    cw = 270; S = Image.new('RGB', (12 * cw + 20, 70 + 2 * (cw + 26)), 'white'); d = ImageDraw.Draw(S)
    d.text((10, 8), 'Fenn craniofacial source candidates — current source | CF1 restrained | CF2 balanced | CF3 stronger; front / profile / 3-4; identical camera, true scale; family v005 realization%s' % (' — EARS HIDDEN' if hid else ' (family human auricle, not final Fenn ear)'), fill=(0, 0, 0), font=f(14, True))
    for r, cfg in enumerate(('c1', 'c2')):
        y0 = 40 + r * (cw + 26); hc = head_c(CF[cfg][0][2])
        for i, (tag, fp, r6) in enumerate(CF[cfg]):
            V = famV[(cfg, tag)][0]; V = hide(V) if hid else V; tg = 'h%s_%s_%s' % ('x' if hid else 'e', cfg, tag); render(V, Qf, np.tile(CLAY, (len(Qf), 1)), tg, vs_(FV(hc)))
            for j, v in enumerate(('front', 'profile', 'q3')): S.paste(img(tg, v, cw), (10 + (3 * i + j) * cw, y0 + 20))
            d.text((14 + 3 * i * cw, y0 + 2), '%s %s' % ({'c1': 'FNL4', 'c2': 'FNF181'}[cfg], tag), fill=(150, 20, 20), font=f(12, True))
    S.save('%s/%s.jpg' % (SH, sname), quality=85)
# ---- sheet 3: per CF, Fenn vs MF vs SG (ears hidden)
for cfg in ('c1', 'c2'):
    cw = 230; S = Image.new('RGB', (9 * cw + 20, 60 + 4 * (cw + 26) + 120), 'white'); d = ImageDraw.Draw(S)
    d.text((10, 8), 'Matched stature (~181 cm) hidden-ear face read, %s: Fenn candidate | Marchfolk | Sagekin — front / profile / 3-4 (ears collapsed; same clay, camera, composition)' % cfg, fill=(0, 0, 0), font=f(14, True))
    for r, (tag, fp, r6) in enumerate(CF[cfg]):
        y0 = 36 + r * (cw + 26)
        for i, (n, V, rr) in enumerate([(tag, famV[(cfg, tag)][0], r6)] + [(h, famV[(cfg, h)][0], hr) for h, hr in HUM[cfg]]):
            tg = 'hx_%s_%s' % (cfg, n); render(hide(V), Qf, np.tile(CLAY, (len(Qf), 1)), tg, vs_(FV(head_c(rr))))
            for j, v in enumerate(('front', 'profile', 'q3')): S.paste(img(tg, v, cw), (10 + (3 * i + j) * cw, y0 + 20))
            d.text((14 + 3 * i * cw, y0 + 2), n if i else 'Fenn %s' % tag, fill=(150, 20, 20), font=f(11, True))
        e = EV['configs'][cfg][tag]; d.text((10 + 9 * cw - 560, y0 + 4), 'systems material %d / 6, orbit share %.2f' % (e['systems_material'], e['orbit_share_of_face_residual']), fill=(0, 0, 0), font=f(11, True))
    y = 40 + 4 * (cw + 26)
    for tag in ('source', 'CF1', 'CF2', 'CF3'):
        e = EV['configs'][cfg][tag]['descriptors']; d.text((10, y), '%-6s vs MF: ' % tag + '  '.join('%s %+.2f%%' % (k.replace('_over_', '/')[:22], v['vs_MF_pct']) for k, v in e.items() if k not in ('head_height_cm',)), fill=(0, 0, 0), font=mono); y += 16
    S.save('%s/CF_3_vs_matched_humans_%s.jpg' % (SH, cfg), quality=85)
# ---- sheet 4: residual heat vs MF (head size removed)
def ramp(t):
    t = np.clip(t, 0, 1)[:, None]; return np.where(t < 0.5, (1 - 2 * t) * np.array([0.15, 0.35, 0.85]) + 2 * t * np.array([0.95, 0.9, 0.3]), (2 - 2 * t) * np.array([0.95, 0.9, 0.3]) + (2 * t - 1) * np.array([0.85, 0.1, 0.1]))
cw = 250; S = Image.new('RGB', (12 * cw + 20, 60 + 2 * (cw + 26) + 40), 'white'); d = ImageDraw.Draw(S)
d.text((10, 8), 'Face residual vs matched Marchfolk after removing head size (similarity fit on all non-ear head vertices) — blue 0 -> yellow 3 -> red >= 6 mm; ears hidden', fill=(0, 0, 0), font=f(14, True))
HEADf = (M @ z0['w_head'][si].astype(float)) > 0.5
for r, cfg in enumerate(('c1', 'c2')):
    y0 = 36 + r * (cw + 26); Vm = famV[(cfg, HUM[cfg][0][0])][0]; hc = head_c(CF[cfg][0][2])
    for i, (tag, fp, r6) in enumerate(CF[cfg]):
        V = famV[(cfg, tag)][0]; fmap = FM.procrustes(Vm[HEADf & ~EARf], V[HEADf & ~EARf]); res = np.linalg.norm(V - fmap(Vm), axis=1) * 10; res[~HEADf] = 0
        tg = 'heat_%s_%s' % (cfg, tag); render(hide(V), Qf, ramp(res[Qf].mean(1) / 6.0), tg, vs_(FV(hc)))
        for j, v in enumerate(('front', 'profile', 'q3')): S.paste(img(tg, v, cw), (10 + (3 * i + j) * cw, y0 + 20))
        d.text((14 + 3 * i * cw, y0 + 2), '%s %s' % (cfg, tag), fill=(150, 20, 20), font=f(12, True))
d.text((10, 40 + 2 * (cw + 26)), 'region RMS vs MF (mm), c1 CF2: ' + '  '.join('%s %.2f' % (k, v) for k, v in EV['configs']['c1']['CF2']['region_rms_vs_MF_mm'].items()), fill=(0, 0, 0), font=mono)
S.save(SH + '/CF_4_residual_heat.jpg', quality=85)
# ---- sheets 5-8: region close-ups
REGV = {'CF_5_cranium_forehead': [('profile', (1, 0.03, 0.05), [0, -3, 4], 10), ('front upper', (0, 1, 0.15), [0, 0, 4], 9)], 'CF_6_orbit_eye': [('front', (0, 1, 0.05), [0, 1, 1.5], 5.5), ('3-4', (0.55, 0.8, 0.05), [2, 1, 1.5], 5.5)],
        'CF_7_cheeks_midface': [('3-4', (0.65, 0.75, 0.0), [2.5, 1, -1.5], 7), ('front', (0, 1, 0.0), [0, 1, -1.5], 7)], 'CF_8_jaw_chin': [('3-4 low', (0.6, 0.75, -0.25), [2, 0, -5.5], 7.5), ('front low', (0, 1, -0.15), [0, 0, -5.5], 7.5)]}
for sname, views in REGV.items():
    cw = 260; S = Image.new('RGB', (5 * cw + 20, 50 + 2 * len(views) * (cw + 24)), 'white'); d = ImageDraw.Draw(S)
    d.text((10, 8), '%s — columns: current source | CF1 | CF2 | CF3 | matched Marchfolk; rows: c1 then c2; ears hidden; identical camera per row' % sname.replace('_', ' ')[5:], fill=(0, 0, 0), font=f(13, True))
    k = 0
    for cfg in ('c1', 'c2'):
        hc = head_c(CF[cfg][0][2]) - np.array([0, 4.0, 8.5]) + np.array([0, 0, 8.5])
        for vn, dr, off, h in views:
            y0 = 30 + k * (cw + 24); k += 1
            cols = [(t, famV[(cfg, t)][0]) for t, _, _ in CF[cfg]] + [(HUM[cfg][0][0], famV[(cfg, HUM[cfg][0][0])][0])]
            for i, (t, V) in enumerate(cols):
                tg = 'r_%s_%s_%s_%s' % (sname[:4], cfg, t, vn.replace(' ', '')); render(hide(V), Qf, np.tile(CLAY, (len(Qf), 1)), tg, vs_([('v', dr, hc + np.array(off, float), h)]), '0', 440)
                S.paste(img(tg, 'v', cw), (10 + i * cw, y0 + 18)); d.text((14 + i * cw, y0 + 2), '%s %s %s' % (cfg, t, vn), fill=(150, 20, 20), font=f(11, True))
    S.save('%s/%s.jpg' % (SH, sname), quality=85)
# ---- sheet 9: wireframe (topology unchanged)
cw = 330; S = Image.new('RGB', (4 * cw + 20, 70 + cw + 40), 'white'); d = ImageDraw.Draw(S)
d.text((10, 8), 'Topology unchanged — family v005 wire, current source vs CF2 (c1): front | profile; face topology hash identical (ec768ae2...), 57,842 V / 57,840 Q', fill=(0, 0, 0), font=f(14, True))
hc = head_c(CF['c1'][0][2])
for i, t in enumerate(('source', 'CF2')):
    tg = 'w_%s' % t; render(famV[('c1', t)][0], Qf, np.tile(CLAY, (len(Qf), 1)), tg, vs_(FV(hc)[:2]), '1', 800)
    for j, v in enumerate(('front', 'profile')): S.paste(img(tg, v, cw), (10 + (2 * i + j) * cw, 40)); d.text((14 + (2 * i + j) * cw, 44), '%s %s' % (t, v), fill=(150, 20, 20), font=f(12, True))
S.save(SH + '/CF_9_wire_topology.jpg', quality=85)
# ---- sheet 10: c1 vs c2 CF2
cw = 300; S = Image.new('RGB', (6 * cw + 20, 70 + cw + 40 + 140), 'white'); d = ImageDraw.Draw(S)
d.text((10, 8), 'Configuration 1 vs configuration 2, CF2 (same craniofacial target set; ears hidden): FNL4-CF2 | FNF181-CF2; front / profile / 3-4', fill=(0, 0, 0), font=f(14, True))
for i, cfg in enumerate(('c1', 'c2')):
    for j, v in enumerate(('front', 'profile', 'q3')): S.paste(img('hx_%s_CF2' % cfg, v, cw), (10 + (3 * i + j) * cw, 40))
y = 50 + cw; cs = EV['configuration_consistency']
for t in ('CF1', 'CF2', 'CF3'):
    d.text((10, y), '%s same signs %s; identity strength c1 %.2f / c2 %.2f; c2/c1 ratios %s' % (t, cs[t]['same_signs'], cs[t]['identity_strength_c1'], cs[t]['identity_strength_c2'], {k.replace('_over_', '/')[:18]: v for k, v in cs[t]['ratio_c2_over_c1'].items()}), fill=(0, 0, 0), font=mono); y += 18
S.save(SH + '/CF_10_config1_vs_config2.jpg', quality=85)
# ---- sheet 11: full body hidden-ear confirmation
cw = 300; S = Image.new('RGB', (8 * cw + 20, 70 + cw + 40), 'white'); d = ImageDraw.Draw(S)
d.text((10, 8), 'Full body, ears hidden: current source vs CF2 (c1 | c2) — body unchanged (max non-head change c1 %.2f mm, c2 %.2f mm; height macro held)' % (EV['configs']['c1']['CF2']['nonhead_max_change_mm'], EV['configs']['c2']['CF2']['nonhead_max_change_mm']), fill=(0, 0, 0), font=f(14, True))
BV = [('front', (0, 1, 0), np.array([0, 0, 94.0]), 96), ('profile', (1, 0, 0), np.array([0, 0, 94.0]), 96)]
k = 0
for cfg in ('c1', 'c2'):
    for t in ('source', 'CF2'):
        tg = 'b_%s_%s' % (cfg, t); render(hide(famV[(cfg, t)][0]), Qf, np.tile(CLAY, (len(Qf), 1)), tg, vs_(BV))
        for v in ('front', 'profile'): S.paste(img(tg, v, cw), (10 + k * cw, 40)); d.text((14 + k * cw, 44), '%s %s %s' % (cfg, t, v), fill=(150, 20, 20), font=f(11, True)); k += 1
S.save(SH + '/CF_11_full_body_hidden_ear.jpg', quality=85)
# ---- sheet 12: expression sanity table
rows = list(EX['bodies'].items()); exs = list(rows[0][1].keys())
S = Image.new('RGB', (1700, 80 + 18 * (len(rows) + 4)), 'white'); d = ImageDraw.Draw(S)
d.text((10, 8), 'Facial readiness sanity (MPFB expression units, diagnostic): new self-intersection pairs / of them in the orbit / faces flipped vs neutral — candidate must not exceed its current source', fill=(0, 0, 0), font=f(13, True))
d.text((10, 34), '%-16s' % 'body' + ''.join('%-24s' % e[:22] for e in exs), fill=(0, 0, 0), font=mono)
for i, (b, v) in enumerate(rows):
    d.text((10, 54 + 18 * i), '%-16s' % b + ''.join('%-24s' % ('%d / %d / %d' % (v[e]['new_selfx_pairs'], v[e]['new_selfx_in_orbit'], v[e]['flipped_faces'])) for e in exs), fill=(0, 0, 0), font=mono)
d.text((10, 60 + 18 * len(rows)), EX.get('verdict_text', ''), fill=(0, 100, 0), font=f(12, True))
S.save(SH + '/CF_12_expression_sanity.jpg', quality=88); print('cf sheets done')
