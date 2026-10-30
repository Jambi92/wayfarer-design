# cg_sheets.py WORK OUT : RP4 Cogling boards (order 9424c72 §20). Neutral clay, orthographic, workbench renders (render_attr.py via hv_ear_quick); diagnostic.
#   A central sources c1 CGJ7 / c2 CGF91-NAT on v005           B compact topology diagnosis per body: thumb wire v005 | Durrim v002 | Pipkin v001 (diagnostic) |
#     Cogling branch v001 (aspect classes + counted rings) | finger close-up | foot / toe wire | face wire
#   C bounds 76 / 91 c1 / 91 c2 / 107 on the Cogling branch     D Cogling vs frozen Pipkin RP4 at equal real height 91 / 107 (ears hidden)
#   E Cogling max 107 vs frozen Durrim RP4 min 122 at REAL height (same ortho scale)   F adult vs generator child proxy (76 / 91; DIAGNOSTIC ONLY)
#   G normalized Cogling vs Marchfolk 173                        H hidden identity: hands hidden / head + hands + feet hidden (Cogling | Pipkin | Marchfolk at 91)
#   I deformation on the Cogling branch: worst hand / foot poses
# Ears hidden where marked: hm08 w_ears > 0.05 harmonically filled (board only). Hidden regions (H): faces whose vertices carry the region's source weights removed.
import sys, os, json, subprocess, numpy as np
from concurrent.futures import ThreadPoolExecutor
W, OUT = sys.argv[1:3]
os.environ['BOARDS'] = ''
src = open('/home/claude/wayfarer-design/tools/rac/rp/pipkin_rp4_v001/pk_sheets.py').read()
exec(src.split('# ---------- A / C')[0])                                          # job / img / r6mesh / fammesh / collapse_ears / body_views / aspect / aheat
exec('def sheet' + src.split('def sheet', 1)[1].split("if 'A' in SEL")[0])
exec('def thumb_view' + src.split('def thumb_view', 1)[1].split("if 'B' in SEL")[0])
TMP = W + '/sheets_r'; os.makedirs(TMP, exist_ok=True); globals()['TMP'] = TMP; os.makedirs(OUT, exist_ok=True)
RA = '/home/claude/wayfarer-design/reviews/reference-assets/r6'; PKF = '/tmp/claude-0/rt/pk/final/cb'; SEL = os.environ.get('CGB', 'ABCDEFGHI')
import scipy.sparse as sp
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/cogling_rp4_v001'); import cg_branch_v001 as CB
DEF = json.load(open(W + '/br/MPFB_COGLING_COMPACT_BRANCH_v001.json'))
def r6path(i): return W + '/nat/CGF91-NAT_r6.npz' if i == 'CGF91-NAT' else '%s/%s_r6.npz' % (RA, i)
def mesh_ears(z, r6p):
    r6 = np.load(r6p); M = sp.csr_matrix((z['M_data'], z['M_indices'], z['M_indptr']), shape=tuple(z['M_shape'])); return (M @ r6['w_ears'][z['src_index']].astype(float)) > 0.05
def heads(z): return {k: np.array(v) for k, v in json.loads(str(z['meta']))['heads'].items()}
CGS = ('CG76H-NAT', 'CGJ7', 'CGF91-NAT', 'CG107-NAT')
def cgb(i): z = np.load('%s/v1/cb/%s_cgb.npz' % (W, i), allow_pickle=True); return z['V'].astype(float), np.asarray(z['Q']), heads(z), z
# ---------- A
if 'A' in SEL:
    for i in ('CGJ7', 'CGF91-NAT'): V, Q, J, z = fammesh('%s/fam/%s_fam.npz' % (W, i)); job('A_' + i, V, Q, None, body_views(V, J))
