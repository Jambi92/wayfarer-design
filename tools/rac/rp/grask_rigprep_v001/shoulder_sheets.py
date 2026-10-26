# shoulder_sheets.py WORKDIR : Track S visual package (order 69f2660 §17). Identical cameras per side and pose for W0 / S1 / S2.
#  S_{abd90,flex90}_{l,r}.jpg : front / rear / 3-4 front / 3-4 rear / axillary close-up (clay + IDs + overlays) + anterior-fold wire close-up
#  S_overview_{l,r}.jpg       : every D1 pose (abd45, abd90, flex90, ext30, girdle variants) x W0 / S1 / S2, 3-4 front camera
#  S_sections.jpg             : sagittal section through GH (flex90) and frontal section through GH (abd90), W0 vs S1 vs S2, both sides
# Overlays (small cubes, posed with the bone that carries them): SC yellow, acromion orange, scapular inferior proxy cyan, scapular medial proxy blue,
# GH red; dark green faces = dominant-bone boundary between the girdle bones (upperarm / clavicle / scapula / thoracic-spine) of the weights in use.
import sys, os, json, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '/tmp/claude-0/rt')
from common import PARTS
from diag_lib import Rig, build_poses, bl_to_src, src_to_bl
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
W = sys.argv[1]; T = os.path.dirname(os.path.abspath(__file__)); BP = os.environ.get('BP', '/home/claude/stc/bin/python3')
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FN = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; f = lambda n, b=False: ImageFont.truetype(FB if b else FN, n)
Z = np.load('/tmp/claude-0/rt/frz/v003_frz.npz'); V0 = Z['V'].astype(float); Q = np.asarray(Z['Q']); FP = Z['FP']; nV = len(V0)
OV = W + '/ov'; SH = W + '/sheets'; os.makedirs(OV, exist_ok=True); os.makedirs(SH, exist_ok=True)
RD = '/tmp/claude-0/rt/rd'; LMJ = json.load(open(RD + '/out/GR_U_REF_RP2_rigprep_landmarks_v002.json'))['joints']
CLAY = np.array([0.80, 0.77, 0.73])
COLS = {'non-contact intersection': (0.9, 0.05, 0.05), 'crease intersection': (1.0, 0.55, 0.0), 'contact pair (allowed)': (0.95, 0.85, 0.2), 'fold (dihedral > 120 deg)': (0.55, 0.0, 0.75),
        'orientation disagreement': (0.95, 0.2, 0.75), 'local fold/inversion': (0.0, 0.75, 0.85), 'compressed loop (< 50 %)': (0.1, 0.25, 0.95), 'girdle weight boundary': (0.05, 0.45, 0.15)}
LMC = {'SC': (1.0, 0.9, 0.0), 'acromion': (1.0, 0.5, 0.0), 'scap. inferior': (0.0, 0.85, 0.9), 'scap. medial': (0.1, 0.2, 0.9), 'GH': (0.9, 0.0, 0.0)}
CFGS = {'W0': (RD + '/rig/weights_v001c.npz', None), 'S1': (RD + '/rig/weights_v001c.npz', W + '/s1/pose_S1.json'), 'S2w': (W + '/s2/weights_S2.npz', None), 'S2': (W + '/s2/weights_S2.npz', W + '/s1/pose_S1.json')}
RIGS = {}; POSES = {}
for k, (wf, pj) in CFGS.items():
    RIGS[k] = Rig(RD + '/rig/rig_v001.json', wf)
    if pj: os.environ['POSE_JSON'] = pj
    else: os.environ.pop('POSE_JSON', None)
    POSES[k] = build_poses(RIGS[k])
os.environ.pop('POSE_JSON', None)
def res(t, p): return json.load(open('%s/diag/diag_results_s_%s.json' % (W, t)))['results'][p]
def girdle_boundary(rig, s):
    nm = rig.names; G = [i for i, n in enumerate(nm) if n in ('upperarm_' + s, 'clavicle_' + s, 'scapula_' + s, 'thoracic_01', 'thoracic_02', 'thoracic_03', 'spine_03')]
    Wg = rig.W[:, G]; dom = np.where(Wg.max(1) > 0.05, Wg.argmax(1), -1); fq = dom[Q]; return (fq != fq[:, :1]).any(1) & (fq >= 0).all(1)
