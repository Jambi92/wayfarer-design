# v004_sheets.py WORKDIR : visual evidence for order 6c38d75 (§16), identical cameras per pose.
#  V_elbow_{45,90,130}.jpg : W0 vs selected corrective C2, LBS and DQS; inner crease / outer contour / front three-quarter + wireframe close-up;
#                            intersection / fold / orientation / local-inversion / compressed-loop IDs coloured, support boundary + band edge drawn
#  V_sections.jpg          : flexion-plane cross-sections at 90 / 130 (LBS, DQS), W0 vs C2, inner crease and outer contour marked, penetration
#                            (BVH-intersecting faces cut by the plane) marked
#  V_corrective_field.jpg  : support / core / taper / guard, |delta| per key, delta direction (arrows), per-edge delta gradient (boundary continuity)
#  V_topology_audit.jpg    : rest wire / ring map around elbow_l_21|22 + ring spacing / posed inner-spacing plots
#  V_right_elbow.jpg       : right side W0 vs C2rx at 90 / 130 (LBS)
import sys, os, json, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '/tmp/claude-0/rt')
from common import PARTS
from diag_lib import bl_to_src
W = sys.argv[1]; T = os.path.dirname(os.path.abspath(__file__)); BP = os.environ.get('BP', '/home/claude/stc/bin/python3')
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FN = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; f = lambda n, b=False: ImageFont.truetype(FB if b else FN, n)
Z = np.load('/tmp/claude-0/rt/frz/v003_frz.npz'); V0 = Z['V'].astype(float); Q = np.asarray(Z['Q']); FP = Z['FP']
OV = W + '/ov'; SH = W + '/sheets'; os.makedirs(OV, exist_ok=True); os.makedirs(SH, exist_ok=True)
CLAY = np.array([0.80, 0.77, 0.73])
COLS = {'non-contact intersection': (0.9, 0.05, 0.05), 'crease intersection': (1.0, 0.55, 0.0), 'fold (dihedral > 120 deg)': (0.55, 0.0, 0.75),
        'skinned-reference-normal orientation disagreement': (0.95, 0.2, 0.75), 'local fold/inversion indicator': (0.0, 0.75, 0.85), 'compressed loop (< 50 %)': (0.1, 0.25, 0.95),
        'corrective support boundary / taper band edge': (0.0, 0.6, 0.15)}
rig = json.load(open('/tmp/claude-0/rt/rd/rig/rig_v001.json')); B = {b['name']: b for b in rig['bones']}
def piv(s): return bl_to_src(np.array(B['forearm_' + s]['head'])[None])[0]
def armfaces(s): return np.isin(FP, [PARTS.index('arm_' + s), PARTS.index('hand_' + s)])
CS = {s: np.load('%s/corr/corr_%s.npz' % (W, 'C2' if s == 'l' else 'C2rx')) for s in 'lr'}
CFG = {s: json.load(open('%s/corr/corr_%s_log.json' % (W, 'C2' if s == 'l' else 'C2rx')))['config'] for s in 'lr'}
def colours(ids, s):
    c = np.tile(CLAY, (len(Q), 1)); prs = ids['pairs']; pc = ids['pair_class']; lv = ids['compressed_loop_vertices']
    if len(lv): c[np.isin(Q, lv).any(1)] = COLS['compressed loop (< 50 %)']
    c[ids['orientation_fail_faces']] = COLS['skinned-reference-normal orientation disagreement']; c[ids['inversion_faces']] = COLS['local fold/inversion indicator']
    if len(ids['fold_faces']): c[ids['fold_faces'].ravel()] = COLS['fold (dihedral > 120 deg)']
    for code, nm in ((1, 'crease intersection'), (0, 'non-contact intersection')):
        if len(prs): c[prs[pc == code].ravel()] = COLS[nm]
    sup = CS[s]['support']; d = np.linalg.norm(V0 - piv(s), axis=1); core = sup & (d <= CFG[s]['R_core'])
    bm = (sup[Q].any(1) & ~sup[Q].all(1)) | (core[Q].any(1) & ~core[Q].all(1)); plain = (c == CLAY).all(1); c[bm & plain] = COLS['corrective support boundary / taper band edge']
    return c
