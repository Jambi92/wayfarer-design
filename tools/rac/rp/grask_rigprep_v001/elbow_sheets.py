# elbow_sheets.py WORKDIR : visual evidence for the nail / elbow isolation cycle (order b303b9e §5), identical cameras per pose.
#  E_failures_{pose}.jpg  : W0 / E1 / E2 under LBS and DQS, clay + failure IDs + support-boundary overlay, and wireframe (D2_l_flex90, D2_l_flex130)
#  E_contour_crease.jpg   : flexion-plane cross-sections at 90 / 130 (outer contour + inner crease, W0 / E1 / E2 overlaid, rest dashed) and
#                           inner-crease close-ups with penetration (intersection faces) and compressed-loop vertices
#  E_weight_maps.jpg      : rest arm: alpha (support + taper band), per-bone delta upperarm_l / forearm_l, total |delta|, per-edge delta change
#  N_nail_fist_pinch.jpg  : fingertip close-ups, W0 / WN / WNcap in D4_l_fist and D5_l_oppose_pinch (clay + wire, nail sets outlined)
import sys, os, json, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '/tmp/claude-0/rt')
from common import PARTS
W = sys.argv[1]; T = os.path.dirname(os.path.abspath(__file__)); BP = os.environ.get('BP', '/home/claude/stc/bin/python3')
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FN = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; f = lambda n, b=False: ImageFont.truetype(FB if b else FN, n)
Z = np.load('/tmp/claude-0/rt/frz/v003_frz.npz'); V0 = Z['V'].astype(float); Q = np.asarray(Z['Q']); FP = Z['FP']
OV = W + '/ov3'; SH = W + '/sheets'; os.makedirs(OV, exist_ok=True); os.makedirs(SH, exist_ok=True)
CLAY = np.array([0.80, 0.77, 0.73])
COLS = {'non-contact intersection': (0.9, 0.05, 0.05), 'crease intersection': (1.0, 0.55, 0.0), 'contact intersection': (0.95, 0.9, 0.1), 'fold (dihedral > 120 deg)': (0.55, 0.0, 0.75),
        'skinned-reference-normal orientation disagreement': (0.95, 0.2, 0.75), 'local fold/inversion indicator': (0.0, 0.75, 0.85), 'compressed loop (< 50 %)': (0.1, 0.25, 0.95),
        'support boundary / taper band edge': (0.0, 0.6, 0.15)}
arm = np.isin(FP, [PARTS.index('arm_l'), PARTS.index('hand_l')]); Qa = Q[arm]
mp = np.load(W + '/w/weights_E1_maps.npz'); SUP = mp['support']; ALPHA = mp['alpha']
rig = json.load(open('/tmp/claude-0/rt/rd/rig/rig_v001.json'))
from diag_lib import bl_to_src
B = {b['name']: b for b in rig['bones']}; EL = bl_to_src(np.array(B['forearm_l']['head'])[None])[0]
DR = np.linalg.norm(V0 - EL, axis=1)
def bandmask():                                                       # faces straddling the support boundary or the core/band boundary
    s = SUP[Qa]; c = (SUP & (DR <= 9.0))[Qa]; return (s.any(1) & ~s.all(1)) | (c.any(1) & ~c.all(1))
BM = bandmask()
def colours(ids, Qs):
    c = np.tile(CLAY, (len(Q), 1)); prs = ids['pairs']; pc = ids['pair_class']; lv = ids['compressed_loop_vertices']
    if len(lv): c[np.isin(Q, lv).any(1)] = COLS['compressed loop (< 50 %)']
    c[ids['orientation_fail_faces']] = COLS['skinned-reference-normal orientation disagreement']; c[ids['inversion_faces']] = COLS['local fold/inversion indicator']
    if len(ids['fold_faces']): c[ids['fold_faces'].ravel()] = COLS['fold (dihedral > 120 deg)']
    for code, nm in ((2, 'contact intersection'), (1, 'crease intersection'), (0, 'non-contact intersection')):
        if len(prs): c[prs[pc == code].ravel()] = COLS[nm]
    return c[arm]
