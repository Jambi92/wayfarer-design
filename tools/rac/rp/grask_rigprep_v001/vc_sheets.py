# vc_sheets.py WORKDIR BASEDIR HELPERDIR : Track E visual evidence (order 69f2660 §11). Identical cameras per side and pose.
#  E_elbow_{l,r}_{120,130}.jpg : W0 / C2 (C2rx right) / H2 / VC3, LBS, inner crease / outer / three-quarter (clay + IDs) + inner-crease wire close-up
#  E_sections.jpg              : flexion-plane sections at 120 / 130, both sides, W0 vs C2|C2rx vs H2 vs VC3 (thick = faces in an intersection pair)
#  E_strain_{l,r}.jpg          : per-face max edge strain maps at 130 (and 120) for C2|C2rx / H2 / VC3, same colour scale (0 .. 150 %)
#  E_field.jpg                 : VC3 posed displacement |X_VC3 - X_W0| at 120 / 130 + support mask (corrective support, exact-zero guard, volume band)
#  E_plots.jpg                 : closed-volume change vs W0, zone proxy, loop spacing, p95 / max strain per angle, W0 / C2 / H2 / VC1-VC3, both sides
import sys, os, json, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '/tmp/claude-0/rt')
from common import PARTS
from diag_lib import bl_to_src
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
W, BD, HD = sys.argv[1:4]; T = os.path.dirname(os.path.abspath(__file__)); BP = os.environ.get('BP', '/home/claude/stc/bin/python3')
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FN = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; f = lambda n, b=False: ImageFont.truetype(FB if b else FN, n)
Z = np.load('/tmp/claude-0/rt/frz/v003_frz.npz'); V0 = Z['V'].astype(float); Q = np.asarray(Z['Q']); FP = Z['FP']
OV = W + '/ov'; SH = W + '/sheets'; os.makedirs(OV, exist_ok=True); os.makedirs(SH, exist_ok=True)
CLAY = np.array([0.80, 0.77, 0.73])
COLS = {'non-contact intersection': (0.9, 0.05, 0.05), 'crease intersection': (1.0, 0.55, 0.0), 'fold (dihedral > 120 deg)': (0.55, 0.0, 0.75),
        'skinned-reference-normal orientation disagreement': (0.95, 0.2, 0.75), 'local fold/inversion indicator': (0.0, 0.75, 0.85), 'compressed loop (< 50 %)': (0.1, 0.25, 0.95)}
rig = json.load(open('/tmp/claude-0/rt/rd/rig/rig_v001.json')); B = {b['name']: b for b in rig['bones']}
piv = lambda s: bl_to_src(np.array(B['forearm_' + s]['head'])[None])[0]
armf = lambda s: np.isin(FP, [PARTS.index('arm_' + s), PARTS.index('hand_' + s)])
REF = {'l': 'C2', 'r': 'C2rx'}; VCT = {'l': 'VC3', 'r': 'VC3r'}
def tag(s, n): return {'VC3': VCT[s], 'VC1': 'VC1' if s == 'l' else 'VC1r', 'VC2': 'VC2' if s == 'l' else 'VC2r'}.get(n, n)
def base(n): return BD if n in ('W0', 'C2', 'C2rx') else (HD if n == 'H2' else W)
def path(s, n, kind, p): return '%s/diag/%s/%s_c_%s_%s.npz' % (base(n), kind, p, s, tag(s, n))
def res(s, n, p): return json.load(open('%s/diag/diag_results_c_%s_%s.json' % (base(n), s, tag(s, n))))['results'][p]
def colours(ids):
    c = np.tile(CLAY, (len(Q), 1)); prs = ids['pairs']; pc = ids['pair_class']; lv = ids['compressed_loop_vertices']
    if len(lv): c[np.isin(Q, lv).any(1)] = COLS['compressed loop (< 50 %)']
    c[ids['orientation_fail_faces']] = COLS['skinned-reference-normal orientation disagreement']; c[ids['inversion_faces']] = COLS['local fold/inversion indicator']
    if len(ids['fold_faces']): c[ids['fold_faces'].ravel()] = COLS['fold (dihedral > 120 deg)']
    for code, nm in ((1, 'crease intersection'), (0, 'non-contact intersection')):
        if len(prs): c[prs[pc == code].ravel()] = COLS[nm]
    return c
