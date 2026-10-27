# v4_sheets.py WORK : order a18371c §19 visual evidence for the MPFB Family Base v004 successor, all four family configurations, identical cameras:
#  v004_topology_<ID>  successor topology overview (wire; added hip ring red, toe-2 ring blue, toe-3 ring green, re-expressed heel rows yellow,
#                      relocated toe-3 forefoot poles orange)
#  v004_heel_<ID>      posterior heel before / after: frozen v003 fit | v004, production -> source deviation heat (0 .. 1.5 mm) + wire
#  v004_hip_<ID>       hip support ring close-up (front / profile / rear), v003 | v004
#  v004_toes_<ID>      toe-2 / toe-3 root rings close-up (dorsal / plantar / medial-front), v003 | v004
#  v004_overlay_<ID>   source vs successor: deviation heat front / profile + silhouette IoU
#  v004_density_<ID>   edge-length / stature heat + per-zone table (v003 | v004)
#  v004_T4_<ID>        T-4 violations (angle red, aspect orange, both purple) feet + pelvis, v003 | v004
#  v004_deform_<ID>    native hm08 | frozen-v003 fit | v004 for hip flex 90, knee 90, ankle dorsi 20, toe flex 30, toe ext 30
#  v004_C1R_face       Skarn C1R identity: C1R source | v004 | pre-C1R (aligned) + face distance heat to each
#  v004_validator_D4   69-station validator (D1 + D3 + D4) on all four, with mode / status
#  v004_change_diagram family topology change diagram v003 -> v004
import sys, os, json, subprocess, numpy as np, trimesh, scipy.sparse as sp
from PIL import Image, ImageDraw, ImageFont
W = sys.argv[1]; BP = '/home/claude/stc/bin/python3'; T = '/home/claude/wayfarer-design/tools/rac/rp/grask_rigprep_v001/render_attr.py'
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001')
from v004_lib import NAT, R6, CFG
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FN = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; f = lambda n, b=False: ImageFont.truetype(FB if b else FN, n)
OV = W + '/ov'; SH = W + '/sheets'; os.makedirs(OV, exist_ok=True); os.makedirs(SH, exist_ok=True); CLAY = np.array([0.80, 0.77, 0.73])
V3P = {'MF-M-R': '/tmp/claude-0/rt/m3/cand/MF-M-R_v003.npz', 'MF-F-R': '/tmp/claude-0/rt/m3/cand/MF-F-R_v003.npz', 'SK208-C1R': '/tmp/claude-0/rt/sk/cand/SK208-C1R_fam.npz', 'SKF208': '/tmp/claude-0/rt/sk/cand/SKF208_fam.npz'}
A3 = {'MF-M-R': '/tmp/claude-0/rt/m3/audit/MF-M-R_v003', 'MF-F-R': '/tmp/claude-0/rt/m3/audit/MF-F-R_v003', 'SK208-C1R': '/tmp/claude-0/rt/sk/audit/SK208-C1R_fam', 'SKF208': '/tmp/claude-0/rt/sk/audit/SKF208_fam'}
LAB = {'MF-M-R': 'Marchfolk M (config 1)', 'MF-F-R': 'Marchfolk F (config 2)', 'SK208-C1R': 'Skarn M C1R (config 1)', 'SKF208': 'Skarn F (config 2)'}
def render(V, Q, col, tg, vs, wire='0', px=420):
    if os.path.exists(OV + '/%s_%s.png' % (tg, vs.split(';')[-1].split(':')[0])): return
    o = OV + '/%s.npz' % tg; np.savez(o, V=V, Q=Q); np.save(o[:-4] + '_c.npy', np.asarray(col, np.float32))
    subprocess.run([BP, T, '--', o, o[:-4] + '_c.npy', OV, tg, vs, wire, str(px)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, env=dict(os.environ, WIRE_T='0.00012'))
    os.remove(o); os.remove(o[:-4] + '_c.npy')
def img(tg, v, cell): return Image.open('%s/%s_%s.png' % (OV, tg, v)).convert('RGB').resize((cell, cell), Image.LANCZOS)
def vs_(views): return ';'.join('%s:%s:%s:%g' % (n, ','.join('%.4f' % x for x in d), ','.join('%.3f' % x for x in c), h) for n, d, c, h in views)
def ramp(t):
    t = np.clip(t, 0, 1)[:, None]; return np.where(t < 0.5, (1 - 2 * t) * np.array([0.15, 0.35, 0.85]) + 2 * t * np.array([0.95, 0.9, 0.3]), (2 - 2 * t) * np.array([0.95, 0.9, 0.3]) + (2 * t - 1) * np.array([0.85, 0.1, 0.1]))
def sheet(title, sub, rows, cell, out, notes=()):
    """rows: list of (row_label, [(tag, view, caption), ...])"""
    nc = max(len(r[1]) for r in rows); S = Image.new('RGB', (20 + nc * cell, 70 + len(rows) * (cell + 26) + 18 * len(notes)), 'white'); d = ImageDraw.Draw(S)
    d.text((10, 8), title, fill=(0, 0, 0), font=f(14, True)); d.text((10, 30), sub, fill=(60, 60, 60), font=f(11))
    for i, (rl, cells) in enumerate(rows):
        y = 52 + i * (cell + 26)
        for j, (tg, v, cap) in enumerate(cells):
            S.paste(img(tg, v, cell), (10 + j * cell, y + 20)); d.text((14 + j * cell, y + 3), cap, fill=(150, 20, 20), font=f(11, True))
    for k, n in enumerate(notes): d.text((10, 56 + len(rows) * (cell + 26) + 18 * k), n, fill=(30, 30, 30), font=f(11))
    S.save(out, quality=85)
core = np.load(W + '/v4core.npz'); rc = core['row_class']; rn = core['ring_name']; n3 = int(core['n_v003'])
for cid in CFG:
    c4 = np.load('%s/cand/%s_v004.npz' % (W, cid)); c3 = np.load(V3P[cid]); nz = np.load(NAT[cid]); r6 = np.load(R6[cid]); meta = json.loads(str(nz['meta'])); H = {k: np.array(v) for k, v in meta['heads'].items()}
    V4, Q4, V3, Q3 = c4['V'], c4['Q'], c3['V'], c3['Q']; st = V4[:, 2].max() - V4[:, 2].min(); tg = cid.replace('-', '')
    # ---- face highlight colours
    vc = np.tile(CLAY, (len(V4), 1)); newv = np.arange(n3, len(V4))
    for nm_, colr in (('hip', (0.9, 0.1, 0.1)), ('toe2', (0.1, 0.3, 0.95)), ('toe3', (0.1, 0.7, 0.2))): vc[newv[np.char.startswith(rn, nm_)]] = colr
    vc[rc == 2] = (0.95, 0.85, 0.1); vc[rc == 4] = (0.95, 0.5, 0.05); fc4 = vc[Q4].max(1) * 0 + np.array([vc[q][np.argmax(np.abs(vc[q] - CLAY).sum(1))] for q in Q4])
    c = np.array([0, 0, st / 2]); BV = [('front', (0, 1, 0), c, st * 0.52), ('rear', (0, -1, 0), c, st * 0.52), ('profile', (1, 0, 0), c, st * 0.52)]
    render(V4, Q4, fc4, 'top_' + tg, vs_(BV), '1', 1000)
    hipc = 0.5 * (H['thigh_l'] + H['thigh_r']); HV = [('hfront', (0, 1, 0), hipc + [0, 0, 2], st * 0.12), ('hprof', (1, 0, 0), H['thigh_l'] + [0, 0, 2], st * 0.12), ('hrear', (0, -1, 0), hipc + [0, 0, 2], st * 0.12)]
    fl = H['foot_l']; bl = H['ball_l']; toec = bl + [-1.0 * np.sign(bl[0]) * 0 + 0, 3.0, -1.5]
    TV = [('tdors', (0, 0.25, 1), toec, 5.5), ('tplant', (0, 0.25, -1), toec, 5.5), ('tmed', (-np.sign(bl[0]) * 1, 0.6, 0.25), toec, 5.5)]
    heelc = fl + [0, -6.0, -4.0]; HE = [('heback', (0, -1, 0.1), heelc, 6.0), ('helat', (np.sign(fl[0]), -0.6, 0.1), heelc, 6.0), ('hemed', (-np.sign(fl[0]), -0.6, 0.1), heelc, 6.0)]
    render(V4, Q4, fc4, 'cl4_' + tg, vs_(BV[:1] + HV + TV), '1', 700)
    vc3 = np.tile(CLAY, (len(V3), 1)); render(V3, Q3, np.tile(CLAY, (len(Q3), 1)), 'cl3_' + tg, vs_(HV + TV), '1', 700)
    sheet('MPFB Family Base v004 successor topology - %s (%s)' % (LAB[cid], cid), '%d verts / %d quads (frozen v003 57,674 / 57,672). Added hip support ring red (84 verts, self-mirrored pelvis ring), toe-2 root rings blue, toe-3 root rings green (24 verts each side); re-expressed heel rows yellow; slid toe-3 forefoot poles orange.' % (len(V4), len(Q4)),
          [('', [('top_' + tg, 'front', 'front'), ('top_' + tg, 'rear', 'rear'), ('top_' + tg, 'profile', 'profile'), ('cl4_' + tg, 'front', 'front (700 px)')])], 420, '%s/v004_topology_%s.jpg' % (SH, cid))
    sheet('Hip support ring close-up - %s' % cid, 'frozen v003 fit (row 1) | successor v004 (row 2); new ring red. Identical cameras.', [('', [('cl3_' + tg, v, 'v003 ' + v[1:]) for v in ('hfront', 'hprof', 'hrear')]), ('', [('cl4_' + tg, v, 'v004 ' + v[1:]) for v in ('hfront', 'hprof', 'hrear')])], 400, '%s/v004_hip_%s.jpg' % (SH, cid))
    sheet('Toe-2 / toe-3 root rings close-up (left foot) - %s' % cid, 'frozen v003 fit (row 1) | successor v004 (row 2); toe-2 ring blue, toe-3 ring green, slid toe-3 forefoot poles orange.', [('', [('cl3_' + tg, v, 'v003 ' + v[1:]) for v in ('tdors', 'tplant', 'tmed')]), ('', [('cl4_' + tg, v, 'v004 ' + v[1:]) for v in ('tdors', 'tplant', 'tmed')])], 400, '%s/v004_toes_%s.jpg' % (SH, cid))
    # ---- heel before / after: production -> source deviation heat
    src = trimesh.Trimesh(r6['V'].astype(float), r6['F'], process=False); _, d4, _ = trimesh.proximity.closest_point(src, V4); _, d3, _ = trimesh.proximity.closest_point(src, V3)
    render(V3, Q3, ramp(d3 * 10 / 1.5)[Q3].mean(1), 'he3_' + tg, vs_(HE), '1', 600); render(V4, Q4, ramp(d4 * 10 / 1.5)[Q4].mean(1), 'he4_' + tg, vs_(HE), '1', 600)
    an3 = json.load(open('/tmp/claude-0/rt/%s.json' % ('m3/anat/%s_v003_anatomy' % cid if cid.startswith('MF') else 'sk/anat/%s_fam_anatomy' % cid))); an4 = json.load(open('%s/anat/%s_v004_anatomy.json' % (W, cid)))
    hv = np.nonzero(rc == 2)[0]
    sheet('Posterior heel mapping before / after - %s' % cid, 'production -> source deviation heat 0 (blue) .. 0.75 (yellow) .. 1.5 mm (red) + wire. Row 1 frozen v003 linear quad-centre rows; row 2 v004 on-surface barycentric rows (8 vertices, 4 mirrored pairs).',
          [('', [('he3_' + tg, v, 'v003 ' + v[2:]) for v in ('heback', 'helat', 'hemed')]), ('', [('he4_' + tg, v, 'v004 ' + v[2:]) for v in ('heback', 'helat', 'hemed')])], 380, '%s/v004_heel_%s.jpg' % (SH, cid),
          ['T-2 feet max (prod->source): v003 %.3f mm -> v004 %.3f mm; re-expressed heel vertices v003 %s mm -> v004 %s mm' % (an3['deviation_prod_to_source']['feet']['max_mm'], an4['deviation_prod_to_source']['feet']['max_mm'],
                                                                                                                     np.round(d3[hv] * 10, 3).tolist(), np.round(d4[hv] * 10, 4).tolist())])
    # ---- overlay
    OVV = [('ofront', (0, 1, 0), c, st * 0.52), ('oprof', (1, 0, 0), c, st * 0.52)]; render(V4, Q4, ramp(d4 * 10 / 1.5)[Q4].mean(1), 'ov4_' + tg, vs_(OVV), '0', 700)
    Vn = nz['V']; render(Vn, nz['Q'], np.tile([0.55, 0.65, 0.9], (len(nz['Q']), 1)), 'ovn_' + tg, vs_(OVV), '0', 700)
    iou = an4['silhouette_iou']
    sheet('Source vs successor overlay - %s' % cid, 'v004 production -> accepted source deviation heat (0 .. 1.5 mm) | source hm08 body (blue), same cameras.', [('', [('ov4_' + tg, 'ofront', 'v004 deviation front'), ('ov4_' + tg, 'oprof', 'v004 deviation profile'), ('ovn_' + tg, 'ofront', 'source front'), ('ovn_' + tg, 'oprof', 'source profile')])], 400,
          '%s/v004_overlay_%s.jpg' % (SH, cid), ['silhouette IoU (3 px/cm, 4x ss): ' + ', '.join('%s %.4f' % kv for kv in iou.items()) + ' | T-1/T-2 %s, T-3 %s, T-7 %s, stature diff %.3f mm' % (an4['T1_T2_pass'], an4['T3_pass'], an4['T7_pass'], an4['stature_diff_mm'])])
    # ---- density
    def vden(V, Q):
        E = np.sort(np.concatenate([Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]]), 1); E = np.unique(E, axis=0); el = np.linalg.norm(V[E[:, 0]] - V[E[:, 1]], axis=1)
        s = np.zeros(len(V)); n = np.zeros(len(V)); np.add.at(s, E[:, 0], el); np.add.at(s, E[:, 1], el); np.add.at(n, E[:, 0], 1); np.add.at(n, E[:, 1], 1); return s / n / st * 100
    dn4 = vden(V4, Q4); dn3 = vden(V3, Q3); DV = [('dfront', (0, 1, 0), c, st * 0.52), ('dfeet', (0, 0.3, 1), np.r_[0, H['ball_l'][1] - 3, 3], 14)]
    render(V3, Q3, ramp(dn3 / 0.6)[Q3].mean(1), 'dn3_' + tg, vs_(DV), '0', 600); render(V4, Q4, ramp(dn4 / 0.6)[Q4].mean(1), 'dn4_' + tg, vs_(DV), '0', 600)
    a3 = json.load(open(A3[cid] + '_audit.json')); a4 = json.load(open('%s/audit/%s_v004_audit.json' % (W, cid)))
    notes = ['zone mean edge / stature %% (limit): ' + '; '.join('%s %.3f -> %.3f (%.2f)' % (k, a3['density_pct_of_stature'][k]['mean'], v['mean'], v['limit']) for k, v in a4['density_pct_of_stature'].items())]
    sheet('Creator density - %s' % cid, 'vertex mean edge length / stature heat 0 (blue) .. 0.3 (yellow) .. 0.6 %% (red). Row: v003 front | v003 feet | v004 front | v004 feet.', [('', [('dn3_' + tg, 'dfront', 'v003 front'), ('dn3_' + tg, 'dfeet', 'v003 feet'), ('dn4_' + tg, 'dfront', 'v004 front'), ('dn4_' + tg, 'dfeet', 'v004 feet')])], 380,
          '%s/v004_density_%s.jpg' % (SH, cid), notes)
    # ---- T-4
    import importlib; core3 = importlib.import_module('core3lib')
    def t4col(V, Q):
        _, _, va, vs = core3.quality(V, Q); col = np.tile(CLAY, (len(Q), 1)); col[va] = (0.9, 0.1, 0.1); col[vs] = (0.95, 0.55, 0.1); col[va & vs] = (0.6, 0.1, 0.7); return col, va, vs
    t3, va3, vs3 = t4col(V3, Q3); t4, va4, vs4 = t4col(V4, Q4); TQ = [('qfeet', (0, 0.3, 1), np.r_[0, H['ball_l'][1] - 3, 3], 14), ('qsole', (0, 0.3, -1), np.r_[0, H['ball_l'][1] - 3, 3], 14), ('qhip', (0, 1, 0), hipc + [0, 0, 2], st * 0.12)]
    render(V3, Q3, t3, 'q3_' + tg, vs_(TQ), '1', 600); render(V4, Q4, t4, 'q4_' + tg, vs_(TQ), '1', 600)
    sheet('T-4 quad quality - %s' % cid, 'violations: angle outside 45-135 deg red, aspect > 4 orange, both purple. Row 1 frozen v003 fit, row 2 v004.', [('', [('q3_' + tg, v, 'v003 ' + v[1:]) for v in ('qfeet', 'qsole', 'qhip')]), ('', [('q4_' + tg, v, 'v004 ' + v[1:]) for v in ('qfeet', 'qsole', 'qhip')])], 380,
          '%s/v004_T4_%s.jpg' % (SH, cid), ['union: v003 %d / %d quads (%.3f %%) -> v004 %d / %d (%.3f %%); angle %d -> %d, aspect %d -> %d' % ((va3 | vs3).sum(), len(Q3), 100 * (va3 | vs3).mean(), (va4 | vs4).sum(), len(Q4), 100 * (va4 | vs4).mean(), va3.sum(), va4.sum(), vs3.sum(), vs4.sum())])
    # ---- deformation
    POS = ['hip_flex90_l', 'knee_90_l', 'ankle_dorsi20_l', 'toe_flex30_l', 'toe_ext30_l']
    def pose_path(p, kind):
        if kind == 'v004': return '%s/def/%s_%s_v004.npz' % (W, p, cid)
        if cid.startswith('MF'):
            if kind == 'native': return ('/tmp/claude-0/rt/m3/v4/%s_%s_native_toe.npz' if p.startswith('toe') else '/tmp/claude-0/rt/m3/def/%s_%s_native.npz') % (p, cid)
            return ('/tmp/claude-0/rt/m3/v4/%s_%s_v003_sanity.npz' if p.startswith('toe') else '/tmp/claude-0/rt/m3/def/%s_%s_v003.npz') % (p, cid)
        return '/tmp/claude-0/rt/sk/def/%s_%s_%s.npz' % (p, cid, 'native' if kind == 'native' else 'fam')
    rows = []
    for kind, Qk in (('native', nz['Q']), ('v003', Q3), ('v004', Q4)):
        cells = []
        for p in POS:
            pz = np.load(pose_path(p, kind)); Vp = pz['V']; sidec = H['thigh_l'] if p.startswith('hip') else (H['calf_l'] if p.startswith('knee') else H['ball_l'])
            dv = (1, 0.15, 0.1) if not p.startswith('toe') else (1, 0.4, 0.3); hh = 22 if p.startswith('hip') else (16 if p.startswith('knee') else 9)
            t_ = 'dp_%s_%s_%s' % (kind, tg, p); render(Vp, Qk, np.tile(CLAY, (len(Qk), 1)), t_, vs_([('v', dv, sidec, hh)]), '1' if kind != 'native' else '1', 500)
            cells.append((t_, 'v', '%s %s  flip %d selfx %d fold %d' % (kind, p.replace('_l', ''), len(pz['flip']), len(pz['selfx']), len(pz['fold']))))
        rows.append(('', cells))
    sheet('Limited deformation sanity - %s' % cid, 'source rig + weights carried through the map (LBS); native hm08 | frozen-v003 fit | successor v004; counts: flipped faces / self-intersection pairs / folds (scale with face count, x4.3 from hm08).', rows, 320, '%s/v004_deform_%s.jpg' % (SH, cid))
    print('sheets', cid, flush=True)
