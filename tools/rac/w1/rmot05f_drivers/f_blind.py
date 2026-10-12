# RAC RM-OT-05F replicated blind-gate RUNNER for the Gorrund hand-sculpt (order §5.4), derived from e_blind (RM-OT-05E).
# Set per run (12 bodies): the 8 human-family controls of the 05A / 05B protocol (Marchfolk and Skarn x reference / Narrow / Broad / low),
# accepted Grask E3 reference + low (every run), and the Gorrund sculpt reference + low (GO5F<SID>, GO5F<SID>-LOW).
# Body only (head and neck removed), height-normalized, matched front + profile, neutral grey + black silhouette, fresh shuffle per run
# (seed per run), codes only; the key is written separately and never shown to scorers. Scorers: f_scorer_prompt.md; tally: f_tally.py.
# Usage: python3 f_blind.py SID run1|run2|run3 [--dry]     (--dry labels the sheet DRY RUN: pipeline check only, never scored)
import os, sys, json, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/rmot05a_drivers')
import a_blind as AB
PK = AB.PK; S = AB.S
OUT = S + '/rmot05f/blind'; os.makedirs(OUT, exist_ok=True); PK.R = S + '/rmot05f/rend_blind'; os.makedirs(PK.R, exist_ok=True)
SET = dict(AB.HUM)
SET['GR-E3-ref'] = 'w2c/b/GR5DE3/GR5DE3'; SET['GR-E3-low'] = 'w2c/b/GR5DE3-LOW/GR5DE3-LOW'
SID = sys.argv[1]; RUN = sys.argv[2]; DRY = '--dry' in sys.argv
SET['GO-S-ref'] = 'w2d/b/GO5F%s/GO5F%s' % (SID, SID); SET['GO-S-low'] = 'w2d/b/GO5F%s-LOW/GO5F%s-LOW' % (SID, SID)
SEED, TAG = {'run1': (20261101, ('P', 'F05a')), 'run2': (20261102, ('Q', 'F05b')), 'run3': (20261103, ('R', 'F05c'))}[RUN]
SEED = SEED * 1000 + sum(ord(ch) * 31 ** i for i, ch in enumerate(SID)) % 997      # fresh shuffle per run AND per delivered sculpt ID
TAG = (TAG[0], TAG[1] + '_' + SID + ('_DRY' if DRY else ''))
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
    d.text((10, 8), ('DRY RUN (pipeline check, not for scoring) - ' if DRY else '') + 'Blind set ' + TAG[0] + ' - body only, height-normalized, front + profile, %s' % ('neutral grey' if mode == 'grey' else 'black silhouette'), font=PK.SS.font(18), fill='black')
    for ri, r in enumerate(rows):
        x = 10; y = 40 + ri * (th + 50)
        for c, (a, b) in r:
            img.paste(a, (x, y), a); img.paste(b, (x + a.width + 6, y), b); d.text((x, y + th + 6), c, font=PK.SS.font(17), fill='black'); x += a.width + b.width + 46
    fn = OUT + '/blind_%s_%s_%s.jpg' % (TAG[0], TAG[1], mode); img.save(fn, quality=88)
    json.dump({'seed': SEED, 'codes': codes, 'paths': SET}, open(OUT + '/key_%s.json' % TAG[1], 'w'), indent=1); print(fn, flush=True)
if __name__ == '__main__':
    for m in ('grey', 'sil'): sheet(m)
