# ear_sheets_v002.py V001_WORK V002_WORK OUTDIR : order 0d9c70b §17 visual acceptance package -- v001 E2 | v002 E2 side by side for c1 and c2,
# identical cameras per sheet (computed once per configuration from the v002 realization), true scale; Workbench orthographic renders.
import sys, os, json, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
from concurrent.futures import ThreadPoolExecutor
os.environ.setdefault('EAR_TOPO', 'v002')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ear_branch_lib as E, ear_zones as Z
W1, W2, OUT = sys.argv[1:4]; os.makedirs(OUT, exist_ok=True); TMP = os.path.join(OUT, '_r'); os.makedirs(TMP, exist_ok=True)
BP = '/home/claude/stc/bin/python3'; REND = '/home/claude/wayfarer-design/tools/rac/rp/grask_rigprep_v001/render_attr.py'
EV1 = '/home/claude/wayfarer-design/reviews/rac-rp3-evidence/fenn_ear_branch_v001'
HEADS = {'c1': 'FNL4-CF2', 'c2': 'FNF181-CF2'}; VER = {'v001': W1, 'v002': W2}
GREY = np.array([0.80, 0.78, 0.76])
def font(sz, bold=False):
    f = '/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf' % ('-Bold' if bold else '')
    return ImageFont.truetype(f, sz) if os.path.exists(f) else ImageFont.load_default()
# ---- topologies of both versions (sheet parameters, parts, corners, zone labels)
L2 = E.canonical_layout()
t1 = np.load(os.path.join(EV1, 'topology/FENN_EAR_BRANCH_TOPOLOGY_v001.npz')); j1 = json.load(open(os.path.join(EV1, 'topology/FENN_EAR_BRANCH_TOPOLOGY_v001.json')))
TOP = {'v001': dict(st=t1['sheet_st'], part=t1['sheet_part'], corners=j1['corners'], J=t1['junction_ring']),
       'v002': dict(st=L2['st'], part=L2['part'], corners=L2['info']['corners'], J=L2['J'])}
def load(ver, h):
    z = np.load('%s/build/%s_E2_branch.npz' % (VER[ver], h)); r = json.load(open('%s/build/%s_E2_branch.json' % (VER[ver], h))); return z, r
def zones(ver, h):
    """per-face zone labels + angle / aspect (v002: ear_zones on the v002 layout; v001: audit per-face arrays)"""
    z, r = load(ver, h); pf = np.load('%s/audit/%s_E2_audit_perface.npz' % (VER[ver], h)); return pf['faces'], pf['ang_bad'], pf['asp']
AU = {(v, c): json.load(open('%s/audit/%s_E2_audit.json' % (VER[v], h))) for v in VER for c, h in HEADS.items()}
ZR = json.load(open(os.path.join(OUT, '..', 'FENN_EAR_v001_v002_zone_report.json'))) if os.path.exists(os.path.join(OUT, '..', 'FENN_EAR_v001_v002_zone_report.json')) else None
jobs = []
def render(tag, npz, col, views, wire=False, px=640):
    vs = ';'.join('%s:%s:%s:%.2f' % (n, ','.join('%.4f' % x for x in d), ','.join('%.3f' % x for x in c), hs) for n, d, c, hs in views)
    cf = os.path.join(TMP, tag + '_col.npy'); np.save(cf, np.asarray(col, np.float32)); jobs.append([BP, REND, '--', npz, cf, TMP, tag, vs, '1' if wire else '0', str(px)])
def img(tag, name): return Image.open(os.path.join(TMP, '%s_%s.png' % (tag, name))).convert('RGB')
def base_cols(z): return np.tile(GREY, (len(z['V']), 1))
def part_cols(z):
    p = z['part']; C = base_cols(z); C[p == 'front'] = [0.88, 0.66, 0.55]; C[p == 'back'] = [0.70, 0.58, 0.80]; C[p == 'rim'] = [0.95, 0.83, 0.45]
    C[p == 'cuff'] = [0.58, 0.76, 0.92]; C[p == 'transition'] = [0.55, 0.85, 0.55]; return C
def heat(x, lo, hi):
    t = np.clip((x - lo) / (hi - lo + 1e-12), 0, 1)[:, None]; return (1 - t) * np.array([0.2, 0.35, 0.85]) + t * np.array([0.95, 0.25, 0.15])
