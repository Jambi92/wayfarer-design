# RAC W3B render / sheet helper (rclose.py workbench renders; matched cameras within a sheet; neutral naked head = base without display)
import os, sys, numpy as np
from PIL import Image, ImageDraw, ImageFont
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import w3b_common as C
R = C.W + '/rend'; os.makedirs(R, exist_ok=True); SH = C.W + '/sheets'; os.makedirs(SH, exist_ok=True)
ORBV = "oF:0:2:0:12:183.2:15;oF34:32:8:0:11:183.2:15;oP:90:2:0:10:183:17;oT:0:70:0:9:183.5:17"
def font(n):
    for p in ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', '/usr/share/fonts/dejavu/DejaVuSans.ttf'):
        if os.path.exists(p): return ImageFont.truetype(p, n)
    return ImageFont.load_default()
def ensure(tag, P, Fa, views, res=800, box=None):
    names = [v.split(':')[0] for v in views.split(';')]
    if all(os.path.exists('%s/%s_%s.png' % (R, tag, n)) for n in names): return
    C.save_head_npz(R + '/%s.npz' % tag, P, Fa, box); C.render(R + '/%s.npz' % tag, R + '/' + tag, views, res); os.remove(R + '/%s.npz' % tag)
def sheet(out, title, sub, rows, views, labels, cell=360):
    names = [v.split(':')[0] for v in views.split(';')]; lw = 260; top = 70 + 24 * len(sub) + 30
    img = Image.new('RGB', (lw + cell * len(names), top + cell * len(rows) + 10), 'white'); d = ImageDraw.Draw(img)
    d.text((14, 12), title, font=font(24), fill='black')
    for i, s in enumerate(sub): d.text((14, 50 + 24 * i), s, font=font(16), fill=(70, 70, 70))
    for j, l in enumerate(labels): d.text((lw + j * cell + 6, top - 26), l, font=font(16), fill=(70, 70, 70))
    for i, (tag, lab) in enumerate(rows):
        d.multiline_text((10, top + i * cell + cell // 2 - 30), lab, font=font(17), fill='black', spacing=4)
        for j, n in enumerate(names):
            p = '%s/%s_%s.png' % (R, tag, n)
            if os.path.exists(p):
                im = Image.open(p).convert('RGBA').resize((cell, cell), Image.LANCZOS); bg = Image.new('RGB', im.size, 'white'); bg.paste(im, mask=im.split()[3]); img.paste(bg, (lw + j * cell, top + i * cell))
    img.save(SH + '/' + out, quality=88); return SH + '/' + out
