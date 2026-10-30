# du2_sheets.py WORK OUT : RP4 v002 revision / closure boards (order 8080f9f §15). Neutral clay, orthographic, workbench renders (render_attr.py via hv_ear_quick).
#   A  thumb MCP revision: v005 | rejected v001 prototype | v002 (wire; branch quads blue, aspect > 4 red, counted validator rings dark blue) on 122 / 137 / c2,
#      plus a v002 aspect heat column
#   B  jaw-neck reroute: before / after wire with poles (red = valence 5, green = valence 3) and the validator neck crease band (amber); v002 surface-deviation heat
#      (vertex distance to the v005 surface, 0 -> 0.5 mm) on 122 / 137 / 152 / c2
#   C  final central candidates DU_M / DU_F_REF_RP4_v001: front / 3/4 / side / rear / head / hand / foot / pelvis
#   D  152 cm permanent comparison: DU152C on v002 | MF152 on v005 (| SG152 context if present): front / 3/4 / side / pelvis / hand / foot / head
#   E  hidden-presentation adult read (bald, clean-shaven, ears hidden by the head-skin cap of hv_hidden_ear.py's method: auricle vertices pulled onto the
#      head surface) c1 / c2: front / 3/4 / side head and bust
#   F  deformation stress: worst pose per candidate + thumb opposition / fist / neck_flex30 / neck_rot45 close-ups (posed npz from mf_deform.py)
#   G  boundary stress: 122 / 137 / 152 thumb + neck wire on v002
import sys, os, json, subprocess, numpy as np
from PIL import Image, ImageDraw
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/halvren_rp3_v001'); os.environ.setdefault('EAR_TOPO', 'v002'); import hv_ear_quick as QK
W, OUT = sys.argv[1:3]; V2 = W + '/v2'; os.makedirs(OUT, exist_ok=True); TMP = W + '/sheets2_r'; os.makedirs(TMP, exist_ok=True); font = QK.font; GREY = np.array(QK.GREY, float)
ENV = dict(os.environ, RENDER_LIGHTING='STUDIO:studio.sl'); jobs = []
def vs(views): return ';'.join('%s:%s:%s:%.2f' % (n, ','.join('%.4f' % x for x in d), ','.join('%.3f' % x for x in c), h) for n, d, c, h in views)
def job(tag, V, Q, col, views, px=600, wire=False):
    np.savez(TMP + '/%s_m.npz' % tag, V=np.asarray(V, np.float32), Q=np.asarray(Q)); np.save(TMP + '/%s_c.npy' % tag, np.asarray(col if col is not None else np.tile(GREY, (len(V), 1)), np.float32))
    if all(os.path.exists(TMP + '/%s_%s.png' % (tag, v[0])) for v in views) and os.environ.get('FORCE') != '1': return
    jobs.append([QK.BP, QK.REND, '--', TMP + '/%s_m.npz' % tag, TMP + '/%s_c.npy' % tag, TMP, tag, vs(views), '1' if wire else '0', str(px)])
def img(tag, v):
    p = TMP + '/%s_%s.png' % (tag, v); return Image.open(p).convert('RGB') if os.path.exists(p) else Image.new('RGB', (500, 500), (255, 200, 200))
def LM(path): return {k: np.array(v['production_p_cm'], float) for k, v in json.load(open(path))['landmarks'].items()}
fam = lambda i: np.load('%s/fam/%s_fam.npz' % (W, i)); cb2 = lambda i: np.load('%s/cb2/%s_cb2.npz' % (V2, i)); cb1 = lambda i: np.load('%s/cb1/%s_cb.npz' % (V2, i))
def aspect(V, Q): P = V[Q]; L = np.linalg.norm(P - np.roll(P, -1, 1), axis=2); return L.max(1) / L.min(1)
def aheat(V, Q, faces):
    a = aspect(V, Q[faces]); col = np.tile(GREY, (len(V), 1)); hv = np.zeros(len(V)); np.maximum.at(hv, Q[faces].ravel(), np.repeat(a, 4))
    col[hv > 0] = [0.72, 0.8, 0.72]; col[hv > 3] = [0.95, 0.65, 0.2]; col[hv > 4] = [0.9, 0.15, 0.1]; return col
