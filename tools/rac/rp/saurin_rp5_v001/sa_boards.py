# sa_boards.py : RP5 Saurin pilot boards (order 53976fb §21) -- neutral clay workbench renders (sa_render / RP4 machinery), matched cameras per board.
# Canonical sources render from the full-resolution base where cropped (head / hands / feet / tail / thigh / surfaced closeups) and from a 150 k-triangle
# decimation for whole-body views. The QuadriFlow scaffold is labelled DIAGNOSTIC everywhere (never the production topology).
import sys, os, json, numpy as np, igl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_render as R
W = '/tmp/claude-0/rt/sa'; L = json.load(open(W + '/lm/SA-M188_landmarks.json'))['landmarks']; g = lambda k: np.array(L[k]['p_cm'])
b = np.load(W + '/src/saurin_w2_final_base.npz'); VM = b['v'].astype(float); F = b['f'].astype(np.int64); VF = np.load(W + '/src/saurin_w2_SA-F188_realization.npz')['v'].astype(float)
dec = np.load(W + '/an/base_dec.npz'); VD, FD = dec['V'], dec['F']
S = np.load(W + '/src/SA-M188_surfaced.npz'); VS = S['v'].astype(float); FS = S['f'].astype(np.int64)
lab = np.load(W + '/lm/SA-M188_regions.npz')['label']
sc = np.load(W + '/scaf/scaffold_120k.npz'); VQ, QQ = sc['V'], sc['Q']
tm = np.load(W + '/tail/SA_tail_module.npz'); VT, QT = tm['V'], tm['Q']; fi, BC = tm['tri'], tm['bc']; VTF = (BC[:, :, None] * VF[F[fi]]).sum(1)
def crop(V, Fc, c, r):
    m = np.all(np.linalg.norm(V[Fc] - c, axis=2) < r, axis=1); Fk = Fc[m]; u = np.unique(Fk); mp = -np.ones(len(V), int); mp[u] = np.arange(len(u)); return V[u], mp[Fk]
C0 = np.array([0, -50, 95.0]); BODY = [('front', (0, 1, 0.02), C0, 200), ('tqf', (1, 1, 0.1), C0, 200), ('side', (1, 0, 0.02), C0, 200), ('rear', (0, -1, 0.02), C0, 200)]
GREY = np.array(R.GREY, float)
# A sources
R.job('A_M', VD, FD, None, BODY); dF = igl.decimate(VF, F, 150000); R.job('A_F', [x for x in dF if isinstance(x, np.ndarray) and x.ndim == 2][0], [x for x in dF if isinstance(x, np.ndarray) and x.ndim == 2][1], None, BODY)
hc = g('eye_xpos') * [0, 1, 1] + np.array([0, -2, -1.0])
for tag, V_, F_ in (('base', VM, F), ('surf', VS, FS)):
    Vh, Fh = crop(V_, F_, hc, 16); R.job('A_head_' + tag, Vh, Fh, None, [('h', (0.6, 1, 0.15), hc, 22)], px=700)
    fc = np.array([-16.0, 2.0, 112.0]); Vf, Ff = crop(V_, F_, fc, 12); R.job('A_flank_' + tag, Vf, Ff, None, [('f', (-1, 0.3, 0.1), fc, 14)], px=700)
    tc = g('tail_chain_06'); Vt, Ft = crop(V_, F_, tc, 14); R.job('A_tail_' + tag, Vt, Ft, None, [('t', (1, 0.1, 0.5), tc, 16)], px=700)
