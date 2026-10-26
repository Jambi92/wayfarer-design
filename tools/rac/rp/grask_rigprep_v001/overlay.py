# overlay.py PROPOSAL.json RENDERDIR OUTDIR : annotate the identical-camera clay renders with the rig-prep proposal and build
# the review sheets. 2-D overlay only (markers are drawn at the projected 3-D position; internal centres lie inside the body).
import sys, os, json, numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fitlib import T_PROD
D = json.load(open(sys.argv[1])); RD, OUT = sys.argv[2], sys.argv[3]; os.makedirs(OUT, exist_ok=True)
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; FONTB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
f = lambda n, b=False: ImageFont.truetype(FONTB if b else FONT, n)
JS = D['joints']
SRC = lambda v: np.array(v, float) - T_PROD                     # production cm -> source frame (renders are in the source frame)
COL = dict(new=(214, 66, 30), alt=(235, 140, 40), frozen=(90, 90, 90), constr=(20, 140, 60), meas=(30, 90, 200), rule=(140, 50, 170),
           X=(220, 30, 30), Y=(20, 150, 40), Z=(30, 70, 220))
def kind(j):
    c = j['provenance_class']
    if c.startswith('fitted'): return 'new'
    if c.startswith('rule'): return 'rule'
    if c.startswith('independently'): return 'meas'
    return 'constr'
def proj(cam, p):
    q = np.asarray(p, float) - np.array(cam['c']); s = cam['px'] / (2 * cam['h'])
    return (cam['px'] / 2 + (q @ np.array(cam['x'])) * s, cam['px'] / 2 - (q @ np.array(cam['y'])) * s)
def visible(cam, j):
    d = np.array(cam['d']); side = j['side']
    if abs(d[0]) > 0.9 and side in 'lr' and np.sign(d[0]) != (1 if side == 'l' else -1): return False
    return True
def draw_view(png, cam, keys=None, label=True, axes=True, alts=True, axlen=6.0, lab_filter=None, scale=1.0, sidecull=True):
    im = Image.open(png).convert('RGB'); dr = ImageDraw.Draw(im); s = cam['px'] / (2 * cam['h']); fs = max(11, int(13 * scale))
    for k, j in JS.items():
        if keys is not None and not keys(k): continue
        if sidecull and not visible(cam, j): continue
        p = SRC(j['position_production_cm']); u, v = proj(cam, p)
        if not (-20 < u < cam['px'] + 20 and -20 < v < cam['px'] + 20): continue
        kd = kind(j); r = 5 * scale
        if kd == 'new':
            if alts:
                for an, ap in j['alternatives_production_cm'].items():
                    au, av = proj(cam, SRC(ap)); fz = an.startswith('C')
                    dr.line([(u, v), (au, av)], fill=(150, 150, 150), width=1)
                    if fz: dr.line([(au - 5, av - 5), (au + 5, av + 5)], fill=COL['frozen'], width=2); dr.line([(au - 5, av + 5), (au + 5, av - 5)], fill=COL['frozen'], width=2)
                    else: dr.ellipse([au - 4, av - 4, au + 4, av + 4], outline=COL['alt'], width=2)
                    if label and scale >= 1: dr.text((au + 5, av - 6), an[0], fill=COL['frozen'] if fz else COL['alt'], font=f(fs - 2))
            if j['uncertainty_cm']:
                R = j['uncertainty_cm'] * s; dr.ellipse([u - R, v - R, u + R, v + R], outline=COL['new'], width=1)
            dr.polygon([(u, v - r - 2), (u + r + 2, v), (u, v + r + 2), (u - r - 2, v)], fill=COL['new'], outline=(0, 0, 0))
        elif kd == 'constr': dr.rectangle([u - r + 1, v - r + 1, u + r - 1, v + r - 1], fill=COL['constr'], outline=(0, 0, 0))
        elif kd == 'meas': dr.ellipse([u - r, v - r, u + r, v + r], fill=COL['meas'], outline=(0, 0, 0))
        else: dr.polygon([(u, v - r - 1), (u + r + 1, v + r), (u - r - 1, v + r)], fill=COL['rule'], outline=(0, 0, 0))
        fr = j.get('frame')
        if axes and fr and 'blender_columns_XYZ' in fr:
            for i, cn in enumerate('XYZ'):
                vb = np.array(fr['blender_columns_XYZ'][i]); va = np.array([vb[0], -vb[1], vb[2]])
                eu, ev = proj(cam, p + va * axlen); dr.line([(u, v), (eu, ev)], fill=COL[cn], width=max(2, int(2 * scale)))
        if label and (lab_filter is None or lab_filter(k)):
            dr.text((u + 7, v + 3), k, fill=(0, 0, 0), font=f(fs))
    return im