def landmarks(t, s, pose):
    M, _ = RIGS[t].pose_mats(pose); out = {}
    rel = lambda bone, p_src: bl_to_src(((M[bone] @ np.linalg.inv(RIGS[t].rest[bone]) @ np.r_[src_to_bl(np.asarray(p_src)[None])[0], 1])[:3])[None])[0]
    out['SC'] = rel('clavicle_' + s, LMJ['sternoclavicular_' + s]['position_source_frame_cm']); out['GH'] = rel('upperarm_' + s, LMJ['glenohumeral_' + s]['position_source_frame_cm'])
    out['acromion'] = rel('scapula_' + s, LMJ['acromion_' + s]['position_source_frame_cm']); out['scap. inferior'] = rel('scapula_' + s, LMJ['scapular_inferior_proxy_' + s]['position_source_frame_cm'])
    out['scap. medial'] = rel('scapula_' + s, LMJ['scapula_medial_proxy_' + s]['position_source_frame_cm']); return out
def cube(c, h=0.7):
    v = np.array([[x, y, z] for x in (-h, h) for y in (-h, h) for z in (-h, h)]) + c
    q = np.array([[0, 1, 3, 2], [4, 6, 7, 5], [0, 4, 5, 1], [2, 3, 7, 6], [0, 2, 6, 4], [1, 5, 7, 3]]); return v, q
def scene(t, s, p, near):
    V = np.load('%s/diag/posed/%s_s_%s.npz' % (W, p, t))['V'].astype(float); ids = np.load('%s/diag/ids/%s_s_%s.npz' % (W, p, t))
    c = np.tile(CLAY, (len(Q), 1)); c[girdle_boundary(RIGS[t], s)] = COLS['girdle weight boundary']
    lv = ids['compressed_loop_vertices']
    if len(lv): c[np.isin(Q, lv).any(1)] = COLS['compressed loop (< 50 %)']
    c[ids['orientation_fail_faces']] = COLS['orientation disagreement']; c[ids['inversion_faces']] = COLS['local fold/inversion']
    if len(ids['fold_faces']): c[ids['fold_faces'].ravel()] = COLS['fold (dihedral > 120 deg)']
    prs = ids['pairs']; pc = ids['pair_class']
    for code, nm in ((2, 'contact pair (allowed)'), (1, 'crease intersection'), (0, 'non-contact intersection')):
        if len(prs): c[prs[pc == code].ravel()] = COLS[nm]
    fm = near(V); Vs = [V]; Qs = [Q[fm]]; Cs = [c[fm]]; off = nV
    for nm, pos in landmarks(t, s, POSES[t][p]).items():
        v, q = cube(pos); Vs.append(v); Qs.append(q + off); Cs.append(np.tile(LMC[nm], (6, 1))); off += 8
    return np.vstack(Vs), np.vstack(Qs), np.vstack(Cs), V, ids