def face_part(z):
    p = z['part'][z['Q']]; C = np.tile(GREY, (len(z['Q']), 1))
    for k, col in (('transition', [0.55, 0.85, 0.55]), ('cuff', [0.58, 0.76, 0.92]), ('back', [0.70, 0.58, 0.80]), ('front', [0.88, 0.66, 0.55]), ('rim', [0.95, 0.83, 0.45])):
        C[(p == k).any(1)] = col
    return C
def t4_cols(ver, h, z):
    F, bad, asp = zones(ver, h); C = face_part(z) * 0.45 + 0.5; C[F] = [0.93, 0.93, 0.93]; C[F[bad]] = [0.92, 0.18, 0.12]; return C
def asp_cols(ver, h, z):
    F, bad, asp = zones(ver, h); C = np.tile(GREY, (len(z['Q']), 1)); C[F] = heat(asp, 1.0, 6.0); C[F[asp > 6]] = [0.55, 0.1, 0.65]; return C
def valence_cols(z):
    Q = z['Q']; Eu = np.unique(np.sort(np.concatenate([Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]]), 1), axis=0); val = np.zeros(len(z['V']), int); np.add.at(val, Eu.ravel(), 1)
    C = part_cols(z) * 0.35 + 0.6; br = z['part'] != 'v005'
    C[br & (val == 3)] = [0.1, 0.3, 0.95]; C[br & (val == 5)] = [0.95, 0.15, 0.1]; C[br & (val >= 6)] = [0.6, 0.1, 0.8]; return C
def rootdev_cols(ver, h, z):
    d = np.load('%s/audit/%s_E2_audit_cuffdev.npy' % (VER[ver], h)); C = base_cols(z); C[d[:, 0].astype(int)] = heat(d[:, 1], 0, 0.6); return C
def thick_cols(ver, z):
    st = TOP[ver]['st']; pt = TOP[ver]['part']; C = base_cols(z); V = z['V']; key = {}
    for v in np.nonzero(pt == 'back')[0]: key[(round(float(st[v, 0]), 9), round(float(st[v, 1]), 9))] = v
    for sd in ('l', 'r'):
        f = np.nonzero(z['side'] == sd)[0][0]
        for v in np.nonzero(pt == 'front')[0]:
            w = key.get((round(float(st[v, 0]), 9), round(float(st[v, 1]), 9)))
            if w is not None: C[f + v] = heat(np.array([np.linalg.norm(V[f + v] - V[f + w])]), 0.15, 0.6)[0]
    return C
def transition_cols(z):
    """cuff faces: count-transition quads (a vertex of the band appears 3 times on one ring) magenta; others by part"""
    C = face_part(z); Q = z['Q']; p = z['part']; cf = np.nonzero((p[Q] == 'cuff').any(1))[0]
    Eu = np.unique(np.sort(np.concatenate([Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]]), 1), axis=0); val = np.zeros(len(z['V']), int); np.add.at(val, Eu.ravel(), 1)
    irr = (val != 4) & (p == 'cuff'); C[cf[irr[Q[cf]].any(1)]] = [0.85, 0.25, 0.75]; return C
# ---- cameras (from the v002 realization of each configuration; used for both versions)
CAM = {}
for c, h in HEADS.items():
    z, r = load('v002', h); V = z['V']; Ce = V[z['side'] == 'l'].mean(0); hv = V[V[:, 2] > V[:, 2].max() - 25]; H = np.array([0.0, hv[:, 1].mean(), V[:, 2].max() - 11.0])
    O = np.array(r['sides']['l']['frame']['O']); f0 = int(np.nonzero(z['side'] == 'l')[0][0]); cs = TOP['v002']['corners']
    up = f0 + np.nonzero((TOP['v002']['part'] != 'rim') & (TOP['v002']['st'][:, 0] > E.S_UP))[0]; Cu = V[up].mean(0)
    CAM[c] = dict(H=H, Ce=Ce, O=O, Cu=Cu, c0=V[f0 + cs['c0']], c1=V[f0 + cs['c1']], c0f=V[f0 + cs['c0f']])
def views(c, names):
    k = CAM[c]; D = dict(front=((0, 1, 0), k['H'], 14), rear=((0, -1, 0), k['H'], 14), prof=((1, 0, 0), k['H'], 14), tqf=((1, 1, 0.1), k['H'], 14), tqr=((1, -1, 0.1), k['H'], 14),
                         top=((0, 0, 1), k['H'], 14), face=((1, 0.9, 0.15), k['Ce'], 4.6), crear=((0.35, -1, 0.1), k['Ce'], 4.6), upper=((1, 0.5, 0.3), k['Cu'], 2.4),
                         root=((1, 0.2, 0.0), k['O'], 3.4), under=((0.3, -0.5, -1), k['Ce'], 3.6), c0=((1, 0.5, -0.25), k['c0'], 1.3), c1=((1, 0.5, 0.25), k['c1'], 1.3),
                         low=((0.2, -1, -0.35), k['Ce'] + np.array([0, 0, -2.0]), 3.0), lobe=((1, 0.2, -0.6), k['c0f'], 1.6))
    return [(n,) + D[n] for n in names]
