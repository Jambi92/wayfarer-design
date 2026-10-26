# mf_sheets.py WORK : RP3 Marchfolk evidence sheets (order d18ff2a §15) for both configurations, identical cameras (render_attr.py, orthographic).
#  MF_body_{M,F}.jpg      : v002 clay front / rear / profile / 3-4 + native hm08 wire and v002 wire (front, profile)
#  MF_closeups_{M,F}.jpg  : face-orbit-mouth, shoulder/axilla, elbow, hand/fingers, pelvis/groin, knee, foot/toes -- native wire | v002 wire | v002 loops
#                           (closed rings counted for contract §7 in colour, poles red)
#  MF_density_{M,F}.jpg   : per-face mean edge length / stature heat (native | v002), front and rear, contract ceilings in the caption
#  MF_overlay_{M,F}.jpg   : production -> source deviation heat (v002) + silhouette overlays (source vs v002 masks) front / profile
#  MF_topology_map.jpg    : common topology: configuration 1 vs 2, faces coloured by face index (identical colouring = identical topology), face / hand / foot
#  MF_deform_{M,F}.jpg    : diagnostic key poses (native | v002) with new self-intersections (red), flipped faces (magenta), new folds (purple)
import sys, os, json, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
W = sys.argv[1]; T = '/home/claude/wayfarer-design/tools/rac/rp/grask_rigprep_v001/render_attr.py'; BP = '/home/claude/stc/bin/python3'
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FN = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; f = lambda n, b=False: ImageFont.truetype(FB if b else FN, n)
OV = W + '/ov'; SH = W + '/sheets'; os.makedirs(OV, exist_ok=True); os.makedirs(SH, exist_ok=True)
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
for C in ('M', 'F'):
    cid = 'MF-%s-R' % C; nz = np.load('%s/src/%s_native.npz' % (W, cid)); vz = np.load('%s/cand/%s_v002.npz' % (W, cid)); m = json.loads(str(nz['meta']))
    Hd = {k: np.array(v) for k, v in m['heads'].items()}; Vn, Qn = nz['V'], nz['Q']; Vv, Qv = vz['V'], vz['Q']; st = Vn[:, 2].max()
    # ---- body
    c = np.array([0, 0, st / 2]); BV = [('front', (0, 1, 0), c, st * 0.52), ('rear', (0, -1, 0), c, st * 0.52), ('profile', (1, 0, 0), c, st * 0.52), ('q3', (0.7, 0.7, 0), c, st * 0.52)]
    render(Vv, Qv, np.tile(CLAY, (len(Qv), 1)), 'body_%s_v002' % C, vs_(BV)); render(Vn, Qn, np.tile(CLAY, (len(Qn), 1)), 'bodyw_%s_n' % C, vs_(BV[:3:2]), '1', 700); render(Vv, Qv, np.tile(CLAY, (len(Qv), 1)), 'bodyw_%s_v' % C, vs_(BV[:3:2]), '1', 700)
    UB = [('upper', (0, 1, 0), np.array([0, 0, st * 0.80]), st * 0.17), ('lower', (0, 1, 0), np.array([0, 0, st * 0.40]), st * 0.17)]
    render(Vn, Qn, np.tile(CLAY, (len(Qn), 1)), 'bodyz_%s_n' % C, vs_(UB), '1', 900); render(Vv, Qv, np.tile(CLAY, (len(Qv), 1)), 'bodyz_%s_v' % C, vs_(UB), '1', 900)
    cell = 330; S = Image.new('RGB', (4 * cell + 20, 80 + 3 * (cell + 24)), 'white'); d = ImageDraw.Draw(S)
    d.text((10, 8), 'Marchfolk %s (%s) R-6 — v002 production candidate clay (row 1); native hm08 wire | v002 wire, front and profile (row 2)' % ('configuration 1' if C == 'M' else 'configuration 2', cid), fill=(0, 0, 0), font=f(15, True))
    d.text((10, 32), 'v002 = hm08 + one linear subdivision + 98 closed leg rings: %d verts / %d quads (native 13,380 / 13,378); surface = source surface' % (len(Vv), len(Qv)), fill=(60, 60, 60), font=f(12))
    for j, v in enumerate(('front', 'rear', 'profile', 'q3')): S.paste(img('body_%s_v002' % C, v, cell), (10 + j * cell, 60))
    for j, (tg, v) in enumerate((('bodyw_%s_n' % C, 'front'), ('bodyw_%s_v' % C, 'front'), ('bodyw_%s_n' % C, 'profile'), ('bodyw_%s_v' % C, 'profile'))):
        S.paste(img(tg, v, cell), (10 + j * cell, 84 + cell)); d.text((14 + j * cell, 66 + cell), ('native hm08', 'v002', 'native hm08', 'v002')[j], fill=(150, 20, 20), font=f(12, True))
    for j, (tg, v) in enumerate((('bodyz_%s_n' % C, 'upper'), ('bodyz_%s_v' % C, 'upper'), ('bodyz_%s_n' % C, 'lower'), ('bodyz_%s_v' % C, 'lower'))):
        S.paste(img(tg, v, cell), (10 + j * cell, 108 + 2 * cell)); d.text((14 + j * cell, 90 + 2 * cell), ('native hm08 upper body', 'v002 upper body', 'native hm08 lower body', 'v002 lower body')[j], fill=(150, 20, 20), font=f(12, True))
    S.save(SH + '/MF_body_%s.jpg' % C, quality=85)
    # ---- close-ups with loops
    au = np.load('%s/audit/%s_v002_loops.npz' % (W, cid), allow_pickle=True); loops = au['loops']; jl = json.loads(str(au['joint_loop_ids'])); poles_v = au['poles']
    an = np.load('%s/audit/%s_native_loops.npz' % (W, cid), allow_pickle=True); poles_n = an['poles']
    def loopcol(Vx, Qx, ids, poles, face_mode=False):
        # alternate two shades per joint so individual rings read as stripes
        cv = np.tile(CLAY, (len(Vx), 1)); pal = [((0.05, 0.3, 0.95), (0.95, 0.85, 0.1)), ((0.1, 0.65, 0.25), (0.95, 0.5, 0.75)), ((0.9, 0.45, 0.0), (0.2, 0.8, 0.9)), ((0.55, 0.15, 0.8), (0.95, 0.95, 0.95))]
        for k, li in enumerate(ids):
            for i, x in enumerate(li):
                if face_mode or i % 2 == 0: cv[loops[x]] = pal[k % 4][i % 2]
        cv[poles] = (0.9, 0.05, 0.05); return cv[Qx].mean(1)
    eye = np.array(m['eye_helpers']['helper-l-eye']); lm = json.load(open('%s/lm/%s_landmarks.json' % (W, cid)))['landmarks']; mc = np.array(lm['mouth_corner_l']['p_cm']) * [0, 1, 1]
    CU = [('face', (0.25, 1, 0.1), 0.5 * (eye + mc) + [-1.5, 0, 0], 7, []), ('shoulder', (0.6, 0.75, 0.2), Hd['upperarm_l'], 10, ['shoulder_l']), ('elbow', (0.95, 0.2, 0.1), Hd['lowerarm_l'], 7, ['elbow_l']),
          ('hand', (0.95, 0.15, 0.1), Hd['hand_l'] + [0.5, 0, -7], 9, ['index_knuckle_l', 'middle_knuckle_l', 'ring_knuckle_l', 'pinky_knuckle_l', 'wrist_l']),
          ('groin', (0.15, 1, 0.1), Hd['thigh_l'] + [-5, 0, -4], 13, ['hip_l']), ('knee', (0.3, 1, 0.1), Hd['calf_l'], 9, ['knee_l']), ('foot', (0.6, 0.6, 0.55), Hd['ball_l'] + [0, 1.5, 0], 8, ['ankle_l', 'toe1_j1_l', 'toe2_j1_l'])]
    cell = 260; S = Image.new('RGB', (3 * cell + 300, 70 + len(CU) * (cell + 8)), 'white'); d = ImageDraw.Draw(S)
    d.text((10, 8), 'Marchfolk %s close-ups — native hm08 wire | v002 wire | v002 joint loops (alternate counted rings coloured; poles red)' % cid, fill=(0, 0, 0), font=f(14, True))
    au_j = json.load(open('%s/audit/%s_v002_audit.json' % (W, cid)))['joint_s7']; an_j = json.load(open('%s/audit/%s_native_audit.json' % (W, cid)))['joint_s7']
    for i, (nm, dr_, cc, h, js) in enumerate(CU):
        v = vs_([('c', dr_, cc, h)]); render(Vn, Qn, np.tile(CLAY, (len(Qn), 1)), 'cu_%s_%s_n' % (nm, C), v, '1', 520); render(Vv, Qv, np.tile(CLAY, (len(Qv), 1)), 'cu_%s_%s_v' % (nm, C), v, '1', 520)
        ids = [jl[k] for k in js if k in jl]
        if nm == 'face':
            fr_ = json.load(open('%s/audit/%s_v002_face.json' % (W, cid))); ids = [[x['loop'] for x in fr_['mouth_rings']['rings']], fr_['orbit_rings_l']['loops'], fr_['orbit_rings_r']['loops']]
        render(Vv, Qv, loopcol(Vv, Qv, ids, poles_v, nm == 'face'), 'cul_%s_%s' % (nm, C), v, '0', 520)
        y = 40 + i * (cell + 8)
        for j, tg in enumerate(('cu_%s_%s_n' % (nm, C), 'cu_%s_%s_v' % (nm, C), 'cul_%s_%s' % (nm, C))): S.paste(img(tg, 'c', cell), (10 + j * cell, y))
        d.text((3 * cell + 20, y + 4), nm, fill=(150, 20, 20), font=f(13, True)); yy = y + 24
        if nm == 'face':
            fn_ = json.load(open('%s/audit/%s_native_face.json' % (W, cid)))
            for t_ in ('mouth rings %d -> %d' % (fn_['mouth_rings']['count'], fr_['mouth_rings']['count']), 'orbit rings L %d -> %d, R %d -> %d' % (fn_['orbit_rings_l']['count'], fr_['orbit_rings_l']['count'], fn_['orbit_rings_r']['count'], fr_['orbit_rings_r']['count']),
                       'poles within 2 cm of mouth: %d; at corners: %d' % (fr_['poles_within_2cm_of_mouth'], fr_['poles_at_mouth_corners']), 'eye sockets + lip slit open (hm08 inner pocket)', '(closed loops about the forward axis)'):
                d.text((3 * cell + 20, yy), t_, fill=(0, 0, 0), font=f(10)); yy += 14
        if nm in ('shoulder', 'groin'):
            d.text((3 * cell + 20, yy + 30), 'shoulder / hip loops are counted by the', fill=(90, 90, 90), font=f(10)); d.text((3 * cell + 20, yy + 43), 'band method (poles interrupt closed rings);', fill=(90, 90, 90), font=f(10)); d.text((3 * cell + 20, yy + 56), 'see joint_s7 in the audit JSON', fill=(90, 90, 90), font=f(10))
        for k in ([kk.replace('knuckle', 'mcp') for kk in js] if js else []):
            if k in au_j:
                a_ = au_j[k]; b_ = an_j.get(k, {}); d.text((3 * cell + 20, yy), '%s: loops %s -> %d (need %d)' % (k, b_.get('loops', '-'), a_['loops'], a_['required']), fill=(0, 0, 0), font=f(10)); yy += 13
                d.text((3 * cell + 30, yy), 'poles on crease %s -> %d %s' % (b_.get('poles_on_crease_line', '-'), a_['poles_on_crease_line'], 'PASS' if a_['pass_firm'] else 'FAIL'), fill=(0, 100, 0) if a_['pass_firm'] else (180, 0, 0), font=f(10)); yy += 15
    S.save(SH + '/MF_closeups_%s.jpg' % C, quality=85)
    # ---- density
    def dens(Vx, Qx): s_ = np.stack([np.linalg.norm(Vx[Qx[:, (k + 1) % 4]] - Vx[Qx[:, k]], axis=1) for k in range(4)], 1).mean(1); return s_ / st * 100
    dn, dv = dens(Vn, Qn), dens(Vv, Qv)
    render(Vn, Qn, ramp(dn / 1.2), 'den_%s_n' % C, vs_(BV[:2])); render(Vv, Qv, ramp(dv / 1.2), 'den_%s_v' % C, vs_(BV[:2]))
    au_d = json.load(open('%s/audit/%s_v002_audit.json' % (W, cid)))['density_pct_of_stature']; an_d = json.load(open('%s/audit/%s_native_audit.json' % (W, cid)))['density_pct_of_stature']
    cell = 330; S = Image.new('RGB', (4 * cell + 20, 90 + cell + 9 * 16), 'white'); d = ImageDraw.Draw(S)
    d.text((10, 8), 'Marchfolk %s edge-length density (per-face mean edge / stature: blue 0 %% -> yellow 0.6 %% -> red >= 1.2 %%)' % cid, fill=(0, 0, 0), font=f(14, True))
    for j, (tg, v, lab) in enumerate((('den_%s_n' % C, 'front', 'native front'), ('den_%s_n' % C, 'rear', 'native rear'), ('den_%s_v' % C, 'front', 'v002 front'), ('den_%s_v' % C, 'rear', 'v002 rear'))):
        S.paste(img(tg, v, cell), (10 + j * cell, 50)); d.text((14 + j * cell, 32), lab, fill=(150, 20, 20), font=f(12, True))
    y = 60 + cell
    for k in au_d: d.text((10, y), '%-6s mean %% stature  native %.3f  ->  v002 %.3f   (ceiling %s)  %s' % (k, an_d[k]['mean'], au_d[k]['mean'], au_d[k]['limit'], 'PASS' if au_d[k]['pass_mean'] else 'FAIL'), fill=(0, 0, 0), font=f(12)); y += 16
    S.save(SH + '/MF_density_%s.jpg' % C, quality=85)
    # ---- deviation / overlay
    import trimesh
    r6 = np.load('/home/claude/wayfarer-design/reviews/reference-assets/r6/%s_r6.npz' % cid); src = trimesh.Trimesh(r6['V'], r6['F'], process=False)
    _, dd, _ = trimesh.proximity.closest_point(src, Vv); fd = dd[Qv].max(1)
    render(Vv, Qv, ramp(fd / 0.3), 'dev_%s' % C, vs_(BV[:3]))
    an_a = json.load(open('%s/anat/%s_v002_anatomy.json' % (W, cid)))
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from PIL import Image as I2
    def sil(V, F, yaw, px=3.0, ss=4):
        a_ = np.radians(yaw); Rm = np.array([[np.cos(a_), -np.sin(a_), 0], [np.sin(a_), np.cos(a_), 0], [0, 0, 1]]); P = V @ Rm.T; q = px * ss; u = (P[:, 0] + 60) * q; v = (185 - P[:, 2]) * q
        im = I2.new('L', (int(120 * px) * ss, int(190 * px) * ss), 0); dr = ImageDraw.Draw(im)
        for t in F: dr.polygon([(u[t[0]], v[t[0]]), (u[t[1]], v[t[1]]), (u[t[2]], v[t[2]])], fill=255)
        return np.array(im, float).reshape(int(190 * px), ss, int(120 * px), ss).mean((1, 3)) >= 127.5
    TPv = np.r_[Qv[:, [0, 1, 2]], Qv[:, [0, 2, 3]]]; ovs = []
    for yaw in (0, 90):
        A = sil(r6['V'], r6['F'], yaw); B = sil(Vv, TPv, yaw); o = np.full(A.shape + (3,), 255, np.uint8); o[A & B] = (170, 170, 170); o[A & ~B] = (220, 30, 30); o[B & ~A] = (30, 80, 220); ovs.append(I2.fromarray(o))
    cell = 330; S = Image.new('RGB', (5 * cell + 20, 110 + cell), 'white'); d = ImageDraw.Draw(S)
    d.text((10, 8), 'Marchfolk %s source vs v002 — production->source deviation heat (blue 0 -> red >= 3 mm, max over face corners) | silhouette overlays at 3 px/cm (grey both, red source only, blue v002 only)' % cid, fill=(0, 0, 0), font=f(13, True))
    for j, v in enumerate(('front', 'rear', 'profile')): S.paste(img('dev_%s' % C, v, cell), (10 + j * cell, 40))
    for j, o in enumerate(ovs): S.paste(o.resize((int(cell * 120 / 190), cell)), (10 + (3 + j) * cell, 40))
    dv_ = an_a['deviation_prod_to_source']['body']; d.text((10, 50 + cell), 'v002 -> source: median %.3f / p95 %.3f / max %.3f mm (T-1 0.5 / 1.5 / 3.0); source -> v002 max %.4f mm; IoU front %.4f profile %.4f rear %.4f; stature diff %.4f mm' %
           (dv_['median_mm'], dv_['p95_mm'], dv_['max_mm'], an_a['deviation_source_to_prod']['body']['max_mm'], an_a['silhouette_iou']['front'], an_a['silhouette_iou']['profile_left'], an_a['silhouette_iou']['rear'], an_a['stature_diff_mm']), fill=(0, 0, 0), font=f(12))
    S.save(SH + '/MF_overlay_%s.jpg' % C, quality=85); print('sheets', C, flush=True)
