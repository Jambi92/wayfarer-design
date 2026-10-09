# RAC W2I2 before / after orthographic sheets (order §18.7): as-built vs leg (L1-L3), forearm (F1-F3) and combined candidates at 188 cm, and
# the root-carriage family (0 / +2 / +4 / +6 / +8 deg; full front / profile / rear 3/4 + close front + close front from 12 deg below).
# One ortho scale per sheet (300 cm full body, 70 cm close). Usage: python3 sa_w2i2_render.py limbs COMBO | carriage
import sys, os, numpy as np
from PIL import Image, ImageDraw
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D); sys.path.insert(0, os.path.join(os.path.dirname(D), 'w2i_drivers'))
import sa_render as R, sa_carriage_render as CR, sa_cand as SC, sa_w2i2_build as WB
def save(bid, p, cand, h=SC.H0):
    fn = R.W + '/npz/%s.npz' % bid
    if not os.path.exists(fn): P, q, k, info = SC.build_c(p, cand, h); np.savez(fn, v=P.astype(np.float32))
    return bid
def rows_sheet(name, items, title, close=False):
    rows = []
    for bid, lab, h in items:
        tag = R.render(bid); ims = [Image.open('%s_%s.png' % (tag, v)).convert('RGBA') for v in ('front', 'profile', 'rear34')]
        if close: ct = CR.close(bid, h); ims += [Image.open('%s_%s.png' % (ct, v)).convert('RGBA') for v in ('cfront', 'cfront_low')]
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
    if out.size[0] > 2400: out = out.resize((out.size[0] * 2 // 3, out.size[1] * 2 // 3))
    out.save(R.W + '/sheets/' + name, quality=88); print('saved', name, out.size)
if __name__ == '__main__':
    if sys.argv[1] == 'limbs':
        combo = sys.argv[2]; it = [(save('SA-M188-W2I2-AS', {}, {}), 'as-built SA-M188 (frozen aff1b52 anatomy)', SC.H0)]
        for c in ('L1', 'L2', 'L3'): it.append((save('SA-M188-W2I2-' + c, {}, WB.CANDS[c]), 'leg candidate %s (thigh +%.1f cm; thorax / neck -%.1f / -%.1f cm)' % (c, WB.CANDS[c]['G'], 0.4 * WB.CANDS[c]['G'], 0.6 * WB.CANDS[c]['G']), SC.H0))
        rows_sheet('w2i2_legs_M188.jpg', it, 'W2I2 leg candidates at 188 cm (copies; standing height constant; tail excluded)')
        it = [(save('SA-M188-W2I2-AS', {}, {}), 'as-built SA-M188', SC.H0)] + [(save('SA-M188-W2I2-' + c, {}, WB.CANDS[c]), 'forearm candidate %s (elbow %.1f cm toward the shoulder)' % (c, WB.CANDS[c]['fa_delta']), SC.H0) for c in ('F1', 'F2', 'F3')]
        rows_sheet('w2i2_forearm_M188.jpg', it, 'W2I2 forearm candidates at 188 cm (shoulder, wrist, hand fixed)')
        cc = WB.combo(combo); it = [(save('SA-M188-W2I2-AS', {}, {}), 'as-built SA-M188', SC.H0), (save('SA-M188-W2I2-' + combo.replace('+', ''), {}, cc), 'combined candidate %s' % combo, SC.H0),
                                   (save('SA-F188-W2I2-AS', SC.B.CEN, {}), 'as-built SA-F188 (§263 centre)', SC.H0), (save('SA-F188-W2I2-' + combo.replace('+', ''), SC.B.CEN, cc), 'combined candidate %s, female centre' % combo, SC.H0),
                                   (save('SA-M168-W2I2-' + combo.replace('+', ''), {}, cc, 168.0), 'combined %s at 168' % combo, 168.0), (save('SA-M208-W2I2-' + combo.replace('+', ''), {}, cc, 208.0), 'combined %s at 208' % combo, 208.0)]
        rows_sheet('w2i2_combined.jpg', it, 'W2I2 combined limb candidate %s: before / after (copies)' % combo)
    else:
        for base, h in (("SA-M188", SC.H0), ("SA-F188", SC.H0), ("SA-M208", 208.0)):
            rows_sheet('w2i2_rootcarriage_%s.jpg' % base[3:], [('%s-R%d' % (base, th), '%s root pitch +%d deg (proximal bend; distal carriage neutral)' % (base, th), h) for th in (0, 2, 4, 6, 8)],
                       'W2I2 root-carriage family: %s (frozen anatomy; carriage only)' % base, close=True)