def heat(x, lo, hi):
    t = np.clip((x - lo) / (hi - lo), 0, 1)[:, None]; return (1 - t) * np.array([0.82, 0.84, 0.88]) + t * np.array([0.9, 0.15, 0.1])
def thumb_view(lm, side='l'):
    th = lm['thumb_mcp_' + side]; ax = lm['thumb_ip_' + side] - lm['thumb_cmc_' + side]; ax /= np.linalg.norm(ax); dv = np.cross(ax, [0, 0, 1.0]); dv = dv / np.linalg.norm(dv) + 0.3 * np.array([0, 1.0, 0])
    return [('t1', tuple(dv), th + 0.5 * ax, 3.4), ('t2', tuple(-dv + np.array([0, 0.8, 0.3])), th + 0.5 * ax, 3.4)]
def neck_frame(z, V, Q):
    meta = json.loads(str(z['meta'])); H = {k: np.array(v) for k, v in meta['heads'].items()}; c = 0.5 * (H['neck_01'] + H['head']); s = (V[:, 2].max() - V[:, 2].min()) / 173.143
    E = np.unique(np.sort(np.stack([Q, np.roll(Q, -1, 1)], 2).reshape(-1, 2), 1), axis=0); near = np.linalg.norm(V[E[:, 0]] - c, axis=1) < 11 * s
    h = float(np.median(np.linalg.norm(V[E[near, 0]] - V[E[near, 1]], axis=1))); return c, h, s
def valence(Q, n): E = np.unique(np.sort(np.stack([Q, np.roll(Q, -1, 1)], 2).reshape(-1, 2), 1), axis=0); return np.bincount(E.ravel(), minlength=n)
SEL = os.environ.get('BOARDS', 'ABCDEFG')
# ---------- A thumb
if 'A' in SEL:
    for i in ('DU122C-NAT', 'DU137C-NAT', 'DUF137C-NAT'):
        lm = LM('%s/lm/%s_fam_landmarks.json' % (W, i)); views = thumb_view(lm); z = fam(i); job('A0_' + i, z['V'], z['Q'], None, views, px=520, wire=True)
        b = cb1(i); V = b['V'].astype(float); Q = np.asarray(b['Q']); col = np.tile(GREY, (len(V), 1)); idx = np.r_[b['branch_split_faces'], np.arange(57840, len(Q))]; a = aspect(V, Q[idx])
        col[np.unique(Q[idx])] = [0.35, 0.55, 0.9]; col[np.unique(Q[idx[a > 4]])] = [0.9, 0.2, 0.15]; job('A1_' + i, V, Q, col, views, px=520, wire=True)
        b = cb2(i); V = b['V'].astype(float); Q = np.asarray(b['Q']); idx = b['branch_thumb_faces']; a = aspect(V, Q[idx]); col = np.tile(GREY, (len(V), 1))
        col[np.unique(Q[idx])] = [0.35, 0.55, 0.9]; col[np.unique(Q[idx[a > 4]])] = [0.9, 0.2, 0.15]
        vj = json.load(open('%s/val/%s_cb2_validator_v2_D1-D6.json' % (V2, i)))
        sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/durrim_rp4_v002'); import compact_branch_v002 as CB
        rr = CB.realize(dict(fam(i)), json.load(open(V2 + '/branch/MPFB_COMPACT_BRANCH_v002.json')))['thumb_info']['l']['fine_rings']
        for rn in ('B', 'T1', 'T2'): col[rr[rn]] = [0.1, 0.2, 0.75]
        job('A2_' + i, V, Q, col, views, px=520, wire=True)
        job('A3_' + i, V, Q, aheat(V, Q, idx), views[:1], px=520, wire=True)
        z0 = fam(i); b2 = cb2(i); rem = np.asarray(b2['branch_thumb_faces']); rem = rem[rem < 57840]; job('A4_' + i, z0['V'], z0['Q'], aheat(z0['V'].astype(float), np.asarray(z0['Q']), rem), views[:1], px=520, wire=True)
        b1 = cb1(i); i1 = np.r_[b1['branch_split_faces'], np.arange(57840, len(b1['Q']))]; job('A5_' + i, b1['V'], b1['Q'], aheat(b1['V'].astype(float), np.asarray(b1['Q']), i1), views[:1], px=520, wire=True)
