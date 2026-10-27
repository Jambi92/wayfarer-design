# sg_extra_sheets.py WORK : order c6c7940 §19 sheets 11 / 14 / 15 + the hip-station diagnostic (identical orthographic cameras across bodies).
#  Sagekin_config_comparison  SGF152-NAT | SGF178 (family) | SGF208 | SG c1 (family), true scale, front + profile; Part A share table
#  Sagekin_vs_Marchfolk_178   SGF178 vs MFF178, SG vs MFM178 (diagnostic matched comparators), clay + silhouette overlays; identity table
#  Sagekin_margin             69-station D1 + D3 + D4 + D5 margin heat: SG, SGF178 next to the frozen v005 realizations
#  Sagekin_hip_diag           lateral hip (+p side of hip_l): band end planes, counted side path, loop column -- SG family vs MF-M v005
import sys, os, json, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001')
W = sys.argv[1]; T = '/home/claude/wayfarer-design/tools/rac/rp/grask_rigprep_v001/render_attr.py'; BP = '/home/claude/stc/bin/python3'
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FN = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; f = lambda n, b=False: ImageFont.truetype(FB if b else FN, n)
OV = W + '/ov'; SH = W + '/sheets'; os.makedirs(OV, exist_ok=True); os.makedirs(SH, exist_ok=True); CLAY = np.array([0.80, 0.77, 0.73]); RA = '/home/claude/wayfarer-design/reviews/reference-assets/r6'
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
fam = lambda cid: (np.load('%s/cand/%s_fam.npz' % (W, cid))['V'].astype(float), np.load('%s/cand/%s_fam.npz' % (W, cid))['Q'])
PA = json.load(open(W + '/partA/SGF178_reference_validation.json'))
# ---------------- 14: configuration comparison (true scale)
B = [('SGF152-NAT', 'SGF152-NAT (c2 min, accepted)', r6body(RA + '/SGF152-NAT_r6.npz')), ('SGF178', 'SGF178 (c2 central, family v005)', fam('SGF178')),
     ('SGF208', 'SGF208 (c2 max, accepted)', r6body(RA + '/SGF208_r6.npz')), ('SG', 'SG (c1 central, family v005)', fam('SG'))]
VW = [('front', (0, 1, 0), np.array([0, 0, 105.0]), 108), ('profile', (1, 0, 0), np.array([0, 0, 105.0]), 108)]
for tg, _, (V, Q) in B: render(V, Q, np.tile(CLAY, (len(Q), 1)), 'cc_' + tg, vs_(VW))
cw, chh = 300, 300; S = Image.new('RGB', (8 * cw + 20, 100 + chh + 26 * 16), 'white'); d = ImageDraw.Draw(S)
d.text((10, 8), 'Sagekin central references and configuration-2 envelope — identical orthographic camera, true scale (frame 216 cm), clay, R-6 stance; front | profile', fill=(0, 0, 0), font=f(15, True))
d.text((10, 30), 'SGF178 = MF-F-R build + accepted Sagekin targets, stature re-solved to 178.00 cm: the construction base of both accepted c2 bounds (RM-OT-05A §2); SGF152-NAT = native short-adult route from the SGF178 macro', fill=(60, 60, 60), font=f(12))
for i, (tg, lab, _) in enumerate(B):
    for j, v in enumerate(('front', 'profile')): S.paste(img('cc_' + tg, v, cw, chh), (10 + (2 * i + j) * cw, 76))
    d.text((14 + 2 * i * cw, 56), '%s — %.2f cm' % (lab, PA['stature'][tg if tg != 'SG' else 'SG']), fill=(150, 20, 20), font=f(12, True))
y = 84 + chh; d.text((10, y), '%-26s %10s %10s %10s %10s  %8s   %s' % ('share of stature', 'SGF152-NAT', 'SGF178', 'SGF208', 'SG (c1)', 'within', 'c2-c1 at 178: Sagekin | Marchfolk (MFF178-MFM178)'), fill=(0, 0, 0), font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 12)); y += 18
for c in PA['continuity']:
    col = (0, 110, 0) if c['within_bounds'] else ((0, 70, 170) if c['same_pattern_as_accepted_c1'] else (170, 90, 0))
    d.text((10, y), '%-26s %10.4f %10.4f %10.4f %10.4f  %8s   %+6.2f %% | %+6.2f %%' % (c['measure'], c['SGF152_NAT'], c['SGF178'], c['SGF208'], c['SG_c1'], 'yes' if c['within_bounds'] else ('c1-pattern' if c['same_pattern_as_accepted_c1'] else '%+.2f%%' % c['excess_outside_pct']), c['sex_delta_SG_pct'], c['sex_delta_MF178_pct']),
           fill=col, font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 12)); y += 16
