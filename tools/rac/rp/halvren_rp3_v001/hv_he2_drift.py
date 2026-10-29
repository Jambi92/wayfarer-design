# hv_he2_drift.py OUT.json OUT.md : Halvren HE2 closure order §4 -- AUTHORED vs REALIZED HE2 domain table. The authored HE2 (HVEAR2) intent per measured
# domain is its authored position t_auth on the Marchfolk -> elf-mean line of the corresponding authored parameter (W1 MF-human vs frozen elf parameters),
# transported onto the MEASURED Marchfolk / elf-mean values of that domain (target = MF_meas + t_auth x (elf_meas - MF_meas)). Realized = the HVEAR2
# guarded HE2 realization on c1 (measured, same rule). Drift = realized - target (signed, and in source-SD units); directional pull = the source whose
# measured value the realized point moved toward (largest positive projection of the drift on the target -> source direction; 'interpolation line'
# when the realized t sits within 0.15 of the realized one-alpha fit to the Marchfolk -> Aelari line); cause = from the control Jacobian (hv_ear_jac.py).
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import hv_ear_domains as D
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001')
OJ, OM = sys.argv[1:3]; jl = lambda p: json.load(open(p)); SRC = jl('/tmp/claude-0/rt/hv/ear/src_dom.json')['items']; DOM = D.DOM
H = 'HVC1-HB2HF2-HPB'; REAL = D.measure('branch', '/tmp/claude-0/rt/hv/ear/he/build/%s_HE2_branch.npz' % H, H)        # HVEAR2 HE2 (pre-correction) guarded realization
NEW = D.measure('branch', '/tmp/claude-0/rt/hv/ear/he3/build/%s_HE2_branch.npz' % H, H) if os.path.exists('/tmp/claude-0/rt/hv/ear/he3/build/%s_HE2_branch.npz' % H) else None
X = {s: np.array([SRC[s][q] for q in DOM]) for s in ('MF', 'FN', 'AE', 'VA')}; sd = np.maximum(np.array(list(X.values())).std(0), [D.FLOOR[q] for q in DOM]); em = np.mean([X[e] for e in ('FN', 'AE', 'VA')], 0)
# authored HVEAR2 HE2 vs W1 MF-human / frozen elf parameters, per domain (parameter used as the authored proxy of the domain)
A2 = dict(L=7.8, wb=2.00, st=0.36, ex=1.10, sh=0.06, lobe=0.20, proj=23, tilt=16, sweep=1.4, concha=0.86, trag=0.31, tauA=12.0)
P = {'MF': dict(L=6.4, wb=1.75, st=0.55, ex=0.5, sh=0.0, lobe=0.18, proj=22, tilt=12, sweep=0.4, concha=0.85, trag=0.30, tauA=12.0),
     'FN': dict(L=8.6, wb=1.80, st=0.30, ex=1.05, sh=0.0, lobe=0.15, proj=50, tilt=32, sweep=1.6, concha=0.72, trag=0.24, tauA=12.0),
     'AE': dict(L=9.4, wb=1.70, st=0.25, ex=0.95, sh=0.0, lobe=0.14, proj=24, tilt=30, sweep=1.7, concha=0.70, trag=0.24, tauA=12.0),
     'VA': dict(L=8.5, wb=2.05, st=0.40, ex=1.25, sh=0.0, lobe=0.16, proj=35, tilt=40, sweep=1.7, concha=0.76, trag=0.26, tauA=12.0)}
PROXY = dict(length_over_HH=('L',), width_over_length=('wb', 'L'), projection_deg=('proj',), upward_ext_over_HH=('L', 'st'), backward_angle_deg=('tilt', 'sweep'), tip_angle_deg=('ex', 'st'),
             lobe_fraction=('lobe',), root_line_deg=('tauA',), concha_depth_over_L=('concha',), tragus_height_frac=('trag',), helix_fullness=('sh', 'st'))