# ---------- B neck
NB = ('DU122C-NAT', 'DU137C-NAT', 'DU152C-NAT', 'DUF137C-NAT'); NV = {}
if 'B' in SEL:
    import trimesh
    for i in NB:
        for tag, z in (('B0_', fam(i)), ('B1_', cb2(i))):
            V = z['V'].astype(float); Q = np.asarray(z['Q']); c, h, s = neck_frame(fam(i), V, Q); t = V[:, 2] - c[2]; col = np.tile(GREY, (len(V), 1))
            band = (np.abs(t) <= 0.5 * h) & (np.linalg.norm(V[:, :2] - c[:2], axis=1) <= 11 * s); col[band] = [0.95, 0.75, 0.2]
            val = valence(Q, len(V)); hl = [5299, 11904] if tag == 'B0_' else [735, 5290, 5300, 7455, 11896, 11905]
            for pv in hl:
                nbv = np.unique(Q[(Q == pv).any(1)]); col[nbv] = np.where(col[nbv] == GREY, [0.85, 0.75, 0.9], col[nbv]); col[pv] = [0.9, 0.1, 0.1] if val[pv] == 5 else [0.1, 0.65, 0.2]
            job(tag + i, V, Q, col, [('side', (1, 0.15, 0.0), c + np.array([2.5, 3.0, 0]), 6.5), ('tq', (0.5, 1, -0.35), c + np.array([0, 3.5, 0]), 6.5)], px=520, wire=True)
        z0 = fam(i); b = cb2(i); V0 = z0['V'].astype(float); Q0 = np.asarray(z0['Q']); T = np.c_[Q0[:, [0, 1, 2]], Q0[:, [0, 2, 3]]].reshape(-1, 3)
        mesh = trimesh.Trimesh(V0, T, process=False); V = b['V'].astype(float); mv = np.r_[b['branch_part'] != 'v005']; ids = np.nonzero(mv)[0]
        _, dist, _ = trimesh.proximity.closest_point(mesh, V[ids]); dv = np.zeros(len(V)); dv[ids] = dist * 10
        c, h, s = neck_frame(z0, V0, Q0); job('B2_' + i, V, b['Q'], heat(dv, 0, 0.5), [('tq', (0.5, 1, -0.35), c + np.array([0, 3.5, 0]), 6.5)], px=520, wire=True)
        NV[i] = dict(neck_max_dev_mm=round(float(dv[b['branch_part'] == 'neck_moved'].max()), 4), thumb_max_dev_mm=round(float(dv[np.isin(b['branch_part'], ['thumb_new', 'thumb_moved'])].max()), 4))
# ---------- C central candidates
AV = ('front', 'tqf', 'side', 'rear', 'head', 'hand', 'foot', 'pelvis')
def body_views(V, lm):
    c = np.array([0, np.median(V[:, 1]), V[:, 2].max() / 2]); h = V[:, 2].max() * 0.56; hd = np.array([0, np.median(V[V[:, 2] > V[:, 2].max() - 20][:, 1]), V[:, 2].max() - 11])
    hand = (lm['wrist_l'] + lm['middle_mcp_l']) / 2; foot = (lm['ankle_l'] + lm['toe2_j1_l']) / 2; pel = lm['pelvis_root']; s = V[:, 2].max() / 137.0
    return [('front', (0, 1, 0.02), c, h), ('tqf', (1, 1, 0.05), c, h), ('side', (1, 0, 0.02), c, h), ('rear', (0, -1, 0.02), c, h), ('head', (0.4, 1, 0.08), hd, 12 * s),
            ('hand', (0.3, 0.6, -0.6), hand, 8 * s), ('foot', (0.6, 1, 0.5), foot, 10 * s), ('pelvis', (0.4, 1, 0.05), pel, 22 * s)]
if 'C' in SEL:
    for i in ('DU137C-NAT', 'DUF137C-NAT'):
        b = cb2(i); job('C_' + i, b['V'], b['Q'], None, body_views(b['V'].astype(float), LM('%s/lm/%s_cb2_landmarks.json' % (V2, i))))
