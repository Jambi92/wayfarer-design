# quick uninformed-reviewer probe sheet: body-only grey (not silhouette), front + profile, height-normalized, shuffled codes
import sys, json, numpy as np
from PIL import Image, ImageDraw
import a_preview as AP
PK = AP.PK; S = AP.S
def sheet(ids, out, seed, mode='grey'):
    rng = np.random.default_rng(seed); order = list(rng.permutation(ids)); codes = {k: 'X%d' % (i + 1) for i, k in enumerate(order)}
    th = 420; tiles = []
    for k in order:
        t = PK.ensure(k, headless=True); row = []
        for v in ('F', 'P'):
            im = PK.tile(t, v, sil=(mode == 'sil')); a = np.array(im.split()[3]); rr = np.where(a.max(1) > 0)[0]; im = im.crop((0, rr[0], im.width, rr[-1] + 1))
            s = th / im.height; row.append(im.resize((max(1, int(im.width * s)), th), Image.LANCZOS))
        tiles.append((codes[k], row))
    W = sum(r[0].width + r[1].width + 40 for _, r in tiles) + 20; img = Image.new('RGB', (W, th + 60), 'white'); d = ImageDraw.Draw(img); x = 10
    for c, (a, b) in tiles:
        img.paste(a, (x, 10), a); img.paste(b, (x + a.width + 5, 10), b); d.text((x, th + 20), c, font=PK.SS.font(18), fill='black'); x += a.width + b.width + 40
    img.save(out, quality=88); json.dump(codes, open(out + '.key.json', 'w'))
if __name__ == '__main__':
    tag = sys.argv[1]
    PK.reg('SK218x', S + '/w2c/sk/SKM218', 'x'); PK.reg('MFx', S + '/w1f/final/MF-M-R', 'x'); PK.reg('GR218x', S + '/w2c/b/GR218R/GR218R', 'x'); PK.reg('GO229x', S + '/w2d/b/GO229/GO229', 'x')
    PK.BODIES['GRA' + tag] = (AP.OUT + '/GRA' + tag, 'x'); PK.BODIES['GOA' + tag] = (AP.OUT + '/GOA' + tag, 'x')
    sheet(['SK218x', 'MFx', 'GR218x', 'GO229x', 'GRA' + tag, 'GOA' + tag], AP.OUT + '/blindq_%s.jpg' % tag, int(sys.argv[2]))