def render(V, Qs, col, tg, vs, wire, px=520):
    o = OV + '/%s.npz' % tg
    if not os.path.exists(OV + '/%s_%s.png' % (tg, vs.split(';')[-1].split(':')[0])):
        np.savez(o, V=V, Q=Qs); np.save(o[:-4] + '_c.npy', col.astype(np.float32))
        subprocess.run([BP, T + '/render_attr.py', '--', o, o[:-4] + '_c.npy', OV, tg, vs, wire, str(px)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, env=dict(os.environ, WIRE_T='0.00025'))
def frame(V, s):
    e = piv(s); d = np.linalg.norm(V0 - e, axis=1); arm = FP == PARTS.index('arm_' + s); vv = np.zeros(len(V0), bool); vv[Q[arm].ravel()] = True
    c = V[vv & (d < 5.5)].mean(0); up = V[vv & (d > 10) & (d < 16) & (V0[:, 2] > e[2])].mean(0); lo = V[vv & (d > 10) & (d < 16) & (V0[:, 2] < e[2])].mean(0)
    n = np.cross(up - c, lo - c); n /= np.linalg.norm(n); inner = (up - c) / np.linalg.norm(up - c) + (lo - c) / np.linalg.norm(lo - c); inner /= np.linalg.norm(inner); return c, n, inner
def legend(dr, y, keys):
    x = 10
    for nm in keys:
        cc = COLS[nm]; dr.rectangle([x, y, x + 14, y + 14], fill=tuple(int(255 * v) for v in cc)); dr.text((x + 18, y - 1), nm, fill=(0, 0, 0), font=f(12)); x += 34 + int(dr.textlength(nm, font=f(12)))
def cvol(V):
    T_ = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]; return float(np.einsum('ij,ij->i', V[T_[:, 0]], np.cross(V[T_[:, 1]], V[T_[:, 2]])).sum() / 6)
E = np.unique(np.sort(np.concatenate([Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]]), 1), axis=0); L0 = np.linalg.norm(V0[E[:, 0]] - V0[E[:, 1]], axis=1)
QE = {}
for k in range(4):
    a, b = np.sort(Q[:, [k, (k + 1) % 4]], 1).T; QE[k] = np.searchsorted(E[:, 0] * len(V0) + E[:, 1], a * len(V0) + b)
def face_strain(V):
    st = np.abs(np.linalg.norm(V[E[:, 0]] - V[E[:, 1]], axis=1) / L0 - 1); return np.max(np.stack([st[QE[k]] for k in range(4)]), 0)
def ramp(t):
    t = np.clip(t, 0, 1)[:, None]; return np.where(t < 0.5, (1 - 2 * t) * np.array([0.85, 0.85, 0.85]) + 2 * t * np.array([1.0, 0.75, 0.1]), (2 - 2 * t) * np.array([1.0, 0.75, 0.1]) + (2 * t - 1) * np.array([0.8, 0.0, 0.1]))
