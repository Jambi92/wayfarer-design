# stageA_sheets.py WORKDIR BASEDIR : Stage A visual evidence (order 8e5021d §8). Identical cameras per side and pose.
#  A_elbow_{l,r}_{90,130}.jpg : W0 / C2 (C2rx right) / H2 (best helper candidate), LBS, inner crease / outer / three-quarter + wire close-up, IDs overlaid
#  A_sections.jpg             : flexion-plane sections at 90 / 130, both sides, W0 vs C2|C2rx vs H2, intersecting faces thick
#  A_helper_field.jpg         : helper share of the W0 forearm weight (rest, both sides) + activation / scale curve
#  A_plots.jpg                : closed-volume change vs W0, zone proxy, loop spacing, p95 / max strain per angle, all candidates, both sides
import sys, os, json, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '/tmp/claude-0/rt')
from common import PARTS
from diag_lib import bl_to_src
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
W, BD = sys.argv[1:3]; T = os.path.dirname(os.path.abspath(__file__)); BP = os.environ.get('BP', '/home/claude/stc/bin/python3')
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FN = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; f = lambda n, b=False: ImageFont.truetype(FB if b else FN, n)
Z = np.load('/tmp/claude-0/rt/frz/v003_frz.npz'); V0 = Z['V'].astype(float); Q = np.asarray(Z['Q']); FP = Z['FP']
OV = W + '/ov'; SH = W + '/sheets'; os.makedirs(OV, exist_ok=True); os.makedirs(SH, exist_ok=True)
CLAY = np.array([0.80, 0.77, 0.73])
COLS = {'non-contact intersection': (0.9, 0.05, 0.05), 'crease intersection': (1.0, 0.55, 0.0), 'fold (dihedral > 120 deg)': (0.55, 0.0, 0.75),
        'skinned-reference-normal orientation disagreement': (0.95, 0.2, 0.75), 'local fold/inversion indicator': (0.0, 0.75, 0.85), 'compressed loop (< 50 %)': (0.1, 0.25, 0.95)}
rig = json.load(open('/tmp/claude-0/rt/rd/rig/rig_v001.json')); B = {b['name']: b for b in rig['bones']}
piv = lambda s: bl_to_src(np.array(B['forearm_' + s]['head'])[None])[0]
armf = lambda s: np.isin(FP, [PARTS.index('arm_' + s), PARTS.index('hand_' + s)])
REF = {'l': 'C2', 'r': 'C2rx'}
def path(s, t, kind, p):
    d = BD if t in ('W0', 'C2', 'C2rx') else W
    return '%s/diag/%s/%s_c_%s_%s.npz' % (d, kind, p, s, t)
def res(s, t, p):
    d = BD if t in ('W0', 'C2', 'C2rx') else W
    return json.load(open('%s/diag/diag_results_c_%s_%s.json' % (d, s, t)))['results'][p]
def colours(ids):
    c = np.tile(CLAY, (len(Q), 1)); prs = ids['pairs']; pc = ids['pair_class']; lv = ids['compressed_loop_vertices']
    if len(lv): c[np.isin(Q, lv).any(1)] = COLS['compressed loop (< 50 %)']
    c[ids['orientation_fail_faces']] = COLS['skinned-reference-normal orientation disagreement']; c[ids['inversion_faces']] = COLS['local fold/inversion indicator']
    if len(ids['fold_faces']): c[ids['fold_faces'].ravel()] = COLS['fold (dihedral > 120 deg)']
    for code, nm in ((1, 'crease intersection'), (0, 'non-contact intersection')):
        if len(prs): c[prs[pc == code].ravel()] = COLS[nm]
    return c
