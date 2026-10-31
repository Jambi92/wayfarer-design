# sa_fc_boards.py CAGE.npz OUTDIR : RP5 full-cage boards (order ad9cb85 §23) -- clay / wire workbench renders (sa_render machinery), c1 = SA-M188 working source.
import sys, os, numpy as np, igl
CG, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True); os.environ['SA_OUT'] = OUT; sys.argv = [sys.argv[0]]
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/saurin_rp5_v001'); import sa_render as R
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_geo as G
from PIL import Image, ImageDraw
z = np.load(CG); Q = z['Q']; fi, bc = z['tri'], z['bc']; F = G.F
VM = (bc[:, :, None] * G.V[F[fi]]).sum(1); VF = (bc[:, :, None] * G.VF2[F[fi]]).sum(1); err = np.load(CG + '.err.npy') if os.path.exists(CG + '.err.npy') else None
nv = len(VM); E = np.unique(np.sort(np.r_[Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]], 1), axis=0); val = np.bincount(E.ravel(), minlength=nv)
GREY = np.array(R.GREY, float); colp = np.tile(GREY, (nv, 1)); colp[val == 3] = [0.15, 0.6, 0.2]; colp[val >= 5] = [0.85, 0.15, 0.1]
el = np.zeros(nv); np.maximum.at(el, E[:, 0], np.linalg.norm(VM[E[:, 0]] - VM[E[:, 1]], axis=1)); h = np.clip(el / 1.13, 0, 1); cold = np.c_[0.2 + 0.7 * h, 0.7 - 0.4 * h, 0.9 - 0.7 * h]
L = G.LM; g = lambda k: L[k]
C0 = np.array([0, -30, 95.0]); BODY = [('front', (0, 1, 0.02), C0, 205), ('side', (1, 0, 0.02), C0, 205), ('rear', (0, -1, 0.02), C0, 205), ('tq', (0.7, 0.7, 0.1), C0, 205)]
hc = np.array([0, 8, 180.0]); HEAD = [('front', (0, 1, 0.05), hc, 22), ('tq', (0.8, 0.8, 0.2), hc, 22), ('side', (1, 0, 0.02), hc, 22), ('under', (0.2, 0.6, -1), hc, 22)]
rc = g('tail_root_centre'); ROOT = [('side', (1, 0, 0.1), rc + [0, -6, 0], 42), ('rear', (0.2, -1, 0.3), rc + [0, -6, 0], 42), ('under', (0.2, -0.3, -1), rc + [0, -6, 0], 42)]
jobs = [('B_wire', VM, Q, None, BODY, True, 1100), ('C_poles', VM, Q, colp, BODY, True, 1100), ('M_density', VM, Q, cold, BODY, False, 900), ('D_head', VM, Q, None, HEAD, True, 900),
        ('H_root', VM, Q, None, ROOT, True, 900), ('K_c1', VM, Q, None, BODY[:3], True, 900), ('K_c2', VF, Q, None, BODY[:3], True, 900)]
for s, sg in (('xpos', 1), ('xneg', -1)):
    hc2 = g('wrist_' + s) + np.array([sg * 5, 2, -8.0]); jobs.append(('G_hand_' + s, VM, Q, None, [('lat', (sg, 0.1, 0.1), hc2, 18), ('med', (-sg, 0.1, 0.1), hc2, 18), ('front', (0, 1, 0), hc2, 18)], True, 900))
    fc = g('ankle_' + s) * [1, 1, 0] + np.array([0, 12, 4.0]); jobs.append(('I_foot_' + s, VM, Q, None, [('top', (0, 0.05, 1), fc, 32), ('side', (sg, 0, 0.1), fc, 32), ('under', (0, 0.05, -1), fc, 32)], True, 900))
    sc = g('glenohumeral_' + s) + np.array([sg * 2, 0, -4.0]); jobs.append(('F_shoulder_' + s, VM, Q, None, [('lat', (sg, 0, 0.1), sc, 30), ('front', (0, 1, 0.1), sc, 30), ('rear', (0, -1, 0.1), sc, 30)], True, 900))
for j in jobs: R.job(j[0], j[1], j[2], j[3], j[4], wire=j[5], px=j[6])
R.run()
def strip(tag, views, title):
    ims = [R.img(tag, v[0]).resize((520, 520)) for v in views]; W_ = 520 * len(ims); M = Image.new('RGB', (W_, 560), 'white'); ImageDraw.Draw(M).text((10, 8), title, fill=(0, 0, 0))
    for i, im in enumerate(ims): M.paste(im, (520 * i, 40))
    M.save(OUT + '/%s.jpg' % tag, quality=88)
for j in jobs: strip(j[0], j[4], '%s  SA_M_REF_RP5_pilot_v001 (c1 SA-M188 working source) -- PILOT / NOT FROZEN' % j[0])
print('boards', len(jobs))