# ---------- B
if 'B' in SEL:
    for i in CGS:
        V, Q, J, z = fammesh('%s/fam/%s_fam.npz' % (W, i)); tv = thumb_view(J); s = V[:, 2].max() / 107.0; job('B0_' + i, V, Q, None, tv, wire=True)
        for tg, p in (('B1', '%s/inh/%s_du2.npz' % (W, i)), ('B2', '%s/inh/%s_pk1.npz' % (W, i))):
            d = np.load(p); Vd = d['V'].astype(float); Qd = np.asarray(d['Q']); job('%s_%s' % (tg, i), Vd, Qd, aheat(Vd, Qd, d['branch_thumb_faces']), tv, wire=True)
        Vb, Qb, Jb, b = cgb(i); col = aheat(Vb, Qb, b['branch_thumb_faces']); rr = CB.realize(dict(np.load('%s/fam/%s_fam.npz' % (W, i), allow_pickle=True)), DEF)['info']['l']['fine_rings']
        for rn in ('B', 'T1', 'T2'): col[rr[rn]] = [0.1, 0.2, 0.75]
        job('B3_' + i, Vb, Qb, col, tv, wire=True)
        fg = 0.5 * (J['index_02_l'] + J['middle_02_l']); job('B4_' + i, V, Q, None, [('fing', (0.2, 0.5, -1.0), fg, 3.0 * s)], wire=True)
        job('B5_' + i, V, Q, None, [('toe', (0.35, 1, 0.9), J['ball_l'] + np.array([0, 2.0 * s, 0]), 4.5 * s)], wire=True)
        top = V[:, 2].max(); hd = np.array([0, np.median(V[V[:, 2] > top - 0.13 * top][:, 1]), top - 0.075 * top]); job('B6_' + i, V, Q, None, [('face', (0.25, 1, 0.05), hd, 0.07 * top)], wire=True)
# ---------- C bounds (branch realizations)
if 'C' in SEL:
    for i in CGS:
        V, Q, J, z = cgb(i); bv = dict((v[0], v) for v in body_views(V, J, H=V[:, 2].max())); job('C_' + i, V, Q, None, [bv[k] for k in ('front', 'tqf', 'side', 'head', 'hand', 'foot')])
# ---------- D Cogling vs frozen Pipkin RP4 (equal real height, ears hidden)
if 'D' in SEL:
    for tag, kind, i, H in (('CG91', 'cg', 'CGJ7', 91.0), ('PK91', 'pk', 'PK91-NAT', 91.0), ('CG107', 'cg', 'CG107-NAT', 107.0), ('PK107', 'pk', 'PK-NAT', 107.0), ('CGF91', 'cg', 'CGF91-NAT', 91.0)):
        if kind == 'cg': V, Q, J, z = cgb(i); ear = mesh_ears(z, r6path(i))
        else:
            z = np.load('%s/%s_pkb.npz' % (PKF, i), allow_pickle=True); V = z['V'].astype(float); Q = np.asarray(z['Q']); J = heads(z); ear = mesh_ears(z, '%s/%s_r6.npz' % (RA, i))
        V = collapse_ears(V, Q, ear); bv = dict((v[0], v) for v in body_views(V, J, H=H)); job('D_' + tag, V, Q, None, [bv[k] for k in ('front', 'tqf', 'side', 'rear', 'pelvis', 'hand', 'foot')])
# ---------- E Cogling 107 vs Durrim 122 (real height, same ortho frame)
if 'E' in SEL:
    V, Q, J, z = cgb('CG107-NAT'); bv = dict((v[0], v) for v in body_views(V, J, H=122.0)); job('E_CG107', V, Q, None, [bv[k] for k in ('front', 'tqf', 'side', 'pelvis', 'hand', 'foot')])
    d = np.load('/tmp/claude-0/rt/du/v2/cb2/DU122C-NAT_cb2.npz'); Vd = d['V'].astype(float); bv = dict((v[0], v) for v in body_views(Vd, heads(d), H=122.0))
    job('E_DU122', Vd, d['Q'], None, [bv[k] for k in ('front', 'tqf', 'side', 'pelvis', 'hand', 'foot')])
# ---------- F adult vs child (ears hidden)
def headviews(V, H):
    top = V[:, 2].max(); hd = np.array([0, np.median(V[V[:, 2] > top - 0.13 * H][:, 1]), top - 0.07 * H]); c0 = np.array([0, np.median(V[:, 1]), H / 2])
    return [('hf', (0, 1, 0.03), hd, 0.095 * H), ('hs', (1, 0, 0.02), hd + np.array([0, -0.01 * H, 0]), 0.11 * H), ('bf', (0, 1, 0.02), c0, H * 0.56), ('bs', (1, 0, 0.02), c0, H * 0.56)]
