# sa6_pd2.py OUT.json W_M.npz CF_M.json : RP6 re-check of the 19 accepted PD-2 creator states (order a407015 §18) under the RP6 rig assumptions.
#   Each state = an accepted dense creator-composition body (canonical W2I6 face list, rebuilt clean workspace cr_<STATE>.npy); the frozen cage is realised on
#   it through the frozen barycentric embedding (no topology / geometry change).  Step A (pre-rig, = RP5 PD-2): neutral state cage flips vs the rest cage and
#   dense-source folds (normal flip vs the canonical base, or area < 5 %).  Step B (rig): the RP6 skeleton definitions re-evaluated on the state (landmark
#   joints via the same affine transfer as c2), the c1 production weights + c1 correctives on the shared topology (RP6 assumption for creator states: one
#   weight / corrective set per base configuration, carried by topology), the full anatomical 34-pose suite at full angle.
#   Ownership per pose: flips located over (<= 1 cm from) a pre-rig source fold of the state, or over a state-neutral cage flip = COMPOSITION/PD-2; other
#   flips = rig-owned on this state; compared with the same pose on c1 (REGRESSION = rig-owned flips on the state where c1 has 0).
import sys, os, json, glob, time, numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sa6_common as C, sa6_pose as SP, sa6_correctives as CC, sa6_skeleton as SK, sa6_fit as FT
OUT, WF, CF = sys.argv[1:4]
d = C.load(); z = np.load(C.FZ + '/SA_RP5_full_cage_freeze_candidate_v001.npz'); w = np.load(C.W + '/work/SA_RP5_WORK_v001.npz'); F = w['f'].astype(np.int64)
VR = np.load(C.W + '/src/saurin_w2_final_base.npz'); VR = VR[[k for k in VR.files if VR[k].shape == w['v_M'].shape][0]].astype(float) if os.path.exists(C.W + '/src/saurin_w2_final_base.npz') else w['v_M'].astype(float)
def fn(P): return np.cross(P[F[:, 1]] - P[F[:, 0]], P[F[:, 2]] - P[F[:, 0]])
nR = fn(VR); aR = np.linalg.norm(nR, axis=1); P0 = (z['bc'][:, :, None] * VR[F[z['tri']]]).sum(1)
R0 = SP.Rig('M', WF); Cr = CC.Correctives.load(R0, CF); A = R0.suite('anat')
base = {}
for pn, spec in A.items():
    T = R0.pose(spec); P = R0.skin(T, R0.V + Cr.delta(T)); base[pn] = int((R0.relcos(P, T) < 0).sum())
res = dict(status='RP6 RIG PILOT / NOT FROZEN', method=open(__file__).read().split('import')[0], c1_reference_flips=base, states={})
for path in sorted(glob.glob(C.W + '/cr_*.npy')):
    nm = os.path.basename(path)[3:-4]; t0 = time.time(); VB = np.load(path).astype(float); nB = fn(VB); aB = np.linalg.norm(nB, axis=1)
    bad = ((nR * nB).sum(1) / (aR * aB + 1e-20) < 0) | (aB < 0.05 * aR); Vs = (z['bc'][:, :, None] * VB[F[z['tri']]]).sum(1)
    q0 = np.cross(P0[R0.Q[:, 2]] - P0[R0.Q[:, 0]], P0[R0.Q[:, 3]] - P0[R0.Q[:, 1]]); q1 = np.cross(Vs[R0.Q[:, 2]] - Vs[R0.Q[:, 0]], Vs[R0.Q[:, 3]] - Vs[R0.Q[:, 1]])
    nflip = np.nonzero((q0 * q1).sum(1) < 0)[0]
    pts = np.r_[VB[F[bad]].mean(1) if bad.any() else np.zeros((0, 3)), Vs[R0.Q[nflip]].mean(1) if len(nflip) else np.zeros((0, 3))]; kd = cKDTree(pts) if len(pts) else None
    J, M = SK.build(Vs, 'state'); Pst = SK.rec(J, M, 'creator state ' + nm)
    R = SP.Rig('M', WF); R.V = Vs; R.P = Pst; R.n0 = R.qn(Vs); R.cfg = 'state'; Cs = CC.Correctives.load(R, CF); S = R.suite('anat')
    st = dict(prerig_source_folds=int(bad.sum()), prerig_neutral_cage_flips=int(len(nflip)), poses={})
    tot_rig = 0; regress = []
    for pn, spec in S.items():
        T = R.pose(spec); P = R.skin(T, R.V + Cs.delta(T)); f = np.nonzero(R.relcos(P, T) < 0)[0]
        if len(f) and kd is not None: dd, _ = kd.query(Vs[R.Q[f]].mean(1)); comp = int((dd <= 1.0).sum())
        else: comp = 0
        rig = int(len(f) - comp); tot_rig += rig
        if rig and base[pn] == 0: regress.append(pn)
        st['poses'][pn] = dict(flips=int(len(f)), composition_pd2=comp, rig_owned=rig, regions=sorted({str(R.ql[q]) for q in f})[:6])
    st.update(rig_owned_total=tot_rig, regressions_vs_c1=regress, owner=('CLEAN' if tot_rig == 0 else 'RIG-OWNED FLIPS ON THIS STATE'))
    res['states'][nm] = st; print(nm, 'prerig folds', int(bad.sum()), 'neutral cage flips', len(nflip), '| rig-owned', tot_rig, 'regress', regress[:6], '%.0fs' % (time.time() - t0), flush=True)
json.dump(res, open(OUT, 'w'), indent=1)
