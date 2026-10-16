# RM-OT-05AB: identical-camera before/after sheet (rows = mesh tags, columns = views) from x_render.py tiles. Read-only.
# Usage: python3 ab_pair_sheet.py TILE_PREFIX_DIR OUT.jpg WIDTH "TAG1:Label 1" "TAG2:Label 2" -- VIEW1 VIEW2 ...
import sys
from PIL import Image, ImageDraw, ImageFont
a = sys.argv[1:]; i = a.index('--'); d, out, w = a[0], a[1], int(a[2]); tags = [t.split(':', 1) for t in a[3:i]]; views = a[i + 1:]
f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
rows = []
for tag, _ in tags:
    r = []
    for v in views:
        im = Image.open('%s/%s_%s.png' % (d, tag, v)).convert('RGBA'); bg = Image.new('RGBA', im.size, (255, 255, 255, 255)); bg.alpha_composite(im)
        im = bg.convert('RGB'); r.append(im.resize((w, round(im.height * w / im.width))))
    rows.append(r)
W = len(views) * w; Hh = sum(max(x.height for x in r) + 40 for r in rows); c = Image.new('RGB', (W, Hh), 'white'); dr = ImageDraw.Draw(c); y = 0
for (tag, lab), r in zip(tags, rows):
    dr.text((10, y + 8), lab, fill='black', font=f); y += 40
    for k, im in enumerate(r):
        c.paste(im, (k * w, y)); dr.line([(k * w, y), (k * w, y + im.height)], fill=(200, 200, 200))
    y += max(x.height for x in r)
c.save(out, quality=88); print(out, c.size)