for c, h in HEADS.items():
    for ver in VER:
        z, r = load(ver, h); npz = '%s/build/%s_E2_branch.npz' % (VER[ver], h); t = '%s_%s' % (c, ver)
        render(t + '_g', npz, base_cols(z), views(c, ['front', 'rear', 'prof', 'tqf', 'tqr', 'top', 'face', 'crear', 'low', 'lobe']))
        render(t + '_w', npz, part_cols(z), views(c, ['face', 'crear', 'upper', 'root', 'under', 'c0', 'c1', 'lobe']), wire=True)
        render(t + '_tr', npz, transition_cols(z), views(c, ['root', 'under']), wire=True)
        render(t + '_v', npz, valence_cols(z), views(c, ['face', 'crear', 'root']), wire=True)
        render(t + '_t4', npz, t4_cols(ver, h, z), views(c, ['face', 'crear', 'root', 'upper']), wire=True)
        render(t + '_as', npz, asp_cols(ver, h, z), views(c, ['face', 'crear', 'root']), wire=True)
        render(t + '_rd', npz, rootdev_cols(ver, h, z), views(c, ['root', 'under']))
        render(t + '_th', npz, thick_cols(ver, z), views(c, ['face', 'crear']))
        for pn in ('neck_flex30', 'neck_ext30', 'head_yaw_l45', 'head_roll_l20'):
            X = np.load('%s/deform/%s_E2_%s.npy' % (VER[ver], h, pn)); pp = os.path.join(TMP, 'pose_%s_%s_%s.npz' % (c, ver, pn)); np.savez_compressed(pp, V=X, Q=z['Q'])
            Cp = X[z['side'] == 'l'].mean(0); render('pose_%s_%s_%s' % (c, ver, pn), pp, part_cols(z), [('tq', (1, 0.3, 0.1), Cp, 8.0)])
# probes (configuration 1): v001 and v002, same camera
PROBES = ['proj_m10', 'proj_p10', 'tilt_m8', 'tilt_p8', 'sweep_m06', 'sweep_p06', 'len_m10', 'len_p10', 'tip_blunt', 'tip_sharp']
for ver in VER:
    for pn in PROBES:
        npz = '%s/probe/%s/FNL4-CF2_E2_branch.npz' % (VER[ver], pn); z = np.load(npz); render('pr_%s_%s' % (ver, pn), npz, part_cols(z), views('c1', ['face']), wire=True, px=420)
# hidden-ear CF2 heads
import scipy.sparse as sp
for c, h in HEADS.items():
    fz = np.load('/tmp/claude-0/rt/fn/cf/fam/%s_fam.npz' % h); V0 = fz['V'].astype(float); Q0 = np.asarray(fz['Q']); z, r = load('v002', h)
    zone = np.zeros(len(V0), bool); zone[z['removed_v005']] = True
    Ei = np.unique(np.sort(np.concatenate([Q0[:, [0, 1]], Q0[:, [1, 2]], Q0[:, [2, 3]], Q0[:, [3, 0]]]), 1), axis=0)
    A0 = sp.coo_matrix((np.ones(2 * len(Ei)), (np.r_[Ei[:, 0], Ei[:, 1]], np.r_[Ei[:, 1], Ei[:, 0]])), shape=(len(V0), len(V0))).tocsr(); deg = np.asarray(A0.sum(1)).ravel()
    X = V0.copy()
    for _ in range(600): X[zone] = (A0 @ X)[zone] / deg[zone, None]
    hp = os.path.join(TMP, 'hidden_%s.npz' % c); np.savez_compressed(hp, V=X, Q=Q0)
    render('hid_' + c, hp, np.tile(GREY, (len(X), 1)), views(c, ['front', 'prof', 'rear', 'tqf']))