def render(V, Qs, col, tag, vs, wire, px=520):
    o = OV + '/%s.npz' % tag
    if not os.path.exists(OV + '/%s_%s.png' % (tag, vs.split(';')[-1].split(':')[0])):
        np.savez(o, V=V, Q=Qs); np.save(o[:-4] + '_c.npy', col.astype(np.float32))
        subprocess.run([BP, T + '/render_attr.py', '--', o, o[:-4] + '_c.npy', OV, tag, vs, wire, str(px)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, env=dict(os.environ, WIRE_T='0.00025'))
def frame(V, s):
    e = piv(s); d = np.linalg.norm(V0 - e, axis=1); arm = FP == PARTS.index('arm_' + s); vv = np.zeros(len(V0), bool); vv[Q[arm].ravel()] = True
    c = V[vv & (d < 5.5)].mean(0); up = V[vv & (d > 10) & (d < 16) & (V0[:, 2] > e[2])].mean(0); lo = V[vv & (d > 10) & (d < 16) & (V0[:, 2] < e[2])].mean(0)
    n = np.cross(up - c, lo - c); n /= np.linalg.norm(n); inner = (up - c) / np.linalg.norm(up - c) + (lo - c) / np.linalg.norm(lo - c); inner /= np.linalg.norm(inner); return c, n, inner
def legend(dr, y, keys):
    x = 10
    for nm in keys:
        cc = COLS[nm]; dr.rectangle([x, y, x + 14, y + 14], fill=tuple(int(255 * v) for v in cc)); dr.text((x + 18, y - 1), nm, fill=(0, 0, 0), font=f(12)); x += 34 + int(dr.textlength(nm, font=f(12)))
FR = {}
Zq = np.load('/tmp/claude-0/rt/frz/v003_frz.npz')
def cvol(V):
    T_ = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]; return float(np.einsum('ij,ij->i', V[T_[:, 0]], np.cross(V[T_[:, 1]], V[T_[:, 2]])).sum() / 6)
for s in 'lr':
    for ang in (90, 130):
        p = 'D2_%s_flex%d' % (s, ang); Vw = np.load(path(s, 'W0', 'posed', p))['V'].astype(float); c, n, inner = frame(Vw, s); FR[(s, ang)] = (c, n, inner); tq = inner + n; tq /= np.linalg.norm(tq)
        vs = ';'.join('%s:%s:%s:9' % (nm, ','.join('%.4f' % v for v in dv), ','.join('%.3f' % v for v in c)) for nm, dv in (('in', inner), ('out', -inner), ('tq', tq)))
        vw = 'w:%s:%s:4.5' % (','.join('%.4f' % v for v in inner), ','.join('%.3f' % v for v in (c + inner * 3.0)))
        rows = []; v0 = cvol(Vw)
        for t in ('W0', REF[s], 'H2'):
            V = np.load(path(s, t, 'posed', p))['V'].astype(float); ids = np.load(path(s, t, 'ids', p)); col = colours(ids)[armf(s)]; Qa = Q[armf(s)]
            render(V, Qa, col, 'a_%s_%s' % (p, t), vs, '0'); render(V, Qa, col, 'aw_%s_%s' % (p, t), vw, '1'); rows.append((t, res(s, t, p), ids, cvol(V) - v0))
        cell = 300; S = Image.new('RGB', (4 * cell + 470, 96 + 3 * (cell + 6)), (255, 255, 255)); dr = ImageDraw.Draw(S)
        dr.text((10, 8), '%s elbow %d deg (LBS) — W0 / %s / H2 (helper scale bulge + reduced C2-style corrective); identical cameras' % ('Left' if s == 'l' else 'Right', ang, REF[s]), fill=(0, 0, 0), font=f(16, True))
        dr.text((10, 32), 'columns: inner crease / outer (olecranon) / three-quarter (clay + IDs) | inner-crease wireframe close-up; arm + hand only', fill=(60, 60, 60), font=f(12))
        legend(dr, 54, list(COLS)[:3]); legend(dr, 74, list(COLS)[3:])
        for i, (t, r, ids, dv) in enumerate(rows):
            y = 96 + i * (cell + 6)
            for j, v in enumerate(('in', 'out', 'tq')): S.paste(Image.open('%s/a_%s_%s_%s.png' % (OV, p, t, v)).convert('RGB').resize((cell, cell), Image.LANCZOS), (j * cell, y))
            S.paste(Image.open('%s/aw_%s_%s_w.png' % (OV, p, t)).convert('RGB').resize((cell, cell), Image.LANCZOS), (3 * cell, y)); it = r['intersections']
            L = [t, 'non-contact %d | crease %d (%.1f mm)' % (it['non_contact'], it['crease'], it['crease_depth_mm']), 'orientation %d | local fold/inv %d' % (r['flips']['total'], r['inversions']['total']),
                 'folds +%d (outside %d) | loop %.2f' % (r['folds']['new'], r['folds']['outside'], r['loop_spacing_min_ratio']), 'p95 strain %.0f %% (max %.0f %%)' % (r['strain']['zone_p95_pct'], r['strain']['zone_max_pct']),
                 'zone proxy %+.1f %% | closed dV vs W0 %+.0f cm3' % (r['volume']['zone_pct'], dv), 'nc ids %s' % (ids['pairs'][ids['pair_class'] == 0][:2].tolist() if len(ids['pairs']) else []),
                 'inversion faces %s' % ids['inversion_faces'][:4].tolist(), 'T-1 %.4f mm' % r['rest_return_T1_mm']]
            for k, l in enumerate(L): dr.text((4 * cell + 10, y + 6 + 20 * k), l, fill=(150, 20, 20) if k == 0 else (0, 0, 0), font=f(12, k == 0))
        S.save(SH + '/A_elbow_%s_%d.jpg' % (s, ang), quality=85); print('sheet', s, ang, flush=True)