# B topology overview: scaffold (diagnostic) + tail module on the base
R.job('B_scaf', VQ, QQ, None, [('front', (0, 1, 0.02), C0, 200), ('side', (1, 0, 0.02), C0, 200), ('rear', (0, -1, 0.02), C0, 200)], wire=True, px=900)
nv = len(VT); E = np.unique(np.sort(np.r_[QT[:, [0, 1]], QT[:, [1, 2]], QT[:, [2, 3]], QT[:, [3, 0]]], 1), axis=0); val = np.bincount(E.ravel(), minlength=nv)
colp = np.tile(GREY, (nv, 1)); colp[val == 3] = [0.15, 0.6, 0.2]; colp[val >= 5] = [0.85, 0.15, 0.1]
el = np.zeros(nv); np.maximum.at(el, E[:, 0], np.linalg.norm(VT[E[:, 0]] - VT[E[:, 1]], axis=1)); hcol = np.clip(el / 1.13, 0, 1)
cold = np.c_[0.2 + 0.7 * hcol, 0.7 - 0.4 * hcol, 0.9 - 0.7 * hcol]
TV = [('side', (1, 0, 0.05), np.array([0, -60, 95.0]), 95), ('top', (0, 0.01, 1), np.array([0, -60, 95.0]), 95), ('under', (0, 0.01, -1), np.array([0, -60, 95.0]), 95)]
R.job('B_tm_poles', VT, QT, colp, TV, wire=True, px=900); R.job('B_tm_dens', VT, QT, cold, TV, wire=False, px=900)
# C head (source wire, scaffold wire), D root, E tail arcs, F hands, G feet
HV = [('front', (0, 1, 0.05), hc, 24), ('tqf', (0.8, 1, 0.1), hc, 24), ('prof', (1, 0, 0.02), hc, 24), ('under', (0.2, 0.6, -1), hc, 24)]
Vh, Fh = crop(VD, FD, hc, 18); R.job('C_src', Vh, Fh, None, HV, wire=True, px=700); Vh2, Qh2 = crop(VQ, QQ, hc, 18); R.job('C_scaf', Vh2, Qh2, None, HV, wire=True, px=700)
rc = g('tail_root_centre'); RV = [('side', (1, 0, 0.1), rc + [0, -8, 0], 40), ('rear', (0.2, -1, 0.3), rc + [0, -8, 0], 40), ('under', (0.2, -0.3, -1), rc + [0, -8, 0], 40)]
Vb, Fb = crop(VD, FD, rc, 45); R.job('D_base', Vb, Fb, None, RV); R.job('D_tm', VT, QT, None, RV, wire=True, px=800)
arc = {k: g('tail_chain_%02d' % k) for k in (4, 8, 12, 16)}
for k, c in arc.items(): R.job('E_tm_%d' % k, VT, QT, None, [('c', (1, 0.15, 0.6), c, 14 if k < 12 else 7)], wire=True, px=700)
R.job('E_tm_root', VT, QT, None, [('c', (0.8, -0.6, 0.5), rc + [0, -4, -2], 30)], wire=True, px=700)
for s, sg in (('xneg', -1),):
    hcen = 0.5 * (g('wrist_' + s) + g('hand_tip1_' + s)); HN = [('palm', (-sg, 0.2, 0), hcen, 18), ('dors', (sg, 0.2, 0), hcen, 18), ('side', (0, 1, 0.1), hcen, 18)]
    Vh, Fh = crop(VM, F, hcen, 14); R.job('F_src', Vh, Fh, None, HN, px=700); Vq, Qq = crop(VQ, QQ, hcen, 14); R.job('F_scaf', Vq, Qq, None, HN, wire=True, px=700)
    fcen = g('ankle_' + s) + np.array([0, 9.0, -6.0]); FN = [('plant', (0, 0.2, -1), fcen, 26), ('dors', (0, 0.3, 1), fcen, 26), ('prof', (1, 0, 0.1), fcen, 26)]
    Vf, Ff = crop(VM, F, fcen, 18); R.job('G_src', Vf, Ff, None, FN, px=700); Vq, Qq = crop(VQ, QQ, fcen, 18); R.job('G_scaf', Vq, Qq, None, FN, wire=True, px=700)
# H c1 / c2: tail module on both + full body side
R.job('H_tm_M', VT, QT, None, TV[:1] + [('rear', (0.3, -1, 0.3), rc + [0, -10, 0], 45)], wire=True, px=800); R.job('H_tm_F', VTF, QT, None, TV[:1] + [('rear', (0.3, -1, 0.3), rc + [0, -10, 0], 45)], wire=True, px=800)
# I deviation heat (source tail -> module distance on the base vertices of the covered region)
sub = tm['sub']; phi = tm['phi']; cov = sub[phi > 0.003]; TC = np.r_[QT[:, [0, 1, 2]], QT[:, [0, 2, 3]]]
for tag, VV, VC in (('M', VM, VT), ('F', VF, VTF)):
    d = np.sqrt(igl.point_mesh_squared_distance(VV[cov], VC, TC)[0]) * 10; Vc_, Fc_ = crop(VV, F, rc + [0, -50, -5], 95)
    col = np.tile(GREY, (len(VV), 1)); t = np.clip(d / 0.8, 0, 1); col[cov] = np.c_[0.25 + 0.7 * t, 0.75 - 0.5 * t, 0.85 - 0.7 * t]
    keep = np.all(np.isin(F, cov), 1); Fk = F[keep]; u = np.unique(Fk); mp = -np.ones(len(VV), int); mp[u] = np.arange(len(u))
    R.job('I_' + tag, VV[u], mp[Fk], col[u], TV, px=800)