print('render jobs', len(jobs), flush=True)
if os.environ.get('NO_RENDER') != '1':
    done_ = lambda j: all(os.path.exists(os.path.join(TMP, '%s_%s.png' % (j[6], v_.split(':')[0]))) for v_ in j[7].split(';'))   # resume: skip finished jobs
    todo = [j for j in jobs if not done_(j)]; print('to render', len(todo), flush=True)
    with ThreadPoolExecutor(int(os.environ.get('EAR_SHEET_THREADS', '2'))) as ex: list(ex.map(lambda j: subprocess.run(j, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL), todo))   # 2 Blender processes: 6 ran out of memory on this 7 GB machine
# ------------------------------------------------------------------ compose
def sheet(fname, title, rows, colw=640, note=None, lab_w=150):
    ncol = max(len(r_[1]) for r_ in rows); Wd = lab_w + ncol * colw; Hh = 70 + sum(colw + 34 for _ in rows) + (44 if note else 0)
    S = Image.new('RGB', (Wd, Hh), 'white'); d = ImageDraw.Draw(S); d.text((14, 14), title, fill=(0, 0, 0), font=font(22, True)); y = 70
    for lab, ims, caps in rows:
        d.text((10, y + colw // 2), lab, fill=(0, 0, 0), font=font(18, True))
        for k, im in enumerate(ims):
            S.paste(im.resize((colw, colw)), (lab_w + k * colw, y))
            if caps and k < len(caps) and caps[k]: d.text((lab_w + 6 + k * colw, y + colw + 4), caps[k], fill=(30, 30, 30), font=font(14))
        y += colw + 34
    if note: d.text((14, y + 6), note, fill=(60, 60, 60), font=font(15))
    S.save(os.path.join(OUT, fname), quality=90)
def zr(ver, c, g):
    if not ZR: return ''
    q = ZR[ver][HEADS[c]]['groups'].get(g) if g != 'total' else ZR[ver][HEADS[c]]['total']
    return '' if not q else 'T-4 %d / %d faces' % (q['angle_viol'], q['faces'])
VC = ['v001 E2', 'v002 E2']
for c, h in HEADS.items():
    G = lambda nm, sfx='_g': [img('%s_%s%s' % (c, v, sfx), nm) for v in VER]
    tot = [zr(v, c, 'total') for v in VER]
    for k, (nm, vn) in enumerate([('full head front', 'front'), ('profile', 'prof'), ('3-4 front', 'tqf'), ('3-4 rear', 'tqr'), ('rear', 'rear'), ('top', 'top')], start=1):
        sheet('FENN_EAR_V2_%02d_%s_%s.jpg' % (k, nm.replace(' ', '_').replace('-', ''), c), 'Fenn ear %s — %s: v001 E2 | v002 E2 (%s CF2 head; identical orthographic camera, true scale)' % (c, nm, h),
              [(c, G(vn), [a + '  ' + b for a, b in zip(VC, tot)])])
    sheet('FENN_EAR_V2_07_wireframe_%s.jpg' % c, 'Fenn ear %s — wireframe: v001 E2 | v002 E2 (front orange, back violet, rim yellow, cuff blue, transition green)' % c,
          [('front', G('face', '_w'), VC), ('rear', G('crear', '_w'), VC)])
    sheet('FENN_EAR_V2_08_upper_extension_%s.jpg' % c, 'Fenn ear %s — upper-extension close-up: v001 kite | v002 tapered leaf (wire; red = T-4 angle violation)' % c,
          [('wire', G('upper', '_w'), VC), ('T-4', G('upper', '_t4'), [a + '  upper ext. ' + zr(v, c, 'upper_extension') for a, v in zip(VC, VER)])])
    sheet('FENN_EAR_V2_09_cuff_transitions_%s.jpg' % c, 'Fenn ear %s — cuff count transitions: v001 | v002 (magenta = cuff faces at a cuff pole; wire)' % c,
          [('side', G('root', '_tr'), [a + '  cuff ' + zr(v, c, 'cuff') for a, v in zip(VC, VER)]), ('below', G('under', '_tr'), VC)])
    sheet('FENN_EAR_V2_10_attachment_corners_%s.jpg' % c, 'Fenn ear %s — attachment corners c0 (lower) and c1 (upper): v001 | v002 (wire)' % c,
          [('c0', G('c0', '_w'), VC), ('c1', G('c1', '_w'), VC)])
    sheet('FENN_EAR_V2_11_lobe_cusp_%s.jpg' % c, 'Fenn ear %s — lobe-cusp region: v001 | v002 (grey low rear view and lobe close-up; wire close-up)' % c,
          [('low rear', G('low'), VC), ('lobe', G('lobe'), VC), ('wire', G('lobe', '_w'), VC)])
    sheet('FENN_EAR_V2_12_T4_%s.jpg' % c, 'Fenn ear %s — T-4 angle heat before / after (red = a corner outside 45-135°; branch faces light)' % c,
          [('front', G('face', '_t4'), tot), ('rear', G('crear', '_t4'), VC), ('root', G('root', '_t4'), VC)])
    sheet('FENN_EAR_V2_13_aspect_%s.jpg' % c, 'Fenn ear %s — quad aspect heat before / after (blue 1 .. red 6; violet > 6)' % c,
          [('front', G('face', '_as'), ['%s aspect max %.2f' % (a, AU[(v, c)]['T4']['aspect_max']) for a, v in zip(VC, VER)]), ('rear', G('crear', '_as'), VC), ('root', G('root', '_as'), VC)])
    sheet('FENN_EAR_V2_14_poles_%s.jpg' % c, 'Fenn ear %s — pole / valence before / after (blue valence 3, red 5, violet 6+; branch only)' % c,
          [('front', G('face', '_v'), ['%s branch poles %d' % (a, AU[(v, c)]['poles_branch_total']) for a, v in zip(VC, VER)]), ('rear', G('crear', '_v'), VC), ('root', G('root', '_v'), VC)])
    sheet('FENN_EAR_V2_15_root_integration_%s.jpg' % c, 'Fenn ear %s — root integration before / after (cuff skin vs the hidden-ear CF2 skull, 0 .. 0.6 cm; wire root close-up)' % c,
          [('deviation', G('root', '_rd'), ['%s root dihedral max %.0f° (v005 %.0f°)' % (a, AU[(v, c)]['root_dihedral']['l']['max_deg'], AU[(v, c)]['root_dihedral']['l']['v005_max_deg']) for a, v in zip(VC, VER)]),
           ('below', G('under', '_rd'), VC), ('wire', G('root', '_w'), VC)])
    sheet('FENN_EAR_V2_16_thickness_%s.jpg' % c, 'Fenn ear %s — thickness (front-back distance, 0.15 .. 0.6 cm) before / after' % c,
          [('front', G('face', '_th'), VC), ('rear', G('crear', '_th'), VC)])
    P = lambda v: [img('pose_%s_%s_%s' % (c, v, pn), 'tq') for pn in ('neck_flex30', 'neck_ext30', 'head_yaw_l45', 'head_roll_l20')]
    sheet('FENN_EAR_V2_17_deformation_%s.jpg' % c, 'Fenn ear %s — static deformation readiness (neck flex 30 | neck ext 30 | head yaw 45 | head roll 20); v001 row / v002 row' % c,
          [('v001', P('v001'), ['neck flex 30', 'neck ext 30', 'yaw L 45', 'roll L 20']), ('v002', P('v002'), None)], colw=520)
for c in HEADS:
    pass
sheet('FENN_EAR_V2_18_shape_probes_c1.jpg', 'Fenn ear c1 — shape-readiness probes on the shared topology (v001 row / v002 row; same camera)',
      [('v001', [img('pr_v001_%s' % p, 'face') for p in PROBES[:5]], PROBES[:5]), ('v002', [img('pr_v002_%s' % p, 'face') for p in PROBES[:5]], None),
       ('v001', [img('pr_v001_%s' % p, 'face') for p in PROBES[5:]], PROBES[5:]), ('v002', [img('pr_v002_%s' % p, 'face') for p in PROBES[5:]], None)], colw=420)
sheet('FENN_EAR_V2_19_c1_vs_c2_E2.jpg', 'Fenn ear v002 E2 — configuration 1 | configuration 2 (shared topology; each on its accepted CF2 head)',
      [('3-4 front', [img('c1_v002_g', 'tqf'), img('c2_v002_g', 'tqf')], ['c1 FNL4-CF2', 'c2 FNF181-CF2']), ('close', [img('c1_v002_g', 'face'), img('c2_v002_g', 'face')], None),
       ('wire', [img('c1_v002_w', 'face'), img('c2_v002_w', 'face')], None)])
for c in HEADS:
    sheet('FENN_EAR_V2_20_hidden_ear_CF2_%s.jpg' % c, 'Fenn %s — hidden-ear CF2 confirmation (v005 ear zone collapsed; sources unchanged) | v002 E2 visible ear, same cameras' % c,
          [('hidden ear', [img('hid_' + c, n) for n in ('front', 'prof', 'tqf')], ['front', 'profile', '3-4 front']), ('v002 E2', [img('%s_v002_g' % c, n) for n in ('front', 'prof', 'tqf')], None)], colw=560)
print('sheets done')