# ---- C1R face identity
cid = 'SK208-C1R'; c4 = np.load('%s/cand/%s_v004.npz' % (W, cid)); r1 = np.load(R6[cid]); r0 = np.load('/home/claude/wayfarer-design/reviews/reference-assets/r6/SK_r6.npz'); fi = json.load(open('%s/anat/%s_v004_face_identity.json' % (W, cid)))
nz = np.load(NAT[cid]); si = nz['src_index']; h1 = r1['V'][si]; h0 = r0['V'][si]; wh = r1['w_head'][si]; we = r1['w_ears'][si]; ear_y = h1[we > 0.5, 1].mean(); face = (wh > 0.5) & (we == 0) & (h1[:, 1] > ear_y); cran = (wh > 0.5) & ~face
def kabsch(P, Q_):
    pc, qc = P.mean(0), Q_.mean(0); U, S_, Vt = np.linalg.svd((P - pc).T @ (Q_ - qc)); D = np.diag([1, 1, np.sign(np.linalg.det(Vt.T @ U.T))]); R = Vt.T @ D @ U.T; return R, qc - pc @ R.T
R, t = kabsch(h0[cran], h1[cran]); V0a = r0['V'] @ R.T + t
s1 = trimesh.Trimesh(r1['V'], r1['F'], process=False); s0 = trimesh.Trimesh(V0a, r0['F'], process=False); V4 = c4['V']; Q4 = c4['Q']
_, e1, _ = trimesh.proximity.closest_point(s1, V4); _, e0, _ = trimesh.proximity.closest_point(s0, V4)
meta = json.loads(str(nz['meta'])); eye = np.array(meta['eye_helpers']['helper-l-eye']); hc = eye * [0, 1, 1] + [0, -1.0, -2.5]; FV = [('front', (0, 1, 0.05), hc, 10), ('q3', (0.6, 0.8, 0.05), hc, 10)]
keep = r1['keep']; F1 = r1['F']; F0 = r0['F']
render(r1['V'], F1, np.tile(CLAY, (len(F1), 1)), 'fid_src', vs_(FV), '0', 600); render(V0a, F0, np.tile(CLAY, (len(F0), 1)), 'fid_pre', vs_(FV), '0', 600); render(V4, Q4, np.tile(CLAY, (len(Q4), 1)), 'fid_v4', vs_(FV), '0', 600)
render(V4, Q4, ramp(e1 * 10 / 3.0)[Q4].mean(1), 'fid_e1', vs_(FV), '0', 600); render(V4, Q4, ramp(e0 * 10 / 3.0)[Q4].mean(1), 'fid_e0', vs_(FV), '0', 600)
sheet('Skarn C1R identity gate - SK208-C1R central face', 'row 1: accepted C1R source | successor v004 | pre-C1R Skarn (rigidly aligned on cranium + ears). Row 2: v004 distance heat 0 .. 3 mm to the C1R source | to the pre-C1R source.',
      [('', [('fid_src', 'front', 'C1R source'), ('fid_v4', 'front', 'v004'), ('fid_pre', 'front', 'pre-C1R (aligned)'), ('fid_v4', 'q3', 'v004 3/4')]), ('', [('fid_e1', 'front', 'v004 -> C1R source'), ('fid_e1', 'q3', 'v004 -> C1R 3/4'), ('fid_e0', 'front', 'v004 -> pre-C1R'), ('fid_e0', 'q3', 'v004 -> pre-C1R 3/4')])], 380,
      SH + '/v004_C1R_face.jpg', ['face (anterior head) v004 -> C1R source median / p95 / max %(median).3f / %(p95).3f / %(max).3f mm' % fi['family_face_to_identity_source_mm'] + ' | v004 -> pre-C1R median / p95 / max %(median).3f / %(p95).3f / %(max).3f mm' % fi['family_face_to_pre_identity_source_mm'] + ' | identity signal mean %(mean).3f mm' % fi['identity_signal_mm']])