def render(V, Qs, col, tag, vs, wire, px=520):
    o = OV + '/%s.npz' % tag
    if not os.path.exists(OV + '/%s_%s.png' % (tag, vs.split(';')[-1].split(':')[0])):
        np.savez(o, V=V, Q=Qs); np.save(o[:-4] + '_c.npy', col.astype(np.float32))
        subprocess.run([BP, T + '/render_attr.py', '--', o, o[:-4] + '_c.npy', OV, tag, vs, wire, str(px)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, env=dict(os.environ, WIRE_T='0.00025'))
def frame(V, s):
    sup = CS[s]['support']; d = np.linalg.norm(V0 - piv(s), axis=1); c = V[sup & (d < 5.5)].mean(0); e = piv(s)
    up = V[sup & (d > 10) & (V0[:, 2] > e[2])].mean(0); lo = V[sup & (d > 10) & (V0[:, 2] < e[2])].mean(0)
    n = np.cross(up - c, lo - c); n /= np.linalg.norm(n); inner = (up - c) / np.linalg.norm(up - c) + (lo - c) / np.linalg.norm(lo - c)
    if np.linalg.norm(inner) < 1e-6: inner = np.cross(n, up - lo)
    inner /= np.linalg.norm(inner); return c, n, inner
def legend(dr, y, keys):
    x = 10
    for nm in keys:
        cc = COLS[nm]; dr.rectangle([x, y, x + 14, y + 14], fill=tuple(int(255 * v) for v in cc)); dr.text((x + 18, y - 1), nm, fill=(0, 0, 0), font=f(12)); x += 34 + int(dr.textlength(nm, font=f(12)))
def res(tag, pose):
    return json.load(open('%s/diag/diag_results_c_%s.json' % (W, tag)))['results'][pose]
# ---------------- elbow sheets (left)
FRAMES = {}
for ang in (45, 90, 130):
    pose = 'D2_l_flex%d' % ang; Vw = np.load('%s/diag/posed/%s_c_l_W0.npz' % (W, pose))['V'].astype(float); c, n, inner = frame(Vw, 'l'); FRAMES[ang] = (c, n, inner)
    tq = inner + n; tq /= np.linalg.norm(tq)
    vs = ';'.join('%s:%s:%s:9' % (nm, ','.join('%.4f' % v for v in dv), ','.join('%.3f' % v for v in c)) for nm, dv in (('in', inner), ('out', -inner), ('tq', tq)))
    vw = 'w:%s:%s:4.5' % (','.join('%.4f' % v for v in inner), ','.join('%.3f' % v for v in (c + inner * 3.0)))
    rows = []
    for m, tags in (('LBS', (('W0', 'l_W0'), ('C2', 'l_C2'))), ('DQS', (('W0', 'dqs_W0'), ('C2', 'dqs_C2')))):
        for nm, tg in tags:
            V = np.load('%s/diag/posed/%s_c_%s.npz' % (W, pose, tg))['V'].astype(float); ids = np.load('%s/diag/ids/%s_c_%s.npz' % (W, pose, tg))
            col = colours(ids, 'l')[armfaces('l')]; Qa = Q[armfaces('l')]
            render(V, Qa, col, 'v4_%s_%s' % (pose, tg), vs, '0'); render(V, Qa, col, 'v4w_%s_%s' % (pose, tg), vw, '1')
            rows.append((m, nm, tg, res(tg, pose), ids))
    cell = 300; S = Image.new('RGB', (4 * cell + 480, 96 + len(rows) * (cell + 6)), (255, 255, 255)); dr = ImageDraw.Draw(S)
    dr.text((10, 8), 'Left elbow %d deg (abd45 shoulder setup) — W0 vs W0 + pose-space corrective C2; LBS and DQS with identical keys / activation; identical cameras' % ang, fill=(0, 0, 0), font=f(16, True))
    dr.text((10, 32), 'columns: inner crease / outer (olecranon) contour / front three-quarter (clay + IDs) | inner-crease wireframe close-up. Arm + hand only.', fill=(60, 60, 60), font=f(12))
    legend(dr, 54, list(COLS)[:4]); legend(dr, 74, list(COLS)[4:])
    for i, (m, nm, tg, r, ids) in enumerate(rows):
        y = 96 + i * (cell + 6)
        for j, v in enumerate(('in', 'out', 'tq')): S.paste(Image.open('%s/v4_%s_%s_%s.png' % (OV, pose, tg, v)).convert('RGB').resize((cell, cell), Image.LANCZOS), (j * cell, y))
        S.paste(Image.open('%s/v4w_%s_%s_w.png' % (OV, pose, tg)).convert('RGB').resize((cell, cell), Image.LANCZOS), (3 * cell, y))
        it = r['intersections']; act = r.get('corrective', {}).get('activation', {}).get('l', {}).get('weights', {})
        L = ['%s  %s%s' % (nm, m, '' if nm == 'W0' else '  activation %s' % {k: round(v, 3) for k, v in act.items()} if act else ''),
             'non-contact %d | crease %d (%.1f mm)' % (it['non_contact'], it['crease'], it['crease_depth_mm']),
             'orientation disagreement %d | local fold/inv %d' % (r['flips']['total'], r['inversions']['total']), 'folds +%d (outside crease %d)' % (r['folds']['new'], r['folds']['outside']),
             'loop min %.2f (%s)' % (r['loop_spacing_min_ratio'], r.get('loop_spacing_worst')), 'p95 strain %.0f %% | cone-volume proxy %+.1f %%' % (r['strain']['zone_p95_pct'], r['volume']['zone_pct']),
             'nc pairs %s' % (ids['pairs'][ids['pair_class'] == 0][:2].tolist() if len(ids['pairs']) else []), 'orientation faces %s' % ids['orientation_fail_faces'][:4].tolist(),
             'inversion faces %s' % ids['inversion_faces'][:4].tolist(), 'rest-return T-1 %.4f mm' % r['rest_return_T1_mm']]
        for k, l in enumerate(L): dr.text((4 * cell + 10, y + 6 + 20 * k), l, fill=(150, 20, 20) if k == 0 else (0, 0, 0), font=f(12, k == 0))
    S.save(SH + '/V_elbow_%d.jpg' % ang, quality=85); print('sheet V_elbow', ang, flush=True)
# ---------------- sections
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
def section(V, c, n, e1, e2, faces):
    d = (V - c) @ n; segs = []; fid = []
    for fi in faces:
        q = Q[fi]; pts = []
        for a_, b_ in ((q[0], q[1]), (q[1], q[2]), (q[2], q[3]), (q[3], q[0])):
            if d[a_] * d[b_] < 0: t = d[a_] / (d[a_] - d[b_]); p = V[a_] + t * (V[b_] - V[a_]); pts.append(((p - c) @ e1, (p - c) @ e2))
        if len(pts) == 2: segs.append(pts); fid.append(fi)
    return segs, fid
fig, axs = plt.subplots(2, 2, figsize=(16, 15)); CC = {'W0': 'k', 'C2': 'tab:red'}
AF = np.nonzero(FP == PARTS.index('arm_l'))[0]
for i, ang in enumerate((90, 130)):
    c, n, inner = FRAMES[ang]; e1 = inner; e2 = np.cross(n, inner); pose = 'D2_l_flex%d' % ang
    for j, (m, tags) in enumerate((('LBS', ('l_W0', 'l_C2')), ('DQS', ('dqs_W0', 'dqs_C2')))):
        ax = axs[i, j]
        for tg in tags:
            V = np.load('%s/diag/posed/%s_c_%s.npz' % (W, pose, tg))['V'].astype(float); ids = np.load('%s/diag/ids/%s_c_%s.npz' % (W, pose, tg))
            near = AF[np.linalg.norm(V[Q[AF]].mean(1) - c, axis=1) < 17]; segs, fid = section(V, c, n, e1, e2, near)
            pen = set(ids['pairs'].ravel().tolist()) if len(ids['pairs']) else set(); nm = 'W0' if tg.endswith('W0') else 'C2'
            for k, (sg, fi) in enumerate(zip(segs, fid)):
                ax.plot([sg[0][0], sg[1][0]], [sg[0][1], sg[1][1]], color=CC[nm], lw=1.0, alpha=0.9, label=nm if k == 0 else None)
                if fi in pen: ax.plot([sg[0][0], sg[1][0]], [sg[0][1], sg[1][1]], color='orange' if nm == 'W0' else 'magenta', lw=3.0, alpha=0.7, label=('%s intersecting faces' % nm) if fi == [x for x in fid if x in pen][0] else None)
        ax.set_aspect('equal'); ax.set_xlim(-12, 14); ax.set_ylim(-16, 16); ax.axhline(0, color='0.85', lw=0.5); ax.axvline(0, color='0.85', lw=0.5)
        ax.annotate('inner crease side', xy=(6, -15), fontsize=10, color='0.3'); ax.annotate('outer (olecranon) contour', xy=(-11.5, -15), fontsize=10, color='0.3')
        ax.set_title('%s %s — flexion-plane section through the posed elbow (W0 frame)\nthick orange / magenta = faces in a BVH intersection pair (W0 / C2)' % (pose, m), fontsize=10)
        ax.legend(loc='upper right', fontsize=9); ax.set_xlabel('cm (toward inner crease)'); ax.set_ylabel('cm (in flexion plane)')
plt.tight_layout(); plt.savefig(SH + '/V_sections.jpg', dpi=70); plt.close(); print('sheet V_sections', flush=True)
# ---------------- corrective field (rest)
C = CS['l']; e = piv('l'); d = np.linalg.norm(V0 - e, axis=1); sup = C['support']; cfg = CFG['l']
vsr = 'f:0,1,0:%.3f,%.3f,%.3f:17;b:0,-1,0:%.3f,%.3f,%.3f:17;m:-1,0.2,0:%.3f,%.3f,%.3f:17' % (*e, *e, *e)
def ramp(w, lo, hi):
    t = np.clip((w - lo) / (hi - lo), 0, 1)[:, None]; return (1 - t) * np.array([0.92, 0.92, 0.92]) + t * np.array([0.85, 0.1, 0.1])
Qa = Q[armfaces('l')]; maps = []
cz = np.tile([0.80, 0.77, 0.73], (len(V0), 1)); cz[sup] = [0.95, 0.75, 0.75]; cz[sup & (d <= cfg['R_core'])] = [0.85, 0.25, 0.25]; g = C['guard']; cz[sup & (g < 1)] = [0.2, 0.6, 0.2]
maps.append(('support: dark red core (<= %.0f cm), pink taper band (to %.0f cm), green = exact-zero guard (radial 1 cm + 1.5 cm from any support boundary incl. part seams)' % (cfg['R_core'], cfg['R_out']), cz, 'sup'))
E = np.unique(np.sort(np.concatenate([Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]]), 1), axis=0); L0 = np.linalg.norm(V0[E[:, 0]] - V0[E[:, 1]], axis=1)
for k in ('K90_l', 'K110_l', 'K130_l'):
    D = C[k]; mag = np.linalg.norm(D, axis=1); maps.append(('%s rest-space |delta| (0 .. %.1f cm)' % (k, max(mag.max(), 0.1)), ramp(mag, 0, max(mag.max(), 0.1)), 'mag_' + k))
    dirc = np.tile([0.92, 0.92, 0.92], (len(V0), 1)); nz = mag > 1e-4; u = np.zeros_like(D); u[nz] = D[nz] / mag[nz, None]
    dirc[nz] = 0.5 + 0.5 * u[nz]; w_ = np.clip(mag / max(mag.max(), 1e-9) * 3, 0, 1)[:, None]; dirc = (1 - w_) * 0.92 + w_ * dirc
    maps.append(('%s delta DIRECTION (RGB = x/left, f/forward, u/up of the unit delta; faded where small)' % k, dirc, 'dir_' + k))
    gr = np.linalg.norm(D[E[:, 0]] - D[E[:, 1]], axis=1) / np.maximum(L0, 1e-9); gv = np.zeros(len(V0)); np.maximum.at(gv, E[:, 0], gr); np.maximum.at(gv, E[:, 1], gr)
    maps.append(('%s per-edge delta gradient |dD|/L (0 .. 1); boundary continuity' % k, ramp(gv, 0, 1.0), 'grad_' + k))
