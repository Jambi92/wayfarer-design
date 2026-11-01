# sa_boards_final.py CAGE.npz DESIGN.pkl OUTDIR : FINAL boards A-P (order 236dddc §15), workbench clay / wire renders (sa_render machinery). No WIP labels.
#   A thigh art-pass before / after / difference   B full wire   C poles / valence   D head / rostrum   E neck / throat   F shoulders / arms (+ axillary vault)
#   G hands / claws   H pelvis / sacrum / tail root   I legs / feet   J tail   K c1 / c2 overlay + difference   L deviation heat maps (T-1 per cage vertex)
#   M density   N layered detail (cage-derived detail surface vs canonical surfaced)   O worst deformation poses + ownership labels   P creator-support states
import sys, os, json, numpy as np, igl
CG, DS, OUT = sys.argv[1:4]; os.makedirs(OUT, exist_ok=True); os.environ['SA_OUT'] = OUT; ARGV = list(sys.argv); sys.argv = [sys.argv[0]]
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/saurin_rp5_v001'); import sa_render as R
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_geo as G, sa_ccage as CC
from PIL import Image, ImageDraw
W = '/tmp/claude-0/rt/sa'; LBL = 'SAURIN RP5 full authored cage -- PILOT / NOT FROZEN'
z = np.load(CG); Q = z['Q']; fi, bc = z['tri'], z['bc']; F = G.F; ql = z['qlab'].astype(str)
VM = (bc[:, :, None] * G.V[F[fi]]).sum(1); VF = (bc[:, :, None] * G.VF2[F[fi]]).sum(1); nv = len(VM); T = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]
E = np.unique(np.sort(np.r_[Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]], 1), axis=0); val = np.bincount(E.ravel(), minlength=nv)
GREY = np.array(R.GREY, float); L = G.LM; g = lambda k: np.asarray(L[k])
def heat(x, lo, hi):
    t = np.clip((x - lo) / (hi - lo), 0, 1); return np.c_[0.25 + 0.7 * t, 0.75 - 0.55 * t * (t > 0.5) + 0.0 * t, 0.9 - 0.75 * t]
C0 = np.array([0, -30, 95.0]); BODY = [('front', (0, 1, 0.02), C0, 205), ('side', (1, 0, 0.02), C0, 205), ('rear', (0, -1, 0.02), C0, 205), ('tq', (0.7, 0.7, 0.1), C0, 205)]
hc = np.array([0, 8, 180.0]); HEAD = [('front', (0, 1, 0.05), hc, 22), ('tq', (0.8, 0.8, 0.2), hc, 22), ('side', (1, 0, 0.02), hc, 22), ('under', (0.2, 0.6, -1), hc, 22)]
nc = np.array([0, 2, 166.0]); NECK = [('front', (0, 1, -0.25), nc, 30), ('side', (1, 0, 0.0), nc, 30), ('under', (0.2, 0.7, -1), nc, 30), ('rear', (0, -1, 0.1), nc, 30)]
rc = g('tail_root_centre'); ROOT = [('side', (1, 0, 0.1), rc + [0, -6, 0], 42), ('rear', (0.2, -1, 0.3), rc + [0, -6, 0], 42), ('under', (0.2, -0.3, -1), rc + [0, -6, 0], 42)]
tc = 0.5 * (g('tail_root_centre') + g('tail_tip')); TAIL = [('side', (1, 0, 0.05), tc, 150), ('top', (0.05, 0, 1), tc, 150), ('rear', (0.3, -1, 0.3), tc, 150)]
jobs = []
def J(tag, V, F_, col, views, wire=True, px=900, title=''): jobs.append((tag, V, F_, col, views, wire, px, title))
# A thigh art-pass: canonical base vs SA_RP5_WORK_v001, difference heat
b0 = np.load(W + '/src/saurin_w2_final_base.npz')['v'].astype(float); dth = np.linalg.norm(G.V - b0, axis=1) * 10
th = (np.abs(G.V[:, 2] - 70) < 30) & (np.abs(G.V[:, 0]) < 30); Fth = F[th[F].all(1)]; thc = np.array([0, 0, 70.0])
TV = [('front', (0, 1, 0.05), thc, 62), ('side', (1, 0, 0.05), thc, 62), ('rear', (0, -1, 0.05), thc, 62)]
J('A_thigh_before', b0, Fth, None, TV, False, 800, 'A thigh: canonical W2I6 base (before)'); J('A_thigh_after', G.V, Fth, None, TV, False, 800, 'A thigh: SA_RP5_WORK_v001 art-pass (after, CLOSED)')
J('A_thigh_diff', G.V, Fth, heat(dth, 0, 2.0), TV, False, 800, 'A thigh: |after - before| 0 (blue) .. 2 mm (red)')
J('B_wire', VM, Q, None, BODY, True, 1100, 'B full wire (c1)')
colp = np.tile(GREY, (nv, 1)); colp[val == 3] = [0.15, 0.6, 0.2]; colp[val == 5] = [0.85, 0.15, 0.1]; colp[val >= 6] = [0.6, 0.1, 0.8]
J('C_poles', VM, Q, colp, BODY, True, 1100, 'C poles: valence 3 green, 5 red, 6+ purple')
J('D_head', VM, Q, None, HEAD, True, 900, 'D head / rostrum'); J('E_neck', VM, Q, None, NECK, True, 900, 'E neck / throat')
for s, sg in (('xpos', 1), ('xneg', -1)):
    sc = g('glenohumeral_' + s) + np.array([sg * 2, 0, -4.0]); J('F_shoulder_' + s, VM, Q, None, [('lat', (sg, 0, 0.1), sc, 30), ('front', (0, 1, 0.1), sc, 30), ('rear', (0, -1, 0.1), sc, 30), ('vault', (sg * 0.6, -0.5, -0.6), sc + [sg * -3, -4, -2], 12)], True, 900, 'F shoulder / arm + axillary vault patch ' + s)
    hc2 = g('wrist_' + s) + np.array([sg * 5, 2, -8.0]); J('G_hand_' + s, VM, Q, None, [('lat', (sg, 0.1, 0.1), hc2, 18), ('med', (-sg, 0.1, 0.1), hc2, 18), ('front', (0, 1, 0), hc2, 18), ('palm', (-sg * 0.6, 0.6, 0.3), hc2, 14)], True, 900, 'G hand / claws ' + s)
    fc = g('ankle_' + s) * [1, 1, 0] + np.array([0, 12, 4.0]); J('I_foot_' + s, VM, Q, None, [('top', (0, 0.05, 1), fc, 32), ('side', (sg, 0, 0.1), fc, 32), ('under', (0, 0.05, -1), fc, 32), ('leg', (sg, 0.3, 0.05), np.array([g('knee_' + s)[0], 0, 50.0]), 105)], True, 900, 'I leg / foot ' + s)