# sections
fig, axs = plt.subplots(2, 2, figsize=(16, 15)); CC = {'W0': 'k', 'C2': 'tab:red', 'C2rx': 'tab:red', 'H2': 'tab:blue'}
for i, ang in enumerate((90, 130)):
    for j, s in enumerate('lr'):
        ax = axs[i, j]; c, n, inner = FR[(s, ang)]; e1 = inner; e2 = np.cross(n, inner); p = 'D2_%s_flex%d' % (s, ang); AF = np.nonzero(FP == PARTS.index('arm_' + s))[0]
        for t in ('W0', REF[s], 'H2'):
            V = np.load(path(s, t, 'posed', p))['V'].astype(float); ids = np.load(path(s, t, 'ids', p)); pen = set(ids['pairs'].ravel().tolist()) if len(ids['pairs']) else set()
            near = AF[np.linalg.norm(V[Q[AF]].mean(1) - c, axis=1) < 17]; dd = (V - c) @ n; first = True
            for fi in near:
                q = Q[fi]; pts = []
                for a_, b_ in ((q[0], q[1]), (q[1], q[2]), (q[2], q[3]), (q[3], q[0])):
                    if dd[a_] * dd[b_] < 0: tt = dd[a_] / (dd[a_] - dd[b_]); pp = V[a_] + tt * (V[b_] - V[a_]); pts.append(((pp - c) @ e1, (pp - c) @ e2))
                if len(pts) == 2:
                    ax.plot([pts[0][0], pts[1][0]], [pts[0][1], pts[1][1]], color=CC[t], lw=1.0, label=t if first else None); first = False
                    if fi in pen: ax.plot([pts[0][0], pts[1][0]], [pts[0][1], pts[1][1]], color=CC[t], lw=3.5, alpha=0.35)
        ax.set_aspect('equal'); ax.set_xlim(-12, 14); ax.set_ylim(-16, 16); ax.legend(loc='upper right', fontsize=9)
        ax.set_title('%s %s LBS — flexion-plane section (thick = faces in a BVH intersection pair)\n-x outer (olecranon) contour, +x inner crease / contact' % (p, 'left' if s == 'l' else 'right'), fontsize=10)
plt.tight_layout(); plt.savefig(SH + '/A_sections.jpg', dpi=70); plt.close(); print('sections', flush=True)
# helper field + activation curve
maps = []
for s in 'lr':
    zH = np.load(W + '/H1/weights_H.npz'); nm = [str(x) for x in zH['names']]; h = zH['W'][:, nm.index('elbow_helper_' + s)]; e = piv(s)
    t = np.clip(h / max(h.max(), 1e-9), 0, 1)[:, None]; col = (1 - t) * np.array([0.92, 0.92, 0.92]) + t * np.array([0.1, 0.35, 0.9]); col[h == 0] = CLAY
    vs = 'f:0,1,0:%.3f,%.3f,%.3f:17;b:0,-1,0:%.3f,%.3f,%.3f:17;m:%d,0.2,0:%.3f,%.3f,%.3f:17' % (*e, *e, -1 if s == 'l' else 1, *e)
    render(V0, Q[armf(s)], col.astype(np.float32), 'helper_%s' % s, vs, '0', 420); maps.append(s)