# J thigh relief
for bid, VV in (('SA-M188', VM), ('SA-F188', VF)):
    z = np.load(W + '/thigh/%s_thigh_relief.npz' % bid); sb = z['sub']; rel = z['rel']; Fs = z['Fs']; Vs = VV[sb]
    t = np.clip(rel / 0.4, -1, 1); col = np.c_[0.6 + 0.35 * t, 0.6 - 0.25 * np.abs(t), 0.6 - 0.35 * t]
    for s, sg in (('l', 1), ('r', -1)):
        c = np.array([sg * 12.0, -6.0, 75.0]); R.job('J_%s_%s' % (bid, s), Vs, Fs, col, [('med', (-sg, -0.6, 0.05), c, 26), ('post', (0.15 * sg, -1, 0.05), c, 26)], px=700)
# L tail deformation (module)
for kind in ('root_lateral_30', 'root_vertical_25', 'mid_lateral_40', 'twist_30'):
    p = np.load(W + '/tail/pose_%s.npz' % kind); R.job('L_' + kind, p['V'], p['Q'], None, [('side', (1, 0, 0.1), np.array([0, -60, 95.0]), 100), ('top', (0, 0.01, 1), np.array([0, -60, 95.0]), 100)], wire=True, px=800)
print('jobs', len(R.jobs), flush=True); R.run(2)
S_ = R.sheet; I_ = R.img
S_('SA_A_canonical_sources.jpg', 'A. Canonical W2I6 sources (verified): SA-M188 base | SA-F188 (§263 centre) whole body with tail; full-resolution closeups unsurfaced base vs canonical surfaced organism',
   [('SA-M188 base', [I_('A_M', v) for v in ('front', 'tqf', 'side', 'rear')]), ('SA-F188', [I_('A_F', v) for v in ('front', 'tqf', 'side', 'rear')]),
    ('base closeups', [I_('A_head_base', 'h'), I_('A_flank_base', 'f'), I_('A_tail_base', 't'), I_('A_M', 'side')]), ('surfaced closeups', [I_('A_head_surf', 'h'), I_('A_flank_surf', 'f'), I_('A_tail_surf', 't'), I_('A_F', 'side')])],
   ['front / head', 'front 3/4 / flank', 'profile / tail', 'rear / profile'], colw=330)
S_('SA_B_topology_overview.jpg', 'B. Topology overview: QuadriFlow full-body scaffold (DIAGNOSTIC ONLY, not production topology) | authored tail module: pole map (green = valence 3, red = valence 5+; poles on the 2:1 rows only) and edge-length map (blue short -> amber 1.13 cm ceiling)',
   [('scaffold (diagnostic)', [I_('B_scaf', v) for v in ('front', 'side', 'rear')]), ('tail module poles', [I_('B_tm_poles', v) for v in ('side', 'top', 'under')]), ('tail module density', [I_('B_tm_dens', v) for v in ('side', 'top', 'under')])],
   ['view 1', 'view 2', 'view 3'], colw=420)
S_('SA_C_head_rostrum.jpg', 'C. Head / rostrum: canonical source wire (decimated) vs the QuadriFlow scaffold (DIAGNOSTIC): no orbit / mouth / jaw-hinge / ridge loop structure emerges automatically -- the head system must be authored',
   [('source', [I_('C_src', v) for v in ('front', 'tqf', 'prof', 'under')]), ('scaffold (diag.)', [I_('C_scaf', v) for v in ('front', 'tqf', 'prof', 'under')])], ['front', '3/4', 'profile', 'underside'], colw=330)