def legend(w):
    im = Image.new('RGB', (w, 62), (255, 255, 255)); dr = ImageDraw.Draw(im); x = 10; y = 8
    items = [('new', 'NEW proposal: fitted centre (circle = uncertainty)'), ('alt', 'alternative A/B (surface definitions)'), ('frozen', 'frozen package value C (MPFB/E3-seeded)'),
             ('constr', 'copied construction joint (surface-validated)'), ('meas', 'measured surface landmark (frozen)'), ('rule', 'rule-based estimate (jaw)')]
    for kd, t in items:
        c = COL[kd]
        if kd == 'new': dr.polygon([(x + 6, y), (x + 12, y + 6), (x + 6, y + 12), (x, y + 6)], fill=c, outline=(0, 0, 0))
        elif kd == 'alt': dr.ellipse([x + 1, y + 1, x + 11, y + 11], outline=c, width=2)
        elif kd == 'frozen': dr.line([(x, y), (x + 12, y + 12)], fill=c, width=2); dr.line([(x, y + 12), (x + 12, y)], fill=c, width=2)
        elif kd == 'constr': dr.rectangle([x + 1, y + 1, x + 11, y + 11], fill=c, outline=(0, 0, 0))
        elif kd == 'meas': dr.ellipse([x, y, x + 12, y + 12], fill=c, outline=(0, 0, 0))
        else: dr.polygon([(x + 6, y), (x + 12, y + 12), (x, y + 12)], fill=c, outline=(0, 0, 0))
        dr.text((x + 17, y - 1), t, fill=(0, 0, 0), font=f(13)); x += 30 + int(dr.textlength(t, font=f(13)))
        if x > w - 330: x = 10; y += 22
    for i, (cn, t) in enumerate((('X', 'X flexion axis'), ('Y', 'Y toward child'), ('Z', 'Z = X × Y'))):
        dr.line([(x + i * 120, y + 6), (x + i * 120 + 20, y + 6)], fill=COL[cn], width=3); dr.text((x + i * 120 + 25, y - 1), t, fill=(0, 0, 0), font=f(13))
    return im
def sheet(name, title, panels, ncol, caption, cell=600):
    rows = (len(panels) + ncol - 1) // ncol; W = ncol * cell; leg = legend(W)
    capl = [caption[i:i + int(W / 7.4)] for i in range(0, len(caption), int(W / 7.4))] if caption else []
    H = 46 + rows * (cell + 26) + leg.height + 18 * len(capl) + 10
    S = Image.new('RGB', (W, H), (255, 255, 255)); dr = ImageDraw.Draw(S); dr.text((10, 10), title, fill=(0, 0, 0), font=f(20, True))
    for i, (im, lab) in enumerate(panels):
        r, c = divmod(i, ncol); im = im.resize((cell, cell), Image.LANCZOS); x0, y0 = c * cell, 46 + r * (cell + 26)
        S.paste(im, (x0, y0 + 24)); dr.text((x0 + 6, y0 + 4), lab, fill=(0, 0, 0), font=f(14, True)); dr.rectangle([x0, y0 + 24, x0 + cell - 1, y0 + 24 + cell - 1], outline=(200, 200, 200))
    y = 46 + rows * (cell + 26); S.paste(leg, (0, y)); y += leg.height
    for l in capl: dr.text((10, y), l, fill=(40, 40, 40), font=f(13)); y += 18
    S.save(os.path.join(OUT, name + '.png'), optimize=True); S.convert('RGB').save(os.path.join(OUT, name + '.jpg'), quality=88); return name
