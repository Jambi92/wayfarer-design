# sw_strain.py WORKDIR : Track S2 strain maps (order 28dd8d3 §20): per-face max |edge strain| (grey 0 -> amber 75 % -> red >= 150 %) for W0 / S2 / SW1 / SW2 / SW3
# at abd90 and flex90, both sides, 3-4 front camera of the shoulder sheets (same ov/*.json camera files).
import sys, os, json, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
W = sys.argv[1]; T = os.path.dirname(os.path.abspath(__file__)); BP = '/home/claude/stc/bin/python3'
fb = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 13); fn = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 11)
Z = np.load('/tmp/claude-0/rt/frz/v003_frz.npz'); V0 = Z['V'].astype(float); Q = np.asarray(Z['Q'])
E = np.unique(np.sort(np.concatenate([Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]]), 1), axis=0); L0 = np.linalg.norm(V0[E[:, 0]] - V0[E[:, 1]], axis=1)
QE = [np.searchsorted(E[:, 0] * len(V0) + E[:, 1], (lambda ab: ab[0] * len(V0) + ab[1])(np.sort(Q[:, [k, (k + 1) % 4]], 1).T)) for k in range(4)]
def ramp(t):
    t = np.clip(t, 0, 1)[:, None]; return np.where(t < 0.5, (1 - 2 * t) * np.array([0.85, 0.85, 0.85]) + 2 * t * np.array([1.0, 0.75, 0.1]), (2 - 2 * t) * np.array([1.0, 0.75, 0.1]) + (2 * t - 1) * np.array([0.8, 0.0, 0.1]))
TG = ['W0', 'S2', 'SW1', 'SW2', 'SW3']; cell = 230; rows = [(s, pz) for s in 'lr' for pz in ('abd90', 'flex90')]
S = Image.new('RGB', (len(TG) * cell + 20, 40 + len(rows) * (cell + 22)), (255, 255, 255)); dr = ImageDraw.Draw(S)
dr.text((10, 8), 'Shoulder strain maps (per-face max |edge strain|; grey 0 -> amber 75 % -> red >= 150 %), 3-4 front, columns ' + ' / '.join(TG), fill=(0, 0, 0), font=fb)
for i, (s, pz) in enumerate(rows):
    p = 'D1_%s_%s' % (s, pz); J = json.load(open('%s/ov/s_%s_W0_tqf.json' % (W, p))); vs = 'tqf:%s:%s:%g' % (','.join('%.4f' % x for x in J['d']), ','.join('%.3f' % x for x in J['c']), J['h'])
    for j, t in enumerate(TG):
        V = np.load('%s/diag/posed/%s_s_%s.npz' % (W, p, t))['V'].astype(float); st = np.abs(np.linalg.norm(V[E[:, 0]] - V[E[:, 1]], axis=1) / L0 - 1); fs = np.max(np.stack([st[q] for q in QE]), 0)
        near = np.linalg.norm(V[Q].mean(1) - np.array(J['c']), axis=1) < 48; o = '%s/ov/sst_%s_%s.npz' % (W, p, t)
        if not os.path.exists(o[:-4] + '_tqf.png'):
            np.savez(o, V=V, Q=Q[near]); np.save(o[:-4] + '_c.npy', ramp(fs[near] / 1.5).astype(np.float32))
            subprocess.run([BP, T + '/render_attr.py', '--', o, o[:-4] + '_c.npy', W + '/ov', 'sst_%s_%s' % (p, t), vs, '0', '380'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        y = 40 + i * (cell + 22); S.paste(Image.open('%s/ov/sst_%s_%s_tqf.png' % (W, p, t)).convert('RGB').resize((cell, cell)), (10 + j * cell, y + 18))
        r = json.load(open('%s/diag/diag_results_s_%s.json' % (W, t)))['results'][p]; dr.text((12 + j * cell, y), '%s %s: p95 %.0f / max %.0f %%' % (t, p, r['strain']['zone_p95_pct'], r['strain']['zone_max_pct']), fill=(0, 0, 0), font=fn)
S.save(W + '/sheets/SW_strain.jpg', quality=85); print('strain')
