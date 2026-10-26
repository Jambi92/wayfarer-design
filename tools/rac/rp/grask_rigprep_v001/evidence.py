# evidence.py WORKDIR : identical-camera clay + wire renders of every D-pose (and its reference / base pose) and the D1-D10 sheets
import sys, os, json, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from diag_lib import Rig, build_poses, bl_to_src
W = sys.argv[1]; T = os.path.dirname(os.path.abspath(__file__)); BP = os.environ.get('BP', '/home/claude/stc/bin/python3')
rig = Rig(W + '/rig/rig_v001.json', W + '/rig/weights_v001c.npz'); P = build_poses(rig)
RES = json.load(open(W + '/diag/diag_results.json'))['results']
DQ = json.load(open(W + '/diag/diag_results_dqs.json'))['results'] if os.path.exists(W + '/diag/diag_results_dqs.json') else {}
os.makedirs(W + '/ev', exist_ok=True); os.makedirs(W + '/dsheets', exist_ok=True)
Z = np.load('/tmp/claude-0/rt/frz/v003_frz.npz'); np.savez(W + '/ev/rest.npz', V=Z['V'], Q=Z['Q'])
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FN = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
f = lambda n, b=False: ImageFont.truetype(FB if b else FN, n)
def bone_head_posed(pose, bone):
    M, _ = rig.pose_mats(pose); return bl_to_src(M[bone][:3, 3][None])[0]