S_('SA_D_pelvis_tail_root.jpg', 'D. Pelvis / tail root: canonical source vs authored tail module (root loop 2 cm caudal of the anatomical root plane; geodesic root rings wrap the posterior pelvis)',
   [('source', [I_('D_base', v) for v in ('side', 'rear', 'under')]), ('tail module', [I_('D_tm', v) for v in ('side', 'rear', 'under')])], ['side', 'rear', 'underside'], colw=420)
S_('SA_E_tail.jpg', 'E. Tail module: root, 25 / 50 / 75 % arc (chain points 4 / 8 / 12) and terminal ring system (chain 16 -> tip cap); ring spacing = ring edge length',
   [('tail module', [I_('E_tm_root', 'c'), I_('E_tm_4', 'c'), I_('E_tm_8', 'c'), I_('E_tm_12', 'c'), I_('E_tm_16', 'c')])], ['root', '25 %', '50 %', '75 %', 'tip'], colw=360)
S_('SA_F_hands.jpg', 'F. Hand / claws (x- side): canonical source (full resolution) vs QuadriFlow scaffold (DIAGNOSTIC): the remesher erodes claws and digit separation -- hands must be authored digit by digit',
   [('source', [I_('F_src', v) for v in ('palm', 'dors', 'side')]), ('scaffold (diag.)', [I_('F_scaf', v) for v in ('palm', 'dors', 'side')])], ['palm', 'dorsal', 'side'], colw=380)
S_('SA_G_feet.jpg', 'G. Foot / claws (x- side): canonical source vs QuadriFlow scaffold (DIAGNOSTIC)',
   [('source', [I_('G_src', v) for v in ('plant', 'dors', 'prof')]), ('scaffold (diag.)', [I_('G_scaf', v) for v in ('plant', 'dors', 'prof')])], ['plantar', 'dorsal', 'profile'], colw=380)
S_('SA_H_c1_c2.jpg', 'H. c1 / c2 shared topology: the SAME tail-module face list realized on SA-M188 and SA-F188 through the shared base face list (identical cameras)',
   [('SA-M188', [I_('H_tm_M', v) for v in ('side', 'rear')]), ('SA-F188', [I_('H_tm_F', v) for v in ('side', 'rear')])], ['side', 'root (rear)'], colw=480)
S_('SA_I_source_deviation.jpg', 'I. Source -> tail-module deviation on the canonical base (blue 0 -> red >= 0.8 mm = T-2 p95 limit): SA-M188 | SA-F188',
   [('SA-M188', [I_('I_M', v) for v in ('side', 'top', 'under')]), ('SA-F188', [I_('I_F', v) for v in ('side', 'top', 'under')])], ['side', 'top', 'underside'], colw=420)
S_('SA_J_thigh_artdebt.jpg', 'J. Deferred medial / posterior thigh art debt: 1.5 cm high-pass relief of the canonical base (red raised / blue recessed, +-4 mm) -- medial and posterior views, both sides, SA-M188 | SA-F188',
   [('%s %s' % (bid, s), [I_('J_%s_%s' % (bid, s), v) for v in ('med', 'post')]) for bid in ('SA-M188', 'SA-F188') for s in ('l', 'r')], ['medial', 'posterior'], colw=420)
S_('SA_K_surface_representation.jpg', 'K. Surface representation: unsurfaced base (what the production cage carries) vs canonical surfaced organism (fine scale relief <= 1.7 mm, normal-only) -- matched closeups',
   [('base (cage target)', [I_('A_head_base', 'h'), I_('A_flank_base', 'f'), I_('A_tail_base', 't')]), ('surfaced (detail layer)', [I_('A_head_surf', 'h'), I_('A_flank_surf', 'f'), I_('A_tail_surf', 't')])],
   ['head', 'flank', 'tail'], colw=420)
S_('SA_L_tail_deformation.jpg', 'L. Diagnostic tail deformation on the authored module (temporary 18-joint chain LBS): root lateral 30 / root vertical 25 / mid-tail lateral 40 / twist 30 deg',
   [(k, [I_('L_' + k, v) for v in ('side', 'top')]) for k in ('root_lateral_30', 'root_vertical_25', 'mid_lateral_40', 'twist_30')], ['side', 'top'], colw=480)
print('SABOARDS', sorted(os.listdir(R._OUT)))
