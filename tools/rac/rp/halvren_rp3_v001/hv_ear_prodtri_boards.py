# hv_ear_prodtri_boards.py PRODTRI_DIR SNAP_DIR OUTDIR : boards for the Halvren ear final production triangulation / shading gate
#   A  triangulation closeups HE1 / HE2 / HE3 (c1, left ear): cuff / root, lobe junction, upper helix / tip -- quads | baked TRI-HV1 triangles | alternate
#      diagonal diagnostic (flagged quads tinted by the fold across their diagonal: amber 20-60, orange 60-90, red > 90 deg; blue = step-5 flips)
#   B  shading on the baked triangles, grazing studio light + specular: front 3/4 | strict side | true rear 3/4 | direct rear | lower-rear 3/4 |
#      lower-root closeup | upper helix / tip closeup (c1 / c2);  B2 the same under a reflection-stripe matcap (zebra: stripe breaks = normal breaks)
#   B3 quads (DCC display) vs baked triangles vs independent rebuild (c1, pixel difference)
#   C  pose stress: the two worst poses per ear / configuration on the baked triangles (camera carried rigidly with the head)
#   D  LOD source / 50 % / 25 %: side and true rear 3/4
import sys, os, json, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageChops
from concurrent.futures import ThreadPoolExecutor
os.environ.setdefault('EAR_TOPO', 'v002'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hv_ear_quick as QK, hv_ear_domains as D
PT, SN, OUT = sys.argv[1:4]; os.makedirs(OUT, exist_ok=True); TMP = os.path.join(PT, 'brd'); os.makedirs(TMP, exist_ok=True)
H = {'c1': 'HVC1-HB2HF2-HPB', 'c2': 'HVF178-HB2HF2-HPB'}; EARS = ('HE1', 'HE2', 'HE3'); GREY = QK.GREY; font = QK.font
jl = lambda p: json.load(open(p)); unit = lambda v: v / max(np.linalg.norm(v), 1e-12)
RJ = {(k, c): jl('%s/%s_%s_prodtri.json' % (PT, k, c)) for k in EARS for c in ('c1', 'c2')}
TZ = {(k, c): np.load('%s/%s_%s_tri.npz' % (PT, k, c), allow_pickle=True) for k in EARS for c in ('c1', 'c2')}
jobs = []
def vspec(views): return ';'.join('%s:%s:%s:%.2f' % (nm, ','.join('%.4f' % x for x in d), ','.join('%.3f' % x for x in cc), h) for nm, d, cc, h in views)
def job(tag, V, F, col, views, wire=False, px=560, env=None):
    np.savez(os.path.join(TMP, tag + '_m.npz'), V=np.asarray(V, np.float32), Q=np.asarray(F)); cf = os.path.join(TMP, tag + '_col.npy')
    np.save(cf, np.asarray(col if col is not None else np.tile(GREY, (len(V), 1)), np.float32))
    jobs.append(([QK.BP, QK.REND, '--', os.path.join(TMP, tag + '_m.npz'), cf, TMP, tag, vspec(views), '1' if wire else '0', str(px)], dict(os.environ, **(env or {}))))
def img(tag, v, sz=None):
    p = os.path.join(TMP, '%s_%s.png' % (tag, v)); im = Image.open(p).convert('RGB') if os.path.exists(p) else Image.new('RGB', (560, 560), (255, 200, 200))
    return im.resize((sz, sz)) if sz else im
def cams(h):
    C = QK.cams(h); rd = D.frame(h, 'l'); O, n, b, u = rd['O'], rd['n'], rd['b'], rd['u']; z3 = np.array([0, 0, 1.0])
    out = {k: (np.asarray(C[k][0], float), np.asarray(C[k][1], float), C[k][2]) for k in ('etq', 'side', 'rq', 'rr', 'lr')}
    out['zf'] = (0.7 * n - b - 0.3 * z3, O - 2.5 * u + 0.3 * b, 2.4); return out, rd
def tipcam(V, side_, part, rd):
    sv = np.nonzero((side_ == 'l') & np.isin(part, ['front', 'back', 'rim']))[0]; top = V[sv[np.argmax((V[sv] - rd['O']) @ rd['u'])]]
    return (rd['n'] + 0.35 * rd['b'] + 0.25 * rd['u'], top - 0.8 * rd['u'], 1.7)
FOLDC = lambda f: [0.95, 0.15, 0.1] if f > 90 else ([0.98, 0.55, 0.1] if f > 60 else [0.95, 0.8, 0.25])
lab = lambda k: k.replace('_', ' ')
SZ = {}
# ---------------- A: triangulation closeups (c1, left ear)
for k in EARS:
    z = TZ[(k, 'c1')]; sz = np.load('%s/%s_%s_branch.npz' % (SN, H['c1'], k)); V = z['V'].astype(float); T = z['Q']; Qq = sz['Q']; part = sz['part']; side_ = sz['side']
    FL = z['flagged']; reg = z['region']; rows = {r['quad']: r for r in RJ[(k, 'c1')]['flagged']['quads']}; flip = set(RJ[(k, 'c1')]['intersection_validation']['flipped_quads'])
    Ta = T.copy(); altT = z['alt_T']
    for i, f in enumerate(FL): Ta[2 * f:2 * f + 2] = altT[2 * i:2 * i + 2]
    fside = np.array([(set(side_[q].tolist()) - {''} or {'-'}).pop() for q in Qq]); fn = np.cross(V[Qq[:, 2]] - V[Qq[:, 0]], V[Qq[:, 3]] - V[Qq[:, 1]])
    cq = np.tile(GREY, (len(Qq), 1)); ct = np.tile(GREY, (len(T), 1)); ca = np.tile(GREY, (len(T), 1))
    for f in FL:
        r = rows[int(f)]; cq[f] = [0.95, 0.15, 0.1] if r['folded'] else [0.98, 0.6, 0.15]
        ct[2 * f:2 * f + 2] = [0.2, 0.45, 0.95] if int(f) in flip else FOLDC(r['fold_chosen_deg']); ca[2 * f:2 * f + 2] = FOLDC(r['fold_alternate_deg'])
    # camera per region: the most-folded flagged quad of the left ear that is visible along its own smooth normal (numpy ray cast against every
    # triangle within 25 cm); the view looks straight down that normal
    vn = np.zeros((len(V), 3)); tn = np.cross(V[T[:, 1]] - V[T[:, 0]], V[T[:, 2]] - V[T[:, 0]])
    for kk in range(3): np.add.at(vn, T[:, kk], tn)
    vn /= np.maximum(np.linalg.norm(vn, axis=1, keepdims=True), 1e-12)
    def visible(o, d):
        A0, B0, C0 = V[T[:, 0]], V[T[:, 1]], V[T[:, 2]]; sel = np.linalg.norm(A0 - o, axis=1) < 25; A0, B0, C0 = A0[sel], B0[sel], C0[sel]
        e1, e2 = B0 - A0, C0 - A0; h_ = np.cross(d, e2); a_ = (e1 * h_).sum(1); ok = np.abs(a_) > 1e-12; f_ = 1 / np.where(ok, a_, 1); s_ = o - A0
        u_ = f_ * (s_ * h_).sum(1); q_ = np.cross(s_, e1); v_ = f_ * (q_ @ d); t_ = f_ * (e2 * q_).sum(1)
        return not (ok & (u_ >= 0) & (v_ >= 0) & (u_ + v_ <= 1) & (t_ > 0.02)).any()
    vws = []
    for rg, names in (('cuff_root', ('cuff', 'root_junction')), ('lobe', ('lobe_junction',)), ('tip', ('upper_helix_tip',))):
        cand = sorted([f for f in FL if reg[f] in names and fside[f] == 'l'], key=lambda f: -rows[int(f)]['fold_chosen_deg'])
        cand += [f for f in range(len(Qq)) if reg[f] in names and fside[f] == 'l' and f not in set(FL)][:400]
        pick = None
        for f in cand:
            cc = V[Qq[f]].mean(0); d = unit(vn[Qq[f]].sum(0))
            if visible(cc + 0.01 * d, d): pick = (cc, d); break
        cc, d = pick if pick else (V[Qq[cand[0]]].mean(0), unit(vn[Qq[cand[0]]].sum(0)))
        vws.append((rg, d, cc, 0.9))
    wt = dict(WIRE_T='0.00008')
    job('A_%s_q' % k, V, Qq, cq, vws, wire=True, env=wt); job('A_%s_t' % k, V, T, ct, vws, wire=True, env=wt); job('A_%s_a' % k, V, Ta, ca, vws, wire=True, env=wt)
# ---------------- B / B2: shading on the baked triangles; B3 quads vs triangles vs rebuild
for k in EARS:
    for c in ('c1', 'c2'):
        z = TZ[(k, c)]; sz = np.load('%s/%s_%s_branch.npz' % (SN, H[c], k)); C, rd = cams(H[c]); vw = [(n_, *C[n_]) for n_ in ('etq', 'side', 'rq', 'rr', 'lr', 'zf')] + [('tip', *tipcam(sz['V'].astype(float), sz['side'], sz['part'], rd))]
        job('B_%s_%s' % (k, c), z['V'], z['Q'], None, vw, env=dict(RENDER_LIGHTING='STUDIO:rim.sl', RENDER_SPEC='1'))
        job('B2_%s_%s' % (k, c), z['V'], z['Q'], None, vw, env=dict(RENDER_LIGHTING='MATCAP:check_reflection_horizontal.exr'))
        if c == 'c1':
            v4 = [x for x in vw if x[0] in ('etq', 'side', 'rq', 'lr')]
            job('B3q_%s' % k, sz['V'], sz['Q'], None, v4, env=dict(RENDER_LIGHTING='MATCAP:check_reflection_horizontal.exr'))
            job('B3t_%s' % k, z['V'], z['Q'], None, v4, env=dict(RENDER_LIGHTING='MATCAP:check_reflection_horizontal.exr'))
            rb = RJ[(k, c)]['rebuild']['path']; job('B3r_%s' % k, np.load(rb)['V'], z['Q'], None, v4, env=dict(RENDER_LIGHTING='MATCAP:check_reflection_horizontal.exr'))
# ---------------- C: two worst poses
PSE = os.path.join(SN, 'pose')
def kabsch(A, B):
    A0, B0 = A - A.mean(0), B - B.mean(0); U_, _, Wt = np.linalg.svd(A0.T @ B0); dd = np.sign(np.linalg.det(Wt.T @ U_.T)); Rm = Wt.T @ np.diag([1, 1, dd]) @ U_.T; return Rm, B.mean(0) - Rm @ A.mean(0)
for k in EARS:
    for c in ('c1', 'c2'):
        z = TZ[(k, c)]; sz = np.load('%s/%s_%s_branch.npz' % (SN, H[c], k)); V0 = z['V'].astype(float); lv = np.nonzero(sz['side'] == 'l')[0]; C, rd = cams(H[c])
        flagc = np.tile(GREY, (len(z['Q']), 1)); flagc[np.r_[2 * z['flagged'], 2 * z['flagged'] + 1]] = [0.98, 0.6, 0.15]
        for pn in RJ[(k, c)]['worst_two_poses']:
            X = np.load('%s/%s_%s_%s.npy' % (PSE, H[c], k, pn)).astype(float); Rm, t = kabsch(V0[lv], X[lv])
            vw = [(n_, Rm @ C[n_][0], Rm @ C[n_][1] + t, C[n_][2]) for n_ in ('etq', 'lr')]; job('C_%s_%s_%s' % (k, c, pn), X, z['Q'], flagc, vw, env=dict(RENDER_LIGHTING='STUDIO:rim.sl', RENDER_SPEC='1'))
# ---------------- D: LOD
for k in EARS:
    for c in ('c1', 'c2'):
        C, rd = cams(H[c]); vw = [(n_, *C[n_]) for n_ in ('side', 'rq')]; z = TZ[(k, c)]
        job('D_%s_%s_src' % (k, c), z['V'], z['Q'], None, vw, env=dict(RENDER_LIGHTING='STUDIO:rim.sl', RENDER_SPEC='1'))
        for r_ in ('50', '25'):
            l = np.load('%s/%s_%s_lod%s.npz' % (PT, k, c, r_)); job('D_%s_%s_%s' % (k, c, r_), l['V'], l['Q'], None, vw, env=dict(RENDER_LIGHTING='STUDIO:rim.sl', RENDER_SPEC='1'))
with ThreadPoolExecutor(3) as ex: list(ex.map(lambda j: subprocess.run(j[0], env=j[1], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL), jobs))
# ---------------- compose
def sheet(fn, title, rows, heads, colw=300, note=None, lab_w=130):
    ncol = max(len(r[1]) for r in rows); nl = note.count('\n') + 1 if note else 0
    S = Image.new('RGB', (lab_w + ncol * colw, 84 + sum(colw + (24 if r[2] else 6) for r in rows) + 20 * nl + 12), 'white'); d = ImageDraw.Draw(S)
    d.text((12, 12), title, fill=(0, 0, 0), font=font(18, True)); y = 54
    for i, h_ in enumerate(heads): d.text((lab_w + i * colw + 4, y), h_, fill=(0, 0, 0), font=font(13, True))
    y += 24
    for lb, ims, cap in rows:
        d.text((8, y + colw // 2 - 20), lb, fill=(0, 0, 0), font=font(14, True))
        for i, im in enumerate(ims): S.paste(im.resize((colw, colw)), (lab_w + i * colw, y))
        y += colw
        if cap: d.text((lab_w + 4, y + 4), cap, fill=(40, 40, 40), font=font(12)); y += 24
        else: y += 6
    if note: d.multiline_text((12, y + 4), note, fill=(60, 60, 60), font=font(13))
    S.save(os.path.join(OUT, fn), quality=90)
def acap(k):
    f = RJ[(k, 'c1')]['flagged']; iv = RJ[(k, 'c1')]['intersection_validation']
    return 'flagged %d (folded %d) | fold chosen max %.0f deg | step-5 flips %d | crossings: fixed a-c %d, TRI-HV1 0' % (f['count'], f['folded'], f['fold_chosen_max'], len(iv['flipped_quads']), sum(iv['fixed_split_ac_crossings'].values()))
rowsA = []
for k in EARS:
    rowsA.append(('%s c1' % k, [img('A_%s_%s' % (k, s_), rg) for rg in ('cuff_root', 'lobe', 'tip') for s_ in ('q', 't', 'a')], acap(k)))
sheet('PT_A_triangulation_closeups.jpg', 'A. Triangulation closeups (c1, left ear): per region -- quads | baked TRI-HV1 triangles | alternate-diagonal diagnostic', rowsA,
      ['cuff/root quads', 'cuff/root TRI-HV1', 'cuff/root alternate', 'lobe quads', 'lobe TRI-HV1', 'lobe alternate', 'tip quads', 'tip TRI-HV1', 'tip alternate'], colw=230,
      note='quads: flagged quads red (folded) / orange (warped > 20 deg).  triangles: tint = fold across the diagonal (amber 20-60, orange 60-90, red > 90 deg); blue = diagonal flipped by step 5 (intersection validation).\nThe alternate panels show the other diagonal on every flagged quad: red there = the alternate would fold the surface (normal break / dent).')
VB = ['etq', 'side', 'rq', 'rr', 'lr', 'zf', 'tip']; HB = ['front 3/4', 'strict side', 'true rear 3/4', 'direct rear', 'lower-rear 3/4', 'lower-root closeup', 'upper helix / tip']
for fn, pre, title in (('PT_B_shading_grazing.jpg', 'B', 'B. Shading on the baked triangles -- grazing studio light (rim) + specular, smooth normals, no normal map'),
                       ('PT_B2_shading_zebra.jpg', 'B2', 'B2. Shading on the baked triangles -- reflection-stripe matcap (zebra): a stripe break = a normal break')):
    sheet(fn, title, [('%s %s' % (k, c), [img('%s_%s_%s' % (pre, k, c), v) for v in VB], None) for k in EARS for c in ('c1', 'c2')], HB, colw=260)
diffs = {}
rows3 = []
for k in EARS:
    dq = [np.asarray(ImageChops.difference(img('B3q_%s' % k, v), img('B3t_%s' % k, v))).mean() for v in ('etq', 'side', 'rq', 'lr')]
    dr = [int(np.asarray(ImageChops.difference(img('B3r_%s' % k, v), img('B3t_%s' % k, v))).max()) for v in ('etq', 'side', 'rq', 'lr')]; diffs[k] = dict(quad_vs_baked_mean_pixel_diff=[round(float(x), 3) for x in dq], rebuild_vs_baked_max_pixel_diff=dr)
    rows3 += [('%s quads' % k, [img('B3q_%s' % k, v) for v in ('etq', 'side', 'rq', 'lr')], None), ('%s TRI-HV1' % k, [img('B3t_%s' % k, v) for v in ('etq', 'side', 'rq', 'lr')], None),
              ('%s rebuild' % k, [img('B3r_%s' % k, v) for v in ('etq', 'side', 'rq', 'lr')], 'rebuild vs baked: max pixel difference %s' % dr)]
sheet('PT_B3_quads_vs_triangles_vs_rebuild.jpg', 'B3. Zebra matcap, c1: quads as displayed by a DCC | baked TRI-HV1 triangles | independent rebuild (same rule)', rows3, ['front 3/4', 'strict side', 'true rear 3/4', 'lower-rear 3/4'], colw=260)
json.dump(diffs, open(os.path.join(OUT, '..', 'board_pixel_diffs.json'), 'w'), indent=1)
rowsC = []
for k in EARS:
    for c in ('c1', 'c2'):
        ps = RJ[(k, c)]['worst_two_poses']; P = RJ[(k, c)]['poses']
        rowsC.append(('%s %s' % (k, c), [img('C_%s_%s_%s' % (k, c, pn), v) for pn in ps for v in ('etq', 'lr')],
                      ' | '.join('%s: inversions %d, contacts %d, flagged max normal change %.1f deg' % (pn, P[pn]['triangle_inversions'], P[pn]['new_contacts'], P[pn]['flagged_max_local_normal_change_deg']) for pn in ps)))
sheet('PT_C_pose_stress.jpg', 'C. Pose stress, baked triangles: two worst poses per ear; flagged quads orange', rowsC,
      ['worst pose: front 3/4', 'worst pose: lower-rear 3/4', '2nd pose: front 3/4', '2nd pose: lower-rear 3/4'], colw=280)
rowsD = []
for k in EARS:
    for c in ('c1', 'c2'):
        L = RJ[(k, c)]['lod']; P_, U_ = L['protected'], L['unconstrained']
        rowsD.append(('%s %s' % (k, c), [img('D_%s_%s_%s' % (k, c, r_), v) for r_ in ('src', '50', '25') for v in ('side', 'rq')],
                      'LOD-HV1 50 %%: drift %.3f cm, root %.3f, self-x %d | 25 %%: drift %.3f, root %.3f, self-x %d | non-manifold / zero-area %d / %d (unconstrained 25 %% self-x %d)' % (
                          P_['0.5']['ear_max_drift_source_to_lod_cm'], P_['0.5']['root_region_max_drift_cm'], P_['0.5']['ear_region_self_intersection_pairs'], P_['0.25']['ear_max_drift_source_to_lod_cm'],
                          P_['0.25']['root_region_max_drift_cm'], P_['0.25']['ear_region_self_intersection_pairs'], P_['0.25']['ear_region_nonmanifold_edges'] + P_['0.5']['ear_region_nonmanifold_edges'],
                          P_['0.25']['ear_region_zero_area_triangles'] + P_['0.5']['ear_region_zero_area_triangles'], U_['0.25']['ear_region_self_intersection_pairs'])))
sheet('PT_D_lod.jpg', 'D. LOD on the baked triangles -- LOD-HV1 (Decimate collapse, cuff / transition / junction ring protected): source | 50 % | 25 %', rowsD, ['source side', 'source rear 3/4', '50 % side', '50 % rear 3/4', '25 % side', '25 % rear 3/4'], colw=250)
print('BOARDS_DONE', sorted(os.listdir(OUT)))