def V(tag, view, **kw):
    png = os.path.join(RD, '%s_%s.png' % (tag, view)); cam = json.load(open(png[:-4] + '.json')); return draw_view(png, cam, **kw)
MAJOR = lambda k: not any(t in k for t in ('_pip_', '_dip_', '_tip_', '_ip_', '_mcp_', '_mtp_', 'mouth', 'ear_tip', 'chin', 'crown', 'eye', 'jaw', 'ear_root'))
BODYK = lambda k: MAJOR(k) or k.startswith(('ball', 'eye', 'jaw', 'crown', 'chin', 'ear_root', 'mouth')) or 'thumb_cmc' in k
OFFS = 'v003 is shown in the v005 source frame (production translation undone); no display offset. '
made = []
for tag, nm, wire in (('v005', 'v005 source (clay)', ''), ('v003w', 'v003 production (clay + wire)', 'w')):
    made.append(sheet('S%s1_body_%s' % ('a' if tag == 'v005' else 'b', tag), 'Grask RP2 rig-prep proposal v001 — whole body — %s' % nm,
        [(V(tag, v, keys=BODYK, label=True, lab_filter=MAJOR, axlen=8, scale=1.2), v) for v in ('front', 'left', 'back', 'q3')], 2,
        OFFS + 'Identical orthographic cameras for v005 and v003. Joint centres are projected; internal centres lie inside the body. Side view shows only the near (left) side. '
        'Uncertainty circles are the largest distance to any alternative (A, B, frozen C).', cell=1000))
CL = [('S2_girdle_shoulder', 'shoulder / girdle (GH, SC, acromion, scapular proxy)', ['shF_l', 'shS_l', 'shF_r', 'shS_r']),
      ('S3_pelvis_hip', 'pelvis / hip / spine base (side views: hanging arm removed)', ['hipF', 'na:hipS_l', 'na:hipS_r']),
      ('S4_elbow', 'elbows', ['elF_l', 'elS_l', 'elF_r', 'elS_r']), ('S5_knee', 'knees', ['knF_l', 'knS_l', 'knF_r', 'knS_r']),
      ('S6_wrist', 'wrists (construction frame origin)', ['wrF_l', 'wrS_l', 'wrF_r', 'wrS_r']), ('S7_ankle', 'ankles', ['anF_l', 'anS_l', 'anF_r', 'anS_r']),
      ('S10_head_neck_jaw', 'head / neck / jaw / eyes', ['hdF', 'hdS', 'hdQ', 'jwS', 'nkS'])]
CAP = {'S2_girdle_shoulder': 'GH alternatives: A = sphere on the lateral/superior cap, B = sphere on the lateral deltoid, C = frozen. The free upper arm meets the torso at the armpit (z ~154 cm), so no section-based shoulder centre exists. SC: A = skin summit beside the jugular notch, C = frozen (about 10 cm deeper).',
       'S3_pelvis_hip': 'Hip: A = soft-tissue thigh axis at the inguinal-fold level, C = frozen. No trochanteric relief exists in the source (lateral hip contour monotonic). Pelvis root: A = midpoint of hips, B = torso-section centroid, C = frozen (production origin unchanged).',
       'S4_elbow': 'Elbow: A = minimum-area section, B = cubital-fossa level, C = frozen (about 5 cm higher). X axis = bend axis of the reference-stance arm (upper-arm x forearm axes).',
       'S5_knee': 'Knee: A = minimum-area "knee waist", B = patellar flattening of the anterior contour, C = frozen. Proposed centre = coordinate median; the source has no condylar relief.',
       'S6_wrist': 'Wrist = v005 hand-construction frame origin (copied, surface-validated). Its frame is the construction hand frame (u distal, v radial, w dorsal).',
       'S7_ankle': 'Ankle: A = anterior ankle crease, B = Achilles concavity, C = frozen. No malleolar relief exists in the source, so axis obliquity is unsupported; X is mediolateral.',
       'S10_head_neck_jaw': 'Closed sculpted mouth (no oral cavity, no mandible) and no separate eyeballs (eyes are sculpted surface on the single body mesh). Jaw hinge = rule-based offset from the ear root (provisional). Head pivot and neck base are internal estimates.'}
