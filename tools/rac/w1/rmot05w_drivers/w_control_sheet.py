# RM-OT-05W (order §6): the complete frozen control set of the 05K/05N/05O/05V blind protocol, shown LABELLED for author review
# (this is an exhibit, not a scorer sheet; scorer sheets stay coded). Each tile must pass w_tile_check.py first; the sheet refuses
# to build otherwise. Controls: Marchfolk and Skarn ref / nar / brd / low and Grask E3 ref / low, headless, front + profile, cached
# by the 05O run (tag K05a_GO-RD3). Also copies the tiles so the protocol survives outside the session that rendered them.
# Usage: python3 w_control_sheet.py CONTROL_TILE_DIR OUTDIR
import sys, os, json, shutil, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
ctl, out = sys.argv[1:3]; os.makedirs(os.path.join(out, 'control_tiles'), exist_ok=True)
CTRL = ['MF-ref', 'MF-nar', 'MF-brd', 'MF-low', 'SK-ref', 'SK-nar', 'SK-brd', 'SK-low', 'GR-E3-ref', 'GR-E3-low']; TAG = 'K05a_GO-RD3'
tiles = {(k, v): os.path.join(ctl, '%s:%s_nh_%s.png' % (TAG, k, v)) for k in CTRL for v in 'FP'}
chk = subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), 'w_tile_check.py'), os.path.join(out, 'tile_check_controls.json')] + list(tiles.values()))
assert chk.returncode == 0, 'control tiles contaminated: sheet refused'
for (k, v), p in tiles.items(): shutil.copy2(p, os.path.join(out, 'control_tiles', '%s_nh_%s.png' % (k, v)))
try: font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 18)
except Exception: font = ImageFont.load_default()
def crop(p):
    im = Image.open(p).convert('RGBA'); a = np.array(im.split()[3]); c = np.where(a.max(0) > 0)[0]; r = np.where(a.max(1) > 0)[0]
    return im.crop((max(c[0] - 10, 0), r[0], min(c[-1] + 10, im.width), r[-1] + 1))
th = 360; cells = []
for k in CTRL:
    pair = [crop(tiles[(k, v)]) for v in 'FP']; cells.append((k, [im.resize((max(1, int(im.width * th / im.height)), th), Image.LANCZOS) for im in pair]))
rows = [cells[i:i + 5] for i in range(0, len(cells), 5)]; W = max(sum(a.width + b.width + 46 for _, (a, b) in r) for r in rows) + 20
img = Image.new('RGB', (W, len(rows) * (th + 50) + 50), 'white'); dr = ImageDraw.Draw(img)
dr.text((10, 8), 'Frozen blind-gate control set (labelled exhibit) - body only, height-normalized, front + profile; all tiles single-island clean', font=font, fill='black')
for ri, r in enumerate(rows):
    x = 10; y = 40 + ri * (th + 50)
    for k, (a, b) in r:
        img.paste(a, (x, y), a); img.paste(b, (x + a.width + 6, y), b); dr.text((x + 4, y + th + 6), k, font=font, fill='black'); x += a.width + b.width + 46
img.save(os.path.join(out, 'control_set_labelled.jpg'), quality=90)
json.dump(dict(controls=CTRL, cache_tag=TAG, tiles=len(tiles), sheet='control_set_labelled.jpg'), open(os.path.join(out, 'control_set.json'), 'w'), indent=1)
print('control sheet ok')