if 'F' in SEL:
    for i, H in (('CG76H-NAT', 76.0), ('CGJ7', 91.0)):
        V, Q, J, z = cgb(i); Vh = collapse_ears(V, Q, mesh_ears(z, r6path(i))); job('F_' + i, Vh, Q, None, headviews(Vh, H))
    for c, p, H in (('CHILD1', W + '/child/CHILD1_r6.npz', 76.0), ('CHILD3', '/tmp/claude-0/rt/pk/child/CHILD3_r6.npz', 91.0)):
        V, Fc, J, z = r6mesh(p); Vh = collapse_ears(V, Fc, np.asarray(z['w_ears']) > 0.05); job('F_' + c, Vh, Fc, None, headviews(Vh, H))
# ---------- G normalized vs Marchfolk
if 'G' in SEL:
    for tag, i in (('CG91', 'CGJ7'), ('CGF91', 'CGF91-NAT')):
        V, Q, J, z = cgb(i); V = collapse_ears(V, Q, mesh_ears(z, r6path(i))); V = V * (173.0 / V[:, 2].max()); c0 = np.array([0, np.median(V[:, 1]), 173 / 2])
        job('G_' + tag, V, Q, None, [('f', (0, 1, 0.02), c0, 97), ('t', (1, 1, 0.05), c0, 97), ('s', (1, 0, 0.02), c0, 97)])
    for tag, p in (('MFM', W + '/full/MF-M-R_r6.npz'), ('MFF', W + '/full/MF-F-R_r6.npz')):
        V, Fc, J, z = r6mesh(p); V = collapse_ears(V, Fc, np.asarray(z['w_ears']) > 0.05); V = V * (173.0 / V[:, 2].max()); c0 = np.array([0, np.median(V[:, 1]), 173 / 2])
        job('G_' + tag, V, Fc, None, [('f', (0, 1, 0.02), c0, 97), ('t', (1, 1, 0.05), c0, 97), ('s', (1, 0, 0.02), c0, 97)])
# ---------- H hidden identity (accepted R-6 sources, all displayed at 91 cm; Marchfolk normalized)
HIDE = {'hands': ('hand_l', 'hand_r', 'fingers_l', 'fingers_r'), 'hhf': ('hand_l', 'hand_r', 'fingers_l', 'fingers_r', 'head', 'ears', 'foot_l', 'foot_r', 'ball_l', 'ball_r')}
if 'H' in SEL:
    for tag, p in (('CG91', RA + '/CGJ7_r6.npz'), ('PK91', RA + '/PK91-NAT_r6.npz'), ('MF', W + '/full/MF-M-R_r6.npz')):
        V, Fc, J, z = r6mesh(p); V = V * (91.0 / V[:, 2].max()); c0 = np.array([0, np.median(V[:, 1]), 91 / 2])
        for hk, keys in HIDE.items():
            w = np.sum([np.asarray(z['w_' + k], float) for k in keys], 0); F2 = Fc[(w[Fc] < 0.5).any(1)]
            job('H_%s_%s' % (hk, tag), V, F2, None, [('f', (0, 1, 0.02), c0, 91 * 0.56), ('t', (1, 1, 0.05), c0, 91 * 0.56), ('s', (1, 0, 0.02), c0, 91 * 0.56)])
# ---------- I deformation (Cogling branch)
POSES_I = (('fist_l', 'hand'), ('thumb_opposition_l', 'hand'), ('wrist_flex60_l', 'hand'), ('toe_ext30_l', 'foot'))
if 'I' in SEL:
    for i in ('CGJ7', 'CGF91-NAT'):
        b = np.load('%s/v1/cb/%s_cgb.npz' % (W, i), allow_pickle=True); Q = np.asarray(b['Q']); J = heads(b); s = b['V'][:, 2].max() / 107.0
        for pn, reg in POSES_I:
            pz = '%s/v1/def/%s_%s_cgb.npz' % (W, pn, i)
            if not os.path.exists(pz): continue
            V = np.load(pz)['V'].astype(float)
            if reg == 'hand':
                c = V[np.asarray(b['branch_part']) == 'thumb_new'][V[np.asarray(b['branch_part']) == 'thumb_new'][:, 0] > 0].mean(0); r = 4.2 * s
                job('I_%s_%s' % (i, pn), V, Q, None, [('n', (0.3, 0.6, -0.6), c, r), ('m', (-0.4, 0.8, 0.3), c, r)], wire=True)
            else:
                c = V[np.argmin(np.linalg.norm(V - (J['ball_l'] + np.array([0, 2.0 * s, 0])), axis=1))]; job('I_%s_%s' % (i, pn), V, Q, None, [('n', (0.6, 1, 0.3), c, 5.0 * s), ('m', (1, 0.2, 0.1), c, 5.0 * s)], wire=True)
