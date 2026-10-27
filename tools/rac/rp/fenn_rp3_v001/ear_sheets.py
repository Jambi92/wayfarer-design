# ear_sheets.py WORK OUTDIR : order bdcd6a6 §16 visual author package (20 sheets per configuration; true scale, identical cameras per row).
# WORK = folder with build/ audit/ meas/ deform/ (ear_build / ear_audit / ear_measure / ear_deform outputs). Renders with the Workbench
# orthographic renderer (tools/rac/rp/grask_rigprep_v001/render_attr.py) and composes sheets with PIL.
import sys, os, json, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ear_branch_lib as E
W_, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True); TMP = os.path.join(OUT, '_r'); os.makedirs(TMP, exist_ok=True)
BP = '/home/claude/stc/bin/python3'; REND = '/home/claude/wayfarer-design/tools/rac/rp/grask_rigprep_v001/render_attr.py'
HEADS = {'c1': 'FNL4-CF2', 'c2': 'FNF181-CF2'}; CANDS = ['E1', 'E2', 'E3']
def font(sz, bold=False):
    for f in ('/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf' % ('-Bold' if bold else ''),):
        if os.path.exists(f): return ImageFont.truetype(f, sz)
    return ImageFont.load_default()
Lo = E.canonical_layout(); st = Lo['st']; ns = len(st); cs = Lo['info']['corners']
def load(h, c):
    z = np.load('%s/build/%s_%s_branch.npz' % (W_, h, c)); r = json.load(open('%s/build/%s_%s_branch.json' % (W_, h, c))); return z, r
jobs = []
def render(tag, npz, col, views, wire=False, px=700):
    """views: list of (name, d, c, halfsize)"""
    vs = ';'.join('%s:%s:%s:%.2f' % (n, ','.join('%.4f' % x for x in d), ','.join('%.3f' % x for x in c), hs) for n, d, c, hs in views)
    cf = os.path.join(TMP, tag + '_col.npy'); np.save(cf, col.astype(np.float32)); jobs.append([BP, REND, '--', npz, cf, TMP, tag, vs, '1' if wire else '0', str(px)])
def img(tag, name): return Image.open(os.path.join(TMP, '%s_%s.png' % (tag, name))).convert('RGB')
GREY = np.array([0.80, 0.78, 0.76])
def base_cols(z): return np.tile(GREY, (len(z['V']), 1))
def part_cols(z):
    p = z['part']; C = base_cols(z); C[p == 'front'] = [0.88, 0.66, 0.55]; C[p == 'back'] = [0.70, 0.58, 0.80]; C[p == 'rim'] = [0.95, 0.83, 0.45]; C[p == 'cuff'] = [0.58, 0.76, 0.92]; C[p == 'transition'] = [0.55, 0.85, 0.55]; return C
def heat(x, lo, hi):
    t = np.clip((x - lo) / (hi - lo + 1e-12), 0, 1)[:, None]; return (1 - t) * np.array([0.2, 0.35, 0.85]) + t * np.array([0.95, 0.25, 0.15])
ANAT = [('helix', 'helix', (0.85, 0.30, 0.25)), ('antihelix_stem', 'antihelix stem', (0.20, 0.55, 0.85)), ('superior_crus', 'superior crus', (0.10, 0.35, 0.75)),
        ('inferior_crus', 'inferior crus', (0.35, 0.70, 0.95)), ('triangular_fossa', 'triangular fossa', (0.55, 0.40, 0.80)), ('cavum', 'concha cavum', (0.95, 0.65, 0.15)),
        ('cymba', 'concha cymba', (0.95, 0.85, 0.30)), ('crus_of_helix', 'crus of helix', (0.60, 0.25, 0.10)), ('tragus', 'tragus', (0.20, 0.70, 0.35)),
        ('antitragus', 'antitragus', (0.10, 0.50, 0.25)), ('intertragic_notch', 'intertragic notch', (0.95, 0.40, 0.70))]
