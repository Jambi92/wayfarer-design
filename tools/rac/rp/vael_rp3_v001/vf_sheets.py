# vf_sheets.py OUTDIR : Vael elf-frame order (2026-10-28) §22 visual package, 22 sheets. Identical orthographic cameras per row, true scale (one camera
# set per configuration, centred on the VD2 source); ears hidden (hm08 w_ears > 0.05 harmonically collapsed), geometry-only grey shading. Workbench renders
# (grask_rigprep_v001/render_attr.py) composed with PIL / matplotlib; resumable; 2 Blender processes.
# Inputs: VF = /tmp/claude-0/rt/vf (cand/, prod/ = family workspace of VF2, comp/ = composition diagnostic), VD2 sources /tmp/claude-0/rt/vd/cand, PA = Part A
# comparators, EV = evidence folder (OUTDIR/..).
import sys, os, json, subprocess, numpy as np, scipy.sparse as sp
from PIL import Image, ImageDraw, ImageFont
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001')
import fn_face_metrics as F
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True); EV = os.path.abspath(OUT + '/..'); E_ = os.environ.get
VF = E_('VF_DIR', '/tmp/claude-0/rt/vf'); W2 = VF + '/prod'; PA = E_('VA_PA', '/tmp/claude-0/rt/va/partA'); TMP = VF + '/sheet_r'; os.makedirs(TMP, exist_ok=True)
BP = '/home/claude/stc/bin/python3'; REND = '/home/claude/wayfarer-design/tools/rac/rp/grask_rigprep_v001/render_attr.py'
GREY = np.array([0.80, 0.78, 0.76]); jl = lambda p: json.load(open(p))
CFG = {'c1': dict(P='VAL4-R1-VD2', FN='FNM178', AE='AEM178', MF='MFM178', SG='SGM178'), 'c2': dict(P='VALF178-R1-VD2', FN='FNF178', AE='AEF178', MF='MFF178', SG='SGF178')}
R6 = {}
for c, K in CFG.items():
    R6['%s_VD2' % c] = '/tmp/claude-0/rt/vd/cand/%s_r6.npz' % K['P']; R6['%s_R1' % c] = '/tmp/claude-0/rt/va2/vc2/r1/%s_r6.npz' % K['P'].replace('-VD2', '')
    for t in ('VF1', 'VF2', 'VF3'): R6['%s_%s' % (c, t)] = '%s/cand/%s-%s_r6.npz' % (VF, K['P'], t)
    for k in ('FN', 'AE', 'MF', 'SG'): R6['%s_%s' % (c, k)] = '%s/cmp/%s_r6.npz' % (PA, K[k])
def font(sz, bold=False):
    f = '/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf' % ('-Bold' if bold else ''); return ImageFont.truetype(f, sz) if os.path.exists(f) else ImageFont.load_default()
nz = np.load('/tmp/claude-0/rt/fn/src/FNL4_native.npz'); Q = np.asarray(nz['Q']); si = nz['src_index']; nV = len(si)
A = sp.coo_matrix((np.ones(4 * len(Q)), (Q[:, :4].ravel(), np.roll(Q, -1, 1).ravel())), shape=(nV, nV)).tocsr(); A = ((A + A.T) > 0).astype(float); deg = np.asarray(A.sum(1)).ravel()
def collapse(V):
    X = V.copy()
    for _ in range(400): X[F.EAR] = (A @ X)[F.EAR] / deg[F.EAR, None]
    return X
def eh(n, path=None):
    p = os.path.join(TMP, 'eh_%s.npz' % n)
    if not os.path.exists(p): np.savez(p, V=collapse(F.load(path or R6[n])['V']), Q=Q)
    return p
jobs = []
def render(tag, npz, col, views, wire=False, px=520):
    vs = ';'.join('%s:%s:%s:%.2f' % (n, ','.join('%.4f' % x for x in d), ','.join('%.3f' % x for x in c), hs) for n, d, c, hs in views)
    cf = os.path.join(TMP, tag + '_col.npy'); np.save(cf, np.asarray(col, np.float32)); jobs.append([BP, REND, '--', npz, cf, TMP, tag, vs, '1' if wire else '0', str(px)])
def img(tag, name):
    p = os.path.join(TMP, '%s_%s.png' % (tag, name)); return Image.open(p).convert('RGB') if os.path.exists(p) else Image.new('RGB', (600, 600), 'white')