print('jobs', len(jobs), flush=True)
with ThreadPoolExecutor(2) as ex: list(ex.map(lambda j: subprocess.run(j, env=ENV, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL), jobs))
AV = ('front', 'tqf', 'side', 'rear', 'head', 'hand', 'foot', 'pelvis'); AH = ['front', 'front 3/4', 'side', 'rear', 'face', 'hand', 'foot', 'pelvis']
if 'A' in SEL: sheet('CG_A_central_sources.jpg', 'A. Cogling central sources on unbranched MPFB Family Base v005 (91 cm): CGJ7 c1 (accepted W1r) | CGF91-NAT c2 (new technical anchor; CGJ7 targets / bone scales / head factor on the configuration-2 base)',
                     [('c1 CGJ7', [img('A_CGJ7', v) for v in AV]), ('c2 CGF91-NAT', [img('A_CGF91-NAT', v) for v in AV])], AH, colw=230)
if 'B' in SEL: sheet('CG_B_compact_topology_diagnosis.jpg', 'B. Compact topology diagnosis, left hand / foot / face: v005 thumb (FAIL 1-2 rings) | frozen Durrim v002 and Pipkin v001 thumbs applied unchanged (DIAGNOSTIC; aspect classes) | '
                     'MPFB_COGLING_COMPACT_BRANCH_v001 (Cogling placement; counted rings B / T1 / T2 dark blue) | v005 long-finger IP close-up | v005 toes (toe 3 / 4 MTP: validator geometry) | v005 face density',
                     [(i, [img('B0_' + i, 't1'), img('B1_' + i, 't1'), img('B2_' + i, 't1'), img('B3_' + i, 't1'), img('B4_' + i, 'fing'), img('B5_' + i, 'toe'), img('B6_' + i, 'face')]) for i in CGS],
                     ['v005 thumb', 'Durrim v002 (diag.)', 'Pipkin v001 (diag.)', 'Cogling branch v001', 'fingers (v005)', 'toes (v005)', 'face (v005)'], colw=270,
                     note='Aspect classes on the branch faces only: green <= 3:1, amber 3-4:1, red > 4:1.')
if 'C' in SEL: sheet('CG_C_bounds.jpg', 'C. Cogling on MPFB_COGLING_COMPACT_BRANCH_v001 across the envelope: 76 (CG76H-NAT) | 91 c1 (CGJ7) | 91 c2 (CGF91-NAT) | 107 (CG107-NAT) -- branch realizations, NOT production candidates (author decision pending)',
                     [(i, [img('C_' + i, v) for v in ('front', 'tqf', 'side', 'head', 'hand', 'foot')]) for i in CGS], ['front', 'front 3/4', 'side', 'face', 'hand', 'foot'], colw=240)
if 'D' in SEL: sheet('CG_D_cogling_vs_pipkin_equal_height.jpg', 'D. Equal real height, ears hidden: Cogling (branch realization) vs frozen Pipkin RP4 realization at 91 and 107 cm; c2 Cogling 91 for reference. Same ortho scale per pair.',
                     [('Cogling 91 c1', [img('D_CG91', v) for v in ('front', 'tqf', 'side', 'rear', 'pelvis', 'hand', 'foot')]), ('Pipkin 91 (frozen)', [img('D_PK91', v) for v in ('front', 'tqf', 'side', 'rear', 'pelvis', 'hand', 'foot')]),
                      ('Cogling 107', [img('D_CG107', v) for v in ('front', 'tqf', 'side', 'rear', 'pelvis', 'hand', 'foot')]), ('Pipkin 107 (frozen)', [img('D_PK107', v) for v in ('front', 'tqf', 'side', 'rear', 'pelvis', 'hand', 'foot')]),
                      ('Cogling 91 c2', [img('D_CGF91', v) for v in ('front', 'tqf', 'side', 'rear', 'pelvis', 'hand', 'foot')])], ['front', 'front 3/4', 'side', 'rear', 'torso / pelvis', 'hand', 'foot'], colw=230)