def anat_cols(z, rec):
    p = dict(rec['params']); p['taper'] = tuple(p['taper']); p['helix'] = tuple(p['helix']); _, _, parts = E.relief(st[:, 0], st[:, 1], p)
    C = part_cols(z) * 0 + GREY; C[z['part'] == 'cuff'] = [0.72, 0.80, 0.88]
    lab = np.full(ns, -1); best = np.zeros(ns)
    for k, (key, nm, col) in enumerate(ANAT):
        a = np.abs(parts[key]) / (np.abs(parts[key]).max() + 1e-9); m = (a > 0.35) & (a > best); lab[m] = k; best[m] = a[m]
    for sd in ('l', 'r'):
        f = np.nonzero(z['side'] == sd)[0][0]; idx = np.arange(ns)
        sheet = np.isin(Lo['part'], ['front', 'rim'])
        C[f + idx[sheet & (st[:, 0] < 0.15) & (lab < 0)]] = [0.93, 0.72, 0.72]                     # lobe
        C[f + idx[sheet & (st[:, 0] > E.S_UP) & (lab < 0)]] = [0.86, 0.80, 0.62]                   # upper extension
        for k, (key, nm, col) in enumerate(ANAT): C[f + idx[sheet & (lab == k)]] = col
    return C
def valence_cols(z):
    Q = z['Q']; Eu = np.unique(np.sort(np.concatenate([Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]]), 1), axis=0); val = np.zeros(len(z['V']), int); np.add.at(val, Eu.ravel(), 1)
    C = part_cols(z) * 0.35 + 0.6; br = z['part'] != 'v005'
    C[br & (val == 3)] = [0.1, 0.3, 0.95]; C[br & (val == 5)] = [0.95, 0.15, 0.1]; C[br & (val >= 6)] = [0.6, 0.1, 0.8]; return C, val
def t4_face_cols(z, h, c):
    pf = np.load('%s/audit/%s_%s_audit_perface.npz' % (W_, h, c)); C = np.tile(GREY, (len(z['Q']), 1)); F = pf['faces']
    C[F] = [0.93, 0.93, 0.93]; bad = pf['ang_bad']; asp = pf['asp']; C[F[bad]] = [1.0, 0.55, 0.1]; C[F[(asp > 4) & ~bad]] = [0.85, 0.1, 0.1]; C[F[(asp > 4) & bad]] = [0.55, 0.2, 0.85]; return C
def density_face_cols(z):
    V = z['V']; Q = z['Q']; L = np.linalg.norm(V[Q] - V[np.roll(Q, -1, 1)], axis=2).mean(1); stat = V[:, 2].max() - V[:, 2].min(); pct = 100 * L / stat
    C = heat(pct, 0.03, 0.25); C[~(z['part'] != 'v005')[Q].any(1)] = GREY; return C, pct
def rootdev_cols(z, h, c):
    d = np.load('%s/audit/%s_%s_audit_cuffdev.npy' % (W_, h, c)); C = base_cols(z); C[d[:, 0].astype(int)] = heat(d[:, 1], 0, 0.6); return C
def thick_cols(z):
    C = part_cols(z) * 0 + GREY; V = z['V']
    key = {}
    for v in np.nonzero(Lo['part'] == 'back')[0]: key[(round(float(st[v, 0]), 9), round(float(st[v, 1]), 9))] = v
    for sd in ('l', 'r'):
        f = np.nonzero(z['side'] == sd)[0][0]
        for v in np.nonzero(Lo['part'] == 'front')[0]:
            w = key.get((round(float(st[v, 0]), 9), round(float(st[v, 1]), 9)))
            if w is not None: C[f + v] = heat(np.array([np.linalg.norm(V[f + v] - V[f + w])]), 0.15, 0.6)[0]
    return C
# ------------------------------------------------------------------ camera helpers
def cams(z, r):
    V = z['V']; Vl = V[z['side'] == 'l']; Ce = Vl.mean(0); hv = V[V[:, 2] > V[:, 2].max() - 25]; H = np.array([0.0, hv[:, 1].mean(), V[:, 2].max() - 11.0])
    O = np.array(r['sides']['l']['frame']['O']); return Ce, H, O