def render(V, Qs, col, tag, vs, wire, px=520):
    o = OV + '/%s.npz' % tag
    if not os.path.exists(OV + '/%s_%s.png' % (tag, vs.split(';')[-1].split(':')[0])):
        np.savez(o, V=V, Q=Qs); np.save(o[:-4] + '_c.npy', col.astype(np.float32))
        subprocess.run([BP, T + '/render_attr.py', '--', o, o[:-4] + '_c.npy', OV, tag, vs, wire, str(px)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, env=dict(os.environ, WIRE_T='0.00025'))
def frame(V):                                                         # posed elbow frame from the posed W0 mesh (identical for all candidates)
    m = SUP & (DR < 5.5); c = V[m].mean(0)
    rest_ax = None
    up = V[SUP & (DR > 10) & (V0[:, 2] > EL[2])].mean(0); lo = V[SUP & (DR > 10) & (V0[:, 2] < EL[2])].mean(0)
    n = np.cross(up - c, lo - c); n /= np.linalg.norm(n); inner = (up - c) / np.linalg.norm(up - c) + (lo - c) / np.linalg.norm(lo - c); inner /= np.linalg.norm(inner)
    return c, n, inner, up, lo
def legend(dr, y, keys):
    x = 10
    for nm in keys:
        cc = COLS[nm]; dr.rectangle([x, y, x + 14, y + 14], fill=tuple(int(255 * v) for v in cc)); dr.text((x + 18, y - 1), nm, fill=(0, 0, 0), font=f(12)); x += 34 + int(dr.textlength(nm, font=f(12)))
CANDS = ('W0', 'E1', 'E2'); FR = {}
for pose in ('D2_l_flex90', 'D2_l_flex130'):
    Vw = np.load('%s/diag/posed/%s_el_lbs_W0.npz' % (W, pose))['V'].astype(float); c, n, inner, up, lo = frame(Vw); FR[pose] = (c, n, inner)
    side = np.cross(n, inner)
    vs = 'in:%s:%s:9;out:%s:%s:9;side:%s:%s:9' % tuple(x for d in (inner, -inner, n) for x in (','.join('%.4f' % v for v in d), ','.join('%.3f' % v for v in c)))
    rows = []
    for m in ('lbs', 'dqs'):
        for cd in CANDS:
            V = np.load('%s/diag/posed/%s_el_%s_%s.npz' % (W, pose, m, cd))['V'].astype(float); ids = np.load('%s/diag/ids/%s_el_%s_%s.npz' % (W, pose, m, cd))
            col = colours(ids, Qa); keep = col.copy(); keep[BM & (col == CLAY).all(1)] = COLS['support boundary / taper band edge']
            render(V, Qa, keep, '%s_%s_%s' % (pose, m, cd), vs, '0'); render(V, Qa, keep, '%s_%s_%s_w' % (pose, m, cd), vs.split(';')[0], '1')
            r = json.load(open('%s/diag/diag_results_el_%s_%s.json' % (W, m, cd)))['results'][pose]; rows.append((m, cd, r, ids))
    cell = 300; S = Image.new('RGB', (4 * cell + 470, 96 + len(rows) * (cell + 6)), (255, 255, 255)); dr = ImageDraw.Draw(S)
    dr.text((10, 8), 'Left elbow %s — W0 baseline vs E1 (uniform taper) vs E2 (crease-biased taper), LBS and DQS with identical arrays; identical cameras; arm/hand crop' % pose, fill=(0, 0, 0), font=f(16, True))
    dr.text((10, 32), 'columns: inner crease / outer (olecranon) / side, clay + failure IDs + support boundary; inner crease wireframe. Orientation = skinned-reference-normal orientation disagreement.', fill=(60, 60, 60), font=f(12))
    legend(dr, 54, list(COLS)[:4]); legend(dr, 74, list(COLS)[4:])
    for i, (m, cd, r, ids) in enumerate(rows):
        y = 96 + i * (cell + 6)
        for j, v in enumerate(('in', 'out', 'side')): S.paste(Image.open('%s/%s_%s_%s_%s.png' % (OV, pose, m, cd, v)).convert('RGB').resize((cell, cell), Image.LANCZOS), (j * cell, y))
        S.paste(Image.open('%s/%s_%s_%s_w_in.png' % (OV, pose, m, cd)).convert('RGB').resize((cell, cell), Image.LANCZOS), (3 * cell, y))
        it = r['intersections']; X = 4 * cell + 10
        L = ['%s  %s' % (cd, m.upper()), 'non-contact %d | crease %d (%.1f mm)' % (it['non_contact'], it['crease'], it['crease_depth_mm']),
             'orientation disagreement %d | local fold/inv %d' % (r['flips']['total'], r['inversions']['total']), 'folds outside crease %d' % r['folds']['outside'],
             'loop min %.2f (%s)' % (r['loop_spacing_min_ratio'], r.get('loop_spacing_worst')), 'p95 strain %.0f %% | cone-volume proxy %+.1f %% (historical)' % (r['strain']['zone_p95_pct'], r['volume']['zone_pct']),
             'non-contact pair ids %s' % (ids['pairs'][ids['pair_class'] == 0][:2].tolist() if len(ids['pairs']) else []), 'orientation face ids %s' % ids['orientation_fail_faces'][:5].tolist(),
             'compressed-loop verts %s' % ids['compressed_loop_vertices'][:5].tolist()]
        for k, l in enumerate(L): dr.text((X, y + 6 + 20 * k), l, fill=(150, 20, 20) if k == 0 else (0, 0, 0), font=f(12, k == 0))
    S.save(SH + '/E_failures_%s.jpg' % pose, quality=85); print('sheet E_failures', pose, flush=True)
# ------------- contour / crease: flexion-plane sections (matplotlib) + crease close-ups
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
def section(V, c, n, e1, e2):
    Qs = Qa; d = (V - c) @ n; segs = []
    for q in Qs:
        pts = []
        for a_, b_ in ((q[0], q[1]), (q[1], q[2]), (q[2], q[3]), (q[3], q[0])):
            if d[a_] * d[b_] < 0: t = d[a_] / (d[a_] - d[b_]); p = V[a_] + t * (V[b_] - V[a_]); pts.append(((p - c) @ e1, (p - c) @ e2))
        if len(pts) == 2: segs.append(pts)
    return segs
fig, axs = plt.subplots(2, 2, figsize=(16, 15)); CC = {'W0': 'k', 'E1': 'tab:blue', 'E2': 'tab:red'}
for i, pose in enumerate(('D2_l_flex90', 'D2_l_flex130')):
    c, n, inner = FR[pose]; e1 = inner; e2 = np.cross(n, inner)
    for j, m in enumerate(('lbs', 'dqs')):
        ax = axs[i, j]
        for cd in CANDS:
            V = np.load('%s/diag/posed/%s_el_%s_%s.npz' % (W, pose, m, cd))['V'].astype(float); near = np.linalg.norm(V - c, axis=1) < 16
            segs = section(np.where(near[:, None], V, c + 1e3), c, n, e1, e2)
            for k, sg in enumerate(segs): ax.plot([sg[0][0], sg[1][0]], [sg[0][1], sg[1][1]], color=CC[cd], lw=1.1 if cd == 'W0' else 0.9, alpha=0.9, label=cd if k == 0 else None)
        ax.set_aspect('equal'); ax.set_xlim(-12, 12); ax.set_ylim(-14, 14); ax.axhline(0, color='0.85', lw=0.5); ax.axvline(0, color='0.85', lw=0.5)
        ax.set_title('%s %s — flexion-plane section through the posed elbow centre\n+x = inner crease side, -x = outer (olecranon) contour; crossing lines = penetration' % (pose, m.upper()), fontsize=10)
        ax.legend(loc='lower left'); ax.set_xlabel('cm (toward inner crease)'); ax.set_ylabel('cm (along flexion plane)')
plt.tight_layout(); plt.savefig(OV + '/sections.png', dpi=80); plt.close()
crows = []
for pose in ('D2_l_flex90', 'D2_l_flex130'):
    c, n, inner = FR[pose]; cc_ = c + inner * 3.5; vs = 'cr:%s:%s:4.5;crs:%s:%s:4.5' % (','.join('%.4f' % v for v in inner), ','.join('%.3f' % v for v in cc_), ','.join('%.4f' % v for v in (inner + 0.8 * n)), ','.join('%.3f' % v for v in cc_))
    for cd in CANDS:
        V = np.load('%s/diag/posed/%s_el_lbs_%s.npz' % (W, pose, cd))['V'].astype(float); ids = np.load('%s/diag/ids/%s_el_lbs_%s.npz' % (W, pose, cd))
        render(V, Qa, colours(ids, Qa), 'cr_%s_%s' % (pose, cd), vs, '1', 480); crows.append((pose, cd))
SEC = Image.open(OV + '/sections.png').convert('RGB'); cell = 250
S = Image.new('RGB', (max(SEC.width, 6 * cell) + 20, 70 + SEC.height + 2 * (cell + 30) + 20), (255, 255, 255)); dr = ImageDraw.Draw(S)
dr.text((10, 8), 'Left elbow outer contour and inner crease at 90 / 130 deg — W0 / E1 / E2 (LBS and DQS sections; LBS crease close-ups with penetration and compressed loops)', fill=(0, 0, 0), font=f(16, True))
legend(dr, 34, list(COLS)[:4]); legend(dr, 52, list(COLS)[4:7]); S.paste(SEC, (10, 70)); y0 = 70 + SEC.height + 10
for k, (pose, cd) in enumerate(crows):
    r_, cI = divmod(k, 3); y = y0 + r_ * (cell + 30)
    for vi, v in enumerate(('cr', 'crs')): S.paste(Image.open('%s/cr_%s_%s_%s.png' % (OV, pose, cd, v)).convert('RGB').resize((cell, cell), Image.LANCZOS), (10 + (cI * 2 + vi) * cell, y + 22))
    dr.text((14 + cI * 2 * cell, y + 2), '%s %s LBS — inner crease (front / oblique), wire' % (pose, cd), fill=(150, 20, 20), font=f(12, True))
S.save(SH + '/E_contour_crease.jpg', quality=85); print('sheet E_contour_crease', flush=True)
# ------------- weight maps (rest)
def ramp(w, lo, hi, neg=False):
    if neg:
        t = np.clip(w / max(abs(lo), abs(hi)), -1, 1)[:, None]; return np.where(t >= 0, (1 - t) * 0.92 + t * np.array([0.85, 0.1, 0.1]), (1 + t) * 0.92 - t * np.array([0.1, 0.25, 0.85]))
    t = np.clip((w - lo) / (hi - lo), 0, 1)[:, None]; return (1 - t) * np.array([0.92, 0.92, 0.92]) + t * np.array([0.85, 0.1, 0.1])
ctr = EL; vsw = 'f:0,1,0:%.3f,%.3f,%.3f:15;b:0,-1,0:%.3f,%.3f,%.3f:15;l:1,0,0:%.3f,%.3f,%.3f:15' % (*ctr, *ctr, *ctr)
z0 = np.load('/tmp/claude-0/rt/rd/rig/weights_v001c.npz'); names = [str(x) for x in z0['names']]; iu, ifo = names.index('upperarm_l'), names.index('forearm_l')
MAPS = [('W0 forearm_l weight', ramp(z0['W'][:, ifo], 0, 1), 'W0f')]
for cd in ('E1', 'E2'):
    mz = np.load(W + '/w/weights_%s_maps.npz' % cd); zc = np.load(W + '/w/weights_%s.npz' % cd)
    if cd == 'E1':
        a = ramp(mz['alpha'], 0, 1); a[~mz['support']] = [0.80, 0.77, 0.73]; bnd = (DR > 9.0) & mz['support']; a[bnd] = a[bnd] * 0.6 + np.array([0.0, 0.6, 0.15]) * 0.4
        MAPS.append(('support alpha (1 core -> 0 band edge); band 9-13 cm tinted green', a, 'alpha'))
    MAPS += [('%s forearm_l weight' % cd, ramp(zc['W'][:, ifo], 0, 1), cd + 'f'), ('%s delta upperarm_l (blue - / red +, +-0.2)' % cd, ramp(mz['dU'], -0.2, 0.2, True), cd + 'dU'),
             ('%s delta forearm_l (+-0.2)' % cd, ramp(mz['dF'], -0.2, 0.2, True), cd + 'dF'), ('%s total |delta| (0..0.2)' % cd, ramp(np.abs(mz['dU']) + np.abs(mz['dF']), 0, 0.2), cd + 'dT')]
    ed = mz['edges']; dv = np.zeros(len(V0)); np.maximum.at(dv, ed[:, 0], mz['edge_delta_change']); np.maximum.at(dv, ed[:, 1], mz['edge_delta_change'])
    MAPS.append(('%s max per-edge change in delta (0..0.08)' % cd, ramp(dv, 0, 0.08), cd + 'dE'))
cell = 250; S = Image.new('RGB', (3 * cell + 470, 50 + len(MAPS) * (cell + 4)), (255, 255, 255)); dr = ImageDraw.Draw(S)
dr.text((10, 10), 'Left-elbow weight maps, rest v003 (front / back / lateral), clay outside the support region', fill=(0, 0, 0), font=f(16, True))
for i, (lab, col, tg) in enumerate(MAPS):
    col = np.asarray(col, float); render(V0, Qa, col, 'wm_' + tg, vsw, '0', 420); y = 46 + i * (cell + 4)
    for j, v in enumerate(('f', 'b', 'l')): S.paste(Image.open('%s/wm_%s_%s.png' % (OV, tg, v)).convert('RGB').resize((cell, cell), Image.LANCZOS), (j * cell, y))
    dr.text((3 * cell + 10, y + 10), lab, fill=(0, 0, 0), font=f(13, True))
    if tg[-2:] in ('dE',):
        lg = json.load(open(W + '/w/weights_%s_log.json' % tg[:2]))['boundary']
        for k, (kk, vv) in enumerate(lg.items()): dr.text((3 * cell + 10, y + 34 + 18 * k), '%s: %s' % (kk, round(vv, 4) if isinstance(vv, float) else vv), fill=(0, 0, 0), font=f(11))
S.save(SH + '/E_weight_maps.jpg', quality=85); print('sheet E_weight_maps', flush=True)
# ------------- nail close-ups in fist / pinch
LM = json.load(open('/tmp/claude-0/rt/rd/out/GR_U_REF_RP2_rigprep_landmarks_v002.json'))['joints']
CAP = json.load(open(W + '/w/weights_WNcap_log.json'))['digits']; PL = json.load(open(W + '/w/weights_WN_log.json'))['digits']
hand = np.isin(FP, [i for i, nn in enumerate(PARTS) if nn.endswith('_l') and nn.startswith(('hand', 'thumb', 'index', 'middle', 'ring', 'pinky'))]); Qh = Q[hand]
rows = []
for pose, digs in (('D4_l_fist', ('index', 'ring')), ('D5_l_oppose_pinch', ('thumb',))):
    Vw = np.load('%s/diag/posed/%s_full_W0.npz' % (W, pose))['V'].astype(float)
    for dg in digs:
        k = dg + '_l'; cap = np.array(CAP[k]['vertex_ids']); pl = np.array(PL[k]['vertex_ids']); ctr = Vw[cap].mean(0)
        P0 = V0[cap] - V0[cap].mean(0); dor0 = np.linalg.svd(P0)[2][2]
        nr = Vw[pl].mean(0) - Vw[np.array(CAP[k]['vertex_ids'])].mean(0)
        # camera: posed dorsal normal of the plate (mean vertex normal direction) and an oblique toward the DIP
        A = Vw[pl] - Vw[pl].mean(0); dn = np.linalg.svd(A)[2][2]; out = Vw[pl].mean(0) - Vw[hand.nonzero()[0][:1]][0]
        if dn @ (Vw[pl].mean(0) - Vw[cap].mean(0) + 1e-6 * dn) < 0: pass
        hv = Vw[np.unique(Q[FP == PARTS.index(k)])]; dn = dn if dn @ (Vw[pl].mean(0) - hv.mean(0)) > 0 else -dn
        tip = np.array(LM['%s_tip_l' % dg]['position_source_frame_cm']); dip = np.array(LM[('%s_dip_l' % dg) if dg != 'thumb' else 'thumb_ip_l']['position_source_frame_cm'])
        vs = 'd:%s:%s:1.6;o:%s:%s:1.6' % (','.join('%.4f' % v for v in dn), ','.join('%.3f' % v for v in ctr), ','.join('%.4f' % v for v in (dn + 0.9 * np.cross(dn, [0, 0, 1]) / max(np.linalg.norm(np.cross(dn, [0, 0, 1])), 1e-6))), ','.join('%.3f' % v for v in ctr))
        for tg in ('W0', 'WN', 'WNcap'):
            V = np.load('%s/diag/posed/%s_full_%s.npz' % (W, pose, tg))['V'].astype(float); ids = np.load('%s/diag/ids/%s_full_%s.npz' % (W, pose, tg))
            col = np.tile(CLAY, (len(Q), 1)); cs = np.zeros(len(V0), int); cs[cap] = 1; cs[pl] = 2; fc = cs[Q]
            col[(fc == 1).all(1)] = [1.0, 0.75, 0.45]; col[(fc == 2).all(1)] = [0.95, 0.5, 0.5]
            col[ids['orientation_fail_faces']] = COLS['skinned-reference-normal orientation disagreement']; col[ids['inversion_faces']] = COLS['local fold/inversion indicator']
            dm = FP == PARTS.index(k)                                   # the digit's own faces only (other digits would occlude in the fist)
            render(V, Q[dm], col[dm], 'nl_%s_%s_%s' % (pose, k, tg), vs, '1', 460)
            ns_ = json.load(open('%s/diag/nailskin_%s.json' % (W, pose)))[tg][k]; rows.append((pose, k, tg, ns_))
cell = 260; S = Image.new('RGB', (6 * cell + 20, 80 + (len(rows) // 3) * (cell + 120)), (255, 255, 255)); dr = ImageDraw.Draw(S)
dr.text((10, 8), 'Nail close-ups, posed: W0 baseline / WN (groove-bounded plate binding) / WNcap (documented cap binding) — dorsal + oblique, wireframe', fill=(0, 0, 0), font=f(16, True))
dr.text((10, 32), 'salmon = WN plate set, orange = rest of the documented cap mask (proximal/lateral fold, groove ring, tip skin); pink = orientation disagreement, cyan = local fold/inversion indicator', fill=(60, 60, 60), font=f(12))
for i in range(0, len(rows), 3):
    y = 56 + (i // 3) * (cell + 120)
    for j in range(3):
        pose, k, tg, ns_ = rows[i + j]
        for vi, v in enumerate(('d', 'o')): S.paste(Image.open('%s/nl_%s_%s_%s_%s.png' % (OV, pose, k, tg, v)).convert('RGB').resize((cell, cell), Image.LANCZOS), (10 + (j * 2 + vi) * cell, y + 20))
        dv = ns_['cap_deviation_from_rigid']; rg = ns_['ring_skin_outside_cap']
        dr.text((12 + j * 2 * cell, y + 2), '%s %s %s' % (pose, k, tg), fill=(150, 20, 20), font=f(12, True))
        for q_, l in enumerate(['cap-mask deviation from rigid (mm): plate %.3f, groove %.3f, fold %.3f' % (dv['plate']['max_mm'], dv['groove_ring']['max_mm'], dv['beyond_groove_fold']['max_mm']),
                                'skin ring outside cap (1 cm): p95 |strain| %.1f %%, max %.1f %%' % (rg['p95_abs_strain_pct'], rg['max_abs_strain_pct']), 'max dihedral change %.1f deg' % rg['max_dihedral_change_deg']]):
            dr.text((12 + j * 2 * cell, y + cell + 26 + 18 * q_), l, fill=(0, 0, 0), font=f(11))
S.save(SH + '/N_nail_fist_pinch.jpg', quality=85); print('sheet N_nail_fist_pinch', flush=True)
