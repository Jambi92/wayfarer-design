# v5_sheets.py WORK : order 33a2dfe §17 visual evidence for the final MPFB Family Base v005 (toe-2 dorsal racetrack), identical cameras per configuration.
import sys, os, json, subprocess, numpy as np, trimesh
from PIL import Image, ImageDraw, ImageFont
W = sys.argv[1]; BP = '/home/claude/stc/bin/python3'; T = '/home/claude/wayfarer-design/tools/rac/rp/grask_rigprep_v001/render_attr.py'
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001')
from v004_lib import NAT, R6, CFG, csr
from core3lib import quality, topo
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FN = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; f = lambda n, b=False: ImageFont.truetype(FB if b else FN, n)
OV = W + '/ov'; SH = W + '/sheets'; os.makedirs(OV, exist_ok=True); os.makedirs(SH, exist_ok=True); CLAY = np.array([0.80, 0.77, 0.73])
V4P = '/tmp/claude-0/rt/v4/cand/%s_v004.npz'; V5P = W + '/cand/%s_v005.npz'
LAB = {'MF-M-R': 'Marchfolk M', 'MF-F-R': 'Marchfolk F', 'SK208-C1R': 'Skarn M C1R', 'SKF208': 'Skarn F'}
def render(V, Q, col, tg, vs, wire='0', px=420):
    if os.path.exists(OV + '/%s_%s.png' % (tg, vs.split(';')[-1].split(':')[0])): return
    o = OV + '/%s.npz' % tg; np.savez(o, V=V, Q=Q); np.save(o[:-4] + '_c.npy', np.asarray(col, np.float32))
    subprocess.run([BP, T, '--', o, o[:-4] + '_c.npy', OV, tg, vs, wire, str(px)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, env=dict(os.environ, WIRE_T='0.00010'))
    os.remove(o); os.remove(o[:-4] + '_c.npy')
def img(tg, v, cell): return Image.open('%s/%s_%s.png' % (OV, tg, v)).convert('RGB').resize((cell, cell), Image.LANCZOS)
def vs_(views): return ';'.join('%s:%s:%s:%g' % (n, ','.join('%.4f' % x for x in d), ','.join('%.3f' % x for x in c), h) for n, d, c, h in views)
def ramp(t):
    t = np.clip(t, 0, 1)[:, None]; return np.where(t < 0.5, (1 - 2 * t) * np.array([0.15, 0.35, 0.85]) + 2 * t * np.array([0.95, 0.9, 0.3]), (2 - 2 * t) * np.array([0.95, 0.9, 0.3]) + (2 * t - 1) * np.array([0.85, 0.1, 0.1]))
def sheet(title, sub, rows, cell, out, notes=()):
    nc = max(len(r) for r in rows); S = Image.new('RGB', (20 + nc * cell, 70 + len(rows) * (cell + 26) + 18 * len(notes)), 'white'); d = ImageDraw.Draw(S)
    d.text((10, 8), title, fill=(0, 0, 0), font=f(14, True)); d.text((10, 30), sub, fill=(60, 60, 60), font=f(11))
    for i, cells in enumerate(rows):
        y = 52 + i * (cell + 26)
        for j, (tg, v, cap) in enumerate(cells): S.paste(img(tg, v, cell), (10 + j * cell, y + 20)); d.text((14 + j * cell, y + 3), cap, fill=(150, 20, 20), font=f(11, True))
    for k, n in enumerate(notes): d.text((10, 56 + len(rows) * (cell + 26) + 18 * k), n, fill=(30, 30, 30), font=f(11))
    S.save(out, quality=85)
z5 = np.load(W + '/v5core.npz'); z4 = np.load('/tmp/claude-0/rt/v4/v4core.npz'); log5 = json.loads(str(z5['log'])); nb = int(z5['n_base']); n3 = int(z5['n_v003']); rc5 = z5['row_class']
t2v4 = n3 + np.nonzero(np.char.startswith(z4['ring_name'], 'toe2'))[0]; rt5 = np.arange(nb, csr(z5).shape[0]); v5c = [t['val5_corner'] for t in log5['turns']]; v3c = [t['centre'] for t in log5['turns']]
LA = json.load(open(W + '/audit/MPFB_v005_toe2_local_audit.json')); TU = json.load(open(W + '/audit/T4_union_v003_tw0_v004_v005.json'))
for cid in CFG:
    c4 = np.load(V4P % cid); c5 = np.load(V5P % cid); V4, Q4, V5, Q5 = c4['V'], c4['Q'], c5['V'], c5['Q']; meta = json.loads(str(c5['meta'])); H = {k: np.array(v) for k, v in meta['heads'].items()}
    JC = {k: np.array(v) for k, v in meta['joint_cubes'].items()}; tg = cid.replace('-', ''); st = V5[:, 2].max() - V5[:, 2].min()
    # colours: v004 toe-2 ring faces red; v005 racetrack faces blue, its turn faces cyan; valence-3 / 5 poles marked
    fc4 = np.tile(CLAY, (len(Q4), 1)); fc4[np.isin(Q4, t2v4).any(1)] = (0.9, 0.15, 0.1)
    fc5 = np.tile(CLAY, (len(Q5), 1)); fc5[np.isin(Q5, rt5).any(1)] = (0.15, 0.35, 0.95); fc5[np.isin(Q5, v3c).any(1)] = (0.1, 0.8, 0.85)
    t2 = JC['l-toe-2-1']; t1 = JC['l-toe-1-1']; t3 = JC['l-toe-3-1']; sgn = np.sign(t2[0])
    TV = [('dors', (0, 0.35, 1), t2 + [0, 0.8, 0], 3.2), ('plant', (0, 0.35, -1), t2 + [0, 0.8, 0], 3.2), ('web12', (-sgn * 0.9, 0.6, 0.6), 0.5 * (t1 + t2) + [0, 0.8, 0.2], 2.4),
          ('web23', (sgn * 0.9, 0.6, 0.6), 0.5 * (t2 + t3) + [0, 0.8, 0.2], 2.4)]
    render(V4, Q4, fc4, 'tw4_' + tg, vs_(TV), '1', 640); render(V5, Q5, fc5, 'tw5_' + tg, vs_(TV), '1', 640)
    la = LA[cid]['delta_vs_tw0']
    sheet('Toe-2 web / root architecture - %s (%s): rejected v004 closed ring (row 1, red) | final v005 dorsal racetrack (row 2, blue; turn quads cyan)' % (LAB[cid], cid),
          'left foot, identical cameras: dorsal | plantar | toe-1/2 web | toe-2/3 web. The racetrack crosses the toe-2 root only over the dorsal sector and never enters the thin plantar / web strip quads.',
          [[('tw4_' + tg, v, 'v004 ' + v) for v in ('dors', 'plant', 'web12', 'web23')], [('tw5_' + tg, v, 'v005 ' + v) for v in ('dors', 'plant', 'web12', 'web23')]], 360, '%s/v005_toe2_topology_%s.jpg' % (SH, cid),
          ['whole-mesh T-4 union added by the toe-2 support vs the ring-free parent: v004 ring +%d quads (aspect>10 +%d) | v005 racetrack +%d quads (aspect>10 +%d); toe-2 patch aspect max v004 %.2f -> v005 %.2f'
           % (TU[cid]['v004']['union'] - TU[cid]['tw0']['union'], TU[cid]['v004']['asp_gt10'] - TU[cid]['tw0']['asp_gt10'], TU[cid]['v005']['union'] - TU[cid]['tw0']['union'], TU[cid]['v005']['asp_gt10'] - TU[cid]['tw0']['asp_gt10'],
              LA[cid]['v004_toe2_ring_patch']['aspect_max'], LA[cid]['v005_racetrack_patch']['aspect_max'])])
    # pole / valence map
    for tag_, V, Q in (('pv4_', V4, Q4), ('pv5_', V5, Q5)):
        _, val = topo(Q, len(V)); vc = np.tile(CLAY, (len(V), 1)); vc[val == 3] = (0.1, 0.3, 0.95); vc[val == 5] = (0.9, 0.1, 0.1); vc[val >= 6] = (0.6, 0.0, 0.6)
        render(V, Q, vc, tag_ + tg, vs_(TV[:2]), '1', 640)
    sheet('Pole / valence map - %s: valence 3 blue, 5 red (vertex colour)' % cid, 'row 1 v004 | row 2 v005. The racetrack adds 4 valence-3 turn centres + 4 valence-5 turn corners per toe, all outside the D4/D5 toe2_j1 crease window (|axial| > 0.5 local loop) and off the web.',
          [[('pv4_' + tg, v, 'v004 ' + v) for v in ('dors', 'plant')], [('pv5_' + tg, v, 'v005 ' + v) for v in ('dors', 'plant')]], 420, '%s/v005_pole_valence_%s.jpg' % (SH, cid))
    # T-4 and aspect heat, source deviation heat
    def t4col(V, Q):
        a, s, va, vs = quality(V, Q); col = np.tile(CLAY, (len(Q), 1)); col[va] = (0.9, 0.1, 0.1); col[vs] = (0.95, 0.55, 0.1); col[va & vs] = (0.6, 0.1, 0.7); return col, ramp((s - 1) / 9)
    q4c, a4c = t4col(V4, Q4); q5c, a5c = t4col(V5, Q5)
    render(V4, Q4, q4c, 'q4_' + tg, vs_(TV[:2]), '1', 600); render(V5, Q5, q5c, 'q5_' + tg, vs_(TV[:2]), '1', 600); render(V4, Q4, a4c, 'a4_' + tg, vs_(TV[:2]), '1', 600); render(V5, Q5, a5c, 'a5_' + tg, vs_(TV[:2]), '1', 600)
    sheet('T-4 local quality - %s: violations angle red / aspect orange / both purple' % cid, 'row 1 v004 | row 2 v005 (dorsal, plantar)', [[('q4_' + tg, 'dors', 'v004 dorsal'), ('q4_' + tg, 'plant', 'v004 plantar')], [('q5_' + tg, 'dors', 'v005 dorsal'), ('q5_' + tg, 'plant', 'v005 plantar')]], 420,
          '%s/v005_T4_local_%s.jpg' % (SH, cid))
    sheet('Aspect-ratio heat - %s: aspect 1 (blue) .. 5.5 (yellow) .. 10+ (red)' % cid, 'row 1 v004 | row 2 v005', [[('a4_' + tg, 'dors', 'v004 dorsal'), ('a4_' + tg, 'plant', 'v004 plantar')], [('a5_' + tg, 'dors', 'v005 dorsal'), ('a5_' + tg, 'plant', 'v005 plantar')]], 420,
          '%s/v005_aspect_%s.jpg' % (SH, cid), ['v005 racetrack patch aspect max %.2f (v004 toe-2 ring %.2f)' % (LA[cid]['v005_racetrack_patch']['aspect_max'], LA[cid]['v004_toe2_ring_patch']['aspect_max'])])
    r6 = np.load(R6[cid]); src = trimesh.Trimesh(r6['V'].astype(float), r6['F'], process=False); _, d5, _ = trimesh.proximity.closest_point(src, V5)
    render(V5, Q5, ramp(d5 * 10 / 1.5)[Q5].mean(1), 'dv5_' + tg, vs_(TV), '1', 600)
    sheet('Source deviation - %s: v005 production -> accepted source 0 (blue) .. 0.75 (yellow) .. 1.5 mm (red)' % cid, 'left foot, toe-2 region', [[('dv5_' + tg, v, v) for v in ('dors', 'plant', 'web12', 'web23')]], 360, '%s/v005_source_deviation_%s.jpg' % (SH, cid),
          ['racetrack vertices -> source max %.3f mm; source -> production near the patch max %.3f mm (v004 %.3f)' % (LA[cid]['patch_prod_to_source_max_mm'], LA[cid]['source_to_prod_near_patch_max_mm']['v005'], LA[cid]['source_to_prod_near_patch_max_mm']['v004'])])
    # deformation toe flex / ext: native | v003 | v004 | v005, flipped faces red
    def pp(p, kind):
        if kind == 'v005': return W + '/def/%s_%s_v005.npz' % (p, cid)
        if kind == 'v004': return '/tmp/claude-0/rt/v4/def/%s_%s_v004.npz' % (p, cid)
        if cid.startswith('MF'): return '/tmp/claude-0/rt/m3/v4/%s_%s_%s.npz' % (p, cid, 'native_toe' if kind == 'native' else 'v003_sanity')
        return '/tmp/claude-0/rt/sk/def/%s_%s_%s.npz' % (p, cid, 'native' if kind == 'native' else 'fam')
    QK = {'native': np.load(NAT[cid])['Q'], 'v003': np.load(('/tmp/claude-0/rt/m3/cand/%s_v003.npz' if cid.startswith('MF') else '/tmp/claude-0/rt/sk/cand/%s_fam.npz') % cid)['Q'], 'v004': Q4, 'v005': Q5}
    rows = []
    for p in ('toe_flex30_l', 'toe_ext30_l'):
        cells = []
        for kind in ('native', 'v003', 'v004', 'v005'):
            z_ = np.load(pp(p, kind)); Qk = QK[kind]; col = np.tile(CLAY, (len(Qk), 1)); col[z_['flip']] = (0.9, 0.1, 0.1); t_ = 'dt_%s_%s_%s' % (kind, tg, p)
            render(z_['V'], Qk, col, t_, vs_([('v', (1, 0.5, 0.5), H['ball_l'] + [0, 2.0, 0], 7)]), '1', 520); cells.append((t_, 'v', '%s %s flips %d' % (kind, p[:7], len(z_['flip']))))
        rows.append(cells)
    fp = json.load(open(W + '/def/MPFB_v005_flip_parentage.json'))['%s toe_ext30_l' % cid]; ft = json.load(open(W + '/def/MPFB_v005_flip_parentage.json'))['fold_test'][cid]
    sheet('Toe flex / ext deformation - %s: native | frozen v003 | v004 | v005 (flipped faces red)' % cid, 'source rig + weights through each map (LBS, single ball bone).', rows, 330, '%s/v005_toe_deform_%s.jpg' % (SH, cid),
          ['toe ext 30: v005 flips whose ring-free parent face did not flip: %d, of which parent-quad folds %d -> topology-attributable %d' % (ft['new_flips'], ft['flipped_in_parent_posed_geometry'], ft['new_flips'] - ft['flipped_in_parent_posed_geometry'])])
    # retention: heel deviation, hip ring, toe-3 ring
    rn = z5['ring_name']; vc = np.tile(CLAY, (len(V5), 1)); vc[n3 + np.nonzero(np.char.startswith(rn, 'hip'))[0]] = (0.9, 0.1, 0.1); vc[n3 + np.nonzero(np.char.startswith(rn, 'toe3'))[0]] = (0.1, 0.7, 0.2); vc[rc5 == 2] = (0.95, 0.85, 0.1)
    hipc = 0.5 * (H['thigh_l'] + H['thigh_r']); fl = H['foot_l']
    RV = [('hip', (0, 1, 0), hipc + [0, 0, 2], st * 0.12), ('heel', (0, -1, 0.1), fl + [0, -6.0, -4.0], 6.0), ('toe3', (0, 0.35, 1), JC['l-toe-3-1'] + [0, 0.8, 0], 3.2)]
    render(V5, Q5, vc[Q5].max(1) * 0 + np.array([vc[q][np.argmax(np.abs(vc[q] - CLAY).sum(1))] for q in Q5]), 'ret_' + tg, vs_(RV), '1', 600); render(V5, Q5, ramp(d5 * 10 / 1.5)[Q5].mean(1), 'reth_' + tg, vs_(RV[1:2]), '1', 600)
    an = json.load(open(W + '/anat/%s_v005_anatomy.json' % cid)); ret = json.load(open(W + '/audit/retention_and_toe2_summary.json'))[cid]['retained']
    sheet('Retention proof - %s: hip ring red, heel rows yellow, toe-3 ring green (v005)' % cid, 'hip | heel | toe-3 root | heel deviation heat (0 .. 1.5 mm)', [[('ret_' + tg, 'hip', 'hip ring'), ('ret_' + tg, 'heel', 'heel rows'), ('ret_' + tg, 'toe3', 'toe-3 ring'), ('reth_' + tg, 'heel', 'heel deviation')]], 360,
          '%s/v005_retention_%s.jpg' % (SH, cid), ['feet T-2 max %.3f mm; hip_l %d/5, toe3_j1_l %d/2 (D1+D3+D4+D5), identical to v004' % (an['deviation_prod_to_source']['feet']['max_mm'], ret['hip_l'][1], ret['toe3_j1_l'][1])])
    # whole body
    c = np.array([0, 0, st / 2]); BV = [('front', (0, 1, 0), c, st * 0.52), ('rear', (0, -1, 0), c, st * 0.52), ('profile', (1, 0, 0), c, st * 0.52)]
    render(V5, Q5, fc5, 'wb_' + tg, vs_(BV), '1', 900)
    sheet('Whole-body confirmation - %s (%s), v005 %d verts / %d quads' % (LAB[cid], cid, len(V5), len(Q5)), 'wire; toe-2 racetrack faces blue', [[('wb_' + tg, v, v) for v in ('front', 'rear', 'profile')]], 440, '%s/v005_body_%s.jpg' % (SH, cid),
          ['T-1/T-2 %s, T-3 %s, T-7 %s, stature diff %.3f mm, min IoU %.4f' % (an['T1_T2_pass'], an['T3_pass'], an['T7_pass'], an['stature_diff_mm'], min(an['silhouette_iou'][k] for k in ('front', 'rear', 'profile_left', 'profile_right')))])
    print('sheets', cid, flush=True)
# ---- validator table D1 + D3 + D4 + D5 (authoritative)
VJ = {c: json.load(open('%s/val/%s_v005_validator_v2_D4_D5.json' % (W, c)))['stations'] for c in CFG}; ks = list(VJ['MF-M-R']); rh = 16; half = (len(ks) + 1) // 2
S = Image.new('RGB', (2 * 800 + 30, 90 + half * rh), 'white'); d = ImageDraw.Draw(S)
d.text((10, 8), 'MPFB Family Base v005 - 69-station counted-loop validator, D1 + D3 + D4 + D5 (authoritative): loops / minimum, valid sides, status', fill=(0, 0, 0), font=f(12, True))
d.text((10, 28), 'firm PASS: ' + ', '.join('%s %d/69' % (c, sum(v['firm_D1_D3'] for v in VJ[c].values())) for c in CFG) + '   (FD = PASS_FALLBACK_DEFINED_SIDES, +D5 = side(s) undefined by D5, +A = adjacent-digit pole scoped)', fill=(60, 60, 60), font=f(11, True))
AB = lambda s: s.replace('PASS_FALLBACK_DEFINED_SIDES', 'FD').replace('PASS_FALLBACK_CLOSED_RING', 'FR').replace('+SCOPED_ADJACENT_DIGIT_POLE', '+A').replace('+D5_INTERDIGITAL_UNDEFINED', '+D5').replace('PASS_SCOPED_ADJACENT_DIGIT_POLE', 'P+A').replace('FAIL_LOOPS', 'F-loops').replace('FAIL_CREASE_POLE', 'F-pole').replace('PASS', 'P')
for blk in range(2):
    bx = 10 + blk * 810
    for j, c in enumerate(CFG): d.text((bx + 130 + j * 165, 52), {'MF-M-R': 'MF-M', 'MF-F-R': 'MF-F', 'SK208-C1R': 'SK-C1R', 'SKF208': 'SK-F'}[c], fill=(0, 0, 0), font=f(11, True))
    for i, k in enumerate(ks[blk * half:(blk + 1) * half]):
        y = 70 + i * rh; d.text((bx, y), k, fill=(0, 0, 0), font=f(11))
        for j, c in enumerate(CFG):
            v = VJ[c][k]; colr = (230, 80, 70) if not v['firm_D1_D3'] else ((245, 200, 80) if v['margin'] == 0 else (170, 225, 170)); x = bx + 130 + j * 165
            d.rectangle([x, y, x + 160, y + rh - 2], fill=colr); d.text((x + 3, y + 1), '%d/%d %s %s' % (v['loops_v2'], v['required'], ''.join(s[0] + s[1] for s in v['valid_sides']), AB(v['status_D1_D3'])), fill=(0, 0, 0), font=f(10))
S.save(SH + '/v005_validator_D5.jpg', quality=90)
# ---- C1R face
cid = 'SK208-C1R'; c5 = np.load(V5P % cid); fi = json.load(open(W + '/anat/%s_v005_face_identity.json' % cid)); r1 = np.load(R6[cid]); src = trimesh.Trimesh(r1['V'], r1['F'], process=False); _, e1, _ = trimesh.proximity.closest_point(src, c5['V'])
meta = json.loads(str(c5['meta'])); eye = np.array(meta['eye_helpers']['helper-l-eye']); hc = eye * [0, 1, 1] + [0, -1.0, -2.5]; FV = [('front', (0, 1, 0.05), hc, 10), ('q3', (0.6, 0.8, 0.05), hc, 10)]
render(r1['V'], r1['F'], np.tile(CLAY, (len(r1['F']), 1)), 'f5src', vs_(FV), '0', 600); render(c5['V'], c5['Q'], np.tile(CLAY, (len(c5['Q']), 1)), 'f5v5', vs_(FV), '0', 600); render(c5['V'], c5['Q'], ramp(e1 * 10 / 3.0)[c5['Q']].mean(1), 'f5e1', vs_(FV), '0', 600)
sheet('Skarn C1R face confirmation - SK208-C1R', 'C1R source | v005 | v005 -> C1R source distance heat 0 .. 3 mm', [[('f5src', 'front', 'C1R source'), ('f5v5', 'front', 'v005'), ('f5e1', 'front', 'v005 -> C1R'), ('f5e1', 'q3', 'v005 -> C1R 3/4')]], 380, SH + '/v005_C1R_face.jpg',
      ['face -> C1R median / p95 / max %(median).3f / %(p95).3f / %(max).3f mm' % fi['family_face_to_identity_source_mm'] + ' | -> pre-C1R median %(median).3f mm' % fi['family_face_to_pre_identity_source_mm'] + ' | identity preserved: %s (face unchanged from v003 / v004)' % fi['identity_preserved']])
# ---- change diagram
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(15.5, 7.5)); ax.axis('off')
def box(x, y, w, h, t, fc): ax.add_patch(plt.Rectangle((x, y), w, h, fc=fc, ec='k', lw=1.2)); ax.text(x + w / 2, y + h / 2, t, ha='center', va='center', fontsize=9.3)
box(0.01, 0.38, 0.15, 0.24, 'FROZEN v003\nFamily Base v1 (historical)\n57,674 V / 57,672 Q\nface 68f7b6a9...', '#dde3ee')
box(0.21, 0.62, 0.18, 0.3, 'v004 candidate (provenance)\n+ heel rows (8)\n+ hip ring (84)\n+ toe-2 CLOSED RING (2 x 24)  REJECTED\n+ toe-3 ring (2 x 24) + pole slides\n57,854 V, face 2bd4c8b3...', '#f3e0c8')
box(0.21, 0.12, 0.18, 0.3, 'retained architecture\n(v004 without the toe-2 ring)\nheel + hip + toe-3 identical rows\n57,806 V', '#e8f0d8')
box(0.45, 0.12, 0.2, 0.3, 'toe-2 DORSAL RACETRACK\n(loop 497: strips 497|1262 + 497|1119)\n2 x 18 V, 8 corner turns\n(4 val-3 + 4 val-5 per toe, outside the crease)\naspect <= 4.7, 0 slivers', '#c9d8f8')
box(0.71, 0.36, 0.13, 0.28, 'FINAL v005\n%d V / %d Q\nhm08 map e690fbaf...\nD1+D3+D4+D5\n69/69 x 4' % (log5['verts'], log5['quads']), '#e6d7f2')
for i, c in enumerate(CFG): box(0.87, 0.78 - i * 0.2, 0.12, 0.14, '%s\nM5 @ race hm08' % c, '#eeeeee'); ax.annotate('', xy=(0.87, 0.85 - i * 0.2), xytext=(0.84, 0.5), arrowprops=dict(arrowstyle='->'))
for a_, b_ in (((0.16, 0.5), (0.21, 0.77)), ((0.30, 0.62), (0.30, 0.42)), ((0.39, 0.27), (0.45, 0.27)), ((0.65, 0.27), (0.71, 0.45))): ax.annotate('', xy=b_, xytext=a_, arrowprops=dict(arrowstyle='->', lw=1.2))
ax.set_title('MPFB family topology: v003 -> v004 (margin hardening) -> v005 (toe-2 web correction): one topology, four realizations', fontsize=12); plt.savefig(SH + '/v005_change_diagram.jpg', dpi=110, bbox_inches='tight')
print('done')