# ---- common topology map
cell = 300; S = Image.new('RGB', (4 * cell + 20, 70 + 2 * (cell + 24)), 'white'); d = ImageDraw.Draw(S)
d.text((10, 8), 'Common topology: configuration 1 (MF-M-R) vs configuration 2 (MF-F-R), v002 faces coloured by face index (identical pattern = identical face list and vertex order)', fill=(0, 0, 0), font=f(13, True))
rng = np.random.default_rng(7)
for i, C in enumerate(('M', 'F')):
    vz = np.load('%s/cand/MF-%s-R_v002.npz' % (W, C)); Vv, Qv = vz['V'], vz['Q']; m = json.loads(str(np.load('%s/src/MF-%s-R_native.npz' % (W, C))['meta'])); Hd = {k: np.array(v) for k, v in m['heads'].items()}
    col = rng.random((len(Qv), 3)) * 0.7 + 0.25 if i == 0 else col
    eye = np.array(m['eye_helpers']['helper-l-eye'])
    v = vs_([('face', (0.25, 1, 0.1), eye + [-3, 0, -3], 8), ('hand', (0.95, 0.15, 0.1), Hd['hand_l'] + [0.5, 0, -7], 9), ('foot', (0.6, 0.6, 0.55), Hd['ball_l'] + [0, 1.5, 0], 8), ('body', (0, 1, 0), [0, 0, Vv[:, 2].max() / 2], 95)])
    render(Vv, Qv, col, 'topo_%s' % C, v, '0', 420)
    for j, vv in enumerate(('body', 'face', 'hand', 'foot')): S.paste(img('topo_%s' % C, vv, cell), (10 + j * cell, 40 + i * (cell + 24)))
    d.text((12, 28 + i * (cell + 24)), 'configuration %d' % (i + 1), fill=(150, 20, 20), font=f(12, True))
