# overlay2.py LANDMARKS_v002.json V001.json OUTDIR : visual sheets for the adjudicated diagnostic landmark package
# (diagnostic skeleton lines, manual rig centres, proxies, construction joints, frozen markers; rejected / old alternatives greyed)
import sys, os, json, numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fitlib import T_PROD
D = json.load(open(sys.argv[1]))['joints']; V1 = json.load(open(sys.argv[2]))['joints']; OUT = sys.argv[3]; os.makedirs(OUT, exist_ok=True)
RD = ['/tmp/claude-0/rt/rd/r', '/tmp/claude-0/rt/rpr/r']
RIG = json.load(open(os.environ.get('RIGJSON', '/tmp/claude-0/rt/rd/rig/rig_v001.json')))
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
f = lambda n, b=False: ImageFont.truetype(FB if b else FONT, n)
COL = dict(manual=(214, 40, 30), proxy=(200, 0, 160), constr=(20, 140, 60), meas=(30, 90, 200), deferred=(140, 50, 170), control=(0, 0, 0), old=(120, 120, 120), bone=(255, 170, 0))
def kind(c):
    if c.startswith('manual-author-rig-proxy'): return 'proxy'
    if c.startswith('manual-author-rig'): return 'manual'
    if c.startswith('deferred'): return 'deferred'
    if c.startswith('rig control'): return 'control'
    if c.startswith('copied') or c.startswith('derived'): return 'constr'
    return 'meas'
SRC = lambda j: np.array(j['position_source_frame_cm'])
def load(view):
    for d in RD:
        p = os.path.join(d, view + '.png')
        if os.path.exists(p): return Image.open(p).convert('RGB'), json.load(open(p[:-4] + '.json'))
    raise FileNotFoundError(view)
def proj(cam, p):
    q = np.asarray(p) - np.array(cam['c']); s = cam['px'] / (2 * cam['h']); return cam['px'] / 2 + (q @ np.array(cam['x'])) * s, cam['px'] / 2 - (q @ np.array(cam['y'])) * s
def vis(cam, side):
    d = np.array(cam['d']); return not (abs(d[0]) > 0.9 and side in 'lr' and np.sign(d[0]) != (1 if side == 'l' else -1))
def draw(view, keys, old=None, label=lambda k: True, bones=True, scale=1.0):
    im, cam = load(view); dr = ImageDraw.Draw(im); fs = int(14 * scale)
    if bones:                                                           # the actual diagnostic-rig bones (rig_v001.json), deform bones only
        for b in RIG['bones']:
            if not b['deform']: continue
            h = np.array(b['head']); t = np.array(b['tail']); hs = np.array([h[0], -h[1], h[2]]) * 100 - T_PROD; ts = np.array([t[0], -t[1], t[2]]) * 100 - T_PROD
            hk = min(D, key=lambda k: np.linalg.norm(SRC(D[k]) - hs))
            if not keys(hk) or not vis(cam, D[hk]['side']): continue
            dr.line([proj(cam, hs), proj(cam, ts)], fill=COL['bone'], width=max(2, int(3 * scale)))
    for k, (p, lab) in (old or {}).items():
        u, v = proj(cam, p); dr.line([(u - 6, v - 6), (u + 6, v + 6)], fill=COL['old'], width=2); dr.line([(u - 6, v + 6), (u + 6, v - 6)], fill=COL['old'], width=2)
        dr.text((u + 7, v - 16), lab, fill=COL['old'], font=f(fs - 2))
    for k, j in D.items():
        if not keys(k) or not vis(cam, j['side']): continue
        u, v = proj(cam, SRC(j)); kd = kind(j['provenance_class']); r = 6 * scale; c = COL[kd]
        if kd == 'manual': dr.polygon([(u, v - r - 2), (u + r + 2, v), (u, v + r + 2), (u - r - 2, v)], fill=c, outline=(0, 0, 0))
        elif kd == 'proxy': dr.polygon([(u - r, v - r), (u + r, v - r), (u, v + r + 2)], fill=c, outline=(0, 0, 0))
        elif kd == 'constr': dr.rectangle([u - r + 1, v - r + 1, u + r - 1, v + r - 1], fill=c, outline=(0, 0, 0))
        elif kd == 'deferred': dr.polygon([(u, v - r), (u + r, v + r), (u - r, v + r)], outline=c, width=2)
        elif kd == 'control': dr.rectangle([u - r, v - r, u + r, v + r], outline=c, width=3)
        else: dr.ellipse([u - r, v - r, u + r, v + r], fill=c, outline=(0, 0, 0))
        if label(k): dr.text((u + 8, v + 2), k, fill=(0, 0, 0), font=f(fs))
    return im
