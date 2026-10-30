# pk_sheets.py WORK OUT : RP4 Pipkin boards (order 25f7ba0 §17). Neutral clay, orthographic, workbench renders (render_attr.py via hv_ear_quick); diagnostic.
#   A central sources c1 PK-NAT / c2 PKF107-NAT on v005     B compact diagnosis (thumb wire / aspect / counted rings: v005 | Durrim v002 diagnostic | Pipkin branch v001;
#   toe 3 / 4 MTP stations)                                  C Pipkin branch realizations c1 / c2 (NOT production candidates: pending author decision)
#   D 122 cm Pipkin vs Durrim (frozen DU122C RP4 realization) E adult vs generator child proxy (diagnostic only)   F normalized Pipkin vs Marchfolk 173
#   G Pipkin vs Cogling context (91 / 107)                   H deformation (thumb / branch close-ups, worst pose)
# Comparator meshes from r6 (accepted R-6 sources; helper geometry removed by the 'keep' mask). Hidden ears where marked: hm08 w_ears > 0.05 flattened (board only).
import sys, os, json, subprocess, numpy as np
from PIL import Image, ImageDraw
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/halvren_rp3_v001'); os.environ.setdefault('EAR_TOPO', 'v002'); import hv_ear_quick as QK
import scipy.sparse as sp
W, OUT = sys.argv[1:3]; os.makedirs(OUT, exist_ok=True); TMP = W + '/sheets_r'; os.makedirs(TMP, exist_ok=True); font = QK.font; GREY = np.array(QK.GREY, float)
ENV = dict(os.environ, RENDER_LIGHTING='STUDIO:studio.sl'); jobs = []; SEL = os.environ.get('BOARDS', 'ABCDEFGH')
RA = '/home/claude/wayfarer-design/reviews/reference-assets/r6'
def vs(views): return ';'.join('%s:%s:%s:%.2f' % (n, ','.join('%.4f' % x for x in d), ','.join('%.3f' % x for x in c), h) for n, d, c, h in views)
def job(tag, V, Q, col, views, px=560, wire=False):
    Q = [list(map(int, q)) for q in Q]
    np.savez(TMP + '/%s_m.npz' % tag, V=np.asarray(V, np.float32), Q=np.array(Q, dtype=object) if len({len(q) for q in Q}) > 1 else np.array(Q))
    np.save(TMP + '/%s_c.npy' % tag, np.asarray(col if col is not None else np.tile(GREY, (len(V), 1)), np.float32))
    if all(os.path.exists(TMP + '/%s_%s.png' % (tag, v[0])) for v in views) and os.environ.get('FORCE') != '1': return
    jobs.append([QK.BP, QK.REND, '--', TMP + '/%s_m.npz' % tag, TMP + '/%s_c.npy' % tag, TMP, tag, vs(views), '1' if wire else '0', str(px)])
def img(tag, v):
    p = TMP + '/%s_%s.png' % (tag, v); return Image.open(p).convert('RGB') if os.path.exists(p) else Image.new('RGB', (500, 500), (255, 200, 200))
def r6mesh(path):
    z = np.load(path); V = z['V'].astype(float); F = np.asarray(z['F']); k = z['keep'].astype(bool); f = F[k[F].all(1)]
    J = {n: np.array(v[0]) for n, v in json.loads(str(z['joints'])).items()}; return V, f, J, z
def fammesh(path):
    z = np.load(path); m = json.loads(str(z['meta'])); return z['V'].astype(float), np.asarray(z['Q']), {k: np.array(v) for k, v in m['heads'].items()}, z
def collapse_ears(V, Q, mask):
    V = V.copy(); n = len(V); E = []
    for q in Q:
        for a in range(len(q)): E.append((q[a], q[(a + 1) % len(q)]))
    E = np.array(E); A = sp.coo_matrix((np.ones(len(E)), (E[:, 0], E[:, 1])), shape=(n, n)).tocsr(); A = ((A + A.T) > 0).astype(float); deg = np.asarray(A.sum(1)).ravel()
    from scipy.sparse.linalg import spsolve                                             # exact harmonic fill of the ear region (boundary = surrounding head skin)
    I = np.nonzero(mask)[0]; B = np.nonzero(~mask)[0]; L = (sp.diags(deg) - A).tocsr()
    LII = L[I][:, I].tocsc(); LIB = L[I][:, B]
    for k in range(3): V[I, k] = spsolve(LII, -LIB @ V[B, k])
    return V