S.save(SH + '/MF_topology_map.jpg', quality=85)
# ---- deformation key poses
for C in ('M', 'F'):
    cid = 'MF-%s-R' % C; nz = np.load('%s/src/%s_native.npz' % (W, cid)); vz = np.load('%s/cand/%s_v002.npz' % (W, cid)); m = json.loads(str(nz['meta'])); Hd = {k: np.array(v) for k, v in m['heads'].items()}
    DN = json.load(open('%s/def/deform_%s_native.json' % (W, cid)))['poses']; DV = json.load(open('%s/def/deform_%s_v002.json' % (W, cid)))['poses']
    poses = list(DN); cell = 220; S = Image.new('RGB', (4 * cell + 20, 50 + ((len(poses) + 1) // 2) * (cell + 34)), 'white'); d = ImageDraw.Draw(S)
    d.text((10, 8), 'Marchfolk %s diagnostic deformation (source rig + weights, LBS); pairs native hm08 | v002' % cid, fill=(0, 0, 0), font=f(12, True)); d.text((10, 24), 'red = new self-intersection, magenta = flipped, purple = new fold; x = in-zone self-x pairs, f = folds, fl = flips', fill=(60, 60, 60), font=f(10))
    for i, pn in enumerate(poses):
        z_ = DN[pn]['zone']; c = np.array(Hd[z_[0]]); r = z_[1] * 1.3
        for j, (tg, Qx) in enumerate((('native', nz['Q']), ('v002', vz['Q']))):
            pz = np.load('%s/def/%s_%s_%s.npz' % (W, pn, cid, tg)); X = pz['V'].astype(float); col = np.tile(CLAY, (len(Qx), 1))
            if len(pz['selfx']): col[pz['selfx'].ravel()] = (0.9, 0.05, 0.05)
            col[pz['flip']] = (0.95, 0.2, 0.75)
            if len(pz['fold']): col[pz['fold'].ravel()] = (0.55, 0.0, 0.75)
            cc = X[np.linalg.norm(X - (X.mean(0) if False else c), axis=1).argsort()[:200]].mean(0)
            dirv = (0.6, 0.75, 0.2) if 'trunk' not in pn else (0, 1, 0.1)
            render(X, Qx, col, 'def_%s_%s_%s' % (pn, C, tg), vs_([('v', dirv, cc, r)]), '0', 360)
            x0 = 10 + (i % 2) * 2 * cell + j * cell; y0 = 40 + (i // 2) * (cell + 34); S.paste(img('def_%s_%s_%s' % (pn, C, tg), 'v', cell), (x0, y0 + 30))
            dd = (DN if j == 0 else DV)[pn]; d.text((x0 + 2, y0), '%s %s' % (pn, tg), fill=(150, 20, 20), font=f(10, True))
            d.text((x0 + 2, y0 + 13), 'x%d f%d fl%d p95 %.0f vol %+.0f%%' % (dd['new_selfx_in_zone'], dd['new_folds_in_zone'], dd['flipped_in_zone'], dd['strain_p95_pct'], dd['zone_volume_pct'] or 0), fill=(0, 0, 0), font=f(10))
    S.save(SH + '/MF_deform_%s.jpg' % C, quality=85)
print('done')