d.text((10, y + 4), 'green = inside [SGF152-NAT, SGF208]; blue = outside on the same side as accepted c1 SG vs SG152-NAT / SG208 (native-route allometry); orange = ratio outside, both components inside', fill=(60, 60, 60), font=f(11))
S.save(SH + '/Sagekin_config_comparison.jpg', quality=85)
# ---------------- 15: Sagekin vs Marchfolk at 178 cm (neutralised: same clay, no hair / clothing, same camera)
P = [('SGF178', fam('SGF178'), 'MFF178', r6body(W + '/partA/cmp/MFF178_r6.npz')), ('SG', fam('SG'), 'MFM178', r6body(W + '/partA/cmp/MFM178_r6.npz'))]
VW2 = [('front', (0, 1, 0), np.array([0, 0, 92.0]), 94), ('profile', (1, 0, 0), np.array([0, 0, 92.0]), 94)]
for a, (Va, Qa), b, (Vb, Qb) in P:
    render(Va, Qa, np.tile(CLAY, (len(Qa), 1)), 'sm2_' + a, vs_(VW2)); render(Vb, Qb, np.tile(CLAY, (len(Qb), 1)), 'sm2_' + b, vs_(VW2))
def sil(V, F, yaw, px=3.0, ss=3):
    a_ = np.radians(yaw); Rm = np.array([[np.cos(a_), -np.sin(a_), 0], [np.sin(a_), np.cos(a_), 0], [0, 0, 1]]); Pp = V @ Rm.T; q = px * ss; u = (Pp[:, 0] + 70) * q; v = (215 - Pp[:, 2]) * q
    im = Image.new('L', (int(140 * px) * ss, int(220 * px) * ss), 0); dr = ImageDraw.Draw(im)
    for t in F: dr.polygon([(u[t[0]], v[t[0]]), (u[t[1]], v[t[1]]), (u[t[2]], v[t[2]])], fill=255)
    return np.array(im, float).reshape(int(220 * px), ss, int(140 * px), ss).mean((1, 3)) >= 127.5
