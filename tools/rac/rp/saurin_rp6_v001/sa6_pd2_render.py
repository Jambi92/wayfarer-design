# sa6_pd2_render.py PD2.json LAYERDIR OUTDIR : visual evidence for the PD-2 creator-state re-check (closure order 58aa486c §2).
#   Per inspected state (known extremes + every state whose base column had rig-owned folds): [neutral state, pre-rig composition folds marked]
#   [worst pose with base correctives only = BEFORE, folded quads red, view centred on the folds] [same pose with base + creator-state layer = production].
#   Uses the same draw routine as sa6_render (extracted from its source, not re-implemented) and the same evaluator as sa6_pd2.
import sys, os, ast, json, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection, LineCollection
from scipy.spatial import cKDTree
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sa6_common as C, sa6_correctives as CC, sa6_fit as FT, sa6_pd2_fit as PF
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sa6_render.py')).read()
exec(compile(ast.Module([n for n in ast.parse(src).body if isinstance(n, ast.FunctionDef) and n.name in ('view_basis', 'draw')], []), 'sa6_render', 'exec'))
PD, LD, OD = sys.argv[1:4]; os.makedirs(OD, exist_ok=True); pd = json.load(open(PD))['states']
d = C.load(); F = PF.Fd; z = PF.z
VR = np.load(C.W + '/src/saurin_w2_final_base.npz'); VR = VR[[k for k in VR.files if VR[k].shape == PF.w['v_M'].shape][0]].astype(float)
def fn(P): return np.cross(P[F[:, 1]] - P[F[:, 0]], P[F[:, 2]] - P[F[:, 0]])
nR = fn(VR); aR = np.linalg.norm(nR, axis=1)
EXTREMES = ['FAHI', 'MUHI', 'MUFAHI', 'NAR', 'BRD', 'M208-B', 'MIN', 'F-N', 'T55']
names = [s for s in EXTREMES if s in pd] + [s for s in pd if s not in EXTREMES and any(r['base_rig_flips'] for r in pd[s]['poses'].values())]
for nm in names:
    st = pd[nm]; R, cfg = PF.state_rig(nm); Cb = CC.Correctives.load(R, PF.WD + '/CF_%s.json' % cfg); Cp = CC.Correctives.load(R, LD + '/CF_state_%s.json' % nm)
    VB = np.load(C.W + '/cr_%s.npy' % nm).astype(float); nB = fn(VB); aB = np.linalg.norm(nB, axis=1)
    bad = ((nR * nB).sum(1) / (aR * aB + 1e-20) < 0) | (aB < 0.05 * aR); comp = np.zeros(len(R.Q), bool)
    if bad.any(): comp = cKDTree(VB[F[bad]].mean(1)).query(R.V[R.Q].mean(1))[0] <= 1.0
    pn = max(st['poses'], key=lambda p: (st['poses'][p]['base_rig_flips'], st['poses'][p]['base_flips'])); spec = R.suite('anat')[pn]; T = R.pose(spec)
    Pb = R.skin(T, R.V + Cb.delta(T)); Pp = R.skin(T, R.V + Cp.delta(T)); fb = np.nonzero(R.relcos(Pb, T) < 0)[0]; fp = np.nonzero(R.relcos(Pp, T) < 0)[0]
    foc = fb if len(fb) else (fp if len(fp) else None)
    ctr = Pb[R.Q[foc]].mean((0, 1)) if foc is not None else Pb.mean(0); rad = (40.0 if pn.startswith('tail') else 22.0) if foc is not None else None
    lat = ctr - Pb.mean(0); lat[2] = 0; view = (np.sign(lat[0]) or 1.0, 0.35, 0.25) if abs(lat[0]) > abs(lat[1]) else (0.25, np.sign(lat[1]) or 1.0, 0.25)
    if pn.startswith('tail'): view = (1.0, -0.45, 0.3)
    f, ax = plt.subplots(1, 3, figsize=(13, 4.6))
    draw(ax[0], R, R.V, (0, 1, 0), flips=np.nonzero(comp)[0], title='%s neutral (base %s) | pre-rig composition folds (red): src %d tris, cage flips %d' % (
        nm, 'c1' if cfg == 'M' else 'c2', st['prerig']['source_folds_union'], st['prerig']['neutral_cage_flips']))
    draw(ax[1], R, Pb, view, ctr, rad, flips=fb, title='%s %s BEFORE (base correctives) | folds %d (rig-owned %d)' % (nm, pn, len(fb), st['poses'][pn]['base_rig_flips']))
    draw(ax[2], R, Pp, view, ctr, rad, flips=fp, title='%s %s PRODUCTION (base + state layer) | folds %d (rig-owned %d)' % (nm, pn, len(fp), st['poses'][pn]['rig_owned']))
    plt.tight_layout(); fo = os.path.join(OD, 'SA_RP6_pd2_%s.png' % nm.replace('+', 'p').replace('.', '_')); f.savefig(fo, dpi=100); plt.close(f); print('wrote', fo, pn, len(fb), len(fp), flush=True)