# ---- validator table (D1 + D3 + D4)
VJ = {c: json.load(open('%s/val/%s_v004_validator_v2_D4.json' % (W, c)))['stations'] for c in CFG}; ks = list(VJ['MF-M-R']); rh = 16; half = (len(ks) + 1) // 2
S = Image.new('RGB', (2 * 760 + 30, 90 + half * rh), 'white'); d = ImageDraw.Draw(S)
d.text((10, 8), 'MPFB Family Base v004 - 69-station validator, D1 + D3 + D4 (authoritative): loops / minimum, status (P = PASS, FD = PASS_FALLBACK_DEFINED_SIDES, FR = closed-ring fallback, +A = adjacent-digit pole scoped, F = FAIL)', fill=(0, 0, 0), font=f(12, True))
d.text((10, 28), 'firm PASS: ' + ', '.join('%s %d/69' % (c, sum(v['firm_D1_D3'] for v in VJ[c].values())) for c in CFG), fill=(60, 60, 60), font=f(11, True))
AB = lambda s: s.replace('PASS_FALLBACK_DEFINED_SIDES', 'FD').replace('PASS_FALLBACK_CLOSED_RING', 'FR').replace('+SCOPED_ADJACENT_DIGIT_POLE', '+A').replace('PASS_SCOPED_ADJACENT_DIGIT_POLE', 'P+A').replace('FAIL_LOOPS', 'F-loops').replace('FAIL_CREASE_POLE', 'F-pole').replace('PASS', 'P')
for blk in range(2):
    bx = 10 + blk * 770
    for j, c in enumerate(CFG): d.text((bx + 130 + j * 155, 52), {'MF-M-R': 'MF-M', 'MF-F-R': 'MF-F', 'SK208-C1R': 'SK-C1R', 'SKF208': 'SK-F'}[c], fill=(0, 0, 0), font=f(11, True))
    for i, k in enumerate(ks[blk * half:(blk + 1) * half]):
        y = 70 + i * rh; d.text((bx, y), k, fill=(0, 0, 0), font=f(11))
        for j, c in enumerate(CFG):
            v = VJ[c][k]; colr = (230, 80, 70) if not v['firm_D1_D3'] else ((245, 200, 80) if v['margin'] == 0 else (170, 225, 170)); x = bx + 130 + j * 155
            d.rectangle([x, y, x + 150, y + rh - 2], fill=colr); d.text((x + 3, y + 1), '%d/%d %s' % (v['loops_v2'], v['required'], AB(v['status_D1_D3'])), fill=(0, 0, 0), font=f(10))
