# RAC RM-OT-05A visual package (order §7 / §8): matched orthographic camera, ground, stature, R-6 stance, reference composition, one grey
# material, no lighting change. Per height 208 / 218 / 229: front / profile / front 3/4 / rear 3/4 in neutral grey (head on), body only
# (head and neck removed by skin weight) and pure black silhouette (body only). Comparators: Marchfolk 203 (208 sheet endpoint), Skarn at
# matched height, the W2 Grask / Gorrund references as provenance, the RM-OT-05A candidates. Close architectural views at matched 229 cm
# (and Grask at 218): each tile centred on that body's own joint, same cm-per-pixel for every tile of a sheet.
import os, sys, json, numpy as np
from PIL import Image, ImageDraw
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(D), 'rmot05_drivers'))
import ot05r_package as PK
S = PK.S; OUT = S + '/rmot05a/sheets'; os.makedirs(OUT, exist_ok=True); PK.SH = OUT; RV = '/home/claude/wayfarer-design/reviews'
B = {'MF203': (S + '/w2a/st/MFM203', 'MF 203 max'),
     'SK208': (RV + '/rac-w3d-evidence/geometry/SK208-C1R', 'SK 208'), 'SK218': (S + '/w2c/sk/SKM218', 'SK 218'), 'SK229': (S + '/w3d/b/SKM229-C1R', 'SK 229'),
     'GRW208': (S + '/w2c/b/GR208/GR208', 'GR 208 W2'), 'GRW218': (S + '/w2c/b/GR218R/GR218R', 'GR 218 W2'), 'GRW229': (S + '/w2c/b/GR229/GR229', 'GR 229 W2'),
     'GRA208': (S + '/w2c/b/GRA208/GRA208', 'GR 208 05A'), 'GRA218': (S + '/w2c/b/GRA218/GRA218', 'GR 218 05A'), 'GRA229': (S + '/w2c/b/GRA229/GRA229', 'GR 229 05A'),
     'GOW208': (S + '/w2d/b/GO208/GO208', 'GO 208 W2'), 'GOW218': (S + '/w2d/b/GO218/GO218', 'GO 218 W2'), 'GOW229': (S + '/w2d/b/GO229/GO229', 'GO 229 W2'),
     'GOA208': (S + '/w2d/b/GOA208/GOA208', 'GO 208 05A'), 'GOA218': (S + '/w2d/b/GOA218/GOA218', 'GO 218 05A'), 'GOA229': (S + '/w2d/b/GOA229/GOA229', 'GO 229 05A'),
     'GOAREF': (S + '/w2d/b/GOAREF/GOAREF', 'GO 230.9 05A')}
PK.BODIES.clear(); PK.BODIES.update(B)
PK.R = S + '/rmot05a/rend'; os.makedirs(PK.R, exist_ok=True)
SETS = {208: ['MF203', 'SK208', 'GRW208', 'GRA208', 'GOW208', 'GOA208'], 218: ['SK218', 'GRW218', 'GRA218', 'GOW218', 'GOA218'],
        229: ['SK229', 'GRW229', 'GRA229', 'GOW229', 'GOA229', 'GOAREF']}
VN = (('F', 'front'), ('P', 'profile'), ('Q', 'front 3/4'), ('RQ', 'rear 3/4'))
def main_sheets():
    for h, ids in SETS.items():
        for vn, vl in VN:
            PK.row_sheet('a_%d_%s_grey.jpg' % (h, vn), 'RM-OT-05A %d cm - %s - neutral grey' % (h, vl), 'MF Marchfolk, SK Skarn, GR Grask, GO Gorrund. W2 = accepted W2 body (provenance); 05A = RM-OT-05A rebuild candidate. Matched ortho camera / ground / stature / composition.', ids, vn)
            PK.row_sheet('a_%d_%s_body.jpg' % (h, vn), 'RM-OT-05A %d cm - %s - body only (head / neck removed)' % (h, vl), 'Head and neck skin removed (skin weight > 0.3): no face, ear, hair or texture information.', ids, vn, headless=True)
            if vn in ('F', 'P'):
                PK.row_sheet('a_%d_%s_sil.jpg' % (h, vn), 'RM-OT-05A %d cm - %s - pure silhouette, body only' % (h, vl), 'Black silhouette, head / neck removed.', ids, vn, sil=True, headless=True)
