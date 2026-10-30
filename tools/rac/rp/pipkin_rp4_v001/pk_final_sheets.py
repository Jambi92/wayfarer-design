# pk_final_sheets.py WORK OUT : RP4 Pipkin final production boards (order 68ba8e5 §8): the Pipkin bodies are the FINAL production realizations
# (MPFB_PIPKIN_COMPACT_BRANCH_v001; identical geometry to PK_M / PK_F_REF_RP4_v001 read-back); comparators as pk_sheets.py (frozen Durrim RP4 DU122C realization,
# generator child proxies = diagnostic only, Marchfolk 173 normalized, Cogling r6 references = context only). Ears hidden where marked: external ear
# (hm08 w_ears > 0.05, carried through the production map M for Pipkin) harmonically filled -- board only.
#   PKF_C candidates c1 / c2   PKF_D 122 Pipkin vs Durrim   PKF_E adult vs child   PKF_F normalized vs Marchfolk   PKF_G Pipkin vs Cogling
import sys, os, json, numpy as np, scipy.sparse as sp
sys.argv = [sys.argv[0], sys.argv[1], sys.argv[2]]; W, OUT = sys.argv[1:3]
os.environ['BOARDS'] = ''                                                         # reuse helpers only
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pk_sheets.py')).read()
exec(src.split('# ---------- A / C')[0])                                          # job / img / r6mesh / collapse_ears / body_views / sheet helpers
exec('def sheet' + src.split('def sheet', 1)[1].split("if 'A' in SEL")[0])
TMP = W + '/sheets_final_r'; os.makedirs(TMP, exist_ok=True); globals()['TMP'] = TMP; os.makedirs(OUT, exist_ok=True)
F = W + '/final/cb'; RAP = '/home/claude/wayfarer-design/reviews/reference-assets/r6'
def prod(i):
    z = np.load('%s/%s_pkb.npz' % (F, i)); J = {k: np.array(v) for k, v in json.loads(str(z['meta']))['heads'].items()}; return z['V'].astype(float), np.asarray(z['Q']), J, z
def prod_ears(i, z):
    r6 = np.load(W + '/nat/PKF107-NAT_r6.npz') if i == 'PKF107-NAT' else np.load('%s/%s_r6.npz' % (RAP, i))
    M = sp.csr_matrix((z['M_data'], z['M_indices'], z['M_indptr']), shape=tuple(z['M_shape'])); return (M @ r6['w_ears'][z['src_index']].astype(float)) > 0.05
for i in ('PK-NAT', 'PKF107-NAT'):
    V, Q, J, z = prod(i); job('C_' + i, V, Q, None, body_views(V, J))
V, Q, J, z = prod('PK122-NAT'); bv = dict((v[0], v) for v in body_views(V, J, H=122.0)); job('D_PK122', V, Q, None, [bv[k] for k in ('front', 'tqf', 'side', 'pelvis', 'hand', 'foot')])
d = np.load('/tmp/claude-0/rt/du/v2/cb2/DU122C-NAT_cb2.npz'); Vd = d['V'].astype(float); Jd = {k: np.array(v) for k, v in json.loads(str(d['meta']))['heads'].items()}
bv = dict((v[0], v) for v in body_views(Vd, Jd, H=122.0)); job('D_DU122', Vd, d['Q'], None, [bv[k] for k in ('front', 'tqf', 'side', 'pelvis', 'hand', 'foot')])
def headviews(V, H):
    top = V[:, 2].max(); hd = np.array([0, np.median(V[V[:, 2] > top - 0.13 * H][:, 1]), top - 0.07 * H]); c0 = np.array([0, np.median(V[:, 1]), H / 2])
    return [('hf', (0, 1, 0.03), hd, 0.095 * H), ('hs', (1, 0, 0.02), hd + np.array([0, -0.01 * H, 0]), 0.11 * H), ('bf', (0, 1, 0.02), c0, H * 0.56), ('bs', (1, 0, 0.02), c0, H * 0.56)]
for i, H in (('PK-NAT', 107.0), ('PK91-NAT', 91.0)):
    V, Q, J, z = prod(i); Vh = collapse_ears(V, Q, prod_ears(i, z)); job('E_' + i, Vh, Q, None, headviews(Vh, H))
for c, H in (('CHILD6', 107.0), ('CHILD3', 91.0)):
    V, Fc, J, z = r6mesh('%s/child/%s_r6.npz' % (W, c)); Vh = collapse_ears(V, Fc, np.asarray(z['w_ears']) > 0.05); job('E_' + c, Vh, Fc, None, headviews(Vh, H))
for tag, i in (('PK107', 'PK-NAT'), ('PKF107', 'PKF107-NAT')):
    V, Q, J, z = prod(i); V = collapse_ears(V, Q, prod_ears(i, z)); V = V * (173.0 / V[:, 2].max()); c0 = np.array([0, np.median(V[:, 1]), 173 / 2])
    job('F_' + tag, V, Q, None, [('f', (0, 1, 0.02), c0, 97), ('t', (1, 1, 0.05), c0, 97), ('s', (1, 0, 0.02), c0, 97)])
