# iso_sheets.py WORKDIR : failure-ID overlays (baseline W0 vs selected candidate W2, identical cameras) and weight before/after maps
import sys, os, json, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '/tmp/claude-0/rt')
from common import PARTS
W = sys.argv[1]; T = os.path.dirname(os.path.abspath(__file__)); BP = os.environ.get('BP', '/home/claude/stc/bin/python3')
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FN = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; f = lambda n, b=False: ImageFont.truetype(FB if b else FN, n)
Z = np.load('/tmp/claude-0/rt/frz/v003_frz.npz'); Q0 = np.asarray(Z['Q']); FPL = Z['FP']; V0 = Z['V']
os.makedirs(W + '/ov', exist_ok=True); os.makedirs(W + '/sheets', exist_ok=True)
CLAY = np.array([0.80, 0.77, 0.73]); COLS = {'non-contact intersection': (0.9, 0.05, 0.05), 'crease intersection': (1.0, 0.55, 0.0), 'contact intersection': (0.95, 0.9, 0.1),
                                            'fold (dihedral > 120 deg)': (0.55, 0.0, 0.75), 'orientation failure (vs skinned normal)': (0.95, 0.2, 0.75),
                                            'local inversion (vs neighbours)': (0.0, 0.75, 0.85), 'compressed loop (< 50 %)': (0.1, 0.25, 0.95)}
def colours(ids):
    c = np.tile(CLAY, (len(Q0), 1)); prs = ids['pairs']; pc = ids['pair_class']
    lv = ids['compressed_loop_vertices']
    if len(lv): m = np.isin(Q0, lv).any(1); c[m] = COLS['compressed loop (< 50 %)']
    for fl in ids['orientation_fail_faces']: c[fl] = COLS['orientation failure (vs skinned normal)']
    for fl in ids['inversion_faces']: c[fl] = COLS['local inversion (vs neighbours)']
    if len(ids['fold_faces']): c[ids['fold_faces'].ravel()] = COLS['fold (dihedral > 120 deg)']
    for code, nm in ((2, 'contact intersection'), (1, 'crease intersection'), (0, 'non-contact intersection')):
        if len(prs): c[prs[pc == code].ravel()] = COLS[nm]
    return c
def crop(side):
    return ~np.array([PARTS[i].endswith('_' + side) and PARTS[i].startswith(('arm', 'hand', 'thumb', 'index', 'middle', 'ring', 'pinky')) for i in FPL])
SETS = [('F_shoulder_l', ['D1_l_abd90', 'D1_l_flex90'], 'a:0,1,0:24,-2,172:22;b:0,-1,0:24,-2,172:22;c:1,0.3,0.4:24,-2,172:22', None),
        ('F_shoulder_r', ['D1_r_abd90', 'D1_r_flex90'], 'a:0,1,0:-24,-2,172:22;b:0,-1,0:-24,-2,172:22;c:-1,0.3,0.4:-24,-2,172:22', None),
        ('F_elbow', ['D2_l_flex90', 'D2_l_flex130'], 'a:0,1,0:40,0,150:20;b:1,0,0:40,0,150:20;c:0,0.3,-1:40,0,150:20', None),
        ('F_hip_groin_l', ['D6_l_flex90', 'D6_l_abd30'], 'a:1,0,0:12,6,112:24;b:0,1,0:12,6,112:24;c:0,0,-1:12,6,112:24', 'l'),
        ('F_hip_groin_r', ['D6_r_flex90', 'D6_r_abd30'], 'a:-1,0,0:-12,6,112:24;b:0,1,0:-12,6,112:24;c:0,0,-1:-12,6,112:24', 'r'),
        ('F_knee', ['D7_l_flex90', 'D7_l_flex140'], 'a:1,0,0:14,-6,72:22;b:-1,0,0:14,-6,72:22;c:0,1,0:14,-6,72:22', None),
        ('F_thumb_fist', ['D4_l_fist', 'D5_l_oppose_pinky', 'D5_l_oppose_pinch'], None, None)]
def focus(pose, bone):
    from diag_lib import Rig, build_poses, bl_to_src
    return None