def body_views(V, J, H=None, tag8=True):
    H = H or V[:, 2].max(); c = np.array([0, np.median(V[:, 1]), H / 2]); h = H * 0.56; top = V[:, 2].max()
    hd = np.array([0, np.median(V[V[:, 2] > top - 0.13 * H][:, 1]), top - 0.07 * H]); s = H / 107.0
    hand = J['hand_l'] + np.array([0.0, 0, -4.0 * s]); foot = J['foot_l'] + np.array([0, -3.0 * s, -3.0 * s]); pel = J['pelvis']
    v = [('front', (0, 1, 0.02), c, h), ('tqf', (1, 1, 0.05), c, h), ('side', (1, 0, 0.02), c, h), ('rear', (0, -1, 0.02), c, h), ('head', (0.4, 1, 0.08), hd, 0.085 * H),
         ('hand', (0.3, 0.6, -0.6), hand, 6 * s), ('foot', (0.6, 1, 0.5), foot, 8 * s), ('pelvis', (0.4, 1, 0.05), pel, 17 * s)]
    return v
def aspect(V, Q): P = V[Q]; L = np.linalg.norm(P - np.roll(P, -1, 1), axis=2); return L.max(1) / L.min(1)
def aheat(V, Q, faces):
    a = aspect(V, Q[faces]); col = np.tile(GREY, (len(V), 1)); hv = np.zeros(len(V)); np.maximum.at(hv, Q[faces].ravel(), np.repeat(a, 4))
    col[hv > 0] = [0.72, 0.8, 0.72]; col[hv > 3] = [0.95, 0.65, 0.2]; col[hv > 4] = [0.9, 0.15, 0.1]; return col
AV = ('front', 'tqf', 'side', 'rear', 'head', 'hand', 'foot', 'pelvis'); AH = ['front', 'front 3/4', 'side', 'rear', 'face', 'hand', 'foot', 'pelvis']
# ---------- A / C
if 'A' in SEL or 'C' in SEL:
    for i in ('PK-NAT', 'PKF107-NAT'):
        V, Q, J, z = fammesh('%s/fam/%s_fam.npz' % (W, i)); job('A_' + i, V, Q, None, body_views(V, J))
        b = np.load('%s/v1/cb/%s_pkb.npz' % (W, i)); job('C_' + i, b['V'], b['Q'], None, body_views(b['V'].astype(float), J))
# ---------- B
TB = ('PK91-NAT', 'PK-NAT', 'PKF107-NAT', 'PK122-NAT')
def thumb_view(J, side='l'):
    th = J['thumb_02_' + side]; ax = J['thumb_03_' + side] - J['thumb_01_' + side]; ax /= np.linalg.norm(ax); dv = np.cross(ax, [0, 0, 1.0]); dv = dv / np.linalg.norm(dv) + 0.3 * np.array([0, 1.0, 0])
    return [('t1', tuple(dv), th + 0.4 * ax, 2.6)]
if 'B' in SEL:
    sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/pipkin_rp4_v001'); sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/durrim_rp4_v002')
    import pk_branch_v001 as PB
    rec = json.load(open(W + '/br/MPFB_PIPKIN_COMPACT_BRANCH_v001.json'))
    for i in TB:
        V, Q, J, z = fammesh('%s/fam/%s_fam.npz' % (W, i)); tv = thumb_view(J); job('B0_' + i, V, Q, None, tv, wire=True)
        d = np.load('%s/inh/%s_du2.npz' % (W, i)); Vd = d['V'].astype(float); Qd = np.asarray(d['Q']); job('B1_' + i, Vd, Qd, aheat(Vd, Qd, d['branch_thumb_faces']), tv, wire=True)
        b = np.load('%s/v1/cb/%s_pkb.npz' % (W, i)); Vb = b['V'].astype(float); Qb = np.asarray(b['Q']); col = aheat(Vb, Qb, b['branch_thumb_faces'])
        rr = PB.realize(dict(np.load('%s/fam/%s_fam.npz' % (W, i))), rec)['info']['l']['fine_rings']
        for rn in ('B', 'T1', 'T2'): col[rr[rn]] = [0.1, 0.2, 0.75]
        job('B2_' + i, Vb, Qb, col, tv, wire=True)
        foot = J['ball_l']; job('B3_' + i, V, Q, None, [('toe', (0.35, 1, 0.9), foot + np.array([0, 2.0 * V[:, 2].max() / 107, 0]), 4.5 * V[:, 2].max() / 107)], wire=True)
# ---------- D 122 Pipkin vs Durrim (real height, soles on the ground)
if 'D' in SEL:
    for i, p in (('PK122', '%s/v1/cb/PK122-NAT_pkb.npz' % W), ('DU122', '/tmp/claude-0/rt/du/v2/cb2/DU122C-NAT_cb2.npz')):
        z = np.load(p); V = z['V'].astype(float); J = {k: np.array(v) for k, v in json.loads(str(z['meta']))['heads'].items()}; bv = dict((v[0], v) for v in body_views(V, J, H=122.0))
        job('D_' + i, V, z['Q'], None, [bv[k] for k in ('front', 'tqf', 'side', 'pelvis', 'hand', 'foot')])
