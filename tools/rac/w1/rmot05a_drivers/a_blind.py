# RAC RM-OT-05A §9 blind readability rerun: 16 bodies (Marchfolk / Skarn human-family controls, Grask, Gorrund x reference, Narrow, Broad,
# low-muscle), body only (head and neck removed), height-normalized, front + profile, shuffled with a fixed seed, codes only. Two sheets per
# set: neutral grey and pure black silhouette. Set NEW = RM-OT-05A candidates; set W2 = the accepted W2 bodies (provenance, same protocol).
# Keys are written separately and are never shown to the scorers.   Usage: python3 a_blind.py
import os, sys, json, numpy as np
from PIL import Image, ImageDraw
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(D), 'rmot05_drivers'))
import ot05r_package as PK
S = PK.S; OUT = S + '/rmot05a/blind'; os.makedirs(OUT, exist_ok=True); PK.R = S + '/rmot05a/rend'
HUM = {'MF-ref': 'w1f/final/MF-M-R', 'MF-nar': 'w2a1/p/MNX', 'MF-brd': 'w2a1/p/MBX', 'MF-low': 'w2a/comp/MFM-LOWMUS',
       'SK-ref': 'w1f/final/SK', 'SK-nar': 'w2b/fr/SKMNarrow', 'SK-brd': 'w2b/fr/SKMBroad', 'SK-low': 'w2b/comp/SKM-LOWMUS'}
SETS = {'NEW': dict(HUM, **{'GR-ref': 'w2c/b/GRA218/GRA218', 'GR-nar': 'w2c/b/GRAN/GRAN', 'GR-brd': 'w2c/b/GRAB/GRAB', 'GR-low': 'w2c/b/GRA218-LOW/GRA218-LOW',
                             'GO-ref': 'w2d/b/GOAREF/GOAREF', 'GO-nar': 'w2d/b/GOAN/GOAN', 'GO-brd': 'w2d/b/GOAB/GOAB', 'GO-low': 'w2d/b/GOAREF-LOW/GOAREF-LOW'}),
        'W2': dict(HUM, **{'GR-ref': 'w2c/b/GR218R/GR218R', 'GR-nar': 'w2c/b/GRN5/GRN5', 'GR-brd': 'w2c/b/GRB2/GRB2', 'GR-low': 'w1l/comp_w1l/GR-BODY-06',
                            'GO-ref': 'w2d/b/GOREF/GOREF', 'GO-nar': 'w2d/b/GON5/GON5', 'GO-brd': 'w2d/b/GOB7/GOB7', 'GO-low': 'w2d/b/GOR-BODY-06/GOR-BODY-06'})}
SEED = {'NEW': 20261011, 'W2': 20261012}
def sheet(setname, mode):
    B = SETS[setname]; rng = np.random.default_rng(SEED[setname]); order = [str(k) for k in rng.permutation(list(B))]
    codes = {k: '%s%02d' % ({'NEW': 'N', 'W2': 'P'}.get(setname, 'Q'), i + 1) for i, k in enumerate(order)}
    for k, p in B.items(): PK.BODIES[setname + ':' + k] = (S + '/' + p, k)
    th = 380; tiles = []
    for k in order:
        t = PK.ensure(setname + ':' + k, headless=True); pair = []
        for v in ('F', 'P'):
            im = PK.tile(t, v, sil=(mode == 'sil')); a = np.array(im.split()[3]); rr = np.where(a.max(1) > 0)[0]; im = im.crop((0, rr[0], im.width, rr[-1] + 1))
            s = th / im.height; pair.append(im.resize((max(1, int(im.width * s)), th), Image.LANCZOS))
        tiles.append((codes[k], pair))
    rows = [tiles[:8], tiles[8:]]; W = max(sum(a.width + b.width + 46 for _, (a, b) in r) for r in rows) + 20
    img = Image.new('RGB', (W, 2 * (th + 50) + 50), 'white'); d = ImageDraw.Draw(img)
    d.text((10, 8), 'Blind set %s - body only, height-normalized, front + profile, %s' % (codes[order[0]][0], 'neutral grey' if mode == 'grey' else 'black silhouette'), font=PK.SS.font(18), fill='black')
    for ri, r in enumerate(rows):
        x = 10; y = 40 + ri * (th + 50)
        for c, (a, b) in r:
            img.paste(a, (x, y), a); img.paste(b, (x + a.width + 6, y), b); d.text((x, y + th + 6), c, font=PK.SS.font(17), fill='black'); x += a.width + b.width + 46
    fn = OUT + '/blind_%s_%s.jpg' % (codes[order[0]][0], mode); img.save(fn, quality=88)
    json.dump({'set': setname, 'seed': SEED[setname], 'codes': codes, 'paths': B}, open(OUT + '/key_%s.json' % setname, 'w'), indent=1); print(fn, flush=True)
if __name__ == '__main__':
    for s in ('NEW', 'W2'):
        for m in ('grey', 'sil'): sheet(s, m)