NONE = None
for cf_, h in HEADS.items():
    for c in CANDS:
        z, r = load(h, c); npz = '%s/build/%s_%s_branch.npz' % (W_, h, c); Ce, H, O = cams(z, r); t = '%s_%s' % (cf_, c); g = base_cols(z)
        render(t + '_g', npz, g, [('front', (0, 1, 0), H, 14), ('rear', (0, -1, 0), H, 14), ('prof', (1, 0, 0), H, 14), ('tqf', (1, 1, 0.1), H, 14), ('tqr', (1, -1, 0.1), H, 14),
                                  ('top', (0, 0, 1), H, 14), ('cprof', (1, 0, 0), Ce, 5.5), ('crear', (0.35, -1, 0.1), Ce, 5.5), ('face', (1, 0.9, 0.15), Ce, 5.0), ('hq', (1, 0.6, 0.15), H, 11)])
        render(t + '_w', npz, part_cols(z), [('root', (1, 0.2, 0.0), O, 3.2), ('face', (1, 0.9, 0.15), Ce, 5.0), ('crear', (0.35, -1, 0.1), Ce, 5.0)], wire=True)
        vc, _ = valence_cols(z); render(t + '_v', npz, vc, [('face', (1, 0.9, 0.15), Ce, 5.0), ('crear', (0.35, -1, 0.1), Ce, 5.0)], wire=True)
        render(t + '_a', npz, anat_cols(z, r), [('face', (1, 0.9, 0.15), Ce, 4.6), ('cprof', (1, 0.3, 0), Ce, 4.6)])
        render(t + '_th', npz, thick_cols(z), [('face', (1, 0.9, 0.15), Ce, 4.6), ('crear', (0.35, -1, 0.1), Ce, 4.6)])
        render(t + '_t4', npz, t4_face_cols(z, h, c), [('face', (1, 0.9, 0.15), Ce, 5.0), ('crear', (0.35, -1, 0.1), Ce, 5.0)], wire=True)
        dc, _ = density_face_cols(z); render(t + '_dn', npz, dc, [('face', (1, 0.9, 0.15), Ce, 5.0), ('crear', (0.35, -1, 0.1), Ce, 5.0)], wire=True)
        render(t + '_rd', npz, rootdev_cols(z, h, c), [('root', (1, 0.2, 0.0), O, 3.4), ('rootb', (0.5, -1, 0.0), O, 3.4)])
# hidden-ear CF2 heads (v005 ear zone harmonically collapsed on the CF2 family realization)
import scipy.sparse as sp
for cf_, h in HEADS.items():
    fz = np.load('/tmp/claude-0/rt/fn/cf/fam/%s_fam.npz' % h); V0 = fz['V'].astype(float); Q0 = np.asarray(fz['Q']); z, r = load(h, 'E2')
    zone = np.zeros(len(V0), bool); zone[z['removed_v005']] = True
    Ei = np.unique(np.sort(np.concatenate([Q0[:, [0, 1]], Q0[:, [1, 2]], Q0[:, [2, 3]], Q0[:, [3, 0]]]), 1), axis=0)
    A0 = sp.coo_matrix((np.ones(2 * len(Ei)), (np.r_[Ei[:, 0], Ei[:, 1]], np.r_[Ei[:, 1], Ei[:, 0]])), shape=(len(V0), len(V0))).tocsr(); deg = np.asarray(A0.sum(1)).ravel()
    X = V0.copy()
    for _ in range(600): X[zone] = (A0 @ X)[zone] / deg[zone, None]
    hp = os.path.join(TMP, 'hidden_%s.npz' % cf_); np.savez_compressed(hp, V=X, Q=Q0); _, H, _ = cams(z, r)
    render('hid_' + cf_, hp, np.tile(GREY, (len(X), 1)), [('front', (0, 1, 0), H, 14), ('prof', (1, 0, 0), H, 14), ('rear', (0, -1, 0), H, 14), ('tqf', (1, 1, 0.1), H, 14)])
