# mf4_sheets.py WORK : order 2d34a0c evidence sheets (v003 freeze candidate; no v004 produced).
#  MF4_toe_attribution_{M,F}.jpg : toes 3-5, dorsal / plantar / medial-side views, v003 wire; faces tinted by OWNING toe (nearest toe axis);
#      the toe3 j3 / toe4 j2 crease slab (|axial| <= 0.5 local loop, radius = station pole radius) drawn in red; poles: on the audited toe = black,
#      flagged poles = yellow (they lie on the neighbouring toe)
#  MF4_validator_{M,F}.jpg : 69-station table, legacy / D1 / D1+D3 verdicts, fallback status
#  MF4_summary.jpg : family-core final topology summary
import sys, os, json, subprocess, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFont
W = sys.argv[1]; T = '/home/claude/wayfarer-design/tools/rac/rp/grask_rigprep_v001/render_attr.py'; BP = '/home/claude/stc/bin/python3'
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FN = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; f = lambda n, b=False: ImageFont.truetype(FB if b else FN, n)
OV = W + '/ov4'; SH = W + '/sheets4'; os.makedirs(OV, exist_ok=True); os.makedirs(SH, exist_ok=True); CLAY = np.array([0.80, 0.77, 0.73])
def render(V, Q, col, tg, vs, wire='0', px=520):
    o = OV + '/%s.npz' % tg
    if not os.path.exists(OV + '/%s_%s.png' % (tg, vs.split(';')[-1].split(':')[0])):
        np.savez(o, V=V, Q=Q); np.save(o[:-4] + '_c.npy', np.asarray(col, np.float32))
        subprocess.run([BP, T, '--', o, o[:-4] + '_c.npy', OV, tg, vs, wire, str(px)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, env=dict(os.environ, WIRE_T='0.00008'))
def img(tg, v, cell): return Image.open('%s/%s_%s.png' % (OV, tg, v)).convert('RGB').resize((cell, cell), Image.LANCZOS)
def vs_(views): return ';'.join('%s:%s:%s:%g' % (n, ','.join('%.4f' % x for x in d), ','.join('%.3f' % x for x in c), h) for n, d, c, h in views)
def segdist(P, pts):
    best = np.full(len(P), 1e9)
    for a, b in zip(pts[:-1], pts[1:]):
        ab = b - a; t = np.clip((P - a) @ ab / (ab @ ab), 0, 1); best = np.minimum(best, np.linalg.norm(P - (a + t[:, None] * ab), axis=1))
    return best
TOECOL = {1: (0.55, 0.75, 0.95), 2: (0.6, 0.9, 0.6), 3: (0.95, 0.85, 0.55), 4: (0.85, 0.65, 0.95), 5: (0.6, 0.9, 0.9)}
for C in 'MF':
    cid = 'MF-%s-R' % C; cz = np.load('%s/cand/%s_v003.npz' % (W, cid)); V = cz['V']; Q = cz['Q']; meta = json.loads(str(cz['meta'])); JC = {k: np.array(v) for k, v in meta['joint_cubes'].items()}
    val = json.load(open('%s/v4/%s_v003_validator_v2.json' % (W, cid)))['stations']
    E = np.sort(np.concatenate([Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]]), 1); vv = np.bincount(np.unique(E, axis=0).ravel(), minlength=len(V)); poles = np.nonzero(vv != 4)[0]
    ax = {}
    for t in range(1, 6):
        ks = sorted([n for n in JC if n.startswith('l-toe-%d-' % t)], key=lambda n: int(n.split('-')[-1])); pts = [JC[k] for k in ks]; pts.append(pts[-1] + (pts[-1] - pts[-2])); ax[t] = pts
    D = np.stack([segdist(V, ax[t]) for t in range(1, 6)], 1); own = D.argmin(1) + 1; ontoe = D.min(1) < 1.0
    cv = np.tile(CLAY, (len(V), 1))
    for t in range(1, 6): cv[ontoe & (own == t)] = TOECOL[t]
    targets = ['toe3_j3_l'] + (['toe4_j2_l'] if C == 'F' else [])
    from core3lib import stations, unit  # noqa
    S = {s[0]: s for s in stations(meta)}
    for nm in targets:
        _, c, d, Wd, Rr, need, Rp = S[nm]; d = unit(np.asarray(d)); P = V - c; t_ = P @ d; rr = np.linalg.norm(P - np.outer(t_, d), axis=1); h = val[nm]['local_loop_cm']
        slab = (np.abs(t_) <= 0.5 * h) & (rr <= Rp); cv[slab] = 0.5 * cv[slab] + 0.5 * np.array([0.95, 0.15, 0.15])
    cv[poles] = (0.1, 0.1, 0.1)
    flag = sorted({p for nm in targets for p in val[nm]['crease_poles']}); cv[flag] = (1.0, 0.9, 0.0)
    fc = cv[Q].mean(1); fc[np.isin(Q, flag).any(1)] = (1.0, 0.85, 0.0); fc[np.isin(Q, np.setdiff1d(poles, flag)).any(1) & ontoe[Q].all(1)] *= 0.55; c0 = JC['l-toe-4-2'] if 'l-toe-4-2' in JC else JC['l-toe-3-2']
    VW = [('dorsal', (0.0, 0.3, 0.95), c0, 2.6), ('plantar', (0.0, 0.2, -0.98), c0, 2.6), ('front', (0.0, 1.0, 0.05), c0, 2.6), ('lateral', (1.0, 0.2, 0.1), c0, 2.6)]
    render(V, Q, fc, 'att_%s' % C, vs_(VW), '1', 640)
    cell = 330; S2 = Image.new('RGB', (4 * cell + 20, 120 + cell + 15 * 15), 'white'); d_ = ImageDraw.Draw(S2)
    d_.text((10, 8), 'Marchfolk %s v003 toe-IP residual attribution (left foot) — faces tinted by owning toe (nearest toe axis): 1 blue, 2 green, 3 sand, 4 lilac, 5 cyan' % cid, fill=(0, 0, 0), font=f(13, True))
    d_.text((10, 28), 'red slab = crease slab of %s (|axial| <= 0.5 loop, radius = station pole radius); black = poles; YELLOW = the flagged "crease poles" of those stations' % ' / '.join(targets), fill=(0, 0, 0), font=f(12))
    for j, v in enumerate(('dorsal', 'plantar', 'front', 'lateral')): S2.paste(img('att_%s' % C, v, cell), (10 + j * cell, 52)); d_.text((14 + j * cell, 56), v, fill=(150, 20, 20), font=f(11, True))
    y = 64 + cell
    for nm in targets:
        r = val[nm]
        for p in r['crease_poles']:
            dd = {t: round(float(segdist(V[p:p + 1], ax[t])[0]), 2) for t in range(1, 6)}; ow = min(dd, key=dd.get)
            d_.text((10, y), '%s: flagged pole %d (valence %d) lies %.2f cm from the toe-%d axis and %.2f cm from the audited toe-%s axis -> belongs to toe %d' % (nm, p, vv[p], dd[ow], ow, dd[int(nm[3])], nm[3], ow), fill=(0, 0, 0), font=f(11)); y += 15
        d_.text((10, y), '   %s own-toe crease poles: %d; own-toe poles within 2 loops: %d; loops %d (need %d), mode %s; status D1 %s, D1+D3 %s' % (nm, len(r['crease_poles_own_digit']), len(r['within2_own_digit']), r['loops_v2'], r['required'], r['loop_mode'], r['status_D1'], r['status_D1_D3']), fill=(0, 0, 120), font=f(11)); y += 18
    S2.save(SH + '/MF4_toe_attribution_%s.jpg' % C, quality=88)
    # validator table
    rows = sorted(val.items()); cell_h = 15; S3 = Image.new('RGB', (1500, 70 + (len(rows) // 2 + 1) * cell_h), 'white'); d_ = ImageDraw.Draw(S3)
    d_.text((10, 8), 'Marchfolk %s v003 — 69-station §7 validator v2: legacy | D1 (authorised) | D1+D3 (proposed digit pole scoping); loops (need), crease poles all / own digit' % cid, fill=(0, 0, 0), font=f(13, True))
    for i, (k, r) in enumerate(rows):
        x0 = 10 + (i % 2) * 745; y0 = 34 + (i // 2) * cell_h
        col = (0, 110, 0) if r['status_D1'] == 'PASS' else ((0, 70, 170) if r['status_D1'].startswith('PASS') else ((150, 90, 0) if r['firm_D1_D3'] else (180, 0, 0)))
        d_.text((x0, y0), '%-13s %s|%s|%s  loops %d (%d)  crease %d/%d  %s / %s' % (k, 'P' if r['firm_legacy'] else 'F', 'P' if r['firm_D1'] else 'F', 'P' if r['firm_D1_D3'] else 'F', r['loops_v2'], r['required'],
                 len(r['crease_poles']), len(r['crease_poles_own_digit']), r['status_D1'], r['status_D1_D3']), fill=col, font=f(10))
    S3.save(SH + '/MF4_validator_%s.jpg' % C, quality=88); print('sheets', C, flush=True)
# ---- foot / toe deformation sanity: native | v002 | v003 for toe flexion / extension + v003 ankle dorsiflexion (left foot)
for C in 'MF':
    cid = 'MF-%s-R' % C; m = json.loads(str(np.load('%s/src/%s_native.npz' % (W, cid))['meta'])); Hd = {k: np.array(v) for k, v in m['heads'].items()}
    Qs = {'native': np.load('%s/src/%s_native.npz' % (W, cid))['Q'], 'v002': np.load('%s/cand/%s_v002.npz' % (W, cid))['Q'], 'v003': np.load('%s/cand/%s_v003.npz' % (W, cid))['Q']}
    J = {'native': json.load(open('%s/v4/deform_%s_native_toe.json' % (W, cid)))['poses'], 'v002': json.load(open('%s/v4/deform_%s_v002_toe.json' % (W, cid)))['poses'], 'v003': json.load(open('%s/v4/deform_%s_v003_sanity.json' % (W, cid)))['poses']}
    tag = {'native': 'native_toe', 'v002': 'v002_toe', 'v003': 'v003_sanity'}
    cell = 300; S4 = Image.new('RGB', (3 * cell + 20, 70 + 2 * (cell + 40)), 'white'); d_ = ImageDraw.Draw(S4)
    d_.text((10, 8), 'Marchfolk %s foot / toe deformation sanity (source rig: one ball bone for all toes; LBS) — native | v002 | v003; red new self-x, magenta flipped, purple new fold' % cid, fill=(0, 0, 0), font=f(12, True))
    for i, pn in enumerate(('toe_flex30_l', 'toe_ext30_l')):
        for j, t in enumerate(('native', 'v002', 'v003')):
            pz = np.load('%s/v4/%s_%s_%s.npz' % (W, pn, cid, tag[t])); X = pz['V'].astype(float); Qx = Qs[t]; col = np.tile(CLAY, (len(Qx), 1))
            if len(pz['selfx']): col[pz['selfx'].ravel()] = (0.9, 0.05, 0.05)
            col[pz['flip']] = (0.95, 0.2, 0.75)
            if len(pz['fold']): col[pz['fold'].ravel()] = (0.55, 0.0, 0.75)
            cc = X[np.linalg.norm(X - Hd['ball_l'], axis=1).argsort()[:200]].mean(0); render(X, Qx, col, 'tdef_%s_%s_%s' % (pn, C, t), vs_([('v', (0.5, 0.6, 0.6), cc, 6)]), '0', 420)
            x0 = 10 + j * cell; y0 = 36 + i * (cell + 40); S4.paste(img('tdef_%s_%s_%s' % (pn, C, t), 'v', cell), (x0, y0 + 30)); dd = J[t][pn]
            d_.text((x0 + 2, y0), '%s %s' % (pn, t), fill=(150, 20, 20), font=f(11, True)); d_.text((x0 + 2, y0 + 14), 'self-x %d folds %d flips %d p95 %.0f%% vol %+.1f%%' % (dd['new_selfx_in_zone'], dd['new_folds_in_zone'], dd['flipped_in_zone'], dd['strain_p95_pct'], dd['zone_volume_pct']), fill=(0, 0, 0), font=f(10))
    S4.save(SH + '/MF4_toe_deform_%s.jpg' % C, quality=88); print('toe deform', C, flush=True)
