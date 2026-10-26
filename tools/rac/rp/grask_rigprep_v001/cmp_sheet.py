# cmp_sheet.py WORKDIR : identical-camera shoulder / pelvis closeups, v002 manual centres vs the rejected / old alternatives (same diagnostic
# weights, only the pivot moved), with the measured numbers under each panel
import sys, os, json, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
W = sys.argv[1]; T = os.path.dirname(os.path.abspath(__file__)); BP = os.environ.get('BP', '/home/claude/stc/bin/python3')
J = json.load(open(W + '/diag/judgement.json'))['placement_comparison']; R = json.load(open(W + '/diag/diag_results.json'))['results']
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FN = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; f = lambda n, b=False: ImageFont.truetype(FB if b else FN, n)
os.makedirs(W + '/cmp', exist_ok=True); os.makedirs(W + '/dsheets', exist_ok=True)
SETS = [('S_shoulder_l_abd90', 'D1_l_abd90', ['', '_alt_oldE3_gh_l', '_alt_v001sphereA_gh_l', '_alt_v001cons_gh_l'], 'v0:0,1,0:28,-4,178:20;v1:0,-1,0:28,-4,178:20'),
        ('S_shoulder_l_flex90', 'D1_l_flex90', ['', '_alt_oldE3_gh_l', '_alt_v001sphereA_gh_l', '_alt_v001cons_gh_l'], 'v0:1,0,0:22,4,172:20;v1:0,1,0:22,4,172:20'),
        ('S_shoulder_r_abd90', 'D1_r_abd90', ['', '_alt_oldE3_gh_r', '_alt_v001sphereA_gh_r', '_alt_v001cons_gh_r'], 'v0:0,1,0:-29,-4,178:20;v1:0,-1,0:-29,-4,178:20'),
        ('S_pelvis_l_flex90', 'D6_l_flex90', ['', '_alt_oldE3_hip_l', '_alt_inguinalA_hip_l'], 'v0:1,0,0:12,6,112:24;v1:0,1,0:12,6,112:24'),
        ('S_pelvis_r_flex90', 'D6_r_flex90', ['', '_alt_oldE3_hip_r', '_alt_inguinalA_hip_r'], 'v0:-1,0,0:-12,6,112:24;v1:0,1,0:-12,6,112:24')]
sys.path.insert(0, '/tmp/claude-0/rt'); from common import PARTS
FPL = np.load('/tmp/claude-0/rt/frz/v003_frz.npz')['FP']
def noarm(npz, s):
    """display crop only: drop that side's arm / hand / finger faces so the hip is unobstructed (disclosed on the sheet)"""
    z = np.load(npz); drop = np.array([PARTS[i].endswith('_' + s) and PARTS[i].startswith(('arm', 'hand', 'thumb', 'index', 'middle', 'ring', 'pinky')) for i in FPL])
    o = npz[:-4] + '_noarm.npz'; np.savez(o, V=z['V'], Q=z['Q'][~drop]); return o
def stats(pose, tag):
    if tag == '': r = R[pose]
    else: r = json.load(open(W + '/diag/diag_results%s.json' % tag))['results'][pose]
    i = r['intersections']; return 'int %d (nc %d) depth %.1f mm | flips %d | folds out %d | zone %+.1f%% | p95 %.0f%% | loop %.2f' % (i['total'], i['non_contact'], i['crease_depth_mm'], r['flips']['total'], r['folds']['outside'], r['volume']['zone_pct'], r['strain']['zone_p95_pct'], r['loop_spacing_min_ratio'] or 0)
for name, pose, tags, vs in SETS:
    cell = 480; S = Image.new('RGB', (2 * cell + 10, 40 + len(tags) * (cell + 54)), (255, 255, 255)); dr = ImageDraw.Draw(S)
    dr.text((10, 10), 'Placement comparison — %s (same diagnostic weights; only the joint pivot differs; identical cameras%s)' % (pose, '; display crop: that side arm/hand hidden' if 'pelvis' in name else ''), fill=(0, 0, 0), font=f(16, True))
    for ri, tg in enumerate(tags):
        npz = W + '/diag/posed/%s%s.npz' % (pose, tg); out = '%s%s' % (name, tg)
        if 'pelvis' in name: npz = noarm(npz, name.split('_')[2])
        if not os.path.exists(W + '/cmp/%s_v0.png' % out):
            subprocess.run([BP, T + '/render.py', '--', npz, W + '/cmp', out, vs, '1', '700'], env=dict(os.environ, WIRE_T='0.0005'), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        y = 40 + ri * (cell + 54)
        for ci in range(2): S.paste(Image.open(W + '/cmp/%s_v%d.png' % (out, ci)).convert('RGB').resize((cell, cell), Image.LANCZOS), (ci * (cell + 10), y + 44))
        lab = 'v002 manual-author-rig centre (adopted)' if tg == '' else tg.replace('_alt_', 'alternative: ')
        dr.text((6, y + 4), lab, fill=(180, 20, 20) if tg == '' else (60, 60, 60), font=f(14, True)); dr.text((6, y + 24), stats(pose, tg), fill=(0, 0, 0), font=f(13))
    S.save(W + '/dsheets/%s.jpg' % name, quality=85); print('cmp', name, flush=True)
