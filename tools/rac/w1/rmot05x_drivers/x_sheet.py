# RM-OT-05X: compose x_render.py tiles onto white with labels; optional height grid (whole-figure views with matched framing).
# Usage: python3 x_sheet.py SPEC.json   SPEC = {"out": jpg, "title": str, "tiles": [[path, label], ...], "cols": n,
#                                              "grid": {"ppm": px_per_m, "ground_row": px, "step_m": 0.1, "label_every": 0.5} (optional), "scale": 0.5}
import sys, json
from PIL import Image, ImageDraw, ImageFont
S = json.load(open(sys.argv[1])); sc = S.get('scale', 0.5)
try: font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 20); tf = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 24)
except Exception: font = tf = ImageFont.load_default()
ims = []
for p, lab in S['tiles']:
    im = Image.open(p).convert('RGBA'); bg = Image.new('RGBA', im.size, (255, 255, 255, 255))
    g = S.get('grid')
    if g:
        d = ImageDraw.Draw(bg); k = 0
        while True:
            y = g['ground_row'] - k * g['step_m'] * g['ppm']
            if y < 0: break
            major = abs((k * g['step_m']) / g['label_every'] - round((k * g['step_m']) / g['label_every'])) < 1e-6
            d.line([(0, y), (im.width, y)], fill=(150, 150, 150, 255) if major else (215, 215, 215, 255), width=2 if k == 0 else 1)
            if major: d.text((4, y - 22), '%.1f' % (k * g['step_m']), font=font, fill=(120, 120, 120, 255))
            k += 1
    bg.alpha_composite(im); bg = bg.convert('RGB'); bg = bg.resize((int(bg.width * sc), int(bg.height * sc)), Image.LANCZOS)
    ims.append((bg, lab))
cols = S.get('cols', len(ims)); rows = [ims[i:i + cols] for i in range(0, len(ims), cols)]
W = max(sum(i.width for i, _ in r) for r in rows); H = sum(max(i.height for i, _ in r) + 34 for r in rows) + 44
sheet = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(sheet); dr.text((8, 8), S['title'], font=tf, fill='black'); y = 44
for r in rows:
    x = 0
    for im, lab in r: sheet.paste(im, (x, y + 30)); dr.text((x + 6, y + 4), lab, font=font, fill='black'); x += im.width
    y += max(i.height for i, _ in r) + 34
sheet.save(S['out'], quality=90); print(S['out'])
