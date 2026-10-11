# RAC RM-UF-05 sheets 1 / 2 / 3 / 6: Skarn diagnostic batches rendered at N4-style neutralization (one grey material, no hair / brows /
# beard / texture, neutral expression, standardized camera; ears visible because ears are not varied in these batches).
import os, sys, json, numpy as np
from PIL import Image, ImageDraw
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(D), 'w3b_drivers')); sys.path.insert(0, os.path.dirname(D))
import w3b_common as C, w3b_sheet as SS, arm_measure as AM
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/rmuf05'; R = S + '/rend'; os.makedirs(R, exist_ok=True)
EV = json.load(open(S + '/eval.json'))
def ensure(bid):
    if all(os.path.exists('%s/%s_%s.png' % (R, bid, n)) for n in 'FP'): return
    d = np.load('%s/b/%s_r6.npz' % (S, bid), allow_pickle=True); V = d['V'].astype(float); F = d['F']; keep = d['keep'].astype(bool)
    c = AM.cranio(d, V, F, keep); e = 0.5 * (d['eye_l'] + d['eye_r']); cu = 0.5 * (c['V'][2] + c['Me'][2]) - 1.5; cf = e[1] - 5
    v = "F:0:0:0:%.2f:%.2f:34;P:90:0:0:%.2f:%.2f:34" % (cf, cu, cf, cu); me = c['Me'][2]
    C.save_head_npz(R + '/%s.npz' % bid, V, F, lambda Q: keep & (Q[:, 2] > me - 6)); C.render(R + '/%s.npz' % bid, R + '/' + bid, v, 500); os.remove(R + '/%s.npz' % bid)
def sheet(out, title, sub, cond, verdict):
    ids = ['SK-%s-%d' % (cond, i) for i in range(8)]; [ensure(b) for b in ids]
    cell = 190; top = 120 + 20 * len(sub); img = Image.new('RGB', (cell * 8 + 20, top + cell * 2 + 60), 'white'); d = ImageDraw.Draw(img)
    d.text((12, 10), title, font=SS.font(22), fill='black')
    for i, s in enumerate(sub): d.text((12, 44 + 20 * i), s, font=SS.font(14), fill=(70, 70, 70))
    for i, b in enumerate(ids):
        for j, n in enumerate('FP'):
            p = '%s/%s_%s.png' % (R, b, n); im = Image.open(p).convert('RGBA').resize((cell, cell), Image.LANCZOS); bg = Image.new('RGB', im.size, 'white'); bg.paste(im, mask=im.split()[3]); img.paste(bg, (10 + i * cell, top + j * cell))
    d.text((12, top + 2 * cell + 14), verdict, font=SS.font(15), fill='black')
    img.save(S + '/sheets/' + out, quality=88); print(out)
def stats(cond):
    r = EV['SK_%s_101' % cond]; cb = r.get('canon_bundle', {})
    return 'D2 NN median %.3f, p5 %.3f, near-clone (<0.015) %.0f %%, min slot coverage %.2f, tuple lift %.1f, Viking-bundle share %.0f %%' % (
        r['D2']['nn_median'], r['D2']['nn_p5'], 100 * r['D2']['frac_nn_below']['0.015'], min(r['slot_coverage'].values()), r['bundle']['lift'], 100 * cb.get('share', 0))
O = json.load(open(S + '/options.json'))
def ov(cond): t = O['SK_%s' % cond]; return 'Options (pass / 4 seeds): A %d, B %d, C %d' % (t['A'], t['B'], t['C'])
L = 'Skarn anchor-scale batch (seed 101, first 8 of N 256) on the accepted SKM190 body. DIAGNOSTIC COVERAGE SAMPLING - NOT POPULATION FREQUENCY.'
sheet('uf05_1_healthy_diverse.jpg', 'RM-UF-05 - healthy diverse batch (broad diagnostic coverage)', [L, 'Front row / profile row. Brow, cheek, nose, jaw, head breadth / depth vary independently inside the W3C / W3D anchor scale.'], 'broad', stats('broad') + '.  ' + ov('broad'))
sheet('uf05_2_near_clone.jpg', 'RM-UF-05 - near-clone failure batch (3 templates + 1 % jitter)', [L, 'The batch collapses to three faces; every option rejects it.'], 'converge', stats('converge') + '.  ' + ov('converge'))
sheet('uf05_3_cliche_bundle.jpg', 'RM-UF-05 - cliche-bundle failure ("mandatory Viking face": heavy brow + square jaw forced)', [L, 'Pairwise distance stays healthy (other regions vary) - only the canon-bundle diagnostic catches it (SKARN L48 / L154; W3C order s5).'], 'cliche', stats('cliche') + '.  ' + ov('cliche'))
sheet('uf05_6_skarn_c1r_central.jpg', 'RM-UF-05 - Skarn C1R central batch (Subtle-like: C1R +-10 % of the anchor span)', [L, 'Central tendency without heavy-brow / square-jaw convergence: Viking-bundle share 0 %. Light-brow / lighter-jaw Skarn stay manually creatable (W3C overlap).'], 'central', stats('central') + '.  ' + ov('central'))