GROUP = {   # test -> (pose names, reference pose name or 'rest', focus bone, half-size cm, view dirs)
 'D1_l': (['D1_l_abd45', 'D1_l_abd90', 'D1_l_abd90_girdle', 'D1_l_flex90', 'D1_l_flex90_girdle', 'D1_l_ext30'], 'rest', 'upperarm_l', 30, ['0,1,0', '0,-1,0', '1,0.4,0.2']),
 'D1_r': (['D1_r_abd45', 'D1_r_abd90', 'D1_r_abd90_girdle', 'D1_r_flex90', 'D1_r_flex90_girdle', 'D1_r_ext30'], 'rest', 'upperarm_r', 30, ['0,1,0', '0,-1,0', '-1,0.4,0.2']),
 'D2': (['D2_l_flex90', 'D2_l_flex130'], 'D2_l_base_abd45', 'forearm_l', 22, ['0,1,0', '1,0,0', '0,0.3,-1']),
 'D3': (['D3_l_flex60', 'D3_l_ext60', 'D3_l_radial20', 'D3_l_ulnar20'], 'D2_l_base_abd45', 'hand_l', 14, ['0,1,0', '1,0,0', '0,-1,0']),
 'D4': (['D4_l_fist', 'D4_l_spread_p10', 'D4_l_spread_m10'], 'D2_l_base_abd45', 'middle_p1_l', 12, ['0,1,0', '1,0,0', '0,-1,0']),
 'D5': (['D5_l_oppose_pinky', 'D5_l_oppose_pinch'], 'D2_l_base_abd45', 'thumb_mc_l', 11, ['0,1,0', '1,0,0', '0,-1,0']),
 'D6_l': (['D6_l_flex45', 'D6_l_flex90', 'D6_l_abd30'], 'rest', 'thigh_l', 34, ['1,0,0', '0,1,0', '0,-1,0']),
 'D6_r': (['D6_r_flex45', 'D6_r_flex90', 'D6_r_abd30'], 'rest', 'thigh_r', 34, ['-1,0,0', '0,1,0', '0,-1,0']),
 'D7': (['D7_l_flex90', 'D7_l_flex140'], 'rest', 'shin_l', 26, ['1,0,0', '0,1,0', '0,-1,0']),
 'D8': (['D8_l_dorsi20', 'D8_l_plantar40', 'D8_l_toes_ext30', 'D8_l_toes_flex30'], 'rest', 'foot_l', 16, ['1,0,0', '-1,0,0', '0,0,1']),
 'D9': (['D9_twist_p30', 'D9_twist_m30', 'D9_flex30'], 'rest', 'thoracic_01', 48, ['0,1,0', '1,0,0', '0,0,1']),
 'D10': (['D10_flex30', 'D10_ext30', 'D10_rot_p45', 'D10_rot_m45'], 'rest', 'neck', 20, ['1,0,0', '0,1,0', '0,0,1']),
}
def render(npz, tag, vs):
    env = dict(os.environ, WIRE_T='0.0005')
    subprocess.run([BP, T + '/render.py', '--', npz, W + '/ev', tag, vs, '1', '700'], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
def summary(r):
    i = r['intersections']; return ['int %d (non-contact %d, crease %d / %.1f mm, contact %d)' % (i['total'], i['non_contact'], i['crease'], i['crease_depth_mm'], i['contact']),
        'folds +%d (outside %d)  flips %d' % (r['folds']['new'], r['folds']['outside'], r['flips']['total']),
        'zone vol %s  strain p95 %.0f%%  loop min %s' % ('n/a' if r['volume']['zone_pct'] is None else '%+.1f%%' % r['volume']['zone_pct'], r['strain']['zone_p95_pct'], 'n/a' if r['loop_spacing_min_ratio'] is None else '%.2f' % r['loop_spacing_min_ratio'])]
made = []
for g, (poses, ref, bone, h, dirs) in GROUP.items():
    focus = np.mean([bone_head_posed(P[p], bone) for p in poses] + [bone_head_posed(P.get(ref, {}), bone)], 0)
    c = ','.join('%.2f' % x for x in focus); vs = ';'.join('v%d:%s:%s:%d' % (i, d, c, h) for i, d in enumerate(dirs))
    rows = [('ref' if ref != 'rest' else 'rest', W + '/ev/rest.npz' if ref == 'rest' else W + '/diag/posed/%s.npz' % ref, None)] + [(p, W + '/diag/posed/%s.npz' % p, RES.get(p)) for p in poses]
    if g.startswith('D6'):                                                  # display crop: hide that side's arm/hand so the hip is unobstructed
        sys.path.insert(0, '/tmp/claude-0/rt'); from common import PARTS
        FPL = np.load('/tmp/claude-0/rt/frz/v003_frz.npz')['FP']; sd = g[-1]
        drop = np.array([PARTS[i].endswith('_' + sd) and PARTS[i].startswith(('arm', 'hand', 'thumb', 'index', 'middle', 'ring', 'pinky')) for i in FPL]); nr = []
        for nm, npz, r in rows:
            z = np.load(npz); o = W + '/ev/%s_%s_noarm.npz' % (g, nm); np.savez(o, V=z['V'], Q=z['Q'][~drop]); nr.append((nm, o, r))
        rows = nr
    for nm, npz, _ in rows:
        if not all(os.path.exists(W + '/ev/%s_%s_v%d.json' % (g, nm, i)) for i in range(len(dirs))): render(npz, '%s_%s' % (g, nm), vs)
    cell = 420; ncol = len(dirs); S = Image.new('RGB', (ncol * cell + 470, 50 + len(rows) * (cell + 8)), (255, 255, 255)); dr = ImageDraw.Draw(S)
    dr.text((10, 12), 'Grask diagnostic rig v001 — %s (v003 derived diagnostic copy; identical cameras per row set; LBS, diagnostic heat weights%s)' % (g, '; display crop: that side arm/hand hidden' if g.startswith('D6') else ''), fill=(0, 0, 0), font=f(18, True))
    for ri, (nm, _, r) in enumerate(rows):
        y = 50 + ri * (cell + 8)
        for ci in range(ncol): S.paste(Image.open(W + '/ev/%s_%s_v%d.png' % (g, nm, ci)).convert('RGB').resize((cell, cell), Image.LANCZOS), (ci * cell, y))
        x = ncol * cell + 10; dr.text((x, y + 6), nm if nm != 'ref' else 'reference: %s' % ref, fill=(0, 0, 0), font=f(15, True))
        if r:
            for k, l in enumerate(summary(r)): dr.text((x, y + 32 + 20 * k), l, fill=(30, 30, 30), font=f(13))
            if nm in DQ: dr.text((x, y + 100), 'DQS (preserve volume) same weights:', fill=(20, 90, 160), font=f(13, True)); [dr.text((x, y + 120 + 20 * k), l, fill=(20, 90, 160), font=f(13)) for k, l in enumerate(summary(DQ[nm]))]
    S.save(W + '/dsheets/%s.jpg' % g, quality=85); made.append(g); print('sheet', g, flush=True)
json.dump(made, open(W + '/dsheets/sheets.json', 'w'))
