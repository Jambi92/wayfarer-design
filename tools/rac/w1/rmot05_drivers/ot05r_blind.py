# RAC RM-OT-05 readability: blind / low-information silhouette diagnostic. 16 bodies (MF / SK / GR / GO x reference, Narrow, Broad, low-muscle),
# body-only black silhouettes (head and neck removed), front + profile, matched ortho scale; order shuffled with a fixed seed and labels
# hidden (codes only). The key is written separately. Supporting evidence only.
import os, sys, json, numpy as np
from PIL import Image, ImageDraw
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import ot05r_package as PK
S = PK.S
B = {'MF-ref': 'w1f/final/MF-M-R', 'MF-nar': 'w2a1/p/MNX', 'MF-brd': 'w2a1/p/MBX', 'MF-low': 'w2a/comp/MFM-LOWMUS',
     'SK-ref': 'w1f/final/SK', 'SK-nar': 'w2b/fr/SKMNarrow', 'SK-brd': 'w2b/fr/SKMBroad', 'SK-low': 'w2b/comp/SKM-LOWMUS',
     'GR-ref': 'w2c/b/GR218R/GR218R', 'GR-nar': 'w2c/b/GRN5/GRN5', 'GR-brd': 'w2c/b/GRB2/GRB2', 'GR-low': 'w2c/b/GR218R/GR218R-LEAN',
     'GO-ref': 'w2d/b/GOREF/GOREF', 'GO-nar': 'w2d/b/GON5/GON5', 'GO-brd': 'w2d/b/GOB7/GOB7', 'GO-low': 'w2d/b/GOREF/GOREF-LEAN'}
for k, p in B.items(): PK.BODIES[k] = (S + '/' + p, k)
rng = np.random.default_rng(20261010); keys = list(B); order = list(rng.permutation(keys)); codes = {k: 'B%02d' % (i + 1) for i, k in enumerate(order)}
json.dump({'order': [str(k) for k in order], 'codes': codes, 'seed': 20261010}, open(S + '/rmot05r/blind_key.json', 'w'), indent=1)
def sheet(out, view):
    tiles = []
    for k in order:
        t = PK.ensure(k, headless=True); im = PK.tile(t, view, sil=True)
        H = 1.0 * im.height; tiles.append((codes[k], im))
    # normalized height: every body scaled to the same displayed height so absolute stature carries no information
    th = 520; row = []
    for c, im in tiles:
        a = np.array(im.split()[3]); rows = np.where(a.max(1) > 0)[0]; im = im.crop((0, rows[0], im.width, rows[-1] + 1))
        s = th / im.height; row.append((c, im.resize((max(1, int(im.width * s)), th), Image.LANCZOS)))
    W = sum(r[1].width + 20 for r in row[:8]) + 40; img = Image.new('RGB', (W, 2 * (th + 60) + 80), 'white'); d = ImageDraw.Draw(img)
    d.text((12, 10), 'RM-OT-05 blind silhouette diagnostic - %s, body only, height-normalized, labels hidden' % view, font=PK.SS.font(20), fill='black')
    for j, (c, im) in enumerate(row):
        r_, cidx = divmod(j, 8); x = 20 + sum(rr[1].width + 20 for rr in row[r_ * 8:j]); y = 60 + r_ * (th + 60)
        img.paste(im, (x, y), im); d.text((x, y + th + 6), c, font=PK.SS.font(16), fill='black')
    img.save(PK.SH + '/' + out, quality=88); print(out)
if __name__ == '__main__':
    sheet('blind_front.jpg', 'F'); sheet('blind_profile.jpg', 'P')