cell = 250; S = Image.new('RGB', (3 * cell + 560, 50 + len(maps) * (cell + 4)), (255, 255, 255)); dr = ImageDraw.Draw(S)
dr.text((10, 10), 'Left-elbow corrective field C2, rest v003 (front / back / medial). Shape-key deltas applied before the armature.', fill=(0, 0, 0), font=f(16, True))
fc = json.load(open('%s/diag/corr_field_C2.json' % W))
for i, (lab, col, tg) in enumerate(maps):
    render(V0, Qa, col[armfaces('l')] if len(col) == len(Q) else col, 'f_' + tg, vsr, '0', 420); y = 46 + i * (cell + 4)
    for j, v in enumerate(('f', 'b', 'm')): S.paste(Image.open('%s/f_%s_%s.png' % (OV, tg, v)).convert('RGB').resize((cell, cell), Image.LANCZOS), (j * cell, y))
    import textwrap
    for q_, l in enumerate(textwrap.wrap(lab, 70)): dr.text((3 * cell + 10, y + 8 + 18 * q_), l, fill=(0, 0, 0), font=f(12, True))
    kk = tg.split('_', 1)[1] if '_' in tg else None
    if kk in fc['keys'] and tg.startswith('grad'):
        st = fc['keys'][kk]
        for q_, l in enumerate(['max |delta| %.3f cm; outside support %.3f; outer 1 cm %.3f' % (st['max_rest_delta_cm'], st['max_delta_outside_support_cm'], st['max_delta_in_outer_band_1cm']),
                                'gradient max core %.3f / band %.3f / boundary edges %.4f' % (st['gradient_max']['core'], st['gradient_max']['band'], st['gradient_max']['boundary_edges']),
                                'gradient p95 core %.3f / band %.3f' % (st['gradient_p95']['core'], st['gradient_p95']['band'])]):
            dr.text((3 * cell + 10, y + 70 + 18 * q_), l, fill=(0, 0, 0), font=f(11))