J('H_root', VM, Q, None, ROOT, True, 900, 'H pelvis / sacrum / tail root (module ring 0 = cage tail hole)'); J('J_tail', VM, Q, None, TAIL, True, 1000, 'J tail (accepted module, unchanged)')
J('K_c1', VM, Q, None, BODY[:3], True, 900, 'K c1 SA-M188'); J('K_c2', VF, Q, None, BODY[:3], True, 900, 'K c2 SA-F188 (same face list / vertex order)')
J('K_c1c2_diff', VF, Q, heat(np.linalg.norm(VF - VM, axis=1), 0, 3.0), BODY[:3], False, 900, 'K |c2 - c1| per vertex 0 .. 3 cm')
# L deviation heat: per cage vertex the max distance of the source vertices it covers (nearest-vertex assignment)
d = np.sqrt(igl.point_mesh_squared_distance(G.V, VM, T)[0]) * 10; _, near = __import__('scipy.spatial', fromlist=['cKDTree']).cKDTree(VM).query(G.V); dv = np.zeros(nv); np.maximum.at(dv, near, d)
J('L_dev_body', VM, Q, heat(dv, 0, 3.0), BODY, False, 1000, 'L T-1 deviation source -> cage, per cage vertex: 0 (blue) .. 3 mm (red)')
J('L_dev_head', VM, Q, heat(dv, 0, 1.5), HEAD, False, 900, 'L T-2 head deviation 0 .. 1.5 mm')
el = np.zeros(nv); np.maximum.at(el, E[:, 0], np.linalg.norm(VM[E[:, 0]] - VM[E[:, 1]], axis=1)); J('M_density', VM, Q, heat(el, 0, 1.13), BODY, False, 900, 'M density: longest incident edge 0 .. 11 mm')
# N layered detail (head / hand close-ups): cage + 2 CC levels + transported canonical relief vs canonical surfaced
dz = np.load(W + '/src/saurin_w2_final_surface_delta.npz')['d'].astype(float); Vu0, Fu = igl.upsample(b0, F); rel = (dz * igl.per_vertex_normals(Vu0, Fu)).sum(1)
Vc0 = (bc[:, :, None] * b0[F[fi]]).sum(1); Vs, Qs, _ = CC.cc(Vc0, Q, np.arange(len(Q))); Vs, Qs, _ = CC.cc(Vs, Qs, np.arange(len(Qs)))
_, ti, cp = igl.point_mesh_squared_distance(Vs, b0, F); kids = Fu.reshape(len(F), 4, 3)[ti]; Nu = igl.per_vertex_normals(Vu0, Fu)
w_ = 1.0 / (np.linalg.norm(Vu0[kids].reshape(len(cp), 12, 3) - cp[:, None], axis=2) + 1e-4); rr = (w_ * rel[kids.reshape(len(cp), 12)]).sum(1) / w_.sum(1)
nn = (w_[:, :, None] * Nu[kids.reshape(len(cp), 12)]).sum(1); nn /= np.linalg.norm(nn, axis=1, keepdims=True); Dsurf = cp + rr[:, None] * nn
for nm_, cen, vw, h in (('head', hc, (0.8, 0.8, 0.2), 16), ('hand', g('wrist_xpos') + [5, 2, -8.0], (1, 0.1, 0.1), 14), ('flank', np.array([14, -5, 125.0]), (1, 0.2, 0.1), 26)):
    mS = np.linalg.norm(Vs - cen, axis=1) < 1.2 * h; Qd = Qs[mS[Qs].all(1)]
    mU = np.linalg.norm(Vu0 - cen, axis=1) < 1.2 * h; Fd = Fu[mU[Fu].all(1)]
    J('N_detail_' + nm_, Dsurf, Qd, None, [('cage_detail', vw, cen, h)], False, 900, 'N layered detail %s: cage-derived detail surface' % nm_)
    J('N_canon_' + nm_, Vu0 + dz, Fd, None, [('canonical', vw, cen, h)], False, 900, 'N canonical surfaced organism %s' % nm_)
