# lf_maps.py WORKDIR : order bd11ab0 §11 field + strain maps, left flex90, identical cameras (3-4 front and the anterior axillary close-up of shoulder_sheets):
#   row 1: strain (per-face max |edge strain|, grey 0 -> red >= 150 %) for W0 / S2 / SW3 / LF1 / LF2
#   row 2: |X - X_SW3| (grey 0 -> red >= 0.5 cm) for LF1 / LF2 on the close-up, plus the LF support beta on the posed SW3 surface (red = 1, support boundary dark)
import sys, os, json, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
W = sys.argv[1]; T = os.path.dirname(os.path.abspath(__file__)); BP = '/home/claude/stc/bin/python3'
fb = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 13); fn = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 11)
Z = np.load('/tmp/claude-0/rt/frz/v003_frz.npz'); V0 = Z['V'].astype(float); Q = np.asarray(Z['Q'])
E = np.unique(np.sort(np.concatenate([Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]]), 1), axis=0); L0 = np.linalg.norm(V0[E[:, 0]] - V0[E[:, 1]], axis=1)
QE = [np.searchsorted(E[:, 0] * len(V0) + E[:, 1], (lambda ab: ab[0] * len(V0) + ab[1])(np.sort(Q[:, [k, (k + 1) % 4]], 1).T)) for k in range(4)]
def ramp(t):
    t = np.clip(t, 0, 1)[:, None]; return np.where(t < 0.5, (1 - 2 * t) * np.array([0.85, 0.85, 0.85]) + 2 * t * np.array([1.0, 0.75, 0.1]), (2 - 2 * t) * np.array([1.0, 0.75, 0.1]) + (2 * t - 1) * np.array([0.8, 0.0, 0.1]))
p = 'D1_l_flex90'; cams = {v: json.load(open('%s/ov/s_%s_W0_%s.json' % (W, p, v))) for v in ('tqf', 'ax')}
vs = ';'.join('%s:%s:%s:%g' % (v, ','.join('%.4f' % x for x in J['d']), ','.join('%.3f' % x for x in J['c']), J['h']) for v, J in cams.items())
def rend(V, col, tg):
    near = np.linalg.norm(V[Q].mean(1) - np.array(cams['tqf']['c']), axis=1) < 48; o = '%s/ov/lfm_%s.npz' % (W, tg)
    if not os.path.exists(o[:-4] + '_ax.png'):
        np.savez(o, V=V, Q=Q[near]); np.save(o[:-4] + '_c.npy', col[near].astype(np.float32))
        subprocess.run([BP, T + '/render_attr.py', '--', o, o[:-4] + '_c.npy', W + '/ov', 'lfm_%s' % tg, vs, '0', '400'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
TG = ['W0', 'S2', 'SW3', 'LF1', 'LF2']; Xs = {t: np.load('%s/diag/posed/%s_s_%s.npz' % (W, p, t))['V'].astype(float) for t in TG}
for t in TG:
    st = np.abs(np.linalg.norm(Xs[t][E[:, 0]] - Xs[t][E[:, 1]], axis=1) / L0 - 1); rend(Xs[t], ramp(np.max(np.stack([st[q] for q in QE]), 0) / 1.5), 'st_' + t)
for t in ('LF1', 'LF2'): rend(Xs[t], ramp(np.linalg.norm(Xs[t] - Xs['SW3'], axis=1)[Q].max(1) / 0.5), 'du_' + t)
beta = np.load(W + '/lf2/lf_key.npz')['beta']; bf = beta[Q].mean(1); col = ramp(bf); col[(beta[Q] > 0).any(1) & (beta[Q] == 0).any(1)] = [0.1, 0.1, 0.1]; rend(Xs['SW3'], col, 'beta')
cell = 230; S = Image.new('RGB', (5 * cell + 20, 60 + 4 * (cell + 22)), (255, 255, 255)); dr = ImageDraw.Draw(S)
dr.text((10, 8), 'Left flex90 — rows 1-2: strain maps (3-4 front / axillary close-up) W0 / S2 / SW3 / LF1 / LF2; rows 3-4: |X - X_SW3| (LF1, LF2) and LF support beta (dark = boundary)', fill=(0, 0, 0), font=fb)
R = {t: json.load(open('%s/diag/diag_results_s_%s.json' % (W, t)))['results'][p] for t in TG}
for j, t in enumerate(TG):
    for i, v in enumerate(('tqf', 'ax')):
        y = 36 + i * (cell + 22); S.paste(Image.open('%s/ov/lfm_st_%s_%s.png' % (W, t, v)).convert('RGB').resize((cell, cell)), (10 + j * cell, y + 18))
        dr.text((12 + j * cell, y), '%s p95 %.0f / max %.0f %%' % (t, R[t]['strain']['zone_p95_pct'], R[t]['strain']['zone_max_pct']), fill=(0, 0, 0), font=fn)
for j, (tg, lab) in enumerate((('du_LF1', 'LF1 |X - X_SW3|'), ('du_LF2', 'LF2 |X - X_SW3|'), ('beta', 'LF support beta'))):
    for i, v in enumerate(('tqf', 'ax')):
        y = 36 + (2 + i) * (cell + 22); S.paste(Image.open('%s/ov/lfm_%s_%s.png' % (W, tg, v)).convert('RGB').resize((cell, cell)), (10 + j * cell, y + 18)); dr.text((12 + j * cell, y), lab, fill=(0, 0, 0), font=fn)
S.save(W + '/sheets/LF_fields_strain.jpg', quality=85); print('done')