S.save(SH + '/V_corrective_field.jpg', quality=85); print('sheet V_corrective_field', flush=True)
# ---------------- topology audit
TA = json.load(open(W + '/topo/topology_density_audit.json')); rings = TA['ring_ids']
cmap = np.tile([0.80, 0.77, 0.73], (len(V0), 1)); names = list(rings)
for i, nm in enumerate(names):
    ix = np.array(rings[nm]); cmap[ix] = [0.25, 0.45, 0.9] if i % 2 else [0.35, 0.75, 0.95]
    if nm.startswith('elbow_l_'): cmap[ix] = [0.95, 0.5, 0.0] if nm not in ('elbow_l_21', 'elbow_l_22') else [0.9, 0.05, 0.05]
vt = 'f:0,1,0:%.3f,%.3f,%.3f:9;m:-1,0.3,0:%.3f,%.3f,%.3f:9' % (*e, *e)
render(V0, Qa, cmap, 'topo_rings', vt, '1', 700)
fig, axs = plt.subplots(1, 2, figsize=(15, 5))
Sx = [r['s_cm'] for r in TA['rings'] if 'spacing_to_next_cm' in r]; Sp = [r['spacing_to_next_cm']['mean'] for r in TA['rings'] if 'spacing_to_next_cm' in r]
Si = [r['spacing_to_next_cm']['inner'] for r in TA['rings'] if 'spacing_to_next_cm' in r]; So = [r['spacing_to_next_cm']['outer'] for r in TA['rings'] if 'spacing_to_next_cm' in r]
axs[0].plot(Sx, Sp, 'k.-', label='mean'); axs[0].plot(Sx, Si, 'r.-', lw=0.8, label='inner crease side'); axs[0].plot(Sx, So, 'b.-', lw=0.8, label='outer side')
for r in TA['rings']:
    if r['ring'].startswith('elbow_l_'): axs[0].axvline(r['s_cm'], color='orange' if r['ring'] not in ('elbow_l_21', 'elbow_l_22') else 'red', lw=0.8); axs[0].text(r['s_cm'], 0.62, r['ring'][6:], rotation=90, fontsize=8)