# ---------- D 152 comparison (common frame: soles on z = 0, same ortho height)
DB = [('DU152C-NAT', 'v2'), ('MF152-NAT', 'fam')] + ([('SG152', 'fam')] if os.path.exists('%s/fam/SG152_fam.npz' % W) else [])
if 'D' in SEL:
    for i, k in DB:
        z = cb2(i) if k == 'v2' else fam(i); V = z['V'].astype(float); lm = LM('%s/lm/%s_%s_landmarks.json' % (V2 if k == 'v2' else W, i, 'cb2' if k == 'v2' else 'fam'))
        c = np.array([0, np.median(V[:, 1]), 152 / 2]); h = 152 * 0.56; hd = np.array([0, np.median(V[V[:, 2] > V[:, 2].max() - 20][:, 1]), V[:, 2].max() - 11])
        job('D_' + i, V, z['Q'], None, [('front', (0, 1, 0.02), c, h), ('tqf', (1, 1, 0.05), c, h), ('side', (1, 0, 0.02), c, h), ('pelvis', (0.4, 1, 0.05), lm['pelvis_root'], 24),
                                        ('hand', (0.3, 0.6, -0.6), (lm['wrist_l'] + lm['middle_mcp_l']) / 2, 9), ('foot', (0.6, 1, 0.5), (lm['ankle_l'] + lm['toe2_j1_l']) / 2, 11), ('head', (0.4, 1, 0.08), hd, 13)])
# ---------- E hidden presentation (external ear = hm08 w_ears > 0.05 carried through M, harmonically collapsed as hv_hidden_ear.py -- board only)
R6P = {'DUF137C-NAT': '/home/claude/wayfarer-design/reviews/rac-rp4-evidence/durrim/partA/DUF137C-NAT_r6.npz'}
if 'E' in SEL:
    import scipy.sparse as sp
    for i in ('DU137C-NAT', 'DUF137C-NAT'):
        b = cb2(i); V = b['V'].astype(float).copy(); Q = np.asarray(b['Q']); s = V[:, 2].max() / 137.0
        r6 = np.load(R6P.get(i, '/home/claude/wayfarer-design/reviews/reference-assets/r6/%s_r6.npz' % i))
        M = sp.csr_matrix((b['M_data'], b['M_indices'], b['M_indptr']), shape=tuple(b['M_shape'])); we = M @ r6['w_ears'][b['src_index']].astype(float); ear = we > 0.05
        A = sp.coo_matrix((np.ones(4 * len(Q)), (Q.ravel(), np.roll(Q, -1, 1).ravel())), shape=(len(V), len(V))).tocsr(); A = ((A + A.T) > 0).astype(float); deg = np.asarray(A.sum(1)).ravel()
        for _ in range(400): V[ear] = (A @ V)[ear] / deg[ear, None]
        hd = np.array([0, np.median(V[V[:, 2] > V[:, 2].max() - 20][:, 1]), V[:, 2].max() - 11]); bust = hd - np.array([0, 0, 12 * s])
        job('E_' + i, V, Q, None, [('front', (0, 1, 0.03), hd, 11 * s), ('tq', (0.8, 1, 0.05), hd, 11 * s), ('side', (1, 0, 0.02), hd, 11 * s), ('bust', (0.6, 1, 0.05), bust, 22 * s)])
# ---------- F deformation stress
if 'F' in SEL:
    for i in ('DU137C-NAT', 'DUF137C-NAT'):
        dj = json.load(open('%s/def/deform_%s_cb2.json' % (V2, i))); poses = dj['poses'] if 'poses' in dj else dj
        worst = max(poses, key=lambda p: (poses[p].get('flipped', 0) if isinstance(poses[p], dict) else 0, poses[p].get('new_self_intersections', 0) if isinstance(poses[p], dict) else 0))
        for pn in ('thumb_opposition_l', 'fist_l', 'neck_flex30', 'neck_rot45'):
            pz = '%s/def/%s_%s_cb2.npz' % (V2, pn, i)
            if not os.path.exists(pz): continue
            P = np.load(pz); V = P['V'].astype(float); Q = np.asarray(P['Q']) if 'Q' in P else np.asarray(cb2(i)['Q']); lmv = LM('%s/lm/%s_cb2_landmarks.json' % (V2, i))
            if pn.startswith('neck'): c = V[np.asarray(cb2(i)['branch_part']) == 'neck_moved'].mean(0); vw = [('n', (0.5, 1, -0.3), c + np.array([0, 1.0, 0]), 7)]
            elif pn in ('thumb_opposition_l', 'fist_l'): bp = np.asarray(cb2(i)['branch_part']); mk = (bp == 'thumb_new') & (V[:, 0] > 0); c = V[mk].mean(0); vw = [('n', (0.3, 0.6, -0.6), c, 5), ('m', (-0.4, 0.8, 0.3), c, 5)]
            else: vw = [('n', (0.6, 1, 0.1), V.mean(0), V[:, 2].max() * 0.56)]
            job('F_%s_%s' % (i, pn), V, Q, None, vw, px=520, wire=True)
