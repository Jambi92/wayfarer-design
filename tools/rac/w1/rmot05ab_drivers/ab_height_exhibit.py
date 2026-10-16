# RM-OT-05AB: equal-displayed-height macro exhibit (display copies scaled to 1.90 m by aa_normalise.py, rendered by x_render.py)
# with each body's own crotch (blue) and lowest-fingertip (red) lines from aa_macro.py, and the W1 ARM levels dashed. Read-only.
# Usage: python3 ab_height_exhibit.py RENDER_DIR MACRO.json OUT.jpg TITLE NAME:LABEL ...   (tiles RENDER_DIR/NAME_F.png, NAME_L.png)
import sys, json
from PIL import Image, ImageDraw, ImageFont
rd, mj, out, title = sys.argv[1:5]; items = [a.split(':', 1) for a in sys.argv[5:]]; M = json.load(open(mj))
ppm = 800 / 2.1; g = 400 + 0.97 * ppm; row = lambda pct: g - 1.90 * pct / 100 * ppm
f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 17); tf = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
cols = [(n, l, v) for v in 'FL' for n, l in items]; W = len(cols) * 400 + 40; c = Image.new('RGB', (W, 650), 'white'); d = ImageDraw.Draw(c)
d.text((20, 10), title, fill='black', font=tf)
for i, (n, lab, v) in enumerate(cols):
    im = Image.open('%s/%s_%s.png' % (rd, n, v)).convert('RGBA'); bg = Image.new('RGBA', im.size, (255, 255, 255, 255)); bg.alpha_composite(im)
    t = bg.convert('RGB').crop((100, 0, 700, 800)).resize((390, 520)); x = 20 + i * 400; y0 = 60; c.paste(t, (x, y0)); sc = 520 / 800
    def ln(pct, col, dash=False):
        y = y0 + row(pct) * sc
        if dash:
            for xx in range(x, x + 390, 14): d.line([(xx, y), (xx + 7, y)], fill=col, width=2)
        else: d.line([(x, y), (x + 390, y)], fill=col, width=3)
    ln(M['GO_W1_ARM']['crotch_pct'], (120, 160, 255), True); ln(M['GO_W1_ARM']['fingertip_pct'], (255, 140, 140), True)
    ln(M[n]['crotch_pct'], (0, 60, 220)); ln(M[n]['fingertip_pct'], (220, 0, 0))
    d.text((x, y0 + 530), lab + (' front' if v == 'F' else ' profile'), fill='black', font=f)
    d.text((x, y0 + 555), 'crotch %.1f%%  fingertip %.1f%%' % (M[n]['crotch_pct'], M[n]['fingertip_pct']), fill='black', font=f)
c.save(out, quality=90); print(out, c.size)
