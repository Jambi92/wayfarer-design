# mf3_sheets.py WORK : RP3 Marchfolk v003 evidence sheets (order 103c832 §15), identical orthographic cameras per configuration (render_attr.py).
#  MF3_body_{M,F}      v003 clay front / rear / profile / 3-4; v002 | v003 wire full body and upper / lower body
#  MF3_closeups_{M,F}  face-orbit-mouth, shoulder / axilla, elbow, hand dorsal (MCP), hand palmar (thenar / hypothenar), ankle, foot dorsal (MTP), foot plantar:
#                      v002 wire | v003 wire | v003 pole map + counted rings (poles red, relocated vertices orange tint, inserted root rings green)
#  MF3_quality_{M,F}   T-4 heat (grey ok, orange angle outside 45-135, red aspect > 4, purple both) v002 | v003, face / hands / feet / body
#  MF3_density_{M,F}   edge-length / stature heat v002 | v003
#  MF3_overlay_{M,F}   v003 -> source deviation heat; v002 -> v003 vertex relocation heat; silhouette overlay source vs v003
#  MF3_deform_{M,F}    diagnostic poses v002 | v003 (red new self-x, magenta flip, purple fold)
#  MF3_knee            configuration-1 knee 90 / 140: source-rig knee centre | section-centroid candidate (v003)
#  MF3_core_diagram    family-core change diagram on the configuration-average surface: v002 poles (blue), v003 poles (red), relocation heat, root rings (green)
import sys, os, json, subprocess, numpy as np, scipy.sparse as sp
from PIL import Image, ImageDraw, ImageFont
W = sys.argv[1]; T = '/home/claude/wayfarer-design/tools/rac/rp/grask_rigprep_v001/render_attr.py'; BP = '/home/claude/stc/bin/python3'
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FN = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; f = lambda n, b=False: ImageFont.truetype(FB if b else FN, n)
OV = W + '/ov3'; SH = W + '/sheets3'; os.makedirs(OV, exist_ok=True); os.makedirs(SH, exist_ok=True)
CLAY = np.array([0.80, 0.77, 0.73])
def render(V, Q, col, tg, vs, wire='0', px=420):
    o = OV + '/%s.npz' % tg
    if not os.path.exists(OV + '/%s_%s.png' % (tg, vs.split(';')[-1].split(':')[0])):
        np.savez(o, V=V, Q=Q); np.save(o[:-4] + '_c.npy', np.asarray(col, np.float32))
        subprocess.run([BP, T, '--', o, o[:-4] + '_c.npy', OV, tg, vs, wire, str(px)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, env=dict(os.environ, WIRE_T='0.00012'))
def img(tg, v, cell): return Image.open('%s/%s_%s.png' % (OV, tg, v)).convert('RGB').resize((cell, cell), Image.LANCZOS)
def vs_(views): return ';'.join('%s:%s:%s:%g' % (n, ','.join('%.4f' % x for x in d), ','.join('%.3f' % x for x in c), h) for n, d, c, h in views)
def ramp(t):
    t = np.clip(t, 0, 1)[:, None]; return np.where(t < 0.5, (1 - 2 * t) * np.array([0.15, 0.35, 0.85]) + 2 * t * np.array([0.95, 0.9, 0.3]), (2 - 2 * t) * np.array([0.95, 0.9, 0.3]) + (2 * t - 1) * np.array([0.85, 0.1, 0.1]))
def quality(V, Q):
    ang = []
    for k in range(4):
        p0, p1, p2 = V[Q[:, (k - 1) % 4]], V[Q[:, k]], V[Q[:, (k + 1) % 4]]; u1 = p0 - p1; u2 = p2 - p1
        ang.append(np.degrees(np.arccos(np.clip((u1 * u2).sum(1) / np.linalg.norm(u1, axis=1) / np.linalg.norm(u2, axis=1), -1, 1))))
    ang = np.stack(ang, 1); sd = np.stack([np.linalg.norm(V[Q[:, (k + 1) % 4]] - V[Q[:, k]], axis=1) for k in range(4)], 1); asp = sd.max(1) / np.maximum(sd.min(1), 1e-9)
    return (ang.min(1) < 45) | (ang.max(1) > 135), asp > 4
def qcol(V, Q):
    a, b = quality(V, Q); c = np.tile(CLAY, (len(Q), 1)); c[a] = (0.95, 0.55, 0.1); c[b] = (0.85, 0.1, 0.1); c[a & b] = (0.55, 0.1, 0.7); return c
core = np.load(W + '/v3/core_final.npz'); n2 = int(core['n_v002']); moved = core['moved']; Q3 = core['Q']
for C in ('M', 'F'):
    cid = 'MF-%s-R' % C; nz = np.load('%s/src/%s_native.npz' % (W, cid)); v2 = np.load('%s/cand/%s_v002.npz' % (W, cid)); v3 = np.load('%s/cand/%s_v003.npz' % (W, cid)); m = json.loads(str(nz['meta']))
    Hd = {k: np.array(v) for k, v in m['heads'].items()}; V2, Q2 = v2['V'], v2['Q']; V3 = v3['V']; st = V3[:, 2].max()
    rel = np.zeros(len(V3)); rel[:n2] = np.linalg.norm(V3[:n2] - V2, axis=1)              # relocation of v002 vertices (cm)
    # ---- body
    c = np.array([0, 0, st / 2]); BV = [('front', (0, 1, 0), c, st * 0.52), ('rear', (0, -1, 0), c, st * 0.52), ('profile', (1, 0, 0), c, st * 0.52), ('q3', (0.7, 0.7, 0), c, st * 0.52)]
    UB = [('upper', (0, 1, 0), np.array([0, 0, st * 0.80]), st * 0.17), ('lower', (0, 1, 0), np.array([0, 0, st * 0.40]), st * 0.17)]
    render(V3, Q3, np.tile(CLAY, (len(Q3), 1)), 'b3_%s' % C, vs_(BV))
    render(V2, Q2, np.tile(CLAY, (len(Q2), 1)), 'w2_%s' % C, vs_(BV[:3:2] + UB), '1', 900); render(V3, Q3, np.tile(CLAY, (len(Q3), 1)), 'w3_%s' % C, vs_(BV[:3:2] + UB), '1', 900)
    cell = 330; S = Image.new('RGB', (4 * cell + 20, 80 + 3 * (cell + 24)), 'white'); d = ImageDraw.Draw(S)
    d.text((10, 8), 'Marchfolk %s v003 shared family core — clay (row 1); v002 | v003 wire front / profile (row 2); upper / lower body (row 3)' % cid, fill=(0, 0, 0), font=f(15, True))
    d.text((10, 32), 'v003 = v002 + %d root rings (%s; mirrored) + surface-constrained pole relocation + T-4 relaxation: %d verts / %d quads' % (len(json.loads(str(core['log']))['rings']), ', '.join(sorted({r['name'][:-2] for r in json.loads(str(core['log']))['rings']})), len(V3), len(Q3)), fill=(60, 60, 60), font=f(11))
    for j, v in enumerate(('front', 'rear', 'profile', 'q3')): S.paste(img('b3_%s' % C, v, cell), (10 + j * cell, 60))
    for row, views in ((1, ('front', 'profile')), (2, ('upper', 'lower'))):
        for j, (tg, v) in enumerate(((('w2_%s' % C), views[0]), (('w3_%s' % C), views[0]), (('w2_%s' % C), views[1]), (('w3_%s' % C), views[1]))):
            S.paste(img(tg, v, cell), (10 + j * cell, 84 + row * (cell + 24) - 0)); d.text((14 + j * cell, 66 + row * (cell + 24)), ('v002 ', 'v003 ', 'v002 ', 'v003 ')[j] + v, fill=(150, 20, 20), font=f(12, True))
    S.save(SH + '/MF3_body_%s.jpg' % C, quality=85)
    # ---- close-ups
    au3 = json.load(open('%s/audit/%s_v003_audit.json' % (W, cid))); au2 = json.load(open('%s/audit/%s_v002_audit.json' % (W, cid)))
    lz = np.load('%s/audit/%s_v003_loops.npz' % (W, cid), allow_pickle=True); loops = lz['loops']; jl = json.loads(str(lz['joint_loop_ids'])); poles3 = lz['poles']
    fr3 = json.load(open('%s/audit/%s_v003_face.json' % (W, cid))); fr2 = json.load(open('%s/audit/%s_v002_face.json' % (W, cid)))
    ring_v = np.arange(n2, len(V3))
    def polemap(ids, face=False):
        cv = np.tile(CLAY, (len(V3), 1)); t_ = np.clip(rel / 0.4, 0, 1)[:, None]; cv = (1 - t_) * cv + t_ * np.array([0.98, 0.6, 0.15])
        cv[ring_v] = (0.1, 0.7, 0.3); pal = ((0.05, 0.3, 0.95), (0.95, 0.85, 0.1))
        for li in ids:
            for i, x in enumerate(li):
                if face or i % 2 == 0: cv[loops[x]] = pal[i % 2]
        cv[poles3] = (0.9, 0.05, 0.05); return cv[Q3].mean(1)
    eye = np.array(m['eye_helpers']['helper-l-eye']); lm = json.load(open('%s/lm/%s_landmarks.json' % (W, cid)))['landmarks']; mc = np.array(lm['mouth_corner_l']['p_cm']) * [0, 1, 1]
    CU = [('face', (0.25, 1, 0.1), 0.5 * (eye + mc) + [-1.5, 0, 0], 7, [], None), ('shoulder', (0.6, 0.75, 0.2), Hd['upperarm_l'], 10, ['shoulder_l'], None),
          ('elbow', (0.95, 0.2, 0.1), Hd['lowerarm_l'], 7, ['elbow_l'], None),
          ('hand_dorsal', (0.95, 0.15, 0.1), Hd['hand_l'] + [0.5, 0, -7], 8, ['index_mcp_l', 'middle_mcp_l', 'ring_mcp_l', 'pinky_mcp_l', 'wrist_l'], None),
          ('hand_palmar', (-0.95, 0.15, -0.1), Hd['hand_l'] + [0.5, 0, -6], 8, ['thumb_mcp_l', 'pinky_mcp_l'], None),
          ('ankle', (0.9, 0.3, 0.1), Hd['foot_l'] + [0, 0, -2], 8, ['ankle_l'], None),
          ('foot_dorsal', (0.3, 0.5, 0.8), Hd['ball_l'] + [0, 1.0, 0], 7, ['toe1_j1_l', 'toe2_j1_l', 'toe3_j1_l', 'toe4_j1_l', 'toe5_j1_l'], None),
          ('foot_plantar', (0.2, 0.4, -0.9), Hd['ball_l'] + [0, 0.0, 0], 8, ['toe2_j3_l', 'toe3_j3_l', 'toe4_j2_l'], None)]
    cell = 250; S = Image.new('RGB', (3 * cell + 330, 46 + len(CU) * (cell + 8)), 'white'); d = ImageDraw.Draw(S)
    d.text((10, 8), 'Marchfolk %s close-ups — v002 wire | v003 wire | v003 poles (red) + relocation (orange) + root rings (green) + counted rings' % cid, fill=(0, 0, 0), font=f(13, True))
    def rn(k):
        return k.replace('_mcp_', '_knuckle_') if '_mcp_' in k and not k.startswith('thumb') else k.replace('thumb_mcp_', 'thumb_ip1_')
    for i, (nm, dr_, cc, h, js, _) in enumerate(CU):
        v = vs_([('c', dr_, cc, h)]); render(V2, Q2, np.tile(CLAY, (len(Q2), 1)), 'cu2_%s_%s' % (nm, C), v, '1', 500); render(V3, Q3, np.tile(CLAY, (len(Q3), 1)), 'cu3_%s_%s' % (nm, C), v, '1', 500)
        ids = [jl[rn(k)] for k in js if rn(k) in jl]
        if nm == 'face': ids = [[x['loop'] for x in fr3['mouth_rings']['rings']], fr3['orbit_rings_l']['loops'], fr3['orbit_rings_r']['loops']]
        render(V3, Q3, polemap(ids, nm == 'face'), 'cup_%s_%s' % (nm, C), v, '0', 500)
        y = 36 + i * (cell + 8)
        for j, tg in enumerate(('cu2_%s_%s' % (nm, C), 'cu3_%s_%s' % (nm, C), 'cup_%s_%s' % (nm, C))): S.paste(img(tg, 'c', cell), (10 + j * cell, y))
        d.text((3 * cell + 20, y + 2), nm, fill=(150, 20, 20), font=f(13, True)); yy = y + 22
        if nm == 'face':
            for t_ in ('mouth rings %d -> %d' % (fr2['mouth_rings']['count'], fr3['mouth_rings']['count']), 'orbit rings L %d -> %d, R %d -> %d' % (fr2['orbit_rings_l']['count'], fr3['orbit_rings_l']['count'], fr2['orbit_rings_r']['count'], fr3['orbit_rings_r']['count']),
                       'poles <2 cm of mouth %d, at corners %d' % (fr3['poles_within_2cm_of_mouth'], fr3['poles_at_mouth_corners']), 'poles <2 cm of each eye %d / %d' % (fr3['poles_within_2cm_of_eye_l'], fr3['poles_within_2cm_of_eye_r'])):
                d.text((3 * cell + 20, yy), t_, fill=(0, 0, 0), font=f(10)); yy += 14
        for k in js:
            a_, b_ = au2['joint_s7'][k], au3['joint_s7'][k]
            d.text((3 * cell + 20, yy), '%s: loops %d -> %d (need %d)' % (k, a_['loops'], b_['loops'], b_['required']), fill=(0, 0, 0), font=f(10)); yy += 13
            d.text((3 * cell + 30, yy), 'crease poles %d -> %d, <2 loops %d -> %d  %s' % (a_['poles_on_crease_line'], b_['poles_on_crease_line'], a_['poles_within_2_loops'], b_['poles_within_2_loops'],
                   'FIRM PASS' if b_['pass_firm'] else 'FIRM FAIL'), fill=(0, 110, 0) if b_['pass_firm'] else (180, 0, 0), font=f(10)); yy += 15
    S.save(SH + '/MF3_closeups_%s.jpg' % C, quality=85)
    # ---- T-4 quality
    QV = [('face', (0.25, 1, 0.1), eye + [-3, 0, -3], 8), ('hand', (0.95, 0.15, 0.1), Hd['hand_l'] + [0.5, 0, -7], 9), ('foot', (0.6, 0.6, 0.55), Hd['ball_l'] + [0, 1.5, 0], 8), ('body', (0, 1, 0), [0, 0, st / 2], st * 0.52)]
    render(V2, Q2, qcol(V2, Q2), 'q2_%s' % C, vs_(QV)); render(V3, Q3, qcol(V3, Q3), 'q3_%s' % C, vs_(QV))
    a2, b2 = quality(V2, Q2); a3, b3 = quality(V3, Q3)
    cell = 300; S = Image.new('RGB', (4 * cell + 20, 90 + 2 * (cell + 24)), 'white'); d = ImageDraw.Draw(S)
    d.text((10, 8), 'Marchfolk %s T-4 quad quality — v002 (row 1) | v003 (row 2): orange angle outside 45-135 deg, red aspect > 4, purple both' % cid, fill=(0, 0, 0), font=f(13, True))
    d.text((10, 28), 'violating quads (union): v002 %d / %d (%.2f %%)  ->  v003 %d / %d (%.2f %%); angle %d -> %d, aspect %d -> %d' % ((a2 | b2).sum(), len(Q2), 100 * (a2 | b2).mean(), (a3 | b3).sum(), len(Q3), 100 * (a3 | b3).mean(), a2.sum(), a3.sum(), b2.sum(), b3.sum()), fill=(0, 0, 0), font=f(12))
    for r_, tg in enumerate(('q2_%s' % C, 'q3_%s' % C)):
        for j, v in enumerate(('face', 'hand', 'foot', 'body')): S.paste(img(tg, v, cell), (10 + j * cell, 60 + r_ * (cell + 24)))
        d.text((12, 46 + r_ * (cell + 24)), ('v002', 'v003')[r_], fill=(150, 20, 20), font=f(12, True))
    S.save(SH + '/MF3_quality_%s.jpg' % C, quality=85)
    # ---- density
    def dens(Vx, Qx): return np.stack([np.linalg.norm(Vx[Qx[:, (k + 1) % 4]] - Vx[Qx[:, k]], axis=1) for k in range(4)], 1).mean(1) / st * 100
    render(V2, Q2, ramp(dens(V2, Q2) / 1.2), 'd2_%s' % C, vs_(BV[:2])); render(V3, Q3, ramp(dens(V3, Q3) / 1.2), 'd3_%s' % C, vs_(BV[:2]))
    d2 = au2['density_pct_of_stature']; d3 = au3['density_pct_of_stature']
    cell = 330; S = Image.new('RGB', (4 * cell + 20, 90 + cell + 10 * 16), 'white'); d = ImageDraw.Draw(S)
    d.text((10, 8), 'Marchfolk %s edge-length density (per-face mean edge / stature: blue 0 %% -> yellow 0.6 %% -> red >= 1.2 %%) — v002 | v003' % cid, fill=(0, 0, 0), font=f(14, True))
    for j, (tg, v, lab) in enumerate((('d2_%s' % C, 'front', 'v002 front'), ('d2_%s' % C, 'rear', 'v002 rear'), ('d3_%s' % C, 'front', 'v003 front'), ('d3_%s' % C, 'rear', 'v003 rear'))):
        S.paste(img(tg, v, cell), (10 + j * cell, 50)); d.text((14 + j * cell, 32), lab, fill=(150, 20, 20), font=f(12, True))
    y = 60 + cell
    for k in d3: d.text((10, y), '%-6s mean %% stature  v002 %.3f -> v003 %.3f   p90 %.3f -> %.3f   (ceiling %s)  %s' % (k, d2[k]['mean'], d3[k]['mean'], d2[k]['p90'], d3[k]['p90'], d3[k]['limit'], 'PASS' if d3[k]['pass_mean'] else 'FAIL'), fill=(0, 0, 0), font=f(12)); y += 16
    S.save(SH + '/MF3_density_%s.jpg' % C, quality=85)
    # ---- overlays
    import trimesh
    r6 = np.load('/home/claude/wayfarer-design/reviews/reference-assets/r6/%s_r6.npz' % cid); src = trimesh.Trimesh(r6['V'], r6['F'], process=False)
    _, dd, _ = trimesh.proximity.closest_point(src, V3); render(V3, Q3, ramp(dd[Q3].max(1) / 0.3), 'dev3_%s' % C, vs_(BV[:3]))
    render(V3, Q3, ramp(rel[Q3].max(1) / 0.5), 'rel3_%s' % C, vs_([('hand', (0.95, 0.15, 0.1), Hd['hand_l'] + [0.5, 0, -7], 9), ('foot', (0.6, 0.6, 0.55), Hd['ball_l'] + [0, 1.5, 0], 8), ('face', (0.25, 1, 0.1), eye + [-3, 0, -3], 8)]))
    an3 = json.load(open('%s/anat/%s_v003_anatomy.json' % (W, cid)))
    from PIL import Image as I2
    def sil(V, F, yaw, px=3.0, ss=4):
        a_ = np.radians(yaw); Rm = np.array([[np.cos(a_), -np.sin(a_), 0], [np.sin(a_), np.cos(a_), 0], [0, 0, 1]]); P = V @ Rm.T; q = px * ss; u = (P[:, 0] + 60) * q; v = (185 - P[:, 2]) * q
        im = I2.new('L', (int(120 * px) * ss, int(190 * px) * ss), 0); dr = ImageDraw.Draw(im)
        for t in F: dr.polygon([(u[t[0]], v[t[0]]), (u[t[1]], v[t[1]]), (u[t[2]], v[t[2]])], fill=255)
        return np.array(im, float).reshape(int(190 * px), ss, int(120 * px), ss).mean((1, 3)) >= 127.5
    TP = np.r_[Q3[:, [0, 1, 2]], Q3[:, [0, 2, 3]]]; A = sil(r6['V'], r6['F'], 0); Bm = sil(V3, TP, 0); o = np.full(A.shape + (3,), 255, np.uint8); o[A & Bm] = (170, 170, 170); o[A & ~Bm] = (220, 30, 30); o[Bm & ~A] = (30, 80, 220)
    cell = 300; S = Image.new('RGB', (6 * cell + 20, 120 + cell), 'white'); d = ImageDraw.Draw(S)
    d.text((10, 8), 'Marchfolk %s source / v002 / v003 — v003->source deviation (blue 0 -> red >= 3 mm) | v002->v003 relocation (blue 0 -> red >= 5 mm) hand, foot, face | silhouette source vs v003' % cid, fill=(0, 0, 0), font=f(12, True))
    for j, v in enumerate(('front', 'profile')): S.paste(img('dev3_%s' % C, v, cell), (10 + j * cell, 40))
    for j, v in enumerate(('hand', 'foot', 'face')): S.paste(img('rel3_%s' % C, v, cell), (10 + (2 + j) * cell, 40))
    S.paste(I2.fromarray(o).resize((int(cell * 120 / 190), cell)), (10 + 5 * cell, 40))
    dv = an3['deviation_prod_to_source']; sv = an3['deviation_source_to_prod']
    d.text((10, 50 + cell), 'v003 -> source max: body %.3f, head %.3f, ears %.3f, hands %.3f, feet %.3f mm | source -> v003 max: body %.3f, hands %.3f, feet %.3f mm | IoU front %.4f rear %.4f profiles %.4f / %.4f | stature %+.4f mm' %
           (dv['body']['max_mm'], dv['head']['max_mm'], dv['ears']['max_mm'], dv['hands']['max_mm'], dv['feet']['max_mm'], sv['body']['max_mm'], sv['hands']['max_mm'], sv['feet']['max_mm'],
            an3['silhouette_iou']['front'], an3['silhouette_iou']['rear'], an3['silhouette_iou']['profile_left'], an3['silhouette_iou']['profile_right'], an3['stature_diff_mm']), fill=(0, 0, 0), font=f(11))
    d.text((10, 68 + cell), 'relocated v002 vertices: %d (max %.2f mm, p95 %.2f mm of the relocated); every relocated vertex lies on the source surface (barycentric on one source triangle)' %
           ((rel > 1e-5).sum(), rel.max() * 10, np.percentile(rel[rel > 1e-5], 95) * 10), fill=(0, 0, 0), font=f(11))
    S.save(SH + '/MF3_overlay_%s.jpg' % C, quality=85)
    # ---- deformation v002 | v003
    D2 = json.load(open('%s/def/deform_%s_v002.json' % (W, cid)))['poses']; D3 = json.load(open('%s/def/deform_%s_v003.json' % (W, cid)))['poses']
    poses = list(D3); cell = 220; S = Image.new('RGB', (4 * cell + 20, 56 + ((len(poses) + 1) // 2) * (cell + 34)), 'white'); d = ImageDraw.Draw(S)
    d.text((10, 8), 'Marchfolk %s diagnostic deformation (source rig + weights, LBS); pairs v002 | v003' % cid, fill=(0, 0, 0), font=f(12, True)); d.text((10, 24), 'red new self-x, magenta flipped, purple new fold; x / f / fl = in-zone counts', fill=(60, 60, 60), font=f(10))
    for i, pn in enumerate(poses):
        z_ = D3[pn]['zone']; cc0 = np.array(Hd[z_[0]]); r = z_[1] * 1.3
        for j, (tg, Qx, DD) in enumerate((('v002', Q2, D2), ('v003', Q3, D3))):
            pz = np.load('%s/def/%s_%s_%s.npz' % (W, pn, cid, tg)); X = pz['V'].astype(float); col = np.tile(CLAY, (len(Qx), 1))
            if len(pz['selfx']): col[pz['selfx'].ravel()] = (0.9, 0.05, 0.05)
            col[pz['flip']] = (0.95, 0.2, 0.75)
            if len(pz['fold']): col[pz['fold'].ravel()] = (0.55, 0.0, 0.75)
            cc = X[np.linalg.norm(X - cc0, axis=1).argsort()[:200]].mean(0); dirv = (0.6, 0.75, 0.2) if 'trunk' not in pn else (0, 1, 0.1)
            render(X, Qx, col, 'def_%s_%s_%s' % (pn, C, tg), vs_([('v', dirv, cc, r)]), '0', 360)
            x0 = 10 + (i % 2) * 2 * cell + j * cell; y0 = 44 + (i // 2) * (cell + 34); S.paste(img('def_%s_%s_%s' % (pn, C, tg), 'v', cell), (x0, y0 + 30))
            dd_ = DD[pn]; d.text((x0 + 2, y0), '%s %s' % (pn, tg), fill=(150, 20, 20), font=f(10, True))
            d.text((x0 + 2, y0 + 13), 'x%d f%d fl%d p95 %.0f vol %+.0f%%' % (dd_['new_selfx_in_zone'], dd_['new_folds_in_zone'], dd_['flipped_in_zone'], dd_['strain_p95_pct'], dd_['zone_volume_pct'] or 0), fill=(0, 0, 0), font=f(10))
    S.save(SH + '/MF3_deform_%s.jpg' % C, quality=85); print('sheets', C, flush=True)
# ---- knee comparison (configuration 1, v003)
cid = 'MF-M-R'; nz = np.load('%s/src/%s_native.npz' % (W, cid)); m = json.loads(str(nz['meta'])); Hd = {k: np.array(v) for k, v in m['heads'].items()}
D3 = json.load(open('%s/def/deform_%s_v003.json' % (W, cid)))['poses']; DK = json.load(open('%s/knee/deform_%s_v003_kneeC.json' % (W, cid)))['poses']
cell = 300; S = Image.new('RGB', (4 * cell + 20, 90 + cell + 40), 'white'); d = ImageDraw.Draw(S)
d.text((10, 8), 'Configuration-1 knee centre diagnostic (v003, source weights, LBS): source-rig knee | section-centroid candidate (+1.92 cm lateral)', fill=(0, 0, 0), font=f(13, True))
for i, pn in enumerate(('knee_90_l', 'knee_140_l')):
    for j, (tg, dd_, dr) in enumerate((('src', D3[pn], 'def'), ('cand', DK[pn], 'knee'))):
        pz = np.load('%s/%s/%s_%s_%s.npz' % (W, dr, pn, cid, 'v003' if tg == 'src' else 'v003_kneeC')); X = pz['V'].astype(float); col = np.tile(CLAY, (len(Q3), 1))
        if len(pz['selfx']): col[pz['selfx'].ravel()] = (0.9, 0.05, 0.05)
        col[pz['flip']] = (0.95, 0.2, 0.75)
        cc = X[np.linalg.norm(X - Hd['calf_l'], axis=1).argsort()[:200]].mean(0); render(X, Q3, col, 'knee_%s_%s' % (pn, tg), vs_([('v', (0.6, 0.75, 0.2), cc, 13)]), '0', 400)
        x0 = 10 + (2 * i + j) * cell; S.paste(img('knee_%s_%s' % (pn, tg), 'v', cell), (x0, 60)); d.text((x0, 36), '%s %s' % (pn, 'source-rig knee' if tg == 'src' else 'centroid candidate'), fill=(150, 20, 20), font=f(11, True))
        d.text((x0, 66 + cell), 'self-x %d  folds %d  flips %d' % (dd_['new_selfx_in_zone'], dd_['new_folds_in_zone'], dd_['flipped_in_zone']), fill=(0, 0, 0), font=f(11))
        d.text((x0, 82 + cell), 'strain p95 %.0f %%  vol %+.1f %%' % (dd_['strain_p95_pct'], dd_['zone_volume_pct']), fill=(0, 0, 0), font=f(11))
S.save(SH + '/MF3_knee.jpg', quality=85)
# ---- family-core diagram on the average surface
vM = np.load('%s/cand/MF-M-R_v003.npz' % W); vF = np.load('%s/cand/MF-F-R_v003.npz' % W); A3 = 0.5 * (vM['V'] + vF['V'])
v2M = np.load('%s/cand/MF-M-R_v002.npz' % W); v2F = np.load('%s/cand/MF-F-R_v002.npz' % W); A2 = 0.5 * (v2M['V'] + v2F['V'])
E2 = np.sort(np.concatenate([Q2[:, [0, 1]], Q2[:, [1, 2]], Q2[:, [2, 3]], Q2[:, [3, 0]]]), 1); val2 = np.bincount(np.unique(E2, axis=0).ravel(), minlength=len(A2)); p2 = np.nonzero(val2 != 4)[0]
E3 = np.sort(np.concatenate([Q3[:, [0, 1]], Q3[:, [1, 2]], Q3[:, [2, 3]], Q3[:, [3, 0]]]), 1); val3 = np.bincount(np.unique(E3, axis=0).ravel(), minlength=len(A3)); p3 = np.nonzero(val3 != 4)[0]
relA = np.zeros(len(A3)); relA[:n2] = np.linalg.norm(A3[:n2] - A2, axis=1)
cv = np.tile(CLAY, (len(A3), 1)); t_ = np.clip(relA / 0.4, 0, 1)[:, None]; cv = (1 - t_) * cv + t_ * np.array([0.98, 0.6, 0.15]); cv[n2:] = (0.1, 0.7, 0.3); cv[p3] = (0.9, 0.05, 0.05)
cv2 = np.tile(CLAY, (len(A2), 1)); cv2[p2] = (0.1, 0.3, 0.95)
m = json.loads(str(np.load('%s/src/MF-M-R_native.npz' % W)['meta'])); Hd = {k: np.array(v) for k, v in m['heads'].items()}
DV = [('hand_d', (0.95, 0.15, 0.1), Hd['hand_l'] + [0.5, 0, -7], 8), ('hand_p', (-0.95, 0.15, -0.1), Hd['hand_l'] + [0.5, 0, -6], 8), ('ankle', (0.9, 0.3, 0.1), Hd['foot_l'] + [0, 0, -2], 8),
      ('foot_d', (0.3, 0.5, 0.8), Hd['ball_l'] + [0, 1.0, 0], 7), ('foot_p', (0.2, 0.4, -0.9), Hd['ball_l'], 8)]
render(A2, Q2, cv2[Q2].mean(1), 'diag2', vs_(DV), '1', 520); render(A3, Q3, cv[Q3].mean(1), 'diag3', vs_(DV), '1', 520)
cell = 280; S = Image.new('RGB', (5 * cell + 20, 120 + 2 * (cell + 24) + 120), 'white'); d = ImageDraw.Draw(S)
d.text((10, 8), 'Family-core change diagram (configuration-average surface; identical for both configurations): v002 poles blue (row 1) | v003 poles red, relocated vertices orange, root rings green (row 2)', fill=(0, 0, 0), font=f(12, True))
for r_, tg in enumerate(('diag2', 'diag3')):
    for j, v in enumerate(('hand_d', 'hand_p', 'ankle', 'foot_d', 'foot_p')): S.paste(img(tg, v, cell), (10 + j * cell, 50 + r_ * (cell + 24))); d.text((12 + j * cell, 34 + r_ * (cell + 24)), ('v002 ', 'v003 ')[r_] + v, fill=(150, 20, 20), font=f(11, True))
lg = json.loads(str(core['log'])); y = 60 + 2 * (cell + 24)
d.text((10, y), 'Topology change: %s' % ', '.join('%s (+%d verts)' % (r['name'], r['verts_added']) for r in lg['rings']), fill=(0, 0, 0), font=f(11)); y += 16
acc = [p for p in lg['poles'] if p['accepted']]; d.text((10, y), 'Pole relocations accepted: %d of %d candidate moves (stations: %s)' % (len(acc), len(lg['poles']), ', '.join(sorted({s if isinstance(s, str) else s[0] for p in acc for s in ([p['station']] if isinstance(p['station'], str) else p['station'][:1])}))), fill=(0, 0, 0), font=f(11)); y += 16
d.text((10, y), 'Poles: v002 %d (val3 %d / val5+ %d)  ->  v003 %d (val3 %d / val5+ %d); vertex order of v002 kept, ring vertices appended (%d -> %d)' % (len(p2), (val2 == 3).sum(), (val2 >= 5).sum(), len(p3), (val3 == 3).sum(), (val3 >= 5).sum(), len(A2), len(A3)), fill=(0, 0, 0), font=f(11))
S.save(SH + '/MF3_core_diagram.jpg', quality=85); print('done')