# ---------- E adult vs child (heads with ears hidden; bodies)
CH = (('PK-NAT', 'CHILD6', 'child'), ('PK91-NAT', 'CHILD3', 'child'))
if 'E' in SEL:
    for a, c, d in CH:
        for tag, path in ((a, '%s/full/%s_r6.npz' % (W, a)), (c, '%s/%s/%s_r6.npz' % (W, d, c))):
            V, F, J, z = r6mesh(path); ear = np.asarray(z['w_ears']) > 0.05; Vh = collapse_ears(V, F, ear); H = V[:, 2].max(); top = H
            hd = np.array([0, np.median(V[V[:, 2] > top - 0.13 * H][:, 1]), top - 0.07 * H]); c0 = np.array([0, np.median(V[:, 1]), H / 2])
            job('E_' + tag, Vh, F, None, [('hf', (0, 1, 0.03), hd, 0.09 * H), ('hs', (1, 0, 0.02), hd, 0.09 * H), ('bf', (0, 1, 0.02), c0, H * 0.56), ('bs', (1, 0, 0.02), c0, H * 0.56)])
# ---------- F normalized Pipkin vs Marchfolk (each displayed at the same height; ears hidden)
if 'F' in SEL:
    for tag, path in (('PK107', '%s/full/PK-NAT_r6.npz' % W), ('PKF107', W + '/nat/PKF107-NAT_r6.npz'), ('MFM', '%s/full/MF-M-R_r6.npz' % W), ('MFF', '%s/full/MF-F-R_r6.npz' % W)):
        V, F, J, z = r6mesh(path); ear = np.asarray(z['w_ears']) > 0.05; V = collapse_ears(V, F, ear); V = V * (173.0 / V[:, 2].max()); c0 = np.array([0, np.median(V[:, 1]), 173 / 2])
        job('F_' + tag, V, F, None, [('f', (0, 1, 0.02), c0, 97), ('t', (1, 1, 0.05), c0, 97), ('s', (1, 0, 0.02), c0, 97)])
# ---------- G Pipkin vs Cogling (real height)
if 'G' in SEL:
    for tag, path in (('PK91', '%s/full/PK91-NAT_r6.npz' % W), ('CG91', '%s/full/CGJ7_r6.npz' % W), ('PK107', '%s/full/PK-NAT_r6.npz' % W), ('CG107', '%s/full/CG107-NAT_r6.npz' % W)):
        V, F, J, z = r6mesh(path); ear = np.asarray(z['w_ears']) > 0.05; V = collapse_ears(V, F, ear); H = 107.0 if '107' in tag else 91.0; c0 = np.array([0, np.median(V[:, 1]), H / 2])
        job('G_' + tag, V, F, None, [('f', (0, 1, 0.02), c0, H * 0.56), ('t', (1, 1, 0.05), c0, H * 0.56), ('s', (1, 0, 0.02), c0, H * 0.56)])
# ---------- H deformation
if 'H' in SEL:
    for i in ('PK-NAT', 'PKF107-NAT'):
        b = np.load('%s/v1/cb/%s_pkb.npz' % (W, i)); Q = np.asarray(b['Q']); bp = np.asarray(b['branch_part'])
        for pn in ('thumb_opposition_l', 'fist_l', 'wrist_flex60_l'):
            pz = '%s/v1/def/%s_%s_pkb.npz' % (W, pn, i)
            if not os.path.exists(pz): continue
            V = np.load(pz)['V'].astype(float); c = V[(bp == 'thumb_new') & (V[:, 0] > 0)].mean(0)
            job('H_%s_%s' % (i, pn), V, Q, None, [('n', (0.3, 0.6, -0.6), c, 3.6), ('m', (-0.4, 0.8, 0.3), c, 3.6)], wire=True)
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
if 'A' in SEL: sheet('PK_A_central_sources.jpg', 'A. Pipkin central sources on unbranched MPFB Family Base v005 (107 cm): PK-NAT c1 (accepted W1e) | PKF107-NAT c2 (new technical anchor)',
                     [('c1 PK-NAT', [img('A_PK-NAT', v) for v in AV]), ('c2 PKF107-NAT', [img('A_PKF107-NAT', v) for v in AV])], AH, colw=230)