for nm, t, vs in CL:
    for tag, lab in (('v005', 'v005 clay'), ('v003w', 'v003 clay + wire')):
        made.append(sheet('%s_%s' % (nm, tag), 'Grask RP2 rig-prep proposal v001 — %s — %s' % (t, lab),
                          [(V(tag + ('na' if v.startswith('na:') else ''), v.replace('na:', ''), keys=(lambda k: BODYK(k) and not k.startswith(('wrist', 'thumb'))) if v.startswith('na:') else ((lambda k: BODYK(k) and JS[k]['side'] != 'c') if nm in ('S4_elbow', 'S5_knee', 'S6_wrist', 'S7_ankle') else BODYK)), v.replace('na:', '') + (' (arm removed)' if v.startswith('na:') else '')) for v in vs], min(4, len(vs)) if len(vs) != 5 else 3, OFFS + CAP[nm], cell=600))
DIG = lambda k: k.startswith(('index', 'middle', 'ring', 'pinky', 'thumb', 'wrist'))
FT = lambda k: k.startswith(('hallux', 'toe2', 'toe3', 'toe4', 'toe5', 'ball', 'ankle'))
DIGLAB = lambda k: ('_mcp_' in k or 'cmc' in k or 'wrist' in k or ('thumb' in k))
for s in 'lr':
    for tag, lab in (('v005', 'v005 clay'), ('v003w', 'v003 clay + wire')):
        made.append(sheet('S8_hand_%s_%s' % (s, tag), 'Grask RP2 rig-prep proposal v001 — %s hand — %s (isolated hand crop)' % ({'l': 'left', 'r': 'right'}[s], lab),
            [(V('%s_hand_%s' % (tag, s), v, keys=lambda k, s=s: DIG(k) and k.endswith('_' + s), axlen=2.0, lab_filter=DIGLAB, sidecull=False), v) for v in ('dors', 'palm', 'rad', 'uln')], 4,
            OFFS + 'MCP / PIP / DIP / tip and thumb CMC / MCP / IP / tip are the exact v005 construction joints; every IP joint is within 0.15 cm of its digit-section centroid; MCP and CMC sit 1.5-2.2 cm inside the palm. Axes 2 cm.', cell=600))
        made.append(sheet('S9_foot_%s_%s' % (s, tag), 'Grask RP2 rig-prep proposal v001 — %s foot — %s (isolated foot crop)' % ({'l': 'left', 'r': 'right'}[s], lab),
            [(V('%s_foot_%s' % (tag, s), v, keys=lambda k, s=s: FT(k) and k.endswith('_' + s), axlen=2.0, lab_filter=lambda k: '_mtp_' in k or 'ball' in k or 'ankle' in k, sidecull=False), v) for v in ('top', 'med', 'lat')], 3,
            OFFS + 'MTP line (hallux->toe5 MTP) and toe joints are exact v004/v005 construction joints, surface-validated. The ankle proposal (provisional) is shown for the foot-segment parent.', cell=600))
json.dump(made, open(os.path.join(OUT, 'sheets.json'), 'w')); print(len(made), 'sheets')