tri = lambda Q: np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]] if Q.shape[1] == 4 else Q
cw = 330; S = Image.new('RGB', (12 * cw // 2 * 2 + 20, 110 + int(cw * 220 / 140 * 0.62) + 20 * 16), 'white'); d = ImageDraw.Draw(S)
S = Image.new('RGB', (2 * (4 * cw + int(cw * 140 / 220) * 2) + 40, 470 + 16 * 14), 'white'); d = ImageDraw.Draw(S)
d.text((10, 8), 'Sagekin vs Marchfolk at matched stature (178 cm), neutralised (same clay, no hair / clothing / culture), identical cameras — clay front / profile | silhouette overlays 3 px/cm', fill=(0, 0, 0), font=f(15, True))
d.text((10, 30), 'overlay: grey both, red Sagekin only, blue Marchfolk only. MFF178 / MFM178 are diagnostic comparators (accepted MF-F-R / MF-M-R builds, stature re-solved to 178), not reference assets', fill=(60, 60, 60), font=f(12))
x0 = 10
for a, (Va, Qa), b, (Vb, Qb) in P:
    for j, (tg, v) in enumerate((('sm2_' + a, 'front'), ('sm2_' + b, 'front'), ('sm2_' + a, 'profile'), ('sm2_' + b, 'profile'))):
        S.paste(img(tg, v, cw), (x0 + j * cw, 74)); d.text((x0 + 4 + j * cw, 56), '%s %s' % (tg[4:], v), fill=(150, 20, 20), font=f(12, True))
    for k, yaw in enumerate((0, 90)):
        A = sil(Va, tri(Qa), yaw); Bm = sil(Vb, tri(Qb), yaw); o = np.full(A.shape + (3,), 255, np.uint8); o[A & Bm] = (170, 170, 170); o[A & ~Bm] = (220, 30, 30); o[Bm & ~A] = (30, 80, 220)
        ow = int(cw * 140 / 220 * 1.0); S.paste(Image.fromarray(o).resize((ow, cw)), (x0 + 4 * cw + k * ow, 74)); d.text((x0 + 4 * cw + k * ow + 4, 56), 'overlay ' + ('front' if yaw == 0 else 'side'), fill=(150, 20, 20), font=f(12, True))
    x0 += 4 * cw + 2 * int(cw * 140 / 220) + 20
y = 90 + cw; mono = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 12)
d.text((10, y), '%-16s %14s %14s %14s %14s' % ('share of stature', 'c2 SGF178-MFF178', 'c1 SG-MFM178', 'RM-OT-05 c2 152', 'RM-OT-05 c2 208'), fill=(0, 0, 0), font=mono); y += 18
for r in PA['identity_vs_marchfolk_178']:
    d.text((10, y), '%-16s %13.2f%% %13.2f%% %14s %14s' % (r['measure'], r['c2_SGF178_vs_MFF178_pct'], r['c1_SG_vs_MFM178_pct'], ('%+.2f%%' % r['closure_c2_152']) if 'closure_c2_152' in r else '-', ('%+.2f%%' % r['closure_c2_208']) if 'closure_c2_208' in r else '-'), fill=(0, 0, 0), font=mono); y += 16
d.text((10, y + 4), 'canon (SAGEKIN_V1 §3): slightly longer limbs, slightly shorter torso, reduced ribcage depth, human hands / feet / auricle; overlap with Marchfolk intended — every direction replicates the accepted 152 / 208 rows, magnitudes in range', fill=(60, 60, 60), font=f(11))
S.save(SH + '/Sagekin_vs_Marchfolk_178.jpg', quality=85)
# ---------------- 11: margin heat table
VAL = {'SG': W + '/val/SG_fam_validator_v2_D4_D5.json', 'SGF178': W + '/val/SGF178_fam_validator_v2_D4_D5.json'}
for k in ('MF-M-R', 'MF-F-R', 'SK208-C1R', 'SKF208'): VAL[k] = '/tmp/claude-0/rt/v5/val/%s_v005_validator_v2_D4_D5.json' % k
VV = {k: json.load(open(p))['stations'] for k, p in VAL.items()}; names = sorted(VV['SG'])
cols = list(VAL); cw2 = 92; S = Image.new('RGB', (2 * (180 + len(cols) * cw2 + 10) + 20, 80 + ((len(names) + 1) // 2) * 17), 'white'); d = ImageDraw.Draw(S)
d.text((10, 8), 'Sagekin 69-station margin table — D1 + D3 + D4 + D5 (authoritative), margin = loops - contract minimum; frozen v005 realizations for reference', fill=(0, 0, 0), font=f(14, True))
def mc(m): return (200, 30, 30) if m < 0 else ((235, 150, 40) if m == 0 else ((240, 220, 90) if m == 1 else (120, 200, 120)))
half = (len(names) + 1) // 2
for h in range(2):
    xo = 10 + h * (180 + len(cols) * cw2 + 10)
    for j, c in enumerate(cols): d.text((xo + 180 + j * cw2, 34), c, fill=(0, 0, 0), font=f(10, True))
    for i, nm in enumerate(names[h * half:(h + 1) * half]):
        y = 52 + i * 17; d.text((xo, y + 2), nm, fill=(0, 0, 0), font=f(11))
        for j, c in enumerate(cols):
            r = VV[c][nm]; m = r['margin']; firm = r['firm_D1_D3']; d.rectangle([xo + 180 + j * cw2, y, xo + 180 + (j + 1) * cw2 - 3, y + 15], fill=mc(m) if firm else (200, 30, 30))
            d.text((xo + 184 + j * cw2, y + 2), '%d/%d %+d%s' % (r['loops_v2'], r['required'], m, '' if firm else ' FAIL'), fill=(0, 0, 0), font=f(10))
S.save(SH + '/Sagekin_margin.jpg', quality=88)
# ---------------- hip diagnostic (hip_l +p side) -- the probe lands on the forearm hanging beside the hip
HD = json.load(open(W + '/hipdiag/hip_diag.json')); from core3lib import stations, unit
D6S = json.load(open(W + '/d6/D6_effect_summary.json'))
cw = 430; S = Image.new('RGB', (4 * cw + 30, 210 + cw), 'white'); d = ImageDraw.Draw(S)
d.text((10, 8), 'hip_l, band side +p — the probe ball (R 12.3 cm) reaches the FOREARM hanging beside the hip in the R-6 stance: the "hip" count on that side is a forearm count', fill=(0, 0, 0), font=f(15, True))
d.text((10, 30), 'blue / yellow alternate = faces on the validator +p side path (Dijkstra between the two selected band-end vertices); green = hip band slab |(v - c).d| <= W on the lateral half; red = band end planes; front view | forearm alone seen from the hip', fill=(60, 60, 60), font=f(12))
for i, (lab, p, lp) in enumerate((('SG', W + '/cand/SG_fam.npz', W + '/audit/SG_fam_loops.npz'), ('MF-M-R', '/tmp/claude-0/rt/v5/cand/MF-M-R_v005.npz', '/tmp/claude-0/rt/v5/audit/MF-M-R_v005_loops.npz'))):
    z = np.load(p); V = z['V'].astype(float); Q = z['Q']; meta = json.loads(str(z['meta'])); St = {x[0]: x for x in stations(meta)}; _, c, dd, Wd, Rr, need, _ = St['hip_l']
    s_ = (V[:, 2].max() - V[:, 2].min()) / 173.143; Wd *= s_; c = np.asarray(c); dd = unit(np.asarray(dd)); ax = (V - c) @ dd; pp = unit(np.cross(dd, [0, 1.0, 0])); lat = (V - c) @ pp
    col = np.tile(CLAY, (len(V), 1)); col[(np.abs(ax) <= Wd) & (lat > 0)] = (0.55, 0.85, 0.55); col[(np.abs(np.abs(ax) - Wd) < 0.15) & (lat > 0)] = (0.9, 0.1, 0.1)
    path = HD[lab]['stations']['hip_l']['sides']['+p']['path']; fc = col[Q].mean(1); pv = {v: k for k, v in enumerate(path)}
    for fi in np.nonzero(np.isin(Q, path).any(1))[0]:
        k = min(pv[v] for v in Q[fi] if v in pv); fc[fi] = (0.05, 0.3, 0.95) if k % 2 == 0 else (0.95, 0.85, 0.1)
    cc = c + pp * 9; tg = 'hipd_%s' % lab; zl = np.load(lp, allow_pickle=True)['zone']
    render(V, Q, fc, tg, vs_([('front', (0, 1, 0), cc, 14)]), '1', 800)
    am = np.isin(zl[Q], ['arm', 'hand']).all(1) & (V[Q].mean(1)[:, 0] > 0); pc = V[path].mean(0)            # forearm alone, seen from the hip (medial) side: the face the probe samples
    render(V, Q[am], fc[am], tg + '_arm', vs_([('medial', (-1, 0, 0), pc, 9)]), '1', 800)
    S.paste(img(tg, 'front', cw), (10 + 2 * i * cw, 80)); S.paste(img(tg + '_arm', 'medial', cw), (10 + (2 * i + 1) * cw, 80))
    d.text((14 + (2 * i + 1) * cw, 84), 'forearm only, seen from the hip side', fill=(0, 0, 160), font=f(11, True))
    sd = HD[lab]['stations']['hip_l']['sides']['+p']
    d.text((14 + 2 * i * cw, 58), '%s: +p path %d edges, %d counted, path zones %s; station %s' % (lab, len(path) - 1, sd['counted'], sorted(set(zl[path].tolist())), 'FAIL 4 / 5' if lab == 'SG' else 'PASS 6 / 5'), fill=(150, 20, 20), font=f(12, True))
y = 92 + cw
for t in ('The SAME foreign-segment artefact is present on all six family realizations (MF-M, MF-F, SK-C1R, SK-F, SG, SGF178): hip +p (lateral) samples lowerarm / hand, and elbow -p (medial) samples the trunk (spine_02).',
          'It passed unnoticed because the forearm carried >= 5 loops inside the band on the other bodies; the longer Sagekin forearm (accepted lowerarm-length target) spaces the same forearm loops wider, so SG counts 4. The hip is not measured by that side.',
          'Proposed D6 (diagnostic, NOT applied to the verdict): a non-digit band side is undefined when a selected endpoint\'s dominant skin bone is not one of the station\'s own bones (hip: pelvis, spine_01, thigh).',
          'D6 effect: SG hip 4 -> 6 (other sides 6 / 6), SG 67 -> 69 / 69; SGF178, MF-M, MF-F, SK-C1R, SK-F stay 69 / 69; no station verdict or loop count is lowered anywhere (%s).' % ', '.join('%s %d' % (k, v['firm_D1_D3_D4_D5_D6']) for k, v in D6S.items())):
    d.text((10, y), t, fill=(0, 0, 0), font=f(12)); y += 18
S.save(SH + '/Sagekin_hip_diag.jpg', quality=88); print('extra sheets done')