SETS = ('W0', 'REF', 'H2', 'VC3'); FR = {}
for s in 'lr':
    for ang in (120, 130):
        p = 'D2_%s_flex%d' % (s, ang); Vw = np.load(path(s, 'W0', 'posed', p))['V'].astype(float); c, n, inner = frame(Vw, s); FR[(s, ang)] = (c, n, inner); tq = inner + n; tq /= np.linalg.norm(tq)
        vs = ';'.join('%s:%s:%s:9' % (nm, ','.join('%.4f' % v for v in dv), ','.join('%.3f' % v for v in c)) for nm, dv in (('in', inner), ('out', -inner), ('tq', tq)))
        vw = 'w:%s:%s:4.5' % (','.join('%.4f' % v for v in inner), ','.join('%.3f' % v for v in (c + inner * 3.0)))
        rows = []; v0 = cvol(Vw)
        for t in SETS:
            t = REF[s] if t == 'REF' else t
            V = np.load(path(s, t, 'posed', p))['V'].astype(float); ids = np.load(path(s, t, 'ids', p)); col = colours(ids)[armf(s)]; Qa = Q[armf(s)]
            render(V, Qa, col, 'e_%s_%s' % (p, tag(s, t)), vs, '0'); render(V, Qa, col, 'ew_%s_%s' % (p, tag(s, t)), vw, '1'); rows.append((t, res(s, t, p), ids, cvol(V) - v0))
            if ang == 130 or t != 'W0':
                fs = face_strain(V)[armf(s)]; render(V, Qa, ramp(fs / 1.5), 'es_%s_%s' % (p, tag(s, t)), vs, '0')
        cell = 300; S = Image.new('RGB', (4 * cell + 470, 96 + 4 * (cell + 6)), (255, 255, 255)); dr = ImageDraw.Draw(S)
        dr.text((10, 8), '%s elbow %d deg (LBS) — W0 / %s / H2 / VC3 (volume-conserving contact redistribution); identical cameras' % ('Left' if s == 'l' else 'Right', ang, REF[s]), fill=(0, 0, 0), font=f(16, True))
        dr.text((10, 32), 'columns: inner crease / outer (olecranon) / three-quarter (clay + IDs) | inner-crease wireframe close-up; arm + hand only', fill=(60, 60, 60), font=f(12))
        legend(dr, 54, list(COLS)[:3]); legend(dr, 74, list(COLS)[3:])
        for i, (t, r, ids, dv) in enumerate(rows):
            y = 96 + i * (cell + 6)
            for j, v in enumerate(('in', 'out', 'tq')): S.paste(Image.open('%s/e_%s_%s_%s.png' % (OV, p, tag(s, t), v)).convert('RGB').resize((cell, cell), Image.LANCZOS), (j * cell, y))
            S.paste(Image.open('%s/ew_%s_%s_w.png' % (OV, p, tag(s, t))).convert('RGB').resize((cell, cell), Image.LANCZOS), (3 * cell, y)); it = r['intersections']
            L = [t, 'non-contact %d | crease %d (%.1f mm)' % (it['non_contact'], it['crease'], it['crease_depth_mm']), 'orientation %d | local fold/inv %d' % (r['flips']['total'], r['inversions']['total']),
                 'folds +%d (outside %d) | loop %.2f' % (r['folds']['new'], r['folds']['outside'], r['loop_spacing_min_ratio']), 'p95 strain %.0f %% (max %.0f %%)' % (r['strain']['zone_p95_pct'], r['strain']['zone_max_pct']),
                 'zone proxy %+.1f %% | closed dV vs W0 %+.0f cm3' % (r['volume']['zone_pct'], dv), 'nc ids %s' % (ids['pairs'][ids['pair_class'] == 0][:2].tolist() if len(ids['pairs']) else []),
                 'inversion faces %s' % ids['inversion_faces'][:4].tolist(), 'T-1 %.4f mm' % r['rest_return_T1_mm']]
            for k, l in enumerate(L): dr.text((4 * cell + 10, y + 6 + 20 * k), l, fill=(150, 20, 20) if k == 0 else (0, 0, 0), font=f(12, k == 0))
        S.save(SH + '/E_elbow_%s_%d.jpg' % (s, ang), quality=85); print('sheet', s, ang, flush=True)
# strain maps
for s in 'lr':
    cell = 280; cols = ['W0', REF[s], 'H2', 'VC3']; S = Image.new('RGB', (3 * cell + 30, 70 + 2 * len(cols) * (cell + 24)), (255, 255, 255)); dr = ImageDraw.Draw(S)
    dr.text((10, 8), '%s elbow: per-face max |edge strain| vs rest (grey 0 %% -> amber 75 %% -> red >= 150 %%), LBS, identical cameras' % ('Left' if s == 'l' else 'Right'), fill=(0, 0, 0), font=f(14, True))
    dr.text((10, 30), 'rows: 130 deg then 120 deg; columns: inner crease / outer / three-quarter. The ~150 %% strip 10-12 cm below the pivot is native W0 LBS (unchanged by every candidate).', fill=(60, 60, 60), font=f(11))
    y = 54
    for ang in (130, 120):
        p = 'D2_%s_flex%d' % (s, ang)
        for t in cols:
            if not os.path.exists('%s/es_%s_%s_in.png' % (OV, p, tag(s, t))): continue
            r = res(s, t, p); dr.text((10, y), '%s %d deg: zone p95 %.0f %%, max %.0f %%' % (t, ang, r['strain']['zone_p95_pct'], r['strain']['zone_max_pct']), fill=(150, 20, 20), font=f(12, True))
            for j, v in enumerate(('in', 'out', 'tq')): S.paste(Image.open('%s/es_%s_%s_%s.png' % (OV, p, tag(s, t), v)).convert('RGB').resize((cell, cell), Image.LANCZOS), (10 + j * cell, y + 18))
            y += cell + 24
    S = S.crop((0, 0, S.width, y + 4)); S.save(SH + '/E_strain_%s.jpg' % s, quality=85); print('strain', s, flush=True)