def blend(a, b):
    A_ = np.asarray(a, float); B_ = np.asarray(b, float); bg = A_[2, 2]
    ma = np.abs(A_ - bg).sum(2) > 6; mb = np.abs(B_ - bg).sum(2) > 6; O = np.full_like(A_, 255.0)
    both = ma & mb; O[both] = 0.5 * (A_[both] + B_[both]); O[ma & ~mb] = [215, 40, 30]; O[mb & ~ma] = [40, 80, 215]; return Image.fromarray(np.clip(O, 0, 255).astype(np.uint8))
def heat(x, lo, hi):
    t = np.clip((x - lo) / (hi - lo + 1e-12), 0, 1)[:, None]; return (1 - t) * np.array([0.2, 0.35, 0.85]) + t * np.array([0.95, 0.25, 0.15])
CAM = {}
for c, K in CFG.items():
    Vv = np.load(eh('%s_VD2' % c))['V']; ym = Vv[:, 1].mean(); j = json.loads(str(np.load(R6['%s_VD2' % c])['joints'])); h = lambda b: np.array(j[b][0]); tl = lambda b: np.array(j[b][1])
    mid = lambda b: 0.5 * (h(b) + tl(b)); fc = 0.5 * (h('foot_l') + h('ball_l')); fc[2] = 6.0
    CAM[c] = dict(B=np.array([0.0, ym, 92.0]), U=np.array([0.0, ym, h('clavicle_l')[2] - 14]), S=np.array([h('clavicle_l')[0] + 9, ym, h('clavicle_l')[2] - 3]), T=np.array([0.0, ym, h('spine_02')[2] + 4]),
                  ua=mid('upperarm_l'), fa=mid('lowerarm_l') + np.array([0, 0, -4.0]), th=mid('thigh_l'), ca=mid('calf_l') + np.array([0, 0, -10.0]), foot=fc, H=np.array([0.0, ym, 160.0]))
BV = lambda c: [('bf', (0, 1, 0), CAM[c]['B'], 96), ('bq', (1, 1, 0.1), CAM[c]['B'], 96), ('bp', (1, 0, 0), CAM[c]['B'], 96), ('bb', (0, -1, 0), CAM[c]['B'], 96)]
RV = lambda c: [('up', (0, 1, 0), CAM[c]['U'], 30), ('sh', (0.3, 1, 0.3), CAM[c]['S'], 13), ('ua', (0.4, 1, 0.1), CAM[c]['ua'], 14), ('fa', (0.4, 1, 0.1), CAM[c]['fa'], 17),
                ('th', (0.3, 1, 0.05), CAM[c]['th'] + np.array([-4.0, 0, 0]), 24), ('ca', (0.4, 1, 0.1), CAM[c]['ca'], 26), ('foot', (0.6, 1, 0.5), CAM[c]['foot'], 11),
                ('tf', (0, 1, 0), CAM[c]['T'], 26), ('tq', (1, 1, 0.1), CAM[c]['T'], 26)]