for tag, path in (('MFM', '%s/full/MF-M-R_r6.npz' % W), ('MFF', '%s/full/MF-F-R_r6.npz' % W)):
    V, Fc, J, z = r6mesh(path); V = collapse_ears(V, Fc, np.asarray(z['w_ears']) > 0.05); V = V * (173.0 / V[:, 2].max()); c0 = np.array([0, np.median(V[:, 1]), 173 / 2])
    job('F_' + tag, V, Fc, None, [('f', (0, 1, 0.02), c0, 97), ('t', (1, 1, 0.05), c0, 97), ('s', (1, 0, 0.02), c0, 97)])
for tag, i, H in (('PK91', 'PK91-NAT', 91.0), ('PK107', 'PK-NAT', 107.0)):
    V, Q, J, z = prod(i); V = collapse_ears(V, Q, prod_ears(i, z)); c0 = np.array([0, np.median(V[:, 1]), H / 2])
    job('G_' + tag, V, Q, None, [('f', (0, 1, 0.02), c0, H * 0.56), ('t', (1, 1, 0.05), c0, H * 0.56), ('s', (1, 0, 0.02), c0, H * 0.56)])
for tag, path, H in (('CG91', '%s/full/CGJ7_r6.npz' % W, 91.0), ('CG107', '%s/full/CG107-NAT_r6.npz' % W, 107.0)):
    V, Fc, J, z = r6mesh(path); V = collapse_ears(V, Fc, np.asarray(z['w_ears']) > 0.05); c0 = np.array([0, np.median(V[:, 1]), H / 2])
    job('G_' + tag, V, Fc, None, [('f', (0, 1, 0.02), c0, H * 0.56), ('t', (1, 1, 0.05), c0, H * 0.56), ('s', (1, 0, 0.02), c0, H * 0.56)])
from concurrent.futures import ThreadPoolExecutor
import subprocess
with ThreadPoolExecutor(2) as ex: list(ex.map(lambda j: subprocess.run(j, env=ENV, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL), jobs))
sheet('PKF_C_production_candidates.jpg', 'C. Pipkin production reference candidates PK_M_REF_RP4_v001 (c1, PK-NAT) | PK_F_REF_RP4_v001 (c2, PKF107-NAT) on MPFB_PIPKIN_COMPACT_BRANCH_v001 -- CANDIDATE / NOT FROZEN',
      [('PK_M_REF_RP4_v001', [img('C_PK-NAT', v) for v in AV]), ('PK_F_REF_RP4_v001', [img('C_PKF107-NAT', v) for v in AV])], AH, colw=230)
sheet('PKF_D_122_pipkin_vs_durrim.jpg', 'D. 122 cm real height, final production realizations: Pipkin PK122 (Pipkin branch v001) | Durrim DU122C (frozen RP4 compact branch v002). Same ortho scale.',
      [('Pipkin 122', [img('D_PK122', v) for v in ('front', 'tqf', 'side', 'pelvis', 'hand', 'foot')]), ('Durrim 122', [img('D_DU122', v) for v in ('front', 'tqf', 'side', 'pelvis', 'hand', 'foot')])],
      ['front', 'front 3/4', 'side', 'torso / pelvis', 'hand', 'foot'], colw=260)
sheet('PKF_E_adult_vs_child.jpg', 'E. Adult vs child (ears hidden; no hair / wrinkles / clothing / scale context): Pipkin final production realization vs generator human-child proxy at matched stature -- proxy DIAGNOSTIC ONLY',
      [('Pipkin 107', [img('E_PK-NAT', v) for v in ('hf', 'hs', 'bf', 'bs')]), ('child proxy 107 (~6 y)', [img('E_CHILD6', v) for v in ('hf', 'hs', 'bf', 'bs')]),
       ('Pipkin 91', [img('E_PK91-NAT', v) for v in ('hf', 'hs', 'bf', 'bs')]), ('child proxy 91 (~3 y)', [img('E_CHILD3', v) for v in ('hf', 'hs', 'bf', 'bs')])], ['head front', 'head side', 'body front', 'body side'], colw=300)
sheet('PKF_F_normalized_vs_marchfolk.jpg', 'F. Normalized silhouettes (equal display height; ears hidden): Pipkin final production realizations vs Marchfolk 173 -- intentionally subtle, not a uniform scale',
      [('Pipkin c1', [img('F_PK107', v) for v in 'fts']), ('Marchfolk c1', [img('F_MFM', v) for v in 'fts']), ('Pipkin c2', [img('F_PKF107', v) for v in 'fts']), ('Marchfolk c2', [img('F_MFF', v) for v in 'fts'])], ['front', 'front 3/4', 'side'], colw=300)
sheet('PKF_G_pipkin_vs_cogling.jpg', 'G. Pipkin (final production realization) vs Cogling references at real height (ears hidden) -- comparison only, intentionally subtle; no Cogling production work',
      [('Pipkin 91', [img('G_PK91', v) for v in 'fts']), ('Cogling 91', [img('G_CG91', v) for v in 'fts']), ('Pipkin 107', [img('G_PK107', v) for v in 'fts']), ('Cogling 107', [img('G_CG107', v) for v in 'fts'])], ['front', 'front 3/4', 'side'], colw=300)
print('PKFINALSHEETS', sorted(os.listdir(OUT)))
