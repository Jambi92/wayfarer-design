# RAC W2I1 D4 render sheets: neutral-carriage states 0 / +4 / +8 / +12 deg (sa_carriage.py npz) - front / profile / rear 3/4 full-body
# orthographic (one 300 cm scale) plus a close straight-front pelvis view (70 cm scale, centred at u 80 x H/188) per state.
# Usage: python3 sa_carriage_render.py   (writes $S/w2i/sheets/sa_carriage_*.jpg)
import os, numpy as np
from PIL import Image, ImageDraw
import sa_render as R
def close(bid, h):
    tag = R.W + '/rend/' + bid + '_close'
    if not os.path.exists(tag + '_cfront.png'):
        P = np.load(R.W + '/npz/%s.npz' % bid)['v']; fn = R.W + '/rend/_tmp.npz'; np.savez(fn, P=P.astype(np.float32), f=R.F.astype(np.int32))
        cu = 82.0 * h / 188.0
        R.subprocess.run(['python3', R.RC], env=dict(os.environ, VIEWS="cfront:0:0:0:-40:%.1f:70;cfront_low:0:-12:0:-40:%.1f:70" % (cu, cu), NPZ=fn, TAG=tag, RES='700'),
                         stdout=R.subprocess.DEVNULL, stderr=R.subprocess.DEVNULL)
    return tag
def sheet(name, base, h, title):
    rows = []
    for lift in (0, 4, 8, 12):
        bid = '%s-C%d' % (base, lift); tag = R.render(bid); ct = close(bid, h)
        ims = [Image.open('%s_%s.png' % (tag, v)).convert('RGBA') for v in ('front', 'profile', 'rear34')] + [Image.open('%s_%s.png' % (ct, v)).convert('RGBA') for v in ('cfront', 'cfront_low')]
        w, hh = ims[0].size; row = Image.new('RGB', (w * 5, hh + 30), 'white')
        for i, im in enumerate(ims): bg = Image.new('RGB', im.size, 'white'); bg.paste(im, mask=im.split()[3]); row.paste(bg, (i * w, 30))
        d = ImageDraw.Draw(row); d.text((8, 8), '%s  neutral carriage +%d deg%s   |   front, profile, rear 3/4 (300 cm)   |   close front, close front from 12 deg below (70 cm)' % (base, lift, '  (outside validated +8 lift)' if lift > 8 else ''), fill='black')
        rows.append(row)
    W_ = rows[0].size[0]; out = Image.new('RGB', (W_, sum(r.size[1] for r in rows) + 40), 'white'); ImageDraw.Draw(out).text((8, 12), title, fill='black'); y = 40
    for r in rows: out.paste(r, (0, y)); y += r.size[1]
    out = out.resize((out.size[0] * 2 // 3, out.size[1] * 2 // 3)); out.save(R.W + '/sheets/' + name, quality=88); print('saved', name, out.size)
if __name__ == '__main__':
    sheet('sa_carriage_M188.jpg', 'SA-M188', 187.88, 'W2I1 D4 neutral-carriage test: SA-M 188 (frozen anatomy; carriage only)')
    sheet('sa_carriage_F188.jpg', 'SA-F188', 187.88, 'W2I1 D4 neutral-carriage test: SA-F 188 (§263 centre; carriage only)')
    sheet('sa_carriage_M208.jpg', 'SA-M208', 208.0, 'W2I1 D4 neutral-carriage test: SA-M 208 (carriage only)')
