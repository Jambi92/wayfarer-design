# RAC Stage C sheet composer: common-scale renders (stc_render.py) side by side on one ground line, labelled.
# Usage: python3 stc_sheet.py OUT.jpg VIEW 'TITLE' prefix=label ...   (VIEW = F | Q | P | B | Fs | Ps or comma list, one row per view)
import sys, numpy as np
from PIL import Image, ImageDraw, ImageFont
out, views, title = sys.argv[1], sys.argv[2].split(','), sys.argv[3]
items = [a.split('=', 1) for a in sys.argv[4:]]
try: font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 18); tfont = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
except Exception: font = tfont = ImageFont.load_default()
def crop(im):
    a = np.array(im.split()[3]); cols = np.where(a.max(0) > 0)[0]
    return im.crop((max(cols[0] - 14, 0), 0, min(cols[-1] + 14, im.width), im.height)) if len(cols) else im
rows = []
for v in views:
    tiles = [(crop(Image.open('%s_%s.png' % (p, v)).convert('RGBA')), lab) for p, lab in items]
    W = sum(t.width for t, _ in tiles); H = tiles[0][0].height
    row = Image.new('RGBA', (W, H + 50), (58, 58, 58, 255)); d = ImageDraw.Draw(row); x = 0
    for t, lab in tiles:
        row.alpha_composite(t, (x, 0)); d.text((x + 6, H + 8), lab, fill=(235, 235, 235), font=font); x += t.width
    gy = int(H - 0.10 * H / 2.8 * 1.0)                      # ground row (camera target 10 cm below frame centre)
    d.line((0, H - 30, W, H - 30), fill=(95, 95, 95), width=1)
    rows.append(row)
W = max(max(r.width for r in rows), int(ImageDraw.Draw(Image.new('RGB', (1, 1))).textlength(title, font=tfont)) + 20); H = sum(r.height for r in rows) + 40
o = Image.new('RGB', (W, H), (58, 58, 58)); d = ImageDraw.Draw(o); d.text((10, 8), title, fill=(255, 255, 255), font=tfont); y = 40
for r in rows: o.paste(r.convert('RGB'), (0, y)); y += r.height
o.save(out, quality=88); print(out, o.size)
