# e2_sheets.py WORKDIR VC3DIR : Track E2 visual evidence (order 28dd8d3 §11), 130 degrees, both sides, VC3 / VC3F1 / VC3F2, identical cameras.
#  E2_closeup_{l,r}.jpg : clay + IDs inner crease / 3-4 contact line / outer, wire close-up, per-face strain (3-4), |X - X_VC3| (3-4), per row
#  E2_support.jpg       : declared interface support (fair_support, rest) per side, front / back / medial
#  E2_sections.jpg      : flexion-plane contact cross-sections VC3 vs F1 vs F2
#  E2_metrics.jpg       : texture (curvature variation, gradient across / along, ripple), physical volume, ring girth
import sys, os, json, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '/tmp/claude-0/rt')
from common import PARTS
from diag_lib import bl_to_src
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
W, V6 = sys.argv[1:3]; T = os.path.dirname(os.path.abspath(__file__)); BP = '/home/claude/stc/bin/python3'
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FN = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; f = lambda n, b=False: ImageFont.truetype(FB if b else FN, n)
Z = np.load('/tmp/claude-0/rt/frz/v003_frz.npz'); V0 = Z['V'].astype(float); Q = np.asarray(Z['Q']); FP = Z['FP']
OV = W + '/ov'; SH = W + '/sheets'; os.makedirs(OV, exist_ok=True); os.makedirs(SH, exist_ok=True)
CLAY = np.array([0.80, 0.77, 0.73]); armf = lambda s: np.isin(FP, [PARTS.index('arm_' + s), PARTS.index('hand_' + s)])
COLS = {'non-contact': (0.9, 0.05, 0.05), 'crease pair': (1.0, 0.55, 0.0), 'orientation disagreement': (0.95, 0.2, 0.75), 'local inversion': (0.0, 0.75, 0.85), 'compressed loop': (0.1, 0.25, 0.95)}
TAGS = {'l': [('VC3', V6, 'VC3'), ('VC3F1', W, 'VC3F1'), ('VC3F2', W, 'VC3F2')], 'r': [('VC3', V6, 'VC3r'), ('VC3F1', W, 'VC3F1r'), ('VC3F2', W, 'VC3F2r')]}
E = np.unique(np.sort(np.concatenate([Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]]), 1), axis=0); L0 = np.linalg.norm(V0[E[:, 0]] - V0[E[:, 1]], axis=1)
QE = [np.searchsorted(E[:, 0] * len(V0) + E[:, 1], (lambda ab: ab[0] * len(V0) + ab[1])(np.sort(Q[:, [k, (k + 1) % 4]], 1).T)) for k in range(4)]
def fstrain(V): st = np.abs(np.linalg.norm(V[E[:, 0]] - V[E[:, 1]], axis=1) / L0 - 1); return np.max(np.stack([st[q] for q in QE]), 0)
def ramp(t):
    t = np.clip(t, 0, 1)[:, None]; return np.where(t < 0.5, (1 - 2 * t) * np.array([0.85, 0.85, 0.85]) + 2 * t * np.array([1.0, 0.75, 0.1]), (2 - 2 * t) * np.array([1.0, 0.75, 0.1]) + (2 * t - 1) * np.array([0.8, 0.0, 0.1]))
def ids_col(ids):
    c = np.tile(CLAY, (len(Q), 1)); lv = ids['compressed_loop_vertices']
    if len(lv): c[np.isin(Q, lv).any(1)] = COLS['compressed loop']
    c[ids['orientation_fail_faces']] = COLS['orientation disagreement']; c[ids['inversion_faces']] = COLS['local inversion']
    prs = ids['pairs']; pc = ids['pair_class']
    for code, nm in ((1, 'crease pair'), (0, 'non-contact')):
        if len(prs): c[prs[pc == code].ravel()] = COLS[nm]
    return c