# O worst deformation poses with ownership labels
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sa_deform4.py')).read().split('res = {}')[0]
ns = {'__file__': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sa_deform4.py')}; sys.argv = ['x', CG, DS, '/dev/null']; exec(compile(src, 'd4', 'exec'), ns)
D4 = json.load(open(os.path.join(os.path.dirname(CG), 'd4_final.json')))['poses'] if os.path.exists(os.path.join(os.path.dirname(CG), 'd4_final.json')) else {}
worst = sorted(D4, key=lambda k: -D4[k]['step1_cage_flips'])[:6] if D4 else ['fist_xpos', 'neck_flex_30', 'shoulder_abd90_xpos', 'tail_root_vertical_25', 'hip_flex70_xpos', 'thumb_opposition_xneg']
for pn in worst:
    Tp = ns['pose'](ns['POSES'][pn]); P3 = ns['skin'](ns['Vc'], ns['W3'], Tp); c3 = ns['relcos'](ns['n0c'], ns['qn'](P3), ns['W3'], Q, Tp)
    col = np.tile(GREY, (nv, 1)); col[Q[c3 < 0].ravel()] = [0.9, 0.15, 0.1]; cen = P3[Q[c3 < 0].ravel()].mean(0) if (c3 < 0).any() else P3.mean(0)
    lab_ = D4.get(pn, {}).get('classification', ''); J('O_' + pn, P3, Q, col, [('a', (0.7, 0.7, 0.2), cen, 40), ('b', (-0.7, -0.7, 0.2), cen, 40)], True, 900, 'O %s (improved diagnostic weights; red = folded quads) -- %s' % (pn, lab_))
# P creator-support states
CR = json.load(open(os.path.join(os.path.dirname(CG), 'creator_final.json'))) if os.path.exists(os.path.join(os.path.dirname(CG), 'creator_final.json')) else {}
for st in ['NAR', 'BRD', 'MUFAHI', 'T80', 'M168', 'M208-B', 'ORB-8', 'ORB+3', 'RDG1.30', 'DSP-HIGH']:
    p = W + '/cr_%s.npy' % st
    if not os.path.exists(p): continue
    VB = np.load(p).astype(float); Pc = (bc[:, :, None] * VB[F[fi]]).sum(1); head = st.startswith(('ORB', 'RDG', 'DSP'))
    vw = HEAD[:2] if head else BODY[:2]; J('P_' + st, Pc, Q, None, vw, True, 900, 'P creator state %s -- %s' % (st, CR.get(st, {}).get('verdict', '')))
for j in jobs: R.job(j[0], j[1], j[2], j[3], j[4], wire=j[5], px=j[6])
R.run()
def strip(tag, views, title):
    ims = [R.img(tag, v[0]).resize((520, 520)) for v in views]; W_ = 520 * len(ims); M = Image.new('RGB', (max(W_, 1040), 560), 'white'); ImageDraw.Draw(M).text((10, 8), title + '   |   ' + LBL, fill=(0, 0, 0))
    for i, im in enumerate(ims): M.paste(im, (520 * i, 40))
    M.save(OUT + '/%s.jpg' % tag, quality=88)
for j in jobs: strip(j[0], j[4], j[7])
print('boards', len(jobs))
