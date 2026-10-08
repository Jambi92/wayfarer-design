# RAC W2I render sheets: orthographic front / profile / rear-3/4 views (Blender workbench via the accepted Saurin rclose.py) of the saved W2I
# Saurin bodies (sa_build.py npz) and selected MPFB comparators; one ortho scale per sheet so actual sizes compare within a sheet.
# Usage: python3 sa_render.py   (writes $S/w2i/sheets/*.jpg)
import os, json, subprocess, numpy as np
from PIL import Image, ImageDraw
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; W = S + '/w2i'; RC = W + '/rodin/g1/rclose.py'
F = np.load(W + '/rodin/c12/g15_body.npz')['F']
REGS = {}
for f in ('rac-w2d-go-evidence/registry.json', 'rac-w2g-hv-evidence/registry.json'): REGS.update(json.load(open('/home/claude/wayfarer-design/reviews/' + f)))
VIEWS = "front:0:0:0:-40:110:300;profile:90:0:0:-40:110:300;rear34:150:0:0:-40:110:300"
os.makedirs(W + '/rend', exist_ok=True); os.makedirs(W + '/sheets', exist_ok=True)
def render(bid):
    tag = W + '/rend/' + bid
    if os.path.exists(tag + '_profile.png'): return tag
    if bid.startswith('SA'):
        P = np.load(W + '/npz/%s.npz' % bid)['v']; f = F
    else:
        z = np.load(REGS[bid]['meas'] + '_r6.npz', allow_pickle=True); P = z['V']; keep = z['keep'].astype(bool); f = z['F'][keep[z['F']].all(1)]
    fn = W + '/rend/_tmp.npz'; np.savez(fn, P=P.astype(np.float32), f=f.astype(np.int32))
    subprocess.run(['python3', RC], env=dict(os.environ, VIEWS=VIEWS, NPZ=fn, TAG=tag, RES='700'), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return tag
def sheet(name, items, title):
    rows = []
    for bid, lab in items:
        tag = render(bid); ims = [Image.open('%s_%s.png' % (tag, v)).convert('RGBA') for v in ('front', 'profile', 'rear34')]
        w, h = ims[0].size; row = Image.new('RGB', (w * 3, h + 30), 'white')
        for i, im in enumerate(ims): bg = Image.new('RGB', im.size, 'white'); bg.paste(im, mask=im.split()[3]); row.paste(bg, (i * w, 30))
        d = ImageDraw.Draw(row); d.text((8, 8), lab, fill='black')
        for i in range(3):
            for cm in range(0, 301, 50):       # ortho scale 300 cm over the frame height: ground grid every 50 cm
                y = 30 + h - int((cm - (110 - 150)) / 300 * h)
                if 30 <= y < h + 30: d.line([(i * w, y), (i * w + 8, y)], fill=(200, 0, 0)); d.text((i * w + 10, y - 6), str(cm), fill=(200, 0, 0))
        rows.append(row)
    W_ = rows[0].size[0]; out = Image.new('RGB', (W_, sum(r.size[1] for r in rows) + 40), 'white'); ImageDraw.Draw(out).text((8, 12), title, fill='black'); y = 40
    for r in rows: out.paste(r, (0, y)); y += r.size[1]
    out.save(W + '/sheets/' + name, quality=88); print('saved', name)
if __name__ == '__main__':
    sheet('sa_statures_168_188_203_208.jpg', [('SA-M168', 'Saurin male centre 168 cm (regional route)'), ('SA-M188', 'SA-M 188 cm (frozen aff1b52)'), ('SA-M203', 'Saurin 203 cm'), ('SA-M208', 'Saurin 208 cm')], 'W2I Saurin stature family (tail excluded from standing height)')
    sheet('sa_female_centre.jpg', [('SA-F168', 'female centre 168 cm'), ('SA-F188', 'SA-F female centre 188 cm (§263)'), ('SA-F208', 'female centre 208 cm'), ('SA-M188', 'male centre 188 cm')], 'W2I Saurin §263 female centre vs male centre')
    sheet('sa_lower_trunk_floor.jpg', [('SA-M168-LT90', 'Saurin 168 cm at the -10 % lower-trunk bound'), ('MF168', 'Marchfolk 168 cm'), ('SA-M203-LT90', 'Saurin 203 cm at the -10 % lower-trunk bound'), ('MF203', 'Marchfolk 203 cm')], 'W2I lower-trunk floor (AD-R36)')
    sheet('sa_frames.jpg', [('SA-M188-N', 'Narrow 188'), ('SA-M188', 'Balanced 188'), ('SA-M188-B', 'Broad 188'), ('SA-M208-B', 'Broad 208')], 'W2I Saurin frames (breadth only; axial lengths, skull, pelvic depth and tail unchanged)')
    sheet('sa_composition.jpg', [('SA-M188-MIN', 'low muscle + low fat'), ('SA-M188', 'reference composition'), ('SA-M188-MUFAHI', 'high muscle + high fat'), ('SA-M208-B-MUHI', 'Broad + high muscle 208')], 'W2I Saurin composition firewall')
    sheet('sa_tails.jpg', [('SA-M188-T55', 'tail 55 % H (coupled base)'), ('SA-M188', 'tail 64.6 % H (reference)'), ('SA-M188-T78', 'Balanced 78 % (RM-UB-04 anchor)'), ('SA-M188-B-T80', 'Broad 80 % (anchor)'), ('SA-M188-N-FAHI-T72', 'Narrow + high fat 72 % (anchor)')], 'W2I tail family / RM-UB-04 anchors')
    sheet('sa_vs_gorrund_208.jpg', [('SA-M208-B', 'Broad Saurin 208'), ('SA-M208-B-MUHI', 'Broad + high-muscle Saurin 208'), ('GO208', 'Gorrund 208 (W2D)')], 'W2I never-Gorrund context at 208 cm')
    sheet('sa_vs_humans_elves_190.jpg', [('SA-M188', 'Saurin 188'), ('MF190', 'Marchfolk 190'), ('SG190', 'Sagekin 190'), ('AE190', 'Aelari 190'), ('VA190', 'Vael 190'), ('HV190', 'Halvren 190')], 'W2I matched-height context (~190 cm)')