def render(V, Qs, col, tg, vs, wire, px=480):
    o = OV + '/%s.npz' % tg
    if not os.path.exists(OV + '/%s_%s.png' % (tg, vs.split(';')[-1].split(':')[0])):
        np.savez(o, V=V, Q=Qs); np.save(o[:-4] + '_c.npy', col.astype(np.float32))
        subprocess.run([BP, T + '/render_attr.py', '--', o, o[:-4] + '_c.npy', OV, tg, vs, wire, str(px)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, env=dict(os.environ, WIRE_T='0.00025'))
for s in 'lr':
    cams = {v: json.load(open('%s/ov/e_D2_%s_flex130_W0_%s.json' % (V6, s, v))) for v in ('in', 'tq', 'out')}
    vs = ';'.join('%s:%s:%s:7' % (v, ','.join('%.4f' % x for x in J['d']), ','.join('%.3f' % x for x in J['c'])) for v, J in cams.items())
    J = cams['tq']; vtq = 'tq:%s:%s:7' % (','.join('%.4f' % x for x in J['d']), ','.join('%.3f' % x for x in J['c'])); vw = 'w:%s:%s:4.5' % (','.join('%.4f' % x for x in J['d']), ','.join('%.3f' % x for x in J['c']))
    Xv = None; rows = []
    for nm, d, tg in TAGS[s]:
        p = 'D2_%s_flex130' % s; V = np.load('%s/diag/posed/%s_c_%s_%s.npz' % (d, p, s, tg))['V'].astype(float); ids = np.load('%s/diag/ids/%s_c_%s_%s.npz' % (d, p, s, tg)); a = armf(s)
        if Xv is None: Xv = V
        render(V, Q[a], ids_col(ids)[a], 'e2_%s' % tg, vs, '0'); render(V, Q[a], ids_col(ids)[a], 'e2w_%s' % tg, vw, '1')
        render(V, Q[a], ramp(fstrain(V)[a] / 1.5), 'e2s_%s' % tg, vtq, '0'); dm = np.linalg.norm(V - Xv, axis=1)[Q].max(1)[a]; render(V, Q[a], ramp(dm / 0.6), 'e2d_%s' % tg, vtq, '0')
        r = json.load(open('%s/diag/diag_results_c_%s_%s.json' % (d, s, tg)))['results'][p]; rows.append((nm, tg, r, ids))
    cell = 250; S = Image.new('RGB', (6 * cell + 330, 100 + 3 * (cell + 6)), (255, 255, 255)); dr = ImageDraw.Draw(S)
    dr.text((10, 8), '%s elbow 130 deg — VC3 vs VC3F1 (interface Taubin fairing) vs VC3F2 (wider band, contact held, guard); identical cameras' % ('Left' if s == 'l' else 'Right'), fill=(0, 0, 0), font=f(15, True))
    dr.text((10, 30), 'columns: inner crease / 3-4 contact line / outer (clay + IDs) | wire close-up | strain (grey 0 -> red >= 150 %) | |X - X_VC3| (grey 0 -> red >= 0.6 cm)', fill=(60, 60, 60), font=f(12))
    x = 10
    for k, c in COLS.items(): dr.rectangle([x, 54, x + 14, 68], fill=tuple(int(255 * v) for v in c)); dr.text((x + 18, 53), k, fill=(0, 0, 0), font=f(12)); x += 40 + int(dr.textlength(k, font=f(12)))
    for i, (nm, tg, r, ids) in enumerate(rows):
        y = 100 + i * (cell + 6)
        for j, v in enumerate(('in', 'tq', 'out')): S.paste(Image.open('%s/e2_%s_%s.png' % (OV, tg, v)).convert('RGB').resize((cell, cell)), (j * cell, y))
        S.paste(Image.open('%s/e2w_%s_w.png' % (OV, tg)).convert('RGB').resize((cell, cell)), (3 * cell, y)); S.paste(Image.open('%s/e2s_%s_tq.png' % (OV, tg)).convert('RGB').resize((cell, cell)), (4 * cell, y))
        S.paste(Image.open('%s/e2d_%s_tq.png' % (OV, tg)).convert('RGB').resize((cell, cell)), (5 * cell, y)); it = r['intersections']
        L = [nm, 'non-contact %d | crease %d (%.1f mm)' % (it['non_contact'], it['crease'], it['crease_depth_mm']), 'orientation %d | local inv %d' % (r['flips']['total'], r['inversions']['total']),
             'folds outside %d | loop %.3f' % (r['folds']['outside'], r['loop_spacing_min_ratio']), 'p95 %.1f %% (max %.0f %%)' % (r['strain']['zone_p95_pct'], r['strain']['zone_max_pct']), 'zone %+.1f %%' % r['volume']['zone_pct'],
             'inversion faces %s' % ids['inversion_faces'][:4].tolist(), 'T-1 %.1e mm' % r['rest_return_T1_mm']]
        for k, l in enumerate(L): dr.text((6 * cell + 10, y + 6 + 20 * k), l, fill=(150, 20, 20) if k == 0 else (0, 0, 0), font=f(12, k == 0))
    S.save(SH + '/E2_closeup_%s.jpg' % s, quality=85); print('closeup', s, flush=True)
# support
cell = 260; S = Image.new('RGB', (3 * cell + 20, 40 + 2 * (cell + 24)), (255, 255, 255)); dr = ImageDraw.Draw(S)
dr.text((10, 8), 'E2 declared interface support (rest v003; blue = fairing weight beta, 1 = full); VC3F2 mask (F1 = narrower 4 cm band)', fill=(0, 0, 0), font=f(13, True))
rig = json.load(open('/tmp/claude-0/rt/rd/rig/rig_v001.json')); B = {b['name']: b for b in rig['bones']}
for i, s in enumerate('lr'):
    b = np.load('%s/corr/corr_%s.npz' % (W, 'VC3F2' if s == 'l' else 'VC3F2r'))['fair_support_' + s]; t = b[Q].mean(1)[:, None]
    col = (1 - t) * CLAY + t * np.array([0.1, 0.35, 0.9]); e = bl_to_src(np.array(B['forearm_' + s]['head'])[None])[0]
    vs = 'f:0,1,0:%.3f,%.3f,%.3f:13;b:0,-1,0:%.3f,%.3f,%.3f:13;m:%d,0.2,0:%.3f,%.3f,%.3f:13' % (*e, *e, -1 if s == 'l' else 1, *e)
    render(V0, Q[armf(s)], col[armf(s)], 'e2sup_%s' % s, vs, '0', 400); y = 30 + i * (cell + 24); dr.text((10, y), '%s: %d support vertices' % (s, int((b > 0).sum())), fill=(0, 0, 0), font=f(12))
    for j, v in enumerate(('f', 'b', 'm')): S.paste(Image.open('%s/e2sup_%s_%s.png' % (OV, s, v)).convert('RGB').resize((cell, cell)), (10 + j * cell, y + 18))
S.save(SH + '/E2_support.jpg', quality=85)
# sections (plane through the posed W0 elbow frame used by the Track E sheets)
fig, axs = plt.subplots(1, 2, figsize=(16, 8)); CC = {'VC3': 'k', 'VC3F1': 'tab:blue', 'VC3F2': 'tab:green'}
for j, s in enumerate('lr'):
    J = json.load(open('%s/ov/e_D2_%s_flex130_W0_in.json' % (V6, s))); c = np.array(J['c']); e1 = np.array(J['d']); n = np.cross(e1, np.array(J['y'])); n /= np.linalg.norm(n); e2 = np.cross(n, e1)
    AF = np.nonzero(FP == PARTS.index('arm_' + s))[0]; ax = axs[j]
    for nm, d, tg in TAGS[s]:
        V = np.load('%s/diag/posed/D2_%s_flex130_c_%s_%s.npz' % (d, s, s, tg))['V'].astype(float); dd = (V - c) @ n; first = True
        for fi in AF[np.linalg.norm(V[Q[AF]].mean(1) - c, axis=1) < 14]:
            q = Q[fi]; pts = []
            for a_, b_ in ((q[0], q[1]), (q[1], q[2]), (q[2], q[3]), (q[3], q[0])):
                if dd[a_] * dd[b_] < 0: tt = dd[a_] / (dd[a_] - dd[b_]); pp = V[a_] + tt * (V[b_] - V[a_]); pts.append(((pp - c) @ e1, (pp - c) @ e2))
            if len(pts) == 2: ax.plot([pts[0][0], pts[1][0]], [pts[0][1], pts[1][1]], color=CC[nm], lw=0.9, label=nm if first else None); first = False
    ax.set_aspect('equal'); ax.set_xlim(-10, 10); ax.set_ylim(-10, 10); ax.legend(fontsize=9); ax.set_title('%s 130 deg contact cross-section (plane through the elbow, normal to the inner-crease view)' % s, fontsize=10)
plt.tight_layout(); plt.savefig(SH + '/E2_sections.jpg', dpi=70); plt.close()
# metrics
TX = json.load(open(W + '/diag/texture.json')); RP = json.load(open(W + '/diag/ripple.json')); OVJ = json.load(open(W + '/diag/overlap.json')); GJ = json.load(open(W + '/diag/girth.json'))
fig, axs = plt.subplots(2, 4, figsize=(22, 9)); NM = ['C2', 'H2', 'VC3', 'F1', 'F2']
for i, s in enumerate('lr'):
    axs[i, 0].bar(NM, [TX['%s_%s' % (n, s)]['curv_var_mean'] for n in NM]); axs[i, 0].set_title('%s: band curvature variation (mean, 1/cm)' % s)
    w = 0.35; xs = np.arange(len(NM)); axs[i, 1].bar(xs - w / 2, [TX['%s_%s' % (n, s)]['grad_across_mean'] for n in NM], w, label='across'); axs[i, 1].bar(xs + w / 2, [TX['%s_%s' % (n, s)]['grad_along_mean'] for n in NM], w, label='along')
    axs[i, 1].set_xticks(xs); axs[i, 1].set_xticklabels(NM); axs[i, 1].legend(); axs[i, 1].set_title('%s: displacement gradient across / along interface' % s)
    n3 = ['C2', 'VC3', 'F1', 'F2']; axs[i, 2].bar(n3, [RP['%s_%s_130' % (n, s)]['ripple_p95_mm'] for n in n3]); axs[i, 2].set_title('%s: ripple p95 (mm)' % s)
    ref = 'C2' if s == 'l' else 'C2rx'; vals = [('W0', OVJ.get('W0_%s_130' % s)), (ref, OVJ.get('%s_%s_130' % (ref, s))), ('H2', OVJ.get('H2_%s_130' % s)), ('VC3', OVJ['VC3_%s_130' % s]), ('F1', OVJ['F1_%s_130' % s]), ('F2', OVJ['F2_%s_130' % s])]
    vals = [(a, b) for a, b in vals if b]; axs[i, 3].bar([a for a, _ in vals], [b['physical_change_vs_base_cm3'] for _, b in vals]); axs[i, 3].set_title('%s: physical volume change vs straight elbow (cm3)' % s)
plt.tight_layout(); plt.savefig(SH + '/E2_metrics.jpg', dpi=60); plt.close()
fig, axs = plt.subplots(1, 2, figsize=(16, 5))
for i, s in enumerate('lr'):
    for n, c in (('C2', 'r'), ('VC3', 'k'), ('F1', 'b'), ('F2', 'g')):
        g = GJ['%s_%s_130' % (n, s)]; ks = list(g); axs[i].plot(range(len(ks)), [g[k]['mean_dr_cm'] for k in ks], c + '-', marker='.', label=n)
    axs[i].axhline(0.35, color='0.6', ls='--', lw=0.8, label='base + 0.35 cm limit'); axs[i].axhline(0, color='0.8', lw=0.6); axs[i].set_xticks(range(len(ks))); axs[i].set_xticklabels(ks, rotation=45); axs[i].legend(fontsize=8)
    axs[i].set_title('%s 130: mean ring radius change vs straight elbow (cm)' % s)
plt.tight_layout(); plt.savefig(SH + '/E2_girth.jpg', dpi=65); plt.close(); print('done')