S.save(SH + '/v004_validator_D4.jpg', quality=90)
# ---- change diagram
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
log = json.loads(str(core['log'])); fig, ax = plt.subplots(figsize=(15, 7.5)); ax.axis('off')
def box(x, y, w, h, t, fc):
    ax.add_patch(plt.Rectangle((x, y), w, h, fc=fc, ec='k', lw=1.2)); ax.text(x + w / 2, y + h / 2, t, ha='center', va='center', fontsize=9.5, wrap=True)
box(0.01, 0.38, 0.17, 0.24, 'FROZEN v003\nMPFB Family Base v1\n57,674 V / 57,672 Q\nface hash 68f7b6a9...\n(immutable, historical)', '#dde3ee')
ops = [('A  posterior-heel rows\n8 vertices (4 mirrored pairs)\nlinear quad-centre -> on-surface\nbarycentric (same hm08 quad)\ntopology unchanged', '#fff2b3'),
       ('B  hip support ring\n1 self-mirrored pelvis ring\n(v003 loops 195 | 790 strip)\n+84 V / +84 Q', '#f8c9c4'),
       ('C  toe-2 root ring (l + r)\nv003 loops 497 | 1262 strip\n+48 V / +48 Q', '#c9d8f8'),
       ('C  toe-3 root ring (l + r)\nv003 loops 508 | 1264 strip\n+48 V / +48 Q\n+ 4 forefoot poles slid 0.6-0.8 mm\n(22 rows) off the toe-3 crease', '#c9efc9')]