def legend(w):
    im = Image.new('RGB', (w, 34), (255, 255, 255)); dr = ImageDraw.Draw(im); x = 10
    for kd, t in (('manual', 'manual-author-rig centre'), ('proxy', 'manual-author-rig-proxy'), ('constr', 'copied construction joint'), ('meas', 'frozen surface marker'),
                  ('deferred', 'deferred facial placeholder'), ('old', 'rejected / old alternative (frozen E3, v001 sphere, inguinal A)'), ('bone', 'diagnostic chain')):
        dr.rectangle([x, 10, x + 14, 24], fill=COL[kd]); dr.text((x + 19, 8), t, fill=(0, 0, 0), font=f(13)); x += 34 + int(dr.textlength(t, font=f(13)))
    return im
def sheet(name, title, panels, ncol, caption, cell=650):
    rows = (len(panels) + ncol - 1) // ncol; W = ncol * cell; lg = legend(W); cap = [caption[i:i + int(W / 7.4)] for i in range(0, len(caption), int(W / 7.4))]
    S = Image.new('RGB', (W, 46 + rows * (cell + 26) + lg.height + 18 * len(cap) + 10), (255, 255, 255)); dr = ImageDraw.Draw(S); dr.text((10, 10), title, fill=(0, 0, 0), font=f(20, True))
    for i, (im, lab) in enumerate(panels):
        r, c = divmod(i, ncol); x0, y0 = c * cell, 46 + r * (cell + 26); S.paste(im.resize((cell, cell), Image.LANCZOS), (x0, y0 + 24)); dr.text((x0 + 6, y0 + 4), lab, fill=(0, 0, 0), font=f(14, True))
    y = 46 + rows * (cell + 26); S.paste(lg, (0, y)); y += lg.height
    for l in cap: dr.text((10, y), l, fill=(40, 40, 40), font=f(13)); y += 18
    S.save(os.path.join(OUT, name + '.jpg'), quality=88); return name
FZ = json.load(open('/home/claude/wayfarer-design/reviews/rac-rp2-evidence/grask_retopo_v003_audit_closure/production/GR_U_REF_RP2_retopo_v003_landmarks.json'))['landmarks']
old = {}
for s in 'lr':
    old['ghC_' + s] = (np.array(FZ['glenohumeral_' + s]['source_frame_cm']), 'old GH (E3)')
    for an, ap in V1['glenohumeral_' + s]['alternatives_production_cm'].items():
        if an.startswith(('A', 'B')): old['gh%s_%s' % (an[0], s)] = (np.array(ap) - T_PROD, 'v001 sphere ' + an[0])
    old['scC_' + s] = (np.array(FZ['sternoclavicular_' + s]['source_frame_cm']), 'old SC (E3)')
    old['hipC_' + s] = (np.array(FZ['hip_' + s]['source_frame_cm']), 'old hip (E3)')
    old['hipA_' + s] = (np.array(V1['hip_' + s]['alternatives_production_cm'][[k for k in V1['hip_' + s]['alternatives_production_cm'] if k.startswith('A')][0]]) - T_PROD, 'inguinal A')