HV = lambda c: [('hfront', (0, 1, 0.03), CAM[c]['H'], 14.5), ('hprof', (1, 0, 0), CAM[c]['H'], 14.5)]
for c in CFG:
    for k in ('R1', 'VD2', 'VF1', 'VF2', 'VF3', 'MF', 'SG', 'FN', 'AE'):
        n = '%s_%s' % (c, k); V = np.load(eh(n))['V']; render('he_' + n, eh(n), np.tile(GREY, (len(V), 1)), BV(c) + RV(c) + (HV(c) if k in ('VD2', 'VF2') else []))
    Va = np.load(eh('%s_VF2' % c))['V']; Vd = np.load(eh('%s_VD2' % c))['V']; d = np.linalg.norm(Va - Vd, axis=1)
    render('disp_%s' % c, eh('%s_VF2' % c), heat(d, 0, 0.8), BV(c)[:3] + RV(c)[:2])
    dh = d * 10; C = np.tile(GREY, (nV, 1)); C[F.HEAD & ~F.EAR] = heat(dh[F.HEAD & ~F.EAR], 0, 1.0); render('fdiff_%s' % c, eh('%s_VF2' % c), C, HV(c))
    nm = CFG[c]['P'] + '-VF2'; z = np.load('/home/claude/wayfarer-design/reviews/reference-assets/r6/%s_r6.npz' % nm); keep = z['keep']; Fx = z['F'][keep[z['F']].all(1)]
    q = os.path.join(TMP, 'src_%s.npz' % c); np.savez_compressed(q, V=z['V'], Q=Fx); render('src_%s' % c, q, np.tile(GREY, (len(z['V']), 1)), BV(c)[:2])
    fp = '%s/fam/%s_fam.npz' % (W2, nm); fz = np.load(fp); render('fam_%s' % c, fp, np.tile(GREY, (len(fz['V']), 1)), BV(c)[:2])
    for pn in ('shoulder_abd90_l', 'shoulder_abd45_l', 'elbow_130_l', 'wrist_flex60_l', 'hip_flex90_l', 'knee_140_l', 'ankle_dorsi20_l'):
        pp = '%s/def/%s_%s_fam.npz' % (W2, pn, nm)
        if not os.path.exists(pp): continue
        X = np.load(pp); Xv = X['V']; C = np.tile(GREY, (len(fz['Q']), 1)); fl = np.asarray(X['flip']).astype(int).ravel(); C[fl[fl < len(C)]] = [0.92, 0.18, 0.12]
        q = os.path.join(TMP, 'pose_%s_%s.npz' % (c, pn)); np.savez_compressed(q, V=Xv, Q=fz['Q']); B_ = np.array([0.0, Xv[:, 1].mean(), (Xv[:, 2].max() + Xv[:, 2].min()) / 2])
        render('pose_%s_%s' % (c, pn), q, C, [('v', (1, 1, 0.05), B_, 100)], px=420)
    for st in ('narrow_low_muscle', 'broad_high_muscle'):
        for t in ('VD2', 'VF2'):
            p = '%s/comp/%s-%s-%s_r6.npz' % (VF, c, t, st)
            if os.path.exists(p): n = 'cmp_%s_%s_%s' % (c, t, st); V = np.load(eh(n, p))['V']; render('he_' + n, eh(n, p), np.tile(GREY, (len(V), 1)), BV(c)[:2])