def render(V, Qs, col, tg, vs, wire, px=480):
    o = OV + '/%s.npz' % tg
    if not os.path.exists(OV + '/%s_%s.png' % (tg, vs.split(';')[-1].split(':')[0])):
        np.savez(o, V=V, Q=Qs); np.save(o[:-4] + '_c.npy', col.astype(np.float32))
        subprocess.run([BP, T + '/render_attr.py', '--', o, o[:-4] + '_c.npy', OV, tg, vs, wire, str(px)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, env=dict(os.environ, WIRE_T='0.0003'))
def legend(dr, y, keys, cols, x=10):
    for nm in keys:
        cc = cols[nm]; dr.rectangle([x, y, x + 14, y + 14], fill=tuple(int(255 * v) for v in cc)); dr.text((x + 18, y - 1), nm, fill=(0, 0, 0), font=f(12)); x += 34 + int(dr.textlength(nm, font=f(12)))
def vspec(s, gh, close):
    sg = 1 if s == 'l' else -1; fmt = lambda v: ','.join('%.3f' % x for x in v)
    c = gh + np.array([sg * 2.0, 3.0, -8.0]); ax = gh + np.array([-sg * 1.0, 6.0, -6.0])     # close-ups: the anterior axillary fold (D1 failure site)
    V_ = [('front', (0, 1, 0.15), c, 26), ('rear', (0, -1, 0.15), c, 26), ('tqf', (sg * 0.75, 0.65, 0.2), c, 26), ('tqr', (sg * 0.75, -0.65, 0.2), c, 26), ('ax', (sg * 0.25, 0.75, -0.6), ax, 11)]
    return ';'.join('%s:%s:%s:%g' % (n, fmt(d), fmt(cc), h) for n, d, cc, h in V_), 'w:%s:%s:8' % (fmt((sg * 0.25, 0.75, -0.6)), fmt(ax))
RE = {k: [] for k in 'lr'}
for s in 'lr':
    gh0 = np.array(LMJ['glenohumeral_' + s]['position_source_frame_cm'])
    for pz in ('abd90', 'flex90'):
        p = 'D1_%s_%s' % (s, pz); rows = []
        for t in ('W0', 'S1', 'S2'):
            gh = landmarks('W0', s, POSES['W0'][p])['GH']; vs, vw = vspec(s, gh, False)
            near = lambda V, gh=gh: np.linalg.norm(V[Q].mean(1) - gh, axis=1) < 48
            Vr, Qr, Cr, V, ids = scene(t, s, p, near); render(Vr, Qr, Cr, 's_%s_%s' % (p, t), vs, '0'); render(Vr, Qr, Cr, 'sw_%s_%s' % (p, t), vw, '1'); rows.append((t, res(t, p)))
        cell = 250; S = Image.new('RGB', (6 * cell + 360, 118 + 3 * (cell + 6)), (255, 255, 255)); dr = ImageDraw.Draw(S)
        dr.text((10, 8), '%s shoulder %s (LBS) — W0 / S1 (girdle mechanics) / S2 (S1 + bounded girdle weight diffusion); identical cameras, same world humerus' % ('Left' if s == 'l' else 'Right', pz), fill=(0, 0, 0), font=f(15, True))
        dr.text((10, 30), 'columns: front / rear / 3-4 front / 3-4 rear / anterior axillary-fold close-up (from below-front) | same close-up, wireframe', fill=(60, 60, 60), font=f(12))
        legend(dr, 52, list(COLS)[:4], COLS); legend(dr, 72, list(COLS)[4:], COLS); legend(dr, 92, list(LMC), LMC)
        for i, (t, r) in enumerate(rows):
            y = 118 + i * (cell + 6)
            for j, v in enumerate(('front', 'rear', 'tqf', 'tqr', 'ax')): S.paste(Image.open('%s/s_%s_%s_%s.png' % (OV, p, t, v)).convert('RGB').resize((cell, cell), Image.LANCZOS), (j * cell, y))
            S.paste(Image.open('%s/sw_%s_%s_w.png' % (OV, p, t)).convert('RGB').resize((cell, cell), Image.LANCZOS), (5 * cell, y)); it = r['intersections']
            L = [t, 'non-contact %d | crease %d (%.1f mm)' % (it['non_contact'], it['crease'], it['crease_depth_mm']), 'contact pairs %d' % it.get('contact', 0), 'orientation %d | local inv %d' % (r['flips']['total'], r['inversions']['total']),
                 'folds +%d (outside %d)' % (r['folds']['new'], r['folds']['outside']), 'loop %.2f' % r['loop_spacing_min_ratio'], 'p95 strain %.0f %% (max %.0f %%)' % (r['strain']['zone_p95_pct'], r['strain']['zone_max_pct']),
                 'zone proxy %+.1f %%' % r['volume']['zone_pct'], 'T-1 %.4f mm' % r['rest_return_T1_mm']]
            for k, l in enumerate(L): dr.text((6 * cell + 10, y + 6 + 20 * k), l, fill=(150, 20, 20) if k == 0 else (0, 0, 0), font=f(12, k == 0))
        S.save(SH + '/S_%s_%s.jpg' % (pz, s), quality=85); print('sheet', s, pz, flush=True)
# overview: every D1 pose, 3/4 front
PZ = ('abd45', 'abd90', 'flex90', 'ext30', 'abd90_girdle', 'flex90_girdle')
for s in 'lr':
    cell = 230; S = Image.new('RGB', (len(PZ) * cell + 20, 60 + 4 * (cell + 40)), (255, 255, 255)); dr = ImageDraw.Draw(S)
    dr.text((10, 8), '%s shoulder, all D1 poses — rows W0 / S1 (mechanics) / S2w (S2 weights, W0 mechanics) / S2 (both), 3-4 front camera centred on the W0 GH' % ('Left' if s == 'l' else 'Right'), fill=(0, 0, 0), font=f(14, True))
    for j, pz in enumerate(PZ):
        p = 'D1_%s_%s' % (s, pz); gh = landmarks('W0', s, POSES['W0'][p])['GH']; vs, _ = vspec(s, gh, False); vs = vs.split(';')[2]
        for i, t in enumerate(('W0', 'S1', 'S2w', 'S2')):
            near = lambda V, gh=gh: np.linalg.norm(V[Q].mean(1) - gh, axis=1) < 48
            Vr, Qr, Cr, V, ids = scene(t, s, p, near); render(Vr, Qr, Cr, 'so_%s_%s' % (p, t), vs, '0', 360); r = res(t, p); it = r['intersections']
            y = 36 + i * (cell + 40); S.paste(Image.open('%s/so_%s_%s_tqf.png' % (OV, p, t)).convert('RGB').resize((cell, cell), Image.LANCZOS), (10 + j * cell, y + 34))
            dr.text((12 + j * cell, y), '%s %s' % (t, pz), fill=(150, 20, 20), font=f(11, True))
            dr.text((12 + j * cell, y + 15), 'nc %d cr %d (%.1f) or %d loop %.2f' % (it['non_contact'], it['crease'], it['crease_depth_mm'], r['flips']['total'], r['loop_spacing_min_ratio']), fill=(0, 0, 0), font=f(10))
    S.save(SH + '/S_overview_%s.jpg' % s, quality=85); print('overview', s, flush=True)
# sections through GH: flex90 sagittal (normal = x), abd90 frontal (normal = f)
fig, axs = plt.subplots(2, 2, figsize=(16, 15)); CC = {'W0': 'k', 'S1': 'tab:blue', 'S2': 'tab:green'}
for i, (pz, nrm, e1, e2, lab) in enumerate((('flex90', np.array([1.0, 0, 0]), np.array([0, 1.0, 0]), np.array([0, 0, 1.0]), 'sagittal (x = GH): +x forward, +y up'),
                                            ('abd90', np.array([0, 1.0, 0]), np.array([1.0, 0, 0]), np.array([0, 0, 1.0]), 'frontal (f = GH): +x left, +y up'))):
    for j, s in enumerate('lr'):
        ax = axs[i, j]; p = 'D1_%s_%s' % (s, pz)
        for t in ('W0', 'S1', 'S2'):
            V = np.load('%s/diag/posed/%s_s_%s.npz' % (W, p, t))['V'].astype(float); ids = np.load('%s/diag/ids/%s_s_%s.npz' % (W, p, t)); pen = set(ids['pairs'][ids['pair_class'] < 2].ravel().tolist()) if len(ids['pairs']) else set()
            c = landmarks('W0', s, POSES['W0'][p])['GH']; dd = (V - c) @ nrm; fc = np.nonzero(np.linalg.norm(V[Q].mean(1) - c, axis=1) < 30)[0]; first = True
            for fi in fc:
                q = Q[fi]; pts = []
                for a_, b_ in ((q[0], q[1]), (q[1], q[2]), (q[2], q[3]), (q[3], q[0])):
                    if dd[a_] * dd[b_] < 0: tt = dd[a_] / (dd[a_] - dd[b_]); pp = V[a_] + tt * (V[b_] - V[a_]); pts.append(((pp - c) @ e1, (pp - c) @ e2))
                if len(pts) == 2:
                    ax.plot([pts[0][0], pts[1][0]], [pts[0][1], pts[1][1]], color=CC[t], lw=0.9, label=t if first else None); first = False
                    if fi in pen: ax.plot([pts[0][0], pts[1][0]], [pts[0][1], pts[1][1]], color=CC[t], lw=3.5, alpha=0.35)
            for nm, pos in landmarks(t, s, POSES[t][p]).items():
                if abs((pos - c) @ nrm) < 6: ax.plot((pos - c) @ e1, (pos - c) @ e2, 'o', color=LMC[nm], mec=CC[t], ms=7)
        ax.set_aspect('equal'); ax.set_xlim(-25, 25); ax.set_ylim(-28, 18); ax.legend(loc='upper right', fontsize=9)
        ax.set_title('%s %s section through the W0 GH — %s\nthick = faces in a non-contact / crease intersection pair; dots = landmarks within 6 cm of the plane' % (p, 'left' if s == 'l' else 'right', lab), fontsize=10)
plt.tight_layout(); plt.savefig(SH + '/S_sections.jpg', dpi=70); plt.close(); print('sections')