# sections
fig, axs = plt.subplots(2, 2, figsize=(16, 15)); CC = {'W0': 'k', 'C2': 'tab:red', 'C2rx': 'tab:red', 'H2': 'tab:blue', 'VC3': 'tab:green'}
for i, ang in enumerate((120, 130)):
    for j, s in enumerate('lr'):
        ax = axs[i, j]; c, n, inner = FR[(s, ang)]; e1 = inner; e2 = np.cross(n, inner); p = 'D2_%s_flex%d' % (s, ang); AF = np.nonzero(FP == PARTS.index('arm_' + s))[0]
        for t in ('W0', REF[s], 'H2', 'VC3'):
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
plt.tight_layout(); plt.savefig(SH + '/E_sections.jpg', dpi=70); plt.close(); print('sections', flush=True)
# displacement field + support mask
c2 = lambda t: (lambda u: u * u * u * (u * (6 * u - 15) + 10))(np.clip(t, 0, 1))
cell = 260; S = Image.new('RGB', (4 * cell + 140, 50 + 6 * (cell + 26)), (255, 255, 255)); dr = ImageDraw.Draw(S)
dr.text((10, 8), 'VC3 displacement |X_VC3 - X_W0| (grey 0 -> amber 1.5 cm -> red >= 3 cm, posed) and rest-space support mask', fill=(0, 0, 0), font=f(14, True)); y = 34
for s in 'lr':
    C = np.load('%s/corr/corr_%s.npz' % (W, VCT[s])); CF = json.load(open('%s/cand/VC3_%s.json' % (W, s))); e = piv(s); d = np.linalg.norm(V0 - e, axis=1)
    for ang in (120, 130):
        p = 'D2_%s_flex%d' % (s, ang); Xw = np.load(path(s, 'W0', 'posed', p))['V'].astype(float); Xv = np.load(path(s, 'VC3', 'posed', p))['V'].astype(float)
        dm = np.linalg.norm(Xv - Xw, axis=1); fm = dm[Q].max(1)[armf(s)]; c, n, inner = FR[(s, ang)]; tq = inner + n; tq /= np.linalg.norm(tq)
        vs = ';'.join('%s:%s:%s:11' % (nm, ','.join('%.4f' % v for v in dv), ','.join('%.3f' % v for v in c)) for nm, dv in (('in', inner), ('out', -inner), ('tq', tq)))
        render(Xv, Q[armf(s)], ramp(fm / 3.0), 'ed_%s' % p, vs, '0')
        dr.text((10, y), '%s %d deg: max displacement %.2f cm, vertices moved > 0.1 mm: %d, max |delta| outside arm part: %.3g cm' % (s, ang, dm.max(), int((dm > 1e-2).sum()), dm[~np.isin(np.arange(len(V0)), Q[FP == PARTS.index('arm_' + s)].ravel())].max()), fill=(0, 0, 0), font=f(12))
        for j, v in enumerate(('in', 'out', 'tq')): S.paste(Image.open('%s/ed_%s_%s.png' % (OV, p, v)).convert('RGB').resize((cell, cell), Image.LANCZOS), (10 + j * cell, y + 18))
        y += cell + 26
    sup = np.zeros(len(V0)); sv = np.nonzero(C['support'])[0] if C['support'].dtype == bool else C['support']; sup[sv] = 1.0
    band = c2((d - CF['vol_r_min']) / 1.5) * (1 - c2((d - (CF['vol_r_max'] - 2.0)) / 2.0)) * sup
    col = np.tile(CLAY, (len(V0), 1)); col[sup > 0] = [0.55, 0.75, 0.95]; t = band[:, None]; col = (1 - t) * col + t * np.array([0.1, 0.6, 0.2])
    fc = col[Q].mean(1)[armf(s)]
    vs = 'f:0,1,0:%.3f,%.3f,%.3f:20;b:0,-1,0:%.3f,%.3f,%.3f:20;m:%d,0.2,0:%.3f,%.3f,%.3f:20' % (*e, *e, -1 if s == 'l' else 1, *e)
    render(V0, Q[armf(s)], fc, 'esup_%s' % s, vs, '0')
    dr.text((10, y), '%s rest: light blue = corrective support (%d v, guard %.1f cm + 1.5 cm geodesic seam guard), green = volume-redistribution band (r %.0f-%.0f cm, inner-crease sector excluded < %.0f cm, cos0 %.1f)' % (s, len(sv), CF['guard_cm'], CF['vol_r_min'], CF['vol_r_max'], CF['vol_inner_exclude_rmax'], CF['vol_inner_cos0']), fill=(0, 0, 0), font=f(11))
    for j, v in enumerate(('f', 'b', 'm')): S.paste(Image.open('%s/esup_%s_%s.png' % (OV, s, v)).convert('RGB').resize((cell, cell), Image.LANCZOS), (10 + j * cell, y + 18))
    y += cell + 26