CAUSE = dict(length_over_HH='calibration: W1 MF-human L 6.4 already realizes 0.28-0.30 HH (Marchfolk auricle 0.24); L also drives upward extension (+0.41 SD / +0.6 cm) and free lobe (+0.69)',
             width_over_length='taper start / early taper narrows the upper ear; width also coupled to concha depth (+0.45), root flare phi0 (-8 deg: +0.42) and placement height (+0.55)',
             projection_deg='calibration: W1 human proj 22 realizes ~23-25 deg vs the flat Marchfolk auricle 6.5 deg; projection itself is NOT linked to root rotation (phi0 / tauA < 0.07 SD)',
             upward_ext_over_HH='the junction-centred placement puts every branch auricle top ~1.9 cm above the root-loop top (Marchfolk 0.3 cm); length and tilt add (+0.41, +0.32)',
             backward_angle_deg='calibration: W1 human tilt 12 realizes ~14 deg (Marchfolk 4.8); sweep is a second backward driver (-0.4: -0.47 SD) -> tilt + sweep add',
             tip_angle_deg='early continuous taper (start 0.36) makes an elf apex (60 deg) whatever the exponent (tex: -0.12 SD per +0.25); only a later start + shoulder rounds it',
             lobe_fraction='the lobe parameter is inert in the realized free lobe (0.0 SD); the free lobe follows length (+0.69) and placement height (+1.15)',
             root_line_deg='attachment-line inclination is set by the junction placement (place_du +2.5, place_db +1.3) and concha depth (-1.7); Marchfolk / elf differences small',
             concha_depth_over_L='the authored concha 0.86 is diluted by the longer ear (depth / L) and the -0.50 seat; +0.25 concha -> +0.87 SD, but concha depth also raises the junction (mound)',
             tragus_height_frac='cavum level falls as the upper extension lengthens (cavum stays at the base)', helix_fullness='early taper start removes the upper helix body; sweep / tilt / shoulder restore it (+0.82 / +0.61 / +0.29)')
rows = {}; tr = (np.array([REAL[q] for q in DOM]) - X['MF']) / np.where(np.abs(em - X['MF']) > 1e-9, em - X['MF'], 1)
xa = (X['AE'] - X['MF']) / sd; ya = (np.array([REAL[q] for q in DOM]) - X['MF']) / sd; k = np.abs(xa) > 0.5; alpha = float(xa[k] @ ya[k] / (xa[k] @ xa[k]))
for i, q in enumerate(DOM):
    ps = PROXY[q]; ta = []
    for pk in ps:
        m, e = P['MF'][pk], np.mean([P[s][pk] for s in ('FN', 'AE', 'VA')])
        if abs(e - m) > 1e-9: ta.append((A2[pk] - m) / (e - m))
    t_auth = float(np.mean(ta)) if ta else 0.0; tgt = X['MF'][i] + t_auth * (em[i] - X['MF'][i]); r = REAL[q]; dr = r - tgt
    pulls = {s: float(dr * (X[s][i] - tgt)) / (abs(X[s][i] - tgt) + 1e-12) for s in ('MF', 'FN', 'AE', 'VA')}
    line_t = alpha * (X['AE'][i] - X['MF'][i]) / ((em[i] - X['MF'][i]) if abs(em[i] - X['MF'][i]) > 1e-9 else 1)
    pull = 'interpolation line (MF->AE alpha %.2f)' % alpha if abs(tr[i] - line_t) <= 0.15 and abs(dr) / sd[i] > 0.25 else (max(pulls, key=pulls.get) if abs(dr) / sd[i] > 0.25 else 'none (on target)')
    rows[q] = dict(authored_t=round(t_auth, 2), authored_target=round(float(tgt), 4), realized=round(float(r), 4), realized_t=round(float(tr[i]), 2), drift=round(float(dr), 4), drift_sd=round(float(dr / sd[i]), 2),
                   pull=pull, cause=CAUSE[q], corrected=(round(float(NEW[q]), 4) if NEW else None))
json.dump(dict(order='chatgpt-rac-rp3-halvren-he2-realization-ear-architecture-closure-order §4', authored='HVEAR2 HE2', realized='HVEAR2 HE2 guarded c1', corrected='HVEAR3 HE2 guarded c1' if NEW else None, rows=rows), open(OJ, 'w'), indent=1)
L = ['| Domain | Authored t | Authored target | Realized (HVEAR2) | Drift (SD) | Pull | Corrected HE2 | Cause |', '|---|---|---|---|---|---|---|---|']
for q, r in rows.items(): L.append('| %s | %.2f | %.3f | %.3f (t %.2f) | %+.2f | %s | %s | %s |' % (q, r['authored_t'], r['authored_target'], r['realized'], r['realized_t'], r['drift_sd'], r['pull'], '%.3f' % r['corrected'] if r['corrected'] is not None else '—', r['cause']))
open(OM, 'w').write('\n'.join(L) + '\n'); print('\n'.join(L))
