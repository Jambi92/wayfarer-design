# defect breakdown (folds / pen / tears / pleats) of a bake checkpoint at hip_flex70_xpos fractions
import sys, os, json, numpy as np
T_ = '/home/claude/wayfarer-design/tools/rac/rp/saurin_rp6_v001'; sys.path.insert(0, T_)
import sa6_bake as SB
import sa6_common as C, sa6_correctives as CC, sa6_fit as FT, sa6_pd2_fit as PF, sa6_layer_harness as H, sa6_blend as BL
nm, BD, ck = sys.argv[1:4]; b = json.load(open(os.path.join(BD, 'bodies.json')))['bodies'][nm]
R, z = BL.rig_of(nm, b, BD); R.rest_inverted = z['rest_inverted']; PF.mask_composition(R, z['comp'])
Bc = H.load_base(R, b['cfg']); P0 = H.Blend(Bc, [(w, H.load_state(R, s)[0]) for s, w in b['w'].items()])
K = CC.Correctives.load(R, ck); P = SB.BakeProxy(P0, K); Sv = CC.Solver(R); Sv.V0 = Sv.body_volume(R.V)
F = np.r_[R.Q[:, [0, 1, 2]], R.Q[:, [0, 2, 3]]].astype(np.int64); w0 = FT.wn_out(R.V, F); PS = R.suite('anat')
pn = 'hip_flex70_xpos'
for fr in [float(x) for x in sys.argv[4].split(',')]:
    spec = [(bb, p, a, dg * fr) for bb, p, a, dg in PS[pn]]; T = R.pose(spec); Pc = R.skin(T, R.V + P.delta(T))
    fo = int((R.relcos(Pc, T) < 0).sum()); pe = int(FT.penetration(R, Pc, F, w0).sum()); te = Sv.tear_edges(Pc)[0]; pl = Sv.pleat_edges(Pc)
    print('%.4f folds %d pen %d tear+pleat %d pleat %d' % (fr, fo, pe, int(te.sum()), int(np.asarray(pl).sum())), flush=True)