# ---------- G boundary
if 'G' in SEL:
    for i in ('DU122C-NAT', 'DU137C-NAT', 'DU152C-NAT'):
        b = cb2(i); V = b['V'].astype(float); lm = LM('%s/lm/%s_cb2_landmarks.json' % (V2, i)); c, h, s = neck_frame(fam(i), V, np.asarray(b['Q']))
        job('G_' + i, V, b['Q'], None, thumb_view(lm)[:1] + [('neck', (0.5, 1, -0.35), c + np.array([0, 3.5, 0]), 6.5)], px=520, wire=True)
with ThreadPoolExecutor(2) as ex: list(ex.map(lambda j: subprocess.run(j, env=ENV, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL), jobs))
def sheet(fn, title, rows, heads, colw=300, lab_w=170, note=None):
    import textwrap
    ncol = max(len(r[1]) for r in rows); Wd = lab_w + ncol * colw; tl = textwrap.wrap(title, int(Wd / 11.2)); nt = []
    if note: nt = [l for p in note.split('\n') for l in (textwrap.wrap(p, int(Wd / 7.3)) or [''])]
    top = 20 + 24 * len(tl) + 10; S = Image.new('RGB', (Wd, top + 30 + len(rows) * (colw + 6) + 19 * len(nt) + 16), 'white'); d = ImageDraw.Draw(S)
    for k, l in enumerate(tl): d.text((12, 12 + 24 * k), l, fill=(0, 0, 0), font=font(18, True))
    y = top
    for k, h_ in enumerate(heads): d.text((lab_w + k * colw + 4, y), h_, fill=(0, 0, 0), font=font(13, True))
    y += 26
    for lb, ims in rows:
        d.multiline_text((8, y + colw // 2 - 20), '\n'.join(textwrap.wrap(lb, 18)), fill=(0, 0, 0), font=font(14, True))
        for k, im in enumerate(ims): S.paste(im.resize((colw, colw)), (lab_w + k * colw, y))
        y += colw + 6
    for k, l in enumerate(nt): d.text((12, y + 4 + 19 * k), l, fill=(60, 60, 60), font=font(13))
    S.save(os.path.join(OUT, fn), quality=90)
TB = ('DU122C-NAT', 'DU137C-NAT', 'DUF137C-NAT')
if 'A' in SEL:
    sheet('DU2_A_thumb_mcp_revision.jpg', 'A. Thumb MCP: v005 (FAIL, 1-2 rings) | rejected v001 prototype (4-6 rings; 100-105 quads > 4:1, red) | MPFB_COMPACT_BRANCH_v002 (branch quads blue, '
          'counted validator rings B / T1 / T2 dark blue, > 4:1 red) | aspect classes per version',
          [(i, [img('A0_' + i, 't1'), img('A1_' + i, 't1'), img('A2_' + i, 't1'), img('A4_' + i, 't1'), img('A5_' + i, 't1'), img('A3_' + i, 't1')]) for i in TB],
          ['v005 wire', 'v001 (rejected) wire', 'v002 wire', 'v005 aspect', 'v001 aspect', 'v002 aspect'], colw=300,
          note='Aspect panels colour only the thumb-zone faces of each version: green <= 3:1, amber 3-4:1, red > 4:1 (T-4). v005 = the 200 parent faces v002 replaces.')
if 'B' in SEL:
    sheet('DU2_B_jaw_neck_reroute.jpg', 'B. Jaw-neck reroute: v005 (pole pair 5299 / 11904 red, in the amber crease band on 137 / 152) | v002 (moved trio per side: valence-5 red, valence-3 green; all above the band) | '
          'v002 surface deviation from the v005 surface (0 grey -> 0.5 mm red)',
          [(i, [img('B0_' + i, 'side'), img('B0_' + i, 'tq'), img('B1_' + i, 'side'), img('B1_' + i, 'tq'), img('B2_' + i, 'tq')]) for i in NB], ['v005 side', 'v005 front 3/4', 'v002 side', 'v002 front 3/4', 'v002 deviation'], colw=300,
          note='\n'.join('%s: max on-surface deviation of re-placed vertices: neck %s mm, thumb %s mm' % (i, NV[i]['neck_max_dev_mm'], NV[i]['thumb_max_dev_mm']) for i in NV))
if 'C' in SEL:
    sheet('DU2_C_central_candidates.jpg', 'C. Durrim production reference candidates on MPFB_COMPACT_BRANCH_v002: DU_M_REF_RP4_v001 (c1, DU137C-NAT) | DU_F_REF_RP4_v001 (c2, DUF137C-NAT) -- NOT frozen',
          [('DU_M_REF_RP4_v001 (c1)', [img('C_DU137C-NAT', v) for v in AV]), ('DU_F_REF_RP4_v001 (c2)', [img('C_DUF137C-NAT', v) for v in AV])], ['front', 'front 3/4', 'side', 'rear', 'head', 'hand', 'foot', 'pelvis'], colw=240)
if 'D' in SEL:
    DV = ('front', 'tqf', 'side', 'pelvis', 'hand', 'foot', 'head')
    sheet('DU2_D_152cm_comparison.jpg', 'D. 152 cm equal-height permanent comparison (same ortho scale, soles on the ground): Durrim DU152C on compact v002 | Marchfolk MF152 on family v005' + (' | Sagekin SG152 (context)' if len(DB) > 2 else ''),
          [(('Durrim 152 (v002)' if i.startswith('DU') else 'Marchfolk 152 (v005)' if i.startswith('MF') else 'Sagekin 152 (context)'), [img('D_' + i, v) for v in DV]) for i, k in DB], ['front', 'front 3/4', 'side', 'pelvis', 'hand', 'foot', 'head'], colw=240)
if 'E' in SEL:
    sheet('DU2_E_hidden_presentation.jpg', 'E. Hidden-presentation adult read: bald, clean-shaven, ears hidden (external ear = hm08 w_ears > 0.05 harmonically flattened, as the accepted hidden-ear gates; a low relief remains), neutral expression -- c1 / c2 production candidates',
          [('c1 DU_M_REF_RP4_v001', [img('E_DU137C-NAT', v) for v in ('front', 'tq', 'side', 'bust')]), ('c2 DU_F_REF_RP4_v001', [img('E_DUF137C-NAT', v) for v in ('front', 'tq', 'side', 'bust')])], ['front', 'front 3/4', 'side', 'bust 3/4'], colw=330)
if 'F' in SEL:
    rows = []
    for i in ('DU137C-NAT', 'DUF137C-NAT'):
        rows.append((i, [img('F_%s_%s' % (i, t), v) for t, v in (('thumb_opposition_l', 'n'), ('thumb_opposition_l', 'm'), ('fist_l', 'n'), ('fist_l', 'm'), ('neck_flex30', 'n'), ('neck_rot45', 'n'))]))
    sheet('DU2_F_deformation_stress.jpg', 'F. Deformation stress on the v002 candidates (left thumb patch and jaw-neck reroute, wire): thumb opposition, fist, neck flex 30, neck rotation 45. '
          'All 18 standard poses: c1 identical to v005; c2 +4 / +8 self-contact pairs at wrist_flex60 / hip_flex90 are the same v005 contacts counted on the finer branch faces (0 unmatched)', rows,
          ['opposition', 'opposition (palm)', 'fist', 'fist (palm)', 'neck flex 30', 'neck rot 45'], colw=280)
if 'G' in SEL:
    sheet('DU2_G_boundary_stress.jpg', 'G. Boundary stress: the same v002 topology at 122 / 137 / 152 cm -- thumb MCP patch and jaw-neck reroute (wire)',
          [(i, [img('G_' + i, 't1'), img('G_' + i, 'neck')]) for i in ('DU122C-NAT', 'DU137C-NAT', 'DU152C-NAT')], ['thumb MCP', 'jaw-neck'], colw=420)
json.dump(NV, open(OUT + '/DU2_branch_surface_deviation.json', 'w'), indent=1); print('SHEETS2', sorted(os.listdir(OUT)))
