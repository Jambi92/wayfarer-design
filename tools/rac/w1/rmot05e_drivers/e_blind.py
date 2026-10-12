# RAC RM-OT-05E §7 replicated blind read (derived from d_blind, RM-OT-05D). 18 bodies, shuffled with a fixed seed, codes only:
#   - the 8 human-family controls of the RM-OT-05A / 05B protocol (Marchfolk and Skarn x reference / Narrow / Broad / low-muscle);
#   - accepted Grask E3 (reference + low) in EVERY run (the 05D run-2 context);
#   - Gorrund 05D E1 baseline (reference + low) and the 05E Gorrund candidates (reference + low).
# Body only (head and neck removed), height-normalized, front + profile, neutral grey + black silhouette. Key never shown to scorers.
# Usage: python3 e_blind.py runA | runB   [candidates, default P1 P2 P3]
import os, sys, json, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/rmot05a_drivers')
import a_blind as AB
PK = AB.PK; S = AB.S
OUT = S + '/rmot05e/blind'; os.makedirs(OUT, exist_ok=True); PK.R = S + '/rmot05e/rend_blind'; os.makedirs(PK.R, exist_ok=True)
SET = dict(AB.HUM)
SET['GR-E3-ref'] = 'w2c/b/GR5DE3/GR5DE3'; SET['GR-E3-low'] = 'w2c/b/GR5DE3-LOW/GR5DE3-LOW'
SET['GO-E1-ref'] = 'w2d/b/GO5DE1/GO5DE1'; SET['GO-E1-low'] = 'w2d/b/GO5DE1-LOW/GO5DE1-LOW'
CANDS = sys.argv[2:] or ['P1', 'P2', 'P3']
for c in CANDS: SET['GO-%s-ref' % c] = 'w2d/b/GO5E%s/GO5E%s' % (c, c); SET['GO-%s-low' % c] = 'w2d/b/GO5E%s-LOW/GO5E%s-LOW' % (c, c)
SEED, TAG = {'runA': (20261018, ('J', 'E05a')), 'runB': (20261019, ('K', 'E05b')), 'runC': (20261020, ('M', 'E05c'))}[sys.argv[1]]
def sheet(mode):
    rng = np.random.default_rng(SEED); order = [str(k) for k in rng.permutation(sorted(SET))]
    codes = {k: TAG[0] + '%02d' % (i + 1) for i, k in enumerate(order)}
    for k, p in SET.items(): PK.BODIES[TAG[1] + ':' + k] = (S + '/' + p, k)
    th = 360; tiles = []
    for k in order:
        t = PK.ensure(TAG[1] + ':' + k, headless=True); pair = []
        for v in ('F', 'P'):
            im = PK.tile(t, v, sil=(mode == 'sil')); a = np.array(im.split()[3]); rr = np.where(a.max(1) > 0)[0]; im = im.crop((0, rr[0], im.width, rr[-1] + 1))
            s = th / im.height; pair.append(im.resize((max(1, int(im.width * s)), th), Image.LANCZOS))
        tiles.append((codes[k], pair))
    rows = [tiles[i:i + 4] for i in range(0, len(tiles), 4)]; W = max(sum(a.width + b.width + 46 for _, (a, b) in r) for r in rows) + 20
    img = Image.new('RGB', (W, len(rows) * (th + 50) + 50), 'white'); d = ImageDraw.Draw(img)
    d.text((10, 8), 'Blind set ' + TAG[0] + ' - body only, height-normalized, front + profile, %s' % ('neutral grey' if mode == 'grey' else 'black silhouette'), font=PK.SS.font(18), fill='black')
    for ri, r in enumerate(rows):
        x = 10; y = 40 + ri * (th + 50)
        for c, (a, b) in r:
            img.paste(a, (x, y), a); img.paste(b, (x + a.width + 6, y), b); d.text((x, y + th + 6), c, font=PK.SS.font(17), fill='black'); x += a.width + b.width + 46
    fn = OUT + '/blind_%s_%s.jpg' % (TAG[0], mode); img.save(fn, quality=88)
    json.dump({'seed': SEED, 'codes': codes, 'paths': SET}, open(OUT + '/key_%s.json' % TAG[1], 'w'), indent=1); print(fn, flush=True)
if __name__ == '__main__':
    for m in ('grey', 'sil'): sheet(m)