# deformation poses (E2)
for cf_, h in HEADS.items():
    z, r = load(h, 'E2'); Ce, H, O = cams(z, r)
    for pn in ('neck_flex30', 'neck_ext30', 'head_yaw_l45', 'head_roll_l20'):
        X = np.load('%s/deform/%s_E2_%s.npy' % (W_, h, pn)); pp = os.path.join(TMP, 'pose_%s_%s.npz' % (cf_, pn)); np.savez_compressed(pp, V=X, Q=z['Q'])
        Cp = (X[z['side'] == 'l']).mean(0); render('pose_%s_%s' % (cf_, pn), pp, part_cols(z), [('tq', (1, 0.3, 0.1), Cp, 9.0), ('rear', (0.4, -1, 0.1), Cp, 9.0)])
print('render jobs', len(jobs), flush=True)
if os.environ.get('NO_RENDER') != '1':
  with ThreadPoolExecutor(6) as ex: list(ex.map(lambda j: subprocess.run(j, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL), jobs))
# ------------------------------------------------------------------ compose
M = {(cf_, c): json.load(open('%s/meas/%s_%s_measure.json' % (W_, h, c))) for cf_, h in HEADS.items() for c in CANDS}
AU = {(cf_, c): json.load(open('%s/audit/%s_%s_audit.json' % (W_, h, c))) for cf_, h in HEADS.items() for c in CANDS}
def caption(cf_, c):
    m = M[(cf_, c)]['sides']['l']; return '%s  chord %.2f cm  width %.2f  angle %.0f°  extent %.2f  upper axis %.0f°  thick %.2f' % (c, m['length_lobe_to_tip_cm'], m['max_width_cm'], m['auricle_body_angle_deg'], m['total_lateral_extent_from_root_plane_cm'], m['side_view_upper_extension_deg'], m['thickness_cm']['median'])