th = np.linspace(0, 150, 301); bt = np.clip((th - 45) / (130 - 45), 0, 1); bt = bt * bt * (3 - 2 * bt)
plt.figure(figsize=(9, 3.2)); plt.plot(th, 1 + 0.15 * bt, label='helper local X scale (H1/H2): 1 + 0.15 beta'); plt.plot(th, bt, '--', label='activation beta = smoothstep(45, 130)')
for a in (45, 60, 75, 90, 110, 120, 130): plt.axvline(a, color='0.85', lw=0.6)
plt.xlabel('forearm flexion (deg)'); plt.legend(fontsize=8); plt.title('Helper activation (0 at <= 45 deg, smooth, returns to 0 on extension)'); plt.tight_layout(); plt.savefig(OV + '/act.png', dpi=75); plt.close()
cell = 260; A = Image.open(OV + '/act.png').convert('RGB'); S = Image.new('RGB', (3 * cell + 20, 60 + 2 * (cell + 26) + A.height + 10), (255, 255, 255)); dr = ImageDraw.Draw(S)
dr.text((10, 8), 'Elbow helper elbow_helper_{l,r}: share of the W0 forearm weight moved to the helper (blue = 1), rest v003, front / back / medial', fill=(0, 0, 0), font=f(14, True))
HL = json.load(open(W + '/H1/helper_log.json'))
for i, s in enumerate(maps):
    y = 36 + i * (cell + 26); dr.text((10, y), '%s: %d vertices, max share %.2f, support <= %.0f cm (left 18 / right 21), seam guard 1.5 cm' % (s, HL['sides'][s]['influence_vertices'], HL['sides'][s]['max_share'], HL['sides'][s]['max_rest_dist_cm']), fill=(0, 0, 0), font=f(12))
    for j, v in enumerate(('f', 'b', 'm')): S.paste(Image.open('%s/helper_%s_%s.png' % (OV, s, v)).convert('RGB').resize((cell, cell), Image.LANCZOS), (10 + j * cell, y + 20))
S.paste(A, (10, 36 + 2 * (cell + 26))); S.save(SH + '/A_helper_field.jpg', quality=85); print('helper field', flush=True)
# plots
J = json.load(open(W + '/diag/stageA_judgement.json'))['tables']; ANG = [45, 60, 75, 90, 110, 120, 130]
fig, axs = plt.subplots(2, 4, figsize=(20, 8))
for i, s in enumerate('lr'):
    D = J[s]
    for n, st in zip(D, ('k-', 'r-', 'g--', 'b-', 'c:')):
        axs[i, 0].plot(ANG, [D[n][str(a)]['vol'] - D['W0'][str(a)]['vol'] for a in ANG], st, marker='.', label=n)
        axs[i, 1].plot(ANG, [D[n][str(a)]['zone'] for a in ANG], st, marker='.', label=n); axs[i, 2].plot(ANG, [D[n][str(a)]['loop'] for a in ANG], st, marker='.', label=n)
        axs[i, 3].plot(ANG, [D[n][str(a)]['p95'] for a in ANG], st, marker='.', label=n + ' p95'); axs[i, 3].plot(ANG, [D[n][str(a)]['smax'] for a in ANG], st, marker='x', alpha=0.4)
    axs[i, 0].set_title('%s: closed-volume change vs W0 (cm3)' % s); axs[i, 1].set_title('%s: zone cone-volume proxy (%%)' % s); axs[i, 2].set_title('%s: loop spacing min ratio' % s); axs[i, 2].axhline(0.5, color='k', lw=0.6, ls='--')
    axs[i, 3].set_title('%s: zone strain p95 (dots) / max (x) %%' % s)
    for a in axs[i]: a.legend(fontsize=7); a.set_xlabel('flexion (deg)')
plt.tight_layout(); plt.savefig(SH + '/A_plots.jpg', dpi=65); plt.close(); print('plots')
