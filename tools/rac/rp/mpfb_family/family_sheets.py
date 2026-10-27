# family_sheets.py WORK RACE ID1[:LABEL] ID2[:LABEL] : MPFB Family Propagation Standard v1 visual evidence set (identical orthographic cameras per configuration).
#  <RACE>_body_<ID>      clay front / rear / profile / 3-4; source (native hm08) wire | family wire, front / profile; upper / lower body
#  <RACE>_face_<ID>      head / face: source clay | family clay | family wire | family face rings (mouth + orbits) + face-ring / pole numbers
#  <RACE>_closeups_<ID>  shoulder, elbow, hand, pelvis, knee, foot: source wire | family wire | family counted loops; validator v2 status per station
#  <RACE>_overlay_<ID>   family -> source deviation heat + silhouette overlays (front / profile)
#  <RACE>_density_<ID>   edge-length / stature heat (source | family) + per-zone table
#  <RACE>_validator_<ID> 69-station validator v2 table (D1 + D3) with fallback statuses
#  <RACE>_deform_<ID>    limited deformation: source | family per pose
# Expects WORK/{src,cand,audit,lm,anat,def,val} as produced by the standard pipeline (run_eval.sh).
import sys, os, json, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
W, RACE = sys.argv[1], sys.argv[2]; IDS = [x.split(':') for x in sys.argv[3:]]
T = '/home/claude/wayfarer-design/tools/rac/rp/grask_rigprep_v001/render_attr.py'; BP = '/home/claude/stc/bin/python3'
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FN = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; f = lambda n, b=False: ImageFont.truetype(FB if b else FN, n)
OV = W + '/ov'; SH = W + '/sheets'; os.makedirs(OV, exist_ok=True); os.makedirs(SH, exist_ok=True); CLAY = np.array([0.80, 0.77, 0.73])
R6P = json.load(open(W + '/r6_paths.json'))
def render(V, Q, col, tg, vs, wire='0', px=420):
    o = OV + '/%s.npz' % tg
    if not os.path.exists(OV + '/%s_%s.png' % (tg, vs.split(';')[-1].split(':')[0])):
        np.savez(o, V=V, Q=Q); np.save(o[:-4] + '_c.npy', np.asarray(col, np.float32))
        subprocess.run([BP, T, '--', o, o[:-4] + '_c.npy', OV, tg, vs, wire, str(px)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, env=dict(os.environ, WIRE_T='0.00012'))
        os.remove(o); os.remove(o[:-4] + '_c.npy')
def img(tg, v, cell): return Image.open('%s/%s_%s.png' % (OV, tg, v)).convert('RGB').resize((cell, cell), Image.LANCZOS)
def vs_(views): return ';'.join('%s:%s:%s:%g' % (n, ','.join('%.4f' % x for x in d), ','.join('%.3f' % x for x in c), h) for n, d, c, h in views)
def ramp(t):
    t = np.clip(t, 0, 1)[:, None]; return np.where(t < 0.5, (1 - 2 * t) * np.array([0.15, 0.35, 0.85]) + 2 * t * np.array([0.95, 0.9, 0.3]), (2 - 2 * t) * np.array([0.95, 0.9, 0.3]) + (2 * t - 1) * np.array([0.85, 0.1, 0.1]))
for cid, lab in IDS:
    nz = np.load('%s/src/%s_native.npz' % (W, cid)); fz = np.load('%s/cand/%s_fam.npz' % (W, cid)); m = json.loads(str(nz['meta'])); Hd = {k: np.array(v) for k, v in m['heads'].items()}
    Vn, Qn, Vf, Qf = nz['V'], nz['Q'], fz['V'], fz['Q']; st = Vn[:, 2].max() - Vn[:, 2].min()
    VS = os.environ.get('FAM_VAL', ''); VL = os.environ.get('FAM_VAL_LABEL', 'D1 + D3')   # e.g. FAM_VAL=_D4_D5 FAM_VAL_LABEL='D1 + D3 + D4 + D5' (authoritative since 78a109f)
    val = json.load(open('%s/val/%s_fam_validator_v2%s.json' % (W, cid, VS)))['stations']; au = json.load(open('%s/audit/%s_fam_audit.json' % (W, cid))); aun = json.load(open('%s/audit/%s_native_audit.json' % (W, cid)))
    an = json.load(open('%s/anat/%s_fam_anatomy.json' % (W, cid))); fr = json.load(open('%s/audit/%s_fam_face.json' % (W, cid))); frn = json.load(open('%s/audit/%s_native_face.json' % (W, cid)))
    lz = np.load('%s/audit/%s_fam_loops.npz' % (W, cid), allow_pickle=True); loops = lz['loops']; jl = json.loads(str(lz['joint_loop_ids'])); poles = lz['poles']
    # ---- body
    c = np.array([0, 0, st / 2]); BV = [('front', (0, 1, 0), c, st * 0.52), ('rear', (0, -1, 0), c, st * 0.52), ('profile', (1, 0, 0), c, st * 0.52), ('q3', (0.7, 0.7, 0), c, st * 0.52)]
    UB = [('upper', (0, 1, 0), np.array([0, 0, st * 0.80]), st * 0.17), ('lower', (0, 1, 0), np.array([0, 0, st * 0.40]), st * 0.17)]
    render(Vf, Qf, np.tile(CLAY, (len(Qf), 1)), 'b_%s' % cid, vs_(BV)); render(Vn, Qn, np.tile(CLAY, (len(Qn), 1)), 'wn_%s' % cid, vs_(BV[:3:2] + UB), '1', 900); render(Vf, Qf, np.tile(CLAY, (len(Qf), 1)), 'wf_%s' % cid, vs_(BV[:3:2] + UB), '1', 900)
    cell = 330; S = Image.new('RGB', (4 * cell + 20, 80 + 3 * (cell + 24)), 'white'); d = ImageDraw.Draw(S)
    d.text((10, 8), '%s %s (%s) — frozen MPFB family base fitted to the accepted source: clay (row 1); source hm08 | family wire (rows 2-3)' % (RACE, cid, lab), fill=(0, 0, 0), font=f(14, True))
    d.text((10, 32), 'family topology %d verts / %d quads, face hash %s…; source hm08 13,380 / 13,378; stature %.2f cm' % (len(Vf), len(Qf), fz['log'] and json.loads(str(fz['log']))['checks']['frozen_face_topology_hash'][:8], st), fill=(60, 60, 60), font=f(12))
    for j, v in enumerate(('front', 'rear', 'profile', 'q3')): S.paste(img('b_%s' % cid, v, cell), (10 + j * cell, 60))
    for row, views in ((1, ('front', 'profile')), (2, ('upper', 'lower'))):
        for j, (tg, v) in enumerate((('wn_%s' % cid, views[0]), ('wf_%s' % cid, views[0]), ('wn_%s' % cid, views[1]), ('wf_%s' % cid, views[1]))):
            S.paste(img(tg, v, cell), (10 + j * cell, 84 + row * (cell + 24))); d.text((14 + j * cell, 66 + row * (cell + 24)), ('source ', 'family ', 'source ', 'family ')[j] + v, fill=(150, 20, 20), font=f(12, True))
    S.save(SH + '/%s_body_%s.jpg' % (RACE, cid), quality=85)
    # ---- face
    eye = np.array(m['eye_helpers']['helper-l-eye']); lm = json.load(open('%s/lm/%s_fam_landmarks.json' % (W, cid)))['landmarks']; mc = np.array(lm['mouth_corner_l']['p_cm']) * [0, 1, 1]
    hc = 0.5 * (eye * [0, 1, 1] + mc) + [0, -1.0, 0.5]; FV = [('front', (0, 1, 0.05), hc, 9), ('q3', (0.6, 0.8, 0.05), hc, 9), ('profile', (1, 0.05, 0), hc + [0, -3, 0], 11)]
    render(Vn, Qn, np.tile(CLAY, (len(Qn), 1)), 'fn_%s' % cid, vs_(FV)); render(Vf, Qf, np.tile(CLAY, (len(Qf), 1)), 'ff_%s' % cid, vs_(FV)); render(Vf, Qf, np.tile(CLAY, (len(Qf), 1)), 'fw_%s' % cid, vs_(FV[:1]), '1', 700)
    cv = np.tile(CLAY, (len(Vf), 1)); pal = ((0.05, 0.3, 0.95), (0.95, 0.85, 0.1))
    for li in ([x['loop'] for x in fr['mouth_rings']['rings']], fr['orbit_rings_l']['loops'], fr['orbit_rings_r']['loops']):
        for i, x in enumerate(li): cv[loops[x]] = pal[i % 2]
    cv[poles] = (0.9, 0.05, 0.05); render(Vf, Qf, cv[Qf].mean(1), 'fr_%s' % cid, vs_(FV[:1]), '0', 700)
    cell = 320; S = Image.new('RGB', (4 * cell + 20, 110 + 2 * (cell + 24)), 'white'); d = ImageDraw.Draw(S)
    d.text((10, 8), '%s %s head / face — source (accepted %s) clay | family clay, front / 3-4 / profile; family wire; family face rings (poles red)' % (RACE, cid, lab), fill=(0, 0, 0), font=f(13, True))
    for j, v in enumerate(('front', 'q3', 'profile')): S.paste(img('fn_%s' % cid, v, cell), (10 + j * cell, 40)); d.text((14 + j * cell, 44), 'source ' + v, fill=(150, 20, 20), font=f(11, True))
    S.paste(img('fw_%s' % cid, 'front', cell), (10 + 3 * cell, 40)); d.text((14 + 3 * cell, 44), 'family wire', fill=(150, 20, 20), font=f(11, True))
    for j, v in enumerate(('front', 'q3', 'profile')): S.paste(img('ff_%s' % cid, v, cell), (10 + j * cell, 64 + cell)); d.text((14 + j * cell, 68 + cell), 'family ' + v, fill=(150, 20, 20), font=f(11, True))
    S.paste(img('fr_%s' % cid, 'front', cell), (10 + 3 * cell, 64 + cell)); d.text((14 + 3 * cell, 68 + cell), 'family face rings', fill=(150, 20, 20), font=f(11, True))
    hv = an['deviation_prod_to_source']['head']; hs = an['deviation_source_to_prod']['head']
    d.text((10, 76 + 2 * cell), 'head zone family->source median / p95 / max %.3f / %.3f / %.3f mm; source->family max %.3f mm (T-2 0.3 / 0.8 / 1.5) | mouth rings %d (source %d), orbit rings %d / %d (source %d / %d), poles at mouth corners %d, within 2 cm of mouth %d' %
           (hv['median_mm'], hv['p95_mm'], hv['max_mm'], hs['max_mm'], fr['mouth_rings']['count'], frn['mouth_rings']['count'], fr['orbit_rings_l']['count'], fr['orbit_rings_r']['count'], frn['orbit_rings_l']['count'], frn['orbit_rings_r']['count'], fr['poles_at_mouth_corners'], fr['poles_within_2cm_of_mouth']), fill=(0, 0, 0), font=f(11))
    S.save(SH + '/%s_face_%s.jpg' % (RACE, cid), quality=85)
    # ---- close-ups
    def loopcol(ids):
        cv = np.tile(CLAY, (len(Vf), 1)); pl = [((0.05, 0.3, 0.95), (0.95, 0.85, 0.1)), ((0.1, 0.65, 0.25), (0.95, 0.5, 0.75))]
        for k, li in enumerate(ids):
            for i, x in enumerate(li):
                if i % 2 == 0: cv[loops[x]] = pl[k % 2][0]
        cv[poles] = (0.9, 0.05, 0.05); return cv[Qf].mean(1)
    rn = lambda k: k.replace('_mcp_', '_knuckle_') if ('_mcp_' in k and not k.startswith('thumb')) else k.replace('thumb_mcp_', 'thumb_ip1_')
    CU = [('shoulder', (0.6, 0.75, 0.2), Hd['upperarm_l'], 12, ['shoulder_l']), ('elbow', (0.95, 0.2, 0.1), Hd['lowerarm_l'], 9, ['elbow_l']),
          ('hand', (0.95, 0.15, 0.1), Hd['hand_l'] + [0.5, 0, -8], 11, ['index_mcp_l', 'middle_mcp_l', 'ring_mcp_l', 'pinky_mcp_l', 'thumb_mcp_l', 'wrist_l']),
          ('pelvis', (0.15, 1, 0.1), Hd['thigh_l'] + [-6, 0, -4], 16, ['hip_l']), ('knee', (0.3, 1, 0.1), Hd['calf_l'], 11, ['knee_l']),
          ('foot', (0.6, 0.6, 0.55), Hd['ball_l'] + [0, 1.5, 0], 10, ['ankle_l', 'toe1_j1_l', 'toe2_j1_l', 'toe3_j1_l', 'toe3_j3_l', 'toe4_j2_l', 'toe5_j1_l'])]
    cell = 250; S = Image.new('RGB', (3 * cell + 420, 40 + len(CU) * (cell + 8)), 'white'); d = ImageDraw.Draw(S)
    d.text((10, 8), '%s %s close-ups — source hm08 wire | family wire | family counted loops (poles red); validator v2 (%s) per station' % (RACE, cid, VL), fill=(0, 0, 0), font=f(13, True))
    for i, (nm, dr_, cc, h, js) in enumerate(CU):
        v = vs_([('c', dr_, cc, h)]); render(Vn, Qn, np.tile(CLAY, (len(Qn), 1)), 'cn_%s_%s' % (nm, cid), v, '1', 500); render(Vf, Qf, np.tile(CLAY, (len(Qf), 1)), 'cf_%s_%s' % (nm, cid), v, '1', 500)
        render(Vf, Qf, loopcol([jl[rn(k)] for k in js if rn(k) in jl]), 'cl_%s_%s' % (nm, cid), v, '0', 500)
        y = 34 + i * (cell + 8)
        for j, tg in enumerate(('cn_%s_%s' % (nm, cid), 'cf_%s_%s' % (nm, cid), 'cl_%s_%s' % (nm, cid))): S.paste(img(tg, 'c', cell), (10 + j * cell, y))
        d.text((3 * cell + 20, y + 2), nm, fill=(150, 20, 20), font=f(13, True)); yy = y + 22
        for k in js:
            r = val[k]; ok = r['firm_D1_D3']
            d.text((3 * cell + 20, yy), '%s: loops %d (need %d), crease own %d / all %d' % (k, r['loops_v2'], r['required'], len(r['crease_poles_own_digit']), len(r['crease_poles'])), fill=(0, 0, 0), font=f(10)); yy += 13
            d.text((3 * cell + 30, yy), r['status_D1_D3'], fill=(0, 110, 0) if ok else (180, 0, 0), font=f(10)); yy += 15
    S.save(SH + '/%s_closeups_%s.jpg' % (RACE, cid), quality=85)
    # ---- overlay
    import trimesh
    r6 = np.load(R6P[cid]); src = trimesh.Trimesh(r6['V'], r6['F'], process=False); _, dd, _ = trimesh.proximity.closest_point(src, Vf)
    render(Vf, Qf, ramp(dd[Qf].max(1) / 0.3), 'dev_%s' % cid, vs_(BV[:3]))
    def sil(V, F, yaw, px=3.0, ss=4):
        a_ = np.radians(yaw); Rm = np.array([[np.cos(a_), -np.sin(a_), 0], [np.sin(a_), np.cos(a_), 0], [0, 0, 1]]); P = V @ Rm.T; q = px * ss; u = (P[:, 0] + 70) * q; v = (220 - P[:, 2]) * q
        im = Image.new('L', (int(140 * px) * ss, int(225 * px) * ss), 0); dr = ImageDraw.Draw(im)
        for t in F: dr.polygon([(u[t[0]], v[t[0]]), (u[t[1]], v[t[1]]), (u[t[2]], v[t[2]])], fill=255)
        return np.array(im, float).reshape(int(225 * px), ss, int(140 * px), ss).mean((1, 3)) >= 127.5
    TP = np.r_[Qf[:, [0, 1, 2]], Qf[:, [0, 2, 3]]]; ovs = []
    for yaw in (0, 90):
        A = sil(r6['V'], r6['F'], yaw); B = sil(Vf, TP, yaw); o = np.full(A.shape + (3,), 255, np.uint8); o[A & B] = (170, 170, 170); o[A & ~B] = (220, 30, 30); o[B & ~A] = (30, 80, 220); ovs.append(Image.fromarray(o))
    cell = 330; S = Image.new('RGB', (5 * cell + 20, 110 + cell), 'white'); d = ImageDraw.Draw(S)
    d.text((10, 8), '%s %s source vs family — family->source deviation heat (blue 0 -> red >= 3 mm) | silhouette overlays 3 px/cm (grey both, red source only, blue family only)' % (RACE, cid), fill=(0, 0, 0), font=f(13, True))
    for j, v in enumerate(('front', 'rear', 'profile')): S.paste(img('dev_%s' % cid, v, cell), (10 + j * cell, 40))
    for j, o in enumerate(ovs): S.paste(o.resize((int(cell * 140 / 225), cell)), (10 + (3 + j) * cell, 40))
    dv_ = an['deviation_prod_to_source']; sv_ = an['deviation_source_to_prod']
    d.text((10, 50 + cell), 'family->source median %.3f / p95 %.3f / max %.3f mm (T-1 0.5 / 1.5 / 3.0); identity max head %.3f ears %.3f hands %.3f feet %.3f (T-2 1.5); source->family max %.3f; IoU front %.4f rear %.4f profiles %.4f / %.4f; stature %+.3f mm' %
           (dv_['body']['median_mm'], dv_['body']['p95_mm'], dv_['body']['max_mm'], dv_['head']['max_mm'], dv_['ears']['max_mm'], dv_['hands']['max_mm'], dv_['feet']['max_mm'], sv_['body']['max_mm'],
            an['silhouette_iou']['front'], an['silhouette_iou']['rear'], an['silhouette_iou']['profile_left'], an['silhouette_iou']['profile_right'], an['stature_diff_mm']), fill=(0, 0, 0), font=f(11))
    S.save(SH + '/%s_overlay_%s.jpg' % (RACE, cid), quality=85)
    # ---- density
    def dens(Vx, Qx): return np.stack([np.linalg.norm(Vx[Qx[:, (k + 1) % 4]] - Vx[Qx[:, k]], axis=1) for k in range(4)], 1).mean(1) / st * 100
    render(Vn, Qn, ramp(dens(Vn, Qn) / 1.2), 'dn_%s' % cid, vs_(BV[:2])); render(Vf, Qf, ramp(dens(Vf, Qf) / 1.2), 'df_%s' % cid, vs_(BV[:2]))
    cell = 330; S = Image.new('RGB', (4 * cell + 20, 90 + cell + 10 * 16), 'white'); d = ImageDraw.Draw(S)
    d.text((10, 8), '%s %s edge-length density (per-face mean edge / stature: blue 0 %% -> yellow 0.6 %% -> red >= 1.2 %%) — source hm08 | family' % (RACE, cid), fill=(0, 0, 0), font=f(14, True))
    for j, (tg, v, lb) in enumerate((('dn_%s' % cid, 'front', 'source front'), ('dn_%s' % cid, 'rear', 'source rear'), ('df_%s' % cid, 'front', 'family front'), ('df_%s' % cid, 'rear', 'family rear'))):
        S.paste(img(tg, v, cell), (10 + j * cell, 50)); d.text((14 + j * cell, 32), lb, fill=(150, 20, 20), font=f(12, True))
    y = 60 + cell; dn_ = aun['density_pct_of_stature']; df_ = au['density_pct_of_stature']
    for k in df_: d.text((10, y), '%-6s mean %% stature  source %.3f -> family %.3f   p90 %.3f   (ceiling %s)  %s' % (k, dn_[k]['mean'], df_[k]['mean'], df_[k]['p90'], df_[k]['limit'], 'PASS' if df_[k]['pass_mean'] else 'FAIL'), fill=(0, 0, 0), font=f(12)); y += 16
    S.save(SH + '/%s_density_%s.jpg' % (RACE, cid), quality=85)
    # ---- validator table
    rows = sorted(val.items()); S = Image.new('RGB', (1500, 70 + (len(rows) // 2 + 1) * 15), 'white'); d = ImageDraw.Draw(S)
    d.text((10, 8), '%s %s — 69-station §7 validator v2 (%s); legacy|D1|verdict, loops (need), crease poles all / own digit' % (RACE, cid, VL), fill=(0, 0, 0), font=f(12, True))
    for i, (k, r) in enumerate(rows):
        x0 = 10 + (i % 2) * 745; y0 = 34 + (i // 2) * 15; col = (0, 110, 0) if r['status_D1_D3'] == 'PASS' else ((0, 70, 170) if r['firm_D1_D3'] else (180, 0, 0))
        d.text((x0, y0), '%-13s %s|%s|%s  loops %d (%d)  crease %d/%d  %s' % (k, 'P' if r['firm_legacy'] else 'F', 'P' if r['firm_D1'] else 'F', 'P' if r['firm_D1_D3'] else 'F', r['loops_v2'], r['required'], len(r['crease_poles']), len(r['crease_poles_own_digit']), r['status_D1_D3']), fill=col, font=f(10))
    S.save(SH + '/%s_validator_%s.jpg' % (RACE, cid), quality=88)
    # ---- deformation source | family
    DN = json.load(open('%s/def/deform_%s_native.json' % (W, cid)))['poses']; DF = json.load(open('%s/def/deform_%s_fam.json' % (W, cid)))['poses']; poses = list(DF)
    cell = 220; S = Image.new('RGB', (4 * cell + 20, 56 + ((len(poses) + 1) // 2) * (cell + 34)), 'white'); d = ImageDraw.Draw(S)
    d.text((10, 8), '%s %s limited deformation (source rig + weights, LBS); pairs source hm08 | family' % (RACE, cid), fill=(0, 0, 0), font=f(12, True)); d.text((10, 24), 'red new self-x, magenta flipped, purple new fold; x / f / fl = in-zone counts', fill=(60, 60, 60), font=f(10))
    for i, pn in enumerate(poses):
        z_ = DF[pn]['zone']; c0 = np.array(Hd[z_[0]]); r = z_[1] * 1.3
        for j, (tg, Qx, DD) in enumerate((('native', Qn, DN), ('fam', Qf, DF))):
            pz = np.load('%s/def/%s_%s_%s.npz' % (W, pn, cid, tg)); X = pz['V'].astype(float); col = np.tile(CLAY, (len(Qx), 1))
            if len(pz['selfx']): col[pz['selfx'].ravel()] = (0.9, 0.05, 0.05)
            col[pz['flip']] = (0.95, 0.2, 0.75)
            if len(pz['fold']): col[pz['fold'].ravel()] = (0.55, 0.0, 0.75)
            cc = X[np.linalg.norm(X - c0, axis=1).argsort()[:200]].mean(0); dirv = (0.6, 0.75, 0.2) if 'trunk' not in pn else (0, 1, 0.1)
            render(X, Qx, col, 'def_%s_%s_%s' % (pn, cid, tg), vs_([('v', dirv, cc, r)]), '0', 360)
            x0 = 10 + (i % 2) * 2 * cell + j * cell; y0 = 44 + (i // 2) * (cell + 34); S.paste(img('def_%s_%s_%s' % (pn, cid, tg), 'v', cell), (x0, y0 + 30)); dd_ = DD[pn]
            d.text((x0 + 2, y0), '%s %s' % (pn, 'source' if tg == 'native' else 'family'), fill=(150, 20, 20), font=f(10, True))
            d.text((x0 + 2, y0 + 13), 'x%d f%d fl%d p95 %.0f vol %+.0f%%' % (dd_['new_selfx_in_zone'], dd_['new_folds_in_zone'], dd_['flipped_in_zone'], dd_['strain_p95_pct'], dd_['zone_volume_pct'] or 0), fill=(0, 0, 0), font=f(10))
    S.save(SH + '/%s_deform_%s.jpg' % (RACE, cid), quality=85); print('sheets', cid, flush=True)
