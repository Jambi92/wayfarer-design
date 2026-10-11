# RAC RM-OT-05 readability closure: neutralized large-race package. Matched camera / ground / stature; R-6 reference stance; reference
# composition; one grey material. Views: front, profile, front 3/4, rear 3/4; black silhouette (alpha); head-cropped body (head and neck
# skin removed by skin weights: w_head + w_neck_01 > 0.3).
import os, sys, json, numpy as np
from PIL import Image, ImageDraw, ImageOps
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(D), 'w3b_drivers'))
import w3b_common as C, w3b_sheet as SS
S = C.S; R = S + '/rmot05r/rend'; SH = S + '/rmot05r/sheets'; os.makedirs(R, exist_ok=True); os.makedirs(SH, exist_ok=True); RV = '/home/claude/wayfarer-design/reviews'
PX = 3.0; SCALE = 250.0; RES = int(SCALE * PX)
BODIES = {}
def reg(bid, path, label): BODIES[bid] = (path, label)
for h, mf, sk, gr, go in ((208, 'w2a/st/MFM203', RV + '/rac-w3d-evidence/geometry/SK208-C1R', 'w2c/b/GR208/GR208', 'w2d/b/GO208/GO208'),
                          (218, None, 'w2c/sk/SKM218', 'w2c/b/GR218R/GR218R', 'w2d/b/GO218/GO218'),
                          (229, None, 'w3d/b/SKM229-C1R', 'w2c/b/GR229/GR229', 'w2d/b/GO229/GO229')):
    if mf: reg('MF203', S + '/' + mf, 'Marchfolk 203 (MF maximum; 208+ not valid)')
    reg('SK%d' % h, sk if sk.startswith('/') else S + '/' + sk, 'Skarn %d' % h); reg('GR%d' % h, S + '/' + gr, 'Grask %d' % h); reg('GO%d' % h, S + '/' + go, 'Gorrund %d' % h)
VIEWS = (('F', 0, 0), ('P', 90, 0), ('Q', 35, 6), ('RQ', 145, 6))
def ensure(bid, headless=False):
    tag = bid + ('_nh' if headless else '')
    if all(os.path.exists('%s/%s_%s.png' % (R, tag, v[0])) for v in VIEWS): return tag
    d = np.load(BODIES[bid][0] + '_r6.npz', allow_pickle=True); V = d['V'].astype(float); F = d['F']; keep = d['keep'].astype(bool)
    if headless: keep = keep & ((d['w_head'] + d['w_neck_01']) < 0.3)
    cf = 0.5 * (V[keep, 1].min() + V[keep, 1].max())
    v = ';'.join('%s:%d:%d:0:%.2f:%.1f:%.1f' % (n, y, e, cf, SCALE / 2 - 5, SCALE) for n, y, e in VIEWS)
    C.save_head_npz(R + '/%s.npz' % tag, V, F, lambda Q: keep); C.render(R + '/%s.npz' % tag, R + '/' + tag, v, RES); os.remove(R + '/%s.npz' % tag); return tag
def tile(tag, view, sil=False):
    im = Image.open('%s/%s_%s.png' % (R, tag, view)).convert('RGBA')
    if sil: a = im.split()[3].point(lambda x: 255 if x > 20 else 0); im = Image.merge('RGBA', (Image.new('L', im.size, 0),) * 3 + (a,))
    a = np.array(im.split()[3]); cols = np.where(a.max(0) > 0)[0]; return im.crop((max(cols[0] - 10, 0), 0, min(cols[-1] + 10, im.width), im.height))
def row_sheet(out, title, sub, ids, view, sil=False, headless=False):
    tags = [ensure(b, headless) for b in ids]; tiles = [tile(t, view, sil) for t in tags]
    W = sum(t.width for t in tiles) + 80; top = 90; img = Image.new('RGB', (W, top + RES + 50), 'white'); d = ImageDraw.Draw(img)
    d.text((12, 10), title, font=SS.font(22), fill='black'); d.text((12, 44), sub, font=SS.font(14), fill=(70, 70, 70))
    ground = top + int(RES / 2 + (SCALE / 2 - 5) * PX)
    for cm in range(0, 241, 20):
        y = ground - int(cm * PX); d.line((0, y, W, y), fill=(235, 235, 235) if cm else (130, 130, 130)); d.text((2, y - 14), str(cm), font=SS.font(11), fill=(120, 120, 120))
    x = 40
    for b, t in zip(ids, tiles):
        img.paste(t, (x, top), t); d.text((x, ground + 6), BODIES[b][1], font=SS.font(13), fill='black'); x += t.width
    img.save(SH + '/' + out, quality=86); print(out, flush=True)
if __name__ == '__main__':
    sets = {208: ['MF203', 'SK208', 'GR208', 'GO208'], 218: ['SK218', 'GR218', 'GO218'], 229: ['SK229', 'GR229', 'GO229']}
    for h, ids in sets.items():
        for vn, vl in (('F', 'front'), ('P', 'profile'), ('Q', 'front 3/4'), ('RQ', 'rear 3/4')):
            row_sheet('r_%d_%s_grey.jpg' % (h, vn), 'Large-race readability %d cm - %s - neutral grey' % (h, vl), 'Matched camera, ground, stature, reference composition, R-6 stance.', ids, vn)
            row_sheet('r_%d_%s_nohead.jpg' % (h, vn), 'Large-race readability %d cm - %s - body only (head and neck removed)' % (h, vl), 'Head / neck skin removed (skin weight > 0.3); no face, ear, hair or texture information.', ids, vn, headless=True)
            row_sheet('r_%d_%s_sil.jpg' % (h, vn), 'Large-race readability %d cm - %s - black silhouette, body only' % (h, vl), 'Pure silhouette, head / neck removed.', ids, vn, sil=True, headless=True)