axs[0].set_xlabel('ring centroid position along the elbow axis s (cm; - upper arm, + forearm)'); axs[0].set_ylabel('rest spacing to next ring (cm)'); axs[0].set_title('Rest ring spacing (all rings 120 verts, valence 4, no poles)'); axs[0].legend(fontsize=8)
for tg, col_ in (('D2_l_flex90_el_lbs_W0', 'tab:orange'), ('D2_l_flex130_el_lbs_W0', 'tab:red')):
    pr = TA['posed_inner_spacing'][tg]; axs[1].plot([p['s_cm'] for p in pr], [p['min_ratio'] for p in pr], '.-', color=col_, label=tg.replace('_el_lbs_W0', ' W0 LBS min ratio'))
axs[1].axhline(0.5, color='k', lw=0.6, ls='--'); axs[1].set_xlabel('s (cm)'); axs[1].set_ylabel('posed / rest spacing, ring pair (min over pairs)'); axs[1].set_title('Where LBS compresses: 2-3 rings either side of the pivot'); axs[1].legend(fontsize=8)
plt.tight_layout(); plt.savefig(OV + '/topo_plot.png', dpi=70); plt.close()
P1 = Image.open(OV + '/topo_plot.png').convert('RGB'); S = Image.new('RGB', (max(2 * 520, P1.width) + 20, 60 + 520 + P1.height + 20), (255, 255, 255)); dr = ImageDraw.Draw(S)
dr.text((10, 10), 'Left-elbow topology-density audit (analysis only; frozen v003 unchanged): edge rings (alternating blue), tagged loops orange, elbow_l_21 / 22 red', fill=(0, 0, 0), font=f(15, True))
for j, v in enumerate(('f', 'm')): S.paste(Image.open('%s/topo_rings_%s.png' % (OV, v)).convert('RGB').resize((520, 520), Image.LANCZOS), (10 + j * 520, 40))
S.paste(P1, (10, 570)); S.save(SH + '/V_topology_audit.jpg', quality=85); print('sheet V_topology_audit', flush=True)
# ---------------- right elbow
rows = []
for ang in (90, 130):
    pose = 'D2_r_flex%d' % ang; Vw = np.load('%s/diag/posed/%s_c_r_W0.npz' % (W, pose))['V'].astype(float); c, n, inner = frame(Vw, 'r'); tq = inner + n; tq /= np.linalg.norm(tq)
    vs = ';'.join('%s:%s:%s:9' % (nm, ','.join('%.4f' % v for v in dv), ','.join('%.3f' % v for v in c)) for nm, dv in (('in', inner), ('out', -inner), ('tq', tq)))
    for nm, tg in (('W0', 'r_W0'), ('C2rx', 'r_C2rx')):
        V = np.load('%s/diag/posed/%s_c_%s.npz' % (W, pose, tg))['V'].astype(float); ids = np.load('%s/diag/ids/%s_c_%s.npz' % (W, pose, tg))
        render(V, Q[armfaces('r')], colours(ids, 'r')[armfaces('r')], 'v4r_%s_%s' % (pose, tg), vs, '0'); rows.append((pose, nm, tg, res(tg, pose)))
