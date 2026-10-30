# du_sheets.py WORK OUT : RP4 Durrim compact-branch pilot boards (neutral clay, orthographic, workbench renders; render_attr.py):
#   DU_A  central source validation: DU137C-NAT (c1) and the new DUF137C-NAT (c2) family realizations: front / front 3/4 / side / rear + head, hand, foot, pelvis
#   DU_B  thumb MCP: unbranched v005 vs compact-branch prototype (wire; new branch quads blue, aspect > 4 red) on DU122C / DU137C / DUF137C
#   DU_N  neck blocker: the v005 submandibular valence-5 poles 5299 / 11904 (red) and the validator neck-station crease band (|axial| <= 0.5 h, amber) on
#         DU122C / DU137C / DU152C / DUF137C / MF152 (side and front 3/4, wire)
#   DU_G  boundary density: 122 / 137 / 152 hands and face wire (unbranched v005)
import sys, os, json, subprocess, numpy as np
from PIL import Image, ImageDraw
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/halvren_rp3_v001'); os.environ.setdefault('EAR_TOPO', 'v002'); import hv_ear_quick as QK
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001'); from core3lib import ring_stations
W, OUT = sys.argv[1:3]; os.makedirs(OUT, exist_ok=True); TMP = W + '/sheets_r'; os.makedirs(TMP, exist_ok=True); font = QK.font; GREY = QK.GREY
ENV = dict(os.environ, RENDER_LIGHTING='STUDIO:studio.sl'); jobs = []
def vs(views): return ';'.join('%s:%s:%s:%.2f' % (n, ','.join('%.4f' % x for x in d), ','.join('%.3f' % x for x in c), h) for n, d, c, h in views)
def job(tag, V, Q, col, views, px=600, wire=False):
    np.savez(TMP + '/%s_m.npz' % tag, V=np.asarray(V, np.float32), Q=np.asarray(Q)); np.save(TMP + '/%s_c.npy' % tag, np.asarray(col if col is not None else np.tile(GREY, (len(V), 1)), np.float32))
    if all(os.path.exists(TMP + '/%s_%s.png' % (tag, v[0])) for v in views) and os.environ.get('FORCE') != '1': return
    jobs.append([QK.BP, QK.REND, '--', TMP + '/%s_m.npz' % tag, TMP + '/%s_c.npy' % tag, TMP, tag, vs(views), '1' if wire else '0', str(px)])
def img(tag, v):
    p = TMP + '/%s_%s.png' % (tag, v); return Image.open(p).convert('RGB') if os.path.exists(p) else Image.new('RGB', (500, 500), (255, 200, 200))
LM = lambda i: {k: np.array(v['production_p_cm'], float) for k, v in json.load(open('%s/lm/%s_fam_landmarks.json' % (W, i)))['landmarks'].items()}
fam = lambda i: np.load('%s/fam/%s_fam.npz' % (W, i))
# ---------- A
for i in ('DU137C-NAT', 'DUF137C-NAT'):
    z = fam(i); V = z['V'].astype(float); lm = LM(i); c = np.array([0, np.median(V[:, 1]), V[:, 2].max() / 2]); h = V[:, 2].max() * 0.56
    hd = np.array([0, np.median(V[V[:, 2] > V[:, 2].max() - 20][:, 1]), V[:, 2].max() - 11]); hand = (lm['wrist_l'] + lm['middle_mcp_l']) / 2; foot = (lm['ankle_l'] + lm['toe2_j1_l']) / 2; pel = lm['pelvis_root']
    job('A_' + i, V, z['Q'], None, [('front', (0, 1, 0.02), c, h), ('tqf', (1, 1, 0.05), c, h), ('side', (1, 0, 0.02), c, h), ('rear', (0, -1, 0.02), c, h),
                                     ('head', (0.4, 1, 0.08), hd, 12), ('hand', (0.3, 0.6, -0.6), hand, 8), ('foot', (0.6, 1, 0.5), foot, 10), ('pelvis', (0.4, 1, 0.05), pel, 22)])
# ---------- B thumb
for i in ('DU122C-NAT', 'DU137C-NAT', 'DUF137C-NAT'):
    lm = LM(i); th = lm['thumb_mcp_l']; ax = lm['thumb_ip_l'] - lm['thumb_cmc_l']; ax /= np.linalg.norm(ax); dv = np.cross(ax, [0, 0, 1.0]); dv = dv / np.linalg.norm(dv) + 0.3 * np.array([0, 1.0, 0])
    z = fam(i); job('B0_' + i, z['V'], z['Q'], None, [('t1', tuple(dv), th + 0.5 * ax, 3.4), ('t2', tuple(-dv + np.array([0, 0.8, 0.3])), th + 0.5 * ax, 3.4)], px=520, wire=True)
    b = np.load('%s/br/%s_cb.npz' % (W, i)); V = b['V'].astype(float); Q = np.asarray(b['Q']); col = np.tile(GREY, (len(V), 1)); nq0 = 57840
    idx = np.r_[b['branch_split_faces'], np.arange(nq0, len(Q))]; P = V[Q[idx]]; L = np.linalg.norm(P - np.roll(P, -1, 1), axis=2); asp = L.max(1) / L.min(1)
    col[np.unique(Q[idx])] = [0.35, 0.55, 0.9]; col[np.unique(Q[idx[asp > 4]])] = [0.9, 0.2, 0.15]
    job('B1_' + i, V, Q, col, [('t1', tuple(dv), th + 0.5 * ax, 3.4), ('t2', tuple(-dv + np.array([0, 0.8, 0.3])), th + 0.5 * ax, 3.4)], px=520, wire=True)