print('render jobs', len(jobs), flush=True)
done_ = lambda j: all(os.path.exists(os.path.join(TMP, '%s_%s.png' % (j[6], v_.split(':')[0]))) for v_ in j[7].split(';'))
todo = [j for j in jobs if not done_(j)]; print('to render', len(todo), flush=True)
with ThreadPoolExecutor(int(E_('VA_SHEET_THREADS', '2'))) as ex: list(ex.map(lambda j: subprocess.run(j, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL), todo))
def sheet(fname, title, rows, colw=420, note=None, lab_w=150, legend=None):
    ncol = max(len(r_[1]) for r_ in rows); Wd = lab_w + ncol * colw; tl = title.split(' — ', 1) if font(21, True).getlength(title) > Wd - 28 else [title]; th = 70 + 30 * (len(tl) - 1)
    nl = len(note.split('\n')) if note else 0; Hh = th + sum(colw + 34 for _ in rows) + (24 * nl + 20 if note else 0)
    S = Image.new('RGB', (Wd, Hh), 'white'); d = ImageDraw.Draw(S)
    for i_, t_ in enumerate(tl): d.text((14, 14 + 30 * i_), t_ if i_ == 0 else '— ' + t_, fill=(0, 0, 0), font=font(21, True))
    y = th
    for lab, ims, caps in rows:
        d.text((10, y + colw // 2), lab, fill=(0, 0, 0), font=font(17, True))
        for k_, im in enumerate(ims):
            S.paste(im.resize((colw, colw)), (lab_w + k_ * colw, y))
            if caps and k_ < len(caps) and caps[k_]: d.text((lab_w + 6 + k_ * colw, y + colw + 4), caps[k_], fill=(30, 30, 30), font=font(14))
        y += colw + 34
    if note:
        for i_, ln in enumerate(note.split('\n')): d.text((14, y + 4 + 24 * i_), ln, fill=(60, 60, 60), font=font(15))
    S.save(os.path.join(OUT, fname), quality=88)
EVC = {c: jl('%s/VF_eval_%s.json' % (EV, c)) for c in CFG}
sp_ = lambda c, t: EVC[c]['spans_vs_MF_pct'][t]; shv = lambda c, t, b: EVC[c]['shafts_vs_VD2_pct'][t][b]['section_share']
T4 = ['VD2', 'VF1', 'VF2', 'VF3']; C4 = ['VD2 (accepted)', 'VF1 (0.6)', 'VF2 (1.0)', 'VF3 (1.4)']
spanline = lambda c: '%s bideltoid vs MF: %s' % (c, '  '.join('%s %+.1f%%' % (t, sp_(c, t)['bideltoid_share']) for t in ('VD2', 'VF1', 'VF2', 'VF3', 'SG', 'FN', 'AE')))
for i, (v, lab) in enumerate((('bf', 'front'), ('bq', 'three-quarter'), ('bp', 'profile'))):
    sheet('VF_%02d_VD2_vs_VF_%s.jpg' % (i + 1, lab.replace('-', '')), 'Vael VD2 vs VF1 / VF2 / VF3 — full body %s, ears hidden, 178 cm, same camera' % lab,
          [(c, [img('he_%s_%s' % (c, t), v) for t in T4], C4) for c in CFG], colw=430, note=spanline('c1') + '\n' + spanline('c2'))
for i, (v, lab) in enumerate((('bf', 'front'), ('bq', 'three-quarter'))):
    sheet('VF_%02d_VF2_vs_humans_%s.jpg' % (i + 4, lab.replace('-', '')), 'Vael VF2 vs Marchfolk / Sagekin — %s, ears hidden, equal height; overlay VF2 red / Marchfolk blue' % lab,
          [(c, [img('he_%s_%s' % (c, t), v) for t in ('VF2', 'MF', 'SG')] + [blend(img('he_%s_VF2' % c, v), img('he_%s_MF' % c, v))], ['Vael VF2', 'Marchfolk', 'Sagekin', 'overlay']) for c in CFG], colw=430)
sheet('VF_06_VF2_vs_Fenn_Aelari.jpg', 'Vael VF2 vs frozen Fenn / frozen Aelari — front, three-quarter, profile (ears hidden, equal height)',
      [('%s %s' % (c, v[1:]), [img('he_%s_%s' % (c, t), v) for t in ('VF2', 'FN', 'AE')], ['Vael VF2', 'frozen Fenn', 'frozen Aelari'] if v == 'bf' else None) for c in CFG for v in ('bf', 'bq', 'bp')], colw=400)
C6 = ['VD2', 'VF2', 'MF', 'SG', 'FN', 'AE']; CP6 = ['Vael VD2', 'Vael VF2', 'Marchfolk', 'Sagekin', 'frozen Fenn', 'frozen Aelari']
def six(fname, title, views, note):
    sheet(fname, title, [('%s %s' % (c, v), [img('he_%s_%s' % (c, t), v) for t in C6], CP6 if v == views[0] else None) for c in CFG for v in views], colw=310, note=note)
six('VF_07_shoulder_span.jpg', 'Shoulder span — upper body front (VD2 | VF2 | Marchfolk | Sagekin | Fenn | Aelari)', ('up',),
    '\n'.join('%s spans vs MF (clavicle span / shoulder joint / bideltoid): %s' % (c, '  '.join('%s %+.1f/%+.1f/%+.1f' % (t, sp_(c, t)['clavicle_span_share'], sp_(c, t)['shoulder_joint_share'], sp_(c, t)['bideltoid_share']) for t in ('VD2', 'VF2', 'SG', 'FN', 'AE'))) for c in CFG))
six('VF_08_clavicle_shoulder_joint.jpg', 'Clavicle / shoulder-joint close-up (VD2 | VF2 | Marchfolk | Sagekin | Fenn | Aelari)', ('sh',), 'shoulder-joint placement moves medially along the clavicle (clavicle bone length x 0.96 at VF2); the upper-thorax side wall below the axilla follows (A2), keeping arm / trunk clearance')
shn = lambda b: '\n'.join('%s %s mid-shaft section vs VD2: %s; vs MF: VF2 %+.1f%%, Fenn %+.1f%%, Aelari %+.1f%%' % (c, b, '  '.join('%s %+.1f%%' % (t, shv(c, t, b)) for t in ('VF1', 'VF2', 'VF3')),
                                       EVC[c]['shafts_vs_MF_pct']['VF2'][b]['section_share'], EVC[c]['shafts_vs_MF_pct']['FN'][b]['section_share'], EVC[c]['shafts_vs_MF_pct']['AE'][b]['section_share']) for c in CFG)
bsn = lambda keys: '\n'.join('%s bases vs MF (VF2 | Fenn | Aelari): %s' % (c, '  '.join('%s %+.1f|%+.1f|%+.1f' % (k, EVC[c]['bases_vs_MF_pct']['VF2'][k], EVC[c]['bases_vs_MF_pct']['FN'][k], EVC[c]['bases_vs_MF_pct']['AE'][k]) for k in keys)) for c in CFG)
six('VF_09_upper_arm_shaft.jpg', 'Upper-arm shaft (VD2 | VF2 | Marchfolk | Sagekin | Fenn | Aelari)', ('ua',), shn('upperarm') + '\n' + bsn(['elbow_share']))
six('VF_10_forearm_wrist_base.jpg', 'Forearm shaft / wrist base (VD2 | VF2 | Marchfolk | Sagekin | Fenn | Aelari)', ('fa',), shn('lowerarm') + '\n' + bsn(['wrist_share', 'palm_root_over_wrist']))
six('VF_11_thigh_knee.jpg', 'Thigh shaft / knee (VD2 | VF2 | Marchfolk | Sagekin | Fenn | Aelari)', ('th',), shn('thigh') + '\n' + bsn(['knee_share']))
six('VF_12_calf_ankle_foot_base.jpg', 'Calf / ankle / foot base (VD2 | VF2 | Marchfolk | Sagekin | Fenn | Aelari)', ('ca', 'foot'), shn('calf') + '\n' + bsn(['ankle_share', 'heel_over_foot_length']))
tor = lambda c: '%s torso / stature vs MF (VD2 | VF2): %s' % (c, '  '.join('%s %+.1f|%+.1f' % (k.replace('_share', ''), EVC[c]['torso_vs_MF_pct']['VD2'][k], EVC[c]['torso_vs_MF_pct']['VF2'][k]) for k in ('thorax_breadth_max_share', 'waist_share', 'crest_share', 'thorax_depth_share')))
sheet('VF_13_torso_waist_regression.jpg', 'Torso / waist regression — R1 | VD2 | VF2 | Marchfolk (front and oblique; no waist pinch, depth kept)',
      [('%s %s' % (c, v), [img('he_%s_%s' % (c, t), v) for t in ('R1', 'VD2', 'VF2', 'MF')], ['R1', 'VD2', 'VF2', 'Marchfolk'] if v == 'tf' else None) for c in CFG for v in ('tf', 'tq')], colw=380, note=tor('c1') + '\n' + tor('c2'))
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
PV = {t: jl('%s/VF_pelvis_%s.json' % (EV, t)) for t in ('VF1', 'VF2', 'VF3')}; PD = jl(EV + '/../vael_rp3_custom_deformation/VD_pelvis_VD2.json')
fig, axs = plt.subplots(1, 2, figsize=(15, 4.8))
for ax, key, ttl in zip(axs, ('leg_share', 'waist_interval_over_torso'), ('hip-joint height / stature (skeletal proxy, t = 0.5): MF < Vael < Aelari < Fenn', 'VA-P6 waist interval / torso < Aelari')):
    x = 0; xt = []; xl = []
    for c in ('c1', 'c2'):
        r0 = [r for r in PD['rules'][c] if r['key'] == key]; ref = {r['rel'][-2:]: r['by_t']['0.5']['ref'] for r in r0}
        vals = [('MF', ref.get('MF')), ('VD2', r0[0]['by_t']['0.5']['VA'])] + [(t, [r for r in PV[t]['rules'][c] if r['key'] == key][0]['by_t']['0.5']['VA']) for t in ('VF1', 'VF2', 'VF3')] + [('AE', ref.get('AE')), ('FN', ref.get('FN'))]
        for lab, v in vals:
            if v is None: continue
            ax.bar(x, v, color={'MF': '#6aa36a', 'AE': '#7a4fb0', 'FN': '#4a78c2'}.get(lab, '#e07a2e')); xt.append(x); xl.append('%s %s' % (c, lab)); x += 1
        x += 1
    vv = [p.get_height() for p in ax.patches]; lo, hi = min(vv), max(vv); ax.set_ylim(lo - 0.3 * (hi - lo), hi + 0.3 * (hi - lo)); ax.set_xticks(xt); ax.set_xticklabels(xl, rotation=60, fontsize=7); ax.set_title(ttl, fontsize=10)
fig.tight_layout(); fig.savefig(os.path.join(OUT, 'VF_14_pelvis_regression.jpg'), dpi=100); plt.close(fig)
sheet('VF_15_silhouette_overlays_vs_MF.jpg', 'Silhouette overlays vs Marchfolk (candidate red / Marchfolk blue) — VD2 | VF1 | VF2 | VF3',
      [('%s %s' % (c, v[1:]), [blend(img('he_%s_%s' % (c, t), v), img('he_%s_MF' % c, v)) for t in T4], C4 if v == 'bf' else None) for c in CFG for v in ('bf', 'bq', 'up')], colw=400)
au = lambda c: '%s VF2: %d vertices moved (rest), max %.2f cm, RMS %.2f cm; per region max cm %s' % (c, EVC[c]['audit']['VF2']['affected_vertices_rest'], EVC[c]['audit']['VF2']['max_cm_rest'], EVC[c]['audit']['VF2']['rms_cm_rest_affected'],
                                                                                                 {k: v['max_cm'] for k, v in EVC[c]['audit']['VF2']['per_region'].items()})
sheet('VF_16_regional_displacement.jpg', 'VEF1 at VF2 — displacement |VF2 - VD2| (blue 0 .. red >= 8 mm)', [(c, [img('disp_%s' % c, v) for v in ('bf', 'bq', 'bp', 'up', 'sh')], ['front', '3/4', 'profile', 'upper body', 'shoulder']) for c in CFG], colw=340,
      note=au('c1') + '\n' + au('c2'))
names = {c: CFG[c]['P'] + '-VF2' for c in CFG}; VA_ = {c: jl('%s/val/%s_fam_validator_v2_D1-D6.json' % (W2, names[c])) for c in CFG}; st_ = sorted(VA_['c1']['stations'])
S = Image.new('RGB', (1200, 140 + 26 * (len(st_) + 2)), 'white'); d = ImageDraw.Draw(S)
d.text((14, 14), 'Vael VF2 family candidates on frozen v005 — validator D1+D3+D4+D5+D6', fill=(0, 0, 0), font=font(20, True))
d.text((14, 44), 'margin = loops - contract minimum (red = 0).   c1: %d / 69   c2: %d / 69' % (VA_['c1']['summary']['firm_pass_count'], VA_['c2']['summary']['firm_pass_count']), fill=(0, 0, 0), font=font(16))
cw = [260, 150, 150, 150, 150, 150, 150]; y = 90
for i, t in enumerate(['station', 'c1 loops', 'c1 min', 'c1 margin', 'c2 loops', 'c2 min', 'c2 margin']): d.text((20 + sum(cw[:i]), y), t, fill=(0, 0, 0), font=font(15, True))
y += 28
for s_ in st_:
    a, b = VA_['c1']['stations'][s_], VA_['c2']['stations'][s_]; vals = [s_, a['loops_v2'], a['required'], a['margin'], b['loops_v2'], b['required'], b['margin']]
    for i, t in enumerate(vals): d.text((20 + sum(cw[:i]), y), str(t), fill=(200, 30, 30) if (i in (3, 6) and t == 0) else (0, 0, 0), font=font(14))
    y += 26
S.save(os.path.join(OUT, 'VF_17_validator_margins.jpg'), quality=88)
fig, ax = plt.subplots(figsize=(11, 4.5)); zs = ['face', 'ears', 'hand', 'foot', 'trunk', 'arm', 'leg', 'neck', 'head']; x = np.arange(len(zs)); okall = True
for i, c in enumerate(CFG):
    aud = jl('%s/audit/%s_fam_audit.json' % (W2, names[c]))['density_pct_of_stature']; ax.bar(x + (i - 0.5) * 0.35, [aud[z]['mean'] for z in zs], 0.35, label=names[c]); okall &= all(aud[z]['pass_mean'] for z in zs)
    ax.scatter(x, [aud[z]['limit'] for z in zs], marker='_', s=600, color='k')
ax.set_xticks(x); ax.set_xticklabels(zs); ax.set_ylabel('mean edge / stature (%)'); ax.set_title('Vael VF2 family density, 9 zones (black bar = limit): %s' % ('all pass' if okall else 'FAIL present')); ax.legend(); fig.tight_layout(); fig.savefig(os.path.join(OUT, 'VF_18_density.jpg'), dpi=105); plt.close(fig)
dc = jl(EV + '/VAEL_deformation_comparison.json'); PN = ('shoulder_abd90_l', 'shoulder_abd45_l', 'elbow_130_l', 'wrist_flex60_l', 'hip_flex90_l', 'knee_140_l', 'ankle_dorsi20_l')
sheet('VF_19_deformation.jpg', 'Vael VF2 family candidates — Standard v1 deformation, shoulders / elbows / wrists / hips / knees / ankles (red = flipped faces)',
      [(c, [img('pose_%s_%s' % (c, p), 'v') for p in PN], ['%s %d (MF v005 %d)' % (p, dc[names[c]]['poses'][p]['aelari_family'], dc[names[c]]['poses'][p]['marchfolk_v005']) for p in PN]) for c in CFG], colw=330,
      note='worst flip excess vs the frozen Marchfolk v005 realisation: %s; poses worse by > 5: %s' % ({n: dc[n]['worst_flip_excess'] for n in dc}, {n: dc[n]['poses_worse_by_more_than_5'] for n in dc}))
FR = jl(EV + '/VF_face_regression.json')
sheet('VF_20_VC2_face_regression.jpg', 'VC2 face regression — VD2 | VF2 (ears hidden) and |VF2 - VD2| on the head (blue 0 .. red >= 1 mm)',
      [('%s %s' % (c, v[1:]), [img('he_%s_VD2' % c, v), img('he_%s_VF2' % c, v), img('fdiff_%s' % c, v)], ['VD2', 'VF2', 'difference'] if v == 'hfront' else None) for c in CFG for v in ('hfront', 'hprof')], colw=400,
      note='\n'.join('%s: head |dV| max %.3f cm (non-rigid part %.3f cm, at the head / neck seam); face systems %d / 6; elf rows %d / 9; whole-face vs MF %.3f mm (VD2 %.3f); brow %+.2f %%; jaw %+.2f %% (VD2 %+.2f)' % (
          c, FR[c]['head_max_dV_cm'], FR[c]['head_nonrigid_cm'], FR[c]['VF2']['face_systems'], FR[c]['VF2']['elf_rows'], FR[c]['VF2']['whole_face_mm'], FR[c]['VD2']['whole_face_mm'], FR[c]['VF2']['brow_pct'], FR[c]['VF2']['jaw_pct'], FR[c]['VD2']['jaw_pct']) for c in CFG))
sheet('VF_21_final_five_population.jpg', 'FINAL equal-height (178 cm) hidden-ear neutral comparison — Vael VF2 | frozen Fenn | frozen Aelari | Marchfolk | Sagekin',
      [('%s %s' % (c, v[1:]), [img('he_%s_%s' % (c, t), v) for t in ('VF2', 'FN', 'AE', 'MF', 'SG')], ['Vael VF2', 'frozen Fenn', 'frozen Aelari', 'Marchfolk', 'Sagekin'] if v == 'bf' else None) for c in CFG for v in ('bf', 'bq', 'bp', 'bb')], colw=330)
CM = jl(EV + '/VF_composition_diagnostic.json')['states']
cmn = '\n'.join('%s: VF2 vs VD2 %s' % (k, '  '.join('%s %+.1f%%' % (q, v) for q, v in d['VF2_vs_VD2_pct'].items() if q != 'stature')) for k, d in CM.items())
sheet('VF_22_composition_stress.jpg', 'Composition firewall diagnostic — narrow / low muscle | balanced | broad / high muscle: VD2 vs VF2 (front)',
      [(c, [img('he_cmp_%s_VD2_narrow_low_muscle' % c, 'bf'), img('he_cmp_%s_VF2_narrow_low_muscle' % c, 'bf'), img('he_%s_VD2' % c, 'bf'), img('he_%s_VF2' % c, 'bf'),
            img('he_cmp_%s_VD2_broad_high_muscle' % c, 'bf'), img('he_cmp_%s_VF2_broad_high_muscle' % c, 'bf')], ['VD2 narrow/low', 'VF2 narrow/low', 'VD2 balanced', 'VF2 balanced', 'VD2 broad/high', 'VF2 broad/high']) for c in CFG],
      colw=300, note=cmn)
print('sheets done', len([f for f in os.listdir(OUT) if f.startswith('VF_')]), flush=True)