cell = 300; S = Image.new('RGB', (3 * cell + 460, 80 + len(rows) * (cell + 6)), (255, 255, 255)); dr = ImageDraw.Draw(S)
dr.text((10, 8), 'Right elbow (LBS) — W0 vs right counterpart C2rx (same class, own geometry, support 21 cm); identical cameras per pose', fill=(0, 0, 0), font=f(16, True)); legend(dr, 34, list(COLS)[:4]); legend(dr, 54, list(COLS)[4:])
for i, (pose, nm, tg, r) in enumerate(rows):
    y = 80 + i * (cell + 6)
    for j, v in enumerate(('in', 'out', 'tq')): S.paste(Image.open('%s/v4r_%s_%s_%s.png' % (OV, pose, tg, v)).convert('RGB').resize((cell, cell), Image.LANCZOS), (j * cell, y))
    it = r['intersections']
    for k, l in enumerate(['%s %s' % (pose, nm), 'non-contact %d | crease %d (%.1f mm)' % (it['non_contact'], it['crease'], it['crease_depth_mm']), 'orientation %d | local inv %d' % (r['flips']['total'], r['inversions']['total']),
                           'loop min %.2f | p95 strain %.0f %%' % (r['loop_spacing_min_ratio'], r['strain']['zone_p95_pct']), 'cone-volume proxy %+.1f %%' % r['volume']['zone_pct']]):
        dr.text((3 * cell + 10, y + 6 + 20 * k), l, fill=(150, 20, 20) if k == 0 else (0, 0, 0), font=f(12, k == 0))
S.save(SH + '/V_right_elbow.jpg', quality=85); print('sheet V_right_elbow', flush=True)
