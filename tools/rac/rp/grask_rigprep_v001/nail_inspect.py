# nail_inspect.py WDIR TAG LANDMARKS.json OUTDIR : visual inspection of the WN nail selection on the frozen v003 rest mesh (order b303b9e §3).
# Per digit (both hands): dorsal / lateral / tip-on / palmar orthographic views with wireframe of the hand-only crop.
#   red = selected (bound 100 % to the distal bone), shade by |delta| (pale red = W0 already ~1.0, deep red = largest change);
#   amber = unselected vertices whose W0 distal-bone share > 0.5 (the distal domain the cap sits in); clay = rest.
import sys, os, json, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '/tmp/claude-0/rt')
from common import PARTS
WD, TAG, LMF, O = sys.argv[1:5]; T = os.path.dirname(os.path.abspath(__file__)); BP = os.environ.get('BP', '/home/claude/stc/bin/python3')
os.makedirs(O + '/r', exist_ok=True)
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FN = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; f = lambda n, b=False: ImageFont.truetype(FB if b else FN, n)
Z = np.load('/tmp/claude-0/rt/frz/v003_frz.npz'); V = Z['V']; Q = np.asarray(Z['Q']); FP = Z['FP']
LOG = json.load(open('%s/weights_%s_log.json' % (WD, TAG))); z0 = np.load('/tmp/claude-0/rt/rd/rig/weights_v001c.npz'); W0 = z0['W']; names = [str(n) for n in z0['names']]
LM = json.load(open(LMF))['joints']; Jc = lambda k: np.array(LM[k]['position_source_frame_cm']); FIT5 = json.load(open('/tmp/claude-0/rt/rpr/fit_v005.json'))
rows = []
for s in 'lr':
    hp = [i for i, n in enumerate(PARTS) if n.endswith('_' + s) and n.startswith(('hand', 'thumb', 'index', 'middle', 'ring', 'pinky'))]
    keep = np.isin(FP, hp); Qh = Q[keep]; mesh = O + '/r/hand_%s.npz' % s
    if not os.path.exists(mesh): np.savez(mesh, V=V, Q=Qh)
    for fg in ('index', 'middle', 'ring', 'pinky', 'thumb'):
        k = '%s_%s' % (fg, s); d = LOG['digits'][k]; ix = np.array(d['vertex_ids']); b = names.index(d['bone'])
        jd = '%s_dip_%s' % (fg, s) if fg != 'thumb' else 'thumb_ip_' + s; D, tp = Jc(jd), Jc('%s_tip_%s' % (fg, s)); dor = np.array(FIT5['cx_' + jd]['dorsal'])
        u = (tp - D) / np.linalg.norm(tp - D); dor = dor - (dor @ u) * u; dor /= np.linalg.norm(dor); lat = np.cross(u, dor)
        c = np.tile([0.80, 0.77, 0.73], (len(V), 1)); dom = W0[:, b] > 0.5; c[dom] = [0.98, 0.78, 0.35]
        dl = 1 - W0[ix, b]; t = np.clip(dl / 0.05, 0, 1)[:, None]; c[ix] = (1 - t) * np.array([1.0, 0.55, 0.55]) + t * np.array([0.75, 0.0, 0.0])
        cf = O + '/r/c_%s.npy' % k; np.save(cf, c.astype(np.float32))
        ctr = D + u * 0.6 * np.linalg.norm(tp - D); h = 1.25 * np.linalg.norm(tp - D) + 0.6
        vs = ';'.join('%s:%.4f,%.4f,%.4f:%.3f,%.3f,%.3f:%.2f' % (nm, *dv, *ctr, h) for nm, dv in (('dorsal', dor), ('lateral', lat), ('tip', u + 0.35 * dor), ('palmar', -dor)))
        if not os.path.exists(O + '/r/%s_palmar.png' % k):
            subprocess.run([BP, T + '/render_attr.py', '--', mesh, cf, O + '/r', k, vs, '1', '420'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        rows.append((k, d, dl))
cell = 300; S = Image.new('RGB', (4 * cell + 430, 80 + len(rows) * (cell + 6)), (255, 255, 255)); dr = ImageDraw.Draw(S)
dr.text((10, 8), '%s nail-binding selection (documented distal-cap set) on frozen v003 (rest): dorsal / lateral / tip-on / palmar, hand-only crop with wireframe' % TAG, fill=(0, 0, 0), font=f(17, True))
dr.text((10, 34), 'red = selected (deep red = largest W0->WN change, pale = W0 already ~1.0 on the distal bone); amber = unselected vertices with W0 distal share > 0.5; clay = rest', fill=(0, 0, 0), font=f(13))
for ri, (k, d, dl) in enumerate(rows):
    y = 64 + ri * (cell + 6)
    for ci, v in enumerate(('dorsal', 'lateral', 'tip', 'palmar')): S.paste(Image.open(O + '/r/%s_%s.png' % (k, v)).convert('RGB').resize((cell, cell), Image.LANCZOS), (ci * cell, y))
    X = 4 * cell + 10
    for j, l in enumerate([k + ' -> ' + d['bone'], 'selected %d verts (parts %s)' % (d['count'], d['parts_of_selected']), 'W0 distal share min %.3f mean %.3f' % (d['W0_share_on_distal_bone']['min'], d['W0_share_on_distal_bone']['mean']),
                           'max |delta| %.3f; verts with delta>0.01: %d' % (d['max_abs_delta'], int((dl > 0.01).sum())), 'bones touched: %s' % ', '.join(d['bones_touched']), 'first ids %s' % d['vertex_ids'][:8]]):
        dr.text((X, y + 8 + 20 * j), l, fill=(0, 0, 0) if j else (150, 20, 20), font=f(12, j == 0))
S.save(O + '/N_nail_selection_%s.jpg' % TAG, quality=86); print('sheet', O + '/N_nail_selection_%s.jpg' % TAG)
