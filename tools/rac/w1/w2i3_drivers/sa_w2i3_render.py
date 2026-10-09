# RAC W2I3 sheets: rebuilt L1 + F2 reference (SA-M188 / SA-F188 vs frozen and W2I2 diagnostic; 168 / 188 / 203 / 208 family) and the caudal-base
# family C0-C3 (full front / profile / rear 3/4 at one 300 cm scale + close front, close below-front, rear close root, side close root at 70 cm).
# Usage: python3 sa_w2i3_render.py ref | caudal
import sys, os, numpy as np
from PIL import Image, ImageDraw
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D); sys.path.insert(0, os.path.join(os.path.dirname(D), 'w2i_drivers')); sys.path.insert(0, os.path.join(os.path.dirname(D), 'w2i2_drivers'))
import sa_render as R, sa_rebuild as RB, sa_cand as SC, sa_build as B
def save(bid, fn_):
    f = R.W + '/npz/%s.npz' % bid
    if not os.path.exists(f): P = fn_(); np.savez(f, v=P.astype(np.float32))
    return bid
def views(bid, spec, tag_sfx):
    tag = R.W + '/rend/' + bid + tag_sfx
    if not os.path.exists(tag + '_' + spec.split(';')[0].split(':')[0] + '.png'):
        P = np.load(R.W + '/npz/%s.npz' % bid)['v']; fn = R.W + '/rend/_tmp3.npz'; np.savez(fn, P=P.astype(np.float32), f=R.F.astype(np.int32))
        R.subprocess.run(['python3', R.RC], env=dict(os.environ, VIEWS=spec, NPZ=fn, TAG=tag, RES='560'), stdout=R.subprocess.DEVNULL, stderr=R.subprocess.DEVNULL)
    return [Image.open('%s_%s.png' % (tag, s.split(':')[0])).convert('RGBA') for s in spec.split(';')]
FULL = "front:0:0:0:-40:110:300;profile:90:0:0:-40:110:300;rear34:150:0:0:-40:110:300"
def close_spec(h):
    c = 90.0 * h / 188.0
    return "cfront:0:0:0:-40:%.1f:70;cbelow:0:-12:0:-40:%.1f:70;crear:180:0:0:-30:%.1f:70;cside:90:0:0:-30:%.1f:70" % (c, c, c + 4, c + 4)
def sheet(name, items, title, close=False):
    rows = []
    for bid, lab, h in items:
        ims = views(bid, FULL, '_w3full') + (views(bid, close_spec(h), '_w3close') if close else [])
        w, hh = ims[0].size; row = Image.new('RGB', (w * len(ims), hh + 30), 'white')
        for i, im in enumerate(ims): bg = Image.new('RGB', im.size, 'white'); bg.paste(im, mask=im.split()[3]); row.paste(bg, (i * w, 30))
        d = ImageDraw.Draw(row); d.text((8, 8), lab, fill='black')
        for i in range(3):
            for cm in range(0, 301, 50):
                y = 30 + hh - int((cm + 40) / 300 * hh)
                if 30 <= y < hh + 30: d.line([(i * w, y), (i * w + 8, y)], fill=(200, 0, 0)); d.text((i * w + 10, y - 6), str(cm), fill=(200, 0, 0))
        rows.append(row)
    W_ = max(r.size[0] for r in rows); out = Image.new('RGB', (W_, sum(r.size[1] for r in rows) + 40), 'white'); ImageDraw.Draw(out).text((8, 12), title, fill='black'); y = 40
    for r in rows: out.paste(r, (0, y)); y += r.size[1]
    if out.size[0] > 2600: out = out.resize((out.size[0] * 3 // 5, out.size[1] * 3 // 5))
    out.save(R.W + '/sheets/' + name, quality=88); print('saved', name, out.size)
if __name__ == '__main__':
    if sys.argv[1] == 'ref':
        it = []
        for sx, p in (("M", {}), ("F", B.CEN)):
            it += [(save('W2I3-SA-%s188-FROZEN' % sx, lambda p=p: RB.build_r(p, {})[0]), 'frozen SA-%s188 (as-built, unchanged)' % sx, B.H0),
                   (save('W2I3-SA-%s188-DIAG' % sx, lambda p=p: SC.build_c(p, {'G': 9.2, 'FT': 0.4, 'fa_delta': 4.2})[0]), 'W2I2 diagnostic L1 + F2 (study warp)', B.H0),
                   (save('W2I3-SA-%s188-R' % sx, lambda p=p: RB.build_r(p, RB.TARGET)[0]), 'W2I3 rebuilt L1 + F2 candidate SA-%s188' % sx, B.H0)]
        sheet('w2i3_rebuilt_188.jpg', it, 'W2I3 rebuilt L1 + F2 reference candidate vs frozen and W2I2 diagnostic (copies; neutral carriage)')
        fam = [(save('W2I3-SA-M%d-R' % h, lambda h=h: RB.build_r({}, RB.TARGET, float(h) if h != 188 else None)[0]), 'rebuilt candidate SA-M%d' % h, float(h)) for h in (168, 188, 203, 208)]
        sheet('w2i3_rebuilt_family.jpg', fam, 'W2I3 rebuilt candidate stature family 168 / 188 / 203 / 208 (regional route)')
    else:
        for sx in ("M", "F"):
            sheet('w2i3_caudal_%s188.jpg' % sx, [('W2I3-SA-%s188-%s' % (sx, c), 'SA-%s188 rebuilt + caudal-base %s' % (sx, c), B.H0) for c in ("C0", "C1", "C2", "C3")],
                  'W2I3 caudal-base contour family C0-C3, SA-%s188 (rebuilt L1 + F2; neutral carriage)' % sx, close=True)