if 'B' in SEL: sheet('PK_B_compact_diagnosis.jpg', 'B. Compact diagnosis, left thumb MCP: v005 (c1 FAIL 1-2 rings; c2 PASS) | Durrim v002 applied as a diagnostic (aspect classes; c2 crease-pole FAIL) | '
                     'MPFB_PIPKIN_COMPACT_BRANCH_v001 (aspect classes; counted rings B / T1 / T2 dark blue) | v005 toes (toe 3 / 4 MTP stations: validator-geometry failure, no topology change)',
                     [(i, [img('B0_' + i, 't1'), img('B1_' + i, 't1'), img('B2_' + i, 't1'), img('B3_' + i, 'toe')]) for i in TB], ['v005', 'Durrim v002 (diagnostic)', 'Pipkin branch v001', 'v005 toes'], colw=320,
                     note='Aspect classes on the branch faces only: green <= 3:1, amber 3-4:1, red > 4:1.')
if 'C' in SEL: sheet('PK_C_branch_realizations.jpg', 'C. Pipkin on MPFB_PIPKIN_COMPACT_BRANCH_v001: c1 PK-NAT | c2 PKF107-NAT -- branch realizations, NOT production candidates (toe-station author decision pending)',
                     [('c1 PK-NAT', [img('C_PK-NAT', v) for v in AV]), ('c2 PKF107-NAT', [img('C_PKF107-NAT', v) for v in AV])], AH, colw=230)
if 'D' in SEL: sheet('PK_D_122_pipkin_vs_durrim.jpg', 'D. 122 cm real-height boundary: Pipkin PK122 (Pipkin branch) | Durrim DU122C (frozen RP4 compact branch v002). Same ortho scale.',
                     [('Pipkin 122', [img('D_PK122', v) for v in ('front', 'tqf', 'side', 'pelvis', 'hand', 'foot')]), ('Durrim 122', [img('D_DU122', v) for v in ('front', 'tqf', 'side', 'pelvis', 'hand', 'foot')])],
                     ['front', 'front 3/4', 'side', 'torso / pelvis', 'hand', 'foot'], colw=260)
if 'E' in SEL: sheet('PK_E_adult_vs_child.jpg', 'E. Adult vs child firewall (ears hidden, no hair / clothing / scale context): adult Pipkin vs generator human-child proxy at matched stature -- the proxy is DIAGNOSTIC ONLY',
                     [('Pipkin 107 (PK-NAT)', [img('E_PK-NAT', v) for v in ('hf', 'hs', 'bf', 'bs')]), ('child proxy 107 (~6 y)', [img('E_CHILD6', v) for v in ('hf', 'hs', 'bf', 'bs')]),
                      ('Pipkin 91 (PK91)', [img('E_PK91-NAT', v) for v in ('hf', 'hs', 'bf', 'bs')]), ('child proxy 91 (~3 y)', [img('E_CHILD3', v) for v in ('hf', 'hs', 'bf', 'bs')])],
                     ['head front', 'head side', 'body front', 'body side'], colw=300)
if 'F' in SEL: sheet('PK_F_normalized_vs_marchfolk.jpg', 'F. Normalized silhouettes (each displayed at the same height; ears hidden): Pipkin is not a uniformly scaled Marchfolk',
                     [('Pipkin c1 107', [img('F_PK107', v) for v in 'fts']), ('Marchfolk c1 173', [img('F_MFM', v) for v in 'fts']), ('Pipkin c2 107', [img('F_PKF107', v) for v in 'fts']), ('Marchfolk c2 173', [img('F_MFF', v) for v in 'fts'])],
                     ['front', 'front 3/4', 'side'], colw=300)
if 'G' in SEL: sheet('PK_G_pipkin_vs_cogling.jpg', 'G. Pipkin vs Cogling context at real height (ears hidden): 91 cm PK91 | CGJ7, and 107 cm PK-NAT | CG107-NAT -- comparison only, no Cogling production work',
                     [('Pipkin 91', [img('G_PK91', v) for v in 'fts']), ('Cogling 91', [img('G_CG91', v) for v in 'fts']), ('Pipkin 107', [img('G_PK107', v) for v in 'fts']), ('Cogling 107', [img('G_CG107', v) for v in 'fts'])],
                     ['front', 'front 3/4', 'side'], colw=300)
if 'H' in SEL:
    rows = [(i, [img('H_%s_%s' % (i, p), v) for p in ('thumb_opposition_l', 'fist_l', 'wrist_flex60_l') for v in ('n', 'm')]) for i in ('PK-NAT', 'PKF107-NAT')]
    sheet('PK_H_deformation.jpg', 'H. Deformation on the Pipkin branch (left thumb patch, wire): thumb opposition, fist, wrist flex 60 -- back / palm views', rows,
          ['opposition', 'opposition (palm)', 'fist', 'fist (palm)', 'wrist flex', 'wrist flex (palm)'], colw=260)
print('PKSHEETS', sorted(os.listdir(OUT)))