for i, (t_, fc) in enumerate(ops): box(0.26, 0.79 - i * 0.24, 0.24, 0.2, t_, fc); ax.annotate('', xy=(0.26, 0.89 - i * 0.24), xytext=(0.18, 0.5), arrowprops=dict(arrowstyle='->', lw=1))
box(0.58, 0.36, 0.18, 0.28, 'SUCCESSOR v004\nMPFB Family Base v2 candidate\n%d V / %d Q\nhm08 -> v004 map (rows <= 4)\nv003 -> v004 map\nrow classes: %s' % (log['verts'], log['quads'], ', '.join('%s:%d' % kv for kv in log['counts'].items())), '#e6d7f2')
for i in range(4): ax.annotate('', xy=(0.58, 0.5), xytext=(0.5, 0.89 - i * 0.24), arrowprops=dict(arrowstyle='->', lw=1))
for i, c in enumerate(CFG): box(0.83, 0.8 - i * 0.2, 0.16, 0.15, '%s\nM4 @ (race hm08 R-6)\nno per-race fitting' % c, '#eeeeee'); ax.annotate('', xy=(0.83, 0.875 - i * 0.2), xytext=(0.76, 0.5), arrowprops=dict(arrowstyle='->', lw=1))
ax.set_title('MPFB family topology change: frozen v003 -> margin-hardened successor v004 (one topology, four realizations)', fontsize=12); plt.savefig(SH + '/v004_change_diagram.jpg', dpi=110, bbox_inches='tight')
print('done')