S.save(SH + '/E_field.jpg', quality=85); print('field', flush=True)
# plots
J = json.load(open(W + '/diag/trackE_judgement.json'))['tables']; ANG = [45, 60, 75, 90, 110, 120, 130]
fig, axs = plt.subplots(2, 4, figsize=(20, 8))
for i, s in enumerate('lr'):
    D = J[s]
    for n, st in zip(D, ('k-', 'r-', 'b-', 'y:', 'c--', 'g-')):
        axs[i, 0].plot(ANG, [D[n][str(a)]['vol'] - D['W0'][str(a)]['vol'] for a in ANG], st, marker='.', label=n)
        axs[i, 1].plot(ANG, [D[n][str(a)]['zone'] for a in ANG], st, marker='.', label=n); axs[i, 2].plot(ANG, [D[n][str(a)]['loop'] for a in ANG], st, marker='.', label=n)
        axs[i, 3].plot(ANG, [D[n][str(a)]['p95'] for a in ANG], st, marker='.', label=n + ' p95'); axs[i, 3].plot(ANG, [D[n][str(a)]['smax'] for a in ANG], st, marker='x', alpha=0.4)
    axs[i, 0].set_title('%s: closed-volume change vs W0 (cm3)' % s); axs[i, 1].set_title('%s: zone cone-volume proxy (%%)' % s); axs[i, 2].set_title('%s: loop spacing min ratio' % s); axs[i, 2].axhline(0.5, color='k', lw=0.6, ls='--')
    axs[i, 3].set_title('%s: zone strain p95 (dots) / max (x) %%' % s); axs[i, 3].set_ylim(0, 300)
    for a in axs[i]: a.legend(fontsize=7); a.set_xlabel('flexion (deg)')
plt.tight_layout(); plt.savefig(SH + '/E_plots.jpg', dpi=65); plt.close(); print('plots')
# overlap-aware volume + girth (diag/overlap.json from elbow_overlap_volume.py, diag/girth.json from elbow_girth.py)
OVJ = json.load(open(W + '/diag/overlap.json')); GJ = json.load(open(W + '/diag/girth.json'))
fig, axs = plt.subplots(2, 3, figsize=(19, 9))
for i, s in enumerate('lr'):
    nm = [('W0', 'k'), (REF[s], 'r'), ('H2', 'b'), ('VC3', 'g')]
    for n, c in nm:
        ys = [OVJ['%s_%s_%d' % (n, s, a)] for a in (90, 120, 130)]
        axs[i, 0].plot([90, 120, 130], [y['div_change_vs_base_cm3'] for y in ys], c + '--', marker='o', label=n + ' closed-mesh (divergence)')
        axs[i, 0].plot([90, 120, 130], [y['physical_change_vs_base_cm3'] for y in ys], c + '-', marker='s', label=n + ' physical (overlap removed)')
        axs[i, 1].bar([90 + 2.2 * nm.index((n, c)) - 3, 120 + 2.2 * nm.index((n, c)) - 3, 130 + 2.2 * nm.index((n, c)) - 3], [y['overlap_cm3'] for y in ys], width=2, color=c, label=n)
        g = GJ['%s_%s_130' % (n if n != 'base' else n, s)]; ks = list(g)
        axs[i, 2].plot(range(len(ks)), [g[k]['mean_dr_cm'] for k in ks], c + '-', marker='.', label=n)
    axs[i, 2].set_xticks(range(len(ks))); axs[i, 2].set_xticklabels(ks, rotation=45, fontsize=7); axs[i, 2].axhline(0, color='0.5', lw=0.6)
    axs[i, 0].set_title('%s: volume change vs the straight-elbow base (cm3)' % s); axs[i, 1].set_title('%s: double-covered overlap volume (winding number >= 1.5), cm3' % s)
    axs[i, 2].set_title('%s 130 deg: mean ring radius change vs straight-elbow base (cm)' % s)
    for a in axs[i]: a.legend(fontsize=6)
plt.tight_layout(); plt.savefig(SH + '/E_volume_physical.jpg', dpi=65); plt.close(); print('volume')