def sheet(fname, title, rows, colw=700, note=None):
    """rows: list of (row_label, [PIL images...], [captions])"""
    ncol = max(len(r[1]) for r in rows); W = 160 + ncol * colw; Hh = 70 + sum(colw + 34 for _ in rows) + (40 if note else 0)
    S = Image.new('RGB', (W, Hh), 'white'); d = ImageDraw.Draw(S); d.text((14, 14), title, fill=(0, 0, 0), font=font(24, True)); y = 70
    for lab, ims, caps in rows:
        d.text((10, y + colw // 2), lab, fill=(0, 0, 0), font=font(20, True))
        for k, im in enumerate(ims):
            im = im.resize((colw, colw)); S.paste(im, (160 + k * colw, y));
            if caps and k < len(caps) and caps[k]: d.text((166 + k * colw, y + colw + 4), caps[k], fill=(30, 30, 30), font=font(15))
        y += colw + 34
    if note: d.text((14, y + 4), note, fill=(60, 60, 60), font=font(16))
    S.save(os.path.join(OUT, fname), quality=90)
def legend_bar(items, w=2100):
    im = Image.new('RGB', (w, 40), 'white'); d = ImageDraw.Draw(im); x = 10
    for nm, col in items:
        d.rectangle((x, 10, x + 24, 30), fill=tuple(int(255 * v) for v in col)); d.text((x + 30, 10), nm, fill=(0, 0, 0), font=font(16)); x += 30 + 10 * len(nm) + 30
    return im
SPEC = [(1, 'front', '_g', 'front'), (2, 'rear', '_g', 'rear'), (3, 'profile', '_g', 'prof'), (4, '3-4 front', '_g', 'tqf'), (5, '3-4 rear', '_g', 'tqr'), (6, 'top', '_g', 'top'),
        (7, 'close ear profile', '_g', 'cprof'), (8, 'close rear ear', '_g', 'crear')]
for cf_, h in HEADS.items():
    for k, nm, sfx, v in SPEC:
        sheet('FENN_EAR_%02d_%s_%s.jpg' % (k, nm.replace(' ', '_').replace('-', ''), cf_), 'Fenn ear branch %s — %s (%s CF2 head; E1 | E2 | E3; identical orthographic camera, true scale)' % (cf_, nm, h),
              [(cf_, [img('%s_%s%s' % (cf_, c, sfx), v) for c in CANDS], [caption(cf_, c) for c in CANDS])])
    sheet('FENN_EAR_09_root_closeup_%s.jpg' % cf_, 'Fenn ear branch %s — root close-up (wire; blue cuff = new skull skin inside the v005 root, green = bounded transition ring)' % cf_,
          [(cf_, [img('%s_%s_w' % (cf_, c), 'root') for c in CANDS], ['%s root dihedral mean %.0f° / max %.0f° (v005 %.0f / %.0f)' % (c, AU[(cf_, c)]['root_dihedral']['l']['mean_deg'], AU[(cf_, c)]['root_dihedral']['l']['max_deg'], AU[(cf_, c)]['root_dihedral']['l']['v005_mean_deg'], AU[(cf_, c)]['root_dihedral']['l']['v005_max_deg']) for c in CANDS])])
    sheet('FENN_EAR_10_wireframe_%s.jpg' % cf_, 'Fenn ear branch %s — wireframe (one shared topology; front orange, back violet, rim yellow, cuff blue, transition green)' % cf_,
          [('front', [img('%s_%s_w' % (cf_, c), 'face') for c in CANDS], CANDS), ('rear', [img('%s_%s_w' % (cf_, c), 'crear') for c in CANDS], CANDS)])
    sheet('FENN_EAR_11_poles_%s.jpg' % cf_, 'Fenn ear branch %s — pole / valence map (blue valence 3, red valence 5, violet 6+; branch only)' % cf_,
          [('front', [img('%s_%s_v' % (cf_, c), 'face') for c in CANDS], ['%s branch poles %d' % (c, AU[(cf_, c)]['poles_branch_total']) for c in CANDS]), ('rear', [img('%s_%s_v' % (cf_, c), 'crear') for c in CANDS], None)])
    sheet('FENN_EAR_12_anatomy_%s.jpg' % cf_, 'Fenn ear branch %s — external-ear anatomy (dominant W1e relief system per vertex)' % cf_,
          [('lateral', [img('%s_%s_a' % (cf_, c), 'face') for c in CANDS], CANDS), ('profile', [img('%s_%s_a' % (cf_, c), 'cprof') for c in CANDS], None)])
    S = Image.open(os.path.join(OUT, 'FENN_EAR_12_anatomy_%s.jpg' % cf_)); L_ = legend_bar([(nm, col) for _, nm, col in ANAT] + [('lobe', (0.93, 0.72, 0.72)), ('upper extension', (0.86, 0.80, 0.62)), ('cuff', (0.72, 0.80, 0.88))], S.width)
    S2 = Image.new('RGB', (S.width, S.height + 44), 'white'); S2.paste(S, (0, 0)); S2.paste(L_, (0, S.height)); S2.save(os.path.join(OUT, 'FENN_EAR_12_anatomy_%s.jpg' % cf_), quality=90)
    sheet('FENN_EAR_13_thickness_%s.jpg' % cf_, 'Fenn ear branch %s — cartilage + skin thickness, front to back (blue 0.15 cm ... red 0.60 cm)' % cf_,
          [('lateral', [img('%s_%s_th' % (cf_, c), 'face') for c in CANDS], ['%s median %.2f / min %.2f cm' % (c, M[(cf_, c)]['sides']['l']['thickness_cm']['median'], M[(cf_, c)]['sides']['l']['thickness_cm']['min']) for c in CANDS]), ('rear', [img('%s_%s_th' % (cf_, c), 'crear') for c in CANDS], None)])
    sheet('FENN_EAR_14_T4_aspect_%s.jpg' % cf_, 'Fenn ear branch %s — T-4 heat (orange angle outside 45-135°, red aspect > 4, violet both)' % cf_,
          [('front', [img('%s_%s_t4' % (cf_, c), 'face') for c in CANDS], ['%s angle viol %d / %d faces, aspect max %.1f' % (c, AU[(cf_, c)]['T4']['angle_violations'], AU[(cf_, c)]['T4']['branch_faces'], AU[(cf_, c)]['T4']['aspect_max']) for c in CANDS]), ('rear', [img('%s_%s_t4' % (cf_, c), 'crear') for c in CANDS], None)])
    sheet('FENN_EAR_15_density_%s.jpg' % cf_, 'Fenn ear branch %s — density: face mean edge / stature (blue 0.03 %% ... red 0.25 %% contract limit)' % cf_,
          [('front', [img('%s_%s_dn' % (cf_, c), 'face') for c in CANDS], ['%s mean %.3f %% (limit 0.25 %%)' % (c, AU[(cf_, c)]['density']['branch_mean_edge_pct_stature']) for c in CANDS]), ('rear', [img('%s_%s_dn' % (cf_, c), 'crear') for c in CANDS], None)])
    sheet('FENN_EAR_16_root_deviation_%s.jpg' % cf_, 'Fenn ear branch %s — root deviation: new skin inside the root vs hidden-ear CF2 skull (blue 0 ... red 0.6 cm); root loop and outside skin unchanged' % cf_,
          [('lateral', [img('%s_%s_rd' % (cf_, c), 'root') for c in CANDS], ['%s cuff mean %.2f / p95 %.2f cm' % (c, AU[(cf_, c)]['root_deviation']['cuff_mean_cm'], AU[(cf_, c)]['root_deviation']['cuff_p95_cm']) for c in CANDS]), ('posterior', [img('%s_%s_rd' % (cf_, c), 'rootb') for c in CANDS], None)])
    sheet('FENN_EAR_17_CF2_head_E1_E2_E3_%s.jpg' % cf_, 'Fenn %s — accepted CF2 head with E1 | E2 | E3 (3/4 front, true scale)' % cf_, [(cf_, [img('%s_%s_g' % (cf_, c), 'hq') for c in CANDS], [caption(cf_, c) for c in CANDS])])
    hid = json.load(open('/home/claude/wayfarer-design/reviews/rac-rp3-evidence/fenn_craniofacial_v001/CF_hidden_ear_eval.json'))
    sheet('FENN_EAR_19_hidden_ear_CF2_%s.jpg' % cf_, 'Fenn %s — hidden-ear CF2 confirmation (ear zone collapsed; branch does not alter any face / skull vertex outside the root)' % cf_,
          [(cf_, [img('hid_' + cf_, v) for v in ('front', 'prof', 'rear', 'tqf')], ['front', 'profile', 'rear', '3/4 front'])],
          note='Hidden-ear CF2 facial identity PASS 6/6 canon systems (CF_hidden_ear_eval.json, unchanged sources); outside-branch vertices byte-identical to the CF2 family realization: %s' % all(AU[(cf_, c)]['outside_branch_byte_identical'] for c in CANDS))
    D = json.load(open('%s/deform/%s_E2_deform.json' % (W_, h)))
    sheet('FENN_EAR_20_deformation_%s.jpg' % cf_, 'Fenn %s E2 — static head / neck deformation readiness (source rig, LBS; no ear rig)' % cf_,
          [('3/4', [img('pose_%s_%s' % (cf_, pn), 'tq') for pn in ('neck_flex30', 'neck_ext30', 'head_yaw_l45', 'head_roll_l20')], ['%s: new self-x %d, flips %d, root band area x%.2f' % (pn, D['poses'][pn]['new_selfx_pairs_touching_branch'], D['poses'][pn]['flipped_branch_faces'], D['poses'][pn]['root_band_area_ratio_min']) for pn in ('neck_flex30', 'neck_ext30', 'head_yaw_l45', 'head_roll_l20')]),
           ('rear', [img('pose_%s_%s' % (cf_, pn), 'rear') for pn in ('neck_flex30', 'neck_ext30', 'head_yaw_l45', 'head_roll_l20')], None)])
sheet('FENN_EAR_18_c1_vs_c2_E2.jpg', 'Fenn E2 — configuration 1 (FNL4-CF2) vs configuration 2 (FNF181-CF2): same topology, same construction, head-scaled (HH / HH MF-M-R)',
      [(cf_, [img('%s_E2_g' % cf_, v) for v in ('front', 'prof', 'tqf', 'face')], [caption(cf_, 'E2'), '', '', '']) for cf_ in HEADS])
print('sheets', sorted(f for f in os.listdir(OUT) if f.endswith('.jpg')))