if 'E' in SEL: sheet('CG_E_cogling107_vs_durrim122.jpg', 'E. REAL-height context (not an equal-height test): Cogling maximum 107 cm (branch realization) | Durrim minimum 122 cm (frozen RP4). Same ortho frame (122 cm).',
                     [('Cogling 107', [img('E_CG107', v) for v in ('front', 'tqf', 'side', 'pelvis', 'hand', 'foot')]), ('Durrim 122', [img('E_DU122', v) for v in ('front', 'tqf', 'side', 'pelvis', 'hand', 'foot')])],
                     ['front', 'front 3/4', 'side', 'torso / pelvis', 'hand', 'foot'], colw=260)
if 'F' in SEL: sheet('CG_F_adult_vs_child.jpg', 'F. Adult vs child (ears hidden; no hair / wrinkles / clothing / tools / scale context): Cogling vs generator human-child proxy at matched stature -- proxy DIAGNOSTIC ONLY. 76 cm is the critical case.',
                     [('Cogling 76 (CG76H-NAT)', [img('F_CG76H-NAT', v) for v in ('hf', 'hs', 'bf', 'bs')]), ('toddler proxy 76 (~1.5 y)', [img('F_CHILD1', v) for v in ('hf', 'hs', 'bf', 'bs')]),
                      ('Cogling 91 (CGJ7)', [img('F_CGJ7', v) for v in ('hf', 'hs', 'bf', 'bs')]), ('child proxy 91 (~3 y)', [img('F_CHILD3', v) for v in ('hf', 'hs', 'bf', 'bs')])], ['head front', 'head side', 'body front', 'body side'], colw=300)
if 'G' in SEL: sheet('CG_G_normalized_vs_marchfolk.jpg', 'G. Normalized silhouettes (equal display height; ears hidden): Cogling is not a uniformly scaled Marchfolk -- distal limb redistribution, narrow core, long hands',
                     [('Cogling c1', [img('G_CG91', v) for v in 'fts']), ('Marchfolk c1', [img('G_MFM', v) for v in 'fts']), ('Cogling c2', [img('G_CGF91', v) for v in 'fts']), ('Marchfolk c2', [img('G_MFF', v) for v in 'fts'])], ['front', 'front 3/4', 'side'], colw=300)
if 'H' in SEL: sheet('CG_H_hidden_identity.jpg', 'H. Hidden-identity boards (all displayed at 91 cm; Marchfolk normalized): hands hidden, then head + hands + feet hidden -- the central body and limb organization alone',
                     [('%s %s' % (lab, hl), [img('H_%s_%s' % (hk, tag), v) for v in 'fts']) for hk, hl in (('hands', 'hands hidden'), ('hhf', 'head+hands+feet hidden')) for tag, lab in (('CG91', 'Cogling 91'), ('PK91', 'Pipkin 91'), ('MF', 'Marchfolk (norm.)'))],
                     ['front', 'front 3/4', 'side'], colw=260)
if 'I' in SEL:
    rows = [(i, [img('I_%s_%s' % (i, p), v) for p, _ in POSES_I for v in ('n', 'm')]) for i in ('CGJ7', 'CGF91-NAT')]
    sheet('CG_I_deformation.jpg', 'I. Deformation on the Cogling branch (wire): fist, thumb opposition, wrist flex 60 (hand / thumb patch), toe extension 30 (foot) -- two views each', rows,
          ['fist', 'fist (2)', 'opposition', 'opposition (2)', 'wrist flex', 'wrist flex (2)', 'toe ext', 'toe ext (2)'], colw=230)
print('CGSHEETS', sorted(os.listdir(OUT)))