for name, poses, vs, side in SETS:
    rows = []
    for p in poses:
        for tag in ('W0', 'W2'):
            npz = W + '/diag/posed/%s_full_%s.npz' % (p, tag); idf = W + '/diag/ids/%s_full_%s.npz' % (p, tag)
            if not os.path.exists(npz): continue
            ids = np.load(idf); col = colours(ids); Vp = np.load(npz)['V']
            if vs is None:                                              # hand sets: camera on the posed hand
                hv = np.isin(FPL, [i for i, n in enumerate(PARTS) if n.endswith('_l') and n.startswith(('hand', 'thumb', 'index', 'middle', 'ring', 'pinky'))])
                cc = Vp[np.unique(Q0[hv])].mean(0); vsx = 'a:0,1,0:%.2f,%.2f,%.2f:12;b:1,0,0:%.2f,%.2f,%.2f:12;c:0,-1,0:%.2f,%.2f,%.2f:12' % (*cc, *cc, *cc)
            else: vsx = vs
            keep = crop(side) if side else np.ones(len(Q0), bool)
            o = W + '/ov/%s_%s.npz' % (p, tag); np.savez(o, V=Vp, Q=Q0[keep]); np.save(o[:-4] + '_c.npy', col[keep])
            tg = '%s_%s' % (p, tag)
            if not os.path.exists(W + '/ov/%s_c.json' % tg):
                subprocess.run([BP, T + '/render_attr.py', '--', o, o[:-4] + '_c.npy', W + '/ov', tg, vsx, '0', '600'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            r = json.load(open(W + '/diag/diag_results_full_%s.json' % tag))['results'][p]
            rows.append((p, tag, tg, ids, r))
    cell = 380; S = Image.new('RGB', (3 * cell + 520, 70 + len(rows) * (cell + 8) + 60), (255, 255, 255)); dr = ImageDraw.Draw(S)
    dr.text((10, 10), 'Grask diagnostic follow-up — %s — failure IDs, baseline W0 vs selected candidate W2 (identical cameras per pose; v003 frozen topology%s)' % (name, '; that side arm/hand hidden' if side else ''), fill=(0, 0, 0), font=f(16, True))
    x = 10
    for nm, c in COLS.items():
        dr.rectangle([x, 40, x + 14, 54], fill=tuple(int(255 * v) for v in c)); dr.text((x + 18, 39), nm, fill=(0, 0, 0), font=f(12)); x += 30 + int(dr.textlength(nm, font=f(12)))
    for ri, (p, tag, tg, ids, r) in enumerate(rows):
        y = 70 + ri * (cell + 8)
        for ci, v in enumerate('abc'): S.paste(Image.open(W + '/ov/%s_%s.png' % (tg, v)).convert('RGB').resize((cell, cell), Image.LANCZOS), (ci * cell, y))
        X = 3 * cell + 10; i = r['intersections']
        L = ['%s — %s' % (p, 'baseline W0 (heat)' if tag == 'W0' else 'candidate W2'),
             'intersections %d: non-contact %d, crease %d (%.1f mm), contact %d' % (i['total'], i['non_contact'], i['crease'], i['crease_depth_mm'], i['contact']),
             'folds +%d (outside %d) | orientation failures %d | local inversions %d' % (r['folds']['new'], r['folds']['outside'], r['flips']['total'], r['inversions']['total']),
             'zone cone-volume proxy %+.1f%% | p95 strain %.0f%% | loop min %s' % (r['volume']['zone_pct'], r['strain']['zone_p95_pct'], 'n/a' if r['loop_spacing_min_ratio'] is None else '%.2f' % r['loop_spacing_min_ratio']),
             'IDs: non-contact pairs %s' % (ids['pairs'][ids['pair_class'] == 0][:3].tolist() if len(ids['pairs']) else []),
             '     inversion faces %s' % ids['inversion_faces'][:6].tolist(), '     fold face pairs %s' % ids['fold_faces'][:3].tolist(),
             '     compressed-loop verts %s' % ids['compressed_loop_vertices'][:6].tolist()]
        for k, l in enumerate(L): dr.text((X, y + 6 + 22 * k), l, fill=(0, 0, 0) if k else (150, 20, 20), font=f(13, k == 0))
    S.save(W + '/sheets/%s.jpg' % name, quality=85); print('sheet', name, flush=True)
# -------------------- weight maps (rest pose; W0 heat vs W2), per-vertex weight of the child bone
z0 = np.load('/tmp/claude-0/rt/rd/rig/weights_v001c.npz'); z2 = np.load(W + '/w/weights_W2.npz'); names = [str(n) for n in z0['names']]
def ramp(w): w = np.clip(w, 0, 1)[:, None]; return (1 - w) * np.array([0.15, 0.25, 0.85]) + w * np.array([0.95, 0.15, 0.1])
WM = [('upperarm_l', 'a:0,1,0:22,-6,168:16;b:0,-1,0:22,-6,168:16'), ('forearm_l', 'a:1,0,0:26,-6,143:11;b:0,1,0:26,-6,143:11'), ('hand_l', 'a:1,0,0:31,2,106:8;b:0,1,0:31,2,106:8'),
      ('thigh_l', 'a:1,0,0:12,0,118:18;b:0,1,0:12,0,118:18'), ('shin_l', 'a:1,0,0:14,-3,71:12;b:0,1,0:14,-3,71:12'), ('thumb_p1_l', 'a:0,1,0:28,8,98:7;b:1,0,0:28,8,98:7'),
      ('index_p3_l', 'a:1,0,0:27,12,82:5;b:0,1,0:27,12,82:5')]
cell = 330; S = Image.new('RGB', (4 * cell + 20, 60 + len(WM) * (cell + 30)), (255, 255, 255)); dr = ImageDraw.Draw(S)
dr.text((10, 10), 'Diagnostic weight maps, rest pose: baseline W0 (bone heat + midline cleanup) vs candidate W2 (local smooth transitions, leakage removal, nail binding). Blue 0 -> red 1.', fill=(0, 0, 0), font=f(15, True))
for ri, (b, vs) in enumerate(WM):
    y = 50 + ri * (cell + 30); dr.text((6, y), b, fill=(0, 0, 0), font=f(14, True))
    for ci, (tag, z) in enumerate((('W0', z0), ('W2', z2))):
        c = ramp(z['W'][:, names.index(b)]); o = W + '/ov/wm_%s_%s' % (b, tag); np.save(o + '.npy', c)
        if not os.path.exists(o + '_b.json'):
            subprocess.run([BP, T + '/render_attr.py', '--', '/tmp/claude-0/rt/frz/v003_frz.npz', o + '.npy', W + '/ov', 'wm_%s_%s' % (b, tag), vs, '0', '500'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        for vi, v in enumerate('ab'):
            S.paste(Image.open(o + '_%s.png' % v).convert('RGB').resize((cell, cell), Image.LANCZOS), (10 + (ci * 2 + vi) * cell, y + 22))
        dr.text((10 + ci * 2 * cell + 4, y + 26), tag, fill=(255, 255, 255), font=f(14, True))
S.save(W + '/sheets/W_weight_maps.jpg', quality=85); print('weight maps done')