# ---------- N neck
NB = ('DU122C-NAT', 'DU137C-NAT', 'DU152C-NAT', 'DUF137C-NAT', 'MF152-NAT'); NV = {}
for i in NB:
    z = fam(i); V = z['V'].astype(float); Q = np.asarray(z['Q']); meta = json.loads(str(z['meta'])); H = {k: np.array(v) for k, v in meta['heads'].items()}
    v = json.load(open('%s/val/%s_fam_validator_v2_D1-D6.json' % (W, i)))['stations']['neck']
    c = 0.5 * (H['neck_01'] + H['head']); d = np.array([0, 0, 1.0])            # validator neck station (core3lib.stations): vertical axis, R = 11 s
    E = np.unique(np.sort(np.stack([Q, np.roll(Q, -1, 1)], 2).reshape(-1, 2), 1), axis=0); em = 0.5 * (V[E[:, 0]] + V[E[:, 1]]); s = (V[:, 2].max() - V[:, 2].min()) / 173.143
    near = np.linalg.norm(em - c, axis=1) < 11.0 * s; hmed = float(np.median(np.linalg.norm(V[E[near, 0]] - V[E[near, 1]], axis=1)))
    t = (V - c) @ d; col = np.tile(GREY, (len(V), 1)); band = (np.abs(t) <= 0.5 * hmed) & (np.linalg.norm((V - c) - np.outer(t, d), axis=1) <= 11.0 * s); col[band] = [0.95, 0.75, 0.2]
    for p in (5299, 11904): col[p] = [0.9, 0.1, 0.1]
    pv = np.unique(Q[(Q == 5299).any(1) | (Q == 11904).any(1)]); col[pv] = np.where(col[pv] == GREY, [0.9, 0.45, 0.45], col[pv])
    NV[i] = dict(status=v['status_D1_D3'], crease=v['crease_poles'], t_pole_over_h=[round(float(((V[p] - c) @ d) / hmed), 2) for p in (5299, 11904)], h_cm=round(hmed, 3))
    job('N_' + i, V, Q, col, [('side', (1, 0.15, 0.0), c + np.array([2.5, 3.0, 0]), 6.5), ('tq', (0.5, 1, -0.35), c + np.array([0, 3.5, 0]), 6.5)], px=520, wire=True)
# ---------- G boundary density (hands, face)
for i in ('DU122C-NAT', 'DU137C-NAT', 'DU152C-NAT'):
    z = fam(i); V = z['V'].astype(float); lm = LM(i); hand = (lm['wrist_l'] + lm['middle_mcp_l']) / 2; s = V[:, 2].max() / 137.0
    hd = np.array([0, np.median(V[V[:, 2] > V[:, 2].max() - 20][:, 1]), V[:, 2].max() - 11])
    job('G_' + i, V, z['Q'], None, [('hand', (0.3, 0.6, -0.6), hand, 8 * s), ('face', (0.35, 1, 0.05), hd, 12 * s), ('foot', (0.6, 1, 0.5), (lm['ankle_l'] + lm['toe2_j1_l']) / 2, 10 * s)], px=520, wire=True)
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
AV = ('front', 'tqf', 'side', 'rear', 'head', 'hand', 'foot', 'pelvis')
sheet('DU_A_central_sources.jpg', 'A. Durrim central sources on the unbranched MPFB Family Base v005 (137 cm): DU137C-NAT c1 (accepted W2H1) | DUF137C-NAT c2 (new technical anchor: MF-F-R base macro + DU137C targets + D1 pelvis, native route)',
      [('c1 DU137C-NAT', [img('A_DU137C-NAT', v) for v in AV]), ('c2 DUF137C-NAT', [img('A_DUF137C-NAT', v) for v in AV])], ['front', 'front 3/4', 'side', 'rear', 'head', 'hand', 'foot', 'pelvis'], colw=240)
sheet('DU_B_thumb_branch.jpg', 'B. Thumb MCP: unbranched v005 (left pair) vs compact-branch prototype v001 (right pair; new quads blue, aspect > 4:1 red). Validator thumb MCP rings: v005 1-2 (FAIL) -> prototype 4-6 (PASS); the prototype costs 100-105 quads above the T-4 4:1 aspect target',
      [(i, [img('B0_' + i, 't1'), img('B1_' + i, 't1')]) for i in ('DU122C-NAT', 'DU137C-NAT', 'DUF137C-NAT')], ['v005 (unbranched)', 'branch prototype v001'], colw=420)
sheet('DU_N_neck_blocker.jpg', 'N. Neck station blocker: v005 submandibular valence-5 poles 5299 / 11904 (red, with their quads pink) and the validator neck crease band (amber, |axial| <= 0.5 h about the neck station centre)',
      [('%s %s' % (i, NV[i]['status']), [img('N_' + i, 'side'), img('N_' + i, 'tq')]) for i in NB], ['side', 'front 3/4 below'], colw=360,
      note='\n'.join('%s: status %s, pole axial offset / h = %s (crease band = |t/h| <= 0.5), h = %s cm' % (i, NV[i]['status'], NV[i]['t_pole_over_h'], NV[i]['h_cm']) for i in NB))
sheet('DU_G_boundary_density.jpg', 'G. Boundary density on the unbranched v005 (wire): Durrim 122 / 137 / 152 cm hands, face and feet (same topology; edge / stature grows as stature falls)',
      [(i, [img('G_' + i, v) for v in ('hand', 'face', 'foot')]) for i in ('DU122C-NAT', 'DU137C-NAT', 'DU152C-NAT')], ['hand', 'face', 'foot'], colw=360)
json.dump(NV, open(OUT + '/../DU_neck_station_poles.json', 'w'), indent=1); print('SHEETS', sorted(os.listdir(OUT)), NV)
