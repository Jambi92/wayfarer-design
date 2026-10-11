# RAC RM-OT-05C §7.2 lightweight blind read. 20 bodies, shuffled with a fixed seed and labelled by code only:
#   - the 8 human-family controls of the RM-OT-05A / 05B protocol (Marchfolk and Skarn x reference / Narrow / Broad / low-muscle);
#   - Grask candidates A / B / C at reference composition and their low-composition states;
#   - Gorrund candidates A / B / C at reference composition and their low-composition states.
# Body only (head and neck removed), height-normalized, front + profile. Two sheets: neutral grey and pure black silhouette. The key is
# written separately and is never shown to the scorers.   Usage: python3 c_blind.py
import os, sys, json, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/rmot05a_drivers')
import a_blind as AB
PK = AB.PK; S = AB.S
OUT = S + '/rmot05c/blind'; os.makedirs(OUT, exist_ok=True); PK.R = S + '/rmot05c/rend_blind'; os.makedirs(PK.R, exist_ok=True)
SET = dict(AB.HUM)
for c in 'ABC':
    SET['GR-%s-ref' % c] = 'w2c/b/GR5C%s/GR5C%s' % (c, c); SET['GR-%s-low' % c] = 'w2c/b/GR5C%s-LOW/GR5C%s-LOW' % (c, c)
    SET['GO-%s-ref' % c] = 'w2d/b/GO5C%s/GO5C%s' % (c, c); SET['GO-%s-low' % c] = 'w2d/b/GO5C%s-LOW/GO5C%s-LOW' % (c, c)
SEED = 20261014
def sheet(mode):
    rng = np.random.default_rng(SEED); order = [str(k) for k in rng.permutation(sorted(SET))]
    codes = {k: 'R%02d' % (i + 1) for i, k in enumerate(order)}
    for k, p in SET.items(): PK.BODIES['C05:' + k] = (S + '/' + p, k)
    th = 360; tiles = []
    for k in order:
        t = PK.ensure('C05:' + k, headless=True); pair = []
        for v in ('F', 'P'):
            im = PK.tile(t, v, sil=(mode == 'sil')); a = np.array(im.split()[3]); rr = np.where(a.max(1) > 0)[0]; im = im.crop((0, rr[0], im.width, rr[-1] + 1))
            s = th / im.height; pair.append(im.resize((max(1, int(im.width * s)), th), Image.LANCZOS))
        tiles.append((codes[k], pair))
    rows = [tiles[i:i + 5] for i in range(0, len(tiles), 5)]; W = max(sum(a.width + b.width + 46 for _, (a, b) in r) for r in rows) + 20
    img = Image.new('RGB', (W, len(rows) * (th + 50) + 50), 'white'); d = ImageDraw.Draw(img)
    d.text((10, 8), 'Blind set R - body only, height-normalized, front + profile, %s' % ('neutral grey' if mode == 'grey' else 'black silhouette'), font=PK.SS.font(18), fill='black')
    for ri, r in enumerate(rows):
        x = 10; y = 40 + ri * (th + 50)
        for c, (a, b) in r:
            img.paste(a, (x, y), a); img.paste(b, (x + a.width + 6, y), b); d.text((x, y + th + 6), c, font=PK.SS.font(17), fill='black'); x += a.width + b.width + 46
    fn = OUT + '/blind_R_%s.jpg' % mode; img.save(fn, quality=88)
    json.dump({'seed': SEED, 'codes': codes, 'paths': SET}, open(OUT + '/key_C05.json', 'w'), indent=1); print(fn, flush=True)
if __name__ == '__main__':
    for m in ('grey', 'sil'): sheet(m)