old['pelC'] = (np.array(FZ['pelvis_root']['source_frame_cm']), 'frozen pelvis_root')
GIR = lambda k: k.startswith(('acromion', 'scapula', 'glenohumeral', 'sternoclavicular', 'thoracic_03', 'elbow', 'neck_base'))
made = []
made.append(sheet('V1_shoulder_scapular', 'Grask diagnostic landmarks v002 — shoulder girdle: acromion, scapular inferior proxy, scapula medial proxy, SC and GH',
    [(draw(v, GIR, {k: o for k, o in old.items() if k.startswith(('gh', 'sc'))}), v) for v in ('v003w_shB_l', 'v003w_shB_r', 'v003w_shF_l', 'v003w_shF_r', 'v005_shS_l', 'v005_shS_r')], 3,
    'GH = acromion anchor, free upper-arm shaft line extrapolated, 4.0 cm below the acromion (AD-R3); SC = jugular/clavicular skin summit + 3.0 cm posterior (AD-R5); '
    'scapula_medial_proxy = 60% inferior-proxy->acromion level, 45% midline->acromion x, projected to the posterior surface (AD-R9). Grey = rejected v001 sphere fits / old frozen E3 points. '
    'v003 in the v005 frame, no display offset; markers projected (internal centres lie inside).'))
AX = lambda k: k.startswith(('pelvis', 'spine', 'thoracic', 'neck', 'head_pivot', 'crown', 'root', 'sternoclavicular', 'hip'))
made.append(sheet('V2_thoracic_chain', 'Grask diagnostic landmarks v002 — axial chain root -> pelvis -> spine_01-03 -> thoracic_01-03 -> neck_base -> head_pivot',
    [(draw(v, AX, {k: o for k, o in old.items() if k.startswith('pel')}), v) for v in ('v003w_torF', 'v003w_torS', 'v003w_torB', 'v005_torS')], 4,
    'thoracic_01/02/03 at 25/50/75% of spine_03 -> neck_base (AD-R6), torso-section centroid clipped to the trunk half-width (19.98 cm) so the arms do not bias it; spine_01-03 and neck_base are the frozen records unchanged. '
    'root (black square, at the ground) = production origin; pelvis = v001 proposal + 5 mm toward the section centroid (AD-R7). Rig-prep controls, not vertebrae.', cell=600))
LEG = lambda k: k.startswith(('pelvis', 'hip', 'knee', 'ankle', 'root', 'spine_01'))
made.append(sheet('V3_pelvis_hip_root', 'Grask diagnostic landmarks v002 — pelvis / hip / root',
    [(draw(v, LEG, {k: o for k, o in old.items() if k.startswith(('hip', 'pel'))}), v) for v in ('v005_hipF', 'v005na_hipS_l', 'v005na_hipS_r')], 3,
    'Hip = v001 consensus moved 5 mm toward the proximal-thigh load axis (AD-R1); grey = old frozen E3 hips (2.9-3.1 cm under the gluteal skin) and the inguinal-axis alternative A. Side views with the hanging arm removed.'))
ALL = lambda k: not k.startswith(('index', 'middle', 'ring', 'pinky', 'hallux', 'toe', 'mouth', 'ear_tip')) and not k.startswith('thumb_') or k.startswith('thumb_cmc')
made.append(sheet('V0_body_diagnostic_skeleton', 'Grask diagnostic landmarks v002 — whole-body diagnostic skeleton (v003 clay + wire)',
    [(draw(v, ALL, None, label=lambda k: not k.startswith(('eye', 'jaw', 'chin', 'crown', 'acromion', 'scapular', 'ear', 'ball', 'thumb'))), v) for v in ('v003w_body_front', 'v003w_body_left', 'v003w_body_back')], 3,
    'Diagnostic chain only (not a final skeleton / UE5 orientation policy). Eyes are non-deforming aim joints; jaw hinges are deferred placeholders (not in the rig).', cell=800))
for s, nm in (('l', 'left'), ('r', 'right')):
    HD = lambda k, s=s: k.endswith('_' + s) and k.startswith(('wrist', 'index', 'middle', 'ring', 'pinky', 'thumb'))
    made.append(sheet('V4_hand_%s' % s, 'Grask diagnostic landmarks v002 — %s hand chains (construction joints, unchanged)' % nm,
        [(draw('v003w_hand_%s_%s' % (s, v), HD, None, label=lambda k: 'mcp' in k or 'cmc' in k or 'wrist' in k), v) for v in ('dors', 'palm', 'rad', 'uln')], 4, 'Hand bone wrist -> middle MCP; fingers MCP->PIP->DIP->tip; thumb CMC->MCP->IP->tip.', cell=600))
json.dump(made, open(os.path.join(OUT, 'landmark_sheets.json'), 'w')); print(len(made), 'landmark sheets')