# close views: (name, region joint, yaw, elev, extent cm, x offset from the joint's own side)
CLOSE = [('shoulder_RQ', 'upperarm_l', 150, 8, 70, 'mid'), ('shoulder_F', 'upperarm_l', 0, 0, 70, 'mid'), ('pelvis_Q', 'thigh_l', 30, 4, 70, 'mid'),
         ('pelvis_P', 'thigh_l', 90, 0, 70, 'mid'), ('thorax_P', 'spine_02', 90, 0, 90, 'mid'), ('thorax_RQ', 'spine_02', 145, 6, 90, 'mid'),
         ('knee_F', 'calf_l', 0, 0, 40, 'joint'), ('knee_P', 'calf_l', 90, 0, 40, 'joint'), ('elbow_F', 'lowerarm_l', 0, 0, 45, 'joint'),
         ('elbow_P', 'lowerarm_l', 90, 0, 45, 'joint'), ('hand_P', 'hand_l', 90, 0, 40, 'joint'), ('foot_Q', 'foot_l', 30, 25, 40, 'joint'), ('ankle_F', 'foot_l', 0, 0, 34, 'joint')]
def close_render(bid):
    tag = bid + '_close'
    if all(os.path.exists('%s/%s_%s.png' % (PK.R, tag, c[0])) for c in CLOSE): return tag
    d = np.load(B[bid][0] + '_r6.npz', allow_pickle=True); V = d['V'].astype(float); F = d['F']; keep = d['keep'].astype(bool); J = json.loads(str(d['joints']))
    vs = []
    for nm, jn, yaw, el, ext, mode in CLOSE:
        p = np.array(J[jn][0]); cx = 0.0 if mode == 'mid' else p[0]; cf = p[1] if mode == 'joint' else 0.5 * (V[keep, 1].min() + V[keep, 1].max())
        vs.append('%s:%d:%d:%.2f:%.2f:%.2f:%.1f' % (nm, yaw, el, cx, cf, p[2], ext))
    PK.C.save_head_npz(PK.R + '/%s.npz' % tag, V, F, lambda Q: keep); PK.C.render(PK.R + '/%s.npz' % tag, PK.R + '/' + tag, ';'.join(vs), 700); os.remove(PK.R + '/%s.npz' % tag)
    return tag
def close_sheets(ids, h):
    tags = [close_render(b) for b in ids]
    for nm, jn, yaw, el, ext, mode in CLOSE:
        tiles = [Image.open('%s/%s_%s.png' % (PK.R, t, nm)).convert('RGBA').resize((420, 420), Image.LANCZOS) for t in tags]
        W = 420 * len(tiles) + 20; img = Image.new('RGB', (W, 420 + 110), 'white'); d = ImageDraw.Draw(img)
        d.text((10, 8), 'RM-OT-05A close architecture - %s - matched %d cm (each tile %d cm wide, centred on that body\'s own joint)' % (nm.replace('_', ' '), h, ext), font=PK.SS.font(18), fill='black')
        for i, (b, t) in enumerate(zip(ids, tiles)):
            bg = Image.new('RGBA', t.size, (236, 236, 236, 255)); bg.alpha_composite(t); img.paste(bg.convert('RGB'), (10 + 420 * i, 44)); d.text((14 + 420 * i, 470), B[b][1], font=PK.SS.font(15), fill='black')
        img.save(OUT + '/c_%d_%s.jpg' % (h, nm), quality=86); print('c', h, nm, flush=True)
if __name__ == '__main__':
    what = sys.argv[1:] or ['main', 'close']
    if 'main' in what: main_sheets()
    if 'close' in what: close_sheets(['SK229', 'GRW229', 'GRA229', 'GOW229', 'GOA229'], 229); close_sheets(['SK218', 'GRW218', 'GRA218'], 218)
